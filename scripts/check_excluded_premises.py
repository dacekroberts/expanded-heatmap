"""Refuse a committed excluded-premises file that carries a name or an address.

These files record left-out rows by register key, type and reason. A name left
out of a map can be a person's own beside a home address, and the exposure
check reads only the rendered map (audit of 2026-11-03, DECISIONS.md).
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANNED = {"business_name", "name", "address", "owner", "legal_name"}


def main():
    files = sorted(ROOT.glob("outputs/*/excluded_premises*.csv"))
    bad = []
    for path in files:
        with path.open(encoding="utf-8", newline="") as f:
            header = next(csv.reader(f), [])
        hit = BANNED & {c.strip().lower() for c in header}
        if hit:
            bad.append(f"{path.relative_to(ROOT)}: {sorted(hit)}")
    for line in bad:
        print("FAIL", line)
    print(f"check_excluded_premises: {len(files)} files, {len(bad)} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
