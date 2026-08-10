#!/usr/bin/env python3
"""Resuelve y descarga las fuentes del apéndice A que están en acceso abierto.

El corpus cita 523 fuentes y de muchas sólo se pudo leer el resumen. Este script
busca cuáles de ellas son legalmente accesibles y trae el PDF.

**Qué hace y qué no.** Pregunta por cada DOI a cinco catálogos abiertos
—OpenAlex, Unpaywall, Europe PMC, arXiv y OpenAIRE, más CORE si se da su clave—
y descarga únicamente lo que esos catálogos declaran abierto. No accede a repositorios
piratas, no sortea muros de pago y no toca las fuentes cerradas: esas se listan
en el informe como lo que son, un hueco declarado.

**El informe importa tanto como los PDF.** `exports/acceso_fuentes.csv` deja por
escrito, fuente a fuente, si hay versión abierta, por qué vía, y si no la hay,
la razón. Una fuente que no se pudo obtener nunca desaparece en silencio: ése es
el mismo principio que gobierna las búsquedas negativas del corpus.

**Los PDF no se versionan.** Van a `fuentes_pdf/`, que está en .gitignore. Sus
licencias son heterogéneas —«bronze» significa legible en la web del editor,
sin licencia abierta explícita— y mezclarlos con un repositorio CC BY 4.0
rompería la frontera de licencias del proyecto.

Uso:
    python3 scripts/fetch_oa.py --mailto tu@correo            # resolver y descargar
    python3 scripts/fetch_oa.py --mailto tu@correo --solo-informe
    python3 scripts/fetch_oa.py --mailto tu@correo --limite 20
    python3 scripts/fetch_oa.py --mailto tu@correo --core-key CLAVE
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APENDICE_A = ROOT / "data" / "apendices" / "A_fuentes.csv"
INFORME = ROOT / "exports" / "acceso_fuentes.csv"
LISTADO = ROOT / "docs" / "FUENTES-SIN-ACCESO.md"
DESTINO = ROOT / "fuentes_pdf"
# La resolución cuesta cientos de consultas; se guarda junto a los PDF, que
# también están fuera del control de versiones.
CACHE = DESTINO / ".resolucion.json"
# Cada cuántas fuentes se vuelca lo hecho. Una pasada completa son horas: si
# se interrumpe, lo trabajado hasta ese punto tiene que quedar en disco.
CHECKPOINT = 10

OPENALEX = "https://api.openalex.org/works"
EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
LOTE = 50  # tope de la API de OpenAlex por consulta

# Identificarse es la norma de cortesía de estas APIs y da acceso al «polite
# pool», más estable. La pausa entre descargas evita castigar a los servidores
# de los editores, que ceden estos PDF de buena fe.
AGENTE = "corredor-eukaryota-holozoa/fetch_oa (+https://github.com/santiqwerty1/corredor-eukaryota-holozoa)"
PAUSA_API = 0.3
PAUSA_DESCARGA = 1.0

CABECERA_INFORME = [
    "clave", "año", "título", "doi", "acceso", "vía", "url_pdf",
    "fichero", "resultado", "detalle",
]


def _pedir(url: str, timeout: int = 40, binario: bool = False):
    req = urllib.request.Request(url, headers={
        "User-Agent": AGENTE,
        "Accept": "application/pdf,*/*" if binario else "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binario else json.load(r)


def leer_apendice_a() -> list[dict]:
    """Las fuentes tal como las declara el corpus. No se modifica nada aquí."""
    with APENDICE_A.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.reader(fh))
    cab, cuerpo = filas[0], filas[1:]
    idx = {n: i for i, n in enumerate(cab)}
    col_doi = next(i for n, i in idx.items() if n.startswith("DOI"))
    fuentes = []
    for f in cuerpo:
        if not f or not f[0].strip():
            continue
        bruto = f[col_doi] if len(f) > col_doi else ""
        m = re.search(r"10\.\d{4,9}/\S+", bruto or "")
        fuentes.append({
            "clave": f[0].strip(),
            "año": f[2].strip() if len(f) > 2 else "",
            "titulo": f[3].strip() if len(f) > 3 else "",
            "doi": m.group(0).rstrip(".").lower() if m else "",
            "url": (bruto or "").strip(),
            "autores": f[1].strip() if len(f) > 1 else "",
            "publicacion": f[4].strip() if len(f) > 4 else "",
        })
    return fuentes


def resolver_openalex(dois: list[str], mailto: str) -> dict[str, dict]:
    """Pregunta a OpenAlex, en lotes, si cada DOI tiene versión abierta."""
    hallado: dict[str, dict] = {}
    for i in range(0, len(dois), LOTE):
        trozo = dois[i:i + LOTE]
        filtro = "doi:" + "|".join("https://doi.org/" + d for d in trozo)
        url = (f"{OPENALEX}?per-page={LOTE}&mailto={urllib.parse.quote(mailto)}"
               "&select=doi,open_access,best_oa_location,publication_year"
               "&filter=" + urllib.parse.quote(filtro, safe=":|/.-"))
        try:
            datos = _pedir(url)
        except Exception as exc:                      # noqa: BLE001
            print(f"  aviso: lote {i // LOTE + 1} no resuelto ({exc})", file=sys.stderr)
            time.sleep(PAUSA_API)
            continue
        for w in datos.get("results", []):
            clave = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            oa = w.get("open_access") or {}
            loc = w.get("best_oa_location") or {}
            hallado[clave] = {
                "abierto": bool(oa.get("is_oa")),
                "estado": oa.get("oa_status") or "",
                "pdf": loc.get("pdf_url") or oa.get("oa_url") or "",
                "via": "openalex",
            }
        print(f"  lote {i // LOTE + 1}/{(len(dois) + LOTE - 1) // LOTE} · "
              f"{len(hallado)} resueltos", file=sys.stderr)
        time.sleep(PAUSA_API)
    return hallado


def resolver_europepmc(doi: str) -> dict | None:
    """Segunda oportunidad: Europe PMC indexa textos completos que OpenAlex a
    veces no enlaza, sobre todo en ciencias de la vida —justo este corpus."""
    url = (f"{EUROPEPMC}?query={urllib.parse.quote(f'DOI:{doi}')}"
           "&format=json&pageSize=1&resultType=core")
    try:
        datos = _pedir(url, timeout=25)
    except Exception:                                  # noqa: BLE001
        return None
    res = (datos.get("resultList") or {}).get("result") or []
    if not res:
        return None
    r = res[0]
    if r.get("isOpenAccess") != "Y":
        return None
    pmcid = r.get("pmcid")
    if not pmcid:
        return None
    return {
        "abierto": True,
        "estado": "open (europepmc)",
        "pdf": f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextPDF",
        "via": "europepmc",
    }


# Qué anfitriones sirven el fichero y cuáles devuelven una página. Medido sobre
# las fuentes que fallaron: europepmc sirvió el 100 % de sus intentos, mientras
# que las webs de editor devuelven 403 y los repositorios, la ficha del depósito.
# El orden de intento sale de aquí, no de qué catálogo dio el enlace.
PREFERENCIA_ANFITRION = [
    (("europepmc.org", "ncbi.nlm.nih.gov/pmc", "pmc.ncbi.nlm.nih.gov"), 0),
    (("arxiv.org", "biorxiv.org", "zenodo.org", "osf.io"), 1),
    ((".edu", ".ac.", "pure.", "repository", "repositorio", "dspace", "hal."), 2),
]
EDITORES = ("wiley.com", "oup.com", "sciencedirect", "springer", "nature.com",
            "tandfonline", "cell.com", "pnas.org", "sagepub", "cambridge.org")


def orden_anfitrion(url: str) -> int:
    u = url.lower()
    for claves, peso in PREFERENCIA_ANFITRION:
        if any(k in u for k in claves):
            return peso
    if any(e in u for e in EDITORES):
        return 9          # casi siempre 403 para un cliente automático
    return 5


def candidatos_semanticscholar(doi: str) -> list[tuple[str, str]]:
    """Semantic Scholar mantiene su propio índice de PDF abiertos.

    Es el que más aporta con diferencia: en la muestra de diagnóstico encontró
    enlace para las seis fuentes que habían fallado por todas las demás vías.
    """
    try:
        d = _pedir("https://api.semanticscholar.org/graph/v1/paper/DOI:"
                   + urllib.parse.quote(doi) + "?fields=openAccessPdf", timeout=25)
    except Exception:                                  # noqa: BLE001
        return []
    u = (d.get("openAccessPdf") or {}).get("url")
    return [(u, "semanticscholar")] if u else []


def candidatos_crossref(doi: str) -> list[tuple[str, str]]:
    """Crossref publica los enlaces que los editores declaran para minería de
    texto. Son la vía que el propio editor ofrece a las herramientas."""
    try:
        d = _pedir("https://api.crossref.org/works/" + urllib.parse.quote(doi), timeout=25)
    except Exception:                                  # noqa: BLE001
        return []
    return [(l["URL"], "crossref/tdm")
            for l in (d.get("message", {}).get("link") or [])
            if l.get("URL") and "pdf" in (l.get("content-type") or "").lower()]


def candidatos_de_pagina(html: bytes, base: str) -> list[tuple[str, str]]:
    """`citation_pdf_url` de la página que se recibió en vez del artículo.

    Las páginas de artículo llevan esa etiqueta justamente para que las
    herramientas encuentren el fichero; Google Scholar se apoya en ella. Como el
    HTML ya está descargado, extraerla no cuesta una petición más.
    """
    try:
        txt = html[:400_000].decode("utf-8", "replace")
    except Exception:                                  # noqa: BLE001
        return []
    pats = [r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url']
    for pat in pats:
        m = re.search(pat, txt, re.I)
        if m:
            return [(urllib.parse.urljoin(base, m.group(1)), "citation_pdf_url")]
    # Sin la etiqueta, los enlaces a fichero de la propia página. Varios
    # repositorios Pure no declaran citation_pdf_url y cuelgan el PDF de un
    # /files/ corriente. Se limita a tres para no convertir esto en un rastreo.
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', txt, re.I)
    fich = [urllib.parse.urljoin(base, h) for h in dict.fromkeys(hrefs)
            if h.lower().endswith(".pdf") or "/files/" in h.lower()]
    return [(u, "enlace-de-la-pagina") for u in fich[:3]]


def candidatos_unpaywall(doi: str, mailto: str) -> list[tuple[str, str]]:
    """Unpaywall conoce depósitos que OpenAlex no enlaza.

    Verificado: para 10.1038/nature14447 OpenAlex no ofrecía ninguna ubicación
    con PDF y Unpaywall lo encontró en el repositorio de Wageningen. Los
    repositorios van primero: sirven el fichero sin negociar con un editor que
    a menudo rechaza a los clientes automáticos.
    """
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={urllib.parse.quote(mailto)}"
    try:
        d = _pedir(url, timeout=25)
    except Exception:                                  # noqa: BLE001
        return []
    locs = [l for l in (d.get("oa_locations") or []) if l]
    locs.sort(key=lambda l: 0 if l.get("host_type") == "repository" else 1)
    salida = []
    for l in locs:
        for u in (l.get("url_for_pdf"), l.get("url")):
            if u:
                salida.append((u, f"unpaywall/{l.get('host_type') or 'oa'}"))
    return salida


def candidatos_arxiv(titulo: str) -> list[tuple[str, str]]:
    """arXiv y bioRxiv alojan versiones de autor de muchos trabajos."""
    if not titulo:
        return []
    q = urllib.parse.quote(f'ti:"{titulo[:110]}"')
    try:
        req = urllib.request.Request(
            f"https://export.arxiv.org/api/query?search_query={q}&max_results=1",
            headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(req, timeout=25) as r:
            xml = r.read().decode("utf-8", "replace")
    except Exception:                                  # noqa: BLE001
        return []
    m = re.search(r"<id>(https?://arxiv\.org/abs/([^<]+))</id>", xml)
    if not m:
        return []
    # Sólo se acepta si el título coincide de verdad: la búsqueda de arXiv es
    # laxa y devolver el PDF equivocado sería peor que no devolver ninguno.
    mt = re.search(r"<entry>.*?<title>(.*?)</title>", xml, re.S)
    if mt:
        norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
        if norm(mt.group(1))[:60] != norm(titulo)[:60]:
            return []
    return [(f"https://arxiv.org/pdf/{m.group(2)}", "arxiv")]


def candidatos_openaire(doi: str) -> list[tuple[str, str]]:
    """OpenAIRE agrega repositorios europeos que los demás no indexan."""
    url = ("https://api.openaire.eu/search/publications?format=json&size=1&doi="
           + urllib.parse.quote(doi))
    try:
        d = _pedir(url, timeout=30)
    except Exception:                                  # noqa: BLE001
        return []
    urls: list[tuple[str, str]] = []
    def buscar(o):
        if isinstance(o, dict):
            for v in o.values():
                buscar(v)
        elif isinstance(o, list):
            for v in o:
                buscar(v)
        elif isinstance(o, str) and o.startswith("http") and (
                o.lower().endswith(".pdf") or "/download/" in o.lower()):
            urls.append((o, "openaire"))
    buscar(d)
    return urls[:3]


def candidatos_core(doi: str, clave: str) -> list[tuple[str, str]]:
    """CORE exige clave gratuita (core.ac.uk/services/api). Sin ella se omite."""
    if not clave:
        return []
    try:
        req = urllib.request.Request(
            "https://api.core.ac.uk/v3/search/works?limit=1&q="
            + urllib.parse.quote(f'doi:"{doi}"'),
            headers={"Authorization": f"Bearer {clave}", "User-Agent": AGENTE})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
    except Exception:                                  # noqa: BLE001
        return []
    salida = []
    for w in (d.get("results") or [])[:1]:
        for u in (w.get("downloadUrl"), *[l.get("downloadUrl") for l in (w.get("sourceFulltextUrls") or []) if isinstance(l, dict)]):
            if u:
                salida.append((u, "core"))
    return salida


def nombre_fichero(f: dict) -> str:
    """`S056 [2024] Reconstructing the last common ancestor.pdf`.

    La clave va delante para que el fichero se rastree hasta la fila del
    apéndice A sin depender del título, que se trunca.
    """
    t = unicodedata.normalize("NFKD", f["titulo"])
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^\w\s-]", "", t).strip()
    t = re.sub(r"\s+", " ", t)[:70].strip()
    return f"{f['clave']} [{f['año'] or 's.f.'}] {t}.pdf".replace("/", "-")


# El último cuerpo no-PDF recibido, para extraerle su citation_pdf_url.
_ULTIMO_CUERPO: list[bytes] = [b""]


def descargar(url: str, destino: Path) -> tuple[str, str]:
    """Devuelve (resultado, detalle). Rechaza lo que no sea un PDF de verdad.

    Un muro de pago responde 200 con una página HTML de «inicie sesión»; sin
    esta comprobación el directorio se llenaría de ficheros .pdf que son avisos
    de acceso denegado, y el informe diría que se obtuvo algo que no se obtuvo.
    """
    try:
        cuerpo = _pedir(url, timeout=90, binario=True)
    except urllib.error.HTTPError as exc:
        return "error", f"HTTP {exc.code}"
    except Exception as exc:                           # noqa: BLE001
        return "error", str(exc)[:80]

    if not cuerpo.startswith(b"%PDF"):
        cabeza = cuerpo[:200].lower()
        que = "HTML" if b"<html" in cabeza or b"<!doctype" in cabeza else "desconocido"
        _ULTIMO_CUERPO[0] = cuerpo
        return "rechazado", f"la respuesta no es un PDF ({que}, {len(cuerpo)} bytes)"
    if len(cuerpo) < 8192:
        return "rechazado", f"PDF sospechosamente pequeño ({len(cuerpo)} bytes)"

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(cuerpo)
    return "descargado", f"{len(cuerpo) // 1024} KB"


RAZONES: dict[str, tuple[str, str]] = {
    "cerrada": ("Sin versión de acceso abierto",
                "Ningún catálogo declara una versión abierta. Vía habitual: préstamo "
                "interbibliotecario, acceso institucional, o escribir a quien firma la "
                "correspondencia — muchos autores envían su propio PDF si se les pide."),
    "error": ("El servidor del editor rechazó la descarga",
              "El catálogo las da por abiertas, pero el servidor responde con un error "
              "(casi siempre 403) a un cliente automático. **Suelen abrirse sin problema "
              "desde un navegador**: prueba el enlace del DOI directamente."),
    "rechazado": ("El enlace no devolvió un PDF",
                  "La respuesta fue una página web, no un artículo: el enlace lleva a la "
                  "ficha del trabajo y el PDF está detrás de otro clic. Abre el DOI y "
                  "busca el enlace de descarga en la propia página."),
    "sin url": ("Declarada abierta, pero sin PDF enlazado",
                "El catálogo la marca como abierta y no da la dirección del fichero. "
                "El DOI suele llevar a la versión legible."),
    "no resoluble": ("No identificable automáticamente",
                     "O no declara DOI —sólo una URL—, o ningún catálogo abierto reconoce "
                     "ese DOI. Hay que ir a mano por la referencia."),
}


def escribir_listado(filas: list[list[str]], fuentes: list[dict]) -> int:
    """Deja en un documento legible las fuentes que no se pudieron obtener.

    El CSV sirve para procesar; esto sirve para trabajar: agrupa por la razón
    del fallo, dice qué hacer con cada grupo y da de cada fuente lo que hace
    falta para pedirla —autores, revista y DOI pinchable—.
    """
    meta = {f["clave"]: f for f in fuentes}
    idx = {n: i for i, n in enumerate(CABECERA_INFORME)}
    grupos: dict[str, list[list[str]]] = {}
    for fila in filas:
        r = fila[idx["resultado"]]
        if r in ("descargado", "ya estaba"):
            continue
        grupos.setdefault(r, []).append(fila)

    total = sum(len(v) for v in grupos.values())
    obtenidas = len(filas) - total
    hoy = time.strftime("%Y-%m-%d")

    out = [
        "# Fuentes sin texto completo",
        "",
        f"De las **{len(filas)}** fuentes del apéndice A se obtuvieron **{obtenidas}** "
        f"por vía de acceso abierto. Las **{total}** restantes están aquí, con la razón "
        "de cada una.",
        "",
        "Generado por `scripts/fetch_oa.py` el " + hoy + ". Para regenerarlo sin volver "
        "a descargar nada:",
        "",
        "```bash",
        "python3 scripts/fetch_oa.py --mailto tu@correo --solo-listado",
        "```",
        "",
        "> Ninguna de estas fuentes se ha retirado del corpus ni se ha marcado como "
        "dudosa: no haber podido descargar el PDF no dice nada sobre la afirmación que "
        "sostiene. Esta lista es un encargo pendiente, no un defecto del corpus.",
        "",
    ]
    for clave in ("cerrada", "error", "rechazado", "sin url", "no resoluble"):
        filas_g = grupos.get(clave)
        if not filas_g:
            continue
        titulo, consejo = RAZONES.get(clave, (clave, ""))
        out += [f"## {titulo} · {len(filas_g)}", "", consejo, "",
                "| Clave | Año | Autores | Título | Publicación | DOI |",
                "|---|---|---|---|---|---|"]
        for fila in sorted(filas_g, key=lambda x: x[idx["clave"]]):
            m = meta.get(fila[idx["clave"]], {})
            doi = fila[idx["doi"]]
            enlace = f"[{doi}](https://doi.org/{doi})" if doi else (m.get("url") or "—")
            esc = lambda s: (s or "").replace("|", "\\|")
            out.append(
                f"| `{fila[idx['clave']]}` | {fila[idx['año']] or '—'} "
                f"| {esc(m.get('autores', ''))[:38]} | {esc(fila[idx['título']])[:76]} "
                f"| {esc(m.get('publicacion', ''))[:34]} | {enlace} |")
        out.append("")

    otros = [k for k in grupos if k not in RAZONES]
    for k in otros:
        out += [f"## {k} · {len(grupos[k])}", ""]
        for fila in grupos[k]:
            out.append(f"- `{fila[idx['clave']]}` {fila[idx['título']][:80]}")
        out.append("")

    out += [
        "## Cómo conseguirlas",
        "",
        "1. **Prueba el DOI en el navegador.** Buena parte de las bloqueadas por el "
        "editor se abren sin más: el rechazo era al cliente automático, no a ti.",
        "2. **Préstamo interbibliotecario.** Si tienes afiliación, es la vía normal y "
        "suele tardar días.",
        "3. **Escribe a quien firma la correspondencia.** Funciona más de lo que parece; "
        "los autores pueden compartir su manuscrito aceptado.",
        "4. **Busca el manuscrito del autor.** Muchas revistas permiten depositarlo en un "
        "repositorio institucional aunque la versión publicada sea de pago.",
        "",
        "Cuando consigas alguna, déjala en `fuentes_pdf/` con el mismo nombre que usa el "
        "script —`CLAVE [AÑO] Título.pdf`— y la próxima ejecución la dará por obtenida "
        "en vez de volver a intentarlo.",
        "",
    ]
    LISTADO.parent.mkdir(parents=True, exist_ok=True)
    LISTADO.write_text("\n".join(out), encoding="utf-8")
    return total


def volcar(filas: list[list[str]], fuentes: list[dict]) -> None:
    """Escribe informe y listado con lo hecho hasta ahora."""
    INFORME.parent.mkdir(parents=True, exist_ok=True)
    with INFORME.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CABECERA_INFORME)
        w.writerows(filas)
    escribir_listado(filas, fuentes)


def cargar_cache() -> dict[str, dict]:
    if not CACHE.exists():
        return {}
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except Exception:                                  # noqa: BLE001
        return {}


def guardar_cache(oa: dict[str, dict]) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(oa, ensure_ascii=False), encoding="utf-8")


def leer_informe() -> list[list[str]]:
    with INFORME.open(encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))[1:]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Descarga las fuentes del apéndice A que están en acceso abierto")
    ap.add_argument("--mailto", required=True,
                    help="tu correo: lo exigen OpenAlex y Europe PMC para identificar al que consulta")
    ap.add_argument("--solo-informe", action="store_true",
                    help="resolver el acceso sin descargar nada")
    ap.add_argument("--limite", type=int, default=0,
                    help="procesar sólo las primeras N fuentes (para probar)")
    ap.add_argument("--core-key", default="",
                    help="clave de CORE (gratuita en core.ac.uk/services/api); sin ella se omite esa fuente")
    ap.add_argument("--rehacer-resolucion", action="store_true",
                    help="ignorar la resolución cacheada y volver a preguntar a los catálogos")
    ap.add_argument("--solo-listado", action="store_true",
                    help="rehacer docs/FUENTES-SIN-ACCESO.md desde el informe ya existente, sin red")
    ap.add_argument("--destino", type=Path, default=DESTINO)
    args = ap.parse_args()

    fuentes = leer_apendice_a()
    if args.solo_listado:
        if not INFORME.exists():
            print(f"no existe {INFORME}: ejecuta antes una pasada completa", file=sys.stderr)
            return 1
        n = escribir_listado(leer_informe(), fuentes)
        print(f"{LISTADO.relative_to(ROOT)} · {n} fuentes sin texto completo", file=sys.stderr)
        return 0
    if args.limite:
        fuentes = fuentes[:args.limite]
    con_doi = [f for f in fuentes if f["doi"]]
    print(f"{len(fuentes)} fuentes en el apéndice A · {len(con_doi)} con DOI", file=sys.stderr)

    oa = {} if args.rehacer_resolucion else cargar_cache()
    if oa:
        print(f"resolución reutilizada de {CACHE.relative_to(ROOT)} "
              f"({len(oa)} fuentes; --rehacer-resolucion para consultar de nuevo)",
              file=sys.stderr)
    faltan_res = [f["doi"] for f in con_doi if f["doi"] not in oa]
    if faltan_res:
        print(f"resolviendo {len(faltan_res)} en OpenAlex…", file=sys.stderr)
        oa.update(resolver_openalex(faltan_res, args.mailto))
        guardar_cache(oa)

    # A las que OpenAlex no da por abiertas se les pregunta a Europe PMC.
    pendientes = [f for f in con_doi
                  if not oa.get(f["doi"], {}).get("abierto")
                  and not oa.get(f["doi"], {}).get("epmc_consultado")]
    if pendientes:
        print(f"consultando Europe PMC por {len(pendientes)} fuentes sin OA en OpenAlex…",
              file=sys.stderr)
        for i, f in enumerate(pendientes, 1):
            alt = resolver_europepmc(f["doi"])
            if alt:
                oa[f["doi"]] = alt
            else:
                oa.setdefault(f["doi"], {"abierto": False, "estado": "", "pdf": "", "via": ""})
                oa[f["doi"]]["epmc_consultado"] = True
            if i % 25 == 0:
                print(f"  {i}/{len(pendientes)}", file=sys.stderr)
                guardar_cache(oa)
            time.sleep(PAUSA_API)
        guardar_cache(oa)

    filas, cuenta = [], {}
    def marcar(k): cuenta[k] = cuenta.get(k, 0) + 1
    interrumpido = False

    try:
        for n_f, f in enumerate(fuentes, 1):
            info = oa.get(f["doi"], {}) if f["doi"] else {}
            fichero = resultado = detalle = ""
            if not f["doi"]:
                acceso, via, url = "sin doi", "", f["url"]
                resultado, detalle = "no resoluble", "la fuente no declara DOI; sólo URL"
            elif not info:
                acceso, via, url = "desconocido", "", ""
                resultado, detalle = "no resoluble", "ningún catálogo abierto reconoce este DOI"
            elif not info.get("abierto"):
                acceso, via, url = "cerrado", info.get("via", ""), ""
                resultado, detalle = "cerrada", "sin versión de acceso abierto declarada"
            else:
                acceso, via, url = info.get("estado", "abierto"), info.get("via", ""), info.get("pdf", "")
                if not url:
                    resultado, detalle = "sin url", "declarada abierta pero sin PDF enlazado"
                elif args.solo_informe:
                    resultado, detalle = "no intentado", "modo --solo-informe"
                else:
                    fichero = nombre_fichero(f)
                    ruta = args.destino / fichero
                    if ruta.exists() and ruta.stat().st_size > 8192:
                        resultado, detalle = "ya estaba", f"{ruta.stat().st_size // 1024} KB"
                    else:
                        # Cadena de candidatos. La ubicación de OpenAlex va
                        # primero; si falla, se pregunta al resto de catálogos
                        # abiertos. Muchos editores rechazan a los clientes
                        # automáticos, pero el mismo trabajo suele estar
                        # depositado en un repositorio que sí lo sirve: para
                        # 10.1038/nature14447, OpenAlex no ofrecía ninguna
                        # ubicación con PDF y Unpaywall lo encontró en el
                        # repositorio de Wageningen.
                        resultado, detalle = descargar(url, ruta)
                        time.sleep(PAUSA_DESCARGA)
                        if resultado != "descargado":
                            extra = []
                            if resultado == "rechazado":
                                extra += candidatos_de_pagina(_ULTIMO_CUERPO[0], url)
                            extra += candidatos_semanticscholar(f["doi"])
                            extra += candidatos_unpaywall(f["doi"], args.mailto)
                            alt = resolver_europepmc(f["doi"])
                            if alt and alt.get("pdf"):
                                extra.append((alt["pdf"], "europepmc"))
                            extra += candidatos_arxiv(f["titulo"])
                            extra += candidatos_crossref(f["doi"])
                            extra += candidatos_openaire(f["doi"])
                            extra += candidatos_core(f["doi"], args.core_key)
                            # Se prueba por anfitrión, no por catálogo: da igual
                            # quién diera el enlace, importa quién lo sirve.
                            cola = sorted(extra, key=lambda c: orden_anfitrion(c[0]))
                            vistos, logrado = {url}, False
                            while cola:
                                u, origen = cola.pop(0)
                                if u in vistos or len(vistos) > 14:
                                    continue
                                vistos.add(u)
                                r2, d2 = descargar(u, ruta)
                                time.sleep(PAUSA_DESCARGA)
                                if r2 == "descargado":
                                    resultado, detalle = r2, f"{d2} (vía {origen})"
                                    via, url, logrado = origen, u, True
                                    break
                                if r2 == "rechazado":
                                    # Los repositorios y PMC devuelven la ficha del
                                    # depósito, y esa ficha declara dónde está el
                                    # PDF. Se sigue un nivel, sin volver atrás.
                                    for u2, _ in candidatos_de_pagina(_ULTIMO_CUERPO[0], u):
                                        if u2 not in vistos:
                                            cola.insert(0, (u2, f"{origen}→pdf_url"))
                            if not logrado:
                                detalle += f"; {len(vistos) - 1} alternativas sin éxito"
                        if resultado != "descargado":
                            fichero = ""
            marcar(resultado)
            filas.append([f["clave"], f["año"], f["titulo"], f["doi"], acceso, via,
                          url, fichero, resultado, detalle])
            if resultado in ("descargado", "rechazado", "error"):
                print(f"  {f['clave']:6} {resultado:11} {detalle}", file=sys.stderr)
            if n_f % CHECKPOINT == 0:
                volcar(filas, fuentes)
    except KeyboardInterrupt:
        interrumpido = True
        print("\n\ninterrumpido: se vuelca lo hecho hasta aquí", file=sys.stderr)

    volcar(filas, fuentes)
    sin_acceso = sum(1 for x in filas if x[8] not in ("descargado", "ya estaba"))

    print("\n" + "=" * 62, file=sys.stderr)
    print(f"informe: {INFORME.relative_to(ROOT)}", file=sys.stderr)
    print(f"listado: {LISTADO.relative_to(ROOT)} · {sin_acceso} sin texto completo", file=sys.stderr)
    for k in sorted(cuenta, key=lambda x: -cuenta[x]):
        print(f"  {cuenta[k]:5}  {k}", file=sys.stderr)
    print(f"\n{sin_acceso} fuentes siguen sin texto completo, y el informe dice por qué "
          f"una a una.\nNo hay huecos silenciosos: ésa es la regla del corpus.",
          file=sys.stderr)
    if interrumpido:
        print(f"\nQuedaron {len(fuentes) - len(filas)} sin procesar. Volver a lanzarlo "
              "reutiliza la resolución y los PDF ya bajados.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
