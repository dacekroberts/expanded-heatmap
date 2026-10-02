"""Step 2 - Kansas City's storefronts from KCMO's Business License Holders.

Input:  data/kansas_city/raw/business_licenses.csv
        data/kansas_city/raw/naics_2022_codes.xlsx
        data/kansas_city/raw/city_boundary_tiger.geojson
Output: data/kansas_city/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **Frozen on 2026-01-15**, so only licences current then are kept: valid
    for 2025 or 2026 (owner, call 10). The page states the data date.
  * **The register writes NAICS 2022 TITLES, not codes**, with the commas
    dropped. Each title is mapped back to its code through the Census
    Bureau's title file, and the shared naics.py classifies unchanged. The
    fee codes some rows carry in place of a title ("Misc Rate 129") name no
    industry: dropped and counted (owner, call 12).
  * **A person's business shows its address, not a name** (Houston's
    sole-owner rule, owner call 11). `dba_name` is the LICENCE HOLDER on every
    row (config explains); where it reads as a person - the register writes
    people surname first, "SURNAME GIVEN-NAME INITIAL" - the business is a person's, and
    the pin shows its address. Otherwise the pin shows the trade name
    (`business_name`) where the register has one, else the holder company -
    unless that trade name is itself a person's (config.PERSON_NAMED_TRADE).
  * **At an apartment or a trailer, a business is a home**, and is left off
    (Sacramento's owner call, Houston's rule). The register's addresses carry
    no unit at all (0 of the kept rows, 2026-09-30), so the test is kept for a
    refresh but does not fire; the person rule above is what protects a home.
  * **Placed by the register's own point**, kept only inside the City of
    Kansas City as TIGER draws it.

Run:  python pipeline/kansas_city/step2_clean_businesses.py
"""
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.kansas_city import config  # noqa: E402
from pipeline.kansas_city.step1_stations import city_polygon  # noqa: E402
from pipeline.residence import looks_organisational, looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.naics import VALUE_COLUMN  # noqa: E402

FETCH = "pipeline/kansas_city/fetch_sources.py"

# A dwelling in the business's own address: Houston's set (APT is
# Sacramento's owner call, TRLR pipeline/residence.py's).
HOME_UNIT = r"\s(?:APT|APARTMENT|TRLR)\b"

# THE HOLDER TEST. The register writes a person surname first, letters only:
# SURNAME GIVEN [MIDDLE...] [initial] [JR|SR|II|III|IV] - "SURNAME GIVEN-NAME INITIAL",
# "SURNAME GIVEN-NAME", a four-part surname then one given name. Two to six words, no digits or
# "&", and no organisation word (residence.py's list, plus the legal and trade
# words this register's companies carry, read off the holders the shape test
# caught, 2026-09-30). It is meant to over-fire: a false "person" only shows
# a company's address in place of its name.
ORG_EXTRA = re.compile(
    r"\b(L\s?L\s?C|L\s?C|P\s?C|P\s?A|PLLC|INC|INCORPORATED|CORPORATION|CORP|CO|LTD|"
    r"LIMITED|LP|LLP|PARTNERSHIP|ASSOCIATES|INVESTMENTS?|PROPERTY|RENTALS?|SALES|"
    r"CAPITAL|PRODUCTS?|INDUSTRIES|MISSOURI|KANSAS|KC|AMERICA|AMERICAN|NATIONAL|"
    r"BANK|FINANCIAL|INSURANCE|AGENCY|EXPRESS|TRAVEL|WIRELESS|PHARMACY|DRUGS?|"
    r"GROCERY|GROCERS|MOTOR|TIRES?|BEER|SPIRITS|TOBACCO|SMOKE|VAPOR|VAPE|BOOKS|"
    r"SOUND|MUSIC|ARTS|FLORAL|JEWELRY|JEWELERS|OPTICAL|FITNESS|YOGA|GYM|STORES?|"
    r"OUTLET|DEPOT|TRADING|IMPORTS?|EXPORTS?|ESTATE)\b")
PERSON_SURNAME_FIRST = re.compile(
    r"^[A-Z][A-Z'\-]+(?:\s+[A-Z][A-Z'\-]*){1,4}(?:\s+(?:JR|SR|II|III|IV))?$")
