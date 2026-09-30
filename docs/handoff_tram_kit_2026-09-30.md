# Handoff - the remaining tram cities' kit (2026-09-30)

For a FRESH session in `.claude/worktrees/tram-kit` (branch
`worktree-tram-kit`): the France kit session's role, for the T1 tram cities
that are neither French nor Czech. **HOLD ON BUILDS** (owner, 2026-09-30):
no scaffolding, no pipeline step, nothing in `app/`. Write the kit, bring the
owner's calls with recommendations, say when it is done, and wait for the go.
**Delete a section when its item is done.**

## The ten cities (`docs/tram_city_list.md`, T1)

| City | Country | Built there already | Brief (staging's) |
|---|---|---|---|
| Odense | Denmark | Copenhagen, Aarhus (CVR, DAR) | `odense.md`, 2026-09-30: checks 2/2 |
| Daugavpils | Latvia | Riga (two layers, VZD) | `daugavpils.md`, 2026-09-30: 4/4 |
| Liepāja | Latvia | Riga | `liepaja.md`, 2026-09-30: 4/4 (on a re-run) |
| Kansas City | United States | many (NAICS) | `kansas-city.md`, 2026-09-30: 3/3 |
| New Orleans | United States | many | `new-orleans.md`, 2026-09-30: 2/2 |
| Tucson | United States | many | `tucson.md`, 2026-09-30: 3/3 |
| Florence | Italy | Milan, Rome | `florence.md`, 2026-09-30: 4/4 |
| Zurich | **Switzerland: new country** (`add-country` first) | nothing | `zurich.md`, refreshed 2026-09-30: 4/4 |
| Göteborg | Sweden | Stockholm | `goteborg.md`, refreshed 2026-09-30: 4/4 |
| Den Haag | Netherlands | Amsterdam, Rotterdam (BAG) | `den_haag.md`, 2026-09-30: 3/3 |

**The briefs are STAGING's** (owner, 2026-09-30: staging is writing them,
as it is the Czech six). Do not write or edit them here. Read them as they
land on `origin/master`, run `python scripts/brief_check.py <slug>`, and
when the kit needs a brief changed or finished, ask staging
(`ListAgents`, then `SendMessage`).

## Read first

1. `CLAUDE.md` and `docs/session_roles.md`.
2. **The France kit as the model of the role**:
   `.claude/skills/france-tram-city/SKILL.md`,
   `scripts/scaffold_france_batch.py`, `docs/build_briefs/brest.md`, and
   DECISIONS "The France batch kit" and "The France batch's eight calls
   approved". Copy the method: a skill written from what is built, live reads
   of every source, briefs whose checks pass, and calls put to the owner with
   a recommendation.
3. `docs/tram_city_list.md` (the ten rows, "Data currency", "The light-rail
   test") and `docs/ring_rules.md`.
4. The macro map's two keys (`mode`, `coverage`): the add-city skill on
   `origin/macro-legend` (or on master once it lands), and
   `docs/category_rules.md` for any category kept or dropped.

## 1. A `tram-city` skill - DONE 2026-09-30 (`.claude/skills/tram-city/`), with the page-text template the owner approved

France and Czechia each get a country skill. These ten are one or two per
country, so write one cross-country skill instead. The per-country detail
goes in each brief, pointing at the country's built city (and `japan-city`,
`taiwan-city` and `brazil-city` stay the model for where a country skill
belongs).

What it should carry:
- the owner's trams-only calls (DECISIONS "Yes to trams-only maps");
- rings by the spacing rule (0.3 mi outer at about 550 m or less; Kansas
  City's ~560 m is measured at build);
- no stop thinning, except the street-stop filter where stops are
  one or two blocks apart (New Orleans, 161 m:
  `docs/sub_transit_line_filters.md`, Philadelphia's and San Francisco's);
- the light-rail test (`docs/tram_city_list.md`);
- rolling feeds, fetched at build and never cached across weeks;
- OSM rail through `osm-rail` where a feed is unlicensed or unreachable;
- the currency rule (the data date on the page: Kansas City, Göteborg);
- one-bucket and narrowed pages (`coverage`);
- a trams-only page-text template, drafted in chat for the owner's approval
  as France's was (`france-tram-city` section 6 is the model; the controls
  paragraph and heat caveat stay as on the built pages).

