"""Place search: the reading a city's index needs before it is published, as
the sample's first batch did it (2026-10-08). REPORTS only; changes nothing.

    python scripts/place_search_review.py odd <city>              # names to read by eye
    python scripts/place_search_review.py tags <city> <text> ...  # OSM tags of named objects
    python scripts/place_search_review.py added <city>            # what the extra query brought
    python scripts/place_search_review.py sizes [<city> ...]      # bytes, gzip, rows by kind

odd: every landmark and place whose names hold no obvious place word (park,
church, museum ...). Brand names and homes carry no leak word, so this is the
list that found Sydney's "Meriton" park, Vancouver's register of heritage
houses, Chicago's "Lawrence House Patio" and Seattle's yoga studio. Read it
whole; a find that no rule in pipeline/place_index.py can catch goes in the
city's config.PLACE_DROPPED by OSM id, with why.

tags: the cached OSM tags behind a name, for deciding why a row is there.

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
    r"meadow|meadows|grove|playlot|ballfield|arboretum|conservatory|pier|wharf|dock|harbour|harbor)\b",
    re.I)


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
        names = sorted({r[3] for r in rows if not PLACE_WORD.search(r[3] + " " + r[4])})
        print(f"== {kind}: {len(rows):,} rows, {len(names):,} without an English place word")
        print(" | ".join(names))


def tags(city, texts):
    cfg = config(city)
    skip = ("addr:", "source", "check_date", "survey", "note", "fixme")
    for path in (cfg.PLACE_OSM_JSON, cfg.PLACE_OSM_EXTRA_JSON):
        for e in elements(path):
            t = e.get("tags") or {}
            if any(s in t.get("name", "") for s in texts) and "highway" not in t:
                print(e["type"], e["id"], {k: v for k, v in t.items() if not k.startswith(skip)})


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
    if len(sys.argv) < 2 or sys.argv[1] not in ("odd", "tags", "added", "sizes"):
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "odd":
        odd(args[0])
    elif cmd == "tags":
        tags(args[0], args[1:])
    elif cmd == "added":
        added(args[0])
    else:
        sizes(args or sorted(p.stem for p in place_index.STATIC_DIR.glob("*.json")))
