"""Place search: every map with a search box is backed by a current index,
its page names only the languages measured for it, and the index carries
nothing but OpenStreetMap's places. Run it; it fails on any of these.

    python scripts/check_place_search.py [--selftest]

WHY A CHECK (owner, 2026-10-07)
-------------------------------
The page's search bullet says which languages a city's search answers in.
Written by hand it would say "English or Japanese" on a Brussels page, so the
index step measures each language's share of the places
(pipeline/place_index.py, LANGUAGES) and the page reads the result
(app/components.search_languages). This re-reads both ends:

  A. A map whose HTML carries the search box has its index
     (app/static/places/<slug>.json) and summary (outputs/<slug>/
     place_search.json), and the URL baked into the map carries the index's
     CURRENT hash: a rebuilt index under an old URL is a map left stale, and a
     browser keeps the old file (the Kyoto pilot showed a removed condominium).
  B. The summary's languages are the index's, and its list follows the rule:
     English first, then the local languages, each at LIST_SHARE or more; a
     declared local language under LOCAL_MIN fails.
  C. The page that embeds the map passes search=<slug> to render_map_help, so
     the bullet is present, and no page writes the bullet itself.
  E. No business or home slipped through: every index row carrying a
     place_index.LEAK_WORDS word in English or a local language is named in
     the city's config.PLACE_REVIEWED with why it is a place, and every
     reviewed name still occurs (a stale entry is a list nobody reads). Kyoto
     found a hotel's footpath, a supermarket's car park and "private land"
     before the minor-way rule; one ruin is reviewed.
     A row kept by an owner's ruling that carries no leak word is recorded in
     config.PLACE_RULED_KEPT ({OSM id or street name: why}; the big review,
     2026-10-13) and held here too: every entry gives its why, names a row of
     the index (a place by its id in the id side file, a street by its name)
     and is not in PLACE_DROPPED. A ruled keep a later rule has taken fails by
     name instead of going unnoticed.
  D. ODbL: the index holds only the fields place_index writes (6 per row, the
     known top-level keys), its licence object names ODbL and the OSM credit,
     LICENSE carves app/static/places/ out, and docs/data_sources.md has the
     row. A field from any other source would bring that source under ODbL
     (4.4(d)).
  F. No name is a placeholder, an error value or a number alone ("Untitled",
     "#N/A", "47"; place_index.junk_name), so none is ever suggested.
  G. Every visitable former home kept against the home rule
     (config.PLACE_VISITABLE) carries its access verdict, an https source
     and the date it was checked, and was checked within
     place_index.VISITABLE_MAX_DAYS: a lapsed entry fails until re-checked
     or removed (owner, 2026-10-08: visitable only, kept up to date).
  H. The index reaches the whole map (owner, 2026-10-12): every station the
     map draws has an indexed place within place_index.COVER_KM. Mexico
     City's index landed cut to the city proper under a regional map, so 11
     stations on the map could not be found. Read from the city's processed
     stations, so on a machine without data/ it is reported as not checked,
     never as passed. KNOWN_GAPS holds a dated defect and may only shrink.
  I. The map asks for its index under the app's own path (owner's London
     report, 2026-10-12): the deployed app is served under /~/+/, and a map
     asking the host's root never loaded its index, so the live search
     answered with stations and lines only while every local test passed.
     The map's script must take the prefix from the page (getIndex) and must
     not fetch the bare URL. A wave rendered from an older map_common fails.
  J. The street lines file (app/static/places/streets/, owner 2026-10-13: a
     picked street shows its whole length) is THIS index's: named in the
     index under its current hash, its rows ascending and each a street row,
     one list of lines a row, and every point of a line inside its street
     row's own extent (STREET_PAD_DEG wider: the simplification and the
     rounding). A line outside its row's extent is a line drawn on another
     street. It carries the index's licence object.
  A and D apply to the intersections file too (app/static/places/crossings/,
     since 2026-10-08): the index names it under its current hash, and it
     holds only [lat, lon, street, street] rows and the index's licence.
"""
import hashlib
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import place_index  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# H: a city whose index is known not to reach its whole map, with the date
# and the reason. A dated defect, not a pass; an entry whose city has no gap
# left fails, so the list only shrinks.
# Empty since Mexico City's index was rebuilt over Tlalnepantla de Baz as
# well, with the tram rescope's stations, 2026-10-13 (it was emptied once
# before, 2026-10-12, when the index first reached the regional map).
KNOWN_GAPS = {}


