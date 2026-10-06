# Takatsuki — build brief

**Band B, food only (Kurume's shape), owner-approved 2026-10-06** (Japan wave
4, a pre-verdict converted in staging's wave 5, call 137:
`docs/decisions_drafts/staging.md`, "Wave 5, second half": "Tottori,
Yamagata, Yao, Takatsuki (food only)"). The Step 0 downloads were approved by
the owner 2026-10-06 (call 141). **Step 0 measured 2026-10-06** (staging).
Into `data/takatsuki/raw/` (gitignored), each from its publisher's own host
with the project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `i2fas.mhlw.go.jp`: `27207_food_business_all.csv` (**1,726,037 B**,
  the size approved), the only business source.
- From `nlftp.mlit.go.jp`: `isj/27207-24.0a.zip` (195,843 B) and
  `isj/27207-19.0b.zip` (10,694 B).

**1,932,574 B in all.** Nothing else was downloaded. Hankyu's and JR West's
station timetable pages were read by plain GET for frequency (pages, not data
files).

**Run `python scripts/brief_check.py takatsuki` before writing any code.**
Then the `japan-city` skill, **Kurume's shape** (`docs/build_briefs/kurume.md`:
MHLW's open data alone, food only, the fixed-premises measure) with Okayama's
and Hiroshima's food-only page; `docs/build_briefs/yao.md` is the same build
on the next city south. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Takatsuki entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; the Tōkaidō Shinkansen crosses the city with no station); (2)
**lines served only by limited expresses DO count** (2026-09-28); (3) **the
city line only**: only stations inside the city get rings, JR and the private
lines are cut at the line, **a one-station stub stays as cut** (2026-09-27);
an URBAN line cut to ONE station is left out, its station kept through the
other lines, and drawn cut only where no other line serves that station
(owner, 2026-10-06, calls 54 and 92; none here); (4) **菓子製造業 and
そうざい製造業 count, in Retail**, the factory share measured and kept
(2026-09-24, 2026-09-27); (5) **the name rule**, version 2 (2026-10-06):
法人名 is an operator column (2026-10-05) and a bare personal name is withheld
whatever it holds; (6) **no page says "currently operating"**. Also: no
frequency floor for JR or private lines in Japan (owner, 2026-10-06, call
46), any stretch at about 11 trains a day or fewer named and drawn (call 86;
none here); fault-based cost clauses accepted for all of Japan (2026-09-24);
English station names from OSM `name:en`; every Japanese city reads
`WAVE2_RULES` (owner, 2026-10-04); **市内一円 rows are not premises** (Kobe's
trap 6, 2026-09-27); MHLW's notifications as a partial Food-shops layer (call
127b, Kurume's and Okayama's Retail); a stated food share where a list is
incomplete (call 125).

**✅ Five station groups, Minoh's size (owner, 2026-10-06, the band row):**
JR 2, Hankyu 3. The owner banded it on that count; Minoh (5) is the
precedent, Mito (6) the next.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Osaka Prefecture**
after wave 4's retag. Its label offset comes from `check_macro_labels.py`
(PROBLEMS 0 at 375, 768 and 1200), never by eye: its dot sits between
Ibaraki's (west) and Hirakata's (south, across the Yodo), both briefed.

