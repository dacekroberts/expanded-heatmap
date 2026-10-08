"""Step 2 - Mexico City storefronts from INEGI's DENUE.

DENUE is a national ESTABLISHMENT register published per entidad federativa, so
the in-city question is answered by which file is downloaded (09 = Ciudad de
Mexico) rather than by a city-name field. That is why this city has no
CITY_KEEP: there is no city column to mis-read, which is the trap that made Los
Angeles' postal community names keep about half its rows.

Privacy, and it is the strongest position of any city here. INEGI already did
the work upstream:
  * `nom_estab` is the EXTERIOR SIGN - INEGI's own dictionary calls it the name
    "visible y escrito en rotulos, fachadas o anuncios luminosos". It is
    populated on 99.95% of rows.
  * `raz_social`, the legal entity name, is OMITTED ENTIRELY when the owner is
    a persona fisica, explicitly "para proteger la confidencialidad de la
    informacion".
So the Los Angeles failure - 68% of rows missing a trade name, the pipeline
falling back to the registrant's own name, ~4,000 individuals published at
their premises - CANNOT happen here: there is no personal name to fall back to,
because the publisher withheld it rather than substituting it. This step
ASSERTS the forbidden columns never arrive, so that claim is structural rather
than a measurement that might drift.
"""

import io
import re
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.counts import pct
from pipeline.taxonomies import load_taxonomy_module
from pipeline.mexico_city.step1_stations import load_scope
from pipeline.mexico_city.config import (
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    DENUE_ACTIVITY_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_MEMBER,
    DENUE_MUNICIPIO_CODE_COLUMN,
    DENUE_MUNICIPIO_COLUMN,
    DENUE_NAME_COLUMN,
    DENUE_REGIONAL_MEMBERS,
    DENUE_REGIONAL_ZIPS,
    DENUE_STATE_CODE,
    DENUE_STATE_COLUMN,
    DENUE_ZIP,
    FORBIDDEN_COLUMNS,
    MEXICO_CITY_BBOX,
    MUNICIPIOS,
    NAME,
    PREMISES_TYPE_COLUMN,
    PREMISES_TYPE_KEEP,
    REGIONAL,
    REGIONAL_STATE_CODE,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
)

# Only these columns are read out of DENUE's 42. Everything else - and in
# particular every column in FORBIDDEN_COLUMNS - is never loaded, so it cannot
# be used by accident downstream.
USECOLS = (
    "id",
    DENUE_NAME_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_ACTIVITY_COLUMN,
    PREMISES_TYPE_COLUMN,
    DENUE_STATE_COLUMN,
    DENUE_MUNICIPIO_COLUMN,
    # MEASURED AND PRINTED, NEVER WRITTEN OUT. `numero_int` is DENUE's
    # structured interior/unit number - better evidence of a dwelling than a
    # regex over free text, which is what the multi-source-city skill asks for.
    # It is loaded so the rate can be reported, and deliberately excluded from
    # businesses_clean.csv: publishing a unit number in order to check for unit
    # numbers would defeat the purpose. scripts/check_personal_exposure.py
    # therefore records this city's residence check as a GAP and points here.
    "numero_int",
    "latitud",
    "longitud",
)

# Entidad 15 also needs the municipio code: the regional scope is cut on it
# (Monterrey's pattern), never on the name.
USECOLS_REGIONAL = USECOLS + (DENUE_MUNICIPIO_CODE_COLUMN,)

# Contact details that could sit inside a SIGN NAME, which is published.
# Monterrey's patterns (pipeline/monterrey/step2_clean_businesses.py). Only
# COUNTS are printed here, so a drift log never carries a sign name; the
# hits are read by hand before publishing and the verdict recorded.
EMAIL_LIKE = re.compile(r"[^\s@]+@[^\s@]+\.[^\s@]+")
PHONE_LIKE = re.compile(r"(?<!\d)\d{8,10}(?!\d)|(?<!\d)\d{2,3}[\s.-]\d{3,4}[\s.-]\d{4}(?!\d)")


