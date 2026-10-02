# Handoff: Seattle (Regional), then Tbilisi (2026-10-02)

For one build session that builds **Seattle (Regional)** first and
**Tbilisi** after it. Written by staging; the owner approved the plan the
same day ("should we pass the seattle regional brief to a new session? and
queue Tbilisi after?", then "yes").

**✅ Seattle (Regional) is RELEASED by the owner, 2026-10-02.** It works in
`.claude/worktrees/seattle-tbilisi` on branch `seattle-tbilisi-build`. There,
`data/` and `.venv-lean` are junctions to the main checkout's. The branch
has no upstream, so a plain `git push` can never reach master.

**🛑 Tbilisi is QUEUED, not released.** Start it only when:
1. Seattle is green and committed;
2. the owner has answered Tbilisi's three 🚨 items in its brief (placeholder
   coordinates, division 45, region) — check the brief and the staging
   drafts file; staging records the answers there;
3. the UK six session's UK-region pass has landed or been reported done,
   because Tbilisi's macro label is measured in a Europe that pass changes.
   Tbilisi's data steps do not wait on it, only its macro label.

**Two other build sessions run at the same time**: the UK six
(`uk-six-build`) and the Japan batch (`japan-batch-build`). Each edits
`app/cities.py`'s region list and claims numbers; see "Numbers" below.

**Delete this file** once both cities have landed.

---

## Seattle (Regional): one lead, agents only for clean splits

**The brief is `docs/build_briefs/seattle.md`, and every owner call in it is
settled** (2026-10-01 and 2026-10-02; no 🚨 left). Read it in full,
especially "The regional screen", "What the build has to pull" and "Open for
the owner (2026-10-02)", then `multi-source-city`, `add-city`,
`address-join`, `osm-rail` and `publish-city`.

**Why one lead and not the UK or Japan layout.** Seattle (Regional) is ONE
page built from five sources across 11 cities, all meeting in one step 2,
one set of rings and one set of rules. It does not split by city. The lead
builds the spine; an agent takes a source leg only where it is independent
and returns a file plus its counts:
- **Agent-able:** the Liquor Board off-premise layer (filter to active,
  join premises addresses to the King and Snohomish address points, trade
  name only); the Snohomish layer (Restaurant and Grocery only, the
  jurisdiction field, not the postal city).
- **The lead's own:** Seattle's register, Bellevue's register, King County
  food joined to parcels, the cross-references between them, rail, step 2's
  merge, the page and every gate.

**The settled calls, in one place** (each in the brief with its numbers):
- **Rail from OpenStreetMap** (`osm-rail`; ODbL, notice 1). Sound Transit's
  GTFS is NOT used (its Transit Data Terms; owner 2026-10-02). Gate 3's
  independent count comes from Sound Transit's own station pages: **39
  stations in 11 cities**, Pinehurst included (opened 2026-09-30).
