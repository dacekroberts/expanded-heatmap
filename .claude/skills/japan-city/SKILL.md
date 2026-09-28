---
name: japan-city
description: Build a Japanese city on the shared modules Kobe built - japan_step1 (MLIT N02 rail cut at the N03 city line, collapsed on N02's station-group code, English names from OSM), japan_step2 (the city's permit lists through the japan_eigyo taxonomy and the MLIT block join, the owner's name rule), the owner's standing calls, the traps Kobe measured, the notices, and a sheet per city (Osaka, Sapporo, Fukuoka, Kyoto and Tokyo built, with what each left the next - Tokyo's service routes, line-code labels and built credits for any big network). Use for any Japanese city after Kobe; read with add-city, address-join, cjk-text and publish-city, which it does not replace.
---

# Building a Japanese city

Written 2026-09-27 from **Kobe**, Japan's first city (`DECISIONS.md`, "Kobe
pipeline built" and the entry above it). Japan is **Spain's shape in its
business leg and Mexico's in everything else**: every city publishes its OWN
permit list, in its own format, but the rail (N02), the city line (N03), the
coordinates (MLIT 位置参照情報) and the taxonomy are national. Kobe put all the
national parts in `pipeline/countries/`, so the next city should be a config,
a `fetch_sources.py` and three thin steps, plus whatever its own list does
differently.

Read the city's brief first (`docs/build_briefs/<city>.md`, and run
`python scripts/brief_check.py <city>`), then this. Kobe's files are the
worked example: `pipeline/kobe/config.py` holds every city-specific choice.

## What already exists - reuse it, do not rewrite it

| Module | What it does |
|---|---|
| `pipeline/countries/japan.py` | N02/N03/ISJ URLs and the SHARED cache (`data/japan/raw/`: N02 once, N03 per prefecture); `CITIES` (ward codes, prefecture, EPSG); `city_boundary()` (N03 wards' union - **never drawn**); `stations()` (Shinkansen dropped, platform centroids); `stub_test()` |
| `pipeline/countries/japan_register.py` | The JOIN: `city_rows()` (CSV / XLSX / zip, any of the four encodings, TSV sniffed), `permits_from_rows()`, `load_city_isj()`, `join_city()` - every normalisation rule, each naming the city that taught it; `kyoto_permit_stream()`; `name_is_operator()` - the owner's name rule |
| `pipeline/countries/japan_step1.py` | THE step 1: `run(config)`. N02 stations inside the city line → collapse on `N02_005g` → OSM `name:en` → gate 3 → excluded stations named by N03 municipality → a lines GeoJSON keyed by `config.LINES` |
| `pipeline/countries/japan_step2.py` | THE step 2: `run(config)`. `config.SOURCES` → closed (廃業) out → not-a-premises → `japan_eigyo` → the join (tiers) → the publisher's own point where the block join misses (`OWN_POINT_FALLBACK`, tier `own`) → one premises in two lists once (`SUPERSEDES`) → one pin per premises and bucket → the name rule → the 菓子/そうざい factory measurement. `ADDRESS_BY_CONSENT` counts a withheld address apart from "not a premises". All four optional, all Fukuoka's (2026-09-28) |
| `pipeline/taxonomies/japan_eigyo.py` | Every permit-type spelling across ten screened lists (289 values); `source` decides Personal services; **`FORM_RULES` read 業態 beside the type** where a list keeps it in its own column (Fukuoka's two; MHLW's everywhere): vehicles, stalls, school kitchens, hotel restaurants out, konbini Retail, yatai in - a form never brings a row in; import-time asserts pin the rule order |
| `pipeline/countries/japan_fetch.py` | THE fetch (2026-09-28): city files from `config.SOURCE_FILES` ({key: (file, URL, dataset page)}), ISJ per ward, N02/N03 into the shared cache, the OSM names query plus the tram-stop query where the config declares `TRAM_OSM_JSON`; keeps what is on disk and records provenance. A city's `fetch_sources.py` is its docstring and `japan_fetch.main(config, __doc__)` |
| `pipeline/countries/japan_official.py` | The official restaurant counts a list is measured against: Tokyo's yearbook table 19-8 per ward, e-Stat's 衛生行政報告例 per city (2026-09-28); `japan_step2.official_shares` reads them where `OFFICIAL_SHARES` is set |
| `pipeline/kobe/step3_map.py` | The template map: `load_geojson_line_shapes` over step 1's GeoJSON, `label_focus=japan.city_boundary(slug)`, **`lang="ja"`** |
| `scripts/check_personal_exposure.py` | `japan=True` on a city's entry runs the name-rule test on what reached the map (must print 0) |
| `scripts/screen_japan_join.py` | The join's measurement, with **Minato as the control** |

**`japan_register.py` has a control: Minato.** Any change to it re-runs
`python scripts/screen_japan_join.py minato` (must stay block 98.0 / chōme 0.2 /
none 1.8) AND every city screen, old against new. Kobe's one change (a city's
name inside an address) moved only Hiroshima, by +0.3 pt, and that diff is the
evidence in `DECISIONS.md`.

**A city's step files are three lines.** Anything a second city would also need
goes into the shared module with the city that taught it named in a comment;
the owner reminded Kobe's build that it exists for the cities after it.

## The owner's standing calls - do not re-ask

- **The Shinkansen does not count** (2026-09-24); `japan.stations()` drops it.
- **Lines served only by limited expresses (特急) DO count** (2026-09-28):
  in Japan a limited express is regularly scheduled commuter traffic, not
  intercity service. Draw such a stretch like any other line. This reverses
  the one-off that left Osaka's Umekita → 福島 track out (2026-09-27);
  revertible if a city shows why (owner).
- **The city line only** (2026-09-24): only stations inside the city get
  rings, because each permit list covers its own city. JR and the private
  railways are drawn and cut at the line - **a one-station stub stays as cut**
  (Kobe's JR Takarazuka Line, 1 of 30; 2026-09-27). An URBAN line cut to a stub
  still goes back to the owner.
- **菓子製造業 and そうざい製造業 count, in Retail** (2026-09-24). The
  factory / central-kitchen share is MEASURED (step 2 prints it) and **kept**
  (2026-09-27: Kobe 115 of 2,362, 4.9%; dropping names matching 工場 / センター
  was rejected because real shops are called …センター).
- **The name rule** (2026-09-27, every Japanese city): where the trade name IS
  the operator's own name, the pin shows its permit type.
  `name_is_operator()` reads 営業者名 / 開設者名 / 申請者名 / 代表者名 IN MEMORY
  and returns only yes or no; nothing else about the operator is kept. A trade
  name that adds a business word to the owner's name (<name>商店) is shown.
  Kobe: 14 in the raw files, 10 on the map. The Latin heuristic's 0 is not a
  finding for Japanese names; the Japan pass is.
- **English station names from OSM `name:en`, Japanese beside them** (the
  Seoul / Taichung precedent; 2026-09-27). A missing name stops step 1.
- **Numerals as figures** (2026-09-28): a number before 丁目 is ALWAYS a
  figure in the English name ("Nishi-11-Chome", never "Nishi juitchome");
  before 条 only where the city's 条 is a numbered street grid, declared as
  `config.JO_IS_GRID` (Sapporo). Elsewhere 条 is part of a name and keeps its
  signed word (Osaka's Kujō, Kyoto's Shijō, Tokyo's Jūjō). `japan_step1`
  STOPS on a violation; fix it in `config.OSM_NAME_EN_OVERRIDES`, a cited
  table ({ja: en}, the OSM spelling replaced in a comment), which is also
  where OSM's inconsistent romanisations are brought to one style (Sapporo:
  29 entries, OSM's hyphenated title case).
- **Sightseeing funiculars are left out** (Kobe's Maya and Rokkō, 2026-09-27),
  and their stations are NOT written to `excluded_stations.csv` (that file is
  for stations cut from a network that IS drawn; `check_scope_disclosure.py`
  refuses any other reason). The page says so.
- **Fault-based cost clauses** are accepted for all of Japan (2026-09-24).
- **No page says "currently operating"**: the lists keep closed premises.
- **Region: East Asia**. Country: "Japan". Projected CRS from
  `japan.CITIES[slug]["epsg"]` (Sapporo and Tokyo 54N, Fukuoka 52N).

## The traps Kobe measured

1. **Collapse stations on `N02_005g`, never the name.** Kobe's name collapse
   joined two 長田 1.5 km apart, two 御影 1.1 km apart and two 住吉 751 m apart;
   the group code merges only real interchanges (widest: 三宮, 273 m). Separate
   stations of different names can sit 29 m apart (Tarumi / Sanyo Tarumi) -
   MLIT keeps them apart, and so does step 1. Read the close-pair list it prints.
2. **N02 files a public line under its LEGAL sections.** The Seishin-Yamate
   Line is 山手線 + 西神線 + 西神延伸線; the Port Liner arrives in two railway
   classes (16 and 24). Build `config.LINES` from `stub_test()`'s table, and
   step 1 stops on any in-city N02 line the config does not name.
3. **A branch with its own public name hides inside an N02 line**: the
   Wadamisaki Line is in JR's 山陽線. `config.BRANCHES` splits it by walking the
   section graph from the terminus to the junction, with a length window that
   stops a runaway walk.
4. **Shared tunnels are filed under each operator**: the Kobe Kōsoku Line is
   阪急/阪神/神戸電鉄 `神戸高速線`. Draw it once, under its own public name.
5. **The city's name can appear INSIDE an address** (灘区…神戸市立六甲山牧場):
   fixed in `permits_from_rows`; the ward is found first now.
6. **市内一円 rows are not premises**: 1,943 of Kobe's 26,704 food rows are
   trucks and stalls licensed citywide under plain 飲食店営業, with no type
   marker. The address, not the type, catches them. Also: 移動美容室 (a salon
   in a vehicle) in the beauty register.
7. **One premises holds several permits.** A bakery with 菓子 and そうざい is
   two rows and one shop: step 2 keeps one pin per (address, trade name,
   bucket) - Kobe dropped 1,183.
8. **Encodings differ inside one city**: Kobe's food list is cp932 CSV, its
   three registers UTF-16 LE, TAB-separated, named `.csv`. `city_rows()` sniffs
   both; declare them in `SOURCE_ENCODING` anyway.
9. **OSM `name:en` disagrees with itself at shared stations** (神戸三宮:
   "Kobe-Sannomiya" / "Kobe Sannomiya"): settle ties in
   `config.OSM_NAME_EN_TIES`, never by first-found. Different stations sharing
   an English name get their operators appended (Mikage (Hankyu) / Mikage
   (Hanshin)) from `LINES[...]["short"]`.
10. **Line colours: readable on BOTH basemaps first.** Kobe's first palette
    cleared Delta-E 45 against the pins by going so dark that JR, the subway
    and Hankyu vanished on the dark basemap. Require 3:1 contrast against
    `theme.DARK["page"]` and `#ffffff`, then 45 against the pins and ~18 between
    lines. The colours are the project's own, hue-matched to the operators',
    so they have no branding excuse below 45; record any exception (Kobe:
    Hanshin blue, 35.3 against Retail blue).
11. **A new East Asia city moves the region's zoom.** Kobe widened the frame,
    and Taoyuan's pill then covered Taichung's marker; one offset change fixed
    it. Measure the new city's label width in the app's own document with two
    known widths reproduced, then re-score every East Asia label.
12. **The N03 extent decides `CITY_BBOX`**, not a guess: Kobe's first box cut
    the city's western edge, and step 1 stopped on it. Re-fetch OSM names if
    the box grows.

## Notices - one per city, and the 出典 line is prescribed

Each city's notice carries its own list's prescribed credit (its brief's
licence section), then the two MLIT credits every city shares, then N03
credited as not drawn, then the two MUST-NOTs. Kobe's (notice 50):

| Part | Wording |
|---|---|
| City list | `出典：「生活衛生関係許可施設等の情報提供」（神戸市）（<page URL>）を加工して作成` + © and the CC BY 2.1 JP link |
| Coordinates | `出典：位置参照情報ダウンロードサービス（国土交通省）（https://nlftp.mlit.go.jp/isj/）を加工して作成` |
| Rail | `「国土数値情報（鉄道データ）」（国土交通省）をもとに作成` |
| City line | `国土数値情報（行政区域データ）` (CC BY 4.0; not drawn) |
| Always | may include closed premises; the city and MLIT did not make and do not endorse the map |

The MLIT lines are the same in every city; copy them, change only the city
part. `check_provenance.py` matches the notice heading against its numbered
item in `docs/data_sources.md`.

## Before any city: the briefs predate Kobe

Every remaining brief was written 2026-09-24, before Kobe. Correct them at the
build (a brief to correct, never a check to relax), in particular:

- **Their privacy sections say never to read the operator columns** (Osaka
  L188, Sapporo L103, Fukuoka L162, Kyoto L45/L214, Tokyo L330). **The owner's
  name rule of 2026-09-27 supersedes that for every Japanese city**: the
  operator column is read in memory to compare, never kept. Check the city's
  column names against `japan_register.OPERATOR_COLS` (営業者名, 開設者名,
  申請者名, 代表者名) and ADD the city's spelling there (Tokyo's 営業者氏名,
  Fukuoka's 開設者法人名（開設者氏名）, Kyoto's 申請者＿申請者名 / 申請者氏名),
  or the rule silently compares nothing - then re-run the Minato control.
- Several still list as open what the owner decided on 2026-09-24 (the
  Shinkansen, 菓子/そうざい, the city-line scope). Mark them decided.
- None has run the **Economic Census join control** (PLAN, "Join control"),
  and none of the five built cities (Kobe to Kyoto) has. **The e-Stat download is approved (owner,
  2026-09-28)**: one national per-ward table serves every city; name its
  file, source and size when fetching it.

## The city sheets (Osaka, Sapporo, Fukuoka and Kyoto built; Tokyo to build)

Sheets from the briefs (line numbers are the brief's), 2026-09-27. Every brief
has a `brief-checks` block; run it first. What each city needs BEYOND Kobe's
config is marked ▶. A built city's sheet is kept for what it left the next.

**Osaka** - ✅ **BUILT 2026-09-27** (72,999 storefronts, 216 stations, 34
lines; DECISIONS "Osaka pipeline built on the shared Japanese steps" and
"Shared code changed for Osaka"). The sheet as written before the build:

(`osaka.md`; 24 wards, EPSG:32653) - the closest to Kobe.
- One city CSV, `…/contents/wdu280/260630zenku.csv` (63,902 rows, as of
  2026-06-30; 61,752 fixed); the portal's `data-00000382` is a stale 2021 twin.
  Personal services: the city's ri/bi/cleaning CSVs, 15,775 premises.
- ▶ **Its 経度 / 緯度 columns are swapped** (`permits_from_rows` already
  swaps them back); its own coordinates are an independent check - median
  38 m against the block point.
- Join 99.1 / 0.9 / 0.0; the kanji-variant rules came from here (曽根崎新地
  alone is 1,807 permits). Underground malls stay unplaced.
- Rail passes: Osaka Metro 80-100%, the New Tram (AGT) 100%, the Hankai tram
  17 of 32 (half a line, not a stub).
- ⚠️ **The list is 67% of MHLW's restaurant count** (54,289 of 81,418). The
  evidence says the national figure is inflated (about 16,260 dead old-law
  permits), not the list short; about 9,000 are unexplained. The owner approved
  page wording for it (L80-87) - use it.
- Notice: `「食品営業許可施設一覧」（大阪市）（…0000575579.html）を加工して作成`,
  and likewise pages 0000431136 and 0000552712.

**Sapporo** - ✅ **BUILT 2026-09-28** (28,674 storefronts, 95 stations, 7
lines; DECISIONS "Sapporo built", "Sapporo's brief corrected before the build"
and "Japanese station names"). The sheet as written before the build:

(`sapporo.md`; 10 wards, **EPSG:32654**).
- `ckan.pf-sapporo.jp` `shokuhin260331.csv` (25,163 rows; 24,257 fixed);
  personal services `sapporo_environmental_hygiene_services` (5,993; resource
  URLs to read at build). **Fetch from ckan.pf-sapporo.jp only.**
- Operator columns: 申請者名 (food); 開設者名 and **開設者住所, an operator's own
  address**, on 1,308 beauty rows - never select it.
- Join 84.7 / **15.2** / 0.2: on the 条 grid a chōme is about one block
  (~100 m), so the chōme tier is near block precision here. Sapporo's grid
  rules are already in `japan_register`.
- Rail passes: three subway lines and the streetcar wholly inside; JR Hokkaido
  cut at the line.
- Notice: 札幌市, both dataset titles and URLs, the CC BY 4.0 link, that it was
  processed; no endorsement, no logos, never "operating".

**Fukuoka** - ✅ **BUILT 2026-09-28** (30,062 storefronts, 71 stations, 9
lines; DECISIONS "Fukuoka steps 1-2" and "Fukuoka built"). What it left for
the cities after it: `FORM_RULES` (業態), `OWN_POINT_FALLBACK`, `SUPERSEDES`,
`ADDRESS_BY_CONSENT` and `SOURCE_AS_OF` (a per-source as-of in
`japan_fetch`); `OPERATOR_COLS` gained 営業者氏名 and 開設者法人名（開設者氏名）, now
REQUIRED_COLUMNS so a renamed column stops the build. Owner's calls: **yatai
(ろ店 / 定置屋台) count** - read what ろ店 means in Tokyo's MHLW rows before
trusting the rule there; **MHLW's rows cannot take the name rule** (no
operator column; accepted); MHLW's point for chōme-tier rows too. OSM had
TRANSLATED three station names (Kashii Shrine, Kushida Shrine, "Fukuoka
(Tenjin)"): read every name, not only the numerals. A city list can be
replaced under the same resource id (Fukuoka's, 2026-09-25): check
`package_show` against the brief. The sheet as written before the build:

(`fukuoka.md`; 7 wards, **EPSG:32652**) - ▶ the first TWO-SOURCE Japanese city.
- The city's own BODIK list (`…/r8.7.csv`, 3,977 rows: permits from before
  2021-06 only) PLUS MHLW's online filings (`i2fas.mhlw.go.jp/…/40130_food_business_all.csv`,
  40,390 live rows, 27,815 permits). They overlap 1.3%.
- ▶ `japan_step2` reads each source the same way; it needs a per-source
  fallback to **MHLW's own coordinates** where the join misses (median 36 m
  from the block point), and MHLW's notifications as a partial food-retail
  bucket (disclosed). BODIK answers 500/502/504: retry with backoff.
- About 79.5% of restaurants are placeable; the owner approved the disclosure.
- Operator columns: MHLW 法人名 / 法人住所 / phones; BODIK
  開設者法人名（開設者氏名） and phones. Some fields are masked ＊＊＊ at source.
  MHLW's FAQ lets a sole trader enter their own name as 屋号 - exactly what the
  name rule is for.
- Rail passes (subway 100%, Nishitetsu Kaizuka 9 of 10). ▶ **Leave out the
  JR Hakata-Minami line** (`LEFT_OUT_LINES`): only Hakata is inside.
- Notices: MHLW (PDL 1.0: source, processed, by whom; no completeness claim)
  and BODIK (CC BY 4.0: each dataset's 作成者, the resource name with its date,
  the URL). One minor MHLW point, 2)ウ, is open.

**Kyoto** - ✅ **BUILT 2026-09-28** (32,355 storefronts, 117 stations, 18
lines; DECISIONS "Kyoto steps 1-3" and "Kyoto built"). What it left for the
cities after it: `config.source_rows` (a source that is rows, not one file:
a rebuilt register, or a complete list plus its months - Tokyo's per-ward
files fit it), `japan_fetch.portal_file` (a portal's own download button,
magic bytes checked), the stream carrying the name rule's ANSWER rather than
the operator's name, and variation selectors stripped before the join.
Owner's calls: the funiculars left out (Kobe's rule now covers every city);
`as_of` = the last day the newest list covers, never the download date. Traps:
a branch whose junction is a long station needs `junction_m` (Kyoto's 350 m,
as Osaka's 大阪); list a branch's stations BEYOND the city line in its
`stations` too, or `excluded_stations.csv` files them under the parent line;
one interchange its operators READ differently (西院: Saiin / Sai) needs a tie.
The sheet as written before the build:

(`kyoto.md`; 11 wards, EPSG:32653) - ▶ a REBUILT register.
- `japan_register.kyoto_permit_stream(raw_dir, as_of)` rebuilds it from the
  2021 `.xls` and 62 monthly XLSX (82 files): 30,351 in term. **Pin `as_of`,
  never today.** It is an upper bound (closures are invisible) - the page says so.
- ▶ `japan_step2` reads files; Kyoto needs a SOURCES entry that yields the
  stream's rows, and the stream must carry `name_is_operator`'s answer (it
  drops the operator columns today, which would make the rule compare nothing).
- ▶ Fetch: no API - GET the resource page, then POST with the session cookie;
  check magic bytes, refuse HTML; `.xls` through xlrd. data.city.kyoto.lg.jp only.
- Join 92.7% block; rules A-D came from here (intersection prefixes, 祇/祗 and
  private-use codes, known-town fallback, twin towns left unplaced: 237 rows).
- Rail passes. ▶ Keihan Keishin keeps 3 of 7; **Kyoto's two funiculars are
  drawn** (its brief, decided before Kobe's call - re-ask if that looks
  inconsistent); the Sagano scenic line is left out.
- Open: same-address successors, the short-term filter, U+E0EE and 三条通大橋東.

**Tokyo** - 🔨 **BUILT on `worktree-japan` 2026-09-28, held for review time**
(63,989 storefronts, 490 stations of which 293 hollow, 52 lines; DECISIONS
"Tokyo step 2 on the roster" and "Tokyo's rail"). What it left for any big
Japanese network:
- **`route` on a LINES entry** (`japan_step1.route_sections`): a public
  SERVICE over parts of several N02 legal lines, stopping at listed stations -
  JR East's nine services over 山手線 / 東北線 / 東海道線 / 中央線 / 総武線 / 常磐線
  / 京葉線 / 赤羽線 (owner: drawn in full, overlapping). `"~名"` passes a station
  without stopping. N02's track can arrive in pieces; each hop picks the piece
  nearest both stations.
- **`GROUP_JOIN`**: a platform N02 grouped apart from its own station (Tokyo
  Station's Keiyō platforms, 424 m) joins it; different stations of one name
  stay apart. **`COLLAPSE_MAX_SPREAD_M`** is per city, citing the real
  interchanges over it (Tokyo 550: 新宿 546 m).
- **`SOURCE_KIND`** (`japan_step2.kind`): several sources of one kind (eight
  wards' food lists) - the key names the source, the kind is what the
  taxonomy reads.
- **Line codes as on-map labels** (`render_heatmap(legend_names=...)`, owner):
  52 full names do not fit (9 unplaceable at 1000 px; short names 59 overlaps at
  343 px); the operators' own codes (JY, G) place all 52 at every width, and the
  legend reads code and full name. Measure a big network's labels EARLY, in a
  scratch render at 343 px, before tuning ends.
- **`scripts/line_colour_search.py`**: the spatial colour search (>= 18 only
  within 500 m, >= 10 city-wide) - 52 lines placed, where the city-wide search
  topped out at Osaka's 34.
- **Station names in SIGNAGE style** for Tokyo (owner): OSM's spellings follow
  the operators' English signs (no macrons; Tokyo Metro's lowercase after a
  hyphen); ties in JR's title case; line and ward names without macrons too.
  The 丁目 figures rule still applies.
- **Credits built from config** (`pipeline/tokyo/credits.py`, notice 56;
  `check_provenance.py` L): one entry per file, each in its own ward's form.
- **The app imports the city's config** (the page reads `HEATMAP_HTML`): never
  run a data check at config import - the deployed app has no `data/`.

The sheet as written before the build:

**Tokyo (8 wards)** - ▶ **read the `tokyo-ward` skill** (2026-09-28): each ward
is its own source (`SOURCE_MUNICIPALITY`, `source_rows`, MHLW's slice under
`SUPERSEDES`), and `OFFICIAL_SHARES` measures each ward's share of the
official count every build (`pipeline/countries/japan_official.py`, the
yearbook and e-Stat readers, shared with `scripts/japan_ward_table.py`). The
shared step 2 read all eight food wards at 99.7% block on 2026-09-28 and
reproduced the brief's eight shares exactly. Wards without data get hollow
"no business data" stations (owner). The sheet as written before that:

(`tokyo.md`; EPSG:32654) - LAST, and not like the others.
- ▶ One file per ward, in five encodings and three formats (Chūō cp932 with
  `所在地_連結表記`; Shinjuku UTF-16, a 2023 snapshot; Taitō Shift_JIS, own
  format, addresses start at the town; Meguro quoted TSV; Shibuya: rows with an
  empty 廃業日 only). `permits_from_rows` handles each; the municipality is the
  WARD, so SOURCES needs a per-source municipality.
- ▶ MHLW's slice added to four wards, de-duplicated against the ward list.
- ⚠️ **The stub test FAILS**: 45% of urban station-line records are inside,
  11 of 19 lines under half; the Arakawa tram keeps 2 of 30, Nippori-Toneri 0
  of 13. The missing wards (Chiyoda first) are a planned project (PLAN).
- Each ward's share of the official count goes on the page (9% Kōtō to 101%
  Shibuya). Each non-catalogue ward needs its own credit; Shinjuku's 2026 PDF
  is NOT permitted.

## Recommending the next city

None in Band A: all six on the owner's order (Osaka → Kobe → Sapporo →
Fukuoka → Kyoto → Tokyo) are built (2026-09-28). The other Japanese cities
wait in their bands (`docs/japan_city_list.md`): Hiroshima food only and on
streetcars (T), Yokohama personal services only (N), Sendai the city's
permission (D). A Tokyo ward whose list turns up is the `tokyo-ward` skill.
