# Verification Receipts

## Public Repository Sentinels (2026-02-11)
- **Repo URL:** https://github.com/SagaGonzo/autonomy-journal
- **CI Run:** https://github.com/SagaGonzo/autonomy-journal/actions/runs/21893252700 (Conclusion: `success`)

### Sentinel Files (Raw Checks)
Verified presence of release pack files on `main`:
- `schemas/autonomy_journal.v1.autonomy.schema.json`: **PRESENT** (Draft-07)
- `tools/make_proofs.sh`: **PRESENT**
- `.github/workflows/ci.yml`: **PRESENT**

## Local Validation (Sandbox)
- **Unicode Guard:** PASS (tools/unicode_guard.py)
- **PII Scan:** PASS (tools/pii_scan.py)
- **Schema Check:** PASS (Draft-07 meta-validation)
- **Instance Validation:** PASS (JSONL against Draft-07 schemas)
- **Determinism:** PASS (sha256 match across runs)

## Schema Version
- **Verified Reality:** JSON Schema Draft-07
- **Schema Declaration:** `http://json-schema.org/draft-07/schema#`
- **PyPI jsonschema:** UNVERIFIED (implementation may vary)

*This document is auto-generated from verified system states.*