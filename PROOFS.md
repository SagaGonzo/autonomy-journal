# Verification Receipts

## Schema Specification
- **JSON Schema Version:** Draft-07 (`http://json-schema.org/draft-07/schema#`)
- **Schema Files:**
  - `schemas/autonomy_journal.v1.autonomy.schema.json`
  - `schemas/reality_state.v1.schema.json`

## Verification Process (2026-02-11)

### 1. Security Gates
- **Unicode Guard:** Scans for hidden/dangerous Unicode characters (BIDI overrides, zero-width, NBSP)
  - Tool: `tools/unicode_guard.py`
  - Status: ✓ PASS
  
- **PII Scan:** Detects personally identifiable information in JSONL outputs
  - Tool: `tools/pii_scan.py`
  - Allowlist: `tools/pii_allowlist.regex`
  - Status: ✓ PASS

### 2. Schema Validation
- **Meta-Validation:** Validates schemas comply with JSON Schema Draft-07 specification
  - Tool: `tools/check_schemas.py`
  - Method: `jsonschema.validators.validator_for()` + `Validator.check_schema()`
  - Status: ✓ PASS

### 3. Instance Validation
- **JSONL Validation:** Validates JSONL data files against schemas
  - Tool: `tools/validate_jsonl.py`
  - Method: Full JSON Schema instance validation
  - Status: ✓ PASS

### 4. Determinism Check
- **Reproducibility:** Verifies identical output across multiple runs
  - Proof Files: `proofs/run1.jsonl`, `proofs/run2.jsonl`
  - Method: SHA256 checksum comparison
  - Status: ✓ PASS (matching checksums)

## Public Repository Status
- **Repository:** https://github.com/SagaGonzo/autonomy-journal
- **Branch:** main
- **Version:** 1.2.3
- **Repro Hash:** `0ced825ca45d52a7ab9160c1a97b1cb00f54d00fece33393ac17390b312a9504`

### CI Status
- **Latest Run:** https://github.com/SagaGonzo/autonomy-journal/actions
- **Validation Gates:** Unicode Guard → PII Scan → Schema Check → Proof Generation → JSONL Validation
- **Status:** All gates enforced in CI

## PyPI Distribution Status
- **Status:** UNVERIFIED
- **Note:** No PyPI distribution receipts available yet. This package is currently verified only via GitHub CI.

---

*This verification document reflects the state of validation tooling and processes.  
Generated output files (proofs/*.jsonl) are excluded from git tracking and regenerated in CI.*