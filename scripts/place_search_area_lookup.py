"""Fill the search area of the plan entries that have none, from the stations
each map draws, by the project's scope rule. One light Overpass query a city.

    python scripts/place_search_area_lookup.py PLAN_JSON [CITY ...] --host MIRROR [--wait MIN] [--report FILE] [--stop-after N]
    python scripts/place_search_area_lookup.py PLAN_JSON [CITY ...] --dry-run
    python scripts/place_search_area_lookup.py --selftest

THE RULE IT APPLIES (owner, 2026-10-12; pipeline/place_index.py, "THE SEARCHED
AREA"): an index covers the boundary the map's businesses are cut to and, on
a regional map, every municipality a drawn station sits in; nothing wider.
PLAN_JSON is a plan of scripts/place_search_scaffold.py, a draft or not. With
no CITY, every city in it whose `relations` is empty is looked up.

PER CITY, ONE QUERY. For every station the map draws
(place_index.map_stations), the administrative boundary relations that hold
it, tags only and no geometry. The raw answer is cached at
data/<city>/raw/osm_place_area_lookup_<date>.json and a city with such a file,
of any date, is never asked again. Boundaries are stable, so an answer from
data months old is accepted here (it is not for places: the place fetch's
PLACE_MAX_AGE_DAYS). The request goes through pipeline/osm.py's fetch, pinned
to --host, while holding that mirror's FetchLock
(pipeline/place_index_fetch.py), as a place fetch does: one query in flight
per mirror on this machine.

CHOOSING THE ADMIN LEVEL: BY PRECEDENT, NEVER BY GUESS. The cities that
already have search (a config with PLACE_AREA) each used relations of some
admin_level, read here from their outline cache. Grouped by country
(app/cities.py), that is the precedent table. A looked-up city is resolved
ONLY when nothing is left to judge: its country has exactly one precedent
level, at least one returned relation is at that level, there are no more
than MAX_AUTO_RELATIONS of them, and at least one of them is the place the
repository says the city is (NAME_ATTRS, CODE_TAGS, or the city's own name).
Everything else is left unfilled with its reason and its candidates, for a
person.

WHAT IT WRITES. The plan, in place, for resolved cities only: `relations`
sorted ascending and a `note` beginning "area from stations, admin_level N,
lookup <date>". A plan's "draft" marker is never removed: a draft stays a
draft until a session has read it. With --report, a JSON file of every city
asked: resolved or not, the relations with their names and levels, the
reason when not, and the precedent table used. --dry-run prints each city's
query, makes no request and writes nothing.

WHAT IT DOES NOT DO. It downloads no geometry: the place fetch's own
boundary-first step re-checks the area (stations per municipality) before
its heavy queries. It never widens an entry that already has relations.

EXIT CODE. 0 when every city asked was answered, resolved or left for a
person; 1 when a request failed, a mirror was given up on (--stop-after
failures in a row, the rest not asked) or a named city is not in the plan; 2
when it could not run.
"""
import argparse
import ast
import datetime
import importlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# The mirrors a lookup may be pinned to: pipeline/osm.py's OVERPASS_HOSTS by
# name, repeated here as scripts/place_search_fetch_queue.py repeats them, so
# parsing the command line imports nothing that can fetch (the selftest fails
# if the lists differ).
MIRRORS = ("overpass-api.de", "overpass.kumi.systems")
# More relations than this are never filled without a person. The widest
# built area is Tokyo's 23 wards and the widest regional one Seattle's 11
# municipalities (2026-10-12), so 25 clears every precedent; past it the
# likelier reading is a level too fine (wards under a city) than a map that
# wide. A regional map can be large, so this is a bar to raise with a
# measured case, not a rule about maps.
MAX_AUTO_RELATIONS = 25
# The in-query timeout, the request's own, the tries and the total budget. A
# tags-only query: the place fetch's outline query, which also returns
# geometry, runs at 60 s. One retry round is two tries on a pinned mirror
# (osm.fetch doubles it), with the owner's 60 s between them after a 504 or
# 429: 90 + 60 + 90 fits in 300.
QUERY_TIMEOUT_S = 60
REQUEST_TIMEOUT_S = 90
REQUEST_RETRIES = 1
REQUEST_DEADLINE_S = 300
# Request failures in a row before the mirror is given up on and the rest of
# the cities left "not asked": a dead mirror costs REQUEST_DEADLINE_S a city,
# two and a half hours for a wave of 30. Three is the number the night runner
# uses to set a mirror aside (scripts/place_search_night.py).
STOP_AFTER = 3
CACHE_GLOB = "osm_place_area_lookup_*.json"
# The area id of a relation is this plus its id (config.PLACE_AREA).
AREA_BASE = 3600000000
# Config attributes that NAME the municipality the map is cut to, compared
# with each relation's NAME_TAGS, and attributes that carry its official
# CODE, compared with the tag OpenStreetMap files that code under. Read from
# the 184 configs without search on 2026-10-13: MUNICIPALITY is on all 92
# Japanese ones, BOUNDARY_COMMUNE_CODE on 23 French, IBGE_MUNICIPIO on all 8
# Brazilian. The two tag keys are OpenStreetMap's usual ones and were NOT
# confirmed against a live answer here; a wrong key only loses that evidence,
# since the city's own name is tried as well.
NAME_ATTRS = ("MUNICIPALITY", "BOUNDARY_NAME", "BOUNDARY_OSM_NAME", "OSM_BOUNDARY_NAME",
              "KOMMUNE_NAME")
