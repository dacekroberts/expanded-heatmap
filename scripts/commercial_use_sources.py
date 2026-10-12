"""Decide how many distinct sources the commercial-use audit must read, by
grouping every city's provenance entries into sources, and print one line per
source with its id, publisher host, cities and layers.

    python scripts/commercial_use_sources.py [--json OUT] [--city SLUG]
    python scripts/commercial_use_sources.py --selftest

Each built city records what it fetched in outputs/<slug>/provenance.json.
That file is a record of files, URLs and bookkeeping, not a source list, and
its shape differs by country. This script walks every file and decides, per
top-level key, whether it is (a) a source entry, (b) bookkeeping that is not
a source (a date, a bounding box, a file-time map, feed metadata), or (c)
something it cannot classify. Kind (c) is printed with its city and key, never
dropped. Source entries are grouped into sources by the publisher's host plus
the dataset page when an entry records one (a `dataset_page`, `page_url`,
`page` or `portal` key), and by the data URL's host plus its first path
segment when it does not. OpenStreetMap entries (an osm_* key, an Overpass
host, a query or an osm_base) are always one source, OpenStreetMap, whatever
mirror host served them.

WHY THAT KEY. Commercial terms attach to the dataset, not to the file. Kobe's
four hygiene files share one dataset page and are one source; its isj and n02
files record no dataset page and are told apart by the first path segment of
their URLs (isj, ksj). Two datasets on one portal stay two sources only
because the dataset page, not the host, is part of the key. The id is the key
made of lower-case ASCII letters, digits and hyphens, so it is stable across
runs and city order; these ids are the `source` values that
scripts/commercial_use_quote_check.py reads in its verdicts file. Two
different sources that would share one id fail the run and name both.

WHAT THE COUNT IS NOT. One source here is one dataset page, so a portal that
publishes thirty datasets under one licence is thirty sources: the run also
counts hosts and lists each host with more than one source, and a person
decides which share a licence. A city whose only recorded source is
OpenStreetMap is listed, since its register is missing from its provenance
file or recorded in a shape set aside here. Every object set aside as
bookkeeping is listed with its cities, and every licence key that sits
outside a source entry is listed with its value, attached to no source.

WHAT IT CANNOT TELL. An entry that records no URL at all is listed as
unclassified, never guessed at: the Czech cities after Prague read their
national files from a shared cache and write url "" for them. A `licence`
field is read where an entry has one and printed beside the source, but the
script decides nothing about licences. Layers come from an entry's `layer`
field where it has one, else from the entry key; they are never translated
into a role. Some cities' provenance omits sources the map still uses, and
some cities have no provenance file at all; those are named, and the run
exits non-zero for them, a finding rather than a pass.
"""
import argparse
import ast
import io
import json
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from check_provenance import SLUG_OVERRIDES  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OSM_SID = "openstreetmap"
OSM_HOST = "openstreetmap.org"
DATASET_PAGE_KEYS = ("dataset_page", "page_url", "page", "portal")
LICENCE_KEYS = ("licence", "license")
ISO_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _is_http(value):
    return isinstance(value, str) and (
        value.startswith("http://") or value.startswith("https://"))


def _slugify(text):
    """Lower case, keep ASCII letters and digits, one hyphen per other run."""
    out, gap = [], False
    for ch in str(text).lower():
        if ("a" <= ch <= "z") or ("0" <= ch <= "9"):
            out.append(ch)
            gap = False
        elif not gap:
            out.append("-")
            gap = True
    while out and out[-1] == "-":
        out.pop()
    return "".join(out)


