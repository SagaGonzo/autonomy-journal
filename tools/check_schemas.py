#!/usr/bin/env python3
"""
Schema Meta-Validator for Autonomy Journal

Validates that all JSON schema files in schemas/ directory are well-formed
and comply with their declared JSON Schema specification.

Uses jsonschema.validators.validator_for() to get the appropriate validator
and then calls Validator.check_schema() to meta-validate.
"""
import sys
import json
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validators
except ImportError:
    print("ERROR: jsonschema library not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)

def check_schema_file(schema_path):
    """
    Meta-validate a single JSON schema file.
    
    Returns (success: bool, error_message: str or None)
    """
    try:
        # Load the schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Get the appropriate validator class for this schema
        ValidatorClass = validators.validator_for(schema)
        
        # Meta-validate the schema
        ValidatorClass.check_schema(schema)
        
        return True, None
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except jsonschema.SchemaError as e:
        return False, f"Invalid schema: {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

def main():
    """Main entry point for schema validation."""
    print("Running Schema Meta-Validation...")
    
    # Find all schema files
    schemas_dir = Path('schemas')
    if not schemas_dir.exists():
        print("ERROR: schemas/ directory not found")
        print("SCHEMA_CHECK_FAIL")
        return 1
    
    schema_files = list(schemas_dir.glob('*.json'))
    if not schema_files:
        print("ERROR: No schema files found in schemas/")
        print("SCHEMA_CHECK_FAIL")
        return 1
    
    # Validate each schema
    all_passed = True
    for schema_file in sorted(schema_files):
        success, error = check_schema_file(schema_file)
        
        if success:
            print(f"✓ {schema_file.name} - valid")
        else:
            print(f"✗ {schema_file.name} - FAILED")
            print(f"  {error}")
            all_passed = False
    
    # Print final result
    if all_passed:
        print("\n✓ SCHEMA_CHECK_PASS")
        return 0
    else:
        print("\n✗ SCHEMA_CHECK_FAIL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
