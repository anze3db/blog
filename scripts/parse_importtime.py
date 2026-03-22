"""
Parse the output of `python -X importtime` and show the top slowest imports.

Usage:
    python -X importtime manage.py check 2> import.log
    python scripts/parse_importtime.py import.log
"""

import sys


def parse_importtime(path):
    entries = []
    with open(path) as f:
        for line in f:
            if not line.startswith("import time:"):
                continue
            # Format: "import time:   self [us] |  cumulative | imported package"
            parts = line.removeprefix("import time:").split("|")
            if len(parts) != 3:
                continue
            try:
                self_us = int(parts[0].strip())
                cumulative_us = int(parts[1].strip())
            except ValueError:
                continue
            module = parts[2].strip()
            entries.append((self_us, cumulative_us, module))
    return entries


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    n = 20
    if len(sys.argv) >= 3:
        n = int(sys.argv[2])

    entries = parse_importtime(sys.argv[1])
    entries.sort(key=lambda e: e[0], reverse=True)

    print(f"{'self (ms)':>10} {'cumul (ms)':>11}  module")
    print("-" * 60)
    for self_us, cumul_us, module in entries[:n]:
        print(f"{self_us / 1000:10.1f} {cumul_us / 1000:11.1f}  {module}")


if __name__ == "__main__":
    main()