def _url_host(url):
    """The publisher's host: lower case, no leading www., and with its port
    when the URL names one (two services on one machine are two hosts)."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    try:
        port = parts.port
    except ValueError:
        port = None
    return f"{host}:{port}" if port else host


def _url_path(url):
    return (urlsplit(url).path or "").strip("/")


def _page_key(url):
    """A dataset page's path with its query string: portals that serve every
    dataset from one address tell them apart only there (Daegu's dataView.do,
    Kumamoto's detail.aspx), so the query is part of what the page is."""
    parts = urlsplit(url)
    path = (parts.path or "").strip("/")
    return f"{path}?{parts.query}" if parts.query else path


def _url_folder(url):
    """A data URL's folder: its path without the file name. A last part with
    no dot in it is an endpoint, not a file, and stays (v1/bag/straten)."""
    path = (urlsplit(url).path or "").strip("/")
    head, _, last = path.rpartition("/")
    return head if "." in last else path


def _is_osm_host(host):
    """True for OpenStreetMap's own hosts and any Overpass mirror."""
    return "openstreetmap" in host or "overpass" in host


def _first_segment(url):
    parts = [p for p in urlsplit(url).path.split("/") if p]
    return parts[0] if parts else ""


def _source_id(host, path):
    parts = [p for p in (_slugify(host), _slugify(path)) if p]
    return "-".join(parts) or "source"


def _is_osm_key(key):
    """True for osm and osm_*, read on the last part of a nested key
    (sources.osm_places is an osm_ key)."""
    last = key.rsplit(".", 1)[-1]
    return last == "osm" or last.startswith("osm_")


def _names_another_publisher(value):
    """True when a dict holds an http URL on a host that is not OpenStreetMap
    or an Overpass mirror: under an osm_ key that is another publisher's
    data (a tile provider, a boundary service), not OpenStreetMap's."""
    return any(_is_http(v) and not _is_osm_host(_url_host(v))
               for v in value.values())


def _osm_bookkeeping(key, value):
    """True when an osm_* value is a timestamp, a number or a numeric list:
    bookkeeping about the OpenStreetMap source, not a marker of it."""
    if isinstance(value, (int, float, bool)) or value is None:
        return True
    if isinstance(value, str):
        return bool(ISO_TS_RE.match(value.strip()))
    if isinstance(value, list):
        return not (bool(value) and all(isinstance(x, str) for x in value))
    return False


def _entry_urls(entry):
    """(dataset page, data URL, licence) read from one source entry object."""
    page = next((entry[k] for k in DATASET_PAGE_KEYS if _is_http(entry.get(k))), "")
    licence = next((entry[k] for k in LICENCE_KEYS
                    if isinstance(entry.get(k), str) and entry[k]), "")
    data = next((entry[k] for k in ("url", "endpoint", "source", "wfs", "feed")
                 if _is_http(entry.get(k))), "")
    if not data:
        data = next((v for k, v in entry.items()
                     if _is_http(v) and k not in DATASET_PAGE_KEYS
                     and "licen" not in k), "")
    return page, data, licence


def _entry_layers(entry, key):
    """Layer names an entry shows: a non-URL `layer` field (also inside a
    `files` list), else the entry's key. Never translated into a role."""
    layers = set()
    layer = entry.get("layer")
    if isinstance(layer, str) and layer and not _is_http(layer):
        layers.add(layer)
    for f in entry.get("files") or []:
        if isinstance(f, dict):
            sub = f.get("layer")
            if isinstance(sub, str) and sub and not _is_http(sub):
                layers.add(sub)
    if not layers and key:
        layers.add(key)
    return sorted(layers)


def _is_source_like(value):
    """True when a dict reads as a source entry: it carries an http URL, a
    URL-bearing or dataset-page key, or the file plus sha256 signature. A
    derived artifact (made_from or tool) is not a source."""
    if not isinstance(value, dict):
        return False
    if any(_is_http(v) for v in value.values()):
        return True
    if "made_from" in value or "tool" in value:
        return False
    if "url" in value or "dataset_page" in value or "page" in value \
            or "page_url" in value or "portal" in value:
        return True
    if "file" in value and "sha256" in value:
        return True
    return False


def _register_source(sid, host, dataset_page, city, layers, licence, identity,
                     state, coarse=None, short=None):
    if sid not in state["identity_of"]:
        state["identity_of"][sid] = identity
        state["sources"][sid] = {
            "id": sid, "host": host, "dataset_page": dataset_page,
            "cities": set(), "layers": set(), "licences": set(),
            "coarse": coarse, "short": short}
    elif state["identity_of"][sid] != identity:
        state["collisions"].add(
            f"id '{sid}' would name two sources: "
            f"'{state['identity_of'][sid]}' and '{identity}'")
        return
    src = state["sources"][sid]
    src["cities"].add(city)
    src["layers"].update(layers)
    if licence:
        src["licences"].add(licence)


def _register_url(name, key, page, data_url, layers, licence, state):
    """Register one entry by its dataset page, else by its data URL. A URL on
    an OpenStreetMap or Overpass host is OpenStreetMap under whatever key.

    A dataset page is keyed with its query string; collect() drops the query
    from the id again where no other page shares the path, so only the
    portals that need it carry it. An entry with no dataset page is keyed on
    its host and FULL folder, since ten datasets can sit under one first
    path part (data.gov.lv); the host and first path part are kept as the
    coarser view, printed for the reader asking whether one licence covers a
    portal."""
    if page:
        host, path = _url_host(page), _page_key(page)
        coarse, short = None, (host, _url_path(page))
    else:
        host, path = _url_host(data_url), _url_folder(data_url)
        coarse, short = f"{host}/{_first_segment(data_url)}", None
    if _is_osm_host(host):
        _register_source(OSM_SID, OSM_HOST, "", name, {key}, "", OSM_SID, state)
        return
    _register_source(_source_id(host, path), host, page, name, layers, licence,
                     f"{host}/{path}", state, coarse=coarse, short=short)


def _shorten_ids(state):
    """Drop the query string from a dataset page's id where no other page
    shares its host and path, and no other source holds the shorter id. Done
    after every file is read, so the result does not depend on their order."""
    by_path = {}
    for sid, s in state["sources"].items():
        if s["short"] is not None:
            by_path.setdefault(s["short"], []).append(sid)
    for (host, path), sids in sorted(by_path.items()):
        if len(sids) != 1:
            continue
        sid, new = sids[0], _source_id(host, path)
        if new == sid or new in state["sources"]:
            continue
        src = state["sources"].pop(sid)
        src["id"] = new
        state["sources"][new] = src
        state["identity_of"][new] = state["identity_of"].pop(sid)


def _set_aside(name, key, value, state):
    """Count one value as bookkeeping, and keep what a reader must still see:
    an object or a list of them (a source can hide in a shape no rule here
    knows, as Denmark's datafordeler entry did), and any key that names a
    licence, with its value."""
    state["bookkeeping"][key] += 1
    if isinstance(value, dict) or (
            isinstance(value, list) and any(isinstance(x, (dict, str)) for x in value)):
        state["objects"].append({"city": name, "key": key})
    if "licen" in key.lower():
        text = value if isinstance(value, str) else json.dumps(
            value, ensure_ascii=False, sort_keys=True)
        state["licence_notes"].append({"city": name, "key": key,
                                       "value": " ".join(text.split())[:200]})


def _walk_dict(name, key, value, state):
    if _is_osm_key(key) and not _names_another_publisher(value):
        if _osm_bookkeeping(key, value):
            _set_aside(name, key, value, state)
        else:
            _register_source(OSM_SID, OSM_HOST, "", name, {key}, "", OSM_SID,
                             state)
        return
    page, data_url, licence = _entry_urls(value)
    if ("made_from" in value or "tool" in value) and not (page or data_url):
        # A derived file names no publisher. One that also carries a URL does,
        # and is read as a source below.
        _set_aside(name, key, value, state)
        return
    if page or data_url:
        _register_url(name, key, page, data_url, _entry_layers(value, key),
                      licence, state)
        return
    if "url" in value or ("file" in value and "sha256" in value):
        state["unclassified"].append(
            {"city": name, "key": key, "reason": "source entry with no URL recorded"})
        return
    # A map of source entries nested under one key (ruian, sources, layers):
    # recurse only when at least one nested dict is itself a source, so a
    # file-hash map such as register_files stays one bookkeeping entry.
    if any(isinstance(v, dict) and (_is_source_like(v) or _is_osm_key(str(k)))
           for k, v in value.items()):
        for sub, subv in value.items():
            if isinstance(subv, dict) and (_is_source_like(subv) or _is_osm_key(str(sub))):
                _walk_dict(name, f"{key}.{sub}", subv, state)
            else:
                _set_aside(name, f"{key}.{sub}", subv, state)
        return
    _set_aside(name, key, value, state)


def _walk_string(name, key, value, state):
    if _is_osm_key(key):
        if ISO_TS_RE.match(value.strip()):
            _set_aside(name, key, value, state)
        else:
            _register_source(OSM_SID, OSM_HOST, "", name, {key}, "", OSM_SID,
                             state)
        return
    if key.endswith("_url"):
        if "licen" in key:
            _set_aside(name, key, value, state)
        elif _is_http(value):
            _register_url(name, key, "", value, {key}, "", state)
        else:
            state["unclassified"].append(
                {"city": name, "key": key, "reason": "a _url key whose value is not a URL"})
        return
    if _is_http(value):
        _register_url(name, key, "", value, {key}, "", state)
        return
    _set_aside(name, key, value, state)


def _walk_list(name, key, value, state):
    if _is_osm_key(key) and value and all(isinstance(x, str) for x in value):
        _register_source(OSM_SID, OSM_HOST, "", name, {key}, "", OSM_SID, state)
    else:
        _set_aside(name, key, value, state)


def _walk_key(name, key, value, state):
    if isinstance(value, dict):
        _walk_dict(name, key, value, state)
    elif isinstance(value, str):
        _walk_string(name, key, value, state)
    elif isinstance(value, list):
        _walk_list(name, key, value, state)
    elif isinstance(value, bool) or value is None or isinstance(value, (int, float)):
        _set_aside(name, key, value, state)
    else:
        state["unclassified"].append(
            {"city": name, "key": key, "reason": "unexpected value type"})


def collect(cities, outputs_dir):
    """Group every city's provenance entries into sources.

    `cities` is a list of {"name", "slug"} and `outputs_dir` a Path. Returns a
    dict of sources (id to source), the unclassified list, the bookkeeping
    counter, the missing-file list, the parse errors and the id collisions.
    """
    state = {"sources": {}, "identity_of": {}, "collisions": set(),
             "unclassified": [], "bookkeeping": Counter(),
             "objects": [], "licence_notes": [],
             "missing": [], "errors": [], "no_source": []}
    for entry in cities:
        name, slug = entry["name"], entry["slug"]
        path = outputs_dir / slug / "provenance.json"
        if not path.exists():
            state["missing"].append({"name": name, "slug": slug})
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            state["errors"].append(f"{path}: cannot parse: {exc}")
            continue
        if not isinstance(data, dict):
            state["errors"].append(f"{path}: not a JSON object")
            continue
        for key, value in data.items():
            _walk_key(name, key, value, state)
    _shorten_ids(state)
    return state


def _exit_code(state):
    """Non-zero for a city with no provenance file, a file that cannot be
    parsed, an id shared by two sources, and a city whose file records no
    source at all (an empty object, or dates and boxes only): a map has
    sources, so that file is as good as missing."""
    return 1 if (state["missing"] or state["errors"] or state["collisions"]
                 or state["no_source"]) else 0


def _portal_groups(state):
    """{host/first path part: sorted ids} for the sources with no dataset
    page that share one, where more than one does: the coarser view."""
    groups = {}
    for s in state["sources"].values():
        if s["coarse"] is not None:
            groups.setdefault(s["coarse"], []).append(s["id"])
    return {g: sorted(ids) for g, ids in sorted(groups.items()) if len(ids) > 1}


def _only_osm(state):
    """Cities whose every recorded source is OpenStreetMap: a map of business
    dots has a register behind it, so its provenance file leaves it out or
    records it in a shape set aside here. Counted as covered, and wrongly."""
    seen = {}
    for s in state["sources"].values():
        for c in s["cities"]:
            seen.setdefault(c, set()).add(s["id"])
    return sorted(c for c, ids in seen.items() if ids == {OSM_SID})


def _grouped(rows, fields):
    """{tuple of fields: sorted cities} for a list of per-city rows."""
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r[f] for f in fields), set()).add(r["city"])
    return {k: sorted(v) for k, v in sorted(groups.items())}


