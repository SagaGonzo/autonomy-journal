# Verification Receipts

## Schema Validation

**JSON Schema Version:** Draft-07 (`http://json-schema.org/draft-07/schema#`)

All schemas in `schemas/` are meta-validated using `jsonschema.validators.validator_for()` and `Validator.check_schema()`.

## Security Gates

The following security checks are enforced in CI:

1. **Unicode Guard** (`tools/unicode_guard.py`)
   - Detects hidden Unicode characters (BIDI overrides, zero-width characters, NBSP)
   - Scans all source files (`.py`, `.sh`, `.yml`, `.json`, `.jsonl`, `.md`, etc.)
   - Fails if dangerous characters are found

2. **PII Scan** (`tools/pii_scan.py`)
   - Scans for personally identifiable information
   - Uses allowlist to exclude false positives

3. **Schema Meta-Validation** (`tools/check_schemas.py`)
   - Validates that schemas themselves are valid JSON schemas
   - Ensures compliance with JSON Schema Draft-07

4. **Instance Validation** (`tools/validate_jsonl.py`)
   - Validates JSONL data against schemas using full `jsonschema.validate()`
   - Enforces schema constraints on all event logs

5. **Determinism Check** (`tools/make_proofs.sh`)
   - Generates proof runs with fixed timestamps
   - Verifies SHA256 checksums match between runs
   - Extracts version from package using AST parsing (no imports)

## CI Workflow

The CI pipeline runs validation steps in this order:
```bash
python3 tools/unicode_guard.py
python3 tools/pii_scan.py
python3 tools/check_schemas.py
bash tools/make_proofs.sh  # includes validate_jsonl.py
```

All scripts use fail-closed design (`set -euo pipefail` for bash, `exit 1` on failure for Python).

## Public Repository Status (2026-02-13)

- **Repository:** https://github.com/SagaGonzo/autonomy-journal
- **CI Status:** Latest runs available at Actions tab
- **Schema Files:** Present in `schemas/` directory
- **Validation Tools:** Present in `tools/` directory

## PyPI Status

**UNVERIFIED** - PyPI package receipts not yet available. Wait for release and verify package hashes against repository source.

## Verification Instructions

To verify locally:
```bash
# Clone repository
git clone https://github.com/SagaGonzo/autonomy-journal.git
cd autonomy-journal

# Install dependencies
pip install jsonschema

# Run full validation
python3 tools/unicode_guard.py
python3 tools/pii_scan.py
python3 tools/check_schemas.py
python3 tools/validate_jsonl.py
bash tools/make_proofs.sh
```

All validation scripts emit verification tokens:
- `UNICODE_GUARD_PASS` / `UNICODE_GUARD_FAIL`
- `PII_SCAN_PASS`
- `SCHEMA_CHECK_PASS` / `SCHEMA_CHECK_FAIL`
- `JSONL_SCHEMA_VALIDATE_PASS` / `JSONL_SCHEMA_VALIDATE_FAIL`
- `PROOFS_OK`

*This document reflects the verified state as of CI implementation. Always check latest CI runs for current status.*