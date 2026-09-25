"""Riga step 2: two layers - food service from the excise register, shops and
services from the cadastre's trade premise groups (docs/build_briefs/riga.md).

Layer 1, `excise`: current licences at a still-open place in Riga whose place
type reads as food service, one row per ADDRESS and place type (a premises
holds several licences - alcohol, tobacco, beer - and the holder is never read,
so de-duplication cannot be by holder). Placed by joining the address to Riga's
own address points: exact, then with the unit after " - " dropped.

Layer 2, `cadastre`: premise groups of use class 1230 whose name reads as a shop
or a personal service (config.NAME_RULES, first match wins), placed at their
building's footprint centroid by building cadastre number; those in a building
the city lists as degrading are dropped.

Reads the cache and NEVER fetches.

    python pipeline/riga/step2_clean_businesses.py
"""
import csv
import re
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.riga import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402


def need(name):
    p = config.DATA_RAW / name
    if not p.exists():
        sys.exit(f"missing {p}.\nRun: python pipeline/riga/fetch_sources.py")
    return p


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", str(s))).strip().casefold()


def to_wgs(gdf):
    return gdf.to_crs(config.CRS_GEOGRAPHIC)


# --- layer 1 -------------------------------------------------------------------
FOOD_KINDS = [("Café", r"kafejn|kafe"), ("Restaurant", r"restor"), ("Pizzeria", r"picērij"),
              ("Bar", r"bār|pub\b|krog|klub"), ("Canteen or bistro", r"ēdn|ēdin|bistro|suši|burger|grill")]


def food_kind(t):
    """The first kind a place type names - "veikals-kafejnīca" is a café."""
    for label, rx in FOOD_KINDS:
        if re.search(rx, t):
            return label
    return "Other food service"


def excise_layer():
    path = need("pdb_akclicences_odata.csv")
    with open(path, encoding="utf-8-sig", newline="") as f:
        header = next(csv.reader(f))
    missing = [c for c in config.EXCISE_COLUMNS if c not in header]
    if missing:
        sys.exit(f"excise columns not in the header: {missing} - re-read it")
    # Every field is space-padded, and an EMPTY "place ended" is two spaces, not
    # a blank (measured 2026-09-24) - so strip everything and test for "".
    ex = pd.read_csv(path, usecols=config.EXCISE_COLUMNS, dtype=str, encoding="utf-8-sig",
                     keep_default_na=False).apply(lambda s: s.str.strip())
    assert not set(config.EXCISE_NEVER) & set(ex.columns), "a never-read column was loaded"
    print(f"excise register: {len(ex):,} licence rows nationally")
    emit("excise_rows", len(ex))
    cur = ex[(ex["Statuss"] == config.EXCISE_CURRENT) & (ex["Darbiba_izbeigta_darbibas_vieta"] == "")]
    riga = cur[cur["Darbibas_vietas_adrese"].str.contains(r", Rīga(?:, LV-\d{4})?$", na=False)].copy()
    print(f"  current, at a still-open place: {len(cur):,}; in Riga: {len(riga):,}")
    riga["type_norm"] = riga["Darbibas_vietas_tips"].fillna("").map(norm)
    food = riga[riga["type_norm"].str.contains(config.FOOD_RE, regex=True)].copy()
    print(f"  food-service place types: {len(food):,} licence rows")
    food["street_addr"] = food["Darbibas_vietas_adrese"].str.replace(r", Rīga(?:, LV-\d{4})?$", "", regex=True)
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

    pts = gpd.read_file(need("adreses.gpkg"))
    pts = pts.set_crs(config.CRS_SOURCE_LV) if pts.crs is None else pts
    pts = to_wgs(pts)
    lut = {}
    for a, geom in zip(pts["adrese"], pts.geometry):
        lut.setdefault(norm(a), geom)
    exact = food["street_addr"].map(lambda a: lut.get(norm(a)))
    stripped = food["street_addr"].str.replace(config.UNIT_SUFFIX_RE, "", regex=True)
    second = stripped.map(lambda a: lut.get(norm(a)))
    geom = exact.where(exact.notna(), second)
    n_exact, n_second = int(exact.notna().sum()), int((exact.isna() & second.notna()).sum())
    print(f"  placed on Riga's address points: exact {n_exact:,} ({n_exact / len(food):.1%}), "
          f"after dropping a unit {n_second:,} ({n_second / len(food):.1%}); unplaced "
          f"{int(geom.isna().sum()):,} ({geom.isna().mean():.1%})")
    emit("food_placed_exact", n_exact)
    emit("food_placed_unit_dropped", n_second)
    emit("food_unplaced", int(geom.isna().sum()))
    food = food[geom.notna()].copy()
    food["latitude"] = [g.y for g in geom.dropna()]
    food["longitude"] = [g.x for g in geom.dropna()]
    unit = food["street_addr"].str.contains(config.UNIT_SUFFIX_RE, regex=True)
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


