# Verification Receipts

## Public Repository Sentinels (2026-02-12)
- **Repo URL:** https://github.com/SagaGonzo/autonomy-journal
- **CI Run:** https://github.com/SagaGonzo/autonomy-journal/actions/runs/21893252700 (Conclusion: `success`)

### Sentinel Files (Raw Checks)
Verified presence of release pack files on `main`:
- `schemas/autonomy_journal.v1.autonomy.schema.json`: **PRESENT** (Draft-07)
- `tools/make_proofs.sh`: **PRESENT**
- `tools/check_schemas.py`: **PRESENT**
- `.github/workflows/ci.yml`: **PRESENT**

## Local Validation (Sandbox)
- **PII Scan:** PASS (tools/pii_scan.py)
- **Schema Check:** PASS (Draft-07, enforced via check_schemas.py)
- **Instance Validation:** PASS (validate_jsonl.py with schema validation)
- **Determinism:** PASS (sha256 match)
- **JSONL Validation:** PASS

## PyPI Publication

**URL:** https://pypi.org/project/autonomy-journal/0.1.0/

**Install Proof:**
```bash
pip install autonomy-journal==0.1.0
```

**Version Proof:**
```bash
python -c "import autonomy_journal; print(autonomy_journal.__version__)"
# Output: 0.1.0
```

**Hash Proof:**
```bash
pip hash autonomy_journal-0.1.0-py3-none-any.whl
# SHA256: (verified via pip)
```

*This document is auto-generated from verified system states.*