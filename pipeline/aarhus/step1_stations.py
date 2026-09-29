"""Aarhus step 1: the Letbane's new-city-tramway stations in Aarhus Kommune.

    python pipeline/aarhus/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT:

  * **Rail from OSM route-relation membership** (the osm-rail skill), as
    Copenhagen's: stations are the `stop` members of the kept relations, never
    a tag search. Whitelist on ref + route + operator, never `network`.
  * **Scope is a SECTION of the network, not the kommune.** 39 Letbane
    stations lie in Aarhus Kommune; the 20 on the purpose-built city tramway
    count, and the 19 on the two converted railways fail the owner's
    15-minute test (config). The three sections are named station by station,
    and this step EXITS unless they partition the kommune's stations exactly.
  * **Two stops are spelled differently by direction** (config's aliases).
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, mapping
from shapely.ops import linemerge, substring, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.aarhus import config  # noqa: E402
from pipeline.aarhus.kommuner import kommune_polygons, read_cached  # noqa: E402
from pipeline.baseline import emit  # noqa: E402

# A collapsed name whose stops are further apart than this is two places, not
# one station with two platforms - step 1 stops rather than average them.
COLLAPSE_MAX_SPREAD_M = 200


def stop_rows():
    els = read_cached(config.OSM_ROUTES_JSON, "rail relations")
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = [e for e in els if e["type"] == "relation"]

    def kept(t):
        return (t.get("route") == config.ROUTE and t.get("ref") in config.LINE_REFS
                and t.get("operator") == config.OPERATOR)

    print("\n  route relations:")
    rows, seen = [], set()
    for r in sorted(rels, key=lambda r: (r["tags"].get("ref", ""), r["id"])):
        t = r["tags"]
        ok = kept(t)
        print(f"    {'KEEP' if ok else 'drop':4} {r['id']:>9} {t.get('ref', ''):3} "
              f"{t.get('operator', '-'):<8} {t.get('name', '')}")
        if not ok:
            continue
        seen.add(t["ref"])
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nt = (n or {}).get("tags", {})
            if not n or nt.get("public_transport") != "stop_position" or not nt.get("name"):
                sys.exit(f"{t['ref']}: stop member {m['ref']} is not a named stop_position")
            rows.append({"line": t["ref"], "node": n["id"], "stop_name": nt["name"],
                         "latitude": n["lat"], "longitude": n["lon"]})
    missing = sorted(set(config.LINE_REFS) - seen)
    if missing:
        sys.exit(f"no kept relation for line(s) {missing} - a line withdrawn or retagged "
                 f"is a scope question, not a config edit")
    return pd.DataFrame(rows).drop_duplicates(["line", "node"])


def _variant_lines(ref):
    """One merged LineString (projected) per SERVICE VARIANT of `ref` - the
    set of stops it calls at - taking the relation with the most geometry of
    each direction pair, as load_osm_line_shapes chooses."""
    els = read_cached(config.OSM_ROUTES_JSON, f"{ref} geometry")
    rels = [e for e in els if e["type"] == "relation"
            and e["tags"].get("ref") == ref and e["tags"].get("route") == config.ROUTE]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}

    def stops(r):
        return frozenset(config.STATION_NAME_ALIASES.get(n, n) for n in (
            nodes[m["ref"]]["tags"]["name"] for m in r["members"]
            if m["type"] == "node" and m.get("role", "").startswith("stop")))

    # TRACK ONLY: each relation also lists ~27 `platform` ways, closed outlines
    # that linemerge would keep as 27 stray rings beside the line.
    def track(r):
        return [m for m in r["members"] if m["type"] == "way" and m.get("geometry")
                and not m.get("role", "").startswith("platform")]

    def npts(r):
        return sum(len(m["geometry"]) for m in track(r))

    by_variant = {}
    for r in rels:
        by_variant.setdefault(stops(r), []).append(r)
    out = []
    for variant, rs in sorted(by_variant.items(), key=lambda kv: -len(kv[0])):
        best = max(rs, key=lambda r: (npts(r), -r["id"]))
        merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                            for m in track(best)]))
        if merged.geom_type != "LineString":
            sys.exit(f"{ref} relation {best['id']}: its ways do not merge into one line "
                     f"({merged.geom_type}) - the cut below needs one")
        line = gpd.GeoSeries([merged], crs=config.CRS_GEOGRAPHIC).to_crs(
            config.CRS_PROJECTED).iloc[0]
        out.append((best["id"], variant, line))
    return out


def _cut_toward(line, at, toward):
    """The part of `line` beyond the point nearest `at`, on `toward`'s side."""
    d_at, d_to = line.project(at), line.project(toward)
    return substring(line, d_at, line.length) if d_to > d_at else substring(line, 0, d_at)


