"""Latvia's step 2, shared: food service from VID's excise register, shops and
services from VZD's cadastre premise groups (Riga's two layers).

Lifted from Riga's step 2 for the tram kit's second and third Latvian cities,
Liepāja and Daugavpils (the tram-city skill, section 4). Riga's step 2 is now
a thin call into this module, and the control is that Riga's output does not
move: `scripts/latvia_register_control.py` builds Riga's frame here and
compares it, row for row, with Riga's committed `businesses_clean.csv`.

THE CLASSIFICATION STAYS IN RIGA'S CONFIG. The excise columns, the food
pattern and the cadastre's name rules (NAME_RULES, NAME_KEEP, NAME_KIND) are
read from the city config passed in; a later Latvian city's config imports
them from `pipeline/riga/config.py`, where `category_continuity_table.py`
reads them by text. One set of rules for the country, decided once.

WHAT DIFFERS BY CITY, and is passed in:
  * the city name the excise address ends with (", Rīga, LV-1050");
  * the address points the food layer is placed on - Riga's own
    `adreses.gpkg`, or VZD's national address file `aw_eka.csv` elsewhere
    (`address_lut_gpkg`, `address_lut_aw_eka`);
  * the ATVK code naming the city's premise-group file and cadastral map;
  * Riga's list of degrading buildings, which no other city publishes.

Reads the cache and NEVER fetches. The register's holder and tax-number
columns are never read (cfg.EXCISE_NEVER, asserted).
"""
import csv
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

import geopandas as gpd
import pandas as pd

from pipeline.baseline import emit
from pipeline.taxonomies import filter_to_storefront


def need(path, fetch):
    if not path.exists():
        sys.exit(f"missing {path}.\nRun: python {fetch}")
    return path


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", str(s))).strip().casefold()


def city_suffix_re(city):
    """The tail an excise or VZD address carries for this city:
    ", Liepāja" or ", Liepāja, LV-3401"."""
    return rf", {re.escape(city)}(?:, LV-\d{{4}})?$"


# --- the address points the food layer is placed on --------------------------
def address_lut_gpkg(path, crs_source, crs_geographic="EPSG:4326"):
    """Riga's own address points: {norm(address): point}, first one wins."""
    pts = gpd.read_file(path)
    pts = pts.set_crs(crs_source) if pts.crs is None else pts
    pts = pts.to_crs(crs_geographic)
    lut = {}
    for a, geom in zip(pts["adrese"], pts.geometry):
        lut.setdefault(norm(a), geom)
    return lut


def address_lut_aw_eka(path, city):
    """VZD's national address file, one city's existing addresses:
    {norm(street address): point}.

    UTF-8 with a BOM (the CSVW metadata says ISO-8859-1; it is wrong). Only
    `STATUSS == EKS` (existing). KOORD_X is the NORTHING and KOORD_Y the
    easting in EPSG:3059, so the degree columns DD_N / DD_E are read instead.
    `STD` is the full address ("Esperanto iela 9, Liepāja, LV-3401"); the city
    and postcode are stripped to match the excise register's street part."""
    from shapely.geometry import Point

    a = pd.read_csv(path, usecols=["STATUSS", "STD", "DD_N", "DD_E"], dtype=str,
                    encoding="utf-8-sig", keep_default_na=False)
    tail = city_suffix_re(city)
    a = a[(a["STATUSS"] == "EKS") & a["STD"].str.contains(tail, regex=True)]
    if a.empty:
        sys.exit(f"no existing addresses in {city} in {path.name} - re-read it")
    lut = {}
    for std, n, e in zip(a["STD"].str.replace(tail, "", regex=True), a["DD_N"], a["DD_E"]):
        if n and e:
            lut.setdefault(norm(std), Point(float(e), float(n)))
    print(f"  VZD address points in {city}: {len(lut):,} (aw_eka.csv, existing only)")
    return lut


# --- layer 1: the excise register (food service) ------------------------------
FOOD_KINDS = [("Café", r"kafejn|kafe"), ("Restaurant", r"restor"), ("Pizzeria", r"picērij"),
              ("Bar", r"bār|pub\b|krog|klub"), ("Canteen or bistro", r"ēdn|ēdin|bistro|suši|burger|grill")]


def food_kind(t):
    """The first kind a place type names - "veikals-kafejnīca" is a café."""
    for label, rx in FOOD_KINDS:
        if re.search(rx, t):
            return label
    return "Other food service"


