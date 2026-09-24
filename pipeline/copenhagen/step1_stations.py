"""Copenhagen step 1: Metro and S-tog stations inside Kobenhavn + Frederiksberg.

    python pipeline/copenhagen/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT:

  * **Rail from OSM route-relation membership** (the osm-rail skill), on a
    recorded ground - see config. Stations are the `stop` members of the kept
    relations, never a tag search, so a line with a relation cannot lose a
    station to a missing tag.
  * **The whitelist is ref + route + operator, never `network`**: every
    relation in the bbox says "Takst Sjaelland", the fare zone.
  * **Two modes share eight station names** (Norreport, Kobenhavn H, ...), one
    interchange each. They collapse to one station by name, and every
    collapsed name's spread is printed, so a merge of two different places
    cannot pass silently.
  * **Kommune polygons come from OSM and carry INNER rings.** Frederiksberg is
    an enclave, so Kobenhavn's relation has holes; a polygon built from its
    outer ways alone would put Frederiksberg's stations in Kobenhavn.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.copenhagen import config  # noqa: E402
from pipeline.copenhagen.kommuner import kommune_polygons, read_cached  # noqa: E402

# A collapsed name whose stops are further apart than this is two places, not
# one station with two platforms - and step 1 stops rather than average them.
COLLAPSE_MAX_SPREAD_M = 400


def stop_rows():
    els = read_cached(config.OSM_ROUTES_JSON, "rail relations")
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = [e for e in els if e["type"] == "relation"]

    def kept(t):
        if t.get("route") == "subway":
            return t.get("ref") in config.METRO_REFS
        return (t.get("route") == "light_rail" and t.get("ref") in config.STOG_REFS
                and t.get("operator") == config.STOG_OPERATOR)

    print("\n  route relations:")
    rows, seen = [], set()
    for r in sorted(rels, key=lambda r: (r["tags"].get("route", ""), r["tags"].get("ref", ""))):
        t = r["tags"]
        ok = kept(t)
        print(f"    {'KEEP' if ok else 'drop':4} {t.get('route', ''):10} {t.get('ref', ''):4} "
              f"{t.get('operator', '-'):<18} {t.get('name', '')}")
        if not ok:
            continue
        seen.add(t["ref"])
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nt = (n or {}).get("tags", {})
            # WHITELIST the stop object: a stop position, never an entrance
            # or a platform way.
            if not n or nt.get("public_transport") != "stop_position" or not nt.get("name"):
                sys.exit(f"{t['ref']}: stop member {m['ref']} is not a named stop_position")
            rows.append({"line": t["ref"], "node": n["id"], "stop_name": nt["name"],
                         "latitude": n["lat"], "longitude": n["lon"]})
    missing = sorted(set(config.LINE_NAMES) - seen)
    if missing:
        sys.exit(f"no kept relation for line(s) {missing} - a line withdrawn or retagged "
                 f"is a scope question, not a config edit")
    return pd.DataFrame(rows).drop_duplicates(["line", "node"])


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    kom = kommune_polygons()
    q = stop_rows()

    aliased = q["stop_name"].isin(config.STATION_NAME_ALIASES)
    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_ALIASES)
    if aliased.any():
        print(f"\n  {int(aliased.sum())} stop(s) renamed by config.STATION_NAME_ALIASES")

    order = list(config.LINE_NAMES)
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
    both = [nm for nm, ls in lines_by_name.items()
            if any(x.startswith("M") for x in ls.split("/"))
            and any(not x.startswith("M") for x in ls.split("/"))]
    print(f"\n  {len(platforms)} stop positions -> {len(by_name)} stations by name; "
          f"{len(both)} Metro/S-tog interchange(s) by shared name. Widest spreads:")
    for nm in spread.sort_values(ascending=False).head(10).index:
        print(f"    {nm:<26} {int(by_name.loc[nm, 'positions'])} positions, "
              f"{spread[nm]:>5.0f} m across  [{lines_by_name[nm]}]")
    too_far = spread[spread > COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"these names are more than {COLLAPSE_MAX_SPREAD_M} m across and would be "
                 f"averaged into one point: {too_far.round().to_dict()}")
    st_rows = by_name.reset_index()
    st_rows["lines"] = st_rows["stop_name"].map(lines_by_name)

    total_per_line = {ln: int(sum(1 for v in st_rows["lines"] if ln in v.split("/")))
                      for ln in order}
    print()
    station_gates.verify_stations(
        city="Copenhagen", platforms=platforms, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS or None,
        actual_per_line={config.LINE_NAMES.get(k, k): v for k, v in total_per_line.items()}
        | {"Metro (network)": int(sum(1 for v in st_rows["lines"]
                                      if any(x.startswith("M") for x in v.split("/")))),
           "S-tog (network)": int(sum(1 for v in st_rows["lines"]
                                      if any(not x.startswith("M") for x in v.split("/"))))})
    if config.OPERATOR_COUNTS_SOURCE:
        print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    pts = gpd.GeoDataFrame(st_rows, geometry=gpd.points_from_xy(st_rows["longitude"],
                                                                st_rows["latitude"]),
                           crs=config.CRS_GEOGRAPHIC)
    hit = gpd.sjoin(pts, kom[["ref", "kommune", "geometry"]], how="left", predicate="within")
    if hit.index.duplicated().any():
        sys.exit(f"stations inside two kommuner at once: "
                 f"{sorted(hit[hit.index.duplicated(keep=False)]['stop_name'].unique())}")
    nowhere = hit[hit["ref"].isna()]
    if len(nowhere):
        sys.exit(f"stations in no kommune polygon (in the sea, or the bbox is too small): "
                 f"{sorted(nowhere['stop_name'])}")
    inside = hit[hit["ref"].isin(config.KOMMUNER)].copy()
    outside = hit[~hit["ref"].isin(config.KOMMUNER)].copy()
    print(f"\n  {len(hit)} stations -> {len(inside)} inside the two kommuner "
          f"({', '.join(f'{n} {int((inside.ref == r).sum())}' for r, n in config.KOMMUNER.items())}), "
          f"{len(outside)} outside")

    inside_per_line = {ln: int(sum(1 for v in inside["lines"] if ln in v.split("/")))
                       for ln in order}
    print("\n  per line, inside the two kommuner:")
    for ln in order:
        exp = config.EXPECTED_INSIDE_PER_LINE.get(ln)
        flag = "" if exp is None or exp == inside_per_line[ln] else f"   <- EXPECTED {exp}"
        print(f"    {config.LINE_NAMES[ln]:<10} {inside_per_line[ln]:>3} of "
              f"{total_per_line[ln]:>3}{flag}")
    if 0 in inside_per_line.values():
        sys.exit("the scope drops a whole line; the scope decision needs re-taking")
    if inside_per_line != config.EXPECTED_INSIDE_PER_LINE:
        sys.exit(f"the two kommuner keep a different set than recorded.\n"
                 f"  measured: {inside_per_line}\n"
                 f"  config  : {config.EXPECTED_INSIDE_PER_LINE}\n"
                 f"Scope is a decision, not a side effect - see config and DECISIONS.md.")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")

    out = pd.DataFrame({
        "station": outside["stop_name"], "lines": outside["lines"],
        "reason": [f"in {k} ({r.zfill(4)}), outside Kobenhavn and Frederiksberg"
                   for k, r in zip(outside["kommune"], outside["ref"])],
        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for k, n in out["reason"].str.extract(r"^in (.+?) \(")[0].value_counts().items():
        print(f"    {k:<26} {n:>3}")

    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "kommune", "latitude", "longitude"]]
            .sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st_rows))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    main()
