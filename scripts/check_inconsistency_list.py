"""Every built city has a row in each of docs/map_inconsistencies.md's tables.

    python scripts/check_inconsistency_list.py            # the committed list
    python scripts/check_inconsistency_list.py --file X   # another copy (for controls)

WHY. The owner asked on 2026-09-24 for ONE place that answers "why does this map
differ from that one", kept current as cities land, and for it to go on the site
once the last viable city is built. A list that is only "kept current" by
remembering goes stale by the next city, the way this project's hand-kept counts
did. So a city that lands without its rows fails here, the way
check_scope_disclosure.py fails a city missing from the excluded-categories page.

WHAT COUNTS AS A ROW. In each table under "### A." to "### D.", the first
column of a row is a city's display name exactly as app/cities.py spells it
("Miami (Regional)"). A bold row ("| **Brazil** |") starts a country group, and
a row whose first cell starts "All" ("All nine") covers every city of that
country. Its number, if it gives one, must equal the country's city count, so a
tenth Brazilian city makes "All nine" fail rather than silently including it.

It checks presence, not content: whether a row is TRUE is the builder's job and
the reason each table cites its sources. A row for a name not in cities.py is
also reported (a renamed or removed city).
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from cities import CITIES  # noqa: E402

TABLES = ("A", "B", "C", "D")
NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def first_cell(line):
    return line.strip().strip("|").split("|")[0].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(ROOT / "docs" / "map_inconsistencies.md"))
    args = ap.parse_args()
    lines = Path(args.file).read_text(encoding="utf-8").splitlines()

    names = {c["name"] for c in CITIES}
    by_country = Counter(c["country"] for c in CITIES)
    country_of = {c["name"]: c["country"] for c in CITIES}

    problems, seen_tables = [], []
    table, country, covered = None, None, set()

    def close(tab):
        if tab is None:
            return
        seen_tables.append(tab)
        missing = sorted(names - covered, key=lambda n: [c["name"] for c in CITIES].index(n))
        if missing:
            problems.append(f"table {tab}: no row for {', '.join(missing)}")

    for line in lines:
        m = re.match(r"^### ([A-D])\.", line)
        if m or (table and line.startswith("## ")):
            close(table)
            table, country, covered = (m.group(1) if m else None), None, set()
            continue
        if not table or not line.startswith("|"):
            continue
        cell = first_cell(line)
        if cell in ("City", "") or set(cell) <= set("-: "):
            continue
        # A heading may carry a note after it: "**Brazil** (all nine)".
        bold = re.match(r"\*\*(.+?)\*\*", cell)
        if bold:
            country = bold.group(1)
            if country not in by_country:
                problems.append(f"table {table}: country heading {country!r} is not a "
                                f"country in app/cities.py")
            continue
        if cell.lower().startswith("all"):
            if country not in by_country:
                problems.append(f"table {table}: {cell!r} is not under a known country heading")
                continue
            words = cell.lower().split()
            n = next((NUMBER_WORDS.get(w, int(w) if w.isdigit() else None)
                      for w in words[1:2]), None)
            if n is not None and n != by_country[country]:
                problems.append(f"table {table}: {cell!r} under {country}, which has "
                                f"{by_country[country]} cities in app/cities.py")
            covered |= {c for c, k in country_of.items() if k == country}
            continue
        if cell not in names:
            problems.append(f"table {table}: row {cell!r} is not a city in app/cities.py "
                            f"(renamed or removed?)")
            continue
        if country and country_of[cell] != country:
            problems.append(f"table {table}: {cell} sits under {country}, but "
                            f"app/cities.py says {country_of[cell]}")
        covered.add(cell)
    close(table)

    for tab in TABLES:
        if tab not in seen_tables:
            problems.append(f"table {tab}: section '### {tab}.' not found")
    if problems:
        print(f"PROBLEMS {len(problems)}")
        for p in problems:
            print("  " + p)
        print("\nAdd the city's rows to docs/map_inconsistencies.md - one per table, "
              "under its country - with the facts from its page, config and outputs.")
        return 1
    print(f"OK - all {len(names)} cities have a row in each of tables "
          f"{', '.join(TABLES)} of docs/map_inconsistencies.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
