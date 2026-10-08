---
name: place-search-city
description: Add place search (the in-map box that finds streets, intersections, stations, lines, neighborhoods and landmarks from an OpenStreetMap index) to a built city's map - the search area, the two Overpass queries, the index step, a new language's word lists and matcher words, the eye read by the place-read agent, review and drop entries, the one re-render, the page bullet, the browser test and the checks - plus the owner's settled calls, the protocol for a rule change that touches built indexes, and the traps the Kyoto pilot and the sample's batches 1, 2a and 2b hit. Use for every city that gets place search (batch 3's size tests, then the site-wide rollout) and for any change to pipeline/place_index.py or the search script. Not for building a city's map (add-city) and not for business registers.
---

# Adding place search to a city

Written 2026-10-08 at the end of the one-city-per-region sample (Kyoto pilot;
batch 1 Seattle, Chicago, Vancouver, Sydney; 2a Montréal, Barcelona,
Marseille, Prague, Brussels; 2b Hong Kong, Seoul, Busan, Tbilisi). It replaces
the recipe sections of `docs/handoff_place_search_2026-10-07.md` and
`docs/handoff_place_search_batch2.md`; the judgment trail, with every owner
quote, is `docs/decisions_drafts/place-search.md` (later `DECISIONS.md`).
Read that file's newest entries before a batch: the owner's open questions
there may have been answered since.

**Until place search lands on master, all of this lives on its branch** (the
worktree once named `charming-lumiere-930853`, moved to `place-search` by
Cleanup); a city is added there, never on master.

## The pieces

| Piece | File |
|---|---|
| Overpass fetch, two queries per city, NOT a step | `pipeline/place_index_fetch.py <city>` |
| Index rules, build and write; word lists per language | `pipeline/place_index.py` |
| A city's index step (runs BEFORE its map step) | `pipeline/<city>/step2b_place_index.py` (copy Sydney's) |
| A city's settings | `PLACE_*` block at the end of `pipeline/<city>/config.py` |
| The search box and matcher (shared, every searched map) | `pipeline/map_common.py`, `PLACE_SEARCH_SCRIPT`, `LANG_WORDS` |
| The map step's one argument | `place_index_url=place_index.index_url("<city>")` |
| The page bullet | `render_map_help(..., search="<city>")` in the city's page |
| The served files (ODbL) | `app/static/places/<city>.json`, `app/static/places/crossings/<city>.json` |
| The page's summary | `outputs/<city>/place_search.json` |
| Every searched map current, languages, ODbL, leaks, junk | `scripts/check_place_search.py` (in `check_all.py`) |
| Every index is what the code builds from its cache | `scripts/check_place_index_drift.py [--against REV]` |
| Reading tools (reports only) | `scripts/place_search_review.py odd / tags / ids / ways / added / sizes` |
| The eye read, one city per call, read-only | the `place-read` agent |

## The owner's calls every city inherits

All quoted in the drafts file; the short list:

