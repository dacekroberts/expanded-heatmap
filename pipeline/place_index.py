"""Build a city's place-search index from its cached OpenStreetMap places.

Shared by every city's `step4_place_index.py`. Reads the cache that
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
import json
import math
from collections import defaultdict

KINDS = ("station", "junction", "landmark", "place", "street", "crossing")

# Name tags read, in order: the first is the display name, the rest are
# searchable aliases. Kana readings let a Japanese reader type in kana.
NAME_TAGS = ("name", "name:en", "name:ja", "name:ja-Latn", "name:ja_rm", "name:ja-Hira",
             "name:ja_kana", "alt_name", "alt_name:en", "official_name", "official_name:en",
             "short_name", "short_name:en", "old_name:en")

# Highways that are not streets a reader would search for: platforms, indoor
# corridors and the like.
SKIP_HIGHWAY = {"platform", "elevator", "corridor", "bus_stop", "proposed", "construction",
                "razed", "abandoned", "disused"}
# Any landmark with one of these is (also) a business, and stays out.
COMMERCIAL_KEYS = ("shop", "office", "craft", "brand", "cuisine", "operator:type")
COMMERCIAL_VALUES = {
    "amenity": {"restaurant", "cafe", "bar", "pub", "fast_food", "bank", "pharmacy",
                "fuel", "parking", "car_rental", "marketplace", "food_court"},
    "tourism": {"hotel", "guest_house", "hostel", "motel", "apartment", "chalet"},
}
# historic=* values that are clutter at a search box (wayside shrines and
# stones number in the hundreds and are named after their saint or deity).
SKIP_HISTORIC = {"wayside_shrine", "wayside_cross", "boundary_stone", "milestone",
                 "memorial", "tomb", "yes"}
# Tourism and education landmarks need a wikidata or wikipedia tag: without
# one, OSM's tourism=attraction and amenity=college in Kyoto included a
# tea-ceremony shop and a private computer school (2026-10-07), businesses by
# another name. Places of worship, parks, gardens, peaks, rivers and historic
# sites need none.
NOTABLE_ONLY = ("tourism", "amenity")
# Never place=isolated_dwelling or farm: a single home (Kyoto's one was an
# apartment building, 2026-10-07).
PLACE_VALUES = {"city", "borough", "suburb", "quarter", "neighbourhood", "village",
                "hamlet", "town", "locality"}
# A street-pair crossing seen at several nodes counts as one place unless its
# nodes lie further apart than this (a long pair of streets crossing twice).
CROSSING_MERGE_M = 250


def _names(tags):
    seen, out = set(), []
    for k in NAME_TAGS:
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


def build(elements, *, city, retrieved, fold=None):
    """Return (index dict, report dict) from one place cache's elements."""
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

    def add(kind, pt, names, bbox=0):
        key = (kind, names[0], round(pt[0], 3), round(pt[1], 3))
        if key in seen_key:
            report[f"{kind}_duplicate"] += 1
            return
        seen_key.add(key)
        rows.append([KINDS.index(kind), _r(pt[0]), _r(pt[1]), names[0], "|".join(names[1:]), bbox])
        report[kind] += 1

    # --- Streets: every way of one name merged; a name used by streets far
    # apart (two 一番町) is kept apart by a coarse grid of 2 km.
    street_nodes = defaultdict(list)          # (name, cell) -> node ids
    street_names = {}                         # (name, cell) -> all names
    node_streets = defaultdict(set)           # node id -> street display names
    for w in ways:
        t = w.get("tags", {})
        if t.get("highway") in SKIP_HIGHWAY or t.get("area") == "yes":
            report["street_way_skipped"] += 1
            continue
        names = _names(t)
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
        for n in w["nodes"]:
            node_streets[n].add(names[0])
    # Neighbouring cells of one name are one street: merge cells that share a node.
    by_name = defaultdict(list)
    for cell in street_nodes:
        by_name[cell[0]].append(cell)
    street_alias = {}                         # display name -> its English-ish aliases
    for name, cells in by_name.items():
        groups = []
        for cell in cells:
            ids = set(street_nodes[cell])
            hit = [g for g in groups if g[0] & ids]
            merged = [ids, list(street_names[cell])]
            for g in hit:
                merged[0] |= g[0]
                merged[1] += [n for n in g[1] if n not in merged[1]]
                groups.remove(g)
            groups.append(merged)
        for ids, names in groups:
            pts = [nodes[n] for n in ids if n in nodes]
            s, w_ = min(p[0] for p in pts), min(p[1] for p in pts)
            n_, e = max(p[0] for p in pts), max(p[1] for p in pts)
            c = ((s + n_) / 2, (w_ + e) / 2)
            anchor = min(pts, key=lambda p: _dist_m(p, c))
            add("street", anchor, names, [_r(s), _r(w_), _r(n_), _r(e)])
        street_alias[name] = [n for g in groups for n in g[1]]

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
            add("crossing", cl[0], [f"{a} / {b}"] + alias)

    # --- Tagged places.
    rivers = defaultdict(list)
    for e in tagged:
        t = e.get("tags", {})
        names = _names(t)
        pt = _point(e)
        if not names or not pt:
            continue
        if t.get("railway") in ("station", "halt", "tram_stop") or t.get("public_transport") == "station":
            add("station", pt, names)
        elif t.get("place") in PLACE_VALUES:
            add("place", pt, names)
        elif e["type"] == "node" and (t.get("highway") == "traffic_signals" or "junction" in t):
            # A signed junction (四条烏丸): the streets through it as aliases.
            via = sorted(node_streets.get(e["id"], ()))
            alias = []
            if len(via) >= 2:
                alias.append(" / ".join(via))
                en = [next((x for x in street_alias.get(v, []) if x != v), None) for v in via]
                if all(en):
                    alias.append(" / ".join(en))
            add("junction", pt, names + [a for a in alias if a not in names])
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
                rivers[names[0]].append((pt, names))
                continue
            if t.get("historic") in SKIP_HISTORIC and not any(
                    t.get(k) for k in ("tourism", "amenity", "leisure", "wikidata")):
                report["landmark_dropped_minor_historic"] += 1
                continue
            add("landmark", pt, names)

    for segs in rivers.values():
        pts = [p for p, _ in segs]
        s, w_ = min(p[0] for p in pts), min(p[1] for p in pts)
        n_, e = max(p[0] for p in pts), max(p[1] for p in pts)
        c = ((s + n_) / 2, (w_ + e) / 2)
        names = []
        for _, ns in segs:
            names += [x for x in ns if x not in names]
        add("landmark", min(pts, key=lambda p: _dist_m(p, c)), names,
            [_r(s), _r(w_), _r(n_), _r(e)] if len(pts) > 1 else 0)

    rows.sort(key=lambda r: (r[0], r[3]))
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
        "fold": fold,
        "kinds": list(KINDS),
        "rows": rows,
    }
    return index, dict(report)
