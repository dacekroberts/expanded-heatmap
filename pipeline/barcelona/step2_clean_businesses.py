"""Step 2 - Barcelona's storefront premises from the 2022 Cens de locals.

A FIELD SURVEY, NOT A REGISTER, which is the shape this project most wants and
has only met once before (Montreal's `locaux-commerciaux`). It records what is
on the street rather than who registered a company, so there is no
registered-office problem to filter out and no holding companies to strip.

Reads what `fetch_sources.py` downloaded and NEVER fetches: a drift check has
to be deterministic and offline. Madrid, Mexico City and Guadalajara import
`requests` inside their step files; Barcelona does not add a fourth exception.

TWO FILTERS DO MOST OF THE WORK, and one of them most registers make you infer:

  * THE VACANCY FILTER. `Nom_Principal_Activitat` is `Actiu` on 58,908 rows and
    `Sense activitat Economica` on 7,180 - premises that are empty and for sale
    or rent, with `Nom_Sector_Activitat` reading *Locals buits en venda i
    lloguer*. Without this, 11% of the pins are shuttered shopfronts. Barcelona
    hands the vacancy signal over explicitly; almost nowhere else does.
  * THE STOREFRONT FILTER, via the taxonomy, which is where the accommodation
    carve-out lives - see `barcelona_activitat.py`.

WHAT THIS CITY DOES NOT NEED, and why that is worth stating. There is no
coordinate-repair step: `Latitud`/`Longitud` are populated and non-zero on
100% of rows, so Barcelona has none of Madrid's `'0.0'` defect and none of Los
Angeles' transposed-longitude problem. And there is no trade-name fallback,
because `Nom_Local` is a trade name and is populated on every row - the failure
that would have published ~4,000 individuals' names in Los Angeles cannot arise
here structurally, rather than being measured as absent.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module
from pipeline.barcelona.config import (
    ACTIVE_COLUMN,
    ACTIVE_VALUE,
    BARCELONA_BBOX,
    BARCELONA_DISTRICT_COUNT,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_RAW_CSV,
    CENSUS_YEAR,
    DATA_PROCESSED,
    FORBIDDEN_COLUMNS,
    PREMISES_ID_COLUMN,
    RAW_CLASSIFICATION_COLUMN,
    TAXONOMY_SYSTEM,
)

# When one premises carries activities in more than one bucket, the most
# specific wins. Madrid's order, for the same reason: a bar inside a shop is a
# bar to the person walking past it.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]


def main():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    if not BUSINESSES_RAW_CSV.exists():
        raise SystemExit(
            f"{BUSINESSES_RAW_CSV.name} is missing, and a step never fetches.\n"
            "  Run:  python pipeline/barcelona/fetch_sources.py")

    print(f"=== Step 2: Barcelona storefront premises ({CENSUS_YEAR} census) ===\n")

    header = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, nrows=1).columns
    leaked = [c for c in header if c.lower() in FORBIDDEN_COLUMNS]
    if leaked:
        raise SystemExit(
            f"the download now carries {leaked}. `USECOLS` is this city's "
            "privacy control and it is applied at download - re-read the "
            "privacy position before using this file.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False)
    print(f"rows in the census                         {len(df):>9,}")
    print(f"  distinct premises ({PREMISES_ID_COLUMN})            "
          f"{df[PREMISES_ID_COLUMN].nunique():>9,}")
    emit("census_rows", len(df))
    emit("distinct_premises_all", int(df[PREMISES_ID_COLUMN].nunique()))

    # --- the vacancy filter, which is mandatory ----------------------------
    vacant = ~df[ACTIVE_COLUMN].str.strip().eq(ACTIVE_VALUE)
    print(f"vacant premises dropped                    {int(vacant.sum()):>9,}"
          f"   ({100 * vacant.mean():.1f}% - empty units for sale or rent)")
    df = df[~vacant].copy()
    print(f"active ({ACTIVE_VALUE})                            {len(df):>9,}")
    emit("vacant_rows", int(vacant.sum()))
    emit("active_rows", len(df))

    # --- coordinates --------------------------------------------------------
    lat = pd.to_numeric(df["Latitud"], errors="coerce")
    lon = pd.to_numeric(df["Longitud"], errors="coerce")
    bad = lat.isna() | lon.isna() | (lat.fillna(0) == 0) | (lon.fillna(0) == 0)
    print(f"  unparseable or literal-zero coordinates  {int(bad.sum()):>9,}"
          f"   ({100 * bad.mean():.2f}%)")
    emit("zero_coordinate_rows", int(bad.sum()))
    df, lat, lon = df[~bad].copy(), lat[~bad], lon[~bad]

    b = BARCELONA_BBOX
    inside = (lat.between(b["lat_min"], b["lat_max"])
              & lon.between(b["lon_min"], b["lon_max"]))
    if (~inside).sum():
        print(f"  out-of-bounds coordinates dropped        "
              f"{int((~inside).sum()):>9,}")
    df, lat, lon = df[inside].copy(), lat[inside], lon[inside]
    df["_lat"], df["_lon"] = lat, lon
    print(f"with usable coordinates                    {len(df):>9,}")
    emit("usable_coordinate_rows", len(df))

    # --- storefront ---------------------------------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"in the three storefront buckets            {len(df):>9,}"
          f"   (dropped {before - len(df):,})")
    emit("storefront_rows", len(df))

    module = load_taxonomy_module(TAXONOMY_SYSTEM)
    df["bucket"] = [module.classify(r) for r in df.to_dict("records")]
    for bucket, n in df["bucket"].value_counts().items():
        print(f"    {bucket:<20} {n:>9,}")
        emit(f"bucket_{bucket.lower().replace(' ', '_')}", int(n))

    # --- one pin per premises ----------------------------------------------
    multi = df.groupby(PREMISES_ID_COLUMN)["bucket"].nunique()
    print(f"\npremises in >1 bucket                      "
          f"{int((multi > 1).sum()):>9,}")
    df["_rank"] = df["bucket"].map({b: i for i, b in enumerate(BUCKET_PRIORITY)})
    df = (df.sort_values([PREMISES_ID_COLUMN, "_rank"])
            .drop_duplicates(PREMISES_ID_COLUMN, keep="first"))
    print(f"one pin per premises                       {len(df):>9,}")
    emit("multi_bucket_premises", int((multi > 1).sum()))
    emit("businesses_clean_rows", len(df))

    # BARCELONA HAS TEN DISTRICTS. Raises rather than warns, on Madrid's
    # precedent: a count that moves means the survey's geography moved, and
    # every row count recorded here would stop meaning what it says.
    districts = df["Nom_Districte"].nunique()
    if districts != BARCELONA_DISTRICT_COUNT:
        raise SystemExit(
            f"{districts} districts, expected {BARCELONA_DISTRICT_COUNT}. "
            "Either the census's scope changed or a filter above is dropping a "
            "district - find out which before mapping this.")
    print(f"  across all {districts} districts")

    out = pd.DataFrame({
        "business_name": df["Nom_Local"].values,
        "latitude": df["_lat"].values,
        "longitude": df["_lon"].values,
        RAW_CLASSIFICATION_COLUMN: df[RAW_CLASSIFICATION_COLUMN].values,
        "Nom_Grup_Activitat": df["Nom_Grup_Activitat"].values,
        "Nom_Sector_Activitat": df["Nom_Sector_Activitat"].values,
        "bucket": df["bucket"].values,
        "districte": df["Nom_Districte"].str.strip().values,
    })

    # Nom_Local is the shop sign. Asserted rather than assumed - a fallback to
    # a person's name is what published ~4,000 of them in Los Angeles, and the
    # claim that this city cannot do that is only worth making if it is checked.
    blank = out["business_name"].isna() | out["business_name"].str.strip().eq("")
    if blank.any():
        raise SystemExit(
            f"{int(blank.sum())} kept premises have no Nom_Local. There is no "
            "name to show and no fallback is acceptable.")
    print("  every kept premises has a Nom_Local (shop sign)")

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\nWrote {len(out):,} premises to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
