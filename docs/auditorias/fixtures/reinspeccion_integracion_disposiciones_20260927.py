"""Reinspección v2: integración 410/408/2 y 816 C, con seis deltas ficticios.

Copia data/docs a /tmp. No copia fuentes científicas ni cambia producción.
La biblioteca temporal solo permite las dos consultas positivas históricas y
contiene un artefacto inventado explícito para ejercitar los seis deltas.
"""
import contextlib
import copy
import csv
import hashlib
import io
import json
import runpy
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

n = runpy.run_path(str(Path(__file__).with_name("revision_disposiciones_independiente_20260927.py")))
ROOT, d, a, write, csvwrite, jsonwrite, sha = (n[k] for k in ("ROOT", "d", "a", "write", "csvwrite", "jsonwrite", "sha"))
from scripts import remediate_trace_residuals as r
KEYS = ("C-2708", "C-2712", "C-2794", "C-2797", "C-2798", "C-2801")
RESULTS = []


def insist(value, message):
    if not value:
        raise AssertionError(message)


def record(name, function):
    try:
        RESULTS.append({"case": name, "result": "PASS", "detail": function()})
    except Exception as exc:
        RESULTS.append({"case": name, "result": "FAIL", "detail": f"{type(exc).__name__}: {exc}"})


def patch_root(stack, module, root):
    for key, value in list(vars(module).items()):
        if isinstance(value, Path) and value.is_relative_to(ROOT):
            stack.enter_context(patch.object(module, key, root / value.relative_to(ROOT)))
        elif isinstance(value, tuple) and value and all(isinstance(x, Path) and x.is_relative_to(ROOT) for x in value):
            stack.enter_context(patch.object(module, key, tuple(root / x.relative_to(ROOT) for x in value)))


