"""Thessaloniki step 2: the City's active-shop-licence layer, classified and
cut to the city.

Reads the cached WFS answer (fetch_sources.py), only the shop code, the
licensed activity, the municipal community and the point: the address
fields (address, street, number, zip, city) are never read into processed/
(the brief's privacy list). Reprojects EPSG:2100 to WGS84 on read, classifies
every row through pipeline/taxonomies/thessaloniki_adeies.py (which raises on
an unlisted activity), keeps the rows inside the Municipality of
Thessaloniki's OSM boundary, and labels each pin with its activity in English:
the layer has no name field (Florence's precedent).

Never prints a row: field values and counts only. Reads the cache and NEVER
fetches.

    python pipeline/thessaloniki/step2_clean_businesses.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.thessaloniki import config  # noqa: E402
from pipeline.thessaloniki.step1_stations import boundary_polygon  # noqa: E402

# Shops sharing one building share one point (26 points carry two to four
# rows, 2026-10-04); a point coinciding with more rows than this is a
# placeholder, not a building, and stops the step.
MAX_ROWS_PER_POINT = 4


def load():
    path = config.LICENCES_GEOJSON
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/thessaloniki/fetch_sources.py")
    payload = json.loads(path.read_text(encoding="utf-8"))
    crs = ((payload.get("crs") or {}).get("properties") or {}).get("name", "")
    if not crs.endswith(config.LAYER_CRS.split(":")[1]):
        sys.exit(f"the layer's crs member is {crs!r}, not {config.LAYER_CRS}: re-read the "
                 f"axis order before reprojecting")
    feats = payload["features"]
    lo, hi = config.LICENCES_ROWS
    if not lo <= len(feats) <= hi or len(feats) != payload.get("numberMatched"):
        sys.exit(f"{len(feats)} features (numberMatched {payload.get('numberMatched')}), "
                 f"outside {lo}-{hi}")
    rows = []
    for f in feats:
        p, g = f["properties"], f.get("geometry") or {}
        xy = g.get("coordinates") if g.get("type") == "Point" else None
        # The layer's own x and y fields are read only to check the axis
        # order of the geometry; they are not kept.
        rows.append({"shop_code": p.get("kodikos_katasthmatos"),
                     "activity": p.get("antikeimeno"),
                     "community": p.get("dimotiki_koinotita"),
                     "gx": xy[0] if xy else np.nan, "gy": xy[1] if xy else np.nan,
                     "fx": p.get("x"), "fy": p.get("y")})
    return pd.DataFrame(rows)


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    df = load()
    n = len(df)
    print(f"Loaded {n:,} rows from {config.LICENCES_GEOJSON.name}")
    emit("rows_read", n)

    # Axis order: the geometry against the layer's own x/y fields.
    both = df.dropna(subset=["gx", "gy", "fx", "fy"])
    off = (np.hypot(both.gx - both.fx.astype(float), both.gy - both.fy.astype(float)) > 1.0).sum()
    swapped = (np.hypot(both.gx - both.fy.astype(float), both.gy - both.fx.astype(float)) <= 1.0).sum()
    print(f"  geometry vs the x/y fields: {len(both):,} rows carry both, {int(off)} differ by "
          f"over 1 m, {int(swapped)} match swapped")
    if off or swapped:
        sys.exit("the geometry does not match the layer's x/y fields: check the axis order")
    df = df.drop(columns=["fx", "fy"])

    # Classification over every row: unlisted values raise in the taxonomy.
    row = lambda a: {tax.VALUE_COLUMN: a}  # noqa: E731
    df["bucket"] = [tax.classify(row(a)) for a in df.activity]
    df["reason"] = [tax.out_reason(row(a)) for a in df.activity]
    catch = sum(tax.is_catchall(row(a)) for a in df.activity)
    blank = int((df.activity.fillna("").str.strip() == "").sum())
    named_catch = catch - blank
    print(f"  {df.activity.nunique(dropna=False)} distinct activity values (blank counted)")
    print(f"  catch-all: {named_catch} 'ANEY' ({named_catch / n:.2%}), {blank} blank; "
          f"together {catch} ({catch / n:.2%})")
    emit("catchall_rows", catch)

    print("  out, by reason:")
    for reason, k in Counter(r for r in df.reason if isinstance(r, str)).most_common():
        print(f"    {k:>5,}  {reason}")
    kept = filter_to_storefront(df, config.TAXONOMY_SYSTEM).copy()
    print(f"  storefront activities: {n:,} -> {len(kept):,}")
    emit("storefront_rows", len(kept))

    no_point = kept.gx.isna() | kept.gy.isna()
    if no_point.any():
        sys.exit(f"{int(no_point.sum())} kept rows without a point")
    to_ll = Transformer.from_crs(config.LAYER_CRS, config.CRS_GEOGRAPHIC, always_xy=True)
    lon, lat = to_ll.transform(kept.gx.values, kept.gy.values)
    kept["longitude"], kept["latitude"] = np.round(lon, 6), np.round(lat, 6)
    b = config.THESSALONIKI_BBOX
    if not (kept.latitude.between(b["lat_min"], b["lat_max"]).all()
            and kept.longitude.between(b["lon_min"], b["lon_max"]).all()):
        sys.exit("reprojected points leave the city's box: check the CRS and the axis order")

    bad = set(kept.community.dropna()) - set(config.COMMUNITIES)
    if bad or kept.community.isna().any():
        sys.exit(f"unknown or missing community labels on kept rows: {sorted(bad)}")
    if kept.shop_code.isna().any() or kept.shop_code.duplicated().any():
        sys.exit("a kept row without a shop code, or a code twice")

    poly, _rel, _area = boundary_polygon(verbose=False)
    pts = gpd.GeoSeries(gpd.points_from_xy(kept.longitude, kept.latitude), crs=config.CRS_GEOGRAPHIC,
                        index=kept.index)
    inside = pts.within(poly)
    if (~inside).any():
        d = (gpd.GeoSeries([poly.boundary], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
             .iloc[0])
        dist = pts[~inside].to_crs(config.CRS_PROJECTED).distance(d)
        print(f"  outside the city's OSM boundary: {int((~inside).sum())} rows, "
              f"{dist.median():.0f} m median and {dist.max():.0f} m at most beyond the line; "
              f"communities {dict(Counter(kept.community[~inside]))}")
    else:
        print("  outside the city's OSM boundary: 0 rows")
    # Dropped, Florence's precedent (the Comune's own layers cut by its OSM
    # polygon): 5 rows, 18 m median and 60 m at most past OSM's line, each
    # carrying a Thessaloniki community label (2026-10-07).
    emit("outside_boundary", int((~inside).sum()))
    kept = kept[inside].copy()

    per_point = kept.groupby(["latitude", "longitude"]).size()
    print(f"  {len(per_point):,} distinct points; {int((per_point > 1).sum())} carry 2 to "
          f"{int(per_point.max())} rows")
    if per_point.max() > MAX_ROWS_PER_POINT:
        sys.exit(f"a point carries {int(per_point.max())} rows: a placeholder, not a building")

    kept["business_name"] = [tax.label(row(a)) for a in kept.activity]
    print("  kept, by bucket:")
    for bucket in ("Food service", "Retail", "Personal services"):
        k = int((kept.bucket == bucket).sum())
        print(f"    {tax.layer_label(bucket):<18} {k:>6,}")
        emit(f"bucket_{bucket.lower().replace(' ', '_')}", k)
    print("  kept, by community: " + ", ".join(f"{c} {k:,}" for c, k in
                                              Counter(kept.community).most_common()))

    out = kept[["shop_code", "business_name", "activity", "community", "latitude", "longitude"]]
    out = out.sort_values("shop_code").reset_index(drop=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
