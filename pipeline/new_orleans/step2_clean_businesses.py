"""Step 2 - New Orleans's storefronts from the City's Active Occupational
Licenses.

Input:  data/new_orleans/raw/occupational_licenses.csv
        data/new_orleans/raw/city_boundary_tiger.geojson
Output: data/new_orleans/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **The owner is never read**: `ownername` (often a person's own name) and
    `businessphone` are never downloaded, and this step asserts neither
    arrived. A licence with no business name shows its address.
  * **The City's own text taxonomy**, `businesstype`, 486 values each with an
    explicit home in `pipeline/taxonomies/nola_businesstype.py`: mapped to the
    NAICS code its title names, so the shared carve-outs hold. Event vendors,
    home offices, flea-market stalls, street artists and video poker leave
    there; an unknown type stops this step.
  * **A business named only as a person shows its address** (Kansas City's
    rule; config.PERSON_NAMED, read by eye).
  * **At an apartment or a trailer, a business is a home**, and is left off
    (Sacramento's owner call, Houston's rule), read from `suite`.
  * **One row per premises** (name + address), placed by the register's own
    point and kept only inside the city as TIGER draws it.

Run:  python pipeline/new_orleans/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.new_orleans import config  # noqa: E402
from pipeline.name_keys import keys_of  # noqa: E402
from pipeline.new_orleans.step1_stations import city_polygon  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402

FETCH = "pipeline/new_orleans/fetch_sources.py"
HOME_UNIT = r"^(?:APT|APARTMENT|TRLR)\b"


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}\nRun: python {FETCH}")
    df = pd.read_csv(config.REGISTER_CSV, dtype=str, keep_default_na=False)
    leaked = [c for c in df.columns if c in config.FORBIDDEN_COLUMNS]
    assert not leaked, f"forbidden columns reached step 2: {leaked}"
    for c in df.columns:
        df[c] = df[c].str.strip()
    print(f"Loaded {len(df):,} active occupational licences")
    emit("register_rows", len(df))

    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  storefront types: {before:,} -> {len(df):,}")
    emit("storefront_rows", len(df))

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    # The register writes an ungeocoded licence at (0, 0), not blank: 219 of them,
    # 2026-09-30.
    no_point = df["latitude"].isna() | df["longitude"].isna() \
        | ((df["latitude"] == 0) & (df["longitude"] == 0))
    print(f"  no point (blank, or the register's 0,0): {int(no_point.sum()):,} not placed")
    emit("no_point", int(no_point.sum()))
    df = df[~no_point].copy()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=df.index)
    inside = pts.within(city_polygon())
    print(f"  outside the City of New Orleans: {int((~inside).sum()):,}")
    emit("outside_city", int((~inside).sum()))
    df = df[inside].copy()

    home = df["suite"].str.upper().str.contains(HOME_UNIT, regex=True)
    print(f"  at an apartment or trailer (suite): {int(home.sum()):,} left off as homes")
    emit("home_unit_dropped", int(home.sum()))
    df = df[~home]

    # A care-of or attention tail names a person or a tax office, not the shop
    # ("HANGER PROST & ORTH C/O GREG MYERS", "FOOT LOCKER #7379 ATTN: TAX DEPT"):
    # cut, before the name is used for anything.
    tail = df["businessname"].str.contains(r"\s(?:C/O|ATTN:?)\s", regex=True)
    df["businessname"] = df["businessname"].str.replace(r"\s+(?:C/O|ATTN:?)\s.*$", "",
                                                        regex=True).str.strip()
    print(f"  care-of or attention tails cut from the name: {int(tail.sum()):,}")
    df["address"] = (df["businessaddress"] + " " + df["suite"]).str.upper() \
        .str.replace(r"\s+", " ", regex=True).str.strip()
    key = df["businessname"].str.upper().str.replace(r"[^A-Z0-9]", "", regex=True) + "|" \
        + df["address"]
    before = len(df)
    df = df.assign(_k=key).sort_values(["_k", "businesslicensenumber"]).drop_duplicates("_k")
    print(f"  one row per premises (name + address): {before:,} -> {len(df):,}")

    no_name = df["businessname"] == ""
    name_keys = keys_of(df["businessname"])
    person_named = ~no_name & name_keys.isin(config.PERSON_NAMED)
    gone = set(config.PERSON_NAMED) - set(name_keys[person_named])
    if gone:
        sys.exit(f"PERSON_NAMED keys no longer matched: {sorted(gone)} - re-read the list "
                 f"against the register")
    df["name_is_address"] = no_name | person_named
    df["business_name"] = df["businessname"].where(~df["name_is_address"], df["address"])
    still = ~df["name_is_address"] & df["business_name"].map(looks_personal)
    print(f"  no business name: {int(no_name.sum()):,}; named only as a person "
          f"(config.PERSON_NAMED): {int(person_named.sum()):,} -> "
          f"{int(df['name_is_address'].sum()):,} show the address; shown names shaped like a "
          f"person's but read as shop names: {int(still.sum()):,}")
    emit("name_as_address", int(df["name_is_address"].sum()))

    b = config.NEW_ORLEANS_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    out = df.rename(columns={"businesslicensenumber": "licence"})[
        ["licence", "business_name", "businesstype", "address", "zip", "businessstartdate",
         "name_is_address", "latitude", "longitude"]]
    out = out.sort_values("licence").reset_index(drop=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