def quiet_of(slug):
    """config.PLACE_QUIET_STATIONS of a city, {} when it has none."""
    try:
        return getattr(importlib.import_module(f"pipeline.{slug}.config"), "PLACE_QUIET_STATIONS", {})
    except ImportError:
        return {}


def check_coverage(slug, index, stations, known=None, lines=None, quiet=None):
    """H for one city: problems, given its index, its map's stations and
    its streets' polylines (place_index.decode_lines), which cover a station
    a long street runs past though the street's one row point is far off."""
    known = KNOWN_GAPS if known is None else known
    bare = place_index.uncovered_stations(index["rows"], stations, lines=lines)
    # A station the city lists as quiet is accounted for; a listed one that
    # is covered after all, or is not on the map, fails by name.
    bare, wrong = place_index.quiet_stations(quiet_of(slug) if quiet is None else quiet, stations, bare)
    if wrong:
        return [f"H: {w}" for w in wrong]
    if bare and slug not in known:
        return [f"H: {len(bare)} map station(s) with no indexed place within {place_index.COVER_KM:g} km "
                f"({', '.join(bare[:6])}): config.PLACE_AREA does not cover the whole map"]
    if not bare and slug in known:
        return ["H: listed in KNOWN_GAPS but every station is covered: delete the entry"]
    return []


TOP_KEYS = {"license", "schema", "city", "languages", "fold", "kinds", "rows", "crossings", "streets",
            "area"}
CROSS_KEYS = {"license", "schema", "city", "part_of", "rows"}
STREET_KEYS = {"license", "schema", "city", "part_of", "scale", "rows", "lines"}
STREET_RE = re.compile(r"^/app/static/places/streets/([a-z0-9_]+)[.]json[?]v=([0-9a-f]+)$")
# About 30 m of latitude: STREET_SIMPLIFY_M and the 5-decimal rounding of
# both the line and the row's extent, with room.
STREET_PAD_DEG = 0.0003
URL_RE = re.compile(r"/app/static/places/([a-z0-9_]+)[.]json[?]v=([0-9a-f]+)")
CROSS_RE = re.compile(r"^/app/static/places/crossings/([a-z0-9_]+)[.]json[?]v=([0-9a-f]+)$")
BULLET = "never leaves your browser"


def rule(langs):
    """The page's list, recomputed from the coverage: the rule in one place."""
    order = list(dict.fromkeys(["en", *langs["local"]]))
    return [place_index.LANGUAGE_NAMES[c] for c in order
            if langs["coverage"].get(c, 0) >= place_index.LIST_SHARE]


def check_ids(slug, index_bytes, index, ids_path):
    """The id side file (outputs/<slug>/place_ids.json) describes THIS index:
    its sha256 is the index file's, its rows are in range, ascending, and
    never a street, and each has one OSM id of the form type/number."""
    import hashlib
    import re
    if not ids_path.is_file():
        return [f"I: no id side file {ids_path.name}: run the index step"]
    ids = json.loads(ids_path.read_text(encoding="utf-8"))
    problems = []
    if ids.get("index_sha256") != hashlib.sha256(index_bytes).hexdigest():
        problems.append("I: the id side file names another build of the index: run the index step")
    rows, osm = ids.get("rows") or [], ids.get("osm") or []
    if len(rows) != len(osm) or rows != sorted(set(rows)):
        problems.append("I: the id side file's rows and ids are not two lists of one length, rows ascending")
    street = index["kinds"].index("street") if "street" in index["kinds"] else -1
    if any(not 0 <= i < len(index["rows"]) or index["rows"][i][0] == street for i in rows):
        problems.append("I: the id side file names a row out of range or a street")
    if any(not re.fullmatch(r"(node|way|relation)/[0-9]+", str(o)) for o in osm):
        problems.append("I: the id side file holds something that is not an OSM type/id")
    return problems


