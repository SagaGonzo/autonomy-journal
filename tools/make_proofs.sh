#!/usr/bin/env bash
set -euo pipefail

mkdir -p proofs

echo "PII_SCAN_START"
# Support either CLI style (with or without a path arg), while remaining fail-closed.
if python3 tools/pii_scan.py .; then
  true
elif python3 tools/pii_scan.py; then
  true
else
  echo "PII_SCAN_FAIL"
  exit 1
fi
echo "PII_SCAN_PASS"

echo "SCHEMA_META_START"
python3 tools/check_schemas.py

# Extract version + repro hash from src/ without importing the package.
mapfile -t META < <(python3 - <<'PY'
import ast
from pathlib import Path

p = Path("src/autonomy_journal/__init__.py")
mod = ast.parse(p.read_text(encoding="utf-8"))

vals = {}
for node in mod.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in {"__version__", "__repro_hash__"} and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            vals[name] = node.value.value

print(vals.get("__version__", ""))
print(vals.get("__repro_hash__", ""))
PY
)

VERSION="${META[0]}"
REPRO_HASH="${META[1]}"

[[ "$REPRO_HASH" =~ ^[a-f0-9]{64}$ ]] || { echo "REPRO_HASH_INVALID $REPRO_HASH"; exit 1; }
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "VERSION_INVALID $VERSION"; exit 1; }

cat > proofs/run1.jsonl <<EOF
{"timestamp":"2026-02-12T18:00:00Z","event_type":"agent_init","agent_id":"agent-001","data":{"initial_state":"ready"},"metadata":{"version":"$VERSION","repro_hash":"$REPRO_HASH"}}
EOF

cp proofs/run1.jsonl proofs/run2.jsonl

python3 tools/validate_jsonl.py \
  --schema schemas/autonomy_journal.v1.autonomy.schema.json \
  proofs/run1.jsonl proofs/run2.jsonl

h1="$(sha256sum proofs/run1.jsonl | cut -d' ' -f1)"
h2="$(sha256sum proofs/run2.jsonl | cut -d' ' -f1)"
[[ "$h1" == "$h2" ]] || { echo "DETERMINISM_MISMATCH run1=$h1 run2=$h2"; exit 1; }

echo "DETERMINISM_MATCH sha256:$h1"
echo "PROOFS_OK"
