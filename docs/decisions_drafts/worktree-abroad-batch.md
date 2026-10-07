# DECISIONS drafts - Abroad batch (`worktree-abroad-batch`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

## Parked calls

Numbered for Staging's wave list; each with a recommendation and its
tradeoff. A parked call stops only what it names.

1. **Bremen: the unversioned CC BY and the database right.** The
   licence-read agent (2026-10-07) found the record's "Creative Commons
   Namensnennung (CC-BY)" unresolvable to a version: DCAT-AP.de's
   unversioned `cc-by` concept maps to no version, opendefinition.org lists
   1.0 to 4.0, and Bremen's own portal records use `cc-by/4.0`, so the
   unversioned id was a choice. Every version permits public display and
   adapted maps, no share-alike, no non-commercial term. The gap: CC BY 4.0
   licenses the sui generis database right (§4) and 3.0 is silent on it, so
   under an older reading the survey's German database right (§87a UrhG) is
   neither licensed nor reserved. The owner's call 13 (2026-10-05, no
   outreach) was made without this point. **Recommendation: accept, on the
   4.0 reading** (opendefinition's overview is 4.0 and it names 4.0 the only
   version for data; the record types the licence "Freie Nutzung"; the map
   publishes aggregated density and a goods group per dot, never the
   database). Tradeoff: if the Kommunalverbund meant 3.0, an objection
   arrives as a removal request, honoured at once; the alternative, asking
   info@kommunalverbund.de, delays Bremen and reverses call 13's
   no-outreach. Stops: Bremen's landing only; the build proceeds on the
   branch.

### 2026-10-07 - Gimpo built: the Gimpo Goldline on SEMAS's register, its own page (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py gimpo`: PASS, 0
  of 13,398 rows show a Korean personal name at a residential address; 11
  withheld by step 2's Korean pass (9 of them inside a ring). SEMAS has no
  owner or phone column.
- **Gimpo built on SEMAS's register and the Gimpo Goldline, page 202.**
  Gimhae's pipeline (code-keyed register, one Overpass query) with Gimpo's
  config: 시군구코드 41570 picked 25,160 rows -> **13,398 storefronts**
  (Food service 6,112, Retail 5,512, Personal services 1,774), exactly the
  brief's screen; 11 personal names at a residential address withheld; out
  by name: hostess bars 139, staff canteens 44, household fuel dealers 10,
  dance halls 4. OSM boundary relation 2409165 (김포시), **295 km²**, gated
  285-305 (the brief's 277 is the land figure). The Goldline (ref
  `김포 골드라인`, light_rail, OSM's #957326, CIE76 62.9 from the nearest
  pin color) drawn to both ends: **9 stations in Gimpo**, 김포공항 (Seoul)
  in `excluded_stations.csv`. Gate 3 exact on the whole line, 10, against
  English Wikipedia's infobox (secondary, as Ansan and Uijeongbu). Median
  spacing 1,459 m (the brief 1,457), standard rings; the light-rail test
  passes (own underground track, every 6 minutes at midday per the brief's
  timetables, spacing above 550 m). **7,187 of 13,398 (53.6%) in a ring**
  (the brief's 53.4%). Not drawn, each with no station in Gimpo: Lines 3, 5,
  9 and Incheon Lines 1 and 2 (AREX and the Seohae Line are `route=train`
  and never queried). The tunnel share was not measured (the drawn geometry
  carries no tunnel tags); the light-rail test does not need it. Step 2
  measured 0.33 GB. Files: `pipeline/gimpo/`, `app/pages/202_Gimpo_Heatmap.py`,
  `app/cities.py`, notices 68 and 1, `docs/data_sources/south-korea.md`
  (three rows), `docs/excluded_categories.md`, `docs/privacy_verdicts.md`,
  `scripts/check_personal_exposure.py`.

### 2026-10-07 - Siheung built: Line 4, the Suin–Bundang and Seohae lines on SEMAS's register, its own page (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py siheung`: PASS,
  0 of 15,206 rows show a Korean personal name at a residential address; 11
  withheld by step 2's Korean pass (4 of them inside a ring).
- **Siheung built on SEMAS's register and Ansan's three lines, page 300.**
  Ansan's step 1 with Gimhae's one-query fetch (Ansan's train-ref clause
  added) and code-keyed register: 시군구코드 41390 picked 25,119 rows ->
  **15,206 storefronts** (7,273 / 5,763 / 2,170), exactly the brief's; 11
  withheld; out by name: hostess bars 287, staff canteens 230, household
  fuel dealers 35, dance halls 5. OSM boundary relation 2409181 (시흥시),
  **166 km²** with its tidal flats, gated 158-174. **9 stations**: Line 4 2,
  Suin–Bundang 4, Seohae 5, 오이도 and 정왕 shared; 114 stations of the
  three lines outside, listed. Gate 3 exact on the Suin–Bundang Line, 63
  (Ansan's source); Line 4 and the Seohae Line not gated whole, as Ansan.
  English names: all 9 resolved from a station object or `name:en`
  (시흥능곡 and 달월 included), no override needed. Median spacing 1,332 m,
  standard rings. **6,106 of 15,206 (40.2%) in a ring** (the brief's 41.2%
  on the probe's points). Line colors are Ansan's: Seohae 29.9 and Line 4
  33.6 below the preferred 45, recorded, as in Ansan. Not drawn: Lines 1, 2,
  7 and Incheon Lines 1 and 2, none with a station in Siheung. Step 2
  measured 0.31-0.41 GB.

### 2026-10-07 - Abroad batch: page proposals, numbers and downstream (abroad-batch)

- **Page sentences outside a template, proposed for review time.** Gimpo:
  "Not drawn: Lines 5 and 9, the Airport Railroad and the Seohae Line, which
  meet the Goldline at Gimpo International Airport in Seoul. None of them
  has a station in the city." (Gimhae's approved not-drawn bullet with
  Gimpo's lines.) Siheung: "Line 4 and the Suin–Bundang Line share Oido and
  Jeongwang, and the Seohae Line runs on its own track through the east of
  the city." (Ansan's shared-stations bullet, filled) and "The Suin–Bundang
  and Seohae lines run about every 15 minutes by day, less often than Line
  4." (Namyangju's approved wait bullet, filled; the brief's disclosure of
  the borderline lines.)
- **Page and notice numbers claimed for the batch:** pages 202 (Gimpo), 300
  (Siheung), 301 (Geneva), 302 (Thessaloniki), 303 (Gelsenkirchen), 304
  (Bremen); notices 154-156 (Geneva, Thessaloniki, Bremen). Staging recorded
  the claim on master the same day.
- **Downstream (`docs/session_roles.md`).** Gimpo and Siheung: notice 68
  (SEMAS) **caption** (the terms prescribe a source credit with no wording
  or place); notice 1, rail, boundary and station names from OpenStreetMap.
  **Open terms question: the SEMAS card hold** (whether SEMAS's permission
  reaches social posts), inherited, so both stay off cards and public pieces
  until the owner rules. New inputs: two cities, notice 68's and notice 1's
  city lists.
