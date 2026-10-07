# Matsue — build brief

**Band B, personal services only, owner-approved 2026-10-06** (Japan wave 4,
banded in staging's wave 5, call 96: `docs/decisions_drafts/staging.md`,
"Wave 5, second half": "Matsue (personal services; PDL 1.0 read)"; the master
list's row: "Personal services only (Kōchi's shape)"). The Step 0 downloads
were approved by the owner 2026-10-06 (call 147). **Step 0 measured
2026-10-06** (staging). Into `data/matsue/raw/` (gitignored), each from its
publisher's own host with the project user-agent, each HTTP 200, under the
file name the host sends:

- From `shimane-opendata.jp` (島根県's portal, records published by 松江市):
  resources **76779** `20260831riyousho.xlsx` (46,625 B), **76780**
  `20260831biyousho.xlsx` (102,585 B) and **76781** `20260831cleaning.xlsx`
  (26,360 B), each as of 2026-08-31, by
  `https://shimane-opendata.jp/resource_download/<id>`.
- From `i2fas.mhlw.go.jp`: `32201_food_business_all.csv` (178,802 B), the
  round's standing control, measured only.
- From `nlftp.mlit.go.jp`: `isj/32201-24.0a.zip` (244,068 B) and
  `isj/32201-19.0b.zip` (8,911 B).

**607,351 B in all.** Nothing else was downloaded as data: not the city's
own food list (site copyright, below), not the portal's older monthly
resources. For rail counts, JR West's station timetable pages (HTML) and
Ichibata's eight station timetable PDFs (304,836 B, in the session
scratchpad only) were read; see Rail.

**Run `python scripts/brief_check.py matsue` before writing any code.** Then
the `japan-city` skill, **Kōchi's shape** (`docs/build_briefs/kochi.md`:
personal services only, food off) and **Matsumoto's for three registers with
the laundry kinds** (`docs/build_briefs/matsumoto.md`). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Matsue
entry; its table is shared code and was not edited). Rail: MLIT N02-25 cut at
the N03 city line, through `pipeline/countries/japan.py` with a scratch
`CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs in Shimane); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE station
is left out, its station kept through the other lines, and drawn cut only
where no other line serves that station (owner, 2026-10-06, calls 54 and 92);
(4) **菓子製造業 and そうざい製造業 count, in Retail** (2026-09-24; moot on a
personal-services page); (5) **the name rule**, version 2 (2026-10-06): a
bare personal name is withheld whatever the operator column holds, and MHLW's
法人名 joins it (2026-10-05); (6) **no page says "currently operating"**.
Also: no frequency floor for JR or private lines in Japan (owner, 2026-10-06,
call 46), any stretch at about 11 trains a day or fewer named and drawn (call
86); fault-based cost clauses accepted for all of Japan (2026-09-24); English
station names from OSM `name:en`; every Japanese city reads `WAVE2_RULES`
(owner, 2026-10-04).

**✅ Food left out (owner, 2026-10-06, the band row).** The city's own food
list falls under the city site's copyright and was not requested (below);
MHLW's file is too thin to stand in (below; Iwaki's call 150 applied).

**✅ The Kisuki Line drawn and named (owner, call 86, the band row).** Its
10 and 11 trains a day at 南宍道 (counted below).

**✅ The tiers disclosed (owner, call 145, Kakogawa's precedent, applied).**
81.3% of Matsue's premises reach a block, 17.0% a town or 大字 centroid, 1.7%
are unplaced (below). The page says so in its coordinates bullet; nothing is
dropped for it. ⚠️ This is lower than Kakogawa's 86.5%: see open call 1.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Matsue
carries `label_tier: "minor"` and goes in the **Japan West** view
(`app/cities.py`), as Okayama and Hiroshima; wave 4's first city to land
retags Japan into the eight regions, Matsue into **Chugoku**. Its label
offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200),
never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 and Matsumoto's and
Takamatsu's precedent: no subway, tram or light rail is drawn; JR West (8
station groups) and the Ichibata Kita-Matsue Line (8, a railway, N02 class
12) are both heavy rail, so the mode follows the backbone.

---

## The one-line summary

**Personal services only, from 松江市's monthly registers on Shimane's
portal (PDL 1.0 as read by staging): barbers 267, beauty salons 574 and
laundries 108 (27 general, 81 pick-up counters) as of 2026-08-31, 98.5%,
101.8% and 98.2% of official; block join 81.3%, 17.0% at a town or 大字
centroid, unplaced 1.7%.** The low block share is structural: MLIT's block
file carries no block at all for five of the towns merged in 2005 (島根町,
美保関町, 八雲町, 八束町 and nearly all of 鹿島町), whose 91 premises take a
大字 centroid. **No food**: the city's list is under site copyright and
MHLW holds 45 open restaurant permits (1.9% of e-Stat's 2,328 in force).
**Rail: 16 N02 station groups**: JR West's San'in Main Line 7 (20 to 45
weekday departures per direction, read), the Kisuki Line's 南宍道 (**10 and
11 a day**, named and drawn, call 86) and the Ichibata Kita-Matsue Line 8
(21 to 24 a day per direction, about hourly, read).

---

## Business leg — 松江市's 生活衛生 registers on Shimane's portal

### Where the city publishes

Shimane Prefecture's portal `https://shimane-opendata.jp` (島根県 dataeye,
run by 一般社団法人データクレイドル) carries one dataset per kind, organisation
松江市, 作成頻度 毎月, each holding **20 monthly resources**, every one **the
full list as of its month end** (「令和8年8月31日時点の松江市内の理容所一覧です。」):

