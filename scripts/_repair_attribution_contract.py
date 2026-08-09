#!/usr/bin/env python3
"""One-shot remediation of the canonical attribution contract in C-001–C-1897.

The script is intentionally temporary.  It uses the frozen pre-degradation
snapshot only to distinguish claims whose attribution was changed solely by
the former literal-passage gate; every exception is listed explicitly below.
"""

from __future__ import annotations

import csv
import io
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path("/tmp/corredor-eukaryota-auditoria-20260808/worktree")
CLAIM_COLUMNS = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]

# New/direct cases for which the cited source asserts or paraphrases the row.
MANUAL_EXPRESS = {
    "C-042", "C-498", "C-526", "C-534", "C-542", "C-550", "C-551",
    "C-559", "C-591", "C-599", "C-615", "C-623", "C-670", "C-672",
    "C-1458", "C-1783", "C-1894", "C-1897",
}

# These two operational negative searches were incorrectly `expresa` in the
# frozen snapshot.  Their only evidence is the bounded search registry.
RESTORE_EXCEPTIONS = {"C-1495", "C-1576"}

# Every synthesis names sufficient, earlier C dependencies explicitly.
MANUAL_SYNTHESES = {
    "C-1006": (
        "sintesis(C-993, C-994, C-995, C-996, C-997, C-998, C-999, "
        "C-1000, C-1001, C-1002, C-1003, C-1004, C-1005)"
    ),
    "C-1087": "sintesis(C-1082, C-1083, C-1084, C-1085, C-1086)",
    "C-1120": "sintesis(C-1088)",
    "C-1309": "sintesis(C-1303, C-1305)",
    "C-1344": "sintesis(C-1122, C-1300, C-1316, C-1323)",
    "C-1639": "sintesis(C-1061, C-1638)",
    "C-1741": "sintesis(C-1737, C-1738, C-1739, C-1740)",
    "C-1770": (
        "sintesis(C-1763, C-1764, C-1765, C-1766, C-1767, C-1768, C-1769)"
    ),
    "C-1776": "sintesis(C-1771, C-1772, C-1773, C-1774, C-1775)",
    "C-1798": "sintesis(C-1794, C-1795, C-1796, C-1797)",
    "C-1815": "sintesis(C-1810, C-1811, C-1812, C-1813, C-1814)",
    "C-1827": "sintesis(C-1822, C-1823, C-1824, C-1825, C-1826)",
    "C-1839": "sintesis(C-1835, C-1836, C-1837, C-1838)",
    "C-1845": "sintesis(C-1840, C-1841, C-1842, C-1843, C-1844)",
    "C-1865": "sintesis(C-1862, C-1863, C-1864)",
    "C-1868": "sintesis(C-1866, C-1867)",
    "C-1879": "sintesis(C-1875, C-1876, C-1877, C-1878)",
    "C-1893": (
        "sintesis(C-1886, C-1887, C-1888, C-1889, C-1890, C-1891, C-1892)"
    ),
}

AUDIT_SENTENCES = (
    "La auditoría independiente no recuperó el fragmento literal exigido "
    "junto al localizador; la atribución se degrada conservadoramente a "
    "glosa y la fuerza no se promueve.",
    "La auditoría independiente no recuperó el fragmento literal exigido "
    "junto al localizador; la fuerza se degrada conservadoramente.",
    "Atribución conservadora como glosa mientras falte un localizador propio "
    "verificable para cada fuente citada.",
    "Atribución conservadora como glosa mientras falte un localizador propio "
    "para cada fuente citada.",
    "Atribución conservadora como glosa mientras el localizador no satisfaga "
    "ambas puertas deterministas.",
    "Atribución conservadora como glosa: la auditoría no verificó un pasaje "
    "propio para cada fuente citada; la referencia se conserva como contexto "
    "bibliográfico y no como apoyo literal inspeccionado.",
)

