#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$(which python3 || which python || echo "")"

if [ -z "$PYTHON_BIN" ]; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi

"$PYTHON_BIN" "$SCRIPT_DIR/setup.py" "$@"