def check_index(slug, index, summary):
    problems = []
    if set(index) != TOP_KEYS:
        problems.append(f"index keys {sorted(index)} are not {sorted(TOP_KEYS)}")
    lic = index.get("license", {})
    if "opendatacommons.org/licenses/odbl" not in lic.get("url", "") or \
            "OpenStreetMap contributors" not in lic.get("attribution", ""):
        problems.append("licence object lacks the ODbL link or the OSM credit")
    bad = [r for r in index.get("rows", []) if len(r) != 6]
    if bad:
        problems.append(f"{len(bad)} row(s) not of 6 fields, e.g. {bad[0][:7]}")
    langs = index.get("languages", {})
    if summary is not None and summary.get("languages") != langs:
        problems.append("summary languages differ from the index's (re-run the index step)")
    if langs.get("list_share") != place_index.LIST_SHARE:
        problems.append(f"built at list_share {langs.get('list_share')}, the rule is {place_index.LIST_SHARE}")
    short = [c for c in langs.get("local", []) if langs["coverage"].get(c, 0) < place_index.LOCAL_MIN]
    if short:
        problems.append(f"local language(s) {short} under {place_index.LOCAL_MIN:.0%}: {langs['coverage']}")
    if langs and langs.get("listed") != rule(langs):
        problems.append(f"listed {langs.get('listed')} but the rule gives {rule(langs)}")
    if langs and not langs.get("listed"):
        problems.append("no language reaches the bar: the page could name none")
    return problems


def check_crossings(slug, index):
    """A and D for the intersections file (owner, 2026-10-08: a second file,
    fetched only when a search asks for an intersection): the index names it
    under its current hash, it holds only [lat, lon, street, street] rows
    whose streets are street rows of the index, and it carries the index's
    licence object, since it can be downloaded on its own."""
    m = CROSS_RE.match(str(index.get("crossings", "")))
    if not m or m.group(1) != slug:
        return ["A: the index names no crossings file of its own"]
    path = place_index.crossings_path(slug)
    if not path.exists():
        return [f"A: no {path.relative_to(ROOT).as_posix()}"]
    if hashlib.sha256(path.read_bytes()).hexdigest()[:len(m.group(2))] != m.group(2):
        return ["A: the index's crossings hash is stale (re-run the index step)"]
    cx = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    if set(cx) != CROSS_KEYS:
        problems.append(f"D: crossings keys {sorted(cx)} are not {sorted(CROSS_KEYS)}")
    if cx.get("license") != index.get("license"):
        problems.append("D: the crossings file's licence object differs from the index's")
    street = index.get("kinds", []).index("street") if "street" in index.get("kinds", []) else None
    rows = index.get("rows", [])
    bad = [r for r in cx.get("rows", []) if len(r) != 4 or not all(
        isinstance(i, int) and 0 <= i < len(rows) and rows[i][0] == street for i in r[2:4])]
    if bad:
        problems.append(f"D: {len(bad)} crossing row(s) not [lat, lon, street, street], e.g. {bad[0]}")
    return problems


def check_streets(slug, index, path=None):
    """J: the street lines file named by the index is this index's."""
    m = STREET_RE.match(str(index.get("streets", "")))
    if not m or m.group(1) != slug:
        return ["J: the index names no street lines file of its own"]
    path = path or place_index.streets_path(slug)
    if not path.exists():
        return [f"J: no {path.name} under app/static/places/streets/: run the index step"]
    if hashlib.sha256(path.read_bytes()).hexdigest()[:len(m.group(2))] != m.group(2):
        return ["J: the index's street lines hash is stale (re-run the index step)"]
    return street_problems(index, json.loads(path.read_text(encoding="utf-8")))


