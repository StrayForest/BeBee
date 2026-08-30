#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
python3 tools/economy/p3_regression.py --output build/test-results/p3-economy-regression.json
python3 tools/economy/p5_seed_regression.py --output build/test-results/p5-seed-economy-regression.json
python3 tools/release/test_release_candidate.py
exec python3 tools/defold/run_tests.py "$@"
