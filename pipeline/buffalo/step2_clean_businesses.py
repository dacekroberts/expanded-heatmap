"""Step 2 - Buffalo's storefronts from THREE registries (New York's shape).

Input:  data/buffalo/raw/city_licences.csv              (qcyy-feh8)
        data/buffalo/raw/nys_retail_food_stores.csv     (9a8c-vfzj)
        data/buffalo/raw/nys_appearance_enhancement.csv (y3u4-jbgh)
        data/buffalo/raw/city_boundary.geojson          (p4ak-r4fg)
Output: data/buffalo/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **"Active" means nothing in the City's file** - `licstatus` is Active on
    every row - so a licence counts only while `expdttm` is on or after
    config.AS_OF_DATE, the fetch date (Chicago's rule).
  * **The City's `businessname` is the trade name** and `dbaname` usually the
    legal entity, the reverse of the usual pair: businessname is displayed.
  * **The State's files are scoped by point-in-boundary**, never by their
    postal city, which reaches into Cheektowaga and Amherst.
  * **One row per site, across sources**, on address AND a normalised name
    (New York's key): under-merging is the safer error, and both numbers
    are printed.
  * **No registrant name is read.** `license_holder_name` is never
    downloaded, and this step asserts it.

Run:  python pipeline/buffalo/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.buffalo import config  # noqa: E402
from pipeline.new_york.step2_clean_businesses import norm_address, norm_name  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.buffalo import (  # noqa: E402
    CITY_DESCRIPT_EXCLUDED,
    NYS_SALON_EXCLUDE_LICENSE_TYPES,
    NYS_SALON_KEEP_LICENSE_TYPES,
    SOURCE_PRIORITY,
)
from pipeline.taxonomies.new_york import nys_store_label  # noqa: E402

SHARED = ["source", "source_key", "business_name", "business_category", "address",
          "unit", "zip", "latitude", "longitude"]
POINT_RE = r"POINT \((-?\d+\.?\d*) (-?\d+\.?\d*)\)"


CITY_GROCERY_CODES = ("FOOD STORE", "MEAT FISH & POULTRY")
_STREET_NOISE = {"ST", "STREET", "AVE", "AVENUE", "AV", "RD", "ROAD", "DR", "DRIVE",
                 "BLVD", "BOULEVARD", "PL", "PLACE", "PKWY", "PARKWAY", "TER",
                 "TERRACE", "CT", "COURT", "LN", "LANE", "HWY", "SQ", "PLZ", "CIR",
                 "E", "W", "N", "S", "EAST", "WEST", "NORTH", "SOUTH"}


def street_key(value):
    """'1281 E DELAVAN AVE ###' and '1281 DELAVAN EAST' -> '1281 DELAVAN'.
    The house number and the street's core words; suffixes, directions and
    punctuation dropped. Only ever compared within one trade (grocers)."""
    words = "".join(c if c.isalnum() else " " for c in str(value or "").upper()).split()
    if not words or not words[0][:1].isdigit():
        return ""
    core = [w for w in words[1:] if w not in _STREET_NOISE]
    return " ".join([words[0].lstrip("0")] + core)


def _read(spec):
    if not spec["file"].exists():
        sys.exit(f"missing {spec['file']}\nRun: python pipeline/buffalo/fetch_sources.py")
    return pd.read_csv(spec["file"], dtype=str, keep_default_na=False, na_values=[""])


def _frame(df, source, spec, name, category, address, zip_col, lat, lon, unit=None):
    return pd.DataFrame({
        "source": source,
        "source_key": df[spec["key_column"]].astype(str).str.strip(),
        "business_name": name.fillna("").str.strip(),
        "business_category": category.fillna("").str.strip(),
        "address": address.fillna("").str.strip(),
        "unit": "" if unit is None else unit.fillna("").str.strip(),
        "zip": zip_col.fillna("").astype(str).str.strip().str.slice(0, 5),
        "latitude": pd.to_numeric(lat, errors="coerce"),
        "longitude": pd.to_numeric(lon, errors="coerce"),
    }, index=df.index)


def load_city(spec):
    df = _read(spec)
    print(f"  loaded {len(df):,} rows ({len(config.CITY_LICENCE_CODES)} codes, filtered at download)")
    status = df["licstatus"].fillna("").value_counts().to_dict()
    print(f"  licstatus: {status}  <- uninformative, so the expiry date decides")
    expiry = pd.to_datetime(df["expdttm"], errors="coerce")
    live = expiry >= pd.Timestamp(config.AS_OF_DATE)
    print(f"  unexpired on {config.AS_OF_DATE}: {int(live.sum()):,} of {len(df):,} "
          f"({int((~live).sum()):,} past expdttm; {int(expiry.isna().sum()):,} undated)")
    df = df[live]
    code = df["descript"].fillna("").str.strip()
    for c, why in CITY_DESCRIPT_EXCLUDED.items():
        n = int((code.str.upper() == c).sum())
        print(f"  excluded {c.title():<16} {n:>4}  - {why}")
    emit("city_unexpired", len(df))
    return _frame(df, "city", spec, name=df["businessname"], category=code,
                  address=df["address"], zip_col=df["zip"],
                  lat=df["latitude"], lon=df["longitude"])


def load_nys_store(spec):
    df = _read(spec)
    print(f"  loaded {len(df):,} rows (postal city BUFFALO, filtered at download)")
    before = len(df)
    df = df[(df["operation_type"].fillna("").str.strip().str.upper() == "STORE")
            & df["estab_type"].fillna("").str.upper().str.startswith("A")]
    print(f"  operation_type Store and estab_type 'A...' (Article 28-A store): "
          f"{before:,} -> {len(df):,}")
    point = df["georeference"].fillna("").str.extract(POINT_RE)
    address = (df["street_number"].fillna("").str.strip() + " "
               + df["street_name"].fillna("").str.strip()).str.strip()
    # The trade name where the State records one, else the licensee entity -
    # New York's rule; check_personal_exposure.py reads the result.
    name = df["dba_name"].where(df["dba_name"].fillna("").str.strip() != "",
                                df["entity_name"])
    return _frame(df, "nys_store", spec, name=name,
                  category=df["estab_type"].map(nys_store_label), address=address,
                  zip_col=df["zip_code"], lat=point[1], lon=point[0],
                  unit=df["address_line_2"])


def load_nys_salon(spec):
    df = _read(spec)
    print(f"  loaded {len(df):,} rows (business city Buffalo, filtered at download)")
    assert "license_holder_name" not in df.columns, (
        "license_holder_name reached step 2: it is a person's name. Fix config.SOURCES.")
    kinds = df["license_type"].fillna("").str.strip().str.upper()
    print("  licence types: " + ", ".join(f"{k} {n}" for k, n in kinds.value_counts().items()))
    df = df[kinds.isin(NYS_SALON_KEEP_LICENSE_TYPES)]
    print(f"  business licences only -> {len(df):,} (dropped "
          f"{', '.join(NYS_SALON_EXCLUDE_LICENSE_TYPES)}: individuals renting a chair)")
    # AT AN APARTMENT, A SALON IS A HOME: left off (owner, 2026-09-29). The
    # register's `business_address_2` writes the unit as "Apt-509".
    unit = df["business_address_2"].fillna("").str.upper()
    home = unit.str.startswith("APT") | df["business_address_1"].fillna("").str.upper() \
        .str.contains(r"\bAPT\b", regex=True)
    print(f"  at an apartment unit: {int(home.sum()):,} left off as homes")
    emit("salon_apartment_dropped", int(home.sum()))
    df = df[~home]
    point = df["georeference"].fillna("").str.extract(POINT_RE)
    return _frame(df, "nys_salon", spec, name=df["business_name"],
                  category=kinds.loc[df.index].map(NYS_SALON_KEEP_LICENSE_TYPES),
                  address=df["business_address_1"], zip_col=df["business_zip"],
                  lat=point[1], lon=point[0], unit=df["business_address_2"])


LOADERS = {"city": load_city, "nys_store": load_nys_store, "nys_salon": load_nys_salon}


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    frames = []
    for source, spec in config.SOURCES.items():
        print(f"\n=== {source} ===")
        f = LOADERS[source](spec)[SHARED]
        print(f"  -> {len(f):,} rows ({int(f['latitude'].isna().sum()):,} without a point)")
        frames.append(f)
    df = pd.concat(frames, ignore_index=True)
    print(f"\n=== combined: {len(df):,} rows ===")

    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"Storefront filter: {before:,} -> {len(df):,}")
    df = df[df["business_name"] != ""]

    # No point: a small share of the State's rows (the brief: 98.0% and 99.8%
    # georeferenced). Dropped and counted, not geocoded - under Los Angeles'
    # threshold for recovery, and printed per source.
    nopoint = df["latitude"].isna() | df["longitude"].isna()
    for s in config.SOURCES:
        n = int((nopoint & (df["source"] == s)).sum())
        if n:
            print(f"  {s}: {n:,} rows with no point, dropped")
    df = df[~nopoint]

    # Point-in-boundary: the City's own polygon, the only in-city test.
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    shape = city.geometry.union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=df.index)
    inside = pts.within(shape)
    print("\nInside the City of Buffalo (point-in-boundary):")
    for s in config.SOURCES:
        m = df["source"] == s
        print(f"  {s:<10} {int((inside & m).sum()):>5,} of {int(m.sum()):>5,}")
    df = df[inside]

    # --- One row per site, across sources: address AND name -----------------
    TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    df["_bucket"] = [TAX.classify({"business_category": c, "source": s})
                     for c, s in zip(df["business_category"], df["source"])]
    df["_addr"] = df["address"].map(norm_address) + "|" + df["zip"]
    df["_site"] = df["_addr"] + "|" + df["business_name"].map(norm_name)
    print(f"\nDedup: {len(df) - df['_addr'].nunique():,} rows share an address with "
          f"another row - NOT merged on address alone")
    rank_key = df["source"].where(~((df["source"] == "city")
                                    & (df["_bucket"] == "Food service")), "city_food")
    df["_rank"] = rank_key.map({s: i for i, s in enumerate(SOURCE_PRIORITY)})
    before = len(df)
    df = df.sort_values(["_site", "_rank", "source_key"]).drop_duplicates("_site")
    print(f"One row per site (address + name): {before:,} -> {len(df):,}")
    for s in config.SOURCES:
        print(f"  {s:<10} {int((df['source'] == s).sum()):>5,} survive")

    # --- A second pass for ONE trade: grocers the City and the State both list.
    # The address + name key misses them because the two registers write one
    # address differently - the City "442 WILLIAM", "1281 DELAVAN EAST"; the
    # State "442 WILLIAM ST", "1281 E DELAVAN AVE" - and the City's name is
    # often the company where the State's is the shop ("SHERAWALI INC." /
    # "DOWNTOWN FOOD MART", 472 Main). Measured 2026-09-29: 257 of the City's
    # 331 grocery licences had a State food store within 50 m. Two grocers at
    # one house number on one street are one shop; the State's row is kept.
    # Restricted to the grocery trade, so a deli and the restaurant beside it
    # are never merged.
    grocer = (((df["source"] == "city")
               & df["business_category"].str.upper().isin(CITY_GROCERY_CODES))
              | (df["source"] == "nys_store"))
    df["_street"] = df["address"].map(street_key) + "|" + df["zip"]
    shared = set(df.loc[grocer & (df["source"] == "nys_store"), "_street"])
    dup = grocer & (df["source"] == "city") & df["_street"].isin(shared) & (df["_street"] != "|")
    print(f"Grocers in both registers (house number + street, suffixes and "
          f"directions ignored): {int(dup.sum()):,} City rows merged into the "
          f"State's")
    emit("city_grocers_merged", int(dup.sum()))
    df = df[~dup]

    # --- A salon licensed under a person's own name shows its licence type ---
    # The State's salon register often carries the licensee's own name as the
    # BUSINESS name ("Julia Wachna", "Luis A Aviles"), mostly in salon-suite
    # buildings. Where the name reads as a person's (pipeline.residence's
    # shared test), the pin shows the licence type instead - Vancouver's and
    # Kobe's "type in place of a personal name" (owner, 2026-09-29). Done
    # AFTER the dedup, so two named suites at one address stay two pins.
    salon = df["source"] == "nys_salon"
    person = salon & df["business_name"].map(looks_personal)
    df.loc[person, "business_name"] = df.loc[person, "business_category"]
    print(f"\nSalon names that read as a person's: {int(person.sum()):,} of "
          f"{int(salon.sum()):,} show the licence type instead")
    emit("salon_name_as_type", int(person.sum()))

    b = config.BUFFALO_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    print("\nBy bucket:")
    print(df["_bucket"].value_counts().to_string())
    for bucket, n in df["_bucket"].value_counts().items():
        emit(f"bucket_{bucket.lower().replace(' ', '_')}", int(n))
    emit("storefronts", len(df))

    out = df[SHARED].sort_values(["source", "source_key"]).reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
