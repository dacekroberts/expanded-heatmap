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
    # New York assembles four registries and NEVER loads a registrant-name
    # column (the salon file's license_holder_name is not even downloaded; its
    # step 2 asserts that). So there is no trade/owner fallback pair to join
    # against - raw and owner are None and the fallback measure is reported as
    # structurally absent, which is a stronger statement than a low count.
    # Its `unit` column is structured (DCA gives APT/STE/FL/RM as their own
    # values), so unlike San Diego the residence check here is real.
    "new_york": dict(raw=None, trade=None, owner=None,
                     processed="businesses_geocoded.csv",
                     address=("address", "unit")),
    # Philadelphia likewise never loads a registrant-name column (its step 2
    # asserts six of them stay absent), and its business_name is never blank,
    # so there is no fallback pair to join against either. What it adds that no
    # other city has is `legalentitytype`: Individual vs a corporate entity,
    # recorded by the registry itself. That is a STRUCTURAL signal, so here the
    # person-like-name regex is the cross-check and this column is the measure
    # - the other way round from every city above.
    "philadelphia": dict(raw=None, trade=None, owner=None,
                         processed="businesses_clean.csv",
                         address=("address", "unit_type", "unit_num"),
                         entity_type="legalentitytype",
                         entity_individual="Individual"),
    # Miami never loads a registrant-name column either: OWNERNAME is populated
    # on 100% of rows and is frequently a person, so fetch_sources.py does not
    # download it and step 2 asserts it and every MAIL* field stay absent.
    # There is therefore no trade/owner fallback pair to join against, and -
    # unlike Los Angeles (68% blank dba_name) and D.C. (49%) - none is needed,
    # because BUSNAME is present on every row. So `raw`, `trade` and `owner`
    # are None and the fallback measure reports as structurally absent, which
    # is a stronger statement than a low count.
    #
    # Its address is one free-text field, so the unit check is a regex over
    # BUSADDR rather than a structured column the way New York's is.
    "miami": dict(raw=None, trade=None, owner=None,
                  processed="businesses_clean.csv",
                  address=("address",)),
    # Boston never loads a personal-name column either: the ISD table carries
    # legalowner/namelast/namefirst and the Licensing Board table carries
    # applicant/manager/day_phone, and fetch_sources.py selects none of them -
    # step 2 asserts all eight stay absent. So the fallback measure reports as
    # structurally absent here too.
    #
    # READ ITS RESIDENCE FIGURE WITH CARE. Boston's addresses carry NO unit
    # designators at all - 0 of its person-like rows have an APT, UNIT, STE or
    # # - so a 0.00% residential reading is a MEASUREMENT GAP, not a verified
    # clean result. Same shape as San Diego's old 0.03%, which turned out to be
    # 2.80% once a parcel join replaced the address text. What limits the real
    # exposure here is the sources rather than the check: a food-service
    # licence and a package-store licence both require commercial premises, so
    # a home cannot hold one. The ISD table's `property_id` IS Boston's
    # assessing parcel id, so a parcel join against the city's Property
    # Assessment data (ODC-PDDL) is available if that is ever not enough.
    "boston": dict(raw=None, trade=None, owner=None,
                   processed="businesses_clean.csv",
                   address=("address",)),
    # Washington D.C. is the first city since Chicago where the trade/owner
    # fallback pair genuinely EXISTS and has to be measured rather than
    # reported as structurally absent. Its step 2 falls back from
    # ENTITYTRADENAME to ENTITYNAME, which is the legal entity's name - a
    # company name for a corporation, and sometimes a person's.
    #
    # Step 0 read that as "the Los Angeles trap at half LA's severity", on a
    # 49% blank-trade-name rate. That rate was measured before the category
    # exclusions, and General Business - 11,074 office rows, mostly with no
    # trade name - is most of it. On the rows that reach the map the gap is
    # 26.9%, and 85.6% of those carry a company-shaped ENTITYNAME.
    #
    # It also carries a STRUCTURAL entity-type signal, like Philadelphia's:
    # ENTITYTYPE names the legal form, and it spells sole trading two ways, so
    # entity_individual is a TUPLE here. That distinction is what the
    # measurement turns on - an LLC registered under its founder's name is a
    # deliberate public commercial act (San Diego's reasoning), whereas a sole
    # proprietorship displaying a person's name is the case to look at.
    "washington_dc": dict(raw="basic_business_licenses.csv",
                          trade="ENTITYTRADENAME", owner="ENTITYNAME",
                          processed="businesses_geocoded.csv",
                          address=("street_address",),
                          entity_type="ENTITYTYPE",
                          entity_individual=("Sole Proprietorship",
                                             "Domestic Sole Proprietor")),
    # Vancouver is REGIONAL (Vancouver + Surrey) and the only entry here whose
    # processed file mixes two registries. `raw` points at Vancouver's own
    # export, because Surrey's has no trade/owner pair to join against: it
    # publishes a single BusinessName and no second name column, so Surrey
    # rows cannot be a substituted fallback by construction.
    #
    # Vancouver's fallback pair genuinely exists, as D.C.'s does:
    # businesstradename -> businessname, blank on 49.6% of MAPPABLE rows (the
    # 63.0% in the build brief was measured before the coordinate and category
    # exclusions - the denominator error this project keeps re-learning).
    #
    # ITS STRUCTURAL SIGNAL IS A NAME FORMAT, NOT A COLUMN, which is why
    # entity_type is absent here even though the city has a structural signal
    # as good as Philadelphia's or D.C.'s: Vancouver WRAPS A SOLE PROPRIETOR'S
    # OWN NAME IN PARENTHESES - "(Christopher Colonia)", "(Qi Liu)". Step 2
    # uses it as the primary signal, unioned with the person-name regex, and
    # records the result in two columns of the processed file:
    # `registrant_name` and `name_suppressed`. Those are reported below
    # instead of an entity_type.
    #
    # So read this city's person-like-name percentage as a CROSS-CHECK of a
    # structural measure, the same way round as Philadelphia's.
    #
    # Its `sep` is ";" - see the read_csv note in check().
    "vancouver": dict(raw="vancouver_business_licences.csv", sep=";",
                      trade="businesstradename", owner="businessname",
                      processed="businesses_clean.csv",
                      address=("address",)),
}

