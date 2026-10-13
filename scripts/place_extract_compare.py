"""Compare a city's Overpass place caches with caches built from an extract
(pipeline/place_extract_fetch.py <city> --out DIR): the proof that the
extract route answers what Overpass answers. A report; it writes nothing in
the repository and fails nothing.

    python scripts/place_extract_compare.py <city> DIR [--show N]

ELEMENTS, by OSM id, in four groups (street ways, their nodes, the main
query's tagged elements, the extra query's): present in one side only, tags
differing, node lists differing, positions differing exactly and by more
than 1.5e-7 degrees (the last decimal Overpass prints).

THE INDEX, in two steps, because the index step's tie-breaks depend on the
order of its input and the extract route does not reproduce Overpass's qt
order:

  A. the Overpass caches as fetched against the SAME caches re-ordered the
     way the extract route orders (street ways, their nodes, then nodes, ways
     and relations, each by id). Same elements, so every row that differs
     here differs by TIE-BREAK alone.
  B. those re-ordered Overpass caches against the extract's. Same order, so
     every row that differs here comes from an ELEMENT that differs, each of
     which the first section lists.

Rows are compared as a multiset of (kind, name, OSM id, the rest), aliases
sorted. Every difference needs a cause before a query is trusted to the
extract route: an edit dated between the two data dates, or "unknown".
"""
import argparse
import importlib
import json
import sys
import tempfile
import types
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import place_index as pi  # noqa: E402

RANK = {"node": 0, "way": 1, "relation": 2}


def load(path):
    return json.loads(Path(path).read_bytes().decode("utf-8"))


def split(els):
    """(street ways, their nodes, tagged elements), each {(type, id): element}."""
    ways, skel, tagged = {}, {}, {}
    for e in els:
        key = (e["type"], e["id"])
        if "nodes" in e:
            ways[key] = e
        elif e["type"] == "node" and "tags" not in e:
            skel[key] = e
        else:
            tagged[key] = e
    return ways, skel, tagged


def pos(e):
    c = e.get("center") or e
    return (c.get("lat"), c.get("lon"))


def diff(label, a, b, show):
    only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    both = sorted(set(a) & set(b))
    tag_diff = [k for k in both if (a[k].get("tags") or {}) != (b[k].get("tags") or {})]
    node_diff = [k for k in both if "nodes" in a[k] and a[k]["nodes"] != b[k].get("nodes")]
    inexact, moved = [], []
    for k in both:
        pa, pb = pos(a[k]), pos(b[k])
        if pa[0] is None or pb[0] is None or pa == pb:
            continue
        d = max(abs(pa[0] - pb[0]), abs(pa[1] - pb[1]))
        (moved if d > 1.5e-7 else inexact).append((d, k))
    print(f"{label}: overpass {len(a):,}, extract {len(b):,}, in both {len(both):,}; only overpass "
          f"{len(only_a)}, only extract {len(only_b)}; tags differ {len(tag_diff)}; node list differs "
          f"{len(node_diff)}; position differs by more than 1.5e-7 deg {len(moved)}, by the last "
          f"decimal {len(inexact)}")

    def name(k, src):
        return f"{k[0]}/{k[1]} {(src[k].get('tags') or {}).get('name', '')!r}"

    for title, keys, src in (("only overpass", only_a, a), ("only extract", only_b, b),
                             ("tags differ", tag_diff, a), ("node list differs", node_diff, a)):
        if keys:
            print(f"   {title}: " + "; ".join(name(k, src) for k in keys[:show]))
    for k in tag_diff[:show]:
        ta, tb = a[k].get("tags") or {}, b[k].get("tags") or {}
        changed = {key: (ta.get(key), tb.get(key)) for key in sorted(set(ta) | set(tb)) if ta.get(key) != tb.get(key)}
        print(f"      {k[0]}/{k[1]}: {changed}")
    for title, rows in (("moved", moved), ("last decimal", inexact)):
        if rows:
            rows.sort(reverse=True)
            print(f"   {title}: " + "; ".join(f"{name(k, a)} {pos(a[k])} vs {pos(b[k])}" for _, k in rows[:show]))
    return {"only_overpass": len(only_a), "only_extract": len(only_b), "tags": len(tag_diff),
            "nodes": len(node_diff), "moved": len(moved), "last_decimal": len(inexact)}


def reorder(payload):
    """An Overpass cache's elements in the extract route's order."""
    ways, skel, tagged = [], [], []
    for e in payload["elements"]:
        (ways if "nodes" in e else skel if e["type"] == "node" and "tags" not in e else tagged).append(e)
    ways.sort(key=lambda e: e["id"])
    skel.sort(key=lambda e: e["id"])
    tagged.sort(key=lambda e: (RANK[e["type"]], e["id"]))
    return {**payload, "elements": ways + skel + tagged}


