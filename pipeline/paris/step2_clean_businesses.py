"""Paris step 2: SIRENE -> the storefronts inside the commune, with coordinates.

    python pipeline/paris/step2_clean_businesses.py

Reads the cache only; `fetch_sources.py` downloads. The two parquets are 2,210
MB and 811 MB, so every read here is ROW GROUP AT A TIME with the Paris filter
applied before anything is accumulated - 44,064,115 rows never exist in memory.

THE COORDINATE LEG IS A JOIN, NOT A GEOCODE. INSEE publishes a separate
geolocation file keyed on the same `siret`, so this city has no geocoding step,
no API key and no rate limit - the only built city of which that is true.

FOUR TRAPS, ALL MEASURED, ALL SILENT IF MISSED:

  * **ACTIVE IS THE LETTER `A`, NOT THE LABEL `Actif`.** Filtering on "Actif"
    returns ZERO rows for all six French cities. Paris runs first as the
    control precisely so a known-good number fails loudly.
  * **THE CRS IS PER ROW.** The geolocation file carries an `epsg` column
    holding 2154 on 99.3% and 2975/5490/2972 for the DOM. Hard-coding 2154 and
    pointing this at Fort-de-France would put every pin in the sea WITHOUT
    ERRORING, so the column is read and anything not metropolitan is dropped.
  * **`qualite_xy` CLASS 33 IS COMMUNE-CENTROID GRADE.** Those rows are not at
    a street address and must not be drawn as though they are. INSEE reports
    its own confidence; do not average over it.
  * **NAF rev. 2, NOT NAF 2025.** Both columns exist. See france.py.
"""
import sys
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.paris import config
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module

NAF = load_taxonomy_module(config.TAXONOMY_SYSTEM)

ADDRESS_COLUMNS = ("numeroVoieEtablissement", "typeVoieEtablissement",
                   "libelleVoieEtablissement", "codePostalEtablissement")

SIRENE_COLUMNS = [
    config.JOIN_KEY, config.COMMUNE_COLUMN, config.STATE_COLUMN,
    config.DIFFUSION_COLUMN, config.NAF_COLUMN, config.EMPLOYEE_BAND_COLUMN,
    config.USUAL_NAME_COLUMN, config.ENSEIGNE_COLUMNS[0], *ADDRESS_COLUMNS,
]

GEO_COLUMNS = [config.JOIN_KEY, config.GEO_LAT_COLUMN, config.GEO_LON_COLUMN,
               config.GEO_EPSG_COLUMN, config.GEO_QUALITY_COLUMN]

CENTROID_QUALITY = "33"


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\n"
                 f"Run: python pipeline/paris/fetch_sources.py")
    return path


def read_paris_rows():
    """Every ACTIVE Paris establishment, streamed a row group at a time."""
    pf = pq.ParquetFile(need(config.SIRENE_PARQUET, "the SIRENE parquet"))
    have = set(pf.schema_arrow.names)
    cols = [c for c in SIRENE_COLUMNS if c in have]
    absent = [c for c in SIRENE_COLUMNS if c not in have]
    if absent:
        sys.exit(f"SIRENE is missing expected column(s) {absent} - the monthly "
                 f"release changed shape. Do NOT proceed on the remainder.")

    frames = []
    for i in range(pf.num_row_groups):
        df = pf.read_row_group(i, columns=cols).to_pandas()
        df = df[df[config.COMMUNE_COLUMN].astype(str)
                .str.startswith(config.COMMUNE_PREFIXES)]
        if len(df):
            frames.append(df)
        if (i + 1) % 80 == 0 or i + 1 == pf.num_row_groups:
            print(f"    row group {i + 1}/{pf.num_row_groups}", flush=True)
    out = pd.concat(frames, ignore_index=True)
    return out, pf.metadata.num_rows


def read_geoloc(sirets):
    """The geolocation rows for a known set of sirets."""
    pf = pq.ParquetFile(need(config.GEOLOC_PARQUET, "the geolocation parquet"))
    have = set(pf.schema_arrow.names)
    absent = [c for c in GEO_COLUMNS if c not in have]
    if absent:
        sys.exit(f"the geolocation file is missing {absent}")
    frames = []
    for i in range(pf.num_row_groups):
        df = pf.read_row_group(i, columns=GEO_COLUMNS).to_pandas()
        df = df[df[config.JOIN_KEY].astype(str).isin(sirets)]
        if len(df):
            frames.append(df)
        if (i + 1) % 60 == 0 or i + 1 == pf.num_row_groups:
            print(f"    row group {i + 1}/{pf.num_row_groups}", flush=True)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=GEO_COLUMNS)


def _text(series):
    """A column as plain text, with every flavour of blank collapsed to "".

    ⚠ `.fillna("")` BEFORE `.astype(str)`, and it is load-bearing. pandas 3.0
    backs string columns with pyarrow, so `.astype(str)` on a null yields <NA>
    rather than the string "nan" - and <NA> then passes an `!= ""` test, so a
    row with no name counts as named and writes an EMPTY field to the CSV.
    That is exactly what happened: step 2 reported "premises name present on
    97,445 rows (100.0%)" against a brief that measures 42.9%, while the first
    CSV row had a blank name. A 100% fill rate was the tell.
    """
    return series.fillna("").astype(str).str.strip()


