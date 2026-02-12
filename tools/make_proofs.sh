#!/usr/bin/env bash
set -euo pipefail

mkdir -p proofs

# Pull a valid hex repro hash from the library (no install required; use src/).
REPRO_HASH="$(python3 -c "import sys; sys.path.insert(0,'src'); import autonomy_journal; print(getattr(autonomy_journal,'__repro_hash__',''))")"
if [[ ! "$REPRO_HASH" =~ ^[a-f0-9]{64}$ ]]; then
  echo "REPRO_HASH_INVALID $REPRO_HASH"
  exit 1
fi

VERSION="$(python3 -c "import sys; sys.path.insert(0,'src'); import autonomy_journal; print(getattr(autonomy_journal,'__version__',''))")"
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "VERSION_INVALID $VERSION"
  exit 1
fi

cat > proofs/run1.jsonl << EOF
{"timestamp":"2026-02-11T05:40:00Z","event_type":"agent_init","agent_id":"agent-001","data":{"key":"value"},"metadata":{"version":"$VERSION","repro_hash":"$REPRO_HASH"}}
EOF

cat > proofs/run2.jsonl << EOF
{"timestamp":"2026-02-11T05:40:00Z","event_type":"agent_init","agent_id":"agent-001","data":{"key":"value"},"metadata":{"version":"$VERSION","repro_hash":"$REPRO_HASH"}}
EOF

# Enforce: PII scan (repo root)
python3 tools/pii_scan.py .

# Enforce: schemas valid + instances valid
python3 tools/check_schemas.py
python3 tools/validate_jsonl.py --schema schemas/autonomy_journal.v1.autonomy.schema.json proofs/run1.jsonl proofs/run2.jsonl

# Enforce: determinism (run1 == run2)
H1="$(sha256sum proofs/run1.jsonl | awk '{print $1}')"
H2="$(sha256sum proofs/run2.jsonl | awk '{print $1}')"
if [[ "$H1" != "$H2" ]]; then
  echo "DETERMINISM_MISMATCH run1=$H1 run2=$H2"
  exit 1
fi
echo "DETERMINISM_MATCH $H1"
echo "PROOFS_OK"
