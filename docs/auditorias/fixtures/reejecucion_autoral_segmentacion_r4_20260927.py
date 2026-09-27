"""Reejecución del autor: evidencia técnica, nunca una firma independiente.

Conserva nominalmente los resultados de cada caso heredado, sin reproducir
textos/objetos duplicados del censo. La fixture independiente queda intacta.
No escribe trazas canónicas ni adjudica fronteras científicas.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "docs/auditorias/fixtures/reinspeccion_independiente_segmentacion_ncden02_r3_20260927.py"
spec = importlib.util.spec_from_file_location("author_rerun_den02_r3", FIXTURE)
review_fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review_fixture)
raw = review_fixture.run()


def compact(value):
    """No transforma un resultado: conserva cada nombre, pass y su contexto.

    Los campos estáticos de identidad de la fixture no identifican al ejecutor
    de esta corrida; se retienen separados para impedir atribución falsa.
    """
    if isinstance(value, list):
        return [compact(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key in {"hashes_before", "hashes_after", "inputs_before", "inputs_after"}:
            continue
        if key in {"revisor", "independencia", "autor_implementacion"}:
            result["campo_estatico_fixture_" + key] = item
        else:
            result[key] = compact(item)
    return result


result = {
    "ejecutor_real": "/root/verificacion_fuentes_nuevas",
    "tipo": "REEJECUCION_AUTORAL_SIN_APROBACION_INDEPENDIENTE",
    "fixture_origen": str(FIXTURE.relative_to(ROOT)),
    "inputs_before": raw["hashes_before"],
    "inputs_after": raw["hashes_after"],
    "resultados": compact(raw),
}
print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
