---
name: tokyo-ward
description: Add one of Tokyo's 23 special wards to the Tokyo map as its own source - each ward is its own publisher, with its own file, format, date, licence, credit and completeness. Covers the ward card (the fields a ward must have before it goes on), the owner's rule for which wards go on, how a ward becomes a config entry on the shared Japanese steps (source_rows, SOURCE_MUNICIPALITY, SUPERSEDES for MHLW's slice), the per-ward share of the official count that the page states, and the traps the eight known wards taught. Use for the Tokyo build and whenever a missing ward's data turns up; read with japan-city, which it does not replace.
---

# Adding a Tokyo ward

Written 2026-09-28, before the Tokyo build, from the eight wards the brief
measured (`docs/build_briefs/tokyo.md`) and a test of the shared steps on all
eight. **Tokyo is not one publisher but 23.** Each special ward runs its own
health centre and publishes (or does not) its own permit list, so the map is
built ward by ward, and a ward can join later without touching the others.

Read `japan-city` first: everything there holds (the join, the taxonomy, the
name rule, the owner's standing calls, the notices' MLIT lines). This skill
is only what a WARD adds.

## The owner's rules for a ward (do not re-ask)

- **A ward is on the map only with a full, current food list** (2026-09-24).
  Partial, stale or first-permits-only lists are recorded and left out.
  **One exception**: Meguro's first-permits list ships at its measured share
  (2026-09-24), disclosed. Shinjuku's 2023 snapshot ships with its vintage
  disclosed (2026-09-24).
- **Each ward's share of the official count goes on the page** (2026-09-24), so
  a partial ward reads as partial. The build MEASURES it (below); nobody types
  it.
- **MHLW's open-data slice is added to Chūō, Kōtō, Minato and Shinjuku**,
  de-duplicated against the ward's own list (2026-09-24). It adds +0.1 to
  +3.1% of the official count; it is not a fix.
- **The COVID-era lists (徹底点検TOKYOサポート and the sticker list) are never
  used**, whatever the catalogue's licence says (2026-09-24).
- **A ward with no business data**: its stations are drawn HOLLOW, ringless,
  with a tooltip "No business data: <ward> publishes no usable food-permit
  list" and a legend row (2026-09-28), because ward boundaries cannot be drawn
  (N03, the Survey Act) and the station is the only place to say it. Built
  2026-09-28: `japan_step1` flags them from `config.NO_DATA_WARDS`
  (`no_data`, `no_data_reason` in stations.csv); `map_common.render_heatmap`
  draws them hollow (filled at opacity 0, so dark mode keeps them hollow),
  rings and counts only the stations WITH data - a business near a ward edge
  goes to its nearest station with data - and adds the legend row. A city
  without the column renders exactly as before (all 54 maps identical).
  **A ward with personal-services registers but no food list is still
  inactive** (owner, 2026-09-28: food is most of any station's count, and
  Ikebukuro drawn from barbers alone would read as a desert). 7 of the 15
  (Chiyoda, Bunkyō, Shinagawa, Ōta, Toshima, Arakawa, Katsushika) publish
  barber / beauty / laundry registers that stay unused, hence "food-permit
  list" in the tooltip.

## The roster: `pipeline/tokyo/wards.py`

**The one place a ward is switched on.** All 23 wards, each `"status":
"active"` (with its `food` files, optional `personal` and `mhlw`, its
`encoding`, a `share_note`) or `"inactive"` (with its `why`, which names the
gap for the page). `japan.CITIES["tokyo"]["wards"]` reads the active codes
from it, so the city line, the address-file fetch and the share check follow;
`NO_DATA_WARDS` (code -> English name) feeds step 1's hollow stations;
`check()` refuses a half-made switch (an active ward with no files, an
inactive one that still lists files, a missing file, a ward without a reason).
It imports nothing from the pipeline, so `japan.py` reads it without a cycle.
2026-09-28: 8 active (Chūō, Minato, Shinjuku, Taitō, Kōtō, Meguro, Setagaya,
Shibuya), 15 inactive.
- **Outreach is the last resort.** Requests to Chiyoda, Toshima, Nerima and
  Edogawa stay parked (`docs/gated_access.md`).

## The ward card - fill it before any code

One per ward, in the Tokyo brief's "Ward cards" section (the `tokyo-sources`
research session writes them for the missing wards). A ward with an empty
field does not go on.

