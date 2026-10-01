"""Tram stations from OpenStreetMap route relations, shared by the tram kits.

Aarhus's `stop_rows()` generalised (the tram-city skill, section 4; agreed
with the Czech kit, 2026-09-30). Seven of the tram kit's ten cities and five
of the six Czech ones take their rail from OSM, so the rules live here, where
the next OSM tram city passes through them, rather than in a sibling city's
step 1 (the osm-rail meta-rule).

Reads a cached Overpass answer and never fetches: each city's
`fetch_sources.py` downloads, with the relations `out geom` and their stop
nodes (plus any `STATION_ADD` node) `out body`.

THE CONTRACT
------------
* **Relations are kept on `ref` and `route`**, and on `operator` only where
  the city names one - never on `network` alone (Copenhagen's rule).
* **Every relation in the cache on a drawn route mode is kept or named in
  `not_drawn`** by relation id, with a reason. One that is neither stops the
  step: the Czech screens found zero-stop refs, unref'd variants and depot
  runs, each a scope question. A `not_drawn` id missing from the cache also
  stops it, since a stale entry hides the next change.
* **Several relations per ref**: a line's stops are the union of its kept
  relations. `map_common.load_osm_line_shapes` draws the one with the most
  geometry.
* **Stop members are `public_transport=stop_position` OR
  `railway=tram_stop`**, named. An untagged or unnamed stop member stops the
  step and is named (Daugavpils's Stropu ciemats is on the routes untagged).
* **`station_add` by node id** for a tagged stop on no route relation
  (Odense's SDU Syd/Hospital Nord), or a stop a relation lists only as a
  named platform (Liepāja's Rožu laukums). Each names its line - or a tuple
  of lines (Plzeň's Jízdecká, 1/2/4) - and its expected name; the step stops
  if OSM renamed it, untagged it, or has since put a stop of that name on a
  route, so a stale add cannot outlive the gap it filled.
* **`accept_members` by node id** for a stop member of a kept relation that
  carries a name but no stop tag (Daugavpils's Stropu ciemats), with the
  same staleness checks.
* **Name collapse at the mean, within `max_spread_m`** (Aarhus's): one
  station per name, its lines joined in the city's order.
* **Scope over a union of polygons** (`split_by_places`): stations outside
  are named with the place they lie in, as Rennes names communes.
* **Lines-only mode** (`select_relations`): the same keep/`not_drawn`
  validation without stations, for a feed with stations but no `shapes.txt`
  (Brno).

Its control is Aarhus: `scripts/osm_tram_control.py` runs this module on
Aarhus's cache and must reproduce Aarhus's `stations.csv` exactly. Aarhus's
own step 1 is not rewired.
"""
import json
import sys

import geopandas as gpd
import pandas as pd

CRS_GEOGRAPHIC = "EPSG:4326"
STOP_TAGS = (("public_transport", "stop_position"), ("railway", "tram_stop"))


def read_elements(path, label, fetch_script):
    """The cached Overpass elements; exits naming the fetch script when absent."""
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python {fetch_script}")
    print(f"  {label}: {path.name} ({path.stat().st_size:,} bytes)")
    return json.loads(path.read_text(encoding="utf-8"))["elements"]


def _is_stop(tags):
    return any(tags.get(k) == v for k, v in STOP_TAGS)


def select_relations(elements, *, routes, refs, operator=None, not_drawn=None,
                     verbose=True):
    """The kept route relations, validated - the lines-only mode.

    routes: the route modes this city draws, e.g. ("tram",) or
      ("tram", "light_rail"). Every relation in `elements` on one of them is
      judged; relations on other modes are ignored.
    refs: the line refs kept, in the city's display order.
    operator: kept relations must carry exactly this `operator`; None skips it.
    not_drawn: {relation id: reason} for every other relation on those modes.

    Returns {ref: [relation, ...]} in `refs` order. Exits on a relation that is
    neither kept nor named, on a stale `not_drawn` id, and on a ref with no
    kept relation.
    """
    not_drawn = dict(not_drawn or {})
    rels = [e for e in elements if e["type"] == "relation"
            and e.get("tags", {}).get("route") in routes]
    if not rels:
        sys.exit(f"no {'/'.join(routes)} relations in the cache - a FAILED fetch, "
                 f"not a negative")
    ids = {r["id"] for r in rels}
    stale = sorted(set(not_drawn) - ids)
    if stale:
        sys.exit(f"NOT_DRAWN names relation(s) no longer in the cache: {stale} - "
                 f"re-read OSM and update the entry, never keep a stale one")

    kept, unjudged = {ref: [] for ref in refs}, []
    if verbose:
        print("\n  route relations:")
    for r in sorted(rels, key=lambda r: (r["tags"].get("ref", ""), r["id"])):
        t = r["tags"]
        ok = (t.get("ref") in kept
              and (operator is None or t.get("operator") == operator))
        if ok and r["id"] in not_drawn:
            sys.exit(f"relation {r['id']} ({t.get('ref')}) is both kept and in "
                     f"NOT_DRAWN - decide which")
        verdict = "KEEP" if ok else ("out" if r["id"] in not_drawn else "????")
        if verbose:
            why = f"  - {not_drawn[r['id']]}" if r["id"] in not_drawn else ""
            print(f"    {verdict:4} {r['id']:>9} {t.get('route', ''):10} "
                  f"{t.get('ref', '-'):4} {t.get('operator', '-'):<10} "
                  f"{t.get('name', '')}{why}")
        if ok:
            kept[t["ref"]].append(r)
        elif r["id"] not in not_drawn:
            unjudged.append(f"{r['id']} ref={t.get('ref')!r} {t.get('name', '')!r}")
    if unjudged:
        sys.exit("relation(s) neither kept nor in NOT_DRAWN - each is a scope "
                 "question:\n  " + "\n  ".join(unjudged))
    missing = [ref for ref, rs in kept.items() if not rs]
    if missing:
        sys.exit(f"no kept relation for line(s) {missing} - a line withdrawn or "
                 f"retagged is a scope question, not a config edit")
    return kept


