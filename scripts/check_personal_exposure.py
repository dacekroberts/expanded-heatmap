"""Personal-data exposure check for a city's rendered map. Read-only.

Every `outputs/<city>/heatmap.html` is committed and meant to be served
publicly, and each pin carries a business NAME at a mapped COORDINATE. Where a
registry has no trade name for a row, the pipelines fall back to the owner or
registrant - which for a sole proprietor is a person's name, often at their
home address. Run this before publishing a city, and whenever a city's step 2
or its taxonomy changes.

    python scripts/check_personal_exposure.py                # every known city
    python scripts/check_personal_exposure.py los_angeles    # one city

It reports, per city:
  * pins whose displayed name can ONLY be the owner/registrant fallback
    (joined back to the raw trade-name column: the authoritative measure),
  * pins whose displayed name matches a conservative personal-name pattern
    (a heuristic - it flags "Jane Smith" and misses "J Smith Consulting"),
  * how many of those sit at an address with an APT/UNIT/STE/# indicator,
  * the classifications those pins carry, so a catch-all code sweeping in
    home-based registrants shows up by name.

Nothing here is a hard pass/fail: a trade name someone chose for their shop is
public commercial information, while a registrant name at a flat number is not.
Read the numbers, then decide per city and record the verdict in DECISIONS.md.
A new city must be added to REGISTRIES below (the columns are per registry).

Los Angeles is the worked example: excluding NAICS 812990 there (2026-09-21)
cut person-like pins from 3,998 to 1,803. See DECISIONS.md.
"""
import html
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# city slug -> how to find the trade name and the fallback in its RAW export.
# raw: file under data/<slug>/raw/; trade: the dba-style column; owner: what
# step 2 falls back to when trade is blank; processed/address: for the
# unit-indicator check (None to skip).
REGISTRIES = {
    "san_diego": dict(raw="sd_businesses_active_datasd.csv", trade="dba_name",
                      owner="business_owner_name", processed="businesses_clean.csv",
                      address=("address_no", "address_road", "address_suite")),
    "san_francisco": dict(raw="sf_business_locations.csv", trade="dba_name",
                          owner="ownership_name", processed="businesses_clean.csv",
                          address=("full_business_address",)),
    "los_angeles": dict(raw="la_active_businesses.csv", trade="dba_name",
                        owner="business_name", processed="businesses_geocoded.csv",
                        address=("street_address",)),
    "chicago": dict(raw="business_licenses_active.csv", trade="doing_business_as_name",
                    owner="legal_name", processed="businesses_clean.csv",
                    address=("address",)),
}

# Tokens that make a name read as an organisation rather than a person. Kept
# broad on purpose: a false "organisation" only makes the report conservative.
ORG = re.compile(
    r"\b(INC|LLC|L\.?L\.?C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PC|PLC|GROUP|"
    r"ENTERPRISE|ENTERPRISES|HOLDING|HOLDINGS|SERVICES|SERVICE|SALON|SHOP|STORE|"
    r"MARKET|CAFE|RESTAURANT|BAR|GRILL|PIZZA|LIQUOR|CLEANERS|CLEANER|BARBER|NAIL|"
    r"NAILS|SPA|STUDIO|BOUTIQUE|DELI|BAKERY|FOOD|FOODS|MART|CENTER|CENTRE|TRUST|"
    r"ASSOCIATION|ASSOC|PARTNERS|PARTNERSHIP|VENTURES|VENTURE|BROS|BROTHERS|THE|AND|"
    r"OF|DBA|USA|INTERNATIONAL|MANAGEMENT|PROPERTIES|REALTY|CONSTRUCTION|DESIGN|"
    r"SOLUTIONS|SYSTEMS|TECHNOLOGIES|CONSULTING|MEDICAL|DENTAL|CLINIC|CHURCH|SCHOOL|"
    r"ACADEMY|FOUNDATION|INSTITUTE|SUPPLY|WHOLESALE|RETAIL|AUTO|MOTORS|REPAIR|"
    r"PLUMBING|ELECTRIC|TRUCKING|TRANSPORT|LOGISTICS|BEAUTY|HAIR|SKIN|MASSAGE|"
    r"TATTOO|LAUNDRY|PET|DOG|KIDS|HOUSE|HOME|CITY|CLUB|LOUNGE|GIFTS)\b")
