# DECISIONS drafts - Regional-1 (`worktree-japan-regional-1`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

The batch (the A/B build plan, 2026-10-07): Maebashi, Fukuyama, Ichinomiya,
Tsu, Fukushima, Iwaki, Akita, Ōita, Gifu, Mito, Morioka; pages 229-239,
notices 176-186.

## Parked calls

1. **Tsu (page 232, notice 179 held): Mie Prefecture's three BODIK lists
   (`240001_food_business_all`, `240001_barbar`, `240001_hair_dressing`) have
   no licence verdict.** The brief records CC BY 4.0 as stated and leaves the
   read to a `licence-read` agent; no read is recorded in staging's drafts,
   `docs/data_sources/japan.md` or `DECISIONS.md` (the wave-5 entry's eleven
   reads do not include Mie). *Recommend:* one licence read of the
   三重県オープンデータ利用規約 (`https://odcs.bodik.jp/240001/tos/`), one read
   for all three lists, by a session cleared to call BODIK's hosts; then
   build. What the brief quotes points to permitted with conditions (CC BY
   4.0, a resource's own licence prevailing, no logo, a fault-based cost
   clause, accepted for Japan 2026-09-24). *Tradeoff:* one read and a later
   build, against a page and notice whose credit and conditions are
   unverified. The scaffold stands as committed (efeaf016); nothing else was
   written. The brief's open call 1 (MHLW's notifications as a partial Food
   shops layer) needs no call: Iwaki's call 150 left 164 addressed retail
   rows out as too thin, and Tsu's are 159 (156 pins), so they stay out and
   MHLW's file stays the control.
   **Resolved 2026-10-07, the same day:** Staging's licence read found Mie's
   lists PERMITTED WITH CONDITIONS (CC BY 4.0 by 第１条; master's staging
   drafts, "Licence reads for the Japan builds"). Tsu is built after it.
2. **Fukushima (page 233, notice 180; built, not blocked): the registers'
   2026 monthly files** (`r0808riyou.csv`, `r0804biyou.csv` to
   `r0807biyou.csv`, 360-709 B each; the same page, publisher and terms;
   none for laundries; the brief's open call 3, staging's call 153). They
   are not approved and were not fetched, so the registers stand at
   2026-03-31 (`SOURCE_AS_OF`) while the food leg reaches 2026-08-31.
   *Recommend* approving them (Ichinomiya's call 128), then rebuilding the
   barber and beauty lists to 2026-08-31 in `config.source_rows`.
   *Tradeoff:* a handful of salons, a re-render and one more approval,
   against registers five months older than the food leg (stated on the
   page and in data_age).

## Proposals for review time (page sentences no template covers)

- **Maebashi** (page 229): "Barbers, beauty salons and laundries come from
  the city's registers, brought up to August 31, 2026 from its March list and
  its monthly lists of openings and closings." and "The laundry register
  lists 139 laundries, against 170 in the national count a year earlier. The
  city notes that some premises are left off at their operators' request."
  (the owner's call 14: build and state the share, citing the dataset's
  note as a stated cause, never the whole of the gap). The same two
  sentences in its What Is Excluded section, and "No Shinkansen station lies
  in the city." there. The notice (176) adds Hamamatsu's form for two lists
  and the sentence "No list is claimed to be complete or current; the
  ministry's holds only filings whose applicants agreed to publish them."
  (第３条).
- **Fukushima** (page 233): "From Fukushima City's list of food-business
  permits (as of March 31, 2026), with the new permits it listed each month
  to August 31, 2026, and its registers of barbers, beauty salons, laundries
  and coin laundries (as of March 31, 2026)." (the template's sentence with
  the months and Sapporo's coin laundries added), and "The JR Ou Line is
  infrequent inside the city: about 11 trains a day each way stop at
  Sasakino and Niwasaka." (call 86 asks for the stretch to be named; no
  approved form yet). In its What Is Excluded section: the Counted
  paragraph's month and upper-bound sentences (from Higashiōsaka's) and "The
  JR Ou Line runs about 11 trains a day each way inside the city; it is
  drawn (owner, 2026-10-06)." The notice (180) adds 新規食品営業許可施設一覧,
  the monthly files' own title, to the brief's five titles, and the
  processing sentence "this project added the new permits to the list".
  Also for review time (open call 4, precedent applied): of the 230 caterers
  left out, 161 also name a counter form (一般食堂 仕出し屋 …); a sentence
  saying so is not on the page.