| Dataset (`/datasets/<n>`) | Newest resource (`/resources/<id>`) | File | Bytes | Rows | Official (e-Stat FY2024) | Share |
|---|---|---|---|---|---|---|
| 1254 【松江市】理容所一覧 | **76779**, 2026-08-31 | `20260831riyousho.xlsx` | **46,625** | **267** | barbers 271 | **98.5%** |
| 898 【松江市】美容所一覧 | **76780**, 2026-08-31 | `20260831biyousho.xlsx` | **102,585** | **574** (+1 repeated header) | beauty salons 564 | **101.8%** |
| 899 【松江市】クリーニング所一覧 | **76781**, 2026-08-31 | `20260831cleaning.xlsx` | **26,360** | **108**: クリーニング所 27, 取次所 81 | 110: general 28, 取次所 82 | **98.2%** (96.4%, 98.8%) |

Official from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv`
(第10表) and `…_cleaning_by_city.csv` (第11表), 島根県松江市 (a core city, so
e-Stat carries its own row), in force 2025-03-31. Each resource page was
published 2026-09-11 and states `PDL1.0（公共データ利用規約第1.0版）`.

- **One sheet each** (`1_理容所`, `2_美容所`, `3_クリーニング所`), a title row,
  then the header on row 2; no empty rows. Columns: 確認番号, 検査確認日,
  営業所郵便番号, **営業所所在地** (barber and beauty: the long label
  `営業所所在地（移動理容所にあっては営業区域及び車両保管場所）` /
  `…（移動美容所にあっては…）`), **営業所名称**, 営業所電話番号,
  **営業者の名称又は氏名**, 代表者の役職及び氏名, 営業者所在地, and in the
  laundry file **クリーニング所又は取次所の別** (クリーニング所 27, 取次所 81).
- **Against the shared tuples**: 営業所名称 is in `NAME_COLS`; the laundry
  file's 営業所所在地 is in `ADDR_COLS`, but ⚠️ **the barber and beauty
  files' long address label is not, so `city_rows` reads 0 rows from them
  today**; ⚠️ **`OPERATOR_COLS` lacks 営業者の名称又は氏名** (without it the
  name rule compares nothing); ⚠️ **`TYPE_COLS` lacks
  クリーニング所又は取次所の別** (`japan_eigyo` keeps both kinds as Personal
  services either way, but the type is what the build records). The scratch
  measurement renamed all three in memory; the build adds them to the shared
  tuples (or a city-local `source_rows`) and re-runs the Minato control.
- ⚠️ **The beauty file repeats its header as its first data row** (its
  確認番号 cell reads 確認番号, its 検査確認日 is text, its address label a
  shorter variant). Once the address label is in `ADDR_COLS`, `xlsx_rows`
  takes row 2 as the header and yields the repeat as a row: drop it (a row
  whose 確認番号 is 確認番号). It is counted out of the 574 above.
- **One barber row is a mobile barber**: its address names a service area
  (two cities) and a vehicle depot in 鳥取県米子市, the shape the column's
  label allows; the shared mobile test (一円, 保健所管, 市内 alone) does not
  catch it, so it reaches no block today. Not a premises: set it aside
  city-locally (an address naming another prefecture), and the e-Stat share
  stays 98.5% on rows or 98.2% on premises (266). No beauty or laundry row
  has the mobile shape. ⚠️ Any new mobile test must not match the substring
  市内: 2 barber and 5 beauty addresses carry it only in 松江市内中原町 (内中原町
  is a town).
- **Dates**: 検査確認日 is an Excel date throughout (barbers 1948-05-07 to
  2026-02-16, beauty 1952-03-14 to 2026-07-14, laundries 1950-08-10 to
  2025-05-07). 確認番号 repeats (barbers 144 distinct of 266, beauty 188 of
  575, laundries 50 of 104, 4 empty): never a key alone; (確認番号,
  検査確認日) is unique in every file.
- **Repeats**: 0 by (address, trade name) in any file; by address alone 2
  barber, 10 beauty, 1 laundry (shared buildings). **15 premises are in both
  the barber and beauty registers** (one pin per premises and bucket keeps
  one per bucket).
- **Standing registers, re-issued whole each month.** The newest resource is
  the list; no months to merge (not Ichinomiya's shape: every month is
  complete). Whether a closed premises leaves the next month's list was not
  measured (the July resource was not downloaded): the page keeps "may
  include closed premises". 5 trade names (2 barber, 2 beauty, 1 laundry)
  name a hospital, a care home or a facility: read them at build against
  Sapporo's welfare-facility rule (which today reads a type, not a name).
- **The resource id changes every month** (76779 for August; July's was
  76656). `japan_fetch.current_url` has no rule for this portal: pin the
  three `resource_download` URLs in `SOURCE_FILES` with `SOURCE_AS_OF`
  2026-08-31 (the resource's own date, never today); a later edition is a
  new id and a re-measure.

### Food — left out

- **The city's own list** (`https://www.city.matsue.lg.jp/soshikikarasagasu/kenkofukushibu_hokeneiseika/hokeneisei/4/2226.html`,
  食品営業許可施設一覧(松江市内), updated 2026-09-08): the full list as of
  2026-05-31 (Excel 310.5 KB and PDF), refreshed every six months (May and
  November), with monthly new-permit files. It carries no open-data licence;
  the city's site terms (`…/matsueshiyakusho/3631.html`) reserve copyright
  and allow no use beyond private copying or quotation without permission.
  **Not requested** (the band row); not downloaded.