CODE_TAGS = {"BOUNDARY_COMMUNE_CODE": "ref:INSEE", "IBGE_MUNICIPIO": "IBGE:GEOCODIGO"}
NAME_TAGS = ("name", "name:en", "name:ja")
_PLACE_AREA_RE = re.compile(r"(?m)^PLACE_AREA\s*=")

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def _read_json(path):
    """A JSON file read as UTF-8 bytes."""
    return json.loads(Path(path).read_bytes().decode("utf-8"))


def _write_json(path, data):
    """A JSON file written as UTF-8 bytes with LF line endings."""
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    Path(path).write_bytes(text.encode("utf-8"))


def _norm(text):
    """A name folded for comparison: accents and case dropped, anything that
    is not a letter or a digit read as a space."""
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).casefold()
    return " ".join("".join(ch if ch.isalnum() else " " for ch in text).split())


def build_query(stations):
    """The one query of a city: the areas holding each distinct station
    point, gathered into one set, then the administrative boundary relations
    those areas were made from, tags only. Points are rounded to 5 decimals
    (about a meter), so two platforms of one station ask once."""
    points = list(dict.fromkeys(f"{lat:.5f},{lon:.5f}" for _, lat, lon in stations))
    lines = [f"[out:json][timeout:{QUERY_TIMEOUT_S}];"]
    for i, point in enumerate(points):
        if i == 0:
            lines.append(f"is_in({point})->.a;")
        else:
            lines.append(f"is_in({point})->.b;")
            lines.append("(.a; .b;)->.a;")
    lines.append('rel(pivot.a)["boundary"="administrative"];')
    lines.append("out tags;")
    return "\n".join(lines) + "\n"