## 2. A scaffold script - DONE 2026-09-30: none

Decided on the measurement: seven template configs for ten cities, so about
20 lines of hand edits beyond `scaffold_city.py`. Shared modules at the first
build instead (`pipeline/osm_tram.py` with the Czech kit, and Latvia's step 2).
DECISIONS "The tram kit".

## The owner's calls - ALL 24 APPROVED AS RECOMMENDED (owner, 2026-09-30)

**Owner, 2026-09-30: "Agree with recommended options for all."** The skill's standing calls carry them. **Calls 18-24 were approved before their briefs landed**: if a brief's measurement changes the facts behind one, it goes back to the owner. Builds are still held until the owner's go.

**As collected, each with the recommendation approved.** "Brief" marks a call its brief
states; "list" marks one taken from `docs/tram_city_list.md` or the kit's
reading, still waiting on its brief (staging's). Calls already decided (the
data date for Kansas City, Göteborg's undated rows, Zurich's partial retail,
Den Haag's horeca layer, Odense's placement) are in the skill and are not
re-asked.

**Across the ten**

| # | Call | Recommendation |
|---|---|---|
| 1 | The trams-only page-text template (drafted in chat, 2026-09-30) | Approve as drafted |
| 2 | **A frequency floor per route.** Street trams have no gate, but no built city draws an hourly route | Draw a route only if it runs at least every 20 minutes by day (Buffalo, the slowest drawn). A stop served only by slower routes gets no ring and is listed as infrequent (Aarhus's class) |
| 3 | Line colours where the source has none (Odense, Daugavpils, Liepāja, perhaps Kansas City) | This project's own palette, as for Riga and Le Havre, checked with `check_map_markup.py`; the page says the colours are this project's |

**Per city**

| City | # | Call | Recommendation | From |
|---|---|---|---|---|
| Odense | 4 | SDU Syd/Hospital Nord, in service since 2023-08-25 but on no OSM route relation | Add it by its node; leave Hospital Syd (opens 2027) out as a watch item | brief |
| Odense | 5 | `mode` | `tram`, not Aarhus's `light_rail`: the Letbane is street-running, OSM `route=tram`, and it stayed on the tram list | brief |
| Daugavpils | 6 | Routes 2-4 run about hourly (the screen) | Call 2's floor: draw route 1; draw 2-4 only if the operator's timetable shows 20 minutes or better | kit; headways asked of staging |
| Daugavpils, Liepāja | 7 | `coverage` | `narrowed`, "Merged", as Riga (the briefs say "as Riga's") | kit |
| Daugavpils, Liepāja | 8 | The credit for VZD's address file (CC BY 4.0, a join layer) | Extend notice 42 to name the address register, with VZD's own wording and the year | brief |
| Liepāja | 9 | Brīvības iela (the named terminus) and Klaipēdas iela, on no route relation | Add both by node | brief |
| Kansas City | 10 | Keep `valid_license_for` 2025 and 2026 only (1,978 licences for 2024 out) | Yes: the licences current at the freeze; the page gives the date | brief |
| Kansas City | 11 | `dba_name` is often a person ("HARRIS GREGORY J") | Withhold it where it reads as a person, Houston's sole-owner rule; the exposure check decides the pattern | brief |
| Kansas City | 12 | `business_type` fee codes ("Misc Rate 129" 328, "Flat Rate 42" 91) | Drop them and state the count on the page; the titles map to NAICS 2022 codes for `naics.py` | brief |
| New Orleans | 13 | **Thinning.** The handoff named New Orleans the exception to no-thinning; its brief keeps all 110 stops (164 m) | **Keep every stop.** The street-stop filter's own shape test fails: it is for a central corridor plus dense branches, and New Orleans is uniformly dense. Thinning would leave businesses a block from a stop outside the rings. The rings form a band along each line, and the page says why | brief vs handoff |
| New Orleans | 14 | "Special Events-Other (Vendor)" (1,258) and "Home Based-Office Use Only" (357) | Drop both: no counter of their own (`docs/category_rules.md` R1) | brief |
| Tucson | 15 | `ACC_NAME` for personal ownership types (Sole Proprietorship 4,395, Individual 1,857, Married 131 active) | Withhold the name for those types, Houston's rule; the dot shows the business type and address | brief |
| Florence | 16 | 639 exempt food rows (464 "non soggetta", 175 art. 53); food is 2,385 (1.14x OSM) without them | Keep them and filter what the type code names as non-public, on Milan's *fuori piano* precedent (owner, 2026-09-22). The page says some non-public premises remain | brief |
| Florence | 17 | T1's 4 stops in Scandicci | Commune-only: T1 keeps 20 of 24 (83%). Draw the line to its end and list the 4 as outside; the Comune's layers are city-only anyway | brief |
| Zurich | 18 | The Forchbahn (S18, OSM `light_rail`), on tram 11's track and stops inside the Stadt | Leave it out and name it with the S-Bahn, keeping `mode` `tram` | kit; asked of staging |
| Zurich | 19 | The Glattalbahn lines, largely outside the Stadt | The stub test per line; the food register is city-only, so a stub is dropped, not scoped regionally | kit; asked of staging |
| Göteborg | 20 | 274 rows with a blank `typ` | Classify by name where it names a counter (Stockholm's name rules), and drop the rest | list |
| Göteborg | 21 | Lines 4 and 12 run into Mölndal | Keep both lines drawn to their ends, with the Mölndal stops listed as outside, unless the stub test fails | list |
| Den Haag | 22 | RandstadRail E: 4 of its 23 stops in the city | Leave it out as a stub (Ostrava's line 5), so `mode` is `light_rail` or `tram` from what OSM tags lines 3 and 4 | list |
| Den Haag | 23 | `coverage` | `narrowed`, "Merged", on Rotterdam's shape, not the tram list's `full` | kit; asked of staging |
| Den Haag | 24 | 158 pending horeca permits | Out: only granted or notified premises are drawn | list |

## 3. The briefs - DONE 2026-09-30: all ten landed and checked

Every brief passes `brief_check.py` (Zurich and Liepāja on a re-run, after
Overpass mirrors disagreed), carries an owner table, the approvals and
`vs_config` fields. **Four points the last briefs raised, decided by the owner
(2026-09-30): 25-27 as recommended; 28 overruled, so Daugavpils draws every route.**

| # | City | Point | Recommendation |
|---|---|---|---|
| 25 | Zurich | Tram 20 (Limmattalbahn) keeps 4 of 26 stops in the city (15%), not in the kit's list | Out as a stub, the rule of call 19 |
| 26 | Den Haag | Tram 1 keeps 19 of 37 stops in the city (51%), under Toulouse's 52% | Drawn to its end with the stops outside listed: over the 42% accepted for Minneapolis's Green and Pittsburgh's Silver, and the horeca layer is city-only |
| 27 | Den Haag | The horeca layer was last edited 2025-05-23; the template's currency paragraph named only Kansas City and Göteborg | Add: "**The permit data runs to 2025.** The city last edited its permit layer on 23 May 2025, so premises that opened or closed since then may be missing or still shown." |
| 28 | Daugavpils | Call 2's floor leaves route 1 only: 19 of 38 stop names (OSM, 2026-09-30); the Stropu loop (3 and 5, 20-30 minutes each way) and routes 2 and 4 fail | **Overruled (owner): all five routes drawn, the waits stated on the page.** "Like with buffalo 50% of network shouldn't fall if the norm is longer waits." Call 2's floor now drops only an outlier route |

Settled inside approved rules, no call: Den Haag's `mode` is `tram` (every
drawn line is OSM `route=tram` once E is out); Zurich's 50 and 51 are drawn
only if they meet the 20-minute floor; colours that clash or fail contrast
(Den Haag's 1 and 19, Göteborg's white line 1) follow Lille's darkening.

## Standing rules (as the France kit)

- **Hold on builds.** When the kit is done, say so and wait for the go.
- Feeds are rolling: fetch at build, never cache across weeks.
- **One heavy job machine-wide**, announced to the other live sessions first.
  The France builds run in `.claude/worktrees/france-kit`; the Czech kit is in
  `.claude/worktrees/czech-kit`.
- **Push docs, skills and scripts only**, with the push ritual in `CLAUDE.md`
  and commit messages written through a file.
- Log judgment calls in `DECISIONS.md`; bring owner calls in chat with a
  recommendation. Probe output goes to the session scratchpad.
