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

CABECERA = ["afirmacion", "clave_fuente", "localizador", "tipo_localizador",
            "pasaje", "estado", "detalle"]

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
    return _limpiar(bruto), secciones


def _limpiar(x: str) -> str:
    x = re.sub(r"<[^>]+>", " ", x)
    x = html.unescape(x)
    return re.sub(r"\s+", " ", x).strip()


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
        palabras = [w for w in re.findall(r"[\wÁ-ÿ]{4,}", pedido)][:6]
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
            tipo, grupos = tipo_de(loc)
            if clave not in xmls:
                salida.append([r[0], clave, loc, tipo, "", "sin texto",
                               "no hay XML de esta fuente"])
                cuenta["sin texto"] = cuenta.get("sin texto", 0) + 1
                continue
            if clave not in cache:
                cache[clave] = texto_de_xml(xmls[clave])
            texto, secciones = cache[clave]
            pasaje, estado, detalle = recortar(texto, secciones, tipo, grupos)
            salida.append([r[0], clave, loc, tipo, pasaje, estado, detalle])
            cuenta[estado] = cuenta.get(estado, 0) + 1
        if args.limite and len(salida) >= args.limite:
            break

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CABECERA)
        w.writerows(salida)

    print(f"\n{SALIDA.relative_to(ROOT)} · {len(salida)} localizadores", file=sys.stderr)
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
