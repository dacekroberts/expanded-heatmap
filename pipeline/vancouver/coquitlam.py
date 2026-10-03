"""Coquitlam's leg of Vancouver (Regional) step 2: load, collapse, classify.

load_coquitlam(csv_path, classify) reads the file pipeline/vancouver/fetch_sources.py writes
and returns one row per licence, bucketed rows only, in the shared columns of
pipeline/vancouver/step2_clean_businesses.py plus `_used_fallback`.

What the source does, measured 2026-10-03 on the 2026-09-04 layer:
  - THE DOUBLE LISTING. The layer holds the whole licence table twice:
    OBJECTID n and n + 6004 are the same licence, identical in every
    published column (6,001 licences). One licence (a grooming salon) is
    listed four times, as two address variants each listed twice, with one
    coordinate pair; the Coquitlam address is kept, as it matches the
    coordinate. So collapsing on COL_FOLDER loses nothing.
  - ONE NAME FIELD. COLBUSINESSNAME is the only name column; there is no
    legal/trade split, so there is no fallback and `_used_fallback` is False
    on every row (Surrey's shape).
  - THE COORDINATES ARE WEB MERCATOR. LAT and LONG hold EPSG:3857 metres
    (LAT is y, about 6.3 million; LONG is x, about -13.7 million), not
    degrees. Converted to EPSG:4326 here.
  - THE LICENCE ID is COL_FOLDER ("26 116374 00": folder year, sequence,
    suffix). The sequence alone is NOT unique: 18 sequences recur under a
    different folder year for an unrelated business, so the key is the whole
    folder string.
"""

import re
import sys

import pandas as pd
from pyproj import Transformer

from pipeline.residence import looks_organisational, looks_personal

COLUMNS = ["source", "key", "business_name", "address", "category",
           "latitude", "longitude", "_used_fallback"]
FORBIDDEN = {"COL_BUSINESSPHONE", "EMAILADDRESS"}
FORBIDDEN_PATTERN = re.compile(r"PHONE|EMAIL|OWNER|MAIL|LICENSEE|LICENCEE", re.I)
STATUS_KEEP = {"Issued", "Renewal"}

# Name-level carve-outs inside a kept subtype, by docs/category_rules.md.
# Each is (subtype, regex on the business name, reason). Re-measure if the
# layer is re-pulled: the counts printed are the check.
CARVE_OUTS = [
    # R1: contract and institutional catering has no counter of its own.
    # 7 licences of one contract caterer at school and civic sites (2026-10-03).
    ("Restaurant Sales", re.compile(r"\bcater", re.I),
     "contract/event caterer (R1)"),
    # Mobile units out (category_rules.md, "Mobile units, kiosk carts").
    # 1 licence (2026-10-03).
    ("Personal Grooming Services", re.compile(r"\bmobile\b", re.I),
     "mobile service, no premises"),
]

# Mall kiosks are left out (owner, 2026-10-02). Two ways in: their own
# subtype, `Retail Sales - Kiosk` (9 licences, None in coquitlam_buckets.py),
# and a kept licence whose unit is the word "Kiosk" ("Kiosk - 2929 Barnet
# Hwy": 1 licence under Retail Sales, 2026-10-03). The second is dropped
# here; a name containing "kiosk" with a normal unit is only reported.
KIOSK = re.compile(r"\bkiosk\b", re.I)
KIOSK_UNIT = re.compile(r"^\s*kiosk\b", re.I)
# The shape of a person's own name printed Surname, Given.
SURNAME_FIRST = re.compile(r"^[A-Za-z][A-Za-z'.-]*(?: [A-Za-z][A-Za-z'.-]*)?, [A-Za-z]")

# Sanity box, generous around the City of Coquitlam (including its northern
# watershed). A point outside it is printed and dropped.
BBOX = {"lat_min": 49.20, "lat_max": 49.47, "lon_min": -122.92, "lon_max": -122.60}

_TO_WGS84 = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)


def _check_columns(df):
    bad = sorted(c for c in df.columns
                 if c in FORBIDDEN or FORBIDDEN_PATTERN.search(c))
    if bad:
        sys.exit(f"coquitlam: forbidden column(s) {bad} in the raw file")


