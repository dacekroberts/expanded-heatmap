"""FAVV-AFSCA's food operators placed on Flanders' VKBO points: the business
leg Antwerp and Ghent share.

TWO SOURCES, NO NAME IN EITHER (the Antwerp brief):

  * FAVV's operator list (`inter_actieve_actoren_EN.csv`, cached once at
    `data/belgium/raw/`, latin-1, one row per operator x place x activity x
    product): the establishment number, the place and activity codes, the
    postcode and commune. No name, no street, no point. The code descriptions
    are French even in the EN file.
  * VKBO, Digitaal Vlaanderen's enriched KBO, through its WFS with field
    selection: the number, the unit type, the NIS code, the Adressenregister
    postcode and the point (Lambert 72, EPSG:31370). Fetched per city by
    `pipeline/<city>/fetch_sources.py` (`belgium_fetch.fetch_vkbo`).

THE CHAIN, each stage counted by the caller:

  1. FAVV rows in the city's postcodes, grouped by establishment
     (`OP N° Unique Id`); each establishment classified as a whole by
     `pipeline/taxonomies/belgium_favv.py` (fixed first-match order).
  2. Joined on the establishment number to VKBO's `Ondernemingsnr`. A FAVV
     number (9xxxxxxxxx, mostly farms) cannot join; KBO establishment numbers
     (2xxxxxxxxx) join to VKBO's establishment units.
  3. VKBO's (0,0) placeholder (an address the Adressenregister did not match;
     not null) dropped by a Belgium-wide Lambert 72 box.
  4. Reprojected to EPSG:4326 for the map; the caller cuts by the city's
     polygon in its own UTM zone.

NO NAME, PHONE OR EMAIL ANYWHERE: FAVV carries none, the VKBO request asks
for none (and the fetch refuses a page carrying any column it did not ask
for), and `assert_no_personal_columns()` checks every frame this module
returns. The establishment number is used to join and then dropped: a sole
trader's number identifies a person's enterprise, so it is not stored in
processed output.
"""
import sys

import pandas as pd

from pipeline.countries.belgium import FAVV_CSV
from pipeline.taxonomies import belgium_favv as tax

# --- FAVV ------------------------------------------------------------------------
FAVV_ENCODING = "latin-1"
# The header as the 2026-09-28 file writes it (latin-1, degree signs included).
# Read by position, checked by name, so a reordered file stops the step.
FAVV_COLUMNS = {0: "OP N° Unique Id", 4: "PAP ACT code", 6: "PAP PLA code",
                14: "PC Code Postal", 15: "GEM Nom", 19: "Date aujourd'hui"}
FAVV_RENAME = {"OP N° Unique Id": "op", "PAP ACT code": "act", "PAP PLA code": "pla",
               "PC Code Postal": "postcode", "GEM Nom": "commune",
               "Date aujourd'hui": "extract_date"}

# --- VKBO, the WFS only --------------------------------------------------------
VKBO_WFS = "https://geo.api.vlaanderen.be/VKBO/wfs"
VKBO_TYPENAME = "VKBO:Vkbo"
# Checked against DescribeFeatureType on 2026-10-04. Never a name
# (Maatschappelijke_naam, Commerciele_naam, Afgekorte_naam, Zoeknaam),
# Telefoonnummer, Email or a street field.
VKBO_FIELDS = ("Ondernemingsnr", "Type_onderneming", "KBO_NISCODE", "AR_postcode")
# Mandatory in the feature type (minOccurs 1, not nillable): the server sends
# them whatever propertyName says, so the fetch asks for them by name, pages
# on OIDN, and does not store them.
VKBO_SERVER_FIELDS = ("UIDN", "OIDN")
VKBO_CRS_URN = "urn:ogc:def:crs:EPSG::31370"
VKBO_CRS = "EPSG:31370"
# Belgium in Lambert 72, with a margin: VKBO's (0,0) placeholder falls outside.
# Real points measured: Antwerp X 142,832-159,587, Y 189,996-229,745; Ghent X
# 94,726-115,970, Y 186,462-208,371 (the briefs).
LAMBERT72_BELGIUM = (17_000.0, 15_000.0, 300_000.0, 250_000.0)  # x0, y0, x1, y1

# Column names that may never appear in any frame this leg writes or returns.
PERSONAL_COLUMN = r"(?i)naam|name|telefoon|phone|email|e-mail|straat|street|huisnr|busnr"


