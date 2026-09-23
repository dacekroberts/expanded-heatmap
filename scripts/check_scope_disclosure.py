"""Every built city's scope must be disclosed on the public exclusions page.

This project scopes each city twice - which rail network its map is drawn
around, and which businesses are counted near it - and both are invisible from
the map. `docs/excluded_categories.md` is where a reader is told, and
`app/pages/91_What_Is_Excluded.py` renders it with a generated station table
spliced in.

The gap this closes is the one that prompted it: a reader asked whether BART
was in the San Francisco build. It is not, deliberately and for a recorded
reason - and nothing published said so. A city whose scope is undisclosed looks
exactly like a city that was checked, which is the same argument that made
`check_provenance.py` a script rather than a paragraph.

Four properties, all fail-closed:

  A  the document still carries the heading the page splices the station table
     at, exactly once - the page falls back to appending the table if it is
     missing, and a silent fallback nobody checks is how this rots;
  B  the station-scope section is still there at all;
  C  every city in `app/cities.py` derives an `outputs/<slug>/` directory, so
     no city's row in the generated table is silently empty;
  D  every city is named in the BUSINESS half of the document, after that
     heading. Being named in the transit half is not enough - a city can be
     mentioned as "Cercanías in Madrid" while none of its own business
     exclusions are written down, which is exactly the state four cities were
     found in.

Property E rides along with C: every committed `excluded_stations.csv` must
classify into a shape the page understands, so a city arriving with a new
schema shows up here rather than as a wrong number on the live site.

  python scripts/check_scope_disclosure.py [--root DIR]

Exit 0 if every property holds.
"""

import argparse
import csv
import sys
from pathlib import Path

# Cities whose business-side exclusions are NOT yet written into
# docs/excluded_categories.md. A dated defect, not a pass - and it expires:
# once a city here IS documented, this check FAILS until it is removed from
# the list, so the list cannot quietly outlive the gap it records.
# Empty as of 2026-09-23: the five cities this check first named - Montréal,
# Madrid, Barcelona, Dublin and Milan - were written up rather than parked.
KNOWN_GAPS = {}

BUSINESS_HEADING = "## Which businesses are counted"
STATION_HEADING = "## Which stations these maps are drawn around"

# The two shapes an excluded_stations.csv comes in: a `reason` column, or
# boundary facts in their own columns. Kept in step with the page's reader.
BOUNDARY_COLUMNS = {"located_in", "state", "distance_outside_m",
                    "in_city_spatial", "municipio_codes"}


def slug(page):
    """`pages/2_San_Francisco_Heatmap.py` -> `san_francisco`."""
    stem = Path(page).stem
    stem = stem.split("_", 1)[1] if stem[0].isdigit() else stem
    return (stem[: -len("_Heatmap")].lower() if stem.endswith("_Heatmap")
            else stem.lower())


def load_cities(root):
    sys.path.insert(0, str(root / "app"))
    for stale in ("cities",):
        sys.modules.pop(stale, None)
    from cities import CITIES
    return CITIES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repository root to check")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    problems = []
    doc_path = root / "docs" / "excluded_categories.md"
    if not doc_path.exists():
        print(f"FAIL  {doc_path} is missing")
        return 1
    doc = doc_path.read_text(encoding="utf-8")

    # A - the splice marker.
    seen = doc.count(BUSINESS_HEADING)
    if seen != 1:
        problems.append(
            f"docs/excluded_categories.md: the heading the station table is "
            f"spliced at appears {seen} times, expected exactly 1 "
            f"({BUSINESS_HEADING!r}). app/pages/91_What_Is_Excluded.py "
            f"splits the document on it.")

    # B - the station section.
    if STATION_HEADING not in doc:
        problems.append(
            f"docs/excluded_categories.md: the station-scope section is gone "
            f"({STATION_HEADING!r}). Transit scope would be undisclosed.")

    cities = load_cities(root)
    business_half = doc.partition(BUSINESS_HEADING)[2]

    for entry in cities:
        name = entry["name"]
        base = name.split(" (")[0]

        # C - the generated table can find this city's outputs.
        city_dir = root / "outputs" / slug(entry["page"])
        if not city_dir.is_dir():
            problems.append(
                f"{name}: no outputs/{city_dir.name}/ directory, so its row in "
                f"the station table on 91_What_Is_Excluded.py renders empty. "
                f"The slug is derived from {entry['page']!r}.")
        else:
            # E - the file classifies into a shape the page understands.
            csv_path = city_dir / "excluded_stations.csv"
            if csv_path.exists():
                with open(csv_path, encoding="utf-8-sig", newline="") as fh:
                    reader = csv.DictReader(fh)
                    columns = set(reader.fieldnames or ())
                    rows = list(reader)
                if "reason" in columns:
                    unknown = [r for r in rows
                               if "spacing" not in (r.get("reason") or "").lower()
                               and "outside" not in (r.get("reason") or "").lower()]
                    if unknown:
                        problems.append(
                            f"{name}: {len(unknown)} row(s) in "
                            f"{csv_path.name} give a reason that is neither a "
                            f"spacing filter nor a boundary - e.g. "
                            f"{unknown[0].get('reason')!r}. The page would "
                            f"count them under 'Other'; describe the new "
                            f"category in the document first.")
                elif not (BOUNDARY_COLUMNS & columns) and rows:
                    problems.append(
                        f"{name}: {csv_path.name} has neither a 'reason' "
                        f"column nor any of {sorted(BOUNDARY_COLUMNS)}, so the "
                        f"page cannot say WHY its {len(rows)} stations were "
                        f"left out.")

        # D - named in the business half.
        documented = base in business_half
        gap_since = KNOWN_GAPS.get(base)
        if documented and gap_since:
            problems.append(
                f"{name}: listed in KNOWN_GAPS since {gap_since} but it IS now "
                f"named in the business half of docs/excluded_categories.md. "
                f"Remove it from KNOWN_GAPS in this script.")
        elif not documented and not gap_since:
            problems.append(
                f"{name}: named nowhere in the business half of "
                f"docs/excluded_categories.md, so the published page does not "
                f"say what this city's maps leave out. Add a section, or add "
                f"the city to KNOWN_GAPS with today's date.")

    for line in problems:
        print(f"FAIL  {line}")
    if KNOWN_GAPS:
        print(f"\n{len(KNOWN_GAPS)} city/cities are a DATED GAP rather than a "
              f"pass: " + ", ".join(f"{c} (since {d})"
                                    for c, d in sorted(KNOWN_GAPS.items())))
    if problems:
        print(f"\n{len(problems)} problem(s).")
        return 1
    print(f"OK  {len(cities)} cities: scope disclosed, station table wired.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
