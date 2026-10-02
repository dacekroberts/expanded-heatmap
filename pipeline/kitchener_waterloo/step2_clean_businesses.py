"""Step 2 - Kitchener–Waterloo's food premises and personal services from the
Region of Waterloo Public Health's inspection registers.

Input:  data/kitchener_waterloo/raw/food_facilities.geojson      (layer 17)
        data/kitchener_waterloo/raw/personal_facilities.geojson  (layer 18)
        data/kitchener_waterloo/raw/Inspections.zip, Inspections_PS.zip
        data/kitchener_waterloo/raw/cities_and_towns.geojson     (the two cities)
Output: data/kitchener_waterloo/processed/businesses_clean.csv
        outputs/kitchener_waterloo/excluded_premises.csv

What a reader should know before trusting the counts printed below:

  * **The live layers are the premises and their points; the zips add the
    type and the inspections.** They join on the facility id. The layers
    are newer than the zips (dated config.AS_OF_DATE): a premises in the
    layer the zips do not hold opened since, has no type, and stays in its
    layer's default bucket (owner, 2026-09-30), counted below.
  * **The registers have no status and no closing date.** A premises the
    zips hold counts when Public Health inspected it within
    config.CURRENCY_YEARS before config.AS_OF_DATE (Ottawa's rule); the zips
    hold exactly those two years of inspections.
  * **What is left out** - institutional, mobile and processing categories,
    the types that are not storefronts, and what a name says a premises is -
    is pipeline/taxonomies/kitchener_waterloo_inspection.py, listed row by
    row in excluded_premises.csv.
  * **In-city is point-in-boundary** against the Region's polygons for
    Kitchener and Waterloo; `SiteCity` is free text with 82 spellings.
  * **SiteTelephone is never fetched.** A name that reads as a person's own
    shows its type instead (Vancouver's and Sacramento's rule,
    pipeline.residence.looks_personal); check_personal_exposure.py measures
    what remains.

Run:  python pipeline/kitchener_waterloo/step2_clean_businesses.py
"""
import io
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.kitchener_waterloo import config  # noqa: E402
from pipeline.name_keys import keys_of  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402

from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.kitchener_waterloo_inspection import (  # noqa: E402
    KNOWN_KINDS, PERSONAL, VALUE_TO_BUCKET, premises_kind)

BEAUTY_TRADE = (r"BARBER|AESTHETIC|ESTHETI|\bINK\b|TATTOO|\bCUTS?\b|CUTZ|CLIPS|NAILZ|LASH|BROW|"
                r"STYLIST|STYLE|HAIRWORKS|UNISEX|ELECTROLYSIS|SEPHORA|SPATHECARY|SUGAR")

OUT =["source_key", "business_name", "premises_kind", "premises_type", "address",
       "last_inspected", "latitude", "longitude"]


def read_zip(path, members):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/kitchener_waterloo/fetch_sources.py")
    with zipfile.ZipFile(path) as z:
        fac, ins = (pd.read_csv(io.BytesIO(z.read(m)), dtype=str, keep_default_na=False,
                                encoding=config.ZIP_ENCODING) for m in members)
        stamp = "%04d-%02d-%02d" % z.getinfo(members[0]).date_time[:3]
    return fac, ins, stamp


def read_register(label, layer_path, zip_path, members):
    if not layer_path.exists():
        sys.exit(f"missing {layer_path}\nRun: python pipeline/kitchener_waterloo/fetch_sources.py")
    g = gpd.read_file(layer_path)
    assert "SiteTelephone" not in g.columns
    fac, ins, stamp = read_zip(zip_path, members)
    if stamp != config.AS_OF_DATE:
        sys.exit(f"{zip_path.name} is dated {stamp}, config.AS_OF_DATE {config.AS_OF_DATE}: "
                 "a re-fetched zip needs the date moved with it")
    if not g["FacilityMasterID"].is_unique or not fac["FACILITYID"].is_unique:
        sys.exit(f"{label}: a facility id is not unique")
    ins["d"] = pd.to_datetime(ins["INSPECTION_DATE"], format="%Y/%m/%d", errors="raise")
    g["premises_type"] = g["FacilityMasterID"].map(fac.set_index("FACILITYID")["SUBCATEGORY"])
    g["in_zip"] = g["FacilityMasterID"].isin(fac["FACILITYID"])
    g["last_inspected"] = g["FacilityMasterID"].map(ins.groupby("FACILITYID")["d"].max())
    print(f"{label}: {len(g):,} in the layer, {len(fac):,} in the zip, "
          f"{int(g['in_zip'].sum()):,} joined; inspections {ins['d'].min().date()} to "
          f"{ins['d'].max().date()}")
    return g


