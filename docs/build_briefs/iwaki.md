# Iwaki — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 81: `docs/decisions_drafts/staging.md`, "Wave 5"). The Step 0
downloads were approved by the owner 2026-10-06 (call 106). **Step 0 measured
2026-10-06** (staging). Into `data/iwaki/raw/` (gitignored), each from its
publisher's own host with the project user-agent, each HTTP 200, under each
URL's own file name as `japan_fetch.get` saves:

- From `www.city.iwaki.lg.jp` (保健所 生活衛生課): the full food list
  `Shokuhin_itiran_R08.csv` (1,032,586 B) and the 29 monthly new-permit CSVs
  on the same page, `Shokuhin_itiran_R0604.csv` … `Shokuhin_itiran_R0808.csv`
  (April 2024 to August 2026, 145,779 B together); the barber and beauty list
  `ribiyoujo_ichiran.csv` (150,938 B) and its four monthly CSVs
  `ribiyoujo_R8.6.csv` … `ribiyoujo_R8.9.csv` (2,809 B).
- From `i2fas.mhlw.go.jp`: `07204_food_business_all.csv` (205,488 B), a
  control.
- From `nlftp.mlit.go.jp`: `isj/07204-24.0a.zip` (516,446 B) and
  `isj/07204-19.0b.zip` (11,198 B).

**2,065,244 B in all, 38 files.** Nothing else was downloaded (not the XLS
twins, not the FY2024 full list `Shokuhin_itiran_R07.csv`). **No laundry list
exists** on the city's open-data pages (disclosed, see Scope).

