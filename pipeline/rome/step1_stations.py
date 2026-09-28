"""Rome step 1: Metro A, B, B1 and C, and the Roma-Viterbo urban service,
stations inside the comune.

    python pipeline/rome/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

  * **Rail from OSM route-relation membership** (osm-rail), on the recorded
    ground in config.RAIL_SOURCE_GROUND. Lines are keyed on RELATION IDS -
    OSM tags B1 with ref "B" - and every relation in the bbox that is not a
    kept line is named in config.LEFT_OUT_RELATIONS, so a new one stops the
    build instead of being silently dropped or silently drawn.
  * Stations are the `stop` members, whitelisted as named stop_positions, and
    collapse by NAME (both directions' positions), with every spread printed.
  * Excluded stations are named with their comune, from OSM's own relations.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.rome import config  # noqa: E402
from pipeline.rome.boundary import city_polygon, neighbour_polygons  # noqa: E402


def rail_elements():
    """The metro cache and tram 8's own cache (2026-09-27), read as one.
    Tram 8 has its own file so the metro cache stayed untouched."""
    els = []
    for path in (config.OSM_RAIL_JSON, config.OSM_TRAM8_JSON):
        if not path.exists():
            sys.exit(f"missing {path}\nRun: python pipeline/rome/fetch_sources.py")
        els += json.loads(path.read_text(encoding="utf-8"))["elements"]
    return els


def stop_rows():
    els = rail_elements()
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = {e["id"]: e for e in els if e["type"] == "relation"}
    line_of = {rid: ln for ln, ids in config.LINE_RELATIONS.items() for rid in ids}
    unknown = sorted(set(rels) - set(line_of) - set(config.LEFT_OUT_RELATIONS))
    if unknown:
        sys.exit(f"OSM route relations neither drawn nor recorded as left out: "
                 f"{[(r, rels[r]['tags'].get('name')) for r in unknown]}")
    missing = sorted(set(line_of) - set(rels))
    if missing:
        sys.exit(f"kept relation(s) missing from OSM: {missing} - a scope question")
    print("  route relations:")
    rows = []
    for rid, r in sorted(rels.items(), key=lambda kv: kv[1]["tags"].get("name", "")):
        t = r["tags"]
        keep = rid in line_of
        print(f"    {'KEEP ' + line_of[rid] if keep else 'out':8} {rid:>8}  {t.get('name', '')}"
              f"{'' if keep else '  - ' + config.LEFT_OUT_RELATIONS[rid]}")
        if not keep:
            continue
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nt = (n or {}).get("tags", {})
            if not n or nt.get("public_transport") != "stop_position" or not nt.get("name"):
                sys.exit(f"{rid}: stop member {m['ref']} is not a named stop_position")
            rows.append({"line": line_of[rid], "node": n["id"],
                         "stop_name": config.STATION_NAME_ALIASES.get(nt["name"], nt["name"]),
                         "latitude": n["lat"], "longitude": n["lon"]})
    return pd.DataFrame(rows).drop_duplicates(["line", "node"])


def thin(st_rows):
    """San Francisco's filter (pipeline/stations.py `thin()`) on each line in
    config.THINNED_LINES (tram 8).

    Walks each direction's relation in stop order, measuring along the line in
    the projected CRS; a stop is kept at each terminus, at each interchange
    (a name another line also serves) and whenever half a mile has run since
    the last kept stop. Returns {name: reason} for the stops cut - worded with
    "spacing", which app/station_scope.py reads as `thinned`.
    """
    rels = {e["id"]: e for e in rail_elements() if e["type"] == "relation"}
    nodes = {e["id"]: e for e in rail_elements() if e["type"] == "node"}
    xy = station_gates.projected_xy(st_rows["stop_name"], st_rows["longitude"],
                                    st_rows["latitude"], config.CRS_PROJECTED,
                                    config.CRS_GEOGRAPHIC)
    lines_of = dict(zip(st_rows["stop_name"], st_rows["lines"].str.split()))
    interchange = {n for n, ls in lines_of.items() if len(ls) > 1}
    kept, cut = set(), {}
    for ln in config.THINNED_LINES:
        # Rotterdam's rule: add a direction only until every stop is covered.
        # Thinning BOTH directions and keeping the union keeps whatever either
        # walk happens to land on, which barely thins (4 of 16 cut, measured).
        names = {n for n, ls in lines_of.items() if ln in ls}
        covered, seqs = set(), []
        for rid in config.LINE_RELATIONS[ln]:
            if covered >= names:
                break
            seq = []
            for m in rels[rid]["members"]:
                if m["type"] == "node" and m.get("role", "").startswith("stop"):
                    nm = nodes[m["ref"]]["tags"]["name"]
                    nm = config.STATION_NAME_ALIASES.get(nm, nm)
                    if not seq or seq[-1] != nm:
                        seq.append(nm)
            covered |= set(seq)
            seqs.append(seq)
            print(f"    walking {rid} ({rels[rid]['tags'].get('name')}): {len(seq)} stops")
        k, cuts = station_gates.thin(seqs, xy, spacing_m=config.THIN_SPACING_M,
                                     interchange=interchange)
        kept |= k
        for c in cuts:
            cut.setdefault(c["station"], (
                f"spacing filter on {config.LINE_NAMES[ln]}: "
                f"{c['metres_since_kept'] / 1609.344:.3f} mi after {c['nearest_kept']}, "
                f"under 0.5 mi"))
    cut = {n: why for n, why in cut.items() if n not in kept}
    print(f"\n  thinning ({', '.join(config.LINE_NAMES[l] for l in config.THINNED_LINES)}): "
          f"{len(kept)} kept, {len(cut)} cut")
    for n, why in sorted(cut.items()):
        print(f"    cut  {n:<32} {why}")
    return cut


def write_lines():
    """The kept relations for step 3's load_osm_line_shapes, keyed by `ref`:
    B1's relations get ref "B1" and only the ways the B trunk does not use."""
    rels = {e["id"]: e for e in rail_elements() if e["type"] == "relation"}
    trunk_ways = {m["ref"] for rid in config.LINE_RELATIONS["B"] for m in rels[rid]["members"]
                  if m["type"] == "way"}
    out = []
    for ln, ids in config.LINE_RELATIONS.items():
        for rid in ids:
            r = json.loads(json.dumps(rels[rid]))
            r["tags"]["ref"] = ln
            if ln == "B1":
                r["members"] = [m for m in r["members"]
                                if m["type"] != "way" or m["ref"] not in trunk_ways]
            out.append(r)
    b1_ways = sum(1 for r in out if r["tags"]["ref"] == "B1" for m in r["members"] if m["type"] == "way")
    config.OSM_LINES_JSON.write_text(json.dumps({"elements": out}), encoding="utf-8")
    print(f"  line geometry -> {config.OSM_LINES_JSON.relative_to(config.ROOT)} "
          f"(B1 cut to its own {b1_ways} way(s))")


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    q = stop_rows()
    order = list(config.LINE_ORDER)
    # B1 SHARES the trunk from Bologna south to Laurentina; its own stations
    # are the ones the B trunk does not serve. So a station's lines list B1
    # only where B does not reach.
    lines_by_name = q.groupby("stop_name")["line"].agg(lambda s: set(s))
    lines_by_name = lines_by_name.map(
        lambda s: " ".join(ln for ln in order if ln in s and not (ln == "B1" and "B" in s)))
    platforms = q.drop_duplicates("node")
    by_name = platforms.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean"),
                                                 positions=("node", "nunique"))
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(platforms["longitude"],
                                                                platforms["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(platforms)} stop positions -> {len(by_name)} stations by name; widest:")
    for nm in spread.sort_values(ascending=False).head(6).index:
        print(f"    {nm:<30} {int(by_name.loc[nm, 'positions'])} positions, "
              f"{spread[nm]:>5.0f} m  [{lines_by_name[nm]}]")
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"names wider than {config.COLLAPSE_MAX_SPREAD_M} m: {too_far.round().to_dict()}")
    st_rows = by_name.reset_index()
    st_rows["lines"] = st_rows["stop_name"].map(lines_by_name)

    def count(ln):
        return int(sum(1 for v in st_rows["lines"] if ln in v.split()))
    metro = {"A", "B", "B1", "C"}
    actual = {"Metro A": count("A"), "Metro B + B1": count("B") + count("B1"),
              "Metro C": count("C"),
              "Metro (network)": int(sum(1 for v in st_rows["lines"] if metro & set(v.split()))),
              "Roma–Viterbo (urban)": count("RV"), "Tram 8": count("8")}
    print()
    station_gates.verify_stations(
        city="Rome", platforms=platforms, stations=st_rows, crs_projected=config.CRS_PROJECTED,
        spacing_min=config.SPACING_MIN_M, expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    thinned = thin(st_rows)
    thinned_rows = st_rows[st_rows["stop_name"].isin(thinned)]
    st_rows = st_rows[~st_rows["stop_name"].isin(thinned)]

    poly = city_polygon()
    pts = gpd.GeoDataFrame(st_rows, geometry=gpd.points_from_xy(st_rows["longitude"],
                                                                st_rows["latitude"]),
                           crs=config.CRS_GEOGRAPHIC)
    within = pts.within(poly)
    inside, outside = pts[within].copy(), pts[~within].copy()
    print(f"\n  comune {config.ISTAT_COMUNE}: {len(pts)} stations -> {len(inside)} inside, "
          f"{len(outside)} outside")
    print("  per line, inside the comune:")
    for ln in order:
        n_all = int(sum(1 for v in pts["lines"] if ln in v.split()))
        n_in = int(sum(1 for v in inside["lines"] if ln in v.split()))
        print(f"    {config.LINE_NAMES[ln]:<9} {n_in:>3} of {n_all:>3}")

    nb = neighbour_polygons()
    excluded = []
    for _, r in outside.iterrows():
        hit = nb[nb.contains(r.geometry) & (nb["istat"] != config.ISTAT_COMUNE)]
        if len(hit) != 1:
            sys.exit(f"{r['stop_name']} is outside Roma and in {len(hit)} recorded comuni")
        excluded.append({"station": r["stop_name"], "lines": r["lines"],
                         "reason": f"in {hit.iloc[0]['name']} ({hit.iloc[0]['istat']}), "
                                   f"outside comune {config.ISTAT_COMUNE}",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    for _, r in thinned_rows.iterrows():
        excluded.append({"station": r["stop_name"], "lines": r["lines"],
                         "reason": thinned[r["stop_name"]],
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    out = pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"])
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for _, r in out.iterrows():
        print(f"    {r['station']:<30} {r['lines']:<5} {r['reason']}")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  max {d.max():,.0f}")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")
    write_lines()
    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st_rows))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    main()
