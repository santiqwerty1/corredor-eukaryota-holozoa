.PHONY: render validate audit check verify verify-core test fetch-oa

PYTHON ?= python3

render:
	$(PYTHON) scripts/render.py

validate:
	$(PYTHON) scripts/validate.py

audit:
	$(PYTHON) scripts/audit_migration.py
	$(PYTHON) scripts/audit_semantics.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

verify-core:
	$(PYTHON) scripts/render.py --check
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/audit_migration.py
	$(PYTHON) scripts/build_table_lineage.py --check
	$(PYTHON) scripts/build_content_trace.py --check
	$(PYTHON) scripts/audit_semantics.py
	$(PYTHON) scripts/audit_requirement_controls.py --root . --verify-artifacts
	$(PYTHON) scripts/audit_full.py
	$(MAKE) test

verify: verify-core
	$(PYTHON) scripts/check_render_idempotence.py
	git diff --check
	$(PYTHON) scripts/check_untracked_whitespace.py
	@if [ "$${AUDIT_ISOLATED_CHILD:-0}" != "1" ]; then \
		$(PYTHON) scripts/check_isolated_verify.py; \
	fi

check: verify

# Descarga las fuentes del apéndice A que están en acceso abierto y deja
# constancia, una a una, de las que no. MAILTO es obligatorio: OpenAlex y
# Europe PMC piden identificar a quien consulta.
fetch-oa:
	@test -n "$(MAILTO)" || (echo "uso: make fetch-oa MAILTO=tu@correo"; exit 1)
	$(PYTHON) scripts/fetch_oa.py --mailto "$(MAILTO)"
