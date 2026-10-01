"""Step 2 - Florence's storefronts from the Comune di Firenze's four activity
layers.

Input:  data/florence/raw/{commercio_sede_fissa,pubblici_esercizi,
        attivita_estetiche,tintolavanderie}_od.json
        data/florence/raw/osm_comuni.json
Output: data/florence/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **No name and no address on any layer**: each row is an id, a point and a
    type. A dot shows its type, in English (florence_attivita.label()).
  * **The layer and its type decide the bucket**
    (pipeline/taxonomies/florence_attivita.py), every pair with a home; an
    unknown pair stops this step. Exempt food service is in (owner, call 16).
  * **Rows sharing a point are drawn as they are** (the brief: a building of
    several premises); the heat layer counts each.
  * **Placed by the layer's own point**, EPSG:3003, kept only inside the
    Comune di Firenze.

Run:  python pipeline/florence/step2_clean_businesses.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.florence import config  # noqa: E402
from pipeline.florence.comuni import FETCH, comune_geometry  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.florence_attivita import label  # noqa: E402


def load():
    frames = []
    for key, name in config.LAYERS.items():
        p = config.DATA_RAW / name
        if not p.exists():
            sys.exit(f"missing {p}\nRun: python {FETCH}")
        d = json.loads(p.read_text(encoding="utf-8"))
        crs = (((d.get("crs") or {}).get("properties") or {}).get("name") or "")
        if not crs.endswith("3003"):
            sys.exit(f"{name}: CRS {crs!r}, not EPSG:3003 - re-read the layer")
        rows = []
        for f in d["features"]:
            pr, g = f["properties"], f.get("geometry") or {}
            x, y = (g.get("coordinates") or [None, None])[:2]
            t = pr.get("tipologiaattivita")
            rows.append({"source": key, "id": f"{key}-{pr.get('id')}",
                         "tipologiaattivita": (t or "").strip(), "x": x, "y": y})
        df = pd.DataFrame(rows)
        print(f"  {key}: {len(df):,} rows")
        emit(f"rows_{key}", len(df))
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def main():
    df = load()
    print(f"Loaded {len(df):,} rows from the Comune's four layers")
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  storefront types: {before:,} -> {len(df):,}")
    emit("storefront_rows", len(df))

    no_point = df["x"].isna() | df["y"].isna()
    print(f"  no point: {int(no_point.sum()):,}")
    df = df[~no_point].copy()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["x"], df["y"]), crs=config.LAYER_CRS,
                        index=df.index).to_crs(config.CRS_GEOGRAPHIC)
    df["longitude"], df["latitude"] = pts.x.round(6), pts.y.round(6)
    inside = pts.within(comune_geometry())
    print(f"  outside the Comune di Firenze: {int((~inside).sum()):,}")
    emit("outside_comune", int((~inside).sum()))
    df = df[inside].copy()

    shared = df.duplicated(["latitude", "longitude"], keep=False)
    print(f"  rows sharing a point with another (drawn as they are): {int(shared.sum()):,}")

    df["business_name"] = [label({"source": s, "tipologiaattivita": t})
                           for s, t in zip(df["source"], df["tipologiaattivita"])]
    b = config.FLORENCE_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    out = df[["id", "source", "business_name", "tipologiaattivita", "latitude",
              "longitude"]].sort_values("id").reset_index(drop=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
