# Itami — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 118: `docs/decisions_drafts/staging.md`, "Wave 5, second half": "Amagasaki,
Suita, Itami, Kakogawa (call 118: 101-106% with old-law permits)"). Hyōgo
Prefecture's files were approved and fetched for the measurement (call 90) and
MLIT's address blocks for the block join (call 106). **Step 0 measured
2026-10-06** (staging). Into `data/itami/raw/` (gitignored), each from its
publisher's own host with the project user-agent, each HTTP 200:

- From `web.pref.hyogo.lg.jp` (保健医療部 生活衛生課), fetched 2026-10-06 into
  `data/hyogo_pref/raw/` and **copied unchanged** into `data/itami/raw/` (and
  `data/kakogawa/raw/`), because a Japanese build reads `data/<slug>/raw/`
  (`config.source_csv`): `000028_food_business_lisence_all.xlsx`
  (**4,519,769 B**, the publisher's spelling), `000028_food_business_notification_all.xlsx`
  (**1,861,708 B**), `000028_barbershop_all.xlsx` (**195,680 B**),
  `000028_beauty_salon_all.xlsx` (**496,756 B**),
  `000028_cleaningbusiness_all.xlsx` (**113,185 B**).
- From `i2fas.mhlw.go.jp`: `28000_food_business_all.csv`, **Hyōgo
  Prefecture's file** (**1,579,737 B**, 2026-10-06), the control.
- From `nlftp.mlit.go.jp` (already cached): `isj/28207-24.0a.zip`
  (123,647 B) and `isj/28207-19.0b.zip` (10,299 B).

**8,900,781 B in all; the only new download for this brief was MHLW's file.**
Nothing else was downloaded.

**Run `python scripts/brief_check.py itami` before writing any code.** Then the
`japan-city` skill, **Tsu's shape** (`docs/build_briefs/tsu.md`: the
prefecture's standing lists, every row assigned to the city by its address),
with Kakogawa as its twin on the same files (`docs/build_briefs/kakogawa.md`).
Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py`'s own functions from scratch scripts
(`scripts/screen_japan_join.py` has no Itami entry; its table is shared code and
was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor for
JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at about
11 trains a day or fewer **named and drawn** (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The Osaka Monorail's one station, 大阪空港, is left out** (owner, the band
row, call 118). ⚠️ It is the one case where calls 54 and 92 would draw a lone
station cut: no other line serves 大阪空港 (Esaka's and 浦安's shape). The band
row is the later and more specific call, so the brief follows it; staging may
want the owner to confirm it knowingly at review time. Toyonaka's map does not
draw it either (`docs/build_briefs/toyonaka.md`: the Monorail's 大阪空港 is in
Itami).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Itami
carries `label_tier: "minor"` and `"region": "Japan West"`, as Nishinomiya and
Himeji do (`app/cities.py`); wave 4's first city to land retags Japan into the
eight regions, Itami into **Kansai**. Its dot (Hankyu 伊丹) sits about 5 km
from Toyonaka's and Amagasaki's centres (both Band A, briefed, not yet built)
and 12 km from Osaka's: its label offset from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`.** The owner's rule (2026-10-02, Nishinomiya's brief): no
tram or light rail; Hankyu's 3 station groups against JR West's 2 make a
private heavy-rail backbone, which reads `metro` (Nishinomiya's precedent).

---

## The one-line summary

**All three buckets from Hyōgo Prefecture's monthly lists (CC BY 4.0 by the
catalogue's terms as stated; the read is pending), cut to Itami by address:
1,727 food permits (1,379 restaurants, 189 of them old-law) through
2026-08-31, and 87 barbers, 296 beauty salons and 71 laundries as of
2026-08-31.** Prefecture-wide the lists are complete (restaurants **101.4%**
of e-Stat's FY2024 count in the prefecture's jurisdiction, barbers 97.3%,
beauty 100.7%, laundries 94.7%). No per-city count exists; **Itami's
restaurant share is estimated at about 86%** (the list's own density across the
jurisdiction, the 5,176 prefecture-wide 県下一円 stall and vehicle permits
removed). Through `japan_eigyo`: **Food service 1,333 rows (1,326 pins),
Retail 278 (238)**; Personal services 454 rows. Block join **95.4%** (food
95.8%), 4.6% town-chōme centroid, 1 row unplaced. **Rail: 6 N02 station
groups, 5 drawn**: the Hankyu Itami Line 3 (6 an hour), JR West's Takarazuka
Line 2 (8.3 and 4 an hour), read from the operators' own timetables; the
Monorail's 大阪空港 left out (above).

---

## Business leg — Hyōgo Prefecture's lists (保健医療部 生活衛生課)

Host `https://web.pref.hyogo.lg.jp` (the prefecture's CMS; the files are also
catalogued at `https://web.pref.hyogo.lg.jp/opendata/index.php`, the
生活衛生課 department's 14 entries, each with the CC BY icon). **The lists cover
the prefecture except its five health-centre cities**
(「兵庫県下（神戸市・姫路市・尼崎市・明石市・西宮市を除く。）」), so Itami, Kakogawa
and every other town are in them. ⚠️ **The host sends no charset**: a brief
check on these pages can only use ASCII anchors.

| Page | Edition | Files (under `/kf14/documents/`) | Cadence |
|---|---|---|---|
| 食品関係営業施設リストの閲覧, `https://web.pref.hyogo.lg.jp/kf14/shokuhineigyoushisetsu_list.html` (更新日 2026-09-24) | 「令和8年8月までのリスト（令和8年9月15日更新）」 | `000028_food_business_lisence_all.xlsx` 許可営業施設 (4,414KB), `000028_food_business_notification_all.xlsx` 届出営業施設 (1,819KB) | 「更新は毎月20日頃です」 |
| 生活衛生関係営業施設リストの閲覧, `https://web.pref.hyogo.lg.jp/kf14/kankyoueigyoushisetsu_list.html` (更新日 2026-09-10) | 「令和8年8月末時点のリスト（令和8年9月10日更新）」 | `000028_barbershop_all.xlsx`, `000028_beauty_salon_all.xlsx`, `000028_cleaningbusiness_all.xlsx` (inns, baths and theatres beside them, not used) | 「更新は月毎（各月の上旬）です」 |

- **The file names never change**: each month's edition replaces the last at
  the same URL. So the build pins `SOURCE_AS_OF` from the page's edition line
  (2026-08-31 for all five), never from the fetch date, and the edition checks
  below fail when a new edition lands (re-measure then).
- 「Excelファイルでは外字は表示されません」: characters outside the standard set
  are dropped in the XLSX (the PDF has them). Measured: **0 Itami addresses and
  1 trade name** carry a placeholder (jurisdiction-wide 4 and 37).

### The food permit list (`000028_food_business_lisence_all.xlsx`)

- **One sheet, header on row 1, 32,433 rows** (the jurisdiction).
  `japan_register.city_rows` reads it as it stands. Columns: 都道府県コード
  (000028), No, **営業所名称**, 営業所郵便番号, **営業所所在地**, 営業所電話番号
  (never), **業種**, **形態**, operator **営業者法人名称**, 営業者役職,
  **営業者氏名**, operator address and phone (never), **許可番号**, **許可日**,
  **有効期限**, 初許可日.
- **Every row is a permit in term**: 有効期限 runs 2026-11-30 to 2033-05-31
  (Hyōgo ends every permit on the last day of February, May, August or
  November, so nothing lapsed between the edition and the next quarter end).
  許可日 2018-10-01 to 2026-08-31; 初許可日 from 1958.
- **Key**: (許可番号, 許可日) is unique but for one pair in Itami (1,726 of
  1,727; 2 pairs prefecture-wide). The number alone repeats (926 distinct in
  Itami): `神北(伊健)第N-N`, the 伊丹健康福祉事務所's series, restarting each year.
- **形態** (the form): 一般 1,707, 露店40L 8, 自動販売機 7, 露店200L/直結 5. ⚠️
  **`FORM_COLS` lacks 形態** (shared code): without it the **13 street-stall
  rows at a street address read as restaurants**. `WAVE2_RULES` already holds
  `form_cols`, so adding 形態 to `FORM_COLS` is enough (`japan_eigyo.FORM_RULES`
  already reads 露店, 自動車 and 自動販売機); re-run the Minato control after.
- `ADDR_COLS` holds 営業所所在地, `NAME_COLS` 営業所名称, `TYPE_COLS` 業種,
  `OPERATOR_COLS` 営業者氏名 (not 営業者法人名称: harmless, a company is never a
  person under the rule).

### Cutting Itami out of the prefecture's lists

- **The rule: an address that begins `伊丹市`** (after NFKC and spaces
  removed; 2 rows in the whole food list carry `兵庫県`, none of them Itami's,
  and the build strips it anyway). **0 rows contain 伊丹市 anywhere else** in
  any of the five files. No municipality-code column exists: the build's
  `config.source_rows` (or `file_rows`) cuts by the prefix and **raises** on a
  row containing 伊丹市 elsewhere (Tsu's rule).
- **The 5,176 prefecture-wide permits** (address `県下一円（ただし、神戸市…を除く）`,
  vehicles and stalls licensed anywhere in the jurisdiction) belong to no
  town; `permits_from_rows` marks them not a premises by `一円`. They are not
  Itami's and not in its count.

### Food by type, through `japan_eigyo` (measured, 形態 read as the form)

| | Rows | Kept | Out (rule) |
|---|---|---|---|
| 飲食店営業 (1) 一般食堂・レストラン等 786 · (4) その他 557 · (2) 仕出し屋・弁当屋 34 · (3) 旅館 1 · (5) 簡易な営業 1 | 1,379 | **1,331 Food service** (+ 2 old-type 喫茶店営業: **1,333**) | 34 仕出し (catering) · 13 stalls by 形態 · 1 旅館 |
| Food retail permits (菓子 141, 食肉販売 62, そうざい 38, 魚介類販売 37) | 278 | **278 Retail** | |
| Vending (調理の機能を有する自動販売機 7) | 7 | 0 | vending |
| Manufacturing and other types (食品の小分け 12, 添加物 7, 漬物 7 …) | 61 | 0 | "no rule", as in every built city |

- **(4) その他 is the list's catch-all, 40% of restaurants** (557 of 1,379;
  49% prefecture-wide). It stays in Food service, as Tsu's 飲食店営業（その他）
  does: **no hostess-venue marker exists** in the list, so snack bars cannot be
  told apart (`docs/category_rules.md` R3 applies "wherever the register names
  them"; here it names none).
- **One pin per (address, trade name, bucket): Food service 1,326, Retail
  238.** 10 (address, trade name, type) groups repeat (20 rows); 1,563
  distinct (address, trade name).
- **Factory share**: 11 of 179 菓子 / そうざい rows (6.1%) are named 工場 or
  センター, kept (the 2026-09-27 call).

### Old-law coverage (Kurashiki's trap) — not this list's problem

- **Old-law permits are in the list**: **247 rows granted before 2021-06-01**
  (restaurants 189: (4) その他 116, (1) 68, (2) 5; 菓子 24, 食肉 10 …), ending
  2026 (83), 2027 (156) and 2028 (8). New-law restaurants by grant year: 2021
  95 · 2022 225 · 2023 253 · 2024 238 · 2025 203 · 2026 176.
- Prefecture-wide the list holds 2,410 old-law restaurants in force against
  e-Stat's 7,192 at 2025-03-31 (17 months earlier): the old-law permits run out
  and come back as new-law ones, and the total still reaches 101.4% (below).

### Completeness — the prefecture measured, Itami estimated

**No official per-city count**: e-Stat's 衛生行政報告例 carries prefectures,
designated and core cities only (`docs/coverage_sweep/japan_universe_mhlw.csv`
has no official count for 28207). **The jurisdiction** (e-Stat FY2024,
2025-03-31: 兵庫県 less Kobe, Himeji, Amagasaki, Akashi and Nishinomiya)
against the lists (2026-08-31):

| | e-Stat in force, the jurisdiction | Hyōgo's list | Share |
|---|---|---|---|
| Restaurants (飲食店営業, old + new law) | **23,537** | 23,875 | **101.4%** |
| Barbers (第10表) | 1,570 | 1,528 | **97.3%** |
| Beauty salons (第10表) | 4,100 | 4,127 | **100.7%** |
| Laundries (premises, 取次所 included) | 836 | 792 | **94.7%** |

**Itami's share, estimated** against the 2021 Economic Census (the census's
飲食店 610, 理容業 83, 美容業 183, 洗濯業 64 establishments in 28207):

- **Restaurants about 86%**: the list holds 2.62 restaurant permits per census
  飲食店 across the jurisdiction once the 5,176 県下一円 permits are removed
  ((23,875 − 5,176) / 7,141); Itami's 1,379 against 610 × 2.62 is **86.3%**
  (fixed premises only, 1,366: 85.5%). With e-Stat's count in place of the
  list's, 87.9%; with the median ratio of ten Kansai core cities' own e-Stat
  counts (2.85 per census 飲食店), 79% (range 70-84%). **The page states about
  86% as an estimate** (call 125's stated share), never as a measured count.
- **Barbers 87.9%** (87 against 99 estimated), **beauty 103.9%** (296 against
  285), **laundries 92.2%** (71 against 77), by the same jurisdiction ratios.
- **The Economic Census control** (`scripts/japan_census_control.py` at
  build): 1,326 Food-service pins against 610 is **2.17 per establishment**, ⚠️
  **above the built cities' 1.56-1.92** (Akita's brief 2.11, Tsu's 2.01).
  Hyōgo's list runs high everywhere (2.56 fixed permits per establishment
  jurisdiction-wide, Itami 2.24): read why on the built pins (one premises
  under several permits or trade names, closures the monthly list keeps, or a
  census undercount) and record the reading.

### Duplicates and closed premises

- **Closures are not marked**: no status column. One sign that the list keeps
  a closed premises for a while: **MHLW's one closed permit in the
  jurisdiction** (許可(廃業), closed 2026-08-05) **is still in the 2026-08 list**
  under its number and grant date. One case; the page keeps "may include
  closed premises".
- Repeats as above (1 number pair, 10 address-name-type groups).

### The notification list (`000028_food_business_notification_all.xlsx`)

13,713 rows prefecture-wide, the same columns with **届出番号** and **施行日**
(2021-06-01 to 2026-08-31: the whole life of the 届出 system) in place of the
permit columns. **Itami: 803 rows** (その他の食料・飲料販売業 202, cup vending 100,
コンビニエンスストア 75, 乳類販売業 72, 集団給食 71, vending 63, 百貨店、総合スーパー
60 …; 形態 一般 530, 自動販売機 196, 集団給食 68). Through `japan_eigyo`: **426
Retail rows, 416 pins** (その他の食料・飲料販売業 194, konbini 75, supermarkets
60, 乳類 41, 野菜果物 14, 食肉 13, 弁当 11, 魚介類 10, 米穀 8); out 196 vending,
80 institutional, 88 manufacturing ("no rule"), 6 not a premises, 4 mail
order. **The prefecture's own complete list**, unlike MHLW's opt-in filings:
open call 1.

### Personal services: the three registers (as of 2026-08-31)

| File | Prefecture rows | **Itami** | Kinds (営業の種類 / 営業の種類２) |
|---|---|---|---|
| `000028_barbershop_all.xlsx` (sheet 理容所) | 1,528 | **87** | 理容所 / 固定 |
| `000028_beauty_salon_all.xlsx` (sheet 美容所) | 4,127 | **296** | 美容所 / 固定 (one 移動 prefecture-wide, not in Itami) |
| `000028_cleaningbusiness_all.xlsx` (sheet クリーニング所) | 792 | **71** | 一般 23, 一般(指定洗濯物取扱) 2, **取次 46** |

- ⚠️ **The header is numbered with circled numerals**: `①営業所名称`,
  `①営業所名称２`, `②営業所所在地`, `③営業の種類`, `③営業の種類２`, `④営業者氏名`,
  `⑤許可年月日`, `⑥許可番号`, `⑦営業所電話番号`, `⑧営業者住所`, `⑨営業者電話番号`,
  `⑩役職`, `⑩代表者氏名`. **`city_rows` reads 0 rows** from each (no header it
  knows). Stripping one leading circled numeral (U+2460 to U+2473) gives
  the columns the shared tuples already hold (営業所所在地, 営業所名称, 営業の種類,
  営業者氏名, 代表者氏名). Either a `file_rows` in the config or the strip in
  `_head` (shared code, then the Minato control and every city screen); the
  measurement stripped it in memory.
- 許可年月日 from 1948 to 2026-08 (standing registers, one date per premises).
  **No repeats** by (address, trade name) in any register; **4 addresses** hold
  both a barber and a beauty salon (one pin per premises and bucket).
- The page says nothing about closed premises: "may include closed premises".

### MHLW's file (28000), the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28000_food_business_all.csv`:
**1,579,737 B, 5,362 rows** (届出 5,004, 許可 351, 届出(廃業) 6, 許可(廃業) 1),
the national schema, UTF-8; permits granted 2017-05-22 to 2026-08-31.

- ⚠️ **Trap: 市区町村名 is `神戸市中央区` on every row** (the prefectural
  government's seat), as Tsu's file names 津市 and Uji's 京都市上京区. A build
  that read 市区町村名 would take all 5,362 rows as Kobe's. Only 1,900 rows
  carry an address; none falls in the five excluded cities.
- **239 rows addressed to Itami** (届出 204, 許可 34, 許可(廃業) 1), every one
  with MHLW's own point. **The 34 open permits are all restaurants; 32 are in
  Hyōgo's list** by (number digits, grant date) (MHLW writes the number bare,
  `N-N`, on 156 of its 351 permits). Prefecture-wide 340 of 351. Hyōgo's list
  is the complete one; MHLW adds nothing to it.
- **Its own point against the block point**: median **32 m**, 99.5% within
  250 m, none over 1 km (221 block-tier rows): the block join is sound here.

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 28207)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28207-24.0a.zip` (123,647 B) and
`…/19.0b/28207-19.0b.zip` (10,299 B): **19,873 block keys**, **391 town-chōme
keys**. Ward-less (`"wardless": True`). Measured with `permits_from_rows`,
`load_city_isj` and `join_city` under `WAVE2_RULES`, unchanged (staging's
`isj_measure`; the food rows filtered to 形態 一般, in force).

| Tier (rows in a bucket) | Food (1,611) | Barbers (87) | Beauty (296) | Laundries (71) | **All (2,065)** |
|---|---|---|---|---|---|
| Block | 95.8% | 96.6% | 93.9% | 91.5% | **95.4%** (1,970) |
| Town-chōme centroid | 4.2% | 3.4% | 5.7% | 8.5% | 4.6% (94) |
| Unplaced | 0.0% | 0.0% | 0.3% | 0.0% | **1 row** |

**The misses, read** (towns only):
- **Chōme tier (94)**: 93 in towns MLIT carries whose number it lacks (寺本4丁目
  5, 緑ケ丘5丁目 4, 北伊丹1丁目 3, 北野5丁目 3, 美鈴町3丁目 2, 池尻1丁目 2 …): the
  chōme centroid by design. 1 字 address (中村字井ノ下) whose 字 MLIT keys
  without blocks.
- **Unplaced (1)**: `宮の前` written with の and the chōme as a number
  (`宮の前N-N-N`), where MLIT keys 宮ノ前1丁目 to 3丁目. One row: not worth
  shared code on its own; read at build.
- Rules used: 168 shifted, 2 suffix affixes, 1 大字. **No publisher
  coordinates** in Hyōgo's lists.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (28207)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_28_GML.zip`, N03 code 28207
(**25.0 km²**, extent W 135.3698, S 34.7568, E 135.4462, N 34.8155; centroid
34.785, 135.407; Osaka International Airport straddles its east edge). No
Shinkansen.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 伊丹線 (阪急電鉄, 12) | Hankyu Itami Line | **3 / 4** | 稲野, 新伊丹, 伊丹 (its terminus) |
| 福知山線 (西日本旅客鉄道, 11) | JR Takarazuka Line (JR宝塚線) | **2 / 30** | 伊丹, 北伊丹 |
| 大阪モノレール線 (大阪モノレール, 23) | Osaka Monorail Main Line | **1 / 14** | 大阪空港 (its terminus, 21 m inside the line): **left out** (above) |

- **6 station records, 6 `N02_005g` groups; 5 drawn.** ⚠️ **Two groups share
  the name 伊丹**: JR West's 伊丹 (006709) and Hankyu's 伊丹 (006714) are
  separate stations **740 m apart** (N02 keeps them apart, trap 1; Kobe's
  Tarumi case). Their labels must tell them apart (JR Itami and Hankyu Itami:
  OSM `name:en` at build, and a label check).
- **Median nearest-group gap 810 m** (740 to 2,250): rings by the spacing rule.
- **Cut at the line**: the Hankyu Itami Line on to 塚口 (Amagasaki, 409 m
  beyond the line, the junction with the Kobe Line); the JR Takarazuka Line on
  to 猪名寺 (Amagasaki, 301 m) and 中山寺 (Takarazuka) and 26 more. Both are
  drawn as cut (Nishinomiya's JR Takarazuka precedent).
- **The stub test** (`stub_test()`): Hankyu Itami 3 of 4 (0.75), JR 2 of 30,
  the Monorail 1 of 14. The Monorail is the only urban one-station line, and
  its call is made (above).
- **The light-rail / rail test**: Hankyu and JR are heavy rail (N02 classes 12
  and 11); the Monorail (class 23) is out. No tram or light rail.
- **Frequency, READ** (the wave-5 probe's cached operator pages, plain GET,
  counted whole here: every departure listed, marked ones included):

  | Station (line, direction) | Weekday departures | Per hour, 07-18 | Midday (10-16) |
  |---|---|---|---|
  | 伊丹 (JR Takarazuka, to 大阪・北新地) | 167 | 8 to 14 | 8.3 an hour (快速, 区間快速, 丹波路快速 included) |
  | 北伊丹 (JR Takarazuka, to 大阪・北新地) | 80 | 4 to 6 | 4 an hour (the rapids pass) |
  | 稲野, 新伊丹, 伊丹 (Hankyu Itami, to 塚口) | 125 each | 6 to 10 | 6 an hour |

  JR West's station timetables (`timetable.jr-odekake.net/station-timetable/<id>?date=20261007`,
  a Wednesday; ids 2822025001, 2823025001), Hankyu's station pages
  (`www.hankyu.co.jp/station/html/HK-18_it_1_w.html`, HK-19, HK-20, weekday).
  **No stretch at or under about 11 trains a day** (call 86). Only counts are
  recorded, never a timetable on the page.
- ⚠️ **Gate 3** at build: Hankyu's Itami Line (4 stations, 3 inside) and JR
  West's station lists. **OSM `name:en`** for 5 groups (one Overpass query at
  build; none queried here).