def excise_layer(cfg, *, excise_csv, city, lut, lut_label):
    """Current licences at a still-open place in `city` whose place type reads
    as food service, one row per ADDRESS and kind, placed on `lut`: exact,
    then with the unit after " - " dropped."""
    with open(excise_csv, encoding="utf-8-sig", newline="") as f:
        header = next(csv.reader(f))
    missing = [c for c in cfg.EXCISE_COLUMNS if c not in header]
    if missing:
        sys.exit(f"excise columns not in the header: {missing} - re-read it")
    # Every field is space-padded, and an EMPTY "place ended" is two spaces, not
    # a blank (measured 2026-09-24) - so strip everything and test for "".
    ex = pd.read_csv(excise_csv, usecols=cfg.EXCISE_COLUMNS, dtype=str, encoding="utf-8-sig",
                     keep_default_na=False).apply(lambda s: s.str.strip())
    assert not set(cfg.EXCISE_NEVER) & set(ex.columns), "a never-read column was loaded"
    print(f"excise register: {len(ex):,} licence rows nationally")
    emit("excise_rows", len(ex))
    tail = city_suffix_re(city)
    cur = ex[(ex["Statuss"] == cfg.EXCISE_CURRENT) & (ex["Darbiba_izbeigta_darbibas_vieta"] == "")]
    here = cur[cur["Darbibas_vietas_adrese"].str.contains(tail, na=False)].copy()
    print(f"  current, at a still-open place: {len(cur):,}; in {city}: {len(here):,}")
    here["type_norm"] = here["Darbibas_vietas_tips"].fillna("").map(norm)
    food = here[here["type_norm"].str.contains(cfg.FOOD_RE, regex=True)].copy()
    print(f"  food-service place types: {len(food):,} licence rows")
    food["street_addr"] = food["Darbibas_vietas_adrese"].str.replace(tail, "", regex=True)
    # One venue is described differently on each of its licences ("kafejnīca",
    # "Kafejnīca, 1. stāvs, 1. telpa"), so de-duplicate on its KIND, not the
    # wording: address + kind. Two venues of one kind at one address merge -
    # the holder that would separate them is never read.
    food["kind"] = food["type_norm"].map(food_kind)
    key = food["street_addr"].map(norm) + "|" + food["kind"]
    food = food[~key.duplicated()].copy()
    print(f"  one per address and kind: {len(food):,} premises  "
          + ", ".join(f"{k} {v:,}" for k, v in food["kind"].value_counts().items()))
    emit("food_premises", len(food))

    exact = food["street_addr"].map(lambda a: lut.get(norm(a)))
    stripped = food["street_addr"].str.replace(cfg.UNIT_SUFFIX_RE, "", regex=True)
    second = stripped.map(lambda a: lut.get(norm(a)))
    geom = exact.where(exact.notna(), second)
    n_exact, n_second = int(exact.notna().sum()), int((exact.isna() & second.notna()).sum())
    print(f"  placed on {lut_label}: exact {n_exact:,} ({n_exact / len(food):.1%}), "
          f"after dropping a unit {n_second:,} ({n_second / len(food):.1%}); unplaced "
          f"{int(geom.isna().sum()):,} ({geom.isna().mean():.1%})")
    emit("food_placed_exact", n_exact)
    emit("food_placed_unit_dropped", n_second)
    emit("food_unplaced", int(geom.isna().sum()))
    food = food[geom.notna()].copy()
    food["latitude"] = [g.y for g in geom.dropna()]
    food["longitude"] = [g.x for g in geom.dropna()]
    unit = food["street_addr"].str.contains(cfg.UNIT_SUFFIX_RE, regex=True)
    print(f"  of those, {int(unit.sum()):,} carry a unit number in the register's address")
    emit("food_with_unit_number", int(unit.sum()))
    # Displayed (owner, 2026-09-24): the STREET ADDRESS WITHOUT its unit number
    # as the dot's title - the shared tooltip shows the name field, so that is
    # where the address goes, as Rotterdam's shop units do - and the kind of
    # place as "Kind". The holder is never read.
    return pd.DataFrame({
        "record_id": "excise:" + food.index.astype(str),
        "source": "excise",
        "business_name": stripped[food.index],
        "address": stripped[food.index],
        "latitude": food["latitude"], "longitude": food["longitude"],
        "activity": food["kind"],
    })


# --- layer 2: the cadastre premise groups (shops and services) ----------------
def name_class(cfg, n):
    for cls, rx in cfg.NAME_RULES:
        if re.search(rx, n):
            return cls
    return "other_unmatched"


