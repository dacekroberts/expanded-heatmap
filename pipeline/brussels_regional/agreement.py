"""The control's agreement half: KBO's filtered, placed units against
hub.brussels's street survey inside the City of Brussels, the only ground
truth (docs/build_briefs/brussels_regional.md, "Agreement with the survey").

The measurement is the screen's (staging, 2026-10-03), with the survey typed
by pipeline/taxonomies/brussels_hub.py, the City page's own taxonomy:

  * a survey row's COMPATIBLE buckets are the buckets of all its kept types
    (a "Boulangerie, Salon de thé" unit is Retail and Food service), and its
    bucket is brussels_hub.classify()'s (Food over Retail over Personal);
  * a KBO unit's buckets are those of all its in-bucket MAIN codes, and its
    bucket the priority's;
  * PRECISION, per bucket: of the KBO units on the City's four postcodes
    (KBO's postcode field) started on or before the survey date, the share
    with a survey row within the radius whose compatible buckets meet the
    unit's buckets;
  * RECALL, per bucket: of the survey's rows on the four postcodes in that
    bucket, the share with a KBO unit within the radius (any start date,
    anywhere in the Region) that carries the bucket.

Distances in EPSG:32631, never in degrees.
"""
import json

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely import STRtree

from pipeline.taxonomies import brussels_hub

BUCKETS = ("Retail", "Food service", "Personal services")


def hub_points(hub_json, postcodes, crs):
    """hub.brussels's rows on the given postcodes: bucket, compatible
    buckets and projected point."""
    rows = json.loads(hub_json.read_text(encoding="utf-8"))
    df = pd.DataFrame(rows)
    df = df[df["postalcode"].astype(str).isin(postcodes)].copy()
    col = brussels_hub.VALUE_COLUMN
    df["bucket"] = [brussels_hub.classify({col: v}) for v in df[col]]
    df["compat"] = [frozenset(brussels_hub.TYPE_TO_BUCKET[t] for t in brussels_hub.types_of(v)
                              if t in brussels_hub.TYPE_TO_BUCKET) for v in df[col]]
    df["lat"] = df["geo_point_2d"].map(lambda p: (p or {}).get("lat"))
    df["lon"] = df["geo_point_2d"].map(lambda p: (p or {}).get("lon"))
    df = df.dropna(subset=["lat", "lon"])
    g = gpd.GeoSeries(gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326").to_crs(crs)
    df["geom"] = list(g.values)
    return df


def _pairs(src, dst, radius):
    if not len(src) or not len(dst):
        return np.array([], dtype=int), np.array([], dtype=int)
    tree = STRtree(np.array(dst["geom"].tolist(), dtype=object))
    si, di = tree.query(np.array(src["geom"].tolist(), dtype=object), predicate="dwithin",
                        distance=radius)
    return si, di


def measure(evaluated, recall_pool, hub, radius):
    """evaluated: KBO units for precision; recall_pool: KBO units for recall.
    Both carry `bucket`, `bset` (frozenset) and a projected `geom`.
    Returns {bucket: {precision, recall, kbo_units, hub_shops, matched, found}}."""
    hb = hub[hub["bucket"].notna()].reset_index(drop=True)
    ev = evaluated.reset_index(drop=True)
    pool = recall_pool.reset_index(drop=True)
    si, di = _pairs(ev, hub, radius)
    ev_b, hub_c = ev["bset"].to_numpy(), hub["compat"].to_numpy()
    ok = np.array([bool(ev_b[a] & hub_c[c]) for a, c in zip(si, di)], dtype=bool)
    p_hit = np.zeros(len(ev), dtype=bool)
    p_hit[si[ok]] = True
    si, di = _pairs(hb, pool, radius)
    hb_b, pool_b = hb["bucket"].to_numpy(), pool["bset"].to_numpy()
    ok = np.array([hb_b[a] in pool_b[c] for a, c in zip(si, di)], dtype=bool)
    r_hit = np.zeros(len(hb), dtype=bool)
    r_hit[si[ok]] = True
    out = {}
    for b in BUCKETS:
        km = ev["bucket"].to_numpy() == b
        hm = hb_b == b
        n_k, n_h = int(km.sum()), int(hm.sum())
        out[b] = {
            "kbo_units": n_k, "hub_shops": n_h,
            "matched": int(p_hit[km].sum()), "found": int(r_hit[hm].sum()),
            "precision": round(100.0 * p_hit[km].mean(), 1) if n_k else None,
            "recall": round(100.0 * r_hit[hm].mean(), 1) if n_h else None,
        }
    return out
