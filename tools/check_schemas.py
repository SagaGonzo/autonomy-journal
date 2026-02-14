#!/usr/bin/env python3
"""
Schema Meta-Validator - Validates JSON Schema files themselves
Uses jsonschema.validators.validator_for to ensure schemas are spec-compliant.
Fail-closed design: exit 1 if any schema is invalid.
"""
import sys
import json
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validators
except ImportError:
    print("SCHEMA_CHECK_FAIL: jsonschema package not installed")
    print("Run: pip install jsonschema")
    sys.exit(1)


def validate_schema_file(schema_path):
    """
    Meta-validate a JSON Schema file.
    Returns (is_valid, error_message).
    """
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"JSON parse error: {e}"
    except Exception as e:
        return False, f"File read error: {e}"
    
    # Determine the appropriate validator class
    try:
        validator_class = validators.validator_for(schema)
    except Exception as e:
        return False, f"Could not determine validator: {e}"
    
    # Check the schema itself (meta-validation)
    try:
        validator_class.check_schema(schema)
    except jsonschema.SchemaError as e:
        return False, f"Schema validation error: {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"
    
    return True, None


def main():
    """Main entry point."""
    schemas_dir = Path('schemas')
    
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_FAIL: schemas/ directory not found")
        return 1
    
    schema_files = sorted(schemas_dir.glob('*.json'))
    
    if not schema_files:
        print("SCHEMA_CHECK_FAIL: No schema files found in schemas/")
        return 1
    
    all_valid = True
    
    for schema_file in schema_files:
        is_valid, error = validate_schema_file(schema_file)
        
        if is_valid:
            print(f"SCHEMA_CHECK_OK: {schema_file.name}")
        else:
            print(f"SCHEMA_CHECK_FAIL: {schema_file.name}")
            print(f"  Error: {error}")
            all_valid = False
    
    if all_valid:
        print("SCHEMA_CHECK_PASS")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
