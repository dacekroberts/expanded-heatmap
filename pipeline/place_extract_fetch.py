"""Write a city's place caches from a regional OpenStreetMap extract filtered
on this machine: the second route beside pipeline/place_index_fetch.py's
Overpass queries, for the same three caches in the same shape. NOT a step:
drift_check.py never runs this file.

    python pipeline/place_extract_fetch.py <city> [--force] [--pbf FILE] [--out DIR] [--max-mb N]
    python pipeline/place_extract_fetch.py --selftest

It answers place_index_fetch.py's OUTLINE_QUERY, QUERY and EXTRA_QUERY, read
from that module as written (the unions are parsed line by line by
pipeline/osm_extract.py, and a QUERY whose shape has changed stops this
script), with osm_extract's five rules. Proven equal to Overpass's answers
on Tbilisi and Seattle, 2026-10-13 (osm-extract skill, "The proof").

  * A cache already on disk is KEPT, never written over, whoever wrote it;
    only --force replaces one. With every cache present nothing is read.
    A kept cache is first held to the CURRENT config.PLACE_AREA: the area
    its provenance entry records (or, with no entry for that file, the
    query the cache itself carries) must be the same area, or the run is
    refused naming both, before anything is written. A cache that records
    no area is kept with a warning.
  * --out DIR writes all three under DIR instead, records nothing, and
    refuses the folder the config's caches live in: the proof's route
    (scripts/place_extract_compare.py).
  * The extract: --pbf FILE, or the smallest region of the download server
    covering the city (its outline cache when there is one, else the map's
    stations), found, held and downloaded by osm_extract.download_extract.
    A held extract no older than PLACE_MAX_AGE_DAYS is used with no request.
    Two runs that need one regional file are safe at once: one download at
    a time on this machine (osm_extract.DownloadLock), and the second run
    finds the first one's file. No Overpass mirror is asked and no mirror
    lock (place_index_fetch.FetchLock) is taken.
  * SEVERAL REGIONS READ AS ONE (owner, 2026-10-13). An area that crosses a
    region border has one covering region, often a country-sized one. When
    that file is over --max-mb, the smallest set of regions (by bytes, at
    most osm_extract.SET_MAX_REGIONS) whose polygons together cover the
    area is taken instead, each file under --max-mb and each downloaded
    under the same rules, all of one dated run. The run says which set and
    why. --pbf given more than once names a set by hand. A set whose files
    do not state one data timestamp is refused; the cache's data date is
    that timestamp and its provenance names every file. One region is still
    taken whenever one under the cap covers the area.
  * AN AREA REACHING PAST ITS REGION'S POLYGON (2026-10-13; Gimpo and
    Incheon stopped on it). Two cases, told apart by the index. The part
    outside lies in ANOTHER region (both Korean cities: the Han estuary is
    inside north-korea's polygon): that region joins the set, and when the
    first region was chosen from the stations alone the command chooses
    again from the area it has just read, once. The part outside lies in NO
    other region (open sea): the region or set is accepted when that part
    is no more than OVERFLOW_MAX_SHARE of the area and every boundary
    closed from the files read; the run prints its size, and the cache's
    source line and "_extract" record it. Anything larger stops.
  * A way-made area and a relation that has lost its boundary tags are both
    taken by id: the area never depends on a boundary's tags.
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
# The largest regional file downloaded without a person naming a higher
# figure (--max-mb): a city whose smallest covering region is larger is a
# country-sized download, and a person's call.
MAX_MB = 1000
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
# The largest share of a search area that may lie outside the region(s) read
# when no other region of the index holds data there (water-side overflow).
# Measured 2026-10-13, the share of each area outside its region's polygon:
# Philadelphia 0.0002% (state line in the Delaware), Gimpo 0.01% (0.04 km2),
# Incheon 0.09% (8.83 km2 of 9,906); all three lay in a neighbouring region
# and went to a set, so NO overflow over open sea has been measured yet. One
# percent is ten times the largest of those: room for a coastline drawn a
# little differently, and far under what a wrong file or a hole in the index
# over land would leave out. Re-measure on the first coastal city accepted.
OVERFLOW_MAX_SHARE = 0.01
# The area a run read from an extract before stopping on AreaPastRegion, by
# city, and what the last region choice was made from: cli() chooses again
# from the area, once.
_AREA_READ, _LAST = {}, {}


class AreaPastRegion(SystemExit):
    """The search area reaches past the region(s) read, into another
    region of the index. `geom` is the area as read."""

    def __init__(self, message, geom):
        super().__init__(message)
        self.geom = geom


def km2(geom):
    """Geodesic area in square kilometres (WGS84)."""
    import pyproj
    return abs(pyproj.Geod(ellps="WGS84").geometry_area_perimeter(geom)[0]) / 1e6
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


_AREA_IN_QUERY = re.compile(r"area(.+?)->\.a;")


def recorded_area(config, key, path):
    """The area a cache on disk was fetched for, as its query states it:
    from the provenance entry `key` when that entry is about this file, else
    from the query the cache itself carries. None when neither records one."""
    prov_path = getattr(config, "PROVENANCE_JSON", None) or (
        Path(__file__).parent.parent / "outputs" / place_index.city_of(config)[0] / "provenance.json")
    query = None
    if Path(prov_path).exists():
        entry = json.loads(Path(prov_path).read_bytes().decode("utf-8")).get(key) or {}
        if entry.get("file") == path.name:
            query = entry.get("query")
    if query is None:
        try:
            query = json.loads(path.read_bytes().decode("utf-8")).get("_query")
        except (ValueError, AttributeError):
            query = None
    m = _AREA_IN_QUERY.search(query or "")
    return m.group(1) if m else None


def same_area(a, b):
    """True when two area selectors name the same area: ids in any order."""
    try:
        return osm_extract.parse_area(a) == osm_extract.parse_area(b)
    except ValueError:
        return str(a).replace(" ", "") == str(b).replace(" ", "")


def check_kept(config, key, path, say=print):
    """A cache about to be KEPT must be of the area the config names now. A
    cache fetched for another area would otherwise be kept in silence and
    indexed as the new one (asked for by the rollout session, 2026-10-13).
    Exits naming both areas; warns when the cache records none."""
    recorded = recorded_area(config, key, path)
    if recorded is None:
        say(f"WARNING: {path.name} records no area (no provenance entry for this file, no query in "
            f"it): not compared with config.PLACE_AREA")
        return
    if not same_area(recorded, config.PLACE_AREA):
        raise SystemExit(f"{path.name}: on disk for area {recorded}, and config.PLACE_AREA is now "
                         f"{config.PLACE_AREA}. Refused: a cache of another area is not kept as this "
                         f"one. Nothing was written. Fetch under a new cache name, or replace it with "
                         f"--force when that is meant.")


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


def choose_extract(config, root=EXTRACT_ROOT, out=print, max_mb=None, transport=None, now=None):
    """The extract for a city with no --pbf: the smallest region covering
    its outline cache when one is on disk, else its stations. When that
    region's file is over `max_mb` and the area crosses a region border, the
    smallest set of regions that together cover it, as an ExtractSet
    (osm_extract.choose_regions has the rule). A part of the area no larger
    than OVERFLOW_MAX_SHARE that no other region holds is passed over
    (water-side overflow). After a run stopped on AreaPastRegion the choice
    is made from the area that run read. `transport` and `now` are the
    selftest's."""
    from shapely.geometry import MultiPoint
    from shapely.ops import unary_union
    slug = place_index.city_of(config)[0]
    ocache = place_index.outline_cache(config)
    seen = _AREA_READ.get(slug)
    _LAST.update(slug=slug, from_area=seen is not None)
    if seen is not None:
        geom, basis = seen, "its search area as read from the extract"
    elif ocache.exists():
        munis = place_index.municipalities(json.loads(ocache.read_bytes().decode("utf-8"))["elements"])
        geom, basis = unary_union([g for _, _, g in munis]), "its outline cache"
    else:
        stations = place_index.map_stations(config)
        if not stations:
            raise SystemExit(f"{slug}: no outline cache and no stations to find its region by: name the "
                             f"extract with --pbf.")
        geom, basis = MultiPoint([(lon, lat) for _, lat, lon in stations]), f"its {len(stations)} stations"
    index = osm_extract.load_index(Path(root) / "index-v1.json")
    age, cap, sizes = place_index_fetch.PLACE_MAX_AGE_DAYS, (max_mb * 1024 * 1024 if max_mb else None), {}

    def size_of(feature):
        size = osm_extract.extract_size(feature, root, max_age_days=age, transport=transport, now=now)
        sizes[feature["properties"]["id"]] = size
        return size["bytes"]

    try:
        regions, why = osm_extract.choose_regions(index, geom, size_of, max_bytes=cap,
                                                  max_uncovered=OVERFLOW_MAX_SHARE)
    except osm_extract.NoRegionSet as exc:
        raise SystemExit(f"{slug}, by {basis}: {exc}")
    if len(regions) > 1:
        out(f"regions: {' + '.join(f['properties']['id'] for f in regions)}, read as one for {slug} by "
            f"{basis}: {why}")
        return osm_extract.download_set(regions, root, sizes=sizes, max_age_days=age, max_bytes=cap,
                                        transport=transport, now=now, out=out)
    region = regions[0]
    if why:
        out(f"region: {region['properties']['id']} for {slug} by {basis}: {why}")
    else:
        out(f"region: {region['properties']['id']}, the smallest covering {slug} by {basis}")
    return osm_extract.download_extract(region, root, max_age_days=age, max_bytes=cap, out=out,
                                        transport=transport, now=now)