# Unit designators that suggest a residence, as opposed to a commercial suite.
# Splitting these is why Los Angeles' jewellery district stopped reading as 42%
# "residential" (DECISIONS.md, 2026-09-21): STE in the Diamond District is an
# office, APT is someone's home.
#
# CORRECTED 2026-09-21. These lists contradicted their own source write-up,
# `docs/passover_name_filtering_skill.md`, on three designators, and the
# contradiction inflated every city's reported residential share:
#   FL / FLOOR and RM / ROOM were listed as RESIDENTIAL here and COMMERCIAL
#     there. "FL 3" and "RM 200" are an office floor and a room in a
#     commercial building; a dwelling is APT or UNIT. Moved to commercial.
#   SPC was listed as COMMERCIAL here and RESIDENTIAL there. A "space" is a
#     mobile-home or trailer space, which is a home. Moved to residential,
#     with SPACE and TRLR added alongside it.
# The source's list also includes a bare LOT as residential (a trailer lot).
# That is deliberately NOT adopted: in these registries "LOT" is at least as
# likely to appear in a parking-lot address, and it could not be verified
# either way, so adopting it would trade a known error for an unknown one.
# PH / BSMT / REAR / LOWR are kept as residential - secondary dwelling units,
# a refinement the source write-up predates rather than contradicts.
UNIT_RESIDENTIAL = re.compile(
    r"\b(APT|APARTMENT|UNIT|PH|BSMT|REAR|LOWR|SPC|SPACE|TRLR)\b")
