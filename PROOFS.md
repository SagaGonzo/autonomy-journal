# Verification Receipts

## Public Repository Sentinels (2026-02-11)
- **Repo URL:** https://github.com/SagaGonzo/autonomy-journal
- **CI Run:** https://github.com/SagaGonzo/autonomy-journal/actions/runs/21893252700 (Conclusion: `success`)

### Sentinel Files (Raw Checks)
Verified presence of release pack files on `main`:
- `schemas/autonomy_journal.v1.autonomy.schema.json`: **PRESENT**
- `tools/make_proofs.sh`: **PRESENT**
- `.github/workflows/ci.yml`: **PRESENT**

## Schema Validation
- **Schema Dialect:** JSON Schema Draft-07
- **$schema URI:** http://json-schema.org/draft-07/schema#
- **Meta-Validation:** PASS (via jsonschema.Draft7Validator.check_schema)

## CI Validation Gates (Expected Tokens)
The CI pipeline enforces the following validation sequence with sentinel tokens:

1. **UNICODE_GUARD_PASS** - No hidden or bidirectional Unicode detected
2. **PII_SCAN_PASS** - No PII policy violations
3. **SCHEMA_CHECK_PASS** - Schema meta-validation passed (Draft-07)
4. **JSONL_VALIDATE_PASS** - JSONL structure validation passed
5. **DETERMINISM_PASS** - SHA256 checksums match (run1.jsonl == run2.jsonl)
6. **PROOF_GENERATION_PASS** - Full proof generation pipeline succeeded

## Repository Version
- **Version:** 1.2.3 (as declared in release_state.v1.2.3.json)
- **Note:** No PyPI distribution verified - repository-only release

## Local Validation (Sandbox)
All validation gates passed in isolated sandbox environment:
- Unicode Guard: PASS
- PII Scan: PASS
- Schema Check: PASS (Draft-07)
- JSONL Validation: PASS
- Determinism: PASS (sha256 match)
- Proof Generation: PASS

*This document reflects the enforced validation reality as of 2026-02-11.*