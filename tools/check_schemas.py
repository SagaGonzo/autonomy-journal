#!/usr/bin/env python3
"""
Meta-validate JSON schemas in ./schemas using the dialect declared by $schema.

Receipt tokens:
  SCHEMA_CHECK_PASS <file>:<file>:<file>
  SCHEMA_CHECK_FAIL <file> <reason>
"""
import json
import sys
from pathlib import Path
from jsonschema import validators


def meta_validate_schema(schema_path):
    """
    Meta-validate a schema file against its declared $schema dialect.
    Returns (is_valid, error_message).
    """
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        # Get the appropriate validator class for the schema's dialect
        if '$schema' not in schema:
            return False, "Missing $schema declaration"
        
        validator_class = validators.validator_for(schema)
        
        # Check if the schema itself is valid
        validator_class.check_schema(schema)
        
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, str(e)


def main():
    """Main schema meta-validation function."""
    schemas_dir = Path('schemas')
    
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_FAIL schemas/ directory not found")
        return 1
    
    schema_files = sorted(schemas_dir.glob('*.json'))
    
    if not schema_files:
        print("SCHEMA_CHECK_FAIL No schema files found")
        return 1
    
    all_valid = True
    valid_schemas = []
    
    for schema_file in schema_files:
        is_valid, error = meta_validate_schema(schema_file)
        
        if is_valid:
            valid_schemas.append(schema_file.name)
        else:
            print(f"SCHEMA_CHECK_FAIL {schema_file.name} {error}")
            all_valid = False
    
    if all_valid:
        # Generate receipt token with all validated schemas
        schema_list = ':'.join(valid_schemas)
        print(f"SCHEMA_CHECK_PASS {schema_list}")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