UNIT_COMMERCIAL = re.compile(
    r"\b(STE|SUITE|BLDG|BUILDING|FRNT|LBBY|OFC|FL|FLOOR|RM|ROOM)\b")

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

# --- Contact details -------------------------------------------------------
# A different exposure from a name, and a worse one: a name at a commercial
# address identifies a business, while an email address or mobile number is a
# direct line to a person. Added 2026-09-21 after a repo grep - not this script
# - found a Gmail address published as a New York pin's business name. Neither
# test above could have caught it: an email fails PERSON and contains an "@",
# and NOT_A_NAME does not list "@", so it was reported as clean.
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Conservative on purpose: a 10-digit run with separators, not any long number
# (a licence number or a street number must not match).
PHONE = re.compile(r"(?:\+?1[ .\-]?)?\(?\d{3}\)?[ .\-]\d{3}[ .\-]\d{4}")
# "C/O JOHN SMITH" names a person who is not the business. The separator is
# MANDATORY: an optional one (`C[/.]?O`) matches the bare abbreviation "CO" and
# flagged every "SAUSAGE CO" and "TYPEWRITER CO" in the project - 567 false
# positives across five cities before this was tightened.
CARE_OF = re.compile(r"\bC[/.]O\b|\bCARE\s+OF\b|\bATTN\b")

# "Andrew Polhemus (Molto Bene Ravioli Co)" - a registry that formats
# business_name as "LEGAL NAME (TRADE NAME)" publishes the licence holder's own
# name whenever the legal entity is an individual. PERSON cannot match it (the
# parenthesis and any digits fail NOT_A_NAME), so this form is invisible to
# every test above while displaying a person's name in full.
PERSON_THEN_TRADE = re.compile(
    r"^([A-Z][A-Za-z'\-]{1,}(?:\s+[A-Z]\.?)?\s+[A-Z][A-Za-z'\-]{1,})\s*\(")

# Registries record a licence holder surname-first, and NOT_A_NAME's comma rule
# treats that as evidence the string is NOT a person - backwards for exactly
# this form. Reported as its own number rather than folded into the PERSON
# count, so the older figures stay comparable across entries in DECISIONS.md.
PERSON_COMMA = re.compile(
    r"^[A-Z][A-Za-z'\-]{1,},\s*[A-Z][A-Za-z'\-]{1,}(?:\s+[A-Z]\.?)?$")


def mask_email(addr):
    local, _, domain = addr.partition("@")
    keep = local[:2] if len(local) > 2 else local[:1]
    return f"{keep}{'*' * max(len(local) - len(keep), 1)}@{domain}"


def mask_phone(num):
    digits = re.sub(r"\D", "", num)
    return f"***-***-{digits[-4:]}" if len(digits) >= 4 else "***"