| Field | What to record | Why it matters |
|---|---|---|
| ward, code | 渋谷区, 13113 | `SOURCE_MUNICIPALITY` and `MUNICIPALITY_CODES` |
| verdict | ON / OFF (one phrase) / OPEN | the owner's rule above |
| file(s), host, size | exact URLs; the ward's own host, or one its pages name (Shibuya's ArcGIS, Meguro's BODIK, Nakano's wagmap were accepted) | `fetch_sources.py`, provenance |
| format | encoding, delimiter, header shape, address layout | the traps below |
| as of | the list's own date | the page, table D |
| closures | the closure column, if any | Shibuya keeps 22,311 closed rows |
| operator columns | exact names | `japan_register.OPERATOR_COLS`; the name rule reads them in memory |
| own coordinates | columns, if any | a check on the join, never the map's source |
| licence | the verdict shape and the credit it prescribes | notice (each ward its own credit) |
| join | block / chōme / none | `scripts/screen_japan_join.py <key>` |
| share | of the yearbook's 飲食店営業 count | the page |
| personal services | the ward's barber / beauty / laundry registers and their date | the layer's own coverage |

## A ward as a config entry

The shared steps already take Tokyo's shape (2026-09-28, each change naming
Tokyo or the city that taught it):

- **`SOURCE_MUNICIPALITY = {key: "渋谷区"}`** (`japan_step2.municipality`): the
  WARD is the municipality its addresses are read against. Without it the
  Tokyo-wide `MUNICIPALITY` would be stripped from nothing and every address
  would lose its ward. Taitō's addresses start at the town: the ward default
  handles it (`permits_from_rows`, a municipality ending 区).
