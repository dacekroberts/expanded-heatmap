"""Glasgow step 2: the FSA's Glasgow City file (Scotland's FHIS scheme) -> the
food storefronts placed inside Glasgow City.

    python pipeline/glasgow/step2_clean_businesses.py

Reads the cache only (pipeline/glasgow/fetch_sources.py downloads). The FSA
reader and its rules are shared with London (pipeline/fsa.py). What a reader
should know before trusting the counts printed below:

  * only pipeline/fsa.py's READ fields are ever read - never the FHIS result
    ("Pass", "Improvement Required"), the phone or the authority's contacts;
    the page shows no result;
  * a storefront at a "Flat" address is never placed (the flat rule, owner
    2026-09-28): Glasgow City lists home bakers and cooks as restaurants at
    their tenement flat, with a point;
  * a premises is placed at the FSA's OWN point or not at all (owner,
    2026-09-28: no postcode centroids here - they would place about 22 more,
    0.4%, at the cost of a second licence notice); the rest are disclosed;
  * a business type the taxonomy does not know stops the step.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import fsa  # noqa: E402
from pipeline.glasgow import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)


def main():
    if not config.FSA_XML.exists():
        sys.exit(f"missing {config.FSA_XML}: run python pipeline/glasgow/fetch_sources.py")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = fsa.load([config.FSA_XML])
    print(f"  {len(df):,} register rows")
    authorities = set(df["LocalAuthorityName"])
    if authorities != {config.FSA_AUTHORITY_NAME}:
        sys.exit(f"  the file names authorities {sorted(authorities)}, expected {config.FSA_AUTHORITY_NAME!r}")
    unknown = sorted(set(df["BusinessType"]) - TAX.KNOWN_TYPES)
    if unknown:
        sys.exit(f"  business type(s) the taxonomy does not know: {unknown}")
    if df["FHRSID"].duplicated().any():
        sys.exit(f"  {df['FHRSID'].duplicated().sum()} duplicate FHRSIDs")

    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")
    print("    " + ", ".join(f"{t} {n:,}" for t, n in df["BusinessType"].value_counts().items()))
    df = fsa.drop_home_premises(df)

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.assign(latitude=lat, longitude=lon, placement="fsa_point")
    no_point = df["latitude"].isna() | df["longitude"].isna()
    pc = df["PostCode"].str.upper().str.strip()
    print(f"\n  {int(no_point.sum()):,} without the FSA's own point, NOT placed ({no_point.mean():.1%}):")
    print(f"    with a full postcode {int((no_point & pc.str.match(fsa.FULL_POSTCODE)).sum()):,}, "
          f"outward code only {int((no_point & pc.str.match(fsa.OUTWARD_POSTCODE)).sum()):,}, "
          f"none {int((no_point & (pc == '')).sum()):,}")
    df = df[~no_point]

    box = config.GLASGOW_BBOX
    in_box = df["latitude"].between(box["lat_min"], box["lat_max"]) & \
        df["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    df = df[in_box]
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), index=df.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(city)
    print(f"  {int((~inside).sum()):,} outside Glasgow City, dropped")
    df = df[inside]

    df = fsa.trade_names(df)

    out = df.rename(columns={"FHRSID": "fhrsid", "BusinessName": "business_name",
                             "LocalAuthorityName": "authority"})[
        ["fhrsid", "business_name", "latitude", "longitude", TAX.VALUE_COLUMN, "authority", "placement"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    bucket = out[TAX.VALUE_COLUMN].map(lambda v: TAX.classify({TAX.VALUE_COLUMN: v}))
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    print("    " + ", ".join(f"{TAX.legend_label(b)} {n:,}" for b, n in bucket.value_counts().items()))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
