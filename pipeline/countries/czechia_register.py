"""ROS02 + RES + RUIAN -> one Czech city's storefronts. Shared by every Czech
city, on Denmark's and Norway's pattern.

⚠ **DELIBERATELY NOT IN `czechia.py`.** That module is imported by a city's
`config.py`, which `app/pages/*.py` imports in turn, so it must stay importable
under the lean deploy venv. This one imports pandas and pyproj and is imported
only by step files.

THE JOIN, in the order it runs:

    ROS02    active establishments (dedupe ICP)      -> where it trades
    RUIAN    the obec's address codes                -> which city, and a point
    RES      the owner, by ICO                       -> activity, form, name
"""
import io
import re
import sys
import zipfile

import pandas as pd

from pipeline.baseline import emit
from pipeline.countries import czechia as CZ
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module

BUCKET_DIVISIONS = ("47", "56", "96")
# Prague Castle, Hrad I. nádvoří - RUIAN code 21690278 - measured in the brief
# at 50.08948, 14.39861 under EPSG:5513 with (X, Y) as published. The step
# re-checks it, because the wrong axis orders land in Germany or the Arctic
# and still look like coordinates.
CRS_CONTROL = ("21690278", 50.08948, 14.39861)


def _need(path, cfg):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/{cfg.SLUG}/fetch_sources.py")
    return path


def nace_labels():
    labels = {}
    for level in CZ.NACE_LEVEL_CODEBOOKS:
        p = CZ.NACE_DIR / f"cz_nace_2025_level{level}.csv"
        if not p.exists():
            sys.exit(f"missing {p}")
        d = pd.read_csv(p, dtype=str)
        labels.update(zip(d["chodnota"], d["text"]))
    return labels


def ruian(cfg):
    """The obec's addresses: code -> WGS84 point and a street-address label."""
    from pyproj import Transformer

    z = zipfile.ZipFile(_need(cfg.RUIAN_ZIP, cfg))
    member = next(n for n in z.namelist() if n.lower().endswith(".csv"))
    a = pd.read_csv(io.BytesIO(z.read(member)), sep=CZ.RUIAN_SEP, dtype=str,
                    encoding=CZ.RUIAN_ENCODING)
    x = pd.to_numeric(a[CZ.RUIAN_X], errors="coerce")
    y = pd.to_numeric(a[CZ.RUIAN_Y], errors="coerce")
    lat, lon = Transformer.from_crs(CZ.RUIAN_CRS, "EPSG:4326").transform(
        x.to_numpy(), y.to_numpy())
    # An address with no coordinates transforms to INFINITY, not NaN - six in
    # Praha (2026-08-31). Made missing here, or they would pass a notna() test
    # and fail the bounding box instead, misreported as a bad coordinate.
    a["latitude"] = pd.Series(lat, index=a.index).where(pd.Series(lat).abs().lt(90).values)
    a["longitude"] = pd.Series(lon, index=a.index).where(pd.Series(lon).abs().lt(180).values)
    code, want_lat, want_lon = CRS_CONTROL
    got = a.loc[a[CZ.RUIAN_CODE] == code, ["latitude", "longitude"]]
    if got.empty or abs(got.iloc[0, 0] - want_lat) > 0.001 or abs(got.iloc[0, 1] - want_lon) > 0.001:
        sys.exit(f"RUIAN CRS control failed: Prague Castle ({code}) came out at "
                 f"{got.values.tolist()}, expected {want_lat}, {want_lon} - the axis "
                 f"order or the CRS is wrong")
    street = a[CZ.RUIAN_STREET].fillna(a[CZ.RUIAN_PART]).fillna("")
    num = a[CZ.RUIAN_HOUSE].fillna("")
    orient = (a[CZ.RUIAN_ORIENT].fillna("") + a[CZ.RUIAN_ORIENT_LETTER].fillna("")).str.strip()
    a["address"] = (street + " " + num + ("/" + orient).where(orient != "", "")).str.strip()
    print(f"RUIAN addresses in obec {cfg.OBEC}: {len(a):,}; coordinates on "
          f"{a['latitude'].notna().mean():.2%}; CRS control (Prague Castle) passed")
    return a.set_index(CZ.RUIAN_CODE)[["latitude", "longitude", "address"]]


def _strip_form(name):
    out = str(name or "").strip()
    for tail in CZ.LEGAL_FORM_TAILS:
        out = re.sub(tail, "", out, flags=re.IGNORECASE).strip()
    return out.rstrip(",").strip()