def _json_payload(state):
    return {
        "cities_only_openstreetmap": _only_osm(state),
        "hosts": len({s["host"] for s in state["sources"].values()}),
        "licence_fields_outside_a_source": [
            {"key": k, "value": v, "cities": cities}
            for (k, v), cities in _grouped(state["licence_notes"], ("key", "value")).items()],
        "objects_set_aside": [
            {"key": k, "cities": cities}
            for (k,), cities in _grouped(state["objects"], ("key",)).items()],
        "cities_without_provenance": sorted(m["name"] for m in state["missing"]),
        "cities_with_no_source": sorted(state["no_source"]),
        "portal_groups": [
            {"group": g, "sources": ids} for g, ids in _portal_groups(state).items()],
        "sources": [
            {"id": s["id"], "host": s["host"], "dataset_page": s["dataset_page"],
             "cities": sorted(s["cities"]), "layers": sorted(s["layers"]),
             "licence": sorted(s["licences"])}
            for s in sorted(state["sources"].values(), key=lambda x: x["id"])
        ],
        "unclassified": [
            {"city": u["city"], "key": u["key"], "reason": u["reason"]}
            for u in sorted(state["unclassified"], key=lambda x: (x["city"], x["key"]))
        ],
    }


def _write_json(path, state):
    text = json.dumps(_json_payload(state), ensure_ascii=False, indent=2,
                      sort_keys=True)
    Path(path).write_bytes((text + "\n").encode("utf-8"))


