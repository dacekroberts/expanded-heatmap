# Drafts: East-2 (branch `worktree-japan-east-2`)

The A/B build plan's East-2 batch (`docs/build_plan_2026-10-07.md`): Koshigaya,
Sagamihara, Fujisawa (A); Kawaguchi, Funabashi, Matsudo, Ichikawa, Urayasu,
Sakura, Yachiyo, Ichihara (B). Pages 240-250, notices 187-197 in build order.
Newest entry first. Cleanup folds this file into `DECISIONS.md`.

## Downstream inputs this branch changes

- New cities (each with `outputs/<slug>/`, a `app/cities.py` entry, a notice
  and rows in `docs/data_sources/japan.md`): Koshigaya (notice 187).
- Station names in English are OpenStreetMap's for every city here; the rail
  is MLIT's N02.
- `pipeline/line_registry.py`: Koshigaya added to the maps of
  `tobu-skytree-line` and `jr-east-musashino-line` (no colour changed).
- Per notice, for Visuals: **187 (Koshigaya): caption only** (PDL 1.0's credit
  has no placement rule beyond being stated with the work; the same reading
  as Kasukabe's 164). No open terms question.

## Parked calls

None yet.

## Applied by precedent (named for the batch report)

- **Koshigaya, the brief's three weighed calls**, each applied as the brief
  recommends on the precedent it names: (1) no food-share sentence on the
  page, the city's withholding note stated with no number (call 125 as read
  for Hirakata, call 154; Kasukabe's call 173 wording); (2) the missing July
  2026 list: the food page re-read at build (brief check, 2026-10-11: still
  no July file), the months stated as April, May, June and August (calls
  126-127: MHLW's permits are not added in its place); (3) MHLW's
  notifications left out, since the city's own list publishes notifications
  (127b answered lists that have none).

## Proposed wording (no template covers these; for review time)

- **Koshigaya** (page 240): "From Koshigaya City's list of food-business
  permits and notifications (as of March 31, 2026, with the new and renewed
  permits it listed for April, May, June and August 2026; the city published
  no list for July) and its lists of barbers, beauty salons and laundries (as
  of October 2, 2026)."; "The city leaves out some premises at their
  operators' request, so the food list is not complete." (Kasukabe's sentence
  with the city as publisher); "Minami-Koshigaya (JR) and Shin-koshigaya
  (Tobu) are separate stations a short walk apart, so their rings overlap.";
  the Reading-the-map placement bullet in Ichinomiya's form with the
  ministry named in full. The notice (187) adds "The city leaves out some
  premises at their operators' request, and no list for July 2026 was
  published." The same facts in its What Is Excluded section.
- **The credit's titles (187)** are the portal datasets' own (【越谷市】食品営業
  許可・届出一覧, 【越谷市】営業施設一覧) with the creator section the licence
  record names; check them against the licence-read report at review time.

## Shared-state findings for review time (not changed here)

- `app/components.py`'s `_OSM_STATION_NAMES` and notice 1's sentence do not
  name Regional-1's eleven cities, and the sentence does not name Kansai-1's
  seven; `app/osm_notice.py` names Kansai-1's but not Regional-1's. East-2's
  cities are added to all three as East-1's were. Cleanup's to reconcile.

## Entries

### 2026-10-11 - Koshigaya built, the March food list kept whole with the months since, and the October registers

- **Koshigaya built (page 240, notice 187), Ichinomiya's shape (a city's own
  full food list kept whole plus the months since, owner call 126) with
  Toyama's point-donor use of MHLW's file: 4,092 storefronts (Food service
  1,988, Food shops 1,114, Personal services 990) around 8 stations on 2
  lines, 71.7% of them in a ring (2,934).** On the Japan foundation's rules
  (no `"rules"` key). The brief's checks: 16/16 (2026-10-11). Sources: the
  city's food list of permits in term and notifications on 2026-03-31 (4,567
  rows) and its monthly lists of April, May, June and August 2026 (235 rows),
  and its barber, beauty and laundry lists of 2026-10-02 (225, 645, 124).
  Every file was on disk from Step 0 (2026-10-06); the build fetched only the
  OSM station names (one Overpass query; overpass-api.de answered 504, the
  kumi mirror answered).
