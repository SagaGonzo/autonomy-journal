#!/usr/bin/env python3
"""
Meta-validate JSON Schemas in ./schemas using the dialect declared by each schema's $schema.

Receipt tokens:
  SCHEMA_CHECK_PASS <path>
  SCHEMA_CHECK_FAIL <path> :: <ExcType>: <message>
"""
import json
from pathlib import Path
from jsonschema.validators import validator_for


def main() -> int:
    ok = True
    schema_dir = Path("schemas")
    if not schema_dir.exists():
        print("SCHEMA_DIR_MISSING schemas/")
        return 1

    for p in sorted(schema_dir.glob("*.json")):
        try:
            schema = json.loads(p.read_text(encoding="utf-8"))
            Validator = validator_for(schema)
            Validator.check_schema(schema)
            print(f"SCHEMA_CHECK_PASS {p.as_posix()}")
        except Exception as e:
            ok = False
            print(f"SCHEMA_CHECK_FAIL {p.as_posix()} :: {type(e).__name__}: {e}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