def street_problems(index, st):
    problems = []
    if set(st) != STREET_KEYS:
        problems.append(f"J: street lines keys {sorted(st)} are not {sorted(STREET_KEYS)}")
    if st.get("license") != index.get("license"):
        problems.append("J: the street lines file's licence object differs from the index's")
    rows, lines, k = st.get("rows") or [], st.get("lines") or [], st.get("scale") or 0
    if len(rows) != len(lines) or rows != sorted(set(rows)) or not k:
        return problems + ["J: rows and lines are not two lists of one length, rows ascending, with a scale"]
    street = index["kinds"].index("street") if "street" in index["kinds"] else -1
    irows = index["rows"]
    if any(not 0 <= i < len(irows) or irows[i][0] != street for i in rows):
        return problems + ["J: the street lines file names a row out of range or not a street"]
    off = 0
    for i, ls in zip(rows, lines):
        box = irows[i][5]
        ok = bool(ls) and bool(box)
        for a in ls if ok else ():
            if len(a) < 4 or len(a) % 2 or not all(isinstance(v, int) for v in a):
                ok = False
                break
            la, lo = a[0], a[1]
            pts = [(la, lo)]
            for j in range(2, len(a), 2):
                la, lo = la + a[j], lo + a[j + 1]
                pts.append((la, lo))
            if any(not (box[0] - STREET_PAD_DEG <= y / k <= box[2] + STREET_PAD_DEG
                        and box[1] - STREET_PAD_DEG <= x / k <= box[3] + STREET_PAD_DEG) for y, x in pts):
                ok = False
                break
        off += not ok
    if off:
        problems.append(f"J: {off} street(s) with a line that is malformed or outside the street's own extent")
    return problems


def check_junk(index):
    """F: no name in the index is a placeholder, an error value or a number
    alone (place_index.junk_name; owner, 2026-10-08), so none can be
    suggested."""
    bad = sorted({n for r in index.get("rows", []) for n in [r[3]] + (r[4].split("|") if r[4] else [])
                  if place_index.junk_name(n)})
    return [f"F: {len(bad)} junk name(s) in the index, e.g. {bad[:3]}"] if bad else []


def check_leaks(slug, index, reviewed=None):
    """E: leak words, against the city's reviewed list."""
    if reviewed is None:
        import importlib
        try:
            reviewed = getattr(importlib.import_module(f"pipeline.{slug}.config"), "PLACE_REVIEWED", {})
        except ImportError:
            return [f"E: no pipeline/{slug}/config.py to hold PLACE_REVIEWED"]
    hits = place_index.leak_hits(index, index.get("languages", {}).get("local", []))
    problems = [f"E: {name!r} carries {word!r}: drop it by a rule in place_index.py, or review it "
                f"in config.PLACE_REVIEWED with why it is a place" for name, word in hits if name not in reviewed]
    # A review is stale when its name carries no leak word at all. One whose
    # row the test no longer fires on (a junction, a French mansion, a street
    # under an allowed word: place_index.leak_hits, the sixth pass,
    # 2026-10-13) is no longer needed and is no failure: it is left to be
    # removed by hand.
    hit_names = {name for name, _ in place_index.leak_hits(
        index, index.get("languages", {}).get("local", []), exempt=False)}
    problems += [f"E: PLACE_REVIEWED names {name!r}, which no longer carries a leak word: remove it"
                 for name in reviewed if name not in hit_names]
    return problems