def build_storefronts(cfg, bbox):
    """The city's storefronts, cleaned, placed and labelled."""
    TAX = load_taxonomy_module(cfg.TAXONOMY_SYSTEM)
    adr = ruian(cfg)

    ros = pd.read_csv(_need(CZ.ROS02_CSV, cfg), dtype=str,
                      usecols=list(CZ.ROS_COLUMNS) + ["DATPLAT"])
    snapshot = ros["DATPLAT"].max()
    print(f"\nROS02: {len(ros):,} rows nationally, snapshot {snapshot}")
    ros = ros.drop_duplicates("ICP")
    # ACTIVE AGAINST THE FILE'S OWN DATE, never today's: a drift check next
    # month must give this month's answer.
    ros = ros[ros["DATUKON"].isna() | (ros["DATUKON"] > snapshot)]
    print(f"  {len(ros):,} distinct establishments active on {snapshot}")
    ros = ros[ros["PKODADM"].isin(adr.index)]
    print(f"  {len(ros):,} with an address in obec {cfg.OBEC}")
    emit("establishments_in_obec", len(ros))

    res = pd.read_csv(_need(CZ.RES_CSV, cfg), dtype=str, usecols=list(CZ.RES_COLUMNS))
    res = res.drop_duplicates("ICO")
    df = ros.merge(res, on="ICO", how="left")
    print(f"  owner found in RES for {df['FORMA'].notna().mean():.2%}")
    before = len(df)
    df = df[df["FORMA"].notna() & df["DDATZAN"].isna()]
    print(f"  {len(df):,} whose owner is active in RES ({before - len(df):,} not)")

    labels = nace_labels()
    df["nace2025_code"] = df["NACE2025"].map(TAX.normalise_code)
    df[cfg.RAW_CLASSIFICATION_COLUMN] = df["nace2025_code"].map(labels).fillna("")
    df = df[df["nace2025_code"].str[:2].isin(BUCKET_DIVISIONS)]
    print(f"\n  {len(df):,} in CZ-NACE 2025 divisions {'/'.join(BUCKET_DIVISIONS)} "
          f"(depth: {df['nace2025_code'].str.len().value_counts().sort_index().to_dict()})")
    emit("bucket_rows", len(df))
    struct = df["nace2025_code"].map(TAX.excluded)
    print(f"  {int(struct.notna().sum()):,} structurally excluded:")
    for p, n in struct.value_counts().items():
        print(f"      {p:<5} {n:>6,}  {TAX.NOT_PREMISES_PREFIXES[p]}")
    df = filter_to_storefront(df, cfg.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")
    emit("storefront_rows", len(df))

    # --- natural persons at their own registered seat: EXCLUDED (owner) ---
    person = df["FORMA"].isin(CZ.NATURAL_PERSON_FORMS)
    at_home = person & (df["PKODADM"] == df["KODADM"])
    print(f"\n  natural persons: {int(person.sum()):,} ({person.mean():.1%}); at their own "
          f"registered seat: {int(at_home.sum()):,} ({at_home.mean():.1%}) - EXCLUDED")

    print("\n  catch-all codes (per-city call, config.CATCH_ALL_EXCLUDE):")
    for code in sorted(TAX.CATCH_ALL_CODES) + ["96230"]:
        m = df["nace2025_code"] == code
        if m.any():
            mark = "DROP" if code in cfg.CATCH_ALL_EXCLUDE else "keep"
            print(f"      {code}  {int(m.sum()):>6,}  ({m.mean():4.1%})  {mark}  natural "
                  f"person {person[m].mean():4.0%}  at own seat {at_home[m].mean():4.0%}  "
                  f"{labels.get(code, '')[:45]}")
    print(f"      (all storefronts: natural person {person.mean():.0%}, at own seat "
          f"{at_home.mean():.0%})")
    df = df[~at_home]
    before = len(df)
    df = df[~df["nace2025_code"].isin(cfg.CATCH_ALL_EXCLUDE)]
    print(f"  {len(df):,} after the own-seat and catch-all exclusions "
          f"({before - len(df):,} catch-all)")

    # --- coordinates: the RUIAN join ----------------------------------------
    df = df.join(adr, on="PKODADM")
    placed = df["latitude"].notna()
    print(f"\n  placed {int(placed.sum()):,} of {len(df):,} ({placed.mean():.2%})")
    df = df[placed]
    before = len(df)
    df = df[df["latitude"].between(bbox["lat_min"], bbox["lat_max"])
            & df["longitude"].between(bbox["lon_min"], bbox["lon_max"])]
    if len(df) != before:
        print(f"  {before - len(df):,} dropped on the sanity bounding box")

    # --- the pin's label ---------------------------------------------------
    #
    # A NATURAL PERSON'S OR A v.o.s. PARTNERSHIP'S NAME IS NEVER SHOWN - a Czech
    # sole trader's business name carries the person's own name by law - so the
    # pin shows the establishment's street address. Companies show their
    # registered name, less the legal-form tail.
    suppressed = df["FORMA"].isin(CZ.NAME_SUPPRESSED_FORMS)
    trade = df["FIRMA"].map(_strip_form)
    df["name_is_address"] = suppressed | (trade == "")
    df["business_name"] = trade.where(~df["name_is_address"], df["address"])
    print(f"\n  registered name shown on {int((~df['name_is_address']).sum()):,} rows "
          f"({(~df['name_is_address']).mean():.1%}); the address on the rest")
    emit("storefronts_placed", len(df))
    emit("name_shown", int((~df["name_is_address"]).sum()))

    out = df.rename(columns={"ICP": "icp"})[
        ["icp", "business_name", "name_is_address", "latitude", "longitude",
         cfg.RAW_CLASSIFICATION_COLUMN, "nace2025_code"]]
    if out["icp"].duplicated().any():
        sys.exit("an establishment appears twice after the join")
    return out
