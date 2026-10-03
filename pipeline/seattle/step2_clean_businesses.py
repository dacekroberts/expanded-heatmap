"""Step 2 - Seattle (Regional)'s storefronts from FIVE sources (the
multi-source-city skill), each in the places the owner assigned it (the
brief's "What the build has to pull"; pipeline/seattle/config.py's table).

Input:  data/seattle/raw/seattle_licences.csv        (City of Seattle)
        data/seattle/raw/bellevue_licences.csv       (City of Bellevue)
        data/seattle/raw/kc_food_inspections.csv     (Public Health - Seattle & King County)
        data/seattle/raw/kc_address_points.csv       (King County, the food join)
        data/seattle/raw/sno_food_establishments.csv (pipeline/seattle/sno_food.py)
        data/seattle/raw/lcb_off_premise_*.xlsx      (pipeline/seattle/lcb_offpremise.py)
        data/seattle/processed/places.geojson, business_scope.geojson (step 1)
Output: data/seattle/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **Every source is scoped by point-in-place**, never by a city-name field:
    Seattle's addresses all read SEATTLE although 1,012 rows lie elsewhere,
    and King County food's `city` is the postal city.
  * **Seattle: every licence year kept** (owner, 2026-10-02). A lapsed FOOD
    row (licence year 2025 or earlier) stays only if King County inspected a
    matching business in 2025 or 2026, by trade name or street address.
    Lapsed retail and personal rows stay, disclosed as possibly closed.
  * **Seattle: HEADER QUARTER and BRANCH both kept, and the head-office rule
    applied** to HEADER QUARTER rows (owner, 2026-10-02; Taipei's rule).
  * **Bellevue: retail and personal services only, issued 2010-01-01 or
    later** (owner, 2026-10-02); its food is King County's.
  * **King County food: a business inspected in 2025 or 2026**, placed by its
    parcel through King County's address points. In Seattle it adds what the
    register lacks by trade name and by street address.
  * **A name that reads as a person's shows the category instead**
    (Vancouver's and Buffalo's rule; the Seattle licence read: person-named
    trade names are never published). A row with no trade name does too.
  * **One row per site across sources**, on address AND a normalised name;
    then grocers sharing a house number and street. Under-merging is the
    safer error; both numbers are printed.
  * **No contact, phone, mailing or legal-name column is read.** The fetch
    never requests them, and this step asserts it.

Run:  python pipeline/seattle/step2_clean_businesses.py
"""
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.new_york.step2_clean_businesses import norm_address, norm_name  # noqa: E402
from pipeline.residence import has_residential_unit, looks_organisational, looks_personal  # noqa: E402
from pipeline.seattle import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.seattle import (  # noqa: E402
    FOOD_NAME_KINDS,
    KC_CLASSIFICATION_OUT,
    KC_CLASSIFICATION_TO_BUCKET,
    SOURCE_PRIORITY,
    food_premises_kind,
)

SHARED = ["source", "source_key", "business_name", "business_category", "naics",
          "address", "municipality", "placement", "latitude", "longitude"]
TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)

# Columns that must never reach this step (the fetch never requests them).
FORBIDDEN = {
    "seattle": ("BUSLIC_CONTACT_NAME", "BUSLIC_PHONE_NUM", "BUSLIC_MAIL_ADRS_TEXT",
                "BUSLIC_LEGAL_NAME"),
    "bellevue": ("LegalEntityName", "Ubi", "MailingAddressLine1", "MailingAddressLine2",
                 "MailingCity", "MailingPostalCode"),
}

# Where each source is used (the brief's "What each jurisdiction publishes").
SEATTLE = "Seattle"
BELLEVUE = "Bellevue"
SNOHOMISH_PLACES = ("Lynnwood", "Mountlake Terrace", config.SNO_UNINCORPORATED)

# A unit, suite or floor inside a street address: dropped for the building key.
_UNIT = re.compile(r"\s(#|STE|SUITE|UNIT|APT|BLDG|FL|FLR|FLOOR|RM|ROOM|SPC|LOWR|UPPR)\b.*$")
# The head-office rule's office markers: a floor of 3 or higher, or a room.
_FLOOR = re.compile(r"\b(?:FL|FLR|FLOOR)\s*(\d+)\b|\b(\d+)(?:ST|ND|RD|TH)\s+(?:FL|FLR|FLOOR)\b")
_ROOM = re.compile(r"\b(?:RM|ROOM)\b")
OFFICE_FLOOR_MIN = 3
OFFICE_EXEMPT_ROWS_AT_ADDRESS = 20


