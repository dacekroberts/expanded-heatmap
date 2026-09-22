"""Step 2 - clean Calgary's business licences into a storefront set.

Input:  data/calgary/raw/business_licences.csv  (OGL - City of Calgary)
        data/calgary/raw/city_boundary.geojson
Output: data/calgary/processed/businesses_clean.csv

CALGARY DOES MOST OF THE CLASSIFYING ITSELF, which is what makes this step
short. Its own categories carry `- PREMISES`, `- NO PREMISES`, `(MOBILE)`,
`(HOME BASED)`, `(MAIL ORDER)` and `(DIRECT SALES)` suffixes, so the question
every other city answers by inference is answered in the category string. See
pipeline/taxonomies/calgary_licencetype.py.

THREE THINGS THIS STEP DOES THAT ARE SPECIFIC TO THIS REGISTER.

  **It splits `licencetypes` on `",\\n"` - a comma AND a newline.** 9,136 of
  23,203 rows carry more than one category, and splitting on a bare "\\n" is
  what produced the "173 categories" in the Canada profile: it shreds each
  value and counts the fragments. The real count is 96.

  **It resolves multi-category rows by BUCKET_PRIORITY**, so a premises that
  holds `FOOD SERVICE - PREMISES` plus `ALCOHOL BEVERAGE SALES (RESTAURANT)`
  plus `OUTDOOR PATIO` counts once, as food service. Those last two are
  endorsements rather than businesses - D.C.'s problem, and the reason most of
  the multi-category rows exist.

  **It parses `point`, a WKT string, not a lat/lon pair.** Populated on 100%
  of rows, so there is no geocoding step.

AND THREE THINGS IT DELIBERATELY DOES NOT DO: no residence inference
(`homeoccind` is `N` on every row - constant, not merely unreliable, and
Vancouver's parcel substitute removed nothing anyway); no name fallback
(`tradename` is blank on ZERO rows); and no personal-column filtering, because
the register publishes none - asserted rather than assumed.

Run:  python pipeline/calgary/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.calgary.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_RAW_CSV,
    CALGARY_BBOX,
    CATEGORY_DELIMITER,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    FORBIDDEN_COLUMNS,
    NAME_COLUMN,
    POINT_COLUMN,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
    STATUS_COLUMN,
    STATUS_KEEP,
    TAXONOMY_SYSTEM,
)

MODULE = load_taxonomy_module(TAXONOMY_SYSTEM)
# "POINT (-114.0719 51.0447)" -> the two numbers.
WKT_POINT = re.compile(r"POINT\s*\(\s*(-?[\d.]+)\s+(-?[\d.]+)\s*\)", re.I)


def winning_category(raw):
    """A premises may hold several categories; resolve to the one whose bucket
    wins under BUCKET_PRIORITY, keeping CALGARY'S OWN wording for the tooltip
    rather than substituting a bucket name."""
    cats = [c.strip() for c in str(raw).split(CATEGORY_DELIMITER) if c.strip()]
    if not cats:
        return None
    ranked = []
    for c in cats:
        bucket = MODULE.classify({MODULE.VALUE_COLUMN: c})
        rank = (MODULE.BUCKET_PRIORITY.index(bucket)
                if bucket in MODULE.BUCKET_PRIORITY
                else len(MODULE.BUCKET_PRIORITY))
        ranked.append((rank, c))
    ranked.sort(key=lambda t: t[0])
    return ranked[0][1]


def main():
    for path in (BUSINESSES_RAW_CSV, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/calgary/fetch_sources.py first.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, encoding=SOURCE_ENCODING,
                     low_memory=False)
    print(f"Licence rows: {len(df):,}")

    leaked = sorted({c for c in df.columns
                     if c.lower() in {f.lower() for f in FORBIDDEN_COLUMNS}})
    if leaked:
        sys.exit(f"{leaked} present. This register has never published a "
                 f"personal column; decide explicitly rather than filtering.")
    print(f"  {len(df.columns)} columns, none personal (asserted)")

    # --- active licences ----------------------------------------------------
    print(f"\n{STATUS_COLUMN}, every value:")
    for k, v in df[STATUS_COLUMN].fillna("<na>").value_counts().items():
        mark = "keep" if k in STATUS_KEEP else "DROP"
        print(f"      {v:>7,}  {k:<28} {mark}")
    before = len(df)
    df = df[df[STATUS_COLUMN].isin(STATUS_KEEP)].copy()
    print(f"  active: {before:,} -> {len(df):,} ({before - len(df):,} dropped) "
          f"- 'Move in Progress' goes because a relocating business's recorded "
          f"address is the one thing this map depends on and the one thing in "
          f"doubt")

    # `homeoccind` is deliberately unused; print it so its uselessness is
    # visible rather than a silent omission.
    if "homeoccind" in df.columns:
        vals = df["homeoccind"].fillna("<na>").value_counts().to_dict()
        print(f"  homeoccind: {vals} - CONSTANT, so no residence signal exists "
              f"here and none is inferred (Vancouver's parcel substitute "
              f"removed nothing)")

    # --- classification -----------------------------------------------------
    multi = df[RAW_CLASSIFICATION_COLUMN].fillna("").str.contains(
        CATEGORY_DELIMITER, regex=False)
    print(f"\n{RAW_CLASSIFICATION_COLUMN}: {int(multi.sum()):,} rows carry more "
          f"than one category; resolved by BUCKET_PRIORITY "
          f"{MODULE.BUCKET_PRIORITY}")
    df[MODULE.VALUE_COLUMN] = df[RAW_CLASSIFICATION_COLUMN].map(winning_category)
    df = df[df[MODULE.VALUE_COLUMN].notna()]

    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM).copy()
    print(f"\nStorefront filter: {before:,} -> {len(df):,} "
          f"({len(df) / before:.1%} kept) - second only to Montréal's 69.4%, "
          f"because Calgary's register is premises-shaped before this project "
          f"filters anything")
    df["bucket"] = [MODULE.classify(r) for r in
                    df[[MODULE.VALUE_COLUMN]].to_dict("records")]
    print("  " + ", ".join(f"{k}={v:,}" for k, v in
                           df["bucket"].value_counts().items()))

    # --- coordinates: a WKT POINT string ------------------------------------
    pts = df[POINT_COLUMN].fillna("").str.extract(WKT_POINT)
    df["longitude"] = pd.to_numeric(pts[0], errors="coerce")
    df["latitude"] = pd.to_numeric(pts[1], errors="coerce")
    bad = df["latitude"].isna() | df["longitude"].isna()
    if bad.any():
        print(f"\n  {int(bad.sum()):,} row(s) had an unparseable {POINT_COLUMN} "
              f"- dropped (sample: {df.loc[bad, POINT_COLUMN].head(2).tolist()})")
        df = df[~bad]
    b = CALGARY_BBOX
    ok = (df["latitude"].between(b["lat_min"], b["lat_max"])
          & df["longitude"].between(b["lon_min"], b["lon_max"]))
    if not ok.all():
        print(f"  {int((~ok).sum()):,} row(s) outside the sanity box - dropped")
        df = df[ok]

    # --- inside Calgary: a CHECK, not a filter ------------------------------
    bnd = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    bnd = (bnd.set_crs(CRS_GEOGRAPHIC) if bnd.crs is None
           else bnd.to_crs(CRS_GEOGRAPHIC))
    geom = bnd.to_crs(CRS_PROJECTED).union_all()
    g = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = g.geometry.within(geom)
    print(f"\nInside Calgary: {int(inside.sum()):,} of {len(g):,} "
          f"({inside.mean():.2%})")
    if int((~inside).sum()):
        print(f"  {int((~inside).sum()):,} outside, listed rather than assumed "
              f"away (KEPT - the City licenses its own territory):")
        for r in g[~inside].head(8).itertuples():
            print(f"      {str(getattr(r, NAME_COLUMN))[:34]:<34} "
                  f"{str(r.address)[:34]}")
    g["in_boundary"] = inside

    # --- the label ----------------------------------------------------------
    # `tradename` is blank on zero rows and there is no second name column, so
    # there is no fallback and no substituted-name exposure.
    g["business_name"] = g[NAME_COLUMN].fillna("").str.strip()
    blank = g["business_name"].eq("")
    if blank.any():
        print(f"\n  dropping {int(blank.sum()):,} row(s) with a blank "
              f"{NAME_COLUMN} (there is no second name column to fall back to, "
              f"which is why none is needed)")
        g = g[~blank]
    g["address"] = g["address"].fillna("").str.strip()

    # --- dedup: one row per premises ---------------------------------------
    order = {b: i for i, b in enumerate(MODULE.BUCKET_PRIORITY)}
    g["_rank"] = g["bucket"].map(order).fillna(len(order)).astype(int)
    g["_name"] = g["business_name"].str.upper().str.strip()
    g["_addr"] = g["address"].str.upper().str.strip()
    before = len(g)
    g = (g.sort_values("_rank")
          .drop_duplicates(subset=["_name", "_addr"], keep="first")
          .drop(columns=["_rank", "_name", "_addr"]))
    print(f"\nDedup on (name, address): {before:,} -> {len(g):,} "
          f"({before - len(g):,} duplicate licences at one premises)")

    out_cols = ["business_name", "address", MODULE.VALUE_COLUMN, "bucket",
                "latitude", "longitude", "getbusid", "in_boundary"]
    out = g[[c for c in out_cols if c in g.columns]].copy()
    print(f"\nFinal: {len(out):,} storefronts")
    print("  by bucket: " + ", ".join(
        f"{k}={v:,}" for k, v in out["bucket"].value_counts().items()))
    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.sort_values("business_name").to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"Wrote {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