## Scope

**Itami City (28207), one municipality, no wards.** Hankyu runs on to
Tsukaguchi and JR to Amagasaki and Takarazuka; cut at the line. The Osaka
Monorail's 大阪空港 is out (the owner's call): the page's rail bullet names it
as left out.

## Licences — as stated; the read is pending

- **Hyōgo Prefecture's lists**: the list pages state no licence themselves;
  the prefecture's catalogue lists all five XLSX under 生活衛生課 with the **CC
  BY** icon, and its terms, 兵庫県オープンデータカタログページ利用規約
  (`https://web.pref.hyogo.lg.jp/kk26/johoseisaku/documents/kiyaku_opendata.pdf`,
  linked from `https://web.pref.hyogo.lg.jp/kk26/johoseisaku/opendata.html`),
  say 3(3) that the catalogue's works are licensed 「CCライセンス表示4.0国際」
  unless noted, with the credit `出典：[著作物のタイトル]、［兵庫県]` for an
  unmodified copy and, for a modified one, 「この[作品]は、以下の著作物を改変して
  利用しています。[タイトル]、［兵庫県]」, and forbid presenting edited data as if
  the prefecture made it; 2(1) puts the catalogue terms above the website's.
  **A licence-read agent reads the source separately; staging records it. No
  verdict here.** Proposed credit, pending that read:
  `この地図は、以下の著作物を改変して利用しています。「食品関係営業施設リスト（許可営業施設）」「理容師法検査確認施設」「美容師法検査確認施設」「クリーニング業法検査確認施設」、兵庫県（2026-08-31）`
  with the CC BY 4.0 link (and 「届出営業施設」 if open call 1 is taken).
