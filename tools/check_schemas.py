#!/usr/bin/env python3
"""
Schema Meta-Validator for Autonomy Journal
Validates that schema files are valid JSON Schemas using jsonschema library.
"""
import json
import sys
from pathlib import Path
from jsonschema import validators

def main() -> int:
    """Validate all schema files in schemas/ directory."""
    schemas_dir = Path("schemas")
    if not schemas_dir.exists():
        print("ERROR: schemas/ directory not found")
        return 1
    
    schema_files = sorted(schemas_dir.glob("*.json"))
    if not schema_files:
        print("ERROR: No schema files found in schemas/")
        return 1
    
    all_valid = True
    for schema_path in schema_files:
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            Validator = validators.validator_for(schema)
            Validator.check_schema(schema)
            print(f"SCHEMA_CHECK_PASS {schema_path.name}")
        except Exception as e:
            all_valid = False
            print(f"SCHEMA_CHECK_FAIL {schema_path.name}: {e}")
    
    if all_valid:
        print("SCHEMA_META_VALIDATE_PASS")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
