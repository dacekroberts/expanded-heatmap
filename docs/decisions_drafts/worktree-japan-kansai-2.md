# Decisions drafts: worktree-japan-kansai-2 (Kansai-2, phase 2 of the A/B build plan)

Entries in the `decisions-entry` format, newest first, each as it should land.
Cleanup folds this file into `DECISIONS.md` when the owner hands it off.

## Parked calls

Named by city and letter; Staging assigns the S numbers when it relays them.

- **Osaka A: the Osaka Metro lines' names on Osaka's map (Cleanup's).** The
  line registry now holds "Osaka Metro Tanimachi Line", "Osaka Metro
  Imazatosuji Line" and "Osaka Metro Nagahori Tsurumi-ryokuchi Line", the
  operator's full name as the wave 2 rule asks, and Moriguchi's, Kadoma's and
  Yao's maps draw them so. Osaka's own map still labels them "Tanimachi
  Line", "Imazatosuji Line" and "Nagahori Tsurumi-ryokuchi Line" (and "Chuo"
  is already "Osaka Metro Chuo Line" there). *Recommend renaming Osaka's
  three at the held WAVE5 re-render*, with Sakai's "Midōsuji Line" (a macron
  in a line name). Tradeoff: until then one line reads under two names on
  neighbouring maps; renaming now would re-render a built map outside a
  review time. The colours are unchanged: Osaka's config reads the same
  values from the registry.
- **Batch B: three page sentences no template covers (proposals, flagged for
  review time).** (1) Ibaraki, Minoh, Moriguchi, Kadoma: "Osaka Prefecture,
  which licenses <City>'s premises, publishes no list of laundries, so they
  are not on this map." and "Restaurants, cafés and shops are not on this map
  either: neither the prefecture nor the city publishes a list of
  food-business permits for <City>." (2) Yao, Takatsuki: "<City> City
  publishes no list of barbers, beauty salons or laundries, so personal
  services are not on this map." and "The map shows about 55% [57%] of the
  restaurant permits in force in <City> by the national count for March
  2025." (owner call 125 asks for the share; no built MHLW-only page words
  it). (3) Kadoma: "Five premises are not on the map: their addresses are
  written by land-lot number in districts where MLIT's data has no such
  numbers." *Recommend approving all three as written*; each follows Kochi's,
  Kurume's and Uji's approved sentences as closely as the facts allow.