- **MHLW open data (28000)**: the control only; PDL 1.0 as recorded in
  `docs/data_sources/japan.md` if it is ever used.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources, not drawn. **JR West's and Hankyu's timetables**: read for counts
  only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

Select 営業所名称, 営業所所在地, 業種, 形態, 許可番号, 許可日, 有効期限 (food;
届出番号 and 施行日 for notifications) and 営業所名称, 営業所所在地, 営業の種類,
営業の種類２ (registers). **Never select 営業所電話番号, 営業者住所 or
営業者電話番号.** The operator columns are read in memory by the name rule and
never kept:

| | Operator columns | Rows | Company (法人名称 filled) | Sole traders (no 法人名称) | Flagged (v2) |
|---|---|---|---|---|---|
| Food permits | 営業者法人名称, 営業者氏名 (filled on every row: a company's representative or the sole trader), 営業者役職 | 1,727 | 853 (848 with a company marker) | **874** | **1** (trade name equals the operator's name), 1 among kept rows; **0** bare personal names |
| Notifications (open call 1) | as food | 803 | 675 | **128** | **5** (trade name = operator), 0 bare |
| Barbers / beauty / laundries | 営業者氏名, 代表者氏名 | 87 / 296 / 71 | no company marker on 73 / 237 / 26 | | **0** |

