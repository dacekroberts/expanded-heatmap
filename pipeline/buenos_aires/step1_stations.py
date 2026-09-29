"""Step 1 - Buenos Aires' Subte stations and lines, from SBASE's own layers,
cross-checked against OpenStreetMap.

THE SOURCE ORDER IS osm-rail's: agency GIS layers first. SBASE (Subterráneos
de Buenos Aires, the city company that owns the Subte) publishes
`estaciones_de_subte.geojson` (90 station points, one per line served) and
`red_subte.geojson` (98 track segments) on BA Data. The brief had reached for
OSM because the city's GTFS feed ships without a `routes.txt`; the layers were
found at the build (owner's download OK 2026-09-28).

WHAT EACH SOURCE SUPPLIES, and why:

  * POSITIONS AND LINE GEOMETRY: SBASE. Every one of its 98 segments lies
    within 30 m of OSM's route (measured 2026-09-28). Línea E's segments are
    drawn twice over (21.5 km of segments on an 11.9 km footprint), so each
    line is dissolved before it is written.
  * STATION NAMES: OSM's, matched to each SBASE point on the same line. SBASE's
    names drop accents and title-case articles ("Peru", "Plaza De Miserere"),
    and one is out of date ("Beata Mama Antula", canonised in 2024). An SBASE
    point with no OSM stop nearby keeps SBASE's name and is printed.
  * GATE 3: SBASE's own per-line counts against the stations this step keeps,
    and OSM's route-relation stops as an independent cross-check.

THE COLLAPSE: an interchange under ONE name (Retiro, on C and E) is one
station; interchanges under different names (Perú, Catedral, Bolívar) stay
separate, as in every other city. A name at two places a kilometre apart
(Pueyrredón, on B and D) stays two stations, shown with line letters.

The Premetro is left out (owner, 2026-09-28: it would add 749 storefronts, 1.2%,
in Villa Lugano, Villa Soldati and Villa Riachuelo). Its OSM relations are
still counted, so a change to it is seen.
"""

import json
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import MultiLineString, mapping
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
    LINES_GEOJSON,
    OSM_BOUNDARY_ADMIN_LEVEL,
    OSM_BOUNDARY_JSON,
    OSM_BOUNDARY_NAME,
    OSM_BOUNDARY_RELATION,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    PREMETRO_REF,
    SBASE_LINES_GEOJSON,
    SBASE_STATIONS_GEOJSON,
    STATIONS_CSV,
)

# CABA is about 203 km2; wide enough for OSM edits, narrow enough to catch a
# ring that did not close.
BOUNDARY_AREA_KM2_MIN = 190.0
BOUNDARY_AREA_KM2_MAX = 215.0

# SBASE's layer, 2026-09-01: 90 stations. Gate 3 compares the stations this
# step keeps per line against these, and OSM's stop members against both.
PUBLISHED_STATIONS_PER_LINE = {
    "Línea A": 18,
    "Línea B": 17,
    "Línea C": 9,
    "Línea D": 16,
    "Línea E": 18,
    "Línea H": 12,
}

# OSM spelling -> one name per station, applied before matching. Línea C's two
# directions spell two stations differently.
OSM_NAME_ALIASES = {
    "Esmeralda y Lavalle": "Lavalle",
    "Independencia (C)": "Independencia",
}

# An SBASE point and an OSM stop on the same line are the same station within
# this; SBASE's points sit at the station, OSM's at each direction's stop
# position.
NAME_MATCH_M = 150.0

# Two points with one name are one station within this; same-name interchanges
# sit within a few hundred metres, Pueyrredón B / D about a kilometre apart.
SAME_STATION_M = 450.0


def read_json(path, label):
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
    data = read_json(OSM_BOUNDARY_JSON, "boundary")
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


def projected(df):
    g = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                      crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    return g.x.to_numpy(), g.y.to_numpy()