def _slug_names(cities, slug):
    return [c["name"] for c in cities if c["slug"] == slug]


def _run(cities, outputs_dir, city=None, json_out=None):
    state = collect(cities, outputs_dir)
    all_names = [c["name"] for c in cities]
    # Coverage is judged on the FULL source set, before any --city filter.
    covered = set()
    for s in state["sources"].values():
        covered |= s["cities"]
    missing_names = {m["name"] for m in state["missing"]}
    uncovered = sorted(n for n in all_names
                       if n not in covered and n not in missing_names)
    state["no_source"] = uncovered

    if city:
        target = set(_slug_names(cities, city))
        if not target:
            print(f"no city has slug '{city}'")
            return 1
        state["sources"] = {sid: s for sid, s in state["sources"].items()
                            if s["cities"] & target}
        state["unclassified"] = [u for u in state["unclassified"]
                                 if u["city"] in target]
        state["missing"] = [m for m in state["missing"] if m["slug"] == city]
        state["no_source"] = [n for n in uncovered if n in target]
        state["objects"] = [o for o in state["objects"] if o["city"] in target]
        state["licence_notes"] = [n for n in state["licence_notes"]
                                  if n["city"] in target]
        print(f"commercial_use_sources --city {city}: "
              f"{len(state['sources'])} sources used by {', '.join(sorted(target))}")
    else:
        hosts = len({s["host"] for s in state["sources"].values()})
        print(f"commercial_use_sources: {len(state['sources'])} sources on "
              f"{hosts} hosts, "
              f"{len(all_names)} cities, {len(state['missing'])} without a "
              f"provenance file, {sum(state['bookkeeping'].values())} "
              f"bookkeeping entries, {len(state['unclassified'])} unclassified "
              f"entries")

    for s in sorted(state["sources"].values(), key=lambda x: x["id"]):
        licence = ", ".join(sorted(s["licences"])) or "(none)"
        layers = ", ".join(sorted(s["layers"])) or "unknown"
        cities_line = ", ".join(sorted(s["cities"]))
        print(f"{s['id']}  {s['host']}  cities={len(s['cities'])}  "
              f"layers={layers}  licence={licence}  cities: {cities_line}")

    if city:
        for n in sorted(target & set(uncovered)):
            print(f"\n{n} has a provenance file but no source entry")
    else:
        if state["missing"]:
            print("\ncities with no provenance file:")
            for m in sorted(state["missing"], key=lambda x: x["name"]):
                print(f"  {m['name']}  ({m['slug']})")
        if uncovered:
            print("\ncities with a provenance file but no source entry:")
            for n in uncovered:
                print(f"  {n}")
    for err in state["errors"]:
        print(f"error: {err}")
    for err in sorted(state["collisions"]):
        print(f"error: {err}")
    if state["unclassified"]:
        print(f"\nunclassified entries ({len(state['unclassified'])}):")
        for u in sorted(state["unclassified"], key=lambda x: (x["city"], x["key"])):
            print(f"  {u['city']}.{u['key']}  ({u['reason']})")
    only_osm = _only_osm(state)
    if only_osm:
        print(f"\ncities whose only recorded source is OpenStreetMap "
              f"({len(only_osm)}): their register is missing from provenance "
              f"or set aside below")
        for n in only_osm:
            print(f"  {n}")
    if not city:
        per_host = Counter(s["host"] for s in state["sources"].values())
        many = [(h, n) for h, n in sorted(per_host.items(), key=lambda x: (-x[1], x[0]))
                if n > 1]
        if many:
            print(f"\nhosts with more than one source ({len(many)}): one licence "
                  f"may cover a whole host; a person decides")
            for h, n in many:
                print(f"  {h}  sources={n}")
    groups = _portal_groups(state)
    if groups:
        print(f"\nportal groups ({len(groups)}): sources with no dataset page "
              f"that share a host and first path part; one licence may cover a "
              f"group, a person decides")
        for g, ids in groups.items():
            print(f"  {g}  sources={len(ids)}: {', '.join(ids)}")
    notes = _grouped(state["licence_notes"], ("key", "value"))
    if notes:
        print(f"\nlicence fields outside a source entry ({len(notes)}): read, "
              f"attached to no source")
        for (k, v), cities in notes.items():
            print(f"  {k} = {v}  cities: {', '.join(cities)}")
    objects = _grouped(state["objects"], ("key",))
    if objects:
        print(f"\nobjects set aside as bookkeeping ({len(objects)} keys): each "
              f"is an object or a list no rule read as a source; check none is one")
        for (k,), cities in objects.items():
            print(f"  {k}  cities: {', '.join(cities)}")
    if state["bookkeeping"]:
        summary = ", ".join(f"{k} x{n}"
                            for k, n in state["bookkeeping"].most_common())
        print(f"\nbookkeeping set aside: {summary}")

    if json_out:
        _write_json(json_out, state)
    return _exit_code(state)


