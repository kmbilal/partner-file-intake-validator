#!/usr/bin/env bash
set -euo pipefail

# Move to project root (no matter where script is run from)
cd "$(dirname "$0")/.."

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies (first run only)
pip install -q -e . >/dev/null 2>&1 || true

echo "Running validation..."
python -m app

echo ""
echo "Outputs written to:"
ls -la sample_data/output

echo ""
echo "Top of rejected_records.csv:"
head -n 5 sample_data/output/rejected_records.csv

echo ""
echo "validation_report.json:"
cat sample_data/output/validation_report.json