# A trailing single initial after two or three words is a person even where a
# word is also a trade word ("FLOWERS BOBBIE S", "WINE CHASE MARLENE M").
PERSON_WITH_INITIAL = re.compile(r"^[A-Z][A-Z'\-]+(?:\s+[A-Z][A-Z'\-]+){1,2}\s+[A-Z]$")
LEGAL_FORM = re.compile(r"\b(L\s?L\s?C|INC|INCORPORATED|CORPORATION|CORP|CO|LTD|LIMITED|"
                        r"LP|LLP|PLLC|PC|PA|PARTNERSHIP)\b")


TRAILING_FORM = re.compile(r"[\s,.]*\b(L\.?\s?L\.?\s?C\.?|INC\.?|CORP\.?|CO\.?|LTD\.?|"
                           r"P\.?C\.?|PLLC|LLP|LP)\s*$")


def strip_legal_form(name):
    """"GIVEN-NAME SURNAME LLC" -> "GIVEN-NAME SURNAME"; a trailing THE too ("... LLC THE")."""
    s = str(name or "").strip()
    for _ in range(2):
        s = re.sub(r"\s+THE$", "", TRAILING_FORM.sub("", s).strip(" ,."))
    return s


def holder_is_person(holder):
    s = re.sub(r"\s+", " ", str(holder or "").upper()).strip(" .,")
    if not s or re.search(r"[\d&/,.]", s):
        return False
    if PERSON_WITH_INITIAL.match(s) and not LEGAL_FORM.search(s):
        return True
    return (bool(PERSON_SURNAME_FIRST.match(s)) and not ORG_EXTRA.search(s)
            and not looks_organisational(s))


def naics_title_lut():
    """Normalised NAICS 2022 title -> its longest code (a 5- and a 6-digit
    code often share a title; the 6-digit one is the industry)."""
    p = config.NAICS_TITLES_XLSX
    if not p.exists():
        sys.exit(f"missing {p}\nRun: python {FETCH}")
    t = pd.read_excel(p, dtype=str)
    code_col = [c for c in t.columns if "Code" in c][0]
    title_col = [c for c in t.columns if "Title" in c][0]
    lut = {}
    for code, title in zip(t[code_col], t[title_col]):
        code = str(code).strip()
        if not code.isdigit():
            continue
        k = norm_title(title)
        if k not in lut or len(code) > len(lut[k]):
            lut[k] = code
    return lut


def norm_title(s):
    # The file marks trilateral titles with a trailing "T"; the register drops
    # every comma. Compare on letters and digits alone.
    s = re.sub(r"(?<=[a-z)])T\s*$", "", str(s).strip())
    return re.sub(r"[^a-z0-9]", "", s.lower())