class Integration:
    def __init__(self, root):
        self.root = root
        shutil.copytree(ROOT / "data", root / "data")
        shutil.copytree(ROOT / "docs", root / "docs")
        self.before_residual = r.RESIDUALS.read_bytes()
        self.before_targets = {p: p.read_bytes() for p in r.TARGETS}
        self.residuals = r.read_csv(r.RESIDUALS)[1]
        self.target_by = {x["claim_id"]: x for p in r.TARGETS for x in r.read_csv(p)[1]}
        self.fake = write(root, "fuentes/S999 ensayo.txt", "Documento artificial de integración. No constituye evidencia científica.\n")
        components = [component for residual in self.residuals if residual["claim_id"] in r.POSITIVE_CLAIMS for component in r.nominal_components(r.nominal_query(residual))]
        write(root, "fuentes/S998 positivas artificiales.txt", "\n".join(components))
        self.author = write(root, "docs/propuesta_fixture.md", "Seis propuestas artificiales. No usar como firma del corpus real.")
        header, claims = r.read_csv(r.CLAIMS)
        self.support = []
        for i, key in enumerate(KEYS):
            claim = dict.fromkeys(header, "Fixture artificial, no aprueba ciencia")
            claim.update({"#": f"C-{9000+i}", "Afirmación": f"Dato artificial {i}.", "Atribución": "expresa", "Fuente": "S999 párrafo 1", "Fuerza": "alta"})
            self.support.append(claim)
        csvwrite(root, r.CLAIMS.relative_to(root), header, claims + self.support)
        # Ejecutar ambos builders sin disposiciones primero, en la misma copia.
        self.baseline, self.probes_before = r.build()
        self.apply(self.baseline)
        self.records = []
        ch, corrections = r.read_csv(r.CORRECTIONS)
        for key, support in zip(KEYS, self.support):
            index, residual = next((i, x) for i, x in enumerate(self.residuals) if x["claim_id"] == key)
            target = self.target_by[key]
            identity = {k: residual[k] for k in ("claim_id", "csv_path", "fila", "columna")}
            value = f"Valor artificial de integración [{support['#']}]"
            correction = {**identity, "contenido_previo": target["contenido"], "contenido_previo_sha256": target["contenido_sha256"], "contenido_corregido": value, "contenido_corregido_sha256": d.cell_hash(value), "autor_correccion": "Autor-Integracion", "evidencia_correccion": "docs/propuesta_fixture.md"}
            corrections.append(correction)
            entry = {**identity, "bn": f"BN-{r.START_BN+index:03d}", "sha256_residual": d.row_hash(residual), "contenido_previo": target["contenido"], "sha256_previo": target["contenido_sha256"], "contenido_nuevo": value, "sha256_nuevo": d.cell_hash(value), "autor": "Autor-Integracion", "fecha_utc": "2026-09-27T01:00:00Z", "componentes": [f"componente ficticio {key}"], "limites_pendientes": "No es una afirmación científica; solo integración ficticia.", "afirmaciones_soporte": {support["#"]: d.row_hash(support)}, "artefactos_soporte": {"fuentes/S999 ensayo.txt": sha(self.fake)}, "evidencia_autor": {"ruta": "docs/propuesta_fixture.md", "sha256": sha(self.author)}}
            _, live_rows = r.read_csv(root / residual["csv_path"])
            live_row = live_rows[int(residual["fila"])-2]
            first = next(iter(live_row))
            names = [first] + [name for name in ("taxón o sistema", "magnitud")
                              if name in live_row and name not in {first, residual["columna"]}]
            entry["identidad_fila"] = {name: live_row[name].strip() for name in names}
            review = {"version": 1, "claim_id": key, "disposicion_sha256": d.proposal_hash(entry), "revisor": "Revisor-Integracion", "fecha_utc": "2026-09-27T01:01:00Z", "dictamen": "CONFORME", "independencia": d.DECLARATION, "cobertura": {f"componente ficticio {key}": [0]}, "pasajes": [{"artefacto": "fuentes/S999 ensayo.txt", "sha256_artefacto": sha(self.fake), "localizador": "párrafo 1", "fragmento_control": "Documento artificial de integración.", "sha256_pasaje": hashlib.sha256(b"Documento artificial de integracion.").hexdigest()}], "limitaciones": "Prueba de infraestructura, no revisión científica."}
            p = jsonwrite(root, f"docs/revision_fixture_{key}.json", review)
            entry["revision_independiente"] = {"ruta": p.relative_to(root).as_posix(), "sha256": sha(p)}
            self.records.append(entry)
        csvwrite(root, r.CORRECTIONS.relative_to(root), ch, corrections)
        jsonwrite(root, d.REGISTRY, {"version": 1, "disposiciones": self.records})

    def apply(self, payloads):
        for path, raw in payloads.items():
            path.write_bytes(raw)

    def good_remediation(self):
        payloads, probes = r.build()
        insist(len(probes) == 408 and all(v[1] == 0 for v in probes.values()), "No conserva 408 negativas")
        insist(probes == self.probes_before, "Cambian términos/resultados históricos")
        insist(len(self.residuals) == 410 and r.POSITIVE_CLAIMS == {"C-2472", "C-2489"}, "Cambió universo 410/408/2")
        insist(r.RESIDUALS.read_bytes() == self.before_residual, "Reescribió residuales")
        for path, raw in payloads.items():
            if path.parent.name == "busquedas_negativas":
                insist(raw == self.baseline[path], "Cambió una BN histórica por disposición")
        for path in r.TARGETS:
            insist(payloads[path] == self.baseline[path], "Reescribió objetivos históricos por disposición")
        self.apply(payloads)
        again, probes_again = r.build()
        insist(payloads == again and probes == probes_again, "Remediación no idempotente")
        return payloads


@contextlib.contextmanager
def integrated():
    with tempfile.TemporaryDirectory() as raw, contextlib.ExitStack() as stack:
        root = Path(raw)
        patch_root(stack, r, root)
        patch_root(stack, a, root)
        yield Integration(root)


