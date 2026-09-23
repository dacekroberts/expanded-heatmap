"""SIRENE -> one French city's storefronts. Shared by every French city.

WHY THIS IS SHARED RATHER THAN COPIED. SIRENE is ONE national register, so a
per-city step 2 is the same 250 lines five times over - the same `"A"`-not-
`"Actif"` trap, the same diffusion mask, the same per-row `epsg`, the same
`qualite_xy` class, the same Milan-hybrid naming. `CLAUDE.md` already makes
this an invariant for rendering ("City step3_map.py files are thin and must not
fork it"), and the reasoning is identical here: five copies must stay in
agreement, and nothing makes them.

Introduced 2026-09-23 while building the SECOND French city, deliberately
before a third could set the per-city pattern - the same timing argument that
moved the parquets into one national cache.

⚠ **DELIBERATELY NOT IN `france.py`.** That module is imported by every French
city's `config.py`, which `app/pages/*.py` imports in turn, so it must stay
importable under the lean deploy venv. This one imports pandas and pyarrow and
is imported only by step files, which never run on the deployed app.

WHAT STAYS PER CITY, and why each is not a candidate for sharing:

  * `COMMUNE_PREFIXES` - the one field that differs by design.
  * the sanity bounding box - each city's own measured extent.
  * `CATCH_ALL_EXCLUDE` - a catch-all's SHARE is a fact about a city, which is
    why `france_naf.py` declines to decide it and `CLAUDE.md` puts the verdict
    in the city's config.
"""
import sys

import pandas as pd
import pyarrow.parquet as pq

from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module

ADDRESS_COLUMNS = ("numeroVoieEtablissement", "typeVoieEtablissement",
                   "libelleVoieEtablissement", "codePostalEtablissement")

# INSEE's own positional quality code. 33 is commune-centroid grade: those rows
# are not at a street address and must not be drawn as though they are.
CENTROID_QUALITY = "33"

BUCKET_DIVISIONS = ("47", "56", "96")


def _text(series):
    """A column as plain text, with every flavour of blank collapsed to "".

    ⚠ `.fillna("")` BEFORE `.astype(str)`, and it is load-bearing. pandas 3.0
    backs string columns with pyarrow, so `.astype(str)` on a null yields <NA>
    rather than the string "nan" - and <NA> then passes an `!= ""` test, so a
    row with no name counts as named and writes an EMPTY field to the CSV.
    That is exactly what happened on Paris: step 2 reported "premises name
    present on 97,445 rows (100.0%)" against a register measured at 38%, while
    the first CSV row had a blank name. A 100% fill rate was the tell.
    """
    return series.fillna("").astype(str).str.strip()


def _address_of(df):
    """A displayable street address, INSEE's own components joined."""
    parts = []
    for col in ADDRESS_COLUMNS:
        s = _text(df[col])
        parts.append(s.where(~s.isin(["nan", "None", "<NA>", ""]), ""))
    joined = (parts[0] + " " + parts[1] + " " + parts[2]).str.strip()
    joined = joined.str.replace(r"\s+", " ", regex=True)
    return joined.where(joined != "", "")


def _sirene_columns(cfg):
    return [
        cfg.JOIN_KEY, cfg.COMMUNE_COLUMN, cfg.STATE_COLUMN,
        cfg.DIFFUSION_COLUMN, cfg.NAF_COLUMN, cfg.EMPLOYEE_BAND_COLUMN,
        cfg.USUAL_NAME_COLUMN, cfg.ENSEIGNE_COLUMNS[0], *ADDRESS_COLUMNS,
    ]


def _geo_columns(cfg):
    return [cfg.JOIN_KEY, cfg.GEO_LAT_COLUMN, cfg.GEO_LON_COLUMN,
            cfg.GEO_EPSG_COLUMN, cfg.GEO_QUALITY_COLUMN]


def _need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun the city's fetch_sources.py")
    return path


def _read_city_rows(cfg):
    """Every establishment in this city, streamed a row group at a time.

    44,064,115 rows never exist in memory: the commune filter is applied inside
    the loop, before anything is accumulated.
    """
    pf = pq.ParquetFile(_need(cfg.SIRENE_PARQUET, "the SIRENE parquet"))
    have = set(pf.schema_arrow.names)
    want = _sirene_columns(cfg)
    absent = [c for c in want if c not in have]
    if absent:
        sys.exit(f"SIRENE is missing expected column(s) {absent} - the monthly "
                 f"release changed shape. Do NOT proceed on the remainder.")
    frames = []
    for i in range(pf.num_row_groups):
        df = pf.read_row_group(i, columns=want).to_pandas()
        df = df[df[cfg.COMMUNE_COLUMN].astype(str)
                .str.startswith(cfg.COMMUNE_PREFIXES)]
        if len(df):
            frames.append(df)
        if (i + 1) % 80 == 0 or i + 1 == pf.num_row_groups:
            print(f"    row group {i + 1}/{pf.num_row_groups}", flush=True)
    return pd.concat(frames, ignore_index=True), pf.metadata.num_rows


