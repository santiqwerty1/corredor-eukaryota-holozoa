"""Fija el ámbito textual y coteja adjudicaciones ya hechas; no emite dictámenes."""
import hashlib
import json
from datetime import datetime, timezone

from inventario_teleologia_20260927 import Corpus, ROOT, collect


def snapshot():
    corpus = Corpus(ROOT)
    paths = set(corpus.section_paths) | set(corpus.claim_paths.values())
    paths |= {ROOT / entry["csv_path"] for entry in corpus.index["tables"]}
    paths |= set(corpus.appendix_paths.values())
    return {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(paths)
    }


def run():
    before = snapshot()
    inventory = collect()
    ledger_path = ROOT / "docs/auditorias/censo_contextos_teleologia_v1_2026-09-27.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    expected = ledger["candidatos"]
    actual = inventory["items"]
    assert len(before) == 123, len(before)
    assert (len(actual), inventory["ocurrencias"]) == (74, 95)
    assert len(expected) == len(actual)
    for current, reviewed in zip(actual, expected):
        for field in ("ruta", "linea", "texto", "sha256_texto"):
            assert current[field] == reviewed[field], (field, current["ruta"], current["linea"])
        assert current["ocurrencias"] == [
            {key: occurrence[key] for key in ("inicio", "fin", "literal")}
            for occurrence in reviewed["ocurrencias"]
        ]
    after = snapshot()
    assert before == after, "El contexto cambió durante el cotejo"
    return {
        "resultado": "COINCIDE_CON_ADJUDICACION_V1",
        "fecha_snapshot_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "rutas": len(after), "candidatos": len(actual), "ocurrencias": inventory["ocurrencias"],
        "sha256_ledger_v1": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        "huellas_rutas": after,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
