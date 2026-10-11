"""Place search: the reading a city's index needs before it is published, as
the sample's first batch did it (2026-10-08). REPORTS only; changes nothing.

    python scripts/place_search_review.py odd <city>              # names to read by eye
    python scripts/place_search_review.py tags <city> <text> ...  # OSM tags of named objects
    python scripts/place_search_review.py ids <city> <type/id> ...  # each id's cached name, before PLACE_DROPPED
    python scripts/place_search_review.py added <city>            # what the extra query brought
    python scripts/place_search_review.py ways <city>             # named minor ways kept and dropped, leak hits
    python scripts/place_search_review.py sizes [<city> ...]      # bytes, gzip, rows by kind

odd: every landmark and place whose names hold no obvious place word (park,
church, museum ...). Brand names and homes carry no leak word, so this is the
list that found Sydney's "Meriton" park, Vancouver's register of heritage
houses, Chicago's "Lawrence House Patio" and Seattle's yoga studio. Read it
whole; a find that no rule in pipeline/place_index.py can catch goes in the
city's config.PLACE_DROPPED by OSM id, with why.

tags: the cached OSM tags behind a name, for deciding why a row is there.
Each line says whether that name is an index row ([in index]); the cache
holds far more than the index, so a hit without it needs no action.

ids: each OSM id ("way/611143901") with its cached name and whether that name
is an index row. Run it on every id before it goes in a city's
config.PLACE_DROPPED (batch 2b, 2026-10-08: three agents' reads gave about
sixty ids; a wrong one would drop the wrong place silently).

ways: for a city in a NEW language, before its word lists are final: the
named minor ways (footway, path, steps, cycleway, track, bridleway, service)
the way-word test keeps and drops, how many of each carry access=private or
no, and every leak word found on a named object, with examples. The dropped
list is where missing way words show (Hong Kong's terraces 臺, Korean steps
계단); the kept list is where a word too loose shows (batch 2b: English
"court" and "drive" kept 155 private driveways in Seattle). Measure every
built city too before adding a word to a language they share.

added: the names the second query (place_index_fetch.EXTRA_QUERY) put in the
index: stadiums, artworks, civic buildings, airports, beaches, bays, places
as areas. Seattle's brought 91 apartment estates mapped as neighbourhoods.

sizes: what a visitor downloads at the first open of the search (gzip), the
intersections file fetched only for an intersection search, rows by kind.
"""
import collections
import gzip
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

# Place words in English only: in another language, read the whole list, or
# add that language's words here when its first city is read.
PLACE_WORD = re.compile(
    r"\b(park|parks|parkette|reserve|church|chapel|cathedral|temple|mosque|synagogue|gurdwara|parish|"
    r"museum|gallery|garden|gardens|playground|green|square|river|creek|lake|pond|beach|bridge|memorial|"
    r"monument|statue|plaza|trail|field|fields|lookout|mount|mountain|peak|hill|cemetery|university|college|"
    r"conservancy|preserve|forest|woods|island|bay|point|ravine|greenway|commons|common|oval|lawn|"
    r"sculpture|mural|fountain|ministries|assembly|tabernacle|congregation|kingdom hall|masjid|"
    r"zoo|aquarium|library|theatre|theater|observatory|lighthouse|cenotaph|marsh|wetland|slough|"
    r"meadow|meadows|grove|playlot|ballfield|arboretum|conservatory|pier|wharf|dock|harbour|harbor|"
    # French, Catalan, Spanish, Czech and Dutch (batch 2a, 2026-10-08).
    r"parc|église|eglise|chapelle|basilique|cathédrale|oratoire|musée|jardin|jardins|fontaine|"
    r"statue|cimetière|île|mont|colline|bibliothèque|théâtre|plage|marché|monument|stade|"
    r"esplanade|calanque|anse|fort|abbaye|couvent|hôtel de ville|mairie|quartier|"
    r"església|capella|basílica|catedral|museu|jardí|font|platja|biblioteca|teatre|mercat|castell|"
    r"monestir|turó|muntanya|barri|parque|iglesia|museo|jardín|playa|mercado|castillo|"
    r"kostel|kaple|katedrála|bazilika|klášter|muzeum|zahrada|zahrady|sady|hřbitov|vrch|hora|ostrov|"
    r"socha|pomník|divadlo|knihovna|hrad|zámek|synagoga|rotunda|vyhlídka|"
    r"kerk|kapel|kathedraal|basiliek|tuin|fontein|standbeeld|schouwburg|bibliotheek|begraafplaats|"
    r"abdij|wijk|plein|"
    # Mexican Spanish and Portuguese (batch 3, 2026-10-11).
    r"parroquia|templo|capilla|santuario|convento|colonia|pueblo|barrio|deportivo|panteón|monumento|"
    r"estatua|fuente|glorieta|alameda|bosque|cerro|teatro|estadio|universidad|plaza|unidad|"
    r"igreja|capela|paróquia|praça|largo|museu|estádio|cemitério|estátua|mirante|jardim|bairro|vila|"
    r"santuário|mosteiro|catedral|universidade|faculdade|pico|morro|serra|represa|rio|córrego)\b",
    re.I)
