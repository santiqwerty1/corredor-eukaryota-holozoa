"""Reproduce R0393 sin modificar canon ni validadores; fixtures en /tmp."""
import contextlib
import csv
import hashlib
import io
import json
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from scripts import build_content_trace as trace
from scripts import audit_semantics as semantics


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


CASES = (
    ("solo_C_no_es_localizador_S", "Se midieron 223 orígenes [C-001].", 1,
     "INCUMPLE_DENSIDAD", "Una C no es una clave de fuente con localizador.", True),
    ("S_solo_en_segunda_oracion", "Se midieron 223 orígenes [C-001]. Otro análisis informó 16 casos [C-001; S01 p. 1].", 2,
     "INCUMPLE_DENSIDAD", "Primera oración cuantitativa sin S/localizador; la segunda no la cubre.", True),
    ("cita_tras_punto_fusiona_oraciones", "Se midieron 223 orígenes. [C-001] Otro análisis informó 16 casos. [C-001; S01 p. 1]", 2,
     "INCUMPLE_DENSIDAD", "El primer grupo pospuesto sólo tiene C; el S de la segunda no lo sustituye.", True),
    ("cita_tras_punto_oculta_segunda_sin_C", "Se midieron 223 orígenes. [C-001; S01 p. 1] Otro análisis informó 16 casos.", 2,
     "INCUMPLE_C_Y_DENSIDAD", "La segunda oración no tiene C ni fuente propios; no hereda los de la primera.", True),
    ("S_sin_localizador", "Se midieron 223 orígenes [C-001; S01].", 1,
     "INCUMPLE_DENSIDAD", "Una cifra exige localizador o marca honesta de imprecisión; la clave sola no basta.", True),
    ("palabra_metodo_no_es_fuente", "Se midieron 223 orígenes [C-001; método propio].", 1,
     "INCUMPLE_DENSIDAD", "La palabra método no acredita ninguna fuente nominal.", True),
    ("control_con_fuente_y_localizador", "Se midieron 223 orígenes [C-001; S01 p. 1].", 1,
     "ESTRUCTURA_PRESENTE_NO_COTEJO_CIENTIFICO", "Fuente/localizador están en la oración; su soporte real no se prueba aquí.", True),
    ("marca_honesta_no_se_convierte_en_pasaje", "Se midieron 223 orígenes [C-001; S01 (sin localizar)].", 1,
     "IMPRECISION_HONESTA_NO_PASAJE_LOCALIZADO", "El contrato admite la marca honesta; no se inventa p.1 ni se confunde con pasaje recuperable.", True),
    ("SIN_FUENTE_no_exime_registro_C", "[SIN FUENTE] Se midieron 223 orígenes; se incluye para explicitar un dato no respaldado.", 1,
     "INCUMPLE_REGISTRO_C", "La marca explícita no elimina el deber independiente de registrar la proposición.", False),
    ("control_abreviatura_bibliografica", "Smith et al. observaron 12 casos [C-001; S01 fig. 2]. Otra observación informó 16 [C-001; S01 p. 3].", 2,
     "ESTRUCTURA_PRESENTE_NO_COTEJO_CIENTIFICO", "Las abreviaturas et al., fig. y p. no constituyen fronteras de oración.", True),
)


def run_case(case):
    key, text, grammatical_count, status, reason, expected_acceptance = case
    with TemporaryDirectory(prefix="r0393-independent-") as temporary:
        root = Path(temporary)
        prose = root / "docs/secciones/003-02-fixture.md"
        prose.parent.mkdir(parents=True)
        prose.write_text(text + "\n", encoding="utf-8")
        claims = root / "data/afirmaciones/03.csv"
        claims.parent.mkdir(parents=True)
        with claims.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Fuente", "Motivo", "Resolución"])
            writer.writerow(["C-001", "Caso sintético para probar el contrato", "caso", "tiene_valor_medido", "223", "S01 p. 1", "Fixture sin firma científica", "resuelta"])
        (root / "data/table_index.json").write_text('{"tables": []}', encoding="utf-8")
        manifest = root / "data/auditoria/mapeo_celdas_afirmaciones.csv"
        manifest.parent.mkdir(parents=True)
        with manifest.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle).writerow(trace.CELL_MANIFEST_HEADER)
        output = root / "docs/auditorias/traza_ficticia.csv"
        capture_out, capture_error = io.StringIO(), io.StringIO()
        with patch.object(trace, "ROOT", root), patch.object(trace, "OUTPUT", output), patch.object(trace, "CELL_MANIFEST", manifest):
            with contextlib.redirect_stdout(capture_out), contextlib.redirect_stderr(capture_error):
                with patch.object(sys, "argv", ["build_content_trace.py"]):
                    built = trace.main()
                with patch.object(sys, "argv", ["build_content_trace.py", "--check"]):
                    checked = trace.main()
            segments = trace.narrative_segments()
        narrative_errors = []
        with patch.object(semantics, "ROOT", root):
            semantics.audit_narrative(narrative_errors)
        accepted = built == checked == 0
        return {
            "id": key, "text": text, "manual_grammatical_sentences": grammatical_count,
            "manual_scope_verdict": status, "manual_reason": reason,
            "trace_segments": [asdict(s) for s in segments], "split_sentences": trace.split_sentences(text),
            "narrative_audit_errors": narrative_errors,
            "trace_build_exit": built, "trace_check_exit": checked, "trace_accepted": accepted,
            "trace_stdout": capture_out.getvalue(), "trace_stderr": capture_error.getvalue(),
            "expected_current_acceptance": expected_acceptance,
            "reproduction": "PASS" if accepted == expected_acceptance else "FAIL",
        }


files = (
    "scripts/audit_requirement_controls.py", "scripts/build_content_trace.py", "scripts/audit_semantics.py",
    "docs/C01-PROMPT-INVESTIGACION.md", "docs/secciones/014-13-13-escalas-tasas-y-recuentos.md",
    "docs/auditorias/DIAGNOSTICO_INDEPENDIENTE_SECCION16_2026-09-27.md",
    "docs/auditorias/controles_requisitos/R-0393.csv",
    str(Path(__file__).relative_to(ROOT)),
)
before = {name: sha((ROOT / name).read_bytes()) for name in files}
prose_path = ROOT / files[4]
live_text = prose_path.read_text().splitlines()[164]
live_segments = [asdict(s) for s in trace.narrative_segments() if s.path == files[4] and s.locator.startswith("L165")]
cases = [run_case(case) for case in CASES]
process = subprocess.run([sys.executable, "scripts/audit_requirement_controls.py", "--root", ".", "--requirement", "R-0393"], cwd=ROOT, text=True, capture_output=True, check=False)
after = {name: sha((ROOT / name).read_bytes()) for name in files}
result = {
    "utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "scope": "Diagnóstico independiente de automatización R0393 y segmentación; sin implementar ni firmar cumplimiento",
    "hashes_before": before, "hashes_after": after, "inputs_stable": before == after,
    "cases": cases, "reproductions": len(cases), "passed": sum(c["reproduction"] == "PASS" for c in cases),
    "live_case": {"path": files[4], "line": 165, "text": live_text,
        "sha256_text_lf": sha((live_text + "\n").encode()), "split_sentences": trace.split_sentences(live_text),
        "segments": live_segments},
    "live_R0393": {"exit": process.returncode, "stdout": process.stdout, "stderr": process.stderr},
}
print(json.dumps(result, ensure_ascii=False, indent=2))
