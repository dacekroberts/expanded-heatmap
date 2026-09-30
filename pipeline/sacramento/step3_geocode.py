"""Step 3 - Place Sacramento's storefronts with the US Census Bureau's batch
geocoder (owner, 2026-09-29), Los Angeles' and D.C.'s shared module.

Input:  data/sacramento/processed/businesses_clean.csv
Output: data/sacramento/processed/businesses_geocoded.csv

Batches are cached under data/sacramento/raw/geocode_cache/ by content hash,
so a re-run and a drift check stay offline (a drift check refuses an uncached
batch: pipeline/offline.py). Only the street, city, state and ZIP are sent -
never a name. Unmatched rows are counted and dropped; matched points outside
the city's sanity box are dropped too.

Run:  python pipeline/sacramento/step3_geocode.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.census_geocoder import geocode_addresses  # noqa: E402
from pipeline.sacramento import config  # noqa: E402
from pipeline.taxonomies import load_taxonomy_module  # noqa: E402


def main():
    if not config.BUSINESSES_CLEAN_CSV.exists():
        sys.exit("Run step2_clean_businesses.py first.")
    df = pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype=str, keep_default_na=False)
    print(f"Geocoding {len(df):,} storefront addresses (street, city, state, ZIP only)")
    matched = geocode_addresses(df, id_col="account", street_col="street", zip_col="zip",
                                city="Sacramento", state="CA", cache_dir=config.GEOCODE_CACHE_DIR)
    print(f"  matched {len(matched):,} of {len(df):,} ({len(matched) / len(df):.1%}); "
          f"match types {matched['match_type'].value_counts().to_dict()}")
    out = df.merge(matched[["id", "latitude", "longitude"]].rename(columns={"id": "account"}),
                   on="account", how="inner")
    b = config.SACRAMENTO_BBOX
    ok = (out["latitude"].between(b["lat_min"], b["lat_max"])
          & out["longitude"].between(b["lon_min"], b["lon_max"]))
    if (~ok).any():
        print(f"  {int((~ok).sum()):,} matched outside the city's box, dropped")
    out = out[ok]

    # POINT-IN-BOUNDARY: Location_City is the POSTAL city, and a "Sacramento"
    # postal address also covers unincorporated county (Los Angeles' lesson:
    # a city field may not mean in the city). The City's OSM polygon decides.
    import geopandas as gpd
    from pipeline.sacramento.step1_stations import boundaries
    b = boundaries()
    city = b[b["id"] == config.OSM_CITY_RELATION].geometry.iloc[0]
    pts = gpd.GeoSeries(gpd.points_from_xy(out["longitude"], out["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=out.index)
    inside = pts.within(city)
    print(f"  inside the City of Sacramento: {int(inside.sum()):,} of {len(out):,} "
          f"({int((~inside).sum()):,} with a Sacramento postal address outside the city, dropped)")
    emit("outside_city_postal", int((~inside).sum()))
    out = out[inside]

    TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    lost = df[~df["account"].isin(out["account"])]
    lb = lost["business_category"].map(lambda c: TAX.classify({"business_category": c}))
    print(f"  not placed or outside the city, by bucket: {lb.value_counts().to_dict()}")
    emit("geocoded", len(out))
    out.to_csv(config.BUSINESSES_GEOCODED_CSV, index=False, encoding="utf-8")
    print(f"\n{len(out):,} placed -> {config.BUSINESSES_GEOCODED_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