# Place words in a script with no word boundary, matched anywhere in the name
# (batch 2b, 2026-10-08): Chinese (Hong Kong), Korean and Georgian. Only
# words of two characters or more, or a temple's: a single 山 or 성 sits
# inside too many estate and district names to shorten the read safely.
PLACE_WORD_ANY = re.compile(
    "公園|遊樂場|花園|廟|寺|教堂|聖堂|博物館|廣場|街市|大學|學院|書院|碼頭|海灘|泳灘|墳場|紀念|"
    "郊野|水塘|石澗|瀑布|海灣|沙灘|球場|運動場|圖書館|劇院|會堂|大會堂|古蹟|遺址|"
    "공원|교회|성당|사찰|박물관|미술관|광장|시장|대학교|호수|저수지|기념|동상|도서관|극장|"
    "경기장|운동장|해수욕장|포구|터널|고개|계곡|유적|서원|향교|궁|능|릉|"
    "პარკი|ეკლესია|ტაძარი|მონასტერი|სინაგოგა|მეჩეთი|მუზეუმი|ბაღი|მოედანი|უნივერსიტეტი|"
    "ხიდი|მთა|ტბა|მდინარე|სასაფლაო|თეატრი|ბიბლიოთეკა|სტადიონი|ძეგლი|ციხე|კოშკი|"
    "გალერეა|სკვერი|უბანი|დასახლება|ხეობა")


def index(city):
    return json.loads(place_index.index_path(city).read_text(encoding="utf-8"))


def config(city):
    return importlib.import_module(f"pipeline.{city}.config")


def elements(path):
    return json.loads(path.read_text(encoding="utf-8"))["elements"]


def odd(city):
    ix = index(city)
    for kind in ("landmark", "place"):
        k = ix["kinds"].index(kind)
        rows = [r for r in ix["rows"] if r[0] == k]
        names = sorted({r[3] for r in rows if not PLACE_WORD.search(r[3] + " " + r[4])
                        and not PLACE_WORD_ANY.search(r[3] + " " + r[4])})
        print(f"== {kind}: {len(rows):,} rows, {len(names):,} without a place word")
        print(" | ".join(names))


def index_names(city):
    return {r[3] for r in index(city)["rows"]}


def tags(city, texts):
    cfg = config(city)
    names = index_names(city)
    skip = ("addr:", "source", "check_date", "survey", "note", "fixme")
    for path in (cfg.PLACE_OSM_JSON, cfg.PLACE_OSM_EXTRA_JSON):
        for e in elements(path):
            t = e.get("tags") or {}
            if any(s in t.get("name", "") for s in texts) and "highway" not in t:
                mark = "[in index] " if t.get("name") in names else ""
                print(mark + e["type"], e["id"], {k: v for k, v in t.items() if not k.startswith(skip)})