def title_to_code(titles, lut):
    """Exact on the normalised title; else the one NAICS title the register's
    text begins (it truncates long titles: "Freight Transportation
    Arrangemen"). Exits on a title that maps to nothing or to two codes."""
    out = {}
    for title in sorted(set(titles)):
        k = norm_title(title)
        if k in lut:
            out[title] = lut[k]
            continue
        hits = {c for t, c in lut.items() if t.startswith(k)}
        longest = {c for c in hits if len(c) == max(map(len, hits))} if hits else set()
        if len(longest) != 1:
            sys.exit(f"business_type {title!r} matches {sorted(hits) or 'no'} NAICS 2022 "
                     f"title(s) - map it by hand")
        out[title] = longest.pop()
        print(f"    truncated title {title!r} -> {out[title]}")
    return out


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}\nRun: python {FETCH}")
    df = pd.read_csv(config.REGISTER_CSV, dtype=str, keep_default_na=False)
    print(f"Loaded {len(df):,} licence holders (frozen {config.REGISTER_DATA_DATE})")
    emit("register_rows", len(df))

    print(f"  valid for: {df['valid_license_for'].value_counts().to_dict()}")
    df = df[df["valid_license_for"].isin(config.VALID_FOR_KEEP)].copy()
    print(f"  current at the freeze ({'/'.join(v[:4] for v in config.VALID_FOR_KEEP)}): "
          f"{len(df):,}")
    emit("current_licences", len(df))

    fee = df["business_type"].str.match(config.FEE_CODE)
    print(f"  fee codes in place of an industry (\"Misc Rate 129\"): {int(fee.sum()):,} "
          f"dropped")
    emit("fee_code_dropped", int(fee.sum()))
    df = df[~fee].copy()

    print("  NAICS 2022 titles -> codes:")
    codes = title_to_code(df["business_type"], naics_title_lut())
    df[VALUE_COLUMN] = df["business_type"].map(codes)
    print(f"    {len(codes):,} distinct titles, every one mapped")

    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  storefront NAICS: {before:,} -> {len(df):,}")
    emit("storefront_rows", len(df))

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    no_point = df["latitude"].isna() | df["longitude"].isna()
    print(f"  no point: {int(no_point.sum()):,}")
    df = df[~no_point]
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=df.index)
    inside = pts.within(city_polygon())
    print(f"  outside the City of Kansas City, Missouri: {int((~inside).sum()):,} "
          f"(by city field: {df.loc[~inside, 'city'].value_counts().head(5).to_dict()})")
    emit("outside_city", int((~inside).sum()))
    df = df[inside].copy()

    df["address"] = df["address"].str.upper().str.replace(r"\s+", " ", regex=True).str.strip()
    home = df["address"].str.contains(HOME_UNIT, regex=True)
    print(f"  at an apartment or trailer: {int(home.sum()):,} left off as homes")
    emit("home_unit_dropped", int(home.sum()))
    df = df[~home]

    # One row per premises, on the name the register gives (trade name, else
    # holder) - BEFORE a person's name is replaced by the address, or two
    # people's businesses at one address would merge.
    holder = df["dba_name"].str.strip()
    trade = df["business_name"].str.strip()
    df["_shown"] = trade.where(trade != "", holder)
    key = df["_shown"].str.upper().str.replace(r"[^A-Z0-9]", "", regex=True) + "|" \
        + df["address"]
    before = len(df)
    df = df.assign(_k=key).sort_values(["_k", "id"]).drop_duplicates("_k")
    print(f"  one row per premises (name + address): {before:,} -> {len(df):,}")

    # A PERSON'S BUSINESS SHOWS ITS ADDRESS (Houston's sole-owner rule, owner
    # call 11), decided on the HOLDER: where it is a person, neither their name
    # nor the trade name they registered is shown. A company's trade name is
    # shown as it chose it (Philadelphia's and San Diego's reading: a name a
    # business registered to trade under is public commercial information) -
    # unless the company is named only as a person (config.PERSON_NAMED).
    person_held = df["dba_name"].map(holder_is_person)
    bare = df["_shown"].map(strip_legal_form)
    person_named = ~person_held & bare.isin(config.PERSON_NAMED)
    gone = set(config.PERSON_NAMED) - set(bare[person_named])
    if gone:
        sys.exit(f"PERSON_NAMED names no longer shown: {sorted(gone)} - re-read the list "
                 f"against the register")
    print(f"  holder reads as a person: {int(person_held.sum()):,}; a company named only "
          f"as a person (config.PERSON_NAMED): {int(person_named.sum()):,}")
    df["name_is_address"] = person_held | person_named
    df["business_name"] = df["_shown"].where(~df["name_is_address"], df["address"])
    shown_holder = ~df["name_is_address"] & (df["business_name"] == holder.loc[df.index])
    print(f"    -> {int(df['name_is_address'].sum()):,} show the address; the rest show the "
          f"trade name {int((~df['name_is_address'] & ~shown_holder).sum()):,}, the holder "
          f"company {int(shown_holder.sum()):,}")
    still = ~df["name_is_address"] & bare.map(looks_personal)
    print(f"    shown names shaped like a person's but read as shop names or brands "
          f"(residence.py; check_personal_exposure reports them): {int(still.sum()):,}")
    emit("name_as_address", int(df["name_is_address"].sum()))

    b = config.KANSAS_CITY_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    out = df.rename(columns={"id": "licence", "zipcode": "zip"})[
        ["licence", "business_name", VALUE_COLUMN, "business_type", "address", "zip",
         "name_is_address", "latitude", "longitude"]]
    out = out.sort_values("licence").reset_index(drop=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
