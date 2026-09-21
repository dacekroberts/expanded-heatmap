"""Step 3 - Recover New York businesses whose source coordinates were missing
or corrupt, by geocoding their street addresses with the Census geocoder.

Input:  data/new_york/processed/businesses_clean.csv
Output: data/new_york/processed/businesses_geocoded.csv

Step 2 flagged two kinds of row as coord_status='missing':

  * no coordinates at all in the source - almost all DCA premises licences
    (4,910 of 35,245 before filtering), plus a few hundred across the other
    three registries;
  * coordinates that were not valid New York points at all - 429 rows, 409 of
    them at exactly (0,0). These are real New York businesses (HASAKI on East
    9th Street, White Castle) with broken coordinates.

Rows located elsewhere in New York State were already dropped in step 2 as out
of scope, so nothing here is an upstate business.

Census results are accepted only inside the city's bounds AND inside the
borough polygons - a "match" in the wrong place is worse than no match. Every
output row records where its coordinates came from (geocode_source =
source | census). Recovery is expected to be partial: some corrupt rows also
carry mangled addresses ("975979 FIRST AVENUE") or none at all ("4 - JFK
AIRPORT"), and the residual is reported by source and bucket so any bias is
visible rather than assumed away.

Run:  python pipeline/new_york/step3_geocode.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.census_geocoder import geocode_addresses  # noqa: E402
from pipeline.new_york.config import (  # noqa: E402
    BOROUGH_TO_POSTAL_CITY,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_GEOCODED_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    GEOCODE_CACHE_DIR,
    GEOCODE_DEFAULT_CITY,
    GEOCODE_STATE,
    NEW_YORK_BBOX,
    SOURCES,
)
from pipeline.taxonomies import load_taxonomy_module  # noqa: E402
from pipeline.new_york.config import TAXONOMY_SYSTEM  # noqa: E402


def main():
    if not BUSINESSES_CLEAN_CSV.exists():
        sys.exit(f"Missing {BUSINESSES_CLEAN_CSV}. Run step2_clean_businesses.py first.")

    df = pd.read_csv(
        BUSINESSES_CLEAN_CSV,
        dtype={"source_key": str, "zip": str, "record_id": str, "business_category": str},
    )
    df["geocode_source"] = df["coord_status"].map({"source": "source"})
    todo = df[df["coord_status"] == "missing"]
    print(f"{len(df):,} in-city storefront rows: {len(df) - len(todo):,} with usable "
          f"source coordinates, {len(todo):,} to geocode by address")
    print("\nTo geocode, by source:")
    print(todo["source"].value_counts().to_string())

    # An address is required; a row without one cannot be recovered at all.
    geocodable = todo[todo["address"].fillna("").str.strip() != ""]
    print(f"\n{len(todo) - len(geocodable):,} of those have no street address and "
          "cannot be recovered")

    postal_city = (
        df["borough"].fillna("").str.strip().str.upper()
        .map(BOROUGH_TO_POSTAL_CITY).fillna(GEOCODE_DEFAULT_CITY)
    )
    matched = geocode_addresses(
        geocodable, id_col="record_id", street_col="address", zip_col="zip",
        city=postal_city, state=GEOCODE_STATE, cache_dir=GEOCODE_CACHE_DIR,
    )
    print(f"\nCensus matched {len(matched):,} of {len(geocodable):,} "
          f"({len(matched) / max(len(geocodable), 1):.1%}); "
          f"match types: {matched['match_type'].value_counts().to_dict()}")

    # Accept only points inside the city's bounds.
    b = NEW_YORK_BBOX
    in_bounds = (matched["latitude"].between(b["lat_min"], b["lat_max"])
                 & matched["longitude"].between(b["lon_min"], b["lon_max"]))
    print(f"{int(in_bounds.sum()):,} matches fall inside the city's bounds; "
          f"{int((~in_bounds).sum()):,} rejected as out of bounds")
    matched = matched[in_bounds].drop_duplicates("id").set_index("id")

    recovered = df["record_id"].isin(matched.index) & (df["coord_status"] == "missing")
    df.loc[recovered, "latitude"] = df.loc[recovered, "record_id"].map(matched["latitude"])
    df.loc[recovered, "longitude"] = df.loc[recovered, "record_id"].map(matched["longitude"])
    df.loc[recovered, "geocode_source"] = "census"

    # Independent check: are the recovered points inside the borough polygons?
    # A point that is not is dropped, not kept on the bbox's word - the bbox is
    # a rectangle and includes water and New Jersey.
    if CITY_BOUNDARY_GEOJSON.exists() and recovered.any():
        boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
        boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                    else boundary.to_crs(CRS_GEOGRAPHIC))
        city = boundary.geometry.union_all()
        rec = df[recovered]
        pts = gpd.GeoSeries(
            gpd.points_from_xy(rec["longitude"], rec["latitude"]),
            crs=CRS_GEOGRAPHIC, index=rec.index)
        inside = pts.within(city)
        print(f"Cross-check: {int(inside.sum()):,} of {len(rec):,} recovered points "
              f"({inside.mean():.1%}) fall inside the five borough polygons")
        outside = rec.index[~inside.values]
        if len(outside):
            print(f"  dropping {len(outside):,} recovered points outside the boroughs")
            df.loc[outside, "geocode_source"] = pd.NA

    unresolved = df["geocode_source"].isna()
    print(f"\nUnrecovered (dropped): {int(unresolved.sum()):,} of {len(df):,} "
          f"({unresolved.mean():.1%})")
    if unresolved.any():
        print("  by source:")
        for source in SOURCES:
            n = int((unresolved & (df["source"] == source)).sum())
            total = int((df["source"] == source).sum())
            if total:
                print(f"    {source}: {n:,} of {total:,} ({n / total:.1%})")
        taxonomy = load_taxonomy_module(TAXONOMY_SYSTEM)
        lost = df[unresolved]
        buckets = [taxonomy.classify({"business_category": c, "source": s})
                   for c, s in zip(lost["business_category"], lost["source"])]
        print("  by bucket:")
        print("    " + pd.Series(buckets).value_counts().to_string().replace("\n", "\n    "))

    out = df[~unresolved].reset_index(drop=True)
    BUSINESSES_GEOCODED_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_GEOCODED_CSV, index=False)
    print(f"\nWrote {len(out):,} rows to {BUSINESSES_GEOCODED_CSV} "
          f"({int((out['geocode_source'] == 'census').sum()):,} from the Census geocoder)")


if __name__ == "__main__":
    main()
