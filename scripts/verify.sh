#!/usr/bin/env bash
# Everything the CI runs: the corpus rebuilt and in sync, the seed in sync, and the tests.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 corpus/build.py && python3 scripts/seed_sql.py
git diff --exit-code corpus sql >/dev/null || { echo "corpus/ ou sql/ mudaram ao reconstruir: commite os arquivos gerados"; }
python3 -m pytest -q
