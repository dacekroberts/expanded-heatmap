---
name: czech-tram-city
description: Build a Czech tram city - the six Czech T1 cities (Brno, Ostrava, Plzeň, Olomouc, Liberec with Jablonec, Most with Litvínov) - on the national chain Prague built - ROS02 establishments, RES activity and the RÚIAN join, with their traps; the per-city RÚIAN coordinate control; the two-obec change a regional city needs; the tram leg (Brno's stops from KORDIS's CC BY feed, everything else from OpenStreetMap through the shared osm_tram module); the scope calls, halved rings, UTM per city (Ostrava 34N), the notices, the page-text template and a sheet per city. Use for any Czech city after Prague, with the city's brief; read with add-city, osm-rail and publish-city, which it does not replace.
---

# Building a Czech tram city

Written 2026-09-30 by the Czech kit session, from Prague's build (`DECISIONS.md`
2026-09-24, the week of 2026-09-20), the six briefs staging wrote on
2026-09-30, and live reads that day (the KORDIS feed, the screen's OSM caches,
`brief_check.py` on all six: 23 of 23 claims hold). Czechia is **Mexico's
shape**, like France: one national register chain, one address file per obec,
one national licence family. So a Czech city costs its tram leg, a scope call
and its notices. The register and taxonomy are shared code already.

**The batch** is the six Czech T1 cities in `docs/tram_city_list.md`: Brno,
Ostrava, Plzeň, Olomouc, Liberec (with Jablonec nad Nisou) and Most (with
Litvínov). Prague is built and draws its metro only.