def ids(city, wanted):
    cfg = config(city)
    names = index_names(city)
    found = {}
    for path in (cfg.PLACE_OSM_JSON, cfg.PLACE_OSM_EXTRA_JSON):
        for e in elements(path):
            key = f"{e['type']}/{e['id']}"
            if key in wanted:
                found[key] = (e.get("tags") or {}).get("name")
    for key in wanted:
        if key not in found:
            print(f"{key}  NOT IN THE CACHE")
        else:
            n = found[key]
            print(f"{key}  {n}  {'[in index]' if n in names else '(not an index row name)'}")


def ways(city):
    cfg = config(city)
    local = cfg.PLACE_LANGUAGES
    name_tags = place_index._name_tags(local)
    kept, dropped = collections.defaultdict(int), collections.defaultdict(int)
    private = collections.Counter()
    leaks = collections.defaultdict(set)
    for path in (cfg.PLACE_OSM_JSON, cfg.PLACE_OSM_EXTRA_JSON):
        for e in elements(path):
            t = e.get("tags") or {}
            if not t.get("name"):
                continue
            names = place_index._names(t, name_tags)
            word = place_index.leak_word(names, local)
            if word:
                leaks[word].add(t["name"])
            if (e["type"] != "way" or t.get("highway") not in place_index.MINOR_HIGHWAYS
                    or t.get("highway") in place_index.SKIP_HIGHWAY or t.get("area") == "yes"
                    or t.get("service") in place_index.SKIP_SERVICE):
                continue
            keep = bool(t.get("wikidata") or t.get("wikipedia") or place_index._reads_as_way(names, local))
            (kept if keep else dropped)[t["name"]] += 1
            private[(keep, t.get("access") in ("private", "no"))] += 1
    print(f"== named minor ways: kept {len(kept):,} names ({private[(True, True)]:,} ways private), "
          f"dropped {len(dropped):,} names ({private[(False, True)]:,} ways private)")
    print("KEPT: " + " | ".join(sorted(kept)[:300]))
    print("DROPPED: " + " | ".join(sorted(dropped)[:300]))
    print("== leak words on named objects:")
    for w in sorted(leaks, key=lambda k: -len(leaks[k])):
        print(f"   {w} ({len(leaks[w])}): " + " | ".join(sorted(leaks[w])[:8]))


def added(city):
    cfg = config(city)
    base = {(e["type"], e["id"]) for e in elements(cfg.PLACE_OSM_JSON)}
    names = {r[3] for r in index(city)["rows"]}
    out = collections.defaultdict(list)
    for e in elements(cfg.PLACE_OSM_EXTRA_JSON):
        t = e.get("tags") or {}
        if (e["type"], e["id"]) in base or t.get("name") not in names:
            continue
        key = next((f"{k}={t[k]}" for k in ("place", "leisure", "tourism", "amenity", "aeroway", "natural")
                    if k in t), "?")
        out[key].append(t["name"])
    for key in sorted(out):
        print(f"== {key} ({len(out[key])}): " + " | ".join(sorted(set(out[key]))))


def sizes(cities):
    for city in cities:
        main = place_index.index_path(city).read_bytes()
        cross = place_index.crossings_path(city).read_bytes()
        ix = json.loads(main)
        kinds = collections.Counter(ix["kinds"][r[0]] for r in ix["rows"])
        print(f"{city}: first open {len(main):,} bytes, {len(gzip.compress(main, 9)):,} gzipped; "
              f"intersections {len(cross):,}, {len(gzip.compress(cross, 9)):,} gzipped, "
              f"{len(json.loads(cross)['rows']):,} rows; {dict(kinds)}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("odd", "tags", "ids", "ways", "added", "sizes"):
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "odd":
        odd(args[0])
    elif cmd == "tags":
        tags(args[0], args[1:])
    elif cmd == "ids":
        ids(args[0], args[1:])
    elif cmd == "ways":
        ways(args[0])
    elif cmd == "added":
        added(args[0])
    else:
        sizes(args or sorted(p.stem for p in place_index.STATIC_DIR.glob("*.json")))
