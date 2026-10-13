"""Ask Wikidata which of a city's cached OSM places have a Wikipedia article
in any language, and cache the answer. NOT a step: drift_check.py never runs
this file.

    python pipeline/place_wikidata_fetch.py <city> [--force] [--out FILE]
    python pipeline/place_wikidata_fetch.py --selftest

Reads config.PLACE_OSM_JSON and, when the config defines it and the file is on
disk, config.PLACE_OSM_EXTRA_JSON, both Overpass-shaped
{"elements": [{"type", "id", "tags"}, ...]}. Every wikidata id on an element
with no wikipedia tag and no tag whose key starts with "wikipedia:" is asked of
Wikidata (wbgetentities, props=sitelinks); which ids have an article in any
language is written to one cache, config.PLACE_WIKIDATA_JSON or, when the
config has no such path, the PLACE_OSM_JSON folder with "osm_places" replaced
by "wikidata_articles" in the file name. Wiring this cache into the index step
is a later change; this file only fetches.

A cache already on disk is kept: without --force only the ids it does not hold
yet are asked, with every id held nothing is asked, and --force asks all of
them again. One request in flight at a time, at most 50 ids a request, at least
1 s between requests; an HTTP 429 or 5xx or a maxlag error is retried after the
Retry-After pause (at least 5 s, at most 120 s, at most 3 tries a batch), then
the run exits non-zero naming the batch. The cache is written after each batch,
so a refused batch leaves the earlier answers on disk.

No provenance entry is written: place_index_fetch.record reads Overpass-shaped
fields (elements, _fetched_from, osm3s, _query) this cache does not carry, and
record is not changed here.
"""
import argparse
import datetime
import importlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.osm import OVERPASS_USER_AGENT  # noqa: E402

API_URL = "https://www.wikidata.org/w/api.php"
BATCH_SIZE = 50
MIN_INTERVAL_S = 1.0
MAX_TRIES = 3
RETRY_MIN_S = 5
RETRY_MAX_S = 120
# Sitelinks that are not Wikipedia articles even though their key ends in
# "wiki". Keys ending in wikiquote, wikisource, wikivoyage, wikinews,
# wikibooks, wikiversity or wiktionary do not end in "wiki" and are out before
# this list is reached.
NON_ARTICLE_WIKIS = frozenset((
    "commonswiki", "specieswiki", "metawiki", "wikidatawiki", "mediawikiwiki",
    "sourceswiki", "foundationwiki", "incubatorwiki", "outreachwiki",
    "wikimaniawiki", "wikifunctionswiki",
))
QID = re.compile(r"^Q\d+$")


def collect_ids(elements):
    """Every distinct Q id in a wikidata tag of an element with no wikipedia
    tag and no tag whose key starts with "wikipedia:", in first-seen order,
    and how many wikidata values were not Q ids."""
    ids, skipped, seen = [], 0, set()
    for element in elements:
        tags = element.get("tags") or {}
        if "wikidata" not in tags:
            continue
        if "wikipedia" in tags or any(k.startswith("wikipedia:") for k in tags):
            continue
        for piece in str(tags["wikidata"]).split(";"):
            piece = piece.strip()
            if QID.match(piece):
                if piece not in seen:
                    seen.add(piece)
                    ids.append(piece)
            else:
                skipped += 1
    return ids, skipped


def is_article_key(key):
    """True when a sitelink key is a Wikipedia article in some language."""
    return key.endswith("wiki") and key not in NON_ARTICLE_WIKIS


def api_url(ids):
    """The wbgetentities URL for one batch. The ids are joined by | and all
    other parameters are fixed, so no percent-encoding is needed."""
    params = "action=wbgetentities&props=sitelinks&format=json&maxlag=5&ids=" + "|".join(ids)
    return f"{API_URL}?{params}"


def parse_entities(payload, ids):
    """{id: article keys} for the ids asked, None for an id absent from the
    reply or whose entry says missing. A redirect comes back under the id that
    was asked and is recorded there."""
    entities = payload.get("entities") or {}
    answered = {}
    for qid in ids:
        obj = entities.get(qid)
        if obj is None or "missing" in obj:
            answered[qid] = None
        else:
            sitelinks = obj.get("sitelinks") or {}
            answered[qid] = sorted(k for k in sitelinks if is_article_key(k))
    return answered