def _read_geoloc(cfg, sirets):
    pf = pq.ParquetFile(_need(cfg.GEOLOC_PARQUET, "the geolocation parquet"))
    have = set(pf.schema_arrow.names)
    want = _geo_columns(cfg)
    absent = [c for c in want if c not in have]
    if absent:
        sys.exit(f"the geolocation file is missing {absent}")
    frames = []
    for i in range(pf.num_row_groups):
        df = pf.read_row_group(i, columns=want).to_pandas()
        df = df[df[cfg.JOIN_KEY].astype(str).isin(sirets)]
        if len(df):
            frames.append(df)
        if (i + 1) % 60 == 0 or i + 1 == pf.num_row_groups:
            print(f"    row group {i + 1}/{pf.num_row_groups}", flush=True)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=want)


def build_storefronts(cfg, city_name, bbox):
    """The city's storefronts, cleaned, geolocated and labelled.

    Prints a count at every filter, which is how a scope mistake surfaces here
    and what becomes the baseline in DECISIONS.md.
    """
    NAF = load_taxonomy_module(cfg.TAXONOMY_SYSTEM)

    print("SIRENE, streaming row groups:")
    df, total_rows = _read_city_rows(cfg)
    print(f"  {total_rows:,} rows in the file")
    print(f"  {len(df):,} in {city_name} (codeCommune starts "
          f"{'/'.join(cfg.COMMUNE_PREFIXES)})")

    # ACTIVE IS THE LETTER, NOT THE LABEL. Filtering on "Actif" returns zero
    # rows for all six French cities; Paris runs first as the control so a
    # known-good number fails loudly.
    df = df[df[cfg.STATE_COLUMN].astype(str) == cfg.STATE_ACTIVE_VALUE]
    print(f"  {len(df):,} active ({cfg.STATE_COLUMN} == "
          f"{cfg.STATE_ACTIVE_VALUE!r})")
    if not len(df):
        sys.exit("zero active rows. This is the 'Actif' bug's signature: the "
                 "state filter matched nothing. Check STATE_ACTIVE_VALUE.")

    # France masks non-diffusible records at source - the name, the address AND
    # the geolocation - so dropping them is not a privacy choice this project
    # made; the rows arrive already hollowed out.
    before = len(df)
    df = df[df[cfg.DIFFUSION_COLUMN].astype(str) == cfg.DIFFUSION_PUBLIC_VALUE]
    print(f"  {len(df):,} publicly diffusible "
          f"({before - len(df):,} masked at source, "
          f"{(before - len(df)) / before * 100:.1f}%)")

    # --- taxonomy ----------------------------------------------------------
    df["naf_code"] = df[cfg.NAF_COLUMN].map(NAF.normalise_code)
    df[cfg.RAW_CLASSIFICATION_COLUMN] = df["naf_code"].map(NAF.label_for)

    in_divisions = df["naf_code"].str[:2].isin(BUCKET_DIVISIONS)
    print(f"\n  {int(in_divisions.sum()):,} in NAF divisions "
          f"{'/'.join(BUCKET_DIVISIONS)} (before the non-premises exclusions)")

    div = df[in_divisions]
    excluded = div[div["naf_code"].isin(NAF.NOT_PREMISES)]
    print(f"  {len(excluded):,} structurally excluded "
          f"({len(excluded) / max(len(div), 1) * 100:.1f}%):")
    for code, n in excluded["naf_code"].value_counts().items():
        print(f"      {code}  {n:>6,}  {NAF.NOT_PREMISES[code]}")

    df = filter_to_storefront(df, cfg.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")

    # The catch-alls the national module deliberately does NOT decide; the
    # per-city verdict is cfg.CATCH_ALL_EXCLUDE.
    print("\n  catch-all codes (per-city call, config.CATCH_ALL_EXCLUDE):")
    for code in sorted(NAF.CATCH_ALL_CODES):
        n = int((df["naf_code"] == code).sum())
        mark = "DROP" if code in cfg.CATCH_ALL_EXCLUDE else "keep"
        print(f"      {code}  {n:>6,}  ({n / max(len(df), 1) * 100:4.1f}%)  "
              f"{mark}  {NAF.label_for(code)[:40]}")

    before = len(df)
    df = df[~df["naf_code"].isin(cfg.CATCH_ALL_EXCLUDE)]
    print(f"  {len(df):,} after the catch-all exclusion "
          f"({before - len(df):,} dropped)")

    # --- coordinates: a JOIN, not a geocode --------------------------------
    df[cfg.JOIN_KEY] = df[cfg.JOIN_KEY].astype(str)
    sirets = set(df[cfg.JOIN_KEY])
    print(f"\ngeolocation file, streaming row groups for {len(sirets):,} sirets:")
    geo = _read_geoloc(cfg, sirets)
    geo[cfg.JOIN_KEY] = geo[cfg.JOIN_KEY].astype(str)
    geo = geo.drop_duplicates(subset=[cfg.JOIN_KEY])
    print(f"  {len(geo):,} matched ({len(geo) / max(len(df), 1) * 100:.2f}% "
          f"coverage)")

    # THE CRS IS PER ROW. Hard-coding 2154 works in every metropolitan city and
    # would put every pin in the sea in Fort-de-France, without erroring.
    epsg = geo[cfg.GEO_EPSG_COLUMN].astype(str).str.replace(r"\.0$", "",
                                                            regex=True)
    print(f"  epsg values present: {epsg.value_counts().to_dict()}")
    keep_epsg = epsg == str(cfg.METROPOLITAN_EPSG)
    if not keep_epsg.all():
        print(f"  dropping {int((~keep_epsg).sum()):,} row(s) outside "
              f"EPSG:{cfg.METROPOLITAN_EPSG} - a DOM grid in a {city_name} "
              f"build is a join error, not a coordinate")
    geo = geo[keep_epsg]

    before = len(geo)
    geo = geo[geo[cfg.GEO_QUALITY_COLUMN].astype(str)
              .str.replace(r"\.0$", "", regex=True) != CENTROID_QUALITY]
    print(f"  {len(geo):,} after dropping qualite_xy {CENTROID_QUALITY} "
          f"(commune centroid): {before - len(geo):,} removed")

    df = df.merge(geo, on=cfg.JOIN_KEY, how="inner")
    print(f"  {len(df):,} storefronts with a usable street-level coordinate")

    df["latitude"] = pd.to_numeric(df[cfg.GEO_LAT_COLUMN], errors="coerce")
    df["longitude"] = pd.to_numeric(df[cfg.GEO_LON_COLUMN], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["latitude", "longitude"])
    df = df[df["latitude"].between(bbox["lat_min"], bbox["lat_max"])
            & df["longitude"].between(bbox["lon_min"], bbox["lon_max"])]
    if len(df) != before:
        print(f"  {before - len(df):,} dropped on the sanity bounding box")

    # --- the pin's label: the MILAN HYBRID ---------------------------------
    #
    # Premises name where the register has one, the address otherwise. The
    # legal-name fallback is NOT built: it would recover ~9 in 10 of the
    # unnamed and publish thousands of individuals' names behind a guard whose
    # failure mode is publishing people. The hybrid needs no guard.
    blank = ["nan", "None", "<NA>", ""]
    enseigne = _text(df[cfg.ENSEIGNE_COLUMNS[0]])
    usual = _text(df[cfg.USUAL_NAME_COLUMN])
    enseigne = enseigne.where(~enseigne.isin(blank), "")
    usual = usual.where(~usual.isin(blank), "")
    addr = _address_of(df)

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

    # ⚠ NO EMPLOYEE FILTER, and that is unresolved rather than decided. Paris's
    # brief recorded 148,633 -> 50,156 "after the employee filter" and PLAN.md
    # called the resulting 92.5% OSM match what turned France into a build -
    # but 50,156 is NOT reachable from trancheEffectifsEtablissement, where NN
    # is 77.3% of Paris's bucket rows. So this prints the discriminator rather
    # than guessing a predicate that happens to hit a number.
    band = _text(df[cfg.EMPLOYEE_BAND_COLUMN])
    is_nn = band.isin(["NN", "", "nan", "<NA>"])
    print("\n  employee band vs the premises-name rate (the discriminator):")
    for label, mask in (("NN / unrecorded", is_nn), ("has a band", ~is_nn)):
        sub = df[mask]
        if not len(sub):
            continue
        print(f"    {label:16s} {len(sub):>7,} rows | "
              f"named {(~sub['name_is_address']).mean() * 100:5.1f}% | "
              f"catch-all "
              f"{sub['naf_code'].isin(NAF.CATCH_ALL_CODES).mean() * 100:5.1f}%")

    # NO LEGAL-NAME COLUMN IS EVER LOADED. Asserted rather than trusted: this
    # is the structural claim that makes Los Angeles' failure mode impossible
    # here rather than merely unlikely.
    forbidden = [c for c in df.columns
                 if c in ("nomUniteLegale", "prenomUsuelUniteLegale",
                          "denominationUniteLegale", "nomUsageUniteLegale")]
    assert not forbidden, f"a personal-name column reached step 2: {forbidden}"

    out = df[["siret", "business_name", "name_is_address", "latitude",
              "longitude", cfg.RAW_CLASSIFICATION_COLUMN, "naf_code"]]
    return out.drop_duplicates(subset=["siret"])