- **Fukuyama** (page 230): "From Fukuyama City's list of food-business
  permits, brought up to August 31, 2026 from its March list and its monthly
  lists of new and renewed permits, and its registers of barbers, beauty
  salons and laundries (as of August 31, 2026)." (the template's first
  business bullet with Maebashi's proposed rebuild wording) and "Permits
  granted since June 2021 that the ministry's list no longer holds are left
  out as closed, and a few permits the ministry's list holds and the city's
  monthly lists do not are added." (calls 5c and 6). In its What Is Excluded
  section, the rebuild and the waiting-renewal wording under **Counted**, the
  145 permits left out as closed, and "The registers list 396 barbers, 1,238
  beauty salons and 173 laundries, against 405, 1,209 and 200 in the national
  count a year earlier." The notice (177) adds "rebuilt the city's food list
  to 31 August 2026 from its March list and its monthly new and renewed
  permits, left out permits granted since June 2021 that the ministry's list
  no longer holds" to Maebashi's processed-by sentence.

## Shared-code findings for review time (not changed here)

- **`japan_register.rebuilt_register` ranks on the latest expiry alone**
  (Fukuyama): a renewal that starts after the as-of then hides the permit in
  force, and step 2's call-172 rule drops the premises (17 in Fukuyama, fixed
  city-locally in `config.rebuilt_food` by ranking only permits started by
  the as-of). Any city with renewal months is exposed; Higashiōsaka, built
  on it, is worth re-measuring. It also keeps only the first non-empty
  `FORM_COLS` value, so under `form_all` a 形態 beside a filled 業態 is lost
  (harmless in Fukuyama).
- **`japan_step2.own_coordinates_check`** prints and emits a chōme-tier
  median of 741,990 m on Fukuyama: 10 rows whose MHLW point lies in
  Fukushima or Tokyo, refused by `CITY_BBOX` and never used. Cosmetic, but
  the figure is in the baseline.
- **A full list kept whole plus new-permit months** cannot be one
  `rebuilt_register` source under calls 161 and 172 (one `TERM_AS_OF` per
  source): two sources of one `SOURCE_KIND` is the shape (Fukushima,
  Ichinomiya, Iwaki). A line for the japan-city skill.
- **`city_rows` trusts the file extension**: Ichinomiya's July beauty file is
  an XLSX named .csv, read city-locally by its magic bytes. Checking the
  bytes first in shared code would cover the next city.

## Entries

### 2026-10-07 - Fukuyama built, the food list rebuilt to August 2026 and checked for closures against MHLW's live file

- **Fukuyama built (page 230, notice 177), Higashiōsaka's rebuilt food
  register plus Matsuyama's MHLW beside a complete city list: 6,365
  storefronts (Food service 2,926, Food shops 1,665, Personal services 1,774)
  around 18 stations on 3 lines, 43.1% of them in a ring (2,745).** On the
  Japan foundation's rules (no `"rules"` key). Sources: the city's CKAN food
  list of 2026-03-31 (5,880 rows) and its five monthly files since (434
  filled rows), rebuilt to 2026-08-31; the seven earlier months read for
  their permit numbers only; MHLW's file (8,573 rows); the barber/beauty
  (1,634) and laundry (173) registers as of 2026-08-31. Built by a subagent
  of the Regional-1 lead, integrated by the lead.
