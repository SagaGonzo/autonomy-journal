#!/usr/bin/env python3
"""
Schema Meta-Validator
Validates that schema files themselves are valid JSON Schema documents.
Uses jsonschema.validators.validator_for() to check schema-of-schemas.
This is fail-closed: exits with code 1 on any failure.
"""
import sys
import json
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validators
except ImportError:
    print("SCHEMA_CHECK_FAIL: jsonschema library not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)

def validate_schema_file(schema_path):
    """Validate a single schema file as a meta-schema check."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Get the appropriate validator class for this schema
        validator_class = validators.validator_for(schema)
        
        # Check the schema itself (meta-validation)
        validator_class.check_schema(schema)
        
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except jsonschema.SchemaError as e:
        return False, f"Invalid schema: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"

def main():
    """Main meta-validation function."""
    schemas_dir = Path('schemas')
    
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_FAIL")
        print("ERROR: schemas/ directory not found")
        return 1
    
    schema_files = list(schemas_dir.glob('*.json'))
    
    if not schema_files:
        print("SCHEMA_CHECK_FAIL")
        print("ERROR: No schema files found in schemas/")
        return 1
    
    all_valid = True
    for schema_file in sorted(schema_files):
        valid, error = validate_schema_file(schema_file)
        if valid:
            print(f"SCHEMA_META_OK {schema_file.name}")
        else:
            print(f"SCHEMA_META_FAIL {schema_file.name}: {error}")
            all_valid = False
    
    if all_valid:
        print("SCHEMA_CHECK_OK")
        return 0
    else:
        print("SCHEMA_CHECK_FAIL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
