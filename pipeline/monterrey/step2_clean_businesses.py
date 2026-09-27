"""Step 2 - Monterrey (Regional) storefronts from INEGI's DENUE.

Guadalajara's step 2 with one change: the regional scope is keyed on INEGI's
municipio CODE (cve_mun), not on the municipio's name. OSM's `INEGI:MUNID` is
the same code, so the register and the boundaries join on one key and no
spelling can come between them. The names are still asserted against DENUE's
own `municipio` column, so a wrong code fails here rather than scoping to a
different municipio.

Privacy is the other two Mexican cities' position, and it is structural:
`nom_estab` is the exterior sign, INEGI withholds `raz_social` for a persona
física, and the forbidden columns (phone, e-mail, web, legal name) are never
loaded - this step asserts they never arrive. See pipeline/countries/mexico.py.
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
from pipeline.monterrey.step1_stations import load_boundaries
from pipeline.monterrey.config import (
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    DENUE_ACTIVITY_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_MEMBER,
    DENUE_MUNICIPIO_CODE_COLUMN,
    DENUE_MUNICIPIO_COLUMN,
    DENUE_NAME_COLUMN,
    DENUE_STATE_CODE,
    DENUE_STATE_COLUMN,
    DENUE_ZIP,
    FORBIDDEN_COLUMNS,
    MONTERREY_BBOX,
    MUNICIPIOS,
    PREMISES_TYPE_COLUMN,
    PREMISES_TYPE_KEEP,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
)

# Only these of DENUE's 42 columns are read; none of FORBIDDEN_COLUMNS is.
USECOLS = (
    "id",
    DENUE_NAME_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_ACTIVITY_COLUMN,
    PREMISES_TYPE_COLUMN,
    DENUE_STATE_COLUMN,
    DENUE_MUNICIPIO_CODE_COLUMN,
    DENUE_MUNICIPIO_COLUMN,
    # Measured and printed, never written out - see Guadalajara's step 2.
    "numero_int",
    "latitud",
    "longitud",
)

# Contact details that could sit inside a SIGN NAME, which is published. They
# are printed for a person to read, never silently kept or dropped. Read on
# 2026-09-27: the one e-mail shape is a shop's sign ("MARY P@PER.COM
# PAPELERIA"), and every phone shape among fixed premises is a Movistar branch
# code ("MOVISTAR 99040007 CAC GALERIAS MONTERREY") - none is a person's contact.
EMAIL_LIKE = re.compile(r"[^\s@]+@[^\s@]+\.[^\s@]+")
# 8-10 digits in one run, or Mexico's 10-digit shape in groups (81 1234 5678).
PHONE_LIKE = re.compile(r"(?<!\d)\d{8,10}(?!\d)|(?<!\d)\d{2,3}[\s.-]\d{3,4}[\s.-]\d{4}(?!\d)")


def require_denue():
    """The DENUE zip must already be here - this step does NOT download it."""
    if not DENUE_ZIP.exists():
        raise SystemExit(
            f"Missing {DENUE_ZIP.name}. Run pipeline/monterrey/fetch_sources.py first."
        )
    print(f"  {DENUE_ZIP.name} ({DENUE_ZIP.stat().st_size:,} bytes)")


def main():
    print("=== Step 2: Monterrey (Regional) storefronts (INEGI DENUE) ===\n")
    tax = load_taxonomy_module(TAXONOMY_SYSTEM)

    require_denue()
    zf = zipfile.ZipFile(DENUE_ZIP)
    if DENUE_MEMBER not in zf.namelist():
        raise SystemExit(
            f"{DENUE_MEMBER} not in the ZIP. Members: {zf.namelist()}. The "
            "dictionary member is a plausible near-miss - never take the first .csv."
        )
    raw = zf.read(DENUE_MEMBER).decode(SOURCE_ENCODING)

    header = pd.read_csv(io.StringIO(raw), nrows=0)
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

    ents = df[DENUE_STATE_COLUMN].value_counts()
    if len(ents) != 1 or ents.index[0] != DENUE_STATE_CODE:
        raise SystemExit(f"expected only cve_ent={DENUE_STATE_CODE}, got {dict(ents)}")
    print(f"  all rows cve_ent={DENUE_STATE_CODE}; "
          f"{df[DENUE_MUNICIPIO_CODE_COLUMN].nunique()} municipios")

    # --- THE REGIONAL SCOPE, by code, with the names asserted ---------------
    code = df[DENUE_MUNICIPIO_CODE_COLUMN].str.zfill(3)
    names_by_code = (df.assign(_c=code).groupby("_c")[DENUE_MUNICIPIO_COLUMN]
                     .agg(lambda s: sorted(set(s))))
    for c, expected in MUNICIPIOS.items():
        seen = names_by_code.get(c)
        if seen != [expected]:
            raise SystemExit(
                f"cve_mun {c}: DENUE names it {seen}, config expects {expected!r}. "
                "The code is the join key; a mismatch means the code is wrong.")
    before = len(df)
    df = df[code.isin(MUNICIPIOS)].copy()
    print(f"\nFour municipios (by INEGI code): {pct(len(df), before, 'Nuevo León units')} kept")
    for m, n in df[DENUE_MUNICIPIO_COLUMN].value_counts().items():
        print(f"    {m:26s} {n:8,}")
    emit("in_scope_rows", len(df))

    # --- FIJO ONLY ---------------------------------------------------------
    before = len(df)
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
          "(no fallback to a legal or personal name exists)")
    names = df["business_name"].fillna("")
    for label, rx in (("e-mail-shaped", EMAIL_LIKE), ("phone-length digit run", PHONE_LIKE)):
        hits = names[names.str.contains(rx)]
        print(f"Sign names with an {label}: {len(hits)}  (read by hand before publishing)")
        for n in hits:
            print(f"      {n}")

    interior = df["numero_int"].fillna("").astype(str).str.strip()
    has_int = int((interior != "").sum())
    print(f"With an interior/unit number: {pct(has_int, len(df), 'storefronts')} "
          "(measured, not written to the output)")

    # --- coordinates -------------------------------------------------------
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    before = len(df)
    df = df[df["latitude"].notna() & df["longitude"].notna()].copy()
    print(f"\nWith coordinates: {pct(len(df), before, 'storefronts')}")
    # THE FOUR MUNICIPIOS' OWN BOUNDARIES, not a bounding box. The screen's
    # OSM query box stops at 25.55 N while Monterrey municipio runs south to
    # 25.48, so a box test dropped 121 storefronts of which almost all are real
    # rows in southern Monterrey. The polygon test keeps those and still drops
    # the genuinely misplaced ones (some sit at 20.6 N, 550 km away).
    _by_muni, union = load_boundaries()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        index=df.index, crs=CRS_GEOGRAPHIC)
    inside = pts.within(union)
    b = MONTERREY_BBOX
    inbox = (df["latitude"].between(b["lat_min"], b["lat_max"])
             & df["longitude"].between(b["lon_min"], b["lon_max"]))
    print(f"Inside the four municipios: {pct(int(inside.sum()), len(df), 'geocoded storefronts')}"
          f"  (a bbox test would have kept {int(inbox.sum()):,})")
    df = df[inside].copy()

    before = len(df)
    df = df.drop_duplicates(subset="id").copy()
    if before != len(df):
        print(f"Dropped {before - len(df):,} duplicate ids")

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = ["business_name", "latitude", "longitude", tax.VALUE_COLUMN,
            "scian", "bucket", "municipio"]
    df[cols].to_csv(BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\nWrote {len(df):,} storefronts to {BUSINESSES_CLEAN_CSV}")
    emit("businesses_clean_rows", len(df))


if __name__ == "__main__":
    main()
