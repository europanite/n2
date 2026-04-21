#!/usr/bin/env python3

"""
Compatibility wrapper for legacy workflow.

Old workflow expects:
    python scripts/generate_pages.py

Current implementation uses:
    scripts/generate_feed.py

So we just delegate.
"""

import subprocess
import sys


def main():
    cmd = [sys.executable, "scripts/generate_feed.py"]
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())