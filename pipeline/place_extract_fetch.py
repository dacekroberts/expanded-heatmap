"""Write a city's place caches from a regional OpenStreetMap extract filtered
on this machine: the second route beside pipeline/place_index_fetch.py's
Overpass queries, for the same three caches in the same shape. NOT a step:
drift_check.py never runs this file.

    python pipeline/place_extract_fetch.py <city> [--force] [--pbf FILE] [--out DIR]
    python pipeline/place_extract_fetch.py --selftest

It answers place_index_fetch.py's OUTLINE_QUERY, QUERY and EXTRA_QUERY, read
from that module as written (the unions are parsed line by line by
pipeline/osm_extract.py, and a QUERY whose shape has changed stops this
script), with osm_extract's five rules. Proven equal to Overpass's answers
on Tbilisi and Seattle, 2026-10-13 (osm-extract skill, "The proof").

  * A cache already on disk is KEPT, never written over, whoever wrote it;
    only --force replaces one. With every cache present nothing is read.
  * --out DIR writes all three under DIR instead, records nothing, and
    refuses the folder the config's caches live in: the proof's route
    (scripts/place_extract_compare.py).
  * The extract: --pbf FILE, or the smallest region of the download server
    covering the city (its outline cache when there is one, else the map's
    stations), found, held and downloaded by osm_extract.download_extract.
    A held extract no older than PLACE_MAX_AGE_DAYS is used with no request.
  * FRESHNESS: the place caches are refused from an extract whose own
    timestamp is older than place_index_fetch.PLACE_MAX_AGE_DAYS (7 days),
    the rule the Overpass route applies to a mirror's answer. The outline
    accepts any date, as there.
  * THE SCOPE STOP: place_index_fetch.check_area runs on the boundaries
    before the heavy pass, exactly as it does before the heavy queries.
  * PLACE_AREA as "(id:...)" (relations, or ways at 2400000000+) or as tag
    filters (Kyoto); anything else stops. A tag filter is matched against
    boundary and multipolygon relations only.
  * config.PLACE_SPLIT is NOT used: it cuts an Overpass query into tiles a
    mirror can answer, and a local read has no such limit.
  * ORDER: each cache is written in one fixed order (street ways by id,
    their nodes by id, then nodes, ways and relations by id). Overpass's qt
    order is not reproduced, so the index step's order-dependent tie-breaks
    (which of two same-name landmark ways is kept, the order of aliases) can
    fall differently from an Overpass cache of the same data.
  * Provenance in place_index_fetch.record's shape: "host" names the
    download server and the extract file, "osm_base" is the extract's own
    timestamp, "query" the Overpass query answered.

Run it through the heavy-job gate: one pass holds every node position of the
region (peaks in the osm-extract skill).
"""
import argparse
import datetime
import importlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline import osm_extract, place_index, place_index_fetch  # noqa: E402

EXTRACT_ROOT = Path(__file__).parent.parent / "data" / "_osm_extracts"
# The two place queries with their unions taken out and the timeout's number
# blanked: what this script answers. A change to either constant in
# place_index_fetch.py that is not a union line stops the run until this file
# and the proof are brought up to date.
MAIN_SHAPE = ('[out:json][timeout:N];\narea{area}->.a;\nway["highway"]["name"](area.a)->.w;\n'
              '.w out body qt;\nnode(w.w);\nout skel qt;\n(\n<UNION>\n);\nout tags center qt;\n')
EXTRA_SHAPE = '[out:json][timeout:N];\narea{area}->.a;\n(\n<UNION>\n);\nout tags center qt;\n'
OUTLINE_SHAPE = '[out:json][timeout:N];\narea{area}->.a;\n(\n<UNION>\n);\nout geom;\n'
OUTLINE_UNION = "  rel(pivot.a);\n  way(pivot.a);"
STREETS = 'way["highway"]["name"](area.a)->.w;'
_UNION = re.compile(r"\(\n(.*?)\n\);", re.S)


def _split(query):
    """(shape, union text) of a query."""
    m = _UNION.search(query)
    if not m:
        raise SystemExit("a place query has no union: pipeline/place_extract_fetch.py cannot mirror it")
    shape = query[:m.start(1)] + "<UNION>" + query[m.end(1):]
    return re.sub(r"timeout:\d+", "timeout:N", shape), m.group(1)


