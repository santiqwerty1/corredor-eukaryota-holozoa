"""Compara NC-DEN02 en memoria; no regenera la traza ni adjudica ciencia."""
import hashlib
import json
import re
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import build_content_trace as trace


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def previous_split(text):
    # Función histórica capturada en el diagnóstico, sin cambiar el módulo en disco.
    sentinel = "\ue000"
    protected = trace.ABBREVIATION.sub(lambda match: match.group().replace(".", sentinel), text)
    return [piece.replace(sentinel, ".").strip()
            for piece in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡“«`])", protected) if piece.strip()]


def input_hashes():
    paths = set((ROOT / "docs/secciones").glob("*.md"))
    paths.update((ROOT / "data/afirmaciones").glob("*.csv"))
    paths.update({ROOT / "data/table_index.json", trace.CELL_MANIFEST, trace.OUTPUT})
    index = json.loads((ROOT / "data/table_index.json").read_text(encoding="utf-8"))
    paths.update(ROOT / row["csv_path"] for row in index["tables"])
    return {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in sorted(paths)}


before = input_hashes()
with patch.object(trace, "split_sentences", previous_split):
    old_narrative = trace.narrative_segments()
new_narrative = trace.narrative_segments()
ambiguities = trace.narrative_ambiguities()
cells = trace.table_cells()
manifest, manifest_errors = trace.load_cell_manifest()
manifest_errors.extend(trace.cell_manifest_errors(cells, manifest))
tables = trace.table_segments(cells, manifest)
old_payload = trace.csv_bytes(old_narrative + tables)
new_payload = trace.csv_bytes(new_narrative + tables)
old_errors = trace.validate_payload(old_payload)
new_errors = trace.validate_payload(new_payload)
old_missing_keys = {(s.path, s.content) for s in old_narrative if not s.claims}
exposed = [s for s in new_narrative if not s.claims and (s.path, s.content) not in old_missing_keys]
old_groups = {}
new_groups = {}
for collection, groups in ((old_narrative, old_groups), (new_narrative, new_groups)):
    for segment in collection:
        key = (segment.path, segment.locator.split(";")[0])
        groups.setdefault(key, []).append(segment)
changed = []
for key in sorted(set(old_groups) | set(new_groups)):
    old = old_groups.get(key, [])
    new = new_groups.get(key, [])
    if old != new:
        changed.append({"path": key[0], "block_locator": key[1],
            "before": [{"locator": s.locator, "sha256_text_lf": sha((s.content + "\n").encode()), "claims": s.claims} for s in old],
            "after": [{"locator": s.locator, "sha256_text_lf": sha((s.content + "\n").encode()), "claims": s.claims} for s in new]})
after = input_hashes()
result = {
    "utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "scope": "Ejecución autoral en memoria; no revisión independiente del parche ni de las C",
    "hashes": {name: sha((ROOT / name).read_bytes()) for name in (
        "scripts/build_content_trace.py", "tests/test_content_trace_sentence_boundaries.py",
        str(Path(__file__).relative_to(ROOT)),
    )},
    "historical_builder_sha256": "665322eef3aa0ffe640173e9463e4b9e3a45687c0af2b26c5270f7764ebb0f54",
    "inputs_before": before, "inputs_after": after, "inputs_stable": before == after,
    "persisted_trace_unchanged": before[str(trace.OUTPUT.relative_to(ROOT))] == after[str(trace.OUTPUT.relative_to(ROOT))],
    "counts": {"old_narrative": len(old_narrative), "new_narrative": len(new_narrative),
        "tables": len(tables), "old_total": len(old_narrative) + len(tables),
        "new_total": len(new_narrative) + len(tables), "changed_blocks": len(changed),
        "newly_exposed_without_C": len(exposed), "ambiguous_blocks": len(ambiguities),
        "ambiguous_boundaries": sum(len(item["fronteras"]) for item in ambiguities)},
    "old_errors": old_errors, "new_errors": new_errors, "manifest_errors": manifest_errors,
    "newly_exposed_without_C": [asdict(s) for s in exposed], "changed_blocks": changed,
    "ambiguities_not_scientific_violations": ambiguities,
    "payloads": {"old": sha(old_payload), "new": sha(new_payload)},
}
print(json.dumps(result, ensure_ascii=False, indent=2))
