#!/usr/bin/env python3
"""
Extract metadata from autonomy_journal package without importing it.

Uses AST parsing to extract __version__ and __repro_hash__ from __init__.py
"""
import ast
import sys
from pathlib import Path

def extract_metadata(init_file='src/autonomy_journal/__init__.py'):
    """Extract version and repro_hash from __init__.py using AST parsing."""
    version = None
    repro_hash = None
    
    try:
        with open(init_file, 'r') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == '__version__' and isinstance(node.value, ast.Constant):
                            version = node.value.value
                        elif target.id == '__repro_hash__' and isinstance(node.value, ast.Constant):
                            repro_hash = node.value.value
    
    except Exception as e:
        print(f"ERROR: Failed to extract metadata: {e}", file=sys.stderr)
        return None, None
    
    return version, repro_hash

def main():
    """Main entry point."""
    version, repro_hash = extract_metadata()
    
    if version is None or repro_hash is None:
        sys.exit(1)
    
    # Output in shell-friendly format
    print(f"VERSION={version}")
    print(f"REPRO_HASH={repro_hash}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