def _retry_wait(headers):
    """Seconds to pause before retrying: the Retry-After header clamped to
    [RETRY_MIN_S, RETRY_MAX_S], or RETRY_MIN_S without one."""
    raw = (headers or {}).get("Retry-After")
    try:
        secs = int(str(raw).strip())
    except (TypeError, ValueError):
        secs = RETRY_MIN_S
    return max(RETRY_MIN_S, min(RETRY_MAX_S, secs))


def _retryable(status, body):
    """True when the answer asks for a retry: HTTP 429 or 5xx, or a 200 whose
    error code is maxlag."""
    if status == 429 or 500 <= status < 600:
        return True
    if status != 200:
        return False
    try:
        payload = json.loads(body)
    except ValueError:
        return False
    return payload.get("error", {}).get("code") == "maxlag"


def ask_batch(ids, transport, pause, say=print):
    """One batch of at most BATCH_SIZE ids, answered and returned as (payload,
    tries). Retried on a retryable answer (pause first), at most MAX_TRIES
    tries, then exits non-zero naming the batch."""
    url = api_url(ids)
    for attempt in range(1, MAX_TRIES + 1):
        status, headers, body = transport(url)
        if _retryable(status, body):
            if attempt == MAX_TRIES:
                raise SystemExit(f"batch {ids[0]}..{ids[-1]}: {MAX_TRIES} tries without an answer; "
                                 f"earlier answers are on disk")
            pause(_retry_wait(headers))
            continue
        if status != 200:
            raise SystemExit(f"batch {ids[0]}..{ids[-1]}: HTTP {status}")
        try:
            return json.loads(body), attempt
        except ValueError as exc:
            raise SystemExit(f"batch {ids[0]}..{ids[-1]}: the reply is not JSON: {exc}")


