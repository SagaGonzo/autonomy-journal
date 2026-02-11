# EVAL1 Artifact Set

## Purpose

This artifact set contains the minimal reproducible environment for evaluating the Autonomy Journal system's deterministic logging and validation capabilities.

## Artifacts

### 1. Test Data
- `proofs/run1.jsonl` - First evaluation run
- `proofs/run2.jsonl` - Second evaluation run (must match run1 for determinism verification)

### 2. Validation Tools
- Schema validators (JSON Schema based)
- PII scanner
- JSONL structure validator

### 3. Expected Outputs
- SHA256 hashes of proof files must match
- All schemas must validate successfully
- PII scan must pass with no violations

## Verification Process

```bash
# Run validation
bash tools/make_proofs.sh

# Verify determinism
sha256sum proofs/run1.jsonl
sha256sum proofs/run2.jsonl
# Both should produce identical hashes
```

## Success Criteria

✓ Deterministic output (identical hashes)
✓ Schema validation passes
✓ PII scan passes
✓ JSONL structure valid

## Repro Hash

The expected repro_hash for this evaluation set is embedded in the source code and verified during each run.
