# Verification Receipts

## Public Repository Sentinels (2026-02-11)
- **Repo URL:** https://github.com/SagaGonzo/autonomy-journal
- **CI Run:** https://github.com/SagaGonzo/autonomy-journal/actions/runs/21893252700 (Conclusion: `success`)

### Sentinel Files (Raw Checks)
Verified presence of release pack files on `main`:
- `schemas/autonomy_journal.v1.autonomy.schema.json`: **PRESENT**
- `tools/make_proofs.sh`: **PRESENT**
- `.github/workflows/ci.yml`: **PRESENT**

## Local Validation (Sandbox)
- **PII Scan:** PASS (tools/pii_scan.py)
- **Unicode Guard:** PASS (tools/unicode_guard.py)
- **Schema Meta-Validation:** PASS (tools/check_schemas.py - Draft-07)
- **JSONL Structure:** PASS (tools/validate_jsonl.py)
- **Determinism:** PASS (sha256 match)
- **Proof Generation:** PASS (tools/make_proofs.sh)

*This document is auto-generated from verified system states.*