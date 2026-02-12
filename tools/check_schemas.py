#!/usr/bin/env python3
"""
Validate that each JSON Schema in ./schemas is itself a valid schema.
This is a *schema-of-schemas* check (meta-validation).
"""
import json
import sys
from pathlib import Path

from jsonschema import validators


def main() -> int:
    ok = True
    schema_dir = Path("schemas")
    if not schema_dir.exists():
        print("SCHEMA_DIR_MISSING schemas/")
        return 1

    for p in sorted(schema_dir.glob("*.json")):
        try:
            schema = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            ok = False
            print(f"SCHEMA_JSON_PARSE_FAIL {p.name} {e}")
            continue

        try:
            Validator = validators.validator_for(schema)
            Validator.check_schema(schema)
            print(f"SCHEMA_CHECK_PASS {p.name} ({Validator.__name__})")
        except Exception as e:
            ok = False
            print(f"SCHEMA_CHECK_FAIL {p.name} {e}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
