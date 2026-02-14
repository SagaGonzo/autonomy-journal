# Verification Receipts

## Public Repository Sentinels (2026-02-11)
- **Repo URL:** https://github.com/SagaGonzo/autonomy-journal
- **CI Status:** Automated validation via GitHub Actions

### Verification Process
The repository implements a multi-layer verification system:

1. **Unicode Guard** (`tools/unicode_guard.py`)
   - Scans all tracked files for hidden/malicious Unicode characters
   - Detects BIDI overrides, zero-width characters, and suspicious Unicode
   - **Status:** PASS (no hidden characters detected)

2. **PII Scan** (`tools/pii_scan.py`)
   - Scans JSONL files for personally identifiable information
   - Uses allowlist-based pattern matching
   - **Status:** PASS (no PII leakage)

3. **Schema Meta-Validation** (`tools/check_schemas.py`)
   - Validates JSON Schema files using `jsonschema.validators.validator_for`
   - Ensures schemas are spec-compliant (JSON Schema Draft-07)
   - **Status:** PASS (all schemas valid)

4. **JSONL Instance Validation** (`tools/validate_jsonl.py`)
   - Validates JSONL event logs against schemas
   - Performs full JSON Schema validation, not just parsing
   - **Status:** PASS (all instances conform to schema)

5. **Determinism Verification** (`tools/make_proofs.sh`)
   - Generates deterministic proof files with fixed timestamps
   - Verifies SHA256 hash consistency across runs
   - Uses fail-closed design (`set -euo pipefail`)
   - **Status:** PASS (deterministic output verified)

### JSON Schema Specification
- **Draft Version:** JSON Schema Draft-07
- **Schema Files:**
  - `schemas/autonomy_journal.v1.autonomy.schema.json`
  - `schemas/reality_state.v1.schema.json`

### PyPI Package Status
- **Status:** UNVERIFIED
- Package verification receipts will be added when available from PyPI attestations

### Sentinel Files (Repository State)
Verified presence of release pack files on `main`:
- `schemas/autonomy_journal.v1.autonomy.schema.json`: **PRESENT**
- `tools/make_proofs.sh`: **PRESENT**
- `tools/unicode_guard.py`: **PRESENT**
- `tools/check_schemas.py`: **PRESENT**
- `tools/validate_jsonl.py`: **PRESENT**
- `.github/workflows/ci.yml`: **PRESENT**

*This document reflects the automated verification state. All validation tools use fail-closed design and emit standardized tokens.*