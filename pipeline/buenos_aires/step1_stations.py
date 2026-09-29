"""Step 1 - Buenos Aires' Subte stations, from OpenStreetMap.

Monterrey's shape (osm-rail): stations are the stop members of the Subte's
route relations, never nodes selected by tag. Every member here is a
`railway=stop` stop position, one per direction, so the collapse is by name
across the two directions of each line - with two corrections the relations
need:

  * LINE A HAS TWO ONE-DIRECTION STATIONS. Pasco is served eastbound only and
    Alberti westbound only, so neither direction's relation lists 18 stops but
    the line has 18 stations. Collapsing both directions counts them right.
  * LÍNEA C SPELLS TWO STATIONS TWO WAYS ("Lavalle" / "Esmeralda y Lavalle",
    "Independencia" / "Independencia (C)"). `NAME_ALIASES` folds them onto
    the operator's names.

AND A NAME IS NOT A PLACE. Pueyrredón is two separate stations about a
kilometre apart (Línea B under Corrientes, Línea D under Santa Fe), so a
name-only collapse would fuse them into one point between the two. The collapse
groups by folded name AND distance (`SAME_STATION_M`); a name that survives as
two places is shown with its line letters. Interchanges under ONE name
(Retiro, Independencia) merge; interchanges under different names (Perú,
Catedral, Bolívar) stay separate stations, as in every other city.

The Premetro's relations are read and counted, and drawn only if
`DRAW_PREMETRO` - the owner's call pending a coverage measurement.
"""

import json
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.stations import verify_stations
from pipeline.buenos_aires.config import (
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DRAW_PREMETRO,
    EXCLUDED_STATIONS_CSV,
    LINE_NAMES,
    OSM_BOUNDARY_ADMIN_LEVEL,
    OSM_BOUNDARY_JSON,
    OSM_BOUNDARY_NAME,
    OSM_BOUNDARY_RELATION,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    PREMETRO_REF,
    STATIONS_CSV,
)

# CABA is 203 km2 (INDEC); a band wide enough for OSM edits, narrow enough to
# catch a ring that did not close.
BOUNDARY_AREA_KM2_MIN = 190.0
BOUNDARY_AREA_KM2_MAX = 215.0

# The operator's station counts per line (gate 3). TODO-free only once cited:
# see OPERATOR_COUNTS_SOURCE.
PUBLISHED_STATIONS_PER_LINE = {
    "Línea A": 18,
    "Línea B": 17,
    "Línea C": 9,
    "Línea D": 16,
    "Línea E": 18,
    "Línea H": 12,
}

# OSM spelling -> the operator's, applied before the collapse.
NAME_ALIASES = {
    "Esmeralda y Lavalle": "Lavalle",
    "Independencia (C)": "Independencia",
}

# Two stop positions with one folded name are one station if within this;
# measured 2026-09-28: same-name interchanges sit within a few hundred metres,
# and the one same-name pair on different streets (Pueyrredón B / D) is ~1 km.
SAME_STATION_M = 450.0


def read_cached(path, label):
    """Read a raw input fetch_sources.py downloaded. This step never fetches."""
    if not path.exists():
        raise SystemExit(f"Missing {path.name} ({label}). "
                         "Run pipeline/buenos_aires/fetch_sources.py first.")
    print(f"  {label}: {path.name} ({path.stat().st_size:,} bytes)")
    return json.loads(path.read_text(encoding="utf-8"))


def fold(name):
    nfkd = unicodedata.normalize("NFKD", name)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).casefold().strip()


