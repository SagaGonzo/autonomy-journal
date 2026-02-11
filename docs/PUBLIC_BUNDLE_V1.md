# Public Bundle V1

## Overview

This bundle represents the first public release of the Autonomy Journal system, containing all necessary components for deterministic, schema-first JSONL logging for agent simulations.

## Bundle Contents

### Core Documentation
- README.md - Project overview
- LICENSE - MIT License
- CITATION.cff - Citation information
- CODE_OF_CONDUCT.md - Community guidelines
- SECURITY.md - Security policy
- ETHICS.md - Ethical framework
- PROOFS.md - Verification receipts
- MISSION.md - Optimization protocol

### Schemas
- `schemas/autonomy_journal.v1.autonomy.schema.json` - Main journal schema
- `schemas/reality_state.v1.schema.json` - Reality state schema

### Tools
- `tools/pii_scan.py` - PII detection and scanning
- `tools/pii_allowlist.regex` - Allowed PII patterns
- `tools/validate_jsonl.py` - JSONL validation
- `tools/make_proofs.sh` - Generate verification proofs

### Source Code
- `src/autonomy_journal/` - Core Python package

### CI/CD
- `.github/workflows/ci.yml` - Continuous integration
- `.github/workflows/release.yml` - Release automation

## Usage

1. Install the package: `pip install -e .`
2. Validate schemas: `python tools/validate_jsonl.py`
3. Run PII scan: `python tools/pii_scan.py`
4. Generate proofs: `bash tools/make_proofs.sh`

## Version

v1.2.3 (2026-02-11)