def load_coquitlam(csv_path, classify):
    """One row per licence, bucketed rows only, every count printed.

    classify: callable taking {"category": ..., "source": "coquitlam"} and
    returning a bucket or None (the taxonomy module's classify()).
    """
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    _check_columns(df)
    print(f"\nCoquitlam: {len(df):,} rows read")

    status = df["U_STATUSCODEDESC"].str.strip()
    print("  status: " + ", ".join(f"{k}={v:,}"
                                   for k, v in status.value_counts().items()))
    df = df[status.isin(STATUS_KEEP)].copy()
    print(f"  after status filter (Issued, Renewal): {len(df):,}")

    # --- collapse the double listing -----------------------------------------
    df["_oid"] = pd.to_numeric(df["OBJECTID"])
    df["_coq"] = df["COL_BUSINESSADDR"].str.contains(r",\s*Coquitlam\b",
                                                     case=False, regex=True)
    same = ["COL_FOLDER", "COLBUSINESSNAME", "U_SUBCODEDESC",
            "U_STATUSCODEDESC", "INDATE", "ISSUEDATE", "LAT", "LONG"]
    per_folder = df.groupby("COL_FOLDER")[same[1:]].nunique()
    varying = {c: int((per_folder[c] > 1).sum()) for c in same[1:]}
    if any(varying.values()):
        sys.exit(f"coquitlam: copies of one licence differ in {varying}; the "
                 f"double listing is no longer a plain repeat")
    copies = df["COL_FOLDER"].value_counts()
    addr_variants = int((df.groupby("COL_FOLDER")["COL_BUSINESSADDR"]
                         .nunique() > 1).sum())
    before = len(df)
    df = (df.sort_values(["COL_FOLDER", "_coq", "_oid"],
                         ascending=[True, False, True])
            .drop_duplicates("COL_FOLDER", keep="first"))
    print(f"  after collapsing the double listing: {before:,} -> {len(df):,} "
          f"licences (copies per licence: "
          f"{copies.value_counts().sort_index().to_dict()}; "
          f"{addr_variants} licence with two address variants, Coquitlam "
          f"address kept)")

    # --- shared columns -------------------------------------------------------
    df["source"] = "coquitlam"
    df["key"] = df["COL_FOLDER"].str.strip()
    df["business_name"] = df["COLBUSINESSNAME"].str.strip()
    df["address"] = df["COL_BUSINESSADDR"].str.strip()
    df["category"] = df["U_SUBCODEDESC"].str.strip()
    df["_used_fallback"] = False
    # A person's own name printed Surname, Given (1 kept licence on
    # 2026-10-03) shows the subtype instead, Vancouver's rule for a legal name
    # standing in for a trade name (DECISIONS 2026-09-21, "A blank trade name
    # yields a neutral label, never a person's name").
    own = (df["business_name"].str.match(SURNAME_FIRST)
           & ~df["business_name"].str.contains("[&0-9]")
           & ~df["business_name"].map(looks_organisational))
    df.loc[own, "business_name"] = df.loc[own, "category"]
    print(f"  a person's own name (Surname, Given) shows the subtype: {int(own.sum())} "
          f"(of every licence, before the bucket filter)")
    x = pd.to_numeric(df["LONG"], errors="coerce")
    y = pd.to_numeric(df["LAT"], errors="coerce")
    lon, lat = _TO_WGS84.transform(x.to_numpy(), y.to_numpy())
    df["latitude"] = lat
    df["longitude"] = lon

    # Home-based signals, measured on every licence before the bucket filter:
    # how many licences share the point, and whether a home-occupation, home
    # day-care or B&B licence sits at the same address text.
    df["_pt"] = df["LAT"].str[:12] + "," + df["LONG"].str[:12]
    df["_pt_n"] = df.groupby("_pt")["_pt"].transform("size")
    addr_norm = (df["address"].str.upper()
                 .str.replace(r"\s+", " ", regex=True).str.strip())
    home_sub = df["category"].str.match(
        r"Home Occupation|Day Care Centre - Residential|Bed & Breakfast")
    df["_home_addr"] = addr_norm.isin(set(addr_norm[home_sub]))

    # --- classify ---------------------------------------------------------------
    df["bucket"] = [classify({"category": c, "source": "coquitlam"})
                    for c in df["category"]]
    print("  all licences by bucket: " + ", ".join(
        f"{k}={v:,}" for k, v in
        df["bucket"].fillna("None").value_counts().items()))
    kiosk_sub = int((df["category"] == "Retail Sales - Kiosk").sum())
    print(f"  mall kiosks left out by subtype 'Retail Sales - Kiosk': "
          f"{kiosk_sub}")
    df = df[df["bucket"].notna()].copy()
    print(f"  bucketed: {len(df):,}")

    for subtype, pattern, reason in CARVE_OUTS:
        hit = (df["category"] == subtype) & df["business_name"].str.contains(
            pattern)
        print(f"  carve-out {reason}: {int(hit.sum())} under {subtype!r}")
        df = df[~hit]

    kiosk_unit = df["address"].str.contains(KIOSK_UNIT)
    print(f"  mall kiosks left out by a 'Kiosk' unit in the address: "
          f"{int(kiosk_unit.sum())} "
          f"({df.loc[kiosk_unit, 'category'].value_counts().to_dict()}); "
          f"kiosks out in all: {kiosk_sub + int(kiosk_unit.sum())}")
    df = df[~kiosk_unit]
    still_kiosk = (df["business_name"].str.contains(KIOSK)
                   | df["address"].str.contains(KIOSK))
    print(f"  kept rows still reading as a kiosk (reported, not dropped): "
          f"{int(still_kiosk.sum())}")

    # --- coordinates ------------------------------------------------------------
    no_xy = df["latitude"].isna() | df["longitude"].isna()
    print(f"  without coordinates: {int(no_xy.sum())} (dropped)")
    df = df[~no_xy]
    b = BBOX
    inside = (df["latitude"].between(b["lat_min"], b["lat_max"])
              & df["longitude"].between(b["lon_min"], b["lon_max"]))
    print(f"  outside the Coquitlam sanity box: {int((~inside).sum())} "
          f"(dropped)")
    for r in df[~inside].itertuples():
        print(f"      {r.key}  {r.address}  {r.latitude:.5f},{r.longitude:.5f}")
    df = df[inside]
    pts = df.groupby([df["latitude"].round(6), df["longitude"].round(6)]).size()
    print(f"  distinct points: {len(pts):,}; most rows at one point: "
          f"{int(pts.max())}; points shared by 5+ licences: "
          f"{int((pts >= 5).sum())}")
    non_coq = ~df["address"].str.contains(r",\s*Coquitlam\b", case=False,
                                          regex=True)
    print(f"  kept rows whose address does not read 'Coquitlam': "
          f"{int(non_coq.sum())}")

    # --- currency and premises signals (reported) -------------------------------
    ren = df["U_STATUSCODEDESC"] == "Renewal"
    stale_ren = ren & (df["INDATE"].str[:8] < "20250904")
    old_issued = (~ren) & df["key"].str[:2].isin(["17", "18", "19", "20",
                                                  "21", "22", "23", "24"])
    print(f"  kept Renewal rows: {int(ren.sum())} (renewal folder opened "
          f"more than 12 months before the layer's last edit: "
          f"{int(stale_ren.sum())}); kept Issued rows in a pre-2025 folder: "
          f"{int(old_issued.sum())}")
    no_unit = ~df["address"].str.contains(r" - ", regex=False)
    lone = no_unit & (df["_pt_n"] == 1)
    cul = no_unit & df["address"].str.contains(
        r"\b(?:Crt|Pl|Cres|Close|Lane)\b,", case=False, regex=True)
    print(f"  home-based signals (reported, not dropped): same address as a "
          f"home-occupation/home day-care/B&B licence {int(df['_home_addr'].sum())}; "
          f"no unit on a Crt/Pl/Cres/Close/Lane street {int(cul.sum())} "
          f"({df.loc[cul, 'category'].value_counts().to_dict()}); "
          f"no unit and the only licence at its point {int(lone.sum())} "
          f"({df.loc[lone, 'category'].value_counts().to_dict()})")
    persons = df["business_name"].map(looks_personal)
    print(f"  kept names that residence.looks_personal reads as a person's: "
          f"{int(persons.sum())}")
    dup = df.assign(_n=df["business_name"].str.upper(),
                    _a=df["address"].str.upper()).duplicated(["_n", "_a"],
                                                             keep=False)
    print(f"  kept licences sharing a name and address with another kept "
          f"licence: {int(dup.sum())} (step 2's per-source name+address "
          f"dedup collapses these)")

    print("  final by bucket: " + ", ".join(
        f"{k}={v:,}" for k, v in df["bucket"].value_counts().items()))
    print(f"  final rows: {len(df):,}")
    return df[COLUMNS].reset_index(drop=True)
