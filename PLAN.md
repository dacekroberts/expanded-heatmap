# Plan

**City building is finished, and the project is in maintenance** (owner,
2026-10-16: no more cities for now). 237 cities are built in 27 countries, all
with place search. What is left: dated re-checks of the built maps, data
refreshes, small known faults, and calls that wait on the owner.

Open work only. Completed work and its reasoning are in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md). The plan as it stood
before this rewrite is kept verbatim in
[`docs/plan_done/2026-10-16.md`](docs/plan_done/2026-10-16.md); earlier done
items are in [`docs/plan_done/`](docs/plan_done/). An item's detail is in
[`docs/plan_detail/`](docs/plan_detail/), under the heading its line names.

Rules that still apply: commit after every green step; log every judgment call
in `DECISIONS.md`; run `python pipeline/drift_check.py <city>` after any
pipeline change.

Detail files: [japan](docs/plan_detail/japan.md),
[labels and macro map](docs/plan_detail/labels_and_macro_map.md),
[city watch](docs/plan_detail/city_watch.md),
[data and disclosure](docs/plan_detail/data_and_disclosure.md),
[process and tooling](docs/plan_detail/process_and_tooling.md).

---

## Due now

**Parked until the owner returns on 2026-11-05** (owner, 2026-10-17): the
items below, Yamagata included, and the dated re-checks due
before then (Milan, Prague, Toronto, Birmingham) wait until then. A
re-check that comes late finds the same change.

- [ ] **Philadelphia's date re-read** (due about 2026-10-13). data_and_disclosure,
  "Published-city date fixes", item (d).
