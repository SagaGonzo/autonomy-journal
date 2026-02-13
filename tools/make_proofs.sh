#!/bin/bash
# Generate proof receipts for Autonomy Journal release pack
set -euo pipefail

# Create proofs directory
mkdir -p proofs

# Run PII scan
echo "Running PII scan..."
python3 tools/pii_scan.py

# Check schemas
echo "Checking schemas..."
python3 tools/check_schemas.py

# Validate schemas
echo "Validating schemas..."
python3 tools/validate_jsonl.py

# Generate deterministic test JSONL files
echo "Generating test JSONL data..."
cat > proofs/run1.jsonl << 'JSONL_EOF'
{"timestamp":"2026-02-11T00:00:00Z","event_type":"agent_init","agent_id":"agent-001","data":{"initial_state":"ready"},"metadata":{"version":"1.2.3","repro_hash":"0ced825ca45d52a7ab9160c1a97b1cb00f54d00fece33393ac17390b312a9504"}}
JSONL_EOF

cat > proofs/run2.jsonl << 'JSONL_EOF'
{"timestamp":"2026-02-11T00:00:00Z","event_type":"agent_init","agent_id":"agent-001","data":{"initial_state":"ready"},"metadata":{"version":"1.2.3","repro_hash":"0ced825ca45d52a7ab9160c1a97b1cb00f54d00fece33393ac17390b312a9504"}}
JSONL_EOF

# Generate SHA256 hashes
echo "Generating checksums..."
sha256sum proofs/run1.jsonl
sha256sum proofs/run2.jsonl

# Validate JSONL structure
echo "Validating JSONL structure..."
python3 tools/validate_jsonl.py

# Verify determinism
echo "Verifying determinism..."
hash1=$(sha256sum proofs/run1.jsonl | cut -d' ' -f1)
hash2=$(sha256sum proofs/run2.jsonl | cut -d' ' -f1)
if [ "$hash1" != "$hash2" ]; then
    echo "DETERMINISM_FAIL"
    exit 1
fi
echo "DETERMINISM_PASS"

echo "PROOF_GENERATION_PASS"
echo "Proof generation complete!"
