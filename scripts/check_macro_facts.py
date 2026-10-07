"""The macro map's per-city facts: the completeness tier each dot is coloured by,
and the tooltip's storefront count, placement and data age - checked, never
hand-kept (owner, 2026-09-28).

    python scripts/check_macro_facts.py            # check (the pre-push hook)
    python scripts/check_macro_facts.py --write    # regenerate app/macro_facts.json

Three things are decided here:

  1. STOREFRONT COUNTS. `app/macro_facts.json` holds each city's storefront
     count, generated from the file the city's map step reads
     (`data/<slug>/processed/businesses_geocoded.csv` where a geocoding step
     exists, else `businesses_clean.csv`) exactly
     as `pipeline/map_common.render_heatmap` counts "available" (rows with a
     coordinate, less `drop_contact_details`). The check regenerates and
     compares. A city whose processed file is absent (a fresh checkout) is
     SKIPPED and named, never counted as a pass of its number. `--write`
     REFUSES instead, writing nothing, when data/ is missing or a city in the
     committed file would lose its count (`refuse_shrunken_write`).
  2. THE TIER (`coverage` in app/cities.py) against the city's row in table B
     of docs/map_inconsistencies.md. "narrowed" needs a structural gap there:
     a bucket missing (a dash), merged or relabelled (the pins cell is not
     three plain figures), or a "Missing or thin" note saying "No ...",
     "... only", "merged" or "Retail =", or a layer called "thin" (owner,
     2026-09-30: New York's and Buffalo's thin retail made them narrowed,
     superseding 2026-09-28). "full" needs three plain figures and no such
     note. "one_bucket" needs a single figure, OR food alone: no Personal
     services (a dash) and a note saying the Retail figure is food shops or
     food retail (owner, 2026-09-30: food shops are food-like and are not a
     second category). A floor (San Francisco's NAICS floor, Brazil's
     unreadable rows) is NOT structural: those cities stay full, and their
     caveats belong on their pages (PLAN).
  3. THE PHRASES (`placement`, `data_age`): every date, year and percentage in
     them must appear in the city's row of table C (placement) or D (data age),
     so a tooltip cannot state a figure the record does not.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "app"))

from cities import CITIES  # noqa: E402
from station_scope import slug  # noqa: E402

FACTS_JSON = ROOT / "app" / "macro_facts.json"
INCONSISTENCIES = ROOT / "docs" / "map_inconsistencies.md"
TIERS = ("full", "narrowed", "one_bucket")
STRUCTURAL = re.compile(r"\bNo [A-Za-z]|\bonly\b|merged|Retail =|\bthin\b")
# The note that makes a Retail figure food: "Retail = food shops only", "Retail = food retail".
FOOD_RETAIL = re.compile(r"Retail = food (?:shops only|retail)\b")
DASH = ("—", "-", "–")
# One-category cities whose table B row carries a token third figure, each
# named with the owner's call - never a threshold, which would decide the next
# city unseen.
ONE_BUCKET_BY_OWNER = {
    "Hong Kong": "owner, 2026-09-30: 34 bathhouses are not enough to make a second category",
}
FIGURE = r"\d[\d,]*"


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(lines, header_prefix):
    """{city name: its cells} for the table whose header starts with prefix.
    A row reading "same" inherits the previous row's text for that cell, as
    the document writes France's and Brazil's rows."""
    starts = [i for i, l in enumerate(lines) if l.startswith(header_prefix)]
    if len(starts) != 1:
        sys.exit(f"{INCONSISTENCIES.name}: expected one table headed {header_prefix!r}")
    out, prev, country, i = {}, None, None, starts[0] + 2
    while i < len(lines) and lines[i].startswith("|"):
        c = cells(lines[i])
        if prev is not None:
            padded = prev + [""] * max(0, len(c) - len(prev))
            c = [(p + " " + x) if x.lower().startswith("same") else x for x, p in zip(c, padded)]
        name = c[0].replace("*", "").strip()
        if c[0].startswith("**") and not any(c[1:]):
            country = name                      # a country header row, e.g. **Brazil**
        elif name.lower().startswith("all ") and country:
            out[f"ALL:{country}"] = c           # Brazil's "All nine" row in table C
            prev = c
        elif name:
            out[name] = c
            prev = c
        i += 1
    return out


def row_for(tbl, name, country=None):
    """A city's row, matching "Dublin" to "Dublin (Regional)" and back; else
    its country's "All ..." row (table C writes Brazil's nine as one)."""
    if name in tbl:
        return tbl[name]
    base = re.sub(r"\s*\(.*\)$", "", name)
    for k, v in tbl.items():
        if re.sub(r"\s*\(.*\)$", "", k) == base:
            return v
    return tbl.get(f"ALL:{country}") if country else None


def processed_dir(city_slug):
    """The folder the city's own config reads (`DATA_PROCESSED`), else
    data/<slug>/processed. A branch that builds a variant into a subfolder
    (a regional switch writing processed/regional/, 2026-10-03) is then
    checked against its own output, while master's shared folder stays
    master's (docs/session_roles.md, the shared data/ junction)."""
    import importlib
    try:
        config = importlib.import_module(f"pipeline.{city_slug}.config")
        return Path(config.DATA_PROCESSED)
    except Exception:
        return ROOT / "data" / city_slug / "processed"


