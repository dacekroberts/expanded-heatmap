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
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path

STATIC_DIR = Path(__file__).parent.parent / "app" / "static" / "places"


def index_path(slug):
    return STATIC_DIR / f"{slug}.json"


def summary_path(slug):
    return Path(__file__).parent.parent / "outputs" / slug / "place_search.json"


def write(index, slug):
    """Write the index (served as-is: bytes, LF only, no BOM) and the page's
    summary, outputs/<slug>/place_search.json: the languages the page names,
    the count and the retrieval date. The app reads the summary, never the
    index, so a page load costs no megabyte."""
    out = index_path(slug)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(json.dumps(index, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    summary = {"index": f"app/static/places/{slug}.json", "places": len(index["rows"]),
               "data_retrieved": index["license"]["data_retrieved"], "languages": index["languages"]}
    summary_path(slug).write_bytes(
        (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
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
    for code in local:
        script = SCRIPTS.get(code)
        if tags.get(f"name:{code}") or (name and (script is None or script.search(name))):
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
# corridors and the like.
SKIP_HIGHWAY = {"platform", "elevator", "corridor", "bus_stop", "proposed", "construction",
                "razed", "abandoned", "disused"}
# Any landmark with one of these is (also) a business, and stays out.
COMMERCIAL_KEYS = ("shop", "office", "craft", "brand", "cuisine")
# operator:type by value: Nishiki Market is run by its shopkeepers' cooperative
# (operator:type=cooperative) and is a place; a private operator is a business.
COMMERCIAL_VALUES = {
    "operator:type": {"private", "business", "commercial"},
    "amenity": {"restaurant", "cafe", "bar", "pub", "fast_food", "bank", "pharmacy",
                "fuel", "parking", "car_rental", "food_court"},
    "tourism": {"hotel", "guest_house", "hostel", "motel", "apartment", "chalet"},
}
# historic=* values that are clutter at a search box (wayside shrines and
# stones number in the hundreds and are named after their saint or deity).
SKIP_HISTORIC = {"wayside_shrine", "wayside_cross", "boundary_stone", "milestone",
                 "memorial", "tomb", "yes"}
# Tourism and education landmarks need a wikidata or wikipedia tag: without
# one, OSM's tourism=attraction and amenity=college in Kyoto included a
# tea-ceremony shop and a private computer school (2026-10-07), businesses by
# another name. Named markets likewise (amenity=marketplace; owner,
# 2026-10-07: notable only), since an OSM marketplace can be one company's
# market hall. Places of worship, parks, gardens, peaks, rivers and historic
# sites need none.
NOTABLE_ONLY = ("tourism", "amenity")
RESIDENTIAL_BUILDINGS = {"house", "residential", "apartments", "detached", "dormitory",
                         "semidetached_house", "terrace", "bungalow"}
# Never place=isolated_dwelling or farm: a single home (Kyoto's one was an
# apartment building, 2026-10-07).
PLACE_VALUES = {"city", "borough", "suburb", "quarter", "neighbourhood", "village",
                "hamlet", "town", "locality"}
# A street-pair crossing seen at several nodes counts as one place unless its
# nodes lie further apart than this (a long pair of streets crossing twice).
CROSSING_MERGE_M = 250


def _names(tags, name_tags):
    seen, out = set(), []
    for k in name_tags:
        for v in (tags.get(k) or "").split(";"):
            v = v.strip()
            if v and v not in seen:
                seen.add(v)
                out.append(v)
    return out


def _dist_m(a, b):
    lat = math.radians((a[0] + b[0]) / 2)
    return math.hypot((a[0] - b[0]) * 110540.0, (a[1] - b[1]) * 111320.0 * math.cos(lat))


def _r(x):
    return round(x, 5)


def _commercial(tags):
    if any(k in tags for k in COMMERCIAL_KEYS):
        return True
    return any(tags.get(k) in vals for k, vals in COMMERCIAL_VALUES.items())


def _point(el):
    if el["type"] == "node":
        return el["lat"], el["lon"]
    c = el.get("center")
    return (c["lat"], c["lon"]) if c else None


def build(elements, *, city, retrieved, local, fold=None):
    """Return (index dict, report dict) from one place cache's elements.
    `local`: the city's local language codes (config.PLACE_LANGUAGES)."""
    name_tags = _name_tags(local)
    nodes = {}
    ways = []
    tagged = []
    for e in elements:
        if e["type"] == "node" and "tags" not in e:
            nodes[e["id"]] = (e["lat"], e["lon"])
        elif e["type"] == "way" and "nodes" in e:
            ways.append(e)
        else:
            tagged.append(e)
            if e["type"] == "node":
                nodes.setdefault(e["id"], (e["lat"], e["lon"]))

    report = defaultdict(int)
    rows = []
    seen_key = set()

    def add(kind, pt, names, langs, bbox=0):
        key = (kind, names[0], round(pt[0], 3), round(pt[1], 3))
        if key in seen_key:
            report[f"{kind}_duplicate"] += 1
            return
        seen_key.add(key)
        # The row's languages ride along as a 7th field until coverage is counted.
        rows.append([KINDS.index(kind), _r(pt[0]), _r(pt[1]), names[0], "|".join(names[1:]), bbox,
                     set(langs)])
        report[kind] += 1

    # --- Streets: every way of one name merged; a name used by streets far
    # apart (two 一番町) is kept apart by a coarse grid of 2 km.
    street_nodes = defaultdict(list)          # (name, cell) -> node ids
    street_names = {}                         # (name, cell) -> all names
    street_langs = defaultdict(set)           # (name, cell) -> languages
    node_streets = defaultdict(set)           # node id -> street display names
    for w in ways:
        t = w.get("tags", {})
        if t.get("highway") in SKIP_HIGHWAY or t.get("area") == "yes":
            report["street_way_skipped"] += 1
            continue
        names = _names(t, name_tags)
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
            merged = [ids, list(street_names[cell]), set(street_langs[cell])]
            for g in hit:
                merged[0] |= g[0]
                merged[1] += [n for n in g[1] if n not in merged[1]]
                merged[2] |= g[2]
                groups.remove(g)
            groups.append(merged)
        for ids, names, langs in groups:
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
            en_a = [x for x in street_alias.get(a, []) if x != a]
            en_b = [x for x in street_alias.get(b, []) if x != b]
            alias = [f"{x} / {y}" for x, y in zip(en_a[:1], en_b[:1])]
            # In a language only where both streets are.
            add("crossing", cl[0], [f"{a} / {b}"] + alias,
                street_lang.get(a, set()) & street_lang.get(b, set()))

    # --- Tagged places.
    rivers = defaultdict(list)
    for e in tagged:
        t = e.get("tags", {})
        names = _names(t, name_tags)
        pt = _point(e)
        if not names or not pt:
            continue
        langs = _langs(t, local)
        if t.get("railway") in ("station", "halt", "tram_stop") or t.get("public_transport") == "station":
            add("station", pt, names, langs)
        elif t.get("place") in PLACE_VALUES:
            add("place", pt, names, langs)
        elif e["type"] == "node" and (t.get("highway") == "traffic_signals" or "junction" in t):
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
            if t.get("place"):
                continue
            if _commercial(t):
                report["landmark_dropped_commercial"] += 1
                continue
            if (any(k in t for k in NOTABLE_ONLY) and t.get("amenity") != "place_of_worship"
                    and not (t.get("wikidata") or t.get("wikipedia"))):
                report["landmark_dropped_not_notable"] += 1
                continue
            # A home is never a landmark: residential land, a house or an
            # apartment building, or private access, unless notable (a former
            # residence that is now a museum). Kyoto's condominium grounds were
            # tagged leisure=park on landuse=residential (2026-10-07).
            if ((t.get("landuse") == "residential" or t.get("building") in RESIDENTIAL_BUILDINGS
                    or t.get("access") == "private")
                    and not (t.get("wikidata") or t.get("wikipedia") or t.get("heritage"))):
                report["landmark_dropped_residential"] += 1
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
            if t.get("waterway"):
                # A river comes as one row per way; merged by name below.
                rivers[names[0]].append((pt, names, langs))
                continue
            if t.get("historic") in SKIP_HISTORIC and not any(
                    t.get(k) for k in ("tourism", "amenity", "leisure", "wikidata")):
                report["landmark_dropped_minor_historic"] += 1
                continue
            add("landmark", pt, names, langs)

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

    rows.sort(key=lambda r: (r[0], r[3]))
    row_langs = [r.pop() for r in rows]
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
        "city": city,
        "languages": languages(row_langs, local),
        "fold": fold,
        "kinds": list(KINDS),
        "rows": rows,
    }
    return index, dict(report)