- **Merge (a) as two sources, not one rebuilt register** (Ichinomiya's
  finding, applied): the March list is source `food` (`TERM_AS_OF`
  2026-03-31: 1 permit past its term) and the months source `food_new` of the
  same kind (`TERM_AS_OF` 2026-08-31: 0 late starters). The months carry
  renewals as well as new permits; one pin per premises and bucket shows a
  renewed premises once (294 repeat rows dropped). The brief's
  `rebuilt_register` worry (rows with no end date dropped) does not arise:
  the list is read whole, so the 1,472 notifications reach step 2. No shared
  code changed; 代表者名（法人） and 代表者_氏名 were already in
  `OPERATOR_COLS` (the foundation).
- **MHLW (calls 126-127):** nothing of it is drawn. `POINT_DONORS` gave its
  own point to 18 city rows the block join left at a town centre (15 pins).
- **Step 2:** of 4,394 storefront rows, 4,244 at the block, 124 at a town
  centre, 18 at MHLW's point, 8 unplaced (0.2%). On the map: 96.7% block,
  3.0% town centre, 0.4% MHLW's point. Not a premises 382 (vehicles, stalls,
  市内一円, storeless). Out by rule 1,019: 291 institutional catering, 254
  vending, 215 manufacturing and other non-counter types, 181 hostess venues
  (種目 カフェバーキャバレー, out whole on Tokyo's precedent, owner 2026-09-29;
  the brief measured 177), 60 caterers (種目 is one value per row, so none
  also names a counter form), 18 inside accommodation. Kept by 種目: 151
  konbini holding a restaurant permit, 79 department stores and
  supermarkets, 37 delis (Retail).
- Against the brief: Food service 1,988 (the brief 1,977 before the foundation's
  rules); Retail 1,114 pins from 1,314 rows (the brief's 1,288 counted rows
  before one pin per premises).
- The 菓子 / そうざい factory share: 19 of 214 (8.9%), kept (owner,
  2026-09-24).
- **Economic Census control:** 1,988 Food service pins against 1,095 飲食店
  establishments in 11222: 1.82 per establishment, inside the built cities'
  1.56-1.92 (the brief's 1.80).
- **Privacy verdict: publish.** `check_personal_exposure.py koshigaya`: the
  Japan pass prints 0; 7 trade names in the raw files are an operator's own
  name, 1 pin shows its permit type.
- **Rail:** N02-25; 8 stations, 8 groups: the Tobu Skytree Line 6 of 55
  (伊勢崎線), JR East's Musashino Line 2 of 27, both main lines cut at the
  line. 南越谷 (JR) and 新越谷 (Tobu), 132 m apart, are separate N02 groups of
  different names and stay apart (trap 1); `SPACING_MIN_M = 100` lets gate 1
  read them as two stations (Tama's precedent). Median nearest-station gap
  1,295 m: standard rings. 9 excluded: 草加市 3, 春日部市 2, 吉川市 2, 三郷市 1,
  川口市 1. Gate 3 exact (6 and 2). English names: OSM's 14 objects, no
  override (Shin-koshigaya and Kita-koshigaya as Tobu signs them).
- **Colours:** both lines are registry lines (`tobu-skytree-line` #007890,
  `jr-east-musashino-line` #F05820): 51.4 and 54.7 from the nearest pin, over
  45. `check_line_identity.py`: PROBLEMS 0.
- **Region:** `Saitama Prefecture` (the view Sōka and Kasukabe are in);
  `label_tier: "minor"`. No region table touched (call 198).