def read_regional():
    """Mexico City (Regional): the four State of México municipios from
    DENUE entidad 15, which INEGI publishes in two ZIPs. Each member is named
    exactly (never the first .csv), the two parts must share no `id`, and
    every configured code must carry the configured name in DENUE's own
    `municipio` column, so a wrong code fails loudly. This step never
    fetches: fetch_sources.py --regional downloads both parts."""
    frames = []
    for path, member in zip(DENUE_REGIONAL_ZIPS, DENUE_REGIONAL_MEMBERS):
        if not path.exists():
            raise SystemExit(f"Missing {path.name}. Run "
                             "pipeline/mexico_city/fetch_sources.py --regional first.")
        zf = zipfile.ZipFile(path)
        if member not in zf.namelist():
            raise SystemExit(f"{member} not in {path.name}. Members: "
                             f"{zf.namelist()}. Never take the first .csv.")
        raw = zf.read(member).decode(SOURCE_ENCODING)
        header = pd.read_csv(io.StringIO(raw), nrows=0)
        present = [c for c in FORBIDDEN_COLUMNS if c in header.columns]
        part = pd.read_csv(io.StringIO(raw), usecols=list(USECOLS_REGIONAL), dtype=str)
        for c in FORBIDDEN_COLUMNS:
            assert c not in part.columns, f"{c} reached the DataFrame"
        print(f"  {path.name} ({path.stat().st_size:,} bytes): {len(part):,} "
              f"units; forbidden columns present but NOT loaded: {present}")
        frames.append(part)
        del raw
    shared = set(frames[0]["id"]) & set(frames[1]["id"])
    if shared:
        raise SystemExit(f"{len(shared):,} ids appear in both entidad 15 parts; "
                         "the parts were expected to be disjoint.")
    df = pd.concat(frames, ignore_index=True)
    print(f"DENUE state {REGIONAL_STATE_CODE}: {len(df):,} economic units "
          "(two parts, no shared id)")
    emit("denue_15_rows", len(df))
    ents = df[DENUE_STATE_COLUMN].value_counts()
    if len(ents) != 1 or ents.index[0] != REGIONAL_STATE_CODE:
        raise SystemExit(f"expected only cve_ent={REGIONAL_STATE_CODE}, got {dict(ents)}")

    code = df[DENUE_MUNICIPIO_CODE_COLUMN].str.zfill(3)
    names_by_code = (df.assign(_c=code).groupby("_c")[DENUE_MUNICIPIO_COLUMN]
                     .agg(lambda s: sorted(set(s))))
    for c, expected in MUNICIPIOS.items():
        seen = names_by_code.get(c)
        if seen != [expected]:
            raise SystemExit(
                f"cve_mun {c}: DENUE names it {seen}, config expects {expected!r}. "
                "The code is the join key; a mismatch means the code is wrong.")
    df = df[code.isin(MUNICIPIOS)].copy()
    df[DENUE_MUNICIPIO_CODE_COLUMN] = df[DENUE_MUNICIPIO_CODE_COLUMN].str.zfill(3)
    print(f"Four municipios (by INEGI code): {len(df):,} units")
    for m, n in df[DENUE_MUNICIPIO_COLUMN].value_counts().items():
        print(f"    {m:26s} {n:8,}")
    emit("in_scope_15_rows", len(df))
    return df


def require_denue():
    """The DENUE zip must already be here - this step does NOT download it.

    It used to, on a cache miss, which meant `drift_check.py` could pull 39 MB
    from INEGI on any checkout without `data/mexico_city/raw/`. See
    pipeline/mexico_city/fetch_sources.py.
    """
    if not DENUE_ZIP.exists():
        raise SystemExit(
            f"Missing {DENUE_ZIP.name}. "
            f"Run pipeline/mexico_city/fetch_sources.py first."
        )
    print(f"  {DENUE_ZIP.name} ({DENUE_ZIP.stat().st_size:,} bytes)")


