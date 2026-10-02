"""Seattle (Regional) step 1: Link's 1 and 2 Line stations, the two lines as
GeoJSON, each station's city, and the area businesses are drawn from.

    python pipeline/seattle/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap route-relation membership (the osm-rail skill), on
the ground recorded in config: a whitelist on network + ref + route; every
other relation in the box is named in config.NOT_DRAWN or the step exits.
Stations are the kept relations' `stop` members, collapsed by name. Each line
is written from the relation with the most TRACK geometry, track ways only.

Pinehurst opened on 2026-09-30, after the relations were last edited: it is
placed from Sound Transit's own station page (its street address, joined to
King County's address points) and the step refuses the addition once OSM's
relations carry the station.

Every station lies in one of the eleven station cities, so nothing is
excluded: excluded_stations.csv is written with a header and no rows
(Calgary's precedent), and station_municipalities.csv names each station's
city (Miami's).
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, mapping
from shapely.ops import linemerge

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.seattle import config  # noqa: E402

COLLAPSE_MAX_SPREAD_M = 200


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/seattle/fetch_sources.py")
    return path


def track(rel):
    return [m for m in rel["members"] if m["type"] == "way" and m.get("geometry")
            and not m.get("role", "").startswith("platform")]


def station_cities():
    """The station cities and every other place a ring can reach, as one
    GeoDataFrame with a `city` column: King County's polygons (unincorporated
    King County under one label) and TIGER's two Snohomish places."""
    kc = gpd.read_file(read_cached(config.KC_CITIES_GEOJSON, "King County cities"))
    kc = kc.to_crs(config.CRS_GEOGRAPHIC)
    kc["city"] = kc["CITYNAME"].fillna("").str.strip()
    kc.loc[kc["city"].isin(["", config.KC_UNINCORPORATED_CITYNAME]), "city"] = \
        config.UNINCORPORATED
    sno = gpd.read_file(read_cached(config.SNO_CITIES_GEOJSON, "Snohomish places"))
    sno = sno.to_crs(config.CRS_GEOGRAPHIC)
    sno["city"] = sno["BASENAME"]
    if sorted(sno["city"]) != ["Lynnwood", "Mountlake Terrace"]:
        sys.exit(f"TIGER returned {sorted(sno['city'])}, not Lynnwood and Mountlake Terrace")
    places = pd.concat([kc[["city", "geometry"]], sno[["city", "geometry"]]], ignore_index=True)
    places = gpd.GeoDataFrame(places, geometry="geometry", crs=config.CRS_GEOGRAPHIC)
    return places.dissolve("city").reset_index()