- **Batch C: macro label widths for three names.** `label_competition.TEXT_WIDTH`
  holds measured widths for Ibaraki, Minoh, Moriguchi, Kadoma and Neyagawa
  (staged 2026-10-04) but not "Ibaraki (Osaka)" (the page's name, call 168),
  "Yao" or "Takatsuki". See the entry below for what this session measured.

## Entries

### 2026-10-11 - Kansai-2: seven Japanese cities built (Ibaraki (Osaka), Minoh, Moriguchi, Kadoma, Neyagawa, Yao, Takatsuki; pages 251-257; notices 198-204)

- **All seven on the shared Japanese steps and the foundation's rules** (no `"rules"` key; no shared-code rule was missing). Steps 1-3 each, committed city by city on `worktree-japan-kansai-2`, nothing pushed. Region "Osaka Prefecture" (the retag has landed; the briefs' "Japan West" predates it), `mode: metro`, `label_tier: "minor"`, the scaffold's label offset (region views and offsets are Cleanup's, call 198).
- **Ibaraki (Osaka), Minoh, Moriguchi, Kadoma: Osaka Prefecture's barber and beauty lists, cut BY ADDRESS** (Itami's shape; a row that begins 茨木市 / 箕面市 / 守口市 / 門真市; any other mid-address mention stops the build). Each kind's full list of 2026-03-31 plus the five monthly new-premises files to 2026-08; `as_of` pinned to 2026-08-31, an upper bound (Kochi's call). The twelve files were copied unchanged from `data/osaka_pref/raw/` into each city's raw folder (Itami's and Kakogawa's precedent with Hyogo's files); no BODIK data file was fetched.
  - Ibaraki: 142 + 484 rows, **621 storefronts**, block 99.8%, 0 unplaced, 10 stations on 4 lines (the brief exactly).
  - Minoh: 52 + 245 rows, **294 storefronts**, block 100%, 5 stations on 2 lines (the brief exactly).
  - Moriguchi: 112 + 263 rows, **375 storefronts** (counted first: above the floor at Minoh's page, calls 115 and 166), block 99.7%, 6 stations on 3 lines.
  - Kadoma: 93 + 246 rows, **334 storefronts**, block 95.9%, 9 at the town-chōme center, **5 unplaced** (the brief measured 10 before the foundation's join rules; brief corrected by this entry), 5 stations on 2 lines.
- **Neyagawa: the city's three BODIK lists of 2026-08-31** (Step 0's files, as cached): 155 + 419 + 64 rows, **630 storefronts** (the brief exactly), block 99.7%, 0 unplaced, 4 stations on 2 lines. Both operator columns are in the shared `OPERATOR_COLS` since the foundation and 営業種別 in `TYPE_COLS_AFTER5`, so the brief's two shared-code items needed nothing.
- **Yao and Takatsuki: MHLW's file alone, food only** (Kurume's shape, call 137), `TERM_AS_OF` 2026-08-31, `ADDRESS_BY_CONSENT` and `OWN_POINT_FALLBACK` (call 127c).
  - Yao: 2,185 storefront rows, **1,956 storefronts** (Food service 1,204, Retail 752), block 96.8%, MHLW's point for 71, 0 unplaced; 1,265 filings without an address; census control 1.32 (the brief's figure, with its reason: 87% of permits, a quarter of fixed addresses withheld). 11 stations on 5 lines.
  - Takatsuki: 2,152 storefront rows, **1,922 storefronts** (Food service 1,116, Retail 806), block 98.2%, MHLW's point for 38, 0 unplaced; 1,328 filings without an address; 3 rows set aside as area-wide (the foundation's 全域 rule, the brief's proposal already in shared code) and the 小字 rule placed what the brief left unplaced; census control 1.16 (the brief's figure: 89% of permits, a fifth of fixed addresses withheld, 216 deli counters in Retail). 5 stations on 2 lines.
  - The census control was not run for the five personal-services pages: `japan_census_control.py` compares 飲食店 establishments, and those maps hold none.