- **MHLW's file (32201)**, measured only:
  `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=32201_food_business_all.csv`:
  **178,802 B, 534 rows** (届出 471, 許可 63, none closed), permits
  2021-11-26 to 2026-07-22. **45 open restaurant permits, 1.9% of e-Stat's
  2,328 in force** (old law 640, revised 1,688). Open notifications 471,
  **256 addressed (54%)**, of which `japan_eigyo` buckets **126 as Retail**
  (その他の食料・飲料販売業, 百貨店・総合スーパー, 乳類販売, 野菜果物 …) and
  130 as nothing (集団給食 74, vending …). Under Iwaki's 164 addressed
  notifications, left out as too thin (call 150): **not proposed** on a
  personal-services page.
- **Economic Census control**: the 2021 census counts 835 飲食店
  establishments in 32201 (`docs/coverage_sweep/japan_universe_mhlw.csv`); no
  food layer, so no ratio.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/32201-24.0a.zip` (244,068 B,
42,488 rows, 1,453 of them 住居表示; **37,851 block keys**, 214 towns),
town-chōme `.../19.0b/32201-19.0b.zip` (8,911 B, **256** towns).
`japan.CITIES` entry at build: `"matsue": {"name": "松江市", "pref": "32",
"epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True, "wards":
["32201"]}`.

| Tier, today's shared code (columns renamed in memory) | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Barbers (266 premises) | **77.8%** | 20.3% | 1.9% |
| Beauty salons (574) | **82.2%** | 16.4% | 1.4% |
| Laundries (108) | **85.2%** | 12.0% | 2.8% |
| … クリーニング所 (27) / 取次所 (81) | 81.5% / 86.4% | 18.5 / 9.9 | 0.0 / 3.7 |
| **All personal services (948)** | **81.3%** (771) | **17.0%** (161) | **1.7%** (16) |

**The misses, read** (towns only, by `tiers.py`, `misses.py` and
`isjcheck.py` in the wave-5 scratch `brief_matsue/`):
- **Chōme tier, 95 in towns MLIT's block file does not carry at all.**
  MLIT keys blocks for 東出雲町 (26 towns), 玉湯町 and 宍道町, but **none for
  島根町, 美保関町, 八雲町 and 八束町, and 2 of 鹿島町's 12 大字**: the 2005
  merger's rural towns on the 島根半島 and the 大根島. Their **91 premises**
  (鹿島町 23, 美保関町 18, 島根町 17, 八束町 19, 八雲町 14) all take a 大字
  centroid (島根町野波, 八束町二子, 八雲町日吉, 美保関町森山 …). A 大字 here can
  be kilometres across; this is what call 145 discloses.
- **Chōme tier, 66 in towns MLIT carries whose 地番 it lacks**: 乃白町 5,
  大庭町 4, 田和山町 4, 朝日町 4, 鹿島町名分 3, 石橋町 2, 西忌部町 2, 千鳥町 2,
  竹矢町 2, 乃木福富町 2 …, Kakogawa's shape (MLIT keys a share of each
  town's lot numbers).
- **Unplaced (16)**: (a) **old addresses** from before 住居表示 or a town
  renaming, which MLIT no longer carries: `上乃木町` with a 4-digit 地番 (6;
  MLIT has 上乃木一丁目 to 十丁目 only), `上乃木町宇賀`, `西津田町阿弥田`,
  `西津田町美月` (MLIT has 西津田一丁目 to 十丁目), `古志原町` (2; MLIT has
  古志原一丁目 to 七丁目); (b) **towns absent from both MLIT files**:
  `白潟本町`, `南寺町`, `東出雲町磯近` (no number); (c) `八雲村東岩坂`, the
  pre-2005 village name for MLIT's 八雲町東岩坂 (an old-municipality rule);
  (d) `浜乃木―丁目`, a dash written for 一 (浜乃木一丁目); (e) `宍道町` with a
  地番 and no 大字. (c) and (d) are one shared rule each; the rest need GSI's
  address search or stay unplaced (open call 1). Follow any shared rule with
  the Minato control (`screen_japan_join.py minato` 98.0 / 0.2 / 1.8) and
  every city screen.
- **No own-point fallback**: the registers carry no coordinates and MHLW
  lists no salons, so call 127c has nothing to use.
- **Independent check** at build: GSI's address search on a sample
  (`screen_japan_join.py`'s `gsi_check`, Sendai's way: 150 rows, 1 request a
  second), weighted to the centroid tier.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_32_GML.zip`, N03 code 32201