**Every call is approved as recommended, the page text and notices word for
word** (owner, 2026-09-30: DECISIONS "The Czech batch's calls and prose
approved as recommended"). **Builds wait for the owner's explicit go**, which
approving the calls did not give. When it comes, build on a branch, never on
master: `app/` lands at review time only.

## Order of work for one city

1. `python scripts/brief_check.py <slug>`, and with `--vs-config` once the
   config exists. A failing claim is a brief to correct, and **the briefs are
   staging's**: ask staging, do not edit them from a build.
2. Read `docs/build_briefs/<slug>.md` and this skill's sheet for the city
   (the last section). The calls in both were put to the owner together.
3. `python scripts/scaffold_city.py --slug <slug> --name "<Name>"
   --system-name "<operator> trams" --taxonomy czech_nace2025 --lat <lat>
   --lon <lon> --region Europe --country Czechia --dry-run`, then without
   `--dry-run` once the owner has said go. Pass **the city's own longitude**:
   the script derives the UTM zone from it, which is what makes Ostrava 34N.
   Add `--mode tram` once the macro-legend branch has landed (its
   `scaffold_city.py` requires it).
4. Replace the generated `config.py` with the Czech template (section 8) and
   fill it from the sheet. Replace the generated step 3's GTFS line loader
   with `load_osm_line_shapes` (every Czech tram city draws its geometry from
   OSM, Brno included).
5. Write step 2 as Prague's (41 lines, a call to `build_storefronts`), step 1
   on `pipeline/osm_tram.py` (section 3), and `fetch_sources.py` (section 3).
   Run the steps, render, and run "Before publishing".

**No batch scaffold script** (DECISIONS "The Czech batch kit": measured, it
does not pay for six cities). Everything a script would fill is on the
sheets below.

## What already exists - reuse it, do not rewrite it

| Module | What it does |
|---|---|
| `pipeline/countries/czechia.py` | The national facts: ROS02, RES and CZ-NACE URLs, the SHARED cache (`data/czechia/raw/`: ROS02 58.5 MB, RES 543 MB, the five CZ-NACE 2025 codebooks), `RUIAN_ATOM_TEMPLATE`, the legal-form codes, the RÚIAN column names, CRS and encoding. Imported by every Czech `config.py`, so it stays lean-venv importable |
| `pipeline/countries/czechia_register.py` | **THE step 2**: `build_storefronts(cfg, bbox)`. ROS02 -> RÚIAN -> RES -> CZ-NACE 2025 -> storefronts. Imports pandas and pyproj, so only step files import it |
| `pipeline/taxonomies/czech_nace2025.py` | CZ-NACE 2025 on prefix at ragged depth; the structural exclusions (479, 5612, 562, 564, 964, 9691). It deliberately does not decide the catch-alls |
| `pipeline/prague/` | The built Czech city. Its step 1 is the model for Brno's stations (`parent_station`), its `fetch_sources.py` for the national files and the ATOM resolve, its `boundary.py` for polygonising an OSM relation with an area gate |
| `pipeline/aarhus/step1_stations.py` | The built OSM tram step 1 (`stop_rows()`), until `pipeline/osm_tram.py` exists |
| `pipeline/map_common.py` `load_osm_line_shapes` | Draws a line from OSM route relations by `ref`, one alignment per line (the relation with the most geometry) |
| `scripts/line_colour_search.py` | Chooses a palette where the operator's colours are unusable: 3:1 on both map pages, CIE76 45 or more from every pin, lines near each other kept apart |

## The owner's standing calls - do not re-ask

- **Trams-only maps are approved** (DECISIONS "Yes to trams-only maps",
  2026-09-29): with no metro, the trams are the rapid transit (Riga's
  precedent), and every tram stop gets rings. **No stop thinning.**
- **Ring size by the spacing rule** (section 5): halved at a median stop gap
  of about 550 m or less. All six measured 294 to 514 m.
- **The natural-person rule** (owner, Prague 2026-09-24): an establishment of
  a natural person at their own registered seat is **excluded**, and the pin
  of every other natural person (forms 101, 105, 107, 424, 425) or v.o.s.
  partnership (111) shows its **address, never the name**.
- **The catch-all rule** (owner, 2026-09-29): `CATCH_ALL_EXCLUDE = ("96990",
  "969")` in every Czech city ("other personal services", exact codes, the
  bare group included because RES is ragged). 96230 (day spas, saunas) is a
  specific class and stays.
- **The currency rule**: ROS02 drops closed establishments (active is judged
  by `DATUKON`), its snapshot (`DATPLAT`, 2026-08-31 today) is well under five
  years old, and the snapshot date goes on the page.
- **Brno's feed is fetched from `kordis-jmk.cz`** under KORDIS's own CC BY 4.0
  grant (owner, 2026-09-30), never from data.brno.cz or the stale
  `content.idsjmk.cz` copy.
- **Olomouc's trams come from OSM** (owner, 2026-09-30): DPMO's feed declares
  no licence, and its colours are all white.
- **Every Czech city tags `"region": "Europe"`.** A Central Europe split is
  the app/chrome role's question, not this skill's.
- **Buses, trolleybuses and trains are never drawn.** Brno's S-trains fail the
  spacing rule (11 stations at a 1,974 m median gap; the tram audit,
  2026-09-29).
- **Approved with the kit (owner, 2026-09-30, "all recommended approaches to
  the calls", "and prose")**:
  - the five OSM cities' colours are the project's own, from
    `scripts/line_colour_search.py` with target hues spaced evenly;
  - **Ostrava's line 5 is left out** (3 of 10 stops in the city);
  - **Liberec is "Liberec (Regional)", with Jablonec nad Nisou**;
  - **Most is built, last, as "Most (Regional)"**, covering Litvínov;
  - **Brno's H4 and P1 are left out**;
  - `mode` `tram` and `coverage` `full` for all six;
  - OSM stops collapse by Aarhus's rule (section 3), Brno's stations are
    the feed's parents;
  - the build order Brno, Plzeň, Olomouc, Ostrava, Liberec, Most;
  - the page text (section 7) and the notices (section 6), word for word.

## 1. The register chain - `czechia_register.py`, with its traps

Prague is the control: 25,275 storefronts from 84,192 active establishments
(2026-09-24). Change nothing in the module without re-running Prague's step 2
and `drift_check.py prague`.

- **ROS02 is the premises register; RES is not.** ROS02 records WHERE each
  establishment (`ICP`) trades (`PKODADM`, a RÚIAN address code). RES records
  the owner's registered SEAT, which is why Prague paused on RES alone. The
  location always comes from ROS02.
- **Rows repeat: dedupe on `ICP`.**
- **Active is judged against the file's own `DATPLAT`, never today**, so a
  drift check next month gives this month's answer.
- **6.6% of active establishments nationally carry no `PKODADM`** and cannot
  be placed. They fall out at the obec filter, silently. Step 2 prints the
  in-obec count; publish its figures, not the brief's.
- **The activity is the OWNER's single CZ-NACE 2025 code** (`NACE2025`, never
  the older `NACE` column), inherited by every establishment it holds: a
  chain's office counts as the chain's trade. The page says so.
- **`KATPO` is never read**: its `000` means "not stated", so it cannot be an
  employee filter.
- **RÚIAN is EPSG:5513 with the published (X, Y)**. The other axis orders land
  in Germany or the Arctic and still look like coordinates, which is why every
  city declares a control (section 2). An address with no coordinates
  transforms to INFINITY, not NaN; `ruian()` makes it missing first. The file
  is cp1250 with `;`.
- **RÚIAN comes through ČÚZK's ATOM service**, which names the current
  month's file. It sidesteps the VDP application's ban on automated
  extraction. Never hard-code a `vymenny_format` path: its date goes stale on
  the 1st.
- ⛔ **Never RŽP (the Trade Register) through ARES**, though it carries an
  establishment type. It is not open data, and ÚOOÚ fined a site in 2019 for
  republishing sole traders' trade data from it (UOOU-10201/18-31).
- **The national files are shared.** ROS02, RES and the codebooks live once in
  the main checkout's `data/czechia/raw/`, behind every worktree's `data/`
  junction. **Never refresh them from a city branch**: a new edition moves
  Prague too. A refresh is its own job, announced, with Prague re-run.
- **Step 2 reads the 543 MB RES file in 500,000-row chunks**, keeping only
  the city's owners: a measured **0.37 GB peak** (Prague, 2026-09-30), so it
  is not a heavy job under the owner's margin rule. Still run Czech step 2s
  one at a time, since they share one disk read.

The screen's figures (2026-09-27, `business_leg.py`): placement 100% in every
city, and the restaurant control (NACE 5611 against OSM's restaurants) at 1.61
to 3.71 times. Prague reads 1.59 to 1.63. A high ratio here is OSM's gap, not
the register's, so the page says so (section 7).

## 2. The RÚIAN control - one per obec file, or `ruian()` stops

`czechia_register.ruian()` exits unless the config declares
`RUIAN_CRS_CONTROL = (RÚIAN code, lat, lon, label)`: one known address in the
obec, whose expected position comes from **a source other than this file**
(the building's published coordinates, or OSM's node for it). It must come out
within 0.001° on both axes. Prague's is the castle. It was a module constant
until 2026-09-27, which would have stopped every other Czech town.

All eight obce files have one, measured by staging on 2026-09-30 (the sheets),
Jablonec's (563510) and Litvínov's (567256) included. For a new obec: pick the
town hall, take OSM's node for it through a bbox-bounded query, and find its
RÚIAN code in the obec file.

### Two obce: the one change to shared code

Liberec (Regional) and Most (Regional) each span two obce, and the module
reads one (`cfg.OBEC`, `cfg.RUIAN_ZIP`, `cfg.RUIAN_CRS_CONTROL`). **Extend it
once, in `czechia_register.py`, never a fork** (Monterrey's and
Kitchener–Waterloo's regional precedent):

- the config declares `OBEC_CODES` (a list, one code for a single-obec city)
  and `RUIAN_CRS_CONTROLS = {obec: (code, lat, lon, label)}`, with one file
  per obec at `DATA_RAW / f"ruian_adr_{obec}.csv.zip"`;
- `ruian()` reads each file, runs **that file's** control, and concatenates.
  Address codes are national, so assert the index stays unique;
- step 2 prints and emits the placed count per obec, for the page;
- a config with only `OBEC` (Prague) takes the old path unchanged.

**Done 2026-09-30, on `czech-build`**, with RES read in 500,000-row chunks of
the city's own owners. The control was Prague's step 2, run from the branch
into the scratchpad (never into the shared `data/prague/processed/`):
byte-identical, every baseline count equal, **peak 0.37 GB**. So a Czech
step 2 is not a heavy job; announce it as a 0.5 GB one, one at a time.

## 3. The tram leg

### Brno: stops from KORDIS's feed, lines from OSM

- **Feed**: `https://kordis-jmk.cz/gtfs/gtfs.zip`, about 9 MB, republished
  weekly on Sunday. **No `feed_info.txt` and no `shapes.txt`.** Read
  2026-09-30: calendar 2026-09-25 to 2026-12-13, calendar_dates to
  2026-12-10.
- **Route types**: 299 bus, 28 rail, 14 trolleybus (800), 13 tram (0), 1
  ferry. Select `route_type 0` AND `route_short_name` in the 11 regular lines
  (1-10, 12). H4 (heritage) and P1 (the Arena Brno event shuttle, sharing line
  1's colour) run no weekday trips; both are out (owner, 2026-09-30).
- **Stations are the feed's own `parent_station` rows, Prague's shape.** All
  329 platforms the 11 lines serve have a parent (2026-09-30): 149 parents, no
  two sharing a name. Take the parent's id, name and coordinates; no name
  collapse and no mean. Exit if a platform has no parent or two parents share
  a name, as Prague's step 1 does.
- ⚠️ **Request stops are stops.** KORDIS codes every request stop (*na
  znamení*) `pickup_type`/`drop_off_type` **3**, which GTFS counts as
  boardable. `boardable_stop_ids`' old default accepted only 0 and dropped **25
  of 149 stations** as "non-revenue"; the default is `("0", "2", "3")` since
  `d928f50` (owner, 2026-09-30), so a new step needs no argument.
- ⚠️ **The feed carries 2.5 months of timetable, so a line's union of trips
  is too wide** (line 4: 54 stations against a 24-stop route). A line serves a
  station when it calls there on **at least 10% of its trips in one
  direction** (`STOP_MIN_SHARE`; Riga's threshold, per station, not per
  exact pattern). Measured: it drops only the Vozovna Medlánky depot. Built:
  **148 stations, 146 in the city**, 336 m median.
- **The spacing gate's floor is 200 m for trams** (`SPACING_MIN_M`, Riga's
  and Aarhus's), never the shared 400 m metro default.
- **Colours are the feed's `route_color`** (DECISIONS 2026-09-30). All 11 pass
  `check_line_colours` as published; line 6's `0777C1` is closest to the pins,
  at 13.2 from Retail, recorded rather than moved (Prague's line C precedent).
- **Geometry from OSM**: `load_osm_line_shapes` by `ref`. OSM carries all 11
  refs, operator "Dopravní podnik města Brna", 26 relations, and even the
  feed's own colours in `colour`. Use `osm_tram`'s lines-only mode to
  validate the relations (every ref present, every relation kept or placed).
- **Gate 3**: OSM's route relations' stop names per line, which are
  independent of the feed. Built: 9 of 11 lines agree; lines 1 and 10 run
  variants on 12-21% of trips (line 1 via Tábor, line 10 to Technologický
  park and Bystrc) that OSM's relations lack. The feed is the operator's, so
  this is recorded, not "fixed".
- **The feed self-attests nothing**, so `fetch_sources.py` records the
  calendar window (the earliest `start_date` and latest `end_date` across
  `calendar.txt` and `calendar_dates.txt`) in `provenance.json`, prints it,
  and refuses an expired feed.

### The other five: OpenStreetMap, through `pipeline/osm_tram.py`

Agreed with the tram kit session on 2026-09-30: **one country-neutral module,
`pipeline/osm_tram.py`, written by whichever OSM tram build goes first** (Czech
or the tram kit's), from Aarhus's `stop_rows()`. Its control is Aarhus's
inputs reproducing Aarhus's `stations.csv`; Aarhus itself is not rewired. It
is shared pipeline code, so **tell the app/chrome role before writing it**.
If it exists, use it. Its contract:

1. **Relations by route AND operator AND ref**, one Overpass query per city
   over a bbox (osm-rail). Never a node tag search.
2. **Every relation in the box is kept or placed in `NOT_DRAWN` by relation
   id with a reason; the step exits on one that is neither.** Ostrava's 9 and
   19 (no stop members), its unref'd line 11 variant (19177807) and Plzeň's
   1X, 4X and depot run (no stops) are placed, not dropped silently.
3. **Several relations per ref are normal** (Ostrava's line 8 has four):
   a line's stops are the union of its kept relations; the drawing takes the
   one with the most geometry.
4. **Stop members** are `public_transport=stop_position` or
   `railway=tram_stop`; exit only on a member that is untagged or unnamed,
   naming it. `STATION_ADD` by node id covers a stop on no relation.
5. **Stations are collapsed by exact name at the mean of their stop
   positions within 200 m**, exiting when a name spreads wider (Aarhus). This
   is the OSM rule. France's never-a-mean rule came from the French portal's
   ODbL conditions and does not reach OSM or Czechia.
6. **Scope over a union of polygons** (two obce), stations outside named with
   the obec or town they lie in.
7. **The operator filter is optional** for the tram kit's cities. Czech
   relations all carry one (the sheets), so set it.

**It exists now** (the tram kit's, on `tram-build`; taken unchanged onto
`czech-build`, its Aarhus control passing). The Czech wrapper is
`pipeline/countries/czechia_osm_tram.py`: a city's step 1 is
`step1(config)` and its step 3 `step3(config, system_name)`. Step 1 writes
each kept ref's relation with the most track to `lines.geojson`, which step 3
draws, so the drawn lines are exactly the kept ones. What the five taught:

- **An unjudged relation stops the step, and that is the point.** Plzeň's two
  line 4 directions carry **no operator tag** in OSM: named in `NOT_DRAWN`,
  their reverse directions kept, and the excluded list shows whether a stop
  was lost (none was).
- **One station under two names**: OSM names a stop's stands apart
  (Ostrava's Hranečník (St. 1) / (St. 5), 120 m apart; Nová Huť hlavní brána
  1 / 2, 61 m). The station gate's close-pair note finds them; fold each with
  `STATION_NAME_ALIASES` into the spelling more lines carry.
- **An interchange on two arms of a junction** can spread past 200 m
  (Ostrava's Sport Aréna 321 m, Mariánské náměstí 223 m). Raise that city's
  `COLLAPSE_MAX_SPREAD_M` on the measurement (Ostrava 330), inside Riga's 300
  and Osaka's 400, and record the next widest name.
- ⚠️ **Count a feed by SERVICE DAY, never over the whole file.** Plzeň's gate 3
  first counted PMDP's trips across its six-month calendar and "found" two
  centre stops OSM lacks, Jízdecká and U Synagogy. Both run on **one day
  only** (service 44: no weekday flags, 2026-10-10 by `calendar_dates`), a
  diversion. On an ordinary Wednesday at the 10% rule, line 2 matches OSM
  exactly, and lines 1 and 4 differ only by the depot. A `STATION_ADD` taken
  from a whole-feed count would have drawn rings round a one-day diversion.
  Where no feed can be read (Olomouc, Ostrava, Liberec, Most), gate 3 is an
  open gap in the config, never a silent pass.

**Line colours: OSM tags none** in the five cities, and no operator's colours
are licensed. Use the project's own palette (Riga's precedent, and Le Havre's
approved call): `scripts/line_colour_search.py <slug>` with the config's
`LINES[key]["hue"]` targets spaced evenly around the hue wheel in line order,
and cite the run in the config. It needs step 1's `lines.geojson`, so run it
after step 1. Never take colours from an operator's website or network plan.

**Gate 3 for an OSM city** needs a count OSM did not make: the operator's
published stop list per line (a count, as Prague used Wikipedia's), or, for
Plzeň, PMDP's feed (read 2026-09-30, permitted; lines 1, 2 and 4 as
`route_type 0`, no colours, no shapes; `https://jizdnirady.pmdp.cz/jr/gtfs`,
GET only). Name the source in `OPERATOR_COUNTS_SOURCE`.

### `fetch_sources.py`, per city

Thin over **`pipeline/countries/czechia_fetch.py`** (built 2026-09-30, imported
only by fetch scripts), with `pipeline/countries/czechia_boundary.py` reading
the boundary for the steps. On Prague's, with these differences:
- **Feeds are rolling: always download**, even when a copy exists. That covers
  Brno's GTFS and every city's OSM query. Prague's keeps a cached copy unless
  `--force`; do not copy that for a feed.
- **The national files are only checked**, never refetched from a city branch
  (section 1). Record the ROS02 snapshot (`DATPLAT`) in `provenance.json`, as
  Prague does, for the page.
- **RÚIAN**: resolve each obec's file through ATOM on every run and record its
  name (it carries the edition date).
- **The OSM boundary**: `rel(<id>);out geom;` for each obec's relation (the
  sheets). Gate it on `ref` ending in the obec code (OSM's obec `ref` is the
  district code plus the RÚIAN obec code: Brno's is `CZ0642582786`) and on
  area, as Prague's `boundary.py` gates on ČÚZK's area.
- **The screen's 2026-09-27 OSM caches** (`data/_staging_scratch_2026-09-27/
  second_cities/czechia/osm_<city>_*.json`) are evidence, never build input.

## 4. Scope - the obec, or two

The businesses are scoped by **RÚIAN's own address list** for the obec
(ROS02's `PKODADM` in it), never by a polygon. The OSM polygon scopes stations
and anchors labels only.

- **One obec**: Brno, Ostrava, Plzeň, Olomouc. Brno's line 2 keeps 36 of 38
  stop names (its Modřice branch leaves the city); every other line in the
  four stays whole, apart from Ostrava's line 5 (left out, owner, 2026-09-30).
  Step 1 asserts `EXPECTED_INSIDE_PER_LINE`; a change is a decision re-taken.
- **Two obce, "(Regional)"** in the display name, as Lille's: Liberec with
  Jablonec nad Nisou (line 11 is 14 + 7), and Most with Litvínov. **Most alone
  fails the stub test** (its lines keep 12 of 24, 6 of 18 and 9 of 21), so the
  joint scope is not optional there. The slug stays the core city's (`liberec`,
  `most`).
- **The stub rule** the scope follows: Toulouse's 52% stayed; the stub
  precedents are Minneapolis and Pittsburgh at 42% (owner). Ostrava's line 5 at
  3 of 10 (30%) is below them all.

## 5. Rings, and the CRS per city

**Halved rings for all six**: edges `[0.0, 0.05, 0.1, 0.2, 0.3]` mi, labels
`0-0.05 mi` to `0.2-0.3 mi`, because every city's median stop gap is under
about 550 m (the briefs, 2026-09-30: Plzeň 294, Olomouc 318, Brno 329, Liberec
with Jablonec 378, Ostrava 424, Most with Litvínov 514). Step 1 prints the
in-scope median; the config comment records it; `scripts/ring_rules_table.py
--write` regenerates `docs/ring_rules.md` after the city lands. **Most is 36 m
from the line**: if its build-day median is over 550, keep the standard edges
and drop the page's half-size sentence.

**UTM per city, never copied**: EPSG:32633 (33N, 12-18° E) for Brno, Plzeň,
Olomouc, Liberec and Most; **EPSG:32634 (34N) for Ostrava**, at 18.29° E. Never
EPSG:4326 for distance, and never RÚIAN's S-JTSK for this project's geometry:
it is converted on read.

## 6. Notices

The page's notices come from `app/components.py` `_NOTICES`, one per
database. Wording is the owner's; draft any new one in chat first.

| Source | Cities | What it needs |
|---|---|---|
| **RES** (ČSÚ), CC BY 4.0 with ČSÚ's data conditions | all six | The existing "Czech Statistical Office (Prague)" notice. Its text names no city, so **add each city to the title**, as Norway's "(Oslo, Bergen)" and Denmark's "(Copenhagen, Aarhus)" do. It discharges ČSÚ's two duties: link the conditions, and mark the data as derived, not official statistics |
| **RÚIAN** (ČÚZK), CC BY 4.0, "ČÚZK, <year>" prescribed | all six | The existing "ČÚZK (Prague)" notice, the title extended the same way. The year is the file's |
| **ROS02** (DIA) | all six | Declared open data, no personal data, no database right: **nothing to display** (read 2026-09-24). Name it in the page text |
| **KORDIS JMK's GTFS**, CC BY 4.0 (read 2026-09-30) | Brno | **A new notice**: credit KORDIS JMK, a.s. and DPMB (the feed's `agency.txt` reads "IDS JMK (Data from: KORDIS JMK, DPMB)", which CC BY §3(a)(1)(A) says to retain); name data.brno.cz (Statutární město Brno) as the distributor; CC BY 4.0 linked; a link to the feed; the changes. No endorsement, no IDS JMK, KORDIS or DPMB logos. **The wording, approved (owner, 2026-09-30)**, is below the table |
| **PMDP's GTFS**, if used as Plzeň's gate 3 | Plzeň | Credit it anyway, on the stricter CC BY reading: "Plzeňské městské dopravní podniky, a.s. (PMDP), GTFS published by the Statutory City of Plzeň at opendata.plzen.eu, CC BY 4.0, modified by this project". Never the city's arms or PMDP's logo |
| **OpenStreetMap**, ODbL 1.0 | all six | © OpenStreetMap contributors on the render, and **a clause in the "OpenStreetMap (rail geometry)" notice** for each city: its tram lines (and, except Brno, their stops) and the obec boundaries used to select them |

**Brno's notice, approved word for word (owner, 2026-09-30)**, titled
"KORDIS JMK (Brno)":

> Tram stops for Brno come from the IDS JMK timetable data (GTFS) published by
> KORDIS JMK, a.s., with data from KORDIS JMK and DPMB, and distributed by the
> Statutory City of Brno at data.brno.cz, under
> [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
> ([feed](https://kordis-jmk.cz/gtfs/gtfs.zip)). Changes: the 11 regular tram
> lines are selected, each stop is reduced to one point, and distance rings are
> computed around it. Not produced or endorsed by KORDIS JMK, DPMB or the City
> of Brno.

**The existing notices (approved the same day)**: the ČSÚ and ČÚZK titles add
each Czech city as it lands ("Czech Statistical Office (Prague, Brno)", and so
on), their text unchanged; each city adds its clause to "OpenStreetMap (rail
geometry)".

Also, for each city: a row per new source in `docs/data_sources/czechia.md`
(the feed or the OSM tram relations, the RÚIAN file, the boundary) **before the
page exists**; the excluded categories in `docs/excluded_categories.md`; and
`check_scope_disclosure.py` passing.

## 7. Page text - approved by the owner, word for word (2026-09-30)

Braces are per-city facts, filled from this city's own step 1, step 2 and
rendered map, never from a brief. Brackets choose a variant. **Departures are
owner calls, never edits.**

**Title**: "{City}: commercial density around tram stops" (Riga's).

> {N} tram lines are drawn, **{operator}'s trams {lines}**, each labelled on
> the map and in the legend. *[Brno:]* The stops come from the IDS JMK
> timetable data published by KORDIS JMK, and the lines are shown in the
> operator's colours; their routes are drawn from OpenStreetMap, because the
> timetable data carries none. *[The other five:]* The lines and stops are
> drawn from OpenStreetMap, and the colours are this project's, because none
> are published for reuse. {City} has no metro: its trams are its rapid
> transit, as Riga's are, so every tram stop gets rings. Buses, trolleybuses
> and trains are not drawn{Brno: ", nor the heritage tram H4 or the event
> shuttle P1"}.
>
> The map covers the **{city of X / cities of Liberec and Jablonec nad Nisou,
> which tram line 11 joins / towns of Most and Litvínov, which the trams
> join}**. {Brno: "Line 2's last two stops, in Modřice beyond the city
> boundary, are left out." / Ostrava: "Line 5, the suburban line to Budišovice,
> is not drawn: only 3 of its 10 stops are in the city."}
>
> Businesses come from the Czech **register of active business establishments**
> (ROS02), which records each place where a business operates at that place's
> own address, placed using the national address register (RÚIAN), the same
> sources as Prague's map. What each establishment does comes from the Czech
> Statistical Office's business register (RES). RES records one main activity
> per business, so every establishment inherits its owner's, and a chain's
> office or warehouse counts as the chain's trade. **Where a business belongs to
> a person trading in their own name, or to a partnership, the map shows its
> address instead of its name.** Where such an establishment is at the owner's
> own registered address, which is usually their home, it is left off the map
> altogether.
>
> **Read the density as a register, not a street survey.** Some establishments
> are newly registered and may not have opened yet. Czechia's classification
> files a web shop under the goods it sells, so some dots are businesses with
> no shop a passer-by could walk into. Against OpenStreetMap's mapped
> restaurants, cafés and takeaways in the city, the register carries about
> **{ratio} times** as many. {Where the ratio is over 2 (Ostrava, Liberec and
> Most at the screen): "OpenStreetMap maps fewer restaurants here than in
> Prague, so the ratio says as much about OpenStreetMap's gaps as about the
> register."} Businesses whose main activity is something else, such as a
> brewery's pub or a wholesaler's shop, are not shown, because no open source
> records what each establishment itself does.
>
> **Tram stops sit closer together than metro stations**, a median of
> {spacing} m here, so the rings are drawn at half the usual size (0.05 to
> 0.3 mi). **About {share} of storefronts sit within a ring.**

Then the controls paragraph and the heat-layer caveat, exactly as on Prague's
page (`app/pages/28_Prague_Heatmap.py`).

**Caption** (from `provenance.json`): "Snapshot: establishments as of **{DATPLAT}**
(ROS02); tram timetable data valid **{start}** to **{end}** (KORDIS JMK)" for
Brno; for the OSM cities, the second half reads "tram lines and stops from
OpenStreetMap, fetched **{date}**".

A city whose build-day median stop gap is over about 550 m (only Most is
close) keeps the standard rings and drops the last paragraph's first
sentence.

## 8. The config template

Paste over `scaffold_city.py`'s generic config, keeping its path block, and
fill the braces from the sheet. Each value carries a comment saying where it
came from, as Prague's does.

```python
from pipeline.countries import czechia as CZ  # noqa: F401  (the national facts)

SLUG = "{slug}"
# ... scaffold_city's path block, plus:
PROVENANCE_JSON = OUTPUTS / "provenance.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_TRAM_JSON = DATA_RAW / "osm_tram.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"   # for line_colour_search.py

# --- Scope ---
SCOPE = "{obec|regional}"
OBEC_CODES = [{obec codes}]
RUIAN_CRS_CONTROLS = {{obec}: ({code}, {lat}, {lon}, "{label}")}   # per file
OSM_BOUNDARY_RELATIONS = {{obec}: {relation id}}   # gated on ref and area
BOUNDARY_AREA_KM2 = ({lo}, {hi})   # the union, against ČÚZK's area

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_PROJECTED = "{EPSG:32633 | EPSG:32634 for Ostrava}"

# --- Rings: halved on the spacing rule; the measured median in the comment ---
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Trams ---
TRAM_SOURCE = "{kordis_gtfs|osm}"
OSM_TRAM_BBOX = ({s}, {w}, {n}, {e})   # the brief's check box
OSM_TRAM_OPERATOR = "{operator, exactly as OSM tags it}"
LINE_ORDER = [...]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
LINES = {k: {"hue": "#..."} for k in LINE_ORDER}   # OSM cities: target hues
LINE_COLOURS = {...}   # the feed's (Brno) or line_colour_search.py's, cited
NOT_DRAWN = {relation_id: "reason"}   # every relation not kept
EXPECTED_INSIDE_PER_LINE = {...}   # step 1 asserts it
OPERATOR_STATION_COUNTS = {...}; OPERATOR_COUNTS_SOURCE = "..."   # gate 3

# --- Businesses ---
TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2
{CITY}_BBOX = {...}   # the placed storefronts' extent plus ~0.02 deg

# --- The macro map ---
MAP_MODE = "tram"
MAP_COVERAGE = "full"
```

`brief_check.py <slug> --vs-config` diffs `OBEC_CODES`, `CRS_PROJECTED`,
`SCOPE`, `MAP_MODE` and `MAP_COVERAGE` against the brief: each brief's CRS
check carries the mappings (staging, 2026-09-30). `SCOPE` is `"obec"` or
`"regional"`, and `OBEC_CODES` is a list of strings, as the briefs have them.

## 9. The macro map and the app entry

- **Two keys** (the macro-legend branch, approved): `mode` is the dot colour,
  `coverage` the fill. All six are `mode` `"tram"` and `coverage` `"full"`
  (ROS02 and RES carry all three buckets), as the briefs propose.
- The `app/cities.py` entry follows Prague's: `placement` "Joined by address
  ({share})", `data_age` "As of {DATPLAT}", `record_kind` "National register",
  `categories` "All three", `country` "Czechia". The label width is measured
  in a real browser for `check_macro_labels.py`.
- Landing: in groups, one sitting each, per `docs/review_time.md`, with one
  `city-added` deploy-verify per group. Approvals and `app/` landings wait for
  review time. Landing `app/cities.py` means rebooting the deployed app.

## Before publishing (each city)

`python scripts/check_personal_exposure.py <slug>`, after adding the city to
its table in Prague's shape (`processed="businesses_clean.csv"`,
`address=("business_name",)`: the structural guarantee by legal form), with
the verdict in `DECISIONS.md`; `python scripts/check_provenance.py` names the city OK; `python
scripts/check_scope_disclosure.py` passes; `python scripts/check_map_markup.py`
passes (line-colour contrast); `python pipeline/drift_check.py <slug>`; `grep
-rn TODO pipeline/<slug> app` is empty; a `DECISIONS.md` entry
(`decisions-entry`). Then `publish-city`.

## The six, one sheet each

Figures are the briefs' and the 2026-09-30 reads. Storefronts are the screen's
(2026-09-27), and step 2 replaces them. Every call was **approved as
recommended** (owner, 2026-09-30).

### Brno

| | |
|---|---|
| Obec | 582786; OSM relation 438171 (`ref` CZ0642582786) |
| Control | `("19095597", 49.1936, 16.6069, "Brno New Town Hall")`, Dominikánské náměstí 196/1 |
| CRS | EPSG:32633 |
| Trams | KORDIS feed, lines 1-10 and 12, `route_type 0`; 149 parent stations network-wide, 147 inside the city (the tram list's 146 was the screen's count); line 2 keeps 36 of 38 |
| Geometry | OSM, operator "Dopravní podnik města Brna", 26 relations, all 11 refs |
| Colours | The feed's: 1 D40000, 2 4AB95D, 3 009E9E, 4 EE7E1E, 5 F31D7F, 6 0777C1, 7 939DAC, 8 E1CB31, 9 8C4A9A, 10 A05A2C, 12 00CCFF |
| Spacing | 329 m: halved rings |
| Storefronts | 7,229 (retail 2,520, food 2,126, personal 2,583); restaurants 1.61× OSM |
| Calls | **approved**: H4 and P1 out; built first |
| Notices | ČSÚ, ČÚZK, a new KORDIS notice, OSM (lines) |

### Ostrava

| | |
|---|---|
| Obec | 554821; OSM relation 437354 (`ref` CZ0806554821) |
| Control | `("3182860", 49.84130, 18.28927, "Magistrát města Ostravy, 30. dubna 635/35")` |
| CRS | **EPSG:32634 (UTM 34N)** |
| Trams | OSM, operator "Dopravní podnik Ostrava": 1-4, 6-8, 10-12, 14, 15, 17, 18; 96 stop names inside |
| Not drawn | 9 and 19 (no stop members); relation 19177807 (an unref'd line 11 variant); line 5 (approved) |
| Spacing | 424 m: halved rings |
| Storefronts | 3,971; restaurants 2.23× OSM (OSM thin) |
| Calls | **approved**: line 5 out (3 of 10 stops inside, 30%; costs Poruba,koupaliště and Krásné Pole); the project's palette; fourth in order |
| Traps | 34N; 33 or 34 relations and 18 refs on 2026-09-30 (OSM moved between reads, so step 1 counts, not the brief); line 7 has a 2-stop relation (17625150) beside its full one |

### Plzeň

| | |
|---|---|
| Obec | 554791; OSM relation 438344 (`ref` CZ0323554791) |
| Control | `("24570222", 49.74836, 13.37775, "Magistrát města Plzně, náměstí Republiky 1/1")` |
| CRS | EPSG:32633 |
| Trams | OSM, operator "Plzeňské městské dopravní podniky, a.s.": 1, 2, 4; 53 stop names, all inside |
| Not drawn | 1X, 4X and a depot run from Vozovna Slovany (no stop members; one untagged operator) |
| Gate 3 | PMDP's GTFS (permitted), credited if used |
| Spacing | 294 m: halved rings |
| Storefronts | 3,513; restaurants 1.99× OSM |
| Calls | **approved**: the project's palette; second in order |

### Olomouc

| | |
|---|---|
| Obec | 500496; OSM relation 437057 (`ref` CZ0712500496) |
| Control | `("25321960", 49.59393, 17.25164, "Olomouc Town Hall, Horní náměstí 583")` |
| CRS | EPSG:32633 |
| Trams | OSM, operator "Dopravní podnik města Olomouce": 1-7, 14 relations; 36 stop names, all inside |
| Spacing | 318 m: halved rings |
| Storefronts | 2,246; restaurants 1.80× OSM |
| Calls | **approved**: the project's palette; third in order. DPMO's feed is not used at all, not even for gate 3 |

### Liberec (Regional)

| | |
|---|---|
| Obce | 563889 Liberec (OSM 439073, `ref` CZ0513563889) + 563510 Jablonec nad Nisou (OSM 438931, `ref` CZ0512563510) |
| Controls | Liberec `("23653124", 50.77000, 15.05845, "Liberec Town Hall, nám. Dr. E. Beneše 1/1")`; Jablonec `("12188018", 50.72452, 15.17128, "Jablonec Town Hall, Mírové náměstí 3100/19")` |
| CRS | EPSG:32633 |
| Trams | OSM, operator "Dopravní podnik měst Liberce a Jablonce nad Nisou": 2, 3, 5, 11; 39 stop names in scope, every line whole (line 11: 14 + 7) |
| Spacing | 378 m: halved rings |
| Storefronts | 2,498 (Jablonec 618); restaurants 2.45× OSM |
| Calls | **approved**: with Jablonec, as "Liberec (Regional)" (Liberec alone would keep line 11 at 14 of 21, 67%); the project's palette; fifth in order |
| Traps | the two-obec change (section 2); DPMLJ's own GTFS reset the connection at the screen |

### Most (Regional)

| | |
|---|---|
| Obce | 567027 Most (OSM 436570, `ref` CZ0425567027) + 567256 Litvínov (OSM 436574, `ref` CZ0425567256) |
| Controls | Most `("25298429", 50.50284, 13.64078, "Most Town Hall (Magistrát), Radniční 1/2")`; Litvínov `("5150507", 50.59881, 13.61171, "Litvínov Town Hall, náměstí Míru 11")` |
| CRS | EPSG:32633 |
| Trams | OSM, operator "Dopravní podnik měst Mostu a Litvínova": 1-4, 8 relations; 27 stop names in scope, every line whole |
| Spacing | 514 m: halved rings, 36 m under the line |
| Storefronts | 1,030 (Litvínov 241); restaurants 3.71× OSM (OSM thin) |
| Calls | **approved**: built, last (the smallest Czech page), as "Most (Regional)" covering Litvínov; the project's palette |
| Traps | the joint scope is required; the two-obec change |