def write_drawn_lines(inside, cut):
    """L2 cut to the new tramway, as GeoJSON for load_geojson_line_shapes.

    The trunk variant (Odder - Lystrup) is cut at Aarhus H, keeping the side
    toward Dokk1; the Lisbjergskolen variant is cut at Lisbjerg Bygade,
    keeping only the branch, so the trunk is not drawn twice. Checked, not
    trusted: every in-scope station lies on the drawn line and every converted-
    railway station lies off it."""
    st = gpd.GeoDataFrame(inside, geometry=gpd.points_from_xy(
        inside["longitude"], inside["latitude"]), crs=config.CRS_GEOGRAPHIC
    ).to_crs(config.CRS_PROJECTED).set_index("stop_name").geometry
    variants = _variant_lines("L2")
    print(f"\n  L2 service variants in OSM: {len(variants)}")
    pieces = []
    for rel_id, variant, line in variants:
        if "Lystrup" in variant:
            piece = _cut_toward(line, st["Aarhus H"], st["Dokk1"])
            what = "trunk, cut at Aarhus H"
        elif "Lisbjergskolen" in variant:
            piece = _cut_toward(line, st["Lisbjerg Bygade"], st["Lisbjergskolen"])
            what = "branch, cut at Lisbjerg Bygade"
        else:
            sys.exit(f"L2 relation {rel_id}: a service variant this step does not know")
        print(f"    relation {rel_id:>9}: {what} - {piece.length / 1000:.1f} of "
              f"{line.length / 1000:.1f} km drawn")
        pieces.append(piece)
    drawn = unary_union(pieces)
    far = {n: round(p.distance(drawn)) for n, p in st.items() if p.distance(drawn) > 60}
    if far:
        sys.exit(f"in-scope stations more than 60 m from the drawn line: {far}")
    off = cut[cut["stop_name"].isin(config.ODDERBANEN + config.GRENAABANEN)]
    offp = gpd.GeoSeries(gpd.points_from_xy(off["longitude"], off["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    near = [n for n, p in zip(off["stop_name"], offp) if p.distance(drawn) < 150]
    if near:
        sys.exit(f"converted-railway stations on the drawn line: {near}")
    geo = gpd.GeoSeries(pieces, crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC)
    feature = {"type": "Feature", "properties": {"line": "L2"},
               "geometry": mapping(MultiLineString(list(geo)))}
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection",
                                                "features": [feature]}),
                                    encoding="utf-8")
    print(f"  drawn L2: {drawn.length / 1000:.1f} km -> "
          f"{config.LINES_GEOJSON.relative_to(config.ROOT)}")


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    kom = kommune_polygons()
    q = stop_rows()

    aliased = q["stop_name"].isin(config.STATION_NAME_ALIASES)
    for old, new in config.STATION_NAME_ALIASES.items():
        if not (q["stop_name"] == old).any() or not (q["stop_name"] == new).any():
            sys.exit(f"alias {old!r} -> {new!r}: both spellings must be present; OSM "
                     f"may have fixed one, so re-read it rather than keep a stale alias")
    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_ALIASES)
    print(f"\n  {int(aliased.sum())} stop position(s) renamed by config.STATION_NAME_ALIASES")

    order = list(config.LINE_REFS)
    lines_by_name = q.groupby("stop_name")["line"].agg(
        lambda s: "/".join(sorted(set(s), key=order.index)))
    platforms = q.drop_duplicates("node")
    by_name = platforms.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean"),
                                                 positions=("node", "nunique"))
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(platforms["longitude"],
                                                                platforms["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(platforms)} stop positions -> {len(by_name)} stations by name. "
          f"Widest spreads:")
    for nm in spread.sort_values(ascending=False).head(6).index:
        print(f"    {nm:<32} {int(by_name.loc[nm, 'positions'])} positions, "
              f"{spread[nm]:>5.0f} m across  [{lines_by_name[nm]}]")
    too_far = spread[spread > COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"these names are more than {COLLAPSE_MAX_SPREAD_M} m across and would be "
                 f"averaged into one point: {too_far.round().to_dict()}")
    st_rows = by_name.reset_index()
    st_rows["lines"] = st_rows["stop_name"].map(lines_by_name)

    print()
    station_gates.verify_stations(
        city="Aarhus", platforms=platforms, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS or None,
        actual_per_line=None)
    print("    gate 3: not run - no operator count exists for the section in scope "
          "(config); the section partition below is this city's check")

    pts = gpd.GeoDataFrame(st_rows, geometry=gpd.points_from_xy(st_rows["longitude"],
                                                                st_rows["latitude"]),
                           crs=config.CRS_GEOGRAPHIC)
    hit = gpd.sjoin(pts, kom[["ref", "kommune", "geometry"]], how="left", predicate="within")
    if hit.index.duplicated().any():
        sys.exit(f"stations inside two kommuner at once: "
                 f"{sorted(hit[hit.index.duplicated(keep=False)]['stop_name'].unique())}")
    nowhere = hit[hit["ref"].isna()]
    if len(nowhere):
        sys.exit(f"stations in no kommune polygon (the bbox is too small?): "
                 f"{sorted(nowhere['stop_name'])}")
    in_kom = hit[hit["ref"].isin(config.KOMMUNER)].copy()
    other_kom = hit[~hit["ref"].isin(config.KOMMUNER)].copy()
    print(f"\n  {len(hit)} Letbane stations -> {len(in_kom)} in Aarhus Kommune, "
          f"{len(other_kom)} in other kommuner")

    # THE SECTION PARTITION: every station in the kommune is on exactly one of
    # the three named sections, and every named station exists.
    sections = {"new tramway": config.NEW_TRAMWAY, "Odderbanen": config.ODDERBANEN,
                "Grenaabanen": config.GRENAABANEN}
    named = [s for names in sections.values() for s in names]
    if len(named) != len(set(named)):
        sys.exit("a station is named in two sections")
    have = set(in_kom["stop_name"])
    unnamed, absent = sorted(have - set(named)), sorted(set(named) - have)
    if unnamed or absent:
        sys.exit(f"the sections no longer partition the kommune's stations.\n"
                 f"  in OSM, in no section: {unnamed}\n  in a section, not in OSM: {absent}\n"
                 f"Scope is a decision, not a side effect - see config and DECISIONS.md.")
    for sec, names in sections.items():
        print(f"    {sec:<12} {len(names):>3}")
    inside = in_kom[in_kom["stop_name"].isin(config.NEW_TRAMWAY)].copy()
    if len(inside) != 20:
        sys.exit(f"{len(inside)} new-tramway stations, not the owner's 20")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    if not 450 <= d.median() <= 550:
        sys.exit(f"the in-scope median gap is {d.median():.0f} m; the halved rings were "
                 f"chosen at 499 m - re-take the ring decision")

    section_of = {s: sec for sec, names in sections.items() for s in names}
    cut = in_kom[~in_kom["stop_name"].isin(config.NEW_TRAMWAY)]
    out = pd.concat([
        pd.DataFrame({"station": cut["stop_name"], "lines": cut["lines"],
                      "reason": [config.SECTION_REASONS[section_of[s]]
                                 for s in cut["stop_name"]],
                      "latitude": cut["latitude"], "longitude": cut["longitude"]}),
        pd.DataFrame({"station": other_kom["stop_name"], "lines": other_kom["lines"],
                      "reason": [f"in {k} ({r}), outside Aarhus Kommune"
                                 for k, r in zip(other_kom["kommune"], other_kom["ref"])],
                      "latitude": other_kom["latitude"], "longitude": other_kom["longitude"]}),
    ])
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for k, n in out["reason"].str.split(r"[,(]").str[0].value_counts().items():
        print(f"    {k.strip():<26} {n:>3}")

    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "kommune", "latitude", "longitude"]]
            .sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    write_drawn_lines(inside, cut)

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st_rows))
    emit("stations_in_kommune", len(in_kom))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    main()
