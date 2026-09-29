"""Newcastle (Regional) step 2: the FSA's five Tyne and Wear authority files ->
the food storefronts placed inside the five districts.

    python pipeline/newcastle/step2_clean_businesses.py

Reads the cache only (pipeline/newcastle/fetch_sources.py downloads). The FSA
reader and its rules are shared (pipeline/fsa.py). What a reader should know
before trusting the counts printed below:

  * only pipeline/fsa.py's READ fields are ever read - never the rating,
    scores, phone or the authority's contact details; the page shows no
    rating (the FSA's conditions attach to a displayed rating);
  * a storefront at a "Flat" address, or named as a childminder, is never
    placed (the flat and childminder rules, owner 2026-09-28);
  * a premises is placed at the FSA's OWN point, else (config.PLACE_AT_CENTROIDS)
    its full postcode's centroid, London's tier. A private-address record
    carries no point and only an outward postcode, so it is never placed;
  * a business type the taxonomy does not know stops the step.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import fsa  # noqa: E402
from pipeline.newcastle import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    files = [config.FSA_RAW_DIR / f"{code}.xml" for code in config.FSA_AUTHORITIES]
    missing = [f.name for f in files if not f.exists()]
    if missing:
        sys.exit(f"missing {missing}: run python pipeline/newcastle/fetch_sources.py")
    df = fsa.load(files)
    print(f"  {len(df):,} register rows in {df['LocalAuthorityName'].nunique()} authorities")
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
    print(f"\n  {int(no_point.sum()):,} without the FSA's own point ({no_point.mean():.1%})")

    pc = df["PostCode"].str.upper().str.strip()
    full = pc.str.match(fsa.FULL_POSTCODE)
    outward = no_point & pc.str.match(fsa.OUTWARD_POSTCODE)
    joinable = pd.Series(False, index=df.index)
    if config.PLACE_AT_CENTROIDS:
        # Tier 2: the postcode unit's centroid (OS Code-Point Open), for a FULL
        # postcode only, kept to the five districts' GSS codes.
        cp = fsa.codepoint(config.CODEPOINT_ZIP, config.CODEPOINT_DISTRICTS, config.CODEPOINT_CRS,
                           config.CRS_GEOGRAPHIC, "python pipeline/newcastle/fetch_sources.py")
        key = pc.str.replace(r"\s+", "", regex=True)
        joinable = no_point & full & key.isin(cp.index)
        ll = cp.loc[key[joinable], ["latitude", "longitude"]].to_numpy()
        df.loc[joinable, ["latitude", "longitude"]] = ll
        df.loc[joinable, "placement"] = "postcode_centroid"
        print(f"    placed at their postcode's centroid: {int(joinable.sum()):,}")
        print(f"    full postcode not in Code-Point (left unplaced): {int((no_point & full & ~joinable).sum()):,}")
    else:
        print(f"    with a full postcode, not placed (no centroid tier): {int((no_point & full).sum()):,}")
    print(f"    outward code only - a private address, never placed: {int(outward.sum()):,}")
    print(f"    no usable postcode (left unplaced): {int((no_point & ~full & ~outward).sum()):,}")
    unplaced = no_point & ~joinable
    print(f"  {int(unplaced.sum()):,} NOT placed ({unplaced.mean():.1%}); by authority:")
    by = df.assign(u=unplaced).groupby("LocalAuthorityName")["u"].agg(["sum", "mean"])
    for name, r in by.sort_values("mean", ascending=False).iterrows():
        print(f"    {name:<26} {int(r['sum']):>5,} ({r['mean']:.1%})")
    df = df[~unplaced]

    box = config.NEWCASTLE_BBOX
    in_box = df["latitude"].between(box["lat_min"], box["lat_max"]) & \
        df["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    df = df[in_box]
    area = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), index=df.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(area)
    print(f"  {int((~inside).sum()):,} outside the five districts, dropped")
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
