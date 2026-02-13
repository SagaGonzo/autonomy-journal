#!/usr/bin/env python3
"""
Schema Meta-Validator for Autonomy Journal
Validates that schema files are valid JSON Schema documents.
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:
    print("SCHEMA_CHECK_ERROR: jsonschema package not installed")
    sys.exit(1)

def check_schema_file(schema_path):
    """Check if a schema file is valid JSON Schema Draft-07."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Check that schema declares Draft-07
        if '$schema' in schema:
            schema_version = schema['$schema']
            if 'draft-07' not in schema_version.lower():
                print(f"SCHEMA_VERSION_MISMATCH {schema_path}: Expected Draft-07, got {schema_version}")
                return False
        
        # Validate schema using Draft7Validator
        Draft7Validator.check_schema(schema)
        print(f"SCHEMA_META_OK {schema_path}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"SCHEMA_JSON_ERROR {schema_path}: {e}")
        return False
    except jsonschema.exceptions.SchemaError as e:
        print(f"SCHEMA_META_INVALID {schema_path}: {e}")
        return False
    except Exception as e:
        print(f"SCHEMA_CHECK_ERROR {schema_path}: {e}")
        return False

def main():
    """Main validation function."""
    schemas_dir = Path('schemas')
    
    if not schemas_dir.exists():
        print("SCHEMA_CHECK_ERROR: schemas/ directory not found")
        return 1
    
    schema_files = sorted(schemas_dir.glob('*.json'))
    if not schema_files:
        print("SCHEMA_CHECK_ERROR: No schema files found")
        return 1
    
    all_valid = True
    for schema_file in schema_files:
        if not check_schema_file(schema_file):
            all_valid = False
    
    if all_valid:
        print("SCHEMA_CHECK_PASS")
        return 0
    else:
        print("SCHEMA_CHECK_FAIL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