def assert_no_personal_columns(df, where):
    import re
    bad = [c for c in df.columns if re.search(PERSONAL_COLUMN, str(c))
           and c not in ("business_name",)]
    if bad:
        sys.exit(f"{where}: column(s) {bad} could carry a name or contact detail - refused")


def read_favv(postcodes, fetch_script):
    """FAVV rows in `postcodes`, one row per establishment, classified.

    Returns (establishments, extract_date). Columns: op, postcodes, communes,
    favv_pairs, code (the place type shown, or empty), bucket, reason."""
    if not FAVV_CSV.exists():
        sys.exit(f"missing {FAVV_CSV}: run python {fetch_script}")
    head = pd.read_csv(FAVV_CSV, encoding=FAVV_ENCODING, dtype=str, nrows=0)
    for i, name in FAVV_COLUMNS.items():
        if head.columns[i] != name:
            sys.exit(f"FAVV column {i} is {head.columns[i]!r}, not {name!r} - the file changed")
    df = pd.read_csv(FAVV_CSV, encoding=FAVV_ENCODING, dtype=str, keep_default_na=False,
                     usecols=list(FAVV_COLUMNS))
    df = df.rename(columns=FAVV_RENAME)
    dates = sorted(set(df["extract_date"]))
    if len(dates) != 1:
        sys.exit(f"FAVV carries {len(dates)} extract dates: {dates[:3]}")
    extract = dates[0].split(" ")[0].replace("/", "-")
    print(f"  FAVV: {len(df):,} rows in Belgium, extract of {extract}")
    df = df[df["postcode"].isin(postcodes)]
    absent = sorted(set(postcodes) - set(df["postcode"]))
    if absent:
        sys.exit(f"FAVV has no row in postcode(s) {absent}")
    print(f"  FAVV: {len(df):,} rows in the {len(postcodes)} postcodes, "
          f"{df['op'].nunique():,} establishments")
    pairs = (df["pla"].str.strip().str.upper() + "/" + df["act"].str.strip().str.upper())
    df = df.assign(pair=pairs)
    g = df.groupby("op")
    est = pd.DataFrame({
        "favv_pairs": g["pair"].agg(lambda s: tax.PAIR_SEP.join(sorted(set(s)))),
        "postcodes": g["postcode"].agg(lambda s: " ".join(sorted(set(s)))),
        "communes": g["commune"].agg(lambda s: " | ".join(sorted(set(s)))),
    })
    if (est["postcodes"].str.contains(" ")).any():
        n = int(est["postcodes"].str.contains(" ").sum())
        print(f"    note: {n} establishment(s) listed under more than one postcode")
    cls = est["favv_pairs"].map(tax.establishment_class)
    est["code"] = cls.map(lambda c: c[0] or "")
    est["bucket"] = cls.map(lambda c: c[1] if c[0] else "")
    est["reason"] = cls.map(lambda c: "" if c[0] else c[1])
    est = est.reset_index()
    return est, extract


def read_vkbo(csv_paths, fetch_script):
    """The cached VKBO rows (number, type, NIS, AR postcode, Lambert 72 x, y)."""
    frames = []
    for p in csv_paths:
        if not p.exists():
            sys.exit(f"missing {p}: run python {fetch_script}")
        frames.append(pd.read_csv(p, dtype=str, keep_default_na=False))
    v = pd.concat(frames, ignore_index=True)
    want = list(VKBO_FIELDS) + ["x", "y"]
    if list(v.columns) != want:
        sys.exit(f"VKBO cache columns {list(v.columns)}, not {want}")
    assert_no_personal_columns(v, "VKBO cache")
    v["x"] = pd.to_numeric(v["x"], errors="coerce")
    v["y"] = pd.to_numeric(v["y"], errors="coerce")
    return v


