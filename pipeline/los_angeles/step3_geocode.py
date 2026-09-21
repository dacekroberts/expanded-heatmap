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
    BUSINESSES_PREFILTER_CSV,
    LOS_ANGELES_BBOX,
    PARCEL_RESIDENCE_CSV,
)
from pipeline.residence import flag_home_based, report  # noqa: E402


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

    # The unfiltered population, written before the filter below so
    # fetch_parcel_residence.py always has the full set to look up. See
    # config.BUSINESSES_PREFILTER_CSV for why this matters.
    BUSINESSES_PREFILTER_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_PREFILTER_CSV, index=False)

    # --- Home-based businesses, against the Assessor's own classification ----
    # Applied here rather than in step 2 because it needs FINAL coordinates:
    # 9% of this city's are recovered by the geocoder above.
    #
    # A scope filter first - a hairdresser or caterer working from the house
    # they own is not a storefront - which also removes this city's largest
    # personal-name exposure. Both conditions are required; see
    # pipeline/residence.py for why land use alone is not a signal.
    #
    # `all_residential` / `all_owner_occupied` describe the CONTAINING parcel
    # where the point sits in one, and only otherwise every parcel within the
    # buffer (the cache's `source` column says which). That distinction is the
    # whole ball game: answering the buffered question for points that do sit
    # inside a parcel made this filter under-remove tenfold, because one rented
    # neighbour cleared a genuine home.
    #
    # The lookup cache is built by fetch_parcel_residence.py, which is not a
    # step*.py so the drift check stays offline. With no cache this filter is
    # skipped and says so: the first run of a fresh checkout produces the
    # unfiltered file the fetch script then reads.
    if PARCEL_RESIDENCE_CSV.exists():
        before = len(out)
        parcels = pd.read_csv(PARCEL_RESIDENCE_CSV, dtype=str)
        m = out.merge(parcels, on="location_account", how="left")
        matched = pd.to_numeric(m["n_parcels"], errors="coerce").fillna(0) > 0
        looked_up = m["n_parcels"].notna()
        print(f"\nParcel lookups available for {int(looked_up.sum()):,} "
              f"person-like rows; {int(matched.sum()):,} matched a parcel "
              f"within the buffer "
              f"({100 * matched.sum() / max(int(looked_up.sum()), 1):.1f}%)")

        at_home = flag_home_based(
            m["business_name"],
            residential=m["all_residential"].eq("true"),
            owner_occupied=m["all_owner_occupied"].eq("true"),
        )
        report("person-like name + residential parcel + homeowner's exemption",
               at_home, before,
               extra={"NAICS": m["naics"], "use_types": m["use_types"]})
        out = out[~at_home.reindex(out.index, fill_value=False)]
        out = out.reset_index(drop=True)
    else:
        print(f"\nNOTE: no {PARCEL_RESIDENCE_CSV.name}, so the home-business "
              f"filter did NOT run. Build it with "
              f"pipeline/los_angeles/fetch_parcel_residence.py, then re-run "
              f"this step.")

    BUSINESSES_GEOCODED_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_GEOCODED_CSV, index=False)
    print(f"\nWrote {len(out):,} rows to {BUSINESSES_GEOCODED_CSV} "
          f"({(out['geocode_source'] == 'census').sum():,} from the Census geocoder)")


if __name__ == "__main__":
    main()