def pinehurst_point():
    """Sound Transit's Pinehurst page gives 13110 5th Ave NE, Seattle: the
    King County address point for that address."""
    spec = config.STATIONS_ADDED["Pinehurst"]
    pts = pd.read_csv(read_cached(config.KC_ADDRESS_CSV, "King County address points"),
                      usecols=["ADDR_FULL", "latitude", "longitude"], dtype={"ADDR_FULL": str})
    hit = pts[pts["ADDR_FULL"].fillna("").str.upper() == spec["address"]]
    if hit.empty:
        sys.exit(f"no King County address point at {spec['address']}")
    return float(hit["latitude"].mean()), float(hit["longitude"].mean())


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    els = json.loads(read_cached(config.OSM_ROUTES_JSON, "rail relations")
                     .read_text(encoding="utf-8"))["elements"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = [e for e in els if e["type"] == "relation"]

    def line_of(t):
        if t.get("network") == config.NETWORK and t.get("route") == "light_rail":
            return next((k for k, v in config.LINE_REFS.items() if t.get("ref") == v), None)
        return None

    print("  route relations in the box:")
    keep, rows = {}, []
    for r in sorted(rels, key=lambda r: r["id"]):
        t = r["tags"]
        line = line_of(t)
        print(f"    {'KEEP' if line else 'drop':4} {r['id']:>9} {t.get('route', ''):10} "
              f"{t.get('network', '-'):<18} {t.get('ref', '-'):<7} {t.get('name', '')}")
        if not line:
            if r["id"] not in config.NOT_DRAWN:
                sys.exit(f"relation {r['id']} ({t.get('name')}) is neither kept nor named "
                         f"in config.NOT_DRAWN - a line this step cannot place")
            continue
        keep.setdefault(line, []).append(r)
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nt = (n or {}).get("tags", {})
            if not n or nt.get("public_transport") != "stop_position" or not nt.get("name"):
                sys.exit(f"stop member {m['ref']} is not a named stop_position")
            rows.append({"node": n["id"], "stop_name": nt["name"], "line": line,
                         "latitude": n["lat"], "longitude": n["lon"]})
    for line in config.LINE_REFS:
        if len(keep.get(line, [])) != 2:
            sys.exit(f"{len(keep.get(line, []))} relations for the {config.LINE_REFS[line]}, "
                     f"not the two directions")

    q = pd.DataFrame(rows)
    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_ALIASES)
    for name in config.STATIONS_ADDED:
        if name in set(q["stop_name"]):
            sys.exit(f"OSM's relations now carry {name}: delete it from "
                     f"config.STATIONS_ADDED and re-run")
    per_line = q.groupby("line")["stop_name"].nunique()
    positions = q.drop_duplicates("node")
    by_name = positions.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean"),
                                                 positions=("node", "nunique")).reset_index()
    g = gpd.GeoDataFrame(positions, geometry=gpd.points_from_xy(positions.longitude,
                                                                positions.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(positions)} stop positions -> {len(by_name)} stations by name; widest "
          f"{spread.idxmax()} {spread.max():.0f} m")
    if (spread > COLLAPSE_MAX_SPREAD_M).any():
        sys.exit(f"names wider than {COLLAPSE_MAX_SPREAD_M} m: "
                 f"{spread[spread > COLLAPSE_MAX_SPREAD_M].round().to_dict()}")
    lines_of = q.groupby("stop_name")["line"].agg(lambda s: ";".join(sorted(set(s))))
    by_name["lines"] = by_name["stop_name"].map(lines_of)

    # Stations Sound Transit serves that the relations do not yet carry.
    added = []
    for name, spec in config.STATIONS_ADDED.items():
        lat, lon = pinehurst_point() if name == "Pinehurst" else (spec["lat"], spec["lon"])
        added.append({"stop_name": name, "latitude": lat, "longitude": lon, "positions": 0,
                      "lines": ";".join(spec["lines"])})
        print(f"  added {name} ({spec['opened']}), from {spec['source']}")
    by_name = pd.concat([by_name, pd.DataFrame(added)], ignore_index=True)
    counts = {config.LINE_REFS[k]: int(per_line.get(k, 0))
              + sum(k in s["lines"] for s in config.STATIONS_ADDED.values())
              for k in config.LINE_REFS}

    print()
    station_gates.verify_stations(
        city="Seattle (Regional)", platforms=positions, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=counts)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    if len(by_name) != config.OPERATOR_STATION_TOTAL:
        sys.exit(f"{len(by_name)} stations, against Sound Transit's {config.OPERATOR_STATION_TOTAL}")
    if counts != config.OPERATOR_STATION_COUNTS:
        sys.exit("a line's station count disagrees with Sound Transit's own pages")

    # --- Each station's city ----------------------------------------------
    places = station_cities()
    pts = gpd.GeoDataFrame(by_name, geometry=gpd.points_from_xy(by_name.longitude,
                                                                by_name.latitude),
                           crs=config.CRS_GEOGRAPHIC)
    joined = gpd.sjoin(pts, places, how="left", predicate="within")
    if joined["city"].isna().any() or joined.index.duplicated().any():
        sys.exit(f"stations in no place or two: {sorted(joined[joined['city'].isna()].stop_name)}")
    by_name["city"] = joined["city"].values
    print("\n  stations by city:")
    print(by_name["city"].value_counts().to_string())
    outside = by_name[~by_name["city"].isin(config.STATION_CITIES)]
    if len(outside):
        sys.exit(f"stations outside the eleven station cities: {sorted(outside.stop_name)}")
    by_name.rename(columns={"stop_name": "station", "city": "municipality"})[
        ["station", "lines", "municipality", "latitude", "longitude"]].sort_values(
        ["municipality", "station"]).to_csv(config.STATION_CITIES_CSV, index=False,
                                            encoding="utf-8")
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")

    nn = pts.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  max {d.max():,.0f}")
    if d.median() < 966:
        sys.exit("median under the 0.6 mi outer ring: the standard rings were chosen above it")

    # --- The business scope: the station cities, plus every ring ---------
    ring = nn.buffer(config.RING_EDGES_METERS[-1]).union_all()
    cities = places[places["city"].isin(config.STATION_CITIES)].to_crs(
        config.CRS_PROJECTED).geometry.union_all()
    scope = cities.union(ring)
    proj = places.to_crs(config.CRS_PROJECTED)
    # Ring area in no loaded polygon: unincorporated Snohomish County, beside
    # Lynnwood (config). Named as a place of its own, so step 2 can label it.
    gap = ring.difference(proj.geometry.union_all())
    if gap.area > 1e4:
        south = gpd.GeoSeries([gap], crs=config.CRS_PROJECTED).to_crs(
            config.CRS_GEOGRAPHIC).total_bounds[1]
        if south < config.SNO_GAP_MIN_LAT:
            sys.exit(f"ring area in no loaded place reaches south to {south:.3f}: not "
                     f"only Snohomish County's unincorporated land")
        proj = pd.concat([proj, gpd.GeoDataFrame({"city": [config.SNO_UNINCORPORATED]},
                                                 geometry=[gap], crs=config.CRS_PROJECTED)],
                         ignore_index=True)
    proj.to_crs(config.CRS_GEOGRAPHIC).to_file(config.PLACES_GEOJSON, driver="GeoJSON")
    reach = proj.assign(ring_km2=proj.geometry.intersection(ring).area / 1e6)
    reach = reach[(reach["ring_km2"] > 0.005) & ~reach["city"].isin(config.STATION_CITIES)]
    print("\n  rings reaching beyond the station cities (km2 of ring):")
    for _, r in reach.sort_values("ring_km2", ascending=False).iterrows():
        print(f"    {r['city']:<28} {r['ring_km2']:.2f}")
    gpd.GeoDataFrame({"scope": ["business scope"]}, geometry=[scope],
                     crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC).to_file(
        config.SCOPE_GEOJSON, driver="GeoJSON")
    print(f"  business scope: {scope.area / 1e6:,.1f} km2 -> {config.SCOPE_GEOJSON.name}")

    out = by_name.rename(columns={"stop_name": "station"})[
        ["station", "lines", "latitude", "longitude"]].sort_values("station")
    out.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    # --- The lines: per line, the relation with the most track, track only --
    feats = []
    for line, rs in keep.items():
        best = max(rs, key=lambda r: (sum(len(m["geometry"]) for m in track(r)), -r["id"]))
        merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                            for m in track(best)]))
        parts = list(getattr(merged, "geoms", [merged]))
        length = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(
            config.CRS_PROJECTED).length.sum() / 1000
        print(f"  {config.LINE_REFS[line]}: relation {best['id']}, {len(parts)} piece(s), "
              f"{length:.1f} km")
        feats.append({"type": "Feature", "properties": {"line": line},
                      "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection",
                                                "features": feats}), encoding="utf-8")

    emit("stop_positions", len(positions))
    emit("stations_in_scope", len(out))
    for k, v in counts.items():
        emit(f"stations_{k.replace(' ', '_').lower()}", v)


if __name__ == "__main__":
    main()
