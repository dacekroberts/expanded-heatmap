"""Step 2 - Pittsburgh's food premises from Allegheny County's food facilities.

Input:  data/pittsburgh/raw/geocoded_food_facilities.csv   (WPRDC, CC0)
        data/pittsburgh/raw/city_boundary_tiger.geojson    (the place polygon)
Output: data/pittsburgh/processed/businesses_clean.csv
        outputs/pittsburgh/excluded_premises.csv

What a reader should know before trusting the counts printed below:

  * **One row per facility, county-wide, as of 2025-08-27** (the resource's
    last modification; config.REGISTER_DATE). Active is the County's own
    `status` 1 with no closing date; 7 is out of business.
  * **In the city** is the County's `municipal` (Pittsburgh-NNN, the city's
    wards) AND a point inside TIGER's polygon.
  * **The category decides, then the name** (pipeline/taxonomies/
    pittsburgh_inspection.py): stadium and arena stands, casino outlets,
    workplace micro-markets, hospital and campus outlets, hotels' back of
    house, pharmacies and dark stores inside the kept categories are left
    out by name, each listed in excluded_premises.csv. Facilities in other
    categories are counted by the register's own description, never named
    here.

Run:  python pipeline/pittsburgh/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.pittsburgh import config  # noqa: E402

from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.pittsburgh_inspection import (  # noqa: E402
    KNOWN_KINDS, NAME_KINDS, OTHER, VALUE_TO_BUCKET, premises_kind)

OUT = ["source_key", "business_name", "category_cd", "description", "premises_kind",
       "address", "zip", "latitude", "longitude"]


def main():
    path = config.FACILITIES_CSV
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/pittsburgh/fetch_sources.py")
    df = pd.read_csv(path, dtype=str, keep_default_na=False, usecols=config.FACILITY_COLUMNS)
    if not df["id"].is_unique:
        sys.exit("facility id is not unique")
    print(f"{len(df):,} facilities county-wide")

    city_rows = df[df["municipal"].str.startswith(config.CITY_KEEP)].copy()
    active = city_rows[(city_rows["status"] == "1") & (city_rows["bus_cl_date"] == "")].copy()
    print(f"In Pittsburgh's wards: {len(city_rows):,}; active (status 1, no closing date): "
          f"{len(active):,}")
    print("  status in the wards:", city_rows["status"].value_counts().to_dict())
    emit("in_wards", len(city_rows))
    emit("active", len(active))

    active["premises_kind"] = [premises_kind(c, n) for c, n in
                               zip(active["category_cd"], active["facility_name"])]
    assert set(active["premises_kind"]) <= KNOWN_KINDS
    other = active[active["premises_kind"] == OTHER]
    print(f"\nOther categories, left out by type: {len(other):,}")
    print(other.groupby(["category_cd", "description"]).size().sort_values(ascending=False)
          .to_string())
    emit("other_category", len(other))

    kept = active[active["premises_kind"] != OTHER].copy()
    kept["business_name"] = kept["facility_name"].str.strip()
    kept["address"] = (kept["num"].str.strip() + " " + kept["street"].str.strip()).str.strip()
    print("\nLeft out by name, inside the kept categories:")
    print(pd.crosstab(kept["premises_kind"], kept["category_cd"].isin({"201", "202", "211", "212"})
                      .map({True: "food", False: "shop"})).to_string())
    for kind, n in kept["premises_kind"].value_counts().items():
        emit(f"kind_{kind.lower().replace(' ', '_').replace(',', '')}", int(n))

    kept["reason"] = kept["premises_kind"].where(kept["premises_kind"].isin(NAME_KINDS), "")
    kept["latitude"] = pd.to_numeric(kept["y"], errors="coerce")
    kept["longitude"] = pd.to_numeric(kept["x"], errors="coerce")
    nopoint = kept["latitude"].isna() | kept["longitude"].isna()
    kept.loc[nopoint & (kept["reason"] == ""), "reason"] = "No point in the register"
    placed = kept[kept["reason"] == ""]
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    pts = gpd.GeoSeries(gpd.points_from_xy(placed["longitude"], placed["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=placed.index)
    outside = placed[~pts.within(city.geometry.union_all())]
    kept.loc[outside.index, "reason"] = "Point outside the City"
    n_nopoint = int((kept["reason"] == "No point in the register").sum())
    print(f"\nNo point: {n_nopoint:,}; point outside the City: {len(outside):,}")
    emit("no_point", n_nopoint)
    emit("outside_city", len(outside))

    excluded = kept[kept["reason"] != ""]
    excluded[["id", "business_name", "description", "address", "reason"]].rename(
        columns={"id": "source_key"}).sort_values(["reason", "business_name", "source_key"]).to_csv(
        config.EXCLUDED_PREMISES_CSV, index=False, encoding="utf-8")
    print(f"{len(excluded):,} left out -> {config.EXCLUDED_PREMISES_CSV.relative_to(config.ROOT)}")

    out = kept[kept["reason"] == ""].copy()
    out = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    assert all(tax.classify({tax.VALUE_COLUMN: v}) for v in out[tax.VALUE_COLUMN])

    b = config.PITTSBURGH_BBOX
    assert out["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert out["longitude"].between(b["lon_min"], b["lon_max"]).all()

    dup = out.duplicated(["business_name", "address", tax.VALUE_COLUMN], keep=False)
    print(f"Facilities sharing a name, address and bucket with another id: {int(dup.sum()):,} "
          "(kept: the County gives each its own id)")
    out["source_key"] = out["id"]
    by_bucket = out[tax.VALUE_COLUMN].map(lambda v: VALUE_TO_BUCKET[v]).value_counts()
    print("\nBy bucket:", by_bucket.to_dict())
    for bucket, n in by_bucket.items():
        emit(f"bucket_{bucket.lower().replace(' ', '_')}", int(n))
    emit("storefronts", len(out))
    out = out[OUT].sort_values("source_key").reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
