# Verification Receipts

## Schema and Validation (Enforced by CI)

- Schema dialect: Draft-07 (`$schema: "http://json-schema.org/draft-07/schema#"`)
- Unicode guard: `python3 tools/unicode_guard.py`
- Schema meta-validation: `python3 tools/check_schemas.py`
- JSONL instance validation: `python3 tools/validate_jsonl.py --schema schemas/autonomy_journal.v1.autonomy.schema.json proofs/*.jsonl`
- Determinism token: `DETERMINISM_MATCH sha256:<hash>` (emitted by `tools/make_proofs.sh`)

## CI Receipts

Workflow:
https://github.com/SagaGonzo/autonomy-journal/actions/workflows/ci.yml

Expected tokens (must appear in CI logs):
- UNICODE_GUARD_PASS
- PII_SCAN_PASS
- SCHEMA_CHECK_PASS schemas/autonomy_journal.v1.autonomy.schema.json
- JSONL_SCHEMA_VALIDATE_PASS proofs/run1.jsonl:1
- JSONL_SCHEMA_VALIDATE_PASS proofs/run2.jsonl:1
- DETERMINISM_MATCH sha256:...
- PROOFS_OK

## PyPI

Status: **UNVERIFIED** (canonical project/version URLs return 404).

Do not claim publication until the canonical URL returns 200 and you paste receipts:
- `pip install autonomy-journal==<version>`
- `python -c "import autonomy_journal; print(autonomy_journal.__version__)"`
- `pip hash autonomy_journal-<version>-py3-none-any.whl`
