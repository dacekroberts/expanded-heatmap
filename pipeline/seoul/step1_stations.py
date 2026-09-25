"""Seoul step 1: the Seoul Metropolitan Subway's drawn lines, from OpenStreetMap.

Stations come from ROUTE-RELATION MEMBERSHIP (osm-rail), never a node tag
filter: the stop nodes of the relations whose ref is a drawn line's, collapsed
by Korean name and then by distance - two real stations share a name more than
once in the region (양평 is on Line 5 in Seoul and on the Gyeongui-Jungang Line
40 km east of it).

Stations inside Seoul are kept, every one of them (the owner's call: the
register is Seoul's, so the map is). Those outside are recorded in
excluded_stations.csv. The lines are still drawn to their ends.

Each drawn line is written to processed/rail_lines.json as ONE relation for
step 3: its longest relation plus only the track another relation adds (a
branch) - Hong Kong's rule.

Reads the cache and NEVER fetches.

    python pipeline/seoul/step1_stations.py
"""
import json
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.seoul import config  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402

TO_M = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
NAME_SOURCE = {}


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/seoul/fetch_sources.py osm")
    return path


def load_osm():
    els = json.loads(need(config.RAIL_OSM_JSON, "OSM rail relations").read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    if not rels:
        sys.exit("the rail file holds no relations - an empty result is not an empty city")
    return rels, nodes


def korean_key(name):
    """The collapse key: NFKC, no spaces, no trailing 역 ("station"), no
    parenthesised subtitle - 서울역 and 서울, 총신대입구(이수) and 총신대입구."""
    s = unicodedata.normalize("NFKC", name or "").split("(")[0].replace(" ", "").strip()
    if len(s) > 2 and s.endswith("역"):
        s = s[:-1]
    return config.KEY_ALIASES.get(s, s)


def stop_seq(rel, nodes, strict=True):
    """The relation's stop nodes in order: [(korean key, english, lat, lon)].
    strict=False (undrawn lines only) skips an unnamed node instead of stopping."""
    out = []
    for m in rel.get("members", []):
        if m["type"] != "node" or not m.get("role", "").startswith("stop"):
            continue
        n = nodes.get(m["ref"])
        if n is None:
            continue
        t = n.get("tags", {})
        ko = config.STOP_NAME_FIX.get(m["ref"]) or t.get("name:ko") or t.get("name") or ""
        key = korean_key(ko)
        if not key and not strict:
            continue
        if not key:
            sys.exit(f"stop node {m['ref']} on {rel['tags'].get('name')} has no name - "
                     f"name it rather than guess")
        en = ""
        for tag in config.ENGLISH_NAME_TAGS:
            if t.get(tag) and m["ref"] not in config.STOP_NAME_FIX:
                en = t[tag].strip()
                NAME_SOURCE[m["ref"]] = tag
                break
        if not en:
            NAME_SOURCE[m["ref"]] = None
        out.append((key, en, n["lat"], n["lon"]))
    return out


def ways_of(rel):
    return [(m["ref"], [(p["lat"], p["lon"]) for p in m["geometry"]])
            for m in rel.get("members", []) if m["type"] == "way" and m.get("geometry")]


def line_geometry(rels, nodes):
    """The longest relation, plus only the ways other relations add away from it."""
    rels = sorted(rels, key=lambda r: sum(len(g) for _, g in ways_of(r)), reverse=True)
    chosen, seen, covered = [], set(), set()
    drawn_m = None
    added_branch = 0
    for i, r in enumerate(rels):
        names = {s[0] for s in stop_seq(r, nodes)}
        if i and not (names - covered):
            continue
        for wid, g in ways_of(r):
            if wid in seen or len(g) < 2:
                continue
            if drawn_m is not None:
                mid = g[len(g) // 2]
                if drawn_m.distance(Point(TO_M.transform(mid[1], mid[0]))) <= config.BRANCH_MIN_M:
                    continue
                added_branch += 1
            chosen.append(g)
            seen.add(wid)
        covered |= names
        drawn_m = unary_union([LineString([TO_M.transform(lo, la) for la, lo in g]) for g in chosen])
    return chosen, added_branch


def boundary_polygon():
    els = json.loads(need(config.BOUNDARY_OSM_JSON, "Seoul boundary").read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation" and e["id"] == config.BOUNDARY_RELATION
            and e.get("tags", {}).get("name") == config.BOUNDARY_NAME]
    if len(rels) != 1:
        sys.exit(f"expected relation {config.BOUNDARY_RELATION} named {config.BOUNDARY_NAME}, "
                 f"got {len(rels)}")
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rels[0]["members"]
             if m["type"] == "way" and m.get("role") == "outer" and m.get("geometry")]
    poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
    area = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    print(f"  boundary: relation {rels[0]['id']} ({rels[0]['tags'].get('name:en')}), {area:,.0f} km2")
    if not lo <= area <= hi:
        sys.exit(f"boundary area {area:,.0f} km2 outside {lo}-{hi} - re-read the relation "
                 f"before changing the gate")
    return poly


def clusters(points, link_m):
    """Single-linkage groups of [(x, y)] at link_m: indices per group."""
    n = len(points)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = points[i], points[j]
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= link_m ** 2:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    rels, nodes = load_osm()

    by_ref = {spec[0]: k for k, spec in config.LINES.items()}
    groups = {k: [] for k in config.LINES}
    not_drawn = {}
    unplaced = []
    for r in rels:
        t = r.get("tags", {})
        ref = t.get("ref")
        if t.get("route") not in config.LINES_ROUTE_TYPES:
            continue
        if ref is None:
            # A few undrawn lines' relations carry no ref; they are placed by
            # name, and only as NOT drawn - a drawn line is never matched on text.
            ref = next((v for k, v in config.NOT_DRAWN_BY_NAME.items()
                        if (t.get("name") or "").startswith(k)), None)
        if ref in by_ref:
            groups[by_ref[ref]].append(r)
        elif ref in config.NOT_DRAWN:
            not_drawn.setdefault(ref, []).append(r)
        else:
            unplaced.append(f"{ref!r}: {t.get('name')}")
    if unplaced:
        sys.exit("metropolitan relations with an unplaced ref - place each in LINES or "
                 "NOT_DRAWN:\n  " + "\n  ".join(unplaced))
    print("Relations matched (ref on the RELATION):")
    for k, (ref, colour, name, _) in config.LINES.items():
        print(f"  {ref:<8} {name:<24} {len(groups[k]):>3} relations")
        if not groups[k]:
            sys.exit(f"no relation for {name}")
    for ref, rs in not_drawn.items():
        print(f"  {ref:<8} {config.NOT_DRAWN[ref]:<24} {len(rs):>3} relations - NOT drawn (owner)")

    # --- stations -------------------------------------------------------------
    plat = []
    for k in config.LINES:
        for r in groups[k]:
            for key, en, la, lo in stop_seq(r, nodes):
                plat.append({"key": key, "en": en, "latitude": la, "longitude": lo, "line": k})
    platforms = pd.DataFrame(plat).drop_duplicates()
    src = pd.Series(NAME_SOURCE).value_counts(dropna=False)
    print(f"\n  {len(platforms)} stop nodes; English name taken from: "
          + ", ".join(f"{i}: {n}" for i, n in src.items()))

    rows = []
    for key, g in platforms.groupby("key"):
        pts = [TO_M.transform(lo, la) for la, lo in zip(g.latitude, g.longitude)]
        parts = clusters(pts, config.COLLAPSE_LINK_M)
        for part in parts:
            sub = g.iloc[part]
            ens = [e for e in sub.en if e]
            en = pd.Series(ens).value_counts().index[0] if ens else ""
            lines = [k for k in config.LINES if k in set(sub.line)]
            rows.append({"key": key, "en": en, "latitude": sub.latitude.mean(),
                         "longitude": sub.longitude.mean(), "lines": lines,
                         "split": len(parts) > 1, "nodes": len(sub)})
    st = pd.DataFrame(rows)
    # The English name: the station object's (railway=station, same Korean name,
    # nearest within the collapse distance), else the stop nodes' own.
    objs = []
    for e in json.loads(need(config.STATION_OSM_JSON, "OSM station names").read_text(
            encoding="utf-8"))["elements"]:
        t = e.get("tags", {})
        la, lo = (e["lat"], e["lon"]) if e["type"] == "node" else (e["center"]["lat"], e["center"]["lon"])
        en = next((t[g].strip() for g in config.ENGLISH_NAME_TAGS if t.get(g)), "")
        if en:
            objs.append((korean_key(t.get("name:ko") or t.get("name")), en, *TO_M.transform(lo, la)))
    src = {"station object": 0, "stop node": 0}
    for i, r in st.iterrows():
        x, y = TO_M.transform(r.longitude, r.latitude)
        near = sorted(((ox - x) ** 2 + (oy - y) ** 2, en) for k, en, ox, oy in objs
                      if k == r.key and (ox - x) ** 2 + (oy - y) ** 2 <= config.COLLAPSE_LINK_M ** 2)
        if near:
            st.at[i, "en"] = near[0][1]
            src["station object"] += 1
        elif r.en:
            src["stop node"] += 1
    print(f"  English names: {src}")
    # Stations beyond the query box have no station object; they are outside
    # Seoul and are recorded by their Korean name. A Seoul station without an
    # English name stops the step below.
    poly = boundary_polygon()
    pts = gpd.GeoSeries(gpd.points_from_xy(st.longitude, st.latitude), crs=config.CRS_GEOGRAPHIC)
    st["in_seoul"] = pts.within(poly).values
    missing_en = st[(st.en == "") & st.in_seoul]
    if len(missing_en):
        sys.exit(f"Seoul stations with no English name in any tag: {list(missing_en.key)}")
    print(f"  {int((st.en == '').sum())} stations outside Seoul recorded by their Korean name")
    st["en"] = st.en.where(st.en != "", st.key)
    # A name shared by two real stations: each is labelled with its lines.
    for i in st.index[st.split]:
        st.at[i, "en"] = (f"{st.at[i, 'en']} "
                          f"({', '.join(config.LINES[k][2] for k in st.at[i, 'lines'])})")
    print(f"  {len(st)} stations under {st.key.nunique()} Korean names; "
          f"{int(st.split.sum())} stations share a name with another and carry their lines: "
          + "; ".join(st[st.split].en))
    st["station"] = st.en
    if st.station.duplicated().any():
        sys.exit(f"duplicate station names after the collapse: "
                 f"{list(st.station[st.station.duplicated()])}")

    # --- Seoul ------------------------------------------------------------------
    per_line = {config.LINES[k][2]: int(sum(k in ls for ls in st[st.in_seoul].lines))
                for k in config.LINES}
    print("\n  stations inside Seoul, per line:")
    for name, n in per_line.items():
        print(f"    {name:<24} {n:>3}")
    kept = st[st.in_seoul].copy()
    kept["lines"] = [" ".join(ls) for ls in kept.lines]

    xy = [TO_M.transform(lo, la) for la, lo in zip(kept.latitude, kept.longitude)]
    pairs = sorted((((xy[i][0] - xy[j][0]) ** 2 + (xy[i][1] - xy[j][1]) ** 2) ** 0.5,
                    kept.station.iloc[i], kept.station.iloc[j])
                   for i in range(len(xy)) for j in range(i + 1, len(xy)))[:4]
    print("  closest pairs: " + "; ".join(f"{a} / {b} {d:.0f} m" for d, a, b in pairs))
    station_gates.verify_stations(
        city="Seoul", platforms=platforms[platforms.key.isin(set(kept.key))],
        stations=kept, crs_projected=config.CRS_PROJECTED)
    emit("stop_nodes", len(platforms))
    emit("stations_all", len(st))
    emit("stations_kept", len(kept))

    out = st[~st.in_seoul].copy()
    out["lines"] = [" ".join(config.LINES[k][2] for k in ls) for ls in out.lines]
    # "outside" is the word app/station_scope.py reads.
    out["reason"] = "outside Seoul's boundary"
    out = out[["station", "lines", "reason", "latitude", "longitude"]].sort_values("station")
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} stations of drawn lines outside Seoul -> {config.EXCLUDED_STATIONS_CSV.name}")
    emit("stations_outside", len(out))

    # Seoul stations served ONLY by an undrawn line are disclosed in prose.
    drawn = set(kept.key)
    off_map = {}
    for ref, rs in not_drawn.items():
        for r in rs:
            for key, en, la, lo in stop_seq(r, nodes, strict=False):
                if key not in drawn and Point(lo, la).within(poly):
                    off_map.setdefault(en or key, config.NOT_DRAWN[ref])
    print("  in Seoul on an undrawn line only: "
          + ("; ".join(f"{n} ({why})" for n, why in sorted(off_map.items())) or "none"))
    emit("stations_off_map", len(off_map))

    kept = kept[["station", "key", "latitude", "longitude", "lines"]].sort_values("station")
    kept.rename(columns={"key": "name_ko"}).to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  wrote {config.STATIONS_CSV.name}: {len(kept)} stations")

    # --- the drawn lines -------------------------------------------------------
    elements = []
    print("\n  line geometry (longest relation + branch track the others add):")
    for k, (ref, colour, name, _) in config.LINES.items():
        ways, branch = line_geometry(groups[k], nodes)
        osm_colours = {r["tags"].get("colour", "").upper() for r in groups[k]} - {""}
        if osm_colours and osm_colours != {config.OSM_COLOUR.get(k, colour).upper()}:
            sys.exit(f"{name}: OSM colours {osm_colours} differ from config {colour}")
        elements.append({"type": "relation", "id": len(elements) + 1,
                         "tags": {"ref": ref, "name": name, "colour": colour},
                         "members": [{"type": "way", "geometry": [{"lat": la, "lon": lo} for la, lo in g]}
                                     for g in ways]})
        print(f"    {name:<24} {colour}  {len(ways):>4} ways ({branch} branch)")
    config.RAIL_LINES_JSON.write_text(json.dumps({"elements": elements}), encoding="utf-8")
    emit("lines_drawn", len(elements))


if __name__ == "__main__":
    main()
