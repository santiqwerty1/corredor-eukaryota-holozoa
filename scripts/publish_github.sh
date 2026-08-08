#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-santiqwerty1/corredor-eukaryota-holozoa}"
VISIBILITY="${VISIBILITY:-private}"

if ! command -v gh >/dev/null 2>&1; then
  echo "Falta GitHub CLI (gh)." >&2
  echo "Instálalo y ejecuta: gh auth login" >&2
  exit 1
fi

gh auth status
python scripts/render.py --check
python scripts/audit_migration.py
python scripts/validate.py

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "El árbol de trabajo tiene cambios sin confirmar." >&2
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  echo "El remoto origin ya existe: $(git remote get-url origin)"
else
  if gh repo view "$TARGET" >/dev/null 2>&1; then
    git remote add origin "git@github.com:${TARGET}.git"
  else
    gh repo create "$TARGET" "--${VISIBILITY}" --source . --remote origin
  fi
fi

git push -u origin main
echo "Publicado en https://github.com/${TARGET}"