# --- layer 2 -------------------------------------------------------------------
def name_class(n):
    for cls, rx in config.NAME_RULES:
        if re.search(rx, n):
            return cls
    return "other_unmatched"


def cadastre_layer():
    z = zipfile.ZipFile(need("premisegroup.zip"))
    xml = [n for n in z.namelist() if n.startswith("PremiseGroup/0001000_") and n.endswith(".xml")]
    if len(xml) != 1:
        sys.exit(f"expected one Riga (ATVK 0001000) premise-group file, found {xml}")
    ns = config.CADASTRE_NS
    rows = []
    for _, el in ET.iterparse(z.open(xml[0]), events=("end",)):
        if el.tag != ns + "PremiseGroupItemData":
            continue
        b = el.find(ns + "PremiseGroupBasicData")
        if b.findtext(f"{ns}PremiseGroupUseKind/{ns}PremiseGroupUseKindId") == config.TRADE_USE_KIND:
            rows.append({"pg": b.findtext(ns + "PremiseGroupCadastreNr"),
                         "name": (b.findtext(ns + "PremiseGroupName") or "").strip(),
                         "floor": b.findtext(ns + "PremiseGroupBuildingFloor"),
                         "building": el.findtext(f"{ns}ObjectRelation/{ns}ObjectCadastreNr")})
        el.clear()
    pg = pd.DataFrame(rows)
    pg["cls"] = pg["name"].str.lower().map(name_class)
    print(f"\ncadastre: {len(pg):,} premise groups of use class {config.TRADE_USE_KIND} in Riga")
    print("  by name: " + ", ".join(f"{k} {v:,}" for k, v in pg["cls"].value_counts().items()))
    emit("trade_premise_groups", len(pg))
    pg = pg[pg["cls"].isin(config.NAME_KEEP)].copy()
    print(f"  kept (shop_retail + personal_service): {len(pg):,}")
    emit("shops_and_services_named", len(pg))

    kk = zipfile.ZipFile(need("0001000_kk_shp.zip"))
    parts = [n for n in kk.namelist() if n.endswith("KKBuilding.shp")]
    zp = (config.DATA_RAW / "0001000_kk_shp.zip").as_posix()
    blds = pd.concat([gpd.read_file(f"zip://{zp}!{p}", columns=["CODE"]) for p in parts], ignore_index=True)
    blds = gpd.GeoDataFrame(blds, crs=config.CRS_SOURCE_LV)
    cent = dict(zip(blds["CODE"], blds.geometry.centroid))
    g = pg["building"].map(cent)
    print(f"  placed at their building's footprint: {int(g.notna().sum()):,} of {len(pg):,} "
          f"({g.notna().mean():.1%}), across {len(parts)} cadastral groups")
    emit("shops_placed", int(g.notna().sum()))
    pg = pg[g.notna()].copy()
    pts = to_wgs(gpd.GeoDataFrame(pg, geometry=list(g.dropna()), crs=config.CRS_SOURCE_LV))

    deg = gpd.read_file(need("vidi_degradejosas_buves.gpkg"))
    bad = set(deg["cadastrename"].dropna())
    drop = pts["building"].isin(bad)
    print(f"  in a building the city lists as degrading ({len(bad):,} listed): {int(drop.sum()):,} dropped")
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
        "activity": pts["cls"].map({"shop_retail": "Shop", "personal_service": "Service"}),
    })


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.concat([excise_layer(), cadastre_layer()], ignore_index=True)
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    if len(df) != before:
        sys.exit("filter_to_storefront dropped rows the layers already decided")
    n, _, poly = __import__("pipeline.riga.step1_stations", fromlist=["city_polygon"]).city_polygon()
    inside = gpd.GeoSeries(gpd.points_from_xy(df.longitude, df.latitude), crs=config.CRS_GEOGRAPHIC).within(poly).values
    if (~inside).any():
        print(f"  {int((~inside).sum())} rows outside the city - dropped: "
              + ", ".join(f"{k} {v}" for k, v in df.loc[~inside, "source"].value_counts().items()))
    df = df[inside]
    if df["record_id"].duplicated().any():
        sys.exit("a record appears twice")
    print(f"\n  {len(df):,} storefronts: " + ", ".join(f"{k} {v:,}" for k, v in df["source"].value_counts().items()))
    emit("storefronts", len(df))
    df.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