def unions():
    """{"streets", "main", "extra": [Clause]} read from place_index_fetch's
    queries; exits when a query is no longer the shape this file answers."""
    main_shape, main_union = _split(place_index_fetch.QUERY)
    extra_shape, extra_union = _split(place_index_fetch.EXTRA_QUERY)
    outline_shape, outline_union = _split(place_index_fetch.OUTLINE_QUERY)
    if (main_shape, extra_shape, outline_shape, outline_union) != (MAIN_SHAPE, EXTRA_SHAPE, OUTLINE_SHAPE,
                                                                   OUTLINE_UNION):
        raise SystemExit("pipeline/place_index_fetch.py's queries changed shape outside their unions. "
                         "pipeline/place_extract_fetch.py answers the shapes it names (MAIN_SHAPE, "
                         "EXTRA_SHAPE, OUTLINE_SHAPE): bring it up to date and run the proof again "
                         "(osm-extract skill).")
    try:
        return {"streets": [osm_extract.parse_statement(STREETS)],
                "main": osm_extract.parse_union(main_union),
                "extra": osm_extract.parse_union(extra_union)}
    except ValueError as exc:
        raise SystemExit(f"pipeline/place_index_fetch.py: {exc}. The extract route cannot answer that "
                         f"statement; teach pipeline/osm_extract.py or keep the city on Overpass.")


def targets(config, force, out_dir=None):
    """[(key, path, write?)] for the outline, main and extra caches, in that
    order. A cache on disk is written only with --force."""
    paths = (("osm_place_outline", place_index.outline_cache(config)),
             ("osm_places", Path(config.PLACE_OSM_JSON)),
             ("osm_places_extra", Path(config.PLACE_OSM_EXTRA_JSON)))
    if out_dir is not None:
        out_dir = Path(out_dir)
        if out_dir.resolve() == paths[1][1].parent.resolve():
            raise SystemExit(f"--out {out_dir} is the folder the city's own caches live in: "
                             f"name another, or drop --out to write the missing caches.")
        return [(key, out_dir / p.name, True) for key, p in paths]
    return [(key, p, force or not p.exists()) for key, p in paths]


def check_fresh(timestamp, pbf, now=None):
    """Exit when the extract's data is older than the place caches may be."""
    age = osm_extract.age_days(timestamp, now)
    limit = place_index_fetch.PLACE_MAX_AGE_DAYS
    if age is None or age > limit:
        raise SystemExit(f"{Path(pbf).name}: data dated {timestamp}, older than {limit} days. The place "
                         f"caches are not written from it: let this script fetch the region's current "
                         f"extract (no --pbf), or name a newer file.")
    return age


def choose_extract(config, root=EXTRACT_ROOT, out=print):
    """The extract for a city with no --pbf: the smallest region covering
    its outline cache when one is on disk, else its stations."""
    from shapely.geometry import MultiPoint
    from shapely.ops import unary_union
    slug = place_index.city_of(config)[0]
    ocache = place_index.outline_cache(config)
    if ocache.exists():
        munis = place_index.municipalities(json.loads(ocache.read_bytes().decode("utf-8"))["elements"])
        geom, basis = unary_union([g for _, _, g in munis]), "its outline cache"
    else:
        stations = place_index.map_stations(config)
        if not stations:
            raise SystemExit(f"{slug}: no outline cache and no stations to find its region by: name the "
                             f"extract with --pbf.")
        geom, basis = MultiPoint([(lon, lat) for _, lat, lon in stations]), f"its {len(stations)} stations"
    index = osm_extract.load_index(Path(root) / "index-v1.json")
    region = osm_extract.smallest_region(index, geom)
    out(f"region: {region['properties']['id']}, the smallest covering {slug} by {basis}")
    return osm_extract.download_extract(region, root, max_age_days=place_index_fetch.PLACE_MAX_AGE_DAYS, out=out)