- **Seattle's register** (PERMITTED WITH CONDITIONS, non-commercial):
  - scope to the city polygon (drops 1,012 rows, 168 in the buckets);
  - keep `HEADER QUARTER` and `BRANCH`, and apply the head-office rule to
    headquarters rows (Taipei and Taichung's; flags 9);
  - **every licence year kept**; a lapsed FOOD row (licence year 2025 or
    earlier) stays only if King County inspected a matching business in
    2025 or 2026, by trade name or street address; lapsed retail and
    personal rows stay, disclosed as possibly closed. Measure what the food
    cross-reference drops, by year, and hand-sample 20 address-only matches.
  - catch-alls 459999 and 812199 hand-sampled for the personal-exposure
    treatment (Los Angeles's).
- **Bellevue's register** (read as permitted, option 1): its **food comes
  from King County's inspections**, as in every King County city; its
  **retail and personal services** take the **2010-01-01 issue-date
  cutoff**; a row without a trade name shows its category, never a legal
  name. `check_personal_exposure.py` is essential (1,174 sole
  proprietorships).
- **King County food inspections** (read as permitted, option 1): display
  "Public Health – Seattle & King County" and "Data provided by permission
  of King County"; no logo; from the address points take only geometry and
  the County's own fields, never the USPS ZIP+4 fields.
- **Snohomish County "Food Service Establishments (2025)"** (SILENT, read
  permissively, owner 2026-10-02): Restaurant and Grocery points only, by
  the layer's jurisdiction field (Lynnwood 310 facilities, Mountlake Terrace
  56). Credit "Snohomish County, Food Service Establishments (2025)", never
  the health department. Its data is no newer than 2025-11-19; the page says
  2025 and never calls it current or complete.
- **The Liquor Board off-premise list** (PERMITTED WITH CONDITIONS,
  non-commercial): a partial retail layer outside Seattle and Bellevue,
  "shops licensed to sell alcohol only"; trade name only; the page states
  the list's date and repeats the Board's data-transfer-error notice if it
  is still on the lists page at build.
- **Personal services outside Seattle and Bellevue: none published,**
  disclosed per city.
- **Rings across a city line** take the neighbour's data or are stated as
  unmapped.

**Mode and label:** `light_rail` (Link). Region `United States West`; the
macro label is measured with `check_macro_labels.py` like any other.

## Tbilisi (queued): the first city in Georgia

**The country profile is `docs/georgia_step0_endpoints.md`; the brief is
`docs/build_briefs/tbilisi.md`.** Read the `add-country` skill's "The country
file is PROVISIONAL" and "The new country on the reference pages" sections
before building: promoting Georgia's endpoints into
`docs/data_sources/georgia.md`, its notice and its reference-page headings
is part of this build, not a tidy-up.
- **Already decided (owner, 2026-10-01):** Geostat's register, the
  undercount disclosed (enterprises, not premises); individual entrepreneurs
  (64%) as unnamed dots, category only; personal ID columns dropped in
  memory before anything is written; Geostat permitted with attribution
  (terms stored in `docs/licenses/`).
- **Traps (the profile):** `X` is latitude and `Y` longitude; the API has no
  column selection; about 50 requests a window (HTTP 429 with
  `retryAfter`: back off, never loop); names come in Georgian script, so
  `check_personal_exposure.py` needs a Georgian pass; use `Activity_2_Code`.
- **Open for the owner** (🚨 in the brief): placeholder coordinates,
  division 45, region. Do not start before they are answered.
- **Mode `metro`.** Tbilisi Metro, 2 lines, 23 stations (OSM 16 + 7, the
  operator's own count).

## Numbers

- **Pages reserved:** Seattle (Regional) **174**, Tbilisi **175**
  (`docs/session_roles.md`). Scaffold with `--page-number`.
- **Notices:** the UK six hold **84–96** and the Japan batch **97–108**,
  both claimed on their own branches. Claim this session's block from
  **109** in `docs/session_roles.md`, and say so to staging.

## Gate order (Band B's, `docs/band_b_retrospective.md`)

1. personal exposure, plus a row in `docs/privacy_verdicts.md`;
2. provenance;
3. scope disclosure, written to `docs/city_page_format.md`;
4. the inconsistency rows and `cities.py` fields;
5. the master list (Seattle leaves Band C, Tbilisi Band B);
6. macro facts and the macro label;
7. the decisions entry;
8. commit;
9. the drift check, its baseline and ring shares;
10. merge master, `check_all.py`, and push at 0 behind.

**Not to master** until the owner's review time.

## Session rules (CLAUDE.md)

- **Decisions go to `docs/decisions_drafts/seattle-tbilisi.md`.**
- **Overpass:** one query in flight per session, one per city; wait 60 s
  after a 504 or 429. Only the lead queries.
- **`data/` is one shared junction.** Never re-run another city's step.
  `data/seattle/raw/` already holds the brief's downloads (the on-premise
  list; a Sound Transit GTFS copy used for counting only, not a source).
- **Memory:** King County's parcels and address points are the largest
  inputs. Run anything with an unknown peak through `heavy_job.py`; three
  build sessions share the machine.
- **Personal data:** Bellevue's sole proprietorships, Seattle's
  person-named trade names and Tbilisi's individual entrepreneurs. Select
  columns before printing; never print, store or quote a person's name, ID,
  phone or address.
- **No backslash or backtick in a Bash command.** Write a script file.
- **Downloads** named in a brief or skill are pre-permitted; anything else
  goes to the owner. **A failing brief claim** goes to staging. A 429 from
  Geostat or a RETRY from Overpass is not a failing claim.
