"""Step 2 - Zurich's storefronts from the Stadt Zürich's Gastwirtschaftsbetriebe
register.

Input:  data/zurich/raw/gastwirtschaftsbetriebe.geojson   (the WFS layer)
        data/zurich/raw/osm_gemeinden.json
Output: data/zurich/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **One register, two buckets** (pipeline/taxonomies/zurich_gastwirtschaft.py):
    food service, and the shops, kiosks and petrol stations licensed to sell
    alcohol. Every `betriebsart` has a home; an unknown one stops this step.
  * **Every row is open**: the publisher publishes "Offen" rows only. A row
    with any other status stops this step rather than being dropped quietly.
  * **The dot shows the trade name** (`betriebsname`) and the kind of licence.
    A trade name that is a person's own name shows the street address instead
    (config.PERSON_NAMED, read by eye; Kansas City's and New Orleans's rule).
  * **Placed by the register's own LV95 point** (`ekoord`/`nkoord`,
    EPSG:2056), checked against the WFS's served WGS84 point, and kept only
    inside the Stadt Zürich.

Run:  python pipeline/zurich/step2_clean_businesses.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.zurich_gastwirtschaft import TYPES  # noqa: E402
from pipeline.zurich import config  # noqa: E402
from pipeline.zurich.gemeinden import FETCH, city_geometry  # noqa: E402

# The served WGS84 point and the LV95 point agree to well under this on every
# row (2026-09-30); a wider gap means the two columns no longer describe the
# same place.
POINT_AGREEMENT_M = 5.0


def load():
    p = config.REGISTER_JSON
    if not p.exists():
        sys.exit(f"missing {p}\nRun: python {FETCH}")
    feats = json.loads(p.read_text(encoding="utf-8"))["features"]
    cols = set(feats[0]["properties"])
    if cols != config.REGISTER_COLUMNS:
        sys.exit(f"register columns changed: {sorted(cols ^ config.REGISTER_COLUMNS)}")
    rows = []
    for f in feats:
        pr, g = f["properties"], f.get("geometry") or {}
        lon, lat = (g.get("coordinates") or [None, None])[:2]
        rows.append({k: pr.get(k) for k in (
            "objectid", "betriebsname", "betriebsart", "betriebsstatus", "jahr",
            "strasselang", "hnr", "plz", "ekoord", "nkoord")} | {"wfs_lon": lon, "wfs_lat": lat})
    return pd.DataFrame(rows)


def main():
    df = load()
    print(f"Loaded {len(df):,} rows from the Gastwirtschaftsbetriebe register")
    emit("rows", len(df))

    status = df["betriebsstatus"].value_counts().to_dict()
    print(f"  betriebsstatus: {status}; jahr: {df['jahr'].value_counts().to_dict()}")
    if set(status) != {"Offen"}:
        sys.exit("a row is not 'Offen' - the publisher says it publishes open premises only; "
                 "re-read the register before filtering")
    print("  betriebsart:")
    for v, n in df["betriebsart"].value_counts().items():
        bucket = TYPES.get(v, ("UNKNOWN",))[0]
        print(f"    {n:>5,}  {v:<34} -> {bucket or 'out'}")

    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  storefront types: {before:,} -> {len(df):,}")
    emit("storefront_rows", len(df))

    no_point = df["ekoord"].isna() | df["nkoord"].isna()
    print(f"  no LV95 point: {int(no_point.sum()):,}")
    df = df[~no_point].copy()
    lv95 = gpd.GeoSeries(gpd.points_from_xy(df["ekoord"], df["nkoord"]), crs=config.CRS_PROJECTED,
                         index=df.index)
    served = gpd.GeoSeries(gpd.points_from_xy(df["wfs_lon"], df["wfs_lat"]),
                           crs=config.CRS_GEOGRAPHIC, index=df.index).to_crs(config.CRS_PROJECTED)
    gap = lv95.distance(served)
    print(f"  LV95 point vs the WFS's WGS84 point: median {gap.median():.2f} m, "
          f"max {gap.max():.2f} m")
    if gap.max() > POINT_AGREEMENT_M:
        sys.exit(f"the LV95 and served points disagree by up to {gap.max():.0f} m - re-read")
    pts = lv95.to_crs(config.CRS_GEOGRAPHIC)
    df["longitude"], df["latitude"] = pts.x.round(6), pts.y.round(6)
    inside = pts.within(city_geometry())
    print(f"  outside the Stadt Zürich: {int((~inside).sum()):,}")
    emit("outside_city", int((~inside).sum()))
    df = df[inside].copy()

    df["address"] = (df["strasselang"].fillna("").str.strip() + " "
                     + df["hnr"].fillna("").astype(str).str.strip()).str.strip()
    name = df["betriebsname"].fillna("").str.strip()
    person = name.isin(config.PERSON_NAMED)
    gone = set(config.PERSON_NAMED) - set(name[person])
    if gone:
        sys.exit(f"PERSON_NAMED names no longer in the register: {sorted(gone)} - re-read "
                 f"the list against it")
    df["business_name"] = name.where(~person, df["address"])
    print(f"  trade names that are a person's own name (config.PERSON_NAMED), shown as the "
          f"address: {int(person.sum()):,}")
    still = ~person & name.map(looks_personal)
    print(f"  shown names shaped like a person's but read as trade names "
          f"(residence.py): {int(still.sum()):,}")
    emit("name_as_address", int(person.sum()))

    shared = df.duplicated(["latitude", "longitude"], keep=False)
    print(f"  rows sharing a point with another (drawn as they are): {int(shared.sum()):,}")

    b = config.ZURICH_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    out = (df.rename(columns={"objectid": "id"})
           [["id", "business_name", "betriebsart", "address", "latitude", "longitude"]]
           .sort_values("id").reset_index(drop=True))
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    by = out["betriebsart"].map(lambda v: TYPES[v][0]).value_counts().to_dict()
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)} "
          f"{by}")
    emit("premises", len(out))
    emit("food_service", int(by.get("Food service", 0)))
    emit("licensed_shops", int(by.get("Retail", 0)))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