def check_ruled_kept(slug, index, ids=None, ruled=None, dropped=None):
    """E: every entry of config.PLACE_RULED_KEPT (a row kept by an owner's
    ruling, with no leak word to put it in PLACE_REVIEWED) is still a row of
    the index. A key of the form type/number is an OSM id and must be in the
    id side file (`ids`, outputs/<slug>/place_ids.json's "osm" list, which
    check I holds to this index); any other key is a name and must be a
    row's name or one of its alternate names. The record shields nothing
    (PLACE_KEPT does that): it fails when a later rule or drop takes the row."""
    if ruled is None:
        try:
            config = importlib.import_module(f"pipeline.{slug}.config")
        except ImportError:
            return []
        ruled = getattr(config, "PLACE_RULED_KEPT", {})
        dropped = getattr(config, "PLACE_DROPPED", {})
    if not ruled:
        return []
    if not isinstance(ruled, dict):
        return ["E: PLACE_RULED_KEPT is not a dict of {OSM id or street name: why}"]
    if ids is None:
        ipath = place_index.ids_path(slug)
        ids = json.loads(ipath.read_text(encoding="utf-8")).get("osm", []) if ipath.is_file() else []
    ids = set(ids)
    names = {n for r in index.get("rows", []) for n in [r[3]] + (r[4].split("|") if r[4] else [])}
    problems = []
    for key, why in ruled.items():
        if not (isinstance(why, str) and why.strip()):
            problems.append(f"E: PLACE_RULED_KEPT gives no why for {key!r}")
        if key in (dropped or {}):
            problems.append(f"E: {key!r} is in PLACE_RULED_KEPT and in PLACE_DROPPED: one of them is wrong")
        elif re.fullmatch(r"(node|way|relation)/[0-9]+", str(key)):
            if key not in ids:
                problems.append(f"E: PLACE_RULED_KEPT names {key}, which is no row of the index (a rule took it, "
                                f"or it joined another row): keep it by id in PLACE_KEPT, or remove the entry")
        elif key not in names:
            problems.append(f"E: PLACE_RULED_KEPT names {key!r}, which is no row of the index: remove the entry, "
                            f"or put the ruling back")
    return problems


def check_visitable(slug, visitable=None, today=None):
    """G: every visitable former home (config.PLACE_VISITABLE) is sound and
    checked within place_index.VISITABLE_MAX_DAYS of today (owner, 2026-10-08:
    "Must make sure info is up-to-date on visitation eligibility"). A lapsed
    entry fails until its visiting status is checked again from its source and
    the date renewed, or the entry is removed (its home then leaves the index)."""
    import datetime
    if visitable is None:
        import importlib
        try:
            visitable = getattr(importlib.import_module(f"pipeline.{slug}.config"), "PLACE_VISITABLE", {})
        except ImportError:
            return []
    today = today or datetime.date.today().isoformat()
    problems = [f"G: {m}" for m in place_index.visitable_problems(visitable)]
    for k, v in visitable.items():
        try:
            age = place_index._days(v["checked"], today)
        except (KeyError, TypeError, ValueError):
            continue
        if age > place_index.VISITABLE_MAX_DAYS:
            problems.append(f"G: {k} ({v.get('name')}) last checked {v['checked']}, {age} days ago: check its "
                            f"visiting status again at its source and renew 'checked', or remove the entry")
    return problems


def check_fetch_path(text):
    """I: the search script reads the app's path prefix and never fetches the
    index or the intersections file by its bare root URL."""
    out = []
    if "function getIndex" not in text or "window.parent.location.pathname" not in text:
        out.append("I: the map does not take the app's path prefix for its index (re-render from "
                   "the current pipeline/map_common.py)")
    if "fetch(URL," in text or "fetch(crossURL," in text:
        out.append("I: the map fetches its index at the host's root, which the deployed app is not at")
    return out


def pages_by_slug():
    out = {}
    for page in sorted((ROOT / "app" / "pages").glob("*.py")):
        text = page.read_text(encoding="utf-8")
        for slug in re.findall(r"from pipeline[.]([a-z0-9_]+)[.]config import", text):
            out.setdefault(slug, []).append((page, text))
    return out


