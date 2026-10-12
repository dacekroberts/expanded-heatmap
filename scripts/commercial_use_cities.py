"""Derive the city table of docs/commercial_use_positions.md from its source
table, and confirm every app/cities.py city appears in it exactly once.

    python scripts/commercial_use_cities.py            # check: exit 1 if stale
    python scripts/commercial_use_cities.py --write    # rewrite the derived parts

The source table is written by hand (one row per licence position, the
verdict after the owner's ruling). The city table is never written by hand
(skill commercial-use-audit, step 7): this script reads every table under
"## Source table" and rewrites the text between the two marker pairs.

Columns read from a source row:
  Cities            `ALL`, or display names from app/cities.py joined by "; ".
  Column            allowed, held or blacklisted.
  Stands without it groups joined by "; ", each `City, City = what is left
                    out`: the cities whose map still stands without the source.

The rule (owner, 2026-10-11): the weakest source in use decides the city.
  allowed              every row on the city is allowed.
  allowed if left out  every row that is not allowed names the city under
                       "Stands without it".
  blacklisted          a blacklisted row has no leave-out route for the city.
  held                 otherwise.
A source re-read later gets a new row and never an edit: the new row's Id is
the old Id plus "+1" ("EW-13+1"), and only the highest-numbered row of an Id
counts.
A name that is not in app/cities.py, a city with no row beyond the ALL row,
or a Column outside the three words fails the run and names the row.
"""
import argparse
import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "commercial_use_positions.md"
MARKS = {
    "summary": ("<!-- summary:start -->", "<!-- summary:end -->"),
    "cities": ("<!-- city-table:start -->", "<!-- city-table:end -->"),
}
COLUMNS = ("allowed", "held", "blacklisted")
ORDER = ("blacklisted", "held", "allowed if left out", "allowed")


def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def source_rows(text):
    """Every data row of every table between the source and city headings."""
    body = text.split("## Source table", 1)[1].split("## City table", 1)[0]
    head, rows = None, []
    for line in body.splitlines():
        if not line.startswith("|"):
            head = None
            continue
        c = cells(line)
        if all(re.fullmatch(r":?-+:?", x) for x in c):
            continue
        if head is None:
            head = c
            continue
        if len(c) != len(head):
            raise SystemExit(f"row with {len(c)} cells under a {len(head)}-column header: {line[:80]}")
        rows.append(dict(zip(head, c)))
    return rows


def derive(rows, cities):
    names = [c["name"] for c in cities]
    known = set(names)
    on = collections.defaultdict(list)
    problems = []
    # A re-read is a new row whose Id is the old Id plus "+N"; the old row
    # stays in the file as written and stops counting.
    newest = {}
    for r in rows:
        base, _, n = r["Id"].partition("+")
        newest[base] = max(newest.get(base, 0), int(n or 0))
    rows = [r for r in rows if int(r["Id"].partition("+")[2] or 0) == newest[r["Id"].partition("+")[0]]]
    for r in rows:
        rid = r["Id"]
        if r["Column"] not in COLUMNS:
            problems.append(f"{rid}: Column is {r['Column']!r}")
        listed = names if r["Cities"] == "ALL" else [x.strip() for x in r["Cities"].split(";") if x.strip()]
        leave = {}
        for group in filter(None, (g.strip() for g in r["Stands without it"].split(";"))):
            who, _, what = group.partition(" = ")
            for city in (x.strip() for x in who.split(",")):
                leave[city] = what.strip()
        for city in list(listed) + list(leave):
            if city not in known:
                problems.append(f"{rid}: {city!r} is not a city in app/cities.py")
        for city in leave:
            if city not in listed:
                problems.append(f"{rid}: {city!r} stands without a source it is not listed under")
        for city in listed:
            on[city].append((r, leave.get(city), r["Cities"] == "ALL"))
    out = []
    for c in cities:
        mine = on.get(c["name"], [])
        if not any(not everywhere for _, _, everywhere in mine):
            problems.append(f"{c['name']}: no source row beyond the ALL row")
        weak = [(r, what) for r, what, _ in mine if r["Column"] != "allowed"]
        fixed = [r for r, what in weak if what is None]
        if not weak:
            column = "allowed"
        elif not fixed:
            column = "allowed if left out"
        elif any(r["Column"] == "blacklisted" for r in fixed):
            column = "blacklisted"
        else:
            column = "held"
        out.append({
            "city": c["name"], "country": c["country"], "column": column,
            "decided": ", ".join(r["Id"] for r in fixed),
            "leave": "; ".join(f"{what} ({r['Id']})" for r, what in weak if what is not None),
            "rows": len(mine),
        })
    if problems:
        raise SystemExit("commercial_use_cities: " + "\n  ".join(problems))
    return out


def render(table):
    count = collections.Counter(t["column"] for t in table)
    summary = [f"{len(table)} cities: " + ", ".join(f"{count[k]} {k}" for k in ORDER) + ".", ""]
    for k in ORDER[:3]:
        summary.append(f"- **{k.capitalize()}** ({count[k]}): " + (", ".join(t["city"] for t in table if t["column"] == k) or "none") + ".")
    lines = ["| City | Country | Column | Decided by | Stands if left out | Rows |", "|---|---|---|---|---|---|"]
    for t in sorted(table, key=lambda t: (t["country"], t["city"])):
        lines.append(f"| {t['city']} | {t['country']} | {t['column']} | {t['decided'] or ' '} | {t['leave'] or ' '} | {t['rows']} |")
    return {"summary": "\n".join(summary), "cities": "\n".join(lines)}


def splice(text, parts):
    for key, (start, end) in MARKS.items():
        a, b = text.index(start) + len(start), text.index(end)
        text = text[:a] + "\n" + parts[key] + "\n" + text[b:]
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="rewrite the derived parts of the file")
    args = ap.parse_args()
    sys.path.insert(0, str(ROOT / "app"))
    from cities import CITIES
    text = DOC.read_bytes().decode("utf-8")
    table = derive(source_rows(text), CITIES)
    if len({t["city"] for t in table}) != len(CITIES):
        raise SystemExit("commercial_use_cities: a city is listed twice in app/cities.py")
    new = splice(text, render(table))
    if args.write:
        DOC.write_bytes(new.encode("utf-8"))
        print(f"commercial_use_cities: wrote {len(table)} cities")
    elif new != text:
        raise SystemExit("commercial_use_cities: the city table is stale; run with --write")
    else:
        print(f"commercial_use_cities: OK, {len(table)} cities, each once")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