def cadastre_layer(cfg, *, premisegroup_zip, atvk, kk_zip, city, degrading_gpkg=None):
    """Premise groups of use class 1230 in ATVK `atvk` whose name reads as a
    shop or a personal service (cfg.NAME_RULES, first match wins), placed at
    their building's footprint centroid by building cadastre number. With
    `degrading_gpkg`, those in a building the city lists as degrading are
    dropped (Riga's list; no other city publishes one)."""
    z = zipfile.ZipFile(premisegroup_zip)
    xml = [n for n in z.namelist() if n.startswith(f"PremiseGroup/{atvk}_") and n.endswith(".xml")]
    if len(xml) != 1:
        sys.exit(f"expected one {city} (ATVK {atvk}) premise-group file, found {xml}")
    ns = cfg.CADASTRE_NS
    rows = []
    for _, el in ET.iterparse(z.open(xml[0]), events=("end",)):
        if el.tag != ns + "PremiseGroupItemData":
            continue
        b = el.find(ns + "PremiseGroupBasicData")
        if b.findtext(f"{ns}PremiseGroupUseKind/{ns}PremiseGroupUseKindId") == cfg.TRADE_USE_KIND:
            rows.append({"pg": b.findtext(ns + "PremiseGroupCadastreNr"),
                         "name": (b.findtext(ns + "PremiseGroupName") or "").strip(),
                         "floor": b.findtext(ns + "PremiseGroupBuildingFloor"),
                         "building": el.findtext(f"{ns}ObjectRelation/{ns}ObjectCadastreNr")})
        el.clear()
    pg = pd.DataFrame(rows)
    pg["cls"] = pg["name"].str.lower().map(lambda n: name_class(cfg, n))
    print(f"\ncadastre: {len(pg):,} premise groups of use class {cfg.TRADE_USE_KIND} in {city}")
    print("  by name: " + ", ".join(f"{k} {v:,}" for k, v in pg["cls"].value_counts().items()))
    emit("trade_premise_groups", len(pg))
    pg = pg[pg["cls"].isin(cfg.NAME_KEEP)].copy()
    print(f"  kept ({' + '.join(cfg.NAME_KEEP)}): {len(pg):,}")
    emit("shops_and_services_named", len(pg))

    kk = zipfile.ZipFile(kk_zip)
    parts = [n for n in kk.namelist() if n.endswith("KKBuilding.shp")]
    zp = kk_zip.as_posix()
    blds = pd.concat([gpd.read_file(f"zip://{zp}!{p}", columns=["CODE"]) for p in parts], ignore_index=True)
    blds = gpd.GeoDataFrame(blds, crs=cfg.CRS_SOURCE_LV)
    cent = dict(zip(blds["CODE"], blds.geometry.centroid))
    g = pg["building"].map(cent)
    print(f"  placed at their building's footprint: {int(g.notna().sum()):,} of {len(pg):,} "
          f"({g.notna().mean():.1%}), across {len(parts)} cadastral groups")
    emit("shops_placed", int(g.notna().sum()))
    pg = pg[g.notna()].copy()
    pts = gpd.GeoDataFrame(pg, geometry=list(g.dropna()), crs=cfg.CRS_SOURCE_LV).to_crs(
        cfg.CRS_GEOGRAPHIC)

    if degrading_gpkg is not None:
        deg = gpd.read_file(degrading_gpkg)
        bad = set(deg["cadastrename"].dropna())
        drop = pts["building"].isin(bad)
        print(f"  in a building the city lists as degrading ({len(bad):,} listed): "
              f"{int(drop.sum()):,} dropped")
        emit("shops_in_degrading_buildings", int(drop.sum()))
        pts = pts[~drop]
    return pd.DataFrame({
        "record_id": "cadastre:" + pts["pg"],
        "source": "cadastre",
        # The premises' registered name (the cadastre's own word, e.g. "Veikals")
        # as the title; whether it is a shop or a service as "Kind".
        "business_name": pts["name"].str.capitalize(),
        "address": "floor " + pts["floor"].fillna("?"),
        "latitude": pts.geometry.y, "longitude": pts.geometry.x,
        "activity": pts["cls"].map(cfg.NAME_KIND),
    })


def combine(cfg, layers, city_poly):
    """The two layers through filter_to_storefront, kept inside `city_poly`
    (EPSG:4326). Exits if the filter drops a row the layers already decided,
    or on a duplicate record."""
    df = pd.concat(layers, ignore_index=True)
    before = len(df)
    df = filter_to_storefront(df, cfg.TAXONOMY_SYSTEM)
    if len(df) != before:
        sys.exit("filter_to_storefront dropped rows the layers already decided")
    inside = gpd.GeoSeries(gpd.points_from_xy(df.longitude, df.latitude),
                           crs=cfg.CRS_GEOGRAPHIC).within(city_poly).values
    if (~inside).any():
        print(f"  {int((~inside).sum())} rows outside the city - dropped: "
              + ", ".join(f"{k} {v}" for k, v in df.loc[~inside, "source"].value_counts().items()))
    df = df[inside]
    if df["record_id"].duplicated().any():
        sys.exit("a record appears twice")
    print(f"\n  {len(df):,} storefronts: "
          + ", ".join(f"{k} {v:,}" for k, v in df["source"].value_counts().items()))
    emit("storefronts", len(df))
    return df


def utf8_console():
    """A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    Latvian letters. UTF-8 regardless of the console."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