def storefronts(city_slug):
    """render_heatmap's "available" count, or None when the file is absent."""
    import pandas as pd
    from pipeline.map_common import drop_contact_details
    # The file the city's map step reads: a city with a geocoding step
    # (Toronto, Los Angeles) maps businesses_geocoded.csv, not the clean file.
    processed = processed_dir(city_slug)
    path = next((p for p in (processed / "businesses_geocoded.csv", processed / "businesses_clean.csv")
                 if p.exists()), None)
    if path is None:
        return None
    df = pd.read_csv(path, low_memory=False)
    df = df.dropna(subset=["latitude", "longitude"])
    return int(len(drop_contact_details(df)))


def committed_counts():
    """The storefront counts in HEAD's app/macro_facts.json, else the file on
    disk when git cannot answer. HEAD rather than the disk, so a shrunken file
    written by an earlier run is not the yardstick for the next one."""
    import subprocess
    res = subprocess.run(["git", "show", "HEAD:app/macro_facts.json"], cwd=ROOT,
                         capture_output=True, encoding="utf-8", errors="replace")
    text = res.stdout if res.returncode == 0 else (
        FACTS_JSON.read_text(encoding="utf-8") if FACTS_JSON.exists() else "{}")
    try:
        return json.loads(text).get("storefronts", {})
    except ValueError:
        return {}


def refuse_shrunken_write(counts):
    """Exit non-zero, writing nothing, when --write would drop a count the
    committed file holds for a city still in app/cities.py.

    On 2026-10-07 regen_generated.py ran in a worktree with no data/ junction:
    every city was skipped, `{"storefronts": {}}` was written and committed,
    and app/label_competition.py ranked the macro map's labels on empty counts
    (DECISIONS.md, 2026-10-07, the macro_facts.json write guard). A skipped
    city is right for the check, which names it; for --write it means the
    inputs are missing, never that the count should go. A city removed from
    app/cities.py drops its count without tripping this, since it is no
    longer compared."""
    import subprocess
    data = ROOT / "data"
    common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            cwd=ROOT, capture_output=True, text=True).stdout.strip()
    shared = Path(common).parent / "data" if common else Path("<main checkout>") / "data"
    junction_hint = (f"Every worktree's data/ is a junction to the shared folder {shared} "
                     f"(docs/session_roles.md). Create it from this checkout's root with "
                     f"`cmd /c mklink /J data \"{shared}\"`, or run this where data/ exists.")
    if not data.exists():
        sys.exit(f"REFUSED: {data} is missing, so no storefront count can be measured and "
                 f"{FACTS_JSON.relative_to(ROOT)} would be written empty. {junction_hint}")
    names = {c["name"] for c in CITIES}
    committed = committed_counts()
    lost = sorted(n for n in committed if n in names and n not in counts)
    if lost:
        shown = ", ".join(lost[:10]) + (f" and {len(lost) - 10} more" if len(lost) > 10 else "")
        sys.exit(f"REFUSED: {FACTS_JSON.relative_to(ROOT)} would hold {len(counts)} storefront "
                 f"counts where the committed file holds {len(committed)}; no processed data "
                 f"here for {len(lost)} of them ({shown}). Nothing written. Check that data/ is "
                 f"the junction to the shared folder and that each city's processed file exists. "
                 f"{junction_hint}")


def figures_in(text):
    """Dates, years and percentages a phrase states."""
    return set(re.findall(r"\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\b(?:19|20)\d{2}\b|\d+(?:\.\d+)?%", text))