def city_listing(root):
    """{pipeline folder: (country, city name)} from app/cities.py's CITIES,
    each folder found through the page that imports its config, as
    scripts/place_search_scaffold.py finds a city's page. A folder whose
    pages name more than one country gets country None."""
    try:
        tree = ast.parse(Path(root, "app", "cities.py").read_bytes().decode("utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return {}
    pages = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "CITIES"
                and isinstance(node.value, ast.List)):
            for entry in node.value.elts:
                if not isinstance(entry, ast.Dict):
                    continue
                pairs = {getattr(k, "value", None): getattr(v, "value", None)
                         for k, v in zip(entry.keys, entry.values)}
                if isinstance(pairs.get("page"), str):
                    pages[pairs["page"]] = (pairs.get("country"), pairs.get("name"))
    found = {}
    for rel, (country, name) in pages.items():
        try:
            page_tree = ast.parse(Path(root, "app", rel).read_bytes().decode("utf-8"))
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        modules = set()
        for node in ast.walk(page_tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
                modules.update(f"{node.module}.{a.name}" for a in node.names)
            elif isinstance(node, ast.Import):
                modules.update(a.name for a in node.names)
        for module in modules:
            m = re.fullmatch(r"pipeline\.([A-Za-z0-9_]+)\.config", module)
            if m:
                found.setdefault(m.group(1), []).append((country, name))
    out = {}
    for folder, seen in found.items():
        countries = {c for c, _ in seen}
        # The shortest name is the city's own where a regional page reads the
        # same config ("Brussels" beside "Brussels (Regional)").
        name = min((n for _, n in seen if isinstance(n, str)), key=len, default=None)
        out[folder] = (countries.pop() if len(countries) == 1 else None, name)
    return out


def built_cities(root):
    """Sorted folders under pipeline/ whose config.py declares PLACE_AREA."""
    out = []
    for path in sorted(Path(root, "pipeline").iterdir()):
        config = path / "config.py"
        try:
            if config.is_file() and _PLACE_AREA_RE.search(config.read_bytes().decode("utf-8")):
                out.append(path.name)
        except (OSError, UnicodeDecodeError):
            continue
    return out


def real_load(city):
    """A city's config module. Importing a config makes no request."""
    return importlib.import_module(f"pipeline.{city}.config")


def precedents(root, listing, load_config):
    """({country: {admin level: [city, ...]}}, [(city, why not read), ...])
    from the cities that already have search: the admin_level tag of each
    relation their PLACE_AREA names, read from the outline cache the place
    fetch wrote. Offline. A built city whose cache is not on this machine, or
    whose country is unknown, adds nothing and is listed, so a thin table is
    seen for what it is."""
    from pipeline import place_index
    table, unread = {}, []
    for city in built_cities(root):
        country = (listing.get(city) or (None, None))[0]
        if not country:
            unread.append((city, "no country in app/cities.py"))
            continue
        try:
            config = load_config(city)
            # An area written as ids names its relations; one written as a
            # tag filter (Kyoto's) names whatever the outline query returned
            # for it, which is every relation of the cache.
            area = str(config.PLACE_AREA).replace(" ", "")
            wanted = ({int(n) - AREA_BASE for n in re.findall(r"\d+", area)}
                      if re.fullmatch(r"\(id:[\d,]+\)", area) else None)
            elements = _read_json(place_index.outline_cache(config))["elements"]
        except KeyboardInterrupt:
            raise
        except BaseException as exc:
            unread.append((city, f"{type(exc).__name__}: {exc}"))
            continue
        levels = set()
        for e in elements:
            if e.get("type") == "relation" and (wanted is None or e.get("id") in wanted):
                level = str((e.get("tags") or {}).get("admin_level", ""))
                if level.isdigit():
                    levels.add(int(level))
        if not levels:
            unread.append((city, "its outline cache holds no admin_level for its relations"))
        for level in levels:
            table.setdefault(country, {}).setdefault(level, []).append(city)
    return table, unread


def relations_of(elements):
    """The administrative relations of an answer, each {"id", "name",
    "level", "tags"}, the finest level first, then by id. level is None when
    the tag is missing or not a number."""
    out = []
    for e in elements:
        if e.get("type") != "relation":
            continue
        tags = e.get("tags") or {}
        level = str(tags.get("admin_level", ""))
        out.append({"id": e["id"], "name": tags.get("name:en") or tags.get("name") or "",
                    "level": int(level) if level.isdigit() else None, "tags": tags})
    return sorted(out, key=lambda r: (-(r["level"] if r["level"] is not None else -1), r["id"]))


def identity(config, city_name):
    """What the repository says the city is: (names, codes, own name). names
    are the config's NAME_ATTRS strings, codes its CODE_TAGS as (tag, value),
    and the own name is app/cities.py's without a bracketed part ("Lille
    (Regional)" is Lille)."""
    names = [v for v in (getattr(config, a, None) for a in NAME_ATTRS)
             if isinstance(v, str) and v.strip()]
    codes = [(tag, str(getattr(config, attr))) for attr, tag in CODE_TAGS.items()
             if isinstance(getattr(config, attr, None), (str, int))
             and not isinstance(getattr(config, attr), bool)]
    own = re.sub(r"\s*\([^)]*\)", "", city_name or "").strip()
    return names, codes, own


def matched_by(relation, names, codes, own):
    """What ties one relation to the city, or None: its official code, a
    config name equal to one of its NAME_TAGS, or, for a config that names
    no municipality, the city's own name as whole words inside one of them
    ("Copenhagen" in "Copenhagen Municipality")."""
    tags = relation["tags"]
    for tag, value in codes:
        if str(tags.get(tag, "")).strip() == value.strip():
            return tag
    held = [_norm(tags[t]) for t in NAME_TAGS if tags.get(t)]
    if any(_norm(n) in held for n in names):
        return "config name"
    # A config that names its municipality is held to that name: the city's
    # own name is evidence only where the config names none.
    wanted = _norm(own)
    if not names and wanted and any(f" {wanted} " in f" {h} " for h in held):
        return "city name"
    return None


def choose(country, relations, table, names, codes, own):
    """(chosen relations or None, level or None, reason or None, how it was
    tied to the city or None). Resolved only when unambiguous; the reason
    says which judgment is left."""
    if not country:
        return None, None, "no country for this city in app/cities.py", None
    levels = table.get(country) or {}
    if not levels:
        return None, None, (f"no built city in {country} to take an admin level from: "
                            f"a first city in a country is a person's call"), None
    if len(levels) > 1:
        said = "; ".join(f"level {lv} ({', '.join(sorted(levels[lv]))})" for lv in sorted(levels))
        return None, None, f"{country}'s built cities used several admin levels: {said}", None
    level = next(iter(levels))
    at_level = [r for r in relations if r["level"] == level]
    if not at_level:
        return None, level, (f"no relation at admin_level {level}, {country}'s precedent "
                             f"({', '.join(sorted(levels[level]))}), holds a station"), None
    if len(at_level) > MAX_AUTO_RELATIONS:
        return None, level, (f"{len(at_level)} relations at admin_level {level}, more than "
                             f"the {MAX_AUTO_RELATIONS} filled without a person"), None
    how = next((h for h in (matched_by(r, names, codes, own) for r in at_level) if h), None)
    if how is None:
        wanted = ", ".join(names + [v for _, v in codes] + ([own] if own else []))
        return None, level, (f"name mismatch: none of the {len(at_level)} relation(s) at "
                             f"admin_level {level} is {wanted}"), None
    return at_level, level, None, how


def cache_dir(root, city, config):
    """Where a city's raw downloads live: its config's DATA_RAW, else
    data/<city>/raw."""
    raw = getattr(config, "DATA_RAW", None)
    return Path(raw) if isinstance(raw, Path) else Path(root, "data", city, "raw")


def real_stations(config):
    """place_index.map_stations: [(name, lat, lon)], or None with no file."""
    from pipeline import place_index
    return place_index.map_stations(config)


def real_fetch(city, query, cache_path, host, wait_min):
    """Ask one mirror the one query, holding that mirror's lock for as long
    as the request is out, and return the elements. Any data date is
    accepted. Raises RuntimeError when the mirror fails and SystemExit when
    the lock stays held past the wait or the run is offline."""
    from pipeline import offline, osm, place_index_fetch
    offline.refuse_if_offline(f"the area lookup of {city}",
                              "Run this script by hand, with the network.")
    lock = place_index_fetch.FetchLock(f"{city} (area lookup)", wait_min, host=host,
                                       blockers=[place_index_fetch.lock_path()])
    with lock:
        elements, _ = osm.fetch(query, cache_path, timeout=REQUEST_TIMEOUT_S,
                                retries=REQUEST_RETRIES, deadline=REQUEST_DEADLINE_S,
                                hosts=osm.pinned(host), max_age_days=None)
    return elements


def _slim(relations):
    """Relations as the report carries them: id, name and level, no tags."""
    return [{"id": r["id"], "name": r["name"], "level": r["level"]} for r in relations]


def lookup_city(city, *, root, listing, table, host, wait_min, dry_run, date,
                load_config, stations_of, fetch):
    """One city's report entry. status is "resolved", "unresolved" (a
    person's call, with the candidates), "skipped" (nothing to ask with),
    "failed" (the request) or "dry run"."""
    entry = {"city": city, "country": (listing.get(city) or (None, None))[0],
             "status": "skipped", "reason": None, "level": None, "relations": [],
             "candidates": [], "from_cache": False}
    try:
        config = load_config(city)
    except KeyboardInterrupt:
        raise
    except BaseException as exc:
        entry["reason"] = f"cannot import pipeline.{city}.config: {type(exc).__name__}: {exc}"
        return entry
    try:
        stations = stations_of(config)
    except SystemExit as exc:
        entry["reason"] = f"stations file not readable: {exc}"
        return entry
    if stations is None:
        entry["reason"] = "no stations file"
        return entry
    if not stations:
        entry["reason"] = "the stations file holds no station"
        return entry
    entry["stations"] = len(stations)
    folder = cache_dir(root, city, config)
    cached = sorted(folder.glob(CACHE_GLOB)) if folder.is_dir() else []
    query = build_query(stations)
    if cached:
        entry["from_cache"] = True
        entry["cache"] = str(cached[-1])
        try:
            elements = _read_json(cached[-1])["elements"]
        except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
            entry.update(status="failed", reason=f"the cached answer {cached[-1].name} cannot be "
                                                 f"read ({exc}): remove it to ask again")
            return entry
    elif dry_run:
        entry.update(status="dry run", query=query)
        return entry
    else:
        path = folder / CACHE_GLOB.replace("*", date)
        entry["cache"] = str(path)
        try:
            elements = fetch(city, query, path, host, wait_min)
        except KeyboardInterrupt:
            raise
        except BaseException as exc:
            entry.update(status="failed", reason=f"lookup failed on {host}: {exc}")
            return entry
    relations = relations_of(elements)
    names, codes, own = identity(config, (listing.get(city) or (None, None))[1])
    chosen, level, reason, how = choose(entry["country"], relations, table, names, codes, own)
    entry["level"] = level
    entry["candidates"] = _slim(relations)
    if chosen is None:
        entry.update(status="unresolved", reason=reason,
                     relations=_slim([r for r in relations if level is not None and r["level"] == level]))
    else:
        entry.update(status="resolved", relations=_slim(sorted(chosen, key=lambda r: r["id"])),
                     matched_by=how)
    return entry


def apply_to_plan(plan, entry, date):
    """Write one resolved city into the plan object: relations ascending and
    the note. The draft's first clause (why its relations were empty) is
    replaced; its later clauses (language, fold) are kept."""
    spec = plan["cities"][entry["city"]]
    spec["relations"] = sorted(r["id"] for r in entry["relations"])
    note = f"area from stations, admin_level {entry['level']}, lookup {date}"
    if len(spec["relations"]) > 1:
        note += f", {len(spec['relations'])} municipalities"
    rest = str(spec.get("note") or "").split("; ")[1:]
    spec["note"] = "; ".join([note] + [c for c in rest if c])


def run(plan_path, cities, *, host=None, wait_min=0, dry_run=False, report_path=None,
        stop_after=STOP_AFTER, root=ROOT, date=None, load_config=real_load,
        stations_of=real_stations, fetch=real_fetch, out=print):
    """Look up the named cities (default: every plan city with no relations)
    and return (exit code, report). The plan and the report are rewritten
    after every city, so a run that is stopped keeps what it had."""
    try:
        plan = _read_json(plan_path)
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        out(f"cannot read {plan_path}: {exc}")
        return 2, None
    if not isinstance(plan, dict) or not isinstance(plan.get("cities"), dict):
        out(f"{plan_path}: the plan must be a JSON object with a cities object")
        return 2, None
    date = date or datetime.date.today().isoformat()
    listing = city_listing(root)
    table, unread = precedents(root, listing, load_config)
    report = {"plan": str(plan_path), "host": host, "date": date, "dry_run": dry_run,
              "precedents": {c: {str(lv): sorted(names) for lv, names in sorted(levels.items())}
                             for c, levels in sorted(table.items())},
              "precedents_not_read": [{"city": c, "why": w} for c, w in unread],
              "cities": []}
    out("Precedent (country: admin level, from which built cities):")
    for country, levels in report["precedents"].items():
        out("  " + country + ": " + "; ".join(f"level {lv} ({', '.join(n)})" for lv, n in levels.items()))
    for city, why in unread:
        out(f"  not read: {city} ({why})")

    bad_names = False
    if cities:
        todo = list(dict.fromkeys(cities))
    else:
        todo = [c for c, spec in plan["cities"].items()
                if isinstance(spec, dict) and not spec.get("relations")]
    failures_in_a_row = 0
    gave_up = False

    def save():
        if report_path and not dry_run:
            _write_json(report_path, report)

    for city in todo:
        spec = plan["cities"].get(city)
        if not isinstance(spec, dict):
            bad_names = True
            entry = {"city": city, "status": "skipped", "reason": "not in the plan"}
        elif spec.get("relations"):
            entry = {"city": city, "status": "skipped",
                     "reason": "the plan already has relations for it, left alone"}
        elif gave_up:
            entry = {"city": city, "status": "not asked",
                     "reason": f"{host} failed {stop_after} lookups in a row"}
        else:
            entry = lookup_city(city, root=root, listing=listing, table=table, host=host,
                                wait_min=wait_min, dry_run=dry_run, date=date,
                                load_config=load_config, stations_of=stations_of, fetch=fetch)
            if entry["status"] == "failed" and not entry.get("from_cache"):
                failures_in_a_row += 1
                gave_up = failures_in_a_row >= stop_after
            elif not entry.get("from_cache") and entry["status"] in ("resolved", "unresolved"):
                failures_in_a_row = 0
        report["cities"].append(entry)
        if entry["status"] == "resolved":
            ids = ", ".join(f"{r['name']} ({r['id']})" for r in entry["relations"])
            out(f"{city}: resolved at admin_level {entry['level']} by {entry['matched_by']}: {ids}"
                + (" [cached answer]" if entry["from_cache"] else ""))
            if not dry_run:
                apply_to_plan(plan, entry, date)
                _write_json(plan_path, plan)
        elif entry["status"] == "dry run":
            out(f"{city}: would ask {host or 'the mirror named'} "
                f"({entry['stations']} stations):\n{entry['query']}")
        else:
            out(f"{city}: {entry['status']} ({entry['reason']})")
        save()

    counts = {}
    for entry in report["cities"]:
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
    report["summary"] = counts
    save()
    out("")
    out("Summary: " + (", ".join(f"{n} {status}" for status, n in sorted(counts.items())) or "no city"))
    if dry_run:
        out("dry run: no request was made and nothing was written")
    failed = counts.get("failed", 0) or counts.get("not asked", 0) or bad_names
    return (1 if failed else 0), report


def main(argv=None, **effects):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan", metavar="PLAN_JSON")
    ap.add_argument("city", nargs="*", metavar="CITY",
                    help="default: every city of the plan with no relations")
    ap.add_argument("--host", metavar="MIRROR", choices=MIRRORS,
                    help="the one Overpass mirror asked: " + " or ".join(MIRRORS))
    ap.add_argument("--wait", type=int, default=0, metavar="MIN",
                    help="minutes to wait for the mirror's lock before a city counts as failed")
    ap.add_argument("--report", metavar="FILE", help="write the JSON report here")
    ap.add_argument("--stop-after", type=int, default=STOP_AFTER, metavar="N",
                    help=f"request failures in a row before the rest are left unasked (default {STOP_AFTER})")
    ap.add_argument("--dry-run", action="store_true",
                    help="print each city's query; no request, nothing written")
    args = ap.parse_args(argv)
    if not args.dry_run and not args.host:
        ap.error("--host MIRROR is required: a lookup is pinned to one mirror")
    if args.stop_after < 1:
        ap.error("--stop-after must be 1 or more")
    code, _ = run(args.plan, args.city, host=args.host, wait_min=args.wait,
                  dry_run=args.dry_run, report_path=args.report,
                  stop_after=args.stop_after, **effects)
    return code


def selftest():
    import os
    import runpy
    import tempfile
    import types

    cases = []

    def report(label, ok):
        cases.append((label, bool(ok)))
        print(f"  {'ok ' if ok else 'BAD'} {label}")

    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))

    def rel(rel_id, level, name, **tags):
        return {"type": "relation", "id": rel_id,
                "tags": dict({"boundary": "administrative", "admin_level": str(level),
                              "name": name}, **tags)}

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        listing_rows = []

        def city(folder, country, name, *, built=None, extra="", stations=True):
            """One city of the temporary tree. built is {relation id: level}
            for a city that already has search."""
            page = f"pages/{len(listing_rows) + 1}_{folder}_Heatmap.py"
            listing_rows.append({"name": name, "page": page, "country": country})
            write(root / "app" / page, f"from pipeline.{folder}.config import HEATMAP_HTML\n")
            raw = root / "data" / folder / "raw"
            text = ("from pathlib import Path\n"
                    f"DATA_RAW = Path({str(raw)!r})\n"
                    f"STATIONS_CSV = Path({str(root / 'data' / folder / 'stations.csv')!r})\n" + extra)
            if stations:
                write(root / "data" / folder / "stations.csv",
                      "station,lat,lon\nOne,10.00001,20.00001\nOne again,10.000012,20.000011\n"
                      "Two,10.5,20.5\n")
            if built is not None:
                ids = ",".join(str(AREA_BASE + r) for r in built)
                text += (f'PLACE_AREA = "(id:{ids})"\n'
                         'PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-01-01.json"\n')
                write(raw / "osm_place_outline_v1.json",
                      json.dumps({"elements": [rel(r, lv, f"R{r}") for r, lv in built.items()]}))
            write(root / "pipeline" / folder / "config.py", text)

        city("a1", "Alphaland", "A One", built={11: 8})
        city("b1", "Betaland", "B One", built={21: 4})
        city("b2", "Betaland", "B Two", built={22: 6, 23: 6})
        city("a2", "Alphaland", "A Two")
        city("b3", "Betaland", "B Three")
        city("g1", "Gammaland", "G One")
        city("a3", "Alphaland", "A Three", extra='MUNICIPALITY = "Somewhere Else"\n')
        city("a4", "Alphaland", "A Four")
        city("a5", "Alphaland", "A Five")
        city("a6", "Alphaland", "A Six", stations=False)
        city("a7", "Alphaland", "A Seven (Regional)", extra='BOUNDARY_COMMUNE_CODE = "12345"\n')
        city("a8", "Alphaland", "A Eight")
        write(root / "app" / "cities.py", "CITIES = " + json.dumps(listing_rows, indent=4) + "\n")

        def load(folder):
            return types.SimpleNamespace(**runpy.run_path(str(root / "pipeline" / folder / "config.py")))

        country_rel = rel(1, 2, "Alphaland")
        answers = {
            "a2": [country_rel, rel(102, 8, "A Two"), rel(101, 8, "Next Town"), rel(150, 4, "A State")],
            "b3": [rel(1, 2, "Betaland"), rel(301, 4, "B Three"), rel(302, 6, "B Three County")],
            "g1": [rel(401, 8, "G One")],
            "a3": [country_rel, rel(501, 8, "A Three Town")],
            "a4": [country_rel] + [rel(600 + i, 8, f"A Four {i}") for i in range(MAX_AUTO_RELATIONS + 1)],
            "a5": [country_rel, rel(701, 6, "A Five County")],
            "a7": [country_rel, rel(802, 8, "Renamed", **{"ref:INSEE": "12345"}), rel(801, 8, "Other")],
            "a8": [country_rel, rel(901, 8, "Another Place")],
        }

        class Fetch:
            def __init__(self, failing=()):
                self.calls, self.failing = [], set(failing)

            def __call__(self, name, query, cache_path, host, wait_min):
                self.calls.append((name, host, query))
                if name in self.failing:
                    raise RuntimeError("the pinned Overpass mirror failed")
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_bytes(json.dumps({"elements": answers[name]}).encode("utf-8"))
                return answers[name]

        def plan_file(names, draft=True):
            path = root / "plan.json"
            plan = {"date": "2026-10-13", "cities": {
                n: {"relations": [], "languages": ["en"], "fold": None,
                    "note": "no boundary relation in the config: look it up; language from LOCAL_LANG"}
                for n in names}}
            if draft:
                plan = dict({"draft": True}, **plan)
            _write_json(path, plan)
            return path

        def go(names, cities=(), fetch=None, **kw):
            lines = []
            fetch = fetch if fetch is not None else Fetch()
            code, rep = run(plan_file(names) if names is not None else root / "plan.json",
                            list(cities), host=kw.pop("host", MIRRORS[1]), root=root,
                            date="2026-10-13", load_config=load, fetch=fetch,
                            out=lines.append, **kw)
            by = {e["city"]: e for e in (rep or {}).get("cities", [])}
            return code, by, "\n".join(lines), fetch

        listing = city_listing(root)
        table, unread = precedents(root, listing, load)
        report("the precedent table groups the built cities' admin levels by country",
               table == {"Alphaland": {8: ["a1"]}, "Betaland": {4: ["b1"], 6: ["b2"]}} and not unread)

        everyone = ["a2", "b3", "g1", "a3", "a4", "a5", "a6", "a7", "a8"]
        report_path = root / "report.json"
        code, by, text, fetch = go(everyone, report_path=report_path)
        plan = _read_json(root / "plan.json")
        report("a country with one precedent level resolves, relations ascending, with the note",
               by["a2"]["status"] == "resolved"
               and plan["cities"]["a2"]["relations"] == [101, 102]
               and plan["cities"]["a2"]["note"] == ("area from stations, admin_level 8, lookup "
                                                    "2026-10-13, 2 municipalities; language from LOCAL_LANG"))
        report("a country whose built cities used two levels is left for a person, with candidates",
               by["b3"]["status"] == "unresolved" and "several admin levels" in by["b3"]["reason"]
               and plan["cities"]["b3"]["relations"] == []
               and {c["id"] for c in by["b3"]["candidates"]} == {1, 301, 302})
        report("a country with no built city is left for a person",
               by["g1"]["status"] == "unresolved" and "no built city in Gammaland" in by["g1"]["reason"]
               and plan["cities"]["g1"]["relations"] == [])
        report("a config naming another municipality is a name mismatch, not filled",
               by["a3"]["status"] == "unresolved" and "name mismatch" in by["a3"]["reason"]
               and "Somewhere Else" in by["a3"]["reason"] and plan["cities"]["a3"]["relations"] == [])
        report("a city whose own name no relation carries is a name mismatch too",
               by["a8"]["status"] == "unresolved" and "name mismatch" in by["a8"]["reason"])
        report("more relations than MAX_AUTO_RELATIONS (25) are not filled",
               MAX_AUTO_RELATIONS == 25 and by["a4"]["status"] == "unresolved"
               and "26 relations at admin_level 8, more than the 25" in by["a4"]["reason"]
               and plan["cities"]["a4"]["relations"] == [])
        report("no relation at the precedent level is said, with what did come back",
               by["a5"]["status"] == "unresolved" and "no relation at admin_level 8" in by["a5"]["reason"]
               and by["a5"]["candidates"][0]["id"] == 701)
        report("a city with no stations file is skipped and never asked",
               by["a6"]["status"] == "skipped" and by["a6"]["reason"] == "no stations file"
               and "a6" not in [c[0] for c in fetch.calls])
        report("an official code ties a renamed relation to its city",
               by["a7"]["status"] == "resolved" and by["a7"]["matched_by"] == "ref:INSEE"
               and plan["cities"]["a7"]["relations"] == [801, 802])
        report("the draft marker is never removed, and unresolved entries are untouched",
               plan.get("draft") is True
               and plan["cities"]["g1"]["note"].startswith("no boundary relation"))
        saved = _read_json(report_path)
        report("the report lists every city, the precedent table and no tags, LF only",
               [e["city"] for e in saved["cities"]] == everyone
               and saved["precedents"]["Betaland"] == {"4": ["b1"], "6": ["b2"]}
               and "tags" not in json.dumps(saved) and b"\r" not in report_path.read_bytes()
               and b"\r" not in (root / "plan.json").read_bytes())
        report("unresolved cities are answers, not failures: exit 0", code == 0)
        report("every request is pinned to the mirror named",
               fetch.calls and all(h == MIRRORS[1] for _, h, _ in fetch.calls))

        code, by, text, again = go(everyone)
        report("a city with a cached answer is never asked again, and resolves the same",
               again.calls == [] and by["a2"]["status"] == "resolved" and by["a2"]["from_cache"]
               and by["b3"]["status"] == "unresolved")

        for name in everyone:
            for old in (root / "data" / name / "raw").glob(CACHE_GLOB):
                old.unlink()
        plan_file(everyone)
        before = (root / "plan.json").read_bytes()
        code, by, text, dry = go(None, dry_run=True, host=None)
        report("a dry run prints each query, asks nothing and writes nothing",
               dry.calls == [] and by["a2"]["status"] == "dry run" and "is_in(10.00001,20.00001)" in text
               and (root / "plan.json").read_bytes() == before
               and not any(list((root / "data" / n / "raw").glob(CACHE_GLOB)) for n in everyone))

        code, by, text, dead = go(["a2", "a3", "a4", "a5", "a7"],
                                  fetch=Fetch(failing=("a2", "a3", "a4", "a5", "a7")))
        report("a mirror that fails three lookups in a row is given up on, the rest not asked",
               code == 1 and [c[0] for c in dead.calls] == ["a2", "a3", "a4"]
               and by["a4"]["status"] == "failed" and by["a5"]["status"] == "not asked"
               and by["a7"]["status"] == "not asked")

        code, by, text, _ = go(["a2"], cities=["a2", "nowhere"])
        report("a named city that is not in the plan is said and makes the exit non-zero",
               code == 1 and by["nowhere"]["reason"] == "not in the plan"
               and by["a2"]["status"] == "resolved")
        code, by, text, held = go(None, cities=["a2"])
        report("an entry that already has relations is left alone",
               by["a2"]["status"] == "skipped" and held.calls == [])

        lines = []
        report("a plan that cannot be read stops the run with exit 2",
               run(root / "absent.json", [], host=MIRRORS[0], root=root, out=lines.append)[0] == 2)

    query = build_query([("A", 1.0, 2.0), ("A again", 1.000001, 2.000001), ("B", 3.0, 4.0)])
    report("the query asks each distinct station point once, tags only, no geometry",
           query.count("is_in(") == 2 and query.rstrip().endswith("out tags;")
           and "geom" not in query and 'rel(pivot.a)["boundary"="administrative"];' in query
           and query.startswith(f"[out:json][timeout:{QUERY_TIMEOUT_S}];"))

    osm_text = (ROOT / "pipeline" / "osm.py").read_bytes().decode("utf-8")
    block = osm_text.split("OVERPASS_HOSTS = (", 1)[1].split(")", 1)[0]
    report("MIRRORS is pipeline/osm.py's host list, in its order",
           tuple(re.findall(r"https://([^/]+)/", block)) == MIRRORS)

    # The real fetch, with the request itself stood in for: the lock is held
    # while the mirror is asked, the fetch is pinned and any data age passes.
    from pipeline import offline, osm, place_index_fetch
    with tempfile.TemporaryDirectory() as tmp:
        seen = {}

        def stand_in(query, cache_path, **kw):
            seen.update(kw, lock=place_index_fetch.lock_path(MIRRORS[1]).exists())
            return [{"type": "relation", "id": 1}], MIRRORS[1]

        kept = {k: os.environ.get(k) for k in ("PLACE_FETCH_LOCK_DIR", offline.NO_NETWORK_ENV)}
        real = osm.fetch
        os.environ["PLACE_FETCH_LOCK_DIR"] = tmp
        os.environ.pop(offline.NO_NETWORK_ENV, None)
        osm.fetch = stand_in
        try:
            got = real_fetch("x", "q", Path(tmp) / "c.json", MIRRORS[1], 0)
            released = not place_index_fetch.lock_path(MIRRORS[1]).exists()
            os.environ[offline.NO_NETWORK_ENV] = "1"
            try:
                real_fetch("x", "q", Path(tmp) / "c.json", MIRRORS[1], 0)
                refused = False
            except SystemExit:
                refused = True
        finally:
            osm.fetch = real
            for key, value in kept.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        report("the real fetch holds the mirror's lock while it asks, pinned, any data age",
               got == [{"type": "relation", "id": 1}] and seen.get("lock") is True and released
               and seen.get("hosts") == osm.pinned(MIRRORS[1]) and seen.get("max_age_days") is None)
        report("the real fetch refuses to ask when the run is offline", refused)

    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