def main():
    food = read_register("Food", config.FOOD_LAYER_GEOJSON, config.FOOD_ZIP,
                         config.FOOD_ZIP_MEMBERS)
    personal = read_register("Personal services", config.PERSONAL_LAYER_GEOJSON,
                             config.PERSONAL_ZIP, config.PERSONAL_ZIP_MEMBERS)
    df = pd.concat([food, personal], ignore_index=True)
    df = gpd.GeoDataFrame(df, geometry="geometry", crs=food.crs).to_crs(config.CRS_GEOGRAPHIC)

    # --- In the two cities: point-in-boundary ------------------------------
    cities = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    inside = df.within(cities.geometry.union_all())
    print(f"\nIn Kitchener or Waterloo: {int(inside.sum()):,} of {len(df):,}")
    emit("in_city", int(inside.sum()))
    df = df[inside].copy()
    print(df["Category"].value_counts().to_string())

    # --- The premises kind: category, type, then name ------------------------
    df["premises_kind"] = [premises_kind(c, s, n) for c, s, n in
                           zip(df["Category"], df["premises_type"], df["FacilityName"])]
    assert set(df["premises_kind"]) <= KNOWN_KINDS, set(df["premises_kind"]) - KNOWN_KINDS
    kept = df["premises_kind"].isin(VALUE_TO_BUCKET)
    no_type = kept & ~df["in_zip"]
    print(f"\nKept types with no zip row (opened since {config.AS_OF_DATE}, kept by "
          f"default): {int(no_type.sum()):,}")
    print(df[no_type]["Category"].value_counts().to_string())
    emit("kept_without_type", int(no_type.sum()))

    # --- Currency: inspected within two years --------------------------------
    cut = pd.Timestamp(config.AS_OF_DATE) - pd.DateOffset(years=config.CURRENCY_YEARS)
    stale = kept & df["in_zip"] & ~(df["last_inspected"] >= cut)
    df["reason"] = df["premises_kind"].where(~kept, "")
    df.loc[stale, "reason"] = f"Not inspected since {cut.date()}"
    print(f"Kept kinds not inspected since {cut.date()}: {int(stale.sum()):,}")
    emit("not_inspected_recently", int(stale.sum()))

    print("\nBy reason:")
    print(df["reason"].replace("", "(kept)").value_counts().to_string())
    for reason, n in df["reason"].replace("", "kept").value_counts().items():
        emit("reason_" + "".join(ch if ch.isalnum() else "_" for ch in reason.lower()), int(n))

    df["address"] = df["SiteStreet"].fillna("").str.strip()
    excluded = df[df["reason"] != ""]
    excluded[["FacilityMasterID", "FacilityName", "premises_type", "address", "reason"]].rename(
        columns={"FacilityMasterID": "source_key", "FacilityName": "business_name"}).sort_values(
        ["reason", "business_name"]).to_csv(config.EXCLUDED_PREMISES_CSV, index=False,
                                            encoding="utf-8")
    print(f"{len(excluded):,} left out -> "
          f"{config.EXCLUDED_PREMISES_CSV.relative_to(config.ROOT)}")

    df = df[df["reason"] == ""].copy()
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    assert all(tax.classify({tax.VALUE_COLUMN: v}) for v in df[tax.VALUE_COLUMN])

    # --- The displayed name: the register's own, unless it reads as a person's
    # Personal services only - the layer that holds home-based operators
    # (Vancouver's and Sacramento's "type in place of a personal name"). NOT
    # the food layer: measured here the shared test flags 386 kept food names,
    # and a read of them found trade names throughout (TIM HORTONS, DAIRY
    # QUEEN, THAI EXPRESS) - Ottawa's finding on the same kind of register.
    # A beauty-trade word also rules a name out as a person's: the shared
    # test's own organisation list lacks them (GREAT CLIPS, RAMI BARBERSHOP).
    df["business_name"] = df["FacilityName"].str.strip()
    ps = df["premises_kind"] == PERSONAL
    person = ps & ((df["business_name"].map(looks_personal) & ~df["business_name"].str.upper(
        ).str.contains(BEAUTY_TRADE)) | keys_of(df["business_name"]).isin(config.PERSON_NAMES))
    df.loc[person, "business_name"] = df.loc[person, "premises_type"].where(
        df.loc[person, "premises_type"].fillna("") != "", "Personal services")
    print(f"\nPersonal-services names that read as a person's: {int(person.sum()):,} show "
          "the type instead")
    emit("name_as_type", int(person.sum()))

    df["latitude"], df["longitude"] = df.geometry.y, df.geometry.x
    b = config.KITCHENER_WATERLOO_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    df["source_key"] = df["FacilityMasterID"]
    df["premises_type"] = df["premises_type"].fillna("")
    df["last_inspected"] = df["last_inspected"].dt.strftime("%Y-%m-%d").fillna("")
    print("\nBy bucket:")
    print(df["premises_kind"].map(VALUE_TO_BUCKET).value_counts().to_string())
    for kind, n in df["premises_kind"].value_counts().items():
        emit("kind_" + "".join(ch if ch.isalnum() else "_" for ch in kind.lower()), int(n))
    emit("storefronts", len(df))
    out = pd.DataFrame(df[OUT]).sort_values("source_key").reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