**Run `python scripts/brief_check.py iwaki` before writing any code.** Then
the `japan-city` skill, **Fukuyama's shape** (a city's own full food list plus
the months since, `rebuilt_register`; `docs/build_briefs/fukuyama.md`) with
**Ichinomiya's merge** (the full list kept whole plus the months, owner
2026-10-06, call 126; `docs/build_briefs/ichinomiya.md`), Hamamatsu's for the
register. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Iwaki entry; its table is shared code
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, read from the
cached zips with a scratch script.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Iwaki
carries `label_tier: "minor"` and goes in the **Japan East** view; wave 4's
first city to land retags Japan into the eight regions, Iwaki into
**Tohoku**. Its label offset comes from `check_macro_labels.py` (PROBLEMS 0
at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 ("unless there is
substantial JR, JR reads as metro"): JR East has all 14 station groups inside
the city line; no subway, tram or private line. Fukuyama's, Okayama's and
Kitakyushu's precedent.

---

## The one-line summary

**Food and personal services from the city's own CSVs (CC BY 4.0 as stated;
the licence read is pending, staging records it); no laundry list.** The food
list of permits in term on 2026-03-31 holds **4,375 rows, 3,393 restaurants
(飲食店営業), 99.1% of e-Stat's 3,425 in force**, old-law permits included
(614 rows, granted 2019-07 to 2021-05: not Kurashiki's trap). The monthly
files publish NEW permits only (183 against the full list's 473 grants in
the same eight months), so the full list is kept whole and the months added
(open call 1): **4,382 permits, 3,409 restaurants (99.5%)**. Barbers 382 and
beauty salons 794 to 2026-09-30, **97.9% and 99.6% of official**. MHLW holds
only 43 of the city's permits (cover 0.01): a coordinate control, not a
closure filter. Block join **78.6%** (food), **90.1% block or 小字 centroid**
with a rule the build adds (measured against MHLW's own points: median 164 m
against 1,479 m today). **Rail: 14 station groups** (JR Jōban 10, JR Ban'etsu
East 5, いわき shared), read from JR East's own timetables: the Ban'etsu East
Line carries **6 to 8 trains a day** each way, drawn and named (call 86).

---

## Business leg — the city's 保健所 lists

Host `https://www.city.iwaki.lg.jp` (the city's own CMS; no catalogue API).
Every file is a plain GET under `/www/contents/<page id>/simple/`.

### Food: 食品営業許可施設, page `/www/contents/1652661537484/index.html`

| File | Bytes | Rows | What it is |
|---|---|---|---|
| `Shokuhin_itiran_R08.csv` 全営業許可施設一覧 令和７年度末時点 | **1,032,586** | **4,375** | permits in term on 2026-03-31; yearly (the FY2024 edition `…_R07.csv` sits beside it, not fetched) |
| `Shokuhin_itiran_R0604.csv` … `R0803.csv` (2024-04 … 2026-03) | 116,458 | 636 | each month's NEW permits; already in the full list (see below), left out |
| `Shokuhin_itiran_R0804.csv` … `R0808.csv` (2026-04 … 08) | 29,321 | 122 (110 restaurants) | the months since; the page says 「令和８年8月31日現在」, registered 2026-09-09 |

- **Encoding**: the full list and the 2025-26 months UTF-8 with BOM; the
  2024 months cp932 with no BOM (`city_rows` reads both). Header on line 1.
  Dates ISO with slashes (`2026/03/31`).
- **One schema throughout** (all 30 files): No, **営業所名称**, **営業所所在地**,
  営業所所在地気付 (the building), 営業所電話番号, **営業者氏名**, **代表者氏名（法人）**,
  **営業者住所**, 営業者住所気付, 営業者電話番号, **業種**, **種目**, 従たる種目1-6,
  **許可番号**, **許可年月日**, **許可満了年月日**.
- **種目** is the sub-type, and it carries the form: バー・スナック等 636,
  blank 598, 一般食堂・レストラン 468, 軽食店 397, 酒場 292, 菓子 239, 自動車による営業
  168, 露店営業（祭礼・催事等に限る。） 147, 給食食堂 141, 料理店 139, 旅館・ホテル 110 …
  (full list). `WAVE2_RULES`' `form_cols` reads it as the form (`FORM_COLS`
  holds 種目), so vehicles, stalls, school kitchens and hotel restaurants
  leave through `FORM_RULES`.
- **318 rows have no premises address**: vehicles 169 and stalls 149, all
  marked so in 種目; `mobile` takes them.
- **The page's note**: some items are withheld where an operator asked
  (「営業者からの申し出があった場合に、一部の項目が掲載されていない施設があります」):
  28 full-list rows have no trade name. The page says nothing about closed
  premises.
- **許可番号 is not unique**: a five-digit number reused across years (1,318
  distinct among 4,375 rows); (許可番号, 許可年月日) is unique but for one row.
  Never key on the number alone.

**Against `japan_register`'s tuples (shared code, not edited here):** every
column is already read (`ADDR_COLS` 営業所所在地, `NAME_COLS` 営業所名称,
`TYPE_COLS` 業種, `FORM_COLS` 種目 under `form_cols`, `OPERATOR_COLS`
営業者氏名) except **代表者氏名（法人）**, which `OPERATOR_COLS` lacks (it holds
代表者氏名（法人のみ）). `rebuilt_register` takes `end_col="許可満了年月日"`,
`granted_col="許可年月日"` (not its defaults).

### Old law, duplicates and closed premises

- **The full list carries every old-law permit still in term** (Kurashiki's
  trap is absent): 614 rows (464 restaurants) granted 2019-07-17 to
  2021-05-31, ending 2026 (328), 2027 (262) and 2028 (24), on 5- to 7-year
  terms. e-Stat counted 970 old-law restaurants on 2025-03-31; those ending
  in FY2025 have left the list or renewed under the revised law. Old-law
  types appear (喫茶店営業 12, 缶詰又は瓶詰食品製造業 2).
- **Only permits in term on its date**: every 許可満了年月日 is on or after
  2026-05-31. 198 rows (134 restaurants) end before 2026-08-31.
- **Repeats**: 98 rows repeat an (address, trade name, type) in 47 groups;
  3,616 distinct (address, trade name) premises. One pin per premises (trap
  7) takes them.
- **The monthly files are new permits, not renewals**: the full list holds
  473 permits granted 2025-08 to 2026-03, the monthly files 183 for those
  months. Of the 122 rows of 2026-04 to 08, only 9 sit at a full-list
  premises of the same type and none matches a full-list (number, grant
  date).
- **The full list appears to drop closed premises at each edition**
  (inferred, not stated): it holds 181 of the 183 permits the months list
  for 2025-08 to 2026-03 by (number, grant date), and 429 of 453 for 2024-04
  to 2025-07 by (dates, type). The 2024-04 to 2025-07 files number permits in
  another series (0 of 453 match by number), so that read uses dates.
- **Closures since 2026-03-31 are invisible**: no closure file, no status
  column, and MHLW cannot test them (43 permits, below).

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 福島県いわき市, 飲食店営業
in force 2025-03-31: **3,425** (old law 970, revised 2,455).

| | Restaurants (飲食店営業) | Share of 3,425 |
|---|---|---|
| Full list, 2026-03-31 | **3,393** | 99.1% |
| (a) Full list whole plus the months to 2026-08-31 (open call 1) | **3,409** | 99.5% |
| (b) Fukuyama's: in term on 2026-08-31 | 3,281 | 95.8% |
| MHLW's open restaurant permits (control) | 37 | 1.1% |

Through `japan_eigyo` (merge (a), `WAVE2_RULES`): **Food service 1,998,
Retail 756**, out 1,628. Restaurant permits out by rule: **the hostess rule
719** (種目 バー・スナック等 and スナック), temporary or mobile 279,
institutional catering 146, inside accommodation 140, 仕出し 61; the rest of
the out rows are manufacturing types. **Economic Census control**
(`scripts/japan_census_control.py` at build): the 2021 census counts **1,226**
飲食店 establishments in 07204; 1,885 distinct placed Food-service premises
is **1.54 per establishment**, just under the built cities' 1.56-1.92,
because the hostess rule takes a fifth of the restaurant permits.
Factory proxy: 39 of 756 Retail trade names contain 工場 or センター (5.2%,
Kobe's 4.9%); step 2 measures it properly.

### MHLW's file (07204), the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=07204_food_business_all.csv`:
**205,488 B, 636 rows** (届出 593, 許可 43, no closed rows), UTF-8 with BOM,
the national schema; latest grant 2026-07-17. The coverage sweep's cover is
**0.01** (`docs/coverage_sweep/japan_universe_mhlw.csv`): Iwaki files its
permits in its own system.

- **Its 43 permits are all city permits**: the digits of each 許可番号
  (`いわき市指令第NNNNN号`) are a city number, and 42 of 43 also match the grant
  date. It adds no premises.
- **Its own coordinates**: block point against MHLW's point, **median 65 m,
  89.9% within 250 m** (168 rows; 11 over 1 km). Its addressed rows join
  60.9 / 26.4 / 12.7 (block / chōme / none), worse than the city's.
- **593 notifications, 240 addressed**: by type Retail 194 (164 addressed:
  その他の食料・飲料販売業 102, 百貨店・総合スーパー 38, コンビニ 10, 米穀 6, 野菜果物 5,
  包装食肉 3); the rest cup vending and other vending (out). Open call 2.
- **No closure filter is possible** (Fukuyama's needs MHLW to hold the city's
  permits).

### Personal services: 理容所・美容所, page `/www/contents/1780984436063/index.html`

| File | Bytes | Rows | Kinds |
|---|---|---|---|
| `ribiyoujo_ichiran.csv` 全施設一覧 令和８年５月末時点 | **150,938** | **1,165** | 美容所 785 · 理容所 378 · （移動）美容所 1 · （移動）理容所 1 |
| `ribiyoujo_R8.6.csv` … `R8.9.csv` 月別新規施設 (2026-06 … 09) | 2,809 | 13 | 美容所 9 · 理容所 4; none in the full list |

- **As of 2026-05-31** (「令和８年５月31日現在」), the months to 2026-09-30
  (「令和８年６月分から毎月追加していきます」). The full list is cp932 (it starts
  with №), the months UTF-8 with BOM. Columns: №, **名称**, 郵便番号,
  **所在地**, 方書（所在地）, 電話番号, **種別**, **開設者**, **代表者氏名（法人のみ）**,
  **開設者住所（法人のみ）**, 方書（開設者住所）, 検査確認番号, 検査確認年月日, 備考
  (empty).
- **A standing register**: 検査確認年月日 runs 1956 to 2026 (1950s 2, 1960s
  28 … 2020s 208). No closure note, no status column, no control.
- **Official** (e-Stat FY2024 第10表, `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv`):
  barbers 390, beauty salons 797. **Shares 97.9% and 99.6%** with the months
  (382, 794); 96.9% and 98.5% on the full list alone.
- 1,158 distinct 検査確認番号 of 1,165; 23 premises listed as both 理容所 and
  美容所 (46 rows, no repeat within a kind): one pin per premises and bucket.
  The two （移動） rows leave by `japan_eigyo`'s mobile-salon rule. **One row
  is addressed in 福島市**, outside the city: drop it.
- **Shared code**: every column is read (`NAME_COLS` 名称, `ADDR_COLS` 所在地,
  `TYPE_COLS` 種別, `OPERATOR_COLS` 開設者 and 代表者氏名（法人のみ）). One file
  holds both kinds: a `source_rows` split by 種別 so `japan_eigyo`'s source
  decides each row (Fukuyama's).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/07204-24.0a.zip` (516,446 B,
73,762 rows, **86,888 block keys** with the Sendai 小字 keys), town-chōme
`.../19.0b/07204-19.0b.zip` (11,198 B, **375**). `japan.CITIES` entry at
build: `"iwaki": {"name": "いわき市", "pref": "07", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["07204"]}`.

| Tier (merge (a), fixed premises in a bucket) | All (2,754) |
|---|---|
| Block | **78.6%** |
| Town-chōme / 大字 centroid | 15.8% (361 at a 大字 centroid) |
| Unplaced | **5.6%** |
| **Block or 小字 centroid** (the rule below) | **90.1%**, chōme 8.3%, unplaced 1.6% |

| Registers | Barbers (382) | Beauty (794) |
|---|---|---|
| Block / chōme / unplaced | 78.0 / 13.9 / 8.1 | 79.3 / 14.1 / 6.5 |
| Block or 小字 centroid (both) | 89.3%, unplaced 1.8% | |

**The misses, read** (towns only, by `misses*.py` in the scratchpad):
- **Iwaki's addresses are 字 addresses** (平字田町, 小名浜字辰巳町): MLIT keys
  them as 大字 平 plus 小字 田町, and the Sendai key already joins them (on the
  in-term register, 1,203 of the 1,539 fixed rows with a 字 hit a block). **MLIT lists only some
  地番 of each 小字** (in 平's 小字 a median of 74% of the numbers up to the
  highest): 平字南町 has 2 numbers in MLIT, 30 rows miss; 小名浜字辰巳町 44, 54
  rows miss. A miss falls to the **大字's centroid** (`oaza`), for 平 or
  小名浜 a whole district.
- **Unplaced (154)**: mostly a 小字 written without 字 (常磐藤原町蕨平 27,
  平六町目 12, 錦町上中田 10, 常磐上湯長谷町釜ノ前 8 …) whose number MLIT lacks;
  rule C tries the 小字 key, misses, and leaves the row unplaced.
- **A 小字-centroid tier** (the mean of MLIT's points in the row's 小字, with
  字 inserted where the address omits it): 205 chōme-tier rows and 110
  unplaced rows name a 小字 MLIT has points for. Against MHLW's own points
  (77 rows off the block tier): **the 小字 centroid lies a median 164 m from
  MHLW's point (75 within 500 m); the 大字 centroid those rows take today,
  1,479 m.** A shared opt-in rule, measurable, so the build adopts it on this
  control (and the Minato control, `screen_japan_join.py minato`, after the
  change); it is not an owner call.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_07_GML.zip`, N03 code
07204 (**1,230.9 km²**, extent W 140.566, S 36.856, E 141.009, N 37.320). Read with a scratch `rail.py` (stations
within the polygon, Shinkansen operator class out).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside, south to north / east to west |
|---|---|---|---|
| 常磐線 (東日本旅客鉄道, 11) | JR Jōban Line | **10 / 81** | 勿来, 植田, 泉, 湯本, 内郷, いわき, 草野, 四ツ倉, 久ノ浜, 末続 |
| 磐越東線 (東日本旅客鉄道, 11) | JR Ban'etsu East Line | **5 / 16** | いわき, 赤井, 小川郷, 江田, 川前 |

- **15 station records, 14 N02_005g groups** (いわき shared, spread 0 m). No
  name in two groups; no pair under 600 m. **Median nearest-station gap
  4,181 m** (3,255 to 7,369): standard rings by the spacing rule.
- **Shinkansen**: none in the city.
- **Cut at the line** (named by N03 municipality at build): Jōban 71 beyond
  (53 outside Fukushima Prefecture; north through 広野町, 楢葉町, 富岡町, 大熊町 to
  南相馬市 and 新地町), Ban'etsu East 11 (田村市 6, 郡山市 2, 小野町 2, 三春町 1).
- **The light-rail/rail test**: both heavy rail (N02 class 11, JR
  conventional). No tram, light rail or urban line.
- **The stub test passes**: neither line is cut to one station.
- **Frequency, read 2026-10-06 from JR East's own station timetables** by
  plain GET (`timetables.jreast.co.jp/timetable/list<code>.html` and its
  weekday pages, the 2610 edition):

  | Station (line, direction) | Weekday departures | 10:00-15:59 / largest gap 09-17 |
  |---|---|---|
  | いわき (Jōban, to 水戸) | 39 | 12 / 49 min |
  | いわき (Jōban, to 原ノ町) | 20 | 6 / 93 min |
  | 勿来 (Jōban, each way) | 32 | 9 / 60-62 min |
  | 久ノ浜 (Jōban, to 原ノ町 / いわき) | 16 / 17 | 4 / 98-100 min |
  | 末続 (Jōban, each way) | 16 | 4 / 98-100 min |
  | いわき (Ban'etsu East, to 郡山) | **8** | 2 / 138 min |
  | 小川郷 (Ban'etsu East, to 郡山 / いわき) | **6 / 8** | 2 and 1 / 138-324 min |
  | 川前 (Ban'etsu East, each way) | **6** | 1 / 296-324 min |

  **Named under call 86: the Ban'etsu East Line inside the city (いわき to
  川前, 4 stations of its own) runs 6 to 8 trains a day each way; it is drawn,
  not left out.** The Jōban north of いわき runs 16 to 20 a day (about every
  90 minutes midday), the south 32 to 39: nothing else near 11. The master
  list's "every 30-60 minutes" holds for the south only. Only these counts
  are recorded, never a timetable on the page (JR East's terms were not
  read).
- ⚠️ **Gate 3** at build: JR East's per-line station counts. **OSM
  `name:en`** for 14 groups (one Overpass query at build; not queried here).

## Scope

**Iwaki City.** The Jōban Line runs on to 水戸 and to 南相馬 and 仙台, the
Ban'etsu East Line to 郡山; cut at the line. **No laundry list is published**
(e-Stat counts 140 laundries): Personal services is barbers and beauty salons
only, said on the page and in `docs/excluded_categories.md` (a sentence no
template covers is a proposal in the drafts file).

## Licences — as stated; the read is pending (`licence-read`, staging records it)

**As stated on each dataset page**, both linking
`http://creativecommons.org/licenses/by/4.0/deed.ja`: the food page says
「このデータはクリエイティブコモンズ表示4.0日本ライセンスの下に提供されています。」 and the
barber and beauty page 「…表示4.0国際ライセンス…」. **CC BY 4.0 has no Japan
port**: the food page's 「日本」 is for the licence read to settle. Both add
that the data may be used and modified freely, that the city does not
guarantee completeness, and that it accepts no liability for damage from use.
The full read runs separately and is **pending**; staging records its verdict
and the credit wording, not this brief.

- **MHLW open data** (if any of open call 2 is taken): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`, its 出典 line and who processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR East's timetables**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food lists carry the operator block**: **営業者氏名** (a sole trader's
  own name on 2,175 of 4,375 full-list rows by the absence of a company
  marker; 442 of 758 monthly rows), **代表者氏名（法人）**, **営業者住所** /
  営業者住所気付 / 営業者電話番号 (the operator's own address and phone) and
  営業所電話番号. Step 2 never reads any of them into an output; 営業者氏名 and
  代表者氏名（法人） are read IN MEMORY for the name rule only (add the second
  to `OPERATOR_COLS`).
- **The register carries 開設者** (no company marker on 1,002 of 1,165 rows),
  代表者氏名（法人のみ）, 開設者住所（法人のみ） and 電話番号. Select 名称, 所在地 and
  種別 only.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): full list **9** rows whose trade name is the operator's own name
  (11 with 代表者氏名（法人） compared too; 1 bare personal name among them);
  months 2; merge (a) 9, **1 of them in a bucket**; register **0** (0 bare);
  MHLW's 法人名 0. No value was printed or stored.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected.
- Run `check_personal_exposure.py iwaki` (`japan=True`) after step 2: the
  rows that matter are the sole traders' trade names; it must print 0.
  Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Tohoku after the retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 54N (EPSG:32654)**: the N03 centroid
lies at longitude 140.786, the extent 140.566 to 141.009, all inside the
138-144 band (computed here, never copied). OSM box from the N03 extent,
rounded out: (36.85, 140.56, 37.33, 141.01). The city is large and its
stations lie along the coast and one valley (140.750 to 140.996 E): check the
opening view with `scripts/check_map_view.js` (`map-view`).

**Scaffold**: `scaffold_city.py --slug iwaki --name Iwaki --system-name "JR
East" --taxonomy japan_eigyo --lat 37.078 --lon 140.786 --region "Japan
East" --country Japan --mode metro --page-number <N>` (`--dry-run` first),
with the page number claimed in `docs/session_roles.md` at build, not here
(Iwaki is not in `docs/staged_cities.json`).

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06, call 81); the Step 0
downloads (call 106); the standing Japanese calls above; `mode: metro`; the
minor tier and Japan East (Tohoku after the retag); no frequency floor (call
46); the Ban'etsu East Line drawn and named (call 86); both lines drawn as cut
(standing call, no stub); the laundry gap disclosed (the master list row).
**By precedent, noted for its size**: 種目 バー・スナック等 is a combined
sub-type naming snack bars, out whole as Tokyo's バー・キャバレー is (owner,
2026-09-29; `docs/category_rules.md`, adult and hostess venues): 719
restaurant permits, a fifth of them.

**Open, each with a recommendation:**

1. **How the months merge with the March list.** (a) **Keep the full list
   whole and add the months** (`rebuilt_register` with `as_of` 2026-03-31):
   **3,409 restaurants, 99.5%**. (b) Fukuyama's method, kept while in term
   on 2026-08-31: 3,281, 95.8%. *Recommend (a), Ichinomiya's answer (call
   126)*: the months publish new permits only (183 of 473 grants), so a
   renewal never appears and (b) would drop up to 134 live restaurants whose
   permit ended between April and August as if closed. Tradeoff: the real
   closures since 2026-03-31 stay on the map (the page keeps "may include
   closed premises"), and the date reads "permits in term on 2026-03-31,
   with new permits to 2026-08-31".
2. **MHLW beside the city's list** (Fukuyama's three, re-weighed for a
   0.01-cover file). (a) Its permits in no city file: **none** (all 43 are
   city permits); nothing to decide. (b) **Its notifications as a partial,
   opt-in Food-shops layer**: *recommend yes, on Matsuyama's, Fukuyama's and
   Ichinomiya's precedent*, disclosed as partial; the tradeoff is a very
   thin layer (164 addressed retail rows, supermarkets 38 and konbini 10
   among them, 61% at block level) and MHLW's credit on the notice. (c) Its
   own point where the block join misses, keyed by the number's digits AND
   the grant date: *recommend yes*, though it reaches at most 43 rows.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `OPERATOR_COLS` + 代表者氏名（法人）; the **小字-centroid tier**
  (above), opt-in, measured against MHLW's points; `rebuilt_register`'s
  `end_col` / `granted_col` passed from the config.
