#!/usr/bin/env python3
"""
Schema Meta-Validator for Autonomy Journal
Validates that JSON schema files are themselves valid schemas.
"""
import json
import sys
from pathlib import Path
import jsonschema
from jsonschema import validators

def validate_schema_file(schema_path):
    """Validate a JSON schema file using meta-validation."""
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        # Get the appropriate validator class for this schema
        ValidatorClass = validators.validator_for(schema)
        
        # Check the schema itself (meta-validation)
        ValidatorClass.check_schema(schema)
        
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except jsonschema.SchemaError as e:
        return False, f"Invalid schema: {e.message}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main schema validation function."""
    schemas_dir = Path('schemas')
    
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_FAIL: schemas/ directory not found")
        return 1
    
    schema_files = list(schemas_dir.glob('*.json'))
    if not schema_files:
        print("SCHEMA_CHECK_FAIL: No schema files found")
        return 1
    
    all_valid = True
    for schema_file in schema_files:
        valid, error = validate_schema_file(schema_file)
        if valid:
            print(f"SCHEMA_CHECK_OK: {schema_file.name}")
        else:
            print(f"SCHEMA_CHECK_FAIL: {schema_file.name} - {error}")
            all_valid = False
    
    if all_valid:
        print("SCHEMA_CHECK_PASS")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
