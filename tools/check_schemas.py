#!/usr/bin/env python3
"""
JSON Schema Meta-Validator for Autonomy Journal

Validates that schema files are:
1. Valid JSON
2. Valid JSON Schema (Draft-07 enforced)
3. Have correct $schema declaration

This runs AFTER unicode_guard and pii_scan, BEFORE instance validation.
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import validators, Draft7Validator
    from jsonschema.exceptions import SchemaError
except ImportError:
    print("SCHEMA_CHECK_FAIL: jsonschema package not installed")
    print("Run: pip install jsonschema")
    sys.exit(1)


def check_schema_file(filepath):
    """Check a single schema file for validity."""
    try:
        # Load schema
        schema = json.loads(filepath.read_text(encoding="utf-8"))
        
        # Check for $schema declaration
        if "$schema" not in schema:
            return False, "Missing $schema declaration"
        
        # Enforce Draft-07 - check against known valid URIs
        VALID_DRAFT7_URIS = {
            "http://json-schema.org/draft-07/schema#",
            "http://json-schema.org/draft-07/schema",
            "https://json-schema.org/draft-07/schema#",
            "https://json-schema.org/draft-07/schema",
        }
        
        schema_uri = schema["$schema"]
        if schema_uri not in VALID_DRAFT7_URIS:
            return False, f"Not Draft-07 schema: {schema_uri}"
        
        # Validate schema structure using jsonschema library
        # This checks that the schema itself is valid
        Validator = validators.validator_for(schema)
        try:
            Validator.check_schema(schema)
        except SchemaError as e:
            return False, f"Invalid schema structure: {e.message}"
        
        # Ensure it's specifically Draft7Validator compatible
        if Validator != Draft7Validator:
            return False, f"Schema validator mismatch: expected Draft7, got {Validator.__name__}"
        
        return True, "OK"
        
    except json.JSONDecodeError as e:
        return False, f"JSON parse error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    """Validate all schema files in schemas/ directory."""
    schemas_dir = Path(__file__).parent.parent / "schemas"
    
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_FAIL: schemas/ directory not found")
        return 1
    
    schema_files = list(schemas_dir.glob("*.json"))
    
    if not schema_files:
        print("SCHEMA_CHECK_FAIL: No schema files found in schemas/")
        return 1
    
    all_passed = True
    
    for schema_file in sorted(schema_files):
        passed, message = check_schema_file(schema_file)
        
        if passed:
            print(f"SCHEMA_CHECK_PASS {schema_file.name}")
        else:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name}: {message}")
            all_passed = False
    
    if all_passed:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
