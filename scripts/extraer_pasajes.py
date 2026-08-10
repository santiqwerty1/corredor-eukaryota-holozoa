#!/usr/bin/env python3
"""Extrae de cada fuente el pasaje que su localizador señala.

Cada afirmación del corpus cita su fuente con un localizador —«S56 líneas
318–321», «S38 resumen y fig. 5», «S57 p. 296»—. Hasta ahora ese localizador
era una promesa: decía dónde mirar, pero nadie podía mirar. Con el texto
completo descargado sí se puede, y este script recorta el fragmento señalado.

Sirve para dos cosas a la vez:

1. **Auditoría.** Pone delante del revisor el trozo exacto que debe juzgar, en
   vez de obligarle a abrir el artículo y buscar. Verificar mil localizadores
   deja de ser inviable.
2. **Ingestión.** §17 exige una capa de pasajes: cada afirmación ingerida
   apunta a un `PASSAGE-` con el texto que la sostiene. Esa capa no existe y
   habría que construirla a mano; esto la produce.

**No decide nada.** No dice si el pasaje sostiene la afirmación: recorta y
presenta. Juzgar es del revisor, que es donde §27.12 pone el juicio humano.
Cuando un localizador no se puede resolver, se dice por qué y se deja el
fragmento vacío: un hueco declarado, nunca un recorte inventado.

Uso:
    python3 scripts/extraer_pasajes.py                    # todas las que se pueda
    python3 scripts/extraer_pasajes.py --clave S56        # sólo una fuente
    python3 scripts/extraer_pasajes.py --limite 50
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "exports" / "afirmaciones.csv"
FUENTES = ROOT / "fuentes_pdf"
SALIDA = ROOT / "exports" / "pasajes.csv"

CABECERA = ["afirmacion", "texto_afirmacion", "clave_fuente", "localizador",
            "tipo_localizador", "pasaje", "estado", "detalle"]
REVISION = ROOT / "docs" / "revision-pasajes.html"

# Cómo se nombra en el corpus el sitio donde mirar. El tipo importa: un
# localizador de línea se resuelve contando, uno de sección se resuelve
# buscando el rótulo, y uno de figura no se resuelve en el texto en absoluto.
PATRONES = [
    ("lineas",   re.compile(r"l[ií]neas?\s+(\d+)\s*[–—-]\s*(\d+)", re.I)),
    ("linea",    re.compile(r"l[ií]nea\s+(\d+)", re.I)),
    ("pagina",   re.compile(r"\bp{1,2}\.?\s*(\d+)", re.I)),
    ("seccion",  re.compile(r"§\s*([\w\s]{3,40})", re.I)),
    # El corpus nombra las secciones en español —«resultados», «discusión»— y
    # a menudo cita varias a la vez: «resumen; resultados», «resultados y
    # discusión». Se reconocen todas y se recortan todas.
    ("apartado", re.compile(r"\b(resumen|abstract|introducci[oó]n|introduction|"
                            r"resultados?|results?|discusi[oó]n|discussion|"
                            r"m[eé]todos?|methods?|materiales|conclusi[oó]n(?:es)?|"
                            r"conclusions?)\b", re.I)),
    ("figura",   re.compile(r"\bfigs?\.?\s*S?\d+|\bfigura\s*\d+", re.I)),
    ("tabla",    re.compile(r"\btablas?\s*S?\d+|\btables?\s*S?\d+", re.I)),
]


# El corpus escribe sus punteros semánticos en español y los artículos están en
# inglés: buscar «clasificación» en un texto inglés no encuentra nada nunca. La
# equivalencia se declara aquí, y se buscan ambas formas.
CONCEPTOS = {
    "clasificación": ("classification", "taxonomy", "taxonomic"),
    "clasificacion": ("classification", "taxonomy"),
    "filogenia": ("phylogeny", "phylogenetic", "phylogenomic"),
    "descripción": ("description", "described", "diagnosis"),
    "descripcion": ("description", "described"),
    "definición": ("definition", "defined", "we define"),
    "definicion": ("definition", "defined"),
    "nomenclatura": ("nomenclature", "nomenclatural", "naming"),
    "revisión": ("revision", "review", "revised"),
    "revision": ("revision", "review"),
    "propuesta": ("propose", "proposal", "we propose"),
    "historia": ("history", "historical", "originally"),
    "método": ("method", "methods"), "metodo": ("method", "methods"),
    "muestreo": ("sampling", "sampled"),
    "edad": ("age", "dated", "dating"),
    "datación": ("dating", "age estimate"), "datacion": ("dating", "age estimate"),
    "topología": ("topology", "tree"), "topologia": ("topology", "tree"),
    "raíz": ("root", "rooting"), "raiz": ("root", "rooting"),
    "genoma": ("genome", "genomic"),
    "ecología": ("ecology", "ecological"), "ecologia": ("ecology", "ecological"),
}


def texto_de_xml(ruta: Path) -> tuple[str, dict[str, str]]:
    """Devuelve el cuerpo en texto plano y sus secciones por rótulo."""
    bruto = ruta.read_text(encoding="utf-8", errors="replace")
    secciones: dict[str, str] = {}
    for m in re.finditer(r"<sec\b[^>]*>(.*?)</sec>", bruto, re.S | re.I):
        cuerpo = m.group(1)
        tit = re.search(r"<title>(.*?)</title>", cuerpo, re.S | re.I)
        if tit:
            secciones[_limpiar(tit.group(1)).lower()] = _limpiar(cuerpo)
    res = re.search(r"<abstract\b[^>]*>(.*?)</abstract>", bruto, re.S | re.I)
    if res:
        secciones["resumen"] = secciones["abstract"] = _limpiar(res.group(1))
    tit = re.search(r"<article-title>(.*?)</article-title>", bruto, re.S | re.I)
    if tit:
        secciones["__titulo__"] = _limpiar(tit.group(1))
    return _limpiar(bruto), secciones


def _limpiar(x: str) -> str:
    x = re.sub(r"<[^>]+>", " ", x)
    x = html.unescape(x)
    return re.sub(r"\s+", " ", x).strip()


def trozo_de(localizador: str, clave: str) -> str:
    """La parte del localizador que habla de ESTA fuente.

    Un localizador como «S275 resumen; S276 resultados» nombra dos sitios
    distintos en dos trabajos distintos. Tratarlo entero para cada fuente
    recortaba de S276 también su resumen, que nadie había citado: el pasaje
    salía más ancho que la cita, y un pasaje que no es el citado no sirve para
    comprobar nada.
    """
    trozos = [s for s in re.split(r"[;·]", localizador or "") if s.strip()]
    propios = [s for s in trozos if re.search(r"\b" + clave + r"\b", s)]
    if not propios:
        return localizador or ""
    # Si el trozo es sólo la clave, la descripción puede venir en el siguiente.
    salida = []
    for s in propios:
        resto = re.sub(r"\b" + clave + r"\b", " ", s).strip(" ,.:")
        salida.append(s if resto else s)
    return "; ".join(salida)


def tipo_de(localizador: str) -> tuple[str, tuple]:
    """El primer patrón que case manda; para «apartado» se devuelven todas las
    secciones citadas, porque «resumen; resultados» son dos sitios, no uno."""
    for nombre, pat in PATRONES:
        if nombre == "apartado":
            todas = [m.group(1) for m in pat.finditer(localizador or "")]
            if todas:
                return nombre, tuple(dict.fromkeys(todas))
            continue
        m = pat.search(localizador or "")
        if m:
            return nombre, m.groups()
    for nombre, pat in PATRONES:            # segunda vuelta: apartado al final
        if nombre == "apartado":
            todas = [m.group(1) for m in pat.finditer(localizador or "")]
            if todas:
                return nombre, tuple(dict.fromkeys(todas))
    # Buena parte de los localizadores del corpus no dicen DÓNDE sino QUÉ:
    # «S01 clasificación», «S109 filogenia», «S124 definición de Amorphea».
    # Son punteros semánticos, y se resuelven buscando el concepto en el texto,
    # no contando líneas.
    concepto = re.sub(r"\bS\d{2,3}\b|\bBN-\d+\b|\bC-\d+\b", " ", localizador or "")
    concepto = re.sub(r"[;:,.·]+", " ", concepto).strip()
    if len(concepto) >= 4 and concepto.lower() not in ("n/a", "na", "s/d"):
        return "concepto", (concepto,)
    return "sin tipo", ()


def recortar(texto: str, secciones: dict[str, str], tipo: str,
             grupos: tuple) -> tuple[str, str, str]:
    """(pasaje, estado, detalle). Nunca inventa: si no se puede, lo dice."""
    if tipo in ("figura", "tabla"):
        return "", "no resoluble en texto", (
            "el localizador señala una figura o tabla, que no vive en el cuerpo "
            "del texto; hay que mirarla en el PDF")
    if tipo == "apartado":
        # El artículo casi siempre está en inglés y el localizador en español.
        ALIAS = {
            "resumen": ("abstract", "resumen"),
            "abstract": ("abstract",),
            "introducción": ("introduction", "introducción"),
            "introduccion": ("introduction",),
            "introduction": ("introduction",),
            "resultado": ("results", "resultados"),
            "resultados": ("results", "resultados"),
            "results": ("results",), "result": ("results",),
            "discusión": ("discussion", "discusión"),
            "discusion": ("discussion",), "discussion": ("discussion",),
            "método": ("methods", "materials"), "métodos": ("methods", "materials"),
            "metodos": ("methods",), "methods": ("methods",), "method": ("methods",),
            "materiales": ("materials", "methods"),
            "conclusión": ("conclusion",), "conclusiones": ("conclusion",),
            "conclusion": ("conclusion",), "conclusions": ("conclusion",),
        }
        trozos, usadas, faltan = [], [], []
        for pedido in grupos:                 # el localizador puede citar varias
            k = (pedido or "").lower()
            hallado = False
            for objetivo in ALIAS.get(k, (k,)):
                for nombre, cuerpo in secciones.items():
                    if objetivo and objetivo in nombre:
                        if nombre not in usadas:
                            trozos.append(f"[{nombre}] {cuerpo}")
                            usadas.append(nombre)
                        hallado = True
                        break
                if hallado:
                    break
            if not hallado:
                faltan.append(k)
        if trozos:
            det = "secciones " + ", ".join(f"«{u}»" for u in usadas)
            if faltan:
                det += f"; sin localizar {', '.join(faltan)}"
            return " ".join(trozos)[:2400], "recortado", det
        return "", "no localizado", f"no hay sección que case con {', '.join(faltan) or grupos}"
    if tipo == "seccion":
        clave = (grupos[0] or "").strip().lower()
        for nombre, cuerpo in secciones.items():
            if clave and clave[:14] in nombre:
                return cuerpo[:1800], "recortado", f"sección «{nombre}»"
        return "", "no localizado", f"no hay sección «{clave}»"
    if tipo == "concepto":
        # Se devuelven los párrafos donde más pesa el concepto pedido. Es una
        # ayuda para encontrar, no un veredicto: el rótulo del estado lo dice.
        pedido = (grupos[0] or "").lower()
        # «tesis general» pide la idea del trabajo entero: el resumen es su sitio.
        if re.search(r"tesis general|tesis del|idea general", pedido):
            for nombre in ("abstract", "resumen"):
                if secciones.get(nombre):
                    return secciones[nombre][:1800], "recortado", (
                        "«tesis general» se resuelve con el resumen, que es donde el "
                        "trabajo enuncia su idea")
        if re.search(r"^t[ií]tulo|\btitle\b", pedido) and secciones.get("__titulo__"):
            return secciones["__titulo__"], "recortado", "título del artículo"
        palabras = [w for w in re.findall(r"[\wÁ-ÿ]{4,}", pedido)][:6]
        # A cada palabra española se le añaden sus equivalentes en inglés.
        for w in list(palabras):
            palabras.extend(CONCEPTOS.get(w, ()))
        if not palabras or not texto:
            return "", "no localizado", f"nada que buscar en «{pedido}»"
        parrafos = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÁ-Ü])", texto)
                    if len(s.strip()) > 120]
        puntuados = []
        for i, s in enumerate(parrafos):
            b = s.lower()
            pts = sum(b.count(w) for w in palabras)
            if pts:
                puntuados.append((pts, i, s))
        puntuados.sort(key=lambda x: (-x[0], x[1]))
        if not puntuados:
            return "", "no localizado", (
                f"«{pedido}» no aparece en el texto completo; puede estar en una "
                "figura, una tabla o el material suplementario")
        trozo = " […] ".join(s for _, _, s in puntuados[:3])
        return trozo[:2400], "por concepto", (
            f"pasajes donde pesa «{pedido}» ({len(puntuados)} candidatos); "
            "es una ayuda para localizar, no un recorte por posición")
    if tipo in ("lineas", "linea", "pagina"):
        # El XML no conserva ni líneas ni páginas del PDF publicado: decirlo es
        # más honrado que devolver un fragmento aproximado y llamarlo el pasaje.
        return "", "no resoluble en texto", (
            "el localizador cuenta líneas o páginas del PDF, y el XML no las "
            "conserva; se resuelve sobre el PDF")
    return "", "sin tipo", "no se reconoce la forma del localizador"


def escribir_revision(salida: list[list]) -> None:
    """Afirmación y pasaje enfrentados, para revisar en tandas.

    Comprobar mil localizadores abriendo mil artículos no lo hace nadie. Con la
    afirmación a la izquierda y lo que dice la fuente a la derecha, el juicio
    —que sigue siendo humano, §27.12— cuesta segundos en vez de minutos.
    """
    ORDEN = {"recortado": 0, "por concepto": 1, "no localizado": 2,
             "no resoluble en texto": 3, "sin texto": 4, "sin tipo": 5}
    filas = sorted(salida, key=lambda r: (ORDEN.get(r[6], 9), r[0]))
    esc = lambda s: (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    cuenta: dict[str, int] = {}
    for r in filas:
        cuenta[r[6]] = cuenta.get(r[6], 0) + 1
    tarjetas = []
    for r in filas:
        pasaje = esc(r[5])[:2000] or "<em>sin pasaje</em>"
        tarjetas.append(f"""<article data-estado="{esc(r[6])}">
 <div class=izq><div class=id>{esc(r[0])} · <span class=src>{esc(r[2])}</span></div>
  <p class=afi>{esc(r[1])[:420]}</p>
  <div class=loc>{esc(r[3])}</div></div>
 <div class=der><div class="est e-{esc(r[6]).replace(' ', '-')}">{esc(r[6])}</div>
  <p class=pas>{pasaje}</p>
  <div class=det>{esc(r[7])}</div></div>
