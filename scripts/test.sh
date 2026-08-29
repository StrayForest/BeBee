#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
python3 tools/economy/p3_regression.py --output build/test-results/p3-economy-regression.json
exec python3 tools/defold/run_tests.py "$@"
