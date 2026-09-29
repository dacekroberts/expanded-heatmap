"""Step 2 - Buenos Aires' storefronts from the 2022-2024 land-use survey,
placed at their cadastral parcels' centroids.

A FIELD SURVEY, like Barcelona's and Dublin's: one row per use the surveyors
saw at an address, with no business names and no coordinates. Three filters
and one join:

  * `TIPO1 == "UNICOMERCIAL"` - a single-use shopfront. MULTICOMERCIAL (malls
    and arcades, whose shops are not itemised) is left out and counted for the
    page's disclosure (owner, 2026-09-28), as are homes with an economic
    activity (a RESIDENCIAL subtype).
  * `ESTADO == "ACTIVO"` - the vacancy filter.
  * the taxonomy (`ba_usos_suelo`), which drops "SIN IDENTIFICAR" shopfronts
    (counted, and disclosed - owner, 2026-09-28) and every non-storefront use.
  * THE PLACEMENT JOIN: the survey's SMP (section-block-parcel) against
    Parcelas' `smp`, both with spaces removed and upper-cased, and the pin at
    the parcel's centroid, taken in UTM 21S. A row whose parcel is absent
    falls back to its BLOCK (the mean of that block's parcel centroids). Both
    tiers are counted; the address-join skill's rule is tiers, never one rate.

Reads what `fetch_sources.py` downloaded and never fetches.
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely import wkt

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module
from pipeline.buenos_aires.config import (
    BUENOS_AIRES_BBOX,
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DATA_PROCESSED,
    FORBIDDEN_COLUMNS,
    PARCELS_CSV,
    RAW_CLASSIFICATION_COLUMN,
    SMP_SEPARATOR,
    SOURCE_ENCODING,
    SURVEY_CSV,
    TAXONOMY_SYSTEM,
)

TAX = load_taxonomy_module(TAXONOMY_SYSTEM)

EXPECTED_COLUMNS = ["OBJECTID", "SMP", "BARRIO", "TIPO1", "TIPO2", "ESTADO", "PISOS",
                    "GP_Q", "OBS", "CALLE", "PUERTA", "UNIFICADO", "SMP_IDEM", "AÑO"]

# CABA has 48 barrios; a survey that loses one has changed scope.
BARRIO_COUNT = 48

PARCEL_CHUNK = 20000


def smp_key(s):
    return s.str.replace(" ", "", regex=False).str.upper()


def block_key(key):
    """Section and block: the first two SMP fields."""
    return key.str.split(SMP_SEPARATOR, n=2).str[:2].str.join(SMP_SEPARATOR)


def parcel_centroids():
    """{smp key: (x, y)} in UTM 21S for every parcel, read in chunks: the file
    is 329 MB of WKT polygons, and only `smp` and `geometry` are read."""
    keys, xs, ys = [], [], []
    n = 0
    for ch in pd.read_csv(PARCELS_CSV, usecols=["smp", "geometry"], dtype=str,
                          chunksize=PARCEL_CHUNK, encoding=SOURCE_ENCODING):
        n += len(ch)
        ch = ch[ch["smp"].notna() & ch["geometry"].notna()]
        c = gpd.GeoSeries(ch["geometry"].map(wkt.loads), crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).centroid
        keys.extend(smp_key(ch["smp"]))
        xs.extend(c.x)
        ys.extend(c.y)
    parcels = pd.DataFrame({"key": keys, "x": xs, "y": ys})
    dup = int(parcels["key"].duplicated().sum())
    print(f"parcels read                               {n:>9,}   "
          f"({dup:,} duplicate keys; first kept)")
    emit("parcels", n)
    return parcels.drop_duplicates("key")


def main():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    for path in (SURVEY_CSV, PARCELS_CSV):
        if not path.exists():
            raise SystemExit(f"{path.name} is missing, and a step never fetches.\n"
                             "  Run:  python pipeline/buenos_aires/fetch_sources.py")

    print("=== Step 2: Buenos Aires storefronts (land-use survey 2022-2024) ===\n")
    df = pd.read_csv(SURVEY_CSV, dtype=str, encoding=SOURCE_ENCODING)
    leaked = [c for c in df.columns if c.lower() in FORBIDDEN_COLUMNS]
    if leaked or list(df.columns) != EXPECTED_COLUMNS:
        raise SystemExit(f"the survey's columns changed: {list(df.columns)}. It has "
                         "carried no names; re-read the privacy position first.")
    for col in ("TIPO1", "TIPO2", "BARRIO"):
        df[col] = df[col].map(TAX.repair)
    print(f"rows in the survey                         {len(df):>9,}")
    emit("survey_rows", len(df))

    active = df[TAX.ACTIVE_COLUMN].eq(TAX.ACTIVE_VALUE)
    multi = int((active & df[TAX.TYPE_COLUMN].eq("MULTICOMERCIAL")).sum())
    print(f"active MULTICOMERCIAL (left out, disclosed) {multi:>8,}")
    emit("multicomercial_active", multi)

    df = df[active & df[TAX.TYPE_COLUMN].eq(TAX.TYPE_VALUE)].copy()
    print(f"active single-use shopfronts               {len(df):>9,}")
    emit("unicomercial_active", len(df))
    unidentified = int(df[RAW_CLASSIFICATION_COLUMN].eq("SIN IDENTIFICAR").sum())
    print(f"  of which SIN IDENTIFICAR (dropped, disclosed) {unidentified:>5,}")
    emit("sin_identificar_active", unidentified)

    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"in the three storefront buckets            {len(df):>9,}"
          f"   (dropped {before - len(df):,})")
    df["bucket"] = [TAX.classify({RAW_CLASSIFICATION_COLUMN: v}) for v in df[RAW_CLASSIFICATION_COLUMN]]
    for bucket, n in df["bucket"].value_counts().items():
        print(f"    {bucket:<20} {n:>9,}")
        emit(f"bucket_{bucket.lower().replace(' ', '_')}", int(n))
    emit("storefront_rows", len(df))

    # --- merged parcels: measured, not de-duplicated --------------------------
    same = df.duplicated(["SMP", RAW_CLASSIFICATION_COLUMN, "CALLE", "PUERTA"], keep=False)
    print(f"\nrows sharing SMP, use, street and number   {int(same.sum()):>9,}"
          f"   (UNIFICADO=SI on {int(df['UNIFICADO'].eq('SI').sum()):,})")
    emit("same_use_same_door_rows", int(same.sum()))

    # --- placement -----------------------------------------------------------
    print("\nPlacement (a join to Parcelas, not a geocoder):")
    parcels = parcel_centroids()
    df["key"] = smp_key(df["SMP"].fillna(""))
    exact = df.merge(parcels, on="key", how="left")
    hit = exact["x"].notna()
    parcels["block"] = block_key(parcels["key"])
    blocks = parcels.groupby("block")[["x", "y"]].mean()
    miss = exact.loc[~hit].drop(columns=["x", "y"])
    miss["block"] = block_key(miss["key"])
    by_block = miss.join(blocks, on="block")
    placed_block = by_block["x"].notna()
    out = pd.concat([exact.loc[hit].assign(placement="parcel"),
                     by_block.loc[placed_block].drop(columns="block").assign(placement="block")])
    unplaced = int((~placed_block).sum())
    n = len(df)
    print(f"  parcel centroid (exact SMP)              {int(hit.sum()):>9,}   ({hit.mean():.1%})")
    print(f"  block centroid (fallback)                {int(placed_block.sum()):>9,}   "
          f"({placed_block.sum() / n:.1%})")
    print(f"  unplaced                                 {unplaced:>9,}   ({unplaced / n:.1%})")
    emit("placed_parcel", int(hit.sum()))
    emit("placed_block", int(placed_block.sum()))
    emit("unplaced", unplaced)

    pts = gpd.GeoSeries(gpd.points_from_xy(out["x"], out["y"]), crs=CRS_PROJECTED).to_crs(CRS_GEOGRAPHIC)
    out["latitude"], out["longitude"] = pts.y.values, pts.x.values
    b = BUENOS_AIRES_BBOX
    inside = (out["latitude"].between(b["lat_min"], b["lat_max"])
              & out["longitude"].between(b["lon_min"], b["lon_max"]))
    if not inside.all():
        raise SystemExit(f"{int((~inside).sum())} placed rows fall outside CABA's box - "
                         "a join error, not a finding.")
    stacked = out.groupby("key").size()
    print(f"  parcels holding more than one storefront {int((stacked > 1).sum()):>9,}   "
          f"(pins stack at the centroid; max {int(stacked.max())})")
    emit("stacked_parcels", int((stacked > 1).sum()))

    barrios = out["BARRIO"].nunique()
    if barrios != BARRIO_COUNT:
        raise SystemExit(f"{barrios} barrios, expected {BARRIO_COUNT}.")
    print(f"  across all {barrios} barrios")

    # No names exist in the survey. The pin reads as its street address, the
    # France and Czechia fallback when a register has no trade name.
    addr = (out["CALLE"].fillna("").str.strip().str.title() + " "
            + out["PUERTA"].fillna("").str.strip()).str.strip()
    out["business_name"] = addr.where(addr != "", "Address not recorded")

    clean = pd.DataFrame({
        "business_name": out["business_name"].values,
        "latitude": out["latitude"].round(6).values,
        "longitude": out["longitude"].round(6).values,
        RAW_CLASSIFICATION_COLUMN: out[RAW_CLASSIFICATION_COLUMN].values,
        "bucket": out["bucket"].values,
        "barrio": out["BARRIO"].values,
        "placement": out["placement"].values,
        "survey_year": out["AÑO"].values,
    }).sort_values(["barrio", "business_name", RAW_CLASSIFICATION_COLUMN], kind="stable")
    clean.to_csv(BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    emit("businesses_clean_rows", len(clean))
    print(f"\nWrote {len(clean):,} storefronts to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