(**572.9 km²**, extent W 132.875, S 35.330, E 133.352, N 35.606; the 2005
merger brought in 鹿島, 島根, 美保関, 八雲, 玉湯, 宍道 and 八束, the 2011 merger
東出雲). Read with `stub_test()`'s method and an in-memory `CITIES` entry
(scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 山陰線 (西日本旅客鉄道, 11) | JR San'in Main Line | **7 / 161** | 揖屋, 東松江, 松江, 乃木, 玉造温泉, 来待, 宍道 |
| 木次線 (西日本旅客鉄道, 11) | JR Kisuki Line | **2 / 18** | 宍道, 南宍道 |
| 北松江線 (一畑電車, 12) | Ichibata Electric Railway Kita-Matsue Line | **8 / 22** | 松江しんじ湖温泉, 松江イングリッシュガーデン前, 朝日ヶ丘, 長江, 秋鹿町, 松江フォーゲルパーク, 高ノ宮, 津ノ森 |

- **17 station records, 16 N02_005g groups** (宍道: San'in and Kisuki, one
  record pair at 0 m). No name in two groups; no pair closer than 600 m.
  **Median nearest-station gap 1,718 m** (1,197 to 4,153): rings by the
  spacing rule at build.
- **Shinkansen**: none.
- **Cut at the line** (named by N03 municipality at build): the San'in Line
  154 beyond (other prefectures 115, 大田市 10, 出雲市 8, 浜田市 8, 江津市 6,
  益田市 5, 安来市 2), the Kisuki Line 16 (雲南市 7, 奥出雲町 7, 広島県 2), the
  Kita-Matsue Line 14 (出雲市 14). 南宍道 sits 526 m inside the city line and
  津ノ森 538 m.
- **The light-rail/rail test**: all three are heavy rail: JR conventional
  (class 11) and the Kita-Matsue Line a private railway (class 12, 普通鉄道).
  No tram or light rail.
- **The stub test**: the Kisuki Line keeps 2 of 18 stations (宍道, its legal
  junction, and 南宍道), a JR line cut at the line: drawn as cut under the
  standing call, no owner question. Its label and legend entry on a short
  stretch: measure placement in a scratch render at build.
- **JR West, read 2026-10-06 from its own station timetables** for all 8 JR
  station groups (8 station index pages and 17 direction pages, every request
  HTTP 200, none refused) by plain GET with the project user-agent:
  `timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=<station>`
  lists a station's direction ids, `station-timetable/<id>?date=20261007`
  (a Wednesday) carries the table. **Method**: one departure per train entry
  on the PC table (each train once, marked trains included); the empty
  placeholder each train-less hour carries holds no minute and counts nothing
  (Akita's trap: counted on the Kisuki pages it would have read 15 for 10).
  Station ids: 揖屋 0640732, 東松江 0640733, 松江 0640734, 乃木 0640735,
  玉造温泉 0640736, 来待 0640737, 宍道 0640738, 南宍道 0641815.

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 揖屋 (San'in, to 松江 / to 米子) | 21 / 22 | 0-3 / 1-3 |
  | 東松江 (San'in, to 松江 / to 米子) | 21 / 22 | 0-3 / 1-3 |
  | 松江 (San'in, to 出雲市 / to 米子) | 44 / 45 | 2-3 / 2-4 |
  | 乃木 (San'in, to 出雲市 / to 松江) | 21 / 21 | 0-2 / 0-3 |
  | 玉造温泉 (San'in, to 出雲市 / to 松江) | 34 / 33 | 1-4 / 1-3 |
  | 来待 (San'in, to 出雲市 / to 松江) | 21 / 20 | 0-3 / 0-2 |
  | 宍道 (San'in, to 出雲市 / to 松江) | 39 / 38 | 1-3 / 1-4 |
  | 宍道 (Kisuki, to 木次) | 10 | 0-1 |
  | **南宍道 (Kisuki, to 宍道 / to 木次)** | **11 / 10** | 0-1 / 0-1 |

  **Named and drawn under call 86**: **the Kisuki Line from 宍道 to 南宍道,
  10 trains a day toward 木次 and 11 toward 宍道** (the longest weekday gap
  between 09:00 and 17:00 is about 3 hours). No San'in station is at or
  under about 11: the thinnest are 来待 (20 toward 松江) and 乃木, 揖屋 and
  東松江 (21), where some limited expresses pass. 松江's counts include the
  limited expresses that stop there.
- **Ichibata, read 2026-10-06 from its own station timetable PDFs** (the
  list page `https://railway.ichibata.co.jp/operate/timetable/list/` links one
  PDF per station, the files dated `P20250401`, the timetable revised
  2025-04-01): the eight stations inside the city, each HTTP 200. The PDFs'
  text carries minutes and hours only (the direction and day labels are
  images): each direction is a table with the hour in the middle, **weekday
  minutes left of it and holiday minutes right**, read so because the
  terminus 松江しんじ湖温泉 has one table and every through station two.
  Counted with `pdftotext -layout -fixed 1` (`ichicount.py`).

  | Station | Weekday departures (each direction) | Holiday |
  |---|---|---|
  | 松江しんじ湖温泉 (terminus) | 23 | 18 |
  | 松江イングリッシュガーデン前 | 23 / 23 | 18 / 19 |
  | 朝日ヶ丘 | 22 / 24 | 17 / 17 |
  | 長江 | 21 / 22 | 17 / 18 |
  | 秋鹿町 | 23 / 23 | 18 / 19 |
  | 松江フォーゲルパーク | 22 / 23 | 18 / 19 |
  | 高ノ宮 | 21 / 22 | 17 / 18 |
  | 津ノ森 | 23 / 23 | 18 / 19 |

  **About hourly, 21 to 24 a day each way: no station at or under about 11.**
  Which table is which direction is not readable from the text; the counts
  agree with the probe's reading (about 23 a day at the terminus).
- ⚠️ **Gate 3** at build: JR West's station counts inside the city (San'in
  7, Kisuki 2, 宍道 shared) and Ichibata's (8 of the line's 22 per its own
  list page; N02 also 22). **OSM `name:en`** for 16 groups (one Overpass
  query at build, in the box below; not queried here).

## Scope

**Matsue City.** The San'in Line runs on to 安来 and 米子 east and 出雲市 west,
the Kisuki Line to 雲南 and 奥出雲, the Kita-Matsue Line to 出雲市 (電鉄出雲市,
and 出雲大社前 by the Taisha Line from 川跡); cut at the line. ⚠️ The city's
extent (573 km², the 島根半島 north coast and the lake 宍道湖 inside it) is far
larger than its urban area: the opening view must fit the stations and
premises, not the N03 polygon (`map-view` at build).

## Licences — as read by staging

**松江市's registers on Shimane's portal: PERMITTED WITH CONDITIONS** (a
licence-read agent, 2026-10-06; staging records it in
`docs/decisions_drafts/staging.md`, "Wave 5, second half"; the build copies
the row into `docs/data_sources/japan.md` from staging's record). As staging
recorded it: **PDL 1.0** on these three resources (each resource page:
`PDL1.0（公共データ利用規約第1.0版）`; older resources and the portal's
catalogue CSV say CC BY), which also grants use under CC BY 4.0. **The
credit** names the creator organisation (**松江市**), the resource name
(【松江市】理容所一覧_20260831 and the other two) and the resource's URL
(`https://shimane-opendata.jp/resources/76779`, `…/76780`, `…/76781`), and
says this project processed the data. **Link `shimane-opendata.jp`, never
`city.matsue.lg.jp`** (the city's site terms ask to be told of links). A
fault-based own-cost clause (§3), accepted for all of Japan (2026-09-24). No
verdict is written in this brief beyond staging's record; take the exact
credit wording from it.

- **The city's food list**: site copyright, not used, not requested.
- **MHLW open data**: measured only; not a source on this page.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR West's and Ichibata's timetables**: read for counts only, never
  reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **営業者の名称又は氏名 holds a person or a company**: a company or
  cooperative marker on 31 of 267 barbers, 107 of 574 beauty salons and 83 of
  108 laundries; **the rest, 236, 467 and 25 rows, carry no marker** (the
  shape of a sole trader's own name). **代表者の役職及び氏名** (a company's
  representative, a person: filled on 33, 110 and 83 rows) and **営業者所在地**
  (the operator's own address, filled for companies) are never selected; the
  scratch dropped 営業者所在地 at read. 営業所電話番号 and 営業所郵便番号 are
  never selected. Select 営業所名称 and 営業所所在地 (and the laundry kind)
  only; read 営業者の名称又は氏名 in memory for the name rule (once it is in
  `OPERATOR_COLS`) and never write it.
- **The name rule, measured in memory** (answers only, never a value):
  **0** bare personal names among the 948 trade names; **0** trade names
  equal to their operator.
- Run `check_personal_exposure.py matsue` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Chugoku after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 132.875-133.352 E, centroid 133.069:
project to **UTM 53N (EPSG:32653)**. OSM box from the N03 extent, rounded
out: (35.32, 132.87, 35.61, 133.36). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B,
personal services only, food left out (call 96); the Kisuki Line drawn and
named (call 86); the tiers disclosed (call 145, applied); MHLW's
notifications left out as too thin (call 150, applied); `mode: metro`; the
minor tier and Japan West (Chugoku after the retag); no frequency floor;
downloads (call 147).

**Answered by the owner on 2026-10-06:** call 183, **built with the tiers disclosed** (call 145), the coordinates bullet stating both shares; call 184, **Ichibata's eight timetable PDFs approved for the build's gate 3** (counts only, never reproduced). The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **The block share, 81.3%, below Kakogawa's 86.5%** (the lowest a Japanese
   brief has carried to build). Call 145 covers it, but 91 premises (9.6%)
   sit at the centroid of a rural 大字 in the merged towns, where MLIT keys no
   block at all, and 16 (1.7%) are unplaced. *Recommend building with the
   tiers disclosed as call 145 says*, the coordinates bullet stating both
   shares; the tradeoff is pins in 島根町, 美保関町, 八雲町, 八束町 and 鹿島町 at a
   大字's centre against adding a per-row geocode (GSI's address search for
   the 177 rows, a new source with its own licence row), which would place
   most of them at their lot.
2. **Ichibata's eight timetable PDFs were read for counts without being
   named in call 147** (304,836 B, kept in the session scratchpad only, never
   in `data/`). Matsumoto's brief held Alpico's PDF back as unnamed. *Recommend
   keeping the counts above and approving the same PDFs for the build's gate
   3*; the tradeoff is one more source read against a frequency the page
   would otherwise mark ASSERTED.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `ADDR_COLS` + the two long address labels; `OPERATOR_COLS` +
  営業者の名称又は氏名; `TYPE_COLS` + クリーニング所又は取次所の別; optionally
  八雲村 → 八雲町 and `―丁目` → `一丁目`. City-local: drop the beauty file's
  repeated header row and the mobile barber row.
- `SOURCE_FILES` pinned to resources 76779, 76780, 76781 with
  `SOURCE_AS_OF` 2026-08-31; whether closed premises leave the monthly list
  (compare two months only if the owner approves a second month).
- The 5 facility-named salons and laundries (Sapporo's rule); the tier shares
  as built for the coordinates bullet (call 145); GSI's sample check.
- Gate 3 (JR West, Ichibata); OSM `name:en`; the Kisuki Line's label on its
  short stretch; line colours on both basemaps; the opening view (`map-view`,
  the polygon far larger than the urban area); `check_provenance.py`;
  `check_scope_disclosure.py` (food out, the laundry kinds kept).

```brief-checks
[
  {
    "id": "matsue-barber-resource",
    "claim": "Shimane's portal: resource 76779 is 松江市's barber list as of 2026-08-31, file 20260831riyousho.xlsx, under PDL 1.0",
    "kind": "http_contains",
    "url": "https://shimane-opendata.jp/resources/76779",
    "present": ["20260831riyousho.xlsx", "PDL1.0", "resource_download/76779"]
  },
  {
    "id": "matsue-beauty-resource",
    "claim": "Resource 76780 is the beauty-salon list as of 2026-08-31, file 20260831biyousho.xlsx, under PDL 1.0",
    "kind": "http_contains",
    "url": "https://shimane-opendata.jp/resources/76780",
    "present": ["20260831biyousho.xlsx", "PDL1.0", "resource_download/76780"]
  },
  {
    "id": "matsue-laundry-resource",
    "claim": "Resource 76781 is the laundry list as of 2026-08-31, file 20260831cleaning.xlsx, under PDL 1.0",
    "kind": "http_contains",
    "url": "https://shimane-opendata.jp/resources/76781",
    "present": ["20260831cleaning.xlsx", "PDL1.0", "resource_download/76781"]
  },
  {
    "id": "matsue-barber-dataset-newest",
    "claim": "The barber dataset (1254) still lists 76779 among its resources (a later month adds a new id: re-measure)",
    "kind": "http_contains",
    "url": "https://shimane-opendata.jp/datasets/1254",
    "present": ["resources/76779", "resource_bundle_download/1254"]
  },
  {
    "id": "matsue-barber-file",
    "claim": "The barber list (46,625 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://shimane-opendata.jp/resource_download/76779",
    "min_bytes": 40000
  },
  {
    "id": "matsue-beauty-file",
    "claim": "The beauty-salon list (102,585 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://shimane-opendata.jp/resource_download/76780",
    "min_bytes": 90000
  },
  {
    "id": "matsue-laundry-file",
    "claim": "The laundry list (26,360 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://shimane-opendata.jp/resource_download/76781",
    "min_bytes": 20000
  },
  {
    "id": "matsue-mhlw-live",
    "claim": "MHLW's open-data file for Matsue (32201) answers a plain keyless GET (measured, not a source)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=32201_food_business_all.csv",
    "min_bytes": 150000
  },
  {
    "id": "matsue-isj-block-live",
    "claim": "MLIT's block-level address file for Matsue (32201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/32201-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "matsue-isj-chome-live",
    "claim": "MLIT's town-chōme file for Matsue (32201) answers keyless - the centroid tier",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/32201-19.0b.zip",
    "min_bytes": 7000
  },
  {
    "id": "matsue-jr-matsue-directions",
    "claim": "JR West lists 松江's two San'in direction timetables (3278024001, 3278024002)",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0640734",
    "present": ["3278024001", "3278024002"]
  },
  {
    "id": "matsue-jr-minamishinji-directions",
    "claim": "JR West lists 南宍道's two Kisuki Line direction timetables (3381059001, 3381059002), the stretch named under call 86",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0641815",
    "present": ["3381059001", "3381059002"]
  },
  {
    "id": "matsue-ichibata-list",
    "claim": "Ichibata's timetable list page links the 2025-04-01 station PDFs read here, the terminus and 津ノ森 among them",
    "kind": "http_contains",
    "url": "https://railway.ichibata.co.jp/operate/timetable/list/",
    "present": ["P20250401new_22_matsueshinjikoonsen.pdf", "P20250401new_15_tsunomori.pdf"]
  },
  {
    "id": "matsue-projected-crs",
    "claim": "Matsue projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 133.07,
    "expect": "EPSG:32653"
  }
]
```
