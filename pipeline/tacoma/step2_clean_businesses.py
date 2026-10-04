"""Step 2 - Tacoma's storefronts from the City's business-license point layer.

Input:  data/tacoma/raw/business_licenses.csv
        data/tacoma/raw/city_boundary_tiger.geojson
Output: data/tacoma/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **Active Tax & License accounts, not licenses.** The layer lists every
    business with an active account and drops closed ones; in the
    publisher's words it "does not indicate whether a business has a
    business license for the current year". No status or expiry field.
  * **In the city by the register's own council district** (1-5), checked
    against the Census Bureau's place polygon. "Not Mapped" rows and rows
    with no district are outside the city (the brief).
  * **NAICS 2022, through the shared naics.py, unchanged.**
  * **A person's name never labels a pin** (Vancouver's rule of 2026-09-21,
    the brief): where the trade name is only the entity's own name, the
    entity carries no legal form, and the name reads as a person's, the pin
    shows its NAICS description instead. A trade name an owner chose is shown
    as chosen.
  * **At an apartment or a trailer, a business is a home**, and is left off
    (Sacramento's owner call, Houston's and Kansas City's rule), read from
    the site's own unit field. The mailing address is never fetched.
  * **One row per premises** on the shown name and the site address.

Run:  python pipeline/tacoma/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.kansas_city.step2_clean_businesses import LEGAL_FORM, holder_is_person  # noqa: E402
from pipeline.residence import looks_organisational, looks_personal  # noqa: E402
from pipeline.tacoma import config  # noqa: E402
from pipeline.tacoma.step1_stations import city_polygon  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.naics import VALUE_COLUMN  # noqa: E402

FETCH = "pipeline/tacoma/fetch_sources.py"
LF = chr(10)

# A dwelling in the site's own unit field: Kansas City's set (APT is
# Sacramento's owner call, TRLR pipeline/residence.py's), with residence.py's
# SPC/SPACE, a mobile-home space (3 storefronts, 2026-10-04). UNIT and BSMT
# stay: a shop's unit as often as a home's.
HOME_UNIT = r"(?:^|\s|#)(?:APT|APARTMENT|TRLR|SPC|SPACE)\b"


def norm(s):
    return s.fillna("").str.strip().str.upper().str.replace(r"\s+", " ", regex=True)


def reads_as_person(name):
    """residence.py's shape test or Kansas City's surname-first one, less any
    organisation word. Meant to over-fire: a false "person" only shows a
    business's category in place of its name."""
    return (looks_personal(name) or holder_is_person(name)) and not looks_organisational(name)


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}\nRun: python {FETCH}")
    df = pd.read_csv(config.REGISTER_CSV, dtype=str, keep_default_na=False)
    print(f"Loaded {len(df):,} active Tax & License accounts")
    emit("register_rows", len(df))

    df = df[df["council_district"].isin(config.IN_CITY_DISTRICTS)].copy()
    print(f"  in a council district (1-5), the register's in-city marker: {len(df):,}")
    emit("in_city_rows", len(df))

    df[VALUE_COLUMN] = df[config.RAW_CLASSIFICATION_COLUMN].str.strip()
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
    print(f"  in a district but outside the TIGER polygon: {int((~inside).sum()):,}, dropped")
    emit("outside_city", int((~inside).sum()))
    df = df[inside].copy()

    unit = norm(df["site_unit_number"])
    home = unit.str.contains(HOME_UNIT, regex=True)
    print(f"  at an apartment or trailer unit: {int(home.sum()):,} left off as homes")
    emit("home_unit_dropped", int(home.sum()))
    df = df[~home].copy()

    trade, entity = norm(df["trade_name"]), norm(df["business_name"])
    df["_shown"] = trade.where(trade != "", entity)
    street = norm(df["site_street"])
    key = (df["_shown"].str.replace(r"[^A-Z0-9]", "", regex=True) + "|" + street + "|"
           + norm(df["site_unit_number"]))
    before = len(df)
    df = df.assign(_k=key).sort_values(["_k", "license_number"]).drop_duplicates("_k")
    print(f"  one row per premises (name + site address): {before:,} -> {len(df):,}")

    # THE NAME RULE (Vancouver's, 2026-09-21): only where the register gives
    # no trade name of its own (the trade name is the entity's name), the
    # entity has no legal form, and the name reads as a person's.
    trade, entity = norm(df["trade_name"]), norm(df["business_name"])
    own = (trade == entity) | (trade == "")
    no_form = ~entity.map(lambda n: bool(LEGAL_FORM.search(n)))
    person = df["_shown"].map(reads_as_person)
    df["name_is_category"] = own & no_form & person
    print(f"  the trade name is the entity's own name: {int(own.sum()):,}; with no legal "
          f"form: {int((own & no_form).sum()):,}; reading as a person's: "
          f"{int(df['name_is_category'].sum()):,} -> the NAICS description shown")
    emit("name_as_category", int(df["name_is_category"].sum()))
    desc = df["naics_code_description"].str.strip()
    df["business_name"] = df["_shown"].where(~df["name_is_category"], desc)
    still = ~df["name_is_category"] & df["_shown"].map(reads_as_person)
    print(f"    trade names an owner chose that are shaped like a person's, shown as "
          f"chosen (check_personal_exposure reports them): {int(still.sum()):,}")

    b = config.TACOMA_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    df["address"] = street + df["site_unit_number"].fillna("").str.strip().map(
        lambda u: f" {u.upper()}" if u else "")
    out = df.rename(columns={"license_number": "licence", "site_zip_code": "zip"})[
        ["licence", "business_name", VALUE_COLUMN, "naics_code_description", "address", "zip",
         "council_district", "name_is_category", "latitude", "longitude"]]
    out = out.sort_values("licence").reset_index(drop=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator=LF)
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