- `as_of` pinned to **2026-03-31** for merge (a) (or 2026-08-31 for (b)),
  never today; the 2024-04 to 2026-03 monthly files left out; no key on
  許可番号 alone.
- The register's months to 2026-09-30 added; the 福島市 row dropped; the
  register's own date stated as 2026-05-31 with the months since.
- Gate 3 (JR East), OSM `name:en`, line colours on both basemaps, the opening
  view (`map-view`), the factory share, the Economic Census control
  (estimated 1.54), `check_provenance.py`, `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "iwaki-food-page",
    "claim": "The food page offers the FY2025 full list and the August 2026 monthly CSV and XLS, and links CC BY 4.0. ASCII strings only: the host sends no charset, so the Japanese text (表示4.0日本, 令和７年度末時点) cannot be matched; a newer full list or month means re-measure",
    "kind": "http_contains",
    "url": "https://www.city.iwaki.lg.jp/www/contents/1652661537484/index.html",
    "present": ["Shokuhin_itiran_R08.csv", "Shokuhin_itiran_R0808.csv", "R080831.xls", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "iwaki-env-page",
    "claim": "The barber and beauty page offers the full list (as of 2026-05-31) and the June to September 2026 monthly CSVs, and links CC BY 4.0. ASCII strings only (no charset sent)",
    "kind": "http_contains",
    "url": "https://www.city.iwaki.lg.jp/www/contents/1780984436063/index.html",
    "present": ["ribiyoujo_ichiran.csv", "ribiyoujo_R8.6.csv", "ribiyoujo_R8.9.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "iwaki-food-full-live",
    "claim": "The full food list (1,032,586 B, 4,375 rows on 2026-10-06) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://www.city.iwaki.lg.jp/www/contents/1652661537484/simple/Shokuhin_itiran_R08.csv",
    "min_bytes": 1000000
  },
  {
    "id": "iwaki-food-aug-live",
    "claim": "The August 2026 monthly food file (6,945 B, 34 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.iwaki.lg.jp/www/contents/1652661537484/simple/Shokuhin_itiran_R0808.csv",
    "min_bytes": 5000
  },
  {
    "id": "iwaki-env-full-live",
    "claim": "The barber and beauty list (150,938 B, 1,165 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.iwaki.lg.jp/www/contents/1780984436063/simple/ribiyoujo_ichiran.csv",
    "min_bytes": 140000
  },
  {
    "id": "iwaki-env-sep-live",
    "claim": "The September 2026 barber and beauty file (759 B, 3 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.iwaki.lg.jp/www/contents/1780984436063/simple/ribiyoujo_R8.9.csv",
    "min_bytes": 500
  },
  {
    "id": "iwaki-mhlw-live",
    "claim": "MHLW's open-data file for Iwaki (07204), the control, answers a plain keyless GET (205,488 B, 636 rows on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=07204_food_business_all.csv",
    "min_bytes": 150000
  },
  {
    "id": "iwaki-isj-block-live",
    "claim": "MLIT's block-level address file for Iwaki (07204) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/07204-24.0a.zip",
    "min_bytes": 500000
  },
  {
    "id": "iwaki-isj-chome-live",
    "claim": "MLIT's town-chōme file for Iwaki (07204) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/07204-19.0b.zip",
    "min_bytes": 10000
  },
  {
    "id": "iwaki-jr-iwaki-timetable",
    "claim": "JR East's timetable index for いわき (0166) still links its three weekday pages: Jōban to 原ノ町 (010), Jōban to 水戸 (020), Ban'etsu East to 郡山 (030) - the frequency source. ASCII strings only (no charset sent)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0166.html",
    "present": ["tt0166/0166010.html", "tt0166/0166020.html", "tt0166/0166030.html"]
  },
  {
    "id": "iwaki-jr-ogawago-timetable",
    "claim": "JR East's timetable index for 小川郷 (0359) links the Ban'etsu East Line both ways - the thinnest in-city stretch (6 to 8 a day each way on 2026-10-06). ASCII strings only",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0359.html",
    "present": ["tt0359/0359010.html", "tt0359/0359020.html"]
  },
  {
    "id": "iwaki-projected-crs",
    "claim": "Iwaki projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.786,
    "expect": "EPSG:32654"
  }
]
```
