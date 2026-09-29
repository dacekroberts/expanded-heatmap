"""London step 2: the FSA's 33 London authority files -> the food storefronts
placed inside Greater London.

    python pipeline/london/step2_clean_businesses.py

Reads the cache only (pipeline/london/fetch_sources.py downloads). What a
reader should know before trusting the counts printed below:

  * only the fields in READ are ever read - never the rating, scores, phone
    or the authority's contact details; the page shows no rating (the FSA's
    conditions attach to a displayed rating);
  * a premises is placed at the FSA's OWN point or not at all (owner,
    2026-09-28: placement of the rest is decided later). A private-address
    record carries no point and only an outward postcode, so it is never
    placed - the owner's rule that a person's name is never shown at what
    looks like their home;
  * a business type the taxonomy does not know stops the step.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.london import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
READ = ("FHRSID", "BusinessName", "BusinessType", "PostCode", "LocalAuthorityName")
# "T/A", "t/a", "Also T/A", "(Trading as ...)", "trading as" - a whole word, so
# "Ta Va" (a restaurant) is untouched.
TRADING_AS = r"(?i)\s*\(?\b(?:also\s+)?(?:t/a|trading\s+as)\b\s*"


def load():
    files = sorted(config.FSA_RAW_DIR.glob("*.xml"))
    if len(files) != config.FSA_AUTHORITY_COUNT:
        sys.exit(f"{len(files)} authority files in {config.FSA_RAW_DIR}, expected "
                 f"{config.FSA_AUTHORITY_COUNT}: run python pipeline/london/fetch_sources.py")
    rows = []
    for f in files:
        for e in ET.parse(f).getroot().iter("EstablishmentDetail"):
            r = {k: (e.findtext(k) or "").strip() for k in READ}
            r["longitude"] = e.findtext("Geocode/Longitude") or ""
            r["latitude"] = e.findtext("Geocode/Latitude") or ""
            rows.append(r)
    return pd.DataFrame(rows)


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = load()
    print(f"  {len(df):,} register rows in {df['LocalAuthorityName'].nunique()} authorities")
    unknown = sorted(set(df["BusinessType"]) - TAX.KNOWN_TYPES)
    if unknown:
        sys.exit(f"  business type(s) the taxonomy does not know: {unknown}")
    if df["FHRSID"].duplicated().any():
        sys.exit(f"  {df['FHRSID'].duplicated().sum()} duplicate FHRSIDs")

    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")
    print("    " + ", ".join(f"{t} {n:,}" for t, n in df["BusinessType"].value_counts().items()))

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.assign(latitude=lat, longitude=lon)
    unplaced = df["latitude"].isna() | df["longitude"].isna()
    print(f"\n  {int(unplaced.sum()):,} without the FSA's own point, NOT placed "
          f"({unplaced.mean():.1%}); by authority, the most:")
    by = df.assign(u=unplaced).groupby("LocalAuthorityName")["u"].agg(["sum", "mean"])
    for name, r in by.sort_values("mean", ascending=False).head(6).iterrows():
        print(f"    {name:<26} {int(r['sum']):>5,} ({r['mean']:.1%})")
    df = df[~unplaced]

    box = config.LONDON_BBOX
    in_box = df["latitude"].between(box["lat_min"], box["lat_max"]) & \
        df["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    df = df[in_box]
    gl = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), index=df.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(gl)
    print(f"  {int((~inside).sum()):,} outside Greater London, dropped")
    df = df[inside]

    # The name on the shop: "Skinner Stores T/A Londis" and "Lydia Oduro
    # Enterprise Trading as LO" show what follows the trading-as marker - the
    # trade name, which is also what keeps a sole trader's own name off the map
    # where they registered both (the owner's rule, 2026-09-28).
    tas = df["BusinessName"].str.split(TRADING_AS, n=1, regex=True)
    has = tas.str.len() == 2
    shown = tas.str[-1].str.strip().str.strip("()").str.strip()
    df = df.assign(BusinessName=df["BusinessName"].where(~has | (shown == ""), shown))
    print(f"  {int(has.sum()):,} names carry a trading-as marker; the trade name after it is shown")

    out = df.rename(columns={"FHRSID": "fhrsid", "BusinessName": "business_name",
                             "LocalAuthorityName": "authority"})[
        ["fhrsid", "business_name", "latitude", "longitude", TAX.VALUE_COLUMN, "authority"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    bucket = out[TAX.VALUE_COLUMN].map(lambda v: TAX.classify({TAX.VALUE_COLUMN: v}))
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    print("    " + ", ".join(f"{TAX.legend_label(b)} {n:,}" for b, n in bucket.value_counts().items()))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