def report_contact_details(rows, names):
    """Contact details and surname-first names in the DISPLAYED pin text.
    Prints masked values: the point is to find and count them, not reprint
    them."""
    emails, phones, commas, care_of = [], [], [], []
    for row, name in zip(rows, names):
        category = html.unescape(str(row[3])) if len(row) > 3 else ""
        for m in EMAIL.findall(name):
            emails.append((mask_email(m), category))
        # An email's digits must not also be counted as a phone number.
        stripped = EMAIL.sub("", name)
        for m in PHONE.findall(stripped):
            phones.append((mask_phone(m), category))
        if CARE_OF.search(name.upper()):
            care_of.append((name, category))
        if PERSON_COMMA.match(name) and not ORG.search(name.upper()):
            commas.append((name, category))

    print(f"  contact details in the displayed name: {len(emails)} email(s), "
          f"{len(phones)} phone number(s), {len(care_of)} 'c/o' marker(s)")
    for masked, cat in emails:
        print(f"    EMAIL {masked}  [{cat}]")
    for masked, cat in phones:
        print(f"    PHONE {masked}  [{cat}]")
    for name, cat in care_of[:5]:
        print(f"    C/O   {name!r}  [{cat}]")

    print(f"  surname-first names (\"Smith, John\"): {len(commas):,} "
          f"({100 * len(commas) / max(len(rows), 1):.1f}%)  "
          f"[NOT counted by the person-name heuristic - its comma rule "
          f"excludes them]")
    if commas:
        by_class = pd.Series([c for _, c in commas]).value_counts().head(5)
        print(f"    their top classifications: {by_class.to_dict()}")

    composite = []
    for row, name in zip(rows, names):
        m = PERSON_THEN_TRADE.match(name)
        if m and not ORG.search(m.group(1).upper()):
            composite.append((m.group(1), html.unescape(str(row[3]))
                              if len(row) > 3 else ""))
    print(f"  person's name followed by a trade name in brackets: "
          f"{len(composite):,} ({100 * len(composite) / max(len(rows), 1):.1f}%)"
          f"  [also invisible to the heuristic]")
    if composite:
        by_class = pd.Series([c for _, c in composite]).value_counts().head(5)
        print(f"    their top classifications: {by_class.to_dict()}")
    return len(emails) + len(phones), len(commas) + len(composite)


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

    if spec["raw"] is None:
        print("  no registrant-name fallback exists for this city: its step 2 "
              "never loads an owner/licence-holder column, so no pin can be "
              "one. Only registered trade names are displayed.")
        raw_path = None
    else:
        raw_path = ROOT / "data" / slug / "raw" / spec["raw"]
    if raw_path is not None and raw_path.exists():
        # `sep` per registry: Opendatasoft exports CSV SEMICOLON-delimited
        # (Vancouver), and read_csv's default comma parses such a file as one
        # single column, so every column lookup below would KeyError.
        raw = pd.read_csv(raw_path, dtype=str, low_memory=False,
                          sep=spec.get("sep", ","))
        trade = raw[spec["trade"]].fillna("").str.strip()
        owner = raw[spec["owner"]].fillna("").str.strip()
        fallback = set(owner[(trade == "") & (owner != "")].str.upper())
        trade_set = set(trade[trade != ""].str.upper())
        only_fb = [n for n in names if n.upper() in fallback and n.upper() not in trade_set]
        print(f"  blank trade name in raw: {int((trade == '').sum()):,} of {len(raw):,} "
              f"({100 * (trade == '').mean():.1f}%)")
        print(f"  pins that can ONLY be the {spec['owner']} fallback: {len(only_fb):,} "
              f"({100 * len(only_fb) / len(rows):.1f}%)")
    elif raw_path is not None:
        print(f"  raw file missing ({raw_path.name}); skipping the fallback join")

    report_contact_details(rows, names)

    personal = [(html.unescape(r[2]).strip(), html.unescape(str(r[3]))) for r in rows
                if looks_personal(html.unescape(r[2]).strip())]
    print(f"  pins whose name looks like a person: {len(personal):,} "
          f"({100 * len(personal) / len(rows):.1f}%)  [heuristic]")
    if personal:
        by_class = pd.Series([c for _, c in personal]).value_counts().head(5)
        print(f"  their top classifications: {by_class.to_dict()}")

    proc = ROOT / "data" / slug / "processed" / spec["processed"]

    # Where the registry records the entity type itself, report that first: it
    # is what the publisher asserts, not what a regex guesses.
    if spec.get("entity_type") and proc.exists():
        d = pd.read_csv(proc, dtype=str, low_memory=False)
        col, individual = spec["entity_type"], spec["entity_individual"]
        # A registry may spell one legal form several ways - D.C. has both
        # "Sole Proprietorship" and "Domestic Sole Proprietor" - so this
        # accepts a tuple as well as a single string.
        wanted = (individual,) if isinstance(individual, str) else tuple(individual)
        if col in d.columns:
            is_individual = d[col].fillna("").str.strip().isin(wanted)
            label = " / ".join(wanted)
            print(f"  {col}: {int(is_individual.sum()):,} of {len(d):,} mapped "
                  f"rows are {label!r} "
                  f"({100 * is_individual.mean():.1f}%)  [structural]")
            # The overlap is the population that actually matters: a row the
            # registry calls an individual AND whose displayed name reads as a
            # person's, rather than a trade name an individual registered.
            want = {n.upper() for n, _ in personal}
            named = d["business_name"].fillna("").str.strip().str.upper().isin(want)
            both = is_individual & named
            print(f"    {label} AND a person-like displayed name: "
                  f"{int(both.sum()):,} of {len(rows):,} pins "
                  f"({100 * int(both.sum()) / len(rows):.2f}%)")

    # A property register beats address text for "is this a home?": the unit
    # indicator below cannot see a detached house. Reported where a city's
    # step 2 carries the columns (Philadelphia joins the City's own parcel
    # data). See docs/data_sources.md and the add-city skill's Step 0.
    if proc.exists():
        d = pd.read_csv(proc, dtype=str, low_memory=False)
        if "parcel_landuse" in d.columns:
            occupied = d["parcel_owner_occupied"].astype(str).str.lower().eq("true")
            want = {n.upper() for n, _ in personal}
            named = d["business_name"].fillna("").str.strip().str.upper().isin(want)
            print(f"  parcel land use of mapped rows: "
                  f"{d['parcel_landuse'].value_counts(dropna=False).head(4).to_dict()}")
            print(f"    owner-occupied (homestead exemption): "
                  f"{int(occupied.sum()):,} of {len(d):,} "
                  f"({100 * occupied.mean():.1f}%)  [structural]")
            print(f"    person-like name AND owner-occupied parcel: "
                  f"{int((named & occupied).sum()):,}"
                  f"  - NOT filtered: most are mixed-use rowhouses where the "
                  f"owner lives above their own shop")

    if personal and spec["address"] and proc.exists():
        d = pd.read_csv(proc, dtype=str, low_memory=False)
        cols = [c for c in spec["address"] if c in d.columns]
        if cols and "business_name" in d.columns:
            addr = d[cols].fillna("").agg(" ".join, axis=1).str.upper()
            want = {n.upper() for n, _ in personal}
            hit = d["business_name"].fillna("").str.strip().str.upper().isin(want)
            if int(hit.sum()):
                unit_hits = addr[hit].map(lambda a: bool(UNIT.search(a)))
                print(f"  of {int(hit.sum()):,} matching processed rows, "
                      f"{int(unit_hits.sum()):,} ({100 * unit_hits.mean():.1f}%) have an "
                      "APT/UNIT/STE/# in the address (possible residence)")
                # Residential and commercial unit designators mean different
                # things; reported apart where the city carries a unit column.
                # Both are shares of the same base - the matching processed
                # rows - and NOT of the line above, whose regex is narrower
                # (it has no FL/RM/PH), so the residential count can exceed it.
                resid = addr[hit].map(lambda a: bool(UNIT_RESIDENTIAL.search(a)))
                comm = addr[hit].map(lambda a: bool(UNIT_COMMERCIAL.search(a)))
                print(f"    of the same {int(hit.sum()):,} rows: "
                      f"{int(resid.sum()):,} ({100 * resid.mean():.1f}%) at a "
                      f"residential unit (APT/UNIT/PH/SPC) and {int(comm.sum()):,} "
                      f"({100 * comm.mean():.1f}%) at a commercial one "
                      f"(STE/BLDG/FL/RM)")
                print(f"    PERSON-LIKE NAME AT A RESIDENTIAL UNIT: {int(resid.sum()):,} "
                      f"of {len(rows):,} pins ({100 * int(resid.sum()) / len(rows):.2f}%)")


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