def address_of(df):
    """A displayable street address, INSEE's own components joined."""
    parts = []
    for col in ADDRESS_COLUMNS:
        s = _text(df[col])
        parts.append(s.where(~s.isin(["nan", "None", "<NA>", ""]), ""))
    joined = (parts[0] + " " + parts[1] + " " + parts[2]).str.strip()
    joined = joined.str.replace(r"\s+", " ", regex=True)
    return joined.where(joined != "", "")


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    print("SIRENE, streaming row groups:")
    df, total_rows = read_paris_rows()
    print(f"  {total_rows:,} rows in the file")
    print(f"  {len(df):,} in Paris (codeCommune starts "
          f"{'/'.join(config.COMMUNE_PREFIXES)})")

    # ACTIVE. The letter, not the label - see the module docstring.
    df = df[df[config.STATE_COLUMN].astype(str) == config.STATE_ACTIVE_VALUE]
    print(f"  {len(df):,} active ({config.STATE_COLUMN} == "
          f"{config.STATE_ACTIVE_VALUE!r})")
    if not len(df):
        sys.exit("zero active rows. This is the 'Actif' bug's signature: the "
                 "state filter matched nothing. Check STATE_ACTIVE_VALUE.")

    # France masks non-diffusible records at source: the name, the address AND
    # the geolocation. Dropping them is not a privacy choice this project made
    # - the rows arrive already hollowed out.
    before = len(df)
    df = df[df[config.DIFFUSION_COLUMN].astype(str)
            == config.DIFFUSION_PUBLIC_VALUE]
    print(f"  {len(df):,} publicly diffusible "
          f"({before - len(df):,} masked at source, "
          f"{(before - len(df)) / before * 100:.1f}%)")

    # --- taxonomy ----------------------------------------------------------
    df["naf_code"] = df[config.NAF_COLUMN].map(NAF.normalise_code)
    df[config.RAW_CLASSIFICATION_COLUMN] = df["naf_code"].map(NAF.label_for)

    in_divisions = df["naf_code"].str[:2].isin(("47", "56", "96"))
    print(f"\n  {int(in_divisions.sum()):,} in NAF divisions 47/56/96 "
          f"(before the non-premises exclusions)")

    # What the national module excludes structurally, itemised here because the
    # shares are a fact about THIS city and PLAN.md records two as unmeasured.
    div = df[in_divisions]
    excluded = div[div["naf_code"].isin(NAF.NOT_PREMISES)]
    print(f"  {len(excluded):,} structurally excluded "
          f"({len(excluded) / max(len(div), 1) * 100:.1f}%):")
    for code, n in excluded["naf_code"].value_counts().items():
        print(f"      {code}  {n:>6,}  {NAF.NOT_PREMISES[code]}")

    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")

    # The catch-alls the national module deliberately does NOT decide. The
    # per-city verdict is config.CATCH_ALL_EXCLUDE, taken from these numbers
    # and from NAF's own class labels - see that constant for the reasoning.
    print("\n  catch-all codes (per-city call, config.CATCH_ALL_EXCLUDE):")
    for code in sorted(NAF.CATCH_ALL_CODES):
        n = int((df["naf_code"] == code).sum())
        mark = "DROP" if code in config.CATCH_ALL_EXCLUDE else "keep"
        print(f"      {code}  {n:>6,}  ({n / max(len(df), 1) * 100:4.1f}%)  "
              f"{mark}  {NAF.label_for(code)[:40]}")

    before = len(df)
    df = df[~df["naf_code"].isin(config.CATCH_ALL_EXCLUDE)]
    print(f"  {len(df):,} after the catch-all exclusion "
          f"({before - len(df):,} dropped)")

    # --- coordinates: a JOIN -----------------------------------------------
    df[config.JOIN_KEY] = df[config.JOIN_KEY].astype(str)
    sirets = set(df[config.JOIN_KEY])
    print(f"\ngeolocation file, streaming row groups for {len(sirets):,} sirets:")
    geo = read_geoloc(sirets)
    geo[config.JOIN_KEY] = geo[config.JOIN_KEY].astype(str)
    geo = geo.drop_duplicates(subset=[config.JOIN_KEY])
    print(f"  {len(geo):,} matched ({len(geo) / max(len(df), 1) * 100:.2f}% "
          f"coverage)")

    # THE CRS IS PER ROW.
    epsg = geo[config.GEO_EPSG_COLUMN].astype(str).str.replace(r"\.0$", "",
                                                               regex=True)
    counts = epsg.value_counts().to_dict()
    print(f"  epsg values present: {counts}")
    keep_epsg = epsg == str(config.METROPOLITAN_EPSG)
    if not keep_epsg.all():
        print(f"  dropping {int((~keep_epsg).sum()):,} row(s) outside "
              f"EPSG:{config.METROPOLITAN_EPSG} - a DOM grid in a Paris build "
              f"is a join error, not a coordinate")
    geo = geo[keep_epsg]

    before = len(geo)
    geo = geo[geo[config.GEO_QUALITY_COLUMN].astype(str)
              .str.replace(r"\.0$", "", regex=True) != CENTROID_QUALITY]
    print(f"  {len(geo):,} after dropping qualite_xy {CENTROID_QUALITY} "
          f"(commune centroid): {before - len(geo):,} removed")

    df = df.merge(geo, on=config.JOIN_KEY, how="inner")
    print(f"  {len(df):,} storefronts with a usable street-level coordinate")

    df["latitude"] = pd.to_numeric(df[config.GEO_LAT_COLUMN], errors="coerce")
    df["longitude"] = pd.to_numeric(df[config.GEO_LON_COLUMN], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["latitude", "longitude"])
    b = config.PARIS_BBOX
    df = df[df["latitude"].between(b["lat_min"], b["lat_max"])
            & df["longitude"].between(b["lon_min"], b["lon_max"])]
    if len(df) != before:
        print(f"  {before - len(df):,} dropped on the sanity bounding box")

    # --- the pin's label: the MILAN HYBRID ---------------------------------
    #
    # Premises name where the register has one, the address otherwise. The
    # legal-name fallback is NOT built: it would recover ~9 in 10 of the
    # unnamed, and publish on the order of ten thousand individuals' names
    # behind a guard whose failure mode is publishing people. The hybrid needs
    # no guard and carries zero residual exposure.
    blank = ["nan", "None", "<NA>", ""]
    enseigne = _text(df[config.ENSEIGNE_COLUMNS[0]])
    usual = _text(df[config.USUAL_NAME_COLUMN])
    enseigne = enseigne.where(~enseigne.isin(blank), "")
    usual = usual.where(~usual.isin(blank), "")
    addr = address_of(df)

    df["business_name"] = enseigne.where(enseigne != "", usual)
    named = (df["business_name"] != "").sum()
    df["name_is_address"] = df["business_name"] == ""
    df["business_name"] = df["business_name"].where(
        df["business_name"] != "", addr)
    still_blank = int((df["business_name"].str.strip() == "").sum())
    print(f"\n  premises name present on {named:,} rows "
          f"({named / max(len(df), 1) * 100:.1f}%); the rest show the address")
    if still_blank:
        print(f"  {still_blank:,} row(s) have neither a name nor an address "
              f"and are dropped - a pin with no label is not a storefront")
        df = df[df["business_name"].str.strip() != ""]

    # --- THE OPEN QUESTION, measured rather than assumed -------------------
    #
    # ⚠ NO EMPLOYEE FILTER IS APPLIED HERE, and that is unresolved rather than
    # decided. The brief records 148,633 -> 50,156 "after the employee filter",
    # and PLAN.md records 50,156 as validated against OSM's 54,198 (92.5%) -
    # the comparison that turned France from a rejection into a build. But
    # 50,156 IS NOT REACHABLE from trancheEffectifsEtablissement: measured
    # 2026-09-23 over the 149,166 bucket rows, NN (non determine) is 115,248 of
    # them (77.3%), so every banded row together is 33,918 and the largest
    # possible cut falls 16,000 short.
    #
    # So this block prints the discriminator instead of guessing a predicate
    # that happens to hit the number. If NN rows are markedly less likely to
    # carry a premises name, they are mostly home registrations and belong out;
    # if they look like ordinary named shops, the brief's figure is the thing
    # that is wrong. Either way the call is the owner's and is recorded in
    # DECISIONS.md before a filter lands here.
    band = _text(df[config.EMPLOYEE_BAND_COLUMN])
    is_nn = band.isin(["NN", "", "nan", "<NA>"])
    print("\n  employee band vs the premises-name rate (the discriminator):")
    for label, mask in (("NN / unrecorded", is_nn), ("has a band", ~is_nn)):
        sub = df[mask]
        if not len(sub):
            continue
        named_share = (~sub["name_is_address"]).mean() * 100
        catchall = sub["naf_code"].isin(NAF.CATCH_ALL_CODES).mean() * 100
        print(f"    {label:16s} {len(sub):>7,} rows | "
              f"named {named_share:5.1f}% | catch-all {catchall:5.1f}%")

    # NO LEGAL-NAME COLUMN IS EVER LOADED. Asserted rather than trusted: this
    # is the structural claim that makes Los Angeles' failure mode impossible
    # here, and an assertion is what makes it checkable.
    forbidden = [c for c in df.columns
                 if c in ("nomUniteLegale", "prenomUsuelUniteLegale",
                          "denominationUniteLegale", "nomUsageUniteLegale")]
    assert not forbidden, f"a personal-name column reached step 2: {forbidden}"

    out = df[["siret", "business_name", "name_is_address", "latitude",
              "longitude", config.RAW_CLASSIFICATION_COLUMN, "naf_code"]]
    out = out.drop_duplicates(subset=["siret"])
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