def main():
    problems = {}
    unread = []
    indexes = sorted((ROOT / "app" / "static" / "places").glob("*.json"))
    pages = pages_by_slug()
    searched = set()
    for html in sorted((ROOT / "outputs").glob("*/heatmap.html")):
        text = html.read_text(encoding="utf-8")
        if "hm-search-input" not in text:
            continue
        slug = html.parent.name
        searched.add(slug)
        p = problems.setdefault(slug, [])
        m = URL_RE.search(text)
        path = place_index.index_path(slug)
        if not m or m.group(1) != slug:
            p.append("A: the map carries a search box but no hashed index URL of its own")
        elif not path.exists():
            p.append(f"A: no index at {path.relative_to(ROOT)}")
        elif hashlib.sha256(path.read_bytes()).hexdigest()[:len(m.group(2))] != m.group(2):
            p.append("A: the map's index URL is stale (re-render the map after the index step)")
        if not place_index.summary_path(slug).exists():
            p.append("A: no outputs/<slug>/place_search.json")
        p += check_fetch_path(text)
        page_texts = pages.get(slug, [])
        if not any(f"search='{slug}'" in t or f'search="{slug}"' in t for _, t in page_texts):
            p.append("C: the city's page does not pass search=<slug> to render_map_help")
    for path in indexes:
        slug = path.stem
        p = problems.setdefault(slug, [])
        if slug not in searched:
            p.append("A: an index no map uses (render the map with place_index_url, or remove it)")
        index = json.loads(path.read_text(encoding="utf-8"))
        sp = place_index.summary_path(slug)
        summary = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else None
        p += check_index(slug, index, summary)
        p += check_ids(slug, path.read_bytes(), index, place_index.ids_path(slug))
        p += check_crossings(slug, index)
        p += check_streets(slug, index)
        p += check_junk(index)
        p += check_leaks(slug, index)
        p += check_ruled_kept(slug, index)
        p += check_visitable(slug)
        stations = place_index.map_stations(importlib.import_module(f"pipeline.{slug}.config"))
        if stations is None:
            unread.append(slug)
        else:
            stpath = place_index.streets_path(slug)
            lines = (place_index.decode_lines(json.loads(stpath.read_text(encoding="utf-8")).get("lines", []))
                     if stpath.exists() else None)
            p += check_coverage(slug, index, stations, lines=lines)
    for page in sorted((ROOT / "app" / "pages").glob("*.py")):
        if BULLET in page.read_text(encoding="utf-8"):
            problems.setdefault(page.name, []).append(
                "C: writes the search bullet itself; it comes from render_map_help")
    if indexes:
        if "app/static/places/" not in (ROOT / "LICENSE").read_text(encoding="utf-8"):
            problems.setdefault("LICENSE", []).append("D: no ODbL carve-out for app/static/places/")
        if "Place search index" not in (ROOT / "docs" / "data_sources.md").read_text(encoding="utf-8"):
            problems.setdefault("docs/data_sources.md", []).append("D: no 'Place search index' row")

    failed = {k: v for k, v in problems.items() if v}
    for slug in sorted(problems):
        if problems[slug]:
            for line in problems[slug]:
                print(f"  FAIL {slug:14} {line}")
        elif slug in searched:
            summary = json.loads(place_index.summary_path(slug).read_text(encoding="utf-8"))
            print(f"  OK   {slug:14} {summary['places']:,} places; the page names "
                  f"{', '.join(summary['languages']['listed'])} {summary['languages']['coverage']}")
    for slug in sorted(KNOWN_GAPS):
        print(f"  GAP  {slug:14} H: {KNOWN_GAPS[slug]}")
    if unread:
        print(f"  H NOT CHECKED for {len(unread)} city(ies), no processed stations on this machine: "
              f"{', '.join(unread)}")
    if failed:
        print(f"\n{len(failed)} place-search problem(s).")
        return 1
    print(f"\nOK - {len(searched)} map(s) with place search, each current, its languages measured.")
    return 0


