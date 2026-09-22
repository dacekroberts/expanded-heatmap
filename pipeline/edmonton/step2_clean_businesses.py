"""Step 2 - clean Edmonton's business licences into a storefront set.

Input:  data/edmonton/raw/business_licences.csv  (Open Data Terms of Use)
        data/edmonton/raw/city_boundary.geojson
Output: data/edmonton/processed/businesses_clean.csv

EDMONTON IS THE FIRST CITY IN THIS PROJECT WHERE THE PUBLISHER DID THE PRIVACY
WORK UPSTREAM, and it changes the shape of this step. Two registers ago,
Vancouver needed a parcel join and a parenthesis heuristic to decide whether a
pin was a person's home. Edmonton needs neither:

  **`licencetype` states premises-or-person.** Keeping `Commercial` (25,105 of
  43,672) drops `Home Based` (14,114) outright, plus `Non-Resident` (2,108,
  mobile trade) and the two individual-held types, `Massage Practitioner`
  (1,582) and `Adult Services` (763). That is Surrey's shape - the city
  asserts it - so NO residence inference is attempted or needed.

  **The City redacts the address itself.** `<REDACTED FOR PRIVACY>` stands in
  for `business_address` on 1,729 of the Commercial rows, and those rows carry
  no coordinates either. They are therefore LOST rather than suppressed, and
  the distinction matters: this step removes nothing for privacy, because
  there is nothing left to remove. `read-licence` step 6b.

  **There is no name to fall back TO.** The register publishes exactly one
  name column and it is the business's - no registrant, owner or contact
  field exists. So Edmonton's privacy position is structural rather than
  measured: no pin CAN be a person's name. Asserted here and in
  fetch_sources.py rather than assumed.

THREE THINGS THIS STEP DOES THAT ARE SPECIFIC TO THIS REGISTER.

  **It splits `business_licence_category` on `";"`.** 5,340 of 25,105 rows
  carry more than one category. A naive `value_counts()` on the raw column
  returns 1,247 COMBINATIONS, which is how the Canada profile arrived at "67
  categories"; the true vocabulary is 60.

  **It resolves multi-category rows by BUCKET_PRIORITY, and unlike Calgary it
  does not have to drop endorsements to do it.** Calgary emits one row per
  category, so an alcohol endorsement is a second row that would double-count
  the restaurant. Edmonton emits one row per licence, so the endorsement is a
  second string on the same row and the pin exists once either way - which is
  why `Alcohol Sales (Consumption On-Premises / *)` is bucketed here and was
  mapped to None in Calgary. See the taxonomy module.

  **It scopes to the city by POLYGON, not by a city field.** The register is
  municipal, so every row is nominally Edmonton's, but the boundary is still
  the check that a coordinate is where it claims - and `qqvh-dp5m` is the
  current corporate boundary of four same-named layers.

Run:  python pipeline/edmonton/step2_clean_businesses.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.edmonton.config import (  # noqa: E402
    ADDRESS_COLUMN,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_RAW_CSV,
    CATEGORIES_EXPECTED,
    CATEGORY_DELIMITER,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EDMONTON_BBOX,
    EXPIRY_COLUMN,
    FORBIDDEN_COLUMNS,
    LICENCE_TYPE_COLUMN,
    LICENCE_TYPE_KEEP,
    NAME_COLUMN,
    PREMISES_KEY,
    RAW_CLASSIFICATION_COLUMN,
    REDACTED_ADDRESS,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
)

MODULE = load_taxonomy_module(TAXONOMY_SYSTEM)


def winning_category(raw):
    """A premises may hold several categories; resolve to the one whose bucket
    wins under BUCKET_PRIORITY, keeping EDMONTON'S OWN wording for the tooltip
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
                     f"pipeline/edmonton/fetch_sources.py first.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, encoding=SOURCE_ENCODING,
                     low_memory=False)
    print(f"Licence rows: {len(df):,}")

    leaked = sorted({c for c in df.columns
                     if c.lower() in {f.lower() for f in FORBIDDEN_COLUMNS}})
    if leaked:
        sys.exit(f"{leaked} present. This register has never published a "
                 f"personal name column, which is the whole basis of "
                 f"Edmonton's privacy position; decide explicitly rather than "
                 f"filtering.")
    print(f"  {len(df.columns)} columns, one name column and it is the "
          f"business's (asserted)")

    # --- premises, not people ----------------------------------------------
    print(f"\n{LICENCE_TYPE_COLUMN}, every value:")
    for k, v in df[LICENCE_TYPE_COLUMN].fillna("<na>").value_counts().items():
        mark = "keep" if k == LICENCE_TYPE_KEEP else "DROP"
        note = {
            "Home Based": "  someone's home - the city states it, so no inference",
            "Non-Resident": "  mobile trade",
            "Massage Practitioner": "  a person, not a premises",
            "Adult Services": "  a person, and out of scope on sensitivity",
        }.get(k, "")
        print(f"      {v:>7,}  {k:<24} {mark}{note}")
    before = len(df)
    df = df[df[LICENCE_TYPE_COLUMN] == LICENCE_TYPE_KEEP].copy()
    print(f"  premises: {before:,} -> {len(df):,} ({before - len(df):,} dropped)")

    # --- the publisher's own redaction, reported not acted on --------------
    red = df[ADDRESS_COLUMN].fillna("") == REDACTED_ADDRESS
    print(f"\n{REDACTED_ADDRESS} on {int(red.sum()):,} rows "
          f"({100 * red.mean():.1f}%) - the publisher's redaction, not a gap. "
          f"These carry no coordinates either, so they are lost at the "
          f"coordinate check below rather than suppressed here.")
    blank_name = df[NAME_COLUMN].isna() | df[NAME_COLUMN].fillna("").eq("")
    print(f"  {NAME_COLUMN} blank on {int(blank_name.sum())} rows - there is no "
          f"second name column to fall back to, so these are dropped rather "
          f"than filled")
    df = df[~blank_name].copy()

    # --- active licences ----------------------------------------------------
    exp = pd.to_datetime(df[EXPIRY_COLUMN], errors="coerce", format="mixed")
    today = pd.Timestamp.today().normalize()
    lapsed = exp.notna() & (exp < today)
    print(f"\n{EXPIRY_COLUMN}: {int(lapsed.sum()):,} already lapsed "
          f"({int(exp.isna().sum())} unparseable). The register publishes "
          f"current licences rather than a term history, so this is the active "
          f"flag and it removes very little.")
    df = df[~lapsed].copy()
    print(f"  active: {len(df):,}")

    # --- classification -----------------------------------------------------
    cats = set()
    for v in df[RAW_CLASSIFICATION_COLUMN].fillna(""):
        cats.update(c.strip() for c in str(v).split(CATEGORY_DELIMITER)
                    if c.strip())
    multi = df[RAW_CLASSIFICATION_COLUMN].fillna("").str.contains(
        CATEGORY_DELIMITER, regex=False)
    print(f"\n{RAW_CLASSIFICATION_COLUMN}: {len(cats)} distinct categories "
          f"(expected {CATEGORIES_EXPECTED}); {int(multi.sum()):,} rows carry "
          f"more than one, resolved by BUCKET_PRIORITY "
          f"{MODULE.BUCKET_PRIORITY}")
    if len(cats) != CATEGORIES_EXPECTED:
        print(f"  NOTE: the vocabulary changed. classify() raises on an "
              f"unknown category, so a new one will stop this run below.")

    df[MODULE.VALUE_COLUMN] = df[RAW_CLASSIFICATION_COLUMN].map(winning_category)
    df = df[df[MODULE.VALUE_COLUMN].notna()].copy()

    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"  storefront: {before:,} -> {len(df):,} "
          f"({before - len(df):,} dropped as out of scope)")
    print("  by bucket:")
    buckets = df[MODULE.VALUE_COLUMN].map(
        lambda v: MODULE.classify({MODULE.VALUE_COLUMN: v}))
    for k, v in buckets.value_counts().items():
        print(f"      {v:>7,}  {k}")

    # --- coordinates --------------------------------------------------------
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    before = len(df)
    missing = df["latitude"].isna() | df["longitude"].isna()
    still_red = (df.loc[missing, ADDRESS_COLUMN].fillna("")
                 == REDACTED_ADDRESS).sum()
    print(f"\nCoordinates: {int(missing.sum()):,} of {before:,} storefront rows "
          f"have none ({100 * missing.mean():.1f}%), of which {int(still_red):,} "
          f"are the publisher's redacted addresses.")
    print(f"  The redaction is nearly all spent before this point: of the 1,729 "
          f"redacted Commercial rows, only {int(still_red):,} reach here, "
          f"because the rest fall out on category. So this {int(missing.sum())}"
          f"-row loss is ordinary missing data, NOT the privacy work.")
    print(f"  No geocoding step: there is no national Canadian geocoder, and "
          f"nothing here to geocode - a redacted row has no address either, "
          f"so the City removed the geolocation along with it (France's "
          f"diffusion-status masking does the same).")
    df = df[~missing].copy()

    in_box = (df["latitude"].between(EDMONTON_BBOX["lat_min"],
                                     EDMONTON_BBOX["lat_max"])
              & df["longitude"].between(EDMONTON_BBOX["lon_min"],
                                        EDMONTON_BBOX["lon_max"]))
    if int((~in_box).sum()):
        print(f"  {int((~in_box).sum()):,} outside the sanity box - dropped")
    df = df[in_box].copy()
    print(f"  with usable coordinates: {len(df):,} "
          f"({100 * len(df) / before:.1f}% of storefront rows)")

    # --- in-city, by polygon ------------------------------------------------
    b = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    geom = b.to_crs(CRS_PROJECTED).union_all()
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = gdf.geometry.within(geom)
    print(f"\nInside the corporate boundary: {int(inside.sum()):,} of "
          f"{len(gdf):,} ({int((~inside).sum()):,} outside - a municipal "
          f"register should contain few, so a large number here would mean the "
          f"wrong boundary layer)")
    df = gdf[inside].drop(columns="geometry").copy()

    # --- deduplicate on the register's own key ------------------------------
    before = len(df)
    df = df.drop_duplicates(subset=[PREMISES_KEY]).copy()
    print(f"\nDeduplicated on {PREMISES_KEY}: {before:,} -> {len(df):,} "
          f"({before - len(df):,} dropped - not on business name, because "
          f"chains share names)")

    # --- the shared column contract ----------------------------------------
    out = df.rename(columns={NAME_COLUMN: "business_name"})[
        ["business_name", "latitude", "longitude", MODULE.VALUE_COLUMN,
         ADDRESS_COLUMN, PREMISES_KEY]].rename(
        columns={ADDRESS_COLUMN: "address"})
    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.sort_values(PREMISES_KEY).to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(out):,} storefronts to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