def check_region(pbf, area, root=EXTRACT_ROOT, out=print):
    """Exit when the area reaches past the region the extract was cut to: a
    boundary can close there while the streets beyond the cut are absent.
    Said out loud when the region cannot be found (no index on disk, or a
    file under another name)."""
    from shapely.geometry import shape
    from shapely.ops import unary_union
    m = osm_extract.DATED.match(Path(pbf).name)
    index_path = Path(root) / "index-v1.json"
    feature = None
    if m and index_path.exists():
        index = json.loads(index_path.read_bytes().decode("utf-8"))
        found = [f for f in index["features"] if f.get("geometry")
                 and "pbf" in f["properties"].get("urls", {})
                 and osm_extract.region_short(f) == m.group("region")]
        feature = found[0] if len(found) == 1 else None
    if feature is None:
        out("  region: NOT checked against the extract's own outline (no index on disk, or the file "
            "is not named <region>-YYMMDD.osm.pbf)")
        return
    if not shape(feature["geometry"]).covers(unary_union(area.parts)):
        raise SystemExit(f"{Path(pbf).name}: the search area reaches past region "
                         f"{feature['properties']['id']}. Use the next larger region.")
    out(f"  region: the area lies wholly inside {feature['properties']['id']}")


def build(config, pbf, *, scope=True, say=print, root=EXTRACT_ROOT):
    """{key: payload} for the three caches of a city from `pbf`, each payload
    in the shape place_index and place_index_fetch.record read."""
    plan = unions()
    try:
        spec = osm_extract.parse_area(config.PLACE_AREA)
    except ValueError as exc:
        raise SystemExit(f"{place_index.city_of(config)[0]}: config.PLACE_AREA: {exc}")
    timestamp = osm_extract.extract_timestamp(pbf)
    outline = []

    def on_area(boundaries, area):
        outline.extend(osm_extract.out_geom(b) for b in boundaries)
        if scope:
            place_index_fetch.check_area(config, outline, out=say)
            check_region(pbf, area, root, out=say)

    got = osm_extract.query(pbf, spec, plan, on_area=on_area, say=say)
    streets = got["elements"]["streets"]
    main = ([osm_extract.out_body(e) for e in streets] + osm_extract.out_skel_nodes(streets)
            + [osm_extract.out_tags_center(e) for e in got["elements"]["main"]])
    extra = [osm_extract.out_tags_center(e) for e in got["elements"]["extra"]]
    source = f"{osm_extract.DOWNLOAD_HOST} ({Path(pbf).name}, filtered on this machine)"
    area_text = config.PLACE_AREA

    def payload(elements, query):
        return {"osm3s": {"timestamp_osm_base": timestamp,
                          "copyright": "The data included in this document is from www.openstreetmap.org. "
                                       "The data is made available under ODbL."},
                "elements": elements, "_fetched_from": source, "_query": query.format(area=area_text),
                "_extract": {"file": Path(pbf).name, "stats": got["stats"],
                             "method": "pipeline/place_extract_fetch.py: the query answered from the "
                                       "extract by pipeline/osm_extract.py's five rules, elements in "
                                       "ascending id order"}}
    return {"osm_place_outline": payload(outline, place_index_fetch.OUTLINE_QUERY),
            "osm_places": payload(main, place_index_fetch.QUERY),
            "osm_places_extra": payload(extra, place_index_fetch.EXTRA_QUERY)}


def run(config, *, force=False, pbf=None, out_dir=None, now=None, say=print, root=EXTRACT_ROOT):
    """The script's body; returns the paths written."""
    todo = targets(config, force, out_dir)
    for key, path, write in todo:
        if not write:
            say(f"{path.name}: kept (on disk; --force replaces it)")
    if not any(write for _, _, write in todo):
        return []
    unions()                                  # stop on a changed query before any read
    if getattr(config, "PLACE_SPLIT", None):
        say("config.PLACE_SPLIT is not used: an extract is read whole")
    if pbf is None:
        pbf = choose_extract(config, root, out=say)
    pbf = Path(pbf)
    if not pbf.exists():
        raise SystemExit(f"{pbf}: no such extract")
    timestamp = osm_extract.extract_timestamp(pbf)
    say(f"{pbf.name}: data dated {timestamp}")
    if any(write for key, _, write in todo if key != "osm_place_outline"):
        check_fresh(timestamp, pbf, now)
    payloads = build(config, pbf, say=say, root=root)
    written = []
    for key, path, write in todo:
        if not write:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        # Bytes, compact, in the order built: the same extract and config
        # give the same file.
        path.write_bytes(json.dumps(payloads[key], ensure_ascii=False).encode("utf-8"))
        kinds = {}
        for e in payloads[key]["elements"]:
            kinds[e["type"]] = kinds.get(e["type"], 0) + 1
        say(f"{path.name}: {len(payloads[key]['elements']):,} elements from {pbf.name} {kinds}")
        if out_dir is None:
            prov = place_index_fetch.record(config, path, key, "filtered from a regional extract")
            say(f"recorded in {prov.parent.name}/{prov.name} as {key}")
        written.append(path)
    return written