- [ ] **Yamagata: rebuild on the October edition** (the list to 2026-10-31,
  due on the city's page about 2026-11-10). The September edition was tried
  and kept off: it dropped about 75 restaurant permits that expired
  2026-09-30 before their renewals reached it (DECISIONS.md, 2026-10-17,
  "Yamagata stays on the August list"). Before rebuilding, check that the
  edition carries those renewals. city_watch, "Yamagata: the September
  food list".
- [ ] **São Paulo's Linha 6-Laranja** stays out until full service, and
  Linha 17 per `docs/recheck_calendar.md`.
- [ ] **The weekly `archive_decisions.py` run** (each Sunday, from
  2026-10-18). process_and_tooling, "Efficiency review follow-ups".

## Dated re-checks

The full calendar is [`docs/recheck_calendar.md`](docs/recheck_calendar.md).

| From | City | What | Detail |
|---|---|---|---|
| 2026-10-19 | Milan | Tram timetables (lane 5) | city_watch, "Trams left off built maps" |
| after 2026-10-26 | Prague | Tram timetables (lane 5) | city_watch, "Trams left off built maps" |
| after 2026-10-31 | Toronto | Tram timetables (lane 5) | city_watch, "Trams left off built maps" |
| about 2026-11-01 | Birmingham | Metro Line 2; the Eastside stops when open | city_watch, "The UK six's watch items" |
| after 2026-11-23 | Rome | Trams 2, 3, 5, 14 and 19 (owner's call) | city_watch, "Trams left off built maps" |
| before 2026-12-12 | Berlin | Refetch before VBB's calendar ends; U6 to Alt-Tegel about 2027-08 | city_watch, "Berlin" |
| after 2026-12-12 | Zurich | Rebuild (temporary trams 50 and 51) | city_watch, "Zurich" |
| end of 2026 | Florence, Salvador | Florence T3; Salvador's VLT in revenue service | city_watch, "Wave-2 follow-ups", "Watch items from group 1" |
| 2026-12-26 (target) | Seoul | The Wirye Line | city_watch, "Trams left off built maps" |
| about 2027-02 | Oslo, Prague | Tram 13 back; Flora reopens (remove the override) | city_watch, "Left by the 2026-10-03 lanes batch", "Prague: Flora reopens" |
| 2027-08-30 | Philadelphia | 11th St back (SEPTA) | city_watch, "Philadelphia: 11th St" |
| about 2027-10 | all | The global re-probe | `docs/city_master_list.md`, "What would reopen it" |

## Data refreshes, no date

- [ ] **London:** refetch place-index tile 2 from `overpass-api.de` (it is May
  data from another mirror), and the FSA extracts before they age. city_watch,
  "London".
- [ ] **Buenos Aires:** SBASE refetch. city_watch, "Buenos Aires".
- [ ] **Kyoto:** add the August 2026 list. japan, "Kyoto's August 2026 list".
- [ ] **Six Japanese cities onto N02-25** (Tokyo, Kobe, Sapporo, Fukuoka,
  Kyoto, Yokohama), one drift check each. japan, "Japanese cities onto N02-25".
- [ ] **Osaka's Umekita to 福島 stretch** is still not drawn. japan, "Osaka's
  Umekita stretch".
- [ ] **Sacramento, once OSM catches up:** list 7th & Railyards (Green, not
  drawn at 30 minutes) and retire `ADDED_STATIONS` for Dos Rios. city_watch,
  "Sacramento's Green Line".
- [ ] **Toulouse and Rennes:** did step 1's name-level fallback fire? One
  read-only step 1 run each. city_watch, "Toulouse and Rennes".

## Known faults and small fixes

Recorded, not urgent; each is small unless it says otherwise.

- [ ] **Search ranking on phones:** where more than four stations share a name,
  a phone's list shows only four of them (New York's six "86 St", "Canal St",
  "Fulton St"); Toronto's "Bathurst" stop is joined to its pin, but typing
  the name does not show that pin. From `scripts/check_map_search.js`
  (2026-10-16: 237 maps, 13,010 stations and 1,275 lines all found; these six
  warnings only).
- [ ] **Names holding a private-use character:** 1,797 names in 29 cities show
  their category instead; restore the character where one publisher uses one
  code point for one known character (larger). Plan line kept in
  `docs/plan_done/2026-10-16.md`, "A repair pass".
- [ ] **A site-wide junk-name check on business dots** in `check_all`
  (U+FFFD, CJK Extension A in `_LETTER`, non-NANP phone formats).
- [ ] **Seattle (Regional)'s Global View button** does nothing on the owner's
  iPhone; not reproduced at 375 px.
- [ ] **Bucharest's address and name functions** to a shared module
  (Cluj-Napoca's step 2 imports them).
- [ ] **Japanese shared-code fixes** (`in_city_first` copies in ten
  `step3_map.py` files) and confirmation of notices 157, 161, 178, 184 and
  186. japan, "Kept from the drafts' notes at the 2026-10-08 fold".
- [ ] **Stockholm's torghandel stall** (`pending` in
  `scripts/category_continuity_table.py`). data_and_disclosure, "The category
  fix batch".
- [ ] **Three code problems from the comment pass.** process_and_tooling,
  "Three code problems from the comment pass".
- [ ] **Date fixes (e) and (f):** expiry leaks, the newest-row date.
  data_and_disclosure, "Published-city date fixes".
- [ ] **Page and label leftovers:** the prose pass's deploy-check items
  (Pittsburgh, Yokohama and Osaka labels; San Diego's page; Toronto's run
  date); What Is Excluded's opening claims; licence gaps; UK line colours,
  day-first notices, "45 from every pin", caterers' counter forms; the legend
  model; Vancouver (Regional) clipped at 375 px; the Overview's colour
  contrast, never measured. data_and_disclosure and labels_and_macro_map,
  under those names; process_and_tooling, "Next landing follow-ups".
- [ ] **Transit-layer gaps found by the transit-layer retrospective (2026-10-16):** no
  script enforces the CIE76 20 pin floor (`check_line_colours()` raises only
  below 10); rail shape and labels have no check in the gate;
  `docs/sub_transit_line_filters.md` lists 8 thinning cities where 13 pages
  thin; `docs/commuter_rail_list.md` says six cities draw commuter rail and
  bolds seven. Each to be confirmed before it is fixed.
- [ ] **Heavy-job gate follow-ups:** Japanese drift memory, orphaned children
  in the ledger. process_and_tooling, "Heavy-job gate follow-ups".

## Waiting on the owner

- [ ] **Outside actions:** upload `visuals/repo/social-preview.png` (GitHub,
  Settings, Social preview) and paste the About text; disable the Max
  account's `place-search-post-landing` task (may fire 2026-10-18 12:05);
  Philadelphia's permission request, no response as of 2026-10-17 (silence is not
  consent; `docs/gated_access.md` item 12).
- [ ] **Deferred under the feature freeze:** the phone legend fold by operator,
  the map's height on phones, a reset-view button, search tuning by feel, a
  per-city sights list for search.
- [ ] **Public pieces:** the cross-city chart, home-page copy, and the
  tone-guide prose pass (about 2026-11-07).
- [ ] **Reviews offered, none started:** a site-wide code audit; the map-only
  navigation go/no-go; six cross-city discrepancy audits; per-city
  restriction disclosures and wait times as data; the per-city comment
  rewording, phase 2.
- [ ] **Tokyo's missing wards** (built with 8 of 23); the Chiyoda ledger and
  four requests are parked as the last resort. japan, "Tokyo: the missing
  wards".

## Ideas, not planned

- Ridership (out of scope; revisit only if asked).
- An English-language switch for station names; better placed in the Travel
  view or transit-globe (owner, 2026-10-12).
- `drift_check.py` saying plainly when a key-gated city's raw input is missing
  (Washington D.C.).
- Miami's all-businesses toggle scoped to the station municipalities.
- A smoke check that re-fetches every recorded endpoint and asserts a plausible
  content type.
