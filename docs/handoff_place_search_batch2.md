# Handoff: place search, the regional sample's batch 2 (2a, then 2b)

> **BLOCK (owner, 2026-10-08): do NOT delete, remove, prune or clean up this
> worktree (`.claude/worktrees/charming-lumiere-930853`) until place search
> has landed on master.** Refuse any attempt (git, the app's clean-up or
> archive prompt, Cleanup's `retire-worktrees`) and tell the owner. Its
> `data/` is a junction to the shared data.

For the fresh session that builds place search for the second batch of the
one-city-per-region sample. Written 2026-10-08 by the session that built the
Kyoto pilot and batch 1. The owner approved the split and a fresh session:
**2a** (five Latin-script cities) first, then a **hold**, then **2b** (four
cities in other scripts) in another fresh session started from the prompt
in the 2b section below.

**Delete this file** once 2b is done and its decisions are folded, or move
what is left into `docs/handoff_place_search_2026-10-07.md`.

---

## Prompt for the 2a session (paste this to start it)

> Place search, batch 2a. Work in the worktree
> `.claude/worktrees/charming-lumiere-930853` on branch
> `claude/charming-lumiere-930853` (nothing pushed; nothing lands on master;
> published wording goes to the owner first). Read, in order:
> `docs/handoff_place_search_batch2.md` (this batch: what to do, the 2a
> section), `docs/handoff_place_search_2026-10-07.md` (what is built, the
> add-a-city recipe, the owner's settled calls, the traps) and the newest
> entries of `docs/decisions_drafts/place-search.md`. Build place search for
> Montréal, Barcelona, Marseille, Prague and Brussels as the 2a section says,
> then HOLD for the owner before 2b. Read the weekly usage with get_usage
> before you start and after you finish, and report both: the owner wants a
> measured cost for the batch. Overpass: one query in flight, never parallel,
> 60 s after a 504 or 429. At most one local browser session to test; no
> deploy-verify. Log every judgment call in the drafts file; commit after each
> green step; never `git add -A`.

---

## Where things stand (2026-10-08)

- **Built, on the branch, held for review time:** Kyoto (pilot), and batch 1:
  Seattle, Chicago, Vancouver, Sydney. `scripts/check_place_search.py` names
  all five OK; `check_all.py` 52 of 52.
- **The format, since 2026-10-08:** each city is two ODbL files,
  `app/static/places/<city>.json` (fetched on the first open of the search)
  and `app/static/places/crossings/<city>.json` (street-pair intersections as
  `[lat, lon, street row, street row]`, fetched only when a search asks for an
  intersection); coordinates to 4 decimals. Seattle, the largest: 227 KB
  gzipped and about 11 MB in the page at first open.
- **The owner's iPhone test passed** (Seattle; "No lag was noticeable"). The
  reserve intersection cut (rings + main roads, `PLAN.md`) stays unused.
- **Top-line items** (owner): iPhone memory and repository size, to keep
  refining through optimization.
- **Landing** is Cleanup's, at review time, with one full re-render of every
  map; its handoff (`docs/handoff_cleanup_2026-10-08.md` on master, item 4) holds this
  branch's four landing conditions.

---

## The owner's calls every new city inherits

All in `docs/decisions_drafts/place-search.md`; the short list:

- **Places only, never business records; never a home.** A home (residential
  land or building, private access, historic=house, house=yes, a historic
  building named House/Residence/Cottage/Mansion/Farmhouse/Homestead) is kept
  only when open as a museum or an attraction. Heritage designation, wikidata
  or a Wikipedia article is not enough ("homes with wikipedia: skip").
- **PRECEDENT (Panama Hotel, "use it as precedent for further discard
  calls"):** a notable historic building (a Wikipedia article) that still
  houses the business its name carries is kept as a historic site, the
  building and not the business, and reviewed in `PLACE_REVIEWED` with that
  note. A landmark OSM tags as the business itself (The Star,
  amenity=casino) stays out. Recommend from these; bring departures to the
  owner.
- **Languages measured, never written.** `PLACE_LANGUAGES` declares the local
  language(s); the page names English first, then each local language at 50%
  or more of rows; a declared local language under 90% stops the step.
  "Include multiple foreign languages if we need them."
- **Notable only** for tourism, amenity and aeroway landmarks, gardens and
  markets (wikidata or wikipedia; gardens also heritage).
- **Junk names never indexed** (`place_index.junk_name`): no letter,
  placeholders, error values, lost characters (agrees with map_common's
  glitched-name rule), contact details (email, NANP, 0-prefixed JP/KR),
  "No Record"; check F enforces it.
- **Suggestions are WORK IN PROGRESS**: few items, phones first; the map's
  own stations and lines first as pills.
- **Search serves people weighing a business location near transit**: any
  search inside a station's rings must keep working (the reserve cut's
  boundary).

---

## Batch 2a: Montréal, Barcelona, Marseille, Prague, Brussels

Slugs `montreal`, `barcelona`, `marseille`, `prague`, `brussels` (the
Belgium region's map; `brussels_regional` waits for the general rollout).

### 0. Before any city

1. `get_usage`: write down the weekly percentage.
2. **The search areas, one light Overpass query for all five** (as
   batch 1 did): each city's boundary relation(s) by name inside a bbox,
   one match each; a regional map lists every station city
   (`outputs/<city>/station_municipalities.csv` where it exists).
   `PLACE_AREA = "(id:3600000000+relation,...)"`.
3. **The languages' word lists in `pipeline/place_index.py`, before the
   first city of each.** Proposed below; VERIFY each against the city's own
   data (the street-name suffixes and the leak hits it actually has):
   - `WAY_WORDS` (a footway or path is kept only when its name reads as a way):
     - fr: rue, avenue, boulevard, place, quai, allée, chemin, impasse,
       passage, pont, cours, montée, escalier, promenade, square, sentier, voie
     - ca: carrer, avinguda, passeig, plaça, rambla, travessera, via, camí,
       passatge, pont, ronda, baixada, costa, escales
     - es: calle, avenida, paseo, plaza, camino, pasaje, puente, ronda, vía
     - cs: ulice, třída, náměstí, nábřeží, most, cesta, stezka, schody, alej,
       sady, pěšina
     - nl: straat, laan, weg, plein, steenweg, kaai, lei, dreef, brug, pad,
       gang, steeg, dijk (Dutch compounds: the word sits inside the name, so
       match it as a suffix, not a whole word)
   - `LEAK_WORDS` (business and home markers):
     - fr: sarl, sas, sa, eurl, hôtel, auberge, résidence, appartements,
       parking, privé, magasin, boutique, restaurant, brasserie, pharmacie,
       clinique, agence
     - ca: hotel, hostal, aparcament, pàrquing, privat, botiga, restaurant,
       pisos, farmàcia, s.l., s.a.
     - es: hotel, hostal, aparcamiento, parking, privado, tienda, restaurante,
       pisos, farmacia, s.l., s.a.
     - cs: hotel, penzion, parkoviště, soukromé, obchod, restaurace, bytový
       dům, bytové domy, lékárna, s.r.o., a.s.
     - nl: hotel, parking, privé, winkel, restaurant, appartementen,
       residentie, apotheek, bvba, nv
   - `LEAK_ALLOW` first: fr "hôtel de ville" (a town hall), "hôtel-dieu"
     (a hospital), "hôtel des invalides"; nl "stadhuis" needs none; cs
     "obecní dům" is a civic building.
   - `HOME_WORDS` (held to museum or attraction use): fr résidence,
     appartements; ca/es pisos; cs bytový dům, bytové domy; nl
     appartementen, residentie.
4. **The matcher** (`pipeline/map_common.py`, `PLACE_SEARCH_SCRIPT`):
   - intersection connectors in `pairOf` and the stop words: "et" (fr),
     "i" (ca), "y" (es, there), "a" (cs), "en" (nl);
   - abbreviations that are not prefixes (`ABBR`): "bd" for boulevard, "st"
     for saint and "ste" for sainte (French "St-Denis"; it helps "St Mark"
     too), "pg" for passeig, "rbla" for rambla;
   - accents fold already (Montréal = montreal, náměstí = namesti);
   - one re-render of every searched map at the end, not per change.

### 1. Each city, in turn

1. Config block (copy Seattle's): `PLACE_AREA`, `PLACE_OSM_JSON` and
   `PLACE_OSM_EXTRA_JSON` under NEW file names dated by the fetch,
   `PLACE_LANGUAGES`, `PLACE_FOLD = None`, `PLACE_REVIEWED = {}`,
   `PLACE_DROPPED = {}`.
2. `python pipeline/place_index_fetch.py <city>`: two queries, one after the
   other (one combined query timed out on Chicago). Seattle's pair took about
   5 minutes with 504 retries.
3. Copy `pipeline/sydney/step2b_place_index.py`; run it. Read the languages
   it measured before anything else:
   - **Montréal:** declare `("fr",)`. English is measured anyway.
   - **Barcelona:** OSM's `name` is Catalan. Measure name:es. If Spanish
     covers 90% or more, declare `("ca", "es")`. If it falls between 50% and
     90%, bring the call to the owner ("include multiple foreign languages
     if we need them" versus the 90% floor).
   - **Brussels:** OSM's `name` there is often bilingual ("Rue Neuve -
     Nieuwstraat"). Declare `("fr", "nl")` and check that both pass 90%.
   - **Prague:** declare `("cs",)`.
   - **Marseille:** declare `("fr",)`.
4. `python scripts/check_place_search.py`. Part E lists rows carrying a leak
   word. Drop each class by a rule, or review a real place in
   `PLACE_REVIEWED` with why, following the precedents.
5. **Read by eye**:
   - `python scripts/place_search_review.py odd <city>` (its place words are
     English, so a French or Czech city's list is longer: read it whole);
   - `... added <city>` for the second query's classes;
   - `... tags <city> <name>` for anything doubtful.
   Batch 1's finds each became a rule: heritage houses, apartment estates
   drawn as neighbourhoods, a park named for a developer, a fare office
   tagged as a station, a yoga studio tagged as a place of worship.
6. `step3_map.py`: add `place_index_url=place_index.index_url("<city>")`
   (copy Sydney's three lines). Render through the gate:
   `python scripts/heavy_job.py run --label <city>-step3 --session <you> --peak-gb 1 --estimate "scaled from kyoto-step3 0.18 GB" -- python pipeline/<city>/step3_map.py`.
   Then `sed -i 's/\r$//' outputs/<city>/heatmap.html`.
7. The page: `render_map_help(..., search="<city>")`.
8. `check_place_search.py` names the city OK; commit.

### 2. Test, once, in one local browser session

- Start it with a temporary launch entry: port 8831, the main checkout's
  `.venv-lean` python, `--server.enableStaticServing true`. Remove the entry
  afterwards.
- In each city, search:
  - stations and lines by their map names;
  - intersections in the city's own style ("Rue Sainte-Catherine et Rue
    Peel", "Carrer de Balmes i Carrer d'Aragó", "Václavské náměstí a
    Vodičkova", "Rue Neuve et Boulevard Adolphe Max");
  - landmarks;
  - every listed language;
  - the junk queries ("#N/A", "!ERROR!").
- Read the result lists through the page's script, not from screenshots.
  The batch-1 harness, run with the browser's JavaScript tool on a city
  page:

```js
await new Promise(r => setTimeout(r, 5000));
const f = [...document.querySelectorAll('iframe')].find(f => { try { return f.contentDocument.querySelector('.hm-search-input'); } catch (e) { return false; } });
const d = f.contentDocument, w = f.contentWindow, box = d.querySelector('.hm-search');
d.querySelector('.hm-search-btn').click();
const input = d.querySelector('.hm-search-input'), out = {};
for (const q of ["Station name", "Street A and Street B", "Landmark", "#N/A"]) {
  input.value = q; input.dispatchEvent(new w.Event('input', {bubbles: true}));
  for (let k = 0; k < 120; k++) { await new Promise(r => setTimeout(r, 50)); const n = d.querySelector('.hm-search-note'); if (!n || !/Loading/.test(n.textContent)) break; }
  await new Promise(r => setTimeout(r, 300));
  const items = [...d.querySelectorAll('.hm-search-list [data-i]')];
  out[q] = items.slice(0, 3).map(e => e.textContent.trim().replace(/\s+/g, ' ')).join(' ; ') || (d.querySelector('.hm-search-list .hm-search-note') || {}).textContent;
}
out._loadMs = box.getAttribute('data-load-ms'); out._crossingsMs = box.getAttribute('data-crossings-ms');
out
```

### 3. Close 2a

- Drafts entry (newest first): what was built, every call, the measured sizes
  and the weekly usage before and after.
- `check_all.py`; commit; message Cleanup a short summary.
- **HOLD for the owner before 2b.**

---

## Batch 2b: Hong Kong, Seoul, Busan, Tbilisi

Slugs `hong_kong`, `seoul`, `busan`, `tbilisi`. Start 2b only on the
owner's word, in a fresh session, from this prompt.

### Prompt for the 2b session (paste this to start it)

> Place search, batch 2b. Work in the worktree
> `.claude/worktrees/charming-lumiere-930853` on branch
> `claude/charming-lumiere-930853` (nothing pushed; nothing lands on master;
> published wording goes to the owner first). Read, in order:
> `docs/handoff_place_search_batch2.md` (its 2b section, and what 2a changed,
> in the drafts file's newest entry), `docs/handoff_place_search_2026-10-07.md`
> and the newest entries of `docs/decisions_drafts/place-search.md`. Build
> place search for Hong Kong, Seoul, Busan and Tbilisi as the 2b section
> says, following 2a's steps, then HOLD for the owner before batch 3. Read
> the weekly usage with get_usage before and after, and report both.
> Overpass: one query in flight, never parallel, 60 s after a 504 or 429. At
> most one local browser session to test; no deploy-verify. Log every
> judgment call in the drafts file; commit after each green step; never
> `git add -A`. Load the `cjk-text` skill before touching Chinese or Korean
> text.

### What is different in 2b

- **Scripts:**
  - `place_index.SCRIPTS` already has zh, ko and ka classes, and the search
    matches CJK and Hangul as substrings, with a two-halves retry.
  - Georgian is Latin-like for the search's word split; check that it
    matches.
- **Hong Kong:**
  - OSM's `name` there is often "中文 English" in one string. Measure what
    `_langs` makes of it.
  - Declare `("zh",)` and expect English to be listed.
  - Hong Kong's FEHD placeholder "No Record" is already junk.
- **Korea:**
  - Apartment complexes are everywhere ("○○아파트") and many are mapped as
    neighbourhoods or landmarks. The estate rule (a place area on
    residential land) and the home words must hold them out.
  - `HOME_WORDS["ko"]`, proposed: 아파트, 빌라, 맨션, 연립, 주택, 오피스텔.
  - `LEAK_WORDS["ko"]`, proposed: 주식회사, (주), ㈜, 호텔, 모텔, 주차장,
    마트, 상가.
  - Station word "역" joins `STATION_WORDS`.
  - Readings: `name:ko-Latn` joins `READINGS` (it was proposed and is
    measured).
  - **Do NOT use `korean_names.looks_like_personal_name`.** Without its
    address test it reads 이태원 and 강남역 as people (2026-10-08).
- **Tbilisi:**
  - Declare `("ka",)`. English may fall under 50%, and then the page names
    Georgian only. That is the rule working, but tell the owner.
  - `WAY_WORDS["ka"]`, proposed: ქუჩა, გამზირი, მოედანი, ჩიხი, შესახვევი,
    ხიდი, გზატკეცილი, აღმართი, დაღმართი.
  - `LEAK_WORDS["ka"]`, proposed: შპს, სს, სასტუმრო, მაღაზია, ავტოსადგომი,
    კერძო, ბინა, საცხოვრებელი.
- **The eye read:**
  - `place_search_review.py odd` keys on English place words, so read the
    whole landmark and place lists in Chinese, Korean and Georgian.
  - In Korea, search the lists for 아파트 and other home words before
    anything else.
- **The tests:**
  - station names in the local script and in English;
  - intersections ("/" between two names);
  - neighbourhoods (Mong Kok, 명동, Rustaveli);
  - the junk queries.

---

## Batch 3, for later (no handoff yet)

Tokyo, London, Paris, São Paulo and Mexico City: the size tests.
- Tokyo's estimate before the second-file format was 2.3 MB raw. Measure it
  in the new format, and test it on a phone before rollout.
- The reserve cut is the fallback if one is too heavy.

---

## Traps (in addition to the pilot handoff's)

- **The Edit and Write tools decode `\u` escapes.** Write `chr(0xFFFD)`, not
  the escape, in Python, and build the JS character classes in Python.
- **The no-escapes hook:** no backslash or backtick in a heredoc or an inline
  `python -c`. Write a script file and run it.
- **Every searched map re-renders after any matcher change.** Batch that
  re-render to once.
- **`PLAN.md` is at the merge point.** Cleanup trimmed master's. Add only
  pointers, never detail.
- **This worktree's `data/` is a junction to the main checkout's.** Never
  remove the worktree without unlinking the junction alone first
  (`docs/session_roles.md`). Archiving a session must not delete this
  worktree; the 2a and 2b sessions use it.