- **Places only, never business records; never a home.** A home (residential
  land or building, private access, historic=house or manor on a plain
  building, house=yes, a historic building named as a house in any of the
  city's languages) is kept only when open as a museum or an attraction. A
  Wikipedia article or a heritage listing is not enough ("homes with
  wikipedia: skip").
- **Visitable former homes** go in `config.PLACE_VISITABLE` by id, each with
  its access verdict, an https source and the date checked; check G fails
  after 365 days. Only homes with a sign of visiting or an owner question are
  researched.
- **PRECEDENT, the Panama Hotel:** a notable historic building that still
  houses the business its name carries is kept as a historic site, reviewed
  by name. One OSM tags as the business itself stays out (The Star).
- **Notable places of worship** on residential land or in a residential
  building are back in; a non-notable one stays out (a house church).
- **Languages are measured, never written.** `PLACE_LANGUAGES` declares the
  local language(s); the page names English first, then each local language
  at 50% or more; a declared language under 90% stops the step. English is
  never forced.
- **Notable only** for tourism, amenity and aeroway landmarks, gardens and
  markets (wikidata or wikipedia; gardens also heritage).
- **Squares are landmarks**; a square already findable by a street of its
  name is a duplicate and dropped.
- **Junk names never indexed** (`junk_name`, check F).
- **Stolpersteine never indexed** (a person at their last home).
- **Suggestions are work in progress**: few items, phones first.
- **Any search inside a station's rings must keep working** (the boundary of
  the reserve intersection cut, unused so far).
- **Top-line, still open:** iPhone memory and repository size. Test the
  largest index on a real phone before a big rollout.

## Before a batch

1. `get_usage`: write down the weekly percentage; report it again at the end.
2. Read the drafts file's newest entries, this skill's "Open owner questions"
   below, and `cjk-text` for any Han, kana or Hangul city.
3. **Overpass: one query in flight per session, never parallel; 60 s after a
   504 or 429** (`pipeline/osm.py` enforces the wait per host).

## Each city

1. **The search area, one light query for the whole batch.** Each city's
   boundary relation, the SAME one its step 1 uses (read the config:
   `BOUNDARY_RELATION`, `OSM_BOUNDARY_NAME_EN`, ISO codes), confirmed by id
   with `out tags`; a regional map lists every station city
   (`outputs/<city>/station_municipalities.csv`). Area id = 3600000000 plus
   the relation id: `PLACE_AREA = "(id:3602297418)"`.
2. **The config block** (end of `config.py`; write it with a script that
   writes bytes, LF): `PLACE_AREA`, `PLACE_OSM_JSON` and
   `PLACE_OSM_EXTRA_JSON` under NEW file names dated by the fetch
   (`osm_places_<date>.json`, `osm_places_extra_<date>.json`; data/ is shared
   by every worktree), `PLACE_LANGUAGES`, `PLACE_FOLD` (`"ja"` or `None`),
   `PLACE_REVIEWED = {}`, `PLACE_DROPPED = {}`.
3. **Fetch:** `python pipeline/place_index_fetch.py <city>` (both queries,
   in turn; records provenance). Chain cities one after another in one
   background command; never two at once. Most first attempts are refused
   and answer after the wait; a city whose run fails both rounds is retried
   alone afterwards.
4. **A new language first** (see "A new language" below), then copy
   `pipeline/sydney/step2b_place_index.py`, rename, run it. Read the
   languages line before anything else.
5. **Read:** `place_search_review.py ways <city>` for a new language;
   `added <city>`; then the **`place-read` agent** (one per city, in the
   background, read-only; give it the slug, the languages and a scratch
   folder). A small city (under about 600 landmark and place rows) can be read
   by hand with `odd`.
6. **Act on the read:**
   - A class a rule can catch goes in `place_index.py` (then the rule-change
     protocol below).
   - A single home or business goes in `PLACE_DROPPED` by id with why. **Run
     `place_search_review.py ids <city> <id> ...` first**: every id must
     print the name meant.
   - A real place carrying a leak word goes in `PLACE_REVIEWED` by name with
     why. Check E fails until it does. **Never loosen check E** to clear a
     class: the 2b audit found an exemption hiding five business driveways.
   - A call no precedent covers (a description standing in for a name, an
     exhibit, a private club in a graded building) is an owner question, not
     a drop.
7. **Map step:** add the import and `place_index_url=...` (copy Sydney's
   three lines); `lang=` must already be there for a CJK city.
8. **Page:** `render_map_help(..., search='<city>')`.
9. **Render ONCE per batch**, after every index is final, every searched map
   (the matcher is in every map):
   `python scripts/heavy_job.py run --label <city>-step3 --session <you> --peak-gb 1 --estimate "scaled from kyoto-step3 0.18 GB" -- python pipeline/<city>/step3_map.py`,
   then `sed -i 's/\r$//' outputs/<city>/heatmap.html`. Seoul's render peaked
   at 1.0 GB.
10. **Checks:** `check_place_search.py` (every city OK),
    `check_place_index_drift.py` (every city OK), `check_provenance.py`
    (each new city OK), `check_all.py`. **Commit only when these are green**:
    a commit with stale maps or indexes built under older rules is not a
    baseline.

## The rule-change protocol

Any change to `place_index.py` (a word list, a rule) or the matcher reaches
every searched city.

1. Before the change, note the last commit.
2. After it, rebuild every index (each step2b) and run
   `python scripts/check_place_index_drift.py --against <that commit>`.
3. **A change meant for a new city that changes a built city's index is a
   change to owner-reviewed work.** Read every row it adds and removes; list
   them in the drafts entry and put them to the owner. Measure on every built
   city BEFORE adding a word to a language they share: 2b's twelve English
   street words admitted 354 rows in three built cities, about 40% of them
   private driveways, plus Sydney's shopping arcades, under a comment that
   said each "read as a street".
4. A rule that tests a tag must be scoped to the objects it is about: 2b's
   "station not yet open" test caught every railway=abandoned object and
   removed Prague's historic horse railway.

## A new language

Add, in `place_index.py`, before its first city, each measured against that
city's own data (`ways`, `odd`, `tags`):

- `LEAK_WORDS` (business and home markers; CJK and Hangul match anywhere,
  others as whole words) and `HOME_WORDS` (the subset that marks a home);
  `LEAK_ALLOW` for compounds that are places ("hôtel de ville"; Korean
  "스마트" holds 마트).
- `WAY_WORDS` (a footway or path is kept only when its name reads as a way;
  a language with none keeps no minor way). `SUFFIX_WAY_LANGUAGES` where the
  way word ends a compound (Dutch -straat, Korean -로). `WAY_LEAD` and
  `WAY_ENDING` where street names carry no street word (Czech).
- `HOME_NAME_LEAD` and `HOME_NAME_END` (a historic building named as a
  house: Maison, Casa, Dům; 가옥, 故居, სახლი).
- `SCRIPTS` (a character class) for a language in its own script, and
  `LANGUAGE_NAMES`. `READINGS` for reading tags (Japanese kana).
- In `map_common.LANG_WORDS`: the connector between two streets ("et", "i",
  "y", "a", "en", "და"; none for Chinese and Korean, where it sits inside
  names), articles, street words and leading street words, station words,
  abbreviations that are not prefixes. Station suffixes written onto a name
  (駅, 站, 역) are `STATION_SUFFIX`. Switched on only by the index's declared
  languages, so a Czech "a" never splits an English query.
- `place_search_review.py`'s place words (`PLACE_WORD`, or `PLACE_WORD_ANY`
  for scripts with no word boundary), so `odd` stays readable.

