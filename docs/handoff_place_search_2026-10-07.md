# Handoff: place search, the Kyoto pilot (2026-10-07)

For the session that takes place search on from here: the review-time testing
and tuning, landing it, then the rollout to other cities. Written by the
pilot session the owner opened on 2026-10-07 (DECISIONS, "Four ideas assessed
before the large review", item 3).

**State:** built and approved for Kyoto ONLY, on branch
`claude/charming-lumiere-930853` (worktree
`.claude/worktrees/charming-lumiere-930853`), the commits from `b2e4a8a4` on, on top of
`8cf5ed4c`. **Nothing is pushed and nothing is on
master.** It lands at review time (PLAN.md, "Review time: the place search
pilot"), which only the owner calls.

The judgment trail, every owner quote included, is
`docs/decisions_drafts/place-search.md` (Cleanup folds it into DECISIONS.md).
Read it before changing anything below.

**Delete this file** when place search has landed and the rollout plan below
is either done or moved into PLAN.md.

---

## What the owner settled (2026-10-07)

- **Places only, never business records**, searched entirely in the visitor's
  browser over a static per-city index from OpenStreetMap. No query reaches a
  server, a log or the URL. Not Nominatim (its policy forbids autocomplete).
- **Never a home:** residential land, houses, apartment buildings, private
  access, residential gardens and `place=isolated_dwelling` are dropped unless
  notable. Kyoto had a condominium's grounds tagged as a park.
- **Notable only** for tourism and education landmarks, gardens and named
  markets: a wikidata or wikipedia tag (gardens: or a heritage tag). Nishiki
  Market is in; company markets ("Yodo Produce Co., Ltd.") stay out.
  `operator:type` marks a business only when private, business or commercial
  (Nishiki is run by its shopkeepers' cooperative).
- **Languages are measured, never written.** Each city declares its local
  language(s) (`config.PLACE_LANGUAGES`); the page names English first, then
  the local languages, each covering at least 50% of the places; a declared
  local language under 90% stops the step. Kyoto: English 73.8%, Japanese
  99.7%, so "in English or Japanese". APPROVED.
- **The map's own stations and lines** are read from the map page itself
  (station tooltips, legend rows, line polylines), so results carry the drawn
  names. They show first as pills under "On this map": a line pill frames the
  line and highlights it as its legend row does; a station pill frames the
  station's outermost ring. The kind ("Line", "Station · 烏丸") is on hover
  only. All 117 Kyoto stations and 18 lines come first by their map names.
- **Suggestions are WORK IN PROGRESS**: nothing until a full keyword (a whole
  word of a name, 4+ Latin letters, 2+ CJK characters, or a second word); at
  most 6 pills and 6 places, 4 and 3 under 480 px; on phones the two groups
  fold ("On this map" open, "Places" folded). To be tuned against real search
  terms in testing; it may go live as is at the owner's call.
- **Wording, all approved:** the placeholder "Street, station, place"; the
  in-box line "Finds streets, intersections, stations, lines, neighborhoods
  and landmarks. Businesses are not searchable, and what you type stays in
  your browser."; the headings "On this map" and "Places"; the labels Station,
  Line, Station not on this map, Intersection, Street, Neighborhood, Landmark;
  "No street, station or place by that name"; "Streets and places are
  searchable on the site's own map pages"; the page bullet in
  `app/components.render_map_help`.
- **The credit:** "Search data © OpenStreetMap contributors (ODbL) · Download
  this index", three links. Moving it into the map's corner credit is an
  optional review-time test; off the map onto the page is NOT safe (the
  Geocoding Guideline asks the search itself to credit OSM).
- **Licence:** the index is an ODbL Derivative Database (licence read
  2026-10-07, PERMITTED WITH CONDITIONS). Each file carries the notice in its
  `license` object; `LICENSE` carves `app/static/places/` out as ODbL only;
  `docs/data_sources.md`, "Place search index". Nothing non-OSM may enter an
  index (ODbL 4.4(d)): the map's stations are joined to OSM's in the browser,
  never in the file.
- **Cities menu out of the map:** review time, measured at 343 px with the
  search box in place.
- **Rollout order:** the Japanese cities, then the US and Canadian grid
  cities, then the rest.

---

## What is built, and where

| Piece | File |
|---|---|
| Overpass fetch, one query per city, cut by the city boundary. NOT a step | `pipeline/place_index_fetch.py <city>` |
| Index build: places, filters, languages, the summary, the hashed URL | `pipeline/place_index.py` |
| Kyoto's index step (runs BEFORE the map step: the map needs the hash) | `pipeline/kyoto/step2b_place_index.py` |
| Kyoto's config: `PLACE_AREA`, `PLACE_OSM_JSON`, `PLACE_LANGUAGES` | `pipeline/kyoto/config.py` |
| The search box, opt-in: `render_heatmap(place_index_url=...)` | `pipeline/map_common.py`, `PLACE_SEARCH_SCRIPT` |
| Kyoto's map step passes `place_index.index_url(config.SLUG)` | `pipeline/kyoto/step3_map.py` |
| The index (ODbL), served by Streamlit's static serving | `app/static/places/kyoto.json`; `.streamlit/config.toml` `[server] enableStaticServing` |
| The page's summary (languages, count, date) the app reads | `outputs/kyoto/place_search.json` |
| The page bullet: `render_map_help(..., search="kyoto")` | `app/components.py`, `app/pages/54_Kyoto_Heatmap.py` |
| The check (in `check_all.py`, with a selftest) | `scripts/check_place_search.py` |
| Licence | `LICENSE` (second exception), `docs/data_sources.md` |

The Kyoto caches in the shared `data/` (new file names; Kyoto's steps 1 and 2
were never re-run): `data/kyoto/raw/osm_places_2026-10-07.json` (the first
build) and `osm_places_v2_2026-10-07.json` (with markets, the one in use).

**This worktree's `data/` is a junction to the main checkout's.** Unlink it
on its own before removing the worktree (`docs/session_roles.md`, step 1).

---

## Measured

- **Kyoto:** 11,846 places (5,151 neighborhoods, 2,649 landmarks, 2,424
  street-pair intersections, 960 streets, 502 signed junctions, 160 OSM
  stations); 1,041,923 bytes, about 270 KB gzipped (Streamlit served 284 KB).
  Fetched on first use of the box, ready in 130-148 ms on a local desktop;
  each keystroke 1-10 ms. The map file grows about 13 KB of script, no data.
- **Tokyo, estimated** from one count-only Overpass query over the 23 wards:
  about 2.3 MB raw, 0.6 MB gzipped, about twice Kyoto's load time.
- **Not measured:** a real phone; MiniSearch's prebuilt index (own matcher
  chosen: its tokenizer cannot find 烏丸 inside 四条烏丸).

---

## Adding a city (the recipe the Kyoto pilot implies)

1. **Config:** `PLACE_AREA` (an Overpass area filter that matches exactly the
   city's boundary; admin levels differ by country, so confirm it matches ONE
   area), `PLACE_OSM_JSON` under a NEW file name dated by the fetch
   (`osm_places_<date>.json`; the retrieval date is read from the name), and
   `PLACE_LANGUAGES` (Brussels would be `("fr", "nl")`; an English-speaking
   city `("en",)`).
2. **Fetch:** `python pipeline/place_index_fetch.py <city>`. The owner's
   Overpass rule: one query in flight per session, never parallel, 60 s after
   a 504 or 429 (`pipeline/osm.py` enforces the wait). About 1 GB a day is
   overpass-api.de's guidance, so roll out over several days.
3. **Index step:** copy `pipeline/kyoto/step2b_place_index.py`, which calls
   `place_index.run(config)` and nothing else. Set `PLACE_FOLD` in config:
   `"ja"` (Japanese long vowels, shijou = shijo) or `None` everywhere else.
   Before a city in a NEW language, add that language's `WAY_WORDS` (a minor
   way is kept only when its name reads as a way) and `LEAK_WORDS` (business
   and home markers) in `place_index.py`; without `WAY_WORDS` no footway or
   service road of that language is indexed.
4. **Map step:** `place_index_url=place_index.index_url(config.SLUG)`, after
   the index step has run; re-render.
5. **Page:** `render_map_help(..., search="<slug>")`.
6. **Checks:** `python scripts/check_place_search.py` must name the city OK.
   Its part E flags every row carrying a business or home word; drop the
   class by a rule in `place_index.py`, or list a real place in the city's
   `PLACE_REVIEWED` with why (Kyoto: one hotel ruin). Then still read the
   index by eye: brand names carry no word. Kyoto found a tea-ceremony shop, a
   private school, a condominium, a garden possibly named after a person and
   supermarket-named footways, each now a rule; the next country will find
   its own.
7. **Test the searches the city is known for**: its intersection style ("5th
   and Pike" in a US grid), its station names, its landmarks, in each listed
   language.

---

## Open, for review time or the next session

- **The WIP suggestions** on a real phone: the open list still covers about
  half the map at 343 px; the pills stack one per row at 190 px.
- **The corner credit test** and the **Cities menu move** (both review time).
- **Landing:** `app/` changes, so `check_deploy_imports.py` (this worktree has
  no `.venv-lean`; run it from one that does), a `map-chrome` deploy-verify
  that opens the search on the live site, and a reboot.
  `pipeline/map_common.py` is shared code (the app/chrome role's): the pilot
  changed it on a branch only; other maps render unchanged
  (`check_render_current.py` treats the block as conditional).
- **Gaps seen in Kyoto:** a line's Japanese name (烏丸線) finds nothing as a
  line, since the map shows English line names only; "Gion Shirakawa" finds
  nothing (no OSM object carries both names); "Kyoto Station" lists the bus
  terminal's alias on the station, which is right but shows the bus
  terminal's Japanese name only on hover.
- **Wired 2026-10-08:** `place_index_fetch.py` records the cache in
  `outputs/<city>/provenance.json` as `osm_places` (a cache on disk is
  recorded without a query); `PLACE_FOLD` is per city; check E scans for
  business and home words. Still not adapted:
  `scripts/check_personal_exposure.py`, built for business names.
- **The sample, one city per region** (owner, 2026-10-08), is build-sized:
  see the drafts entry of 2026-10-08 for the proposed list.

---

## Traps the pilot hit

- **The Edit and Write tools decode `\u` escapes** into literal characters.
  The JS character classes are built in Python (`_js_ranges` in
  `map_common.py`); keep it that way.
- **A browser keeps a static file.** A rebuilt index under the same URL went
  unseen, so the URL carries the file's content hash and the map is
  re-rendered after every index build (`check_place_search.py` A).
- **Overpass `area` by name** can match more than the city; Kyoto's
  `["name"="京都市"]["admin_level"="7"]` matched one, and Tokyo's 23 wards came
  from `rel(area.東京都)["admin_level"="7"]["name"~"区$"]` (23 relations).
- **Station joining** by any shared word joined a scenic railway's stop to
  the next station; the rule is the same core name or the same first word,
  then a name already held, and a same-named stray within 1.5 km is dropped.
- **Screenshots of the embedded map can lag** a click; read the map's zoom
  through the page's script before calling a click broken.
- **Windows writes CRLF:** `sed -i 's/\r$//' outputs/<city>/heatmap.html`
  after every render, before staging.