- **`config.source_rows(key)`** (Kyoto's): a ward with more than one file
  (Meguro's `all_new_8.csv` + `all_old_8.csv`) is one source.
- **`MUNICIPALITY_CODES = {"渋谷区": "13113"}`**: the baseline keys.
- **`OFFICIAL_SHARES = True`**: the share check, below.
- **MHLW's slice for a ward**: a source keyed like `mhlw_13103` with its own
  `SOURCE_MUNICIPALITY`, in `ADDRESS_BY_CONSENT` and `OWN_POINT_FALLBACK`
  (Fukuoka's mechanisms), and **`SUPERSEDES = {"minato": ("mhlw_13103",)}`**:
  the ward's own row wins where both lists hold a premises (same ward, town,
  block, trade name and bucket). MHLW's files are cached in `data/mhlw/raw/`
  (13101-13104, 13108, 13113, 13116).
- **One ISJ directory for all the wards** (`ISJ_DIR`): `load_city_isj` keys each
  block by its ward, so eight wards' files sit side by side. Minato's pair is
  at `data/tokyo/raw/` itself, the rest under `data/tokyo/raw/<code>/`.

**Measured 2026-09-28** on all eight food wards through the shared step 2 (a
scratch config): 55,153 storefront rows, **99.7% block, 0.3% chōme, 0.1%
unplaced**; where a ward publishes its own coordinates, a median **24 m** from
the block point (25,149 rows). Per ward, the join matches the brief's screen
within 0.6 pt (Shinjuku 98.9% against 99.2%).

## The share of the official count - measured every build

`japan_step2.official_shares` (opt-in, `OFFICIAL_SHARES = True`) counts each
municipality's 飲食店 permit rows the brief's way - vehicles and stalls IN (the
official count includes them), closed rows OUT - against
`pipeline/countries/japan_official.py`: Tokyo's yearbook table 19-8 per ward,
e-Stat's 衛生行政報告例 per designated city. It emits `official_rows_<code>`
and `official_count_<code>` to the baseline, so `drift_check` flags any share
that moves, and writes `outputs/tokyo/official_shares.json`, **which the page
reads**. The eight wards' shares, reproduced exactly on 2026-09-28:

| Ward | Rows | Official | Share |
|---|---|---|---|
| Shibuya 13113 | 10,887 | 10,798 | 100.8% |
| Shinjuku 13104 | 12,888 | 15,356 | 83.9% |
| Taitō 13106 | 6,533 | 8,112 | 80.5% |
| Setagaya 13112 | 5,845 | 9,291 | 62.9% |
| Meguro 13110 | 2,279 | 4,370 | 52.2% |
| Minato 13103 | 4,892 | 15,939 | 30.7% |
| Chūō 13102 | 1,319 | 11,056 | 11.9% |
| Kōtō 13108 | 570 | 6,102 | 9.3% |

**The page states each share WITHOUT MHLW's slice** (owner 2026-09-28): the
share describes the ward's own publication; MHLW's +0.1 to +3.1 pt is said
once in prose. Tokyo's config lists its MHLW sources in `SHARE_SKIP`.

## The traps the eight wards taught

1. **Shibuya's national-schema export read NOTHING** through the shared step
   until 2026-09-28: its address is `施設所在地_連結表記` and its type
   `営業の種類もしくは営業の形態`, neither then known to `japan_register`.
   Both are now in `ADDR_COLS` / `TYPE_COLS`. **A new ward whose rows all come
   back "not a premises" has an address column the reader does not know** -
   check `rows[0].keys()` against `ADDR_COLS` first.
2. **Closed rows**: Shibuya marks them `廃業日`, MHLW `廃業年月日` or a
   `(廃業)` in 申請区分; both are dropped as `closed`. A ward list that keeps
   closed premises under another column name will inflate its share past 100%
   - Shibuya's is 100.8% with them out.
3. **Five encodings and three formats**: Chūō cp932 with empty split columns
   (the joined `所在地_連結表記` is read); Shinjuku UTF-16 LE with the whole
   address in 町字; Taitō Shift_JIS, own format, addresses starting at the
   town, operator columns (individuals masked ※ at source); Meguro a
   quote-wrapped TSV (registers); Setagaya own format. `city_rows` sniffs them
   all; declare each in `SOURCE_ENCODING` anyway.
4. **`業態` is read beside the type** (Fukuoka's `FORM_RULES`): the national
   schema carries it, so Tokyo's vehicles, stalls, staff canteens and hotel
   restaurants are caught - 2026-09-28's test dropped 362 rows by form.
   **Fukuoka's yatai rule (ろ店 counts)** runs here too: read what ろ店 means in
   Tokyo's rows before trusting it; a festival stall is not a yatai.
5. **Taitō's operator columns carry home addresses.** Only 名称 and 所在地 are
   ever selected; the name rule reads the operator's NAME in memory and nothing
   else. Taitō, Shinagawa, Shibuya and Bunkyō's registers carry 営業者氏名 and
   営業者_所在地: add each ward's spelling to `OPERATOR_COLS` and re-run the
   Minato control.
6. **A building name holding 丁目 is read as the town**: `新宿1-3-12
   壱丁目参番館` - 4 of the 33 unplaced rows in the test. Measured, not fixed;
   fix it in `permits_from_rows` (with the Minato control) if a new ward has
   more.
7. **Each ward its own credit** (Shibuya, Taitō, Setagaya and Meguro prescribe
   theirs; the catalogue's wards share one combined notice with a DATE OF USE).
   Build the notice from the ward cards, never by hand (the plan's item 5).

## Adding a ward later

1. The ward card, complete, with verdict ON (the owner's rule).
2. `python scripts/screen_japan_join.py <key>`: the join, block rate against
   the other wards'.
3. **The switch, in `pipeline/tokyo/wards.py` only**: `"status": "active"`,
   its `food` files (and `personal`, `mhlw` if any), `encoding`,
   `share_note`; delete `why`. Its operator columns go into
   `japan_register.OPERATOR_COLS` if new (then the Minato control), and its
   credit into the notice.
4. `python pipeline/tokyo/fetch_sources.py isj` (its address files), then the
   three steps: step 1 turns its stations from hollow to ringed by itself, and
   step 2 prints and emits its share.
5. The map checks, drift (`--update-baseline`: an intended change), the page's
   ward table (from `official_shares.json`), `excluded_categories.md`, the
   notice, DECISIONS. Published prose waits for the owner.
