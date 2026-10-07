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

## Entries

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