def _fetch(url):
    """One HTTP GET; returns (status, headers, body text). An HTTP error is
    returned, not raised, so its status and headers reach the retry logic."""
    req = urllib.request.Request(url, headers={"User-Agent": OVERPASS_USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.headers, resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers, exc.read().decode("utf-8")


def chunks(ids, size=BATCH_SIZE):
    """ids cut into lists of at most `size`, in order."""
    for i in range(0, len(ids), size):
        yield ids[i:i + size]


def write_cache(path, articles, fetched):
    """The one cache file, as UTF-8 bytes with LF line endings and sorted
    keys: _source (host, api, licence, fetched date, id count) then articles."""
    payload = {
        "_source": {
            "host": "www.wikidata.org",
            "api": "wbgetentities, props=sitelinks",
            "licence": "CC0 1.0",
            "fetched": fetched,
            "ids": len(articles),
        },
        "articles": articles,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))


def run(config, *, force=False, out_path=None, transport=_fetch, pause=time.sleep,
        today=None, say=print):
    """The script's body; returns the cache path written, or None when nothing
    changed. `transport` is a callable(url) -> (status, headers, body), and
    `pause` sleeps between requests and before a retry: both are the
    selftest's."""
    today = today or datetime.date.today()
    main_path = Path(config.PLACE_OSM_JSON)
    if not main_path.exists():
        raise SystemExit(f"{main_path.name}: not on disk; write it with pipeline/place_index_fetch.py "
                         f"or pipeline/place_extract_fetch.py, then run this again")
    elements = list(json.loads(main_path.read_bytes().decode("utf-8")).get("elements") or [])
    extra = getattr(config, "PLACE_OSM_EXTRA_JSON", None)
    if extra and Path(extra).exists():
        elements += json.loads(Path(extra).read_bytes().decode("utf-8")).get("elements") or []
    ids, skipped = collect_ids(elements)
    if skipped:
        say(f"{skipped} wikidata value(s) not Q ids: not sent")
    cache_path = Path(getattr(config, "PLACE_WIKIDATA_JSON")) if getattr(config, "PLACE_WIKIDATA_JSON", None) \
        else main_path.with_name(main_path.name.replace("osm_places", "wikidata_articles", 1))
    if out_path is not None:
        cache_path = Path(out_path)
    cache = json.loads(cache_path.read_bytes().decode("utf-8")) if cache_path.exists() else None
    if cache is not None and not force:
        articles = dict(cache.get("articles") or {})
        need = [qid for qid in ids if qid not in articles]
    else:
        articles, need = {}, list(ids)
    if not need:
        say(f"{cache_path.name}: every id already held ({len(ids)} id(s)); no request made")
        return None
    requests = 0
    for i, batch in enumerate(chunks(need)):
        if i:
            pause(MIN_INTERVAL_S)
        payload, tries = ask_batch(batch, transport, pause, say)
        requests += tries
        articles.update(parse_entities(payload, batch))
        write_cache(cache_path, articles, today.isoformat())
    with_article = sum(1 for v in articles.values() if isinstance(v, list) and v)
    without = sum(1 for v in articles.values() if v == [])
    missing = sum(1 for v in articles.values() if v is None)
    say(f"ids found {len(ids)}; asked {len(need)}; with an article {with_article}; "
        f"without {without}; missing {missing}; requests {requests}")
    return cache_path


def selftest():
    import tempfile
    cases = []

    def case(label, ok):
        cases.append((label, bool(ok)))

    def ids_of(url):
        return urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)["ids"][0].split("|")

    case("the User-Agent holds no @ character", "@" not in OVERPASS_USER_AGENT)

    elements = [
        {"type": "node", "id": 1, "tags": {"wikidata": "Q5;Q6"}},
        {"type": "node", "id": 2, "tags": {"wikidata": "Q5x"}},
        {"type": "node", "id": 3, "tags": {"wikidata": "P31"}},
        {"type": "node", "id": 4, "tags": {"wikidata": "Q7", "wikipedia": "en:X"}},
        {"type": "node", "id": 5, "tags": {"wikidata": "Q8", "wikipedia:en": "X"}},
        {"type": "node", "id": 6, "tags": {"name": "no wikidata"}},
        {"type": "node", "id": 7, "tags": {"wikidata": "Q5;Q5"}},
    ]
    ids, skipped = collect_ids(elements)
    case("Q5;Q6 gives two ids; Q5x and P31 are not sent; a wikipedia or wikipedia: tag contributes "
         "no id; a repeated id is kept once",
         ids == ["Q5", "Q6"] and skipped == 2)

    case("enwiki is an article; commonswiki is not; wikiquote, wikisource, wikivoyage, wikinews, "
         "wikibooks, wikiversity and wiktionary are not (no wiki suffix)",
         is_article_key("enwiki") and not is_article_key("commonswiki")
         and not any(is_article_key(k) for k in (
             "enwikiquote", "enwikisource", "enwikivoyage", "enwikinews",
             "enwikibooks", "enwikiversity", "enwiktionary")))

    payload = {"entities": {
        "Q1": {"sitelinks": {"enwiki": {"title": "X"}, "commonswiki": {"title": "Y"}}},
        "Q2": {"sitelinks": {"commonswiki": {"title": "Y"}}},
        "Q3": {"missing": ""},
    }}
    got = parse_entities(payload, ["Q1", "Q2", "Q3", "Q4"])
    case("enwiki plus commonswiki gives one article; commonswiki alone gives none; a missing entry and "
         "an id absent from the reply are null and counted",
         got == {"Q1": ["enwiki"], "Q2": [], "Q3": None, "Q4": None})

    case("120 ids make batches of 50, 50 and 20",
         [len(c) for c in chunks([f"Q{i}" for i in range(1, 121)])] == [50, 50, 20])

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        today = datetime.date(2026, 10, 13)

        class City:
            SLUG = "testville"
            PLACE_OSM_JSON = d / "osm_places_2026-10-08.json"
            PLACE_OSM_EXTRA_JSON = d / "osm_places_extra_2026-10-08.json"

        cache_path = d / "wikidata_articles_2026-10-08.json"

        def enwiki(asked):
            return json.dumps({"entities": {q: {"sitelinks": {"enwiki": {"title": "T"}}} for q in asked}})

        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": i, "tags": {"wikidata": f"Q{i}"}} for i in range(1, 121)
        ]}).encode("utf-8"))
        urls = []

        def t(url):
            urls.append(url)
            return 200, {}, enwiki(ids_of(url))

        run(City, transport=t, pause=lambda s: None, today=today, say=lambda *a: None)
        payload = json.loads(cache_path.read_bytes().decode("utf-8"))
        case("120 ids make 3 requests of 50, 50 and 20, and the cache holds every id",
             [len(ids_of(u)) for u in urls] == [50, 50, 20]
             and len(payload["articles"]) == 120 and payload["_source"]["ids"] == 120
             and payload["_source"]["fetched"] == "2026-10-13"
             and payload["_source"]["host"] == "www.wikidata.org"
             and payload["_source"]["licence"] == "CC0 1.0")

        before = cache_path.read_bytes()
        again_urls = []

        def t2(url):
            again_urls.append(url)
            return 200, {}, "{}"

        run(City, transport=t2, pause=lambda s: None, today=today, say=lambda *a: None)
        case("a cache holding every id makes no request and leaves the file unchanged",
             again_urls == [] and cache_path.read_bytes() == before)

        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": 1, "tags": {"wikidata": "Q1"}},
            {"type": "node", "id": 2, "tags": {"wikidata": "Q2"}},
            {"type": "node", "id": 3, "tags": {"wikidata": "Q3"}},
        ]}).encode("utf-8"))
        cache_path.write_bytes(json.dumps({
            "_source": {"host": "www.wikidata.org", "api": "wbgetentities, props=sitelinks",
                        "licence": "CC0 1.0", "fetched": "2026-10-12", "ids": 2},
            "articles": {"Q1": ["enwiki"], "Q2": ["frwiki"]},
        }).encode("utf-8"))
        asked = []

        def t3(url):
            q = ids_of(url)
            asked.extend(q)
            return 200, {}, json.dumps({"entities": {qid: {"sitelinks": {}} for qid in q}})

        run(City, transport=t3, pause=lambda s: None, today=today, say=lambda *a: None)
        payload = json.loads(cache_path.read_bytes().decode("utf-8"))
        case("a cache holding some ids asks only the others, and the old answers are unchanged in the file",
             asked == ["Q3"] and payload["articles"]["Q1"] == ["enwiki"]
             and payload["articles"]["Q2"] == ["frwiki"] and payload["articles"]["Q3"] == []
             and payload["_source"]["ids"] == 3 and payload["_source"]["fetched"] == "2026-10-13")

        force_asked = []

        def t4(url):
            q = ids_of(url)
            force_asked.extend(q)
            return 200, {}, json.dumps({"entities": {qid: {"sitelinks": {"dewiki": {"title": "T"}}} for qid in q}})

        run(City, force=True, transport=t4, pause=lambda s: None, today=today, say=lambda *a: None)
        payload = json.loads(cache_path.read_bytes().decode("utf-8"))
        case("--force asks every id again and replaces the answers",
             sorted(force_asked) == ["Q1", "Q2", "Q3"]
             and payload["articles"] == {"Q1": ["dewiki"], "Q2": ["dewiki"], "Q3": ["dewiki"]})

        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": 1, "tags": {"wikidata": "Q1"}},
            {"type": "node", "id": 2, "tags": {"wikidata": "Q2"}},
            {"type": "node", "id": 3, "tags": {"wikidata": "Q3"}},
            {"type": "node", "id": 4, "tags": {"wikidata": "Q4"}},
        ]}).encode("utf-8"))
        cache_path.unlink()
        said = []

        def t5(url):
            return 200, {}, json.dumps({"entities": {
                "Q1": {"sitelinks": {"enwiki": {"title": "T"}}},
                "Q2": {"sitelinks": {}},
                "Q3": {"missing": ""},
            }})

        run(City, transport=t5, pause=lambda s: None, today=today, say=said.append)
        line = next(s for s in said if "with an article" in s)
        case("the summary counts an id absent from the reply as missing",
             "with an article 1" in line and "without 1" in line and "missing 2" in line
             and "requests 1" in line)

        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": 1, "tags": {"wikidata": "Q9"}},
        ]}).encode("utf-8"))
        cache_path.unlink()
        pauses = []
        state = {"n": 0}

        def t6(url):
            state["n"] += 1
            if state["n"] == 1:
                return 200, {"Retry-After": "7"}, json.dumps({"error": {"code": "maxlag"}})
            return 200, {}, json.dumps({"entities": {"Q9": {"sitelinks": {"enwiki": {"title": "T"}}}}})

        run(City, transport=t6, pause=pauses.append, today=today, say=lambda *a: None)
        payload = json.loads(cache_path.read_bytes().decode("utf-8"))
        case("a maxlag error then a good reply retries once and keeps the answer",
             state["n"] == 2 and pauses == [7] and payload["articles"]["Q9"] == ["enwiki"])

        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": i, "tags": {"wikidata": f"Q{i}"}} for i in range(1, 61)
        ]}).encode("utf-8"))
        cache_path.unlink()

        def t7(url):
            q = ids_of(url)
            if len(q) == 50:
                return 200, {}, json.dumps({"entities": {qid: {"sitelinks": {"enwiki": {"title": "T"}}} for qid in q}})
            return 429, {}, ""

        caught = None
        try:
            run(City, transport=t7, pause=lambda s: None, today=today, say=lambda *a: None)
        except SystemExit as exc:
            caught = exc
        payload = json.loads(cache_path.read_bytes().decode("utf-8"))
        case("three failures in a row exit non-zero naming the batch, and the earlier answers are on disk",
             caught is not None and "Q51" in str(caught)
             and set(payload["articles"]) == {f"Q{i}" for i in range(1, 51)}
             and payload["_source"]["ids"] == 50)

        raw = cache_path.read_bytes()
        parsed = json.loads(raw.decode("utf-8"))
        case("the written file has no carriage return and its keys are sorted",
             b"\r" not in raw
             and list(parsed) == sorted(parsed)
             and list(parsed["_source"]) == sorted(parsed["_source"])
             and list(parsed["articles"]) == sorted(parsed["articles"]))

        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": 1, "tags": {"wikidata": "Q9"}},
        ]}).encode("utf-8"))
        cache_path.unlink()
        pauses2 = []
        state2 = {"n": 0}

        def t8(url):
            state2["n"] += 1
            if state2["n"] == 1:
                return 429, {}, ""
            return 200, {}, json.dumps({"entities": {"Q9": {"sitelinks": {}}}})

        run(City, transport=t8, pause=pauses2.append, today=today, say=lambda *a: None)
        case("a 429 with no Retry-After waits 5 s and retries once",
             state2["n"] == 2 and pauses2 == [5])

        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": 1, "tags": {"wikidata": "Q1"}},
        ]}).encode("utf-8"))
        City.PLACE_OSM_EXTRA_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": 2, "tags": {"wikidata": "Q2"}},
        ]}).encode("utf-8"))
        cache_path.unlink()
        extra_asked = []

        def t9(url):
            q = ids_of(url)
            extra_asked.extend(q)
            return 200, {}, json.dumps({"entities": {qid: {"sitelinks": {}} for qid in q}})

        run(City, transport=t9, pause=lambda s: None, today=today, say=lambda *a: None)
        case("the extra cache contributes its ids too", sorted(extra_asked) == ["Q1", "Q2"])

        out_file = d / "elsewhere.json"
        City.PLACE_OSM_JSON.write_bytes(json.dumps({"elements": [
            {"type": "node", "id": 1, "tags": {"wikidata": "Q1"}},
        ]}).encode("utf-8"))
        cache_path.unlink()

        def t10(url):
            return 200, {}, json.dumps({"entities": {q: {"sitelinks": {}} for q in ids_of(url)}})

        run(City, out_path=out_file, transport=t10, pause=lambda s: None, today=today, say=lambda *a: None)
        case("--out writes the cache to the named file and not the default",
             out_file.exists() and not cache_path.exists())

        class WithPath(City):
            PLACE_WIKIDATA_JSON = d / "named.json"

        run(WithPath, force=True, transport=t10, pause=lambda s: None, today=today, say=lambda *a: None)
        case("config.PLACE_WIKIDATA_JSON names the cache when the config defines it",
             (d / "named.json").exists())

        class NoMain(City):
            PLACE_OSM_JSON = d / "absent.json"

        caught = None
        try:
            run(NoMain, transport=t10, pause=lambda s: None, today=today, say=lambda *a: None)
        except SystemExit as exc:
            caught = exc
        case("PLACE_OSM_JSON missing on disk exits non-zero naming the script that writes it",
             caught is not None and "place_index_fetch.py" in str(caught)
             and "place_extract_fetch.py" in str(caught))

    for label, ok in cases:
        print(f"  {'ok ' if ok else 'BAD'} {label}")
    good = sum(ok for _, ok in cases)
    print(f"{good} of {len(cases)} cases behaved as intended.")
    return 0 if good == len(cases) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("city")
    ap.add_argument("--force", action="store_true",
                    help="ask every id again, replacing the cache's answers")
    ap.add_argument("--out", metavar="FILE",
                    help="write the cache here instead, and record no provenance")
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")
    run(config, force=args.force, out_path=args.out)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(selftest() if "--selftest" in sys.argv else main())
