"""Fail when a built city's provenance is not actually recorded.

    python scripts/check_provenance.py [--strict]

WHY THIS EXISTS, AND WHY IT IS A SCRIPT RATHER THAN A PARAGRAPH
---------------------------------------------------------------
`CLAUDE.md` calls `docs/data_sources.md` the only way a build can be
reproduced, and `add-city` Step 0.4 makes recording a source a build
requirement. Both were followed, and both were followed for the US cities
only. Twice:

  - **Canada, 2026-09-21.** Six municipalities built. Their NOTICES went into
    `data_sources.md` the same day, correctly. Their ENDPOINTS did not reach
    the three provenance tables at all, their FEEDS never reached the GTFS
    licence table, and one publisher - the Province of British Columbia, whose
    layer names 30 stations - was never read. Found 2026-09-22, a day later.
  - **Mexico, 2026-09-22.** Mexico City and Guadalajara built. Same omission,
    caught by this script on the day it was written rather than by a reader.

Each time the gap was invisible in exactly the way that matters: **a city whose
provenance is unrecorded looks identical to a city that was checked.** A prose
rule cannot tell those apart. This can.

The thing both misses have in common is that the country was PROFILED before
any of its cities was built, so a whole country's sources arrived through
`add-country` - which writes `docs/<country>_step0_endpoints.md` - and the
per-city step that would have copied them into `data_sources.md` was never the
step anyone was on. So the check is deliberately keyed on the BUILT CITY, not
on the country file.

WHAT IT CHECKS
--------------
  A. Every city in `app/cities.py` has at least one row naming it in each of
     the three provenance tables.
  B. Every URL constant that a city's `pipeline/<slug>/config.py` actually
     resolves to appears verbatim in `data_sources.md`. This is the strongest
     check here and the one that catches a source nobody thought of as a
     source - a naming layer, a parcel join, a geocoder.
  C. `app/components.py`'s `_NOTICES` and `data_sources.md`'s numbered notices
     are in bijection. A required string displayed but unexplained, or
     explained but not displayed, both fail.
  D. Notice numbers are unique and contiguous from 1. They were neither: the
     list carried two item 8s and two item 15s from 2026-09-21 to 2026-09-22,
     because each country's block was appended without renumbering.

KNOWN_GAPS below is a list of DEFECTS, not exemptions. Entries are dated, the
report prints them loudly, and a stale entry - one naming a city that is now
recorded - fails the check, so the list can only shrink. `--strict` ignores it
entirely and is what CI should run once the list is empty.
"""

import argparse
import ast
import importlib
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

DATA_SOURCES = ROOT / "docs" / "data_sources.md"
CITIES_PY = ROOT / "app" / "cities.py"
COMPONENTS_PY = ROOT / "app" / "components.py"

# Defects awaiting work, each with the date it was recorded. NOT an allowlist:
# a city here is one whose provenance is missing and known to be missing. Delete
# the entry when the rows land - leaving it stale fails the check.
KNOWN_GAPS = {}

# Slug for a city whose pipeline package is not named after its display name.
SLUG_OVERRIDES = {
    "Vancouver (Regional)": "vancouver",
    "Guadalajara (Regional)": "guadalajara",
    "Miami (Regional)": "miami",
    "Washington D.C.": "washington_dc",
    "Montréal": "montreal",
    "Mexico City": "mexico_city",
}

# A city's rows may name it differently from its page title - Vancouver's are
# filed under "Vancouver" and "Surrey" because the build spans two
# municipalities. Map display name -> the names any of which satisfies a table.
TABLE_ALIASES = {
    "Vancouver (Regional)": ("Vancouver", "Surrey"),
    "Guadalajara (Regional)": ("Guadalajara",),
    "Miami (Regional)": ("Miami",),
    "Washington D.C.": ("Washington D.C.",),
}

# A notice's heading in app/components.py is the publisher's full legal name;
# data_sources.md numbers it by the short name the rest of the file uses. Both
# spellings are deliberate, so the bijection is checked through this map rather
# than by loosening the match until everything passes.
NOTICE_ALIASES = {
    "San Francisco Municipal Transportation Agency": "SFMTA",
    "Chicago Transit Authority": "CTA",
    "OpenStreetMap (Mexican rail)": "OpenStreetMap",
}

TABLES = (
    ("## Business registries", "business registries"),
    ("## Transit feeds (GTFS)", "transit feeds"),
    ("## Boundary layers", "boundary layers"),
)

# URLs that are deliberately not in data_sources.md, with the reason. Keep this
# tiny; the default answer to "this URL is not recorded" is to record it.
URL_EXEMPT = {
    # Documentation pointers inside config comments, not fetched by the build.
    "https://github.com/dacekroberts/expanded-heatmap",
}


def read(path):
    return path.read_text(encoding="utf-8")


def section(text, heading, headings):
    """Return the slice of `text` under `heading`, up to the next heading."""
    start = text.index(heading)
    later = [text.index(h) for h in headings if text.index(h) > start]
    return text[start:min(later)] if later else text[start:]


def city_names():
    """Parse app/cities.py without importing streamlit."""
    tree = ast.parse(read(CITIES_PY))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == "CITIES" for t in node.targets
        ):
            return [
                next(
                    v.value
                    for k, v in zip(d.keys, d.values)
                    if getattr(k, "value", None) == "name"
                )
                for d in node.value.elts
            ]
    sys.exit("check_provenance: could not find CITIES in app/cities.py")