def load_boundary():
    """CABA as one polygon. Step 3 reads it too, for label anchoring."""
    data = read_cached(OSM_BOUNDARY_JSON, "boundary")
    rels = [e for e in data["elements"] if e["type"] == "relation"]
    if len(rels) != 1 or rels[0]["id"] != OSM_BOUNDARY_RELATION:
        raise SystemExit(f"expected relation {OSM_BOUNDARY_RELATION} alone, got "
                         f"{[r['id'] for r in rels]}")
    tags = rels[0]["tags"]
    if (tags.get("name"), tags.get("admin_level")) != (OSM_BOUNDARY_NAME, OSM_BOUNDARY_ADMIN_LEVEL):
        raise SystemExit(f"relation {OSM_BOUNDARY_RELATION} is now "
                         f"{tags.get('name')!r} at admin_level {tags.get('admin_level')}.")
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rels[0]["members"]
             if m.get("type") == "way" and m.get("role") == "outer" and m.get("geometry")]
    poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
    area = gpd.GeoSeries([poly], crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).area.iloc[0] / 1e6
    print(f"  CABA boundary: {area:,.1f} km2")
    if not BOUNDARY_AREA_KM2_MIN <= area <= BOUNDARY_AREA_KM2_MAX:
        raise SystemExit(f"CABA area {area:,.0f} km2 outside "
                         f"{BOUNDARY_AREA_KM2_MIN:,.0f}-{BOUNDARY_AREA_KM2_MAX:,.0f}.")
    return poly


def stop_rows(rels, nodes):
    rows = []
    for r in rels:
        ref = r["tags"].get("ref")
        for m in r["members"]:
            if m["type"] != "node" or not str(m.get("role", "")).startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            if n is None:
                raise SystemExit(f"stop member {m['ref']} of {ref} is missing from "
                                 "osm_stations.json - a partial Overpass result.")
            name = (n.get("tags", {}).get("name") or "").strip()
            if not name:
                raise SystemExit(f"unnamed stop member {m['ref']} on {ref}.")
            name = NAME_ALIASES.get(name, name)
            rows.append({"ref": ref, "name": name, "latitude": n["lat"], "longitude": n["lon"]})
    return pd.DataFrame(rows)