def check_phrases(problems, name, field, phrase, row):
    if row is None:
        problems.append(f"{name}: no row in {INCONSISTENCIES.name} to check its {field} against")
        return
    text = " ".join(row)
    for f in figures_in(phrase):
        bare = f.rstrip("%")
        if bare not in text:
            problems.append(f"{name}: {field} {phrase!r} states {f}, which its row does not")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="regenerate app/macro_facts.json")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    lines = io.open(INCONSISTENCIES, encoding="utf-8").read().split("\n")
    tb = table(lines, "| City | Source kind |")
    tc = table(lines, "| City | Location method")
    td = table(lines, "| City | Business data as-of")

    problems, skipped, counts = [], [], {}
    for c in CITIES:
        name, s = c["name"], slug(c["page"])
        cov = c.get("coverage")
        for field in ("coverage", "placement", "data_age"):
            if not c.get(field):
                problems.append(f"{name}: app/cities.py has no {field!r}")
        if cov and cov not in TIERS:
            problems.append(f"{name}: coverage {cov!r} is not one of {TIERS}")
        b = row_for(tb, name)
        if cov in TIERS and b is not None:
            # the in-ring pins cell: the last "/"-separated cell before the note
            # (Brazil's per-city rows are shorter than the header)
            slashed = [x for x in b[1:-1] if "/" in x]
            pins = slashed[-1] if slashed else ""
            parts = [p.strip() for p in pins.split("/")] if pins else []
            plain = len(parts) == 3 and all(re.fullmatch(FIGURE, p) for p in parts)
            note = b[-1]
            structural = (not plain) or bool(STRUCTURAL.search(note))
            if cov == "full" and structural:
                problems.append(f"{name}: coverage 'full', but table B shows a structural gap "
                                f"(pins {pins!r}; note {note!r})")
            if cov == "narrowed" and not structural:
                problems.append(f"{name}: coverage 'narrowed', but table B shows three plain "
                                f"buckets and no structural note ({note!r})")
            single = len(parts) == 1 or sum(bool(re.search(FIGURE, p)) for p in parts) == 1
            food_alone = (len(parts) == 3 and parts[2] in DASH and bool(FOOD_RETAIL.search(note)))
            if cov == "one_bucket" and not (single or food_alone or name in ONE_BUCKET_BY_OWNER):
                problems.append(f"{name}: coverage 'one_bucket', but table B shows {pins!r} "
                                f"(note {note!r})")
        elif cov in TIERS:
            problems.append(f"{name}: no row in table B of {INCONSISTENCIES.name}")
        check_phrases(problems, name, "placement", c.get("placement", ""), row_for(tc, name, c.get("country")))
        check_phrases(problems, name, "data_age", c.get("data_age", ""), row_for(td, name, c.get("country")))
        n = storefronts(s)
        if n is None:
            skipped.append(name)
        else:
            counts[name] = n

    if args.write:
        refuse_shrunken_write(counts)
        FACTS_JSON.write_text(json.dumps({"storefronts": counts}, indent=2, ensure_ascii=False,
                                         sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(f"wrote {FACTS_JSON.relative_to(ROOT)}: {len(counts)} cities")
    else:
        stored = json.loads(FACTS_JSON.read_text(encoding="utf-8")).get("storefronts", {}) \
            if FACTS_JSON.exists() else {}
        if not FACTS_JSON.exists():
            problems.append(f"{FACTS_JSON.relative_to(ROOT)} is missing: run with --write")
        for name in {c["name"] for c in CITIES} - set(stored):
            problems.append(f"{name}: no storefront count in {FACTS_JSON.name}")
        for name, n in counts.items():
            if name in stored and stored[name] != n:
                problems.append(f"{name}: {FACTS_JSON.name} says {stored[name]:,} storefronts, "
                                f"the processed data holds {n:,} - run with --write")
    if skipped:
        print(f"  counts not re-measured (no processed data here): {', '.join(skipped)}")
    if problems:
        for p in problems:
            print(f"  PROBLEM  {p}")
        print(f"\n{len(problems)} problem(s). Fix the record or the tier - never loosen the rule.")
        return 1
    tiers = {t: sum(1 for c in CITIES if c.get("coverage") == t) for t in TIERS}
    print(f"OK - {len(CITIES)} cities: " + ", ".join(f"{t} {n}" for t, n in tiers.items())
          + f"; tiers agree with table B, every phrase's figures with tables C and D, "
            f"storefront counts current for {len(counts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