def resolved_urls(slug):
    """Import a city's config and collect every http(s) URL it resolves to.

    Importing rather than grepping is the point: Vancouver builds four of its
    endpoints from an `_ODS` prefix via f-strings, so the literal never appears
    in the file and a grep would report them absent.
    """
    try:
        mod = importlib.import_module(f"pipeline.{slug}.config")
    except Exception as exc:                                  # noqa: BLE001
        return None, f"could not import pipeline.{slug}.config: {exc}"
    urls = set()

    def walk(value):
        if isinstance(value, str):
            if value.startswith("http"):
                urls.add(value)
        elif isinstance(value, dict):
            for v in value.values():
                walk(v)
        elif isinstance(value, (list, tuple, set, frozenset)):
            for v in value:
                walk(v)

    for name in dir(mod):
        if not name.startswith("_"):
            walk(getattr(mod, name))
    return urls, None


def notice_headings(doc):
    """(number, heading) for each numbered notice in data_sources.md."""
    sec = doc[doc.index("## Notices this project MUST display when published"):]
    out = []
    for m in re.finditer(r"^\*\*(\d+)\.\s+(.+?)\s+—", sec, re.M):
        out.append((int(m.group(1)), m.group(2).strip().strip("*")))
    return out


def displayed_notices():
    """Headings in app/components.py's _NOTICES, read as source, not imported."""
    src = read(COMPONENTS_PY)
    start = src.index("_NOTICES")
    end = src.index("def ", start)
    return re.findall(r'^\s{4}\("([^"]+)"', src[start:end], re.M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="ignore KNOWN_GAPS and fail on every finding")
    args = ap.parse_args()

    doc = read(DATA_SOURCES)
    headings = [h for h, _ in TABLES] + ["## Geocoding"]
    blocks = {label: section(doc, h, headings) for h, label in TABLES}

    failures, gaps = [], []
    names = city_names()
    print(f"check_provenance: {len(names)} cities in app/cities.py\n")

    # --- A + B, per city ---------------------------------------------------
    for name in names:
        known = name in KNOWN_GAPS and not args.strict
        problems = []

        for alias_source in (TABLE_ALIASES.get(name, (name,)),):
            for label in blocks:
                if not any(
                    re.search(r"^\|\s*\**" + re.escape(a), blocks[label], re.M)
                    for a in alias_source
                ):
                    problems.append(f"no row in {label}")

        slug = SLUG_OVERRIDES.get(name, name.lower().replace(" ", "_"))
        urls, err = resolved_urls(slug)
        if err:
            problems.append(err)
        else:
            # Compare percent-DECODED, both sides. San Francisco's boundary
            # endpoint resolves to `county%3D%27San%20Francisco%27` while
            # data_sources.md records the readable `county='San Francisco'`.
            # Those are the same request and a raw string compare calls them
            # different.
            doc_plain = unquote(doc)
            missing = sorted(
                u for u in urls
                if u not in URL_EXEMPT
                and u not in doc and unquote(u) not in doc_plain
            )
            problems += [f"endpoint not in data_sources.md: {u}"
                         for u in missing]

        if problems:
            (gaps if known else failures).append((name, problems))
        else:
            if name in KNOWN_GAPS and not args.strict:
                failures.append((name, [
                    "listed in KNOWN_GAPS but nothing is missing - delete the "
                    "entry; the list may only shrink"]))
            else:
                print(f"  OK   {name}")

    # --- C + D, notices ----------------------------------------------------
    numbered = notice_headings(doc)
    nums = [n for n, _ in numbered]
    doc_headings = {h for _, h in numbered}
    shown = displayed_notices()

    if nums != list(range(1, len(nums) + 1)):
        dupes = sorted({n for n in nums if nums.count(n) > 1})
        failures.append(("notices", [
            f"numbers are not unique and contiguous from 1: {nums}"
            + (f" (duplicates: {dupes})" if dupes else "")]))

    for h in shown:
        candidate = NOTICE_ALIASES.get(h, h)
        if not any(candidate in dh or dh in candidate for dh in doc_headings):
            failures.append(("notices", [
                f"'{h}' is DISPLAYED in app/components.py but has no numbered "
                f"item in data_sources.md"]))

    print(f"\n  notices: {len(numbered)} numbered, {len(shown)} displayed")

    # --- report ------------------------------------------------------------
    if gaps:
        print("\n" + "=" * 70)
        print("OPEN GAPS - these are DEFECTS, not exemptions. Fix and delete")
        print("the KNOWN_GAPS entry. Run with --strict to fail on them.")
        print("=" * 70)
        for name, problems in gaps:
            print(f"\n  {name}  [{KNOWN_GAPS[name]}]")
            for p in problems:
                print(f"      - {p}")

    if failures:
        print("\n" + "=" * 70)
        print("FAILED")
        print("=" * 70)
        for name, problems in failures:
            print(f"\n  {name}")
            for p in problems:
                print(f"      - {p}")
        print("\nA city whose provenance is unrecorded looks exactly like a "
              "city that was checked.\nThat is what this script exists to "
              "tell apart. Record the source; do not\nrelax the check.")
        return 1

    print("\nAll recorded." if not gaps else
          "\nNo new failures, but the open gaps above are still open.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