MOTIVE_OVERRIDES = {
    "C-975": (
        "S229 define la adquisición desde el ambiente y S268 documenta saltos "
        "entre hospedadores; la fila parafrasea conjuntamente ambos alcances."
    ),
    "C-1110": (
        "S229 relaciona cuellos de botella con tamaño efectivo pequeño y S286 "
        "formaliza el efecto de muestreo entre generaciones; la fila "
        "parafrasea ese alcance conjunto."
    ),
    "C-1116": (
        "S229 trata reemplazo y adquisición exógena, mientras S262 y S268 "
        "documentan reemplazos o saltos entre hospedadores."
    ),
    "C-976": "Es una convención terminológica propia del corpus.",
    "C-1495": (
        "La búsqueda recuperó un modelo hidrodinámico, no ATP, consumo de "
        "oxígeno ni coste de crecimiento por roseta."
    ),
    "C-1576": (
        "Las fuentes evaluadas informan presencia y expresión, no presupuestos "
        "energéticos homogéneos."
    ),
    "C-1603": (
        "El modelo reducido recuperado cuantifica flujo y disipación "
        "hidrodinámica del collar, no ATP, oxígeno, calor, coste de crecimiento "
        "ni una comparación metabólica común de rutas."
    ),
    "C-1677": (
        "Es una regla documental explícita: evita convertir una edad de linaje "
        "o de estado observado en el instante no observado de captura."
    ),
    "C-1805": (
        "La fuente primaria vincula la propuesta del término con 1963."
    ),
    "C-1806": (
        "Las fuentes describen una categoría de afinidad incierta, no un clado."
    ),
}

SOURCE_OVERRIDES = {
    "C-1805": "S395 título y propuesta",
    "C-1806": "S395; S396",
    # R-0410: S397 is type `otro` and cannot sustain broad consensus here.
    "C-1889": "S395, S396",
}