- **The rebuild reproduces the brief exactly**: 6,314 rows read, 5,942 after
  de-duplication, **5,738 in term, 4,238 restaurants**. It is city-local
  (`config.rebuilt_food`), because `japan_register.rebuilt_register` returns
  no permit number (the closure filter and MHLW's point key on it) and keeps
  only the first form column (業態 before 形態); a check stops the build if
  its in-term set ever differs from the shared function's.
- **A renewal that starts after the as-of waits; the permit it replaces
  stands** (call 172, applied to the rebuild). Ranked on the latest expiry
  alone, 19 renewals in the August file that start on 2026-09-01 won their
  premises, and step 2's call-172 rule then dropped them, so 17 premises
  whose permit ran to 2026-08-31 left the map. The rebuild now ranks only
  permits started by 2026-08-31: in force 5,736 (4,237 restaurants), 17 with
  a waiting renewal; the 2 with no earlier permit wait. No direct precedent:
  for review time.
- **The closure filter (owner, 2026-10-05, call 6)**: 151 new-law permits
  MHLW no longer holds, the brief exactly (115 restaurants). Read at build: 7
  premises had been renewed in MHLW's file alone under a new number starting
  2026-09-01, so the filter would have dropped an open premises whose renewal
  call 172 then makes wait. A permit MHLW renewed for the same premises and
  type under a number no city file lists is therefore not a closure (6 after
  the rebuild; precedent: the waiting renewal above). **145 left out as
  closed (109 restaurants); the register keeps 4,128 restaurants, 96.0% of
  e-Stat's 4,302** (the brief 4,123, 95.8%). For review time.
- **MHLW beside the city's list (owner, 2026-10-05, call 5)**: its 3,282
  notifications (1,854 addressed) and 7 closed ones, and its 44 open permits
  in no city file (34 restaurants; 10 start 2026-09-01 and wait, 15 are
  institutional kitchens) through `config.mhlw_rows`: 836 Food shops pins and
  6 Food service pins. Its point by permit number rides on 3,468 rebuilt
  city rows (`OWN_POINT_FALLBACK` = food and MHLW; call 5a says "by permit
  number", so not Matsuyama's `POINT_DONORS` name match). `SUPERSEDES` drops
  395 city rows for an MHLW row at the same premises and bucket (mostly
  supermarkets and konbini holding a city permit and filing a notification).
- **Step 2:** 7,269 storefront rows; on the map 90.3% block (5,746), 4.8%
  MHLW's point (303), 5.0% town-chōme or 大字 centre (316); 27 unplaced
  (0.4%), most in 水呑町三新田 (MLIT's files lack it). MHLW's point against the
  block point: median 39 m, 95.6% within 250 m (3,559 rows; the brief 38 m /
  96.2%). Set aside: 178 area-wide addresses (広島県内 vehicles), 1 in another
  municipality. Not a premises 102; no address published 1,429 (MHLW; no
  restaurant); closed 7; starting after the as-of 10 (MHLW). Out by rule
  1,735: 540 manufacturing and other non-counter types, 421 canteens, 274
  snack bars and cabarets, 216 vending, 123 karaoke and amusement venues, 74
  temporary or mobile, 53 inside accommodation, 26 caterers, 8 mail order.
  482 repeat permits shown once.
- **Registers**: barbers 396, beauty 1,238 (one file split by 種類),
  laundries 173 (3 empty rows dropped as no premises); shares of e-Stat
  FY2024 97.8%, 102.4%, 86.5%. No laundry sentence on the page beyond the
  counts in What Is Excluded: the dataset gives no cause (Maebashi's was the
  owner's call 14 for its own note).
- The 菓子 / そうざい factory share: 52 of 601 (8.7%), kept (owner,
  2026-09-24).
- **Rail**: N02-25, the brief's stub test reproduced (Sanyo 5 of 131, Fukuen
  12 of 27, Ibara 3 of 15), 18 stations (福山 and 神辺 shared), median gap
  1,479 m: standard rings. 7 excluded (Fuchu 4, Ibara 2, Onomichi 1). OSM
  `name:en` for all 18 (27 objects; one query under the session's Overpass
  lock, overpass-api.de 504, kumi answered); 1 override (備後本庄
  Bingo-Honjo, OSM's macron). No gate 3: no line wholly inside (Fukui's
  form). No frequency floor (calls 46 and 86); JR at least hourly. Colours
  from `line_colour_search.py` (Sanyo teal, Fukuen red-orange, Ibara green;
  closest pair 92.7).
- **Economic Census control:** 2,926 Food service pins against 1,737 飲食店
  establishments in 34207: 1.68 per establishment, the brief's estimate,
  inside the built cities' 1.56-1.92.
- **Privacy verdict: publish.** `check_personal_exposure.py fukuyama`: the
  Japan pass prints 0; 35 trade names in the raw files are an operator's own
  name, 6 pins show their permit type.

### 2026-10-07 - Fukushima built, the full food list kept whole with five months of new permits, all three buckets from the city's own lists

- **Fukushima built (page 233, notice 180): 3,335 storefronts (Food service
  1,653, Food shops 621, Personal services 1,061) around 22 stations on 4
  lines, 60.4% of them in a ring (2,013).** Fukuyama's shape (a city's full
  food list plus the months since) with Ichinomiya's answered merge. All
  three buckets come from the city's own CSVs on its 食品営業許可施設、
  生活衛生関係施設一覧 page (CC BY 2.1 JP by the 福島市オープンデータ利用規約;
  the uncapped ４ accepted, call 110). No `"rules"` key (`ALL_RULES`).
  `brief_check.py` 18/18 (2026-10-07). Built by a subagent of the
  Regional-1 lead, integrated by the lead.
- **The merge (the brief's open call 1), by precedent: Ichinomiya's call 125
  and Iwaki's 149.** The list of permits in term on 2026-03-31 is kept whole,
  and the five monthly lists of new permits (April to August) are added.
  They are read as two sources, `food` and `food_new` (`SOURCE_KIND`), each
  through `rebuilt_register`, and each permit's term is read against its own
  file's date (`TERM_AS_OF` 2026-03-31 and 2026-08-31). One source rebuilt
  from all six files has only one as-of: 2026-03-31 would hold back the 89
  new permits as late starters (call 172), and 2026-08-31 would drop the 98
  permits expiring in May and July (call 161), which the months never
  republish.
- **The brief's figures reproduce:** one rebuild of all six files gives
  3,769 rows, 2,883 restaurant permits (101.3% of e-Stat's 2,846), Food
  service 1,658 and Retail 772. The two sources give 3,776 rows (3,689 +
  87); the 7 extra rows are new permits at a premises already in the full
  list (4 Food service, 1 Retail, 2 snack bars), and one pin per premises
  folds them. Permits past their term 0; starting after the as-of 0. City
  config only; the foundation's checklist names Fukushima's kind per file
  as city-local.
- **MHLW's file stays a control** (open call 2, staging's call 152), by
  Iwaki's call 150 and Tsu's precedent: a thin notifications layer stays
  out. Its 44 permits are all in the city's files, and it has 144 fixed
  Retail notifications. Not in `SOURCE_FILES`, not on the notice; a
  "(control)" row in `docs/data_sources/japan.md`.
- **Caterers (open call 4):** the shared `FORM_RULES` as written
  (`docs/category_rules.md`; Sasebo's and Kanazawa's 仕出し precedent). 230
  restaurant permits go out as 仕出し, 161 of them also naming a counter
  form.
- **The registers' monthly files** (open call 3, staging's 153) were not
  fetched; the registers stand at 2026-03-31 (parked call 2, not blocking).
- **Step 2:** 4,869 rows read (food 3,689, months 87, barbers 278, beauty
  638, laundries 125, coin laundries 52). Not a premises 162 (145 food
  permits with no address, the festival stalls among them, and 17 storeless
  laundry pick-ups). Out by rule 1,196: 277 snack bars and cabarets, 230
  caterers, 229 manufacturing and other non-counter types, 186 vehicles
  (種目 自動車による営業, four spellings), 161 canteens, 106 inside
  accommodation, 7 vending. Join, 3,511 storefront rows: block 3,176,
  town-chōme 150, 小字 centroid 178 (the foundation's `koaza_centroid`),
  unplaced 7 (0.2%; the brief's 40 came before the foundation's 字 rules).
  One pin per premises: 169 repeat rows. On the map: 90.9% block, 4.3%
  town-chōme, 4.9% 小字. Registers against e-Stat FY2024: barbers 278 of
  282, beauty salons 638 of 630, laundries 108 of 117, as the brief says.
- **The 菓子 / そうざい factory share:** 18 of 553 (3.3%), kept (owner,
  2026-09-24).
- **Economic Census control:** 1,653 Food service pins against 1,030 飲食店
  establishments in 07201 (2021, table 9-1A, industry 76): 1.60 per
  establishment, inside the built cities' 1.56-1.92. The brief's 1,226
  establishments and its 1.35 estimate do not reproduce from
  `japan_census_control.py`.
- **Privacy verdict: publish.** `check_personal_exposure.py fukushima`: the
  Japan pass prints 0; 4 trade names in the raw files are an operator's own
  name, 2 pins show their permit type. 営業者氏名 / 営業者氏名漢字 and 開設者氏名
  are read in memory only; the operators' own addresses and phones are never
  selected.
- **Rail:** N02-25, 22 stations: the Iizaka Line 12 of 12, the Abukuma
  Express 5 of 24, JR Tohoku 5 of 155, JR Ou 3 of 105 (福島 one group on all
  four, spread 36 m). The Tohoku Shinkansen dropped; the Yamagata
  Shinkansen stops at neither 笹木野 nor 庭坂. 5 excluded: 伊達市 3, 二本松市
  1, Yamagata Prefecture 1 (板谷). Gate 3: Fukushima Kotsu's timetable page
  lists 12 stations, exact. English names: OSM's 32 objects, 3 cited
  overrides (Bijutsukan-toshokan-mae; Iizaka-onsen, as Hakodate's
  Yunokawa-onsen; Ioji-mae for OSM's Iohji-mae). Line names follow JR
  East's 福島 timetable index and ii-den.jp, with no macrons. Colours from
  `line_colour_search.py` (the Abukuma blue goes teal, Maebashi's; the
  Tohoku green olive; closest pair 45.4). Median station spacing 862 m:
  standard rings. No frequency floor (calls 46 and 86): the Ou Line from 福島
  to 庭坂, about 11 trains a day each way, drawn and named.
- **A slip:** staging's record did not quote the terms' ２(３) credit form,
  so the build fetched the terms PDF the brief names
  (`opendatariyokiyaku_2.pdf`, 133,265 B, HTTP 200, the city's host) into
  the scratchpad and read the form only; the verdict was not re-read. A
  terms page, not data, but not named for fetching at the build.
- **For the next city with a full list plus new-permit months:** under the
  foundation's term rules (calls 161 and 172) it cannot be one
  `rebuilt_register` source, since `TERM_AS_OF` takes one date per source;
  two sources by `SOURCE_KIND` is the shape (Ichinomiya's and Iwaki's too).
  Proposed for the japan-city skill at review time.
- **Not done here, by rule:** no region view, label tier or label offset
  (owner, call 198); `screen_japan_join.py` has no Fukushima entry;
  `city_master_list.md`'s built counts are Staging's.

### 2026-10-07 - Maebashi built, two food lists split by date and registers rebuilt to August 2026

- **Maebashi built (page 229, notice 176), Fukuoka's and Utsunomiya's
  two-source food shape plus its 生活衛生 registers: 4,696 storefronts (Food
  service 2,074, Food shops 1,362, Personal services 1,260) around 19
  stations on 3 lines, 40.5% of them in a ring (1,901).** The first city on
  the Japan foundation's rules (no `"rules"` key; `japan.city_rules` gives
  `ALL_RULES`). Sources: MHLW's filings (4,133 rows, every permit first
  granted from 2023 and the notifications), the city's food file from its
  former system (2,117 rows, as of 2026-06-30, granted 2019-10 to
  2023-03-31; the newest edition at build, `brief_check.py` 9/9), and the
  registers rebuilt by `config.source_rows`: the 2026-03-31 base zip plus
  five months of new and closed zips, keyed on 整理番号, every closure
  matched (barbers 310, beauty 830, laundries 139: the brief exactly). The
  rebuild stops the build on a closure that matches nothing, a repeated or a
  blank key, so it is exact, never an upper bound. A city `source_rows`, as
  the build prompt says for a zipped register; no shared code changed for it.
- **Terms (calls 161 and 172):** `TERM_AS_OF` MHLW 2026-08-31 (the month its
  file covers; newest permit 2026-08-28), the food file 2026-06-30 (its own
  date; its 179 rows expiring 2026-09-30 are in term then). Past term 0;
  starting after the as-of 1.
- **Step 2:** of 5,078 storefront rows, 4,628 at the block, 237 at MHLW's own
  point (all from chōme), 211 at a town centre, 2 unplaced (a barber at
  駒形町東高島 and a laundry at 駒形町増田境, addresses MLIT's files do not
  hold). On the map: 91.7% block, 4.4% MHLW's point, 3.9% town centre.
  MHLW's point against the block point: median 42 m, 92.4% within 250 m
  (2,100 rows), the brief exactly. 149 of the city's rows dropped for an MHLW
  row (`SUPERSEDES`: the brief's 18 counted restaurant permits only; the key
  is per premises and bucket, so the co-located Retail rows and konbini
  permits it lists go too, as the one-pin rule would fold them), 231 repeat
  permits shown once. Set aside: 3 mobile salons (`idou`, the brief's three),
  2 area-wide addresses. Closed 16; no address published 635 (MHLW; 38 of
  1,850 open restaurant permits, "one in 50", the brief's figure); not a
  premises 328. Out by rule 1,466: 409 manufacturing and other non-counter
  types (the brief's 299 + 110 exactly), 407 snack bars and cabarets by
  業態, 299 canteens, 187 temporary or mobile, 78 vending, 49 inside
  accommodation, 30 caterers, 7 mail order.
- The 菓子 / そうざい factory share: 34 of 541 (6.3%), kept (owner,
  2026-09-24).
- **Economic Census control:** 2,074 Food service pins against 1,299 飲食店
  establishments in 10201: 1.60 per establishment, inside the built cities'
  1.56-1.92 (the brief predicted 1.62 before de-duplication).
- **Privacy verdict: publish.** `check_personal_exposure.py maebashi`: the
  Japan pass prints 0; 19 trade names in the raw files are an operator's own
  name, 3 pins show their permit type. The name rule compares MHLW's 法人名,
  the food file's 営業者名 and the registers' 開設者氏名 / 営業者氏名 and their
  representatives, in memory only.
- **The privacy check's Japan pass corrected** (`scripts/check_personal_exposure.py`):
  it read a city's rules as `CITIES[slug].get("rules", ())`, so a city built
  after the foundation (no `"rules"` key) was checked with no rules while
  step 2 reads `ALL_RULES`; on Maebashi it counted 10 names step 2's rules do
  not flag (26 names against 19). Now `japan.city_rules(slug)`, which returns
  `WAVE2_RULES` for every built city, so their verdicts stand (Sasebo
  re-run: 0). East-1 made the identical one-line change on its branch.
- **Rail:** N02-25; 19 stations: the Jomo Line 14 of 23, JR Ryomo 4 of 19, JR
  Joetsu 2 of 39 (新前橋 one group on both JR lines). No Shinkansen station
  in the city; JR's Agatsuma Line has no in-city station of its own and is
  not drawn. Median nearest-station gap 1,000 m: standard rings. 6 excluded:
  桐生市 2, 高崎市 2, 伊勢崎市 1, 渋川市 1. Gate 3: the Jomo Electric
  Railway's timetable index gives 14 in-city stations, exact. English names:
  OSM's 35 objects, 1 cited override (心臓血管センター, "Shinzo-kekkan
  Center"). Colours from `line_colour_search.py` (the Jomo blue goes teal,
  Sasebo's; Ryomo yellow to ochre; closest pair 61.3). No frequency floor
  (calls 46 and 86): the Jomo Line every 30 minutes, nothing under hourly.
- **Not done here, by rule:** no region view, label tier or label offset
  (owner, call 198: Cleanup builds the Japan views), so the scaffold's
  default offset stands and Maebashi has no `label_tier`; `screen_japan_join.py`
  has no Maebashi entry (step 2 measures the join); `city_master_list.md`'s
  built counts are Staging's (the plan's change 4), so `check_provenance.py`
  fails on them until Staging moves the batch.
