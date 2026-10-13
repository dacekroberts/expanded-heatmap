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


def _site_url(path, data):
    """The site path of a file under app/static/, stamped with the hash of its
    content `data` (index_url's reason)."""
    rel = path.relative_to(STATIC_DIR.parent).as_posix()
    return f"/app/static/{rel}?v={hashlib.sha256(data).hexdigest()[:12]}"


def summary_path(slug):
    return Path(__file__).parent.parent / "outputs" / slug / "place_search.json"


def files(index, slug):
    """{path: bytes} for the three files an index step writes: the
    intersections file, the index (served as-is: bytes, LF only, no BOM) and
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
    cpath = crossings_path(slug)
    cbytes = json.dumps({"license": index["license"], "schema": SCHEMA, "city": index["city"],
                         "part_of": f"{slug}.json", "rows": cross},
                        ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    # The index carries the intersections file's hashed path, so a rebuilt
    # intersections file is never served from a browser's old copy.
    index["crossings"] = _site_url(cpath, cbytes)
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
    return {cpath: cbytes, index_path(slug): ibytes, summary_path(slug): sbytes}


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
        bare = uncovered_stations(index["rows"], stations)
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
    index, report = build(payload["elements"], city=name, retrieved=retrieved,
                          local=config.PLACE_LANGUAGES, fold=fold, dropped=dropped,
                          visitable=live, rebuilt=rebuilt)
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
    "ka": "Georgian", "da": "Danish", "sv": "Swedish", "nb": "Norwegian", "ro": "Romanian",
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


def leak_word(names, local):
    """The first LEAK_WORD of English or a local language in `names`, after
    LEAK_ALLOW compounds are removed; None when there is none."""
    low = " | ".join(names).lower()
    for code in dict.fromkeys(["en", *local]):
        for allow in LEAK_ALLOW.get(code, ()):
            low = low.replace(allow, " ")
        for word in LEAK_WORDS.get(code, ()):
            if _has_word(word, low):
                return word
    return None


def leak_hits(index, local):
    """[(row name, word)] for every index row whose names carry a LEAK_WORD."""
    out = []
    for r in index["rows"]:
        word = leak_word([r[3]] + (r[4].split("|") if r[4] else []), local)
        if word:
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
    tags += ["alt_name", "alt_name:en", "official_name", "official_name:en",
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


def languages(row_langs, local):
    """Coverage of English and each local language over the index's rows, and
    the languages the page may name, English first, then the local ones."""
    order = list(dict.fromkeys(["en", *local]))
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
    return {"local": list(local), "coverage": coverage, "list_share": LIST_SHARE, "listed": listed}

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
SUFFIX_WAY_LANGUAGES = {"nl", "ko"}
# Street names that carry no street word at all. Czech names a street with a
# preposition ("Na Viničce", "U Vizerky", "Pod Havránkou") or an adjective
# agreeing with the unwritten "ulice" ("Bělohorská", "Goyova"): Prague's
# named footways and tracks lost 2,345 ways to the way-word test alone
# (batch 2a, 2026-10-08). WAY_LEAD is the name's first word, WAY_ENDING the
# ending of its last.
WAY_LEAD = {"cs": ("na", "u", "k", "ke", "pod", "nad", "za", "do", "ve", "v", "při", "před",
                   "mezi", "po", "proti", "přes", "od", "ze", "z")}
# A trailing Roman numeral ("Herálecká II", "Podnikatelská Ⅰ") is set aside first.
WAY_ENDING = {"cs": ("á", "ní", "ova", "ého")}
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
OTHER_MODES = ("bus", "ferry", "trolleybus", "coach", "minibus")
# And by the facility's own tag, where no mode is written: Hong Kong's public
# transport interchanges (amenity=bus_station), ferry piers and the Ngong
# Ping cable-car terminal (aerialway=station), 2026-10-08.
NOT_RAIL = {"amenity": {"bus_station", "ferry_terminal"}, "aerialway": {"station"}}
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
                  "cs": ("dům", "vila"), "nl": ("huis",)}
# And where the house word CLOSES the name (batch 2b, 2026-10-08): Korean 가옥
# and 고택 (a traditional house), 옛집 (an old house), 생가 (a birthplace),
# 저택 and 주택; Chinese 故居 and 舊居 (a former residence), 大宅, 別墅 and
# 宅; Georgian სახლი (a house), as the last word. A house-museum (tourism=
# museum, სახლ-მუზეუმი) passes _public_home, as a museum in a 생가 does.
HOME_NAME_END = {"ko": ("가옥", "고택", "옛집", "생가", "저택", "주택"),
                 "zh": ("故居", "舊居", "大宅", "別墅", "宅"), "ka": ("სახლი",)}


# historic=* values that are a house: a manor is OSM's manor house or country
# house (Marseille's 130-odd bastides and its town mansions, the hôtels
# particuliers, batch 2a, 2026-10-08), held to _public_home as historic=house is.
HOME_HISTORIC = {"house", "manor"}
# Amenities that make a historic house a civic place (_home). Places of
# worship are not among them: a house church can be someone's home.
CIVIC_AMENITIES = {"townhall", "arts_centre", "community_centre", "library", "theatre"}


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
                and any(_home_name(n, local) for n in names)))


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
            or any(m in low for m in JUNK_MARKS) or bool(_CONTACT.search(name)))


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
           "perennial border", "mooring anchors", "solarium"),
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
           "유아숲체험장", "가족조각상", "호상비문", "강학공간"),
    "zh": ("祠堂", "土地", "土地廟", "土地公", "伯公", "社壇", "碉堡", "涼亭", "公園", "遊樂場", "休憩處",
           "觀景台", "廟",
           # The outside name net's read of the 19 built cities (owner, 2026-10-12).
           "炮台"),
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
           "iglesia católica", "iglesia mormona", "jardín botánico", "casa de retiros"),
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
    "ka": ("ეკლესია", "პარკი", "სკვერი", "ძეგლი", "შადრევანი", "ბაღი", "სასაფლაო"),
}


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
    "ko": re.compile(r"\d+호 공원"),
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
    low = unicodedata.normalize("NFKC", name).lower().strip(" .,;:()")
    if _CJK_WORD.search(low):
        low = re.sub(r"[\s#]*\d+$", "", low).strip()
        return any(low in BARE_TYPE_NAMES.get(c, ()) for c in ("en", *local))
    # Accents set aside for a Latin word: Mexico City's "jardin" and "Area
    # verde" are the listed words unaccented (batch 3, 2026-10-11).
    low = _unaccent(low)
    return any(low in _BARE_FOLDED.get(c, ()) for c in ("en", *local))


def _unaccent(s):
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))


_BARE_FOLDED = {c: {_unaccent(w) for w in ws} for c, ws in BARE_TYPE_NAMES.items()
                if c not in ("ja", "ko", "zh")}
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
                "el": ("greek",)}


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
                if ws[-1] == w:
                    return True
            elif _CJK_WORD.search(w):
                if low.endswith(w):
                    return True
            elif ws[-1] == w or (code in WAY_WORD_LEADS and ws[0] == w):
                return True
    return False


# Languages whose street word leads the name (_named_street).
WAY_WORD_LEADS = {"fr", "ca", "es", "cs", "pt"}


def _reads_as_way(names, local):
    """True when a name reads as a way in English or a local language: a CJK
    way word anywhere in it (三条小橋), a Latin one as a whole word, or, in a
    language that compounds (SUFFIX_WAY_LANGUAGES), as a word's ending
    ("Nieuwstraat")."""
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


SQUARE_DUP_M = 500
SQUARE_NEAR_M = 150
# Abbreviated square words read in full when a square is compared with the
# streets and squares around it (_square_keys): "nám." is náměstí. The word
# itself stays: Barcelona's Placeta del Pi and Plaça del Pi are two squares.
SQUARE_ABBR = {"nam": "namesti"}


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


# THE INDEX REACHES THE WHOLE MAP (owner, 2026-10-12). Mexico City's index
# landed cut to the city proper after its map became regional: the 11
# stations in the four added municipios were on the map and not in the
# search, with 0 or 1 indexed places within 1 km of each. The rule: every
# station the map draws has at least one indexed place, other than a
# station, within COVER_KM. Measured on the 19 indexes of 2026-10-12, the
# emptiest covered stations hold 2 (Montreal's Anse-a-l'Orme), 3 (Kyoto's
# Hozukyo and Kibuneguchi) and 4 (Busan's Seokdae), so zero is a boundary
# cut and not a quiet station. Re-measure before raising the floor.
# run() exits on it; scripts/check_place_search.py H re-reads it.
COVER_KM = 1.0
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


def uncovered_stations(rows, stations, km=None):
    """Names of the stations with no index row, other than a station row,
    within COVER_KM. rows are the index's ([kind, lat, lon, ...], kind 0 a
    station); a 0.01 degree grid keeps it linear."""
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
            out.append(name)
    return out


def _dist_m(a, b):
    lat = math.radians((a[0] + b[0]) / 2)
    return math.hypot((a[0] - b[0]) * 110540.0, (a[1] - b[1]) * 111320.0 * math.cos(lat))


def _r(x):
    # 4 decimals, about 11 m: the search jumps to zoom 16 and marks the spot
    # with a 14 px circle (owner, 2026-10-08: index size). Was 5.
    return round(x, 4)


def _commercial(tags):
    if any(k in tags for k in COMMERCIAL_KEYS):
        return True
    # A ruin is no business, whatever building it was (Seattle's Coal Creek
    # Hotel ruins, building=hotel, reviewed).
    if tags.get("building") in COMMERCIAL_BUILDINGS and not (
            tags.get("wikidata") or tags.get("wikipedia") or tags.get("heritage")
            or tags.get("historic") in ("ruins", "archaeological_site")):
        return True
    return any(tags.get(k) in vals for k, vals in COMMERCIAL_VALUES.items())


def _point(el):
    if el["type"] == "node":
        return el["lat"], el["lon"]
    c = el.get("center")
    return (c["lat"], c["lon"]) if c else None


def build(elements, *, city, retrieved, local, fold=None, dropped=(), visitable=(), rebuilt=()):
    """Return (index dict, report dict) from one place cache's elements.
    `local`: the city's local language codes (config.PLACE_LANGUAGES).
    `dropped`: OSM objects ("way/504652702") a reading by eye found to be a
    business or a home that no rule catches (config.PLACE_DROPPED).
    `visitable`: homes the public can visit today, kept against the home rule
    (config.PLACE_VISITABLE's live entries; VISITABLE FORMER HOMES above).
    `rebuilt`: names of streets closed for rebuilding, kept although OSM
    draws them highway=construction (config.PLACE_REBUILT)."""
    name_tags = _name_tags(local)
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

    report = defaultdict(int)
    not_open = []                             # stations skipped as not yet open
    rows = []
    square_rows = []                          # place=square landmark rows (the duplicate pass)
    # The extent of the city's own street nodes, a little wider: an area that
    # only touches the city comes with its center outside it (Sydney's
    # "Sydney" place area at 150.80 E, its "Inner West"; 2026-10-08).
    lats = [p[0] for p in nodes.values()]
    lons = [p[1] for p in nodes.values()]
    extent = (min(lats) - EXTENT_PAD, min(lons) - EXTENT_PAD,
              max(lats) + EXTENT_PAD, max(lons) + EXTENT_PAD) if lats else None
    seen_key = set()
    seen_near = defaultdict(list)             # (kind, name) -> (point, is_area)

    def add(kind, pt, names, langs, bbox=0, area=False):
        key = (kind, names[0], round(pt[0], 3), round(pt[1], 3))
        near = NEAR_DUP_M.get(kind)
        if key in seen_key or (near and any(
                (area or a) and _dist_m(p, pt) <= near for p, a in seen_near[(kind, names[0])])):
            report[f"{kind}_duplicate"] += 1
            return
        seen_key.add(key)
        seen_near[(kind, names[0])].append((pt, area))
        # The row's languages ride along as a 7th field until coverage is counted.
        rows.append([KINDS.index(kind), _r(pt[0]), _r(pt[1]), names[0], "|".join(names[1:]), bbox,
                     set(langs)])
        report[kind] += 1

    # --- Streets: every way of one name merged; a name used by streets far
    # apart (two 一番町) is kept apart by a coarse grid of 2 km.
    street_nodes = defaultdict(list)          # (name, cell) -> node ids
    street_names = {}                         # (name, cell) -> all names
    street_langs = defaultdict(set)           # (name, cell) -> languages
    street_open = defaultdict(bool)           # (name, cell) -> a way the public may use
    node_streets = defaultdict(set)           # node id -> street display names
    for w in ways:
        # A way a reading by eye found to be a business's or a home's own
        # road (config.PLACE_DROPPED; London's "Momento Hayes - Parking
        # Approach Road", a development's drive drawn highway=residential).
        if f"way/{w['id']}" in dropped:
            report["street_way_dropped_by_id"] += 1
            continue
        t = w.get("tags", {})
        names = _local_first(t, _names(t, name_tags), local)
        # STREETS BEING REBUILT (owner, 2026-10-11): highway=construction is
        # skipped because most such ways are roads not yet open (Hong Kong's
        # D1 to D7), and no tag tells those from a street closed for
        # rebuilding (Tbilisi's Rustaveli Avenue, all 22 of its ways). A city
        # names the second kind in config.PLACE_REBUILT, by name with why and
        # the date; a name no construction way in the cache carries stops the
        # step (build_city), so an entry retires when the street reopens.
        if t.get("highway") == "construction" and any(n in rebuilt for n in names):
            report["street_way_kept_rebuilt"] += 1
        elif (t.get("highway") in SKIP_HIGHWAY or t.get("area") == "yes"
                or t.get("service") in SKIP_SERVICE):
            report["street_way_skipped"] += 1
            continue
        if (t.get("highway") in MINOR_HIGHWAYS and not (t.get("wikidata") or t.get("wikipedia"))
                and not _reads_as_way(names, local)
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
        prev = street_names.get(cell, [])
        street_names[cell] = prev + [n for n in names if n not in prev]
        street_langs[cell] |= _langs(t, local)
        street_open[cell] |= not (minor and t.get("access") in ("private", "no")
                                  and not (t.get("wikidata") or t.get("wikipedia"))
                                  and not _private_street(names, local))
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
            merged = [ids, list(street_names[cell]), set(street_langs[cell]), street_open[cell]]
            for g in hit:
                merged[0] |= g[0]
                merged[1] += [n for n in g[1] if n not in merged[1]]
                merged[2] |= g[2]
                merged[3] |= g[3]
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
        if not groups:
            continue
        for ids, names, langs, _open in groups:
            pts = [nodes[n] for n in ids if n in nodes]
            s, w_ = min(p[0] for p in pts), min(p[1] for p in pts)
            n_, e = max(p[0] for p in pts), max(p[1] for p in pts)
            c = ((s + n_) / 2, (w_ + e) / 2)
            anchor = min(pts, key=lambda p: _dist_m(p, c))
            add("street", anchor, names, langs, [_r(s), _r(w_), _r(n_), _r(e)])
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
    for e in tagged:
        t = e.get("tags", {})
        names = _local_first(t, _names(t, name_tags), local)
        pt = _point(e)
        if not names or not pt:
            continue
        if extent and not (extent[0] <= pt[0] <= extent[2] and extent[1] <= pt[1] <= extent[3]):
            report["outside_area"] += 1
            continue
        langs = _langs(t, local)
        if (t.get("public_transport") == "station" and not t.get("railway")
                and not any(t.get(k) == "yes" for k in RAIL_MODES)
                and (any(t.get(k) not in (None, "no") for k in OTHER_MODES)
                     or any(t.get(k) in v for k, v in NOT_RAIL.items()))):
            # A bus or ferry terminal, or a tour boat's dock ("Wendella
            # Tours - Michigan Avenue", Chicago, 2026-10-08): no station.
            report["station_skipped_not_rail"] += 1
            continue
        lifecycle = next((f"{k}={t[k]}" for k in ("proposed", "construction") if t.get(k) == "yes"), None) \
            or next((f"{k}={t[k]}" for k in ("proposed:railway", "construction:railway",
                                             "proposed:public_transport", "construction:public_transport")
                     if t.get(k)), None)
        if (t.get("public_transport") == "station"
                and (t.get("railway") in ("construction", "proposed", "disused", "abandoned", "razed")
                     or lifecycle)):
            # Busan's seven light-rail stations under construction carry
            # public_transport=station already (2026-10-08): not yet a
            # station. Stations only: Prague's historic horse railway
            # (railway=abandoned) is a landmark. The lifecycle tags are read
            # too: five proposed stops of the Texcoco-La Paz light rail carry
            # railway=prpopsed, a typo no list of values holds, beside
            # proposed=yes and proposed:railway=stop (Mexico City, 2026-10-12).
            report["station_skipped_not_open"] += 1
            tag = (f"railway={t['railway']}"
                   if t.get("railway") in ("construction", "proposed", "disused", "abandoned", "razed")
                   else lifecycle)
            not_open.append({"osm": f"{e['type']}/{e['id']}", "name": names[0], "tag": tag})
            continue
        if t.get("emergency") == "designated" and (t.get("railway") or t.get("public_transport")):
            # A platform for emergency use only (Hong Kong's Light Rail
            # "Hung Tin Road Emergency Platform", 2026-10-08): no station.
            report["station_skipped_emergency"] += 1
            continue
        if t.get("railway") in ("station", "halt", "tram_stop") or t.get("public_transport") == "station":
            add("station", pt, names, langs)
        elif t.get("place") in PLACE_VALUES:
            # A place drawn as an area on residential land is an estate, its
            # homes' own name ("Kentbrook Apartments", Seattle: 85 of the
            # place areas, 2026-10-08); a place named for a business or a
            # home is one, as a landmark is. A hamlet or village is a
            # settlement whatever its land use: Hong Kong's New Territories
            # villages, 22 drawn on residential land (batch 2b, 2026-10-08);
            # no other built city had one.
            if (e["type"] != "node" and t.get("place") not in SETTLEMENTS
                    and (t.get("landuse") == "residential" or t.get("residential"))):
                report["place_dropped_estate"] += 1
                continue
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
            if t.get("place") == "hamlet" and not notable and _population(t) is not None \
                    and _population(t) < HAMLET_MIN_POPULATION:
                report["place_dropped_small_hamlet"] += 1
                continue
            if leak_word(names, local):
                report["place_dropped_leak_word"] += 1
                continue
            if bare_type(names[0], local):
                report["place_dropped_bare_type"] += 1
                continue
            names = [n for n in names if not bare_type(n, local)]
            add("place", pt, names, langs, area=e["type"] != "node")
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
            add("junction", pt, names + [a for a in alias if a not in names], langs)
        else:
            # A named square is a landmark when no street carries its name:
            # Brussels' Grand-Place is a pedestrian AREA (skipped as a street)
            # tagged place=square (batch 2a, 2026-10-08). Never one indoors or
            # underground: Kyoto's mall plazas at level -1 (ゼスト御池, コトチカ)
            # and Vancouver's "Time Out Stage", indoor=room.
            square = (t.get("place") == "square" and names[0] not in street_alias
                      and t.get("indoor") in (None, "no") and t.get("location") != "underground"
                      and not str(t.get("level", "0")).lstrip().startswith("-"))
            if t.get("place") and not square:
                continue
            if bare_type(names[0], local, t):
                report["landmark_dropped_bare_type"] += 1
                continue
            names = [n for n in names if not bare_type(n, local, t)]
            if _exhibit(t):
                report["landmark_dropped_exhibit"] += 1
                continue
            if _commercial(t):
                report["landmark_dropped_commercial"] += 1
                continue
            if (any(k in t for k in NOTABLE_ONLY) and t.get("amenity") != "place_of_worship"
                    and not (t.get("wikidata") or t.get("wikipedia"))):
                report["landmark_dropped_not_notable"] += 1
                continue
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
            oid = f"{e['type']}/{e['id']}"
            if _home(t, names, local) and not _public_home(t) and oid not in visitable:
                report["landmark_dropped_residential"] += 1
                continue
            # A landmark named as a bare Japanese personal name (the map's sign
            # rule, japan_register.bare_personal_name: a common surname, a space,
            # a given name) is someone's house or grave, unless public. The
            # Korean rule (korean_names.looks_like_personal_name) is NOT used:
            # without its address test it reads 이태원 and 강남역 as people.
            if "ja" in local and not _public_home(t) and oid not in visitable and any(_bare_personal(n) for n in names):
                report["landmark_dropped_personal_name"] += 1
                continue
            # A garden is often a private one at a house, and may carry a
            # person's own name ("Aoyama's Garden", Kyoto, 2026-10-07): kept only
            # when notable (wikidata, wikipedia or a heritage designation), and
            # a residential garden never.
            if t.get("leisure") == "garden" and (
                    t.get("garden:type") == "residential"
                    or not (t.get("wikidata") or t.get("wikipedia") or t.get("heritage"))):
                report["landmark_dropped_garden"] += 1
                continue
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
            word = leak_word(names, local)
            home_word = word in {w for c in (["en", *local]) for w in HOME_WORDS.get(c, ())}
            if word and not (
                    _public_home(t) or oid in visitable or t.get("historic") in ("ruins", "archaeological_site")
                    or (t.get("wikipedia") and not home_word)):
                report["landmark_dropped_leak_word"] += 1
                continue
            if t.get("waterway"):
                # A river comes as one row per way; merged by name below.
                rivers[names[0]].append((pt, names, langs))
                continue
            # A Stolperstein names one person at their last home ("Zde bydlela
            # Irma Kohnová", here lived ...): a private person at a home, never
            # a place to search, whatever its wikidata item (Prague's came in
            # bulk from the small-monuments register; batch 2a, 2026-10-08).
            if t.get("memorial") == "stolperstein":
                report["landmark_dropped_stolperstein"] += 1
                continue
            if t.get("historic") == "tomb" and any(FAMILY_TOMB.match(n.strip()) for n in names):
                report["landmark_dropped_family_tomb"] += 1
                continue
            if t.get("historic") in SKIP_HISTORIC and not any(
                    t.get(k) for k in ("tourism", "amenity", "leisure", "wikidata")):
                report["landmark_dropped_minor_historic"] += 1
                continue
            before = len(rows)
            add("landmark", pt, names, langs, area=e["type"] != "node")
            if t.get("place") == "square" and len(rows) > before:
                square_rows.append(rows[-1])

    for segs in rivers.values():
        pts = [p for p, _, _ in segs]
        s, w_ = min(p[0] for p in pts), min(p[1] for p in pts)
        n_, e = max(p[0] for p in pts), max(p[1] for p in pts)
        c = ((s + n_) / 2, (w_ + e) / 2)
        names = []
        for _, ns, _ in segs:
            names += [x for x in ns if x not in names]
        add("landmark", min(pts, key=lambda p: _dist_m(p, c)), names,
            set().union(*(ls for _, _, ls in segs)),
            [_r(s), _r(w_), _r(n_), _r(e)] if len(pts) > 1 else 0)

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
    for sq in square_rows:
        words = _square_keys([sq[3]] + (sq[4].split("|") if sq[4] else []))
        keys = {"".join(w) for w in words}
        for o in rows:
            if o is sq or id(o) in drop or not (o[0] == street_kind or id(o) in square_ids):
                continue
            d = _dist_m((sq[1], sq[2]), (o[1], o[2]))
            if d > SQUARE_DUP_M:
                continue
            owords = _square_keys([o[3]] + (o[4].split("|") if o[4] else []))
            # Spelt almost alike only under the same first word: Placeta del Pi
            # and Plaça del Pi are two squares.
            if keys & {"".join(w) for w in owords} or (d <= SQUARE_NEAR_M and any(
                    a[0] == b[0] and difflib.SequenceMatcher(None, "".join(a), "".join(b)).ratio() >= 0.9
                    for a in words for b in owords)):
                drop.add(id(sq))
                break
    if drop:
        rows[:] = [r for r in rows if id(r) not in drop]
        report["landmark"] -= len(drop)
        report["square_dropped_duplicate"] += len(drop)
    rows.sort(key=lambda r: (r[0], r[3]))
    row_langs = [r.pop() for r in rows]
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
        "languages": languages(row_langs, local),
        "fold": fold,
        "kinds": list(KINDS),
        "rows": rows,
        # write() puts these in crossings_path() and their site path here.
        "crossing_rows": crossing_rows,
        # write() puts these in the page's summary, never in the served file.
        "stations_not_open": sorted(not_open, key=lambda r: r["osm"]),
    }
    return index, dict(report)