**✅ `mode`: `metro`** (the owner's rule of 2026-10-02): JR holds 2 of the 5
groups, Hankyu's Kyoto Line is a railway (N02 class 12); no subway, tram or
light rail. Kurume's and Minoh's precedent.

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム file for Takatsuki
(PDL 1.0, as recorded): 2,453 open restaurant permits, 89.3% of e-Stat's
2,747 in force.** 343 of the 1,916 "addressed" permits give only
`大阪府高槻市内一円` (自動車 and 露店 permits, not premises), so 1,573 carry a
real address; **on fixed premises 1,573 of 2,006 (78.4%) can be placed**,
Kurume's 79.6% the precedent; **57.3% of the in-force count**. Block join
**97.9%** of storefronts, MHLW's own point for the 0.9% left. Storefronts:
**Food service 1,117, Retail 1,035** (623 permits, 412 notifications).
**Rail: 5 station groups** (JR Kyoto Line 2, Hankyu Kyoto Line 3), all read
from the operators' own timetables: 6 to 18 trains an hour, 116 a day at the
fewest.

---

## Business leg — MHLW's open data, alone

| | MHLW open data (27207) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27207_food_business_all.csv`: **1,726,037 B, 4,501 rows** (届出 1,465, 許可 3,014, 許可(廃業) 16, 届出(廃業) 6). UTF-8 with BOM, CRLF, the national schema |
| As of / cadence | Permits **2021-06-04 to 2026-08-31**; closures dated 2026-08-01 .. 08-21 (the file keeps a closed row for its last month only). Monthly (MHLW). Pin `as_of` to **2026-08-31** |
| Columns | as Yao's and Kurume's: **営業施設名称、屋号又は商号**, **営業の種類**, **業態**, **営業施設所在地**, 営業施設方書, **緯度 / 経度**, **法人名**, 法人番号, 法人住所, phones, permit dates, **廃業年月日**, **申請区分**, 許可条件, 備考 (25 columns) |
| Shared code | reads every column already |

**Takatsuki licenses its own food premises** (a core city since 2003; MHLW's
file is keyed 27207). The city publishes no food list: its open data is on
BODIK (organisation `272078`, 28 datasets, CC BY 4.0), none a permit list (a
search of the organisation for 営業許可, 理容, 美容, クリーニング and 食品衛生
returns 0); the city's own open-data page (`/soshiki/8/1319.html`) points
there (staging's probe; the master list's row).

### Counts that matter

Open restaurant permits: 許可, 飲食店営業, no 廃業年月日, 許可満了日 on or after
2026-08-31 (none listed has expired).

- **2,453 open 飲食店営業 permits = 89.3% of e-Stat's FY2024 in force
  (2,747: old law 926, revised 1,821).** By grant year: 2021 208 · 2022 470
  · 2023 518 · 2024 422 · 2025 442 · 2026 393. Every 初回許可年月日 is on or
  after 2021-06-01; terms run 5 years (448) or 6 (2,005).
- **Old-law coverage (Kurashiki's trap): absent, as in every MHLW file.**
  The 294 missing are the old law's permits still in term, which renew into
  MHLW as they expire. Permits granted by 2025-03-31 still open: **1,727 =
  94.8%** of e-Stat's 1,821 revised-law restaurants at that date.
- 🔎 **Addresses.** 1,916 of 2,453 (78.1%) carry a non-blank 営業施設所在地.
  **343 read only `大阪府高槻市内一円`** (one spelling on every restaurant row):
  業態 自動車 (types I to III, 連合 included) 199, 露店 144; they share 2
  points. **A real address: 1,573, 64.1% of all open restaurant permits.**
- **On fixed premises** (Kurume's measure: every citywide row and every
  vehicle or stall 業態 set aside, `FORM_RULES`' temporary/mobile words:
  自動車 261, 露店 186, of which 104 unaddressed): **1,573 of 2,006, 78.4%**,
  above the reduced-bucket bar's 70%. 業態 is published on every fixed,
  unaddressed permit (433; 許可条件 on 432 names no vehicle or stall), so the
  split is measured. The 433 withheld: 軽食・喫茶 85, 居酒屋 66, 委託給食 46,
  バー 40, スナック 25, 和食店 21 … Bars, snacks and stands withhold a little
  more (76.0% addressed against 78.8%). 1,570 distinct (address, trade name)
  pairs.
- **Of the in-force count: 1,573 fixed, addressed permits = 57.3% of
  e-Stat's 2,747** (stated on the page, call 125).
- **Through `japan_eigyo`** (every open row, step 2's order; 4,479 rows):
  **not a premises 1,730** (blank address 1,329, 一円 401), institutional
  catering 271 (委託給食 by 業態 96), no rule 128 (manufacturing), hostess
  venues by 業態 76, vending 60, entertainment by 業態 27, 仕出し 18,
  accommodation 8, temporary 4. **Storefronts: Food service 1,117, Retail
  1,035** (permits 623, **notifications 412**, a partial opt-in bucket as in
  Kurume, Fukuoka and Okayama). **223 permits filed 業態 そうざい店頭販売**
  (a deli counter) go to Retail by the owner's deli rule (2026-10-04; 216 of
  them open storefronts), the main reason Food service sits
  well under the fixed count. By rule across both: deli 216, 菓子 187, other
  food sales 136, konbini 162, butchers 85, supermarkets 58, fishmongers 45 …
- **Closed premises**: MHLW keeps a closed row for the last month only
  (許可(廃業) 16, all restaurants, August 2026). **Repeats**: 8 extra rows in
  8 (address, trade name, type) groups among open addressed rows; one pin per
  premises (trap 7) takes them.
- ⚠️ **One citywide spelling the shared test misses**: a single row reads
  `大阪府高槻市全域`; `permits_from_rows` tests 一円, not 全域 (Aomori's brief
  proposes adding 全域; the same change covers it).
- ⚠️ **Economic Census control** (`scripts/japan_census_control.py` at
  build): the 2021 census counts **963** 飲食店 establishments in 27207; 1,116
  distinct placed Food-service premises is **1.16 per establishment**, below
  the built cities' 1.56-1.92 and Kurume's 1.37: 89% of permits, a fifth of
  fixed addresses withheld, and the deli counters moved to Retail. Report it
  with that reason.

### Personal services: none published

The city's 理容所の開設 page (`/soshiki/39/2777.html`, ページID 002777,
更新日 2024-09-26) carries the procedure and a form (PDF), no list; nothing on
BODIK (above). **A food-only page**, Kurume's and Hiroshima's precedent:
"**This map shows food businesses only.**"

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27207-24.0a.zip` (195,843 B,
**11,404 block keys**), town-chōme `.../19.0b/27207-19.0b.zip` (10,694 B,
**379**). `japan.CITIES` entry at build: `"takatsuki": {"name": "高槻市",
"pref": "27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["27207"]}`.

| Tier (storefronts, `WAVE2_RULES`) | All (2,152) | Food service (1,117) | Retail permits (623) | Notifications (412) |
|---|---|---|---|---|
| Block | **97.9%** | 98.5% | 97.8% | 96.6% |
| Town-chōme | 1.2% | 0.7% | 1.3% | 2.4% |
| Unplaced | 0.9% (19) | 0.8% | 1.0% | 1.0% |
| **Block, chōme or MHLW's own point** (`OWN_POINT_FALLBACK`) | **100%** | | | |

- **Independent check**: MHLW's own coordinates against the block point,
  **median 30 m, 99.0% within 250 m** (2,107 rows; 6 over 1 km).
- **The misses, read** (towns only): **16 of the 19 unplaced write 小字 in
  the address** (田能小字的谷 4, 中畑小字久保条 3, 田能小字中山 2, 出灰小字二の瀬 2 …,
  the northern hill villages), where MLIT keys the same places as
  `田能字的谷` (the shared Sendai key, 大字 + 字 + 小字). Others: 二料久野ケ谷,
  緑町3丁目, and one address with the prefecture and city written twice.
  Chōme tier: 上牧南駅前町 11, 白梅町 3 … (地番 the block file does not key).
- ⚠️ **Shared code proposed: read 小字 as 字 in the address** before the town
  parse. Measured in a scratch rewrite: unplaced **19 → 3** (block +6,
  town-chōme +10). Re-run the Minato control (`screen_japan_join.py minato`)
  and every city screen after it. MHLW's own point places all 19 meanwhile.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip`, N03 code
27207 (**105.2 km²**, extent W 135.557, S 34.781, E 135.673, N 34.977; the
northern two thirds are forested hills to the Kyoto border, every station in
the south).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 東海道線 (西日本旅客鉄道, 11) | JR Kyoto Line (JR京都線) | **2 / 59** | 摂津富田, 高槻 |
| 京都線 (阪急電鉄, 12) | Hankyu Kyoto Line | **3 / 27** | 富田, 高槻市, 上牧 |

- **5 station records, 5 `N02_005g` groups.** No name in two groups. **Two
  close pairs, kept apart as N02 keeps them** (trap 1; Tsu's 川合高岡 and 一志
  precedent): **摂津富田 (JR) and 富田 (Hankyu) 285 m**, **高槻 (JR) and
  高槻市 (Hankyu) 574 m**, separate stations of different names on different
  operators. **Median nearest-group gap 574 m** (285 to 4,300; 上牧 alone in
  the northeast), above the station gate's 400 m floor; ring size by the
  spacing rule at build (the tram kit's 0.3 mi outer ring applies at about
  550 m or less, so Takatsuki sits just above it: read the build's own
  computation).
- **Shinkansen**: the Tōkaidō Shinkansen runs through the city with no
  station; nothing to drop.
- **Cut at the line** (named by N03 municipality at build): JR 57 beyond
  (大阪市 10, 吹田市 2, 茨木市 2, 摂津市 1, 島本町 1, Kyoto and beyond 41); Hankyu
  24 (大阪市 6, 茨木市 3, 吹田市 1, 摂津市 1, 島本町 1, Kyoto 12). Near the line
  but outside: Hankyu's 総持寺 (Ibaraki, 131 m), Keihan's 枚方公園 (289 m) and
  樟葉 (499 m) across the Yodo (not drawn here; Hirakata's page). Inside but
  near: 上牧 125 m from the line.
- **The stub test passes**: JR keeps 2, Hankyu 3; no urban line.
- **The light-rail/rail test**: both railways (N02 class 11 and 12). No tram,
  light rail or subway.
- **Frequency, READ 2026-10-06** (weekday departures; counts only, never a
  timetable on the page): Hankyu from its own station pages
  (`www.hankyu.co.jp/station/html/HK-7x_ky_<d>_w.html`, the j5 probe's
  method), JR West from the wave-5 probe's cached
  `timetable.jr-odekake.net/station-timetable/<id>` pages, re-counted here:

  | Station (line, direction) | All day | 10:00-15:59 |
  |---|---|---|
  | 高槻 (JR, to 大阪; `2789011002`) | 301 | **16 an hour** (8 locals, 新快速, 快速) |
  | 摂津富田 (JR, to 大阪; `2790011002`) | 150 | **8** (locals) |
  | 富田 (Hankyu HK-71, to 大阪梅田 / 京都河原町) | 124 / 118 | **6** (locals) |
  | 高槻市 (Hankyu HK-72, to 大阪梅田 / 京都河原町) | 298 / 222 | **17.8 / 12** (特急, 準急, locals from here) |
  | 上牧 (Hankyu HK-73, both ways) | 118 / 116 | **6** (準急) |

  **No stretch is at or under about 11 trains a day** (call 86).
- ⚠️ **Gate 3** at build: JR West's and Hankyu's station counts inside the
  city (2 and 3). **OSM `name:en`** for 5 groups (one Overpass query at
  build; not queried here).

## Scope

**Takatsuki City (27207).** JR and Hankyu run on to Osaka and Kyoto; cut at
the line.

## Licences — MHLW as recorded

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` (read 2026-10-02 for Okayama and Kurume; no new
  read). **MUST DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy.
- The city's BODIK datasets (CC BY 4.0) are not used.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources. **Operators' timetables**: counts only.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- MHLW's file carries **法人名, 法人番号, 法人住所 and 営業施設電話番号**: never
  selected into an output. 法人名 is read IN MEMORY for the name rule only.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): 法人名 filled on **1,438 of 2,152** storefront rows, a company marker
  on 1,157, **none on 281**; **0** rows whose trade name is the operator's own
  name, **0** bare personal names.
- Run `check_personal_exposure.py takatsuki` (`japan=True`) after step 2; it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag), `label_tier:
"minor"`, `"country": "Japan"`. The city runs 135.557-135.673 E, centroid
135.608: project to **UTM 53N (EPSG:32653)**. OSM box from the N03 extent,
rounded out: (34.78, 135.55, 34.98, 135.68).

**Scaffold**: `scaffold_city.py --slug takatsuki --name Takatsuki
--system-name "JR West and Hankyu" --taxonomy japan_eigyo --lat 34.851 --lon
135.618 --region "Japan West" --country Japan --mode metro --page-number <N>`
(`--dry-run` first; the point is the stations', not the N03 centroid in the
hills), the number claimed in `docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** Band B, food only, Kurume's shape, five station
groups (call 137); the downloads (call 141); the standing Japanese calls;
`mode: metro`; the minor tier, Japan West now and Osaka Prefecture after the
retag; no frequency floor (call 46); MHLW's notifications as partial Retail
(call 127b); the food share stated (call 125); MHLW's own point where the
join misses (call 127c).

**Open:** none for the owner. The fixed-premises share (78.4%) clears the
70% bar. Two shared-code proposals go to the build (小字 as 字; 全域 as not a
premises), each with the Minato control.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control, `screen_japan_join.py
  minato`, and every city screen): 小字 read as 字 (19 → 3 unplaced);
  **全域** in `permits_from_rows`' not-a-premises test (one row here; Aomori's
  1,284).
