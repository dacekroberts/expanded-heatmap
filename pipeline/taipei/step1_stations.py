"""Taipei (Regional) step 1: every metro and light-rail line in Taipei and New
Taipei, from OpenStreetMap (owner, 2026-09-25).

Stations come from ROUTE-RELATION MEMBERSHIP (osm-rail), collapsed by Chinese
name and then by distance (Seoul's method). English names from the stop nodes'
name:en. Gate 3: Taipei Metro's own station list, line by line, for its lines.

Scope: stations in Taipei or New Taipei. No boundary polygon is read (Overpass
504ed on boundaries throughout 2026-09-25): a station is in the region when
each city's own door-plate file puts plates of that city around it - the
publishers' own data, two files that each cover exactly one city.

Each drawn line is written to processed/rail_lines.json as ONE relation: its
longest relation plus the track other relations add (Hong Kong's rule).

Reads the cache and NEVER fetches.

    python pipeline/taipei/step1_stations.py
"""
import csv
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.taipei import config  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402

TO_M = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
PLATE_TO_M = Transformer.from_crs(config.PLATE_CRS, config.CRS_PROJECTED, always_xy=True)


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/taipei/fetch_sources.py")
    return path


def zh_key(name):
    s = unicodedata.normalize("NFKC", name or "").split("(")[0].replace(" ", "").replace("台", "臺")
    return s[:-1] if len(s) > 2 and s.endswith("站") and not s.endswith("車站") else s


def english(name):
    """OSM's English name, cleaned: no status text in parentheses (R01 carries
    "(Under construction)" while its tags and the operator's list say it is a
    stop), no trailing "Station" except where the word is the name's own
    (Taipei Main Station, an HSR station)."""
    n = re.sub(r"\s*\((?:under construction)\)", "", name.strip(), flags=re.I)
    base = re.sub(r"\s+station$", "", n, flags=re.I)
    if base.lower().endswith(" main"):
        return base[:-5] + " Main Station"
    if base.endswith("HSR"):
        return base + " Station"
    return base


def line_of(rel):
    t = rel.get("tags", {})
    for key, spec in config.LINES.items():
        ref, name_has = spec["ref"], spec.get("name_has")
        if t.get("ref") == ref and (name_has is None or name_has in (t.get("name") or "")) \
                and not any(x in (t.get("name") or "") for x in spec.get("name_not", ())):
            return key
    return None


def stops_of(rel, nodes):
    out = []
    for m in rel.get("members", []):
        if m["type"] != "node" or not m.get("role", "").startswith("stop"):
            continue
        n = nodes.get(m["ref"])
        if n is None:
            continue
        t = n.get("tags", {})
        key = zh_key(t.get("name:zh") or t.get("name"))
        if not key:
            UNNAMED.add((m["ref"], rel["tags"].get("name")))
            continue
        out.append((key, (t.get("name:en") or "").strip(),
                    (t.get("ref") or "").strip(), n["lat"], n["lon"]))
    return out


UNNAMED = set()


def ways_of(rel):
    return [(m["ref"], [(p["lat"], p["lon"]) for p in m["geometry"]])
            for m in rel.get("members", []) if m["type"] == "way" and m.get("geometry")]