- **Rail calls applied from the briefs (precedent decides):** Moriguchi's Imazatosuji Line drawn cut at 太子橋今市 and the Monorail left out at 大日 (call 116); Kadoma's Nagahori Tsurumi-ryokuchi Line drawn cut at 門真南 and the Monorail left out at 門真市 (call 167); Neyagawa's 寝屋川公園 kept as cut (the band row); Yao's Tanimachi Line drawn cut at 八尾南 (calls 54 and 92), the Osaka Higashi Line's 久宝寺 as cut, the Nishi-Shigi Cable left out (Kobe's rule).
- **Judgment calls made at the build, each on a precedent:**
  - **Moriguchi's 太子橋今市 is one N02 station group of both subway lines** (150 m): the Imazatosuji platform is inside the city, the Tanimachi platform 30 m outside. The shared collapse keeps one station carrying both lines, so the Tanimachi Line counts 3 by group where the brief counted 2 by platform (trap 1, collapse on `N02_005g`). Gate 3 is set to 3 with the reason in the config. The Imazatosuji Line stays drawn, as call 116 says.
  - **Moriguchi's gate-1 floor lowered to 300 m** (`SPACING_MIN_M`): six real stations on 12.7 km², collapsed median 371 m (太子橋今市-土居 355 m, 守口-守口市 361 m, 土居-滝井 371 m), each pair two stations under two names. Toyama's and Tbilisi's precedent for a measured, cited floor. Halved rings by the spacing rule (median under 550 m).
  - **守口 (Tanimachi) and 守口市 (Keihan) kept apart** (the brief's open call 2, its recommendation): N02 keeps them apart under different names (trap 1; Tsu's precedent).
  - **Food left off the five personal-services pages** (each brief's open call, its recommendation; the band rows already say barbers and beauty only): MHLW's prefecture file holds 23 to 33 addressed restaurants per city.
  - **Kadoma's `OSM_BBOX` widened** from the brief's (34.71-34.75 N) to 34.70-34.76 N: step 1 stopped because the N03 extent left the brief's box (trap 12); OSM names re-fetched.
  - **Takatsuki's rings are standard**: step 1's median is 574 m, above the rule's 550 m.
- **Line identity (the owner's hard line):** every shared line reads its colour from `pipeline/line_registry.py`. Four lines entered the registry in the colours a built map already drew, and that map's config now reads the same value from it (no output changes): the Osaka Monorail Saito Line (Suita's `#708898`), Osaka Metro's Tanimachi (`#933CA5`), Imazatosuji (`#E77512`) and Nagahori Tsurumi-ryokuchi (`#7CA014`) lines (Osaka's). Two lines are new to the site, each with its own colour: the Hankyu Minoh Line `#905840` (pins 47.7; 20.1 from the Hankyu Takarazuka Line's `#B7572D`, which it meets at 石橋阪大前 on Toyonaka's map: `line_colour_search.py minoh` alone returned the Takarazuka Line's own colour, since it reads one map) and the Kintetsu Shigi Line `#A04818` (pins 48.1, other lines 32.0 or more). `check_line_identity.py`: PROBLEMS 0.
- **Station names, Hiroshima's style:** Ibaraki 2 overrides (阪大病院前 as Handai-byoin-mae, 彩都西 as Saito-nishi) and one tie (南茨木 as Minami-Ibaraki); Minoh 1 (箕面船場阪大前 as Minoh-semba-handai-mae); Kadoma 1 (門真南 as Kadoma-minami); Yao 2 (久宝寺口 without macrons, 八尾南 as Yao-minami). Keihan's 守口市, 門真市 and 寝屋川市 stay as OSM and Keihan write them (Moriguchishi, Kadomashi, Neyagawashi; Hirakata's 枚方市 precedent), Hankyu's with a hyphen (Ibaraki-shi, Takatsuki-shi).
- **Privacy: `check_personal_exposure.py` prints 0 for each (Japan pass).** Verdict for all seven: **publish**. Ibaraki 2 pins show their register type (2 operator matches in the raw rows); Minoh 0 (0); Moriguchi 1 (1); Kadoma 0 (0); Neyagawa 0 (0: the one laundry trade name equal to an operator column is a cooperative's, in 法人営業者名称, which the `coop` rule reads as no person; counted in memory, yes or no only); Yao 0 pins (2 matches in the raw rows, neither a storefront); Takatsuki 0 pins (1 match, not a storefront). Operator columns (開設者; Neyagawa's 営業者名称（法人の場合は代表者氏名） and 法人営業者名称; MHLW's 法人名) are read in memory only; phones, 法人番号, 法人住所 and operators' addresses are never selected.
- **Licences:** Osaka Prefecture's lists and Neyagawa's were read by Staging's licence-read agents on 2026-10-07 (DECISIONS, "Licence reads for the Japan builds"): both PERMITTED WITH CONDITIONS, CC BY 4.0. Rows written to `docs/data_sources/japan.md`; MHLW's PDL 1.0 as recorded.
- **Downstream (Visuals, Analytics):** seven new cities; `app/cities.py`, `app/components.py` (notices 198-204), `app/osm_notice.py`, the macro facts and ring shares change. Rail for all seven is MLIT N02; **station names in English are from OpenStreetMap** on all seven. Per notice, where it must appear: the licences prescribe no placement on the work's face (CC BY 4.0 "reasonable manner"; PDL 1.0 a 出典 line), so **caption only** for 198-204, as Kansai-1's. **No open terms question** on any of the seven.
- **Slips, stated:** (1) `brief_check.py minoh` was run twice back to back, so two BODIK metadata calls landed within a few seconds of each other, inside one city but under the 20 s spacing; every other BODIK call this session was a single package_search per city, minutes apart. No block followed. (2) A scratch helper cut too much of Moriguchi's cloned config (it matched `LEFT_OUT_LINES = {` for `LINES = {`); caught at import, the config rebuilt, nothing committed from the broken state.
- **Not this session's, left as found:** `fingerprint.py coverage` (the owner's key marks no new map), `check_macro_labels.py` for cities labelled in no view (Cleanup's, call 198), and `check_provenance.py`'s master-list count (Staging's).
