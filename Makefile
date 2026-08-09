.PHONY: render validate audit check verify verify-core test

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
