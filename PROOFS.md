# Verification Receipts

## Schema Validation (Draft-07)

This repository uses **JSON Schema Draft-07** for all schema definitions, as declared in the `$schema` field of `schemas/autonomy_journal.v1.autonomy.schema.json`.

All validation uses the `jsonschema` library's Draft-07 validator.

## CI Validation Gates

The CI pipeline enforces the following sequential validation gates:

1. **Unicode Guard** (`tools/unicode_guard.py`)
   - Detects hidden/bidirectional Unicode characters
   - Scans .jsonl files and dotfiles
   - Emits: `UNICODE_GUARD_PASS` or `UNICODE_GUARD_FAIL`

2. **PII Scan** (`tools/pii_scan.py`)
   - Scans for personally identifiable information
   - Uses allowlist from `tools/pii_allowlist.regex`
   - Emits: `PII_SCAN_PASS` or `PII_SCAN_FAIL`

3. **Schema Meta-Validation** (`tools/check_schemas.py`)
   - Validates that schema files are valid JSON Schema Draft-07
   - Uses `jsonschema.validators.validator_for()` and `Validator.check_schema()`
   - Emits: `SCHEMA_CHECK_PASS` or `SCHEMA_CHECK_FAIL`

4. **JSONL Instance Validation** (`tools/validate_jsonl.py`)
   - Validates JSONL records against schema using `jsonschema.validate()`
   - Performs full instance validation
   - Emits: `JSONL_VALIDATE_PASS` or `JSONL_VALIDATE_FAIL`

5. **Proof Generation** (`tools/make_proofs.sh`)
   - Generates deterministic proof receipts
   - Verifies reproducibility (run1 == run2)
   - Emits: `PROOFS_OK` or fails with exit 1

## Repository Version

- **Current Version**: 1.2.3 (as defined in `release_state.v1.2.3.json`)
- **Note**: This repository version is independent of any PyPI package claims

## Expected CI Tokens

A successful CI run emits these tokens in order:

```
UNICODE_GUARD_PASS
PII_SCAN_PASS
SCHEMA_CHECK_PASS
SCHEMA_CHECK_OK
JSONL_VALIDATE_PASS
DETERMINISM_MATCH
PROOFS_OK
```

## Verification

All validation scripts use fail-closed design:
- Exit with code 1 on any failure
- Use `set -euo pipefail` in bash scripts
- Emit explicit FAIL tokens on error

*This document reflects the enforced reality of the CI validation pipeline.*