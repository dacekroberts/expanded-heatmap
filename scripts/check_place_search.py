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
KNOWN_GAPS = {
    "mexico_city": "2026-10-12: the index is cut to Ciudad de Mexico, the map is regional; rebuilt in "
                   "the search rollout's first wave (owner; PLAN.md)",
}


def check_coverage(slug, index, stations, known=None):
    """H for one city: problems, given its index and its map's stations."""
    known = KNOWN_GAPS if known is None else known
    bare = place_index.uncovered_stations(index["rows"], stations)
    if bare and slug not in known:
        return [f"H: {len(bare)} map station(s) with no indexed place within {place_index.COVER_KM:g} km "
                f"({', '.join(bare[:6])}): config.PLACE_AREA does not cover the whole map"]
    if not bare and slug in known:
        return ["H: listed in KNOWN_GAPS but every station is covered: delete the entry"]
    return []


TOP_KEYS = {"license", "city", "languages", "fold", "kinds", "rows", "crossings"}
CROSS_KEYS = {"license", "city", "part_of", "rows"}
URL_RE = re.compile(r"/app/static/places/([a-z0-9_]+)[.]json[?]v=([0-9a-f]+)")
CROSS_RE = re.compile(r"^/app/static/places/crossings/([a-z0-9_]+)[.]json[?]v=([0-9a-f]+)$")
BULLET = "never leaves your browser"


def rule(langs):
    """The page's list, recomputed from the coverage: the rule in one place."""
    order = list(dict.fromkeys(["en", *langs["local"]]))
    return [place_index.LANGUAGE_NAMES[c] for c in order
            if langs["coverage"].get(c, 0) >= place_index.LIST_SHARE]


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
    hit_names = {name for name, _ in hits}
    problems += [f"E: PLACE_REVIEWED names {name!r}, which no longer carries a leak word: remove it"
                 for name in reviewed if name not in hit_names]
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
        p += check_crossings(slug, index)
        p += check_junk(index)
        p += check_leaks(slug, index)
        p += check_visitable(slug)
        stations = place_index.map_stations(importlib.import_module(f"pipeline.{slug}.config"))
        if stations is None:
            unread.append(slug)
        else:
            p += check_coverage(slug, index, stations)
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
            "crossings": "/app/static/places/crossings/x.json?v=0"}
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
    ]
    for label, rows, reviewed, want in leak_cases:
        got = len(check_leaks("x", dict(base, languages=ja, rows=rows), reviewed))
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
    cover_cases = [
        ("a station with a place beside it", near, [("A", 10.0, 20.0)], {}, 0),
        ("a station past the index's edge", near, [("A", 10.0, 20.0), ("B", 10.3, 20.0)], {}, 1),
        ("only another station nearby is no cover", [[0, 10.0, 20.0, "A", "", 0]], [("A", 10.0, 20.0)], {}, 1),
        ("a known gap is reported, not failed", near, [("B", 10.3, 20.0)], {"x": "dated"}, 0),
        ("a known gap that has closed", near, [("A", 10.0, 20.0)], {"x": "dated"}, 1),
    ]
    for label, rows, stations, known, want in cover_cases:
        got = len(check_coverage("x", dict(base, rows=rows), stations, known))
        ok += got == want
        print(f"  {'ok ' if got == want else 'BAD'} {label}: {got} problem(s)")
    total = (len(cases) + 1 + len(leak_cases) + 1 + len(junk_cases) + len(visit_cases)
             + len(cover_cases))
    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
