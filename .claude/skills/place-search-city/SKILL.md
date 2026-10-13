---
name: place-search-city
description: Add place search (the in-map box that finds streets, intersections, stations, lines, neighborhoods and landmarks from an OpenStreetMap index) to a built city's map - the search area, the two Overpass queries, the index step, a new language's word lists and matcher words, the eye read by the place-read agent, review and drop entries, the one re-render, the page bullet, the browser test and the checks - plus the owner's settled calls, the protocol for a rule change that touches built indexes, and the traps the Kyoto pilot and the sample's batches 1, 2a, 2b and 3 hit. Use for every city that gets place search (the site-wide rollout, once the owner's phone test of the largest index has passed) and for any change to pipeline/place_index.py or the search script. Not for building a city's map (add-city) and not for business registers.
---

# Adding place search to a city

Written 2026-10-08 at the end of the one-city-per-region sample (Kyoto pilot;
batch 1 Seattle, Chicago, Vancouver, Sydney; 2a Montréal, Barcelona,
Marseille, Prague, Brussels; 2b Hong Kong, Seoul, Busan, Tbilisi), updated
2026-10-11 after batch 3 (Tokyo, London, Paris, São Paulo, Mexico City) and
the owner's answers to 2b's nine questions. It replaces
the recipe sections of `docs/handoff_place_search_2026-10-07.md` and
`docs/handoff_place_search_batch2.md`; the judgment trail, with every owner
quote, is `DECISIONS.md` and `docs/decisions/2026-10-04.md` (the pilot's
drafts file, folded 2026-10-12).
Read that file's newest entries before a batch: the owner's open questions
there may have been answered since.

**Until place search lands on master, all of this lives on its branch** (the
worktree `.claude/worktrees/place-search`, branch `place-search`; both once
named `charming-lumiere-930853`, moved by Cleanup 2026-10-08); a city is added there, never on master.

## The rollout: the cheap path (the owner's ruling, 2026-10-12)

Written by Cleanup at the phase 2 landing, when place search reached master
with 19 cities and 218 were left, and made the ruling for the rollout by the
owner the same day (`DECISIONS.md`, 2026-10-12, "The search rollout's cheap
path"). Where it differs from the sections below, THIS section wins for the
rollout; the owner's calls on what an index may hold are unchanged. Lines
marked TO BUILD name a script that does not exist yet.

**Where a city's cost sits.** Measured by kind, not yet by tokens:

| Step | Needs a model |
|---|---|
| Search area, languages, fold in the config; the thin step2b | No |
| The two Overpass queries | No (slow by the one-query rule, no tokens) |
| Index build, languages, summary, page bullet | No |
| The eye read and what it turns into (drops, reviews, questions) | Yes |
| Visitable former homes | Yes, with web checks |
| Re-render and browser test | Once per wave |

**The path, per wave:**

1. **The size projection comes before the first wave.** 19 indexes are
   39.2 MB raw, about 2 MB a city; 237 at that rate is roughly 475 MB, an
   extrapolation. `place_search_review.py sizes` gives the measured figures;
   the wave order is the owner's, on that number.
2. **Scaffold the wave in one script** (built 2026-10-12,
   `scripts/place_search_scaffold.py --plan <plan.json> [--write]`): each
   city's `PLACE_*` block and its step2b, the map step's argument and the
   page's `search=`. The plan file is a session's: per city its relation
   ids, languages and fold (the script's docstring has the shape); the
   script decides nothing and refuses a city that does not fit the pattern.
   Run it without `--write` first. **A scaffolded city fails
   `check_place_search.py` until its fetch, index step and render are done,
   so scaffold a wave on its own branch and push nothing until the wave is
   built.**
   The area follows the scope rule ("The search area" under "Each city"):
   the boundary the map's businesses are cut to, plus every station
   municipality on a regional map, and nothing wider. Languages from
   `pipeline/travel_packs.LOCAL_LANG`, then MEASURED by the step as always.
   The area ids are still confirmed by one light query for the wave.
3. **Fetch as an unattended queue** (built 2026-10-12,
   `scripts/place_search_fetch_queue.py`, over `place_index_fetch.py`; `--dry-run` first, `--retries N` for a wave holding a `PLACE_SPLIT` city, a child stopped after 180 min): one
   city after another, the wait after a 504 or 429, a log line per city, a
   retry list at the end. **The one-query rule is a LOCK in the fetch
   script** (`FetchLock`, built 2026-10-12; `--wait MINUTES`), not a hook: a lock guards the queue and anything an
   outside model drives; a hook guards only a Claude session. No session
   needs to be open while it runs.
   **Two queues, one per Overpass mirror** (owner, 2026-10-12;
   `docs/rule_history.md`, #overpass): `--host overpass-api.de` and
   `--host overpass.kumi.systems`, each its own heavy job with its OWN city
   list. Never the same city in both. The large cities and every
   `PLACE_SPLIT` city go to `overpass-api.de` (kumi has timed out on heavy
   queries); the small and middle ones to kumi. A pinned child asks its one
   mirror for the whole city and holds only that mirror's lock; a queue with
   no `--host` holds both and runs alone.
4. **Build every index of the wave**, then read the languages lines and
   `street_dropped_leak_word` for any language's first city in a country.
5. **The eye read stays; a cheaper model reads first.** "The eye read is
   not optional" (Traps) holds. After the DeepSeek integration: a first
   pass by the cheaper model, one request per city, given the rows
   `place_search_review.py odd` and `tags` already select and a fixed rubric
   (home, business, description for a name, glitched name, exhibit, real
   place), returning JSON: id, name as cached, class, the tag it rests on.
   Then `ids` confirms every id against its cached name, as for any agent's
   claims. The `place-read` agent reads only a city whose first pass
   returns a class no rule or precedent covers, and a sample of the rest.
   Try it on three built cities whose reads are on record (Kyoto, Seoul,
   Paris) and compare before any new city relies on it. Place names from
   OpenStreetMap may go to an outside model; nothing from a business
   register may, and no key enters the repository.
   **Which model reads what (owner, 2026-10-13):** the `place-read` agent
   on the session's top model for station, junction, place and landmark
   rows; a Sonnet-tier `place-read` (the Agent tool's `model: sonnet`) for
   the street screen, one city per call. Measured on Birmingham, Boston and
   Tacoma against wave 1's applied drops: Sonnet found 34 of 38 dropped
   street names and 43 of 77 dropped ids, Haiku 15 of 38 and 32 of 77. The
   test indexes predated the rules of 2026-10-13, which now drop several of
   the missed classes; re-measure before moving the place and landmark rows
   to a lower tier. Haiku reads nothing.
6. **Visitable former homes are left out of the rollout**: the home rule
   already keeps homes out, and `PLACE_VISITABLE` is added later for the
   cities the owner names.
7. **A new language is still done first and by hand** ("A new language"
   below), and the rule-change protocol still applies in full: a word added
   for a new city is measured on every built city of that language.
8. **One re-render and one browser test per wave.** The render is every map
   (the matcher is shared), through the heavy-job gate. The browser test
   samples a few cities of the wave, not all.

**What the phase 2 landing's lanes learned (2026-10-12), for the browser
test and any deploy-verify lane on a searched map:**

- A lane server started from another worktree does not read the tree's
  `.streamlit/config.toml`: without `--server.enableStaticServing true` the
  index URL returns Streamlit's HTML shell with status 200 and every map
  falls back to stations only. Confirm `/app/static/places/<city>.json`
  returns JSON before any search test.
- **The deployed app is not at the host's root.** Streamlit Community Cloud
  serves it under `/~/+/`, so the index is at
  `/~/+/app/static/places/<city>.json`. From the landing until the owner's
  London report the map asked the root, the index never loaded, and the live
  search answered with the map's own stations and lines only, while every
  local test passed. The search script now takes the prefix from the page's
  own path (`BASE` in `PLACE_SEARCH_SCRIPT`). **After every push that touches
  a searched map, type a street name into the deployed box**; a reachable
  index file proves nothing about the address the map asks.
- The Travel file host answers only the live app and localhost or 127.0.0.1
  on ports 8501 and 8000. A lane on any other port sees a CORS refusal and a
  blank Travel basemap, which is the port and not a defect.
- In a hidden browser pane `requestAnimationFrame` never fires: Leaflet's
  animated moves stall and the Travel map never loads its style. Prepend a
  16 ms timer stand-in to the map's `srcdoc`, load it in a frame of exact
  size, and scroll with `behavior: "instant"` (the map document sets smooth
  scrolling).
- Closing the search box leaves the map at the found place; the mark and the
  fade end on the 12 s timer or the next search. The owner accepted this
  (2026-10-12); a return-to-start button is an idea in `PLAN.md`.

**Stale below once the landing is on master:** "Until place search lands on
master, all of this lives on its branch". After the landing, a wave gets a
branch of its own from master; the `place-search` worktree is retired only
on the owner's word.

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
| Stations OSM draws as not yet open (an internal watch file) | `docs/place_search_unopened_stations.json` |
| The watch file says what the last index builds skipped (in `check_all.py`) | `scripts/check_place_unopened.py` |
| The eye read, one city per call, read-only | the `place-read` agent |

## The owner's calls every city inherits

All quoted in the drafts file; the short list:

- **The suggestion list, as tuned on the live site (owner, 2026-10-12;
  `PLACE_SEARCH_SCRIPT`, every searched map, so a change is one re-render of
  them all):**
  - *Same-named streets carry their neighborhood in parentheses*, nearest
    the middle of the view first: "Brick Lane (Mile End New Town)". The
    neighborhood is the nearest `place` row within 4 km (`NEAR_PLACE_M`), as
    OpenStreetMap names it; a unique name is unchanged. Most repeats are
    other streets, not stretches: London has four Brick Lanes and 56 High
    Streets.
  - *Stretches of one street within 600 m are one row* (`STRETCH_M`,
    `oneRowAStreet`), opening on all of them. Measured on the 19 indexes:
    London 55,283 street rows to 55,003; Chicago 4,643 to 3,689.
  - *Ranking, best first*: the name itself; a name holding the whole phrase
    ("Avenida Paseo de la Reforma"); an alternate name that is the phrase;
    a name the phrase begins. Regression queries to re-run after any change:
    "Paseo de la Reforma" (Mexico City), "Sanjo Street" and 三条通 (Kyoto),
    "Damen and North", "Clark and Lake", "Art Institute" (Chicago), "Brick
    Lane", "Oxford Street" (London).
  - "Lake Shore Dr" (Chicago) lists the Drives, not the Lake Shore Drive
    Synagogue: the typed street type's bonus goes to streets only (fixed
    2026-10-12; a regression query). The four-letter gate, streets ranked
    after other kinds, and the places group folded on a phone are "good for
    now" (owner, 2026-10-12).
  - **To rank-test without a browser**: cut the search script out of a
    rendered map and run it on the index with Node (the scratch harness of
    2026-10-12 slices from `var KIND_RANK` to `function isOwn`, stubs the
    map and prints each result's score). It found in one run what reading
    the code had not.
- **Street coverage is measured, not assumed**: distinct street names in the
  index against named highway ways in the cache run 85 to 99% on 18 built
  cities and 72% in Tokyo, where 812 of the 1,203 names left out are
  footways (station entrances, taxi stands, plazas). A new city under 85%
  gets the same breakdown by highway class before it lands.

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
- **Stolpersteine never indexed** (a person at their last home), nor a tomb
  named for a family (`FAMILY_TOMB`: Paris's cemeteries are mapped tomb by
  tomb, 43 of them under private families' names).
- **A name that is only its object's type is no name** (owner, 2026-10-11):
  `BARE_TYPE_NAMES`, per language, matched as the whole name on landmarks and
  places (놀이터, 祠堂, 本殿, "Monument", "Édicule Guimard"). An object whose
  main name is bare goes whole. A description longer than a type word ("open
  area with bench") goes in `PLACE_DROPPED` by id.
- **A code plus a type is no name either** (owner, 2026-10-12: "yes drop"):
  a parcel or building code beside a type word ("54F - Greenbelt", "103D -
  Utility ROW", "Building 30", "10. zastavení"). `CODED_TYPE` in
  `place_index.py`, built 2026-10-12, matched as the whole name and kept
  narrow on purpose: a leading parcel code needs its spaced dash or a listed
  type word, so "5th Avenue Theatre" and Chicago's "Park 399" stay. **A
  registered code is a name** (owner, the same day): a landmark carrying
  wikidata, wikipedia, `heritage` or `ref:nrhp` keeps its coded name
  (`REGISTERED_KEYS`), so Seattle's 27 National Register buildings at Sand
  Point and the Locks and Prague's 14 Stations of the Cross on Petřín stay;
  the rule takes Surrey's park parcels from Vancouver (83 rows with the type
  words) and a park lot from Busan. The same change added 41 bare type words
  the outside net found and dropped 23 objects by id (five glitched names,
  one house, descriptions); 149 rows left 16 of the 19 built indexes, none
  were added. **A title is not a type**: "Crossing", "Rectangle", "Vodopád"
  and "Rozhledna" are notable artworks' titles and stay, so a viewpoint
  under the word "Rozhledna" went by id, not by the word. Measure each new
  word or pattern on its built cities first.
- **The outside name review is a second net, never the first pass** (owner,
  2026-10-12): `scripts/place_name_net.py` stages a commit's index names and
  collects the replies; the prompt is `scripts/place_name_net_prompt.md`.
  It sees names only, so every flag is checked against the object's tags
  before anything is dropped: on the 19 built cities nearly every flagged
  estate, house and venue was a correct keep (a neighbourhood node, a museum
  with wikidata, a notable theatre). Each call needs the owner's yes.
- **Museum exhibits are not landmarks** (owner, 2026-10-11):
  `EXHIBIT_HISTORIC` (aircraft, tank, cannon, missile, rocket, vehicle,
  locomotive, railway_car) needs the object's own wikidata, and the
  mass-produced ones a tourism tag as well; a painting hung indoors is an
  exhibit whatever its wikidata. Ships, wrecks and historic railways stay.
- **No glitched name goes live, and none is repaired** (owner, 2026-10-11): a
  corrected name would not be OSM's. Where `name` carries a third script and
  a local-language name exists, that name leads (`_local_first`); every other
  glitch (cut short, stray characters, a wrong object's name) is dropped by
  id. A name that states the same thing in two languages either side of a
  separator, each part one of the object's own name:<language> values, is no
  glitch and stays whole.
- **Private minor ways are no streets** (owner, 2026-10-11): a street whose
  every way is a footway, path, track or service road with access=private or
  no, none notable, goes with its crossings. **Except a private street named
  as a residential street** ("keep those streets"): `PRIVATE_STREET_LEAD`,
  French so far (villa, cité, square, impasse, hameau). A new language's
  words are measured on its built cities first, and never include an access
  or service road's word.
- **A housing estate named as one needs wikidata or an article**
  (`ESTATE_NAME`, English "X Estate"; owner, 2026-10-11), and **a hamlet
  whose population tag is under 50 goes** unless notable
  (`HAMLET_MIN_POPULATION`, site-wide; one with no population tag stays).
- **Streets closed for rebuilding** are kept by name in `config.PLACE_REBUILT`
  (owner, 2026-10-11; Tbilisi's Rustaveli Avenue); a name no construction way
  carries stops the step.
- **Religious residences are held to the worship precedent, BY ID, never by a
  rule** (owner, 2026-10-11): a convent, monastery, seminary, priests' house
  or 精舍 tagged a place of worship is dropped in `PLACE_DROPPED` unless
  notable. No rule can tell a monastery that is a residence from a temple.
- **A removed object is dropped by id** (owner, 2026-10-11, Hong Kong's
  Pillar of Shame): a search must not move the map to a place where the
  thing is not.
- **The rules of 2026-10-13 (landed 86aadced) made rules of what the eye
  read used to drop by id.** `docs/place_search_exclusions.md` is the record
  of every class left out, with its rule and date: read it before a read,
  and add a row there in the same commit as any new class. What changes for
  a builder:
  - **Not there is a rule now**, not an id: a landmark or place demolished,
    razed, removed or abandoned by its own tags goes (`lifecycle`), a closed
    station goes (`station_closed`), a ride tagged a station goes
    (`station_ride`). The rule reads the tags narrowly, so a vanished thing
    the tags do not mark is still a `PLACE_DROPPED` id. A `PLACE_DROPPED` id
    that matches no row after a rebuild is expected: remove the entry.
  - **A place that stands and is closed for works is kept by id** in
    `config.PLACE_CLOSED_FOR_WORKS` (owner, 2026-10-13: a Paris museum, a
    Seattle library branch and a playground). Read every row the not-yet-open
    test drops in a new city for this class; no tag separates them.
  - **A grave or a plaque needs a Wikipedia article of its own**
    (`grave_or_plaque`, `own_article`); a Wikidata entry alone admits none,
    and an article that is the person's is not the grave's. Statues, busts
    and public memorials are untouched. Where the tags cannot say whose the
    article is, the row stays as it was: do not decide those by eye.
  - **Private streets go by rule** on residential and unclassified ways too
    (`street_public`), with busways and race tracks (`street_real`) and
    minor-way streets named by a description (`street_description`). A way's
    own article keeps one.
  - **A tram stop's platforms are one row** (`PLATFORM_MERGE_M`); an
    interchange stays two.
  - **A district with an article of its own is a neighborhood**, so read the
    rows `added` lists for a county or district that only borders the city
    and drop it by id (Prague's two).
  - **Misspelled names are never corrected**; the page says so.
- **A station OSM draws as not yet open is no station**, and is recorded in
  `docs/place_search_unopened_stations.json` (owner, 2026-10-11: an internal
  watch file, never page text). A station leaves the file when OSM marks it
  open and its city's index is rebuilt from a new cache.
  `scripts/check_place_unopened.py` fails until the file matches what each
  index step skipped (`stations_not_open` in `outputs/<city>/place_search.json`):
  add a row for a new one, with its line and where the line came from
  (relation, tag or a published source; null with a reason, never a guess).
- **Suggestions are work in progress**: few items, phones first.
- **Any search inside a station's rings must keep working** (the boundary of
  the reserve intersection cut, unused so far).
- **Top-line:** repository size is still open. iPhone memory: the owner's
  phone test of São Paulo, the largest index (1,229 KB first open), passed
  on 2026-10-11; a city much larger than that is tested again first.

## Before a batch

1. `get_usage`: write down the weekly percentage; report it again at the end.
2. Read the drafts file's newest entries, this skill's "Open owner questions"
   below, and `cjk-text` for any Han, kana or Hangul city.
3. **Overpass: one query in flight per mirror, each pinned to its mirror
   (`--host`); an unpinned fetch runs alone; 60 s after a 504 or 429**
   (`pipeline/osm.py` enforces the wait per host; the fetch script's lock per
   mirror enforces the rest).

## Each city

1. **The search area: the scope rule (owner, 2026-10-12).** An index covers
   exactly the municipalities its map covers, and the map draws that area's
   outline while the search box is open. Work it out in this order, and
   write down which case each city is:
   - **The floor: the boundary the map's businesses are cut to.** Read the
     city's config for what step 1 or step 2 clips to (`BOUNDARY_RELATION`,
     `OSM_BOUNDARY_NAME_EN`, a TIGER GEOID, an ISO code), then find the OSM
     relation of that SAME place. A county is not the city inside it: the
     wave 1 plan gave Buffalo Erie County where the map is cut to the City
     of Buffalo, and its fetch failed on the size (2026-10-12).
   - **A regional map adds every municipality a drawn station sits in**
     (`outputs/<city>/station_municipalities.csv`), each by its own
     relation. Not the county or metropolitan area that holds them.
   - **A station on unincorporated land** adds the smallest named area that
     holds it (a census-designated place, a township), recorded in the
     config beside `PLACE_AREA` with the station's name.
   - **Nothing wider without the owner's word.** A municipality with none
     of the map's stations is refused by `scripts/check_place_scope.py`
     unless `PLACE_AREA_KEPT = {"relation/123": "why, who, when"}` in the
     config records the reason: the owner's ruling, or the business
     boundary itself on a map whose stations all sit outside it. Bring its
     measured index size with the request.
   - **Confirm every relation by id in one light query for the batch**
     (`out tags`): the name, `boundary=administrative` and the admin level
     are what the config says. Area id = 3600000000 plus the relation id:
     `PLACE_AREA = "(id:3602297418)"`, several as `"(id:A,B,C)"`.
   - **Two checks hold it, floor and ceiling.** `check_place_search.py` H
     fails an index that stops short of a station (Mexico City,
     2026-10-12); `check_place_scope.py` fails one that reaches a
     municipality with no station and no recorded reason. The index step
     counts stations per municipality into `outputs/<city>/place_search.json`
     ("area"): read that list after the first build, before the eye read.
   - **The index step also writes `outputs/<city>/place_ids.json`** (owner,
     2026-10-12, for the travel app): the OSM id behind each station,
     junction, landmark and neighborhood row, by row position, with the
     sha256 of the index it describes. Commit it with the index; no browser
     fetches it. `check_place_search.py` I holds it to its index.
   - **The index step also writes the street lines file**
     (`app/static/places/streets/<city>.json`, owner 2026-10-13): a picked
     street is drawn at its whole length, and the ring stays where no line
     can be drawn. Commit it with the index and follow the
     **`place-street-lines` skill** for the size line, rule J and the one
     street to pick in the browser test.
   - **Look at the outline once**, in the browser test: open the search box
     and see that the dashed line holds every station and no stray island
     or missing municipality. The outline is exterior rings only, simplified
     by 40 m, parts under 0.2% of the area left out
     (`place_index.OUTLINE_SIMPLIFY_M`, `OUTLINE_MIN_SHARE`).
2. **The config block** (end of `config.py`; write it with a script that
   writes bytes, LF): `PLACE_AREA`, `PLACE_OSM_JSON` and
   `PLACE_OSM_EXTRA_JSON` under NEW file names dated by the fetch
   (`osm_places_<date>.json`, `osm_places_extra_<date>.json`; data/ is shared
   by every worktree), `PLACE_LANGUAGES`, `PLACE_FOLD` (`"ja"` or `None`),
   `PLACE_REVIEWED = {}`, `PLACE_DROPPED = {}`.
3. **Fetch:** `python pipeline/place_index_fetch.py <city>` (three queries
   in turn, **the boundary first** (owner, 2026-10-12): the area's
   boundaries with their geometry, `osm_place_outline_v1.json`, then places,
   then the extra classes; records provenance). The fetch counts the map's
   stations per municipality on the boundary and **stops before the two
   heavy queries** when one holds none and has no `PLACE_AREA_KEPT` entry,
   or when a boundary does not close. A place answer whose data is over 7
   days old is refused and the next mirror asked (`PLACE_MAX_AGE_DAYS`):
   read `osm_base` in the provenance after a fetch. A city fetched before
   2026-10-12 lacks the boundary: the queue sees that and fetches only it.
   Chain cities one after another in one
   background command; never two at once. Most first attempts are refused
   and answer after the wait; a city whose run fails both rounds is retried
   alone afterwards. **A city too large for one answer** (the server's own
   timeout, a "remark" in the log: São Paulo's 724,666 elements, London's
   1,066,979; Mexico City's 402,007 answered whole in about 170 s) gets
   `PLACE_SPLIT = {"bbox": (s, w, n, e), "rows": R, "cols": C}` in its
   config: `fetch_split` asks the first query once per tile, each still cut
   by `PLACE_AREA`, keeps each tile's answer beside the cache so only a
   refused tile is asked again, and merges by OSM id. Re-run the script
   until every tile is in.
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

- `BARE_TYPE_NAMES` (the type words that stand in for names; measure each on
  every built city of the language first) and, where estates are mapped as
  places, `NUMBERED_BLOCK`.

Built so far: ja, en, fr, ca (es searched as well in Barcelona), cs, nl, zh,
ko, ka, es (declared since Mexico City) and pt (São Paulo).

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
- **highway=construction is skipped**: a street being rebuilt goes in
  `config.PLACE_REBUILT` by name (Tbilisi's Rustaveli Avenue); a road not yet
  open stays out. Only a missing famous street shows the need.
- **The fade picks the business dots out by how they are drawn** (paths with
  fill-opacity 0.85 and a 1 px stroke), since a class on them would change
  every map's script and make the unsearched maps stale. If the dots'
  drawing changes in `map_common`, the selector in the search's styles
  changes with it.
- **A CSS transition does not advance in a hidden browser pane**: a test that
  reads an opacity right after a class change sees the old value. The fade
  has none.
- **Leaflet's tooltip pane is hidden on a touch screen** (the tap script):
  anything the search must show on a phone goes in a pane of its own, as the
  found place's name label does. A desktop test does not see the difference.
- **A static file is cached by the browser**: the map carries the index's
  content hash, so every index rebuild means a re-render (check A).
- **Windows writes CRLF**: write bytes; `sed -i 's/\r$//'` after renders.
- **data/ is a junction shared by every worktree**: never re-run a city's
  steps 1 and 2 from the branch; caches go under new file names.
- **Map station names come from the map**, joined to OSM's in the browser,
  never in the file (ODbL 4.4(d)): nothing non-OSM enters an index.

- **A leak word in one country is a street type in another**: "privada" as a
  Spanish leak word dropped 4,393 of Mexico City's streets (a Privada is a
  cul-de-sac there). Read `street_dropped_leak_word` after the first build
  of a language's first city in a new country.
- **A rule on a tag value takes whatever carries it**: "a painting is an
  exhibit" took Prague's Lennon Wall (artwork_type=painting, on a street)
  until it was scoped to indoor ones. The moved-rows check
  (`check_place_index_drift.py --against`) is what caught it: read it after
  every rule, not only at the end.
- **Wikidata is not always the object's own**: Seoul's tanks carry their
  MODEL's item, São Paulo's clinic the article for clinics, Paris's tombs an
  item for the tomb. "Notable" by wikidata alone lets these in.
- **`PLACE_LANGUAGES = ()` names no language on the page**: an English city
  declares `("en",)`, as Seattle and Sydney do.
- **`PLACE_DROPPED` reaches ways too** (since batch 3): a business's or a
  development's own road drawn as a street can be dropped by its way id.
- **The reads screen, they do not read everything**, in a large city: Tokyo's
  6,300 names ending 公園, 神社 and 寺 and London's 1,640 parks were filtered,
  not read line by line. Say so in the drafts entry.

## For the audit after the rollout (owner, 2026-10-11)

- Names cut short or mistyped: only an eye read finds them, and batch 3's
  reads listed about 150 plain typos they did not drop.
- access=no on a trail can be a closure, not private land (Hong Kong's
  country-park paths went with the private minor ways).
- Lesser streets under reconstruction are in no keep-list.
- Tokyo's 今戸神社 is out (Cyrillic words before its name in OSM, no Japanese
  name tag to lead) until OSM is fixed.

## Open owner questions (as of 2026-10-11; check the drafts file)

2b's nine and batch 3's ten are answered (the calls above; the phone test
passed). **Monuments and galleries are handled by id** (owner, 2026-10-11):
holding historic=monument to the notable rule, or treating a gallery without
a Wikipedia tag as a dealer, was measured and NOT applied (it removed Seoul's
King Sejong statue and its Museum of Art, among about 420 rows). A dealer's
gallery is the business itself whatever its article; a public or charitable
gallery stays. **The found place's marker** (owner, 2026-10-11) sits in its
own pane above the dots, with a casing and the dark accent on the dark map,
and the dots, cluster bubbles and heat fade to 28% while it shows; they are
never switched off. A picked line (search, legend row or tap) fades them
too, with a casing under the line and a boxed label, until it is unpicked:
built in the search script, which watches the legend rows, so an unsearched
map's legend pick is unchanged until the rollout reaches it (owner,
2026-10-11: it lands with the rollout). The outline is black on the light
map and white on the dark one. With Cleanup
for review
time: the WIP suggestion tuning, the corner credit test, the Cities menu
move, and whether "Download this index" also links the intersections file.

## Batch 3, the size tests: the result (2026-10-11)

First open and intersections file, gzipped, against Seoul's 383 KB and 247 KB:
São Paulo 1,229 and 785 KB (3.2 times Seoul on both, the largest); London
1,199 and 709; Mexico City 877 and 643; Tokyo 325 and 35 (most of its
streets carry no name); Paris 181 and 94. The nineteen cities' files are
39.2 MB raw. **The owner's phone test of São Paulo passed (2026-10-11).**
The reserve intersection cut (rings plus main roads, `PLAN.md`) stays
unbuilt and unused. Tokyo's 23 wards are their own relations (admin_level 7, names
ending 区, inside ISO3166-2 JP-13), listed in `pipeline/tokyo/config.py`.
