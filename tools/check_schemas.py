#!/usr/bin/env python3
"""
Schema Validator for Autonomy Journal
Validates that all schema files are valid JSON Schema documents.
"""
import json
import sys
from pathlib import Path
from jsonschema import validators

def main():
    """Validate all schema files in schemas/ directory."""
    ok = True
    schemas_dir = Path("schemas")
    
    if not schemas_dir.exists():
        print("ERROR: schemas/ directory not found")
        return 1
    
    schema_files = sorted(schemas_dir.glob("*.json"))
    if not schema_files:
        print("ERROR: No schema files found in schemas/")
        return 1
    
    for p in schema_files:
        try:
            schema = json.loads(p.read_text(encoding="utf-8"))
            Validator = validators.validator_for(schema)
            Validator.check_schema(schema)
            print(f"SCHEMA_CHECK_PASS {p.name}")
        except Exception as e:
            print(f"SCHEMA_CHECK_FAIL {p.name}: {e}")
            ok = False
    
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
