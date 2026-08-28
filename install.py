#!/usr/bin/env python3
"""
Root entrypoint for GSC & GA4 MCP Setup.
Delegates directly to scripts/setup.py.
"""
import os
import sys
from pathlib import Path

script_path = Path(__file__).parent / "scripts" / "setup.py"
if not script_path.exists():
    print(f"❌ Error: {script_path} not found.")
    sys.exit(1)

# Execute scripts/setup.py
with open(script_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), str(script_path), 'exec')
    exec(code, globals())