- `config.source_rows`: MHLW's file alone; `as_of` pinned to **2026-08-31**,
  never today. Expect about 1,117 Food-service and 1,035 Retail storefronts.
- **Placement disclosure** (Hiroshima's and Kurume's wording): about one fixed
  restaurant in five withholds its address (21.6%); the page states the food
  share against the in-force count (57.3%, call 125).
- The Economic Census control (1.16, below the built range, with the reason);
  the factory share; gate 3; OSM `name:en`; line colours on both basemaps;
  **the opening view** (`map-view`: the north is empty hills, so the fit must
  take the stations, not the N03 extent); `check_provenance.py`;
  `check_scope_disclosure.py`.
- The page's businesses bullet and What Is Excluded: food only, no personal
  services list, old-law permits and withheld addresses missing.

```brief-checks
[
  {
    "id": "takatsuki-mhlw-live",
    "claim": "MHLW's open-data file for Takatsuki (27207) answers a plain keyless GET (1,726,037 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27207_food_business_all.csv",
    "min_bytes": 1500000
  },
  {
    "id": "takatsuki-isj-block-live",
    "claim": "MLIT's block-level address file for Takatsuki (27207) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27207-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "takatsuki-isj-chome-live",
    "claim": "MLIT's town-chome file for Takatsuki (27207) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27207-19.0b.zip",
    "min_bytes": 8000
  },
  {
    "id": "takatsuki-bodik-no-permit-lists",
    "claim": "The city's BODIK organisation (272078) holds no food, barber, beauty or laundry list: a search for 営業許可, 理容, 美容, クリーニング and 食品衛生 returns 0 (one BODIK call)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:272078&q=%E5%96%B6%E6%A5%AD%E8%A8%B1%E5%8F%AF%20OR%20%E7%90%86%E5%AE%B9%20OR%20%E7%BE%8E%E5%AE%B9%20OR%20%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0%20OR%20%E9%A3%9F%E5%93%81%E8%A1%9B%E7%94%9F&rows=0",
    "present": ["\"count\": 0", "\"success\": true"]
  },
  {
    "id": "takatsuki-hankyu-timetable",
    "claim": "Hankyu's weekday timetable page for 高槻市 (HK-72, Kyoto Line, toward 大阪梅田) answers with departure links - a frequency source",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/html/HK-72_ky_1_w.html?no_redirect",
    "present": ["HK-72", "TM="]
  },
  {
    "id": "takatsuki-jr-timetable",
    "claim": "JR West's timetable index for 高槻 (EID 0610122) links the JR Kyoto Line's two weekday pages (2789011001, 2789011002)",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0610122",
    "present": ["2789011001", "2789011002"]
  },
  {
    "id": "takatsuki-projected-crs",
    "claim": "Takatsuki projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.608,
    "expect": "EPSG:32653"
  }
]
```