Built so far: ja, en, fr, ca (es searched as well in Barcelona), cs, nl, zh,
ko, ka. Batch 3 needs pt (São Paulo) and es (Mexico City) at full strength;
es has words but has never been a declared language.

## The browser test, once per batch

- A launch entry in the WORKTREE's own `.claude/launch.json` (gitignored;
  `preview_start` reads the session's working directory, not the main
  checkout's): the main checkout's `.venv-lean/Scripts/python.exe`,
  `-m streamlit run app/Overview.py --server.port 8832 --server.headless true
  --server.address 127.0.0.1 --server.enableStaticServing true`. Remove the
  file and stop the server afterwards.
- Search in each city: stations by map name and in the local script (with
  the station word: 金鐘站, 강남역), lines by their legend names, an
  intersection in the city's own style with each connector, landmarks in each
  listed language, a removed row (must find nothing), "#N/A" and "!ERROR!".
  Check that a sample intersection really crosses before calling it a miss.
- Read results through the page, never screenshots, on a city page:

```js
const QUERIES = ["Station", "Street A and Street B", "Landmark", "#N/A"];
await new Promise(r => setTimeout(r, 8000));
const f = [...document.querySelectorAll('iframe')].find(f => { try { return f.contentDocument.querySelector('.hm-search-input'); } catch (e) { return false; } });
const d = f.contentDocument, w = f.contentWindow, box = d.querySelector('.hm-search');
d.querySelector('.hm-search-btn').click();
const input = d.querySelector('.hm-search-input'), out = {};
for (const q of QUERIES) {
  input.value = q; input.dispatchEvent(new w.Event('input', {bubbles: true}));
  for (let k = 0; k < 200; k++) { await new Promise(r => setTimeout(r, 50)); const n = d.querySelector('.hm-search-note'); if (!n || !/Loading/.test(n.textContent)) break; }
  await new Promise(r => setTimeout(r, 400));
  out[q] = [...d.querySelectorAll('.hm-search-list [data-i]')].slice(0, 3).map(e => (e.getAttribute('title') ? '[' + e.getAttribute('title') + '] ' : '') + e.textContent.trim().replace(/\s+/g, ' ')).join(' ; ') || ((d.querySelector('.hm-search-list .hm-search-note') || {}).textContent || '(nothing)');
}
out._loadMs = box.getAttribute('data-load-ms'); out._crossingsMs = box.getAttribute('data-crossings-ms');
out
```

