#!/usr/bin/env python3
"""
Schema Meta-Validator for Autonomy Journal
Validates that all JSON schemas in schemas/ are valid meta-schemas.
Uses jsonschema.validators.validator_for to ensure schemas are well-formed.
"""
import sys
import json
from pathlib import Path

try:
    from jsonschema import validators
    from jsonschema.exceptions import SchemaError
except ImportError:
    print("ERROR: jsonschema package not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)


def validate_schema_file(schema_path):
    """
    Meta-validate a single schema file using jsonschema.
    Returns (success: bool, error_message: str or None)
    """
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Cannot read file: {e}"
    
    try:
        # Get the appropriate validator class for this schema
        validator_class = validators.validator_for(schema)
        
        # Check the schema itself is valid
        validator_class.check_schema(schema)
        
        return True, None
    except SchemaError as e:
        return False, f"Schema validation error: {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    """Main validation function."""
    schemas_dir = Path('schemas')
    
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_FAIL: schemas/ directory not found")
        return 1
    
    schema_files = list(schemas_dir.glob('*.json'))
    
    if not schema_files:
        print("SCHEMA_CHECK_FAIL: No schema files found in schemas/")
        return 1
    
    print("Meta-validating JSON schemas...")
    all_valid = True
    
    for schema_file in sorted(schema_files):
        success, error = validate_schema_file(schema_file)
        
        if success:
            print(f"  ✓ {schema_file.name}")
        else:
            print(f"  ✗ {schema_file.name}")
            print(f"    {error}")
            all_valid = False
    
    if all_valid:
        print("\nSCHEMA_CHECK_PASS")
        return 0
    else:
        print("\nSCHEMA_CHECK_FAIL")
        return 1


if __name__ == '__main__':
    sys.exit(main())