def osm_stops():
    """Every stop member of the Subte's OSM route relations: ref, name, point."""
    st = read_json(OSM_STATIONS_JSON, "OSM stop nodes")
    rt = read_json(OSM_ROUTES_JSON, "OSM routes")
    nodes = {e["id"]: e for e in st["elements"] if e["type"] == "node"}
    rels = [e for e in rt["elements"] if e["type"] == "relation"]
    subway = [r for r in rels if r["tags"].get("route") == "subway"]
    premetro = [r for r in rels if r["tags"].get("route") == "tram"
                and r["tags"].get("ref") == PREMETRO_REF]
    other = [r for r in rels if r not in subway and r not in premetro]
    if other:
        raise SystemExit(f"unexpected Subte-network relations: "
                         f"{[(r['tags'].get('route'), r['tags'].get('ref')) for r in other]}")
    refs = sorted({r["tags"].get("ref") for r in subway})
    if refs != sorted(LINE_NAMES):
        raise SystemExit(f"OSM subway refs {refs} != {sorted(LINE_NAMES)}")
    rows = []
    for r in subway:
        for m in r["members"]:
            if m["type"] != "node" or not str(m.get("role", "")).startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            if n is None:
                raise SystemExit(f"stop member {m['ref']} is missing from osm_stations.json.")
            name = (n.get("tags", {}).get("name") or "").strip()
            rows.append({"ref": r["tags"]["ref"], "name": OSM_NAME_ALIASES.get(name, name),
                         "latitude": n["lat"], "longitude": n["lon"]})
    print(f"  OSM: {len(subway)} subway relations, {len(premetro)} Premetro "
          f"({'drawn' if DRAW_PREMETRO else 'not drawn'})")
    return pd.DataFrame(rows), len(premetro)


def sbase_stations():
    data = read_json(SBASE_STATIONS_GEOJSON, "SBASE stations")
    rows = []
    for f in data["features"]:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"][:2]
        rows.append({"sbase_id": p["id"], "ref": (p.get("linea") or "").strip().upper(),
                     "sbase_name": (p.get("estacion") or "").strip(),
                     "latitude": lat, "longitude": lon})
    df = pd.DataFrame(rows)
    bad = sorted(set(df["ref"]) - set(LINE_NAMES))
    if bad or df["sbase_name"].eq("").any():
        raise SystemExit(f"SBASE stations: unknown lines {bad} or unnamed points.")
    return df


def name_from_osm(sb, osm):
    """Each SBASE point takes the name of the nearest OSM stop on its own line."""
    sx, sy = projected(sb)
    ox, oy = projected(osm)
    names, dists = [], []
    for i, ref in enumerate(sb["ref"]):
        on_line = np.where(osm["ref"].to_numpy() == ref)[0]
        d = np.hypot(ox[on_line] - sx[i], oy[on_line] - sy[i])
        j = on_line[int(d.argmin())]
        dists.append(float(d.min()))
        names.append(osm["name"].iloc[j] if d.min() <= NAME_MATCH_M else None)
    sb = sb.assign(osm_name=names, osm_m=np.round(dists, 0))
    unmatched = sb[sb["osm_name"].isna()]
    for _, r in unmatched.iterrows():
        print(f"  no OSM stop within {NAME_MATCH_M:.0f} m of SBASE {r['ref']} "
              f"{r['sbase_name']!r} ({r['osm_m']:.0f} m); SBASE's name kept")
    sb["name"] = sb["osm_name"].fillna(sb["sbase_name"])
    renamed = sb[sb["osm_name"].notna() & (sb["osm_name"].map(fold) != sb["sbase_name"].map(fold))]
    print(f"  OSM names matched: {int(sb['osm_name'].notna().sum())} of {len(sb)} "
          f"(median {sb['osm_m'].median():.0f} m); spelled differently by SBASE: {len(renamed)}")
    return sb, renamed


def collapse(points):
    """Group by folded name, split any name whose points lie farther apart than
    SAME_STATION_M, merge the rest into one station."""
    points = points.copy()
    points["key"] = points["name"].map(fold)
    points["x"], points["y"] = projected(points)
    points["place"] = -1
    place = 0
    for _key, idx in points.groupby("key").groups.items():
        unassigned = set(idx)
        while unassigned:
            seed = unassigned.pop()
            cluster, frontier = {seed}, [seed]
            while frontier:
                i = frontier.pop()
                near = [j for j in list(unassigned)
                        if np.hypot(points.at[i, "x"] - points.at[j, "x"],
                                    points.at[i, "y"] - points.at[j, "y"]) <= SAME_STATION_M]
                for j in near:
                    unassigned.discard(j)
                    cluster.add(j)
                    frontier.append(j)
            points.loc[list(cluster), "place"] = place
            place += 1
    grouped = (points.groupby("place")
               .agg(key=("key", "first"), name=("name", "first"),
                    latitude=("latitude", "mean"), longitude=("longitude", "mean"),
                    refs=("ref", lambda s: "".join(sorted(set(s)))))
               .reset_index())
    split = grouped[grouped.duplicated("key", keep=False)]
    for key in sorted(split["key"].unique()):
        parts = split[split["key"] == key]
        print(f"  one name, {len(parts)} places: {parts['name'].iloc[0]!r} on "
              f"{', '.join(parts['refs'])} - shown with line letters")
        for i in parts.index:
            grouped.at[i, "name"] = f"{grouped.at[i, 'name']} ({'/'.join(grouped.at[i, 'refs'])})"
    points["station"] = points["place"].map(grouped.set_index("place")["name"])
    return points, grouped