def stop_rows(elements, *, routes, refs, operator=None, not_drawn=None,
              station_add=None, name_aliases=None, accept_members=None, verbose=True):
    """One row per (line, stop node): line, node, stop_name, latitude,
    longitude, source ("route" or "added").

    station_add: {node id: (line ref or tuple of refs, expected name)} for a
      stop on no kept relation. A tuple adds one row per ref, for a stop
      several lines serve (Plzeň's Jízdecká, lines 1, 2 and 4). An optional
      third element is the name the station takes, for one node only (New
      Orleans's two "Poydras Street" stops, 600 m apart on two lines).
    name_aliases: {spelling: canonical} for one stop spelled two ways; both
      spellings must be present, or the alias is stale.
    accept_members: {node id: expected name} for a STOP MEMBER of a kept
      relation that carries a name but no stop tag (Daugavpils's Stropu
      ciemats, tagged only as a bus-stop platform). Each was looked at; the
      step stops if the node is retagged as a stop (remove the entry), renamed,
      or no longer a stop member.
    """
    kept = select_relations(elements, routes=routes, refs=refs, operator=operator,
                            not_drawn=not_drawn, verbose=verbose)
    nodes = {e["id"]: e for e in elements if e["type"] == "node"}
    accept = dict(accept_members or {})
    rows, accepted = [], set()
    for ref, rs in kept.items():
        for r in rs:
            for m in r["members"]:
                if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                    continue
                n = nodes.get(m["ref"])
                nt = (n or {}).get("tags", {})
                if n and m["ref"] in accept:
                    if _is_stop(nt):
                        sys.exit(f"accepted member {m['ref']} ({accept[m['ref']]}) is now "
                                 f"tagged as a stop - remove it from accept_members")
                    if nt.get("name") != accept[m["ref"]]:
                        sys.exit(f"accepted member {m['ref']}: OSM now names it "
                                 f"{nt.get('name')!r}, not {accept[m['ref']]!r} - re-read it")
                    accepted.add(m["ref"])
                elif not n or not _is_stop(nt) or not nt.get("name"):
                    sys.exit(f"{ref} relation {r['id']}: stop member node {m['ref']} "
                             f"({nt.get('name', 'no name')!r}, tags {nt}) is not a named "
                             f"stop_position or tram_stop - fix the reading, or "
                             f"name it in accept_members")
                rows.append({"line": ref, "node": n["id"], "stop_name": nt["name"],
                             "latitude": n["lat"], "longitude": n["lon"],
                             "source": "route"})
    stale = sorted(set(accept) - accepted)
    if stale:
        sys.exit(f"accept_members names node(s) no longer a stop member of a kept "
                 f"relation: {stale} - re-read OSM")
    q = pd.DataFrame(rows).drop_duplicates(["line", "node"])

    on_routes, route_q = set(q["node"]), q[["line", "stop_name"]].copy()
    for node_id, spec in (station_add or {}).items():
        # (ref, OSM name) or (ref, OSM name, shown name): the third renames ONE
        # node, for two lines' stops OSM names alike far apart (New Orleans's
        # "Poydras Street" on Loyola Avenue and on the riverfront, 2026-09-30),
        # which a name alias - every node of a spelling - cannot separate.
        ref, name = spec[0], spec[1]
        shown = spec[2] if len(spec) > 2 else name
        n = nodes.get(node_id)
        nt = (n or {}).get("tags", {})
        if not n:
            sys.exit(f"STATION_ADD node {node_id} ({name}) is not in the cache - "
                     f"the fetch must ask for it")
        # A PLATFORM node is accepted for an add, and only for an add: Liepāja's
        # Rožu laukums is on both route relations as a `platform` member with no
        # stop position at all (2026-09-30). Each add is named in config and
        # looked at, so this widens nothing a route relation reads.
        if (not (_is_stop(nt) or nt.get("public_transport") == "platform")
                or nt.get("name") != name):
            sys.exit(f"STATION_ADD node {node_id}: OSM now has {nt.get('name')!r}, "
                     f"tagged {({k: nt.get(k) for k, _ in STOP_TAGS})}, not a stop "
                     f"or platform named {name!r} - re-read it")
        lines = (ref,) if isinstance(ref, str) else tuple(ref)
        # The gap is per line: an add is stale when the node, or a stop of the
        # name it takes, is on ITS OWN line's relations. Another line's stop of
        # that name is a shared station (New Orleans's 46 joining 47's Loyola
        # Avenue stops) or, renamed, a different one.
        own = set(route_q.loc[route_q["line"].isin(lines), "stop_name"])
        if node_id in on_routes or shown in own:
            sys.exit(f"STATION_ADD node {node_id} ({name}) is now on a route "
                     f"relation of {'/'.join(lines)} as a stop - OSM filled the gap; "
                     f"remove the add")
        unknown = [x for x in lines if x not in kept]
        if not lines or unknown:
            sys.exit(f"STATION_ADD node {node_id} names line(s) {unknown or lines!r}, "
                     f"not kept refs")
        q = pd.concat([q, pd.DataFrame([{
            "line": x, "node": node_id, "stop_name": shown, "latitude": n["lat"],
            "longitude": n["lon"], "source": "added"} for x in lines])], ignore_index=True)
        if verbose:
            print(f"    ADD  node {node_id} {name!r} on {'/'.join(lines)}"
                  + (f" as {shown!r}" if shown != name else ""))

    for old, new in (name_aliases or {}).items():
        if not (q["stop_name"] == old).any() or not (q["stop_name"] == new).any():
            sys.exit(f"alias {old!r} -> {new!r}: both spellings must be present; OSM "
                     f"may have fixed one, so re-read it rather than keep a stale alias")
    if name_aliases:
        n_alias = int(q["stop_name"].isin(name_aliases).sum())
        q["stop_name"] = q["stop_name"].replace(name_aliases)
        if verbose:
            print(f"\n  {n_alias} stop position(s) renamed by the name aliases")
    return q.reset_index(drop=True)


