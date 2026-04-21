#!/usr/bin/env python3
"""Compatibility wrapper for legacy workflow entrypoint."""

import subprocess
import sys


def main() -> int:
    result = subprocess.run([sys.executable, "scripts/generate_feed.py"], check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