def collapse(stops):
    """Group by folded name, then split any name whose stop positions lie
    farther apart than SAME_STATION_M (single-linkage in UTM metres)."""
    stops = stops.copy()
    stops["key"] = stops["name"].map(fold)
    xy = gpd.GeoSeries(gpd.points_from_xy(stops["longitude"], stops["latitude"]),
                       crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    stops["x"], stops["y"] = xy.x.values, xy.y.values
    stops["place"] = -1
    place = 0
    for _key, idx in stops.groupby("key").groups.items():
        idx = list(idx)
        unassigned = set(idx)
        while unassigned:
            seed = unassigned.pop()
            cluster, frontier = {seed}, [seed]
            while frontier:
                i = frontier.pop()
                near = [j for j in list(unassigned)
                        if np.hypot(stops.at[i, "x"] - stops.at[j, "x"],
                                    stops.at[i, "y"] - stops.at[j, "y"]) <= SAME_STATION_M]
                for j in near:
                    unassigned.discard(j)
                    cluster.add(j)
                    frontier.append(j)
            stops.loc[list(cluster), "place"] = place
            place += 1
    grouped = (stops.groupby("place")
               .agg(key=("key", "first"),
                    name=("name", lambda s: max(sorted(set(s)), key=lambda v: sum(ord(c) > 127 for c in v))),
                    latitude=("latitude", "mean"), longitude=("longitude", "mean"),
                    refs=("ref", lambda s: "".join(sorted(set(s)))),
                    positions=("name", "size"))
               .reset_index())
    split = grouped[grouped.duplicated("key", keep=False)]
    for key in sorted(split["key"].unique()):
        parts = split[split["key"] == key]
        print(f"  one name, {len(parts)} places: {parts['name'].iloc[0]!r} on "
              f"{', '.join(parts['refs'])} - shown with line letters")
        for i in parts.index:
            grouped.at[i, "name"] = f"{grouped.at[i, 'name']} ({'/'.join(grouped.at[i, 'refs'])})"
    stops["station"] = stops["place"].map(grouped.set_index("place")["name"])
    return stops, grouped


def main():
    print("=== Step 1: Buenos Aires Subte stations (OpenStreetMap) ===\n")
    print("Reading cached OSM:")
    st_data = read_cached(OSM_STATIONS_JSON, "stations")
    rt_data = read_cached(OSM_ROUTES_JSON, "routes")
    boundary = load_boundary()

    rels = [e for e in rt_data["elements"] if e["type"] == "relation"]
    subway = [r for r in rels if r["tags"].get("route") == "subway"]
    premetro = [r for r in rels if r["tags"].get("route") == "tram"
                and r["tags"].get("ref") == PREMETRO_REF]
    other = [r for r in rels if r not in subway and r not in premetro]
    if other:
        raise SystemExit(f"unexpected Subte-network relations: "
                         f"{[(r['tags'].get('route'), r['tags'].get('ref')) for r in other]}")
    refs = sorted({r["tags"].get("ref") for r in subway})
    if refs != sorted(LINE_NAMES):
        raise SystemExit(f"subway refs {refs} != {sorted(LINE_NAMES)}")
    for ref in refs:
        n = sum(1 for r in subway if r["tags"].get("ref") == ref)
        if n != 2:
            raise SystemExit(f"Línea {ref}: {n} route relations, expected 2 (one per direction).")
    print(f"\nRoute relations: {len(subway)} subway over {', '.join(refs)}; "
          f"{len(premetro)} Premetro ({'drawn' if DRAW_PREMETRO else 'not drawn'})")

    nodes = {e["id"]: e for e in st_data["elements"] if e["type"] == "node"}
    drawn = subway + (premetro if DRAW_PREMETRO else [])
    stops = stop_rows(drawn, nodes)
    print(f"Stop positions on drawn lines: {len(stops)}")
    stops, stations = collapse(stops)
    print(f"Collapsed to {len(stations)} stations "
          f"(positions per station: {stations['positions'].value_counts().sort_index().to_dict()})")
    merged = stations[stations["refs"].str.len() > 1]
    print(f"  same-name interchanges merged: {', '.join(merged['name']) or 'none'}")

    gdf = gpd.GeoDataFrame(stations, geometry=gpd.points_from_xy(stations["longitude"],
                                                                 stations["latitude"]),
                           crs=CRS_GEOGRAPHIC)
    inside = gdf.within(boundary)
    kept, outside = gdf[inside].copy(), gdf[~inside].copy()
    print(f"\nInside CABA: {len(kept)}   outside: {len(outside)}")
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    b_proj = gpd.GeoSeries([boundary], crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).iloc[0]
    dist = (outside.to_crs(CRS_PROJECTED).geometry.apply(lambda g: g.distance(b_proj)).round(0)
            if len(outside) else pd.Series(dtype=float))
    (outside.drop(columns="geometry")
     .assign(distance_outside_m=dist.values,
             lines=outside["refs"].map(lambda s: ", ".join(LINE_NAMES.get(c, c) for c in s)))
     .rename(columns={"name": "station"})
     .reindex(columns=["station", "latitude", "longitude", "lines", "distance_outside_m"])
     .to_csv(EXCLUDED_STATIONS_CSV, index=False))
    print(f"  wrote {EXCLUDED_STATIONS_CSV.name} ({len(outside)} excluded)")

    # --- gate 3 ---------------------------------------------------------------
    print("\n--- station verification ---")
    actual = {}
    for ref, line in LINE_NAMES.items():
        actual[line] = int(stops.loc[stops["ref"] == ref, "station"].nunique())
    print(f"OSM stations per line (both directions): {actual}")
    print(f"Operator's published count             : {PUBLISHED_STATIONS_PER_LINE}")

    st_out = kept.drop(columns="geometry").rename(columns={"name": "station"})
    verify_stations(
        city="Buenos Aires",
        platforms=stops.rename(columns={"station": "_s"})[["name", "latitude", "longitude"]],
        stations=st_out,
        crs_projected=CRS_PROJECTED,
        expected_per_line=PUBLISHED_STATIONS_PER_LINE,
        actual_per_line=actual,
    )
    emit("stop_positions", len(stops))
    emit("stations", len(st_out))
    emit("stations_outside_caba", len(outside))
    emit("premetro_relations", len(premetro))

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (st_out.sort_values("station")[["station", "latitude", "longitude"]]
     .to_csv(STATIONS_CSV, index=False))
    print(f"\nWrote {len(st_out)} stations to {STATIONS_CSV}")


if __name__ == "__main__":
    main()
