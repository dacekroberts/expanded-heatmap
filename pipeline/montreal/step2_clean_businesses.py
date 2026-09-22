"""Step 2 - clean Montréal's commercial survey into a storefront set.

Input:  data/montreal/raw/occupation_commerciale.csv  (Ville de Montréal)
        data/montreal/raw/agglomeration.geojson
Output: data/montreal/processed/businesses_clean.csv

THIS IS THE SHORTEST STEP 2 IN THE PROJECT, and the reason is the source.
`locaux-commerciaux` is a FIELD SURVEY of street-level commerce, not a licence
register, so most of what every other city's step 2 does here has nothing to
do. There is no licence-status filter, no home-occupation exclusion, no
registrant-name fallback, no residence inference, no geocoding, and no
address dedup. What it has instead are two filters no other city has needed:

  **VACANT units are excluded.** `USAGE1 == 'VACANT'` on 3,500 of 28,621 rows.
  A licence register cannot contain an empty shop; a survey of premises can,
  and counting them would measure the supply of retail space rather than
  commerce.

  **`SCIAN` is filtered by LENGTH, not by null.** It is a 1-character
  placeholder on some rows, so `notna()` would keep codes that cannot be
  classified.

AND ADDRESS DEDUP IS DELIBERATELY ABSENT. `ID` is unique across every row, so
one row is one surveyed unit. 6,500 rows share an ADRESSE with another and
that is CORRECT: 7275 rue Sherbrooke E holds 174 units and 7999 boulevard des
Galeries-d'Anjou holds 152, each a distinct business with its own SUITE.
Miami's and Vancouver's (name, address) dedup would collapse a shopping centre
to one shop. This step asserts `ID` is unique instead, so if the survey ever
starts repeating it the run stops rather than silently over-counting.

Run:  python pipeline/montreal/step2_clean_businesses.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.montreal.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_RAW_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    FORBIDDEN_COLUMNS,
    MONTREAL_BBOX,
    PREMISES_KEY,
    PREMISES_TYPE_COLUMN,
    RAW_CLASSIFICATION_COLUMN,
    SCIAN_CODE_LENGTH,
    SOURCE_DELIMITER,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
    USAGE_COLUMN,
    USAGE_VACANT,
    VACANT_FOR_RENT_COLUMN,
)

MODULE = load_taxonomy_module(TAXONOMY_SYSTEM)


def main():
    for path in (BUSINESSES_RAW_CSV, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/montreal/fetch_sources.py first.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, sep=SOURCE_DELIMITER, dtype=str,
                     encoding=SOURCE_ENCODING, low_memory=False)
    print(f"Survey rows: {len(df):,}")

    leaked = sorted(set(df.columns) & set(FORBIDDEN_COLUMNS))
    if leaked:
        sys.exit(f"{leaked} present. This survey has never published a "
                 f"personal column; decide explicitly rather than filtering.")

    if not df[PREMISES_KEY].is_unique:
        n = int(df[PREMISES_KEY].duplicated().sum())
        sys.exit(f"{PREMISES_KEY} is no longer unique ({n:,} repeats). This "
                 f"step relies on one row being one surveyed unit and does NO "
                 f"address dedup, because 6,500 rows legitimately share an "
                 f"address. A premises key is now needed - see config.py.")
    print(f"  {PREMISES_KEY} unique: one row is one surveyed unit, so no "
          f"address dedup is done (6,500 rows share an address legitimately)")

    # --- vacancies ----------------------------------------------------------
    vacant = df[USAGE_COLUMN].eq(USAGE_VACANT)
    for_rent = df[VACANT_FOR_RENT_COLUMN].eq("Oui")
    print(f"\nVacancy, the filter no licence register needs:")
    print(f"  {USAGE_COLUMN} == {USAGE_VACANT!r}: {int(vacant.sum()):,} "
          f"({vacant.mean():.1%}) - EXCLUDED, an empty shopfront is premises "
          f"rather than a business")
    # MEASURED: for_rent is a strict SUBSET of vacant (0 rows are for-rent
    # without being USAGE1-vacant), i.e. "vacant AND advertised". So filtering
    # on it instead would keep the other 2,788 vacant units - which is exactly
    # why USAGE1 is the filter and this column is not.
    print(f"  {VACANT_FOR_RENT_COLUMN} == 'Oui': {int(for_rent.sum()):,} - a "
          f"strict SUBSET of the above ({int((for_rent & ~vacant).sum())} are "
          f"for-rent without being USAGE1-vacant), so filtering on it instead "
          f"would leave {int((vacant & ~for_rent).sum()):,} vacant units in")
    df = df[~vacant].copy()
    print(f"  remaining: {len(df):,}")

    # --- classification -----------------------------------------------------
    code = df[RAW_CLASSIFICATION_COLUMN].fillna("").str.strip()
    usable = code.str.len().eq(SCIAN_CODE_LENGTH)
    print(f"\n{RAW_CLASSIFICATION_COLUMN}: {int(usable.sum()):,} of "
          f"{len(df):,} are {SCIAN_CODE_LENGTH}-digit ({usable.mean():.1%}); "
          f"{int((~usable & code.ne('')).sum()):,} are shorter placeholders "
          f"and {int(code.eq('').sum()):,} are blank")
    df = df[usable].copy()
    # SCIAN IS NAICS, so the shared module classifies it unchanged. Renaming to
    # its VALUE_COLUMN is the only adaptation this city needs.
    df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: MODULE.VALUE_COLUMN})

    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM).copy()
    print(f"\nStorefront filter (naics.py, unchanged): {before:,} -> "
          f"{len(df):,} ({len(df) / before:.1%} kept) - the highest share of "
          f"any source here, because this is a survey of commerce rather than "
          f"a register of licences")
    df["bucket"] = [MODULE.classify(r) for r in
                    df[[MODULE.VALUE_COLUMN]].to_dict("records")]
    print("  " + ", ".join(f"{k}={v:,}" for k, v in
                           df["bucket"].value_counts().items()))
    print(f"\n  by premises type ({PREMISES_TYPE_COLUMN}) - ALL kept, see "
          f"config.py:")
    for k, v in df[PREMISES_TYPE_COLUMN].value_counts().items():
        print(f"      {v:>6,}  {k}")

    # --- coordinates --------------------------------------------------------
    df["latitude"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["LONG"], errors="coerce")
    bad = df["latitude"].isna() | df["longitude"].isna()
    if bad.any():
        print(f"\n  {int(bad.sum()):,} row(s) had unparseable LAT/LONG - dropped")
        df = df[~bad]
    b = MONTREAL_BBOX
    ok = (df["latitude"].between(b["lat_min"], b["lat_max"])
          & df["longitude"].between(b["lon_min"], b["lon_max"]))
    if not ok.all():
        print(f"  {int((~ok).sum()):,} row(s) outside the sanity box - dropped")
        df = df[ok]

    # --- inside the agglomeration? a CHECK, not a filter --------------------
    bnd = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    bnd = (bnd.set_crs(CRS_GEOGRAPHIC) if bnd.crs is None
           else bnd.to_crs(CRS_GEOGRAPHIC))
    geom = bnd.to_crs(CRS_PROJECTED).union_all()
    g = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = g.geometry.within(geom)
    print(f"\nInside the agglomeration: {int(inside.sum()):,} of {len(g):,} "
          f"({inside.mean():.2%})")
    # The publisher already scopes this file to its own territory, so the
    # polygon is a check - the same reasoning as Vancouver's, where a
    # containment filter would have deleted Stanley Park.
    if int((~inside).sum()):
        print(f"  {int((~inside).sum()):,} outside, listed rather than assumed "
              f"away (KEPT - the City surveys its own territory):")
        for r in g[~inside].head(8).itertuples():
            print(f"      {str(r.NOM_ETAB)[:34]:<34} {str(r.ADRESSE)[:32]:<32} "
                  f"{r.ARRONDISSEMENT}")
    g["in_boundary"] = inside

    # --- the label ----------------------------------------------------------
    # NOM_ETAB is the ESTABLISHMENT's name, populated on every row, and this
    # survey has no registrant-name column at all - so no pin can show a
    # person's name that this pipeline substituted. Structural, not measured.
    g["business_name"] = g["NOM_ETAB"].fillna("").str.strip()
    blank = g["business_name"].eq("")
    if blank.any():
        print(f"\n  dropping {int(blank.sum()):,} row(s) with a blank "
              f"NOM_ETAB (there is no second name column to fall back to, "
              f"which is why none is needed)")
        g = g[~blank]
    g["address"] = g["ADRESSE"].fillna("").str.strip()

    out_cols = ["business_name", "address", MODULE.VALUE_COLUMN, "bucket",
                "latitude", "longitude", PREMISES_KEY, PREMISES_TYPE_COLUMN,
                "ARRONDISSEMENT", "in_boundary"]
    out = g[out_cols].copy()
    print(f"\nFinal: {len(out):,} storefronts")
    print("  by bucket: " + ", ".join(
        f"{k}={v:,}" for k, v in out["bucket"].value_counts().items()))
    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.sort_values("business_name").to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"Wrote {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