def street_of(address):
    """'1234 MAIN ST # 200, SEATTLE, WA 98101-1234' -> '1234 MAIN ST # 200'."""
    return str(address or "").split(",")[0].strip().upper()


def base_key(street):
    """The building: the normalised street address with any unit dropped."""
    return norm_address(_UNIT.sub("", " " + str(street or "").upper()).strip())


def _read(path, label):
    if not Path(path).exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/seattle/fetch_sources.py")
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""])


def _frame(source, key, name, category, naics_code, address, lat, lon, placement):
    return pd.DataFrame({
        "source": source, "source_key": key.astype(str).str.strip(),
        "business_name": name.fillna("").astype(str).str.strip(),
        "business_category": category.fillna("").astype(str).str.strip(),
        "naics": naics_code.fillna("").astype(str).str.strip() if naics_code is not None else "",
        "address": address.fillna("").astype(str).str.strip(), "municipality": "",
        "placement": placement,
        "latitude": pd.to_numeric(lat, errors="coerce"),
        "longitude": pd.to_numeric(lon, errors="coerce")})


def label_places(df, places):
    """Each row's place, by point-in-polygon; outside every loaded place ''."""
    pts = gpd.GeoDataFrame(df[[]], geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
                           crs=config.CRS_GEOGRAPHIC)
    j = gpd.sjoin(pts, places[["city", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated()]
    return j["city"].fillna("").reindex(df.index)


def person_named(names, structural):
    """The name rule's test: a STRUCTURAL signal that the registrant is a
    person (Seattle: the trade name is the legal name; Bellevue: a sole
    proprietorship) AND a name shaped like a person's with no organisation
    word. The shape test alone is not used: it reads two-word shop names
    ("BLUE MOON") as people, 2,079 of Seattle's 9,349 rows when tried."""
    return structural & names.map(looks_personal) & ~names.map(looks_organisational)


# --- King County food ---------------------------------------------------------

def load_kc_food(points):
    spec = config.SOURCES["kc_food"]
    k = _read(spec["file"], "King County food inspections")
    print(f"  {len(k):,} inspection rows, {k['business_id'].nunique():,} businesses")
    k["_d"] = pd.to_datetime(k["inspection_date"], errors="coerce")
    last = k.sort_values(["business_id", "_d", "inspection_serial_num"]).groupby(
        "business_id").tail(1)
    year = last["_d"].dt.year
    print("  last inspected, by year: " + ", ".join(
        f"{y} {n}" for y, n in year.value_counts().sort_index().items()))
    last = last[year >= 2025]
    print(f"  inspected in 2025 or 2026: {len(last):,}  (the currency rule's snapshot)")
    emit("kc_food_current", len(last))
    cls = last["classification"].fillna("").str.strip().str.upper()
    unknown = set(cls) - set(KC_CLASSIFICATION_TO_BUCKET) - set(KC_CLASSIFICATION_OUT)
    if unknown:
        sys.exit(f"King County classifications not in the taxonomy: {sorted(unknown)}")
    for c, why in KC_CLASSIFICATION_OUT.items():
        n = int((cls == c).sum())
        if n:
            print(f"    out  {c.title():<32} {n:>5}  {why}")

    # Placement by parcel: the address point on the parcel whose address is
    # the business's; else the parcel's primary point; else an address match
    # that names one place only. Unplaced rows are dropped and counted.
    pts = points.copy()
    pts["_base"] = pts["ADDR_FULL"].map(base_key)
    by_pin_addr = pts.drop_duplicates(["PIN", "_base"]).set_index(["PIN", "_base"])
    prim = pts[pts["PRIM_ADDR"] == "1"].drop_duplicates("PIN").set_index("PIN")
    span = pts.groupby("_base").agg(lat_min=("latitude", "min"), lat_max=("latitude", "max"),
                                    lon_min=("longitude", "min"), lon_max=("longitude", "max"),
                                    latitude=("latitude", "mean"),
                                    longitude=("longitude", "mean"))
    # One place: every point under that address within about 150 m.
    one_place = span[((span.lat_max - span.lat_min) < 0.0014)
                     & ((span.lon_max - span.lon_min) < 0.002)]
    last = last.copy()
    last["_base"] = last["address"].map(base_key)
    tiers, lat, lon = [], [], []
    for pin, b in zip(last["parcel_number"].fillna(""), last["_base"]):
        hit, tier = None, "unplaced"
        if pin and (pin, b) in by_pin_addr.index:
            hit, tier = by_pin_addr.loc[(pin, b)], "parcel and address"
        elif pin and pin in prim.index:
            hit, tier = prim.loc[pin], "parcel"
        elif b in one_place.index:
            hit, tier = one_place.loc[b], "address"
        tiers.append(tier)
        lat.append(None if hit is None else hit["latitude"])
        lon.append(None if hit is None else hit["longitude"])
    last["_tier"], last["latitude"], last["longitude"] = tiers, lat, lon
    print("  placement: " + ", ".join(f"{t} {n:,}" for t, n in
                                       last["_tier"].value_counts().items()))
    for t, n in last["_tier"].value_counts().items():
        emit(f"kc_food_placed_{t.replace(' ', '_')}", int(n))
    # The tooltip shows the inspection program's own class.
    return _frame("kc_food", last["business_id"], last["name"],
                  last["classification"].str.strip(), None, last["address"],
                  last["latitude"], last["longitude"], last["_tier"]), last


# --- City of Seattle -----------------------------------------------------------

def load_seattle(places, kc_current):
    spec = config.SOURCES["seattle"]
    s = _read(spec["file"], "Seattle licences")
    bad = [c for c in FORBIDDEN["seattle"] if c in s.columns]
    assert not bad, f"{bad} reached step 2: never requested. Fix config.SOURCES."
    print(f"  {len(s):,} rows (every one ACTIVE, every one with a point)")
    before = len(s)
    s = s.drop(columns="objectid").drop_duplicates()
    print(f"  exact duplicate rows dropped: {before - len(s):,}")
    s["_year"] = pd.to_numeric(s["BUSLIC_YEAR_NUM"], errors="coerce")
    before = len(s)
    s = s.sort_values(["BUSLIC_LOCATION_ID", "_year", "BUSLIC_ID"]).drop_duplicates(
        "BUSLIC_LOCATION_ID", keep="last")
    print(f"  one row per location, its latest licence: {before:,} -> {len(s):,}")
    f = _frame("seattle", s["BUSLIC_LOCATION_ID"], s["BUSLIC_TRADE_NAME"],
               s["BUSLIC_NAICS_DESC"].str.strip().str.capitalize(), s["BUSLIC_NAICS_CODE"],
               s["BUSLIC_LOCATION_ADRS_TEXT"].map(street_of), s["latitude"], s["longitude"],
               "register point")
    f["_year"], f["_loctype"] = s["_year"].values, s["BUSLIC_LOCATION_TYPE"].values
    same = set(_read(config.SOURCES["seattle_same_name"]["file"],
                     "Seattle same-name ids")["BUSLIC_LOCATION_ID"])
    f["_person"] = person_named(f["business_name"], f["source_key"].isin(same))
    f["municipality"] = label_places(f, places)
    out = f["municipality"] != SEATTLE
    print(f"  outside the City of Seattle: {int(out.sum()):,} (" + ", ".join(
        f"{m or 'none'} {n}" for m, n in f.loc[out, "municipality"].value_counts().items())
        + ") - dropped: a Seattle licence is no cover of another place")
    f = f[~out]
    f["_bucket"] = [TAX.classify({"source": "seattle", "naics": c}) for c in f["naics"]]
    f = f[f["_bucket"].notna()]
    print(f"  in the buckets: {len(f):,}  " + str(f["_bucket"].value_counts().to_dict()))
    emit("seattle_bucket_rows", len(f))

    # The head-office rule on HEADER QUARTER rows (Taipei's, owner 2026-10-02).
    street = f["address"].str.upper()
    floor = street.str.extract(_FLOOR).astype(float).max(axis=1)
    officey = (floor >= OFFICE_FLOOR_MIN) | street.str.contains(_ROOM)
    building = street.map(base_key)
    exempt = building.map(building.value_counts()) >= OFFICE_EXEMPT_ROWS_AT_ADDRESS
    hq = f["_loctype"] == "HEADER QUARTER"
    drop = hq & officey & ~exempt
    print(f"  head-office rule: {int((hq & officey).sum())} HEADER QUARTER rows on floor "
          f"{OFFICE_FLOOR_MIN}+ or in a room, {int((hq & officey & exempt).sum())} exempt "
          f"(a building with {OFFICE_EXEMPT_ROWS_AT_ADDRESS}+ storefront rows), "
          f"{int(drop.sum())} dropped; {int((~hq & officey).sum())} BRANCH rows look the same "
          f"and stay")
    emit("seattle_head_office_dropped", int(drop.sum()))
    f = f[~drop]

    # Lapsed food: kept only where King County inspected a matching business in
    # 2025 or 2026 inside Seattle, by trade name or street address.
    kc = kc_current[kc_current["municipality"] == SEATTLE]
    kc_names = set(kc["business_name"].map(norm_name)) - {""}
    kc_streets = set(kc["address"].map(base_key)) - {""}
    food = f["_bucket"] == "Food service"
    lapsed = f["_year"] <= 2025
    by_name = f["business_name"].map(norm_name).isin(kc_names)
    by_street = f["address"].map(base_key).isin(kc_streets)
    print("  food rows by licence year (rows / name match / street match / either):")
    for y in sorted(f.loc[food, "_year"].dropna().unique()):
        m = food & (f["_year"] == y)
        n = int(m.sum())
        print(f"    {int(y)}  {n:>5}  {int((m & by_name).sum()):>5}  "
              f"{int((m & by_street).sum()):>5}  {int((m & (by_name | by_street)).sum()):>5}")
    drop = food & lapsed & ~(by_name | by_street)
    for y in sorted(f.loc[drop, "_year"].unique()):
        n = int((drop & (f["_year"] == y)).sum())
        print(f"    lapsed {int(y)} food rows with no inspected match, dropped: {n}")
        emit(f"seattle_lapsed_food_dropped_{int(y)}", n)
    f["_street_only"] = food & lapsed & by_street & ~by_name
    print(f"  kept on a street match alone: {int(f['_street_only'].sum())} (hand-sampled "
          f"2026-10-02, the drafts file)")
    emit("seattle_lapsed_food_street_only", int(f["_street_only"].sum()))
    f = f[~drop]
    for b in ("Retail", "Personal services"):
        n = int(((f["_bucket"] == b) & (f["_year"] <= 2025)).sum())
        print(f"  lapsed {b} rows kept, disclosed as possibly closed: {n}")
        emit(f"seattle_lapsed_{b.lower().replace(' ', '_')}_kept", n)
    return f


# --- City of Bellevue ----------------------------------------------------------

def load_bellevue(places, titles):
    spec = config.SOURCES["bellevue"]
    b = _read(spec["file"], "Bellevue licences")
    bad = [c for c in FORBIDDEN["bellevue"] if c in b.columns]
    assert not bad, f"{bad} reached step 2: never requested. Fix config.SOURCES."
    print(f"  {len(b):,} rows (licences never expire; CancelDate is the only closure)")
    cancel = pd.to_datetime(b["CancelDate"], format="%m/%d/%Y", errors="coerce")
    live = cancel.isna() | (cancel > pd.Timestamp(config.AS_OF_DATE))
    print(f"  not cancelled on {config.AS_OF_DATE}: {int(live.sum()):,} "
          f"({int((cancel > pd.Timestamp(config.AS_OF_DATE)).sum())} cancel dates in the future)")
    b = b[live].copy()
    code = b["Naic"].fillna("").str.strip()
    f = _frame("bellevue", b["BusinessId"], b["Dba"],
               code.map(titles).fillna(""), code,
               b["PhysicalAddressLine1"].fillna("") + (" " + b["PhysicalAddressLine2"]).fillna(""),
               b["latitude"], b["longitude"], "register point")
    f["_issued"] = pd.to_datetime(pd.to_numeric(b["IssueDate"], errors="coerce"), unit="ms")
    f["_person"] = person_named(f["business_name"],
                                b["LegalEntityType"].fillna("").str.upper()
                                .isin(["SOLE PROPRIETORSHIP", "INDIVIDUAL"]))
    f = f[f["latitude"].notna()]
    f["municipality"] = label_places(f, places)
    f = f[f["municipality"] == BELLEVUE]
    print(f"  inside the City of Bellevue: {len(f):,}")
    f["_bucket"] = [TAX.classify({"source": "bellevue", "naics": c}) for c in f["naics"]]
    f = f[f["_bucket"].notna()]
    print(f"  Retail and Personal services (food is King County's): {len(f):,} "
          + str(f["_bucket"].value_counts().to_dict()))
    old = f["_issued"] < pd.Timestamp("2010-01-01")
    undated = f["_issued"].isna()
    print(f"  issued before 2010-01-01, dropped: {int(old.sum())}; no issue date: "
          f"{int(undated.sum())} (kept: the cutoff needs a date to apply)")
    emit("bellevue_pre2010_dropped", int(old.sum()))
    f = f[~old]
    # No NAICS title in the register: a code Seattle's register names takes
    # that title, else the bucket's name.
    f.loc[f["business_category"] == "", "business_category"] = f["_bucket"]
    return f


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    places = gpd.read_file(config.PLACES_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    scope = gpd.read_file(config.SCOPE_GEOJSON).to_crs(config.CRS_GEOGRAPHIC).geometry.union_all()
    points = _read(config.KC_ADDRESS_CSV, "King County address points")[
        ["PIN", "ADDR_FULL", "PRIM_ADDR", "latitude", "longitude"]]
    points["latitude"] = pd.to_numeric(points["latitude"])
    points["longitude"] = pd.to_numeric(points["longitude"])

    print("\n=== kc_food ===")
    kc, kc_raw = load_kc_food(points)
    kc = kc[kc["latitude"].notna()].copy()
    kc["municipality"] = label_places(kc, places)
    kc["_bucket"] = [TAX.classify({"source": "kc_food", "business_category": c})
                     for c in kc["business_category"]]
    in_seattle = kc["municipality"] == SEATTLE
    print(f"  in Seattle: {int(in_seattle.sum()):,} (each matched to the register below)")

    print("\n=== seattle ===")
    sea = load_seattle(places, kc[kc["_bucket"].notna()])
    titles = (sea.drop_duplicates("naics").set_index("naics")["business_category"])

    # In Seattle the register AND King County food (the brief's table): a
    # King County business the register holds by trade name or by street
    # address is the register's row; the rest join as King County rows (1,572
    # of 5,182, every class, on 2026-10-02; 1,080 storefronts inside the
    # scope after the storefront filter and the dedup, nearly all General
    # Food Services). Matching on either key errs toward under-adding.
    names = set(sea["business_name"].map(norm_name)) - {""}
    streets = set(sea["address"].map(base_key)) - {""}
    held = in_seattle & (kc["business_name"].map(norm_name).isin(names)
                         | kc["address"].map(base_key).isin(streets))
    print(f"  King County food in Seattle: {int(in_seattle.sum()):,}; held by the register "
          f"{int(held.sum()):,}; added {int((in_seattle & ~held).sum()):,}")
    emit("kc_food_added_in_seattle", int((in_seattle & ~held).sum()))

    print("\n=== bellevue ===")
    bel = load_bellevue(places, titles)

    print("\n=== sno_food ===")
    from pipeline.seattle import sno_food
    sno = sno_food.load()
    print(f"  {len(sno):,} facilities from the module")

    print("\n=== lcb_retail ===")
    from pipeline.seattle import lcb_offpremise
    lcb = lcb_offpremise.load()
    print(f"  {len(lcb):,} premises from the module")

    frames = []
    for f in (kc[~held], sea, bel, sno, lcb):
        f = f.copy()
        if "municipality" not in f.columns or (f["municipality"] == "").all():
            f["municipality"] = ""
        for c in SHARED:
            if c not in f.columns:
                f[c] = ""
        f["_person"] = f["_person"].astype(bool) if "_person" in f.columns else False
        frames.append(f[SHARED + ["_person"]])
    df = pd.concat(frames, ignore_index=True)
    df = df[df["latitude"].notna() & df["longitude"].notna()]
    df["municipality"] = label_places(df, places)

    # Each source in its own places only.
    allowed = {
        "seattle": lambda m: m == SEATTLE,
        "bellevue": lambda m: m == BELLEVUE,
        "kc_food": lambda m: ~m.isin(SNOHOMISH_PLACES) & (m != ""),
        "sno_food": lambda m: m.isin(SNOHOMISH_PLACES),
        "lcb_retail": lambda m: ~m.isin([SEATTLE, BELLEVUE]) & (m != ""),
    }
    keep = pd.Series(False, index=df.index)
    for s, rule in allowed.items():
        m = df["source"] == s
        keep |= m & rule(df["municipality"])
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=df.index)
    in_scope = pts.within(scope)
    print("\nIn each source's own places and inside the business scope:")
    for s in SOURCE_PRIORITY:
        m = df["source"] == s
        print(f"  {s:<11} {int((m & keep & in_scope).sum()):>6,} of {int(m.sum()):>6,}")
    df = df[keep & in_scope].copy()

    # The food registers' name layer (Minneapolis's precedent; the taxonomy's
    # FOOD_NAME_PATTERNS): a workplace cafeteria, vending route, hotel kitchen,
    # members' club or pharmacy filed as food service is written as its kind,
    # which maps to no bucket.
    food = df["source"].isin(["kc_food", "sno_food"])
    kinds = [food_premises_kind(c, n) for c, n in
             zip(df.loc[food, "business_category"], df.loc[food, "business_name"])]
    df.loc[food, "business_category"] = kinds
    named = df.loc[food, "business_category"].isin(FOOD_NAME_KINDS)
    print("\nThe food registers' name layer (left out by name):")
    for (s, k), n in df.loc[food][named].groupby(["source", "business_category"]).size().items():
        print(f"  {s:<9} {k:<26} {n:>4}")
        emit(f"name_kind_{s}_{k.lower().replace(' ', '_')}", int(n))

    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"Storefront filter: {before:,} -> {len(df):,}")
    df["_bucket"] = [TAX.classify(r) for r in df[["source", "business_category", "naics"]]
                     .to_dict("records")]

    # --- One row per site, across sources: address AND name -----------------
    df["_base"] = df["address"].map(lambda a: base_key(street_of(a)))
    df["_site"] = df["_base"] + "|" + df["business_name"].map(norm_name)
    df["_rank"] = df["source"].map({s: i for i, s in enumerate(SOURCE_PRIORITY)})
    before = len(df)
    df = df.sort_values(["_site", "_rank", "source_key"]).drop_duplicates("_site")
    print(f"\nOne row per site (address + name): {before:,} -> {len(df):,}")
    emit("site_dedup_merged", before - len(df))
    # A second pass for grocers: a Liquor Board grocery licence, or Bellevue's
    # own grocery licence, at the house number and street of a food register's
    # shop is that shop. Restricted to shops, so a restaurant and the grocer
    # beside it are never merged.
    shop = (df["source"].isin(["kc_food", "sno_food"])) & (df["_bucket"] == "Retail")
    shops = set(df.loc[shop, "_base"]) - {""}
    second = (((df["source"] == "lcb_retail")
               | ((df["source"] == "bellevue") & df["naics"].str.startswith("445")))
              & df["_base"].isin(shops))
    print(f"Grocers in a food register and another source at one address: "
          f"{int(second.sum()):,} merged into the food register's row "
          + str(df.loc[second, "source"].value_counts().to_dict()))
    emit("grocers_merged", int(second.sum()))
    df = df[~second]

    # --- The name rule, after the dedup --------------------------------------
    # No trade name, or a person's own name by the register's structural
    # signal (person_named): the category shows instead. The food registers'
    # and the Liquor Board's names are premises names, read by
    # scripts/check_personal_exposure.py rather than swapped wholesale.
    print("\nThe name rule (the category shown instead of the name):")
    # A name shaped like a person's at a residential unit (APT, UNIT, PH...)
    # is treated as one in every source: 13 such pins inside the rings on the
    # first render (2026-10-02), read by check_personal_exposure.py.
    blank = df["business_name"] == ""
    home = (df["business_name"].map(looks_personal)
            & df["address"].map(has_residential_unit))
    swap = blank | df["_person"] | home
    for s in SOURCE_PRIORITY:
        m = df["source"] == s
        print(f"  {s:<11} {int((m & blank).sum()):>5} without a trade name, "
              f"{int((m & df['_person']).sum()):>5} a person's own name, "
              f"{int((m & home & ~df['_person']).sum()):>4} a person-like name at a "
              f"residential unit")
    df.loc[swap, "business_name"] = df.loc[swap, "business_category"]
    emit("names_shown_as_category", int(swap.sum()))

    b = config.SEATTLE_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    print("\nBy place and source:")
    print(pd.crosstab(df["municipality"], df["source"], margins=True).to_string())
    print("\nBy bucket:")
    print(df["_bucket"].value_counts().to_string())
    for bucket, n in df["_bucket"].value_counts().items():
        emit(f"bucket_{bucket.lower().replace(' ', '_')}", int(n))
    for s, n in df["source"].value_counts().items():
        emit(f"source_{s}", int(n))
    emit("storefronts", len(df))

    out = df[SHARED].sort_values(["source", "source_key"]).reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