def shim(config, folder):
    """The city's config with its two place caches read from `folder`."""
    s = types.SimpleNamespace(**{k: getattr(config, k) for k in dir(config) if not k.startswith("__")})
    s.PLACE_OSM_JSON = Path(folder) / Path(config.PLACE_OSM_JSON).name
    s.PLACE_OSM_EXTRA_JSON = Path(folder) / Path(config.PLACE_OSM_EXTRA_JSON).name
    s.__name__ = config.__name__
    return s


def rows_of(index):
    out = Counter()
    for i, r in enumerate(index["rows"]):
        norm = [("|".join(sorted(v.split("|"))) if j == 4 and isinstance(v, str) else v) for j, v in enumerate(r)]
        out[json.dumps([pi.KINDS[r[0]], r[3], index["row_osm"][i] or None, norm], ensure_ascii=False)] += 1
    return out


def row_diff(label, a, b, show):
    only_a, only_b = a - b, b - a
    same = sum((a & b).values())
    kinds = Counter(json.loads(k)[0] for k in list(only_a.elements()) + list(only_b.elements()))
    print(f"{label}: {sum(a.values()):,} rows against {sum(b.values()):,}; identical {same:,}; only in the "
          f"first {sum(only_a.values())}, only in the second {sum(only_b.values())}; by kind {dict(kinds)}")
    for title, rows in (("first", only_a), ("second", only_b)):
        for k in sorted(rows)[:show]:
            kind, name, osm_id, row = json.loads(k)
            print(f"   only {title}: {kind} {name!r} {osm_id or ''} {str(row[1:3])} {str(row[4:])[:120]}")
    return sum(only_a.values()), sum(only_b.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("city")
    ap.add_argument("extract_dir")
    ap.add_argument("--show", type=int, default=8)
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")
    ex = Path(args.extract_dir)
    o_main, o_extra = load(config.PLACE_OSM_JSON), load(config.PLACE_OSM_EXTRA_JSON)
    e_main, e_extra = load(ex / Path(config.PLACE_OSM_JSON).name), load(ex / Path(config.PLACE_OSM_EXTRA_JSON).name)
    print(f"== {args.city}: data dates")
    for label, p in (("overpass main", o_main), ("overpass extra", o_extra), ("extract", e_main)):
        base = p.get("osm3s", {})
        print(f"   {label}: {base.get('timestamp_osm_base')}"
              + (f" (areas {base['timestamp_areas_base']})" if "timestamp_areas_base" in base else "")
              + f", {p.get('_fetched_from')}")
    print("== elements")
    ow, osk, ot = split(o_main["elements"])
    ew, esk, et = split(e_main["elements"])
    diff("street ways", ow, ew, args.show)
    diff("street nodes", osk, esk, args.show)
    diff("main tagged", ot, et, args.show)
    diff("extra tagged", split(o_extra["elements"])[2], split(e_extra["elements"])[2], args.show)
    outline = ex / pi.OUTLINE_CACHE_NAME
    if outline.exists() and pi.outline_cache(config).exists():
        mo = {m[0]: m[2] for m in pi.municipalities(load(pi.outline_cache(config))["elements"])}
        me = {m[0]: m[2] for m in pi.municipalities(load(outline)["elements"])}
        same = sum(1 for k in mo if k in me and mo[k].equals(me[k]))
        print(f"outline: overpass {len(mo)} boundaries (data {load(pi.outline_cache(config)).get('osm3s', {}).get('timestamp_osm_base')}),"
              f" extract {len(me)}; same ids {sorted(mo) == sorted(me)}; same outer shape {same}")
    print("== indexes")
    index_o, _ = pi.build_city(config)
    with tempfile.TemporaryDirectory() as d:
        for name, payload in ((Path(config.PLACE_OSM_JSON).name, o_main),
                              (Path(config.PLACE_OSM_EXTRA_JSON).name, o_extra)):
            (Path(d) / name).write_bytes(json.dumps(reorder(payload), ensure_ascii=False).encode("utf-8"))
        # The index step reads the outline beside the place cache.
        (Path(d) / pi.OUTLINE_CACHE_NAME).write_bytes(pi.outline_cache(config).read_bytes())
        index_s, _ = pi.build_city(shim(config, d))
    index_e, _ = pi.build_city(shim(config, ex))
    ro, rs, re_ = rows_of(index_o), rows_of(index_s), rows_of(index_e)
    row_diff("A. tie-break (Overpass as fetched against Overpass re-ordered)", ro, rs, args.show)
    row_diff("B. elements (Overpass re-ordered against the extract)", rs, re_, args.show)
    row_diff("C. the two indexes as built (A and B together)", ro, re_, 0)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
