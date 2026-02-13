# Verification Receipts

## Verification Process

This repository implements a comprehensive verification pipeline to ensure code integrity, security, and deterministic behavior.

### Validation Steps (in order)

1. **Unicode Guard** (`tools/unicode_guard.py`)
   - Scans for hidden Unicode characters (BIDI overrides, zero-width characters, NBSP-like)
   - Acts as security gatekeeper against supply chain attacks
   - Status: ✓ PASS

2. **PII Scan** (`tools/pii_scan.py`)
   - Detects personally identifiable information in JSONL files
   - Uses allowlist for expected patterns
   - Status: ✓ PASS

3. **Schema Meta-Validation** (`tools/check_schemas.py`)
   - Validates JSON schemas using `jsonschema.validators.validator_for`
   - Ensures schemas are well-formed and conform to **JSON Schema Draft-07**
   - Status: ✓ PASS

4. **JSONL Instance Validation** (`tools/validate_jsonl.py`)
   - Validates JSONL files against schemas (full instance validation)
   - Verifies all events conform to schema requirements
   - Status: ✓ PASS

5. **Deterministic Proof Generation** (`tools/make_proofs.sh`)
   - Generates reproducible JSONL outputs
   - Verifies version and repro_hash consistency
   - Confirms deterministic behavior via SHA256 comparison
   - Status: ✓ PASS

## Schema Information

- **Schema Version:** JSON Schema Draft-07
- **Primary Schema:** `schemas/autonomy_journal.v1.autonomy.schema.json`
- **Reality State Schema:** `schemas/reality_state.v1.schema.json`

## Public Repository Sentinels

- **Repo URL:** https://github.com/SagaGonzo/autonomy-journal
- **CI Status:** Automated via GitHub Actions (`.github/workflows/ci.yml`)
- **Latest CI Run:** See Actions tab for current status

### Verified Files on `main` Branch

- `schemas/autonomy_journal.v1.autonomy.schema.json`: ✓ PRESENT
- `schemas/reality_state.v1.schema.json`: ✓ PRESENT
- `tools/unicode_guard.py`: ✓ PRESENT
- `tools/check_schemas.py`: ✓ PRESENT
- `tools/validate_jsonl.py`: ✓ PRESENT
- `tools/make_proofs.sh`: ✓ PRESENT
- `.github/workflows/ci.yml`: ✓ PRESENT

## PyPI Distribution Status

**Status:** UNVERIFIED

PyPI receipts are not currently available. This document will be updated when PyPI distribution is verified with cryptographic receipts.

## Reproducibility Notes

- All proof JSONL files are generated deterministically
- Version and repro_hash are extracted from `release_state.*.json` without importing the package
- Timestamps in generated proofs are fixed for reproducibility
- SHA256 checksums verify bit-for-bit reproducibility

---

*This document reflects the current state of the verification system. Last updated: 2026-02-13*