#!/usr/bin/env bash
# One-command demo: tests, the calculator on a real Calgary scenario, then the HTML report.
set -e
cd "$(dirname "$0")/.."
pause() { [ -n "$DEMO_FAST" ] || sleep "${1:-2}"; }

echo "== 1. The research files the agents write (Glacier Ridge, Calgary) =="
head -20 examples/calgary/glacier-ridge.md
pause 3

echo; echo "== 2. Affordability with the Canadian rules, shown with every input =="
python3 scripts/affordability.py --price 665000 --down 66500 --rate 4.0 --years 25 \
  --insured --first-time --stress-auto --monthly-income 12500 --annual-fees 498.02
pause 3

echo; echo "== 3. Tests =="
python3 -m unittest discover -s tests 2>&1 | tail -3
pause 1

echo; echo "== 4. Shareable report =="
python3 scripts/build_report.py examples/calgary demo/report.html
command -v open >/dev/null && [ -z "$DEMO_FAST" ] && open demo/report.html || true
