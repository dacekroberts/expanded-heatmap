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
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.counts import pct
from pipeline.taxonomies import load_taxonomy_module
from pipeline.mexico_city.config import (
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    DENUE_ACTIVITY_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_MEMBER,
    DENUE_MUNICIPIO_COLUMN,
    DENUE_NAME_COLUMN,
    DENUE_STATE_CODE,
    DENUE_STATE_COLUMN,
    DENUE_URL,
    DENUE_ZIP,
    FORBIDDEN_COLUMNS,
    MEXICO_CITY_BBOX,
    OVERPASS_USER_AGENT,
    PREMISES_TYPE_COLUMN,
    PREMISES_TYPE_KEEP,
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


def download():
    if DENUE_ZIP.exists():
        print(f"  cached {DENUE_ZIP.name} ({DENUE_ZIP.stat().st_size:,} bytes)")
        return
    print(f"  downloading {DENUE_URL}")
    DENUE_ZIP.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(DENUE_URL, timeout=900,
                     headers={"User-Agent": OVERPASS_USER_AGENT})
    r.raise_for_status()
    # Magic bytes, not the filename the server claims - add-country's rule,
    # learned from Busan serving a PNG under a CSV's Content-Disposition.
    if not r.content.startswith(b"PK\x03\x04"):
        raise SystemExit(
            f"DENUE download is not a ZIP (first bytes {r.content[:8]!r}). "
            "Check what the server actually sent before trusting it."
        )
    DENUE_ZIP.write_bytes(r.content)
    print(f"  wrote {DENUE_ZIP.stat().st_size:,} bytes")


def main():
    print("=== Step 2: Mexico City storefronts (INEGI DENUE) ===\n")
    tax = load_taxonomy_module(TAXONOMY_SYSTEM)

    download()
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
          f"{df['municipio'].nunique()} alcaldias")

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
          "(no fallback to a legal or personal name exists - see the docstring)")

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
    print(f"Inside the sanity box: {pct(int(inbox.sum()), len(df), 'geocoded storefronts')}")
    df = df[inbox].copy()

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
