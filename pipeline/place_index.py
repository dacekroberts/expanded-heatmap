"""Build a city's place-search index from its cached OpenStreetMap places.

Shared by every city's `step2b_place_index.py`. Reads the cache that
pipeline/place_index_fetch.py wrote (config.PLACE_OSM_JSON) and never fetches.

Places only, never business records (owner, 2026-10-07; DECISIONS.md "Four
ideas assessed", item 3): streets, intersections, stations, neighborhoods and
landmarks. Any landmark carrying a commercial tag (shop, office, craft, brand,
cuisine, a lodging or eating amenity) is dropped and counted, so a place of
worship that is also a gift shop never enters the index. Nothing joins the
index to the business registers.

The file is searched ENTIRELY in the visitor's browser (map_common's
PLACE_SEARCH_SCRIPT), downloaded on first use of the search box, never
embedded in a map: the iPhone literal limit (110,861) is per map, and the
index must not add to it.

FORMAT (compact; one row per place, kinds by index into "kinds"):
    {"license": {name, url, attribution, attribution_url, notice,
     data_retrieved}, "city": ..., "fold": "ja" | null, "kinds": [...],
     "rows": [[kind, lat, lon, name, alt, bbox_or_0], ...]}
`alt` is the other names joined by "|"; `bbox` is [s, w, n, e] for a street
(the map fits it) and 0 for a point. Coordinates at 5 dp (about 1 m).

LICENCE: ODbL 1.0. The index is a Derivative Database of OpenStreetMap (OSMF's
Substantial guideline: a whole city's streets), published under ODbL; the
notice travels inside the file (`licence`) and the map shows the credit.
"""
import difflib
import hashlib
import json
import math
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

STATIC_DIR = Path(__file__).parent.parent / "app" / "static" / "places"


def index_path(slug):
    return STATIC_DIR / f"{slug}.json"


def crossings_path(slug):
    """The street-pair intersections, a file of their own (owner, 2026-10-08:
    the index's size, a top-line item): fetched only when a search asks for an
    intersection, so a first search downloads and holds about half as much
    (Seattle 563 to 269 KB gzipped, measured)."""
    return STATIC_DIR / "crossings" / f"{slug}.json"


def streets_path(slug):
    """Each street row's drawn length (STREET_SIMPLIFY_M), a file of its own:
    fetched at the first street picked from the search, so opening the search
    costs nothing more."""
    return STATIC_DIR / "streets" / f"{slug}.json"


def _site_url(path, data):
    """The site path of a file under app/static/, stamped with the hash of its
    content `data` (index_url's reason)."""
    rel = path.relative_to(STATIC_DIR.parent).as_posix()
    return f"/app/static/{rel}?v={hashlib.sha256(data).hexdigest()[:12]}"


def ids_path(slug):
    return Path(__file__).parent.parent / "outputs" / slug / "place_ids.json"


def summary_path(slug):
    return Path(__file__).parent.parent / "outputs" / slug / "place_search.json"


def files(index, slug):
    """{path: bytes} for the files an index step writes: the intersections
    file, the street lines file, the index (served as-is: bytes, LF only, no
    BOM), the id side file and
    the page's summary, outputs/<slug>/place_search.json (the languages the
    page names, the count and the retrieval date; the app reads the summary,
    never the index, so a page load costs no megabyte). Computed without
    writing, so scripts/check_place_index_drift.py can compare them with the
    files on disk. `index` is build()'s, and is not changed."""
    index = dict(index)
    cross = index.pop("crossing_rows")
    # Never in the served index: the summary alone carries them.
    not_open = index.pop("stations_not_open", [])
    munis = index.pop("area_municipalities", [])
    row_osm = index.pop("row_osm", [])
    lines = index.pop("street_lines", [])
    index.pop("street_lines_raw", None)
    index.pop("wikidata_asked", None)
    cpath = crossings_path(slug)
    cbytes = json.dumps({"license": index["license"], "schema": SCHEMA, "city": index["city"],
                         "part_of": f"{slug}.json", "rows": cross},
                        ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    # The index carries the intersections file's hashed path, so a rebuilt
    # intersections file is never served from a browser's old copy.
    index["crossings"] = _site_url(cpath, cbytes)
    # THE STREET LINES FILE (street_lines): `rows` ascending, each a street
    # row's position in the index, and `lines` beside it, that street's
    # polylines. A line is a flat list of integers in units of 1/`scale`
    # degree: the first latitude and longitude, then each later point as its
    # difference from the one before. Hashed into the index like the
    # intersections file.
    stpath = streets_path(slug)
    stbytes = json.dumps({"license": index["license"], "schema": SCHEMA, "city": index["city"],
                          "part_of": f"{slug}.json", "scale": 100000,
                          "rows": [r for r, _ in lines], "lines": [l for _, l in lines]},
                         ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    index["streets"] = _site_url(stpath, stbytes)
    ibytes = json.dumps(index, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    summary = {"index": f"app/static/places/{slug}.json", "places": len(index["rows"]) + len(cross),
               "data_retrieved": index["license"]["data_retrieved"], "languages": index["languages"],
               # The stations skipped as not yet open at this build (OSM id,
               # name, tag): scripts/check_place_unopened.py holds
               # docs/place_search_unopened_stations.json to this list.
               "stations_not_open": not_open,
               # The municipalities the index covers, each with the number of
               # the map's stations inside it: scripts/check_place_scope.py
               # fails one with none and no entry in config.PLACE_AREA_KEPT.
               "area": munis}
    sbytes = (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    # THE ID SIDE FILE (owner, 2026-10-12, for the travel app): the OSM object
    # behind each station, junction, landmark and neighborhood row, by the
    # row's position in the index. Streets and rivers carry none (each is
    # many ways). Two parallel lists, rows ascending. Committed under
    # outputs/, never under app/static: no browser fetches it. It names the
    # exact index it describes by that file's sha256, so a reader can refuse
    # a side file that belongs to another build.
    pairs = [(i, o) for i, o in enumerate(row_osm) if o]
    ids = {"schema": SCHEMA, "index": f"app/static/places/{slug}.json",
           "index_sha256": hashlib.sha256(ibytes).hexdigest(),
           "license": index["license"]["name"], "attribution": index["license"]["attribution"],
           "rows": [i for i, _ in pairs], "osm": [o for _, o in pairs]}
    idbytes = (json.dumps(ids, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    return {cpath: cbytes, stpath: stbytes, index_path(slug): ibytes, summary_path(slug): sbytes,
            ids_path(slug): idbytes}


def write(index, slug):
    """Write files(index, slug) and return the index's path."""
    for path, data in files(index, slug).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return index_path(slug)


# Folds the browser applies to Latin text on both sides of a match (the search
# script's norm()): "ja" folds Japanese long vowels written out, shijou =
# shijo. A city sets config.PLACE_FOLD to one of these, or None.
FOLDS = (None, "ja")


# THE SEARCHED AREA (owner, 2026-10-12: "a defined rule ... for what is
# included in search indexers vs what isn't", and a border drawn on the map
# "where search is no longer usable"). An index covers exactly the
# municipalities config.PLACE_AREA names: the boundary the map's businesses
# are cut to and, on a regional map, every municipality a drawn station sits
# in. Nothing wider without the owner's word, recorded per municipality in
# config.PLACE_AREA_KEPT ({"relation/123": "why"}). The index carries the
# area as {"names": [...], "outline": [ring, ...]}: the municipalities' names
# and their merged outline, each ring a flat [lat, lon, lat, lon, ...].
# OUTLINE_SIMPLIFY_M is measured in the city's own projected CRS, never in
# degrees. Re-measure the index sizes if either constant changes.
# THE FILES' SCHEMA NUMBER (owner, 2026-10-12, for the travel app that reads
# them): in the index and in its intersections file. 1 is the format with
# "area". Raise it when a reader of the files would have to change: a key
# removed or renamed, a row's fields reordered. A key added is not a break.
SCHEMA = 1
OUTLINE_SIMPLIFY_M = 40
# A part under this share of the whole area is left undrawn (islets, slivers).
OUTLINE_MIN_SHARE = 0.002


OUTLINE_CACHE_NAME = "osm_place_outline_v1.json"

# A STREET'S DRAWN LENGTH (owner, 2026-10-13: a street picked without an
# intersection shows its whole length). Each street row's ways, joined end to
# end where they share an end node and simplified by STREET_SIMPLIFY_M in the
# city's own projected CRS, go to a side file (streets_path) the browser
# fetches at the first street picked; the index carries no geometry. A line is
# what OSM names with exactly the row's name: it stops where the name changes
# ("Pike Street" ends where "East Pike Street" begins) and at the edge of the
# fetched area. Re-measure the files' sizes if the constant changes.
STREET_SIMPLIFY_M = 10


def chain_ways(ways, nodes):
    """The polylines [[(lat, lon), ...], ...] of one street's `ways`
    ([(way id, [node id, ...]), ...]), joined end to end where two share an
    end node. In way-id order, so a rebuild gives the same lines. A divided
    street stays two lines, a street with a gap as many as it has pieces."""
    left = [list(ids) for _, ids in sorted(ways)]
    left = [[n for n in ids if n in nodes] for ids in left]
    left = [ids for ids in left if len(ids) > 1]
    ends = defaultdict(list)                  # end node -> positions in `left`
    for i, ids in enumerate(left):
        ends[ids[0]].append(i)
        ends[ids[-1]].append(i)
    used = [False] * len(left)

    def take(node):
        for i in ends[node]:
            if not used[i]:
                used[i] = True
                return left[i] if left[i][0] == node else left[i][::-1]
        return None

    out = []
    for i, ids in enumerate(left):
        if used[i]:
            continue
        used[i] = True
        cur = list(ids)
        # A closed way (a roundabout, a loop street) is whole as it is.
        while cur[0] != cur[-1]:
            nxt = take(cur[-1])
            if nxt is None:
                break
            cur += nxt[1:]
        while cur[0] != cur[-1]:
            nxt = take(cur[0])
            if nxt is None:
                break
            cur = nxt[::-1][:-1] + cur
        out.append([nodes[n] for n in cur])
    return out


def street_lines(raw, crs_projected):
    """[[row, [line, ...]], ...] from build()'s "street_lines_raw", each line
    simplified by STREET_SIMPLIFY_M in `crs_projected` and written as a flat
    list of integers: the first point's latitude and longitude in units of
    1e-5 degree, then each later point as its difference from the one before
    (62% of the bytes of plain coordinates, measured on Seattle)."""
    from pyproj import Transformer
    from shapely.geometry import LineString
    to_m = Transformer.from_crs("EPSG:4326", crs_projected, always_xy=True).transform
    to_deg = Transformer.from_crs(crs_projected, "EPSG:4326", always_xy=True).transform
    out = []
    for row, lines in raw:
        enc = []
        for line in lines:
            xs, ys = to_m([p[1] for p in line], [p[0] for p in line])
            kept = LineString(list(zip(xs, ys))).simplify(STREET_SIMPLIFY_M, preserve_topology=False)
            if kept.is_empty or len(kept.coords) < 2:
                continue
            lons, lats = to_deg(*zip(*kept.coords))
            pts = [(round(la * 1e5), round(lo * 1e5)) for la, lo in zip(lats, lons)]
            flat = [pts[0][0], pts[0][1]]
            for a, b in zip(pts, pts[1:]):
                if a != b:
                    flat += [b[0] - a[0], b[1] - a[1]]
            if len(flat) > 2:
                enc.append(flat)
        if enc:
            out.append([row, enc])
    return out


def outline_cache(config):
    """The cache place_index_fetch.py writes the area's boundaries to:
    OUTLINE_CACHE_NAME beside the place cache. One name for every city, so
    scripts/place_search_fetch_queue.py finds it from the place cache's path;
    a re-pull takes a new name here."""
    return Path(config.PLACE_OSM_JSON).parent / OUTLINE_CACHE_NAME


def municipalities(elements):
    """[(osm id "relation/123", name, shapely geometry in EPSG:4326)] for the
    boundaries an OUTLINE_QUERY answer holds. A relation's outer ways are
    polygonized; its inner rings are ignored, so an enclave reads as covered.
    The name is the English one when OSM has it."""
    from shapely.geometry import LineString, Polygon
    from shapely.ops import polygonize, unary_union
    out = []
    for e in elements:
        tags = e.get("tags") or {}
        if e["type"] == "relation":
            lines = [LineString([(g["lon"], g["lat"]) for g in m["geometry"]])
                     for m in e.get("members", [])
                     if m["type"] == "way" and m.get("role") in ("outer", "", None)
                     and len(m.get("geometry") or []) >= 2]
            geom = unary_union(list(polygonize(unary_union(lines)))) if lines else None
        elif e["type"] == "way" and len(e.get("geometry") or []) >= 4:
            geom = Polygon([(g["lon"], g["lat"]) for g in e["geometry"]])
        else:
            continue
        if geom is None or geom.is_empty:
            raise ValueError(f"{e['type']}/{e['id']} ({tags.get('name')}): no closed outline in the cache")
        out.append((f"{e['type']}/{e['id']}", tags.get("name:en") or tags.get("name") or "", geom))
    return sorted(out, key=lambda m: m[1])


def outline(munis, crs_projected):
    """The index's "area" for municipalities() of a city: names in order and
    the merged outline's rings, simplified by OUTLINE_SIMPLIFY_M in
    `crs_projected` (the city's own) and rounded to 5 decimals."""
    from pyproj import Transformer
    from shapely.ops import transform, unary_union
    to_m = Transformer.from_crs("EPSG:4326", crs_projected, always_xy=True).transform
    to_deg = Transformer.from_crs(crs_projected, "EPSG:4326", always_xy=True).transform
    merged = unary_union([transform(to_m, g).buffer(0) for _, _, g in munis])
    merged = merged.simplify(OUTLINE_SIMPLIFY_M, preserve_topology=True)
    parts = list(getattr(merged, "geoms", [merged]))
    parts = [g for g in parts if g.area >= OUTLINE_MIN_SHARE * merged.area]
    rings = []
    for g in sorted(parts, key=lambda g: -g.area):
        ring = []
        for x, y in transform(to_deg, g.exterior).coords:
            ring += [round(y, 5), round(x, 5)]
        rings.append(ring)
    return {"names": [n for _, n, _ in munis], "outline": rings}


def scope_refusals(munis, counts, kept):
    """One sentence per municipality the scope rule refuses: none of the
    map's stations inside (`counts`, by OSM id) and no entry in `kept`
    (config.PLACE_AREA_KEPT). Empty when the area stands. Used by the fetch,
    before its heavy queries, and by scripts/check_place_scope.py's rule B on
    the committed summary."""
    return [f"{name} ({osm_id}) holds none of the map's stations and has no entry in "
            f"config.PLACE_AREA_KEPT"
            for osm_id, name, _ in munis if counts.get(osm_id) == 0 and osm_id not in kept]


def stations_per_municipality(munis, stations):
    """{osm id: number of the map's stations inside}, for the ceiling check
    (scripts/check_place_scope.py)."""
    from shapely.geometry import Point
    from shapely.prepared import prep as _prep
    counts = {}
    for osm_id, _, geom in munis:
        inside = _prep(geom).contains
        counts[osm_id] = sum(1 for _, lat, lon in stations if inside(Point(lon, lat)))
    return counts


# AN ARTICLE OF ITS OWN, ASKED OF WIKIDATA (owner, 2026-10-13: "yes and
# delegate"). Most notable objects carry a wikidata tag and no wikipedia tag
# (1,278 works of public art left the 19 on the tag alone). The fetch script,
# pipeline/place_wikidata_fetch.py, asks Wikidata once which of a city's
# entries have a Wikipedia article in any language and caches the answer:
#     {"_source": {...}, "articles": {"Q1": ["enwiki", "frwiki"], "Q2": [], "Q3": null}}
# an empty list for an entry with no article, null for one the lookup could
# not read. This module only READS the cache (a step never fetches). With no
# cache on disk the rules fall back to the wikipedia tag and the step says
# so; with a cache that lacks an entry the step needs, it stops naming the
# fetch script. Read for public art and libraries only (rules 16
# and 39); every other "own article" test still reads the wikipedia tag.
#
# THE LOOKUP IS NARROW BY RULE (owner, 2026-10-13: "narrow the lookup and
# hard code the narrowing as a rule"). Wikidata is asked only about an object
# of a kind listed here, the kinds a rule reads the answer for: the 19 live
# cities carry 14,071 entries on objects with no wikipedia tag, and the rules
# read 1,849 of them. article_lookup_kind is the ONE test: the rule below
# and the fetch script both call it, so the fetch cannot ask about a kind no
# rule reads, and a rule cannot read a kind the fetch did not ask about. A
# new kind is added here, with the owner's ruling, and nowhere else.
ARTICLE_LOOKUP_KINDS = (
    ("tourism", "artwork", "artwork"),      # rule 16, public art
    ("amenity", "library", "library"),      # rule 39, libraries
)


def article_lookup_kind(tags):
    """The kind ("artwork", "library") under which an object's own article
    is asked of Wikidata, None for every other object."""
    for key, value, kind in ARTICLE_LOOKUP_KINDS:
        if tags.get(key) == value:
            return kind
    return None


def wikidata_cache(config):
    """The path of a city's Wikidata article cache: config.PLACE_WIKIDATA_JSON,
    else beside the place cache, "osm_places" in its name read as
    "wikidata_articles"."""
    given = getattr(config, "PLACE_WIKIDATA_JSON", None)
    if given is not None:
        return Path(given)
    main = Path(config.PLACE_OSM_JSON)
    return main.with_name(main.name.replace("osm_places", "wikidata_articles", 1))


def read_wikidata_articles(path):
    """{wikidata id: [wiki, ...] or None} from a cache file, None when the
    file is not there. No network, and no import of the fetch module."""
    path = Path(path)
    if not path.is_file():
        return None
    return dict(json.loads(path.read_text(encoding="utf-8")).get("articles") or {})


def has_article(tags, articles, own=False, own_entry=True):
    """True when an object has an article of its own: `own`, its wikipedia
    tag read as today (own_article: not a section, an anchored list or its
    subject's), OR its Wikidata entry has a Wikipedia article in the cache
    `articles` AND the entry is the object's own (`own_entry`: no other
    object of the city's cache carries it, build()'s own_item)."""
    if own:
        return True
    wd = (tags.get("wikidata") or "").strip()
    return bool(wd and own_entry and (articles or {}).get(wd))


def city_of(config):
    """(slug, name) for a city's config module, pipeline.<slug>.config. The
    slug comes from the module path, since 78 of 170 configs had no SLUG
    (2026-10-08); the name, which only the index's "city" field carries, from
    NAME or CITY_NAME, else the slug in title case."""
    slug = getattr(config, "SLUG", None) or config.__name__.split(".")[-2]
    name = getattr(config, "NAME", None) or getattr(config, "CITY_NAME", None)
    return slug, name if isinstance(name, str) else slug.replace("_", " ").title()


def run(config):
    """A city's index step: read the cache place_index_fetch.py wrote, build,
    write the index and the page's summary, report. Never fetches. A city's
    step2b_place_index.py calls this and nothing else.

    config needs PLACE_OSM_JSON and PLACE_OSM_EXTRA_JSON (each dated by its
    name: osm_places[_vN|_extra]_<date>.json), PLACE_LANGUAGES and
    PLACE_FOLD; the slug and name come from city_of."""
    slug, _ = city_of(config)
    index, report = build_city(config)
    stations = map_stations(config)
    if stations is None:
        print(f"  coverage: not checked (no {getattr(config, 'STATIONS_CSV', 'STATIONS_CSV')})")
    else:
        bare = uncovered_stations(index["rows"], stations,
                                  lines=decode_lines([l for _, l in index.get("street_lines", [])]))
        bare, wrong = quiet_stations(getattr(config, "PLACE_QUIET_STATIONS", {}), stations, bare)
        if wrong:
            import sys
            sys.exit("; ".join(wrong))
        if bare:
            import sys
            sys.exit(f"{len(bare)} station(s) on the {slug} map have no indexed place within "
                     f"{COVER_KM:g} km: {', '.join(bare[:12])}. config.PLACE_AREA does not cover the "
                     f"whole map (a regional map needs every municipality it draws): widen it, then "
                     f"run: python pipeline/place_index_fetch.py {slug} --force")
    out = write(index, slug)
    cpath = crossings_path(slug)
    print(f"Wrote {out} ({out.stat().st_size:,} bytes, {len(index['rows']):,} places), "
          f"{cpath.relative_to(STATIC_DIR).as_posix()} ({cpath.stat().st_size:,} bytes, "
          f"{report.get('crossing', 0):,} intersections) and {summary_path(slug).name}")
    print(f"  languages: {index['languages']['coverage']} -> the page names {index['languages']['listed']}")
    if report.get("wikidata_cache_absent") and report.get("wikidata_entries_asked"):
        print(f"  NO WIKIDATA CACHE at {wikidata_cache(config)}: {report['wikidata_entries_asked']:,} "
              f"entries went unasked, so public art and libraries were held to the wikipedia tag alone. "
              f"Run: python pipeline/place_wikidata_fetch.py {slug}")
    for k in sorted(report):
        print(f"  {k}: {report[k]:,}")
    return index


def build_city(config):
    """(index, report) for a city's config, exactly as run() builds it, writing
    nothing; it exits naming the fetch script when a cache is missing."""
    import sys
    slug, name = city_of(config)
    if not config.PLACE_OSM_JSON.exists():
        sys.exit(f"Missing {config.PLACE_OSM_JSON}.\nRun: python pipeline/place_index_fetch.py {slug}")
    fold = config.PLACE_FOLD
    if fold not in FOLDS:
        sys.exit(f"config.PLACE_FOLD {fold!r} is not one of {FOLDS}")
    extra = config.PLACE_OSM_EXTRA_JSON
    if not extra.exists():
        sys.exit(f"Missing {extra}.\nRun: python pipeline/place_index_fetch.py {slug}")
    payload = json.loads(config.PLACE_OSM_JSON.read_text(encoding="utf-8"))
    # The extra query's classes (place_index_fetch.EXTRA_QUERY), merged by
    # OSM id: a place node can come in both.
    seen = {(e["type"], e["id"]) for e in payload["elements"]}
    extra_els = json.loads(extra.read_text(encoding="utf-8"))["elements"]
    payload["elements"] += [e for e in extra_els if (e["type"], e["id"]) not in seen]
    # An object in both keeps the extra query's center: Brussels' Grand-Place
    # is a highway area (the first query, nodes and no center) and a
    # place=square (the second, with its center); build() needs both.
    centers = {(e["type"], e["id"]): e["center"] for e in extra_els if "center" in e}
    for e in payload["elements"]:
        if "nodes" in e and "center" not in e and (e["type"], e["id"]) in centers:
            e["center"] = centers[(e["type"], e["id"])]
    # The retrieval date is the caches' own, from their file names (the
    # older of the two): never today.
    retrieved = min(p.stem.rsplit("_", 1)[-1] for p in (config.PLACE_OSM_JSON, extra))
    dropped = getattr(config, "PLACE_DROPPED", {})
    visitable = getattr(config, "PLACE_VISITABLE", {})
    bad = visitable_problems(visitable)
    if bad:
        sys.exit("config.PLACE_VISITABLE: " + "; ".join(bad))
    # Dated by the cache, never today, so a rebuild reproduces: an entry
    # checked more than VISITABLE_MAX_DAYS before the cache was fetched is
    # ignored (its home goes back out). scripts/check_place_search.py G holds
    # the calendar line.
    live = {k for k, v in visitable.items() if _days(v["checked"], retrieved) <= VISITABLE_MAX_DAYS}
    rebuilt = getattr(config, "PLACE_REBUILT", {})
    works = getattr(config, "PLACE_CLOSED_FOR_WORKS", {})
    index, report = build(payload["elements"], city=name, retrieved=retrieved,
                          local=config.PLACE_LANGUAGES, fold=fold, dropped=dropped,
                          visitable=live, rebuilt=rebuilt, closed_for_works=set(works),
                          way_words=tuple(getattr(config, "PLACE_WAY_WORDS", ())),
                          kept=set(getattr(config, "PLACE_KEPT", {})),
                          map_stations=list(map_stations(config) or []),
                          also=tuple(getattr(config, "PLACE_LANGUAGES_ALSO", ())),
                          station_strip=tuple(getattr(config, "PLACE_STATION_STRIP", ())),
                          articles=read_wikidata_articles(wikidata_cache(config)),
                          keep_named_private=bool(getattr(config, "PLACE_KEEP_NAMED_PRIVATE_STREETS", False)),
                          keep_interchanges=bool(getattr(config, "PLACE_KEEP_INTERCHANGES", False)))
    if rebuilt and report.get("street_way_kept_rebuilt", 0) == 0 or any(
            not any((e.get("tags") or {}).get("highway") == "construction"
                    and n in (e.get("tags") or {}).values() for e in payload["elements"])
            for n in rebuilt):
        sys.exit("config.PLACE_REBUILT names a street no highway=construction way in the cache "
                 "carries: remove it (the street has reopened, or the name is wrong)")
    ocache = outline_cache(config)
    if not ocache.exists():
        sys.exit(f"Missing {ocache}.\nRun: python pipeline/place_index_fetch.py {slug}")
    munis = municipalities(json.loads(ocache.read_text(encoding="utf-8"))["elements"])
    if not munis:
        sys.exit(f"{ocache}: no boundary in it; config.PLACE_AREA names none")
    stations = map_stations(config)
    counts = stations_per_municipality(munis, stations) if stations is not None else {}
    # The municipality with the most of the map's stations first, so the map
    # can say "Seattle and 10 more"; by name where stations are not counted.
    munis.sort(key=lambda m: (-counts.get(m[0], 0), m[1]))
    index["area"] = outline(munis, config.CRS_PROJECTED)
    index["street_lines"] = street_lines(index.pop("street_lines_raw"), config.CRS_PROJECTED)
    kept = getattr(config, "PLACE_AREA_KEPT", {})
    stale = sorted(set(kept) - {m[0] for m in munis})
    if stale:
        sys.exit(f"config.PLACE_AREA_KEPT names {stale}, not in config.PLACE_AREA: remove them")
    # Never in the served index: the summary alone carries it.
    index["area_municipalities"] = [
        {"osm": osm_id, "name": name, "stations": counts.get(osm_id),
         **({"kept": kept[osm_id]} if osm_id in kept else {})}
        for osm_id, name, _ in munis]
    found = {f"{e['type']}/{e['id']}" for e in payload["elements"]}
    stale = sorted(set(dropped) - found)
    if stale:
        sys.exit(f"config.PLACE_DROPPED names {stale}, not in the cache: remove them")
    # A kept id the cache does not hold keeps nothing: stop, never pass.
    stale = sorted(set(getattr(config, "PLACE_KEPT", {})) - found)
    if stale:
        sys.exit(f"config.PLACE_KEPT names {stale}, not in the cache: remove them (the object left "
                 f"OpenStreetMap or its id changed), or fetch again")
    # A cache absent from disk is no answer: the rules fall back to the
    # wikipedia tag alone, and run() says so. A cache that is there and lacks
    # an entry the step needs is stale, and stops the step.
    known = read_wikidata_articles(wikidata_cache(config))
    report["wikidata_cache_absent"] = int(known is None)
    report["wikidata_entries_asked"] = len(index.get("wikidata_asked", ()))
    unasked = [] if known is None else sorted(set(index.get("wikidata_asked", ())) - set(known))
    if unasked:
        sys.exit(f"{len(unasked)} Wikidata entr{'y' if len(unasked) == 1 else 'ies'} the index step needs "
                 f"({', '.join(unasked[:5])}{', ...' if len(unasked) > 5 else ''}) "
                 f"{'are' if len(unasked) > 1 else 'is'} not in {wikidata_cache(config)}.\n"
                 f"Run: python pipeline/place_wikidata_fetch.py {slug}")
    stale = sorted(set(getattr(config, "PLACE_KEPT", {})) - found)
    if stale:
        sys.exit(f"config.PLACE_KEPT names {stale}, not in the cache: remove them")
    stale = sorted(set(works) - found)
    if stale:
        sys.exit(f"config.PLACE_CLOSED_FOR_WORKS names {stale}, not in the cache: remove them")
    stale = sorted(set(visitable) - found)
    if stale:
        sys.exit(f"config.PLACE_VISITABLE names {stale}, not in the cache: remove them")
    return index, report


# VISITABLE FORMER HOMES (owner, 2026-10-08: "yes short list, visitable only
# hard line. Must make sure info is up-to-date on visitation eligibility. if
# too much to maintain then can the whole idea"). A city's
# config.PLACE_VISITABLE names, by OSM id, a home the home rule holds out that
# the public can visit today, each with its evidence:
#     "way/515857420": {"name": "旧三井家下鴨別邸", "access": "OPEN_REGULAR",
#                       "source": "https://...", "checked": "2026-10-08",
#                       "why": "one sentence"}
# access is OPEN_REGULAR (a public schedule) or OPEN_SEASONAL (public opening
# periods each year); by appointment, events or heritage days only is not
# visitable. An entry lapses VISITABLE_MAX_DAYS after it was checked:
# check_place_search.py G fails from that day until it is re-checked or
# removed, and the index step ignores it once the cache is newer.
VISITABLE_ACCESS = ("OPEN_REGULAR", "OPEN_SEASONAL")
VISITABLE_MAX_DAYS = 365
VISITABLE_KEYS = {"name", "access", "source", "checked", "why"}


def _days(a, b):
    """Days from date a to date b (ISO strings)."""
    import datetime
    return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days


def visitable_problems(visitable):
    """What is wrong with a config.PLACE_VISITABLE, as messages; [] when sound."""
    import datetime
    out = []
    for k, v in visitable.items():
        if not re.fullmatch(r"(node|way|relation)/[0-9]+", k):
            out.append(f"{k}: not an OSM id")
            continue
        if not isinstance(v, dict) or set(v) != VISITABLE_KEYS:
            out.append(f"{k}: fields must be {sorted(VISITABLE_KEYS)}")
            continue
        if v["access"] not in VISITABLE_ACCESS:
            out.append(f"{k}: access {v['access']!r} is not one of {VISITABLE_ACCESS}")
        if not str(v["source"]).startswith("https://"):
            out.append(f"{k}: source must be an https URL")
        try:
            datetime.date.fromisoformat(v["checked"])
        except (TypeError, ValueError):
            out.append(f"{k}: checked {v['checked']!r} is not a date")
    return out


def index_url(slug):
    """The site path a map fetches its index from, stamped with the file's
    content hash: a browser keeps its copy of a static file, so a rebuilt
    index under the same URL went unseen in the Kyoto pilot (2026-10-07).
    The index step therefore runs before the map step (step2b_place_index.py)."""
    path = index_path(slug)
    if not path.exists():
        raise SystemExit(f"Missing {path}.\nRun: python pipeline/{slug}/step2b_place_index.py")
    return f"/app/static/places/{slug}.json?v={hashlib.sha256(path.read_bytes()).hexdigest()[:12]}"


def index_url_for(config):
    """index_url() for a city whose config declares place search (PLACE_AREA),
    else None. For a map step shared by a country (pipeline/countries/
    france_tram, czechia_osm_tram, uk): 33 cities' own step3 files hold no
    render_heatmap() call to give the argument to, so the shared call asks
    here and a city gains search by its config alone
    (scripts/place_search_scaffold.py reads this function's name in a module
    to know the map step needs no edit)."""
    if getattr(config, "PLACE_AREA", None) is None:
        return None
    return index_url(city_of(config)[0])


KINDS = ("station", "junction", "landmark", "place", "street", "crossing")

# LANGUAGES (owner, 2026-10-07: the page names the languages a city's search
# answers in, from a check, never a fixed "Japanese"). Each city declares its
# local language(s), config.PLACE_LANGUAGES (Brussels: French and Dutch). The
# index reads the main name, English, and each local language's own name,
# romanizations and readings (_name_tags). Each row records which of those
# languages it carries, and the page lists a language only where it covers at
# least LIST_SHARE of the rows: across all of Kyoto's named objects name:en is
# on 64%, name:id 27% (a bulk copy of the romaji) and name:fr 11%, so a
# language a tag merely mentions is no claim. A declared local language under
# LOCAL_MIN means the declaration is wrong, and the step stops.
# scripts/check_place_search.py re-reads the result.
LIST_SHARE = 0.5
LOCAL_MIN = 0.9
LANGUAGE_NAMES = {
    "en": "English", "ja": "Japanese", "ko": "Korean", "zh": "Chinese", "fr": "French",
    "nl": "Dutch", "de": "German", "es": "Spanish", "ca": "Catalan", "eu": "Basque",
    "gl": "Galician", "it": "Italian", "pt": "Portuguese", "cs": "Czech", "lv": "Latvian",
    "ka": "Georgian", "ru": "Russian", "da": "Danish", "sv": "Swedish", "nb": "Norwegian", "ro": "Romanian",
    "hu": "Hungarian", "el": "Greek", "pl": "Polish", "tr": "Turkish", "fi": "Finnish",
}
# Readings a local language's readers type in (kana for Japanese).
READINGS = {"ja": ("name:ja-Hira", "name:ja_kana")}


# LEAK WORDS: strong markers of a business or a home in a place's names.
# scripts/check_place_search.py (E) fails on any index row carrying one unless
# the city's config.PLACE_REVIEWED names it, with the reason it is a place (a
# ruin of a hotel, a museum named after its founding company). A CJK word
# matches anywhere, a Latin one as a whole word; LEAK_ALLOW lists compounds
# that hold a word and are places (商店街, a shopping street). Calibrated on
# Kyoto, 2026-10-07; each new language adds its own words before its first
# city.
LEAK_WORDS = {
    "ja": ("株式会社", "有限会社", "合同会社", "(株)", "（株）", "㈱", "(有)", "（有）", "商店", "本店",
           "支店", "ホテル", "旅館", "マンション", "ハイツ", "レジデンス", "コーポ", "アパート", "メゾン",
           "社宅", "駐車場", "駐輪場", "不動産", "クリニック", "医院", "歯科", "薬局", "私有地"),
    "en": ("inc", "llc", "ltd", "corp", "company", "store", "shop", "restaurant", "cafe", "hotel",
           "hostel", "motel", "salon", "clinic", "pharmacy", "apartment", "apartments", "apts",
           "condominium", "condo", "condos", "parking", "private",
           # Chicago's "Access food court", a service way (batch 2b, 2026-10-08).
           "food court"),
    # Batch 2a (2026-10-08): the handoff's proposals, each language checked
    # against its city's own hits (docs/decisions_drafts/place-search.md).
    "fr": ("sarl", "sas", "eurl", "hôtel", "auberge", "résidence", "appartements", "parking",
           "privé", "privée", "magasin", "boutique", "restaurant", "brasserie", "pharmacie",
           "clinique", "agence",
           # Housing estates: a subdivision, a social-housing group (Marseille).
           "lotissement", "morcellement", "hlm", "h.l.m.",
           # A drive-through, in French usage (Marseille's "Mc Drive", a
           # service way; batch 2b, 2026-10-08).
           "mc drive", "mcdrive"),
    "ca": ("hotel", "hostal", "aparcament", "pàrquing", "privat", "privada", "botiga", "restaurant",
           "pisos", "farmàcia", "s.l.", "s.a."),
    # NOT "privada" (batch 3, 2026-10-11): in Mexico a Privada is a street
    # type ("1a Privada Tula", "Privada de Matamoros"), a public address;
    # as a leak word it dropped 4,393 of Mexico City's streets. Barcelona,
    # which also reads these words, has no street they decide.
    "es": ("hotel", "hostal", "aparcamiento", "parking", "privado", "propiedad privada", "tienda",
           "restaurante", "pisos", "farmacia", "s.l.", "s.a.", "estacionamiento", "s.a. de c.v.",
           "condominio", "condominios", "departamentos", "motel"),
    # Batch 3 (2026-10-11): Portuguese (Sao Paulo), checked against its own
    # hits. "particular" is Brazil's word for a private lane (Rua Particular).
    "pt": ("hotel", "pousada", "motel", "estacionamento", "particular", "privado", "privada", "loja",
           "restaurante", "farmácia", "condomínio", "residencial", "apartamentos", "ltda", "s.a.",
           "supermercado", "shopping"),
    "cs": ("hotel", "penzion", "parkoviště", "soukromé", "soukromá", "obchod", "restaurace",
           "bytový dům", "bytové domy", "lékárna", "s.r.o.", "a.s.", "rezidence"),
    "nl": ("hotel", "parking", "privé", "winkel", "restaurant", "appartementen", "residentie",
           "apotheek", "bvba", "nv"),
    # German (owner, 2026-10-13; docs/decisions_drafts/search-lang-de.md, measured
    # on Gelsenkirchen, Bremen, Berlin and Zurich). NOT "ag" and "kg": "ag" as
    # a whole word dropped Bremen's AG-Weser-Straße. Not leak words, measured:
    # siedlung (145 Berlin neighborhoods), betriebshof (tram stops), residenz,
    # werkstatt, "e.V.".
    "de": ("hotel", "gasthof", "gasthaus", "pension", "parkplatz", "parkhaus", "tiefgarage", "privat",
           "privatweg", "privatstraße", "privatgrundstück", "laden", "geschäft", "restaurant",
           "gaststätte", "wohnanlage", "wohnpark", "wohnhaus", "mehrfamilienhaus", "apotheke", "gmbh",
           "ohg", "supermarkt", "einkaufszentrum", "zufahrt", "seniorenresidenz", "autohaus",
           "tankstelle"),
    # Danish (owner, 2026-10-13; search-final's search-lang-da.md, with its id catches and future edit points).
    "da": ("hotel", "hotellet", "vandrerhjem", "parkeringsplads", "p-plads", "parkeringshus", "p-hus",
           "privat", "privatvej", "privat vej", "butik", "restaurant", "apotek", "aps", "a/s",
           "supermarked", "indkøbscenter", "tankstation", "varelevering", "indkørsel", "udkørsel",
           "boligforening", "andelsboligforening", "ejerforening", "plejehjem", "drive-in"),
    # Norwegian (owner, 2026-10-13; search-final's search-lang-nb.md, with its id catches and future edit points).
    "nb": ("hotell", "hotel", "pensjonat", "vandrerhjem", "parkering", "parkeringsplass",
           "parkeringshus", "parkeringsanlegg", "parkeringskjeller", "p-hus", "p-plass",
           "beboerparkering", "gjesteparkering", "garasje", "garasjer", "garasjeanlegg", "garasjeport",
           "privat", "privat vei", "privat veg", "privatvei", "innkjørsel", "innkjøring", "utkjørsel",
           "utkjøring", "avkjørsel", "oppkjørsel", "adkomst", "atkomst", "varelevering", "varemottak",
           "butikk", "restaurant", "kafé", "kafe", "apotek", "as", "a/s", "asa", "borettslag", "brl",
           "sameie", "sameiet", "boligsameie", "kjøpesenter", "legesenter", "tannlege", "leiligheter",
           "boliger", "studentboliger", "omsorgsboliger", "snuplass", "busslomme"),
    # Swedish (owner, 2026-10-13; search-final's search-lang-sv.md, with its id catches and future edit points).
    "sv": ("hotell", "vandrarhem", "pensionat", "värdshus", "parkering", "parkeringsplats",
           "parkeringshus", "parkeringsgarage", "kundparkering", "besöksparkering", "personalparkering",
           "p-hus", "garage", "privat", "privatväg", "butik", "affär", "restaurang", "apotek", "ab",
           "aktiebolag", "handelsbolag", "brf", "bostadsrättsförening", "bostadsrättsföreningen",
           "bostadshus", "flerfamiljshus", "lägenheter", "radhus", "studentbostäder", "äldreboende",
           "vårdboende", "seniorboende", "samfällighet", "köpcentrum", "galleria", "gallerian",
           "stormarknad", "bensinstation", "infart", "utfart", "inlastning", "varumottagning",
           "godsmottagning", "serviceväg", "drive-in"),
    # Latvian (owner, 2026-10-13; search-final's search-lang-lv.md, with its id catches and future edit points).
    "lv": ("viesnīca", "hotelis", "hostelis", "motelis", "viesu nams", "viesu māja", "stāvvieta",
           "autostāvvieta", "stāvlaukums", "privāts", "privāta", "privātais", "privātā",
           "privātīpašums", "privātmāja", "privātmājas", "veikals", "lielveikals", "restorāns",
           "kafejnīca", "aptieka", "sia", "a/s", "dzīvokļi", "daudzdzīvokļu", "dzīvojamā māja",
           "tirdzniecības centrs", "iebrauktuve", "piebraucamais", "klīnika", "autoserviss", "garāžas",
           "kooperatīvs", "pansija", "pansionāts", "degvielas uzpildes stacija"),
    # Romanian (owner, 2026-10-13; search-final's search-lang-ro.md, with its id catches and future edit points).
    "ro": ("hotel", "hotelul", "hostel", "motel", "pensiune", "pensiunea", "parcare", "parcarea",
           "privat", "privată", "magazin", "restaurant", "restaurantul", "farmacia", "srl", "s.r.l.",
           "s.a.", "supermarket", "hipermarket", "benzinărie", "benzinăria", "rezidențial",
           "rezidenţial", "residence", "apartamente", "blocuri", "acces", "intrare"),
    # Italian (owner, 2026-10-13; search-final's search-lang-it.md, with its id catches and future edit points).
    "it": ("albergo", "ostello", "agriturismo", "affittacamere", "b&b", "parcheggio", "parcheggi",
           "garage", "autorimessa", "proprietà privata", "strada privata", "negozio", "ristorante",
           "trattoria", "pizzeria", "farmacia", "supermercato", "ipermercato", "centro commerciale",
           "condominio", "residence", "appartamenti", "srl", "s.r.l.", "s.p.a.", "snc", "s.n.c.",
           "s.a.s.", "ingresso", "accesso", "autolavaggio", "distributore"),
    # Greek (owner, 2026-10-13; search-final's search-lang-el.md, with its id catches and future edit points).
    "el": ("ξενοδοχείο", "ξενώνας", "πάρκινγκ", "στάθμευση", "στάθμευσης", "γκαράζ", "ιδιωτικός",
           "ιδιωτική", "ιδιωτικό", "φαρμακείο", "εστιατόριο", "ταβέρνα", "κατάστημα", "σούπερ μάρκετ",
           "εμπορικό κέντρο", "πρατήριο", "βενζινάδικο", "πολυκατοικία", "διαμερίσματα", "α.ε.",
           "ε.π.ε.", "ο.ε.", "ι.κ.ε.", "επε", "ικε"),
    # Batch 2b (2026-10-08): Chinese (Hong Kong), Korean (Seoul, Busan) and
    # Georgian (Tbilisi), each checked against its city's own hits. A CJK or
    # Hangul word matches anywhere; a Georgian one as a whole word.
    "zh": ("有限公司", "公司", "集團", "酒店", "賓館", "旅館", "餐廳", "酒樓", "商場", "商店",
           "超級市場", "停車場", "診所", "醫務所", "藥房", "寫字樓", "私人", "私家", "屋苑", "住宅"),
    "ko": ("주식회사", "(주)", "㈜", "호텔", "모텔", "주차장", "마트", "상가", "아파트", "빌라", "맨션",
           "연립", "주택", "오피스텔", "사유지"),
    "ka": ("შპს", "სს", "სასტუმრო", "მაღაზია", "ავტოსადგომი", "რესტორანი", "აფთიაქი", "კლინიკა",
           "კერძო", "ბინა", "საცხოვრებელი"),
}
LEAK_ALLOW = {"ja": ("商店街", "名店街"), "en": ("shopping street",),
              # A town hall and a hospital (Paris's Hôtel-Dieu, Marseille's).
              "fr": ("hôtel de ville", "hôtel-de-ville", "hôtel-dieu", "hôtel des invalides"),
              # "스마트" (smart) holds 마트 (mart); 주택가 is a residential
              # street, a place word (batch 2b, 2026-10-08).
              "ko": ("스마트",)}
# The LEAK_WORDS that mark a home (or private land): a landmark carrying one
# is held to _public_home, where a Wikipedia article is no exemption.
HOME_WORDS = {
    "ja": ("マンション", "ハイツ", "レジデンス", "コーポ", "アパート", "メゾン", "社宅", "私有地"),
    "en": ("apartment", "apartments", "apts", "condominium", "condo", "condos", "private"),
    "fr": ("résidence", "appartements", "privé", "privée", "lotissement", "morcellement", "hlm",
           "h.l.m."),
    "ca": ("pisos", "privat", "privada"),
    "es": ("pisos", "privado", "propiedad privada", "condominio", "condominios", "departamentos"),
    "pt": ("particular", "privado", "privada", "condomínio", "residencial", "apartamentos"),
    "cs": ("bytový dům", "bytové domy", "soukromé", "soukromá", "rezidence"),
    "nl": ("appartementen", "residentie", "privé"),
    "de": ("wohnanlage", "wohnpark", "wohnhaus", "mehrfamilienhaus", "privat", "privatweg",
           "privatstraße", "privatgrundstück", "seniorenresidenz"),
    "da": ("privat", "privatvej", "privat vej", "boligforening", "andelsboligforening", "ejerforening",
           "plejehjem"),
    "nb": ("privat", "privat vei", "privat veg", "privatvei", "borettslag", "brl", "sameie", "sameiet",
           "boligsameie", "leiligheter", "boliger", "studentboliger", "omsorgsboliger",
           "beboerparkering"),
    "sv": ("privat", "privatväg", "brf", "bostadsrättsförening", "bostadsrättsföreningen", "bostadshus",
           "flerfamiljshus", "lägenheter", "radhus", "studentbostäder", "äldreboende", "vårdboende",
           "seniorboende", "samfällighet"),
    "lv": ("privāts", "privāta", "privātais", "privātā", "privātīpašums", "privātmāja", "privātmājas",
           "dzīvokļi", "daudzdzīvokļu", "dzīvojamā māja", "pansionāts"),
    "ro": ("privat", "privată", "rezidențial", "rezidenţial", "residence", "apartamente", "blocuri"),
    "it": ("proprietà privata", "strada privata", "condominio", "residence", "appartamenti"),
    "el": ("πολυκατοικία", "διαμερίσματα", "ιδιωτικός", "ιδιωτική", "ιδιωτικό"),
    "zh": ("私人", "私家", "屋苑", "住宅"),
    "ko": ("아파트", "빌라", "맨션", "연립", "주택", "오피스텔", "사유지"),
    "ka": ("კერძო", "ბინა", "საცხოვრებელი"),
}


def _has_word(word, low):
    """True when `word` occurs in the lowercased text `low`: a CJK word
    anywhere (四条 in 四条烏丸), any other as a whole word or phrase, accents
    included ("hôtel", "bytový dům", "s.r.o."). Until batch 2a (2026-10-08)
    Latin words were whole [a-z] runs, which split "hôtel" at its accent; the
    five built indexes rebuilt byte-identical under this rule."""
    if _CJK_WORD.search(word):
        return word in low
    return re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", low) is not None


# A LEAK WORD OF ONE LANGUAGE IS A PLAIN WORD OF ANOTHER (candidate 29,
# owner 2026-10-13): English "store" is "big" in Danish, Norwegian and
# Swedish ("Store Kongensgade"). The English word is not read in a city that
# declares one of them; every word set aside is listed here.
LEAK_SET_ASIDE = {"da": ("store",), "nb": ("store",), "sv": ("store",)}


# WHERE THE LEAK-WORD TEST NO LONGER FIRES (a fault mended, the sixth pass,
# 2026-10-13). Check E of scripts/check_place_search.py fired 334 times on the
# 151 extract-run cities and 325 were false alarms, settled by hand
# (data/_search_rollout/extract_rules34/leak_streets.tsv):
#   * a signed junction named for the building beside it (130 rows, Korean 99
#     and Japanese 31): a junction row is never dropped for a leak word by
#     build(), so leak_hits() no longer lists one;
#   * a French listed mansion or institution, a "hôtel" in the French sense
#     (about 135): on a LANDMARK, in a French-language city, a name that
#     starts "Hôtel de", "Hôtel du", "Hôtel des", "Hôtel d'" or "Hôtel-" and a
#     word is read without its first word (FRENCH_MANSION). A hotel business
#     so named is still held out by its lodging tag (_commercial). "Hôtel"
#     and a family name alone ("Hôtel Gradis") is NOT read: nothing tells it
#     from a hotel's trade name, and it stays a review in PLACE_REVIEWED.
#     "Hôtel particulier" and "Ancien hôtel" as whole names are bare type
#     words (BARE_TYPE_NAMES_6);
#   * "brasserie" in a French street's name (10: "Rue de la Brasserie"), which
#     _named_street keeps already: leak_hits() no longer lists a street row
#     for a word in LEAK_STREET_ALLOW.
# Measured on the 19 live cities, 2026-10-13: 3 landmark rows return (Brussels'
# Hôtel des Douanes, Paris's Hôtel de Poulpry and Hôtel du Petit Monaco), none
# leaves, and 58 of the 133 reviews in their config.PLACE_REVIEWED are no
# longer needed (38 junctions, Seoul 36; 20 mansions, Paris 18). Check E tells
# such a review from a stale one with leak_hits(exempt=False).
FRENCH_MANSION = {"fr": re.compile(r"^h[oô]tel(?=\s+(?:de|du|des)\s|\s+d['’]|-\w)")}
LEAK_STREET_ALLOW = {"fr": ("brasserie",)}


def leak_word(names, local, landmark=False):
    """The first LEAK_WORD of English or a local language in `names`, after
    LEAK_ALLOW compounds are removed; None when there is none. `landmark`:
    the names are a landmark's, read with FRENCH_MANSION."""
    if landmark:
        read = []
        for n in names:
            n = n.lower().strip()
            for c in local:
                if c in FRENCH_MANSION:
                    n = FRENCH_MANSION[c].sub(" ", n)
            read.append(n)
        names = read
    low = " | ".join(names).lower()
    for code in dict.fromkeys(["en", *local]):
        for allow in LEAK_ALLOW.get(code, ()):
            low = low.replace(allow, " ")
        for word in LEAK_WORDS.get(code, ()):
            if code not in local and any(word in LEAK_SET_ASIDE.get(c, ()) for c in local):
                continue
            if _has_word(word, low):
                return word
    return None


def leak_hits(index, local, exempt=True):
    """[(row name, word)] for every index row whose names carry a LEAK_WORD.
    `exempt` (the default) leaves out what the test no longer fires on: a
    junction row, a French mansion's name on a landmark, a street row under a
    LEAK_STREET_ALLOW word. exempt=False is the test as it was, which check E
    uses to tell a review that is no longer needed from one that is stale."""
    kinds = index.get("kinds") or KINDS
    street_ok = {w for c in local for w in LEAK_STREET_ALLOW.get(c, ())}
    out = []
    for r in index["rows"]:
        kind = kinds[r[0]] if exempt else None
        if kind == "junction":
            continue
        word = leak_word([r[3]] + (r[4].split("|") if r[4] else []), local, landmark=kind == "landmark")
        if word and not (kind == "street" and word in street_ok):
            out.append((r[3], word))
    return sorted(set(out))


def _char_class(*pairs):
    return re.compile("[" + "".join(chr(a) + "-" + chr(b) for a, b in pairs) + "]")


# A local language with its own script must show it in `name`; one written in
# Latin letters is taken as declared (its words cannot be told apart by script).
SCRIPTS = {
    "ja": _char_class((0x3040, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF)),
    "zh": _char_class((0x3400, 0x4DBF), (0x4E00, 0x9FFF)),
    "ko": _char_class((0xAC00, 0xD7AF), (0x1100, 0x11FF)),
    "ka": _char_class((0x10A0, 0x10FF)),
    "el": _char_class((0x0370, 0x03FF)),
}
# Words matched anywhere rather than whole (_has_word): kana, Han, Hangul.
_CJK_WORD = _char_class((0x3040, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF),
                        (0xAC00, 0xD7AF), (0xFF08, 0xFF09), (0x3231, 0x3231))


def _name_tags(local):
    """The name tags read, in order: the first is the display name, the rest
    searchable aliases. For Kyoto (local ja) this is the pilot's first list."""
    tags = ["name", "name:en"]
    for code in local:
        tags += [f"name:{code}", f"name:{code}-Latn", f"name:{code}_rm", *READINGS.get(code, ())]
    # int_name since the fourth pass (2026-10-13): Thessaloniki writes its
    # Latin-letter names there on 44% of rows.
    tags += ["alt_name", "alt_name:en", "int_name", "official_name", "official_name:en",
             "short_name", "short_name:en", "old_name:en"]
    return tuple(dict.fromkeys(tags))


def _langs(tags, local):
    """The languages, of English and the local ones, that one object's names are in."""
    out = set()
    name = tags.get("name") or ""
    # The main name counts for the FIRST declared language written in Latin
    # letters only: a second one (Barcelona's Spanish beside Catalan,
    # Brussels' Dutch beside French) is measured by its own name:<code> tag,
    # never credited from a name in another language (batch 2a, 2026-10-08).
    first_latin = next((c for c in local if c not in SCRIPTS), None)
    for code in local:
        script = SCRIPTS.get(code)
        if tags.get(f"name:{code}") or (name and (script.search(name) if script else code == first_latin)):
            out.add(code)
    if any(tags.get(k) for k in ("name:en", "alt_name:en", "official_name:en", "short_name:en")):
        out.add("en")
    return out


def languages(row_langs, local, also=()):
    """Coverage of English and each local language over the index's rows, and
    the languages the page may name, English first, then the local ones.
    `also`: languages declared below the floor (config.PLACE_LANGUAGES_ALSO;
    owner, 2026-10-13: "declare"): a city's second language whose names are
    on a share of its rows (Cluj-Napoca's Hungarian 39.8%, Daugavpils'
    Russian 15.5%). The floor, LOCAL_MIN (90%), is asked of PLACE_LANGUAGES
    only; a language declared here has its name:<code> tags read as aliases
    and its coverage measured, is never credited from the main name, and is
    named on the page at LIST_SHARE (50%) like any other."""
    order = list(dict.fromkeys(["en", *local, *also]))
    n = max(len(row_langs), 1)
    coverage = {c: round(sum(c in s for s in row_langs) / n, 3) for c in order}
    short = [c for c in local if coverage[c] < LOCAL_MIN]
    if short:
        raise SystemExit(f"declared local language(s) {short} cover under {LOCAL_MIN:.0%} of the "
                         f"places ({coverage}): check config.PLACE_LANGUAGES")
    unnamed = [c for c in order if c not in LANGUAGE_NAMES]
    if unnamed:
        raise SystemExit(f"no display name for language code(s) {unnamed}: add to LANGUAGE_NAMES")
    listed = [LANGUAGE_NAMES[c] for c in order if coverage[c] >= LIST_SHARE]
    return {"local": list(local), "coverage": coverage, "list_share": LIST_SHARE, "listed": listed,
            **({"also": list(also)} if also else {})}

# Highways that are not streets a reader would search for: platforms, indoor
# corridors, parking aisles, driveways, service areas and the like.
SKIP_HIGHWAY = {"platform", "elevator", "corridor", "bus_stop", "proposed", "construction",
                "razed", "abandoned", "disused", "services", "rest_area"}
SKIP_SERVICE = {"parking_aisle", "driveway", "drive-through", "emergency_access"}
# MINOR WAYS are named after the business they serve as often as after a
# place: Kyoto's footways and cycleways included "ライフ" (a supermarket chain),
# its bicycle parking and car park, a hotel's footpath and a mall's exit
# (2026-10-07). A minor way is kept only when its name reads as a way in one
# of the city's languages (WAY_WORDS) or it is notable; every class from
# residential up is a public street and kept as named. A language with no
# WAY_WORDS entry keeps no minor way until one is added.
MINOR_HIGHWAYS = {"footway", "path", "steps", "cycleway", "track", "bridleway", "service"}
WAY_WORDS = {
    "ja": ("通", "道", "路", "坂", "橋", "小路", "小径", "参道", "筋", "街道", "線", "並木", "広場",
           "ロード", "ストリート", "トンネル", "はし", "ばし", "みち", "さか", "ざか", "径"),
    "en": ("street", "road", "avenue", "lane", "way", "walk", "path", "trail", "alley", "bridge",
           "steps", "stairs", "boulevard", "promenade", "passage", "plaza", "row", "greenway",
           "tunnel", "footpath", "towpath"),
    # NOT here (batch 2b audit, 2026-10-08): drive, court, crescent, close,
    # mews and the like. Added for Hong Kong's terraces, they admitted 155
    # named minor ways in Seattle and 199 in Vancouver, about 40% of them
    # access=private driveways of housing complexes ("Chinook Court",
    # "Marlin Quay"), and Sydney's shopping arcades. Hong Kong's terraces are
    # found by their Chinese names (臺, 台).
    # Batch 2a (2026-10-08), checked against each city's named minor ways.
    "fr": ("rue", "avenue", "boulevard", "place", "quai", "allée", "chemin", "impasse", "passage",
           "pont", "passerelle", "cours", "montée", "escalier", "escaliers", "promenade", "square",
           "sentier", "voie", "piste", "traverse", "ruelle", "esplanade", "parvis", "galerie",
           # Québec street types (Montréal's named footways, 2026-10-08).
           "terrasse", "croissant", "carré", "côte", "carrefour", "cour", "route", "circuit",
           # Marseille's (2026-10-08): roundabouts, breakwaters, corniches, valleys.
           "rond-point", "digue", "corniche", "vallon"),
    "ca": ("carrer", "avinguda", "passeig", "plaça", "rambla", "travessera", "via", "camí",
           "passatge", "pont", "ronda", "baixada", "pujada", "costa", "escales", "placeta",
           "jardins", "corriol", "sender",
           # Barcelona's named footways (2026-10-08): roads, squares, quays, stream-beds
           # turned streets, viaducts and shortcuts.
           "carretera", "pla", "moll", "riera", "torrent", "rotonda", "viaducte", "drecera",
           "passadís", "carreró", "travessia", "pas", "túnel", "davallada", "passarel·la",
           "pasarel·la"),
    "es": ("calle", "avenida", "paseo", "plaza", "camino", "pasaje", "puente", "ronda", "vía",
           "escaleras", "sendero",
           # Mexico City's street types (batch 3, 2026-10-11, from its named
           # minor ways): pedestrian lanes of housing units (andador), dead
           # ends (cerrada, privada, callejón, retorno), causeways and axes.
           "andador", "cerrada", "privada", "callejón", "retorno", "calzada", "eje", "circuito",
           "prolongación", "boulevard", "viaducto", "periférico", "carretera", "brecha", "vereda",
           "escalinata", "rinconada", "ciclovía", "ciclopista", "túnel", "glorieta", "malecón"),
    # Batch 3 (2026-10-11): Portuguese, from Sao Paulo's named minor ways.
    "pt": ("rua", "avenida", "alameda", "travessa", "praça", "largo", "viela", "estrada", "rodovia",
           "ponte", "viaduto", "passarela", "escadaria", "beco", "caminho", "trilha", "passagem",
           "ladeira", "túnel", "ciclovia", "calçadão", "marginal", "via", "elevado", "passeio",
           "escadão", "escada", "ciclopassarela"),
    "cs": ("ulice", "třída", "náměstí", "nábřeží", "most", "lávka", "cesta", "stezka", "schody",
           "schodiště", "alej", "sady", "pěšina", "průchod", "pasáž", "nároží", "stoupání",
           "náplavka"),
    "nl": ("straat", "laan", "weg", "plein", "steenweg", "kaai", "lei", "dreef", "brug", "pad",
           "gang", "steeg", "dijk", "doorgang", "trap", "wandeling", "promenade", "galerij"),
    # German (owner, 2026-10-13; search-lang-de.md), a word's ending
    # (SUFFIX_WAY_LANGUAGES): "Hauptstraße", "Kirchweg". Field-name endings in
    # by the owner's word: -kamp, -winkel, -acker, -hof and -höfe (out:
    # -garten, -wiese, -heide). Swiss German for Zurich: -wegli, -rain, -halde,
    # -quai, -viadukt. Low German: -deich, -pad, -pforte (out: -gang, 13 of
    # Berlin's 19 no street name, and -moor). -eck in after the Berlin
    # measurement.
    # THE ID CATCHES (owner): -hof also ends a shopping passage, a schoolyard
    # and a works yard (Bremen's "Lloydhof" and "Alter Schulhof", Berlin's
    # "Zuwegung Wirtschaftshof", dropped by id), and -eck a corner cafe or a
    # building. When a German city's cache is refreshed, list its minor-way
    # street rows ending -hof or -eck that are new since the last read. The
    # misfires per word are in search-lang-de.md (tunnel 8 of 11 in Berlin,
    # passage 5 of 11): the rows go by id, the words stay.
    "de": ("straße", "strasse", "str", "weg", "gasse", "allee", "platz", "ring", "damm", "ufer", "brücke",
           "steg", "pfad", "stieg", "steig", "treppe", "promenade", "chaussee", "markt", "wall", "graben",
           "passage", "tunnel", "unterführung", "durchgang", "trasse", "kamp", "winkel", "acker", "hof",
           "höfe", "wegli", "rain", "halde", "quai", "viadukt", "deich", "pad", "pforte", "eck"),
    # Danish (owner, 2026-10-13; search-final's search-lang-da.md, with its id catches and future edit points).
    "da": ("gade", "gaden", "vej", "vejen", "allé", "alle", "alléen", "alleen", "stræde", "strædet",
           "plads", "pladsen", "torv", "torvet", "sti", "stien", "bro", "broen", "boulevard", "passage",
           "passagen", "kaj", "kajen", "gyde", "gyden", "trappe", "trappen", "tunnel", "tunnelen",
           "promenade", "promenaden", "vold", "volden", "dæmning", "dæmningen", "viadukt", "viadukten",
           "smøge", "smøgen", "strøg", "strøget", "brygge", "bryggen", "vænget", "skellet", "vangen",
           "krogen", "toften", "højen", "svinget", "kæret", "lodden", "dyssen"),
    # Norwegian (owner, 2026-10-13; search-final's search-lang-nb.md, with its id catches and future edit points).
    "nb": ("vei", "veien", "veg", "vegen", "gate", "gata", "gaten", "allé", "alléen", "strede",
           "stredet", "veita", "veiten", "ringen", "faret", "stubben", "plass", "plassen", "torg",
           "torget", "torv", "torvet", "allmenning", "allmenningen", "almenning", "almenningen", "kai",
           "kaia", "kaien", "brygge", "brygga", "bryggen", "terrasse", "terrassen", "sti", "stien",
           "stigen", "smau", "smauet", "smug", "smuget", "gangen", "tråkk", "tråkket", "løype", "løypa",
           "løypen", "passasje", "passasjen", "promenade", "promenaden", "bakke", "bakken", "bakkene",
           "bakkane", "kleiv", "kleiva", "kleiven", "kleivene", "sving", "svingen", "svingene",
           "svingane", "krok", "kroken", "bru", "brua", "bro", "broen", "trapp", "trappa", "trappen",
           "trappene", "tunnel", "tunnelen", "tunellen", "viadukt", "undergang", "undergangen", "lia",
           "lien", "toppen", "grenda", "grenden", "tunet", "jordet", "kollen", "berget", "haugen",
           "gården"),
    # Swedish (owner, 2026-10-13; search-final's search-lang-sv.md, with its id catches and future edit points).
    "sv": ("gata", "gatan", "väg", "vägen", "gränd", "gränden", "stig", "stigen", "backe", "backen",
           "torg", "torget", "plan", "plats", "platsen", "allé", "allén", "gång", "gången", "bro",
           "bron", "spång", "spången", "trappa", "trappan", "trappor", "trapporna", "trapp", "brink",
           "brinken", "krok", "kroken", "krokarna", "slinga", "slingan", "kaj", "kajen", "led", "leden",
           "lid", "liden", "stråk", "stråket", "strand", "stranden", "promenad", "promenaden",
           "esplanad", "esplanaden", "tunnel", "tunneln", "viadukt", "viadukten", "passage", "passagen",
           "terrass", "terrassen", "svängen", "ringen", "länken", "rundan", "faret", "gård", "gården",
           "gårdar", "gårdarna", "lycka", "lyckan", "lyckor", "lyckorna"),
    # Latvian (owner, 2026-10-13; search-final's search-lang-lv.md, with its id catches and future edit points).
    "lv": ("iela", "šķērsiela", "jauniela", "augšiela", "līnija", "šķērslīnija", "gatve", "prospekts",
           "bulvāris", "šoseja", "ceļš", "aleja", "laukums", "skvērs", "aplis", "gāte", "sēta", "tilts",
           "tunelis", "dambis", "aizsargdambis", "krastmala", "ostmala", "mols", "promenāde", "pasāža",
           "taka", "laipa", "veloceliņš"),
    # Romanian (owner, 2026-10-13; search-final's search-lang-ro.md, with its id catches and future edit points).
    "ro": ("strada", "aleea", "intrarea", "drumul", "bulevardul", "șoseaua", "şoseaua", "calea",
           "piața", "piaţa", "piațeta", "piaţeta", "splaiul", "prelungirea", "fundătura", "cheiul",
           "rondul", "podul", "pasajul", "pasarela", "promenada", "scările"),
    # Italian (owner, 2026-10-13; search-final's search-lang-it.md, with its id catches and future edit points).
    "it": ("via", "viale", "vialetto", "vicolo", "vico", "viuzzo", "viuccia", "largo", "piazza",
           "piazzale", "piazzetta", "piazzaletto", "corso", "strada", "stradone", "lungotevere",
           "lungarno", "lungomare", "lungolago", "lungomura", "ponte", "ponticello", "passerella",
           "salita", "discesa", "rampa", "rampe", "scalea", "scalinata", "scala", "gradinata",
           "cordonata", "clivo", "clivio", "erta", "borgo", "borghetto", "chiasso", "sdrucciolo",
           "sentiero", "ciclabile", "ciclovia", "ciclopedonale", "superciclabile", "passeggiata",
           "passaggio", "passetto", "sottopasso", "sottopassaggio", "sottovia", "galleria pedonale",
           "traforo", "viadotto", "cavalcavia", "circonvallazione", "rotatoria", "svincolo", "raccordo",
           "complanare", "traversa", "argine", "arco", "belvedere"),
    # Greek (owner, 2026-10-13; search-final's search-lang-el.md, with its id catches and future edit points).
    "el": ("οδός", "λεωφόρος", "πλατεία", "πάροδος", "στοά", "μονοπάτι", "γέφυρα", "σκάλες",
           "πεζόδρομος"),
    # Batch 2b (2026-10-08), checked against each city's named minor ways.
    # Hong Kong writes a street's type last, in one word (彌敦道, 西洋菜南街,
    # 摩羅上街), and a lane, court or terrace as 巷, 里, 坊, 台 or 圍.
    "zh": ("街", "道", "路", "巷", "里", "徑", "橋", "隧道", "坊", "圍", "台", "臺", "天橋", "梯", "階",
           "步道", "行人路", "通道", "斜路", "大道", "公路", "繞道", "小路", "古道", "棧道",
           # Hong Kong's pedestrian squares, roundabouts, interchanges and
           # prayas, drawn as footways (2026-10-08).
           "廣場", "迴旋處", "交匯處", "海旁"),
    # Korean street names end in 로 (a road), 길 (a street), 대로 (a
    # boulevard) or 교 / 대교 (a bridge), with no space: matched as a word's
    # ending (SUFFIX_WAY_LANGUAGES). 산책로 and 둘레길 are walking trails.
    "ko": ("로", "길", "대로", "대교", "교", "다리", "거리", "터널", "고가", "지하도", "육교", "굴다리",
           "산책로", "둘레길", "보도", "고개",
           # Seoul's and Busan's named steps (88계단), underpasses and
           # flyovers, and a transliterated "road" (문텐로드), 2026-10-08.
           "계단", "지하차도", "고가차도", "로드"),
    # Georgian: street, avenue, square, lane, alley, bridge, highway, ascent,
    # descent, road, path, embankment; the word stands alone, after the name
    # in the genitive (რუსთაველის გამზირი).
    "ka": ("ქუჩა", "გამზირი", "მოედანი", "ჩიხი", "შესახვევი", "ხიდი", "გზატკეცილი", "აღმართი",
           "დაღმართი", "გზა", "ბილიკი", "სანაპირო", "გასასვლელი", "ქ.",
           # Stairs (Tbilisi's named minor ways, 2026-10-08).
           "კიბე", "კიბეები"),
}
# ONE CITY'S OWN WAY WORDS (owner, 2026-10-13: "sounds good for melbourne"):
# config.PLACE_WAY_WORDS lists extra words for that city's minor-way test
# only, each a whole word as an English one is. Melbourne's public lanes are
# service ways named "X Place", "Court", "Mews", "Terrace" and "Arcade",
# words WAY_WORDS leaves out on the batch 2b audit (about 180 of the 331
# names its index leaves out; wave 1's measure). The other rules still apply
# to a way the words admit: a private one goes, a name with a business word
# goes. No city sets it yet.
#
# PRIVATE STREETS NAMED AS STREETS (owner, 2026-10-11): the private-minor-way
# rule took 351 street rows in Paris, among them the Villas, Cités, Hameaux,
# private Squares and Impasses, which are addressed residential streets
# behind a gate. A private minor way whose name LEADS with one of these words
# is kept, and reads as a way (villa, cité and hameau are not in WAY_WORDS,
# where they would also admit a housing estate's footpaths by name). French
# only so far: measure a word on every built city of its language before
# adding it, and never a word for an access or service road.
PRIVATE_STREET_LEAD = {"fr": ("villa", "cité", "square", "impasse", "hameau")}


def _private_street(names, local):
    for code in local:
        lead = PRIVATE_STREET_LEAD.get(code, ())
        for n in names:
            ws = re.findall(r"\w+", n.lower())
            if ws and ws[0] in lead:
                return True
    return False


# Languages that write a way word inside a compound ("Nieuwstraat",
# "Kerkpad"; Korean 세종대로): _reads_as_way matches it as a word's ending there.
SUFFIX_WAY_LANGUAGES = {"nl", "ko", "de", "da", "nb", "sv"}
GLUED_STREET_LANGUAGES = SUFFIX_WAY_LANGUAGES - {"ko"}
# Street names that carry no street word at all. Czech names a street with a
# preposition ("Na Viničce", "U Vizerky", "Pod Havránkou") or an adjective
# agreeing with the unwritten "ulice" ("Bělohorská", "Goyova"): Prague's
# named footways and tracks lost 2,345 ways to the way-word test alone
# (batch 2a, 2026-10-08). WAY_LEAD is the name's first word, WAY_ENDING the
# ending of its last.
WAY_LEAD = {"cs": ("na", "u", "k", "ke", "pod", "nad", "za", "do", "ve", "v", "při", "před",
                   "mezi", "po", "proti", "přes", "od", "ze", "z"),
            # German names a lane by a preposition too ("Am Wall", "Zum
            # Hafen"): the loosest group, about 15 misfires in Berlin ("Am
            # Reitstall") against about 80 real names (search-lang-de.md).
            "de": ("am", "an", "auf", "im", "in", "zum", "zur", "hinter", "unter", "vor", "bei", "beim"),
            "da": ("ved",)}
# A trailing Roman numeral ("Herálecká II", "Podnikatelská Ⅰ") is set aside first.
WAY_ENDING = {"cs": ("á", "ní", "ova", "ého"),
              # Greek names a street in the genitive with no street word
              # (search-lang-el.md): the ending of the name's last word,
              # accented and plain forms both, since the test folds no accent.
              "el": ("ου", "ού", "ας", "άς", "ης", "ής", "ος", "ων", "ών", "ους", "ως", "η", "ή", "α",
                     "ά")}
ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}
# Any landmark with one of these is (also) a business, and stays out.
COMMERCIAL_KEYS = ("shop", "office", "craft", "brand", "cuisine")
# operator:type by value: Nishiki Market is run by its shopkeepers' cooperative
# (operator:type=cooperative) and is a place; a private operator is a business.
COMMERCIAL_VALUES = {
    "operator:type": {"private", "business", "commercial"},
    # casino and stock_exchange: Sydney's The Star and the ASX, notable but
    # businesses as a bank is (2026-10-08).
    "amenity": {"restaurant", "cafe", "bar", "pub", "fast_food", "bank", "pharmacy",
                "fuel", "parking", "car_rental", "food_court", "casino", "stock_exchange"},
    "tourism": {"hotel", "guest_house", "hostel", "motel", "apartment", "chalet"},
    # A yoga studio also tagged a place of worship (Seattle, 2026-10-08).
    "leisure": {"fitness_centre"},
}
# A public_transport=station tagged with one of OTHER_MODES and neither a
# railway tag nor one of RAIL_MODES is a bus or ferry terminal. One with no
# mode at all stays: Kyoto's 鞍馬駅 and Seattle's South Bellevue carry none.
# Any value but "no" marks the mode: Hong Kong's termini carry bus=private
# and bus=minibus (batch 2b, 2026-10-08).
RAIL_MODES = ("train", "subway", "light_rail", "tram", "monorail", "funicular")
RAIL_STATION_VALUES = {"subway", "light_rail", "train"}
OTHER_MODES = ("bus", "ferry", "trolleybus", "coach", "minibus")
# And by the facility's own tag, where no mode is written: Hong Kong's public
# transport interchanges (amenity=bus_station), ferry piers and the Ngong
# Ping cable-car terminal (aerialway=station), 2026-10-08.
NOT_RAIL = {"amenity": {"bus_station", "ferry_terminal"}, "aerialway": {"station"}}
NOT_STATION_AMENITY = {"school", "kindergarten", "college", "university"}
# A commercial building is a business unless notable: Sydney's numbered
# "Bay 0" to "Bay 15", historic=building on building=commercial (2026-10-08).
# A hotel building likewise (Barcelona's Casa Cambó, building=hotel, batch 2a).
# And a data centre (Marseille's U-boat bunker, building=data_center, batch 2a).
COMMERCIAL_BUILDINGS = {"commercial", "retail", "office", "hotel", "data_center"}
# historic=* values that are clutter at a search box (wayside shrines and
# stones number in the hundreds and are named after their saint or deity).
# NOT "monument" (measured 2026-10-11, after the owner's yes to holding it to
# the rule memorials follow): across the nineteen indexes it removed about
# 420 rows, among them Seoul's statue of King Sejong and its March 1st
# monument, Montréal's Canadiens statues, Chicago's Marquette Monument,
# Mexico City's Monumento a Morelos and Sydney's Queen Victoria Building,
# none of which carries wikidata in OSM. London's graves and mis-named nodes
# under historic=monument are dropped by id instead. Put back to the owner.
SKIP_HISTORIC = {"wayside_shrine", "wayside_cross", "boundary_stone", "milestone",
                 "memorial", "tomb", "yes"}
# Tourism and education landmarks need a wikidata or wikipedia tag: without
# one, OSM's tourism=attraction and amenity=college in Kyoto included a
# tea-ceremony shop and a private computer school (2026-10-07), businesses by
# another name. Named markets likewise (amenity=marketplace; owner,
# 2026-10-07: notable only), since an OSM marketplace can be one company's
# market hall. Places of worship, parks, gardens, peaks, rivers and historic
# sites need none. Airports likewise (aeroway), so a private airstrip stays
# out (2026-10-08).
NOTABLE_ONLY = ("tourism", "amenity", "aeroway")
RESIDENTIAL_BUILDINGS = {"house", "residential", "apartments", "detached", "dormitory",
                         "semidetached_house", "terrace", "bungalow"}
# A historic building named as a home is one ("Faulkner House", "Walker
# Residence"; Vancouver, 2026-10-08), unless its building tag says otherwise.
HOME_NAME = re.compile(r"\b(house|residence|cottage|mansion|farmhouse|homestead)$", re.I)
# The same in a local language, where the house word LEADS the name
# ("Maison Joseph-Masson", Montréal, 2026-10-08: historic=manor on
# building=yes, not open to visitors). Leading only: a Dutch "-huis" ending is
# a town hall (stadhuis) or a hospital (ziekenhuis), and Prague's "Obecní dům"
# is a civic building.
HOME_NAME_LEAD = {"fr": ("maison", "manoir"), "ca": ("casa",), "es": ("casa",),
                  "pt": ("casa", "residência", "solar", "palacete"),
                  "cs": ("dům", "vila"), "nl": ("huis",),
                  # NOT "haus": in Westphalia it names a manor (Haus Darl), and
                  # a "-haus" ending is a town hall or a hospital.
                  "de": ("wohnhaus", "villa", "landhaus"),
                  "da": ("villa", "landsted", "landstedet"),
                  "nb": ("villa",),
                  "sv": ("villa", "bostadshus"),
                  "lv": ("villa", "vila", "savrupmāja", "dzīvojamā"),
                  "ro": ("casa", "casă", "vila", "vilă"),
                  "it": ("villino", "villini"),
                  "el": ("οικία", "κατοικία", "βίλα", "βίλλα", "έπαυλη", "αρχοντικό", "σπίτι")}
# And where the house word CLOSES the name (batch 2b, 2026-10-08): Korean 가옥
# and 고택 (a traditional house), 옛집 (an old house), 생가 (a birthplace),
# 저택 and 주택; Chinese 故居 and 舊居 (a former residence), 大宅, 別墅 and
# 宅; Georgian სახლი (a house), as the last word. A house-museum (tourism=
# museum, სახლ-მუზეუმი) passes _public_home, as a museum in a 생가 does.
HOME_NAME_END = {"ko": ("가옥", "고택", "옛집", "생가", "저택", "주택"),
                 "zh": ("故居", "舊居", "大宅", "別墅", "宅"), "ka": ("სახლი",),
                 # Where the house word comes last (candidate 34, owner
                 # 2026-10-13): Latvian "Mindeļa villa"; Norwegian farms, the
                 # three words as the whole last word, so "kirkegård" (a
                 # churchyard) and "skolegård" are not read.
                 "lv": ("villa",), "nb": ("gård", "hovedgård", "prestegård")}


# historic=* values that are a house: a manor is OSM's manor house or country
# house (Marseille's 130-odd bastides and its town mansions, the hôtels
# particuliers, batch 2a, 2026-10-08), held to _public_home as historic=house is.
HOME_HISTORIC = {"house", "manor"}
# Amenities that make a historic house a civic place (_home). Places of
# worship are not among them: a house church can be someone's home.
CIVIC_AMENITIES = {"townhall", "arts_centre", "community_centre", "library", "theatre"}


# German only (HOME_LEAD_ON_PARKS): measured on the 19, the Spanish lead
# "casa" took six of Mexico City's culture houses tagged leisure=park ("Casa
# de la Cultura ...") and no home; no other language's lead moved a row.
# Measure a language on its built cities before adding it.
HOME_LEAD_ON_PARKS = {"de"}


def _home_lead(name, local):
    ws = re.findall(r"\w+", name.lower()) or [""]
    return any(ws[0] in HOME_NAME_LEAD.get(c, ()) for c in local if c in HOME_LEAD_ON_PARKS)


def _home_name(name, local):
    if HOME_NAME.search(name):
        return True
    low = name.lower().strip()
    ws = re.findall(r"\w+", low) or [""]
    if any(ws[0] in HOME_NAME_LEAD.get(c, ()) for c in local):
        return True
    return any(low.endswith(e) if _CJK_WORD.search(e) else ws[-1] == e
               for c in local for e in HOME_NAME_END.get(c, ()))


def _home(tags, names, local=()):
    """True for a home: residential land, a house or an apartment building,
    private access, or a historic house."""
    if tags.get("historic") == "district":
        return False      # an area of homes is a place (Chicago's Prairie Avenue District)
    # A civic institution in a historic house is the institution, not a home:
    # Marseille's district town halls and an arts centre sit in bastides
    # tagged historic=manor (batch 2a, 2026-10-08). The house tests by history
    # and name below skip it; the land, building and access tests still apply.
    civic = tags.get("amenity") in CIVIC_AMENITIES
    # A NOTABLE place of worship on residential land or in a residential
    # building is a place (owner, 2026-10-08: "yes notable place of worship
    # back in"): Prague's Hussite churches and Barcelona's parishes in
    # apartment blocks. A non-notable one stays out, since a house church can
    # be a home; private access still keeps either out.
    worship = tags.get("amenity") == "place_of_worship" and bool(tags.get("wikidata") or tags.get("wikipedia"))
    return ((tags.get("landuse") == "residential" and not worship)
            or (tags.get("building") in RESIDENTIAL_BUILDINGS and not worship)
            or tags.get("access") == "private" or (tags.get("historic") == "house" and not civic)
            # A manor on a plain building: Montréal's Château Goyer, a manor
            # on building=pavilion in a park, stays.
            or (tags.get("historic") in HOME_HISTORIC and tags.get("building") in (None, "yes")
                and not civic)
            or tags.get("house") == "yes"
            # By name only where the building tag says no more: Kyoto's
            # "Kwasan Observatory Solar House" is building=university.
            or (tags.get("historic") and tags.get("building") in (None, "yes") and not civic
                and any(_home_name(n, local) for n in names))
            # A park or a garden whose name LEADS with a house word is the
            # house's grounds (the third list, 2026-10-13: Berlin's "Villa
            # Lemm", leisure=park). The lead only: a name that ends in one
            # ("Hull House Park") is a park named for a house.
            or (tags.get("leisure") in ("park", "garden") and any(_home_lead(n, local) for n in names)))


def _home_signs(tags, names, local=()):
    """["access"] where access=private is the ONLY thing that makes an object
    a home for _home, [] where _home does not fire, else ["other"]."""
    if not _home(tags, names, local):
        return []
    less = {k: v for k, v in tags.items() if k != "access"}
    return ["other"] if tags.get("access") != "private" or _home(less, names, local) else ["access"]


def _private_access_only(tags, names, local=()):
    """True where access=private alone trips the home test on something that
    is no home by its tags: not a garden or a park (a private garden is a
    home's) and not a castle or palace (a residence). Asked only of an object
    with an article of its own (landmark_drop)."""
    return (_home_signs(tags, names, local) == ["access"] and not tags.get("leisure")
            and tags.get("historic") != "castle" and not tags.get("castle_type"))


def _public_home(tags):
    """A home a visitor may look for: open as a museum or an attraction. A
    heritage designation, a wikidata item or a Wikipedia article is not:
    Canada's Register of Historic Places reached wikidata in bulk, and
    Chicago's landmark apartment buildings have articles, and each is still
    somebody's home (2026-10-08)."""
    # A bare tourism=yes is no opening: Barcelona's Casa Comalat, an apartment
    # building, carries it with access=private (batch 2a, 2026-10-08). Private
    # access alone is not tested here: Brussels' Royal Palace carries it, and
    # opens to visitors each summer.
    return bool(tags.get("tourism") not in (None, "yes") or tags.get("museum"))
# Never place=isolated_dwelling or farm: a single home (Kyoto's one was an
# apartment building, 2026-10-07).
PLACE_VALUES = {"city", "borough", "suburb", "quarter", "neighbourhood", "village",
                "hamlet", "town", "locality"}
SETTLEMENTS = {"city", "town", "village", "hamlet"}
# A street-pair crossing seen at several nodes counts as one place unless its
# nodes lie further apart than this (a long pair of streets crossing twice).
CROSSING_MERGE_M = 250
# A place or landmark of the same name this near another is the same one
# when either is an area: a suburb's node and its area's center lie up to a
# few hundred metres apart (Sydney's Redfern, The Rocks; 2026-10-08). Two
# nodes are two places: Kyoto has many same-named 町 close together.
NEAR_DUP_M = {"place": 1500, "landmark": 300}
# Degrees around the street nodes' extent within which a tagged place counts
# as the city's (about 500 m).
EXTENT_PAD = 0.005


# Names that are no name: placeholders, error values, a number alone (owner,
# 2026-10-08: "exclude error search terms like # or !ERROR!"). Found in the
# sample: Seattle's artwork "Untitled" and street "3816-3852" (an address
# range), Chicago's streets "47" and "315, 379, 383, 384 & 385" (ramp and
# route numbers), Kyoto's landmarks "1080" and "7105". A name like this is
# dropped and the object keeps its others; with none left, it goes.
JUNK_NAMES = {"untitled", "unnamed", "unknown", "noname", "no name", "nan", "null", "none",
              "undefined", "n/a", "na", "error", "test", "tbd", "todo", "fixme", "?",
              # Hong Kong's FEHD placeholder (Cleanup's inventory, 2026-10-08).
              "no record", "no record found"}
# Contact details in a name: an email or a phone number; the name goes, as
# map_common._has_contact_details drops the row. NANP 3-3-4 as there, plus a
# trunk-prefixed Japanese or Korean number (075-123-4567, 02-123-4567), which
# that rule misses (Cleanup's inventory, 2026-10-08). The junk-name pass is
# to merge the two.
_CONTACT = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
                      r"|(?:\+?1[ .\-]?)?\(?\d{3}\)?[ .\-]\d{3}[ .\-]\d{4}"
                      r"|(?<!\d)0\d{1,3}-\d{2,4}-\d{4}(?!\d)")
# A web address is no name (a fault mended, 2026-10-13: Toronto's landmark
# named "https://papemosque.ca/"). The scheme anywhere, or a leading "www.".
_WEB_ADDRESS = re.compile(r"https?://|^www[.]", re.I)
# A height is no name (a fault mended, 2026-10-13: peaks named "109m",
# "120.6m", "222M"; Sasebo 74, Nagasaki 22). The number-alone rule reads a
# number with the metre sign as a number alone. The whole name only.
_HEIGHT_ONLY = re.compile(r"\d+(?:[.,]\d+)?\s*m", re.I)
JUNK_MARKS = ("#n/a", "#ref", "#value", "#div/0", "#name?", "#num", "#null", "!error",
              chr(0xFFFD))  # the replacement character, a broken decode


def _bare_personal(name):
    # Imported here: japan_register is only needed for a Japanese city.
    from pipeline.countries.japan_register import bare_personal_name
    return bare_personal_name(name)


def junk_name(name):
    low = name.strip().lower()
    # A "?" where a character was lost in decoding, as map_common's
    # glitched-name rule reads it (Cleanup, 2026-10-08): leading and not
    # followed by a space ("??野家"; New York's "? TEA" stays), or between two
    # letters ("Montr?al"). The two rules are to agree, and merge at landing.
    lost = (low.startswith("?") and not low.startswith("? ")) or any(
        low[i] == "?" and low[i - 1].isalpha() and low[i + 1].isalpha() for i in range(1, len(low) - 1))
    return (lost or not any(c.isalpha() for c in low) or low.strip("!?.#() ") in JUNK_NAMES
            or any(m in low for m in JUNK_MARKS) or bool(_CONTACT.search(name))
            or bool(_WEB_ADDRESS.search(low))
            or bool(_HEIGHT_ONLY.fullmatch(unicodedata.normalize("NFKC", low))))


# BARE TYPE WORDS (owner, 2026-10-11: "proposed list sounds good"): a name
# that is only its object's type describes and does not name; Seoul carried
# 19 playgrounds named 놀이터 and 12 rest spots named 쉼터, Hong Kong 14
# ancestral halls named 祠堂, Kyoto ten 本殿 (a shrine's main hall). Matched
# as the WHOLE name only, in English and the city's languages, on landmarks
# and places, never streets, stations or junctions. A number after a CJK or
# Hangul word is set aside ("놀이터 2"); never after a Latin one, since
# Chicago's "Park 399" is the Park District's own name for the park. An
# object whose main name is bare goes whole (its English alias is the same
# word translated: "Main Hall", "Neighborhood Park"); a bare alias beside a
# real name goes alone.
# The cost: a real place whose only name is its type goes too. Measured on
# the fourteen built indexes before it was added
# (docs/decisions_drafts/place-search.md, 2026-10-11); measure a new word on
# every built city of its language first.
BARE_TYPE_NAMES = {
    "en": ("monument", "memorial", "sculpture", "statue", "stupa", "park", "playground", "church",
           "chapel", "temple", "shrine", "fountain", "garden", "viewpoint", "lookout", "pavilion",
           "gazebo", "clubhouse", "greenbelt", "korean church", "playpark", "prayer room",
           # London's read (batch 3; owner, 2026-10-11: "measure and add"),
           # measured on Seattle, Chicago, Vancouver and Sydney first: street
           # furniture, garden and estate structures, earthworks and prayer
           # rooms under their type alone. NOT here, since each is also a
           # place's real name somewhere: The Green, The Glade, Village
           # Green, The Terrace, Memorial Park, Memorial Gardens, Italian
           # Gardens, Japanese Garden, Old Town Hall, Pagoda, Amphitheatre,
           # Totem Pole, Spa, Lion.
           "war memorial", "first world war memorial", "second world war memorial",
           "world war 1 memorial", "boer war memorial", "civilian memorial",
           "police public callbox", "police call box", "police phone post",
           "police telephone callbox", "coal tax post", "lamp post", "lamp standard",
           "ventilation shaft cover", "anglican chapel", "nonconformist chapel",
           "multi-faith prayer room", "multi faith prayer room", "multifaith prayer room",
           "multi-faith room", "multifaith centre", "prayer hall", "prayer rooms",
           "chaplaincy centre", "alcove", "gate lodge", "icehouse", "ice well", "summerhouse",
           "stable block", "the stables", "columbarium", "church porch", "lych gate", "lime kiln",
           "conduit head", "gothic arch", "gothic ruins", "ruined arch", "gateway tower",
           "the folly", "the grotto", "cattle trough", "double cattle trough",
           "victorian cattle trough", "drinking fountain", "victorian drinking fountain",
           "obelisk", "the obelisk", "clocktower", "sundial", "tumulus", "mill ruins",
           "waterwheel pit", "water treatment", "bomb crater", "blast mound", "tank traps",
           "type 22 pillbox", "fossil pit", "fossilised tree", "the earthworks",
           "community garden", "bandstand", "the bandstand", "the band stand", "paddocks",
           "the meadow", "the walled garden", "outdoor learning area", "tree space",
           "athletics stadium", "piazza", "the plaza", "the main square", "main quad",
           "south quad", "figurehead", "waterfall", "rope circle", "ravine",
           "common watercourse", "pocket park", "play area",
           # The outside name net's read of the 19 built cities (owner, 2026-10-12).
           "detention pond", "meadow", "lawn", "showring", "gatehouse", "control tower",
           "perennial border", "mooring anchors", "solarium",
           # Wave 1's candidates (owner, 2026-10-13), measured on the 19 built
           # cities first: 5 rows, "The Quad" in Chicago and Seattle, "Quad"
           # in Montréal, "Parade Ground" in Seattle and Sydney. Seattle's
           # Quad keeps its row on an article of its own.
           "walled garden", "standing stone", "stone circle", "clock tower", "packhorse bridge",
           "grotto", "dovecot", "kiln", "mort safe", "parade ground", "chaplaincy", "prayer room",
           "cairn", "cross", "tower", "barrow", "bathhouse", "battery", "bullaun stone",
           "water pump", "ice house", "martello tower", "granary", "sheep fold", "mill race",
           "parish centre", "quad", "the quad", "pharmacy", "worship center", "sculpture garden",
           "dog park", "off leash dog park", "water fountain", "community park", "urban park",
           "rooftop park", "redwood grove", "secret garden",
           # Wave 1's second list (owner, 2026-10-13, the second rule batch;
           # the counts are in THE SECOND RULE BATCH below). NOT "back lane":
           # a real street name (Manchester), taken out of
           # STREET_DESCRIPTIONS by the same ruling.
           "office", "garage", "sanctuary", "masjid", "mini-park", "mini park", "minipark",
           "sports complex", "greenstreets", "greenstreet", "green streets", "green street", "greenway",
           "parkland",
           "barn", "cistern", "tot lot", "totlot", "swp"),
    "ja": ("本殿", "本堂", "拝殿", "灯籠", "唐門", "山門", "五重塔", "御影堂", "金堂", "鳥居", "鐘楼",
           "石碑", "公園", "児童公園", "広場", "記念碑",
           # Tokyo's read (batch 3, 2026-10-11): shrine fixtures, pocket parks
           # and privately owned public open space under their type alone.
           "児童遊園", "遊園", "ポケットパーク", "公開空地", "公開空き地", "空地", "電柱", "時計台",
           "稲荷", "庚申塔", "神楽殿", "合祀殿", "三重塔", "車祓所", "絵馬掛", "社号碑", "力石",
           "正門", "黒門", "日本庭園", "暗渠", "駐車場", "富士塚",
           # The outside name net's read of the 19 built cities (owner, 2026-10-12).
           "法堂", "仁王門", "百度石"),
    "ko": ("놀이터", "어린이놀이터", "쉼터", "전망대", "대웅전", "칠성각", "산신각", "근린공원", "쌈지공원",
           "어린이공원", "소공원", "공원", "녹지", "교회", "성당", "불교", "원불교", "통일교", "정자",
           "팔각정", "삼각점", "사자상", "분수", "분수대", "약수터", "운동장", "광장", "기념비", "동상",
           "조형물", "조각상", "연못",
           # The outside name net's read of the 19 built cities (owner, 2026-10-12).
           "비석", "배수로", "화단", "대운동장", "산책공원", "분수공원", "강변 공원", "가마터",
           "유아숲체험장", "가족조각상", "호상비문", "강학공간",
           # The final group's reads of Anyang and Gwangju (owner, 2026-10-13,
           # the third list).
           "족구장", "고인돌", "왕국회관", "가든", "공터", "구령대", "물놀이장", "산책로", "생태 공원",
           "조각공원", "호수공원", "기념탑", "설립기념탑", "일주문", "비좌", "연자방아", "훈련센터",
           "자연마을", "놀이공원", "물놀이공원", "썬큰광장"),
    "zh": ("祠堂", "土地", "土地廟", "土地公", "伯公", "社壇", "碉堡", "涼亭", "公園", "遊樂場", "休憩處",
           "觀景台", "廟",
           # The outside name net's read of the 19 built cities (owner, 2026-10-12).
           "炮台",
           # Earth-god shrines under their type alone (candidate 19, owner
           # 2026-10-13; the commonest whole names of Taipei's, Taoyuan's and
           # Taichung's places of worship: 福德祠 134, 福德宮 120, 土地公廟 116).
           # The last two are "福德祠(土地公廟)" less its closing bracket, as
           # bare_type strips it. NOT 福安宮, 福興宮, 萬善堂: temples' own names.
           "福德祠", "福德宮", "福德廟", "福德正神", "土地公廟", "土地公祠", "伯公廟", "福德祠(土地公廟",
           "福德宮(土地公廟"),
    "fr": ("cuve", "ancienne batterie", "monument", "statue", "fontaine", "parc", "église", "chapelle",
           "jardin", "square", "calvaire", "croix",
           # Paris's read (batch 3, 2026-10-11). "Édicule Guimard" is the
           # type of 57 metro entrances mapped one by one as artworks.
           "synagogue", "presbytère", "aumônerie", "salle de prière", "crypte", "grande crypte",
           "gradins", "monument aux morts", "monument du souvenir", "espace canin",
           "le jardin botanique", "la parcelle", "ancien réservoir", "le square",
           "centre bouddhiste", "chapelle orthodoxe", "édicule guimard",
           # The outside name net's read of the 19 built cities (owner, 2026-10-12).
           # Marseille's ruins on the Frioul islands, each mapped with its
           # description in the name field.
           "toilettes", "pont aqueduc", "ancien socle", "ancienne vigie", "tour penchée",
           "niche à chien", "terrasse funéraire", "anciens fours à chaux",
           "ruines du vieux moulin", "édicule des eaux", "ancienne cuve pour canon",
           "ruines d'un jaç"),
    "ca": ("capella", "font", "parc", "església", "monument", "jardí", "jardins",
           # The outside name net's read of the 19 built cities (owner, 2026-10-12).
           "església evangèlica", "centre ecumènic", "umbracle", "testimoni de jehova"),
    "es": ("capilla", "fuente", "parque", "iglesia", "monumento", "plaza", "jardín", "kiosco",
           "templo", "parroquia", "jardinera", "área verde", "juegos infantiles",
           # The wider Mexico City area's read (owner, 2026-10-12): 46 rows in
           # Ecatepec and Naucalpan, none in Barcelona. "catedral" (Ecatepec's
           # cathedral under its type word) and "parque hundido" (a known
           # park's own name in Ciudad de Mexico) are left out on purpose.
           "área verde comunitaria", "circuito para bicicletas", "andador para bicicletas",
           "arboleda", "arbolera", "jardín comunal", "corredor del camellon", "zona de juegos",
           "cancha de football", "campo fut7", "parque deportivo", "parque canino",
           "parque escolar", "parque de la iglesia", "parque de la glorieta",
           "parque de la colonia", "parque del pueblo", "parque del mercado", "plaza civica",
           "patio iglesia", "ciclopista", "centro religioso", "iglesia cristiana",
           "templo adventista", "iglesia antigua", "estatua moderna", "reloj", "virgen monumental",
           # Mexico City's read (batch 3, 2026-10-11): street shrines, median
           # strips, courts and a housing unit's common areas, each mapped
           # with its description in the name field.
           "altar", "nicho", "virgen", "ermita", "bautisterio", "seminario", "convento", "camellón",
           "cancha", "canchas", "cancha de futbol", "andador", "sendero", "placita", "triángulo",
           "el triángulo", "bandera", "asta bandera", "escudo", "áreas verdes", "zona verde",
           "área común", "áreas comunes", "área infantil", "área de juegos", "juegos",
           "aparatos de ejercicio", "zona de perros", "parque recreativo", "parque infantil",
           "centro comunitario", "centro de reuniones", "vecindad", "terreno", "helipuerto",
           "iglesia católica", "iglesia mormona", "jardín botánico", "casa de retiros",
           # Guadalajara's estate amenities tagged parks (candidate 26, owner
           # 2026-10-13). NOT "coto" names; "camellón" is above.
           "terraza", "casa club"),
    "pt": ("praça", "parque", "igreja", "capela", "monumento", "estátua", "fonte", "jardim",
           "playground", "quadra", "mirante", "coreto", "área verde",
           # Sao Paulo's read (batch 3, 2026-10-11).
           "pracinha", "praçinha", "parcão", "parklet", "lazer", "bosque", "busto", "capelinha",
           "casa paroquial", "casa de oração", "centro espírita", "seminário teológico",
           "mata nativa", "terreno", "pequeno parque", "área arborizada", "área verde livre",
           "praça pública", "praça da igreja", "nossa praça", "academia ao ar livre",
           "campo de futebol", "sem denominação"),
    "cs": ("kaple", "kostel", "park", "pomník", "památník", "socha", "kříž", "zvonice",
           "hřbitovní kaple", "bývalá kaple", "památník padlých", "pomník padlých"),
    "nl": ("kapel", "kerk", "park", "fontein", "standbeeld", "monument"),
    # German (owner, 2026-10-13; search-lang-de.md: 45 rows over the four
    # cities). NOT "marktplatz" (a square's real name), "ohne titel" (a
    # title), rathaus, bürgerpark, stadtwald, rosengarten, dorfkirche
    # (proper names in use).
    "de": ("kirche", "kapelle", "park", "spielplatz", "denkmal", "brunnen", "friedhof", "mahnmal",
           "wegekreuz", "wegkreuz", "bolzplatz", "sportplatz", "grünanlage", "ehrenmal", "gedenkstein",
           "kriegerdenkmal", "gedenktafel", "skulptur", "pfarrhaus", "gedenkkreuz", "trauerhalle",
           "evangelisches gemeindehaus", "friedhofskapelle", "dachgarten", "rodelberg", "badestrand",
           "fkk-strand", "hundestrand", "tennisstadion", "hügelgrab", "kirchgemeindehaus", "atrium",
           "hartplatz"),
    # Danish (owner, 2026-10-13; search-final's search-lang-da.md, with its id catches and future edit points).
    "da": ("kirke", "kapel", "park", "legeplads", "mindesten", "mindesmærke", "monument", "springvand",
           "kirkegård", "skulptur", "statue", "genforeningssten", "genforeningsstenen", "byfredssten",
           "bautasten", "mindelund", "vandkunst", "græsplæne", "stenkister", "bænk", "sten",
           "abstrakt skulptur", "steler"),
    # Norwegian (owner, 2026-10-13; search-final's search-lang-nb.md, with its id catches and future edit points).
    "nb": ("kirke", "kapell", "park", "lekeplass", "leikeplass", "lekeplassen", "minnesmerke",
           "monument", "statue", "skulptur", "fontene", "kirkegård", "gravlund", "krigsminnesmerke",
           "minnelund", "kanoner", "kanon", "relieff", "telefon", "gurdwara", "bosetning"),
    # Swedish (owner, 2026-10-13; search-final's search-lang-sv.md, with its id catches and future edit points).
    "sv": ("kyrka", "kyrkan", "kapell", "kapellet", "park", "parken", "lekplats", "lekplatsen",
           "lekpark", "minnesmärke", "minnessten", "minneslund", "fontän", "fontänen", "kyrkogård",
           "kyrkogården", "begravningsplats", "skulptur", "staty", "byst", "kors", "fotbollsplan",
           "bollplan", "idrottsplats", "badplats", "utsikt", "utsiktsplats", "utsiktspunkt", "gravfält",
           "runsten", "domarring", "kvarnruin", "hamnkran", "lekparken"),
    # Latvian (owner, 2026-10-13; search-final's search-lang-lv.md, with its id catches and future edit points).
    "lv": ("baznīca", "kapela", "kapliča", "lūgšanu nams", "parks", "skvērs", "rotaļu laukums",
           "bērnu rotaļu laukums", "bērnu laukums", "sporta laukums", "basketbola laukums",
           "futbola laukums", "suņu pastaigu laukums", "skeitparks", "stadions", "pludmale",
           "peldvieta", "piemineklis", "piemiņas akmens", "piemiņas plāksne", "piemiņas zīme",
           "memoriāls", "skulptūra", "strūklaka", "krusts", "kapi", "kapsēta", "estrāde"),
    # Romanian (owner, 2026-10-13; search-final's search-lang-ro.md, with its id catches and future edit points).
    "ro": ("biserică", "biserica", "capelă", "capela", "parc", "parcul", "loc de joacă", "troiță",
           "troița", "cruce", "monument", "statuie", "bust", "fântână", "fântână arteziană", "cimitir",
           "foișor", "clopotniță", "casa parohială", "casă parohială", "biserica ortodoxă",
           "biserică ortodoxă", "biserica reformată", "teren de sport"),
    # Italian (owner, 2026-10-13; search-final's search-lang-it.md, with its id catches and future edit points).
    "it": ("chiesa", "cappella", "parco", "giardino", "giardini", "parco giochi", "area giochi",
           "fontana", "fontanella", "monumento", "monumento ai caduti", "statua", "madonnina",
           "edicola", "obelisco", "rudere", "ruderi", "anfiteatro", "mausoleo", "colombario", "ninfeo",
           "cisterna", "cisterne", "sacrario", "area fitness", "area relax", "parco condominiale",
           "parco comunale", "giardino comunale", "giardino parrocchiale", "parco per bambini",
           "parco della chiesa", "chiesa evangelica", "chiesa cristiana evangelica",
           "chiesa apostolica", "evangelica", "sala del regno", "sala del regno dei testimoni di geova",
           "tomba romana", "tombe romane", "cisterna romana", "villa romana", "villa rustica",
           "domus rustica", "mausoleo romano", "sepolcro romano", "terme romane", "terme romana",
           "ninfeo romano", "colonna romana", "cippo romano", "vasca romana",
           "resti di una villa romana", "zona archeologica", "necropoli arcaica",
           "basilica paleocristiana", "latrine pubbliche", "cortili porticati", "strada lastricata",
           "piazzale lastricato", "calidarium", "frigidarium", "colonnata", "edicola di culto",
           "sepolcro a camera", "roman tomb", "pista ciclabile", "percorso ciclopedonale"),
    # Greek (owner, 2026-10-13; search-final's search-lang-el.md, with its id catches and future edit points).
    "el": ("εκκλησία", "εκκλησάκι", "παρεκκλήσι", "ναός", "ιερός ναός", "πάρκο", "πάρκο τσέπης",
           "παιδική χαρά", "πλατεία", "μνημείο", "ηρώο", "άγαλμα", "προτομή", "γλυπτό", "κρήνη",
           "βρύση", "νεκροταφείο", "κοιμητήριο", "εικονοστάσι", "βοηθητικό γήπεδο"),
    "ka": ("ეკლესია", "პარკი", "სკვერი", "ძეგლი", "შადრევანი", "ბაღი", "სასაფლაო"),
}
# THE SIXTH PASS'S WORDS (owner, 2026-10-13: "all approved", the sixteen
# rulings; the bare-type lists gain the words the readers found, a fault and
# no new ruling). Each is a WHOLE name a reader dropped as a bare type word:
# the five pilot cities read in full (Rio de Janeiro, Madrid, Osaka, Daegu,
# Amsterdam: data/_search_rollout/pilot_reads) and the final group's held
# rows (data/_search_rollout/final_held_settle; Taichung 127, Brasilia 45).
# The guards are unchanged: an article of the object's own keeps a row,
# config.PLACE_KEPT keeps one, a station of the map or of a rail network is
# never dropped. Measured on the 19 live cities, 2026-10-13: 13 rows leave
# (Busan 5, Mexico City 3, Kyoto 2, Seoul 2, Tokyo 1), none in Sao Paulo or
# Hong Kong; on the five pilot cities 98, 97 of them a reader's drop. NOT
# here, though readers dropped rows under each: Spanish "polvorín" (owner,
# 2026-10-13: Mexico City's "El Polvorín" is a proper name), "mirador",
# "parque hundido" (Mexico City's park of that name), "las estufas" and
# "plaza gastronómica", Portuguese "cruz", and the sentence-long
# descriptions no list can hold.
BARE_TYPE_NAMES_6 = {
    "en": ("soccer field", "public garden", "outdoor gym", "speedway stadium"),
    "pt": ("assentos", "academia popular ao ar livre", "arena", "avião", "ciep", "complexo esportivo",
           "obelisco", "parquinho", "pátio externo", "praça rotatória", "trevo", "entrada/saida",
           "quadra de futebol", "rua projetada", "ruinas", "área de convivência", "loteamento",
           "catedral tombada", "edifício tombado", "paróquia", "área livre", "churrasqueira pública",
           "ponto de encontro comunitário", "ponto de enconto comunitário",
           "ponto de encontro de comunitário", "pec", "ponto de convivência", "campo gramado",
           "campo de areia", "campo aberto", "campinho de futebol", "gramado", "quadra de areia",
           "quadra de futvolei", "quadra poliesportiva", "academia comunitária",
           "area verde comunitária", "centro comunitario", "centro esportivo publico",
           "parque de esportes", "parque de uso múltiplo", "praça comunitária pública",
           "praça de entrequadras", "pracinha da igreja", "calçada arborizada", "circo", "cras",
           "totem", "horatorio", "largo"),
    "es": ("hórreo", "laberinto", "parque lineal", "parterre", "puente", "reloj de sol",
           "capilla universitaria", "capilla del hospital", "antiguas tuberías",
           "antiguo depósito de agua", "canchas deportivas", "unidad deportiva", "arboretum",
           "parque público", "parque comunitario", "parque recreactivo", "astas", "pileta",
           "area recreativa", "area de descanso", "parque de juegos", "parque para niños",
           "parquesito", "plasita", "rotonda", "arco", "centro deportivo", "estadio de beisbol",
           "canalon", "crisol de fundición", "grúa portal"),
    "ko": ("교육관", "배드민턴장", "야외공연장", "운동시설", "추모비", "축구경기장", "테니스장", "무명봉"),
    "ja": ("ゲートボール場", "丘", "仏", "地蔵", "大師堂", "幹線用水路", "手水舎", "瞑想室", "社務所",
           "芝生広場", "護摩堂", "貯水池", "遥拝所", "曼荼羅", "新興宗教", "キリスト教会",
           "メインスタンド", "バックスタンド", "北スタンド", "南スタンド", "表忠碑", "戦没記念碑",
           "開発公園", "屋上広場", "多目的広場", "中心伽藍", "本坊庭園", "演舞場", "文殊菩薩", "針塚",
           "神籬磐境", "荒神様", "正一位稲荷大明神", "遺跡", "仏舎利塔", "浄水場跡", "自由広場",
           "多目的自由広場", "自然動物公園", "祠", "森の遊び場"),
    "zh": ("百姓公廟", "萬善堂", "體育館", "三角公園", "萬善祠", "大眾爺廟", "觀音亭", "親水公園",
           "水源地", "福德正神", "福德正神廟", "福德堂", "百姓公", "百姓祠", "萬應公", "萬靈祠",
           "觀音廟", "宮廟", "舍利塔", "金紙爐", "活動中心", "技擊館", "綜合球場", "羽球館", "體操館",
           "口袋公園", "兒童公園", "園道", "綠園道", "運動公園", "運動設施", "開放空間", "足球場",
           "滑板場", "棒/壘球場", "環保公園", "河堤公園", "站前公園", "站前廣場", "古井", "門樓", "中廊",
           "操場", "戶外表演舞台", "噴水池廣場", "農場", "苗圃", "分場", "馬場", "福利社", "伙房", "堰堤",
           "福德詞", "圖書館", "行刑場", "瀑布", "鄉界"),
    "nl": ("heemtuin", "koninkrijkszaal", "zonder titel", "ziekenboeg", "oud kapelleke"),
    "fr": ("donjon", "aqueduc", "totem", "mairie", "paroisse", "grotte mariale", "infirmerie",
           "hôtel particulier", "ancien hôtel"),
    "it": ("sport park", "casa del parco", "viale principale", "piazzale circolare"),
    "ro": ("tun", "tunuri", "monumentul eroilor", "turnul de apă", "parc copii", "biserica veche"),
    "da": ("bypark midt", "bypark nord"),
    "nb": ("lommeparken", "pocketparken", "park vest", "øvre park", "østre parkdrag"),
    "sv": ("borggården", "entretorg", "köksträdgård", "örtagården", "orangeriet", "ödetomten", "rinken"),
    "lv": ("komandpunkts",),
    "el": ("κέντρο",),
}
for _code, _words in BARE_TYPE_NAMES_6.items():
    BARE_TYPE_NAMES[_code] = BARE_TYPE_NAMES.get(_code, ()) + _words
# A SIXTH-PASS WORD THAT IS ALSO A SETTLEMENT'S OWN NAME, kept on a PLACE row
# (measured 2026-10-13 on the final group's cities, built in memory): Taipei's
# and Taoyuan's hamlets and localities 水源地 (4), 堰堤 and 苗圃, Yamagata's
# quarter 大師堂. On a landmark each is still a bare type word.
BARE_WORD_SETTLEMENTS = frozenset(("水源地", "堰堤", "苗圃", "大師堂"))


# A CODE PLUS A TYPE IS NO NAME EITHER (owner, 2026-10-12: "yes drop"): a
# parcel or building code beside a type word. The outside name net found the
# class live: Surrey's park parcels in the Vancouver index ("54F - Greenbelt",
# "103D - Utility ROW", "122L Greenbelt", 20 rows), Sand Point's and the
# Ballard Locks' numbered buildings in Seattle ("Building 30", "Operating
# House No. 1"), the numbered Stations of the Cross on Petrin in Prague
# ("10. zastavení"), both kept after all by REGISTERED_KEYS below, and a
# numbered park lot in Busan ("921호 공원"). Matched as the WHOLE name, case as written, in
# English and the city's languages. Deliberately narrow: a leading parcel
# code needs its spaced dash or one of Surrey's four type words, so "5th
# Avenue Theatre" and Chicago's "Park 399" (the Park District's own name,
# see below) are untouched. Measure a new pattern on every built city first.
CODED_TYPE = {
    "en": re.compile(r"\d{1,3}[A-Z]{1,2}\s+-\s+\S.*"
                     r"|\d{1,3}[A-Z]{1,2}\s+(?:Greenbelts?|Detention Pond|Utility ROW|Neighbourhood Park)"
                     r"|Building \d+(?: ?[A-Z])?"
                     r"|Operating House No\.? ?\d+"),
    "cs": re.compile(r"\d+\. zastavení"),
    # A gated estate's numbered section (Guadalajara's "Cluster 12"; candidate 26).
    "es": re.compile(r"[Cc]luster \d+[A-Za-z]?"),
    # "115호 어린이공원", "1호근린공원" (Anyang; the third list, 2026-10-13).
    # "제1호근린공원" (Daegu's read; the sixth pass, 2026-10-13) is the same
    # lot number written in full.
    "ko": re.compile(r"(?:제\s*)?\d+호\s*(?:어린이|근린|소|쌈지)?\s*공원"),
    # The sixth pass (2026-10-13), each from a reader's drops. Osaka's
    # "開発2号公園": the placeholder 開発公園 (a park provided under a
    # development permit, seven rows under the bare word) with its lot number.
    "ja": re.compile(r"開発\s*\d+\s*号\s*公園"),
    # Rio de Janeiro's inclined-lift stops, "Estação 1" to "Estação 5" on
    # three lifts (13 rows); on a station the guard still decides.
    "pt": re.compile(r"[Ee]stação \d+"),
    # Taichung's numbered courts, plazas and zones: "第一中庭", "第六廣場", "第三區".
    "zh": re.compile(r"第[一二三四五六七八九十\d]+(?:中庭|廣場|區)"),
}


def coded_type(name, local):
    """True when `name` is a code beside a type word (CODED_TYPE)."""
    text = unicodedata.normalize("NFKC", name).strip()
    return any(CODED_TYPE[c].fullmatch(text) for c in ("en", *local) if c in CODED_TYPE)


# A REGISTERED CODE IS A NAME (owner, 2026-10-12, on the first measurement of
# CODED_TYPE): a landmark that carries wikidata, wikipedia or a heritage
# registration keeps its coded name, since the register knows it by that
# label. Measured on the 19 built cities: 27 of Seattle's numbered buildings
# (National Register, `ref:nrhp`) and all 14 of Petrin's Stations of the Cross
# (wikidata) stay; none of Surrey's 82 parcels and not Busan's park lot carry
# any of the four. A bare type word is dropped whatever the object carries.
REGISTERED_KEYS = ("wikidata", "wikipedia", "heritage", "ref:nrhp")


def bare_type(name, local, tags=None):
    """True when `name` is only a type word of English or a local language,
    or a code beside one. `tags` is the object's tags: a registered object
    (REGISTERED_KEYS) keeps a coded name."""
    if coded_type(name, local):
        return not (tags and any(tags.get(k) for k in REGISTERED_KEYS))
    # BEHIND AN ARTICLE, OR IN TWO LANGUAGES (candidate 22, owner 2026-10-13):
    # the name is split at a bar, slash or dash with a space either side,
    # one leading article of English or a city's language is set aside from
    # each part (BARE_ARTICLES), and the name is bare when EVERY part is a
    # listed word ("Le Château", "Château - Kasteel"). One part a real name
    # and it stays ("Château - Kasteel van Beersel"). Nothing else is
    # stripped: a name in two scripts with no separator is read whole.
    parts = [x for x in _NAME_SEPARATOR.split(unicodedata.normalize("NFKC", name)) if x.strip()]
    return bool(parts) and all(_bare_word(x, local) for x in parts)


BARE_ARTICLES = {"en": ("the",), "fr": ("le", "la", "les", "l'", "l’"), "nl": ("de", "het"),
                 "es": ("el", "la", "los", "las"), "ca": ("el", "la", "els", "les", "l'", "l’"),
                 "pt": ("o", "a", "os", "as"), "de": ("der", "die", "das")}


def _bare_word(part, local):
    low = part.lower().strip(" .,;:()")
    if _CJK_WORD.search(low):
        low = re.sub(r"[\s#]*\d+$", "", low).strip()
        # A spaced form is the listed word (the sixth pass, 2026-10-13:
        # Daegu's "어린이 공원", "어린이 놀이터", "야외 공연장", "축구 경기장").
        return any(w in BARE_TYPE_NAMES.get(c, ()) for c in ("en", *local) for w in (low, low.replace(" ", "")))
    # Accents set aside for a Latin word: Mexico City's "jardin" and "Area
    # verde" are the listed words unaccented (batch 3, 2026-10-11).
    low = _unaccent(low)
    if any(low in _BARE_FOLDED.get(c, ()) for c in ("en", *local)):
        return True
    for code in ("en", *local):
        for art in BARE_ARTICLES.get(code, ()):
            rest = low[len(art):].lstrip() if low.startswith(art + " ") or (
                art[-1] in "'’" and low.startswith(art)) else None
            if rest and any(rest in _BARE_FOLDED.get(c, ()) for c in ("en", *local)):
                return True
    return False


def _unaccent(s):
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))


_BARE_FOLDED = {c: {_unaccent(w) for w in ws} for c, ws in BARE_TYPE_NAMES.items()
                if c not in ("ja", "ko", "zh")}


# A PLACE OF WORSHIP NAMED ONLY BY ITS DENOMINATION OR HALL TYPE (owner,
# 2026-10-13: "1 shared rule"; the fifth pass). "Kingdom Hall of Jehovah's
# Witnesses", "Methodist Church", "Gurdwara" describe and do not name: 77 such
# rows were confirmed by hand in the 33 wave 1 cities
# (data/_search_rollout/wave1_flag_check), 73 of which this reads. Asked of
# amenity=place_of_worship landmarks only, of the leading name only, never of
# a station, a place or a street. The name is bare when EVERY word of it is a
# listed denomination word or phrase, a hall-type word or a joiner, in
# English or a language of the city, and it holds a denomination and at most
# one hall-type word, or one hall-type word and nothing else. Any other word
# keeps the row: a saint, a place, a street, an ordinal ("First Baptist
# Church" is how that church is known), a word such as "Christ" or "Trinity"
# outside a listed phrase, and a second hall-type word ("Temple Baptist
# Church", London's "Temple Church"). Kept against it: an object with a
# Wikipedia article of its own, and an id in config.PLACE_KEPT.
# Words are listed as _worship_fold folds a name: lower case, Latin accents
# and apostrophes set aside, punctuation read as a space. A phrase is listed
# where one of its words would be too wide alone ("kingdom", "christ",
# "army", "nova vida").
# A CHURCH NAMED ONLY BY ITS CHAIN OR BODY IS THE SAME CLASS (owner,
# 2026-10-13, the sixteen rulings, 2; the sixth pass): Rio de Janeiro's
# "Igreja Universal do Reino de Deus", Osaka's 天理教, 創価学会 and 金光教.
# A BODY (WORSHIP_BODIES) is a denomination whose own name holds a hall-type
# word ("Church of Christ"): only joiners and one hall-type word may follow
# it, so "Church of Christ Presbyterian" keeps its row (owner, the same
# day: a second denomination after a body's name is a distinguishing word).
# A nationality is listed only inside a denomination's name ("Greek
# Orthodox"): "Russian-Ukrainian Seventh Day Adventist Church" keeps its row.
# Measured on the 19 live cities, 2026-10-13, against the fifth pass: 17 more
# rows leave (Sao Paulo 12, Tokyo 4, Mexico City 1) and 8 return, six on
# the body and nationality tests and two on an entry with an article in the
# cache; on the five pilot cities 74 leave (Rio de Janeiro 39 beyond the
# 173 the fifth pass's lists take there, Madrid 13, Osaka 12 beyond 23,
# Amsterdam 10). A language other than English holds only words
# read under a name of this class in a cache (a live city's, a pilot city's,
# or a reader's hand-confirmed rows); measure a new word on every built city
# of its language first.
WORSHIP_DENOMINATIONS = {
    "en": ("methodist", "baptist", "catholic", "anglican", "lutheran", "presbyterian", "pentecostal",
           "evangelical", "orthodox", "apostolic", "adventist", "episcopal", "congregational",
           "congregationalist", "unitarian", "mormon", "quaker", "quakers", "friends", "mennonite",
           "nazarene", "wesleyan", "reformed", "reform", "protestant", "christian", "buddhist", "hindu",
           "sikh", "muslim", "islamic", "jewish", "scientology", "spiritualist", "united", "uniting",
           "roman", "rc", "lds", "greek orthodox", "russian orthodox", "romanian orthodox",
           "ukrainian orthodox", "serbian orthodox", "polish rc",
           "jehovahs witnesses", "salvation army", "latter day saints", "new apostolic",
           "seventh day adventist", "seventh day adventists", "christian science",
           "society of friends", "soka gakkai"),
    "fr": ("catholique", "catholiques", "romaines", "protestant", "protestante", "evangelique",
           "chretienne", "baptiste", "adventiste", "antoiniste", "paroissial", "temoins de jehovah",
           "adventiste du 7e jour"),
    "es": ("evangelica", "cristiana", "adventista", "adventista del septimo dia", "bautista", "budista",
           "mormona", "nueva apostolica", "espanola reformada episcopal", "testigos de jehova",
           "testigos cristianos de jehova"),
    "pt": ("batista", "baptista", "metodista", "adventista", "presbiteriana", "evangelica", "pentecostal",
           "protestante", "catolica", "crista", "universal", "quadrangular", "congregacional",
           "congregacao", "wesleyana", "testemunhas de jeova",
           "congregacao crista no brasil", "congregacao crista do brasil", "universal do reino de deus",
           "assembleia de deus", "adventista do setimo dia", "mundial do poder de deus",
           "evangelho quadrangular", "internacional da graca de deus", "deus e amor",
           "messianica mundial do brasil", "nova vida"),
    "nl": ("jehovahs getuigen", "jehovas getuigen", "apostolisch genootschap", "baptistenkerk",
           "gereformeerde gemeente", "leger des heils", "adventkerk"),
    "cs": ("svedkove jehovovi",),
    "lv": ("jehovas liecinieku",),
    "ko": ("여호와의 증인", "여호와의증인", "하나님의 교회", "하나님의교회", "세계복음선교협회"),
    "ja": ("エホバの証人", "創価学会", "天理教", "天理教会", "幸福の科学", "金光教", "pl教団", "辯天宗"),
    "zh": ("耶和華見證人", "神召會", "淨土宗", "浸禮會", "校園團契", "天理教", "創價學會", "中國佛教會"),
}
WORSHIP_BODIES = {
    "en": ("church of god", "church of christ", "church of jesus christ of latter day saints",
           "church of scientology", "church of england", "church of scotland", "church of the nazarene",
           "united church of canada", "united church of christ"),
    "fr": ("eglise de jesus christ des saints des derniers jours",),
    "es": ("iglesia de jesucristo de los santos de los ultimos dias", "iglesia universal del reino de dios"),
    "pt": ("igreja de jesus cristo dos santos dos ultimos dias",),
    "nl": ("kerk van jezus christus van de heiligen der laatste dagen",),
    "lv": ("pedejo dienu sveto jezus kristus baznica", "latvijas apvienota metodistu baznica"),
    "ja": ("末日聖徒イエス・キリスト教会",),
}
WORSHIP_HALLS = {
    "en": ("church", "chapel", "temple", "mosque", "masjid", "synagogue", "gurdwara", "mandir", "hall",
           "centre", "center", "cathedral", "parish", "citadel", "kingdom hall", "gospel hall",
           "meeting house", "meetinghouse"),
    "fr": ("eglise", "temple", "synagogue", "paroisses", "centre", "salle du royaume", "salles du royaume"),
    "es": ("iglesia", "templo", "capilla", "comunidad", "sinagoga", "salon del reino", "casa de oracion"),
    "pt": ("igreja", "salao do reino", "centro de adoracao"),
    "nl": ("kerk", "koninkrijkszaal"),
    "cs": ("sal kralovstvi",),
    "lv": ("valstibas zale",),
    "ko": ("왕국회관",),
    "ja": ("王国会館", "教会", "分教会"),
}
WORSHIP_JOINERS = {"en": ("of", "the", "and", "for"), "fr": ("de", "des", "du", "la", "le", "les", "et"),
                   "es": ("de", "del", "la", "el", "los", "las", "y"),
                   "pt": ("de", "do", "da", "dos", "das", "e", "a", "o"), "nl": ("van", "de", "der", "des"),
                   "ja": ("の",)}
# A denomination spelt as its mappers spell it, read as its listed phrase
# (wave 1: "Jehova's Witnesses", "Jehovahs Witness", "Jehovah's Wittnesses",
# "Jehovah's Withesses", each on a Kingdom Hall).
WORSHIP_RESPELL = {"en": ((re.compile(r"\bjehovah?s? wit{1,2}[nh]ess(?:es)?\b"), "jehovahs witnesses"),),
                   # Matching faults mended (2026-10-13), no body added: a
                   # listed body spelled out, and a listed hall named short.
                   "ja": ((re.compile(r"パーフェクト\s*リバティー\s*教団"), "pl教団"),),
                   "pt": ((re.compile(r"\bsalao (d[ao]s testemunhas de jeova)\b"), r"salao do reino \1"),)}
_WORSHIP_PATTERNS = {}


def _worship_fold(name):
    low = unicodedata.normalize("NFKC", name).lower()
    if not _CJK_WORD.search(low):
        low = _unaccent(low)
    # A leading elided article is set aside ("L'Église de Jésus-Christ ...";
    # a matching fault mended, 2026-10-13).
    low = re.sub(r"^l['’ʼ`]", "", low)
    low = re.sub(r"['’ʼ`]", "", low)
    return " ".join(re.sub(r"[^\w]+", " ", low, flags=re.UNICODE).replace("_", " ").split())


def worship_only(name, local):
    """True when `name` is only denomination words, hall-type words and
    joiners of English or a local language (WORSHIP_DENOMINATIONS,
    WORSHIP_BODIES, WORSHIP_HALLS): a denomination with one hall-type word
    at most, a body's name with nothing but joiners and one hall-type word
    after it, or one hall-type word alone."""
    codes = tuple(dict.fromkeys(("en", *local)))
    if codes not in _WORSHIP_PATTERNS:
        def words(table):
            return {_worship_fold(w) for c in codes for w in table.get(c, ())}

        def pattern(entries):
            # A CJK or Hangul entry needs no space after it; a Latin one ends
            # at a space or the name's end. Longest first, so a phrase is
            # read whole before its words.
            return "(?:" + "|".join(re.escape(w) + (r"\s*" if _CJK_WORD.search(w) else r"(?:\s+|$)")
                                    for w in sorted(entries, key=lambda w: (-len(w), w))) + ")"
        joiners = words(WORSHIP_JOINERS)
        hall, join = pattern(words(WORSHIP_HALLS)), pattern(joiners)
        rest = pattern(words(WORSHIP_DENOMINATIONS) | joiners)
        _WORSHIP_PATTERNS[codes] = (
            # Denominations and joiners, then one hall-type word among more
            # of them, or a body's name with joiners and one hall-type word.
            re.compile(f"{rest}*(?:{hall}{rest}*|{pattern(words(WORSHIP_BODIES))}{join}*(?:{hall}{join}*)?)?"),
            joiners)
    whole, joiners = _WORSHIP_PATTERNS[codes]
    low = _worship_fold(name)
    for c in codes:
        for spelt, phrase in WORSHIP_RESPELL.get(c, ()):
            low = spelt.sub(phrase, low)
    if not low or all(w in joiners for w in low.split()):
        return False
    # Every parse of `whole` that holds no denomination is a hall-type word
    # among joiners, which is bare too.
    return whole.fullmatch(low) is not None


# A RELIGIOUS OFFICE, AN EDUCATION HALL OR A RESIDENCE TAGGED A PLACE OF
# WORSHIP (owner, 2026-10-13, the sixteen rulings, 1: "dropped; a monastery
# or convent with an article of its own stays"; the sixth pass). Asked of
# amenity=place_of_worship landmarks, of the leading name. A Latin-script
# word is the name's HEAD (WORSHIP_OFFICE_HEADS: "Seminário Arquidiocesano de
# São José") or stands anywhere as a whole word (WORSHIP_OFFICE_WORDS: "Catholic Diocese
# of San Diego", "Pittsburgh Presbytery"); a CJK or Hangul word stands
# anywhere, since the type closes the name ("대구대영교회 교육관"). Kept: an
# article of the object's own, an entry of its own with an article in the
# Wikidata cache, an id in config.PLACE_KEPT.
# A NAMED CONVENT IS A PLACE, NOT AN OFFICE (owner, 2026-10-13, on the sixth
# pass's report): "convento" is no head in Spanish or Portuguese, so Rio de
# Janeiro's "Convento de Santa Teresa" and Madrid's "Convento de Santa
# Catalina de Siena" and "Convento de las Clarisas" keep their rows. The
# bare word "Convento" alone is still a bare type word (BARE_TYPE_NAMES).
# Each word is in a reader's drops under this class. Measured on the 19 live
# cities, 2026-10-13: 21 rows leave (Seoul 15, Busan 4, London 1, Tokyo 1);
# on the five pilot cities 11 (Daegu 10, Rio de Janeiro 1). NOT listed, the evidence being one
# row or none: English "convent" and "seminary", Spanish "hermanas",
# "misioneras" and "oblatas" (an order's name heading a house), Korean
# 참신관 and 대건관 (a hall's own name), "ministries", "foundation" and
# "associates" (each also a congregation's name).
WORSHIP_OFFICE_HEADS = {"pt": ("seminario",)}
WORSHIP_OFFICE_WORDS = {
    "en": ("diocese", "archdiocese", "presbytery", "federation of churches"),
    "ko": ("교육관", "교육원", "비전관", "교구청", "수녀회", "신학대학", "교사실"),
    "ja": ("社務所", "教化部"),
    "zh": ("校牧室",),
}


def worship_office(name, local):
    """True when `name` reads as a religious office, hall or residence
    (WORSHIP_OFFICE_HEADS, WORSHIP_OFFICE_WORDS) in English or a local
    language."""
    low = _worship_fold(name)
    codes = tuple(dict.fromkeys(("en", *local)))
    if any(low == h or low.startswith(h + " ") for c in codes for h in WORSHIP_OFFICE_HEADS.get(c, ())):
        return True
    # A Latin-script word is not read in a name that holds CJK or Hangul: Hong
    # Kong's "天主教香港教區基督之母堂 Catholic Diocese of Hong Kong Mother of
    # Christ Church" is a church, its diocese named in passing.
    mixed = bool(_CJK_WORD.search(low))
    for c in codes:
        for w in WORSHIP_OFFICE_WORDS.get(c, ()):
            if w in low if _CJK_WORD.search(w) else not mixed and re.search(rf"\b{re.escape(w)}\b", low):
                return True
    return False


# A FACILITY OF AN APARTMENT ESTATE OR A MALL TAGGED A PARK OR A SQUARE
# (owner, 2026-10-13, the sixteen rulings, 7: "dropped, by a rule where a tag
# or an estate's brand name shows it"; the sixth pass). Asked of leisure=park,
# leisure=playground and place=square, on three signs:
#   * the operator names a condominium, a residents' body, an estate's
#     management or a mall (ESTATE_FACILITY_OPERATOR: Rio de Janeiro's
#     operator=condominio and "NorteShopping", Guadalajara's "La Bella
#     Residencial", Taoyuan's 社區管理委員會);
#   * the operator's own name heads the object's name and a facility word
#     closes it (Daegu's "보성은하타운 주민 운동장", operator 보성은하타운).
#     Without the facility word the sign is not read: a city that runs
#     "Riverside Park" can be named Riverside, and Guadalajara's "Parque
#     Belcanto" (operator Belcanto) stays a by-id drop;
#   * the name is an estate's brand and a facility word (ESTATE_BRANDS,
#     ESTATE_FACILITY_ENDS, per language: Daegu's "삼산타운어린이놀이터",
#     "신천자이 놀이터"), or says the thing lies inside a complex (Osaka's
#     "セントプレイスシティー内の広場", Daegu's "... 내 공원").
# A park tied to an estate only by a name ending in the park word stays
# (Daegu's "신암그린타운공원": a reader could not tell it from a public park).
# NOT built: a square inside a mall or a zoo known only by its coordinates
# (Osaka's ATC and Hankyu plazas, Tennoji Zoo's exhibit plazas), which the
# cache cannot place; listed in the decisions draft. access=residents is not
# read: no reader's row carries it. Measured on the 19 live cities,
# 2026-10-13: none leaves; on the five pilot cities 15 (Daegu 11, Rio de
# Janeiro 3, Osaka 1), 14 of them a reader's drop.
ESTATE_FACILITY_OPERATOR = re.compile(
    r"condom[ií]nio|condominium|residencial|fraccionamiento|associa[cç][aã]o de moradores|residents'? association"
    r"|homes association|homeowners|shopping|outlet|\bmall\b|管理委員會|管理組合", re.I)
ESTATE_BRANDS = {"ko": re.compile(r"아파트|타운|자이|아이위시|리슈빌|네오빌|\d차")}
ESTATE_FACILITY_ENDS = {"ko": ("놀이터", "체육시설", "운동장", "산책로", "다목적구장", "광장", "내 공원"),
                        "ja": ("内の広場",)}
# A facility word that needs no brand before it: it says "inside".
ESTATE_INSIDE_ENDS = ("내 공원", "内の広場")
ESTATE_FACILITY_KEYS = (("leisure", "park"), ("leisure", "playground"), ("place", "square"))


def estate_facility(tags, names, local):
    """The sign that a park, a playground or a square is an estate's or a
    mall's own facility, else None."""
    if not names or not any(tags.get(k) == v for k, v in ESTATE_FACILITY_KEYS):
        return None
    operator = (tags.get("operator") or "").strip()
    if ESTATE_FACILITY_OPERATOR.search(operator):
        return f"operator={operator}"
    name = unicodedata.normalize("NFKC", names[0]).strip()
    head = unicodedata.normalize("NFKC", operator)
    led = len(head) >= 3 and name.lower().startswith(head.lower()) and len(name) > len(head)
    for c in local:
        for end in ESTATE_FACILITY_ENDS.get(c, ()):
            if name.endswith(end) and len(name) > len(end):
                if end in ESTATE_INSIDE_ENDS:
                    return f"the name ends {end!r}"
                if led:
                    return f"operator={operator} heads the name, before {end!r}"
                if c in ESTATE_BRANDS and ESTATE_BRANDS[c].search(name[:-len(end)]):
                    return f"an estate's brand and {end!r}"
    return None


# A PARK NAMED AS A SQUARE THAT REPEATS A STREET ROW IS ONE ROW (owner,
# 2026-10-13, the sixteen rulings, 9: "one row, by extending the square and
# street merge to parks"; the sixth pass). A leisure=park whose name leads
# with a square word (SQUARE_HEADS, per language) is that square's garden:
# where a STREET row within SQUARE_DUP_M bears the name, the street row
# stands for both. Never against another park or square: same-named parks
# more than 300 m apart are two rows (ruling 12).
# Square words only. A park under a street word ("Avenida de Brasil", five of
# the 50 rows Madrid's reader listed) or a garden word (Barcelona's "Jardins
# de ...", 19 parks beside pedestrian ways of their name) keeps its row: the
# park is the thing there and the way is its path.
# Measured 2026-10-13: Madrid 52 (its reader listed 50); Rio de Janeiro 244;
# on the 19 live cities 1,120, of which Sao Paulo 1,045 ("Praça ..." parks
# beside the street of the square), Barcelona 39, Mexico City 15, Montreal
# 13, Paris 6. French "square" is NOT a head: a Paris square is a garden.
# The Portuguese count is far above what the ruling was shown and is
# flagged for the owner in the decisions draft.
SQUARE_HEADS = {"es": ("plaza", "plazuela", "plazoleta", "glorieta"), "pt": ("praça", "largo"),
                "ca": ("plaça", "placeta"), "fr": ("place",), "it": ("piazza", "piazzale", "largo")}


def square_led(name, local):
    """True when `name` leads with a square word of a local language
    (SQUARE_HEADS) and holds more than that word."""
    words = _unaccent(unicodedata.normalize("NFKC", name).lower()).split()
    return len(words) > 1 and any(words[0] == _unaccent(w) for c in local for w in SQUARE_HEADS.get(c, ()))
# A numbered block of a housing estate, mapped as a place: Mexico City's
# "Grupo 12", "Manzana 82" (batch 3, 2026-10-11). The whole name, places only.
NUMBERED_BLOCK = {"es": re.compile(r"(grupo|manzana|edificio)\s+\w{1,4}", re.I),
                  "pt": re.compile(r"(bloco|quadra|edifício|edificio)\s+\w{1,4}", re.I)}
# A HOUSING ESTATE NAMED AS ONE (owner, 2026-10-11: "yes, state reasoning ...
# for lack of wikidata"): London maps its council estates as place nodes, so
# the residential-area test cannot see them; 53 places were named "X Estate",
# 11 with wikidata. An estate with a wikidata item or an article is a known
# district of the city (Aylesbury, White City, Pullens) and stays; one with
# neither is people's homes under the landlord's name for them, with nothing
# public to say it is used as a district's name, and goes. The lack of
# wikidata is the whole reason: no estate was judged one by one.
ESTATE_NAME = {"en": re.compile(r"\bestate$", re.I)}
# A HAMLET UNDER THE FLOOR (owner, 2026-10-11, a site-wide rule: "population
# floor: 50 or higher"): Mexico City's census import maps 609 localities as
# place=hamlet, 91 of them with ten people or fewer and some under a family's
# name ("Los Aguilar", "Rancho Tres Hermanos"): one household, a home. A
# hamlet whose OSM population tag is under the floor goes unless notable. One
# with no population tag stays: nothing says how small it is (Hong Kong's
# villages carry none).
HAMLET_MIN_POPULATION = 50


def _population(tags):
    digits = re.sub(r"[\s,.]", "", str(tags.get("population") or ""))
    return int(digits) if digits.isdigit() else None


# A family's grave: Paris's cemeteries are mapped tomb by tomb, each with a
# wikidata item for the TOMB, and 13 are "Famille Dumur" and the like, private
# families' names. A tomb so named is never indexed (batch 3, 2026-10-11).
FAMILY_TOMB = re.compile(r"(famille|familles|familia|família|family)\b", re.I)


# A NAME IN A THIRD SCRIPT (owner, 2026-10-11, on the hard line against
# glitched names live): Seoul's Bukchon Hanok Village carried the `name`
# "북촌한옥마을 ДЕРЕВНЯ". Where `name` holds a run of two or more letters in a
# script that is neither Latin nor one of the city's own, and the object has
# a name in a local language (else in English, where no local language has a
# script of its own), that name leads and `name` is not read. Without one
# the object is untouched (a review by eye, then
# config.PLACE_DROPPED): a rule cannot tell a glitch from a second language.
# Runs of two: Vancouver's hən̓q̓əmin̓əm̓ street names use single Greek and
# Cyrillic letters inside Latin words, and are names.
_SCRIPT_RANGES = {
    "greek": ((0x0370, 0x03FF),), "cyrillic": ((0x0400, 0x04FF),), "armenian": ((0x0530, 0x058F),),
    "hebrew": ((0x0590, 0x05FF),), "arabic": ((0x0600, 0x06FF),), "devanagari": ((0x0900, 0x097F),),
    "gurmukhi": ((0x0A00, 0x0A7F),), "thai": ((0x0E00, 0x0E7F),), "georgian": ((0x10A0, 0x10FF),),
    "hangul": ((0xAC00, 0xD7AF), (0x1100, 0x11FF)), "kana": ((0x3040, 0x30FF),),
    "han": ((0x3400, 0x4DBF), (0x4E00, 0x9FFF)),
}
# Han in a Korean name is hanja (Seoul's "서십자각 터 西十字閣址"), its own.
_OWN_SCRIPTS = {"ja": ("kana", "han"), "zh": ("han",), "ko": ("hangul", "han"), "ka": ("georgian",),
                "el": ("greek",), "ru": ("cyrillic",)}


# What sits between the two halves of a bilingual name: a bar, a slash or a
# dash with a space either side.
_NAME_SEPARATOR = re.compile(r"\s+[|/\-\u2013\u2014]\s+")


def _third_script(name, local):
    own = {s for c in local for s in _OWN_SCRIPTS.get(c, ())}
    for script, pairs in _SCRIPT_RANGES.items():
        if script in own:
            continue
        cls = "[" + "".join(chr(a) + "-" + chr(b) for a, b in pairs) + "]"
        if re.search(cls + "{2}", name):
            return True
    return False


def _local_first(tags, names, local):
    """`names` with the local-language name leading, and `name` gone, when
    `name` carries a third script (above); else `names` unchanged."""
    name = (tags.get("name") or "").strip()
    if not names or names[0] != name or not _third_script(name, local):
        return names
    # THE SAME NAME IN TWO LANGUAGES is no glitch (owner, 2026-10-11: "exempt
    # separator that states the same thing in two languages"): New
    # Westminster's "Sukh Sagar Park | ਸੁਖ ਸਾਗਰ ਪਾਰਕ" is its name:en and its
    # name:pa either side of a separator. Only where EVERY part is one of the
    # object's own name:<language> values: a separator alone proves nothing,
    # since a stray word can sit behind one too.
    parts = [p.strip() for p in _NAME_SEPARATOR.split(name)]
    own = {(v or "").strip() for k, v in tags.items() if k.startswith("name:")}
    if len(parts) > 1 and all(p and p in own for p in parts):
        return names
    for code in (*local, *(() if any(c in _OWN_SCRIPTS for c in local) else ("en",))):
        lead = (tags.get(f"name:{code}") or "").strip()
        if lead and lead != name and lead in names and not _third_script(lead, local):
            return [lead] + [n for n in names if n not in (lead, name)]
    return names


# EXHIBITS (owner, 2026-10-11: "drops okay"): a museum yard's hardware is
# mapped piece by piece, about 80 landmarks at Seoul's War Memorial and 24 at
# Kyoto's railway museum. A historic=* of these values is kept only with its
# own wikidata item. For the mass-produced ones a tourism tag is asked as
# well: all 28 of Seoul's that carried wikidata carried the MODEL's (M47
# Patton, Scud), where Hong Kong's Noonday Gun and Vancouver's Nine O'Clock
# Gun carry tourism=attraction. Ships, wrecks and historic railways are
# individual things or places and are not in the rule. The cost: a lone tank
# standing as a memorial with no wikidata goes (Marseille's char Jeanne-d'Arc).
EXHIBIT_HISTORIC = {"aircraft", "tank", "cannon", "missile", "rocket", "vehicle",
                    "locomotive", "railway_car"}
MODEL_EXHIBITS = {"aircraft", "tank", "cannon", "missile", "rocket", "vehicle"}
# EXHIBITS UNDER THEIR CLASS'S OR KIND'S ARTICLE (the third list,
# 2026-10-13): Anyang's railway museum yard carried eight ("Mika-type steam
# locomotive"). Three tests: an entry another object of the cache carries is
# the class's (build()'s own_item, any EXHIBIT_HISTORIC value); a locomotive
# or railway car needs a tourism tag or an article under its own name
# (RAIL_EXHIBITS, _titled_by_name: Chicago's Pioneer Zephyr and Vancouver's
# Canadian Pacific 374 stay on theirs); a vehicle with no historic tag
# (locomotive:type on a tourism=attraction) likewise needs that article.
RAIL_EXHIBITS = {"locomotive", "railway_car"}


def _titled_by_name(tags):
    title = fold_name(article_title(tags.get("wikipedia") or ""))
    return bool(title) and title == fold_name(tags.get("name") or "")
STOLPERSTEIN_MEMORIALS = {"stolperstein", "stolperschwelle"}


def _exhibit(tags):
    # A painting hung INDOORS is an exhibit whatever its wikidata: the Museu
    # Paulista's 73 canvases are mapped one by one as artworks (Sao Paulo,
    # batch 3, 2026-10-11), as are three of Washington's state art collection
    # in Seattle. Indoors only: Prague's Lennon Wall is artwork_type=painting
    # too, on a street, and the unscoped test took it.
    if (tags.get("tourism") == "artwork" and tags.get("artwork_type") == "painting"
            and (tags.get("indoor") == "yes" or tags.get("location") == "indoor")):
        return True
    h = tags.get("historic")
    if not h and tags.get("locomotive:type") and not tags.get("railway"):
        return not _titled_by_name(tags)
    if h not in EXHIBIT_HISTORIC:
        return False
    return not (tags.get("wikidata") and (h not in MODEL_EXHIBITS or tags.get("tourism")))


def _names(tags, name_tags):
    seen, out = set(), []
    for k in name_tags:
        for v in (tags.get(k) or "").split(";"):
            v = v.strip()
            if v and v not in seen and not junk_name(v):
                seen.add(v)
                out.append(v)
    return out


def _named_street(name, local):
    """True for a street name to keep: no business or home word in it, or a
    business word in a name that still reads as a street, a way word first or
    last ("Clinic Road", "Car Park Road" and "Hostel Hill Path" in Hong Kong,
    Brussels' Rue du Magasin and Rue de l'Hôtel des Monnaies, Barcelona's
    Carrer de l'Hostal d'en Sol, Montréal's Avenue De l'Hotel-de-Ville; batch
    2b, 2026-10-08, measured on every built index). A home or private word
    never passes (Seattle's "Private Road"), nor a lowercase description
    (Vancouver's "to parking garage below plaza")."""
    word = leak_word([name], local)
    if word is None:
        return True
    if word in {w for c in ("en", *local) for w in HOME_WORDS.get(c, ())} or name[:1].islower():
        return False
    # Less the business word itself, whose phrase may hold a way word (a
    # food court, a McDrive).
    low = unicodedata.normalize("NFKC", name).lower().strip().replace(word, " ")
    ws = re.findall(r"\w+", low)
    if not ws:
        return False
    # The way word in the name's own position: last in English and Chinese
    # ("Clinic Road", 保健路), first where the street word leads (Rue du
    # Magasin, Carrer de l'Hostal), a whole word in Korean. A Korean ending
    # alone is too loose: 상가진입로 (a shopping arcade's entry road) ends
    # in 로; English "Road to 113/114 Parking Lot" leads with it (batch 2b
    # audit, 2026-10-08).
    for code in dict.fromkeys(["en", *local]):
        for w in WAY_WORDS.get(code, ()):
            if code in SUFFIX_WAY_LANGUAGES:
                # A glued name passes on its ending in a Latin-script suffix
                # language ("Hotelstraße", "Store Kongensgade"; candidate 33,
                # 2026-10-13). Korean keeps the whole word (상가진입로).
                if ws[-1] == w or (code in GLUED_STREET_LANGUAGES and ws[-1].endswith(w)):
                    return True
            elif _CJK_WORD.search(w):
                if low.endswith(w):
                    return True
            elif ws[-1] == w or (code in WAY_WORD_LEADS and ws[0] == w):
                return True
    return False


# Languages whose street word leads the name (_named_street).
WAY_WORD_LEADS = {"fr", "ca", "es", "cs", "pt", "ro", "it"}


def _reads_as_way(names, local, extra=()):
    """True when a name reads as a way in English or a local language: a CJK
    way word anywhere in it (三条小橋), a Latin one as a whole word, or, in a
    language that compounds (SUFFIX_WAY_LANGUAGES), as a word's ending
    ("Nieuwstraat"). `extra`: one city's own way words
    (config.PLACE_WAY_WORDS), whole words as a Latin one is."""
    if any(_has_word(w.lower(), n.lower()) for w in extra for n in names):
        return True
    for code in dict.fromkeys(["en", *local]):
        lead, ending = WAY_LEAD.get(code, ()), WAY_ENDING.get(code, ())
        for n in names:
            ws = re.findall(r"\w+", unicodedata.normalize("NFKC", n).lower())
            while len(ws) > 1 and ws[-1] in ROMAN:
                ws.pop()
            if ws and ((len(ws) > 1 and ws[0] in lead) or (ending and ws[-1].endswith(ending))):
                return True
        for word in WAY_WORDS.get(code, ()):
            for n in names:
                low = n.lower()
                if code in SUFFIX_WAY_LANGUAGES:
                    if any(t.endswith(word) for t in re.findall(r"\w+", low)):
                        return True
                elif _has_word(word, low):
                    return True
    return False


# ---------------------------------------------------------------------------
# THE RULINGS OF 2026-10-13 (owner; DECISIONS.md, "Place search: the owner's
# rulings on keep against drop, personal names, private streets and the typo
# line"). Every figure below was measured on the 19 built cities, on the
# caches of 2026-10-07 to 2026-10-11; re-measure a figure before relying on
# it for a new city. docs/place_search_exclusions.md lists every class.
# ---------------------------------------------------------------------------


def fold_name(s):
    """A name with case, accents, spaces and punctuation set aside: the key
    two rows of one thing share ("St. Mary's" and "St Marys")."""
    s = unicodedata.normalize("NFKD", unicodedata.normalize("NFKC", s).casefold())
    return "".join(ch for ch in s if ch.isalnum())


# THE FAME TEST (owner, 2026-10-13: "famous landmark rule takes priority over
# others"): a `wikipedia` tag of the object's OWN. Not its own, read from the
# tags alone: an article named twice or by a section ("#"), one the object
# shares with its subject, brand or operator, and one another object in the
# cache carries too (Paris's 69 metro entrances all tagged "Édicule Guimard",
# a presbytery tagged with its church's article). Two objects of one folded
# name within SAME_THING_M are one thing drawn twice and share nothing; the
# ways of one street share nothing whatever their distance.
SAME_THING_M = 300
_SUBJECT_KEYS = ("subject", "buried", "name:etymology", "brand", "operator")
# For candidate 38 the subject key alone: measured on the 19, an entry equal
# to operator:wikidata or name:etymology:wikidata sat on the thing itself
# (Roehampton University, Barcelona's Teatre Grec), which stays.
SUBJECT_ENTRY_KEYS = ("subject",)
# Words that say an article is about a grave, a plaque or a monument and not
# about the person it names ("Tomb of Karl Marx", "Tombe d'Oscar Wilde",
# "Monument funéraire de ..."). In the article's language, which is often not
# the city's, so one list. A whole word, or anywhere in a Han or kana title.
OBJECT_WORDS = (
    "tomb", "tombs", "grave", "gravesite", "mausoleum", "memorial", "monument", "cenotaph", "crypt",
    "plaque", "statue", "sepulchre", "tombstone", "headstone",
    "tombe", "tombeau", "sépulture", "mémorial", "mausolée", "crypte", "stèle", "cénotaphe", "caveau",
    "tumba", "sepulcro", "mausoleo", "monumento", "placa", "estatua", "estàtua", "estátua", "túmulo",
    "jazigo", "mausoléu", "làpida",
    "hrob", "hrobka", "pomník", "památník", "pamětní", "socha", "mauzoleum", "náhrobek",
    "graf", "grafmonument", "gedenkteken", "gedenkplaat", "standbeeld", "grab", "grabmal", "denkmal",
    "მემორიალი", "ძეგლი", "საფლავი", "памятник", "мемориал", "мемарыяльная", "могила",
    "墓", "陵", "塚", "古墳", "碑", "像")
# Korean, as a title's ending only: 능 and 비 sit inside common words.
OBJECT_ENDINGS = ("묘", "릉", "능", "묘역", "묘소", "기념비", "동상", "비석")


def article_title(value):
    """The title of a `wikipedia` tag's article: the language prefix, a
    trailing disambiguation in brackets and underscores set aside."""
    title = re.sub(r"^[A-Za-z][A-Za-z\-]{1,11}:", "", value.strip()).replace("_", " ").strip()
    return re.sub(r"\s*\([^()]*\)$", "", title).strip()


def _object_title(title):
    low = title.lower()
    return any(_has_word(w, low) for w in OBJECT_WORDS) or low.endswith(OBJECT_ENDINGS)


def grave_or_plaque(tags):
    """"grave", "plaque" or None (the test the 2026-10-13 measure used)."""
    if tags.get("cemetery") == "grave" or tags.get("historic") == "tomb" or tags.get("tomb"):
        return "grave"
    if tags.get("memorial") in ("plaque", "blue_plaque"):
        return "plaque"
    return None


def _memorial(tags):
    return bool(tags.get("historic") == "memorial" or tags.get("memorial")
                or (tags.get("tourism") == "artwork" and tags.get("artwork_type") in ("statue", "bust")))


def own_article(tags, names, shared=False):
    """("own" | "not" | "undecided" | "none", why) for an object's `wikipedia`
    tag. `shared`: another object in the cache carries the same article.
    "undecided" is a verdict: the tags cannot tell, and the caller leaves the
    row as it was (never a guess). A grave or a plaque is named for its
    subject, so an article under the row's own name is the subject's unless
    the title says tomb, plaque or monument; any other memorial under its own
    name could be either."""
    wp = (tags.get("wikipedia") or "").strip()
    if not wp:
        return "none", ""
    if ";" in wp:
        return "not", "several articles in one tag"
    if "#" in wp:
        return "not", "a section of another article"
    wd = (tags.get("wikidata") or "").strip()
    for key in _SUBJECT_KEYS:
        if (tags.get(f"{key}:wikipedia") or "").strip() == wp:
            return "not", f"the article is its {key}'s ({key}:wikipedia)"
        if wd and wd in [v.strip() for v in (tags.get(f"{key}:wikidata") or "").split(";")]:
            return "not", f"the item is its {key}'s ({key}:wikidata)"
    if shared:
        return "not", "the article is shared with another object"
    title = article_title(wp)
    person = grave_or_plaque(tags)
    if person or _memorial(tags):
        if _object_title(title):
            return "own", "the title names the object"
        if person and fold_name(title) in {fold_name(n) for n in names}:
            return "not", "the article bears the row's name, its subject's"
        return "undecided", "a memorial's article that could be its subject's"
    return "own", ""


# A PLACE OR LANDMARK THAT IS NOT THERE (owner, 2026-10-13: "the search must
# not land where the thing is not"): demolished, razed, removed, abandoned or
# not yet open by its own tags, article or not. Read narrowly, since a
# lifecycle prefix sits on one feature of an object and not on the object:
#   * a plain flag (demolished=yes, abandoned=yes, construction=yes) is the
#     object's own;
#   * a prefixed key (demolished:building=church) counts only where the
#     object has no live amenity, tourism, leisure, natural or man_made key:
#     London's St John Zachary is a garden today on the site of a demolished
#     church, and stays;
#   * the same feature live and prefixed alike (leisure=park beside
#     construction:leisure=park, eight Hong Kong parks) says both: the row
#     stays and is listed, never a guess;
#   * on a place, a demolished or abandoned prefix on the place key itself
#     (Hong Kong's former villages, place=locality with abandoned:place=
#     village or demolished:place=hamlet). A proposed or construction prefix
#     there never drops a place: a locality proposed to become a quarter is
#     there today;
#   * an ABANDONED landmark with a historic tag is a historic site and is
#     there; a NOT-YET-OPEN one that is historic, listed or has a start date
#     behind it is being rebuilt (build()'s landmark()).
# NOT read: disused (a disused fountain stands), was: (a former use) and
# end_date on anything but a station. The 2026-10-13 measure counted 266
# rows with a wider test (any of these prefixes on any feature key, disused
# and end_date included); the narrow reading and its count are in
# docs/decisions_drafts/search-rules.md, flagged for the owner.
LIFE_GONE = ("razed", "demolished", "removed", "destroyed")
LIFE_AHEAD = ("proposed", "construction", "planned")
LIFE_FEATURES = ("railway", "building", "amenity", "tourism", "historic", "leisure", "shop", "man_made",
                 "highway", "public_transport", "place", "natural", "landuse",
                 # demolished:waterway=canal (Buffalo's Enlarged Erie Canal; the
                 # second batch, 2026-10-13).
                 "waterway")
LIFE_LIVE_KEYS = ("amenity", "tourism", "leisure", "natural", "man_made")


def _future(value, retrieved):
    """True for a date tag later than the cache (`retrieved`, ISO)."""
    v = str(value or "").strip()
    return bool(re.match(r"\d{4}", v)) and v[:10] > retrieved and not retrieved.startswith(v)


def _past(value, retrieved):
    # Stray characters before the year are set aside ("=1959", "~1959"; the
    # second batch, 2026-10-13): the date is still a date.
    v = str(value or "").strip().lstrip("=~<> ")
    return bool(re.match(r"(1[5-9]|20)\d{2}", v)) and v[:10] < retrieved and not retrieved.startswith(v)


def lifecycle(tags, retrieved, place=False):
    """("gone" | "abandoned" | "ahead" | "both", the deciding tag) for a place
    or a landmark its own tags say is not there, else None."""
    classes = (("gone", LIFE_GONE), ("abandoned", ("abandoned",)), ("ahead", LIFE_AHEAD))
    for cls, prefixes in classes:
        for p in prefixes:
            if tags.get(p) == "yes":
                return cls, f"{p}=yes"
    # READ AS GONE (the second batch, 2026-10-13): a derelict canal (10 named
    # ways in the 52 caches, Manchester 8) and a place of worship tagged
    # disused=yes (3: Washington 2, Montreal 1). disused=yes on anything else
    # is still not read: a disused fountain stands.
    if not place and tags.get("waterway") == "derelict_canal":
        return "gone", "waterway=derelict_canal"
    if not place and tags.get("disused") == "yes" and tags.get("amenity") == "place_of_worship":
        return "gone", "disused=yes on a place of worship"
    if place:
        for cls, prefixes in classes:
            for p in prefixes:
                v = tags.get(f"{p}:place")
                if v and v == tags.get("place"):
                    return "both", f"{p}:place={v}"
                if v and cls != "ahead":
                    return cls, f"{p}:place={v}"
        return None
    for k in ("railway", "building", "highway"):
        v = tags.get(k)
        if v in ("razed", "abandoned") or v in LIFE_AHEAD:
            return ("gone" if v == "razed" else "abandoned" if v == "abandoned" else "ahead"), f"{k}={v}"
    for cls, prefixes in classes:
        keys = sorted(k for k in tags if k.partition(":")[0] in prefixes
                      and k.partition(":")[2] in LIFE_FEATURES)
        if not keys:
            continue
        # The same feature live and prefixed (leisure=park beside
        # construction:leisure=park, eight Hong Kong parks) says both: "both"
        # is a verdict the caller keeps and lists, never a guess.
        both = [k for k in keys if tags.get(k.partition(":")[2]) == tags[k]]
        if both:
            return "both", f"{both[0]}={tags[both[0]]}"
        if not any(tags.get(k) for k in LIFE_LIVE_KEYS):
            return cls, f"{keys[0]}={tags[keys[0]]}"
    if _future(tags.get("opening_date"), retrieved):
        return "ahead", f"opening_date={tags['opening_date']}"
    return None


# A STATION THAT IS NO STATION TO SEARCH (owner, 2026-10-13).
# Not yet open: opening_date after the cache, beside the lifecycle tags read
# since 2026-10-08, and on any station or stop, not only public_transport=
# station (a Birmingham tram stop carries construction=yes on railway=
# tram_stop; wave 1, 2026-10-13). Closed: end_date before the cache, a
# disused, abandoned, razed or demolished prefix on railway or
# public_transport, disused=yes or abandoned=yes (2 rows on the 19).
STATION_CLOSED_PREFIXES = ("disused", "abandoned", "razed", "demolished")
# A STATION CLOSED TO THE PUBLIC GETS NO ROW (owner, 2026-10-13: "3 shared
# rule"; the fifth pass): access=private on a station object. Washington's
# Capitol subway (Hart, Rayburn, Dirksen, Russell and two "U.S. Capitol": 6
# objects in wave 1). On the 19 live cities it takes 2 rows, both in Tokyo:
# 大田 and 志茂田, the practice stations of a railway's training centre
# (usage=training). NARROWED from the ruling's "private or no": access=no is
# NOT read. The one station row that carries it on the 19 is a public
# national-rail halt (Marseille's Sainte-Marthe-en-Provence, access=no on its
# building node); the four other objects so tagged, private or no, are bus
# stations and depots that were no rows already. A station the map draws is
# never dropped by this (the station guard). Re-measure before adding a value.
STATION_PRIVATE_ACCESS = ("private",)
# STATION LEAKS THE PILOT READS FOUND (faults mended without a ruling, the
# sixth pass, 2026-10-13; data/_search_rollout/pilot_reads). Each passed
# because no tag the station tests read said what it was:
#   * operational_status=closed (Madrid's "Estación de Darío Gazapo", a
#     subway station with no network and no end date);
#   * a freight station known only by its name (Madrid's "Estación de
#     Mercancías Madrid - Abroñigal", railway=station with no passenger tag):
#     STATION_FREIGHT_WORDS, a whole word of the name, per language, Spanish
#     only since no other reader found one;
#   * a station entrance or a ticket gate tagged public_transport=station
#     (STATION_ENTRANCES: Madrid's "Vinateros" entrance 208 m from the
#     station's own row, Osaka's 東改札口 and 西改札口): no row where a
#     station row of its name stands within OUTLINE_SAME_M, and no row at all
#     unless the map draws its name (the merges);
#   * a bus rapid transit station with no railway tag, kept as a lone station
#     object on its network tag (Rio de Janeiro's "Ibiapina" and "Penha 2",
#     network=BRT): BUS_NETWORK names the networks that are no rail sign.
# A station the map draws is never dropped by any of these (the station
# guard). NOT built: Amsterdam's "Oranje Nassaulaan", a stop its description
# tag calls a diversion stop. The city's map draws it (its operator's own feed
# lists it), so the guard keeps it whatever a rule said.
# Measured on the 19 live cities, 2026-10-13: 3 rows leave, all entrances in
# Tokyo (北口, 日暮里駅 南改札口, 熊野前駅出入口); on the five pilot cities 7.
STATION_FREIGHT_WORDS = {"es": ("mercancías",)}
# Faults the full reads found (2026-10-13). A Japanese station name that
# ENDS in a freight word (川崎貨物, 福岡貨物ターミナル, 吹田貨物ターミナル), a
# station whose operator is a freight railway and nothing else (the whole
# operator tag: a passenger station shared with one lists both), and a
# station name ending 跡地, a former site. 跡地 is read on stations only: on
# a landmark it names a historic site's marker.
STATION_FREIGHT_ENDS = {"ja": ("貨物", "貨物ターミナル", "貨物駅")}
STATION_FREIGHT_OPERATORS = frozenset(("jr貨物", "日本貨物鉄道", "神奈川臨海鉄道", "ftl"))
STATION_FORMER_ENDS = {"ja": ("跡地",)}
STATION_ENTRANCES = {"subway_entrance", "train_station_entrance"}
BUS_NETWORK = re.compile(r"\bBRT\b|\bbus\b|autob[uú]s|[oô]nibus", re.I)


def station_out_of_service(tags, names, local):
    """The sign that a station carries no passengers in normal service
    (operational_status=closed, a freight word in its name), else None."""
    if tags.get("operational_status") == "closed":
        return "operational_status=closed"
    low = _unaccent(unicodedata.normalize("NFKC", names[0]).lower()) if names else ""
    for c in local:
        for w in STATION_FREIGHT_WORDS.get(c, ()):
            if re.search(rf"\b{re.escape(_unaccent(w))}\b", low):
                return f"a freight station by its name ({w})"
        for w in STATION_FREIGHT_ENDS.get(c, ()):
            if low.endswith(w) and len(low) > len(w):
                return f"a freight station by its name ({w})"
        for w in STATION_FORMER_ENDS.get(c, ()):
            if low.endswith(w) and len(low) > len(w):
                return f"a former site by its name ({w})"
    if unicodedata.normalize("NFKC", str(tags.get("operator") or "")).strip().lower() in STATION_FREIGHT_OPERATORS:
        return f"a freight railway's station (operator={tags['operator']})"
    return None


def station_closed(tags, retrieved):
    """The tag that says a station has closed, else None."""
    for p in STATION_CLOSED_PREFIXES:
        for k in ("railway", "public_transport"):
            if tags.get(f"{p}:{k}"):
                return f"{p}:{k}={tags[f'{p}:{k}']}"
    for k in ("disused", "abandoned"):
        if tags.get(k) == "yes":
            return f"{k}=yes"
    if _past(tags.get("end_date"), retrieved):
        return f"end_date={tags['end_date']}"
    return None


# A STATION THE MAP DRAWS IS NOT CLOSED BY A DISUSED TAG (the station guard,
# 2026-10-13; found in Toronto, wave 1). Seven Eglinton line stations the
# map draws carry disused:public_transport=station in OpenStreetMap and had
# no station row; the name guard of the three tests below misses them (the
# map says "Avenue Station", OSM "Avenue"). Spared: a station within
# STATION_DRAWN_M of a map station whose name is its own or begins it (or
# the reverse), names folded. Position alone is not enough and neither is
# the name. Measured on the caches of 237 cities, closed-tagged stations
# within 500 m of a map station: 20. The test spares 11 (Toronto's 7 at 7
# to 50 m; Riga's 4 tram stops at 1 to 50 m) and leaves 9: under another
# name Grenoble's abandoned tramway stop at 56 m and Hong Kong's stop of
# 2002 at 46 m; too far Rio de Janeiro's Olaria bus station at 179 m and
# Edmonton's old NAIT at 251 m. A dated closure (end_date before the cache)
# is never spared, whatever else the object carries: Rio de Janeiro's
# Bonsucesso, the map station's own name at 66 m, closed in 2016, and
# Minneapolis's Target Field commuter platform at 52 m, closed in 2026.
# Re-measure
# (data/_search_rollout/live_rules56/disused_map_stations.tsv) if the
# distance or the name test changes.
STATION_DRAWN_M = 100


def drawn_station_here(names, pt, drawn_at):
    """True when a station the map draws (`drawn_at`: [(folded name, lat,
    lon)]) lies within STATION_DRAWN_M of `pt` and one of `names`, folded,
    is its name, begins it or is begun by it."""
    own = [f for f in (fold_name(n) for n in names) if f]
    for name, lat, lon in drawn_at:
        if name and _dist_m(pt, (lat, lon)) <= STATION_DRAWN_M \
                and any(name.startswith(f) or f.startswith(name) for f in own):
            return True
    return False


def station_ride(tags):
    """The tag that says a station is a ride's and not a transit stop: a
    tourist or miniature railway inside a park or a museum (14 rows on the
    19: London's miniature railways, Ocean Park's train in Hong Kong).
    usage=tourism is the cleanest of them (wave 1, 2026-10-13; 11 of the 14).
    tourism=attraction ALONE is no sign: Hong Kong's Peak Tram termini and
    Sao Paulo's Estação da Luz carry it. An operator's or network's name is
    not read either (a heritage line can be a city's transit)."""
    if tags.get("usage") == "tourism":
        return "usage=tourism"
    if tags.get("attraction"):
        return f"attraction={tags['attraction']}"
    for k in ("railway", "station"):
        if tags.get(k) == "miniature":
            return f"{k}=miniature"
    if "miniature" in str(tags.get("railway:traffic_mode") or ""):
        return f"railway:traffic_mode={tags['railway:traffic_mode']}"
    return None


# A STREET NAME THAT DESCRIBES (owner, 2026-10-13): on a street whose every
# way is a minor way, a name that is a bare type or way word ("Path", "The
# Walk"), a description ("Service Road", "Pedestrian Crossing") or a type and
# a code ("Footpath 104", "Trail #2", "Bridge 22") is no name: 89 and 41 rows
# on the 19. Never on a street with a way of residential class or above: 193
# such rows are real streets (London's "The Avenue"). Kept all the same: an
# alley or lane with a number (Sydney's "Lane 5"), and a local way word with
# a number where streets are numbered (Rua 1, Calle 5, Eje 3: 3,297 rows).
# English only; measure a new language's phrases on its built cities first.
STREET_DESCRIPTIONS = frozenset((
    "exit", "entrance", "entry", "access", "access road", "access lane", "access path", "access way",
    "service road", "service lane", "service alley", "service entrance", "service access",
    "bus terminus", "bus terminal", "bus station", "bus lane", "bus only", "buses only", "bus loop",
    "bus stop", "bus bay", "busway", "park path", "dirt path", "dirt road", "dirt track", "gravel path",
    "gravel road", "footpath", "foot path", "public footpath", "path", "trail", "walkway", "walking path",
    "walking trail", "sidewalk", "pavement", "alley", "alleyway", "back alley", "driveway", "drive",
    "ramp", "stairs", "steps", "staircase", "stairway", "bike path", "bicycle path", "cycle path",
    "cycle track", "bike lane", "cycle lane", "cycleway", "bikeway", "bike trail", "pedestrian path",
    "pedestrian walkway", "pedestrian crossing", "pedestrian access", "pedestrian bridge", "crosswalk",
    "crossing", "underpass", "overpass", "subway", "footbridge", "foot bridge", "bridge", "tunnel",
    "fire lane", "fire road", "fire access", "emergency access", "emergency exit", "loading dock",
    "loading bay", "parking", "car park", "track", "road", "street", "lane", "slip road", "on ramp",
    "off ramp", "on-ramp", "off-ramp", "taxi rank", "taxi stand", "drop off", "drop-off", "pick up",
    "pick-up", "turnaround", "roundabout", "u-turn", "unnamed road", "shortcut", "short cut",
    "cut through", "towpath", "boardwalk", "connector", "link", "link road", "haul road", "private road",
    "private drive", "private", "no entry", "one way", "main entrance", "rear entrance", "back entrance",
    "side entrance", "delivery", "deliveries", "delivery entrance", "delivery road", "loop", "loop road",
    "trailhead", "nature trail", "bridle path", "bridleway", "public bridleway", "public right of way",
    "right of way", "easement", "laneway", "rear lane", "garage", "garages", "service",
    "maintenance road", "maintenance access", "school path", "school entrance", "station access",
    "station entrance", "station approach", "platform", "platform access", "concourse", "arcade",
    "escalator", "lift", "elevator", "passage", "passageway", "corridor", "pathway", "path to beach",
    "beach access", "boat ramp", "slipway", "jetty", "pier", "promenade", "esplanade", "greenway"))
_STREET_CODE_TYPES = (
    "route", "highway", "hwy", "road", "bridge", "ramp", "exit", "gate", "lot", "path", "trail",
    "track", "tunnel", "loop", "section", "sector", "block", "bay", "stand", "stairs", "steps", "line",
    "aisle", "drive aisle", "level", "platform", "pier", "dock", "berth", "entrance", "access", "unit",
    "building", "zone", "area", "phase", "stage", "parking", "car park", "access road", "service road",
    "footpath", "walkway", "taxiway", "runway", "stair", "staircase", "driveway", "subway", "underpass",
    "footbridge", "culvert")
_STREET_CODE = r"(?:(?:no\.?\s*|#\s*|nr\.?\s*|n[°º]\s*)?\d+[a-z]{0,2}(?:[/\-]\d+[a-z]?)?|[a-z])"
_STREET_TYPE_CODE = re.compile(
    r"(?:" + "|".join(re.escape(w) for w in sorted(_STREET_CODE_TYPES, key=len, reverse=True))
    + r")\s+" + _STREET_CODE, re.I)
_STREET_ALLEY_CODE = re.compile(r"(?:public\s+)?(?:alley|lane|laneway)\s+(?:no\.?\s*|#\s*)?\d+[a-z]?", re.I)
_STREET_PAVEMENT = re.compile(r"\s\(?(?:\w+\s)?(pavement|sidewalk|footway)$")


def street_description(name, local):
    """The class of a street name that describes and does not name
    ("bare type", "way word", "description", "pavement", "type and code"),
    else None. Asked of a street whose every way is a minor way only."""
    low = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", name).casefold().strip(" .,;:()"))
    low = low[4:] if low.startswith("the ") else low
    # The second batch's classes first (2026-10-13): "Alley 12" is a numbered
    # alley there and no longer the name _STREET_ALLEY_CODE keeps.
    second = street_description_2(name)
    if second:
        return second
    plain = re.sub(r"\s+", " ", _plain(name).casefold().strip(" .,;:()"))
    for code in local:
        m = PATH_CODE[code].fullmatch(plain) if code in PATH_CODE else None
        # A code there must be: the bare word "Weg" is the way-word class.
        if m and re.search(r"\d|\s", plain):
            return "path code"
    if _STREET_ALLEY_CODE.fullmatch(low):
        return None
    if coded_type(name, local):
        return "type and code"
    if bare_type(name, local):
        return "bare type"
    ways = {w for c in ("en", *local) for w in WAY_WORDS.get(c, ())}
    if low in ways or name.strip().casefold() in ways:
        return "way word"
    if low in STREET_DESCRIPTIONS:
        return "description"
    if _STREET_PAVEMENT.search(low):
        return "pavement"
    m = re.fullmatch(r"(.+?)\s+" + _STREET_CODE, low)
    if m and tuple(local) != ("en",) and m.group(1) in {w for c in local for w in WAY_WORDS.get(c, ())}:
        return None
    if _STREET_TYPE_CODE.fullmatch(low):
        return None if low.split()[0] in ("route", "highway", "hwy") else "type and code"
    return None


# BUSWAYS AND RACE TRACKS (owner, 2026-10-13): a street whose every way is
# highway=busway or raceway is no street to search, unless a way has its own
# article: 126 rows on the 19 (100 busways, 26 raceways, among them the
# corners of Interlagos, each named on its own way). A street with one other
# way keeps all its ways (71 rows).
NOT_STREET_HIGHWAYS = {"busway", "raceway"}
# PRIVATE RESIDENTIAL STREETS (owner, 2026-10-13: "drop as ruled"): a street
# whose every way is access=private or no on highway=residential or
# unclassified, 4,102 rows on the 19 (1.6% of streets; Mexico City 1,982,
# London 1,088). It departs from the Paris precedent of 2026-10-11 (addressed
# private streets kept); the owner kept the ruling. PRIVATE_STREET_LEAD
# stands (52 rows) and so does a way's own article.
# living_street since the third list (2026-10-13): seven Berlin streets
# tagged access=private on it.
# PER CITY, A NAMED PRIVATE STREET STAYS (config.PLACE_KEEP_NAMED_PRIVATE_STREETS;
# owner, 2026-10-13: "named keep, codenamed drop", then "yes" to a per-city
# setting): the rule took 2,391 named streets out of Guadalajara and 124 out
# of Monterrey, the grids of gated neighborhoods, where the tag marks a gate
# and not a driveway. With the switch on, a private street goes only when
# its name is a code beside a type word (street_description). Off everywhere
# else: the rule stands for the estate roads it was written for.
PRIVATE_STREET_HIGHWAYS = {"residential", "unclassified", "living_street"}
# PLACE KINDS THE INDEX DOES NOT LIST, kept on an article of their own
# (owner, 2026-10-13): an island or an islet as a landmark, a district as a
# neighborhood (121 measured, with archipelagos, which are not built).
ISLAND_VALUES = {"island", "islet"}
# ONE ROW A STOP (owner, 2026-10-13): tram platforms of one folded name
# within PLATFORM_MERGE_M, every one railway=tram_stop, are one stop mapped a
# row a platform (294 rows on the 19, 205 of them in Prague). Rows that
# differ in mode or network are an interchange and stay two rows (261), and
# so do same-mode rows that are not tram stops (35).
PLATFORM_MERGE_M = 250
# ONE STOP, ONE ROW (faults the full reads found, 2026-10-13). Was 150 m and
# tram stops of one folded name only. Now: the name is read with a station
# word and a direction note in brackets set aside (_stop_key: "奈多駅" is
# "奈多", "Grand Arénas (dir Nice)" is "Grand Arénas"); tram stops of one
# such name chained within PLATFORM_MERGE_M are one row (Den Haag's four
# stops stand 170 to 230 m apart); and so are stations or halts of one
# railway value, UNLESS two of them carry different operators, networks or
# Wikidata entries, which is an interchange of two railways and stays two
# rows (Hiroshima's 新白島, Kochi's 朝倉, Seongnam's 모란). NOT built: a
# trailing platform number ("Gare de Tours 1" and "2"), which would also
# join "Terminal 1" and "Terminal 2"; those go by id.
_DIRECTION_NOTE = re.compile(r"\s*[(（]\s*(?:dir[.]?|direction|richting|vers)\s[^)）]*[)）]\s*$", re.I)


def _stop_key(name):
    return _station_core(_DIRECTION_NOTE.sub("", name))


def _one_railway(members):
    """True when station rows of one name may be one row: all tram stops, or
    nodes all of one railway value (station, halt) with no two different
    operators, networks or Wikidata entries among them."""
    kinds = {m[9].get("railway") for m in members}
    if kinds == {"tram_stop"}:
        return True
    if len(kinds) != 1 or not (kinds & {"station", "halt"}):
        return False
    if not all(m[7].startswith("node/") for m in members):
        return False                      # an outline is the outline merge's
    return all(len({(m[9].get(k) or "").strip() for m in members} - {""}) <= 1
               for k in ("operator", "network", "wikidata"))
# ONE ROW A THING (owner, 2026-10-13): junction, place and landmark rows of
# one folded name chained within ROW_MERGE_M are one thing in several rows
# (417 on the 19: Hong Kong's signalled junctions a row a signal, Kyoto's 町
# drawn twice). Supersedes "two nodes are two places" at NEAR_DUP_M for rows
# this near; a river row is never merged.
ROW_MERGE_M = 300
# A WIKIDATA ENTRY SHARED BY THREE OR MORE ROWS admits none of them (owner,
# 2026-10-13): 23 rows on the 19 were held only by an item their whole group
# shares (Seattle's park-system and campus items). Counted after the merges
# above, so one thing drawn three times is not a group.
SHARED_WIKIDATA_MIN = 3
# Ways of one name with no entry, this many or more, are the segments of the
# one relation of that name that carries the entry (the merges; sixth pass).
SEGMENTS_MIN = 2


# ---------------------------------------------------------------------------
# THE SECOND RULE BATCH (owner, 2026-10-13; DECISIONS.md, "Place search: the
# second rule batch and the final group", and the build's own entry, "Place
# search: the second rule batch built"). Classes wave 1's readers found in 33
# English-language cities. Every figure below was measured on 2026-10-13: "the
# 19" are the live cities on their caches of 2026-10-07 to 2026-10-11, "wave
# 1" the 33 cities of branch search-wave1 built in memory with no by-id drop.
# Re-measure a figure before relying on it for a new city.
# ---------------------------------------------------------------------------

# PRIVATE ALLEYS (rule 1): the private-street rule reads a service=alley way
# as it reads a residential one, so a street whose ways are private on both
# goes (Buffalo's "Trestle Alley", one residential way and one alley): 8 rows
# on the 19, 5 in wave 1.
PRIVATE_STREET_SERVICES = {"alley"}
# OPEN ON FOOT IS NOT PRIVATE (owner, 2026-10-13): a way whose foot tag lets
# people in is no private way for either private-street rule, whatever access
# says. Florence's limited-traffic zone is access=no with motor_vehicle=
# permit and foot=yes, and lost 55 public streets. access=private or no with
# no foot tag stays private.
FOOT_OPEN = {"yes", "designated", "permissive"}
# ---------------------------------------------------------------------------
# THE THIRD LIST (owner, 2026-10-13: "new rules and narrow version accepted";
# docs/decisions_drafts/search-rules-3.md), classes the final group's reads
# found in Anyang, Gwangju, Berlin, Bremen, Zurich and Gelsenkirchen. Figures
# measured 2026-10-13 on the 19 live cities and wave 1's 33, in memory.
# ---------------------------------------------------------------------------
# An apartment estate or its management office as a park's operator (3).
ESTATE_OPERATOR = re.compile("아파트|관리사무소|관리소")
# A customers-only service road named by a description (4): every way
# highway=service with access=customers, and a Korean name whose last word
# is a bare road word (Gwangju's "후문 진입로", "단지 내 도로"). The tags alone
# are no test: measured on the 19 they took 32 named streets (Montreal's
# Place du Canada, Sao Paulo's gated Alamedas), which stay.
CUSTOMER_ROAD_ENDS = ("도로", "진입로")
# A SITE OR BOUNDARY RELATION THAT REPEATS ANOTHER ROW (9): a type=site or
# boundary relation whose Wikidata entry or Wikipedia article another row
# carries is that thing's second row, set at the middle of scattered members
# (Bremen's university, 3 km from its campus row). Beyond ROW_MERGE_M only:
# nearer rows of one name are merged already, and a relation that near is on
# the object.
SITE_RELATION_TYPES = {"site", "boundary"}
# A public_transport=station OBJECT WITH NO RAILWAY TAG IS NO STATION ROW
# (13): a service point, a mezzanine, a bus terminal with no mode written.
# Reconciled with the lone stop area: one that lists a rail mode or carries a
# station tag stays where no other station row carries its station (the
# same test, OUTLINE_BESIDE_M and OUTLINE_SAME_M).
# PUBLIC ART NEEDS A WIKIPEDIA ARTICLE OF ITS OWN (16; owner, 2026-10-13:
# "yes article needed"): tourism=artwork was in on a wikidata tag alone
# (1,048 of Berlin's 1,111 artworks). The cost the owner accepted: a real
# sculpture with no article leaves too. An article the tags cannot place
# (own_article's "undecided") keeps the row as it was.
# A CODE BESIDE A PATH TYPE (17), German, on a street whose every way is a
# minor way: "Weg 5", "Weg X", "Querweg 12", "3. Querweg", "Stichweg A",
# "Ring II", "Fußweg 3", "Nebenweg 1" (Berlin: 79 names, 227 ways). NEVER
# "Straße N", a real Berlin street name on any class of way, and never a
# name before the type ("Volksgartenweg 1", "Pfuhlweg II").
PATH_CODE = {"de": re.compile(r"(?:\d+\.\s*)?(?:querweg|stichweg|nebenweg|fussweg|weg|ring)"
                              r"(?:\s+(?:\d+[a-z]?|[a-z]|[ivx]+))?")}
# A DEAD RAILWAY ALIGNMENT (18): a way whose railway is abandoned, disused,
# razed or dismantled, or prefixed so, with no wikipedia tag, is a line on
# old maps and no place (Berlin 28). A standing structure under a lifecycle
# tag (a water tower, a tunnel, a bridge) is not this class.
DEAD_RAILWAY_VALUES = {"abandoned", "disused", "razed", "dismantled"}
DEAD_RAILWAY_PREFIXES = ("abandoned", "disused", "razed", "dismantled", "demolished")
STANDING_KEYS = ("building", "man_made", "bridge", "tunnel", "tourism", "amenity")


def dead_railway(tags):
    """The tag that says a way is a dead railway alignment, else None."""
    if any(tags.get(k) not in (None, "no") for k in STANDING_KEYS) or tags.get("wikipedia"):
        return None
    if tags.get("railway") in DEAD_RAILWAY_VALUES:
        return f"railway={tags['railway']}"
    return next((f"{p}:railway={tags[f'{p}:railway']}" for p in DEAD_RAILWAY_PREFIXES if tags.get(f"{p}:railway")),
                None)


# A NAME ENDING "(historical)" IS GONE (rule 3): the GNIS import's mark for a
# feature no longer there ("Lake Vista Park (historical)"). Any tagged row.
# And, narrowly, the German marks the final group's reads found (the third
# list, 2026-10-13): "(geschlossen)", "(abgebrannt)", "(stillgelegt)",
# "(außer Betrieb)". NOT "ehem." or "ehemalig": it leads 39 Berlin landmark
# names, several of them standing buildings.
# And the marks the full reads found (2026-10-13), in either bracket form:
# (閉鎖), (閉鎖中), (予定地), （廃駅）, (폐역).
HISTORICAL_NAME = re.compile(
    r"[(（](?:historical|geschlossen|abgebrannt|stillgelegt|außer betrieb|ausser betrieb|fechado|fechada"
    r"|閉鎖|閉鎖中|予定地|廃駅|폐역)[)）]\s*$", re.I)
# REGISTER AND INVENTORY ENTRIES (rule 4): historic=maritime, naval, military
# and engine are the values a register district's members and a museum's
# hardware carry. A landmark of these values needs a Wikipedia article of its
# own; a register number, a heritage tag or a Wikidata entry admits none: 55
# rows on the 19 (Seattle 51, the Ballard Locks and Sand Point's buildings
# among them) and 326 in wave 1 (New York 85, Philadelphia 85).
REGISTER_HISTORIC = {"maritime", "engine", "naval", "military"}
# OR A WIKIDATA ENTRY OF ITS OWN (owner, 2026-10-13, on the first changed-row
# report: "a Wikidata entry of the row's OWN counts as well"). Own: no other
# object in the city's cache carries the entry (own_item), and it is not the
# object's subject's, brand's or operator's. That is the test that catches an
# entry for a class of thing (Seoul's tanks carry their MODEL's entry, one
# entry on several objects; Seattle's three lock ways share the Locks'). Not
# for historic=engine: an engine is a model's example, as MODEL_EXHIBITS
# are, and a lone one would carry its model's entry unshared. Back on the
# 19: Seattle's Pacific Tower, Naval Reserve Armory Building and Canoe House.
REGISTER_ITEM_VALUES = REGISTER_HISTORIC - {"engine"}
# KEPT BY THE OWNER'S WORD, BY ID (owner, 2026-10-13): config.PLACE_KEPT
# names an object, with why, that the bare-type or the register-entry rule
# would drop and the owner keeps: Seattle's Ballard Locks (the dam carries
# neither an article nor an entry, the lock ways share one) and London's
# "Greenway", a named linear park under a bare type word. Those two rules
# only; an id not in the cache stops the step.
# INTERCHANGE NAMES KEPT, PER CITY (owner, 2026-10-13: "keep as per-city with
# reasoning"): config.PLACE_KEEP_INTERCHANGES = True keeps a city's
# interchange names as street names, by name and by the motorway-junction
# test alike. Hong Kong sets it (44 rows).
# A REGISTER NUMBER SHARED BY A DISTRICT (rule 4, "numbered buildings of a
# register district go"): a ref:nrhp value on SHARED_REGISTER_MIN or more
# objects of the cache is the district's, and keeps no coded name
# ("Building 10"). Wikidata or wikipedia on the object still does.
SHARED_REGISTER_MIN = 3
# ONE ROW A STATION (rule 5). A public_transport=stop_area relation groups a
# station's parts and is no station. A station outline (a way or relation
# tagged public_transport=station with no railway tag) within
# OUTLINE_BESIDE_M of a rail-tagged station row, or within OUTLINE_SAME_M of
# one of its folded name, is that station's building. Station rows sharing
# one Wikidata entry, chained within COMPLEX_MERGE_M, are one transfer
# complex: one row, the others' names its aliases. A bus station
# (NOT_RAIL's amenity) with no railway tag is no rail station whatever rail
# mode it lists. On the 19: 5 stop areas, 91 outlines, 215 rows merged into
# their complex (Tokyo 88, Seoul 45, Barcelona 34), 1 bus station. In wave 1:
# 15, 6, 59 (New York 36) and 6. Two names the map draws are never merged
# (complex_parts, the fifth pass).
OUTLINE_BESIDE_M = 150
OUTLINE_SAME_M = 400
COMPLEX_MERGE_M = 600
# A STREET'S WAY IS NEVER A LANDMARK ROW (rule 7), whatever historic, tourism
# or bridge:name tag it carries: the street row is the way's row. Not an
# area (a square drawn as a pedestrian area is a landmark by the ruling of
# the same day) and not one of these values, which are no ways to travel.
# 27 rows on the 19 and 76 in wave 1, registered bridges under bridge:name
# among them (Seattle's Aurora Bridge), which the first batch had named.
NOT_A_STREET_WAY = SKIP_HIGHWAY | {"traffic_island"}
# A SETTLEMENT'S BOUNDARY (rule 10) is no second place row beside the node
# that bears its name: a boundary tagged as one of these kinds, where a city,
# town, village or hamlet node of the same folded name is in the cache
# (11 rows on the 19, 13 in wave 1).
BOUNDARY_DUP_PLACES = SETTLEMENTS | {"suburb", "borough"}
# A SUBURB'S BOUNDARY BESIDE ITS OWN SUBURB NODE (a fault mended, the sixth
# pass, 2026-10-13). Rule 10 read the node only where it is a city, a town, a
# village or a hamlet, so Rio de Janeiro's bairro boundaries tagged
# place=suburb kept a second row beside their place=suburb nodes ("Ilha de
# Guaratiba", its centre 2.9 km from the node, beyond what NEAR_DUP_M joins;
# "Freguesia (Ilha)", 250 m from the node "Freguesia"). A suburb's or a
# borough's node counts where it has the boundary's own place value and lies
# within BOUNDARY_NODE_M of the boundary's centre: a city can hold two
# suburbs of one name (Rio has two Freguesias, 24 km apart), so the distance
# is part of the test here, as it is not for a settlement. Measured on the 19
# live cities, 2026-10-13: no row leaves; Rio de Janeiro's two do.
BOUNDARY_NODE_M = 5000
# ESTATES IN THE PLURAL AND MOBILE-HOME PARKS (rule 9), held to ESTATE_NAME's
# test: a place so named needs wikidata or an article (2 rows on the 19; in
# wave 1 29 and, all in Miami, 25).
ESTATES_NAME = {"en": re.compile(r"\bestates$", re.I)}
MOBILE_HOME_PARK = re.compile(
    r"\b(?:mobile homes?|manufactured homes?|trailer (?:park|court|village|ranch|haven|city|town|lodge|estates?)"
    r"|mobile (?:park|court|village|manor|estates?|community|lodge|colony|city|ranch|terrace|haven))\b", re.I)
# NAMED ROUNDABOUTS STAY (owner, 2026-10-13: "keep the named roundabouts"):
# a street whose every way is junction=roundabout or circular. One constant,
# so the other answer given that day is one edit. The count each way is in
# the report key street_roundabout_kept and in the decisions entry: 479
# rows stay on the 19 (Sao Paulo 159, London 115, Marseille 102) and 373 in
# wave 1; False drops them all.
ROUNDABOUTS_STAY = True
ROUNDABOUT_JUNCTIONS = {"roundabout", "circular"}
# STANDING BUT ABANDONED OR RUINED LANDMARKS STAY (owner, 2026-10-13: "keep
# all standing abandoned landmarks"). True holds one to an article of its
# own, the other answer given that day. The count each way is the log's
# abandoned_standing records and in the decisions entry: 297 rows on the 19
# and 335 in wave 1 stand abandoned or ruined with no article of their own;
# True drops them all.
ABANDONED_NEED_ARTICLE = False
# INTERCHANGES, RAMPS AND MANAGED LANES (rules 11 and 12, question b) are no
# streets. By name whatever the ways: "X Interchange", "X Onramp", "X Off
# Ramp", "X Drwy". By name on ramp-class ways only: a name ending "Ramp" or
# Melbourne's "Ramp On" and "Ramp Of". By tag: a circular junction whose
# every way is a motorway's (Manchester's "Simister Island"). A managed
# lane's label ("HOV", "Express Lanes") on motorway ways only. On the 19:
# 51 interchanges (Hong Kong 44), 25 ramps (Sydney 24), 1 managed lane. In
# wave 1: 65, 97 (Melbourne 91), 14 managed lanes and 7 names ending Drwy.
MOTORWAY_HIGHWAYS = {"motorway", "motorway_link"}
RAMP_HIGHWAYS = MOTORWAY_HIGHWAYS | {"trunk_link", "primary_link", "secondary_link", "tertiary_link"}
_NEVER_STREET = (("interchange", re.compile(r"\binterchange$", re.I)),
                 ("ramp", re.compile(r"\b(?:on|off)[ -]?ramp$", re.I)),
                 ("driveway", re.compile(r"\bdrwy\.?$", re.I)))
RAMP_NAME = re.compile(r"\bramp(?: on| off?)?$", re.I)
MANAGED_LANE = re.compile(r"\b(?:hov|hot lanes?|express ?lanes?|managed lanes?|carpool lanes?)\b", re.I)


def _abandoned_standing(tags):
    """The tag that says a landmark stands abandoned or in ruins, else None
    (ABANDONED_NEED_ARTICLE's class)."""
    flag = next((k for k in ("abandoned", "disused") if tags.get(k) == "yes"), None)
    if flag:
        return f"{flag}=yes"
    if tags.get("ruins") not in (None, "no"):
        return f"ruins={tags['ruins']}"
    for k in ("historic", "building"):
        if tags.get(k) == "ruins":
            return f"{k}=ruins"
    return next((f"{k}={tags[k]}" for k in sorted(tags)
                 if k.partition(":")[0] in ("abandoned", "disused") and k.partition(":")[2] in LIFE_FEATURES), None)


def _bridge_led(tags, names):
    """`names` with bridge:name leading, for a bridge drawn on a road whose
    bridge:name differs from its name; else `names` itself."""
    bridge = (tags.get("bridge:name") or "").strip()
    if tags.get("highway") and tags.get("bridge") not in (None, "no") and bridge \
            and bridge != names[0] and not junk_name(bridge):
        return [bridge] + [n for n in names if n != bridge]
    return names


# A station word closing a name is set aside when an outline is matched to
# its node (Gwangju's outline "상무역" beside its node "상무").
STATION_NAME_ENDS = ("station", "역", "駅", "站")


def _station_core(name):
    # Folded like the name: fold_name writes a Hangul syllable as its jamo.
    key = fold_name(name)
    return next((key[:-len(end)] for end in map(fold_name, STATION_NAME_ENDS)
                 if key.endswith(end) and len(key) > len(end)), key)


# TWO STATIONS OF THE MAP ARE NEVER ONE ROW (owner, 2026-10-13, the fifth
# pass; a fault found in Boston, wave 1). Boylston's node carries Park
# Street's Wikidata entry, so the complex merge folded Boylston, 350 m off,
# into Park Street as an alias and Boylston had no row. A complex whose rows
# bear two or more names the map draws (map_stations, folded) is split at
# those names: each drawn name keeps a row, and a row under any other name
# joins the nearest of them. With one drawn name or none the complex merges
# as before. Distance is NOT the test: Barcelona's "Barcelona-Passeig de
# Gràcia" is its metro station's own rail hall at 357 m, Boylston another
# station at 350 m. On the 19 live cities it undoes 2 of the 210 merges:
# London's Monument beside Bank (354 m) and Barcelona's Provença beside
# Diagonal (191 m). Needs STATIONS_CSV on the machine, as the guard does.
def complex_parts(members, drawn):
    """`members` (station rows of one Wikidata entry, chained within
    COMPLEX_MERGE_M) split into the groups that merge: one group a name."""
    # STATIONS OF DIFFERENT NAMES DO NOT FOLD ON A SHARED ENTRY ALONE (owner,
    # 2026-10-13, the full reads): Toyama's 電鉄富山 carried JR 富山's entry
    # and had no row, Nagasaki's JR 浦上 was an alias of its tram stop,
    # Kagoshima's JR station an alias of 鹿児島駅前. Rows of one name, a
    # station word set aside (_station_core), are one row; every other name
    # keeps its own. `drawn` is no longer read: two map names are two names.
    parts = defaultdict(list)
    for r in members:
        parts[_station_core(r[3])].append(r)
    return [parts[n] for n in sorted(parts)]


def street_never(name):
    """The class of a street name that is no street's whatever its ways
    ("interchange", "ramp", "driveway"), else None."""
    text = _plain(name)
    return next((cls for cls, pat in _NEVER_STREET if pat.search(text)), None)


def _plain(name):
    """A name less its format characters (a hidden left-to-right mark ends
    3,299 of Los Angeles's alley names) and outer spaces."""
    return "".join(ch for ch in unicodedata.normalize("NFKC", name)
                   if unicodedata.category(ch) != "Cf").strip()


# DESCRIPTIONS AS STREET NAMES, the second list (rule 11, questions c and f),
# asked like street_description of a street whose every way is a minor way:
# 127 rows on the 19, every one a cycle facility (Chicago 52, Sydney 40),
# and 3,751 in wave 1 (Los Angeles 3,313, Sacramento 299).
# A street type word, as written or abbreviated, closes a street's name:
_TYPE = (r"(?:street|st|avenue|ave|av|boulevard|blvd|road|rd|drive|dr|way|place|pl|court|ct|lane|ln"
         r"|parkway|pkwy|highway|hwy|terrace|circle)\.?")
_COMPASS = r"(?:\s+(?:north|south|east|west|northeast|northwest|southeast|southwest|n|s|e|w|ne|nw|se|sw))?"
# "Alley" and digits only (Los Angeles 3,304 rows, Sacramento 10). A lane
# with a number stays a name (Sydney's "Lane 5").
NUMBERED_ALLEY = re.compile(r"alley\s*(?:no\.?\s*|#\s*)?\d+")
# Two street names and "Alley", no connector: Sacramento's alleys named by
# the two streets they run between ("12th Avenue 13th Avenue Alley").
CROSS_STREET_ALLEY = re.compile(r".+\s" + _TYPE + r"\s+.+\s" + _TYPE + r"\s+alley")
PATH_BETWEEN = re.compile(r"(?:path|pathway|walkway|footpath|foot path|trail|stairs|steps|stairway|sidewalk)"
                          r" between .+ and .+")
# A cycle facility named for the street it runs on: a street's name, type
# word included, then the facility ("15th Street NW Cycletrack", "Austin
# Street Bikeway"). NOT a name ending "Trail" and not one with no street type
# word: "Los Angeles River Bike Path" and "Footscray Road Trail" are trails'
# own names and stay.
CYCLE_FACILITY = re.compile(
    r".+\s" + _TYPE + _COMPASS + r"\s+(?:(?:protected|separated|buffered|two-way)\s+)?"
    r"(?:cycle\s?track|cycle\s?way|bike\s?way|bike lane|bicycle lane|cycle lane|bike path|bicycle path"
    r"|cycle path|side\s?path)")
DRIVEWAY_NAME = re.compile(r".+\sdriveway")
# The two alley classes are no names on a way of any class: 23 of
# Sacramento's cross-street alley ways are drawn highway=residential.
ANY_WAY_DESCRIPTIONS = {"numbered alley", "cross-street alley"}


def street_description_2(name):
    """The second batch's classes of a minor-way street name that describes
    ("numbered alley", "cross-street alley", "path between", "cycle
    facility", "driveway"), else None."""
    low = re.sub(r"\s+", " ", _plain(name).casefold().strip(" .,;:()"))
    for cls, pat in (("numbered alley", NUMBERED_ALLEY), ("cross-street alley", CROSS_STREET_ALLEY),
                     ("path between", PATH_BETWEEN), ("cycle facility", CYCLE_FACILITY),
                     ("driveway", DRIVEWAY_NAME)):
        if pat.fullmatch(low):
            return cls
    return None


def _clusters(points, radius):
    """Index lists of `points` [(lat, lon)] chained within `radius` metres
    (single link), each of two or more, in first-member order."""
    parent = list(range(len(points)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if _dist_m(points[i], points[j]) <= radius:
                parent[find(i)] = find(j)
    out = defaultdict(list)
    for i in range(len(points)):
        out[find(i)].append(i)
    return sorted((v for v in out.values() if len(v) > 1), key=lambda v: v[0])


SQUARE_DUP_M = 500
SQUARE_NEAR_M = 150
# Abbreviated square words read in full when a square is compared with the
# streets and squares around it (_square_keys): "nám." is náměstí. The word
# itself stays: Barcelona's Placeta del Pi and Plaça del Pi are two squares.
SQUARE_ABBR = {"nam": "namesti"}
# THE SQUARE MERGE LOSES NO NAME (a fault mended, 2026-10-13). A park named
# as a square (the sixth pass) is one row with a street only when the street
# row bears the park's own leading name, joiners set aside (SQUARE_JOINERS:
# "Praça do Japão" is the street "Praça Japão"); a name spelled another way
# ("Praça John Kennedy" beside "Praça Jonh Kennedy") or a street under
# another name keeps the park its own row. Whatever merges, the row that
# stays carries the merged square's exact spelling as an alternate name when
# it differs. On the extract run 41 merged squares were not findable under
# their names, 8 of them beside a street of another name
# (data/_search_rollout/extract_rules56/squares_name_not_findable.tsv).
SQUARE_JOINERS = frozenset(("de", "do", "da", "dos", "das", "du", "des", "del", "d", "la", "las", "los",
                            "le", "les", "l", "el", "els"))


def _square_keys(names):
    """Each name folded to its words: accents, case and punctuation gone, a
    leading abbreviated square word in full."""
    out = set()
    for n in names:
        ws = re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKD", n.lower())
                        .encode("ascii", "ignore").decode())
        if ws:
            out.add(tuple([SQUARE_ABBR.get(ws[0], ws[0])] + ws[1:]))
    return out


def _square_joined(names):
    """_square_keys with the joiners after the first word set aside, each
    name one string."""
    return {"".join([ws[0]] + [w for w in ws[1:] if w not in SQUARE_JOINERS]) for ws in _square_keys(names)}


# THE INDEX REACHES THE WHOLE MAP (owner, 2026-10-12). Mexico City's index
# landed cut to the city proper after its map became regional: the 11
# stations in the four added municipios were on the map and not in the
# search, with 0 or 1 indexed places within 1 km of each. The rule: every
# station the map draws has at least one indexed place, other than a
# station, within COVER_KM. Measured on the 19 indexes of 2026-10-12, the
# emptiest covered stations hold 2 (Montreal's Anse-a-l'Orme), 3 (Kyoto's
# Hozukyo and Kibuneguchi) and 4 (Busan's Seokdae), so on those 19 zero was a
# boundary cut and not a quiet station. Re-measure before raising the floor.
# run() exits on it; scripts/check_place_search.py H re-reads it.
# QUIET STATIONS (owner, 2026-10-13). Zero is not always a cut: the final
# group found stations inside their search area with nothing indexed within
# the distance (Most's stops in the Zaluzi chemical works, Yamagata's). A
# city names each in config.PLACE_QUIET_STATIONS = {"<station name as in
# STATIONS_CSV>": "why, who, when"}, and the rule counts it as accounted for.
# The list may not rot: a listed station that has an indexed place within
# COVER_KM after all, or is not on the map, stops the step and fails check H,
# naming it (quiet_stations).
COVER_KM = 1.0


def quiet_stations(quiet, stations, bare):
    """(the uncovered stations `bare` less those config.PLACE_QUIET_STATIONS
    lists, problems): a problem for each listed name that is no station of
    the map (`stations`, map_stations()) or is covered after all."""
    on_map = {name for name, _, _ in stations}
    problems = [f"config.PLACE_QUIET_STATIONS lists {name!r}, which is not a station on the map: remove it"
                for name in sorted(quiet) if name not in on_map]
    problems += [f"config.PLACE_QUIET_STATIONS lists {name!r}, which has an indexed place within "
                 f"{COVER_KM:g} km: remove it"
                 for name in sorted(quiet) if name in on_map and name not in bare]
    return [name for name in bare if name not in quiet], problems
_STATION_COLS = (("latitude", "longitude"), ("lat", "lon"), ("stop_lat", "stop_lon"), ("lat", "lng"))


def map_stations(config):
    """[(name, lat, lon)] for the stations a city's map draws, from
    config.STATIONS_CSV, or None when that file is not on this machine
    (data/ is not committed). Exits on a file whose columns it cannot read,
    since a coverage check that silently reads nothing is no check."""
    import csv
    import sys
    path = getattr(config, "STATIONS_CSV", None)
    if path is None or not Path(path).is_file():
        return None
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return []
    cols = {c.lower(): c for c in rows[0]}
    pair = next(((cols[a], cols[b]) for a, b in _STATION_COLS if a in cols and b in cols), None)
    if pair is None:
        sys.exit(f"{path}: no latitude and longitude columns among {list(rows[0])}; "
                 f"add the pair to place_index._STATION_COLS")
    name = cols.get("station") or cols.get("name") or cols.get("stop_name") or list(rows[0])[0]
    return [(r[name], float(r[pair[0]]), float(r[pair[1]])) for r in rows]


def decode_lines(encoded, scale=100000):
    """The polylines [[(lat, lon), ...], ...] of the street lines file's
    `lines` ([[flat, ...], ...], one list per street row, as street_lines
    writes them)."""
    out = []
    for flats in encoded:
        for flat in flats:
            la, lo = flat[0], flat[1]
            pts = [(la / scale, lo / scale)]
            for k in range(2, len(flat) - 1, 2):
                la, lo = la + flat[k], lo + flat[k + 1]
                pts.append((la / scale, lo / scale))
            out.append(pts)
    return out


def _seg_dist_m(p, a, b):
    """Metres from p to the segment a-b, on a local flat grid at p."""
    kx = 111320.0 * math.cos(math.radians(p[0]))
    ax, ay = (a[1] - p[1]) * kx, (a[0] - p[0]) * 110540.0
    bx, by = (b[1] - p[1]) * kx, (b[0] - p[0]) * 110540.0
    dx, dy = bx - ax, by - ay
    d2 = dx * dx + dy * dy
    t = 0.0 if d2 == 0 else max(0.0, min(1.0, -(ax * dx + ay * dy) / d2))
    return math.hypot(ax + t * dx, ay + t * dy)


def uncovered_stations(rows, stations, km=None, lines=None):
    """Names of the stations with no index row, other than a station row,
    within COVER_KM. rows are the index's ([kind, lat, lon, ...], kind 0 a
    station); a 0.01 degree grid keeps it linear.

    lines, when given, are the indexed streets' polylines (decode_lines): a
    station the row points miss is covered when a street's drawn line passes
    within COVER_KM. A street row has one point, and a long rural road's
    point can lie kilometres from a station the road runs past (Ottawa's
    Bowesville, 2026-10-13: inside the area, two unindexed parks and
    Bowesville Road nearby). A boundary cut still fails: a station outside
    the fetched area has no fetched street beside it."""
    km = COVER_KM if km is None else km
    grid = {}
    for r in rows:
        if r[0] != 0:
            grid.setdefault((math.floor(r[1] * 100), math.floor(r[2] * 100)), []).append((r[1], r[2]))
    span = int(km / 1.0) + 2
    out = []
    for name, lat, lon in stations:
        i0, j0 = math.floor(lat * 100), math.floor(lon * 100)
        near = any(_dist_m((lat, lon), p) <= km * 1000.0
                   for i in range(i0 - span, i0 + span + 1) for j in range(j0 - span, j0 + span + 1)
                   for p in grid.get((i, j), ()))
        if not near:
            out.append((name, lat, lon))
    if out and lines:
        # Only the stations the points missed are measured against the
        # segments, so the cost is a few stations times the city's segments.
        reach = km * 1000.0
        out = [(name, lat, lon) for name, lat, lon in out
               if not any(_seg_dist_m((lat, lon), a, b) <= reach
                          for line in lines for a, b in zip(line, line[1:]))]
    return [name for name, _, _ in out]


def _dist_m(a, b):
    lat = math.radians((a[0] + b[0]) / 2)
    return math.hypot((a[0] - b[0]) * 110540.0, (a[1] - b[1]) * 111320.0 * math.cos(lat))


def _r(x):
    # 4 decimals, about 11 m: the search jumps to zoom 16 and marks the spot
    # with a 14 px circle (owner, 2026-10-08: index size). Was 5.
    return round(x, 4)


def _commercial_reasons(tags):
    """Why _commercial fires: the commercial keys present, "building", and
    each COMMERCIAL_VALUES hit as "key=value"."""
    out = [k for k in COMMERCIAL_KEYS if k in tags]
    # A ruin is no business, whatever building it was (Seattle's Coal Creek
    # Hotel ruins, building=hotel, reviewed).
    if tags.get("building") in COMMERCIAL_BUILDINGS and not (
            tags.get("wikidata") or tags.get("wikipedia") or tags.get("heritage")
            or tags.get("historic") in ("ruins", "archaeological_site")):
        out.append("building")
    return out + [f"{k}={tags[k]}" for k, vals in COMMERCIAL_VALUES.items() if tags.get(k) in vals]


def _commercial(tags):
    return bool(_commercial_reasons(tags))


# The business signs an article of the object's own outweighs (owner,
# 2026-10-13; landmark_drop): a private operator and an office tag, nothing
# else. operator:type=business or commercial is not among them.
KEPT_COMMERCIAL_REASONS = {"office", "operator:type=private"}
# What a rule's record keeps of an object's tags (build()'s `log`).
_LOG_KEYS = {"wikidata", "wikipedia", "heritage", "ref:nrhp", "historic", "tourism", "amenity", "building",
             "leisure", "landuse", "access", "memorial", "cemetery", "tomb", "place", "railway",
             "public_transport", "highway", "service", "station", "usage", "attraction", "artwork_type",
             "man_made", "natural", "office", "shop", "brand", "bridge", "area", "opening_date",
             "start_date", "end_date", "construction", "proposed", "disused", "abandoned", "demolished",
             "razed", "removed", "castle_type", "garden:type", "network", "ruins"}
_LOG_PREFIXES = {"subject", "buried", "operator", "bridge", "proposed", "construction", "planned",
                 "disused", "abandoned", "razed", "demolished", "removed", "destroyed", "was"}


def _point(el):
    if el["type"] == "node":
        return el["lat"], el["lon"]
    c = el.get("center")
    return (c["lat"], c["lon"]) if c else None


def build(elements, *, city, retrieved, local, fold=None, dropped=(), visitable=(), rebuilt=(),
          closed_for_works=(), way_words=(), kept=(), keep_interchanges=False, keep_named_private=False,
          map_stations=(), also=(),
          station_strip=(), articles=None, log=None):
    """Return (index dict, report dict) from one place cache's elements.
    `local`: the city's local language codes (config.PLACE_LANGUAGES).
    `dropped`: OSM objects ("way/504652702") a reading by eye found to be a
    business or a home that no rule catches (config.PLACE_DROPPED).
    `visitable`: homes the public can visit today, kept against the home rule
    (config.PLACE_VISITABLE's live entries; VISITABLE FORMER HOMES above).
    `rebuilt`: names of streets closed for rebuilding, kept although OSM
    draws them highway=construction (config.PLACE_REBUILT).
    `closed_for_works`: OSM objects that stand but are closed for works, kept
    although their tags read as not yet open (config.PLACE_CLOSED_FOR_WORKS).
    `way_words`: this city's own words for the minor-way name test
    (config.PLACE_WAY_WORDS).
    `kept`: OSM objects kept by the owner's word against the bare-type and
    register-entry rules (config.PLACE_KEPT).
    `keep_interchanges`: this city's interchange names are street names
    (config.PLACE_KEEP_INTERCHANGES).
    `map_stations`: the stations the city's map draws (map_stations()), for
    the station guard: names, or (name, lat, lon) where the positions are
    known (the disused test's guard, drawn_station_here, reads them).
    `also`: languages declared below the floor (config.PLACE_LANGUAGES_ALSO).
    `station_strip`: endings taken off station names (config.PLACE_STATION_STRIP).
    `articles`: the city's Wikidata article cache (read_wikidata_articles),
    None when there is none.
    `log`: a list that receives one record per decision of the 2026-10-13
    rules (class, action, OSM id, name, the deciding tag), for the changed-row
    report of a rule change; nothing reads it otherwise."""
    also = tuple(a for a in also if a not in local)
    read = (*local, *also)
    name_tags = _name_tags(read)
    asked = set()                             # Wikidata entries has_article was asked about

    def langs_of(t):
        return _langs(t, local) | {a for a in also if t.get(f"name:{a}")}
    kept_ids = set(kept)
    kept_given = frozenset(kept)          # config.PLACE_KEPT as given (the admission at the end)
    # A RIVER IS ONE ROW OF MANY WAYS (candidate 28, owner 2026-10-13): its
    # row carries the id of its lowest-numbered way in place_ids.json, and an
    # id of ANY of its ways in config.PLACE_DROPPED or PLACE_KEPT stands for
    # the whole row, so a river can be dropped or kept by id.
    dropped, river_names = set(dropped), {"dropped": set(), "kept": set()}
    for e in elements:
        t = e.get("tags") or {}
        oid = f"{e['type']}/{e['id']}"
        if t.get("waterway") and (oid in dropped or oid in kept_ids):
            ns = _local_first(t, _names(t, name_tags), read)
            if ns:
                river_names["dropped" if oid in dropped else "kept"].add(ns[0])
    for e in elements:
        t = e.get("tags") or {}
        if t.get("waterway") and (river_names["dropped"] or river_names["kept"]):
            ns = _local_first(t, _names(t, name_tags), read)
            if ns and ns[0] in river_names["dropped"]:
                dropped.add(f"{e['type']}/{e['id']}")
            elif ns and ns[0] in river_names["kept"]:
                kept_ids.add(f"{e['type']}/{e['id']}")
    drawn = {fold_name(n if isinstance(n, str) else n[0]) for n in map_stations}
    drawn_at = [(fold_name(n[0]), n[1], n[2]) for n in map_stations if not isinstance(n, str)]

    def note(cls, act, osm, name, why="", tags=None, bbox=None, ways=None):
        if log is not None:
            log.append({"class": cls, "act": act, "osm": osm, "name": name, "why": why, "bbox": bbox,
                        **({"ways": ways} if ways else {}),
                        "tags": {k: v for k, v in (tags or {}).items() if k in _LOG_KEYS
                                 or k.partition(":")[0] in _LOG_PREFIXES}})

    carriers = defaultdict(list)              # wikipedia value -> (OSM id, folded name, point, a way)

    def article(e, t, names, pt, way=False):
        """own_article() for one element, with who shares its article."""
        wp = (t.get("wikipedia") or "").strip()
        if not wp:
            return "none", ""
        oid, mine = f"{e['type']}/{e['id']}", fold_name(names[0])
        others = [c for c in carriers[wp] if c[0] != oid and not (
            c[1] == mine and ((way and c[3]) or _dist_m(c[2], pt) <= SAME_THING_M))]
        # The one object an article is named after owns it, whoever else
        # carries it: Chicago's Pullman National Historical Park and the
        # buildings inside it tagged with the park's article. Not where
        # another carrier bears the same name (the 69 Édicule Guimard).
        if others and fold_name(article_title(wp)) == mine and not any(c[1] == mine for c in others):
            others = []
        return own_article(t, names, shared=bool(others))

    nodes = {}
    ways = []
    tagged = []
    for e in elements:
        if e["type"] == "node" and "tags" not in e:
            nodes[e["id"]] = (e["lat"], e["lon"])
        elif e["type"] == "way" and "nodes" in e:
            ways.append(e)
            # A highway way that is also a place (a square drawn as a pedestrian
            # area) goes on to the place pass too, with run()'s center.
            if (e.get("tags") or {}).get("place") and "center" in e \
                    and f"way/{e['id']}" not in dropped:
                tagged.append(e)
        else:
            if f"{e['type']}/{e['id']}" in dropped:
                continue
            tagged.append(e)
            if e["type"] == "node":
                nodes.setdefault(e["id"], (e["lat"], e["lon"]))

    # Who else carries each article (own_article's `shared`): every named
    # object in the cache, a highway way at its middle node.
    for e in elements:
        t = e.get("tags") or {}
        wp = (t.get("wikipedia") or "").strip()
        if not wp:
            continue
        ns = _local_first(t, _names(t, name_tags), read)
        is_way = e["type"] == "way" and "nodes" in e
        if is_way:
            ids = [n for n in e["nodes"] if n in nodes]
            pt = nodes[ids[len(ids) // 2]] if ids else None
        else:
            pt = _point(e)
        if ns and pt:
            carriers[wp].append((f"{e['type']}/{e['id']}", fold_name(ns[0]), pt, is_way))

    report = defaultdict(int)
    not_open = []                             # stations skipped as not yet open
    rows = []
    square_rows = []                          # place=square landmark rows (the duplicate pass)
    park_square_rows = []                     # parks named as a square or a street (the same pass)
    # The extent of the city's own street nodes, a little wider: an area that
    # only touches the city comes with its center outside it (Sydney's
    # "Sydney" place area at 150.80 E, its "Inner West"; 2026-10-08).
    lats = [p[0] for p in nodes.values()]
    lons = [p[1] for p in nodes.values()]
    extent = (min(lats) - EXTENT_PAD, min(lons) - EXTENT_PAD,
              max(lats) + EXTENT_PAD, max(lons) + EXTENT_PAD) if lats else None
    seen_key = set()
    seen_near = defaultdict(list)             # (kind, name) -> (point, is_area)

    def add(kind, pt, names, langs, bbox=0, area=False, osm=None, ways=None, tags=None):
        key = (kind, names[0], round(pt[0], 3), round(pt[1], 3))
        near = NEAR_DUP_M.get(kind)
        if key in seen_key or (near and any(
                (area or a) and _dist_m(p, pt) <= near for p, a in seen_near[(kind, names[0])])):
            report[f"{kind}_duplicate"] += 1
            if osm:
                note("same_name_near", "merge", osm, names[0], f"a {kind} row of that name is near", tags)
            return
        seen_key.add(key)
        seen_near[(kind, names[0])].append((pt, area))
        # A street's ways (chain_ways), the row's OSM id ("node/123"; None
        # for a street or a river, which are many ways), its languages and
        # its object's tags (the merges after the tagged pass read them) ride
        # along as a 7th to 10th field until the rows are sorted; none is
        # served in the index.
        rows.append([KINDS.index(kind), _r(pt[0]), _r(pt[1]), names[0], "|".join(names[1:]), bbox,
                     ways, osm, set(langs), tags or {}])
        report[kind] += 1

    # --- Streets: every way of one name merged; a name used by streets far
    # apart (two 一番町) is kept apart by a coarse grid of 2 km.
    street_nodes = defaultdict(list)          # (name, cell) -> node ids
    street_ways = defaultdict(list)           # (name, cell) -> (way id, its node ids)
    street_names = {}                         # (name, cell) -> all names
    street_langs = defaultdict(set)           # (name, cell) -> languages
    street_open = defaultdict(bool)           # (name, cell) -> a way the public may use
    # The 2026-10-13 rules, each true once one way of the street clears it:
    # not a private residential way, not a busway or raceway, not a minor way.
    street_public = defaultdict(bool)
    street_real = defaultdict(bool)
    street_major = defaultdict(bool)
    street_nonramp = defaultdict(bool)
    street_nonmotorway = defaultdict(bool)
    street_nonround = defaultdict(bool)
    street_noncustomer = defaultdict(bool)
    square_areas = []                         # pedestrian areas with an article of their own
    way_tags = {w["id"]: w.get("tags", {}) for w in ways} if log is not None else {}
    node_streets = defaultdict(set)           # node id -> street display names
    for w in ways:
        # A way a reading by eye found to be a business's or a home's own
        # road (config.PLACE_DROPPED; London's "Momento Hayes - Parking
        # Approach Road", a development's drive drawn highway=residential).
        if f"way/{w['id']}" in dropped:
            report["street_way_dropped_by_id"] += 1
            continue
        t = w.get("tags", {})
        names = _local_first(t, _names(t, name_tags), read)
        # STREETS BEING REBUILT (owner, 2026-10-11): highway=construction is
        # skipped because most such ways are roads not yet open (Hong Kong's
        # D1 to D7), and no tag tells those from a street closed for
        # rebuilding (Tbilisi's Rustaveli Avenue, all 22 of its ways). A city
        # names the second kind in config.PLACE_REBUILT, by name with why and
        # the date; a name no construction way in the cache carries stops the
        # step (build_city), so an entry retires when the street reopens.
        # A highway tag can list two values (Minneapolis's bus platforms,
        # highway=platform;bus_stop, 4 ways indexed under two station names;
        # the second batch, 2026-10-13): each is read. Under whatever name,
        # a real street's included: the ten Miami platforms and seven
        # Washington proposed ways wave 1 listed by id were skipped already,
        # their streets' rows coming from the streets' own ways.
        hw = {v.strip() for v in str(t.get("highway") or "").split(";")}
        if t.get("highway") == "construction" and any(n in rebuilt for n in names):
            report["street_way_kept_rebuilt"] += 1
        elif t.get("public_transport") == "platform" or t.get("railway") == "platform":
            # A STOP'S PLATFORM IS NO STREET, whatever highway value it
            # carries (a fault mended, 2026-10-13: SKIP_HIGHWAY read
            # highway=platform alone, and Milan's 527 footways tagged
            # public_transport=platform, named for their stops, were street
            # rows). The stop's own row is its station's.
            report["street_way_skipped_platform"] += 1
            continue
        elif (hw & SKIP_HIGHWAY or t.get("area") == "yes"
                or t.get("service") in SKIP_SERVICE):
            report["street_way_skipped"] += 1
            if names and t.get("highway") not in SKIP_HIGHWAY and t.get("area") != "yes" \
                    and t.get("service") not in SKIP_SERVICE:
                report["street_way_skipped_listed_value"] += 1
                note("street_way_listed_value", "drop", f"way/{w['id']}", names[0],
                     f"highway={t.get('highway')}", t, ways=[w["id"]])
            # A PEDESTRIAN SQUARE DRAWN AS AN AREA is no street, and is a
            # landmark when it has an article of its own (owner, 2026-10-13:
            # 47 such areas on the 19 had no row at all; a rest area stays
            # out). Read after the tagged pass, as a square is; one that is
            # also tagged place=* is read there already.
            if (t.get("highway") == "pedestrian" and t.get("area") == "yes" and t.get("wikipedia")
                    and names and not (t.get("place") and "center" in w)):
                square_areas.append((w, t, names))
            continue
        if (t.get("highway") in MINOR_HIGHWAYS and not (t.get("wikidata") or t.get("wikipedia"))
                and not _reads_as_way(names, local, way_words)
                and not (t.get("access") in ("private", "no") and _private_street(names, local))):
            report["minor_way_dropped_not_a_way_name"] += 1
            continue
        # A road named for private or parking access, or a business, is no
        # street to search; a name of that kind beside a real one is dropped
        # alone (Vancouver's "26 Avenue", alt_name "Private Access", 2026-10-08).
        # One that reads as a street keeps its name (_named_street), on a
        # street of residential class or above only: a minor way named for a
        # business stays out (Seoul's "힐스테이트 상가진입로", a shopping
        # arcade's entry road, and "Road to 113/114 Parking Lot"; batch 2b
        # audit, 2026-10-08).
        minor = t.get("highway") in MINOR_HIGHWAYS
        kept = [n for n in names if (not leak_word([n], local) if minor else _named_street(n, local))]
        if names and not kept:
            report["street_dropped_leak_word"] += 1
            continue
        if len(kept) < len(names):
            report["street_name_dropped_leak_word"] += 1
        names = kept
        if not names:
            continue
        pts = [nodes[n] for n in w["nodes"] if n in nodes]
        if not pts:
            report["street_way_no_nodes"] += 1
            continue
        mid = pts[len(pts) // 2]
        cell = (names[0], int(mid[0] / 0.018), int(mid[1] / 0.022))
        street_nodes[cell].extend(w["nodes"])
        street_ways[cell].append((w["id"], w["nodes"]))
        prev = street_names.get(cell, [])
        street_names[cell] = prev + [n for n in names if n not in prev]
        street_langs[cell] |= langs_of(t)
        shut = t.get("access") in ("private", "no") and t.get("foot") not in FOOT_OPEN
        street_open[cell] |= not (minor and shut
                                  and not (t.get("wikidata") or t.get("wikipedia"))
                                  and not _private_street(names, local))
        way_article = bool(t.get("wikipedia")) and article(w, t, names, mid, way=True)[0] == "own"
        street_public[cell] |= not (shut
                                    and (t.get("highway") in PRIVATE_STREET_HIGHWAYS
                                         or t.get("service") in PRIVATE_STREET_SERVICES)
                                    and not way_article and not _private_street(names, local))
        # The second batch's tests (2026-10-13), each true once one way of
        # the street is NOT of the class: a ramp-class way, a motorway's
        # way, a roundabout's way.
        street_nonramp[cell] |= not hw <= RAMP_HIGHWAYS
        street_nonmotorway[cell] |= not hw <= MOTORWAY_HIGHWAYS
        street_nonround[cell] |= t.get("junction") not in ROUNDABOUT_JUNCTIONS
        street_noncustomer[cell] |= not (t.get("highway") == "service" and t.get("access") == "customers"
                                         and not way_article)
        street_real[cell] |= way_article or not (
            {v.strip() for v in str(t.get("highway") or "").split(";")} & NOT_STREET_HIGHWAYS)
        street_major[cell] |= not minor or bool(t.get("wikidata") or t.get("wikipedia"))
        for n in w["nodes"]:
            node_streets[n].add(names[0])
    # Neighbouring cells of one name are one street: merge cells that share a node.
    by_name = defaultdict(list)
    for cell in street_nodes:
        by_name[cell[0]].append(cell)
    street_alias = {}                         # display name -> its English-ish aliases
    street_lang = {}                          # display name -> its languages
    for name, cells in by_name.items():
        groups = []
        for cell in cells:
            ids = set(street_nodes[cell])
            hit = [g for g in groups if g[0] & ids]
            merged = [ids, list(street_names[cell]), set(street_langs[cell]), street_open[cell],
                      list(street_ways[cell]), street_public[cell], street_real[cell],
                      street_major[cell], street_nonramp[cell], street_nonmotorway[cell],
                      street_nonround[cell], street_noncustomer[cell]]
            for g in hit:
                merged[0] |= g[0]
                merged[1] += [n for n in g[1] if n not in merged[1]]
                merged[2] |= g[2]
                merged[3] |= g[3]
                merged[4] += g[4]
                for k in range(5, 12):
                    merged[k] |= g[k]
                groups.remove(g)
            groups.append(merged)
        # KEPT all the same (owner, 2026-10-11, on what the rule took in
        # Paris, Marseille and Brussels: "keep those streets"): a private
        # street NAMED as a residential street (PRIVATE_STREET_LEAD: Villa
        # Mozart, Cité Bergère, Impasse des Éperonniers), an address a
        # visitor can stand at the gate of.
        # PRIVATE MINOR WAYS (owner, 2026-10-11): a street whose every way is
        # a footway, path, track or service road with access=private or no,
        # none of them notable, is no street to search: airport and campus
        # service roads, military-base streets, gated communities (1 to 3% of
        # street rows in the 2b cities). Its crossings go with it. access=no
        # on a trail can also be a CLOSURE (Hong Kong's country-park paths):
        # noted for the audit after the rollout, not told apart here.
        shut = [g for g in groups if not g[3]]
        for g in shut:
            report["street_dropped_private_minor"] += 1
            for n in g[0]:
                node_streets[n].discard(name)
        groups = [g for g in groups if g[3]]
        # The 2026-10-13 rules (PRIVATE_STREET_HIGHWAYS, NOT_STREET_HIGHWAYS,
        # street_description), each asked of the whole street: one way that
        # clears a rule keeps every way of the street. Crossings go with a
        # dropped street, as above.
        described = street_description(name, local)
        # The second batch (2026-10-13): a name that is no street's whatever
        # its ways (street_never), a ramp's name on ramp-class ways, a
        # circular junction on a motorway's ways, a managed lane's label on
        # motorway ways. A named roundabout stays while ROUNDABOUTS_STAY.
        never = street_never(name)
        if keep_interchanges and never == "interchange":
            never = None
        plain = _plain(name)
        for g in list(groups):
            round_ = not g[10]
            private = not g[5] and (described or not keep_named_private)
            cls = ("private_residential" if private else "customers_only" if not g[11] and name.split()[-1:] and name.split()[-1] in CUSTOMER_ROAD_ENDS
                   else "busway_raceway" if not g[6]
                   else "description" if described and not g[7]
                   else "description" if described in ANY_WAY_DESCRIPTIONS
                   else never if never
                   else "ramp" if not g[8] and RAMP_NAME.search(plain)
                   else "interchange" if round_ and not g[9] and not keep_interchanges
                   else "managed_lane" if not g[9] and MANAGED_LANE.search(plain)
                   else "roundabout" if round_ and not ROUNDABOUTS_STAY else None)
            if cls is None:
                if round_:
                    report["street_roundabout_kept"] += 1
                continue
            report[f"street_dropped_{cls}"] += 1
            if log is not None:
                first = min(g[4])[0]
                pts = [nodes[n] for n in g[0] if n in nodes]
                note(f"street_{cls}", "drop", f"way/{first}", name,
                     (described if cls == "description" else "") + f" ({len(g[4])} way(s))",
                     way_tags.get(first),
                     bbox=[_r(min(q[0] for q in pts)), _r(min(q[1] for q in pts)),
                           _r(max(q[0] for q in pts)), _r(max(q[1] for q in pts))],
                     ways=sorted(i for i, _ in g[4]))
            for n in g[0]:
                node_streets[n].discard(name)
            groups.remove(g)
        if not groups:
            continue
        for ids, names, langs, _open, group_ways, *_flags in groups:
            pts = [nodes[n] for n in ids if n in nodes]
            s, w_ = min(p[0] for p in pts), min(p[1] for p in pts)
            n_, e = max(p[0] for p in pts), max(p[1] for p in pts)
            c = ((s + n_) / 2, (w_ + e) / 2)
            anchor = min(pts, key=lambda p: _dist_m(p, c))
            add("street", anchor, names, langs, [_r(s), _r(w_), _r(n_), _r(e)], ways=group_ways)
        street_alias[name] = [n for g in groups for n in g[1]]
        street_lang[name] = set().union(*(g[2] for g in groups))

    # --- Crossings: two street names meeting at a shared node ("5th and
    # Pike"). One row per pair, unless the pair meets again far away.
    pair_pts = defaultdict(list)
    crossings = []                            # (point, street A, street B, languages)
    for n, names in node_streets.items():
        if len(names) < 2 or n not in nodes:
            continue
        names = sorted(names)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                pair_pts[(names[i], names[j])].append(nodes[n])
    for (a, b), pts in pair_pts.items():
        clusters = []
        for p in pts:
            for cl in clusters:
                if _dist_m(cl[0], p) <= CROSSING_MERGE_M:
                    cl.append(p)
                    break
            else:
                clusters.append([p])
        for cl in clusters:
            # The display pairs the local names; the alias pairs the English
            # ones, so "Shijo Karasuma" finds 四条通 / 烏丸通.
            # Kept by the two street names, each resolved to its row below;
            # in a language only where both streets are.
            crossings.append((cl[0], a, b, street_lang.get(a, set()) & street_lang.get(b, set())))

    # --- Tagged places.
    rivers = defaultdict(list)
    held_by_wikidata = {}                     # OSM id -> the item that alone admits its row
    item_ids = defaultdict(set)               # wikidata value -> the objects that carry it
    for e in elements:
        for wd in str((e.get("tags") or {}).get("wikidata") or "").split(";"):
            if wd.strip():
                item_ids[wd.strip()].add((e["type"], e["id"]))

    def own_item(t):
        """True when `t` carries one Wikidata entry no other object of the
        cache carries, and it is not its subject's, brand's or operator's."""
        wd = (t.get("wikidata") or "").strip()
        if not wd or ";" in wd or len(item_ids[wd]) != 1:
            return False
        return not any(wd in [v.strip() for v in (t.get(f"{k}:wikidata") or "").split(";")]
                       for k in _SUBJECT_KEYS)

    # The second batch (2026-10-13). A register number SHARED_REGISTER_MIN or
    # more objects carry is their district's (own_register); the settlements
    # drawn as nodes name the boundaries that repeat them (rule 10).
    register_ids = defaultdict(set)
    settlement_nodes = set()
    district_nodes = defaultdict(list)        # (place value, folded name) -> node points
    for e in elements:
        t = e.get("tags") or {}
        ref = (t.get("ref:nrhp") or "").strip()
        if ref:
            register_ids[ref].add((e["type"], e["id"]))
        if e["type"] == "node" and t.get("place") in SETTLEMENTS and not (
                extent and not (extent[0] <= e["lat"] <= extent[2] and extent[1] <= e["lon"] <= extent[3])):
            ns = _local_first(t, _names(t, name_tags), read)
            if ns:
                settlement_nodes.add(fold_name(ns[0]))
        # A suburb's or a borough's node (BOUNDARY_NODE_M; the sixth pass).
        elif e["type"] == "node" and t.get("place") in BOUNDARY_DUP_PLACES:
            ns = _local_first(t, _names(t, name_tags), read)
            if ns:
                district_nodes[(t["place"], fold_name(ns[0]))].append((e["lat"], e["lon"]))
    district_refs ={ref for ref, ids in register_ids.items() if len(ids) >= SHARED_REGISTER_MIN}

    def own_register(t):
        """`t` less a register number its district shares: only a
        registration of the object's own keeps a coded name."""
        if (t.get("ref:nrhp") or "").strip() in district_refs:
            return {k: v for k, v in t.items() if k not in ("ref:nrhp", "heritage")}
        return t

    def landmark_drop(t, names, oid, own, kept=None):
        """(reason, names) for a landmark the rules drop, the reason a
        report key's ending; (None, names less their bare aliases) for one
        they keep. `own`: the object has an article of its own (the fame
        test), which keeps it against five of the tests (owner, 2026-10-13);
        each such keep is appended to `kept`. No side effect, so the caller
        can ask again with a tag taken away."""
        kept = [] if kept is None else kept
        rt = own_register(t)
        if bare_type(names[0], local, rt) and oid in kept_ids:
            kept.append("by_id")
        elif bare_type(names[0], local, rt):
            # KEPT on an article of its own (81 measured, 69 of them Paris's
            # Édicule Guimard, whose article is the type's and shared): not
            # where the article's title is the bare word itself, the type's
            # article (London's "Lych Gate", en:Lychgate).
            if not (own and fold_name(article_title(t["wikipedia"])) != fold_name(names[0])):
                return "bare_type", names
            kept.append("bare_type")
        names = names[:1] + [n for n in names[1:] if not bare_type(n, local, rt)] if kept else \
            [n for n in names if not bare_type(n, local, rt)]
        # NAMED ONLY BY ITS DENOMINATION OR HALL TYPE (worship_only; owner,
        # 2026-10-13, the fifth pass). Kept by id, or on an article of its
        # own, whatever the article's title: London's Friends Meeting House
        # and its synagogues stand under articles named as they are.
        # A RELIGIOUS OFFICE, HALL OR RESIDENCE (worship_office; the sixth
        # pass) is held to the same test. An entry of the object's own with
        # an article in the city's Wikidata cache keeps a row too (owner,
        # 2026-10-13); the cache is read where it holds the entry and is not
        # asked for it (article_lookup_kind stays public art and libraries).
        worship = (None if t.get("amenity") != "place_of_worship" or not names
                   else "worship_type" if worship_only(names[0], local)
                   else "worship_office" if worship_office(names[0], local) else None)
        if worship:
            if oid in kept_ids:
                kept.append("by_id")
            elif own or has_article(t, articles, own_entry=own_item(t)):
                kept.append(worship)
            else:
                return worship, names
        if _exhibit(t) or (t.get("historic") in EXHIBIT_HISTORIC and not own_item(t)) or (
                t.get("historic") in RAIL_EXHIBITS and not (t.get("tourism") or _titled_by_name(t))):
            return "exhibit", names
        why = _commercial_reasons(t)
        if why:
            # KEPT on an article of its own where the only business sign is a
            # private operator or an office tag (115 measured: private
            # universities and museums, parliaments, town halls). A brand, a
            # shop or a lodging tag still keeps a row out (the Panama Hotel
            # precedent: the building, never the business).
            if not (own and set(why) <= KEPT_COMMERCIAL_REASONS):
                return "commercial", names
            kept.append("commercial")
        # A PARK AN APARTMENT ESTATE RUNS (the third list, 2026-10-13): a
        # leisure=park whose operator names an apartment estate or its
        # management office is the estate's own ground. A park tied to an
        # estate only by its name stays.
        if t.get("leisure") == "park" and ESTATE_OPERATOR.search(t.get("operator") or ""):
            return "estate_park", names
        # A FACILITY OF AN APARTMENT ESTATE OR A MALL (estate_facility; the
        # sixth pass). An article of its own, or an id in PLACE_KEPT, keeps it.
        facility = estate_facility(t, names, local)
        if facility and not own and oid not in kept_ids:
            return "estate_facility", names
        if (any(k in t for k in NOTABLE_ONLY) and t.get("amenity") != "place_of_worship"
                and not (t.get("wikidata") or t.get("wikipedia"))):
            return "not_notable", names
        # NOT a rule that a tourism=gallery needs a Wikipedia TAG (measured
        # 2026-10-11, after the owner's yes): it removed the Seoul Museum
        # of Art, Busan's city art museum, Vancouver's Bill Reid Gallery,
        # Sydney's S.H. Ervin Gallery, Kew's Marianne North Gallery and
        # the Grand Palais's national galleries, public galleries whose
        # OSM objects carry wikidata and no wikipedia tag. Dealers'
        # galleries are dropped by id (config.PLACE_DROPPED). Put back to
        # the owner.
        # A home is never a landmark (_home), unless public (_public_home:
        # a former residence that is now a museum) or listed as visitable
        # today with a dated source (config.PLACE_VISITABLE). Kyoto's condominium
        # grounds were tagged leisure=park on landuse=residential
        # (2026-10-07); Vancouver's register of heritage houses carries the
        # names of the families who built them (2026-10-08).
        if _home(t, names, local) and not _public_home(t) and oid not in visitable:
            # KEPT on an article of its own where access=private is the only
            # home sign and the object is no garden, park or palace (a
            # university, a library, a monument behind a fence: 11 rows on
            # the 19; "about 16" by eye, the rest undecidable by tag). A home
            # with its own article stays out (owner, 2026-10-13: 294 rows).
            if not (own and _private_access_only(t, names, local)):
                return "residential", names
            kept.append("residential")
        # A landmark named as a bare Japanese personal name (the map's sign
        # rule, japan_register.bare_personal_name: a common surname, a space,
        # a given name) is someone's house or grave, unless public. The
        # Korean rule (korean_names.looks_like_personal_name) is NOT used:
        # without its address test it reads 이태원 and 강남역 as people.
        if "ja" in local and not _public_home(t) and oid not in visitable and any(_bare_personal(n) for n in names):
            return "personal_name", names
        # A garden is often a private one at a house, and may carry a
        # person's own name ("Aoyama's Garden", Kyoto, 2026-10-07): kept only
        # when notable (wikidata, wikipedia or a heritage designation), and
        # a residential garden never.
        if t.get("leisure") == "garden" and (
                t.get("garden:type") == "residential"
                or not (t.get("wikidata") or t.get("wikipedia") or t.get("heritage"))):
            return "garden", names
        # A landmark named for a business or a home is one, unless public
        # in _public_home's sense or a ruin (then check_place_search.py E
        # asks for a review): Sydney's "Serviced Apartments Park", a
        # leisure=park; Chicago's landmark apartment buildings, homes
        # whatever their designation; Kyoto's 愛宕山ホテル跡, a hotel's
        # ruins, stays (2026-10-08).
        # A business word may pass on a Wikipedia article (a landmark
        # building, reviewed by name); a home word may not. PRECEDENT
        # (owner, 2026-10-08, Seattle's Panama Hotel): a notable historic
        # building that still houses the business its name carries is
        # kept, as a historic site, the building and not the business; one
        # tagged as the business itself (amenity=casino, tourism=hotel)
        # stays out (_commercial). Homes with an article stay out.
        word = leak_word(names, local, landmark=True)
        home_word = word in {w for c in (["en", *local]) for w in HOME_WORDS.get(c, ())}
        if word and not (
                _public_home(t) or oid in visitable or t.get("historic") in ("ruins", "archaeological_site")
                or (t.get("wikipedia") and not home_word)):
            return "leak_word", names
        if t.get("waterway"):
            # A river comes as one row per way; merged by name by the caller.
            return None, names
        # A Stolperstein names one person at their last home ("Zde bydlela
        # Irma Kohnová", here lived ...): a private person at a home, never
        # a place to search, whatever its wikidata item (Prague's came in
        # bulk from the small-monuments register; batch 2a, 2026-10-08).
        # A Stolperschwelle is one too (the third list, 2026-10-13:
        # memorial=stolperschwelle, artwork_type=stolperstein).
        if t.get("memorial") in STOLPERSTEIN_MEMORIALS or t.get("artwork_type") == "stolperstein":
            return "stolperstein", names
        if t.get("historic") == "tomb" and any(FAMILY_TOMB.match(n.strip()) for n in names):
            return "family_tomb", names
        if t.get("historic") in SKIP_HISTORIC and not any(
                t.get(k) for k in ("tourism", "amenity", "leisure", "wikidata")):
            # KEPT on an article of its own though it has no Wikidata entry
            # (23 measured; 6 pass the fame test, the others carry their
            # subject's article, a section, or one the tags cannot place).
            if not own:
                return "minor_historic", names
            kept.append("minor_historic")
        return None, names

    def landmark(e, t, names, pt, langs, square_like=False):
        """One landmark candidate through the rules: a row, a river segment,
        or a counted drop."""
        oid = f"{e['type']}/{e['id']}"
        seen_tags = t
        verdict, why = article(e, t, names, pt)
        own = verdict == "own"
        # THE SUBJECT'S ENTRY IS NOT THE OBJECT'S (candidate 38, owner
        # 2026-10-13): a wikidata tag equal to the object's subject:wikidata
        # admits it to nothing (SUBJECT_ENTRY_KEYS; a bench under the
        # entry of the poet it is named for).
        wd = (t.get("wikidata") or "").strip()
        subject = wd and next((k for k in SUBJECT_ENTRY_KEYS if wd in [
            v.strip() for v in (t.get(f"{k}:wikidata") or "").split(";")]), None)
        if subject:
            t = {k: v for k, v in t.items() if k != "wikidata"}
        # A BRIDGE'S OWN NAME (owner, 2026-10-13): a registered bridge drawn
        # on a road came in under the road's name ("Aurora Avenue North" for
        # Seattle's Aurora Bridge). bridge:name leads (_bridge_led). A
        # street's way reaches here only when no street row bears the name
        # it would have as a landmark (the tagged pass).
        led = _bridge_led(t, names)
        if led is not names:
            note("bridge_name", "rename", oid, led[0], f"was {names[0]}", t)
            names = led
            report["landmark_named_by_bridge_name"] += 1
        life = lifecycle(t, retrieved)
        if life:
            # Read narrowly (logged in the drafts file, flagged for the
            # owner): an ABANDONED object with a historic tag is a historic
            # site and is there (Hong Kong's wartime pillboxes, Shing Mun
            # Redoubt); a NOT-YET-OPEN one that is historic, listed or has a
            # start date behind it is being rebuilt, and is there too.
            if life[0] == "both":
                note("not_there_kept", "kept", oid, names[0], f"{life[1]}: live and prefixed alike", t)
            # CLOSED FOR WORKS, BY ID (owner, 2026-10-13, on the first
            # changed-row report: a museum and a library closed for
            # renovation and a playground being rebuilt are there). No tag
            # separates them from a place not yet built: the three carry
            # three different tags and none of historic, heritage or a start
            # date. Only the not-yet-open class; a demolished object is never
            # kept this way.
            elif life[0] == "ahead" and oid in closed_for_works:
                note("not_there_kept", "kept", oid, names[0], f"{life[1]}: closed for works, by id", t)
            elif life[0] == "abandoned" and t.get("historic"):
                note("not_there_kept", "kept", oid, names[0], f"{life[1]}: a historic site", t)
            # A DISUSED PLACE OF WORSHIP WITH AN ARTICLE OR AN ENTRY OF ITS
            # OWN STAYS (owner, 2026-10-13, the abandoned-landmark ruling):
            # it stands. Montreal's Saint-Enfant-Jesus du Mile-End.
            elif life[1].startswith("disused=yes") and (own or own_item(t)):
                note("not_there_kept", "kept", oid, names[0], f"{life[1]}: an article or entry of its own", t)
            elif life[0] == "ahead" and (t.get("historic") or t.get("heritage")
                                         or _past(t.get("start_date"), retrieved)):
                note("not_there_kept", "kept", oid, names[0], f"{life[1]}: a rebuilding", t)
            else:
                report["landmark_dropped_not_there"] += 1
                note("not_there", "drop", oid, names[0], f"{life[0]}: {life[1]}", t)
                return
        # THE THIRD LIST (2026-10-13): a dead railway alignment (18), and
        # public art without a Wikipedia article of its own (16).
        dead = e["type"] == "way" and dead_railway(t)
        if dead:
            report["landmark_dropped_dead_railway"] += 1
            note("dead_railway", "drop", oid, names[0], dead, t)
            return
        # Rule 16 and rule 39 (a library is a landmark only with an article
        # of its own; owner, 2026-10-13: "same rule") ask has_article: the
        # wikipedia tag as before, else the Wikidata cache.
        needs = article_lookup_kind(t)
        # AN ARTICLE UNDER THE OBJECT'S OWN NAME IS ITS OWN here, whatever
        # subject tag repeats it (found 2026-10-13 with the caches read):
        # Chicago's mappers copy a work's own article into subject:wikipedia,
        # and Cloud Gate (en:Cloud Gate) read as its subject's and left. A
        # work whose entry is copied into subject:wikidata with no article
        # under its name is still not told apart from a statue of its
        # subject (Tokyo's Maman, Chicago's Sue): those go, and are listed.
        if needs and verdict == "not" and _titled_by_name({**seen_tags, "name": names[0]}):
            needs = None
        # Kept by id against this rule too (config.PLACE_KEPT; owner,
        # 2026-10-13, "yes if not costly"): a known work whose entry has no
        # article in any language, or is copied into its subject tag.
        if oid in kept_ids:
            needs = None
        if needs and verdict in ("none", "not"):
            mine = own_item(seen_tags)
            if mine:
                asked.add(seen_tags["wikidata"].strip())
            if not has_article(seen_tags, articles, own=False, own_entry=mine):
                report[f"landmark_dropped_{needs}_no_article"] += 1
                note(f"{needs}_no_article", "drop", oid, names[0], why or "no article on the tag or in Wikidata", t)
                return
        # REGISTER AND INVENTORY ENTRIES (REGISTER_HISTORIC; the second
        # batch, 2026-10-13): an article of the object's own, or no row.
        if t.get("historic") in REGISTER_HISTORIC and not own and oid not in kept_ids and not (
                t["historic"] in REGISTER_ITEM_VALUES and own_item(t)):
            report["landmark_dropped_register_entry"] += 1
            note("register_entry", "drop", oid, names[0], f"historic={t['historic']}, no article of its own", t)
            return
        # STANDING BUT ABANDONED OR RUINED (ABANDONED_NEED_ARTICLE).
        standing = not own and _abandoned_standing(t)
        if standing and ABANDONED_NEED_ARTICLE:
            report["landmark_dropped_abandoned"] += 1
            note("abandoned_no_article", "drop", oid, names[0], standing, t)
            return
        # PERSONAL NAMES (owner, 2026-10-13): a grave or a plaque is kept
        # only on a Wikipedia article of its own; its Wikidata entry alone
        # admits it no longer (258 graves and 241 plaques were in on a key).
        # Nothing in the data tells a private person from a public one, which
        # is why the article is the test. Statues, busts and public
        # memorials are untouched. Where the tags cannot say whose the
        # article is, the row stays as it was and is listed (never a guess).
        person = grave_or_plaque(t)
        stripped = None
        if person and (t.get("wikidata") or t.get("wikipedia")):
            if not own and verdict != "undecided":
                stripped = why or "a Wikidata entry and no article"
                t = {k: v for k, v in t.items() if k not in ("wikidata", "wikipedia")}
        kept = []
        reason, names = landmark_drop(t, names, oid, own, kept)
        # Kept by id (config.PLACE_KEPT) against the landmark tests as well:
        # Tokyo's Maman carries its entry as its subject's too, and left here
        # as a work with no entry of its own (2026-10-13).
        if reason and oid in kept_ids and t.get("tourism") == "artwork":
            reason = None
        if reason:
            report[f"landmark_dropped_{reason}"] += 1
            if log is not None and subject and landmark_drop(seen_tags, names, oid, own)[0] is None:
                note("subject_entry", "drop", oid, names[0], f"wikidata is its {subject}'s", seen_tags)
            elif log is not None:
                if stripped and landmark_drop(seen_tags, names, oid, own)[0] is None:
                    note(f"{person}_no_own_article", "drop", oid, names[0], stripped, seen_tags)
                elif reason in ("worship_type", "worship_office", "estate_facility"):
                    note(reason, "drop", oid, names[0],
                         {"worship_type": "named only by its denomination, chain or hall type",
                          "worship_office": "a religious office, hall or residence by its name",
                          "estate_facility": estate_facility(t, names, local) or ""}[reason], t)
                elif verdict == "undecided" and reason in ("bare_type", "minor_historic"):
                    note("keep_undecided", "left out", oid, names[0], f"{reason}: {why}", t)
                elif own and reason == "residential" and _home_signs(t, names, local) == ["access"]:
                    note("keep_undecided", "left out", oid, names[0],
                         "access=private on a garden, a park or a palace: a home or not, "
                         "the tags cannot tell", t)
                elif reason == "bare_type":
                    note("bare_type", "drop", oid, names[0], "a bare type word, or a code beside one", t)
            return
        for k in kept:
            note(f"kept_{k}", "keep", oid, names[0], "an article of its own", t)
        if t.get("waterway"):
            # A river comes as one row per way; merged by name below.
            rivers[names[0]].append((pt, names, langs, oid))
            return
        if t.get("wikidata") and not kept:
            less = {k: v for k, v in t.items() if k != "wikidata"}
            if landmark_drop(less, names, oid, own)[0] is not None:
                held_by_wikidata[oid] = t["wikidata"]
        before = len(rows)
        add("landmark", pt, names, langs, area=e["type"] != "node", osm=oid, tags=seen_tags)
        if len(rows) > before:
            if standing:
                note("abandoned_standing", "measure", oid, names[0], standing, t)
            if person and verdict == "undecided":
                note(f"{person}_undecided", "kept", oid, names[0], why, t)
            if t.get("place") in ISLAND_VALUES:
                note("kept_island", "keep", oid, names[0], "an article of its own", t)
            if square_like:
                note("kept_square_area", "keep", oid, names[0], "an article of its own", t)
            if t.get("place") == "square" or square_like:
                square_rows.append(rows[-1])
            elif t.get("leisure") == "park" and square_led(names[0], local):
                park_square_rows.append(rows[-1])

    for e in tagged:
        t = e.get("tags", {})
        names = _local_first(t, _names(t, name_tags), read)
        pt = _point(e)
        if not names or not pt:
            continue
        if extent and not (extent[0] <= pt[0] <= extent[2] and extent[1] <= pt[1] <= extent[3]):
            report["outside_area"] += 1
            continue
        langs = langs_of(t)
        oid = f"{e['type']}/{e['id']}"
        # The second batch (2026-10-13): a name that says the thing is gone
        # (HISTORICAL_NAME; 5 rows in wave 1, none on the 19), and a stop-area
        # relation, which groups a station's parts (20 station rows: wave 1
        # 15, Montreal 4, Vancouver 1; 18 beside the station's own row).
        if HISTORICAL_NAME.search(names[0]):
            report["dropped_historical_name"] += 1
            note("historical_name", "drop", oid, names[0], "the name says it is gone", t)
            continue
        stop_area = e["type"] == "relation" and t.get("public_transport") == "stop_area"
        if stop_area and not t.get("railway"):
            report["station_skipped_stop_area"] += 1
            note("station_stop_area", "drop", oid, names[0], "public_transport=stop_area, no railway tag", t)
            continue
        station = t.get("railway") in ("station", "halt", "tram_stop") or t.get("public_transport") == "station"
        # A RAILWAY LINE IS NO STATION, AND NEITHER IS A SCHOOL (faults
        # mended, 2026-10-13): a route relation tagged public_transport=
        # station (the 山陽新幹線 in Hiroshima and Kakogawa), and an object
        # with no railway tag whose amenity is a school's (NOT_STATION_AMENITY;
        # Yao's 八尾市立東中学校 with a stray station=subway). The school goes
        # on to the landmark rules. NOT built: asking every station row for a
        # railway tag, which Kyoto's 鞍馬駅 and Seattle's South Bellevue lack.
        if station and e["type"] == "relation" and t.get("type") == "route":
            report["station_skipped_route_relation"] += 1
            note("station_route_relation", "drop", oid, names[0], "type=route", t)
            continue
        if station and not t.get("railway") and t.get("amenity") in NOT_STATION_AMENITY:
            station = False
        rail_mode = any(t.get(k) == "yes" for k in RAIL_MODES)
        if (t.get("public_transport") == "station" and not t.get("railway")
                # A bus station is no rail station whatever rail mode it
                # lists (the second batch, 2026-10-13: Dallas's three, tagged
                # light_rail=yes or train=yes beside their stations' rows).
                and (t.get("amenity") == "bus_station"
                     or (not rail_mode
                         and (any(t.get(k) not in (None, "no") for k in OTHER_MODES)
                              or any(t.get(k) in v for k, v in NOT_RAIL.items()))))):
            # A bus or ferry terminal, or a tour boat's dock ("Wendella
            # Tours - Michigan Avenue", Chicago, 2026-10-08): no station.
            report["station_skipped_not_rail"] += 1
            if rail_mode:
                note("station_bus_station", "drop", oid, names[0], "amenity=bus_station, no railway tag", t)
            continue
        lifecycle_tag = next((f"{k}={t[k]}" for k in ("proposed", "construction") if t.get(k) == "yes"), None) \
            or next((f"{k}={t[k]}" for k in ("proposed:railway", "construction:railway",
                                             "proposed:public_transport", "construction:public_transport")
                     if t.get(k)), None) \
            or (f"opening_date={t['opening_date']}" if _future(t.get("opening_date"), retrieved) else None)
        if station and (t.get("railway") in ("construction", "proposed", "disused", "abandoned", "razed")
                        or lifecycle_tag):
            # Busan's seven light-rail stations under construction carry
            # public_transport=station already (2026-10-08): not yet a
            # station. Stations only: Prague's historic horse railway
            # (railway=abandoned) is a landmark. The lifecycle tags are read
            # too: five proposed stops of the Texcoco-La Paz light rail carry
            # railway=prpopsed, a typo no list of values holds, beside
            # proposed=yes and proposed:railway=stop (Mexico City, 2026-10-12).
            # Since 2026-10-13 on any station or stop (construction=yes on a
            # railway=tram_stop) and with opening_date after the cache.
            report["station_skipped_not_open"] += 1
            tag = (f"railway={t['railway']}"
                   if t.get("railway") in ("construction", "proposed", "disused", "abandoned", "razed")
                   else lifecycle_tag)
            not_open.append({"osm": oid, "name": names[0], "tag": tag})
            if t.get("public_transport") != "station" or tag.startswith("opening_date"):
                note("station_not_open", "drop", oid, names[0], tag, t)
            continue
        if t.get("emergency") == "designated" and (t.get("railway") or t.get("public_transport")):
            # A platform for emergency use only (Hong Kong's Light Rail
            # "Hung Tin Road Emergency Platform", 2026-10-08): no station.
            report["station_skipped_emergency"] += 1
            continue
        if station:
            # The 2026-10-13 station rules (station_closed, station_ride): a
            # closed station; a ride; a business or a bare type word tagged a
            # station with no rail tag at all (a car park named for its
            # station, a ticket shop: 5 rows) or with no registered key (a
            # temple's slope car halt named 本堂: 1 row). Each is dropped,
            # never passed on to the landmark rules.
            # An ending a city's stops carry in OSM and its map does not
            # (config.PLACE_STATION_STRIP; Cluj-Napoca's tram stops end " Tram").
            for end in station_strip:
                names = list(dict.fromkeys(n[:-len(end)].rstrip() if n.endswith(end) and len(n) > len(end) else n
                                           for n in names))
            closed = station_closed(t, retrieved)
            # A station the map draws, at its place and under its name, is
            # not closed by a disused tag (drawn_station_here); a dated
            # closure still closes it.
            if closed and not _past(t.get("end_date"), retrieved) and drawn_station_here(names, pt, drawn_at):
                note("station_closed_tag_drawn", "kept", oid, names[0], f"{closed}, a station of the map", t)
                closed = None
            # A station kept by id (config.PLACE_KEPT; Taoyuan's 新富, a halt
            # tagged access=private) is admitted at the end of the build,
            # whatever these tests say.
            # NO PASSENGERS, NO STATION (candidate 42, owner 2026-10-13):
            # passenger=no or public_transport=no on a station is a freight
            # or works halt. A station the map draws stays (the guard).
            if not closed and (t.get("passenger") == "no" or t.get("public_transport") == "no") \
                    and fold_name(names[0]) not in drawn:
                closed = "passenger=no" if t.get("passenger") == "no" else "public_transport=no"
            # CLOSED TO THE PUBLIC, NO STATION ROW (STATION_PRIVATE_ACCESS;
            # owner, 2026-10-13, the fifth pass). A station the map draws
            # stays (the guard).
            if not closed and t.get("access") in STATION_PRIVATE_ACCESS and fold_name(names[0]) not in drawn:
                closed = f"access={t['access']}"
            # NOT IN PASSENGER SERVICE BY ITS OWN WORDS (station_out_of_service;
            # the sixth pass). A station the map draws stays (the guard).
            if not closed and fold_name(names[0]) not in drawn:
                closed = station_out_of_service(t, names, local)
            ride = station_ride(t)
            no_rail = not (t.get("railway") or t.get("station") or any(t.get(k) == "yes" for k in RAIL_MODES))
            skip = (("closed", closed) if closed else ("ride", ride) if ride
                    else ("business", "+".join(_commercial_reasons(t))) if no_rail and _commercial(t)
                    else ("bare_type", "no wikidata or wikipedia")
                    if bare_type(names[0], local) and not (t.get("wikidata") or t.get("wikipedia")) else None)
            # A STATION OF THE MAP OR OF A RAIL NETWORK IS NEVER DROPPED FOR A
            # BARE TYPE NAME (owner, 2026-10-13: every drawn station is
            # searchable). Monterrey's "Sendero", a metro terminus, is a
            # Spanish bare word. Guarded: a name the map draws
            # (STATIONS_CSV, folded), or station=subway, light_rail or train,
            # or a network tag on a railway station, halt or tram stop.
            if skip and skip[0] == "bare_type" and (
                    fold_name(names[0]) in drawn or t.get("station") in RAIL_STATION_VALUES
                    or (t.get("network") and t.get("railway") in ("station", "halt", "tram_stop"))):
                note("station_bare_name_kept", "kept", oid, names[0], "a station of the map or of a rail network", t)
                skip = None
            if skip:
                report[f"station_skipped_{skip[0]}"] += 1
                note(f"station_{skip[0]}", "drop", oid, names[0], skip[1], t)
                continue
            add("station", pt, names, langs, osm=oid, tags=t)
            continue
        # A BUS STOP IS NO LANDMARK AND NO PLACE, whatever other key it
        # carries (a fault mended, 2026-10-13: Nara's bus stop with a stray
        # historic tag). highway=bus_stop only: public_transport=platform
        # also sits on piers and squares that are places.
        if t.get("highway") == "bus_stop":
            report["dropped_bus_stop"] += 1
            note("bus_stop", "drop", oid, names[0], "highway=bus_stop", t)
            continue
        verdict, why = article(e, t, names, pt)
        own = verdict == "own"
        if t.get("place") in PLACE_VALUES or (t.get("place") == "district" and own):
            life = lifecycle(t, retrieved, place=True)
            if life and life[0] == "both":
                note("not_there_kept", "kept", oid, names[0], f"{life[1]}: live and prefixed alike", t)
            elif life:
                report["place_dropped_not_there"] += 1
                note("not_there", "drop", oid, names[0], f"{life[0]}: {life[1]}", t)
                continue
            # A SETTLEMENT'S BOUNDARY IS NOT A SECOND ROW beside its node
            # (the second batch, 2026-10-13): the boundary's center can lie
            # far from the place (New Orleans's, 25 km off in marsh), beyond
            # what NEAR_DUP_M joins. A boundary with no such node keeps its
            # row (a ward), and so does a boundary of any lesser kind: seven
            # of Dublin's townlands are named "Newtown", as a village
            # elsewhere in the county is.
            if (e["type"] != "node" and (t.get("boundary") or t.get("type") == "boundary")
                    and t.get("place") in BOUNDARY_DUP_PLACES
                    and fold_name(names[0]) in settlement_nodes):
                report["place_dropped_boundary_duplicate"] += 1
                note("boundary_duplicate", "drop", oid, names[0], "a settlement node bears the name", t)
                continue
            # A SUBURB'S OR A BOROUGH'S BOUNDARY BESIDE ITS OWN NODE (a fault
            # mended, the sixth pass; BOUNDARY_NODE_M): the node of the same
            # place value and folded name, a closing bracket set aside
            # ("Freguesia (Ilha)"), within the distance.
            if e["type"] != "node" and (t.get("boundary") or t.get("type") == "boundary") \
                    and t.get("place") in BOUNDARY_DUP_PLACES:
                keys = {fold_name(names[0]), fold_name(re.sub(r"\s*\([^()]*\)\s*$", "", names[0]))}
                near = [q for k in keys for q in district_nodes.get((t["place"], k), ())
                        if _dist_m(pt, q) <= BOUNDARY_NODE_M]
                if near:
                    report["place_dropped_boundary_duplicate"] += 1
                    note("boundary_duplicate", "drop", oid, names[0],
                         f"its own {t['place']} node is {round(min(_dist_m(pt, q) for q in near))} m off", t)
                    continue
            # A place drawn as an area on residential land is an estate, its
            # homes' own name ("Kentbrook Apartments", Seattle: 85 of the
            # place areas, 2026-10-08); a place named for a business or a
            # home is one, as a landmark is. A hamlet or village is a
            # settlement whatever its land use: Hong Kong's New Territories
            # villages, 22 drawn on residential land (batch 2b, 2026-10-08);
            # no other built city had one. KEPT on an article of its own
            # (owner, 2026-10-13: 46 rows, 36 in London, to match the estate
            # kept as a point).
            if (e["type"] != "node" and t.get("place") not in SETTLEMENTS
                    and (t.get("landuse") == "residential" or t.get("residential"))):
                # Kept by id too (config.PLACE_KEPT, 2026-10-13: a real
                # neighborhood drawn on residential land).
                if oid in kept_ids:
                    note("kept_estate_area", "keep", oid, names[0], "by id", t)
                elif not own:
                    report["place_dropped_estate"] += 1
                    continue
                note("kept_estate_area", "keep", oid, names[0], "an article of its own", t)
            # A place drawn as an area WITH A HOUSE NUMBER is one address, a
            # building or a block of them: Mexico City's developer towers
            # ("TORRE CADU OASIS") and the 26 numbered sections of one estate
            # (batch 3, 2026-10-11); none in the fourteen built before it.
            if e["type"] != "node" and t.get("place") not in SETTLEMENTS and t.get("addr:housenumber"):
                report["place_dropped_estate"] += 1
                continue
            if any(NUMBERED_BLOCK[c].fullmatch(names[0].strip()) for c in local if c in NUMBERED_BLOCK):
                report["place_dropped_estate"] += 1
                continue
            notable = bool(t.get("wikidata") or t.get("wikipedia"))
            if not notable and any(ESTATE_NAME[c].search(names[0].strip()) for c in ("en", *local)
                                   if c in ESTATE_NAME):
                report["place_dropped_estate"] += 1
                continue
            # ESTATES_NAME and MOBILE_HOME_PARK (the second batch,
            # 2026-10-13), held to the same test.
            estate2 = (None if notable
                       else "estates_plural" if any(ESTATES_NAME[c].search(names[0].strip()) for c in ("en", *local)
                                                    if c in ESTATES_NAME)
                       else "mobile_home_park" if MOBILE_HOME_PARK.search(names[0])
                       or t.get("residential") == "trailer_park" else None)
            if estate2:
                report["place_dropped_estate"] += 1
                note(estate2, "drop", oid, names[0], "no wikidata and no article", t)
                continue
            if t.get("place") == "hamlet" and not notable and _population(t) is not None \
                    and _population(t) < HAMLET_MIN_POPULATION:
                report["place_dropped_small_hamlet"] += 1
                continue
            if leak_word(names, local):
                report["place_dropped_leak_word"] += 1
                continue
            lead = names[:0]
            # A settlement whose own name is a type word (BARE_WORD_SETTLEMENTS).
            if names[0].strip() in BARE_WORD_SETTLEMENTS:
                lead = names[:1]
            elif bare_type(names[0], local):
                # KEPT on an article of its own (London's quarter "Temple",
                # en:Temple, London), as a bare landmark is.
                if not (own and fold_name(article_title(t["wikipedia"])) != fold_name(names[0])):
                    report["place_dropped_bare_type"] += 1
                    note("bare_type", "drop", oid, names[0], "a bare type word, or a code beside one", t)
                    continue
                note("kept_bare_type", "keep", oid, names[0], "an article of its own", t)
                lead = names[:1]
            names = lead + [n for n in names[len(lead):] if not bare_type(n, local)]
            before = len(rows)
            add("place", pt, names, langs, area=e["type"] != "node", osm=oid, tags=t)
            if t.get("place") == "district" and len(rows) > before:
                note("kept_district", "keep", oid, names[0], "an article of its own", t)
        elif e["type"] == "node" and (t.get("highway") == "traffic_signals" or "junction" in t):
            # A signal's number is no name (Sydney's "5065", 2026-10-08).
            if not any(c.isalpha() for c in names[0]):
                report["junction_numbered"] += 1
                continue
            # A signed junction (四条烏丸): the streets through it as aliases,
            # and their shared languages with its own.
            via = sorted(node_streets.get(e["id"], ()))
            alias = []
            if len(via) >= 2:
                alias.append(" / ".join(via))
                en = [next((x for x in street_alias.get(v, []) if x != v), None) for v in via]
                if all(en):
                    alias.append(" / ".join(en))
                langs = langs | set.intersection(*(street_lang.get(v, set()) for v in via))
            add("junction", pt, names + [a for a in alias if a not in names], langs, osm=oid, tags=t)
        else:
            # A named square is a landmark when no street carries its name:
            # Brussels' Grand-Place is a pedestrian AREA (skipped as a street)
            # tagged place=square (batch 2a, 2026-10-08). Never one indoors or
            # underground: Kyoto's mall plazas at level -1 (ゼスト御池, コトチカ)
            # and Vancouver's "Time Out Stage", indoor=room.
            square = (t.get("place") == "square" and names[0] not in street_alias
                      and t.get("indoor") in (None, "no") and t.get("location") != "underground"
                      and not str(t.get("level", "0")).lstrip().startswith("-"))
            # An island or an islet with an article of its own is a landmark
            # (ISLAND_VALUES); every other place value stays unlisted.
            if t.get("place") and not square and not (t.get("place") in ISLAND_VALUES and own):
                continue
            # A STREET'S WAY IS NEVER A LANDMARK ROW (NOT_A_STREET_WAY; the
            # second batch, 2026-10-13): 103 rows in the 52 cities were a
            # road or path under a historic, tourism or bridge:name tag.
            # ONLY WHERE A STREET ROW BEARS THE NAME (owner, 2026-10-13, on
            # the first changed-row report): the name the landmark row would
            # have, bridge:name leading. With no such street row the landmark
            # row is the only way to find the thing, and stays under the
            # landmark rules (Seattle's Aurora Bridge, on Aurora Avenue North).
            if (e["type"] == "way" and t.get("highway") and t.get("area") != "yes" and not square
                    and _bridge_led(t, names)[0] in street_alias
                    and not {v.strip() for v in t["highway"].split(";")} & NOT_A_STREET_WAY):
                report["landmark_dropped_street_way"] += 1
                note("street_way_landmark", "drop", oid, names[0], f"highway={t['highway']}", t)
                continue
            landmark(e, t, names, pt, langs)

    for segs in rivers.values():
        pts = [p for p, *_ in segs]
        s, w_ = min(p[0] for p in pts), min(p[1] for p in pts)
        n_, e = max(p[0] for p in pts), max(p[1] for p in pts)
        c = ((s + n_) / 2, (w_ + e) / 2)
        names = []
        for _, ns, *_ in segs:
            names += [x for x in ns if x not in names]
        before = len(rows)
        add("landmark", min(pts, key=lambda p: _dist_m(p, c)), names,
            set().union(*(seg[2] for seg in segs)),
            [_r(s), _r(w_), _r(n_), _r(e)] if len(pts) > 1 else 0)
        # The row's id rides in its tags field until the merges are done: a
        # river row is never merged, which the merges tell by its empty id.
        if len(rows) > before:
            rows[-1][9] = {"_river": min((seg[3] for seg in segs),
                                         key=lambda o: (o.split("/")[0], int(o.split("/")[1])))}

    # Pedestrian squares drawn as areas (collected in the street pass), each
    # held to the landmark rules; one a street already names is findable.
    for w, t, names in square_areas:
        if names[0] in street_alias:
            report["square_area_named_by_a_street"] += 1
            continue
        c = w.get("center")
        pts = [nodes[n] for n in w["nodes"] if n in nodes]
        if not c and not pts:
            continue
        pt = (c["lat"], c["lon"]) if c else (sum(p[0] for p in pts) / len(pts),
                                             sum(p[1] for p in pts) / len(pts))
        if article(w, t, names, pt)[0] != "own":
            report["square_area_without_own_article"] += 1
            continue
        landmark(w, t, names, pt, _langs(t, local), square_like=True)

    # A square already findable under its name is a duplicate (owner,
    # 2026-10-08: "remove duplicates if we can"): a street or another square
    # within SQUARE_DUP_M carrying the same name once accents, case and
    # punctuation are set aside ("nám. Hedviky Vilgusové" is the street
    # "náměstí Hedviky Vilgusové"), or, within SQUARE_NEAR_M, one spelt almost
    # alike ("Plaça de Carme Monturiol", "Plaça de Carmen Monturiol"). Only
    # streets and squares: a statue, station or neighbourhood named like the
    # square is another thing (Barcelona's statue of Emili Vendrell in his
    # plaça; Brussels' station Masui by Place Masui).
    drop = set()
    street_kind = KINDS.index("street")
    square_ids = {id(r) for r in square_rows}
    # A park named as a square or a street (square_led; the sixth pass) is
    # held to the streets alone, never to a square or another park.
    park_ids = {id(r) for r in park_square_rows}
    for sq in square_rows + park_square_rows:
        words = _square_keys([sq[3]] + (sq[4].split("|") if sq[4] else []))
        keys = {"".join(w) for w in words}
        for o in rows:
            if o is sq or id(o) in drop or not (o[0] == street_kind or (
                    id(o) in square_ids and id(sq) not in park_ids)):
                continue
            d = _dist_m((sq[1], sq[2]), (o[1], o[2]))
            if d > SQUARE_DUP_M:
                continue
            onames = [o[3]] + (o[4].split("|") if o[4] else [])
            owords = _square_keys(onames)
            # A park: only a street that bears its leading name
            # (SQUARE_JOINERS), never one spelt almost alike.
            if id(sq) in park_ids:
                same = bool(_square_joined([sq[3]]) & _square_joined(onames))
            else:
                # Spelt almost alike only under the same first word: Placeta
                # del Pi and Plaça del Pi are two squares.
                same = bool(keys & {"".join(w) for w in owords}) or (d <= SQUARE_NEAR_M and any(
                    a[0] == b[0] and difflib.SequenceMatcher(None, "".join(a), "".join(b)).ratio() >= 0.9
                    for a in words for b in owords))
            if same:
                drop.add(id(sq))
                if sq[3] not in onames:
                    o[4] = "|".join(onames[1:] + [sq[3]])
                    report["square_name_kept_as_alternate"] += 1
                if id(sq) in park_ids:
                    report["park_dropped_street_duplicate"] += 1
                    note("park_street_duplicate", "merge", sq[7], sq[3],
                         f"the street row {o[3]!r} is {round(d)} m off", sq[9])
                break
    if drop:
        rows[:] = [r for r in rows if id(r) not in drop]
        report["landmark"] -= len(drop)
        report["square_dropped_duplicate"] += len(drop)
    # --- The merges of 2026-10-13 (PLATFORM_MERGE_M, ROW_MERGE_M) and the
    # shared-item rule (SHARED_WIKIDATA_MIN), in that order: a thing drawn in
    # three rows is merged before its item is counted.
    gone = set()

    def merge(members, cls):
        """Keep the member nearest the group's middle (the lower OSM id on a
        tie, so a rebuild keeps the same row); its names and languages take
        in the others'."""
        mid = (sum(r[1] for r in members) / len(members), sum(r[2] for r in members) / len(members))
        keep = min(members, key=lambda r: (round(_dist_m((r[1], r[2]), mid)),
                                           r[7].split("/")[0], int(r[7].split("/")[1])))
        alias = [a for a in keep[4].split("|") if a]
        for r in members:
            if r is keep:
                continue
            alias += [n for n in [r[3], *r[4].split("|")] if n and n != keep[3] and n not in alias]
            keep[8] |= r[8]
            gone.add(id(r))
            report[KINDS[r[0]]] -= 1
            report[f"{KINDS[r[0]]}_merged_{cls}"] += 1
            note(f"merged_{cls}", "merge", r[7], r[3], f"into {keep[7]} ({KINDS[r[0]]})", r[9])
        keep[4] = "|".join(alias)

    # SEGMENTS BESIDE THE RELATION THAT CARRIES THE ARTICLE (a fault mended,
    # the sixth pass, 2026-10-13; SEGMENTS_MIN). Amsterdam's museum railway
    # is drawn as seven ways with no entry and one route relation with the
    # entry and the article: eight rows. Landmark ways of one folded name
    # that carry neither wikidata nor wikipedia, SEGMENTS_MIN or more of
    # them, fold into the ONE relation row of that name that carries an
    # entry or an article, at any distance; the relation's row stands. One
    # such way alone is not read: a building beside a like-named site is
    # another thing. Read before the same-name merges, which would fold the
    # relation into the segment beside it. NOT mended: a relation whose centre
    # lies within NEAR_DUP_M of a segment read before it is that segment's
    # duplicate in add() and has no row to fold into; the segments then stay
    # as they were. Measured on the 19 live cities:
    # 10 rows fold (Seoul's city wall, 8 ways; a Tokyo park, 2), and
    # Amsterdam's 7.
    named_relations, bare_ways = defaultdict(list), defaultdict(list)
    for r in rows:
        if not r[7] or id(r) in gone or KINDS[r[0]] != "landmark":
            continue
        entry = (r[9].get("wikidata") or r[9].get("wikipedia") or "").strip()
        if r[7].startswith("relation/") and entry:
            named_relations[fold_name(r[3])].append(r)
        elif r[7].startswith("way/") and not entry:
            bare_ways[fold_name(r[3])].append(r)
    for name in sorted(bare_ways):
        if len(bare_ways[name]) < SEGMENTS_MIN or len(named_relations.get(name, ())) != 1:
            continue
        keep = named_relations[name][0]
        for r in bare_ways[name]:
            keep[8] |= r[8]
            gone.add(id(r))
            report["landmark"] -= 1
            report["landmark_merged_segments"] += 1
            note("merged_segments", "merge", r[7], r[3], f"into {keep[7]} (landmark), which carries the entry", r[9])
    by_name = defaultdict(list)
    for r in rows:
        if r[7] and KINDS[r[0]] in ("station", "junction", "place", "landmark") and fold_name(r[3]) \
                and id(r) not in gone:
            by_name[(r[0], _stop_key(r[3]) if KINDS[r[0]] == "station" else fold_name(r[3]))].append(r)
    for (kind, _), items in by_name.items():
        if len(items) < 2:
            continue
        station = KINDS[kind] == "station"
        for group in _clusters([(r[1], r[2]) for r in items], PLATFORM_MERGE_M if station else ROW_MERGE_M):
            members = [items[i] for i in group]
            if not station:
                merge(members, "duplicate")
            elif _one_railway(members):
                merge(members, "platform")
    # ONE LINEAR MONUMENT DRAWN IN SEGMENTS IS ONE ROW (candidate 40, owner
    # 2026-10-13): landmark rows of one folded name and one Wikidata entry,
    # every one a way or a relation, at any distance (Rome's Aurelian Walls,
    # 27 rows). The row's point is the segment's nearest the middle of them
    # all (merge()), so it lies on the monument. Nodes are not merged: two
    # casts of one statue are two places.
    by_segment = defaultdict(list)
    for r in rows:
        if r[7] and id(r) not in gone and KINDS[r[0]] == "landmark" and not r[7].startswith("node/") \
                and (r[9].get("wikidata") or "").strip():
            by_segment[(fold_name(r[3]), r[9]["wikidata"].strip())].append(r)
    for key in sorted(by_segment):
        if len(by_segment[key]) > 1:
            merge(by_segment[key], "segments")
    # ONE ROW A STATION (the second batch, 2026-10-13). An outline with no
    # railway tag beside a rail-tagged station row is that station's building
    # and no row (OUTLINE_BESIDE_M, OUTLINE_SAME_M: 97 of the 134 outline
    # rows in the 52 cities; those further off are bus terminals and the
    # like and stay). Then station rows sharing one Wikidata entry are one
    # transfer complex (COMPLEX_MERGE_M: 274 rows merged, Tokyo 88, Seoul 45,
    # New York 36, Barcelona 34), the others' names the kept row's aliases.
    # A STOP-AREA RELATION STAYS WHERE NO OTHER ROW CARRIES ITS STATION
    # (owner, 2026-10-13: "yes stop area with your rule"). The cache holds no
    # members, so the test is by position and name: another station row
    # within OUTLINE_BESIDE_M, one of its folded name within OUTLINE_SAME_M,
    # or one sharing its Wikidata entry. Kept: Washington's two streetcar
    # stops that are mapped as stop areas only.
    stations = [r for r in rows if KINDS[r[0]] == "station" and id(r) not in gone]

    def is_stop_area(r):
        return r[7].startswith("relation/") and r[9].get("public_transport") == "stop_area"

    # A STATION'S OUTLINE UNDER THE STATION'S NAME (owner, 2026-10-13): a
    # station way or relation within OUTLINE_BESIDE_M of a station node of
    # its folded name, or one sharing its Wikidata entry, is that station
    # drawn twice, whatever railway tag it carries (Gwangju's 상무역, 15 m
    # from its node). It merges into the node's row, its names aliases. An
    # outline with no such node is the station's only row and stays.
    # A STATION ENTRANCE OR TICKET GATE IS NO STATION ROW (STATION_ENTRANCES;
    # the sixth pass), read before the outline merges so that no outline is
    # folded into an entrance. It stays only where the map draws its name and
    # no station row of that name stands within OUTLINE_SAME_M.
    for r in stations:
        if r[9].get("railway") not in STATION_ENTRANCES:
            continue
        mine = _station_core(r[3])
        o = next((o for o in stations if o is not r and o[9].get("railway") not in STATION_ENTRANCES
                  and _station_core(o[3]) == mine
                  and _dist_m((r[1], r[2]), (o[1], o[2])) <= OUTLINE_SAME_M), None)
        if o is None and fold_name(r[3]) in drawn:
            note("station_entrance_kept", "kept", r[7], r[3], "a station of the map, and no other row", r[9])
            continue
        gone.add(id(r))
        report["station"] -= 1
        report["station_dropped_entrance"] += 1
        note("station_entrance", "drop", r[7], r[3],
             f"railway={r[9]['railway']}" + (f", beside {o[7]}" if o is not None else ""), r[9])
    stations = [r for r in stations if id(r) not in gone]
    station_nodes = [r for r in stations if r[7].startswith("node/")]
    for r in stations:
        if r[7].startswith("node/") or is_stop_area(r) or id(r) in gone:
            continue
        mine, wd = _station_core(r[3]), (r[9].get("wikidata") or "").strip()
        o = next((o for o in station_nodes if id(o) not in gone
                  and _dist_m((r[1], r[2]), (o[1], o[2])) <= OUTLINE_BESIDE_M
                  and (_station_core(o[3]) == mine or (wd and wd == (o[9].get("wikidata") or "").strip()))), None)
        if o is not None:
            alias = [a for a in o[4].split("|") if a]
            alias += [n for n in [r[3], *r[4].split("|")] if n and n != o[3] and n not in alias]
            o[4] = "|".join(alias)
            o[8] |= r[8]
            gone.add(id(r))
            report["station"] -= 1
            report["station_merged_outline"] += 1
            note("merged_outline", "merge", r[7], r[3], f"into {o[7]} (station)", r[9])
    stations = [r for r in stations if id(r) not in gone]

    for r in [x for x in stations if is_stop_area(x)]:
        mine, wd = fold_name(r[3]), (r[9].get("wikidata") or "").strip()
        for o in stations:
            if o is r or id(o) in gone or is_stop_area(o):
                continue
            d = _dist_m((r[1], r[2]), (o[1], o[2]))
            if (d <= OUTLINE_BESIDE_M or (d <= OUTLINE_SAME_M and fold_name(o[3]) == mine)
                    or (wd and wd == (o[9].get("wikidata") or "").strip())):
                gone.add(id(r))
                report["station"] -= 1
                report["station_skipped_stop_area"] += 1
                note("station_stop_area", "drop", r[7], r[3], f"{round(d)} m from {o[7]} ({o[3]})", r[9])
                break
        else:
            note("station_stop_area_kept", "kept", r[7], r[3], "no other row carries the station", r[9])
    stations = [r for r in stations if id(r) not in gone]
    rail = [r for r in stations if r[9].get("railway")]
    for r in stations:
        if r[9].get("railway") or r[9].get("public_transport") != "station":
            continue
        mine = fold_name(r[3])
        for o in rail:
            d = _dist_m((r[1], r[2]), (o[1], o[2]))
            if d <= OUTLINE_BESIDE_M or (d <= OUTLINE_SAME_M and fold_name(o[3]) == mine):
                gone.add(id(r))
                report["station"] -= 1
                report["station_dropped_outline"] += 1
                note("station_outline", "drop", r[7], r[3], f"{round(d)} m from {o[7]} ({o[3]})", r[9])
                break
        else:
            # NO RAILWAY TAG, NO STATION ROW (the third list, 13). Kept, as
            # the lone stop area is, where it lists a rail mode or carries a
            # station tag and no rail-tagged station row stands for it.
            # A network tag or a name the map draws counts as well: Brussels'
            # Hotel des Monnaies, Rogier, Madou and Botanique are outlines
            # with a network and no mode, each its station's only row.
            # A bus network's tag is no rail sign (BUS_NETWORK; the sixth pass).
            if (r[9].get("station") or any(r[9].get(k) == "yes" for k in RAIL_MODES)
                    or (r[9].get("network") and not BUS_NETWORK.search(
                        f"{r[9]['network']} {r[9].get('operator') or ''}"))
                    or fold_name(r[3]) in drawn):
                note("station_no_railway_tag_kept", "kept", r[7], r[3], "a rail sign, and no other row", r[9])
            else:
                gone.add(id(r))
                report["station"] -= 1
                report["station_dropped_no_railway_tag"] += 1
                note("station_no_railway_tag", "drop", r[7], r[3], "public_transport=station alone", r[9])
    by_item = defaultdict(list)
    for r in stations:
        if id(r) not in gone:
            for wd in {w.strip() for w in str(r[9].get("wikidata") or "").split(";") if w.strip()}:
                by_item[wd].append(r)
    for wd in sorted(by_item):
        items = [r for r in by_item[wd] if id(r) not in gone]
        for group in _clusters([(r[1], r[2]) for r in items], COMPLEX_MERGE_M):
            parts = complex_parts([items[i] for i in group], drawn)
            for part in parts:
                if len(part) > 1:
                    merge(part, "complex")
                if len(parts) > 1:
                    note("complex_kept_apart", "kept", part[0][7], part[0][3],
                         f"{wd} is shared with another station of the map", part[0][9])
    if gone:
        rows[:] = [r for r in rows if id(r) not in gone]
    # A SITE OR BOUNDARY RELATION THAT REPEATS ANOTHER ROW (the third list, 9).
    by_entry = defaultdict(list)
    for r in rows:
        if r[7] and KINDS[r[0]] in ("landmark", "place"):
            for key in ("wikidata", "wikipedia"):
                if (r[9].get(key) or "").strip():
                    by_entry[(key, r[9][key].strip())].append(r)

    def site_relation(r):
        return r[7].startswith("relation/") and (r[9].get("type") in SITE_RELATION_TYPES or r[9].get("boundary"))

    gone = set()
    for (key, value), items in by_entry.items():
        for r in items:
            if id(r) in gone or not site_relation(r):
                continue
            # A PLACE ROW FOLDS ONLY INTO A PLACE ROW (a fault mended,
            # 2026-10-13): 18 Prague boroughs had no row under their own
            # name, each boundary folded into its town hall, a landmark
            # that carries the borough's Wikidata entry.
            other = next((o for o in items if o is not r and not site_relation(o)
                          and (KINDS[r[0]] != "place" or KINDS[o[0]] == "place")
                          and _dist_m((r[1], r[2]), (o[1], o[2])) > ROW_MERGE_M), None)
            if other is not None:
                gone.add(id(r))
                report[KINDS[r[0]]] -= 1
                report["dropped_site_relation_repeat"] += 1
                note("site_relation_repeat", "drop", r[7], r[3],
                     f"{key}={value} also on {other[7]}, {round(_dist_m((r[1], r[2]), (other[1], other[2])))} m off",
                     r[9])
    if gone:
        rows[:] = [r for r in rows if id(r) not in gone]
    shared = defaultdict(int)
    for r in rows:
        for wd in str(r[9].get("wikidata") or "").split(";"):
            if wd.strip():
                shared[wd.strip()] += 1
    gone = set()
    for r in rows:
        held = held_by_wikidata.get(r[7])
        if not held:
            continue
        n = max(shared[wd.strip()] for wd in held.split(";") if wd.strip())
        if n >= SHARED_WIKIDATA_MIN:
            gone.add(id(r))
            report[KINDS[r[0]]] -= 1
            report["landmark_dropped_shared_wikidata"] += 1
            note("shared_wikidata", "drop", r[7], r[3], f"{held} on {n} rows", r[9])
        elif n == 2:
            note("shared_wikidata_two", "measure", r[7], r[3], f"{held} on 2 rows", r[9])
    if gone:
        rows[:] = [r for r in rows if id(r) not in gone]
    # PLACE_KEPT ADMITS A ROW (owner, 2026-10-13: a famous place the rules
    # pass over for want of a Wikidata or Wikipedia tag is kept by id). Read
    # last, after every drop and merge: an id of config.PLACE_KEPT that is in
    # the cache, has a name and bears no row gets one, a landmark unless its
    # tags make it a station or a place (a ferry terminal way, a marketplace
    # node, a bridge node under a tram stop's name). Only PLACE_DROPPED
    # outranks it. Not for a way kept as a river or a street (a waterway or
    # highway tag): those ids stand for rows that carry no id. A row of the
    # same kind and name beside it is that row already (add()).
    have = {r[7] for r in rows if r[7]}
    wanted = {k for k in kept_given if k not in have and k not in dropped}
    if wanted:
        for e in elements:
            oid = f"{e['type']}/{e['id']}"
            t = e.get("tags") or {}
            if oid not in wanted or (e["type"] == "way" and (t.get("waterway") or t.get("highway"))):
                continue
            wanted.discard(oid)
            names = _local_first(t, _names(t, name_tags), read)
            pt = _point(e)
            if pt is None and e.get("nodes"):
                pts = [nodes[n] for n in e["nodes"] if n in nodes]
                pt = (sum(q[0] for q in pts) / len(pts), sum(q[1] for q in pts) / len(pts)) if pts else None
            if not names or not pt:
                note("kept_by_id_no_row", "measure", oid, names[0] if names else "", "no name or no point", t)
                continue
            kind = ("station" if t.get("railway") in ("station", "halt", "tram_stop")
                    or t.get("public_transport") == "station"
                    else "place" if t.get("place") in PLACE_VALUES else "landmark")
            before = len(rows)
            add(kind, pt, names, langs_of(t), area=e["type"] != "node", osm=oid, tags=dict(t))
            if len(rows) > before:
                report[f"{kind}_admitted_by_id"] += 1
                note("kept_by_id_admitted", "kept", oid, names[0], f"config.PLACE_KEPT, a {kind} row", t)
    rows.sort(key=lambda r: (r[0], r[3]))
    river_ids = [r.pop().get("_river") for r in rows]     # the object's tags
    row_langs = [r.pop() for r in rows]
    row_osm = [r.pop() or river for r, river in zip(rows, river_ids)]
    row_ways = [r.pop() for r in rows]
    # Each crossing as [lat, lon, row of street A, row of street B]; the
    # browser builds its name ("5th Avenue / Pike Street") and its English
    # pair (Kyoto's "Shijo Street / Karasuma Street") from those rows. A name
    # used by streets far apart (two 一番町) resolves to the row whose extent
    # holds the crossing, else the nearest.
    street_rows = defaultdict(list)
    for i, r in enumerate(rows):
        if r[0] == KINDS.index("street"):
            street_rows[r[3]].append(i)

    def street_at(name, pt):
        def far(i):
            b = rows[i][5]
            if b and b[0] <= pt[0] <= b[2] and b[1] <= pt[1] <= b[3]:
                return 0
            return _dist_m(pt, (rows[i][1], rows[i][2]))
        return min(street_rows[name], key=far) if street_rows.get(name) else None

    crossing_rows, seen_cross = [], set()
    for pt, a, b, langs in crossings:
        ia, ib = street_at(a, pt), street_at(b, pt)
        if ia is None or ib is None:
            report["crossing_without_street"] += 1
            continue
        row = [_r(pt[0]), _r(pt[1]), ia, ib]
        if tuple(row) in seen_cross:
            report["crossing_duplicate"] += 1
            continue
        seen_cross.add(tuple(row))
        crossing_rows.append(row)
        row_langs.append(langs)
        report["crossing"] += 1
    crossing_rows.sort()
    index = {
        # ODbL 4.2(b)-(d): the licence URI and the notice travel IN the file
        # (licence read 2026-10-07; docs/data_sources.md, "Place search index").
        "license": {
            "name": "Open Database License (ODbL) v1.0",
            "url": "https://opendatacommons.org/licenses/odbl/1-0/",
            "attribution": "© OpenStreetMap contributors",
            "attribution_url": "https://www.openstreetmap.org/copyright",
            "notice": ("This place index is a database derived from OpenStreetMap data, "
                       "© OpenStreetMap contributors, and is made available under the Open "
                       "Database License (ODbL) v1.0: https://opendatacommons.org/licenses/odbl/1-0/. "
                       "Source credits: https://www.openstreetmap.org/copyright. The method that "
                       "builds it is published at https://github.com/dacekroberts/expanded-heatmap."),
            "data_retrieved": retrieved,
        },
        "schema": SCHEMA,
        "city": city,
        "languages": languages(row_langs, local, also),
        # build_city() holds these to the city's Wikidata cache; never served.
        "wikidata_asked": sorted(asked),
        "fold": fold,
        "kinds": list(KINDS),
        "rows": rows,
        # write() puts these in crossings_path() and their site path here.
        "crossing_rows": crossing_rows,
        # write() puts these in the page's summary, never in the served file.
        "stations_not_open": sorted(not_open, key=lambda r: r["osm"]),
        # write() puts these in ids_path(), never in the served file.
        "row_osm": row_osm,
        # build_city() simplifies these (street_lines); write() puts them in
        # streets_path(), never in the served index.
        "street_lines_raw": [[i, chain_ways(w, nodes)] for i, w in enumerate(row_ways) if w],
    }
    return index, dict(report)


def _selftest():
    """The 2026-10-13 rules on a made-up city: each case is a row that is
    there, or is not, only because of the rule it names (break a rule in a
    copy and its case fails: scripts/rule_breaks.py with
    scripts/place_index_breaks.json). Reads no file and builds everything it
    needs here."""
    els, ids = [], iter(range(1, 100000))
    target = [els]

    def node(lat, lon, **tags):
        e = {"type": "node", "id": next(ids), "lat": lat, "lon": lon}
        if tags:
            e["tags"] = {k.replace("__", ":"): v for k, v in tags.items()}
        target[0].append(e)
        return e["id"]

    def street(name, lat, highway="residential", share=None, lon=-122.30, **tags):
        """A two-node way running east at `lat`; `share` is a node id it ends on."""
        a = share or node(lat, lon)
        b = node(lat + 0.0002, lon + 0.002)
        target[0].append({"type": "way", "id": next(ids), "nodes": [a, b],
                    "tags": {"name": name, "highway": highway,
                             **{k.replace("__", ":"): v for k, v in tags.items()}}})
        return a, b

    def area(lat, lon, **tags):
        target[0].append({"type": "way", "id": next(ids), "center": {"lat": lat, "lon": lon},
                    "tags": {k.replace("__", ":"): v for k, v in tags.items()}})

    # Streets.
    main_a, _ = street("Main Street", 47.6000)
    street("Gated Lane", 47.6010, access="private", share=main_a)
    street("Gated Court", 47.6020, highway="unclassified", access="no")
    half_a, _ = street("Half Lane", 47.6030, access="private")
    street("Half Lane", 47.6031, share=half_a)
    street("Known Close", 47.6040, access="private", wikipedia="en:Known Close")
    street("Bus Road", 47.6050, highway="busway")
    street("Race Bend", 47.6060, highway="raceway")
    mixed_a, _ = street("Mixed Way", 47.6070, highway="busway")
    street("Mixed Way", 47.6071, share=mixed_a)
    street("Footpath 104", 47.6080, highway="footway")
    street("The Walk", 47.6090, highway="path")
    street("Service Road", 47.6100, highway="service")
    street("The Avenue", 47.6110)
    street("Lane 5", 47.6120, highway="footway")
    # Stations.
    node(47.6200, -122.31, name="Old Town", railway="tram_stop")
    node(47.6206, -122.31, name="Old Town", railway="tram_stop")
    node(47.6304, -122.31, name="Union", railway="station")
    node(47.6316, -122.31, name="Union", railway="tram_stop")
    node(47.6400, -122.31, name="Future Halt", railway="tram_stop", construction="yes")
    node(47.6410, -122.31, name="Later Station", railway="station", opening_date="2027-01-01")
    node(47.6420, -122.31, name="Opened Station", railway="station", opening_date="2020-05-01")
    node(47.6430, -122.31, name="Shut Station", railway="station", end_date="2002-07-14")
    node(47.6440, -122.31, name="Ghost Halt", railway="halt", abandoned="yes")
    node(47.6450, -122.31, name="Toy Station", railway="station", usage="tourism")
    node(47.6460, -122.31, name="Peak Tram", railway="station", tourism="attraction")
    node(47.6470, -122.31, name="Car Park Station", public_transport="station", amenity="parking")
    node(47.6480, -122.31, name="Monument", railway="station", wikidata="Q100")
    node(47.6490, -122.31, name="Chapel", railway="halt")
    # Places.
    node(47.6500, -122.32, name="Old Village", place="locality", abandoned__place="village")
    node(47.6510, -122.32, name="New Quarter", place="quarter", construction__place="quarter")
    node(47.6520, -122.32, name="Flag Hamlet", place="hamlet", demolished="yes")
    node(47.6525, -122.32, name="Twice Hamlet", place="hamlet", abandoned__place="hamlet")
    node(47.6530, -122.32, name="Green Island", place="island", wikipedia="en:Green Island")
    node(47.6540, -122.32, name="Bare Islet", place="islet")
    node(47.6550, -122.32, name="North District", place="district", wikipedia="en:North District")
    node(47.6555, -122.32, name="South District", place="district")
    area(47.6560, -122.32, name="Model Dwellings", place="neighbourhood", landuse="residential",
         wikipedia="en:Model Dwellings")
    area(47.6570, -122.32, name="Plain Dwellings", place="neighbourhood", landuse="residential")
    node(47.6580, -122.32, name="Riverside", place="suburb")
    node(47.6595, -122.32, name="Riverside", place="suburb")
    node(47.6600, -122.33, name="Hillside", place="suburb")
    node(47.6660, -122.33, name="Hillside", place="suburb")
    node(47.6700, -122.32, name="Five Ways", highway="traffic_signals")
    node(47.6709, -122.32, name="Five Ways", highway="traffic_signals")
    node(47.6720, -122.32, name="St. Mary's Church", amenity="place_of_worship")
    node(47.6729, -122.32, name="St Marys Church", amenity="place_of_worship")
    # Graves, plaques and memorials.
    node(47.6800, -122.32, name="Ada Person", historic="tomb", wikidata="Q1")
    node(47.6805, -122.32, name="Bea Person", historic="tomb", wikidata="Q2", wikipedia="en:Tomb of Bea Person")
    node(47.6810, -122.32, name="Cy Person", historic="tomb", wikidata="Q3", wikipedia="en:Cy Person")
    node(47.6815, -122.32, name="Dee Person", historic="tomb", wikidata="Q4", wikipedia="en:Delia Person")
    node(47.6820, -122.32, name="Eli Person", historic="memorial", memorial="plaque", wikidata="Q5")
    node(47.6825, -122.32, name="Fay Person", historic="memorial", memorial="statue", wikidata="Q6")
    # Keep beats drop on an article of the object's own.
    node(47.6900, -122.32, name="Monument", historic="monument", wikipedia="en:Monument to the Fire")
    node(47.6905, -122.32, name="Fountain", amenity="fountain", wikidata="Q7", wikipedia="en:Fountain")
    node(47.6910, -122.32, name="Sundial", tourism="artwork", wikipedia="en:Sundial Park")
    node(47.6990, -122.32, name="Sundial", tourism="artwork", wikipedia="en:Sundial Park")
    node(47.7000, -122.32, name="Hill College", amenity="college", operator__type="private",
         wikipedia="en:Hill College")
    node(47.7005, -122.32, name="Brand Museum", tourism="museum", brand="Brand", wikipedia="en:Brand Museum")
    node(47.7010, -122.32, name="Fenced Library", amenity="library", access="private",
         wikipedia="en:Fenced Library")
    node(47.7015, -122.32, name="Fenced Garden", leisure="garden", access="private", wikidata="Q8",
         wikipedia="en:Fenced Garden")
    node(47.7020, -122.32, name="Fenced Palace", historic="castle", access="private",
         wikipedia="en:Fenced Palace")
    node(47.7025, -122.32, name="Old Marker", historic="milestone", wikipedia="en:Old Marker")
    node(47.7030, -122.32, name="Lost Marker", historic="milestone")
    node(47.7035, -122.32, name="Stone of Remembrance", historic="memorial",
         wikipedia="en:Remembrance Memorial")
    node(47.7040, -122.32, name="Wayside Saint", historic="memorial", wikipedia="en:Wayside Saint")
    # Not there.
    node(47.7100, -122.32, name="Razed Hall", historic="yes", wikidata="Q9", razed__building="yes")
    node(47.7105, -122.32, name="Garden On Site", leisure="park", demolished__building="church")
    node(47.7110, -122.32, name="Old Fort", historic="fort", abandoned="yes", wikidata="Q10")
    node(47.7115, -122.32, name="Empty Park", leisure="park", abandoned="yes")
    node(47.7120, -122.32, name="New Park", leisure="park", construction="yes")
    node(47.7125, -122.32, name="Both Park", leisure="park", construction__leisure="park")
    node(47.7127, -122.32, name="Both Hall", historic="yes", wikidata="Q15", razed__historic="yes")
    node(47.7130, -122.32, name="Reopening Museum", tourism="museum", wikidata="Q11",
         opening_date="2030-01-01", start_date="1977")
    node(47.7135, -122.32, name="Unbuilt Museum", tourism="museum", wikidata="Q12", opening_date="2030-01-01")
    works = node(47.7137, -122.32, name="Closed Museum", tourism="museum", wikidata="Q16",
                 opening_date="2030-01-01")
    gone_id = node(47.7138, -122.32, name="Listed Ruin", historic="yes", wikidata="Q17", razed__building="yes")
    node(47.7140, -122.32, name="Disused Fountain", amenity="fountain", wikidata="Q13",
         disused__amenity="drinking_water")
    # An item shared by three rows, and one shared by two.
    for i, name in enumerate(("Piece One", "Piece Two", "Piece Three")):
        node(47.7200 + i * 0.005, -122.32, name=name, tourism="attraction", wikidata="Q77")
    for i, name in enumerate(("Pair One", "Pair Two")):
        node(47.7400 + i * 0.005, -122.32, name=name, tourism="attraction", wikidata="Q88")
    # A pedestrian square drawn as an area, and a bridge on a road.
    sq = [node(47.7500, -122.32), node(47.7500, -122.319), node(47.7505, -122.319)]
    target[0].append({"type": "way", "id": next(ids), "nodes": sq + sq[:1],
                "tags": {"name": "Market Square", "highway": "pedestrian", "area": "yes",
                         "wikipedia": "en:Market Square"}})
    sq = [node(47.7600, -122.32), node(47.7600, -122.319), node(47.7605, -122.319)]
    target[0].append({"type": "way", "id": next(ids), "nodes": sq + sq[:1],
                "tags": {"name": "Plain Plaza", "highway": "pedestrian", "area": "yes",
                         "wikipedia": "en:City Park#Plaza"}})
    area(47.7640, -122.32, name="River Road", highway="primary", bridge="yes", bridge__name="Iron Bridge",
         historic="yes", wikidata="Q14")

    # --- The second batch (2026-10-13).
    def rel(lat, lon, **tags):
        target[0].append({"type": "relation", "id": next(ids), "center": {"lat": lat, "lon": lon},
                    "tags": {k.replace("__", ":"): v for k, v in tags.items()}})

    # Streets.
    shut_a, _ = street("Shut Alley", 47.8000, access="private")
    street("Shut Alley", 47.8001, highway="service", service="alley", access="private", share=shut_a)
    open_a, _ = street("Open Alley", 47.8010, access="private")
    street("Open Alley", 47.8011, highway="service", service="alley", share=open_a)
    street("Platform Road", 47.8020, highway="platform;bus_stop")
    street("Mill Interchange", 47.8030, highway="primary")
    street("Mill Road Onramp", 47.8040)
    street("Mill Road Ramp", 47.8050, highway="motorway_link")
    street("Hill Ramp", 47.8060, highway="tertiary")
    street("Depot Drwy", 47.8070)
    street("Depot Plaza Driveway", 47.8080, highway="service")
    street("Queen Driveway", 47.8090)
    street("Mill Island", 47.8100, highway="motorway", junction="circular")
    street("Mill Circle", 47.8110, highway="primary", junction="roundabout")
    street("I 5 HOV", 47.8120, highway="motorway")
    street("Express Lane", 47.8130)
    street("Alley 87582" + chr(0x200E), 47.8140, highway="service", service="alley")
    street("12th Avenue 13th Avenue Alley", 47.8150, highway="service", service="alley")
    street("Matsui Alley", 47.8160, highway="service", service="alley")
    street("1st Street 2nd Street Alley", 47.8165)
    street("Path between Oak Drive and Elm Drive", 47.8170, highway="footway")
    street("M Street Bike Path", 47.8180, highway="cycleway")
    street("River Bike Path", 47.8190, highway="cycleway")
    street("Mill Road Trail", 47.8200, highway="cycleway")
    street("Back Lane", 47.8210, highway="footway")
    street("Hosier Place", 47.8220, highway="service")
    street("Gated Place", 47.8230, highway="service", access="private")
    street("Famous Street", 47.8240)
    street("Fair Plaza", 47.8245)
    # Stations.
    rel(47.6304, -122.31, name="Union (all platforms)", railway="station", public_transport="stop_area")
    rel(47.8700, -122.31, name="Tram Halt Group", railway="station", public_transport="stop_area")
    area(47.8250, -122.31, name="Central Bus Hub", public_transport="station", amenity="bus_station",
         light_rail="yes")
    node(47.8310, -122.31, name="Harbor", railway="station")
    area(47.8314, -122.31, name="Harbor Station Building", public_transport="station", subway="yes")
    area(47.8400, -122.31, name="Far Depot", public_transport="station", subway="yes")
    area(47.8450, -122.31, name="Bus Yard", public_transport="station")
    node(47.8500, -122.31, name="Times Square", railway="station", wikidata="Q500")
    node(47.8518, -122.31, name="Port Authority", railway="station", wikidata="Q500")
    node(47.8600, -122.31, name="North Loop", railway="station", wikidata="Q501")
    node(47.8900, -122.31, name="South Loop", railway="station", wikidata="Q501")
    node(47.8610, -122.31, name="Stray Station", railway="station", end_date="=1959")
    # Places.
    node(47.8320, -122.32, name="Lost Park (historical)", leisure="park")
    node(47.8330, -122.32, name="Shady Estates", place="neighbourhood")
    node(47.8340, -122.32, name="Known Estates", place="neighbourhood", wikidata="Q600")
    node(47.8350, -122.32, name="Sunny Trailer Park", place="hamlet")
    node(47.8360, -122.32, name="Rivertown", place="town")
    rel(47.8800, -122.32, name="Rivertown", place="town", boundary="administrative")
    rel(47.8370, -122.32, name="Wardville", place="suburb", boundary="administrative")
    node(47.8380, -122.32, name="Newtown", place="village")
    rel(47.8850, -122.32, name="Newtown", place="locality", boundary="administrative")
    # Landmarks.
    node(47.8420, -122.32, name="Pump Works", historic="maritime", wikidata="Q700", ref__nrhp="55")
    node(47.8425, -122.32, name="Pump Annex", historic="maritime", wikidata="Q700")
    node(47.8430, -122.32, name="Old Dock", historic="maritime", wikipedia="en:Old Dock")
    node(47.8433, -122.32, name="Lone Armory", historic="naval", wikidata="Q703")
    node(47.8436, -122.32, name="Lone Engine", historic="engine", wikidata="Q704")
    dam = node(47.8438, -122.32, name="Lock Dam", historic="maritime")
    green = node(47.8565, -122.32, name="Greenway", leisure="park")
    area(47.8497, -122.32, name="Lone Steps", highway="steps", tourism="attraction", wikidata="Q705")
    node(47.8535, -122.32, name="Known Chapel", amenity="place_of_worship", disused="yes", wikidata="Q706")
    for i, name in enumerate(("Building 7", "Building 8", "Drill Hall")):
        node(47.8440 + i * 0.001, -122.32, name=name, historic="building", ref__nrhp="123")
    node(47.8480, -122.32, name="Building 9", historic="building", ref__nrhp="999")
    area(47.8490, -122.32, name="Famous Street", highway="residential", tourism="attraction", wikidata="Q701")
    area(47.8495, -122.32, name="Fair Plaza", highway="pedestrian", area="yes", tourism="attraction",
         wikidata="Q702")
    area(47.8520, -122.32, name="Old Cut", historic="canal", waterway="derelict_canal")
    river = [next(ids), next(ids), next(ids), next(ids)]
    for k, (rid, name) in enumerate(zip(river, ("Mill Creek", "Mill Creek", "Lost Creek", "Lost Creek"))):
        target[0].append({"type": "way", "id": rid, "center": {"lat": 47.8570 + k * 0.001, "lon": -122.32},
                          "tags": {"name": name, "waterway": "river"}})
    node(47.8530, -122.32, name="Shut Chapel", amenity="place_of_worship", disused="yes")
    node(47.8540, -122.32, name="Ruined Mill", historic="ruins")
    node(47.8550, -122.32, name="Masjid", amenity="place_of_worship")
    node(47.8560, -122.32, name="Tot Lot", leisure="park")

    # --- The third list (2026-10-13).
    node(47.7700, -122.32, name="Engine 3100", historic="locomotive", wikidata="Q900")
    node(47.7705, -122.32, name="Royal Train", historic="locomotive", tourism="attraction", wikidata="Q901")
    node(47.7707, -122.32, name="Zephyr", historic="locomotive", wikidata="Q910", wikipedia="en:Zephyr")
    node(47.7710, -122.32, name="Coach A", historic="railway_car", tourism="attraction", wikidata="Q902")
    node(47.7790, -122.32, name="Coach B", historic="railway_car", tourism="attraction", wikidata="Q902")
    node(47.7715, -122.32, name="EMU Demo", tourism="attraction", locomotive__type="electric", wikidata="Q903",
         wikipedia="en:KTX Class")
    node(47.7720, -122.32, name="Old 99", tourism="attraction", locomotive__type="steam", wikidata="Q904",
         wikipedia="en:Old 99")
    node(47.7000, -122.325, name="City College", amenity="college", wikidata="Q905")
    # A borough's boundary and its town hall share one entry: two rows.
    rel(47.7700, -122.345, name="Ward Nine", place="suburb", boundary="administrative", wikidata="Q970")
    node(47.7600, -122.345, name="Ward Nine Town Hall", amenity="townhall", wikidata="Q970")
    # A subway station that is also tagged a bus station.
    node(47.5600, -122.31, name="Broadview", railway="station", station="subway", public_transport="station",
         amenity="bus_station", bus="yes")
    node(47.7710, -122.345, name="https://example.org/", historic="monument")
    street("Tramstop Street", 47.5500, highway="footway", public_transport="platform")
    street("Halt Lane", 47.5490, highway="footway", railway="platform")
    rel(47.7400, -122.325, name="City College", type="site", amenity="college", wikidata="Q905")
    node(47.7050, -122.325, name="Art School", amenity="college", wikidata="Q906")
    rel(47.7058, -122.325, name="Art School Grounds", type="site", amenity="college", wikidata="Q906")
    node(47.7725, -122.32, name="Bronze Horse", tourism="artwork", wikidata="Q907")
    node(47.7730, -122.32, name="Cloud Gate", tourism="artwork", wikipedia="en:Cloud Gate")
    node(47.7735, -122.32, name="Founder Statue", tourism="artwork", artwork_type="statue",
         wikipedia="en:John Founder")
    area(47.7740, -122.32, name="Old Branch Line", historic="railway", railway="abandoned", wikidata="Q908")
    area(47.7745, -122.32, name="Old Trunk Line", historic="railway", railway="abandoned",
         wikipedia="en:Old Trunk Line")
    area(47.7750, -122.32, name="Rail Water Tower", historic="yes", railway="disused", man_made="water_tower",
         wikidata="Q909")
    street("Shut Close", 47.8235, highway="living_street", access="private")
    # --- The fourth pass (2026-10-13).
    node(47.7770, -122.32, name="Iron Horse", tourism="artwork", wikidata="Q920", int_name="Cheval de Fer")
    node(47.7772, -122.32, name="Twin A", tourism="artwork", wikidata="Q921")
    node(47.7771, -122.32, name="Bean Gate", tourism="artwork", wikipedia="en:Bean Gate",
         subject__wikipedia="en:Bean Gate")
    node(47.7773, -122.32, name="Old Mayor", tourism="artwork", wikipedia="en:John Mayor",
         subject__wikipedia="en:John Mayor")
    node(47.7774, -122.32, name="Twin B", tourism="artwork", wikidata="Q921")
    node(47.7776, -122.32, name="Town Library", amenity="library", wikidata="Q922")
    node(47.7778, -122.32, name="Great Library", amenity="library", wikidata="Q923")
    node(47.7780, -122.32, name="Null Library", amenity="library", wikidata="Q924")
    node(47.7782, -122.32, name="Poet Bench", tourism="attraction", wikidata="Q927", subject__wikidata="Q927")
    for k in range(3):
        area(47.7000 + k * 0.02, -122.3245, name="Old Wall", historic="citywalls", wikidata="Q925")
    node(47.7010, -122.3245, name="Cast Statue", tourism="attraction", wikidata="Q926")
    node(47.7410, -122.3245, name="Cast Statue", tourism="attraction", wikidata="Q926")
    node(47.6660, -122.32, name="St Luke", amenity="place_of_worship")
    area(47.6675, -122.32, name="St Luke", amenity="place_of_worship", building="church")
    node(47.6452, -122.31, name="Freight Yard", railway="station", passenger="no")
    node(47.6454, -122.31, name="Works Halt", railway="station", public_transport="no")
    node(47.6456, -122.31, name="Mill Stop Tram", railway="tram_stop")
    street("Zone Street", 47.8237, access="no", foot="yes", motor_vehicle="permit")
    node(47.8650, -122.31, name="Depot Halt", railway="station")
    area(47.8642, -122.31, name="Depot Halt Station", railway="station", building="train_station")
    area(47.8720, -122.31, name="Net Hall", public_transport="station", network="Metro")
    area(47.8680, -122.31, name="Lone Hall", railway="station", building="train_station")
    node(47.8683, -122.31, name="Other Stop", railway="station")
    node(47.7755, -122.32, name="The Fountain", amenity="fountain", wikidata="Q911")
    node(47.7760, -122.32, name="Fountain - Chapel", amenity="place_of_worship")
    node(47.7765, -122.32, name="Fountain - Saint Ann", amenity="place_of_worship")
    node(47.6492, -122.31, name="Greenway", railway="station", station="subway")
    node(47.6494, -122.31, name="Sanctuary", railway="halt")
    node(47.6496, -122.31, name="Parkland", railway="halt", network="Metro")
    node(47.6498, -122.31, name="Barn", railway="halt")
    # --- The fifth pass (2026-10-13).
    node(47.7300, -122.33, name="Kingdom Hall of Jehovah's Witnesses", amenity="place_of_worship")
    node(47.7310, -122.33, name="Methodist Church", amenity="place_of_worship")
    node(47.7320, -122.33, name="Gurdwara", amenity="place_of_worship")
    node(47.7330, -122.33, name="First Baptist Church", amenity="place_of_worship")
    node(47.7340, -122.33, name="St Agnes Catholic Church", amenity="place_of_worship")
    node(47.7350, -122.33, name="Temple Baptist Church", amenity="place_of_worship")
    node(47.7360, -122.33, name="Friends Meeting House", amenity="place_of_worship",
         wikipedia="en:Friends Meeting House, Testville")
    witnesses = node(47.7370, -122.33, name="Jehovah's Witnesses", amenity="place_of_worship")
    node(47.7380, -122.33, name="Baptist Church", historic="building", wikidata="Q950")
    node(47.6440, -122.31, name="Methodist Church", railway="halt", amenity="place_of_worship")
    node(47.6430, -122.31, name="Senate Halt", railway="station", access="private")
    node(47.6420, -122.31, name="Members Halt", railway="station", access="private")
    # The disused test's guard: a map station at the node and under its
    # name; one under another name; one far off; one with a dated closure.
    node(47.6000, -122.31, name="Laird", railway="station", disused__public_transport="station")
    node(47.5900, -122.31, name="Old Depot", railway="station", disused__railway="station")
    node(47.5800, -122.31, name="Wynford", railway="station", disused__public_transport="station")
    node(47.5700, -122.31, name="Oakwood", railway="station", disused__railway="station", end_date="2016-10-14")
    node(47.6410, -122.31, name="Fenced Halt", railway="halt", access="no")
    node(47.8960, -122.31, name="Park Row", railway="station", wikidata="Q960")
    # One name, one entry, 400 m apart: one row (the complex merge).
    node(47.5300, -122.31, name="Pair Hall", railway="station", wikidata="Q9961")
    node(47.5336, -122.31, name="Pair Hall", railway="station", wikidata="Q9961")
    # One stop, one row (the full reads' faults, 2026-10-13).
    node(47.5200, -122.31, name="Quay Stop", railway="tram_stop")
    node(47.5218, -122.31, name="Quay Stop", railway="tram_stop")
    node(47.5100, -122.31, name="Harbour (dir North)", railway="tram_stop")
    node(47.5105, -122.31, name="Harbour (dir South)", railway="tram_stop")
    node(47.5000, -122.31, name="Mill Junction", railway="station")
    node(47.5015, -122.31, name="Mill Junction", railway="station")
    node(47.4900, -122.31, name="Two Lines", railway="station", operator="North Railway")
    node(47.4915, -122.31, name="Two Lines", railway="station", operator="South Railway")
    rel(47.4800, -122.31, name="Trunk Line", type="route", public_transport="station", train="yes")
    node(47.4000, -122.31, name="Far Hall", railway="station", wikidata="Q9962")
    node(47.4270, -122.31, name="Far Hall", railway="station", wikidata="Q9962")
    area(47.4700, -122.31, name="East School", amenity="school", public_transport="station", station="subway")
    node(47.4600, -122.31, name="Library West Gate", highway="bus_stop", historic="Old Park Gate")
    kept_halt = node(47.4500, -122.31, name="Kept Halt", railway="halt", access="private")
    ferry = node(47.4400, -122.31, name="Old Ferry Terminal", amenity="ferry_terminal")
    node(47.4300, -122.31, name="Tram Bridge", railway="tram_stop")
    bridge = node(47.4301, -122.31, name="Tram Bridge", tourism="viewpoint")
    shut_halt = node(47.4200, -122.31, name="Dropped Halt", railway="halt")
    node(47.8962, -122.31, name="Park Row Concourse", railway="station", wikidata="Q960")
    node(47.8990, -122.31, name="Boyle Square", railway="station", wikidata="Q960")
    # --- The sixth pass (2026-10-13).
    node(47.7400, -122.33, name="Church of Christ Presbyterian", amenity="place_of_worship")
    node(47.7410, -122.33, name="Church of God", amenity="place_of_worship")
    node(47.7420, -122.33, name="Russian Baptist Church", amenity="place_of_worship")
    node(47.7430, -122.33, name="Greek Orthodox Church", amenity="place_of_worship")
    node(47.7440, -122.33, name="Gospel Hall", amenity="place_of_worship", wikidata="Q930")
    node(47.7450, -122.33, name="Kingdom Hall", amenity="place_of_worship", wikidata="Q931")
    node(47.7460, -122.33, name="Presbytery of Testville", amenity="place_of_worship")
    node(47.7470, -122.33, name="Catholic Diocese of Testville", amenity="place_of_worship")
    node(47.7480, -122.33, name="St Clare Convent", amenity="place_of_worship")
    node(47.7490, -122.33, name="Lakeside Green", leisure="park", operator="Lakeside Homes Association")
    node(47.7500, -122.33, name="Founders Green", leisure="park", operator="Founders Condominium",
         wikipedia="en:Founders Green")
    node(47.7510, -122.33, name="Mall Court", place="square", operator="Westfield Shopping")
    node(47.7520, -122.33, name="Rotary Green", leisure="park", operator="Rotary Club")
    node(47.6380, -122.31, name="Gate Halt", railway="station")
    node(47.6395, -122.31, name="Gate Halt", railway="subway_entrance", public_transport="station")
    node(47.6340, -122.31, name="East Ticket Gate", railway="train_station_entrance", public_transport="station")
    node(47.6300, -122.31, name="Drawn Gate", railway="subway_entrance", public_transport="station")
    area(47.6260, -122.31, name="Rapid Bus Stop", public_transport="station", network="BRT")
    node(47.7000, -122.335, name="Southside", place="suburb")
    rel(47.7200, -122.335, name="Southside", place="suburb", boundary="administrative")
    node(47.6100, -122.335, name="Farside", place="suburb")
    rel(47.8800, -122.335, name="Farside (North)", place="suburb", boundary="administrative")
    node(47.7600, -122.335, name="Nearside", place="suburb")
    rel(47.7610, -122.335, name="Nearside (East)", place="suburb", boundary="administrative")
    for k in range(3):
        area(47.7900 + k * 0.01, -122.335, name="Museum Railway", historic="railway")
    rel(47.7950, -122.3355, name="Museum Railway", type="route", historic="railway", wikidata="Q940")
    area(47.8300, -122.335, name="Lone Mill", historic="building")
    rel(47.8700, -122.335, name="Lone Mill", type="site", historic="building", wikidata="Q941")
    colonia = next(ids)
    target[0].append({"type": "way", "id": colonia, "center": {"lat": 47.6575, "lon": -122.32},
                      "tags": {"name": "Colonia Real", "place": "neighbourhood", "landuse": "residential"}})
    # A German city and a Korean one, each its own cache.
    de_els = []
    target[0] = de_els
    street("Hauptstraße", 52.5000, lon=13.40)
    street("Kirchweg", 52.5005, highway="footway", lon=13.40)
    street("Zum Hafen", 52.5010, highway="footway", lon=13.40)
    street("Spielgerät", 52.5020, highway="footway", lon=13.40)
    street("Weg 5", 52.5030, highway="footway", lon=13.40)
    street("Straße 5", 52.5040, highway="footway", lon=13.40)
    street("Volksgartenweg 1", 52.5050, highway="footway", lon=13.40)
    street("Zufahrt Nord", 52.5060, lon=13.40)
    node(52.5100, 13.401, name="Kapelle", amenity="place_of_worship")
    node(52.5110, 13.401, name="Villa Lemm", leisure="park")
    node(52.5120, 13.401, name="Schlosspark", leisure="park")
    node(52.5130, 13.401, name="Alte Mühle (abgebrannt)", historic="yes", wikidata="Q1")
    node(52.5140, 13.401, name="Ehem. Rathaus", historic="yes", wikidata="Q2")
    node(52.5150, 13.401, name="Betraum", historic="memorial", memorial="stolperschwelle", tourism="attraction",
         wikidata="Q3")
    de_rows = {(KINDS[r[0]], r[3]) for r in build(de_els, city="Teststadt", retrieved="2026-10-10",
                                                  local=("de",))[0]["rows"]}
    ko_els = []
    target[0] = ko_els
    street("시험로", 37.4000, lon=126.95)
    node(37.4010, 126.951, name="족구장", leisure="park")
    node(37.4020, 126.951, name="115호 어린이공원", leisure="park")
    node(37.4030, 126.951, name="포도원놀이터", leisure="park", operator="호계대림아파트관리소")
    node(37.4040, 126.951, name="포도원공원", leisure="park")
    street("후문 진입로", 37.4050, highway="service", access="customers", lon=126.95)
    street("정문 진입로", 37.4060, highway="service", lon=126.95)
    street("시험 안길", 37.4070, highway="service", access="customers", lon=126.95)
    # The sixth pass (2026-10-13), Korean.
    node(37.4080, 126.951, name="어린이 공원", leisure="park")
    node(37.4090, 126.951, name="제1호근린공원", leisure="park")
    node(37.4100, 126.951, name="삼산타운어린이놀이터", leisure="park")
    node(37.4110, 126.951, name="신암그린타운공원", leisure="park")
    node(37.4120, 126.951, name="한빛마을 주민 운동장", leisure="park", operator="한빛마을")
    node(37.4125, 126.951, name="새봄한빛회 운동장", leisure="park", operator="한빛회")
    node(37.4130, 126.951, name="새봄어린이놀이터", leisure="park")
    node(37.4140, 126.951, name="시험교회 교육관", amenity="place_of_worship")
    node(37.4150, 126.951, name="시험교회", amenity="place_of_worship")
    ko_rows = {(KINDS[r[0]], r[3]) for r in build(ko_els, city="시험시", retrieved="2026-10-10",
                                                  local=("ko",))[0]["rows"]}
    # The sixth pass (2026-10-13): a Spanish city and a French one.
    es_els = []
    target[0] = es_els
    street("Plaza Mayor", 40.4000, lon=-3.70)
    node(40.4005, -3.6995, name="Plaza Mayor", leisure="park")
    node(40.4100, -3.6995, name="Plaza Nueva", leisure="park")
    street("Plaza Japón", 40.4300, lon=-3.70)
    node(40.4305, -3.6995, name="Plaza del Japón", leisure="park")
    street("Plaza Jonh Kennedy", 40.4400, lon=-3.70)
    node(40.4405, -3.6995, name="Plaza John Kennedy", leisure="park")
    street("Avenida de Brasil", 40.4020, lon=-3.70)
    node(40.4022, -3.6995, name="Avenida de Brasil", leisure="park")
    street("Bosque Viejo", 40.4040, lon=-3.70)
    node(40.4042, -3.6995, name="Bosque Viejo", leisure="park")
    node(40.4060, -3.6995, name="Plaza Mayor", place="square")
    node(40.4200, -3.6995, name="Convento de las Clarisas", amenity="place_of_worship")
    node(40.4210, -3.6995, name="Iglesia del Convento", amenity="place_of_worship")
    node(40.4220, -3.6995, name="Hórreo", historic="monument")
    node(40.4230, -3.6995, name="Templo budista", amenity="place_of_worship")
    node(40.4240, -3.6995, name="Estación de Mercancías Norte", railway="station")
    node(40.4250, -3.6995, name="Estación de Mercancías Sur", railway="station")
    node(40.4260, -3.6995, name="Estación Cerrada", railway="station", operational_status="closed")
    es_rows = defaultdict(int)
    es_alias = {}
    for r in build(es_els, city="Prueba", retrieved="2026-10-10", local=("es",),
                   map_stations=["Estación de Mercancías Sur"])[0]["rows"]:
        es_rows[(KINDS[r[0]], r[3])] += 1
        es_alias[(KINDS[r[0]], r[3])] = r[4]
    fr_els = []
    target[0] = fr_els
    street("Rue de la Brasserie", 48.8500, lon=2.35)
    node(48.8510, 2.351, name="Hôtel de Lauzun", historic="building")
    node(48.8520, 2.351, name="Hôtel d'Aumont", historic="building")
    node(48.8530, 2.351, name="Hôtel Ibis Centre", historic="building")
    node(48.8540, 2.351, name="Hôtel de Paris", tourism="hotel", wikidata="Q1")
    node(48.8550, 2.351, name="Hôtel particulier", historic="building")
    node(48.8560, 2.351, name="Carrefour de l'Hôtel", highway="traffic_signals")
    fr_index = build(fr_els, city="Essai", retrieved="2026-10-10", local=("fr",))[0]
    fr_rows = {(KINDS[r[0]], r[3]) for r in fr_index["rows"]}
    small = {}
    for code, streets, extra in (
            ("da", [("Store Kongensgade", "residential"), ("Hotel Strandvej", "residential"), ("Kirkestien", "footway")],
             [("Store Plads", {"place": "suburb"})]),
            ("nb", [("Storgata", "footway")], []),
            ("sv", [("Stora gården", "footway"), ("Lilla gården", "path"), ("Kungsgatan", "footway")], []),
            ("lv", [("Brīvības iela", "footway")], [("Mindeļa villa", {"historic": "building"})]),
            ("ro", [("Strada Mare", "footway")], []),
            ("it", [("Via Roma", "footway"), ("Via Albergo Vecchio", "residential")],
             [("Chiesa", {"amenity": "place_of_worship"})]),
            ("el", [("Αριστοτέλους", "footway"), ("Οδός Ερμού", "footway")], []),
            ("pt", [("Rua Um", "residential")], [("Seminário Maior", {"amenity": "place_of_worship"}),
                                                  ("Igreja do Seminário", {"amenity": "place_of_worship"}),
                                                  ("Convento de Santa Teresa", {"amenity": "place_of_worship"})]),
            ("ja", [("試験通", "residential")], [("大師堂", {"place": "quarter"}),
                                                  ("大師堂", {"amenity": "place_of_worship"}),
                                                  ("川崎貨物", {"railway": "station"}),
                                                  ("北港", {"railway": "station", "operator": "JR貨物"}),
                                                  ("南港", {"railway": "station", "operator": "JR東日本;JR貨物"}),
                                                  ("工場跡地", {"railway": "station"}),
                                                  ("東口 (閉鎖)", {"railway": "station"}),
                                                  ("西町（廃駅）", {"railway": "station"})])):
        target[0] = []
        for k, (name, hw) in enumerate(streets):
            street(name, 55.0 + k * 0.001, highway=hw, lon=12.0)
        for k, (name, tags) in enumerate(extra):
            node(55.01 + k * 0.001, 12.001, name=name, **tags)
        small[code] = {(KINDS[r[0]], r[3]) for r in build(target[0], city="Test", retrieved="2026-10-10",
                                                          local=(code,))[0]["rows"]}
    target[0] = []
    street("Strada Mare", 46.77, lon=23.59, name__hu="Nagy utca")
    street("Strada Mica", 46.771, lon=23.59)
    street("Strada Lunga", 46.772, lon=23.59)
    also_index = build(target[0], city="Test", retrieved="2026-10-10", local=("ro",), also=("hu",))[0]
    target[0] = els

    log = []
    index, report = build(els, city="Testville", retrieved="2026-10-10", local=("en",), log=log,
                          map_stations=["Barn", "Works Halt", "Members Halt", "Park Row", "Boyle Square",
                                        "Drawn Gate", ("Laird Station", 47.6003, -122.31),
                                        ("Mill Road", 47.5900, -122.31), ("Wynford Station", 47.5830, -122.31),
                                        ("Oakwood", 47.5700, -122.31)],
                          articles={"Q930": ["enwiki"], "Q920": ["enwiki"], "Q921": ["enwiki"], "Q922": [], "Q923": ["frwiki"],
                                    "Q924": None},
                          closed_for_works={f"node/{works}", f"node/{gone_id}"})
    worded, worded_report = build(els, city="Testville", retrieved="2026-10-10", local=("en",),
                      closed_for_works={f"node/{works}", f"node/{gone_id}"}, way_words=("place",),
                      kept={f"node/{dam}", f"node/{green}", f"way/{colonia}", f"node/{witnesses}",
                            f"node/{kept_halt}", f"node/{ferry}", f"node/{bridge}"},
                      keep_interchanges=True,
                      keep_named_private=True,
                      station_strip=(" Tram",))
    worded_rows = {(KINDS[r[0]], r[3]) for r in worded["rows"]}
    dropped_rows = {(KINDS[r[0]], r[3]) for r in build(
        els, city="Testville", retrieved="2026-10-10", local=("en",),
        dropped={f"way/{river[3]}": "why", f"node/{shut_halt}": "why", f"node/{ferry}": "why"},
        kept={f"node/{ferry}"},
        closed_for_works={f"node/{works}", f"node/{gone_id}"})[0]["rows"]}
    rows = {(KINDS[r[0]], r[3]) for r in index["rows"]}
    count = defaultdict(int)
    for r in index["rows"]:
        count[(KINDS[r[0]], r[3])] += 1
    alias = {(KINDS[r[0]], r[3]): r[4] for r in index["rows"]}
    not_open = {r["name"] for r in index["stations_not_open"]}
    cases = [
        # (what the rule says, True when the index agrees)
        ("a public street is a row", ("street", "Main Street") in rows),
        ("a private residential street is no row", ("street", "Gated Lane") not in rows),
        ("an access=no unclassified street is no row", ("street", "Gated Court") not in rows),
        ("one public way keeps a private street", ("street", "Half Lane") in rows),
        ("a private street with its own article stays", ("street", "Known Close") in rows),
        ("a busway is no row", ("street", "Bus Road") not in rows),
        ("a raceway is no row", ("street", "Race Bend") not in rows),
        ("a street with a way that is no busway stays", ("street", "Mixed Way") in rows),
        ("a type and a code on a minor way is no name", ("street", "Footpath 104") not in rows),
        ("a way word alone on a minor way is no name", ("street", "The Walk") not in rows),
        ("a description on a minor way is no name", ("street", "Service Road") not in rows),
        ("a way word on a residential street is a name", ("street", "The Avenue") in rows),
        ("a numbered lane on a minor way is a name", ("street", "Lane 5") in rows),
        ("tram platforms of one name are one row", count[("station", "Old Town")] == 1),
        ("a station and a tram stop of one name are two rows", count[("station", "Union")] == 2),
        ("construction=yes on a tram stop is not open", "Future Halt" in not_open
         and ("station", "Future Halt") not in rows),
        ("an opening date after the cache is not open", "Later Station" in not_open),
        ("an opening date behind the cache is open", ("station", "Opened Station") in rows),
        ("an end date behind the cache is closed", ("station", "Shut Station") not in rows
         and "Shut Station" not in not_open),
        ("abandoned=yes on a halt is closed", ("station", "Ghost Halt") not in rows),
        ("usage=tourism is a ride", ("station", "Toy Station") not in rows),
        ("tourism=attraction alone is no ride", ("station", "Peak Tram") in rows),
        ("a station with no rail tag and a business tag is none",
         not any(n == "Car Park Station" for _, n in rows)),
        ("a bare station name with an item stays", ("station", "Monument") in rows),
        ("a bare station name with no item goes", ("station", "Chapel") not in rows),
        ("an abandoned prefix on place drops a place", ("place", "Old Village") not in rows),
        ("a place live and under construction alike stays", ("place", "New Quarter") in rows),
        ("demolished=yes drops a place", ("place", "Flag Hamlet") not in rows),
        ("a place live and abandoned alike stays", ("place", "Twice Hamlet") in rows),
        ("an island with its own article is a landmark", ("landmark", "Green Island") in rows),
        ("an islet with no article is no row", not any(n == "Bare Islet" for _, n in rows)),
        ("a district with its own article is a place", ("place", "North District") in rows),
        ("a district with no article is no row", not any(n == "South District" for _, n in rows)),
        ("an estate area with its own article is a place", ("place", "Model Dwellings") in rows),
        ("an estate area with no article is no row", ("place", "Plain Dwellings") not in rows),
        ("two place rows of one name within 300 m are one", count[("place", "Riverside")] == 1),
        ("two place rows of one name 660 m apart are two", count[("place", "Hillside")] == 2),
        ("two junction rows of one name within 300 m are one", count[("junction", "Five Ways")] == 1),
        ("two landmark rows that fold alike are one, the other spelling an alias",
         sum(count[("landmark", n)] for n in ("St. Mary's Church", "St Marys Church")) == 1
         and any("Mary" in alias.get(("landmark", n), "") for n in ("St. Mary's Church", "St Marys Church"))),
        ("a grave with an item and no article is no row", ("landmark", "Ada Person") not in rows),
        ("a grave with its own article is a row", ("landmark", "Bea Person") in rows),
        ("a grave under its subject's article is no row", ("landmark", "Cy Person") not in rows),
        ("a grave whose article the tags cannot place stays", ("landmark", "Dee Person") in rows),
        ("a plaque with an item and no article is no row", ("landmark", "Eli Person") not in rows),
        ("a statue with an item stays", ("landmark", "Fay Person") in rows),
        ("a bare type word with its own article is a row", ("landmark", "Monument") in rows),
        ("a bare type word under the type's article is no row", ("landmark", "Fountain") not in rows),
        ("a bare type word under a shared article is no row", ("landmark", "Sundial") not in rows),
        ("a private operator with its own article is a row", ("landmark", "Hill College") in rows),
        ("a brand with its own article is no row", ("landmark", "Brand Museum") not in rows),
        ("private access on a library with its own article is a row", ("landmark", "Fenced Library") in rows),
        ("private access on a garden stays a home's", ("landmark", "Fenced Garden") not in rows),
        ("private access on a palace stays a home's", ("landmark", "Fenced Palace") not in rows),
        ("a minor historic object with its own article is a row", ("landmark", "Old Marker") in rows),
        ("a minor historic object with no article is no row", ("landmark", "Lost Marker") not in rows),
        ("a memorial whose article names the object is a row", ("landmark", "Stone of Remembrance") in rows),
        ("a memorial whose article could be its subject's is left out", ("landmark", "Wayside Saint") not in rows),
        ("a razed building is no row", ("landmark", "Razed Hall") not in rows),
        ("a garden on a demolished church's site stays", ("landmark", "Garden On Site") in rows),
        ("an abandoned historic site stays", ("landmark", "Old Fort") in rows),
        ("an abandoned park is no row", ("landmark", "Empty Park") not in rows),
        ("a park under construction is no row", ("landmark", "New Park") not in rows),
        ("a park live and under construction alike stays", ("landmark", "Both Park") in rows),
        ("a historic object live and razed alike stays", ("landmark", "Both Hall") in rows),
        ("a museum reopening later, with a start date, stays", ("landmark", "Reopening Museum") in rows),
        ("a museum not yet open is no row", ("landmark", "Unbuilt Museum") not in rows),
        ("a place closed for works, named by id, stays", ("landmark", "Closed Museum") in rows),
        ("a razed object is never kept by id", ("landmark", "Listed Ruin") not in rows),
        ("a disused prefix drops nothing", ("landmark", "Disused Fountain") in rows),
        ("an item on three rows admits none", not any(n.startswith("Piece") for _, n in rows)),
        ("an item on two rows admits both", count[("landmark", "Pair One")] + count[("landmark", "Pair Two")] == 2),
        ("a pedestrian area with its own article is a landmark", ("landmark", "Market Square") in rows),
        ("a pedestrian area under another thing's article is no row", not any(n == "Plain Plaza" for _, n in rows)),
        ("a bridge on a road, no street row of its name, is a landmark under bridge:name",
         ("landmark", "Iron Bridge") in rows and "River Road" in alias.get(("landmark", "Iron Bridge"), "")),
        ("a street's way with no street row of its name stays a landmark", ("landmark", "Lone Steps") in rows),
        ("a register entry with a Wikidata entry of its own is a row", ("landmark", "Lone Armory") in rows),
        ("an engine with a Wikidata entry and no article is no row", ("landmark", "Lone Engine") not in rows),
        ("an object kept by id stays against the register and bare-type rules",
         ("landmark", "Lock Dam") not in rows and ("landmark", "Greenway") not in rows
         and ("landmark", "Lock Dam") in worded_rows and ("landmark", "Greenway") in worded_rows),
        ("a city that keeps its interchange names keeps them", ("street", "Mill Interchange") in worded_rows
         and ("street", "Mill Island") in worded_rows),
        ("a disused place of worship with an entry of its own stays", ("landmark", "Known Chapel") in rows),
        ("a stop-area relation no other row stands for stays", ("station", "Tram Halt Group") in rows),
        # --- The second batch (2026-10-13).
        ("a street private on a residential way and on an alley is no row", ("street", "Shut Alley") not in rows),
        ("a private street with an open alley stays", ("street", "Open Alley") in rows),
        ("a highway tag listing platform is no street", ("street", "Platform Road") not in rows),
        ("an interchange's name is no street", ("street", "Mill Interchange") not in rows),
        ("an onramp's name is no street on any way", ("street", "Mill Road Onramp") not in rows),
        ("a name ending Ramp on a ramp-class way is no street", ("street", "Mill Road Ramp") not in rows),
        ("a name ending Ramp on a road stays", ("street", "Hill Ramp") in rows),
        ("a name ending Drwy is no street on any way", ("street", "Depot Drwy") not in rows),
        ("a name ending Driveway on a minor way is no street", ("street", "Depot Plaza Driveway") not in rows),
        ("a name ending Driveway on a residential street stays", ("street", "Queen Driveway") in rows),
        ("a circular junction on motorway ways is an interchange", ("street", "Mill Island") not in rows),
        ("a named roundabout stays, and is counted", ("street", "Mill Circle") in rows
         and report.get("street_roundabout_kept") == 1),
        ("a managed lane's label on a motorway is no street", ("street", "I 5 HOV") not in rows),
        ("a lane label on a residential street stays", ("street", "Express Lane") in rows),
        ("Alley and digits, a hidden mark set aside, is no name",
         not any(n.startswith("Alley 87582") for _, n in rows)),
        ("an alley named by two streets is no name", ("street", "12th Avenue 13th Avenue Alley") not in rows),
        ("an alley with a name stays", ("street", "Matsui Alley") in rows),
        ("an alley named by two streets is no name on a residential way either",
         ("street", "1st Street 2nd Street Alley") not in rows),
        ("a path between two streets is no name", ("street", "Path between Oak Drive and Elm Drive") not in rows),
        ("a cycle facility named for its street is no name", ("street", "M Street Bike Path") not in rows),
        ("a cycle path with a name of its own stays", ("street", "River Bike Path") in rows),
        ("a trail named for a road stays", ("street", "Mill Road Trail") in rows),
        ("Back Lane is a name", ("street", "Back Lane") in rows),
        ("a city's own way word admits a minor way", ("street", "Hosier Place") not in rows
         and ("street", "Hosier Place") in worded_rows),
        ("a city's own way word admits no private way", ("street", "Gated Place") not in worded_rows),
        ("a stop-area relation is no station row", not any(n == "Union (all platforms)" for _, n in rows)),
        ("a bus station listing a rail mode is no station", not any(n == "Central Bus Hub" for _, n in rows)),
        ("a station outline beside its station is no row", not any(n == "Harbor Station Building" for _, n in rows)
         and ("station", "Harbor") in rows),
        ("a station object with no railway tag, a rail mode and no station beside it stays",
         ("station", "Far Depot") in rows),
        ("a station object with no railway tag and no rail mode is no row",
         not any(n == "Bus Yard" for _, n in rows)),
        # --- The third list (2026-10-13), German and Korean.
        ("German: a way word ends a compound", ("street", "Kirchweg") in de_rows),
        ("German: a leading preposition reads as a way", ("street", "Zum Hafen") in de_rows),
        ("German: a footway with no way word is no street", ("street", "Spielgerät") not in de_rows),
        ("German: a leak word drops a street", ("street", "Zufahrt Nord") not in de_rows),
        ("German: a bare type word is no name", ("landmark", "Kapelle") not in de_rows),
        ("a code beside a path type on a minor way is no name", ("street", "Weg 5") not in de_rows),
        ("Straße and a number is a name", ("street", "Straße 5") in de_rows),
        ("a name before the path type and a number is a name", ("street", "Volksgartenweg 1") in de_rows),
        ("a park whose name leads with a house word is the house's", ("landmark", "Villa Lemm") not in de_rows
         and ("landmark", "Schlosspark") in de_rows),
        ("a name ending (abgebrannt) is gone", not any(n.startswith("Alte Mühle") for _, n in de_rows)),
        ("a name led by Ehem. stays", ("landmark", "Ehem. Rathaus") in de_rows),
        ("a Stolperschwelle is read as a Stolperstein", ("landmark", "Betraum") not in de_rows),
        ("Korean: the third list's bare type words are no names", ("landmark", "족구장") not in ko_rows),
        ("Korean: a numbered park lot is a code beside a type", ("landmark", "115호 어린이공원") not in ko_rows),
        ("a park an apartment estate's office runs is no row", ("landmark", "포도원놀이터") not in ko_rows
         and ("landmark", "포도원공원") in ko_rows),
        ("a customers-only service road is no street", ("street", "후문 진입로") not in ko_rows
         and ("street", "정문 진입로") in ko_rows),
        ("the private-street rule reads living_street", ("street", "Shut Close") not in rows),
        # --- The fourth pass (2026-10-13).
        ("public art whose own entry has an article in the cache is a row", ("landmark", "Iron Horse") in rows),
        ("public art under an entry two objects share is no row", not any(n.startswith("Twin") for _, n in rows)),
        ("public art whose article bears its own name is a row, though a subject tag repeats it",
         ("landmark", "Bean Gate") in rows and ("landmark", "Old Mayor") not in rows),
        ("a library whose entry has no article is no row", ("landmark", "Town Library") not in rows
         and ("landmark", "Null Library") not in rows),
        ("a library whose own entry has an article is a row", ("landmark", "Great Library") in rows),
        ("the entries the lookup is asked about are listed",
         {"Q907", "Q920", "Q922", "Q923", "Q924"} <= set(index["wikidata_asked"]) and "Q921" not in index["wikidata_asked"]),
        ("the lookup is narrow by rule: public art and libraries, no other kind",
         article_lookup_kind({"tourism": "artwork"}) == "artwork"
         and article_lookup_kind({"amenity": "library"}) == "library"
         and article_lookup_kind({"tourism": "museum", "wikidata": "Q1"}) is None
         and article_lookup_kind({"historic": "memorial", "wikidata": "Q1"}) is None
         and {k for _, _, k in ARTICLE_LOOKUP_KINDS} == {"artwork", "library"}),
        ("has_article: the tag, or an own entry with an article",
         has_article({}, None, own=True) and has_article({"wikidata": "Q1"}, {"Q1": ["enwiki"]})
         and not has_article({"wikidata": "Q1"}, {"Q1": []}) and not has_article({"wikidata": "Q1"}, {"Q1": None})
         and not has_article({"wikidata": "Q1"}, {"Q1": ["enwiki"]}, own_entry=False)
         and not has_article({"wikidata": "Q1"}, None)),
        ("int_name is an alias", "Cheval de Fer" in alias.get(("landmark", "Iron Horse"), "")),
        ("an entry that is the object's subject's admits it to nothing", ("landmark", "Poet Bench") not in rows),
        ("a monument drawn in segments is one row", count[("landmark", "Old Wall")] == 1),
        ("two nodes of one name and entry far apart stay two", count[("landmark", "Cast Statue")] == 2),
        ("a place-of-worship node beside the way of its name is one row", count[("landmark", "St Luke")] == 1),
        ("a station with passenger=no is no station", ("station", "Freight Yard") not in rows),
        ("a map station tagged public_transport=no stays", ("station", "Works Halt") in rows),
        ("a station the map draws at its place stays against a disused tag (the station guard)",
         ("station", "Laird") in rows and ("station", "Laird") not in worded_rows),
        ("a disused station beside a map station of another name is no row", ("station", "Old Depot") not in rows),
        ("a disused station far from the map station of its name is no row", ("station", "Wynford") not in rows),
        ("a station with a dated closure is no row, a map station or not", ("station", "Oakwood") not in rows),
        ("a city's station ending is stripped", ("station", "Mill Stop Tram") in rows
         and ("station", "Mill Stop") in worded_rows and ("station", "Mill Stop Tram") not in worded_rows),
        ("Danish: store is no leak word, and a glued street passes beside one",
         ("street", "Store Kongensgade") in small["da"] and ("street", "Hotel Strandvej") in small["da"]
         and ("street", "Kirkestien") in small["da"] and ("place", "Store Plads") in small["da"]),
        ("Norwegian: a glued way word", ("street", "Storgata") in small["nb"]),
        ("Swedish: a glued way word, and -gården a street ending on any way", ("street", "Kungsgatan") in small["sv"]
         and ("street", "Stora gården") in small["sv"] and ("street", "Lilla gården") in small["sv"]),
        ("Latvian: a way word, and a house word closing a name", ("street", "Brīvības iela") in small["lv"]
         and ("landmark", "Mindeļa villa") not in small["lv"]),
        ("Romanian: a leading way word", ("street", "Strada Mare") in small["ro"]),
        ("Italian: a leading way word, beside a leak word too, and a bare type word",
         ("street", "Via Roma") in small["it"] and ("street", "Via Albergo Vecchio") in small["it"]
         and ("landmark", "Chiesa") not in small["it"]),
        ("Greek: a genitive ending and a way word", ("street", "Αριστοτέλους") in small["el"]
         and ("street", "Οδός Ερμού") in small["el"]),
        ("a language declared below the floor is read and measured, and stops nothing",
         any("Nagy utca" in r[4] for r in also_index["rows"]) and also_index["languages"]["also"] == ["hu"]
         and 0 < also_index["languages"]["coverage"]["hu"] < LOCAL_MIN and "Hungarian" not in also_index["languages"]["listed"]),
        ("fold_name: final sigma and the cedilla letters fold with their twins",
         fold_name("ΟΔΟΣ") == fold_name("οδός") and fold_name("Ştefan Ţepeş") == fold_name("Ștefan Țepeș")),
        ("a river row carries the id of its lowest way",
         f"way/{river[0]}" in index["row_osm"] and f"way/{river[1]}" not in index["row_osm"]),
        ("a river is dropped whole by the id of one of its ways", ("landmark", "Lost Creek") in rows
         and ("landmark", "Lost Creek") not in dropped_rows and ("landmark", "Mill Creek") in dropped_rows),
        ("a street closed to traffic and open on foot is no private street", ("street", "Zone Street") in rows),
        ("a station's outline under its node's name, a station word aside, is one row with it",
         count[("station", "Depot Halt")] == 1 and ("station", "Depot Halt Station") not in rows),
        ("a lone station object with a network tag stays", ("station", "Net Hall") in rows),
        ("a station outline with no node of its name stays", ("station", "Lone Hall") in rows),
        ("a bare type word behind an article is bare", ("landmark", "The Fountain") not in rows),
        ("two bare words either side of a dash are bare", not any(n == "Fountain - Chapel" for _, n in rows)),
        ("a bare word beside a real name stays", ("landmark", "Fountain - Saint Ann") in rows),
        ("a subway station under a bare type word stays", ("station", "Greenway") in rows),
        ("a halt under a bare type word, no network and not on the map, goes", ("station", "Sanctuary") not in rows),
        ("a network's halt under a bare type word stays", ("station", "Parkland") in rows),
        ("a station of the map under a bare type word stays", ("station", "Barn") in rows),
        ("an estate area kept by id stays", ("place", "Colonia Real") not in rows
         and ("place", "Colonia Real") in worded_rows),
        # --- The fifth pass (2026-10-13).
        ("a place of worship named by its hall type and denomination is no row",
         ("landmark", "Kingdom Hall of Jehovah's Witnesses") not in rows),
        ("a place of worship named by its denomination and one hall word is no row",
         ("landmark", "Methodist Church") not in rows),
        ("a place of worship named by one hall-type word is no row", ("landmark", "Gurdwara") not in rows),
        ("an ordinal keeps a place of worship", ("landmark", "First Baptist Church") in rows),
        ("a saint keeps a place of worship", ("landmark", "St Agnes Catholic Church") in rows),
        ("a second hall-type word keeps a place of worship", ("landmark", "Temple Baptist Church") in rows),
        ("a place of worship with an article of its own stays", ("landmark", "Friends Meeting House") in rows),
        ("a place of worship kept by id stays", ("landmark", "Jehovah's Witnesses") not in rows
         and ("landmark", "Jehovah's Witnesses") in worded_rows),
        ("the worship rule reads places of worship only", ("landmark", "Baptist Church") in rows),
        ("a station is never read by the worship rule", ("station", "Methodist Church") in rows),
        ("worship_only: a denomination as its mappers spell it",
         worship_only("Kingdom Hall of Jehovah's Wittnesses", ()) and worship_only("Jehovahs Witness", ())
         and not worship_only("Jehovah Shalom Church", ())),
        ("worship_only: a word outside a listed phrase keeps a name",
         not worship_only("Christ Church", ()) and not worship_only("Temple Church", ())
         and worship_only("Church of Christ", ()) and worship_only("The Salvation Army", ())),
        ("worship_only: a city's languages are read, and no other",
         worship_only("Salle du Royaume des Témoins de Jéhovah", ("fr",))
         and not worship_only("Salle du Royaume des Témoins de Jéhovah", ("pt",))
         and not worship_only("Église Saint-Paul", ("fr",)) and worship_only("Igreja Batista", ("pt",))
         and worship_only("創価学会", ("ja",)) and worship_only("여호와의증인 왕국회관", ("ko",))
         and not worship_only("순복음교회", ("ko",))),
        ("a station closed to the public is no row", ("station", "Senate Halt") not in rows),
        ("a station of the map tagged access=private stays (the station guard)", ("station", "Members Halt") in rows
         and ("station", "Members Halt") not in worded_rows),
        ("access=no on a station is not read", ("station", "Fenced Halt") in rows),
        ("two stations of the map that share an entry are two rows", count[("station", "Park Row")] == 1
         and count[("station", "Boyle Square")] == 1
         and "Boyle Square" not in alias.get(("station", "Park Row"), "")),
        ("a station under another name keeps its row, whatever entry it shares",
         ("station", "Park Row Concourse") in rows
         and "Park Row Concourse" not in alias.get(("station", "Park Row"), "")),
        ("with no map station named, stations of three names that share an entry are three rows",
         sum((k, n) in worded_rows for k, n in (("station", "Park Row"), ("station", "Park Row Concourse"),
                                                ("station", "Boyle Square"))) == 3),
        # --- The sixth pass (2026-10-13).
        ("a denomination after a body's name keeps a place of worship",
         ("landmark", "Church of Christ Presbyterian") in rows and ("landmark", "Church of God") not in rows),
        ("a nationality outside a denomination's name keeps a place of worship",
         ("landmark", "Russian Baptist Church") in rows and ("landmark", "Greek Orthodox Church") not in rows),
        ("an entry of its own with an article in the cache keeps a place of worship",
         ("landmark", "Gospel Hall") in rows),
        ("an entry the cache does not hold keeps none", ("landmark", "Kingdom Hall") not in rows),
        ("a religious office tagged a place of worship is no row",
         ("landmark", "Presbytery of Testville") not in rows
         and ("landmark", "Catholic Diocese of Testville") not in rows),
        ("an office word no reader's row supports keeps its row", ("landmark", "St Clare Convent") in rows),
        ("worship_office: a head leads the name, a CJK word stands anywhere, a city's languages only",
         worship_office("Seminário Maior de São José", ("pt",)) and not worship_office("Igreja do Seminário", ("pt",))
         and not worship_office("Seminário Maior de São José", ("es",)) and worship_office("八幡神社社務所", ("ja",))
         and not worship_office("八幡神社", ("ja",))),
        ("a named convent is a place and keeps its row", es_rows[("landmark", "Convento de las Clarisas")] == 1
         and es_rows[("landmark", "Iglesia del Convento")] == 1
         and ("landmark", "Convento de Santa Teresa") in small["pt"]),
        ("Portuguese: a seminary tagged a place of worship is no row, by the name's head",
         ("landmark", "Seminário Maior") not in small["pt"] and ("landmark", "Igreja do Seminário") in small["pt"]),
        ("Polvorín behind an article is a name", not bare_type("El Polvorín", ("es",)) and bare_type("Hórreo", ("es",))),
        ("Korean: a church's education hall is no row", ("landmark", "시험교회 교육관") not in ko_rows
         and ("landmark", "시험교회") in ko_rows),
        ("a park a homes association runs is no row", ("landmark", "Lakeside Green") not in rows),
        ("an estate's park with an article of its own stays", ("landmark", "Founders Green") in rows),
        ("a square a mall runs is no row", ("landmark", "Mall Court") not in rows),
        ("a park any other body runs stays", ("landmark", "Rotary Green") in rows),
        ("Korean: an estate's brand and a facility word is no row", ("landmark", "삼산타운어린이놀이터") not in ko_rows),
        ("Korean: a park named for an estate stays", ("landmark", "신암그린타운공원") in ko_rows),
        ("Korean: a facility word with no estate brand stays", ("landmark", "새봄어린이놀이터") in ko_rows),
        ("an operator's name heading a facility's name is no row", ("landmark", "한빛마을 주민 운동장") not in ko_rows),
        ("an operator's name inside a facility's name is not read", ("landmark", "새봄한빛회 운동장") in ko_rows),
        ("estate_facility: parks, playgrounds and squares only, and the inside words",
         estate_facility({"leisure": "park"}, ["セントプレイスシティー内の広場"], ("ja",)) is not None
         and estate_facility({"historic": "monument", "operator": "X Condominio"}, ["Y"], ("pt",)) is None
         and estate_facility({"leisure": "park", "operator": "Belcanto"}, ["Parque Belcanto"], ("es",)) is None
         and estate_facility({"leisure": "park", "operator": "Riverside"}, ["Riverside Park"], ("en",)) is None),
        ("Spanish: a park named as a square a street row bears is one row",
         es_rows[("landmark", "Plaza Mayor")] == 0 and es_rows[("street", "Plaza Mayor")] == 1),
        ("Spanish: a park named as a square with no street of its name stays",
         es_rows[("landmark", "Plaza Nueva")] == 1),
        ("Spanish: a park and a street that differ by a joiner are one row, the park's spelling an alternate",
         es_rows[("landmark", "Plaza del Japón")] == 0 and es_alias[("street", "Plaza Japón")] == "Plaza del Japón"),
        ("Spanish: a park spelled another way than its street keeps its own row",
         es_rows[("landmark", "Plaza John Kennedy")] == 1 and es_alias[("street", "Plaza Jonh Kennedy")] == ""),
        ("Spanish: a park under a street word, or no way word, stays beside a street of its name",
         es_rows[("landmark", "Avenida de Brasil")] == 1 and es_rows[("landmark", "Bosque Viejo")] == 1),
        ("worship_office: an English word is not read in a name that holds CJK",
         worship_office("Catholic Diocese of Testville", ()) and not worship_office("基督之母堂 Catholic Diocese Church", ())),
        ("Spanish: the sixth pass's bare type words and a denomination's temple are no names",
         es_rows[("landmark", "Hórreo")] == 0 and es_rows[("landmark", "Templo budista")] == 0),
        ("Spanish: a freight station by its name is no row", es_rows[("station", "Estación de Mercancías Norte")] == 0),
        ("Spanish: a freight station the map draws stays (the station guard)",
         es_rows[("station", "Estación de Mercancías Sur")] == 1),
        ("operational_status=closed closes a station", es_rows[("station", "Estación Cerrada")] == 0),
        ("a station entrance beside its station's row is no row", count[("station", "Gate Halt")] == 1),
        ("a ticket gate tagged a station is no row", ("station", "East Ticket Gate") not in rows),
        ("an entrance the map draws, with no other row, stays (the station guard)",
         ("station", "Drawn Gate") in rows and ("station", "Drawn Gate") not in worded_rows),
        ("a bus rapid transit station is no rail station on its network tag",
         not any(n == "Rapid Bus Stop" for _, n in rows) and ("station", "Net Hall") in rows),
        ("a suburb's boundary beside its own suburb node is no second row", count[("place", "Southside")] == 1),
        ("a suburb's boundary 30 km from a node of its name stays", ("place", "Farside (North)") in rows),
        ("a closing bracket is set aside when a boundary is matched to its node",
         ("place", "Nearside (East)") not in rows and ("place", "Nearside") in rows),
        ("ways with no entry are the segments of the relation that carries it",
         count[("landmark", "Museum Railway")] == 1
         and any(o.startswith("relation/") for r, o in zip(index["rows"], index["row_osm"])
                 if r[3] == "Museum Railway")),
        ("one way beside a like-named relation far off stays", count[("landmark", "Lone Mill")] == 2),
        ("bare_type: the sixth pass's spaced, numbered and placeholder forms",
         bare_type("어린이 공원", ("ko",)) and bare_type("제1호근린공원", ("ko",)) and bare_type("開発公園", ("ja",))
         and bare_type("開発2号公園", ("ja",)) and bare_type("Estação 3", ("pt",))
         and not bare_type("Estação Central", ("pt",)) and bare_type("第一中庭", ("zh",))
         and bare_type("Hôtel particulier", ("fr",)) and not bare_type("어린이 공원", ("ja",))),
        ("a settlement whose own name is a type word keeps its place row, and a landmark so named goes",
         ("place", "大師堂") in small["ja"] and ("landmark", "大師堂") not in small["ja"]),
        ("Korean: a spaced and a numbered type word are no names",
         ("landmark", "어린이 공원") not in ko_rows and ("landmark", "제1호근린공원") not in ko_rows),
        ("French: a mansion named Hôtel de or Hôtel d' is no leak", ("landmark", "Hôtel de Lauzun") in fr_rows
         and ("landmark", "Hôtel d'Aumont") in fr_rows),
        ("French: a hotel's trade name is still a leak", ("landmark", "Hôtel Ibis Centre") not in fr_rows),
        ("French: a hotel business named as a mansion is held out by its tag",
         ("landmark", "Hôtel de Paris") not in fr_rows),
        ("French: Hôtel particulier as a whole name is a bare type word",
         ("landmark", "Hôtel particulier") not in fr_rows),
        ("leak_hits: no junction row, no French mansion, no allowed street word; the old test lists all three",
         ("junction", "Carrefour de l'Hôtel") in fr_rows and ("street", "Rue de la Brasserie") in fr_rows
         and leak_hits(fr_index, ("fr",)) == []
         and {n for n, _ in leak_hits(fr_index, ("fr",), exempt=False)}
         == {"Carrefour de l'Hôtel", "Rue de la Brasserie", "Hôtel de Lauzun", "Hôtel d'Aumont"}),
        ("leak_word: the mansion reading is a landmark's and a French city's",
         leak_word(["Hôtel de Lauzun"], ("fr",)) == "hôtel" and leak_word(["Hôtel de Lauzun"], ("fr",), landmark=True) is None
         and leak_word(["Hotel de Lauzun"], ("nl",), landmark=True) == "hotel"
         and leak_word(["Grand Hôtel de Lauzun"], ("fr",), landmark=True) == "hôtel"),
        ("a name ending (FECHADO) says the thing is closed",
         HISTORICAL_NAME.search("Motel Kasulo (FECHADO)") is not None),
        # Lines reach the search box from the map, never from the index: no
        # kind holds one, so no index rule can drop a line by its name.
        ("the index holds no kind for a transit line", "line" not in KINDS and "route" not in KINDS),
        ("bare_type: Spanish estate words and a numbered cluster",
         bare_type("Casa Club", ("es",)) and bare_type("Cluster 12", ("es",)) and not bare_type("Coto Real", ("es",))),
        ("bare_type: an earth-god shrine under its type alone",
         bare_type("福德祠", ("zh",)) and bare_type("福德祠(土地公廟)", ("zh",)) and not bare_type("福安宮", ("zh",))),
        ("bare_type: a French article and a two-language pair",
         bare_type("Le Château", ("fr", "nl")) is False and bare_type("La Fontaine", ("fr",))
         and bare_type("Fontaine - Fontein", ("fr", "nl")) and not bare_type("Fontaine - Manneken", ("fr", "nl"))),
        ("a locomotive with an entry and no tourism tag is an exhibit", ("landmark", "Engine 3100") not in rows
         and ("landmark", "Royal Train") in rows),
        ("a locomotive under an article of its own name stays", ("landmark", "Zephyr") in rows),
        ("a customers-only service road under a name stays", ("street", "시험 안길") in ko_rows),
        ("exhibits sharing one entry are admitted by their class's", not any(n.startswith("Coach") for _, n in rows)),
        ("a vehicle under its kind's article is an exhibit", ("landmark", "EMU Demo") not in rows
         and ("landmark", "Old 99") in rows),
        ("a site relation repeating a row's entry far off is no row", count[("landmark", "City College")] == 1),
        ("a site relation on its object stays", ("landmark", "Art School Grounds") in rows),
        ("tram stops of one name 200 m apart are one row", count[("station", "Quay Stop")] == 1),
        ("a direction note in brackets does not part a stop's platforms",
         count[("station", "Harbour (dir North)")] + count[("station", "Harbour (dir South)")] == 1),
        ("two station rows of one name and no second operator are one row", count[("station", "Mill Junction")] == 1),
        ("two operators' stations of one name stay two rows", count[("station", "Two Lines")] == 2),
        ("a route relation is no station", not any(n == "Trunk Line" for _, n in rows)),
        ("a school tagged a station with no railway tag is no station", ("station", "East School") not in rows),
        ("a bus stop is no landmark", not any(n == "Library West Gate" for _, n in rows)),
        ("PLACE_KEPT admits a row for an object in no landmark class",
         ("landmark", "Old Ferry Terminal") in worded_rows and ("landmark", "Old Ferry Terminal") not in rows),
        ("a kept bridge under a tram stop's name is its own landmark row",
         ("landmark", "Tram Bridge") in worded_rows and ("station", "Tram Bridge") in worded_rows
         and ("landmark", "Tram Bridge") not in rows),
        ("PLACE_DROPPED reaches a station by id, and outranks PLACE_KEPT",
         ("station", "Dropped Halt") in rows and ("station", "Dropped Halt") not in dropped_rows
         and ("landmark", "Old Ferry Terminal") not in dropped_rows),
        ("PLACE_KEPT holds a station against the closed tests", ("station", "Kept Halt") in worded_rows
         and ("station", "Kept Halt") not in rows),
        ("Japanese: a freight terminal by its name or its operator is no station",
         ("station", "川崎貨物") not in small["ja"] and ("station", "北港") not in small["ja"]
         and ("station", "南港") in small["ja"]),
        ("Japanese: a station named as a former or closed site is no row",
         ("station", "工場跡地") not in small["ja"] and not any(n in ("東口 (閉鎖)", "西町（廃駅）") for _, n in small["ja"])),
        ("a height is no name", junk_name("109m") and junk_name("120.6m") and junk_name("222M")
         and not junk_name("8 Mile") and not junk_name("M109")),
        ("the denomination rule reads a leading elided article and two listed bodies spelled out",
         worship_only("L'Église de Jésus-Christ des Saints des Derniers Jours", ("fr",))
         and not worship_only("L'Église Saint-Paul", ("fr",))
         and worship_only("パーフェクトリバティー教団", ("ja",))
         and worship_only("Salão das Testemunhas de Jeová", ("pt",))),
        ("a borough's boundary does not fold into its town hall", ("place", "Ward Nine") in rows
         and ("landmark", "Ward Nine Town Hall") in rows),
        ("a subway station also tagged a bus station is a station", ("station", "Broadview") in rows),
        ("a web address is no name", junk_name("https://example.org/") and junk_name("www.example.org")
         and not junk_name("World Wide Web Plaza") and not any("example.org" in n for _, n in rows)),
        ("a stop's platform drawn as a footway is no street", ("street", "Tramstop Street") not in rows
         and ("street", "Halt Lane") not in rows),
        ("own_article: a list article with an anchor is not the object's",
         own_article({"wikipedia": "de:Liste der Kulturdenkmäler in Bremen-Mitte#1500,T008"}, ["Bacchus"])[0] == "not"),
        ("public art with an entry and no article is no row", ("landmark", "Bronze Horse") not in rows),
        ("public art with its own article is a row", ("landmark", "Cloud Gate") in rows),
        ("public art whose article the tags cannot place stays", ("landmark", "Founder Statue") in rows),
        ("a dead railway alignment with no article is no row", not any(n == "Old Branch Line" for _, n in rows)),
        ("a dead railway alignment with an article stays", any(n == "Old Trunk Line" for _, n in rows)),
        ("a standing structure under a railway lifecycle tag stays", ("landmark", "Rail Water Tower") in rows),
        ("station rows of different names sharing an item are two rows, neither an alias",
         count[("station", "Times Square")] == 1 and count[("station", "Port Authority")] == 1
         and "Port Authority" not in alias.get(("station", "Times Square"), "")),
        ("station rows of one name sharing an item within 600 m are one row", count[("station", "Pair Hall")] == 1),
        ("station rows of one name sharing an item 3 km apart are two", count[("station", "Far Hall")] == 2),
        ("station rows sharing an item 3 km apart are two", ("station", "North Loop") in rows
         and ("station", "South Loop") in rows),
        ("an end date with a stray character closes a station", ("station", "Stray Station") not in rows),
        ("a name ending (historical) is no row", not any(n.startswith("Lost Park") for _, n in rows)),
        ("a place named Estates with no item is no row", ("place", "Shady Estates") not in rows),
        ("a place named Estates with an item stays", ("place", "Known Estates") in rows),
        ("a trailer park tagged a hamlet is no row", ("place", "Sunny Trailer Park") not in rows),
        ("a town's boundary beside its node is no second row", count[("place", "Rivertown")] == 1),
        ("a boundary with no node of its name stays", ("place", "Wardville") in rows),
        ("a locality's boundary named like a village elsewhere stays", count[("place", "Newtown")] == 2),
        ("a register entry under an item another object shares is no row",
         ("landmark", "Pump Works") not in rows and ("landmark", "Pump Annex") not in rows),
        ("a register entry with its own article is a row", ("landmark", "Old Dock") in rows),
        ("a numbered building under its district's register number is no row",
         ("landmark", "Building 7") not in rows and ("landmark", "Drill Hall") in rows),
        ("a numbered building under a register number of its own stays", ("landmark", "Building 9") in rows),
        ("a street's way under a tourism tag is no landmark row beside its street row",
         ("landmark", "Famous Street") not in rows and ("street", "Famous Street") in rows),
        ("a pedestrian area under a tourism tag stays a landmark", ("landmark", "Fair Plaza") in rows),
        ("a derelict canal is no row", not any(n == "Old Cut" for _, n in rows)),
        ("a disused place of worship is no row", ("landmark", "Shut Chapel") not in rows),
        ("a standing ruin stays", ("landmark", "Ruined Mill") in rows
         and any(x["class"] == "abandoned_standing" and x["name"] == "Ruined Mill" for x in log)),
        ("the second list's bare type words are no names",
         not any(n in ("Masjid", "Tot Lot") for _, n in rows)),
        ("the report counts the private residential streets", report.get("street_dropped_private_residential") == 4),
        ("with a city's switch on, a named private street stays (none of the four fixtures is code-named)",
         worded_report.get("street_dropped_private_residential", 0) == 0),
        ("the log names a rule for a dropped street",
         any(x["class"] == "street_busway_raceway" and x["name"] == "Bus Road" for x in log)),
        ("own_article: a section is not the object's", own_article({"wikipedia": "en:A#B"}, ["A"])[0] == "not"),
        ("_station_core: a Hangul station word is set aside", _station_core("상무역") == _station_core("상무")
         and _station_core("역") == fold_name("역")),
        ("quiet_stations: a listed uncovered station is accounted for",
         quiet_stations({"B": "why"}, [("A", 1, 1), ("B", 2, 2)], ["B"]) == ([], [])),
        ("quiet_stations: an unlisted uncovered station still fails",
         quiet_stations({"B": "why"}, [("A", 1, 1), ("B", 2, 2), ("C", 3, 3)], ["B", "C"])[0] == ["C"]),
        ("quiet_stations: a listed station that is covered is a problem",
         len(quiet_stations({"A": "why"}, [("A", 1, 1), ("B", 2, 2)], [])[1]) == 1),
        ("quiet_stations: a listed name that is no station of the map is a problem",
         len(quiet_stations({"Z": "why"}, [("A", 1, 1)], [])[1]) == 1),
        ("own_article: the subject's article is not the object's",
         own_article({"wikipedia": "en:X", "subject:wikipedia": "en:X"}, ["Y"])[0] == "not"),
        ("street_description: a local way word with a number is a name",
         street_description("Rua 1", ("pt",)) is None and street_description("Trail #2", ("en",)) is not None),
        ("lifecycle: was: and disused: are not read",
         lifecycle({"was:building": "yes", "disused:building": "yes"}, "2026-10-10") is None),
    ]
    bad = [what for what, ok in cases if not ok]
    for what in bad:
        print(f"BAD   {what}")
    print(f"place_index selftest: {len(cases) - len(bad)} of {len(cases)} cases hold")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(_selftest())
    sys.exit("usage: python pipeline/place_index.py --selftest   (a city's index: its step2b_place_index.py)")
