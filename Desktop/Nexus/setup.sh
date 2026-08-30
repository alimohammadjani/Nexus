#!/usr/bin/env bash
set -euo pipefail

echo "==> DevHub setup"
echo "==> Backend environment"
if [ ! -d "backend/.venv" ]; then
  python3 -m venv backend/.venv
fi
backend/.venv/bin/pip install -U pip
backend/.venv/bin/pip install -r backend/requirements.txt -r backend/requirements-dev.txt

echo "==> Frontend dependencies"
cd frontend
if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi
cd ..

echo "==> Backend tests"
(cd backend && .venv/bin/python -m pytest -q)

echo "Done. Run the API with: make api"
echo "Run the frontend with: make web"