NOT_A_NAME = re.compile(r"[&/,\d\.]")
PERSON = re.compile(r"^[A-Z][A-Za-z'\-]{1,}(?:\s+[A-Z])?\s+[A-Z][A-Za-z'\-]{1,}$")
UNIT = re.compile(r"\b(APT|UNIT|STE|SUITE|SPC|#)\b")


def pins(slug):
    """[lat, lon, name, classification, station, ring] for every pin in the map."""
    text = (ROOT / "outputs" / slug / "heatmap.html").read_text(encoding="utf-8")
    return [r for b in re.findall(r"var data = (\[\[.*?\]\]);", text, re.S) for r in json.loads(b)]


def looks_personal(name):
    upper = name.upper()
    return bool(PERSON.match(name)) and not ORG.search(upper) and not NOT_A_NAME.search(upper)


def check(slug):
    spec = REGISTRIES.get(slug)
    if spec is None:
        print(f"\n=== {slug}: NOT IN REGISTRIES - add its trade/owner columns to this script")
        return
    rows = pins(slug)
    names = [html.unescape(r[2]).strip() for r in rows]
    print(f"\n=== {slug}: {len(rows):,} pins, {len(set(names)):,} distinct names")

    raw_path = ROOT / "data" / slug / "raw" / spec["raw"]
    if raw_path.exists():
        raw = pd.read_csv(raw_path, dtype=str, low_memory=False)
        trade = raw[spec["trade"]].fillna("").str.strip()
        owner = raw[spec["owner"]].fillna("").str.strip()
        fallback = set(owner[(trade == "") & (owner != "")].str.upper())
        trade_set = set(trade[trade != ""].str.upper())
        only_fb = [n for n in names if n.upper() in fallback and n.upper() not in trade_set]
        print(f"  blank trade name in raw: {int((trade == '').sum()):,} of {len(raw):,} "
              f"({100 * (trade == '').mean():.1f}%)")
        print(f"  pins that can ONLY be the {spec['owner']} fallback: {len(only_fb):,} "
              f"({100 * len(only_fb) / len(rows):.1f}%)")
    else:
        print(f"  raw file missing ({raw_path.name}); skipping the fallback join")

    personal = [(html.unescape(r[2]).strip(), html.unescape(str(r[3]))) for r in rows
                if looks_personal(html.unescape(r[2]).strip())]
    print(f"  pins whose name looks like a person: {len(personal):,} "
          f"({100 * len(personal) / len(rows):.1f}%)  [heuristic]")
    if personal:
        by_class = pd.Series([c for _, c in personal]).value_counts().head(5)
        print(f"  their top classifications: {by_class.to_dict()}")

    proc = ROOT / "data" / slug / "processed" / spec["processed"]
    if personal and spec["address"] and proc.exists():
        d = pd.read_csv(proc, dtype=str, low_memory=False)
        cols = [c for c in spec["address"] if c in d.columns]
        if cols and "business_name" in d.columns:
            addr = d[cols].fillna("").agg(" ".join, axis=1).str.upper()
            want = {n.upper() for n, _ in personal}
            hit = d["business_name"].fillna("").str.strip().str.upper().isin(want)
            if int(hit.sum()):
                flagged = UNIT.search  # noqa: F841 - readability
                unit_hits = addr[hit].map(lambda a: bool(UNIT.search(a)))
                print(f"  of {int(hit.sum()):,} matching processed rows, "
                      f"{int(unit_hits.sum()):,} ({100 * unit_hits.mean():.1f}%) have an "
                      "APT/UNIT/STE/# in the address (possible residence)")


def main():
    slugs = sys.argv[1:] or sorted(p.name for p in (ROOT / "outputs").iterdir() if p.is_dir())
    print("Personal-data exposure in the rendered maps (read-only).")
    print("A trade name is public commercial information; a registrant's name at a")
    print("flat number is not. Decide per city and record it in DECISIONS.md.")
    for slug in slugs:
        if (ROOT / "outputs" / slug / "heatmap.html").exists():
            check(slug)
        else:
            print(f"\n=== {slug}: no rendered map")


if __name__ == "__main__":
    main()
