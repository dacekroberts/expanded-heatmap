"""Reads the committed excluded_stations.csv files and says why each is there.

Shared DELIBERATELY between app/pages/201_What_Is_Excluded.py, which renders
these counts for readers, and scripts/check_scope_disclosure.py, which fails
when a new city arrives in a shape neither understands. Two copies of this
vocabulary would drift, and the drift would be invisible: the page would
quietly bucket a new city's stations under "Other" while the check went on
passing.

Stdlib only - no pandas, no streamlit - so the check can import it without the
app's runtime and the app can import it without the pipeline's.

THE FILES DO NOT SHARE A SCHEMA, and that is not an oversight: each city's
step 1 records what it actually knows. Some name the reason in a `reason`
column; the rest carry boundary facts in their own columns (`commune`,
`located_in`, `state`, `distance_outside_m`). Both shapes are read here, and
anything matching neither is counted as `other` rather than folded into a
bucket it might not belong in - which is what makes an unfamiliar new city
show up as a failure instead of a wrong number.
"""

import csv
from pathlib import Path

# Columns that, on their own, mean "this station is in another municipality".
BOUNDARY_COLUMNS = {"located_in", "state", "distance_outside_m",
                    "in_city_spatial", "municipio_codes", "commune"}


def slug(page):
    """`pages/2_San_Francisco_Heatmap.py` -> `san_francisco`.

    Derived rather than stored: cities.py already treats the page path as the
    link between an entry and its city, and a second hand-kept key is a second
    thing to get wrong. A rename that breaks this shows as an empty row, so
    check_scope_disclosure.py asserts every slug resolves to a real directory.
    """
    stem = Path(page).stem
    stem = stem.split("_", 1)[1] if stem[0].isdigit() else stem
    return (stem[: -len("_Heatmap")].lower() if stem.endswith("_Heatmap")
            else stem.lower())


def classify(reason, city):
    """One of 'thinned', 'infrequent', 'outside', 'closed' or 'other' for a
    `reason` cell.

    `outside` covers two things a reader sees as one: a station standing in
    another municipality, and a line in the same feed that belongs to a
    neighbouring town's own network - Marseille's file carries seven stations
    of "Aubagne's tram, not Marseille's". Both mean the station is not in the
    city this map is built from.

    `closed` is a station the timetable does not serve because it is closed
    for works (Berlin's U6 Tegel branch, 2026-09-28, owner: drawn as the
    timetable runs), Sacramento's Township 9 and Prague's Flora, all under the
    one rule of 2026-09-29 (docs/category_rules.md, "Station scope").
    """
    text = (reason or "").lower()
    if "spacing" in text:
        return "thinned"
    # `infrequent`: a stop on a light-rail stretch that runs less often than
    # the 15-minute test (Aarhus's converted railways, 2026-09-29, owner).
    if "15-minute" in text:
        return "infrequent"
    if "closed for works" in text:
        return "closed"
    if "outside" in text or f"not {city.lower()}'s" in text:
        return "outside"
    return "other"


def counts_for(csv_path, city):
    """(outside, thinned, other, closed, infrequent) for one city's file, or
    None if there is none. Each later category is appended, so the earlier
    ones keep their positions."""
    if not csv_path.exists():
        return None
    with open(csv_path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or ())
        rows = list(reader)
    if "reason" in columns:
        tally = {"outside": 0, "thinned": 0, "other": 0, "closed": 0, "infrequent": 0}
        for row in rows:
            tally[classify(row.get("reason"), city)] += 1
        return (tally["outside"], tally["thinned"], tally["other"], tally["closed"],
                tally["infrequent"])
    if BOUNDARY_COLUMNS & columns:
        return len(rows), 0, 0, 0, 0
    return 0, 0, len(rows), 0, 0


def scope_rows(root, cities):
    """One dict per city: name, the network mapped, and the five counts
    from `counts_for()`.

    `counts` is None for a city with no excluded_stations.csv at all - every
    station of its network is on its map - which the caller renders as a dash
    rather than as a zero it did not measure.
    """
    rows = []
    for entry in cities:
        base = entry["name"].split(" (")[0]
        rows.append({
            "name": entry["name"],
            "slug": slug(entry["page"]),
            "network": network_label(entry),
            "counts": counts_for(
                Path(root) / "outputs" / slug(entry["page"])
                / "excluded_stations.csv", base),
        })
    return rows


def network_label(entry):
    """The network from a city's blurb, without its line list.

    The blurb names the network and then its lines; the lines are the city
    page's job. Only a PARENTHESISED list is dropped, so the parts that are not
    line lists survive - New York's Staten Island Railway, Mexico City's Tren
    Ligero - which cutting at the first bracket would have lost.
    """
    blurb = entry.get("blurb", "").split(" — ")[0]
    out, depth = [], 0
    for char in blurb:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(char)
    return " ".join("".join(out).split()).strip().rstrip(",")