</article>""")
    botones = "".join(f'<button data-f="{esc(k)}">{esc(k)} ({v})</button>'
                      for k, v in sorted(cuenta.items(), key=lambda x: -x[1]))
    html = f"""<!doctype html><meta charset="utf-8">
<title>Revisión de pasajes</title>
<style>
 body{{font:15px/1.55 system-ui,sans-serif;margin:0;padding:1.5rem;background:#fbfbfd;color:#1a1a1f}}
 h1{{font-size:20px;margin:0 0 .3rem}} .nota{{color:#555;max-width:70ch;margin:0 0 1rem}}
 nav{{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1rem;position:sticky;top:0;
   background:#fbfbfd;padding:.5rem 0;border-bottom:1px solid #e3e3e8;z-index:2}}
 button{{border:1px solid #d0d0d8;background:#fff;border-radius:6px;padding:5px 11px;
   font:inherit;font-size:13px;cursor:pointer}} button[aria-pressed=true]{{background:#1a1a1f;color:#fff}}
 article{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:1.2rem;
   background:#fff;border:1px solid #e3e3e8;border-radius:9px;padding:.9rem 1.1rem;margin-bottom:.7rem}}
 .id{{font:600 12px ui-monospace,monospace;color:#5a5a6a}} .src{{color:#7a6ad0}}
 .afi{{margin:.35rem 0;font-size:14px}} .loc{{font:12px ui-monospace,monospace;color:#7a7a8a}}
 .pas{{margin:.35rem 0;font-size:13.5px;color:#2a2a35;max-height:15em;overflow:auto}}
 .det{{font-size:11.5px;color:#7a7a8a}}
 .est{{display:inline-block;font-size:11px;padding:2px 8px;border-radius:20px;background:#eee}}
 .e-recortado{{background:#d8f0dc}} .e-por-concepto{{background:#e5e2fb}}
 .e-no-localizado,.e-sin-texto{{background:#f6e3d8}}
 @media(max-width:820px){{article{{grid-template-columns:1fr}}}}
</style>
<h1>Revisión de pasajes</h1>
<p class=nota><strong>{len(filas)}</strong> localizadores. A la izquierda lo que afirma el
corpus; a la derecha lo que dice la fuente en el sitio que la propia afirmación señala.
El script recorta y presenta: <strong>decidir si el pasaje sostiene la afirmación es
tuyo</strong>. Un pasaje ausente no es un defecto de la afirmación, es un localizador que
no se pudo resolver, y el rótulo dice por qué.</p>
<nav><button data-f="" aria-pressed="true">todos ({len(filas)})</button>{botones}</nav>
{chr(10).join(tarjetas)}
<script>
 const arts=[...document.querySelectorAll('article')],bs=[...document.querySelectorAll('nav button')];
 bs.forEach(b=>b.onclick=()=>{{bs.forEach(x=>x.setAttribute('aria-pressed',x===b));
  const f=b.dataset.f; arts.forEach(a=>a.style.display=(!f||a.dataset.estado===f)?'':'none');}});
</script>"""
    REVISION.parent.mkdir(parents=True, exist_ok=True)
    REVISION.write_text(html, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Extrae los pasajes que citan las afirmaciones")
    ap.add_argument("--clave", help="procesar sólo esta fuente (p. ej. S56)")
    ap.add_argument("--limite", type=int, default=0)
    args = ap.parse_args()

    xmls = {p.name.split()[0]: p for p in FUENTES.glob("*.xml")}
    if not xmls:
        print(f"no hay ningún .xml en {FUENTES}: ejecuta antes fetch_oa.py", file=sys.stderr)
        return 1
    print(f"{len(xmls)} fuentes con texto completo en XML", file=sys.stderr)

    with EXPORT.open(encoding="utf-8", newline="") as fh:
        filas = [r for r in list(csv.reader(fh))[1:] if len(r) > 6]

    cache: dict[str, tuple[str, dict]] = {}
    salida, cuenta = [], {}
    for r in filas:
        loc = r[6] or ""
        for clave in dict.fromkeys(re.findall(r"\bS\d{2,3}\b", loc)):
            if args.clave and clave != args.clave:
                continue
            propio = trozo_de(loc, clave)
            tipo, grupos = tipo_de(propio)
            if clave not in xmls:
                salida.append([r[0], r[1], clave, loc, tipo, "", "sin texto",
                               "no hay XML de esta fuente"])
                cuenta["sin texto"] = cuenta.get("sin texto", 0) + 1
                continue
            if clave not in cache:
                cache[clave] = texto_de_xml(xmls[clave])
            texto, secciones = cache[clave]
            pasaje, estado, detalle = recortar(texto, secciones, tipo, grupos)
            salida.append([r[0], r[1], clave, propio if propio != loc else loc,
                           tipo, pasaje, estado, detalle])
            cuenta[estado] = cuenta.get(estado, 0) + 1
        if args.limite and len(salida) >= args.limite:
            break

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CABECERA)
        w.writerows(salida)

    escribir_revision(salida)
    print(f"\n{SALIDA.relative_to(ROOT)} · {len(salida)} localizadores", file=sys.stderr)
    print(f"{REVISION.relative_to(ROOT)} · para revisar enfrentando afirmación y pasaje",
          file=sys.stderr)
    for k in sorted(cuenta, key=lambda x: -cuenta[x]):
        print(f"  {cuenta[k]:6}  {k}", file=sys.stderr)
    util = cuenta.get("recortado", 0) + cuenta.get("por concepto", 0)
    print(f"\n{util} localizadores con pasaje delante: {cuenta.get('recortado', 0)} "
          f"recortados por sección y {cuenta.get('por concepto', 0)} localizados por "
          f"concepto.\nEl resto declara por qué no se pudo, que es la única forma "
          f"honrada de contarlo.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