def write_lines():
    """Each line's SBASE segments dissolved to one (Multi)LineString."""
    data = read_json(SBASE_LINES_GEOJSON, "SBASE lines")
    segs = {}
    for f in data["features"]:
        ref = (f["properties"].get("nombre") or "").split()[-1].upper()
        segs.setdefault(ref, []).append(f["geometry"])
    if sorted(segs) != sorted(LINE_NAMES):
        raise SystemExit(f"SBASE line layer refs {sorted(segs)} != {sorted(LINE_NAMES)}")
    feats = []
    for ref in LINE_NAMES:
        geoms = gpd.GeoDataFrame.from_features(
            [{"type": "Feature", "properties": {}, "geometry": g} for g in segs[ref]]).geometry
        before = geoms.set_crs(CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).length.sum() / 1000
        merged = linemerge(unary_union(list(geoms)))
        after = gpd.GeoSeries([merged], crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).length.iloc[0] / 1000
        parts = 1 if merged.geom_type == "LineString" else len(merged.geoms)
        print(f"  {LINE_NAMES[ref]}: {len(segs[ref])} segments, {before:.1f} km -> "
              f"{after:.1f} km dissolved, {parts} part(s)")
        feats.append({"type": "Feature", "properties": {"line": ref}, "geometry": mapping(merged)})
    LINES_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                             encoding="utf-8")
    print(f"  {len(feats)} lines -> {LINES_GEOJSON.name}")


def main():
    print("=== Step 1: Buenos Aires Subte stations (SBASE, cross-checked with OSM) ===\n")
    print("Reading cached sources:")
    boundary = load_boundary()
    osm, n_premetro = osm_stops()
    sb = sbase_stations()
    print(f"  SBASE: {len(sb)} station points over lines {', '.join(sorted(sb['ref'].unique()))}")

    print("\nNames:")
    sb, renamed = name_from_osm(sb, osm)
    print("\nCollapse:")
    points, stations = collapse(sb)
    merged = stations[stations["refs"].str.len() > 1]
    print(f"  {len(points)} line-station points -> {len(stations)} stations; "
          f"same-name interchanges merged: {', '.join(merged['name']) or 'none'}")

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

    print("\nLines:")
    write_lines()

    # --- gate 3, and OSM as the independent cross-check -----------------------
    print("\n--- station verification ---")
    actual = {LINE_NAMES[r]: int(points.loc[points["ref"] == r, "station"].nunique())
              for r in LINE_NAMES}
    osm_count = {LINE_NAMES[r]: int(osm.loc[osm["ref"] == r, "name"].map(fold).nunique())
                 for r in LINE_NAMES}
    print(f"OSM route-relation stations per line: {osm_count}")
    if osm_count != PUBLISHED_STATIONS_PER_LINE:
        raise SystemExit("OSM's per-line count disagrees with SBASE's: find out which "
                         "is wrong before drawing.")
    st_out = kept.drop(columns="geometry").rename(columns={"name": "station"})
    verify_stations(
        city="Buenos Aires",
        platforms=osm[["name", "latitude", "longitude"]],
        stations=st_out,
        crs_projected=CRS_PROJECTED,
        expected_per_line=PUBLISHED_STATIONS_PER_LINE,
        actual_per_line=actual,
    )
    emit("sbase_points", len(sb))
    emit("osm_names_matched", int(sb["osm_name"].notna().sum()))
    emit("stations", len(st_out))
    emit("stations_outside_caba", len(outside))
    emit("premetro_relations", n_premetro)

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (st_out.sort_values("station")[["station", "latitude", "longitude"]]
     .to_csv(STATIONS_CSV, index=False))
    print(f"\nWrote {len(st_out)} stations to {STATIONS_CSV}")
    if len(renamed):
        print("\nSBASE spelling -> name used (OSM):")
        for _, r in renamed.sort_values(["ref", "sbase_id"]).iterrows():
            print(f"  {r['ref']}  {r['sbase_name']!r} -> {r['name']!r}")


if __name__ == "__main__":
    main()
