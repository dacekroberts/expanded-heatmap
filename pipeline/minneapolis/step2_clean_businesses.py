"""Step 2 - Minneapolis's food premises from the City's food inspections.

Input:  data/minneapolis/raw/food_inspections.json        (ArcGIS, paged)
        data/minneapolis/raw/city_boundary_tiger.geojson  (the place polygon)
Output: data/minneapolis/processed/businesses_clean.csv
        outputs/minneapolis/excluded_premises.csv

What a reader should know before trusting the counts printed below:

  * **One row per violation, not per facility.** A facility is its
    HealthFacilityIDNumber; its name, category, address and point are taken
    from its latest inspection.
  * **No status and no closing date.** A facility counts when inspected
    within config.CURRENCY_YEARS before config.AS_OF_DATE (the fetch date).
  * **The category decides, then the name** (pipeline/taxonomies/
    minneapolis_inspection.py): contract caterers, hospital cafeterias,
    vending routes, hotels, venues and pharmacies inside the kept categories
    are left out by name, each listed in excluded_premises.csv. Facilities in
    categories that are not storefronts are counted, never named here: BOARD
    AND LODGING's names include people's own at homes.
  * **In-city is point-in-boundary** against TIGER's place polygon.

Run:  python pipeline/minneapolis/step2_clean_businesses.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.minneapolis import config  # noqa: E402

from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.minneapolis_inspection import (  # noqa: E402
    KNOWN_KINDS, NAME_KINDS, OUT_CATEGORIES, VALUE_TO_BUCKET, display_name, premises_kind)

OUT = ["source_key", "business_name", "facility_category", "premises_kind", "address",
       "zip_code", "last_inspected", "latitude", "longitude"]


def main():
    path = config.FOOD_INSPECTIONS_JSON
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/minneapolis/fetch_sources.py")
    raw = json.loads(path.read_text(encoding="utf-8"))
    df = pd.DataFrame(raw["features"])
    if len(df) != raw["count"]:
        sys.exit(f"{len(df):,} rows cached, the server counted {raw['count']:,}")
    if set(df.columns) != set(config.FOOD_FIELDS):
        sys.exit(f"columns {sorted(df.columns)} are not config.FOOD_FIELDS")
    df["d"] = pd.to_datetime(df["DateOfInspection"], unit="ms")
    as_of = pd.Timestamp(config.AS_OF_DATE)
    if df["d"].max() > as_of + pd.Timedelta(days=1):
        sys.exit(f"an inspection dated {df['d'].max()} after AS_OF_DATE {config.AS_OF_DATE}: "
                 "a re-fetched table needs the date moved with it")
    print(f"{len(df):,} violation rows, {df['HealthFacilityIDNumber'].nunique():,} facilities, "
          f"{df['d'].min().date()} to {df['d'].max().date()}")

    # --- One row per facility: its latest inspection ------------------------
    df = df.sort_values(["d", "InspectionIDNumber", "OBJECTID"])
    fac = df.groupby("HealthFacilityIDNumber").tail(1).copy()
    # The point from the latest row that HAS one: some inspections' rows carry
    # none (Cub Foods, Lunds & Byerlys), while earlier ones do.
    has_pt = df[df["Latitude"].fillna(0).ne(0) & df["Longitude"].fillna(0).ne(0)]
    pt = has_pt.groupby("HealthFacilityIDNumber")[["Latitude", "Longitude"]].last()
    fac = fac.drop(columns=["Latitude", "Longitude"]).join(pt, on="HealthFacilityIDNumber")
    cut = as_of - pd.DateOffset(years=config.CURRENCY_YEARS)
    recent = fac[fac["d"] >= cut].copy()
    print(f"Inspected since {cut.date()}: {len(recent):,} ({len(fac) - len(recent):,} older)")
    emit("facilities", len(fac))
    emit("inspected_recently", len(recent))

    recent["facility_category"] = (recent["FacilityCategory"].fillna("").str.strip().str.upper()
                                   .replace("", "UNCATEGORISED"))
    unknown = set(recent["facility_category"]) - set(VALUE_TO_BUCKET) - OUT_CATEGORIES
    if unknown:
        sys.exit(f"categories this taxonomy has not placed: {sorted(unknown)}")
    recent["business_name"] = recent["BusinessName"].map(display_name)
    recent["premises_kind"] = [premises_kind(c, n) for c, n in
                               zip(recent["facility_category"], recent["BusinessName"])]
    assert set(recent["premises_kind"]) <= KNOWN_KINDS
    print("\nBy category:")
    print(recent["facility_category"].value_counts().to_string())
    kept_cat = recent[recent["facility_category"].isin(VALUE_TO_BUCKET)].copy()
    print("\nLeft out by name, inside the kept categories:")
    print(pd.crosstab(kept_cat["premises_kind"], kept_cat["facility_category"])
          .loc[lambda t: t.index.isin(NAME_KINDS)].to_string())
    for kind, n in recent["premises_kind"].value_counts().items():
        emit(f"kind_{kind.lower().replace(' ', '_')}", int(n))

    # --- Placed, and in the City --------------------------------------------
    kept_cat["reason"] = kept_cat["premises_kind"].where(
        kept_cat["premises_kind"].isin(NAME_KINDS), "")
    nopoint = kept_cat["Latitude"].fillna(0).eq(0) | kept_cat["Longitude"].fillna(0).eq(0)
    kept_cat.loc[nopoint & (kept_cat["reason"] == ""), "reason"] = "No point in the table"
    placed = kept_cat[kept_cat["reason"] == ""]
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    pts = gpd.GeoSeries(gpd.points_from_xy(placed["Longitude"], placed["Latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=placed.index)
    outside = placed[~pts.within(city.geometry.union_all())]
    kept_cat.loc[outside.index, "reason"] = "Point outside the City"
    print(f"\nNo point: {int((kept_cat.reason == 'No point in the table').sum()):,}; "
          f"outside the City: {len(outside):,}")
    emit("no_point", int((kept_cat.reason == "No point in the table").sum()))
    emit("outside_city", len(outside))

    # --- One shop, one pin: a shop licensed twice in the same bucket ---------
    # A grocer holds a GROCERY and a MEAT MARKET licence for one counter
    # (HALAL HOUSE INC, 1001 FRANKLIN AVE E, twice). Same name (legal suffix
    # dropped), same street address (unit dropped), same bucket -> one pin,
    # GROCERY's first. Retail only: two RESTAURANT licences under one name and
    # street address are an operator's separate bars in one building, told
    # apart by unit. Different buckets stay apart too: a supermarket's deli is
    # licensed as a RESTAURANT and keeps its own id (Ottawa's precedent).
    live = kept_cat[kept_cat["reason"] == ""].copy()
    live["_bucket"] = live["facility_category"].map(VALUE_TO_BUCKET)
    live["_nm"] = (live["business_name"].str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True)
                   .str.replace(r"\b(LLC|INC|CO|CORP)\b", "", regex=True)
                   .str.replace(r"\s+", " ", regex=True).str.strip())
    live["_addr"] = live["FullAddress"].fillna("").str.upper().str.replace(r"\s*#.*$", "",
                                                                           regex=True)
    order = {"GROCERY": 0, "MARKET": 1, "LIQOFFSALE": 2, "MEAT MARKET": 3, "RESTAURANT": 0}
    live = live.sort_values(["_nm", "_addr", "facility_category"],
                            key=lambda s: s.map(order) if s.name == "facility_category" else s)
    twice = (live.duplicated(["_nm", "_addr", "_bucket"]) & live["_addr"].ne("")
             & live["_bucket"].eq("Retail"))
    kept_cat.loc[live.index[twice], "reason"] = "Second licence of the same shop"
    print(f"Second licences of one shop, same bucket: {int(twice.sum()):,}")
    emit("second_licence", int(twice.sum()))

    excluded = kept_cat[kept_cat["reason"] != ""]
    excluded[["HealthFacilityIDNumber", "business_name", "facility_category", "FullAddress",
              "reason"]].rename(columns={"HealthFacilityIDNumber": "source_key",
                                         "FullAddress": "address"}).sort_values(
        ["reason", "business_name", "source_key"]).to_csv(
        config.EXCLUDED_PREMISES_CSV, index=False, encoding="utf-8")
    print(f"{len(excluded):,} left out -> {config.EXCLUDED_PREMISES_CSV.relative_to(config.ROOT)}")

    out = kept_cat[kept_cat["reason"] == ""].copy()
    out = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    assert all(tax.classify({tax.VALUE_COLUMN: v}) for v in out[tax.VALUE_COLUMN])

    b = config.MINNEAPOLIS_BBOX
    assert out["Latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert out["Longitude"].between(b["lon_min"], b["lon_max"]).all()

    out = out.rename(columns={"HealthFacilityIDNumber": "source_key", "FullAddress": "address",
                              "ZipCode": "zip_code", "Latitude": "latitude",
                              "Longitude": "longitude"})
    out["last_inspected"] = out["d"].dt.strftime("%Y-%m-%d")
    by_bucket = out[tax.VALUE_COLUMN].map(lambda v: tax.classify({tax.VALUE_COLUMN: v})).value_counts()
    print("\nBy bucket:", by_bucket.to_dict())
    for bucket, n in by_bucket.items():
        emit(f"bucket_{bucket.lower().replace(' ', '_')}", int(n))
    emit("storefronts", len(out))
    out = out[OUT].sort_values("source_key").reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
