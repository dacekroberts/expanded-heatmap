"""Step 3 - Recover Los Angeles businesses whose source coordinates were
unusable, by geocoding their street addresses with the Census geocoder.

Input:  data/los_angeles/processed/businesses_clean.csv
Output: data/los_angeles/processed/businesses_geocoded.csv

Step 2 flagged ~9% of storefront rows (coord_status = needs_geocode): corrupt
source coordinates, heavily skewed to businesses that started in 2020 or
later. This step geocodes those by address. Census results are accepted only
inside the city's coordinate bounds; anything unmatched or out of bounds is
dropped and counted. Every output row records where its coordinates came
from (geocode_source = source | census), so the recovered points can always
be told apart.

Run:  python pipeline/los_angeles/step3_geocode.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.census_geocoder import geocode_addresses  # noqa: E402
from pipeline.los_angeles.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_GEOCODED_CSV,
    CITIES_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_FIELD,
    CITY_BOUNDARY_NAME,
    CRS_GEOGRAPHIC,
    GEOCODE_CACHE_DIR,
    LOS_ANGELES_BBOX,
)


def main():
    if not BUSINESSES_CLEAN_CSV.exists():
        sys.exit(f"Missing {BUSINESSES_CLEAN_CSV}. Run step2_clean_businesses.py first.")

    df = pd.read_csv(BUSINESSES_CLEAN_CSV, dtype={"naics": str, "zip_code": str, "record_id": str})
    df["geocode_source"] = df["coord_status"].map({"source": "source"})
    todo = df[df["coord_status"] == "needs_geocode"]
    print(f"{len(df):,} in-city storefront rows: {len(df) - len(todo):,} with usable source "
          f"coordinates, {len(todo):,} to geocode by address\n")

    matched = geocode_addresses(
        todo, id_col="location_account", street_col="street_address", zip_col="zip_code",
        city="Los Angeles", state="CA", cache_dir=GEOCODE_CACHE_DIR,
    )
    print(f"\nCensus matched {len(matched):,} of {len(todo):,} ({len(matched) / max(len(todo), 1):.1%}); "
          f"match types: {matched['match_type'].value_counts().to_dict()}")

    # Accept only points inside the city's bounds - a "match" in the wrong
    # place is worse than no match.
    b = LOS_ANGELES_BBOX
    in_bounds = matched["latitude"].between(b["lat_min"], b["lat_max"]) & \
        matched["longitude"].between(b["lon_min"], b["lon_max"])
    print(f"{int(in_bounds.sum()):,} matches fall inside the city's bounds; "
          f"{int((~in_bounds).sum()):,} rejected as out of bounds")
    matched = matched[in_bounds].drop_duplicates("id").set_index("id")

    recovered = df["location_account"].isin(matched.index) & (df["coord_status"] == "needs_geocode")
    df.loc[recovered, "latitude"] = df.loc[recovered, "location_account"].map(matched["latitude"])
    df.loc[recovered, "longitude"] = df.loc[recovered, "location_account"].map(matched["longitude"])
    df.loc[recovered, "geocode_source"] = "census"

    # Independent check on the recovered points: are they inside the polygon?
    if CITIES_BOUNDARY_GEOJSON.exists() and recovered.any():
        cities = gpd.read_file(CITIES_BOUNDARY_GEOJSON)
        cities = cities.set_crs(CRS_GEOGRAPHIC) if cities.crs is None else cities.to_crs(CRS_GEOGRAPHIC)
        la = cities[cities[CITY_BOUNDARY_FIELD] == CITY_BOUNDARY_NAME]
        rec = df[recovered]
        pts = gpd.GeoDataFrame(
            rec[["location_account"]],
            geometry=gpd.points_from_xy(rec["longitude"], rec["latitude"]), crs=CRS_GEOGRAPHIC,
        )
        inside = gpd.sjoin(pts, la[["geometry"]], predicate="within", how="left")["index_right"].notna()
        print(f"Cross-check: {int(inside.sum()):,} of {len(rec):,} recovered points "
              f"({inside.mean():.1%}) fall inside the City of Los Angeles polygon.")

    unresolved = df["geocode_source"].isna()
    start_year = pd.to_datetime(df["location_start_date"], errors="coerce").dt.year
    recent = start_year >= 2020
    print(f"\nUnrecovered (dropped): {int(unresolved.sum()):,} of {len(df):,} "
          f"({unresolved.mean():.1%}); among businesses started 2020+: "
          f"{int((unresolved & recent).sum()):,} of {int(recent.sum()):,} "
          f"({(unresolved & recent).sum() / max(recent.sum(), 1):.1%}) - the residual bias.")

    out = df[~unresolved].reset_index(drop=True)
    BUSINESSES_GEOCODED_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_GEOCODED_CSV, index=False)
    print(f"\nWrote {len(out):,} rows to {BUSINESSES_GEOCODED_CSV} "
          f"({(out['geocode_source'] == 'census').sum():,} from the Census geocoder)")


if __name__ == "__main__":
    main()