def city_list(cities_py):
    """Parse app/cities.py's CITIES into [{"name", "slug"}] without importing
    streamlit. The slug is the outputs folder: check_provenance.SLUG_OVERRIDES
    where a name differs, else the lower-cased name with spaces as
    underscores. Several names may share one slug; each reads that folder."""
    tree = ast.parse(cities_py.read_text(encoding="utf-8"))
    names = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == "CITIES" for t in node.targets):
            for d in node.value.elts:
                pairs = {getattr(k, "value", None): getattr(v, "value", None)
                         for k, v in zip(d.keys, d.values)}
                if pairs.get("name"):
                    names.append(pairs["name"])
    return [{"name": n, "slug": SLUG_OVERRIDES.get(n, n.lower().replace(" ", "_"))}
            for n in names]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", metavar="OUT",
                    help="also write the result as JSON (UTF-8, LF, keys sorted)")
    ap.add_argument("--city", metavar="SLUG",
                    help="report only the sources this slug's cities use")
    ap.add_argument("--selftest", action="store_true",
                    help="run the fabricated cases and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    cities = city_list(ROOT / "app" / "cities.py")
    return _run(cities, ROOT / "outputs", city=args.city, json_out=args.json)


def selftest():
    """Fabricated provenance objects in a temporary folder, through the same
    collect and _run that main() uses, including the exit codes."""
    from contextlib import redirect_stdout

    tmp = Path(tempfile.mkdtemp(prefix="commercial_use_sources_"))
    results = [0, 0]  # ok, total

    def put(slug, obj=None, raw=None):
        d = tmp / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "provenance.json").write_bytes(
            (raw if raw is not None else json.dumps(obj)).encode("utf-8"))

    def run(cities, **kw):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = _run(cities, tmp, **kw)
        return rc, buf.getvalue()

    def case(label, cond):
        results[1] += 1
        results[0] += bool(cond)
        print(f"  {'ok ' if cond else 'BAD'} {label}")

    def city(name, slug):
        return {"name": name, "slug": slug}

    try:
        # 1. Two cities sharing one national source collapse to one source.
        put("c1a", {"reg": {"url": "https://national.example/reg.csv",
                            "file": "r.csv", "sha256": "x"}})
        put("c1b", {"reg": {"url": "https://national.example/reg.csv",
                            "file": "r.csv", "sha256": "x"}})
        res = collect([city("A", "c1a"), city("B", "c1b")], tmp)
        case("two cities sharing one national source collapse to one source",
             len(res["sources"]) == 1
             and next(iter(res["sources"].values()))["cities"] == {"A", "B"})

        # 2. Two datasets on one portal host stay two sources: only the
        #    dataset page, not the host, can tell them apart.
        put("c2", {
            "d1": {"url": "https://portal.example/x/d1.csv",
                   "dataset_page": "https://portal.example/dataset/d1"},
            "d2": {"url": "https://portal.example/x/d2.csv",
                   "dataset_page": "https://portal.example/dataset/d2"}})
        res = collect([city("A", "c2")], tmp)
        case("two datasets on one portal host stay two sources",
             len(res["sources"]) == 2)

        # 3. An entry with no URL is reported unclassified with city and key.
        put("c3", {"weird": {"file": "f.bin", "sha256": "abc"}})
        res = collect([city("A", "c3")], tmp)
        case("an entry with no URL is unclassified, named with city and key",
             res["unclassified"] == [
                 {"city": "A", "key": "weird",
                  "reason": "source entry with no URL recorded"}]
             and not res["sources"])

        # 4. A city with no provenance file is named and the exit code is
        #    non-zero, through _run (main's body), not only collect.
        put("c4a", {"reg": {"url": "https://x.example/r.csv", "file": "r",
                            "sha256": "s"}})
        rc, out = run([city("A", "c4a"), city("B", "c4b")])
        case("a city with no provenance file is named and the run exits non-zero",
             rc != 0 and "B" in out and "c4b" in out)

        # 5. Two Overpass mirror hosts are one OpenStreetMap source.
        put("c5a", {"osm_rail": {"host": "overpass-api.de", "query": "q"}})
        put("c5b", {"osm_rail": {"host": "overpass.kumi.systems", "query": "q"}})
        res = collect([city("A", "c5a"), city("B", "c5b")], tmp)
        case("two Overpass mirror hosts are one OpenStreetMap source",
             len(res["sources"]) == 1
             and OSM_SID in res["sources"]
             and res["sources"][OSM_SID]["cities"] == {"A", "B"})

        # 6. A date string and a bounding box are bookkeeping, not sources and
        #    not unclassified.
        put("c6", {"fetched_utc": "2026-01-01T00:00:00+00:00",
                   "osm_bbox": [1.0, 2.0, 3.0, 4.0],
                   "reg": {"url": "https://x.example/r.csv", "file": "r",
                           "sha256": "s"}})
        res = collect([city("A", "c6")], tmp)
        case("a date and a bounding box are bookkeeping, not sources or unclassified",
             len(res["sources"]) == 1
             and "fetched_utc" in res["bookkeeping"]
             and "osm_bbox" in res["bookkeeping"]
             and not res["unclassified"])

        # 7. Source ids are the same whatever order the cities are read in.
        put("c7a", {"reg": {"url": "https://nat.example/reg.csv", "file": "r",
                            "sha256": "s"}, "osm_host": "overpass-api.de"})
        put("c7b", {"reg": {"url": "https://nat.example/reg.csv", "file": "r",
                            "sha256": "s"}})

        def canon(res):
            return sorted((sid, sorted(s["cities"]))
                          for sid, s in res["sources"].items())

        r1 = collect([city("A", "c7a"), city("B", "c7b")], tmp)
        r2 = collect([city("B", "c7b"), city("A", "c7a")], tmp)
        case("source ids are the same whatever order the cities are read in",
             canon(r1) == canon(r2) and len(r1["sources"]) == 2)

        # 8. Two different sources forced onto one id fail and name both.
        put("c8", {"s1": {"url": "https://a.b/x.csv",
                          "dataset_page": "https://a.b/d/p"},
                   "s2": {"url": "https://a-b/x.csv",
                          "dataset_page": "https://a-b/d/p"}})
        rc, out = run([city("A", "c8")])
        case("two different sources forced onto one id fail and name both",
             rc != 0 and "a.b" in out and "a-b" in out)

        # 9. A provenance file that is not valid JSON fails and names the file.
        put("c9", raw="{ this is not json")
        rc, out = run([city("A", "c9")])
        case("a provenance file that is not valid JSON fails and names the file",
             rc != 0 and "c9" in out and "provenance.json" in out)

        # 10. --json output is byte-identical across two runs.
        put("c10a", {"reg": {"url": "https://nat.example/reg.csv", "file": "r",
                             "sha256": "s"},
                     "osm_places": {"host": "overpass-api.de", "query": "q"},
                     "weird": {"file": "f", "sha256": "x"}})
        put("c10b", {"reg": {"url": "https://nat.example/reg.csv", "file": "r",
                             "sha256": "s"}})
        cities = [city("A", "c10a"), city("B", "c10b")]
        j1, j2 = tmp / "r1.json", tmp / "r2.json"
        with redirect_stdout(io.StringIO()):
            _run(cities, tmp, json_out=j1)
            _run(cities, tmp, json_out=j2)
        case("--json output is byte-identical across two runs",
             j1.read_bytes() == j2.read_bytes())

        # 11. A leading www. is not part of a publisher's host.
        put("c11a", {"reg": {"url": "https://www.nat.example/reg.csv"}})
        put("c11b", {"reg": {"url": "https://nat.example/reg.csv"}})
        res = collect([city("A", "c11a"), city("B", "c11b")], tmp)
        case("a host with and without www. is one source",
             len(res["sources"]) == 1)

        # 12. Sources are written in id order, whatever order they were met.
        put("c12", {"z": {"url": "https://zzz.example/a.csv"},
                    "a": {"url": "https://aaa.example/a.csv"}})
        j3 = tmp / "r3.json"
        with redirect_stdout(io.StringIO()):
            _run([city("A", "c12")], tmp, json_out=j3)
        ids = [s["id"] for s in json.loads(j3.read_bytes().decode("utf-8"))["sources"]]
        case("--json lists sources in id order", ids == sorted(ids) and len(ids) == 2)

        # 13. An entry's licence field is printed beside its source.
        put("c13", {"reg": {"url": "https://lic.example/r.csv", "licence": "CC BY 4.0"}})
        rc, out = run([city("A", "c13")])
        case("an entry's licence field is printed beside its source",
             "licence=CC BY 4.0" in out)

        # 14. A top-level string whose key ends _url is a source.
        put("c14", {"gtfs_url": "https://feeds.example/gtfs/feed.zip"})
        res = collect([city("A", "c14")], tmp)
        case("a top-level _url string is a source",
             list(res["sources"]) == ["feeds-example-gtfs"])

        # 15. --city reports that slug's sources only; an unknown slug fails.
        put("c15a", {"reg": {"url": "https://only-a.example/r.csv"}})
        put("c15b", {"reg": {"url": "https://only-b.example/r.csv"}})
        both = [city("A", "c15a"), city("B", "c15b")]
        rc, out = run(both, city="c15a")
        rc_unknown, _ = run(both, city="no_such_slug")
        case("--city reports one slug's sources, and an unknown slug exits non-zero",
             rc == 0 and "only-a-example" in out and "only-b-example" not in out
             and rc_unknown != 0)

        # 16. A map of source entries under one key is walked, one source each.
        put("c16", {"ruian": {"100": {"url": "https://one.example/a.zip"},
                              "200": {"url": "https://two.example/b.zip"}}})
        res = collect([city("A", "c16")], tmp)
        case("a map of source entries under one key gives one source each",
             len(res["sources"]) == 2
             and {"ruian.100"} in [s["layers"] for s in res["sources"].values()])

        # 17. A city's outputs folder follows check_provenance's overrides.
        over_name, over_slug = next(
            (n, s) for n, s in sorted(SLUG_OVERRIDES.items())
            if s != n.lower().replace(" ", "_"))
        cities_py = tmp / "cities.py"
        cities_py.write_bytes(
            f'CITIES = [{{"name": {over_name!r}}}, {{"name": "Plain Name"}}]\n'.encode("utf-8"))
        case("a city's folder follows the slug overrides, else its lower-cased name",
             city_list(cities_py) == [{"name": over_name, "slug": over_slug},
                                      {"name": "Plain Name", "slug": "plain_name"}])

        # 18. A city with only OpenStreetMap recorded is named as such.
        put("c18a", {"osm_rail": {"host": "overpass-api.de", "query": "q"}})
        put("c18b", {"osm_rail": {"host": "overpass-api.de", "query": "q"},
                     "reg": {"url": "https://reg.example/r.csv"}})
        rc, out = run([city("OnlyOsm", "c18a"), city("HasRegister", "c18b")])
        section = out.split("only recorded source is OpenStreetMap", 1)[-1].split("\n\n", 1)[0]
        case("a city with only OpenStreetMap recorded is named, one with a register is not",
             "only recorded source is OpenStreetMap (1)" in out
             and "OnlyOsm" in section and "HasRegister" not in section)

        # 19. An object no rule reads as a source is listed with its city, and
        #     a licence key outside any source entry is listed with its value.
        put("c19", {"reg": {"url": "https://reg.example/r.csv"},
                    "register_x": {"snapshot": "2026-01-01", "rows": 5},
                    "gtfs_licence": "odc-odbl"})
        rc, out = run([city("Hidden", "c19")])
        objects = out.split("objects set aside as bookkeeping", 1)[-1]
        case("an object set aside is listed with its city, and a licence key with its value",
             "register_x  cities: Hidden" in objects
             and "gtfs_licence = odc-odbl  cities: Hidden" in out)

        # 20. The header counts hosts as well as sources.
        put("c20", {"d1": {"url": "https://p.example/x/1.csv",
                           "dataset_page": "https://p.example/dataset/d1"},
                    "d2": {"url": "https://p.example/x/2.csv",
                           "dataset_page": "https://p.example/dataset/d2"}})
        rc, out = run([city("A", "c20")])
        case("the header counts hosts as well as sources, and names a host with two",
             "2 sources on 1 hosts" in out and "p.example  sources=2" in out)

        # Found by an adversarial review (2026-10-12): each is a way the count
        # could be wrong and look right.

        # 21. Dataset pages that differ only in the query string are two
        #     sources (Daegu serves nine registers from one dataView.do).
        put("c21", {"a": {"dataset_page": "https://portal.example/view.do?id=1"},
                    "b": {"dataset_page": "https://portal.example/view.do?id=2"}})
        res = collect([city("A", "c21")], tmp)
        case("dataset pages differing only in the query string stay two sources",
             sorted(res["sources"]) == ["portal-example-view-do-id-1",
                                        "portal-example-view-do-id-2"])

        # 22. With no dataset page, files in two folders under one first path
        #     part are two sources, and the coarser view groups them; an
        #     endpoint with no file name keeps its whole path.
        put("c22", {"register": {"url": "https://files.example/download/reg/business.csv"},
                    "permits": {"url": "https://files.example/download/permits/all.csv"},
                    "api": {"url": "https://files.example/v1/bag/straten"}})
        rc, out = run([city("A", "c22")])
        case("two folders under one path part are two sources, grouped in the portal view",
             "files.example/download  sources=2: files-example-download-permits, "
             "files-example-download-reg" in out
             and "files-example-v1-bag-straten  " in out)

        # 29. A page's query string stays in the id only where another page
        #     shares the path; whatever order the files are read in.
        put("c29a", {"a": {"dataset_page": "https://one.example/view.do?id=7"}})
        put("c29b", {"b": {"dataset_page": "https://two.example/view.do?id=1"}})
        put("c29c", {"c": {"dataset_page": "https://two.example/view.do?id=2"}})
        trio = [city("A", "c29a"), city("B", "c29b"), city("C", "c29c")]
        want = ["one-example-view-do", "two-example-view-do-id-1", "two-example-view-do-id-2"]
        case("a query string stays in the id only where the path is shared, in any order",
             sorted(collect(trio, tmp)["sources"]) == want
             and sorted(collect(trio[::-1], tmp)["sources"]) == want)

        # 23. Another publisher's URL under an osm_ key is that publisher's.
        put("c23", {"osm_basemap": {"tiles": "https://carto.example/light/z.png"}})
        res = collect([city("A", "c23")], tmp)
        case("another publisher's URL under an osm_ key is not OpenStreetMap",
             list(res["sources"]) == ["carto-example-light"])

        # 24. An Overpass or OpenStreetMap URL under any key is OpenStreetMap.
        put("c24", {"overpass_url": "https://overpass-api.de/api/interpreter",
                    "credit": {"url": "https://www.openstreetmap.org/copyright"}})
        res = collect([city("A", "c24")], tmp)
        case("an Overpass or OpenStreetMap URL under any key is OpenStreetMap",
             list(res["sources"]) == [OSM_SID])

        # 25. An osm_ entry nested in a map of sources is OpenStreetMap.
        put("c25", {"sources": {"osm_places": {"host": "overpass-api.de", "query": "q"},
                                "reg": {"url": "https://reg.example/data/r.csv"}}})
        res = collect([city("A", "c25")], tmp)
        case("an osm_ entry nested under another key is OpenStreetMap",
             sorted(res["sources"]) == [OSM_SID, "reg-example-data"])

        # 26. A file that records no source is as good as missing: named, in
        #     the JSON, and the run exits non-zero.
        put("c26", {"fetched_utc": "2026-01-01T00:00:00+00:00"})
        j4 = tmp / "r4.json"
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = _run([city("Hollow", "c26")], tmp, json_out=j4)
        case("a provenance file with no source fails the run and is named",
             rc != 0 and "Hollow" in buf.getvalue()
             and json.loads(j4.read_bytes().decode("utf-8"))["cities_with_no_source"] == ["Hollow"])

        # 27. A derived file that also names a URL is read as a source.
        put("c27", {"boundary": {"tool": "osmium", "url": "https://gadm.example/data/x.zip"},
                    "derived": {"tool": "ogr2ogr", "made_from": "x.zip"}})
        res = collect([city("A", "c27")], tmp)
        case("a URL beside a tool key is a source; a tool with no URL is set aside",
             list(res["sources"]) == ["gadm-example-data"]
             and [o["key"] for o in res["objects"]] == ["derived"])

        # 28. A port is part of the host.
        put("c28", {"a": {"url": "https://svc.example:8443/api/x.csv"},
                    "b": {"url": "https://svc.example:9443/api/y.csv"}})
        res = collect([city("A", "c28")], tmp)
        case("two ports on one machine are two hosts",
             sorted(res["sources"]) == ["svc-example-8443-api", "svc-example-9443-api"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"{results[0]} of {results[1]} cases behaved as intended.")
    return 0 if results[0] == results[1] else 1


if __name__ == "__main__":
    sys.exit(main())
