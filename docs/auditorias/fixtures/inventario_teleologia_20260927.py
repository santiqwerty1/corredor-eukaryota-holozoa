"""Inventario mecánico sin adjudicación de candidatos y sus contextos."""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts.audit_requirement_controls import Corpus

PATTERN = re.compile(
    r"\b(superior|inferior|primitiv[oa]s?|avanzad[oa]s?|más evolucionad[oa]s?|"
    r"intento fallido|paso obligatorio|fósil viviente|eslabón perdido|"
    r"eucariota primitivo|organismo simple|versi[oó]n antigua|"
    r"versi[oó]n detenida)\b|apareci[oó] para|"
    r"todavía no hab[ií]a desarrollado", re.IGNORECASE,
)


def collect(root=ROOT):
    corpus = Corpus(root)
    paths = set(corpus.section_paths) | set(corpus.claim_paths.values())
    paths |= {root / e["csv_path"] for e in corpus.index["tables"]}
    paths |= set(corpus.appendix_paths.values())
    result = []
    for path in sorted(paths):
        lines = path.read_text(encoding="utf-8").splitlines()
        header = next(csv.reader([lines[0]])) if path.suffix == ".csv" else None
        for number, line in enumerate(lines, 1):
            hits = list(PATTERN.finditer(line))
            if not hits:
                continue
            cells = dict(zip(header, next(csv.reader([line])))) if header else None
            result.append({
                "numero": len(result)+1, "ruta": path.relative_to(root).as_posix(), "linea": number,
                "texto": line, "sha256_texto": hashlib.sha256((line+"\n").encode()).hexdigest(),
                "celdas": cells, "contexto": lines[max(0, number-3):min(len(lines), number+2)],
                "ocurrencias": [{"inicio": m.start(), "fin": m.end(), "literal": m.group()} for m in hits],
            })
    return {"rutas": len(paths), "candidatos": len(result),
            "ocurrencias": sum(len(x["ocurrencias"]) for x in result), "items": result}


if __name__ == "__main__":
    print(json.dumps(collect(), ensure_ascii=False))