def check_region(pbf, area, root=EXTRACT_ROOT, out=print):
    """Exit when the area reaches past the region the extract was cut to: a
    boundary can close there while the streets beyond the cut are absent.
    Said out loud when the region cannot be found (no index on disk, or a
    file under another name). For several extracts read as one, the area is
    held to the regions' polygons taken together.

    A part of the area outside the polygon(s) is one of two things
    (osm_extract.beyond): data ANOTHER region holds, which raises
    AreaPastRegion naming that region (it belongs in the set), or water no
    region holds, which is accepted up to OVERFLOW_MAX_SHARE of the area and
    returned as {"km2", "share", "outside", "accepted_as"} for the cache to
    record. The boundaries have closed from the file(s) by the time this
    runs: query() exits before it otherwise."""
    from shapely.geometry import shape
    from shapely.ops import unary_union
    files = osm_extract.as_files(pbf)
    index_path = Path(root) / "index-v1.json"
    features = []
    if index_path.exists():
        index = json.loads(index_path.read_bytes().decode("utf-8"))
        for f in files:
            m = osm_extract.DATED.match(f.name)
            found = [x for x in index["features"] if m and x.get("geometry")
                     and "pbf" in x["properties"].get("urls", {})
                     and osm_extract.region_short(x) == m.group("region")]
            features += found if len(found) == 1 else []
    if len(features) != len(files):
        out("  region: NOT checked against the extract's own outline (no index on disk, or the file "
            "is not named <region>-YYMMDD.osm.pbf)")
        return
    ids = " + ".join(f["properties"]["id"] for f in features)
    where = f"regions {ids} taken together" if len(files) > 1 else f"region {ids}"
    whole = unary_union(area.parts)
    rest, others = osm_extract.beyond(index, whole, features)
    if rest.is_empty or rest.area == 0:
        out(f"  region: the area lies wholly inside {ids}" + (" taken together" if len(files) > 1 else ""))
        return None
    size, share = km2(rest), km2(rest) / km2(whole)
    said = f"{size:,.2f} km2, {share:.3%} of the area,"
    if others:
        raise AreaPastRegion(f"{Path(pbf).name}: the search area reaches past {where}: {said} lies in "
                             f"{' + '.join(others)}. The regions are to be read as one set: run with no "
                             f"--pbf (they are then chosen from the area itself), or name every file "
                             f"with --pbf.", whole)
    if share > OVERFLOW_MAX_SHARE:
        raise SystemExit(f"{Path(pbf).name}: the search area reaches past {where}: {said} lies outside, in "
                         f"no other region of the index, over the {OVERFLOW_MAX_SHARE:.0%} accepted as "
                         f"water-side overflow. Use the next larger region.")
    out(f"  region: {said} lies outside {where}, where no other region of the index holds data: accepted "
        f"as water-side overflow (every boundary closed from the file(s) read)")
    return {"km2": round(size, 3), "share": round(share, 6), "outside": ids,
            "accepted_as": "water-side overflow: no other region of the index holds data there"}