def join(est, vkbo):
    """Establishments joined to VKBO, with `joined` and `placed` flags.

    Every establishment comes back (kept and out alike, so the caller can
    count both); `placed` rows carry latitude and longitude (EPSG:4326),
    the (0,0) placeholder never does."""
    from pyproj import Transformer

    units = vkbo[vkbo["Ondernemingsnr"].str.match(r"^2\d{9}$")]
    dup = units["Ondernemingsnr"].duplicated(keep=False)
    if dup.any():
        # One establishment unit under two NIS codes (Borsbeek's move into
        # Antwerp): the rows must agree on the point, else the join is ambiguous.
        d = units[dup].groupby("Ondernemingsnr")[["x", "y"]].nunique()
        if (d > 1).any().any():
            sys.exit(f"{int((d > 1).any(axis=1).sum())} VKBO establishment number(s) carry "
                     f"two different points - the join would be ambiguous")
        units = units.drop_duplicates("Ondernemingsnr")
        print(f"    VKBO: {int(dup.sum())} rows repeat an establishment number at one point; "
              f"kept once")
    j = est.merge(units[["Ondernemingsnr", "Type_onderneming", "KBO_NISCODE", "AR_postcode",
                         "x", "y"]],
                  left_on="op", right_on="Ondernemingsnr", how="left")
    joined = j["Ondernemingsnr"].notna()
    x0, y0, x1, y1 = LAMBERT72_BELGIUM
    real = joined & j["x"].between(x0, x1) & j["y"].between(y0, y1)
    j["joined"], j["placed"] = joined, real
    j["longitude"], j["latitude"] = float("nan"), float("nan")
    lon, lat = Transformer.from_crs(VKBO_CRS, "EPSG:4326", always_xy=True).transform(
        j.loc[real, "x"].values, j.loc[real, "y"].values)
    j.loc[real, "longitude"], j.loc[real, "latitude"] = lon, lat
    return j.drop(columns=["Ondernemingsnr"])