- The console's 404s for `/<Page>/_stcore/health` and `host-config` are
  Streamlit's own probes before the root path answers; check the network
  list shows each index and intersections file at 200.

## Closing a batch

- A drafts entry, newest first (`decisions-entry` format): what was built,
  every call, the rows rule changes moved in built cities, the eye reads'
  drops, the measured sizes, the browser test and its gaps, the weekly usage
  before and after, numbered questions for the owner.
- `check_all.py`; commit; never `git add -A` (stage the paths listed by
  `git status`); `git status` clean and the worktree ON its branch, not a
  detached HEAD; nothing pushed; servers stopped.
- Tell Cleanup in one message; HOLD for the owner before the next batch.

## Traps

- **The Edit and Write tools decode `\u` escapes**; JS character classes are
  built in Python (`map_common._js_ranges`). **No backslash or backtick in a
  heredoc or `python -c`** (the hook blocks it): write a script file.
- **Editing configs with a regex** spanning `PLACE_REVIEWED = {}` matched
  into `PLACE_DROPPED`'s closing brace (2b): replace exact text, and assert
  the count.
- **An agent's ids are claims**: `ids` before `PLACE_DROPPED`.
- **A tag the rules trust can lie**: Seoul has apartment complexes tagged
  historic=castle, a restaurant's plaque tagged a monument, eleven
  fortune-tellers tagged places of worship. The eye read is not optional.
- **tourism=attraction makes a home public** under the current rule
  (Tbilisi's heritage houses, Casa Batlló); a house known not to be open
  despite it goes in `PLACE_DROPPED` with the evidence.
- **Do not use `korean_names.looks_like_personal_name`** here: without its
  address test it reads 이태원 and 강남역 as people.
- **Hong Kong's `name` is "中文 English"** in one string; languages are
  credited from the script and name:en, nothing parsed from the string.
- **A Korean way-word ending is loose** (상가진입로, a shopping arcade's entry
  road, ends in 로): the named-street rule takes a whole word in Korean.
- **highway=construction is skipped**, which loses streets being rebuilt
  (Tbilisi's Rustaveli Avenue) as well as roads not yet open (owner question).
- **A static file is cached by the browser**: the map carries the index's
  content hash, so every index rebuild means a re-render (check A).
- **Windows writes CRLF**: write bytes; `sed -i 's/\r$//'` after renders.
- **data/ is a junction shared by every worktree**: never re-run a city's
  steps 1 and 2 from the branch; caches go under new file names.
- **Map station names come from the map**, joined to OSM's in the browser,
  never in the file (ODbL 4.4(d)): nothing non-OSM enters an index.

## Open owner questions (as of 2026-10-08; check the drafts file)

The 2b entry's nine: built indexes the 2b rules changed; descriptions
standing in for names; museum exhibits; glitched names; private minor ways;
streets under reconstruction; religious residences; Hong Kong's Pillar of
Shame; homes public on tourism=attraction alone. Earlier and still open: the
WIP suggestion tuning, the corner credit test, the Cities menu move, and
whether "Download this index" also links the intersections file.

## Batch 3, the size tests

Tokyo, London, Paris, São Paulo, Mexico City. Measure each first open and
intersections file (`sizes`) against Seoul's 387 KB and 247 KB gzipped, and
test the largest on a real phone before the rollout. The reserve intersection
cut (rings plus main roads, `PLAN.md`) is the fallback if one is too heavy.
Tokyo's 23 wards need the ward relations (`rel(area.東京都)["admin_level"="7"]["name"~"区$"]`).
