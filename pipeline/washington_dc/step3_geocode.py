"""Step 3 - Recover the D.C. premises whose register row carries no
coordinates, by geocoding their street addresses with the Census geocoder.

Input:  data/washington_dc/processed/businesses_clean.csv
Output: data/washington_dc/processed/businesses_geocoded.csv

Step 2 flagged 451 of 5,294 premises (8.5%) as `needs_geocode`. Unlike Los
Angeles, where the flagged rows had CORRUPT coordinates - longitude copied from
latitude, (0,0), whole-degree placeholders, and a bias towards businesses
registered since 2020 - D.C.'s flagged rows have no coordinates at all. They
are the rows the District's own geocoder failed on, which is also why they
carry neither a MAR_ID nor a WARD.

Step 0 expected MAR_ID to recover them. It cannot: they are the same rows.
What they do have is a street address, all 451 of them, so the recovery path is
the Census geocoder - already built, US-only, and cached by content hash so
re-runs and drift checks stay deterministic.

Census results are accepted only inside the District's bounds; anything
unmatched or out of bounds is dropped and counted. Every output row records
where its coordinates came from (`geocode_source` = source | census), so the
recovered points can always be told apart.

Run:  python pipeline/washington_dc/step3_geocode.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.census_geocoder import geocode_addresses  # noqa: E402
from pipeline.washington_dc.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_GEOCODED_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    DC_BBOX,
    GEOCODE_CACHE_DIR,
)


def main():
    if not BUSINESSES_CLEAN_CSV.exists():
        sys.exit(f"Missing {BUSINESSES_CLEAN_CSV}. Run "
                 f"step2_clean_businesses.py first.")

    df = pd.read_csv(BUSINESSES_CLEAN_CSV,
                     dtype={"record_id": str, "zip_code": str,
                            "MAR_ID": str, "CUSTOMERNUMBER": str})
    df["geocode_source"] = df["coord_status"].map({"source": "source"})
    todo = df[df["coord_status"] == "needs_geocode"]
    print(f"{len(df):,} premises: {len(df) - len(todo):,} with register "
          f"coordinates, {len(todo):,} to geocode by address\n")

    if todo.empty:
        out = df
    else:
        matched = geocode_addresses(
            todo, id_col="record_id", street_col="street_address",
            zip_col="zip_code", city="Washington", state="DC",
            cache_dir=GEOCODE_CACHE_DIR,
        )
        print(f"\nCensus matched {len(matched):,} of {len(todo):,} "
              f"({len(matched) / max(len(todo), 1):.1%}); match types: "
              f"{matched['match_type'].value_counts().to_dict()}")

        # Accept only points inside the District's bounds - a "match" in the
        # wrong place is worse than no match, and D.C.'s street grid repeats
        # across the Maryland line.
        b = DC_BBOX
        in_bounds = (matched["latitude"].between(b["lat_min"], b["lat_max"])
                     & matched["longitude"].between(b["lon_min"], b["lon_max"]))
        print(f"{int(in_bounds.sum()):,} matches fall inside the District's "
              f"bounds; {int((~in_bounds).sum()):,} rejected as out of bounds")
        matched = matched[in_bounds].drop_duplicates("id").set_index("id")

        recovered = (df["record_id"].isin(matched.index)
                     & (df["coord_status"] == "needs_geocode"))
        df.loc[recovered, "latitude"] = \
            df.loc[recovered, "record_id"].map(matched["latitude"])
        df.loc[recovered, "longitude"] = \
            df.loc[recovered, "record_id"].map(matched["longitude"])
        df.loc[recovered, "geocode_source"] = "census"

        # Independent check: are the recovered points inside the polygon, not
        # just inside the bounding box?
        if CITY_BOUNDARY_GEOJSON.exists() and recovered.any():
            dc = gpd.read_file(CITY_BOUNDARY_GEOJSON)
            dc = (dc.set_crs(CRS_GEOGRAPHIC) if dc.crs is None
                  else dc.to_crs(CRS_GEOGRAPHIC))
            rec = df[recovered]
            pts = gpd.GeoSeries(
                gpd.points_from_xy(rec["longitude"], rec["latitude"]),
                crs=CRS_GEOGRAPHIC)
            inside = pts.within(dc.geometry.iloc[0])
            print(f"Cross-check: {int(inside.sum()):,} of {len(rec):,} "
                  f"recovered points ({inside.mean():.1%}) fall inside the "
                  f"District polygon.")

        unresolved = df["geocode_source"].isna()
        print(f"\nUnrecovered (dropped): {int(unresolved.sum()):,} of "
              f"{len(df):,} ({unresolved.mean():.1%})")
        # The bias check the add-city skill requires: a loss concentrated in
        # one bucket would distort the map even at this size.
        if unresolved.any():
            tot = df["bucket"].value_counts()
            lost = df[unresolved]["bucket"].value_counts()
            print("  by bucket: " + ", ".join(
                f"{b} {lost.get(b, 0)}/{tot.get(b, 0)} "
                f"({lost.get(b, 0) / max(tot.get(b, 1), 1):.1%})"
                for b in tot.index))
        out = df[~unresolved]

    out = out.reset_index(drop=True)
    out["record_id"] = out.index.astype(str)
    print(f"\nBy bucket:\n  "
          + out["bucket"].value_counts().to_string().replace("\n", "\n  "))
    print(f"\nBy coordinate origin:\n  "
          + out["geocode_source"].value_counts().to_string().replace("\n", "\n  "))

    BUSINESSES_GEOCODED_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_GEOCODED_CSV, index=False)
    print(f"\nWrote {len(out):,} rows to {BUSINESSES_GEOCODED_CSV}")


if __name__ == "__main__":
    main()