def build(config, pbf, *, scope=True, say=print, root=EXTRACT_ROOT):
    """{key: payload} for the three caches of a city from `pbf`, each payload
    in the shape place_index and place_index_fetch.record read."""
    plan = unions()
    try:
        spec = osm_extract.parse_area(config.PLACE_AREA)
    except ValueError as exc:
        raise SystemExit(f"{place_index.city_of(config)[0]}: config.PLACE_AREA: {exc}")
    # One extract, or several read as one: the set's data date is its files'
    # one timestamp, and Path(pbf).name below names every file of it.
    timestamp = osm_extract.set_timestamp(pbf)
    outline, overflow = [], {}

    def on_area(boundaries, area):
        outline.extend(osm_extract.out_geom(b) for b in boundaries)
        if scope:
            place_index_fetch.check_area(config, outline, out=say)
            overflow.update(check_region(pbf, area, root, out=say) or {})

    got = osm_extract.query(pbf, spec, plan, on_area=on_area, say=say)
    streets = got["elements"]["streets"]
    main = ([osm_extract.out_body(e) for e in streets] + osm_extract.out_skel_nodes(streets)
            + [osm_extract.out_tags_center(e) for e in got["elements"]["main"]])
    extra = [osm_extract.out_tags_center(e) for e in got["elements"]["extra"]]
    passed_over = ""
    if overflow:
        # Recorded where both the cache and its provenance entry carry it.
        got["stats"]["overflow"] = dict(overflow)
        passed_over = (f"; {overflow['km2']:,.2f} km2 ({overflow['share']:.3%}) of the area lies outside "
                       f"the region(s), accepted as water-side overflow")
    source = f"{osm_extract.DOWNLOAD_HOST} ({Path(pbf).name}, filtered on this machine{passed_over})"
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


