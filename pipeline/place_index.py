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


def _site_url(path):
    """The site path of a file under app/static/, stamped with its content
    hash (index_url's reason)."""
    import hashlib
    rel = path.relative_to(STATIC_DIR.parent).as_posix()
    return f"/app/static/{rel}?v={hashlib.sha256(path.read_bytes()).hexdigest()[:12]}"


def summary_path(slug):
    return Path(__file__).parent.parent / "outputs" / slug / "place_search.json"


def write(index, slug):
    """Write the index (served as-is: bytes, LF only, no BOM) and the page's
    summary, outputs/<slug>/place_search.json: the languages the page names,
    the count and the retrieval date. The app reads the summary, never the
    index, so a page load costs no megabyte."""
    # The crossings first: the index carries their file's hashed path, so a
    # rebuilt crossings file is never served from a browser's old copy.
    cross = index.pop("crossing_rows")
    cpath = crossings_path(slug)
    cpath.parent.mkdir(parents=True, exist_ok=True)
    cpath.write_bytes(json.dumps({"license": index["license"], "city": index["city"],
                                  "part_of": f"{slug}.json", "rows": cross},
                                 ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    index["crossings"] = _site_url(cpath)
    out = index_path(slug)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(json.dumps(index, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    summary = {"index": f"app/static/places/{slug}.json", "places": len(index["rows"]) + len(cross),
               "data_retrieved": index["license"]["data_retrieved"], "languages": index["languages"]}
    summary_path(slug).write_bytes(
        (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return out


# Folds the browser applies to Latin text on both sides of a match (the search
# script's norm()): "ja" folds Japanese long vowels written out, shijou =
# shijo. A city sets config.PLACE_FOLD to one of these, or None.
FOLDS = (None, "ja")


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
    index, report = build(payload["elements"], city=name, retrieved=retrieved,
                          local=config.PLACE_LANGUAGES, fold=fold, dropped=dropped,
                          visitable=live)
    found = {f"{e['type']}/{e['id']}" for e in payload["elements"]}
    stale = sorted(set(dropped) - found)
    if stale:
        sys.exit(f"config.PLACE_DROPPED names {stale}, not in the cache: remove them")
    stale = sorted(set(visitable) - found)
    if stale:
        sys.exit(f"config.PLACE_VISITABLE names {stale}, not in the cache: remove them")
    out = write(index, slug)
    cpath = crossings_path(slug)
    print(f"Wrote {out} ({out.stat().st_size:,} bytes, {len(index['rows']):,} places), "
          f"{cpath.relative_to(STATIC_DIR).as_posix()} ({cpath.stat().st_size:,} bytes, "
          f"{report.get('crossing', 0):,} intersections) and {summary_path(slug).name}")
    print(f"  languages: {index['languages']['coverage']} -> the page names {index['languages']['listed']}")
    for k in sorted(report):
        print(f"  {k}: {report[k]:,}")
    return index


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
           "condominium", "condo", "condos", "parking", "private"),
    # Batch 2a (2026-10-08): the handoff's proposals, each language checked
    # against its city's own hits (docs/decisions_drafts/place-search.md).
    "fr": ("sarl", "sas", "eurl", "hôtel", "auberge", "résidence", "appartements", "parking",
           "privé", "privée", "magasin", "boutique", "restaurant", "brasserie", "pharmacie",
           "clinique", "agence",
           # Housing estates: a subdivision, a social-housing group (Marseille).
           "lotissement", "morcellement", "hlm", "h.l.m."),
    "ca": ("hotel", "hostal", "aparcament", "pàrquing", "privat", "privada", "botiga", "restaurant",
           "pisos", "farmàcia", "s.l.", "s.a."),
    "es": ("hotel", "hostal", "aparcamiento", "parking", "privado", "privada", "tienda", "restaurante",
           "pisos", "farmacia", "s.l.", "s.a."),
    "cs": ("hotel", "penzion", "parkoviště", "soukromé", "soukromá", "obchod", "restaurace",
           "bytový dům", "bytové domy", "lékárna", "s.r.o.", "a.s.", "rezidence"),
    "nl": ("hotel", "parking", "privé", "winkel", "restaurant", "appartementen", "residentie",
           "apotheek", "bvba", "nv"),
}
LEAK_ALLOW = {"ja": ("商店街", "名店街"), "en": ("shopping street",),
              # A town hall and a hospital (Paris's Hôtel-Dieu, Marseille's).
              "fr": ("hôtel de ville", "hôtel-de-ville", "hôtel-dieu", "hôtel des invalides")}
# The LEAK_WORDS that mark a home (or private land): a landmark carrying one
# is held to _public_home, where a Wikipedia article is no exemption.
HOME_WORDS = {
    "ja": ("マンション", "ハイツ", "レジデンス", "コーポ", "アパート", "メゾン", "社宅", "私有地"),
    "en": ("apartment", "apartments", "apts", "condominium", "condo", "condos", "private"),
    "fr": ("résidence", "appartements", "privé", "privée", "lotissement", "morcellement", "hlm",
           "h.l.m."),
    "ca": ("pisos", "privat", "privada"),
    "es": ("pisos", "privado", "privada"),
    "cs": ("bytový dům", "bytové domy", "soukromé", "soukromá", "rezidence"),
    "nl": ("appartementen", "residentie", "privé"),
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
           "escaleras", "sendero"),
    "cs": ("ulice", "třída", "náměstí", "nábřeží", "most", "lávka", "cesta", "stezka", "schody",
           "schodiště", "alej", "sady", "pěšina", "průchod", "pasáž", "nároží", "stoupání",
           "náplavka"),
    "nl": ("straat", "laan", "weg", "plein", "steenweg", "kaai", "lei", "dreef", "brug", "pad",
           "gang", "steeg", "dijk", "doorgang", "trap", "wandeling", "promenade", "galerij"),
}
# Languages that write a way word inside a compound ("Nieuwstraat",
# "Kerkpad"): _reads_as_way matches it as a word's ending there.
SUFFIX_WAY_LANGUAGES = {"nl"}
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
RAIL_MODES = ("train", "subway", "light_rail", "tram", "monorail", "funicular")
OTHER_MODES = ("bus", "ferry", "trolleybus", "coach")
# A commercial building is a business unless notable: Sydney's numbered
# "Bay 0" to "Bay 15", historic=building on building=commercial (2026-10-08).
# A hotel building likewise (Barcelona's Casa Cambó, building=hotel, batch 2a).
# And a data centre (Marseille's U-boat bunker, building=data_center, batch 2a).
COMMERCIAL_BUILDINGS = {"commercial", "retail", "office", "hotel", "data_center"}
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
                  "cs": ("dům", "vila"), "nl": ("huis",)}


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
    first = (re.findall(r"\w+", name.lower()) or [""])[0]
    return any(first in HOME_NAME_LEAD.get(c, ()) for c in local)


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
    return (tags.get("landuse") == "residential" or tags.get("building") in RESIDENTIAL_BUILDINGS
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


def _names(tags, name_tags):
    seen, out = set(), []
    for k in name_tags:
        for v in (tags.get(k) or "").split(";"):
            v = v.strip()
            if v and v not in seen and not junk_name(v):
                seen.add(v)
                out.append(v)
    return out


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


def build(elements, *, city, retrieved, local, fold=None, dropped=(), visitable=()):
    """Return (index dict, report dict) from one place cache's elements.
    `local`: the city's local language codes (config.PLACE_LANGUAGES).
    `dropped`: OSM objects ("way/504652702") a reading by eye found to be a
    business or a home that no rule catches (config.PLACE_DROPPED).
    `visitable`: homes the public can visit today, kept against the home rule
    (config.PLACE_VISITABLE's live entries; VISITABLE FORMER HOMES above)."""
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
    node_streets = defaultdict(set)           # node id -> street display names
    for w in ways:
        t = w.get("tags", {})
        if (t.get("highway") in SKIP_HIGHWAY or t.get("area") == "yes"
                or t.get("service") in SKIP_SERVICE):
            report["street_way_skipped"] += 1
            continue
        names = _names(t, name_tags)
        if (t.get("highway") in MINOR_HIGHWAYS and not (t.get("wikidata") or t.get("wikipedia"))
                and not _reads_as_way(names, local)):
            report["minor_way_dropped_not_a_way_name"] += 1
            continue
        # A road named for private or parking access, or a business, is no
        # street to search; a name of that kind beside a real one is dropped
        # alone (Vancouver's "26 Avenue", alt_name "Private Access", 2026-10-08).
        kept = [n for n in names if not leak_word([n], local)]
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
        names = _names(t, name_tags)
        pt = _point(e)
        if not names or not pt:
            continue
        if extent and not (extent[0] <= pt[0] <= extent[2] and extent[1] <= pt[1] <= extent[3]):
            report["outside_area"] += 1
            continue
        langs = _langs(t, local)
        if (t.get("public_transport") == "station" and not t.get("railway")
                and not any(t.get(k) == "yes" for k in RAIL_MODES)
                and any(t.get(k) == "yes" for k in OTHER_MODES)):
            # A bus or ferry terminal, or a tour boat's dock ("Wendella
            # Tours - Michigan Avenue", Chicago, 2026-10-08): no station.
            report["station_skipped_not_rail"] += 1
            continue
        if t.get("railway") in ("station", "halt", "tram_stop") or t.get("public_transport") == "station":
            add("station", pt, names, langs)
        elif t.get("place") in PLACE_VALUES:
            # A place drawn as an area on residential land is an estate, its
            # homes' own name ("Kentbrook Apartments", Seattle: 85 of the
            # place areas, 2026-10-08); a place named for a business or a
            # home is one, as a landmark is.
            if e["type"] != "node" and (t.get("landuse") == "residential" or t.get("residential")):
                report["place_dropped_estate"] += 1
                continue
            if leak_word(names, local):
                report["place_dropped_leak_word"] += 1
                continue
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
            if _commercial(t):
                report["landmark_dropped_commercial"] += 1
                continue
            if (any(k in t for k in NOTABLE_ONLY) and t.get("amenity") != "place_of_worship"
                    and not (t.get("wikidata") or t.get("wikipedia"))):
                report["landmark_dropped_not_notable"] += 1
                continue
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
        "city": city,
        "languages": languages(row_langs, local),
        "fold": fold,
        "kinds": list(KINDS),
        "rows": rows,
        # write() puts these in crossings_path() and their site path here.
        "crossing_rows": crossing_rows,
    }
    return index, dict(report)