def line_geometry(rels):
    rels = sorted(rels, key=lambda r: sum(len(g) for _, g in ways_of(r)), reverse=True)
    chosen, seen, drawn_m = [], set(), None
    for r in rels:
        for wid, g in ways_of(r):
            if wid in seen or len(g) < 2:
                continue
            if drawn_m is not None:
                mid = g[len(g) // 2]
                if drawn_m.distance(Point(TO_M.transform(mid[1], mid[0]))) <= config.BRANCH_MIN_M:
                    continue
            chosen.append(g)
            seen.add(wid)
        drawn_m = unary_union([LineString([TO_M.transform(lo, la) for la, lo in g]) for g in chosen])
    return chosen


def clusters(points, link_m):
    parent = list(range(len(points)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if np.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1]) <= link_m:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(len(points)):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def plate_points(path, xcol, ycol, encoding="utf-8-sig"):
    """Every door plate's projected point, from one city's file."""
    xs, ys = [], []
    with need(path, "door plates").open(encoding=encoding, errors="replace", newline="") as f:
        for r in csv.DictReader(f):
            try:
                xs.append(float(r[xcol]))
                ys.append(float(r[ycol]))
            except (ValueError, KeyError):
                continue
    x, y = PLATE_TO_M.transform(xs, ys)
    return np.c_[x, y]


def operator_lists():
    text = need(config.METRO_LIST_CSV, "Taipei Metro's list").read_bytes().decode("utf-8").lstrip(chr(0xFEFF))
    per = {}
    for row in list(csv.reader(io.StringIO(text)))[1:]:
        line = row[1].strip("'")
        for sid, name in re.findall(r"'([A-Z]+\d+[A-Z]?)','([^']+)'", row[2]):
            per.setdefault(line, {})[sid] = zh_key(name)
    return per


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    els = json.loads(need(config.RAIL_OSM_JSON, "OSM relations").read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    groups = {k: [] for k in config.LINES}
    unplaced = []
    for r in rels:
        k = line_of(r)
        if k:
            groups[k].append(r)
        elif (r["tags"].get("ref"), r["tags"].get("colour")) not in config.NOT_DRAWN:
            unplaced.append(f"{r['id']} ref={r['tags'].get('ref')!r} {r['tags'].get('name')}")
    if unplaced:
        sys.exit("relations placed in no line - add to LINES or NOT_DRAWN:\n  " + "\n  ".join(unplaced))
    print("Relations matched:")
    for k, spec in config.LINES.items():
        print(f"  {k:<4} {spec['name']:<24} {len(groups[k]):>2} relations")
        if not groups[k]:
            sys.exit(f"no relation for {spec['name']}")

    plat = []
    for k in config.LINES:
        for r in groups[k]:
            for key, en, ref, la, lo in stops_of(r, nodes):
                plat.append({"key": key, "en": en, "ref": ref, "latitude": la, "longitude": lo, "line": k})
    platforms = pd.DataFrame(plat).drop_duplicates()
    if UNNAMED:
        # A stop node with no name at all cannot be collapsed with its station;
        # it is listed, and its station still arrives through its named nodes.
        print(f"  unnamed stop nodes skipped: {sorted(UNNAMED)}")
    rows = []
    for key, g in platforms.groupby("key"):
        pts = [TO_M.transform(lo, la) for la, lo in zip(g.latitude, g.longitude)]
        parts = clusters(pts, config.COLLAPSE_LINK_M)
        for part in parts:
            sub = g.iloc[part]
            ens = [e for e in sub.en if e]
            rows.append({"key": key, "en": english(pd.Series(ens).value_counts().index[0]) if ens else "",
                         "refs": sorted({x for x in sub.ref if x}),
                         "latitude": sub.latitude.mean(), "longitude": sub.longitude.mean(),
                         "lines": [k for k in config.LINES if k in set(sub.line)],
                         "split": len(parts) > 1})
    st = pd.DataFrame(rows)
    for i in st.index[st.split]:
        st.at[i, "en"] = f"{st.at[i, 'en']} ({', '.join(config.LINES[k]['name'] for k in st.at[i, 'lines'])})"
    missing = st[st.en == ""]
    if len(missing):
        sys.exit(f"stations with no English name: {list(missing.key)}")
    st["station"] = st.en
    if st.station.duplicated().any():
        sys.exit(f"duplicate station names: {list(st.station[st.station.duplicated()])}")
    print(f"  {len(platforms)} stop nodes -> {len(st)} stations; split names: "
          + ("; ".join(st[st.split].station) or "none"))

    # --- gate 3: Taipei Metro's own list ------------------------------------------
    ops = operator_lists()
    expected, actual = {}, {}
    for k, spec in config.LINES.items():
        op_lines = spec.get("operator_lines")
        if not op_lines:
            continue
        want = set().union(*(set(ops.get(ol, {}).values()) for ol in op_lines))
        got = set(st.key[[k in ls for ls in st.lines]])
        expected[spec["name"]], actual[spec["name"]] = len(want), len(got)
        if want != got:
            print(f"    {spec['name']}: list only {sorted(want - got)}  OSM only {sorted(got - want)}")

    # --- scope: the two cities' own door plates ----------------------------------
    tp = plate_points(config.TAIPEI_DOORPLATE_CSV, *config.TAIPEI_PLATE_XY)
    ntp = plate_points(config.NEW_TAIPEI_DOORPLATE_CSV, *config.NEW_TAIPEI_PLATE_XY)
    print(f"  door plates: Taipei {len(tp):,}, New Taipei {len(ntp):,}")
    xy = np.array([TO_M.transform(lo, la) for la, lo in zip(st.latitude, st.longitude)])

    def near(plates):
        return np.array([int((np.hypot(plates[:, 0] - x, plates[:, 1] - y) <= config.SCOPE_RADIUS_M).sum())
                         for x, y in xy])
    st["plates_taipei"], st["plates_new_taipei"] = near(tp), near(ntp)
    st["city"] = np.where(st.plates_taipei + st.plates_new_taipei == 0, "",
                          np.where(st.plates_taipei >= st.plates_new_taipei, "Taipei", "New Taipei"))
    st["in_region"] = st.city != ""
    print(f"  in the region: {int(st.in_region.sum())} (Taipei {int((st.city == 'Taipei').sum())}, "
          f"New Taipei {int((st.city == 'New Taipei').sum())}); outside: {int((~st.in_region).sum())}")

    kept = st[st.in_region].copy()
    station_gates.verify_stations(
        city="Taipei (Regional)", platforms=platforms[platforms.key.isin(set(kept.key))],
        stations=kept, crs_projected=config.CRS_PROJECTED,
        expected_per_line=expected, actual_per_line=actual)
    emit("stop_nodes", len(platforms))
    emit("stations_all", len(st))
    emit("stations_kept", len(kept))

    out = st[~st.in_region].copy()
    out["lines"] = [" ".join(config.LINES[k]["name"] for k in ls) for ls in out.lines]
    out["reason"] = "outside Taipei and New Taipei (no door plate of either city within 300 m)"
    out[["station", "lines", "reason", "latitude", "longitude"]].sort_values("station").to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    emit("stations_outside", len(out))
    print(f"  {len(out)} outside -> {config.EXCLUDED_STATIONS_CSV.name}: " + ", ".join(out.station))

    kept["lines"] = [" ".join(ls) for ls in kept.lines]
    kept.rename(columns={"key": "name_zh"})[["station", "name_zh", "city", "latitude", "longitude",
                                             "lines"]].sort_values("station").to_csv(
        config.STATIONS_CSV, index=False, encoding="utf-8")

    elements = []
    print("\n  line geometry:")
    for k, spec in config.LINES.items():
        ways = line_geometry(groups[k])
        elements.append({"type": "relation", "id": len(elements) + 1,
                         "tags": {"ref": k, "name": spec["name"], "colour": spec["colour"]},
                         "members": [{"type": "way", "geometry": [{"lat": la, "lon": lo} for la, lo in g]}
                                     for g in ways]})
        print(f"    {spec['name']:<24} {spec['colour']}  {len(ways):>3} ways")
    config.RAIL_LINES_JSON.write_text(json.dumps({"elements": elements}), encoding="utf-8")
    emit("lines_drawn", len(elements))


if __name__ == "__main__":
    main()
