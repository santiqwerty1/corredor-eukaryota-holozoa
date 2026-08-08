.PHONY: render validate audit check

render:
	python scripts/render.py

validate:
	python scripts/validate.py

audit:
	python scripts/audit_migration.py

check:
	python scripts/render.py --check
	python scripts/audit_migration.py
	python scripts/validate.py
