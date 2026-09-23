"""Download Dublin's three raw sources into data/dublin/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py. `drift_check.py` globs step*.py, so a
download that lived in a step would turn every drift check into a question
about the CURRENT UPSTREAM rather than about the COMMITTED CODE - and Toronto
proved that is not pedantic, producing a map missing a storefront while the
row-count baseline reported identical.

Run this once by hand; the steps then read the cache and exit non-zero naming
this script if it is missing.

    python pipeline/dublin/fetch_sources.py
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.dublin import config
from pipeline.osm import fetch as osm_fetch

HEADERS = {"User-Agent": "Mozilla/5.0 (expanded-heatmap; Dublin build)"}


def _get(url, timeout=300):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_valuations():
    """One call per local authority, concatenated.

    `LocalAuthority` is matched EXACTLY and a wrong string returns HTTP 200
    with an empty list rather than an error, so every authority asserts a
    non-trivial row count instead of trusting the status code.
    """
    print(f"Valuation register: {config.VALUATION_API}")
    rows = []
    for authority in config.AUTHORITIES:
        params = {
            "Fields": "*",
            "LocalAuthority": authority,
            "Format": "json",
            "Download": "false",
        }
        url = config.VALUATION_API + "?" + urllib.parse.urlencode(
            params, safe="*()")
        got = json.loads(_get(url))
        if len(got) < 1000:
            sys.exit(
                f"  {authority}: {len(got)} rows - too few to be real.\n"
                f"  The API returns HTTP 200 with an EMPTY LIST for an "
                f"unrecognised LocalAuthority, so this is almost certainly a "
                f"changed spelling rather than a changed register. Check "
                f"config.AUTHORITIES against the register's own values.")
        for row in got:
            row["_authority"] = authority
        rows += got
        print(f"  {authority:32s} {len(got):7,} rows")

    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.BUSINESSES_RAW_JSON.write_text(json.dumps(rows), encoding="utf-8")
    print(f"  -> {config.BUSINESSES_RAW_JSON.name}  {len(rows):,} rows total")


def fetch_boundary():
    """The four authorities' polygons, from the SYNCHRONOUS FeatureServer.

    Not the endpoint data.gov.ie lists: that is the ArcGIS Hub async download
    API, which answers HTTP 202 with a job id and needs a second call.
    """
    print(f"\nBoundary: {config.BOUNDARY_SERVICE}")
    names = "','".join(config.AUTHORITIES.values())
    where = urllib.parse.quote(f"{config.BOUNDARY_NAME_FIELD} IN ('{names}')")
    url = (f"{config.BOUNDARY_SERVICE}/query?where={where}"
           f"&outFields={config.BOUNDARY_NAME_FIELD}"
           f"&outSR=4326&f=geojson")
    gj = json.loads(_get(url))
    feats = gj.get("features") or []
    if not feats:
        sys.exit("  no boundary features returned - check "
                 f"{config.BOUNDARY_NAME_FIELD} spellings in config.AUTHORITIES")

    got = {f["properties"][config.BOUNDARY_NAME_FIELD] for f in feats}
    missing = set(config.AUTHORITIES.values()) - got
    if missing:
        sys.exit(f"  boundary layer returned nothing for: {sorted(missing)}.\n"
                 f"  The register and the boundary spell one authority "
                 f"differently; config.AUTHORITIES maps between them.")

    config.BOUNDARY_GEOJSON.write_text(json.dumps(gj), encoding="utf-8")
    print(f"  -> {config.BOUNDARY_GEOJSON.name}  {len(feats)} polygon(s) "
          f"across {len(got)} authorities")
    if len(feats) != config.BOUNDARY_PARTS_EXPECTED:
        print(f"  NOTE: {len(feats)} parts, brief recorded "
              f"{config.BOUNDARY_PARTS_EXPECTED}. Step 1 dissolves by name, so "
              f"this changes nothing unless an authority vanished.")


def fetch_gtfs():
    """The NTA national feed, TRIMMED to Dublin's three drawn routes.

    The download is 158 MB and its shapes.txt is 372 MB over 8.0M rows - the
    whole of Ireland, buses included. Parsing that in step 1 and again in step
    3, on every run and every drift check, would cost more than the rest of
    this city put together. So the trim happens ONCE, here, where downloading
    already lives, and the steps read a small zip with the standard loaders.

    Trimming is not filtering-for-convenience: the output is a valid GTFS
    subset, so `map_common.load_line_shapes` needs no Dublin-specific branch
    and this city does not fork the renderer.
    """
    import csv
    import io
    import zipfile

    print(f"\nGTFS: {config.GTFS_URL}")
    if not config.GTFS_ALL_ZIP.exists():
        raw = _get(config.GTFS_URL, timeout=900)
        if raw[:4] != b"PK\x03\x04":
            sys.exit(f"  not a zip - first bytes {raw[:8]!r}. A download that "
                     f"delegates to another portal can serve an HTML page or "
                     f"an unrelated image with an honest Content-Disposition, "
                     f"so the magic bytes are what decide this.")
        config.GTFS_ALL_ZIP.write_bytes(raw)
        print(f"  downloaded {len(raw):,} bytes")
    else:
        print(f"  using cached {config.GTFS_ALL_ZIP.name} "
              f"({config.GTFS_ALL_ZIP.stat().st_size:,} bytes)")

    def read(zf, name):
        with zf.open(name) as fh:
            return list(csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig")))

    with zipfile.ZipFile(config.GTFS_ALL_ZIP) as zf:
        info = read(zf, "feed_info.txt")
        if info:
            print(f"  feed_info: {info[0].get('feed_start_date')} -> "
                  f"{info[0].get('feed_end_date')}")

        routes = [r for r in read(zf, "routes.txt")
                  if r["route_id"] in config.ROUTES]
        missing = set(config.ROUTES) - {r["route_id"] for r in routes}
        if missing:
            sys.exit(f"  route_id(s) not in the feed: {sorted(missing)}. The "
                     f"NTA rewrites these between releases; re-read routes.txt "
                     f"rather than guessing a new spelling.")
        for r in routes:
            print(f"    {r['route_id']:20s} type={r['route_type']:2s} "
                  f"short={r['route_short_name']!r} "
                  f"colour={r.get('route_color') or '(EMPTY)'}")

        keep_routes = set(config.ROUTES)
        trips = [t for t in read(zf, "trips.txt")
                 if t["route_id"] in keep_routes]
        keep_trips = {t["trip_id"] for t in trips}
        keep_shapes = {t["shape_id"] for t in trips if t.get("shape_id")}
        print(f"    {len(trips):,} trips, {len(keep_shapes)} shapes")

        # Streamed, because shapes.txt and stop_times.txt are the two files
        # that make the feed big.
        def stream(name, keep_col, keep_set):
            out = []
            with zf.open(name) as fh:
                for row in csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig")):
                    if row[keep_col] in keep_set:
                        out.append(row)
            return out

        shapes = stream("shapes.txt", "shape_id", keep_shapes)
        stop_times = stream("stop_times.txt", "trip_id", keep_trips)
        keep_stops = {s["stop_id"] for s in stop_times}
        stops = [s for s in read(zf, "stops.txt")
                 if s["stop_id"] in keep_stops]
        print(f"    {len(shapes):,} shape points, {len(stop_times):,} stop "
              f"times, {len(stops):,} stops")

    def write(zf, name, rows):
        if not rows:
            return
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()),
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
        zf.writestr(name, buf.getvalue())

    with zipfile.ZipFile(config.GTFS_ZIP, "w",
                         compression=zipfile.ZIP_DEFLATED) as out:
        write(out, "routes.txt", routes)
        write(out, "trips.txt", trips)
        write(out, "shapes.txt", shapes)
        write(out, "stop_times.txt", stop_times)
        write(out, "stops.txt", stops)
        write(out, "feed_info.txt", info)
    print(f"  -> {config.GTFS_ZIP.name}  "
          f"{config.GTFS_ZIP.stat().st_size:,} bytes")


def fetch_rail():
    """Route relations WITH THEIR MEMBER LISTS, and their stop nodes.

    KEPT AS THE CROSS-CHECK, not as the source. See config.ROUTES.

    `out geom` on the relations, not `out tags`. It carries BOTH things the
    build needs and neither of the cheaper verbs does: the member node refs
    step 1 uses for station membership, and the member WAY GEOMETRY that
    map_common.load_osm_line_shapes draws the lines from. `out body` gives
    the first and not the second. The member list is the whole
    point: `node(r)` recurses over EVERY relation the query matched, Commuter
    and InterCity included, so the node set alone cannot say which stops belong
    to a drawn line. Deriving stations from the node set would silently put
    Dundalk and Portlaoise in a Dublin map. Step 1 intersects the node set with
    the KEPT relations' members instead - which is the osm-rail skill's rule
    that stations come from route-relation membership, not from a tag filter.

    The whole bbox is still fetched rather than only the kept refs, so step 1
    can report what it dropped and why.

    Delegated to pipeline.osm.fetch, which handles the mirrors, the retries,
    and the empty-200 that overpass.osm.ch returned for this exact query on
    2026-09-22 - a lie a hand-rolled loop accepted, reporting 0 relations
    against a real 42.
    """
    south, west, north, east = config.RAIL_BBOX
    query = (
        "[out:json][timeout:240];"
        '(relation["type"="route"]["route"~"^(tram|train)$"]'
        f"({south},{west},{north},{east}););"
        "out geom;"
        "node(r);"
        "out tags center;")
    print("\nRail: OpenStreetMap")
    elements, host = osm_fetch(query, config.RAIL_OSM_JSON)
    rels = sum(1 for e in elements if e["type"] == "relation")
    nodes = sum(1 for e in elements if e["type"] == "node")
    with_members = sum(1 for e in elements
                       if e["type"] == "relation" and e.get("members"))
    print(f"  via {host}: {rels} relations ({with_members} carrying members), "
          f"{nodes} nodes")
    if with_members < rels:
        sys.exit("  some relations came back WITHOUT member lists - the query "
                 "must use `out geom`, and step 1 cannot tell a Luas stop "
                 "from a Dundalk one without them.")
    print(f"  -> {config.RAIL_OSM_JSON.name}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="re-download even where the cache already exists")
    args = ap.parse_args()

    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    for path, fn, what in (
            (config.BUSINESSES_RAW_JSON, fetch_valuations, "valuations"),
            (config.BOUNDARY_GEOJSON, fetch_boundary, "boundary"),
            (config.GTFS_ZIP, fetch_gtfs, "gtfs"),
            (config.RAIL_OSM_JSON, fetch_rail, "rail cross-check")):
        if path.exists() and not args.force:
            print(f"{what}: cached at {path.name} (--force to refresh)")
            continue
        fn()
    print("\nDone. The steps read these files and never fetch.")