ATTRIBUTION_TAG = re.compile(
    r"\[([^\]\n]*?);\s*(expresa|glosa|síntesis|sintesis)\]"
)
CLAIM_REF = re.compile(r"\bC-\d{3,5}\b")
OPERATIONAL_REF = re.compile(r"\b(?:BN-\d{3}|Q-\d{4})\b")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def serialize(rows: list[dict[str, str]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=CLAIM_COLUMNS,
        quoting=csv.QUOTE_ALL,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def clean_audit_motive(text: str) -> str:
    for sentence in AUDIT_SENTENCES:
        text = text.replace(sentence, "")
    return re.sub(r"\s+", " ", text).strip()


def operational_source(text: str) -> str:
    refs = list(dict.fromkeys(OPERATIONAL_REF.findall(text)))
    return "; ".join(refs) if refs else "n/a"


def category(attribution: str) -> str:
    return "síntesis" if attribution.startswith("sintesis(") else attribution


def expanded_claim_refs(text: str) -> list[str]:
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in re.finditer(r"C-(\d{3,5})\s*[–-]\s*C-(\d{3,5})", text):
        start, end = map(int, match.groups())
        if start <= end:
            refs.extend(
                f"C-{number:03d}" if number < 1000 else f"C-{number}"
                for number in range(start, end + 1)
            )
            occupied.append(match.span())
    for match in CLAIM_REF.finditer(text):
        if not any(start <= match.start() < end for start, end in occupied):
            refs.append(match.group(0))
    return list(dict.fromkeys(refs))


def main() -> None:
    old_by_assertion: dict[str, list[dict[str, str]]] = defaultdict(list)
    for section in range(15):
        old_path = SNAPSHOT / "data" / "afirmaciones" / f"{section:02d}.csv"
        if not old_path.exists():
            continue
        for row in read_rows(old_path):
            old_by_assertion[row["Afirmación"]].append(row)

    all_rows: list[dict[str, str]] = []
    rows_by_path: dict[Path, list[dict[str, str]]] = {}
    before = Counter()
    decisions = Counter()

    for section in range(15):
        path = ROOT / "data" / "afirmaciones" / f"{section:02d}.csv"
        rows = read_rows(path)
        rows_by_path[path] = rows
        for row in rows:
            before[category(row["Atribución"])] += 1
            if row["Atribución"] == "glosa":
                historical = old_by_assertion[row["Afirmación"]]
                restore = (
                    len(historical) == 1
                    and historical[0]["Atribución"] == "expresa"
                    and row["#"] not in RESTORE_EXCEPTIONS
                )
                if restore:
                    row["Atribución"] = "expresa"
                    decisions["restaurada_expresa"] += 1
                elif row["#"] in MANUAL_EXPRESS:
                    row["Atribución"] = "expresa"
                    decisions["adjudicada_expresa"] += 1
                elif row["#"] in MANUAL_SYNTHESES:
                    row["Atribución"] = MANUAL_SYNTHESES[row["#"]]
                    decisions["adjudicada_sintesis"] += 1
                else:
                    row["Fuente"] = operational_source(row["Fuente"])
                    decisions["glosa_genuina"] += 1

            row["Motivo"] = clean_audit_motive(row["Motivo"])
            if row["#"] in MOTIVE_OVERRIDES:
                row["Motivo"] = MOTIVE_OVERRIDES[row["#"]]
            if row["#"] in SOURCE_OVERRIDES:
                row["Fuente"] = SOURCE_OVERRIDES[row["#"]]

            if row["#"] == "C-1889":
                row["Atribución"] = "sintesis(C-1805, C-1806)"

            if not row["Motivo"]:
                raise RuntimeError(f"Motivo vacío tras remediación: {row['#']}")
            all_rows.append(row)

    if decisions != Counter({
        "restaurada_expresa": 525,
        "adjudicada_expresa": 18,
        "adjudicada_sintesis": 18,
        "glosa_genuina": 102,
    }):
        raise RuntimeError(f"Censo de decisiones inesperado: {decisions}")

    by_id = {row["#"]: row for row in all_rows}
    after = Counter(category(row["Atribución"]) for row in all_rows)
    if before != Counter({"expresa": 902, "glosa": 663, "síntesis": 332}):
        raise RuntimeError(f"Censo inicial inesperado: {before}")
    if after != Counter({"expresa": 1445, "glosa": 102, "síntesis": 350}):
        raise RuntimeError(f"Censo final inesperado: {after}")
    for row in all_rows:
        if row["Atribución"] == "glosa" and re.search(r"\bS\d{2,3}\b", row["Fuente"]):
            raise RuntimeError(f"Glosa conserva fuente S: {row['#']}")

    for path, rows in rows_by_path.items():
        path.write_text(serialize(rows), encoding="utf-8", newline="")

    # Keep the block being edited concurrently by the node-coverage agent byte-identical.
    section14 = ROOT / "docs/secciones/015-14-14-nombres-y-nomenclatura.md"
    section14_before = section14.read_text(encoding="utf-8")
    block_match = re.search(
        r"(?ms)^## 14\.4\..*?(?=^## 14\.5\.)", section14_before,
    )
    if not block_match:
        raise RuntimeError("No se pudo aislar §14.4")
    protected_block = block_match.group(0)

    narrative_paths = sorted((ROOT / "docs/secciones").glob("*.md"))
    for path in narrative_paths:
        if not re.match(r"(?:00[1-9]|01[0-5])-", path.name):
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        in_protected_14_4 = False
        rewritten: list[str] = []
        for line in lines:
            if path == section14:
                if line.startswith("## 14.4."):
                    in_protected_14_4 = True
                elif in_protected_14_4 and line.startswith("## 14.5."):
                    in_protected_14_4 = False

            if not in_protected_14_4:
                def replace_tag(match: re.Match[str]) -> str:
                    fields = match.group(1)
                    claim_field = fields.split(";", 1)[0].strip()
                    refs = expanded_claim_refs(claim_field)
                    if not refs or any(ref not in by_id for ref in refs):
                        return match.group(0)
                    categories = {category(by_id[ref]["Atribución"]) for ref in refs}
                    if len(categories) != 1:
                        raise RuntimeError(
                            f"Rótulo con categorías mixtas en {path}: {refs}"
                        )
                    live_category = next(iter(categories))
                    if live_category == "glosa":
                        ops = list(dict.fromkeys(OPERATIONAL_REF.findall(fields)))
                        source = "; ".join(ops) if ops else "n/a"
                        return f"[{claim_field}; {source}; glosa]"
                    return f"[{fields}; {live_category}]"

                line = ATTRIBUTION_TAG.sub(replace_tag, line)
            rewritten.append(line)

        text = "".join(rewritten)
        if path == section14:
            replacements = {
                "[C-1805; S395 título y propuesta; S397 historia]":
                    "[C-1805; S395 título y propuesta]",
                "[C-1806; S395; S396; S397]": "[C-1806; S395; S396]",
                "[C-1889; S395, S396, S397]": "[C-1889; S395, S396]",
            }
            for old, new in replacements.items():
                if text.count(old) != 1:
                    raise RuntimeError(f"Localizador narrativo inesperado: {old}")
                text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="")

    section14_after = section14.read_text(encoding="utf-8")
    block_after = re.search(
        r"(?ms)^## 14\.4\..*?(?=^## 14\.5\.)", section14_after,
    )
    if not block_after or block_after.group(0) != protected_block:
        raise RuntimeError("§14.4 cambió durante la remediación")

    print(f"antes={dict(before)}")
    print(f"decisiones={dict(decisions)}")
    print(f"después={dict(after)}")


if __name__ == "__main__":
    main()