The prefecture publishes sole traders' own names in 営業者氏名; nothing reads
them for output. No value was printed or stored. Run
`check_personal_exposure.py itami` with `japan=True` after step 2 (it must
print 0) and record the verdict in the drafts file and
`docs/privacy_verdicts.md`.

## Region and CRS

`"region": "Japan West"` (Kansai after the retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 53N (EPSG:32653)**: the extent
135.3698 to 135.4462 lies inside the 132-138 band, computed here, never copied.

**Scaffold**: `scaffold_city.py --slug itami --name Itami --system-name "Hankyu
and JR West" --taxonomy japan_eigyo --lat 34.7799 --lon 135.4137 --region
"Japan West" --country Japan --mode metro --page-number <N>` (`--dry-run`
first; Hankyu 伊丹's N02 point), the page number claimed in
`docs/session_roles.md` at build, not here. A `japan.CITIES` entry: `"itami":
{"name": "伊丹市", "pref": "28", "epsg": 32653, "n02": "25", "rules":
WAVE2_RULES, "wardless": True, "wards": ["28207"]}`. `SOURCE_FILES` under the
file names above; `SOURCE_AS_OF` 2026-08-31 for each (the pages' edition lines),
never today. `LEFT_OUT_LINES` (or the step-1 equivalent) names the Osaka
Monorail.

## Owner calls

**Made (do not re-ask):** Band A (call 118); the files (call 90) and MLIT's
blocks (call 106); the Osaka Monorail's 大阪空港 left out (the band row; see the
note above on calls 54 and 92); the standing Japanese calls; `mode: metro`; the
minor tier and Japan West (Kansai after the retag); the JR Takarazuka and
Hankyu Itami lines drawn as cut (standing call 3); no frequency floor; a stated
share where a list cannot be measured per city (call 125, as about 86%).

**Answered by the owner on 2026-10-06:** call 163, **the Osaka Monorail's one station (大阪空港) drawn cut** (no other line serves it: calls 54 and 92), so 6 station groups drawn; call 164, **Hyōgo's own notification list added as a Food-shops layer** (Yokkaichi's precedent; its operator-name rows go through the name rule). The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **Hyōgo's own notification list as a Food-shops layer** (416 Retail pins:
   konbini 75, supermarkets 60, other food and drink sales 194, milk, produce,
   butchers …). *Recommend yes*, Yokkaichi's precedent: it is the publisher's
   complete list (every notification since the system began, 2021-06-01),
   already approved, cached and under the same terms, unlike MHLW's opt-in
   filings. Tradeoff: the template's standing bullet ("Food businesses that
   only notify … are not in the list") is then wrong for Itami, so its
   replacement is a proposal in the drafts file at build; 5 notification rows
   fall to the name rule. Without it, Retail is the permit-holding shops only
   (238 pins, no konbini or supermarket). Decide it with Kakogawa's open call
   1, the same file.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control,
  `screen_japan_join.py minato` 98.0 / 0.2 / 1.8, and every city screen):
  `FORM_COLS` + 形態; the registers' circled-numeral header (strip in `_head`,
  or a `file_rows` in the config); Itami's `japan.CITIES` entry.
- ⚠️ **`config.source_rows`**: the `伊丹市` prefix cut (strip `兵庫県` first),
  raising on a row that contains 伊丹市 elsewhere. Never MHLW's 市区町村名.
- ⚠️ The Economic Census control (2.17, above the built range) and its reading;
  the stated food share (about 86%, the method above) in the page's bullet,
  drafted as a review-time proposal.
- The two 伊丹 labels; gate 3 (Hankyu, JR West); OSM `name:en`; line colours on
  both basemaps; the macro label against Amagasaki's, Toyonaka's and
  Nishinomiya's; the opening view (`map-view`); the factory share printed by
  step 2; `check_provenance.py`; `check_scope_disclosure.py` (the Monorail
  named as left out).

```brief-checks
[
  {
    "id": "itami-hyogo-food-page",
    "claim": "Hyogo's food list page links both XLSX (permits, notifications) at the sizes of the 2026-08 edition (4,414KB, 1,819KB). ASCII anchors only: the host sends no charset. A failure on the sizes means a new edition: re-measure",
    "kind": "http_contains",
    "url": "https://web.pref.hyogo.lg.jp/kf14/shokuhineigyoushisetsu_list.html",
    "present": ["/kf14/documents/000028_food_business_lisence_all.xlsx", "/kf14/documents/000028_food_business_notification_all.xlsx", "4,414KB", "1,819KB"]
  },
  {
    "id": "itami-hyogo-registers-page",
    "claim": "Hyogo's registers page links the barber, beauty and laundry XLSX at the sizes of the 2026-08-31 edition (192KB, 486KB, 111KB); ASCII anchors only",
    "kind": "http_contains",
    "url": "https://web.pref.hyogo.lg.jp/kf14/kankyoueigyoushisetsu_list.html",
    "present": ["000028_barbershop_all.xlsx", "000028_beauty_salon_all.xlsx", "000028_cleaningbusiness_all.xlsx", "192KB", "486KB", "111KB"]
  },
  {
    "id": "itami-hyogo-food-permits-file",
    "claim": "The food permit list (4,519,769 B on 2026-10-06) answers a plain GET",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kf14/documents/000028_food_business_lisence_all.xlsx",
    "min_bytes": 4000000
  },
  {
    "id": "itami-hyogo-notifications-file",
    "claim": "The food notification list (1,861,708 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kf14/documents/000028_food_business_notification_all.xlsx",
    "min_bytes": 1500000
  },
  {
    "id": "itami-hyogo-barber-file",
    "claim": "The barber register (195,680 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kf14/documents/000028_barbershop_all.xlsx",
    "min_bytes": 150000
  },
  {
    "id": "itami-hyogo-beauty-file",
    "claim": "The beauty register (496,756 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kf14/documents/000028_beauty_salon_all.xlsx",
    "min_bytes": 400000
  },
  {
    "id": "itami-hyogo-laundry-file",
    "claim": "The laundry register (113,185 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kf14/documents/000028_cleaningbusiness_all.xlsx",
    "min_bytes": 90000
  },
  {
    "id": "itami-hyogo-terms",
    "claim": "Hyogo's open-data page links the catalogue terms PDF (kiyaku_opendata.pdf, which licenses the catalogue's works under CC BY 4.0) and the catalogue",
    "kind": "http_contains",
    "url": "https://web.pref.hyogo.lg.jp/kk26/johoseisaku/opendata.html",
    "present": ["/kk26/johoseisaku/documents/kiyaku_opendata.pdf", "opendata/index.php"]
  },
  {
    "id": "itami-hyogo-terms-pdf",
    "claim": "The catalogue terms PDF answers a plain GET",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kk26/johoseisaku/documents/kiyaku_opendata.pdf",
    "min_bytes": 50000
  },
  {
    "id": "itami-mhlw-live",
    "claim": "MHLW's open-data file for Hyogo Prefecture (28000), the control, answers a plain keyless GET (1,579,737 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28000_food_business_all.csv",
    "min_bytes": 1200000
  },
  {
    "id": "itami-isj-block-live",
    "claim": "MLIT's block-level address file for Itami (28207) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28207-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "itami-isj-chome-live",
    "claim": "MLIT's town-chome address file for Itami (28207) answers keyless - the centroid tier",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/28207-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "itami-jr-itami-timetable",
    "claim": "JR West's weekday timetable for JR Itami toward Osaka (id 2822025001), the page counted (167 departures)",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/2822025001?date=20261007",
    "present": ["大阪・北新地方面", "minute-item"]
  },
  {
    "id": "itami-hankyu-itami-timetable",
    "claim": "Hankyu's weekday timetable for Hankyu Itami (HK-20, Itami Line toward Tsukaguchi), the page counted (125 departures)",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/html/HK-20_it_1_w.html?no_redirect",
    "present": ["伊丹線", "TM="]
  },
  {
    "id": "itami-projected-crs",
    "claim": "Itami projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.407,
    "expect": "EPSG:32653"
  }
]
```