def collapse(q, *, refs, crs_projected, max_spread_m=200, verbose=True):
    """One station per name at the mean of its stop positions.

    Returns (platforms, stations): platforms is `q` one row per node; stations
    has stop_name, latitude, longitude, positions, lines ("L1/L2", in `refs`
    order). Exits when a name's positions spread wider than `max_spread_m` -
    two places, not one station with two platforms.
    """
    order = list(refs)
    lines_by_name = q.groupby("stop_name")["line"].agg(
        lambda s: "/".join(sorted(set(s), key=order.index)))
    platforms = q.drop_duplicates("node")
    by_name = platforms.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean"),
                                                 positions=("node", "nunique"))
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(
        platforms["longitude"], platforms["latitude"]), crs=CRS_GEOGRAPHIC
    ).to_crs(crs_projected)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    if verbose:
        print(f"\n  {len(platforms)} stop positions -> {len(by_name)} stations by "
              f"name. Widest spreads:")
        for nm in spread.sort_values(ascending=False).head(6).index:
            print(f"    {nm:<32} {int(by_name.loc[nm, 'positions'])} positions, "
                  f"{spread[nm]:>5.0f} m across  [{lines_by_name[nm]}]")
    too_far = spread[spread > max_spread_m]
    if len(too_far):
        sys.exit(f"these names are more than {max_spread_m} m across and would be "
                 f"averaged into one point: {too_far.round().to_dict()}")
    stations = by_name.reset_index()
    stations["lines"] = stations["stop_name"].map(lines_by_name)
    return platforms, stations


def split_by_places(stations, places, *, keep, place_col="name", key_col="ref"):
    """Scope over a UNION of polygons.

    places: GeoDataFrame (EPSG:4326) with `key_col`, `place_col`, geometry -
      every polygon the network touches, so a station outside is named with
      the place it lies in.
    keep: the `key_col` values in scope.

    Returns (inside, outside), each a GeoDataFrame with `key_col` and
    `place_col` joined on. Exits on a station in two places or in none.
    """
    pts = gpd.GeoDataFrame(stations, geometry=gpd.points_from_xy(
        stations["longitude"], stations["latitude"]), crs=CRS_GEOGRAPHIC)
    hit = gpd.sjoin(pts, places[[key_col, place_col, "geometry"]], how="left",
                    predicate="within").drop(columns="index_right")
    if hit.index.duplicated().any():
        sys.exit(f"stations inside two places at once: "
                 f"{sorted(hit[hit.index.duplicated(keep=False)]['stop_name'].unique())}")
    nowhere = hit[hit[key_col].isna()]
    if len(nowhere):
        sys.exit(f"stations in no place polygon (the fetch bbox is too small?): "
                 f"{sorted(nowhere['stop_name'])}")
    inside = hit[hit[key_col].isin(keep)].copy()
    return inside, hit[~hit[key_col].isin(keep)].copy()