def selftest():
    import tempfile
    cases = []

    def case(label, ok):
        cases.append((label, bool(ok)))

    def stopped(fn):
        try:
            fn()
        except SystemExit as exc:
            return str(exc.code)
        return None

    plan = unions()
    case("the three unions are read from place_index_fetch's queries, line for line",
         len(plan["main"]) == len(_split(place_index_fetch.QUERY)[1].splitlines()) == 13
         and len(plan["extra"]) == len(_split(place_index_fetch.EXTRA_QUERY)[1].splitlines()) == 7
         and [c.text for c in plan["streets"]] == [STREETS])
    kept = place_index_fetch.QUERY
    try:
        place_index_fetch.QUERY = kept.replace("out tags center qt;", "out tags qt;")
        why = stopped(unions)
        place_index_fetch.QUERY = kept.replace('  way["waterway"="river"]["name"](area.a);',
                                               '  way["waterway"="river"]["name"](47.0,1.0,48.0,2.0);')
        why2 = stopped(unions)
        place_index_fetch.QUERY = kept.replace('  way["waterway"="river"]["name"](area.a);',
                                               '  way["waterway"="canal"]["name"](area.a);')
        moved = unions()["main"][-1].matches({"waterway": "canal", "name": "x"})
    finally:
        place_index_fetch.QUERY = kept
    case("a query changed outside its union stops the run", why and "changed shape" in why)
    case("a union line the extract route cannot answer stops the run", why2 and "cannot answer" in why2)
    case("a changed union line is followed with no edit here", moved)

    nodes, ways, relations = osm_extract.test_world()
    # A named place and a library inside Alpha, for the extra query.
    nodes[60] = (0.3, 0.3, {"amenity": "library", "name": "Alpha Library"})
    nodes[61] = (0.8, 0.2, {"railway": "station", "name": "Alpha Station"})
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        pbf = osm_extract.write_test_extract(d / "world-260101.osm.pbf", nodes, ways, relations,
                                             timestamp="2026-01-01T06:00:00Z")
        csv_path = d / "stations.csv"
        csv_path.write_bytes(b"station,lat,lon\nOne,0.2,0.2\nTwo,0.5,1.5\n")
        raw = d / "raw"

        class City:
            SLUG = "testville"
            PLACE_OSM_JSON = raw / "osm_places_2026-01-01.json"
            PLACE_OSM_EXTRA_JSON = raw / "osm_places_extra_2026-01-01.json"
            PLACE_AREA = "(id:3600000001,3600000002)"
            STATIONS_CSV = csv_path
            PROVENANCE_JSON = d / "provenance.json"

        class OneSided(City):
            STATIONS_CSV = d / "one.csv"

        OneSided.STATIONS_CSV.write_bytes(b"station,lat,lon\nOne,0.2,0.2\n")
        day = datetime.datetime(2026, 1, 3, tzinfo=datetime.timezone.utc)
        said = []
        written = run(City, pbf=pbf, now=day, say=said.append, root=d)
        main = json.loads(City.PLACE_OSM_JSON.read_bytes().decode("utf-8"))
        extra = json.loads(City.PLACE_OSM_EXTRA_JSON.read_bytes().decode("utf-8"))
        outline = json.loads(place_index.outline_cache(City).read_bytes().decode("utf-8"))
        case("a city with no cache gets all three, in the shape the index step reads",
             len(written) == 3 and main["osm3s"]["timestamp_osm_base"] == "2026-01-01T06:00:00Z"
             and [e["id"] for e in main["elements"] if "nodes" in e] == [201, 204]
             and {e["id"] for e in extra["elements"]} == {60}
             and [n for _, n, _ in place_index.municipalities(outline["elements"])] == ["Alpha", "Beta"])
        ways_first = [("nodes" in e, e["type"] == "node" and "tags" not in e) for e in main["elements"]]
        tagged = [(e["type"], e["id"]) for e in main["elements"] if "tags" in e and "nodes" not in e]
        rank = {"node": 0, "way": 1, "relation": 2}
        case("the main cache is street ways, then their nodes, then tagged elements, each by id",
             ways_first == sorted(ways_first, reverse=True)
             and tagged == sorted(tagged, key=lambda k: (rank[k[0]], k[1])) and len(tagged) >= 5)
        prov = json.loads(City.PROVENANCE_JSON.read_bytes().decode("utf-8"))
        case("provenance names the download host and the extract file, in the Overpass route's shape",
             set(prov) == {"osm_place_outline", "osm_places", "osm_places_extra"}
             and prov["osm_places"]["host"] == f"{osm_extract.DOWNLOAD_HOST} (world-260101.osm.pbf, filtered on this machine)"
             and prov["osm_places"]["osm_base"] == "2026-01-01T06:00:00Z"
             and prov["osm_places"]["query"] == place_index_fetch.QUERY.format(area=City.PLACE_AREA)
             and set(prov["osm_places"]) == {"bytes", "elements", "file", "host", "how", "osm_base", "query",
                                             "retrieved", "sha256"})
        first = {p.name: p.read_bytes() for p in written}
        # NEVER OVER A CACHE: a second run reads nothing and writes nothing.
        City.PLACE_OSM_JSON.write_bytes(b'{"elements": [], "marker": "an Overpass cache"}')
        said.clear()
        again = run(City, pbf=d / "absent.osm.pbf", now=day, say=said.append, root=d)
        case("NEVER OVER A CACHE: with every cache on disk nothing is read or written",
             again == [] and b"an Overpass cache" in City.PLACE_OSM_JSON.read_bytes()
             and sum("kept" in s for s in said) == 3)
        City.PLACE_OSM_EXTRA_JSON.unlink()
        again = run(City, pbf=pbf, now=day, say=said.append, root=d)
        case("only a missing cache is written; the ones on disk stay as they were",
             [p.name for p in again] == [City.PLACE_OSM_EXTRA_JSON.name]
             and b"an Overpass cache" in City.PLACE_OSM_JSON.read_bytes())
        again = run(City, pbf=pbf, now=day, force=True, say=said.append, root=d)
        case("--force replaces all three, and the same extract gives the same bytes (a fixed order)",
             len(again) == 3 and {p.name: p.read_bytes() for p in again} == first)
        why = stopped(lambda: run(City, pbf=pbf, out_dir=raw, now=day, say=said.append, root=d))
        case("--out refuses the folder the city's own caches live in", why and "own caches" in why)
        before = City.PROVENANCE_JSON.read_bytes()
        side = run(City, pbf=pbf, out_dir=d / "proof", now=day, say=said.append, root=d)
        case("--out writes all three elsewhere, the same bytes, and records nothing",
             {p.name: p.read_bytes() for p in side} == first and City.PROVENANCE_JSON.read_bytes() == before
             and all(p.parent == d / "proof" for p in side))
        # FRESHNESS, from the extract's own date.
        late = datetime.datetime(2026, 1, 9, tzinfo=datetime.timezone.utc)
        for p in (City.PLACE_OSM_JSON, City.PLACE_OSM_EXTRA_JSON):
            p.unlink()
        kept_outline = place_index.outline_cache(City).read_bytes()
        why = stopped(lambda: run(City, pbf=pbf, now=late, say=said.append, root=d))
        case("FRESHNESS: an extract older than 7 days writes no place cache",
             why and "older than 7 days" in why and not City.PLACE_OSM_JSON.exists()
             and place_index.outline_cache(City).read_bytes() == kept_outline)
        edge = datetime.datetime(2026, 1, 8, 5, tzinfo=datetime.timezone.utc)
        case("an extract just inside 7 days is accepted", len(run(City, pbf=pbf, now=edge, say=said.append, root=d)) == 2)
        for p in (City.PLACE_OSM_JSON, City.PLACE_OSM_EXTRA_JSON):
            p.unlink()
        place_index.outline_cache(City).unlink()
        City.PLACE_OSM_JSON.write_bytes(b"{}")
        City.PLACE_OSM_EXTRA_JSON.write_bytes(b"{}")
        got = run(City, pbf=pbf, now=late, say=said.append, root=d)
        case("the outline alone accepts an extract of any date",
             [p.name for p in got] == [place_index.OUTLINE_CACHE_NAME])
        # THE SCOPE STOP, before any place cache.
        for p in (City.PLACE_OSM_JSON, City.PLACE_OSM_EXTRA_JSON, place_index.outline_cache(City)):
            p.unlink()
        why = stopped(lambda: run(OneSided, pbf=pbf, now=day, say=said.append, root=d))
        case("THE SCOPE STOP: a municipality with no station stops the run and nothing is written",
             why and "Beta (relation/2)" in why and not City.PLACE_OSM_JSON.exists()
             and not place_index.outline_cache(City).exists())

        class Kyotoish(City):
            PLACE_AREA = '["name"="Alpha"]["admin_level"="8"]["boundary"="administrative"]'
            STATIONS_CSV = OneSided.STATIONS_CSV

        got = run(Kyotoish, pbf=pbf, out_dir=d / "tags", now=day, say=said.append, root=d)
        tagged_outline = json.loads(got[0].read_bytes().decode("utf-8"))["elements"]
        case("PLACE_AREA given as tag filters is answered", [e["id"] for e in tagged_outline] == [1])

        class Unreadable(City):
            PLACE_AREA = '["name"~"Alp"]'

        why = stopped(lambda: run(Unreadable, pbf=pbf, out_dir=d / "bad", now=day, say=said.append, root=d))
        case("a PLACE_AREA it cannot represent stops, naming it", why and "PLACE_AREA" in why)

        class Split(City):
            PLACE_SPLIT = {"bbox": (0, 0, 1, 2), "rows": 2, "cols": 2}

        said.clear()
        run(Split, pbf=pbf, out_dir=d / "split", now=day, say=said.append, root=d)
        case("PLACE_SPLIT is said to be unused, and the whole area is read",
             any("PLACE_SPLIT is not used" in s for s in said)
             and (d / "split" / City.PLACE_OSM_JSON.name).read_bytes() == first[City.PLACE_OSM_JSON.name])
        # The region check: the area against the extract's own outline.
        index = {"features": [{"properties": {"id": "world", "urls": {"pbf": "https://download.geofabrik.de/world-latest.osm.pbf"}},
                               "geometry": {"type": "Polygon", "coordinates": [[[-1, -1], [1.5, -1], [1.5, 2], [-1, 2], [-1, -1]]]}}]}
        (d / "index-v1.json").write_bytes(json.dumps(index).encode("utf-8"))
        why = stopped(lambda: run(City, pbf=pbf, out_dir=d / "edge", now=day, say=said.append, root=d))
        case("an area reaching past the extract's region stops the run", why and "next larger region" in why)
    for label, ok in cases:
        print(f"  {'ok ' if ok else 'BAD'} {label}")
    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("city")
    ap.add_argument("--force", action="store_true", help="replace caches already on disk")
    ap.add_argument("--pbf", metavar="FILE", help="read this extract; nothing is downloaded")
    ap.add_argument("--out", metavar="DIR", help="write all three caches here and record nothing (the proof)")
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")
    start = time.time()
    written = run(config, force=args.force, pbf=args.pbf, out_dir=args.out)
    if written:
        peak = ""
        try:
            import psutil
            mem = psutil.Process().memory_info()
            peak = f", peak memory {getattr(mem, 'peak_wset', mem.rss) / 2 ** 20:,.0f} MB"
        except ImportError:
            pass
        print(f"{len(written)} cache(s) written in {time.time() - start:.1f} s{peak}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(selftest() if "--selftest" in sys.argv else main())
