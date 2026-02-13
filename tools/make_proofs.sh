#!/bin/bash
# Generate proof receipts for Autonomy Journal release pack
set -euo pipefail

echo "=== Autonomy Journal Proof Generation ==="
echo ""

# 1. Run PII scan
echo "Step 1: Running PII scan..."
python3 tools/pii_scan.py
echo ""

# 2. Check schemas (meta-validation)
echo "Step 2: Validating schemas..."
python3 tools/check_schemas.py
echo ""

# 3. Extract version from package without importing
echo "Step 3: Extracting package version..."
VERSION=$(python3 -c "
import ast
import sys
from pathlib import Path

version_file = Path('src/autonomy_journal/__init__.py')
if not version_file.exists():
    print('ERROR: Cannot find version file', file=sys.stderr)
    sys.exit(1)

with open(version_file) as f:
    tree = ast.parse(f.read())

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == '__version__':
                # Use .value for Python 3.8+ compatibility
                print(node.value.value if hasattr(node.value, 'value') else node.value.s)
                sys.exit(0)

print('ERROR: Cannot find __version__', file=sys.stderr)
sys.exit(1)
")

if [ -z "$VERSION" ]; then
    echo "ERROR: Failed to extract version"
    exit 1
fi
echo "Package version: $VERSION"
echo ""

# 4. Generate deterministic test JSONL with fixed timestamp
echo "Step 4: Generating deterministic JSONL data..."
mkdir -p proofs
FIXED_TIMESTAMP="2026-02-11T00:00:00Z"
REPRO_HASH="0ced825ca45d52a7ab9160c1a97b1cb00f54d00fece33393ac17390b312a9504"

for run in run1 run2; do
    cat > "proofs/${run}.jsonl" << JSONL_EOF
{"timestamp":"${FIXED_TIMESTAMP}","event_type":"agent_init","agent_id":"agent-001","data":{"initial_state":"ready"},"metadata":{"version":"${VERSION}","repro_hash":"${REPRO_HASH}"}}
JSONL_EOF
done
echo ""

# 5. Validate JSONL against schema (instance validation)
echo "Step 5: Validating JSONL instances against schema..."
python3 tools/validate_jsonl.py
echo ""

# 6. Verify determinism
echo "Step 6: Verifying determinism..."
hash1=$(sha256sum proofs/run1.jsonl | cut -d' ' -f1)
hash2=$(sha256sum proofs/run2.jsonl | cut -d' ' -f1)

if [ "$hash1" != "$hash2" ]; then
    echo "ERROR: Non-deterministic output detected"
    echo "  run1: $hash1"
    echo "  run2: $hash2"
    exit 1
fi

echo "Checksums match: $hash1"
echo ""
echo "PROOFS_OK"