def run_step2(cfg, city, fetch_script):
    """Step 2 for a Flemish city: FAVV -> classified establishments -> VKBO
    points -> inside the commune polygon -> businesses_clean.csv. Every stage
    is printed; the figures the drift check watches are emitted."""
    import geopandas as gpd

    from pipeline.baseline import emit
    from pipeline.countries.belgium import commune_geometry
    from pipeline.taxonomies import filter_to_storefront

    label = city.capitalize()
    print(f"{label} step 2: FAVV-AFSCA's food operators on VKBO's points\n")
    est, extract = read_favv(cfg.POSTCODES, fetch_script)

    def cls(r):
        if r["code"]:
            return tax.legend_label(r["bucket"])
        return r["reason"]
    est["class"] = est.apply(cls, axis=1)
    print("\n  establishments by class (first match, fixed order):")
    for c, n in est["class"].value_counts().items():
        print(f"    {n:>6,}  {c}")
    kept = est[est["code"] != ""]
    print("  kept, by the place type shown:")
    for code in tax.ORDER:
        n = int((kept["code"] == code).sum())
        print(f"    {code:<5} {tax.PIN_LABEL[code]:<12} {n:>6,}")
    both = est["favv_pairs"].map(lambda s: tax.CATERER in {p for p, _ in tax.parse_pairs(s)})
    print(f"  caterers also registered as a kept type (kept by that type): "
          f"{int((both & (est['code'] != '')).sum())}")

    vk = read_vkbo([cfg.VKBO_CSV], fetch_script)
    x0, y0, x1, y1 = LAMBERT72_BELGIUM
    zero = ~(vk["x"].between(x0, x1) & vk["y"].between(y0, y1))
    print(f"\n  VKBO: {len(vk):,} rows " + str(vk["KBO_NISCODE"].value_counts().to_dict())
          + f"; by type {vk['Type_onderneming'].value_counts().to_dict()}; on the (0,0) "
          f"placeholder or off Belgium {int(zero.sum()):,}")
    real = vk[~zero]
    print(f"  VKBO real points: X {real['x'].min():,.0f}-{real['x'].max():,.0f}, "
          f"Y {real['y'].min():,.0f}-{real['y'].max():,.0f} (Lambert 72)")

    j = join(est, vk)
    rows = []
    for c in list(dict.fromkeys(["Food service", "Food shops"] + list(est["class"].unique()))):
        m = j["class"] == c
        if not m.any():
            continue
        n, nj, npl = int(m.sum()), int((m & j["joined"]).sum()), int((m & j["placed"]).sum())
        internal = int((m & ~j["joined"] & j["op"].str.startswith("9")).sum())
        rows.append((c, n, nj, npl, internal))
    print(f"\n  {'class':<62} {'FAVV':>6} {'joined':>7} {'placed':>7} {'rate':>6}  "
          f"(misses with a FAVV-internal number)")
    for c, n, nj, npl, internal in rows:
        print(f"  {c[:62]:<62} {n:>6,} {nj:>7,} {npl:>7,} {npl / n:>6.1%}  ({internal})")
    jt = j[j["joined"] & (j["code"] != "")]
    print(f"  kept and joined, by VKBO unit type: {jt['Type_onderneming'].value_counts().to_dict()}")

    p = j[j["placed"] & (j["code"] != "")].copy()
    box = getattr(cfg, f"{city.upper()}_BBOX")
    in_box = p["latitude"].between(box["lat_min"], box["lat_max"]) & \
        p["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"\n  {len(p):,} kept establishments placed; {int((~in_box).sum())} outside the sanity "
          f"box")
    poly = gpd.GeoSeries([commune_geometry(cfg.OSM_COMMUNES_JSON, fetch_script, cfg.OWN_NIS,
                                           cfg.COMMUNE_AREA_KM2, label)],
                         crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED).iloc[0]
    pts = gpd.GeoSeries(gpd.points_from_xy(p["longitude"], p["latitude"]), index=p.index,
                        crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED)
    inside = pts.within(poly)
    out_by = p.loc[~inside, "KBO_NISCODE"].value_counts().to_dict()
    print(f"  {int((~inside).sum())} placed outside {label}'s polygon (NIS {cfg.OWN_NIS}), "
          f"dropped; by VKBO NIS code {out_by}")
    p = p[inside & in_box]

    if cfg.BORSBEEK_POSTCODE:
        bb = est["postcodes"].str.split().map(lambda s: cfg.BORSBEEK_POSTCODE in s)
        arrived = p["postcodes"].str.split().map(lambda s: cfg.BORSBEEK_POSTCODE in s)
        print(f"\n  Borsbeek ({cfg.BORSBEEK_POSTCODE}): FAVV establishments {int(bb.sum())}, kept "
              f"{int((bb & (est['code'] != '')).sum())} (food service "
              f"{int((bb & (est['bucket'] == 'Food service')).sum())}, food shops "
              f"{int((bb & (est['bucket'] == 'Retail')).sum())}); placed inside "
              f"{int(arrived.sum())} (VKBO NIS {p.loc[arrived, 'KBO_NISCODE'].value_counts().to_dict()})")
        if not arrived.any():
            sys.exit("no Borsbeek (2150) premises arrived inside the city - the merger scope failed")
        emit("borsbeek_placed", int(arrived.sum()))

    out = shown_columns(p)
    kept_rows = filter_to_storefront(out, cfg.TAXONOMY_SYSTEM)
    if len(kept_rows) != len(out):
        sys.exit(f"filter_to_storefront kept {len(kept_rows)} of {len(out)}: the module and the "
                 f"join disagree")
    out = out.sort_values(["favv_code", "latitude", "longitude"]).reset_index(drop=True)
    out.to_csv(cfg.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    counts = out["favv_code"].map(tax.BUCKET).map(tax.legend_label).value_counts()
    print(f"\n  {len(out):,} food premises -> {cfg.BUSINESSES_CLEAN_CSV.relative_to(cfg.ROOT)} "
          f"(FAVV extract {extract})")
    print("    " + ", ".join(f"{b} {n:,}" for b, n in counts.items()))
    print(f"    columns: {list(out.columns)}")
    emit("favv_establishments", len(est))
    emit("kept_establishments", int((est["code"] != "").sum()))
    emit("food_service", int(counts.get("Food service", 0)))
    emit("food_shops", int(counts.get("Food shops", 0)))
    emit("storefronts", len(out))
    return extract


def shown_columns(placed):
    """The columns a city's businesses_clean.csv carries: the type in place of a
    name (Berlin's precedent), FAVV's own category, the pairs classify() reads,
    the point and the postcode. No establishment number."""
    out = pd.DataFrame({
        "business_name": placed["code"].map(tax.PIN_LABEL),
        "latitude": placed["latitude"].round(7),
        "longitude": placed["longitude"].round(7),
        tax.VALUE_COLUMN: placed["code"].map(tax.FAVV_DESCRIPTION),
        "favv_pairs": placed["favv_pairs"],
        "favv_code": placed["code"],
        "postcode": placed["AR_postcode"].where(placed["AR_postcode"] != "", placed["postcodes"]),
        "vkbo_nis": placed["KBO_NISCODE"],
    })
    assert_no_personal_columns(out, "businesses_clean")
    return out