def six():
    with integrated() as f:
        f.good_remediation()
        claims_raw, manifest_raw, ids = a.build()
        insist(len(ids) == 816, "No conserva 816 C")
        claims = {x["#"]: x for x in csv.DictReader(io.StringIO(claims_raw.decode()))}
        leaked = []
        for key, support in zip(KEYS, f.support):
            row = claims[key]
            insist(row["Atribución"] == f"sintesis({support['#']})", "Herencia de C ajenas: " + row["Atribución"])
            if "BN-" in row["Fuente"]:
                leaked.append({"C": key, "Fuente": row["Fuente"]})
        a.CLAIMS.write_bytes(claims_raw)
        a.MANIFEST.write_bytes(manifest_raw)
        again = a.build()
        insist((claims_raw, manifest_raw, ids) == again, "Atómicas no idempotentes")
        insist(not leaked, "Hereda BN ajenas pese a excluir dependencias históricas: " + json.dumps(leaked, ensure_ascii=False))
        return "6 deltas; 410/408/2, consultas/BN/historia intactas, 816C, solo nuevas dependencias e idempotencia."


def remediation_race():
    with integrated() as f:
        original = r.source_snapshot
        def mutate_after_validation():
            f.fake.write_bytes(f.fake.read_bytes() + b" Changed after validation.")
            return original()
        with patch.object(r, "source_snapshot", side_effect=mutate_after_validation):
            try:
                payloads, _ = r.build()
            except RuntimeError as exc:
                return "Rechazo: " + str(exc)
        insist(not any(x["contenido_nuevo"].encode() in payloads[f.root / x["csv_path"]] for x in f.records), "Materializa los seis deltas después de cambiar su artefacto ya validado")


def atomic_race():
    with integrated() as f:
        f.good_remediation()
        original = r.semantic_dispositions
        changed_value = "CAMBIO POSTERIOR NO REVISADO [C-9000]"
        def validate_then_change(*args, **kwargs):
            result = original(*args, **kwargs)
            header, corrections = r.read_csv(r.CORRECTIONS)
            entry = next(x for x in corrections if x["claim_id"] == KEYS[0])
            entry["contenido_corregido"] = changed_value
            entry["contenido_corregido_sha256"] = d.cell_hash(changed_value)
            csvwrite(f.root, r.CORRECTIONS.relative_to(f.root), header, corrections)
            target = f.records[0]
            header, rows = r.read_csv(f.root / target["csv_path"])
            rows[int(target["fila"])-2][target["columna"]] = changed_value
            csvwrite(f.root, target["csv_path"], header, rows)
            # El manifiesto conserva la versión histórica admitida por el builder.
            header, rows = r.read_csv(a.MANIFEST)
            for row in rows:
                if all(row[k] == target[k] for k in ("csv_path", "fila", "columna")):
                    row["contenido"] = target["contenido_previo"]
                    row["contenido_sha256"] = target["sha256_previo"]
            csvwrite(f.root, a.MANIFEST.relative_to(f.root), header, rows)
            return result
        with patch.object(r, "semantic_dispositions", side_effect=validate_then_change):
            try:
                claims_raw, _, _ = a.build()
            except RuntimeError as exc:
                return "Rechazo: " + str(exc)
        insist(changed_value.encode() not in claims_raw, "La C atómica materializa corrección distinta de la propuesta validada")


record("six_dispositions_full_build_history_dependencies_idempotence", six)
record("remediation_source_changed_after_disposition_validation", remediation_race)
record("atomic_correction_changed_after_disposition_validation", atomic_race)
print(json.dumps({"utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "hashes": {p: sha(ROOT / p) for p in ("scripts/residual_semantic_dispositions.py", "scripts/remediate_trace_residuals.py", "scripts/build_atomic_cell_claims.py", str(Path(__file__).relative_to(ROOT)))}, "tests": len(RESULTS), "passed": sum(x["result"] == "PASS" for x in RESULTS), "results": RESULTS}, ensure_ascii=False, indent=2))
