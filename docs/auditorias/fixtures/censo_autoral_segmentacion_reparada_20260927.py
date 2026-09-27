"""Reejecuta el censo inicial en memoria y evita repetir texto por frontera.

Los bloques completos y los spans se conservan. El literal redundante de cada
frontera se identifica por su huella; no se cambia ninguna adjudicación ni dato.
No escribe archivos ni regenera derivados.
"""
import contextlib
import hashlib
import io
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve()
with contextlib.redirect_stdout(io.StringIO()):
    namespace = runpy.run_path(str(HERE.with_name("censo_autoral_segmentacion_20260927.py")))
result = namespace["result"]
for block in result["ambiguities_not_scientific_violations"]:
    for frontier in block["fronteras"]:
        literal = frontier.pop("literal")
        frontier["sha256_literal_lf"] = hashlib.sha256((literal + "\n").encode()).hexdigest()
result["representation_note"] = (
    "Bloques completos y spans Unicode conservados; se omite únicamente el literal "
    "redundante por frontera, cuya huella se conserva. No es un censo adjudicado."
)
result["hashes"][str(HERE.relative_to(namespace["ROOT"]))] = hashlib.sha256(HERE.read_bytes()).hexdigest()
print(json.dumps(result, ensure_ascii=False))
