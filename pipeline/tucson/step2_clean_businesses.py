"""Step 2 - Tucson's storefronts from the City's BUSLIC business-licence layer.

Input:  data/tucson/raw/buslic_active.csv
        data/tucson/raw/city_boundary_tiger.geojson
Output: data/tucson/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **Active licences that are not home occupations**, filtered at the
    server (config.REGISTER_WHERE) and asserted here.
  * **NAICS, the shared module**, unchanged: the layer carries a 6-digit
    `NAIC_CODE`. Non-store sellers (454), caterers, parking and the other
    shared carve-outs leave by code (pipeline/taxonomies/naics.py).
  * **One row per premises**: a business holds several licences at one
    address (a business licence, a tobacco licence, a liquor licence), so
    rows collapse on name and address.
  * **A person's business shows its address, not its name** (owner, call 15:
    Houston's rule): OWN_TYPE Sole Proprietorship, Individual or Married. So
    does a business whose account name is only a person's name, whatever its
    OWN_TYPE (config.PERSON_NAMED, read by eye; Kansas City's rule).
  * **At an apartment or a trailer, a business is a home**, and is left off
    (Sacramento's owner call, Houston's rule), read from the `APT` field.
  * **Placed by the layer's own point**, kept only inside the City of Tucson
    as TIGER draws it; a licence the City did not geocode is not placed.

Run:  python pipeline/tucson/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.name_keys import keys_of  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.naics import VALUE_COLUMN  # noqa: E402
from pipeline.tucson import config  # noqa: E402
from pipeline.tucson.step1_stations import city_polygon  # noqa: E402

FETCH = "pipeline/tucson/fetch_sources.py"

# A dwelling in the APT field: Houston's set. STE, UNIT and BOX are shop
# suites and mailboxes ("STE 101", "UNIT 260"), measured on a sample 2026-09-30.
HOME_UNIT = r"^(?:APT|APARTMENT|TRLR)\b"


def _s(col):
    return col.fillna("").astype(str).str.strip()


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}\nRun: python {FETCH}")
    df = pd.read_csv(config.REGISTER_CSV, dtype=str, keep_default_na=False)
    for c in df.columns:
        df[c] = _s(df[c])
    assert (df["LIC_STATUS"] == "Active").all() and (df["HOME_OCCUPATION"] == "F").all(), \
        "the download's filter did not hold"
    print(f"Loaded {len(df):,} active licences that are not home occupations")
    emit("register_rows", len(df))
    print(f"  licence types: {df['LIC_TYPE'].value_counts().head(8).to_dict()}")

    df[VALUE_COLUMN] = df[config.RAW_CLASSIFICATION_COLUMN]
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  storefront NAICS: {before:,} -> {len(df):,}")
    emit("storefront_rows", len(df))

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    no_point = df["latitude"].isna() | df["longitude"].isna()
    print(f"  not geocoded by the City (no point): {int(no_point.sum()):,} not placed; "
          f"by CITY {df.loc[no_point, 'CITY'].value_counts().head(4).to_dict()}")
    emit("no_point", int(no_point.sum()))
    df = df[~no_point].copy()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=df.index)
    inside = pts.within(city_polygon())
    print(f"  outside the City of Tucson: {int((~inside).sum()):,} (by CITY: "
          f"{df.loc[~inside, 'CITY'].value_counts().head(5).to_dict()})")
    emit("outside_city", int((~inside).sum()))
    df = df[inside].copy()

    home = df["APT"].str.upper().str.contains(HOME_UNIT, regex=True)
    print(f"  at an apartment or trailer (APT field): {int(home.sum()):,} left off as homes")
    emit("home_unit_dropped", int(home.sum()))
    df = df[~home]

    df["address"] = (df["ADDRESS"] + " " + df["APT"]).str.upper() \
        .str.replace(r"\s+", " ", regex=True).str.strip()
    no_name = df["ACC_NAME"] == ""
    print(f"  no account name: {int(no_name.sum()):,} (shown by address)")
    key = df["ACC_NAME"].str.upper().str.replace(r"[^A-Z0-9]", "", regex=True) + "|" \
        + df["address"]
    before = len(df)
    df = df.assign(_k=key).sort_values(["_k", "ACC_NUM"]).drop_duplicates("_k")
    print(f"  one row per premises (name + address): {before:,} -> {len(df):,}")

    # A PERSON'S BUSINESS SHOWS ITS ADDRESS (owner, call 15): by OWN_TYPE, and
    # by an account name that is only a person's (config.PERSON_NAMED).
    person_type = df["OWN_TYPE"].isin(config.PERSONAL_OWN_TYPES)
    name_keys = keys_of(df["ACC_NAME"])
    person_named = ~person_type & name_keys.isin(config.PERSON_NAMED)
    gone = set(config.PERSON_NAMED) - set(name_keys[person_named])
    if gone:
        sys.exit(f"PERSON_NAMED keys no longer matched: {sorted(gone)} - re-read the list "
                 f"against the register")
    df["name_is_address"] = person_type | person_named | no_name
    print(f"  personal ownership type: {int(person_type.sum()):,} "
          f"{df.loc[person_type, 'OWN_TYPE'].value_counts().to_dict()}; named only as a "
          f"person (config.PERSON_NAMED): {int(person_named.sum()):,}")
    df["business_name"] = df["ACC_NAME"].where(~df["name_is_address"], df["address"])
    still = ~df["name_is_address"] & df["business_name"].map(looks_personal)
    print(f"    -> {int(df['name_is_address'].sum()):,} show the address; shown names shaped "
          f"like a person's but read as shop names (check_personal_exposure reports "
          f"them): {int(still.sum()):,}")
    emit("name_as_address", int(df["name_is_address"].sum()))

    b = config.TUCSON_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    out = df.rename(columns={"ACC_NUM": "licence", "OWN_TYPE": "own_type",
                             "ZIP_CODE": "zip", "NAIC_DESC": "naics_desc"})[
        ["licence", "business_name", VALUE_COLUMN, "naics_desc", "address", "zip", "own_type",
         "name_is_address", "latitude", "longitude"]]
    out = out.sort_values("licence").reset_index(drop=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