def run(config, *, force=False, pbf=None, out_dir=None, now=None, say=print, root=EXTRACT_ROOT,
        max_mb=None):
    """The script's body; returns the paths written."""
    todo = targets(config, force, out_dir)
    for key, path, write in todo:
        if not write:
            check_kept(config, key, path, say)
            say(f"{path.name}: kept (on disk; --force replaces it)")
    if not any(write for _, _, write in todo):
        return []
    unions()                                  # stop on a changed query before any read
    if getattr(config, "PLACE_SPLIT", None):
        say("config.PLACE_SPLIT is not used: an extract is read whole")
    if pbf is None:
        pbf = choose_extract(config, root, out=say, max_mb=max_mb)
    pbf = osm_extract.one_or_set(pbf)
    if not pbf.exists():
        raise SystemExit(f"{pbf}: no such extract")
    timestamp = osm_extract.set_timestamp(pbf)
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
        # An area made from a closed WAY (Miami names two: Overpass area id
        # 2400000000 + the way's id), beside one made from a relation.
        ways[500] = ([7, 8, 9, 10, 7], {"name": "Hole Village", "boundary": "census"})
        # A city relation that has lost its boundary and admin_level tags
        # (Buffalo's relation 175031, version 49): the area is taken by id.
        relations[6] = (relations[2][0], {"name": "Beta"})
        pbf2 = osm_extract.write_test_extract(d / "world2-260101.osm.pbf", nodes, ways, relations,
                                              timestamp="2026-01-01T06:00:00Z")
        (d / "three.csv").write_bytes(b"station,lat,lon\nOne,0.2,0.2\nTwo,0.5,1.5\nThree,0.5,0.5\n")

        class WayMade(City):
            PLACE_AREA = "(id:3600000001,2400000500)"
            STATIONS_CSV = d / "three.csv"
            PLACE_AREA_KEPT = {}

        got = run(WayMade, pbf=pbf2, out_dir=d / "waymade", now=day, say=said.append, root=d)
        way_outline = json.loads(got[0].read_bytes().decode("utf-8"))["elements"]
        way_main = json.loads(got[1].read_bytes().decode("utf-8"))["elements"]
        way_el = next((e for e in way_outline if e["type"] == "way"), {})
        case("an area made from a closed way is cut and outlined as a way with its geometry",
             [(e["type"], e["id"]) for e in way_outline] == [("way", 500), ("relation", 1)]
             and way_el.get("nodes") == [7, 8, 9, 10, 7] and len(way_el.get("geometry", [])) == 5
             and way_el["geometry"][0] == {"lat": 0.4, "lon": 0.4}
             and [n for _, n, _ in place_index.municipalities(way_outline)] == ["Alpha", "Hole Village"]
             and {e["id"] for e in way_main if e.get("tags", {}).get("place")} == {23, 24})

        class Untagged(City):
            PLACE_AREA = "(id:3600000001,3600000006)"

        got = run(Untagged, pbf=pbf2, out_dir=d / "untagged", now=day, say=said.append, root=d)
        bare = json.loads(got[0].read_bytes().decode("utf-8"))["elements"]
        bare_main = json.loads(got[1].read_bytes().decode("utf-8"))["elements"]
        case("a boundary relation with no boundary or admin_level tag is still the area its id names",
             [(e["id"], sorted(e["tags"])) for e in bare if e["id"] == 6] == [(6, ["name"])]
             and any(e["id"] == 400 for e in bare_main)
             and len(bare_main) == len(json.loads((d / "proof" / City.PLACE_OSM_JSON.name).read_bytes()
                                                  .decode("utf-8"))["elements"]))
        # The region check: the area against the extract's own outline.
        index = {"features": [{"properties": {"id": "world", "urls": {"pbf": "https://download.geofabrik.de/world-latest.osm.pbf"}},
                               "geometry": {"type": "Polygon", "coordinates": [[[-1, -1], [1.5, -1], [1.5, 2], [-1, 2], [-1, -1]]]}}]}
        (d / "index-v1.json").write_bytes(json.dumps(index).encode("utf-8"))
        why = stopped(lambda: run(City, pbf=pbf, out_dir=d / "edge", now=day, say=said.append, root=d))
        case("an area reaching past the extract's region stops the run", why and "next larger region" in why)

        # SEVERAL REGIONS READ AS ONE: the same world cut at lon = 1 into two
        # regional files (osm_extract.cut_world), under a country too large
        # for the cap.
        m = d / "multi"
        (m / "west").mkdir(parents=True)
        (m / "east").mkdir()
        nodes[80] = (0.5, 0.9, {"place": "suburb", "name": "On A Crossing Way"})
        nodes[81] = (0.5, 1.1, {})
        ways[205] = ([80, 81], {"highway": "residential", "name": "Crosses The Cut"})
        whole = osm_extract.write_test_extract(d / "world3-260101.osm.pbf", nodes, ways, relations,
                                               timestamp="2026-01-01T06:00:00Z")
        west_part = osm_extract.cut_world(nodes, ways, relations, lambda lon: lon < 1.0)
        east_part = osm_extract.cut_world(nodes, ways, relations, lambda lon: lon >= 1.0)
        west = osm_extract.write_test_extract(m / "west" / "west-260101.osm.pbf", *west_part,
                                              timestamp="2026-01-01T06:00:00Z")
        east = osm_extract.write_test_extract(m / "east" / "east-260101.osm.pbf", *east_part,
                                              timestamp="2026-01-01T06:00:00Z")
        host_url = f"https://{osm_extract.DOWNLOAD_HOST}/"

        def strip(rid, x0, x1):
            return {"properties": {"id": rid, "urls": {"pbf": f"{host_url}{rid}-latest.osm.pbf"}},
                    "geometry": {"type": "Polygon",
                                 "coordinates": [[[x0, -10], [x1, -10], [x1, 10], [x0, 10], [x0, -10]]]}}

        def write_index(folder, east_to=10):
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "index-v1.json").write_bytes(json.dumps({"features": [
                strip("country", -10, 10), strip("country/west", -10, 1.05),
                strip("country/east", 0.95, east_to)]}).encode("utf-8"))

        write_index(m)
        asked = []

        class Body:
            def __init__(self, data):
                self.data, self.pos = data, 0

            def read(self, n):
                chunk = self.data[self.pos:self.pos + n]
                self.pos += len(chunk)
                return chunk

            def close(self):
                pass

        def transport(method, url, headers):
            name = url.rsplit("/", 1)[-1]
            asked.append((method, name))
            if method == "HEAD" and "-latest" in name:
                return 302, {"Location": url.replace("-latest", "-260101")}, None
            data = whole.read_bytes()
            # The country file states 5 MB to a HEAD: over a 1 MB cap.
            size = len(data) if method == "GET" else 5 * 2 ** 20
            return 200, {"Content-Length": str(size)}, (Body(data) if method == "GET" else None)

        import os
        armed = os.environ.pop("HEATMAP_NO_NETWORK", None)
        try:
            said.clear()
            chosen = choose_extract(City, m, out=said.append, max_mb=1, transport=transport, now=day)
            case("a city crossing a region border, its one covering region over the cap, takes the smallest "
                 "set of regions, says which and why, and downloads nothing already held",
                 isinstance(chosen, osm_extract.ExtractSet) and chosen.name == "east-260101.osm.pbf + west-260101.osm.pbf"
                 and any(s.startswith("regions: country/east + country/west, read as one for testville") and
                         "country, is 5 MB, over the 1 MB cap" in s for s in said)
                 and [a[0] for a in asked] == ["HEAD", "HEAD"] and not (m / osm_extract.LEDGER_NAME).exists())
            said.clear()
            asked.clear()
            single = choose_extract(City, m, out=said.append, max_mb=100, transport=transport, now=day)
            case("the same city with its covering region under the cap takes that ONE region, in the same words",
                 single.name == "country-260101.osm.pbf" and "region: country, the smallest covering testville by "
                 "its 2 stations" in said and ("GET", "country-260101.osm.pbf") in asked)
        finally:
            if armed is not None:
                os.environ["HEATMAP_NO_NETWORK"] = armed
        ref = run(City, pbf=whole, out_dir=d / "ref", now=day, say=said.append, root=d / "no-index")
        said.clear()
        two = run(City, pbf=chosen, out_dir=d / "two", now=day, say=said.append, root=m)

        def elements(paths):
            return [json.loads(p.read_bytes().decode("utf-8"))["elements"] for p in paths]
        two_main = json.loads(two[1].read_bytes().decode("utf-8"))
        case("the set gives the three caches the whole file gives, element for element, each id once",
             elements(two) == elements(ref) and [e["id"] for e in two_main["elements"] if "nodes" in e].count(205) == 1
             and any("taken together" in s for s in said) and any("taken once" in s for s in said))
        case("a cache from a set names every file it was read from and the set's one data date",
             two_main["_fetched_from"] == f"{osm_extract.DOWNLOAD_HOST} (east-260101.osm.pbf + west-260101.osm.pbf, "
                                          "filtered on this machine)"
             and two_main["_extract"]["stats"]["files"] == ["east-260101.osm.pbf", "west-260101.osm.pbf"]
             and two_main["osm3s"]["timestamp_osm_base"] == "2026-01-01T06:00:00Z")
        by_hand = run(City, pbf=[str(west), str(east)], out_dir=d / "hand", now=day, say=said.append, root=m)
        case("several --pbf name a set by hand, and the order of the files does not change the elements",
             elements(by_hand) == elements(ref))
        late_east = osm_extract.write_test_extract(d / "east-260102.osm.pbf", *east_part,
                                                   timestamp="2026-01-02T06:00:00Z")
        why = stopped(lambda: run(City, pbf=[west, late_east], out_dir=d / "apart", now=day, say=said.append, root=m))
        case("a set whose files are of two data dates is refused before anything is read or written",
             why and "not one snapshot" in why and not (d / "apart").exists())
        write_index(d / "multi2", east_to=1.5)
        why = stopped(lambda: run(City, pbf=chosen, out_dir=d / "past", now=day, say=said.append, root=d / "multi2"))
        case("an area reaching past the regions of a set taken together stops the run",
             why and "country/east + country/west taken together" in why and not (d / "past").exists())

        # THE AREA PAST ITS REGION. The whole file under west's name, west's
        # polygon ending at 1.5: a quarter of the area lies in east.
        (d / "over" / "west").mkdir(parents=True)
        as_west = d / "over" / "west" / "west-260101.osm.pbf"
        as_west.write_bytes(whole.read_bytes())

        def over_index(folder, west_to, east_from, east_to):
            folder.mkdir(parents=True, exist_ok=True)
            rows = [strip("country", -10, 10), strip("country/west", -10, west_to)]
            if east_from is not None:
                rows.append(strip("country/east", east_from, east_to))
            (folder / "index-v1.json").write_bytes(json.dumps({"features": rows}).encode("utf-8"))

        over_index(d / "over", 1.5, 1.5, 10)
        caught = []
        try:
            run(City, pbf=as_west, out_dir=d / "sibling", now=day, say=said.append, root=d / "over")
        except AreaPastRegion as exc:
            caught.append(exc)
        case("OVERFLOW INTO ANOTHER REGION is never accepted: the run stops naming the region that holds "
             "the rest, and nothing is written",
             caught and "reaches past region country/west" in str(caught[0]) and "lies in country/east" in str(caught[0])
             and "25." in str(caught[0]) and not (d / "sibling").exists())
        (d / "over" / "east").mkdir()
        (d / "over" / "east" / "east-260101.osm.pbf").write_bytes(east.read_bytes())
        (d / "over" / "west" / "west-260101.osm.pbf").write_bytes(west.read_bytes())
        kept_seen = dict(_AREA_READ)
        try:
            _AREA_READ[City.SLUG] = caught[0].geom if caught else None
            said.clear()
            again = choose_extract(City, d / "over", out=said.append, max_mb=1, transport=transport, now=day)
            case("the choice made again from the area as read takes the set that holds all of it",
                 isinstance(again, osm_extract.ExtractSet) and again.name == "east-260101.osm.pbf + west-260101.osm.pbf"
                 and any("by its search area as read from the extract" in s for s in said) and _LAST.get("from_area"))
        finally:
            _AREA_READ.clear()
            _AREA_READ.update(kept_seen)
        # Open sea: east's polygon ends at 1.99 and nothing else is there.
        over_index(d / "sea", 1.05, 0.95, 1.99)
        said.clear()
        sea = run(City, pbf=chosen, out_dir=d / "sea-out", now=day, say=said.append, root=d / "sea")
        sea_main = json.loads(sea[1].read_bytes().decode("utf-8"))
        sea_over = sea_main["_extract"]["stats"].get("overflow", {})
        case("WATER-SIDE OVERFLOW: a part of the area no other region holds, under the bound, is accepted; "
             "its size is printed and recorded in the cache and its source line, and the elements are the same",
             elements(sea) == elements(ref) and abs(sea_over.get("share", 0) - 0.0051) < 2e-4 and sea_over.get("km2", 0) > 0
             and sea_over.get("outside") == "country/east + country/west"
             and "accepted as water-side overflow" in sea_main["_fetched_from"]
             and any("accepted as water-side overflow" in s and "km2" in s for s in said))
        over_index(d / "sea2", 1.05, 0.95, 1.9)
        why = stopped(lambda: run(City, pbf=chosen, out_dir=d / "sea2-out", now=day, say=said.append, root=d / "sea2"))
        case("an overflow over the bound stops, with its size, though no other region holds it",
             why and "over the 1% accepted" in why and "next larger region" in why and not (d / "sea2-out").exists())
        (d / "open" / "west").mkdir(parents=True)
        (d / "open" / "west" / "west-260101.osm.pbf").write_bytes(west.read_bytes())
        over_index(d / "open", 0.999, None, None)

        class AlphaOnly(OneSided):
            PLACE_AREA = "(id:3600000001)"

        why = stopped(lambda: run(AlphaOnly, pbf=d / "open" / "west" / "west-260101.osm.pbf", out_dir=d / "open-out",
                                  now=day, say=said.append, root=d / "open"))
        case("a boundary that does not close from the file read is refused before any overflow is weighed",
             why and "not whole in this extract" in why and not (d / "open-out").exists())

        # A KEPT cache is held to the area the config names now.
        run(City, pbf=chosen, now=day, say=said.append, root=m)
        prov = json.loads(City.PROVENANCE_JSON.read_bytes().decode("utf-8"))
        case("provenance from a set names every file",
             "east-260101.osm.pbf + west-260101.osm.pbf" in prov["osm_places"]["host"])
        kept_bytes = City.PLACE_OSM_JSON.read_bytes()

        class Moved(City):
            PLACE_AREA = "(id:3600000001)"

        why = stopped(lambda: run(Moved, pbf=chosen, now=day, say=said.append, root=m))
        case("KEPT CACHE, AREA CHANGED: a cache recorded for another area is refused, naming both areas, "
             "and nothing is written",
             why and "(id:3600000001,3600000002)" in why and "is now (id:3600000001)." in why
             and City.PLACE_OSM_JSON.read_bytes() == kept_bytes)

        class Reordered(City):
            PLACE_AREA = "(id:3600000002, 3600000001)"

        said.clear()
        case("the same ids in another order are the same area: the caches are kept, with no warning",
             run(Reordered, pbf=chosen, now=day, say=said.append, root=m) == []
             and sum("kept" in s for s in said) == 3 and not any("WARNING" in s for s in said))

        class Unrecorded(City):
            PROVENANCE_JSON = d / "no-provenance.json"

        class UnrecordedMoved(Unrecorded):
            PLACE_AREA = "(id:3600000001)"

        why = stopped(lambda: run(UnrecordedMoved, pbf=chosen, now=day, say=said.append, root=m))
        case("with no provenance entry the area is read from the query the cache itself carries",
             why and "(id:3600000001,3600000002)" in why and "Refused" in why)
        City.PLACE_OSM_JSON.write_bytes(b'{"elements": []}')
        said.clear()
        case("KEPT CACHE, NO AREA RECORDED: it is kept, with a printed warning naming the file",
             run(Unrecorded, pbf=chosen, now=day, say=said.append, root=m) == []
             and [s for s in said if s.startswith("WARNING")] == [
                 f"WARNING: {City.PLACE_OSM_JSON.name} records no area (no provenance entry for this file, "
                 f"no query in it): not compared with config.PLACE_AREA"]
             and City.PLACE_OSM_JSON.read_bytes() == b'{"elements": []}')
    for label, ok in cases:
        print(f"  {'ok ' if ok else 'BAD'} {label}")
    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("city")
    ap.add_argument("--force", action="store_true", help="replace caches already on disk")
    ap.add_argument("--pbf", metavar="FILE", action="append",
                    help="read this extract; nothing is downloaded. Repeat it to read several as one")
    ap.add_argument("--max-mb", type=int, default=MAX_MB, metavar="N",
                    help=f"the largest regional file downloaded without a person (default {MAX_MB})")
    ap.add_argument("--out", metavar="DIR", help="write all three caches here and record nothing (the proof)")
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")
    start = time.time()
    written = run(config, force=args.force, pbf=args.pbf, out_dir=args.out, max_mb=args.max_mb)
    if written:
        peak = ""
        try:
            import psutil
            mem = psutil.Process().memory_info()
            peak = f", peak memory {getattr(mem, 'peak_wset', mem.rss) / 2 ** 20:,.0f} MB"
        except ImportError:
            pass
        print(f"{len(written)} cache(s) written in {time.time() - start:.1f} s{peak}")


def cli():
    """main(), and main() once more when the region was chosen from the
    stations or an outline and the area then read reaches into another
    region: the second choice is made from that area and takes the set. A
    run given --pbf, or one already chosen from the area, is not repeated."""
    _AREA_READ.clear()
    _LAST.clear()
    try:
        return main()
    except AreaPastRegion as exc:
        if not _LAST.get("slug") or _LAST.get("from_area"):
            raise
        _AREA_READ[_LAST["slug"]] = exc.geom
        print(f"{exc}\nThe region(s) were not chosen from the area itself: choosing again from the area "
              f"as read.")
        return main()


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(selftest() if "--selftest" in sys.argv else cli())