def selftest():
    good = {"local": ["fr", "nl"], "coverage": {"en": 0.2, "fr": 0.95, "nl": 0.93},
            "list_share": place_index.LIST_SHARE, "listed": ["French", "Dutch"]}
    cases = [
        ("bilingual city lists both, not English", good, 0),
        ("hand-written English slipped in", dict(good, listed=["English", "French", "Dutch"]), 1),
        ("a local language under the floor", dict(good, coverage={"en": 0.2, "fr": 0.95, "nl": 0.5}), 1),
    ]
    base = {"license": {"url": "https://opendatacommons.org/licenses/odbl/1-0/",
                        "attribution": "© OpenStreetMap contributors"},
            "city": "X", "fold": None, "kinds": [], "rows": [[0, 1, 2, "a", "", 0]],
            "crossings": "/app/static/places/crossings/x.json?v=0", "schema": 1,
            "streets": "/app/static/places/streets/x.json?v=0",
            "area": {"names": ["X"], "outline": [[1, 2, 1, 3, 2, 3, 1, 2]]}}
    ok = 0
    for label, langs, want in cases:
        got = len(check_index("x", dict(base, languages=langs), None))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    extra = dict(base, languages=good, rows=[[0, 1, 2, "a", "", 0, "register"]])
    got = len(check_index("x", extra, None))
    ok += got == 1
    print(f"  {'ok ' if got == 1 else 'BAD'} a 7th field from another source: {got} problem(s)")
    ja = {"local": ["ja"], "coverage": {"en": 0.7, "ja": 0.99}, "list_share": 0.5, "listed": []}
    leak_cases = [
        ("a hotel's footpath", [[0, 1, 2, "リッチモンドホテル", "", 0]], {}, 1),
        ("a shopping street is a place", [[0, 1, 2, "古川町商店街", "", 0]], {}, 0),
        ("a reviewed ruin", [[0, 1, 2, "愛宕山ホテル跡", "", 0]], {"愛宕山ホテル跡": "a ruin"}, 0),
        ("a stale review", [[0, 1, 2, "三条通", "", 0]], {"愛宕山ホテル跡": "a ruin"}, 1),
        ("an English alias", [[0, 1, 2, "某", "Sunrise Apartments", 0]], {}, 1),
        # The sixth pass (2026-10-13): a junction row is not listed, and a
        # review of one is no longer needed without being stale.
        ("a junction named for a hotel", [[1, 1, 2, "リッチモンドホテル前", "", 0]], {}, 0),
        ("a review the test no longer needs", [[1, 1, 2, "リッチモンドホテル前", "", 0]],
         {"リッチモンドホテル前": "a signed junction"}, 0),
    ]
    for label, rows, reviewed, want in leak_cases:
        got = len(check_leaks("x", dict(base, languages=ja, rows=rows), reviewed))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    # PLACE_RULED_KEPT (the big review, 2026-10-13): a recorded keep is a
    # row of the index, a place by id and a street by name.
    krows = [[0, 1, 2, "Old Mill", "", 0], [1, 1, 2, "Mill Lane", "Mill Ln", 0]]
    kids = ["way/7"]
    ruled_cases = [
        ("a ruled keep by id and one by street name", {"way/7": "'Old Mill', stands", "Mill Lane": "a road"}, {}, 0),
        ("a ruled keep under an alternate name", {"Mill Ln": "a road"}, {}, 0),
        ("a ruled keep whose id is no row", {"way/8": "'Old Barn', stands"}, {}, 1),
        ("a ruled keep whose street is no row", {"Barn Lane": "a road"}, {}, 1),
        ("a ruled keep with no why", {"way/7": ""}, {}, 1),
        ("a ruled keep that is also dropped", {"way/7": "stands"}, {"way/7": "a home"}, 1),
        ("an id is never read as a name", {"way/9": "a row named way/9"}, {}, 1),
        ("no record at all", {}, {}, 0),
    ]
    for label, ruled, dropped, want in ruled_cases:
        got = len(check_ruled_kept("x", dict(base, languages=ja, rows=krows + [[0, 1, 2, "way/9", "", 0]]),
                                   kids, ruled, dropped))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    got = len(check_crossings("x", dict(base, crossings="/app/static/places/y.json?v=0")))
    ok += got == 1
    print(f"  {'ok ' if got == 1 else 'BAD'} an index naming another file as its crossings: {got} problem(s)")
    junk_cases = [("an error value and a number alone", [[0, 1, 2, "#N/A", "47", 0]], 1),
                  ("a real name with a number", [[0, 1, 2, "5th Avenue", "", 0]], 0)]
    for label, rows, want in junk_cases:
        got = len(check_junk(dict(base, rows=rows)))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    entry = {"name": "x", "access": "OPEN_REGULAR", "source": "https://example.org/visit",
             "checked": "2026-10-08", "why": "open daily"}
    visit_cases = [("a fresh entry", {"way/1": entry}, "2026-12-01", 0),
                   ("a lapsed entry", {"way/1": entry}, "2027-10-20", 1),
                   ("appointment only is not visitable", {"way/1": dict(entry, access="APPOINTMENT")},
                    "2026-12-01", 1),
                   ("no source", {"way/1": {k: v for k, v in entry.items() if k != "source"}}, "2026-12-01", 1)]
    for label, visitable, today, want in visit_cases:
        got = len(check_visitable("x", visitable, today))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    near = [[2, 10.001, 20.001, "a street", "", 0]]
    far = [[2, 10.045, 20.0, "a long road", "", 0]]

    def road(dlon):
        return [(9.95, 20.0 + dlon), (10.05, 20.0 + dlon)]
    cover_cases = [
        ("a station with a place beside it", near, [("A", 10.0, 20.0)], {}, 0),
        ("a station past the index's edge", near, [("A", 10.0, 20.0), ("B", 10.3, 20.0)], {}, 1),
        ("only another station nearby is no cover", [[0, 10.0, 20.0, "A", "", 0]], [("A", 10.0, 20.0)], {}, 1),
        ("a known gap is reported, not failed", near, [("B", 10.3, 20.0)], {"x": "dated"}, 0),
        ("a known gap that has closed", near, [("A", 10.0, 20.0)], {"x": "dated"}, 1),
        # A road 10 km long whose row point is 5 km off passes 100 m from the
        # station (Ottawa's Bowesville); the same road 2 km away is no cover.
        ("a long street passing the station, its point far off", far, [("A", 10.0, 20.0)], {}, 0, [road(0.001)]),
        ("a long street 2 km from the station", far, [("A", 10.0, 20.0)], {}, 1, [road(0.02)]),
        ("no street lines given: the row points decide", far, [("A", 10.0, 20.0)], {}, 1, None),
    ]
    for label, rows, stations, known, want, *rest in cover_cases:
        got = len(check_coverage("x", dict(base, rows=rows), stations, known, lines=rest[0] if rest else None))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    quiet_cases = [
        ("a quiet station, listed", near, [("A", 10.0, 20.0), ("B", 10.3, 20.0)], {"B": "why"}, 0),
        ("a quiet station listed, another uncovered", near, [("B", 10.3, 20.0), ("C", 10.6, 20.0)], {"B": "why"}, 1),
        ("a listed station that is covered", near, [("A", 10.0, 20.0)], {"A": "why"}, 1),
        ("a listed station that is not on the map", near, [("A", 10.0, 20.0)], {"Z": "why"}, 1),
    ]
    for label, rows, stations, quiet, want in quiet_cases:
        got = len(check_coverage("x", dict(base, rows=rows), stations, {}, quiet=quiet))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    current = "function getIndex(u) { window.parent.location.pathname; fetch(abs(u), opt) }"
    path_cases = [
        ("a map that takes the app's prefix", current, 0),
        ("a map rendered before the fix", 'loading = fetch(URL, {credentials: "omit"})', 2),
        ("the prefix read but the bare URL still fetched", current + " fetch(crossURL, opt)", 1),
    ]
    for label, text, want in path_cases:
        got = len(check_fetch_path(text))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    sidx = dict(base, kinds=["station", "street"],
                rows=[[0, 10.0, 20.0, "A", "", 0], [1, 10.001, 20.001, "a street", "", [10.0, 20.0, 10.002, 20.002]]])
    sfile = {"license": base["license"], "schema": 1, "city": "X", "part_of": "x.json", "scale": 100000}
    street_cases = [
        ("a line inside its street's extent", dict(sfile, rows=[1], lines=[[[1000000, 2000000, 200, 200]]]), 0),
        ("a line that leaves its street", dict(sfile, rows=[1], lines=[[[1000000, 2000000, 5000, 200]]]), 1),
        ("a line for a row that is no street", dict(sfile, rows=[0], lines=[[[1000000, 2000000, 1, 1]]]), 1),
        ("a field from another source", dict(sfile, rows=[1], lines=[[[1000000, 2000000, 200, 200]]], width=[9]), 1),
    ]
    for label, st, want in street_cases:
        got = len(street_problems(sidx, st))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    total = (len(cases) + 1 + len(leak_cases) + len(ruled_cases) + 1 + len(junk_cases) + len(visit_cases)
             + len(cover_cases) + len(quiet_cases) + len(path_cases) + len(street_cases))
    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