def main():
    print(f"=== Step 2: {NAME} storefronts (INEGI DENUE) ===\n")
    tax = load_taxonomy_module(TAXONOMY_SYSTEM)

    require_denue()
    zf = zipfile.ZipFile(DENUE_ZIP)
    if DENUE_MEMBER not in zf.namelist():
        raise SystemExit(
            f"{DENUE_MEMBER} not in the ZIP. Members: {zf.namelist()}. Note "
            "the dictionary member is a plausible-looking near-miss - reading "
            "it returns 43 rows of column documentation, not data."
        )
    # LATIN-1. Declared in config, not sniffed: a UTF-8 decode raises here.
    raw = zf.read(DENUE_MEMBER).decode(SOURCE_ENCODING)

    header = pd.read_csv(io.StringIO(raw), nrows=0)
    # THE STRUCTURAL PRIVACY CLAIM. These columns exist in the file and are
    # deliberately not read; if a future DENUE edition renames one into our
    # USECOLS, this fails loudly rather than publishing a phone number.
    leaked = [c for c in FORBIDDEN_COLUMNS if c in USECOLS]
    assert not leaked, f"forbidden column in USECOLS: {leaked}"
    present = [c for c in FORBIDDEN_COLUMNS if c in header.columns]
    print(f"Forbidden columns present in the source but NOT loaded: {present}")

    df = pd.read_csv(io.StringIO(raw), usecols=list(USECOLS), dtype=str)
    total = len(df)
    print(f"\nDENUE state {DENUE_STATE_CODE}: {total:,} economic units")
    emit("denue_rows", total)
    for c in FORBIDDEN_COLUMNS:
        assert c not in df.columns, f"{c} reached the DataFrame"

    # --- state sanity: the file should be one state ------------------------
    ents = df[DENUE_STATE_COLUMN].value_counts()
    if len(ents) != 1 or ents.index[0] != DENUE_STATE_CODE:
        raise SystemExit(f"expected only cve_ent={DENUE_STATE_CODE}, got {dict(ents)}")
    print(f"  all rows cve_ent={DENUE_STATE_CODE}; "
          f"{df[DENUE_MUNICIPIO_COLUMN].nunique()} alcaldias")
    del raw

    # --- Mexico City (Regional): entidad 15's four municipios ---------------
    # One register over two entidades, so no cross-source dedup is needed:
    # DENUE's `id` is national, and the two sets are asserted disjoint.
    if REGIONAL:
        print()
        df15 = read_regional()
        shared = set(df["id"]) & set(df15["id"])
        if shared:
            raise SystemExit(f"{len(shared):,} ids appear in both entidades 09 and 15.")
        df = pd.concat([df, df15], ignore_index=True)
        print(f"{NAME}: {len(df):,} economic units in scope")

    # --- FIJO ONLY ---------------------------------------------------------
    before = len(df)
    if REGIONAL:
        fijo = df[PREMISES_TYPE_COLUMN] == PREMISES_TYPE_KEEP
        for m, g in fijo.groupby(df[DENUE_MUNICIPIO_COLUMN].where(
                df[DENUE_STATE_COLUMN] == REGIONAL_STATE_CODE, "(Ciudad de México)")):
            print(f"    {m:26s} Fijo {pct(int(g.sum()), len(g), 'units')}")
    df = df[df[PREMISES_TYPE_COLUMN] == PREMISES_TYPE_KEEP].copy()
    print(f"\n{PREMISES_TYPE_COLUMN}={PREMISES_TYPE_KEEP} only: "
          f"{pct(len(df), before, 'economic units')} kept "
          f"({before - len(df):,} Semifijo dropped)")
    emit("fijo_rows", len(df))

    # --- classify ----------------------------------------------------------
    df = df.rename(columns={
        DENUE_NAME_COLUMN: "business_name",
        DENUE_ACTIVITY_COLUMN: tax.VALUE_COLUMN,
        DENUE_CODE_COLUMN: "scian",
        "latitud": "latitude",
        "longitud": "longitude",
    })
    df["bucket"] = df.apply(lambda r: tax.classify(r), axis=1)
    before = len(df)
    df = df[df["bucket"].notna()].copy()
    print(f"\nStorefront categories: {pct(len(df), before, 'fixed premises')}")
    for b, n in df["bucket"].value_counts().items():
        print(f"    {b:20s} {n:8,}  {pct(n, len(df), 'storefronts')}")
        emit(f"bucket_{b.lower().replace(' ', '_')}", n)
    emit("storefront_rows", len(df))

    # --- names -------------------------------------------------------------
    blank = int(df["business_name"].isna().sum() + (df["business_name"] == "").sum())
    print(f"\nBlank trade names: {pct(blank, len(df), 'storefronts')} "
          "(no fallback to a legal or personal name exists - see the docstring)")
    names = df["business_name"].fillna("")
    for label, rx in (("e-mail-shaped", EMAIL_LIKE), ("phone-length digit run", PHONE_LIKE)):
        print(f"Sign names with an {label}: {int(names.str.contains(rx).sum()):,}"
              "  (counts only; read by hand before publishing)")
    if REGIONAL:
        is15 = df[DENUE_STATE_COLUMN] == REGIONAL_STATE_CODE
        print("Per municipio of the four (storefronts by bucket, blank names):")
        for m, g in df[is15].groupby(DENUE_MUNICIPIO_COLUMN):
            gb = int(g["business_name"].isna().sum() + (g["business_name"] == "").sum())
            print(f"    {m:26s} {len(g):7,}  {dict(g['bucket'].value_counts())}  "
                  f"blank {gb}")

    # --- the residence signal, measured here because it is not published ---
    interior = df["numero_int"].fillna("").astype(str).str.strip()
    has_int = int((interior != "").sum())
    print(f"With an interior/unit number: {pct(has_int, len(df), 'storefronts')} "
          "(DENUE's structured numero_int; measured, not written to the output)")
    # An interior number on a storefront is usually a unit in a plaza or a
    # market rather than a dwelling - `tipoCenCom`/`nom_CenCom` exist for
    # exactly that - so this is reported as context, not as a residence count.
    # No threshold is asserted: there is no personal name on any pin to
    # co-locate with an address, which is the exposure this check exists for.

    # --- coordinates -------------------------------------------------------
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    before = len(df)
    df = df[df["latitude"].notna() & df["longitude"].notna()].copy()
    print(f"\nWith coordinates: {pct(len(df), before, 'storefronts')}")
    b = MEXICO_CITY_BBOX
    inbox = (df["latitude"].between(b["lat_min"], b["lat_max"])
             & df["longitude"].between(b["lon_min"], b["lon_max"]))
    if not REGIONAL:
        print(f"Inside the sanity box: {pct(int(inbox.sum()), len(df), 'geocoded storefronts')}")
        df = df[inbox].copy()
    else:
        # CDMX's rows keep the city-alone test (the sanity box), so the CDMX
        # side of the map does not move. Entidad 15's rows are tested against
        # the SCOPE polygon (CDMX and the four municipios), Monterrey's
        # pattern of testing a regional register against its own boundaries
        # rather than a box. Points outside their OWN municipio are counted
        # for the record; a point over a municipio line inside the scope is a
        # real storefront placed a little off, and stays.
        #
        # Measured 2026-10-07: 416 of 127,860 entidad 15 storefronts lie
        # outside the scope and are dropped. 398 are one compact cluster that
        # DENUE codes Nezahualcóyotl and OSM places 14-823 m east of its
        # polygon (the Chimalhuacán side), over 5 km from any station, so no
        # ring count moves with it; Naucalpan has 13, La Paz 4, Ecatepec 1.
        # 21 Naucalpan rows that fall inside CDMX stay. Re-measure if either
        # boundary file is re-fetched.
        is15 = df[DENUE_STATE_COLUMN] == REGIONAL_STATE_CODE
        print(f"CDMX rows inside the sanity box: "
              f"{pct(int((inbox & ~is15).sum()), int((~is15).sum()), 'geocoded storefronts')}")
        scope, _cdmx, by_code = load_scope()
        sub = df[is15]
        pts = gpd.GeoSeries(gpd.points_from_xy(sub["longitude"], sub["latitude"]),
                            index=sub.index, crs=CRS_GEOGRAPHIC)
        in_scope = pts.within(scope)
        munid = REGIONAL_STATE_CODE + sub[DENUE_MUNICIPIO_CODE_COLUMN]
        own = pd.Series(False, index=sub.index)
        for code, geom in by_code.items():
            mask = munid == code
            own[mask] = pts[mask].within(geom)
        print("Entidad 15 storefronts outside their own municipio polygon:")
        for m, g in own.groupby(sub[DENUE_MUNICIPIO_COLUMN]):
            print(f"    {m:26s} {int((~g).sum()):5,} of {len(g):,}")
        print(f"Entidad 15 storefronts inside the scope polygon: "
              f"{pct(int(in_scope.sum()), len(sub), 'geocoded storefronts')}"
              f"  (inside the sanity box: {int(inbox[is15].sum()):,})")
        emit("outside_scope_15_rows", int((~in_scope).sum()))
        keep = inbox & ~is15
        keep.loc[sub.index] = in_scope.values
        df = df[keep].copy()

    # --- dedupe on DENUE's own primary key ---------------------------------
    before = len(df)
    df = df.drop_duplicates(subset="id").copy()
    if before != len(df):
        print(f"Dropped {before - len(df):,} duplicate ids")

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    # `"municipio"` here is THIS PROJECT'S OUTPUT column, beside business_name
    # and bucket - not DENUE's input column, which is DENUE_MUNICIPIO_COLUMN
    # above. They are the same string only because the column passes through
    # unrenamed. Left as a literal deliberately: if DENUE renamed its column,
    # this output contract should not move with it.
    cols = ["business_name", "latitude", "longitude", tax.VALUE_COLUMN,
            "scian", "bucket", "municipio"]
    df[cols].to_csv(BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\nWrote {len(df):,} storefronts to {BUSINESSES_CLEAN_CSV}")
    emit("businesses_clean_rows", len(df))


if __name__ == "__main__":
    main()
