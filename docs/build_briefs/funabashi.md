# Funabashi — build brief

**Band B, personal services only, owner-approved 2026-10-04** (Japan's third
wave; the Step 0 downloads approved 2026-10-05, staging's call 10,
`docs/decisions_drafts/staging.md`, "Band B's licence terms accepted, the
briefs' calls made, the Japanese Band B briefs and a Hamburg re-check
approved"). **Step 0 measured 2026-10-05** (staging). Downloaded, each from
its publisher's own host, into `data/funabashi/raw/` (gitignored), named as
the publisher serves them:

- From `data.bodik.jp` (one `package_show` per dataset, then each file once,
  every BODIK request 16 s or more apart, each HTTP 200; no 403, 429 or 5xx):
  `riyouroichiranall.csv` (43,498 B), `biyouroichiranall1.csv` (182,360 B),
  `kurininngu202607.csv` (47,069 B). Each dataset holds **one resource and no
  other** (no earlier monthly file, no closure file), so the conditional part
  of the approval (earlier or closure resources in the same datasets) fetched
  nothing.
- From `nlftp.mlit.go.jp`: `isj/12204-24.0a.zip` (280,138 B) and
  `isj/12204-19.0b.zip` (9,646 B).
- Not fetched: MHLW's file (12204), since food is off and no control needed
  it; the three other 生活衛生 datasets in the same family (below, findings).

**Run `python scripts/brief_check.py funabashi` before writing any code.**
Then the `japan-city` skill, **Kōchi's shape** (personal services only, a
full list per kind; `docs/build_briefs/kochi.md`, `pipeline/kochi/config.py`).
Unlike Matsudo and Ichikawa (Chiba Prefecture's lists, cut by address), the
publisher here is **the city itself**: Funabashi is a 中核市 with its own
health centre, which is why the prefecture's dataset 6 leaves it out.
Coordinates: the `address-join` skill, measured with the shared
`pipeline/countries/japan_register.py` functions from scratch scripts
(`scripts/screen_japan_join.py` has no Funabashi entry; add one at build).
Rail: MLIT N02-25 cut at the N03 city line, measured through
`pipeline/countries/japan.py` with a scratch `CITIES` entry (none was added to
the shared module).

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to
the owner (open call 1); (4) **菓子製造業 and そうざい製造業 count, in Retail**
(2026-09-24; moot on a personal-services page); (5) **the name rule**: where
the trade name IS the operator's own name, the pin shows its permit type, the
operator column read in memory only (2026-09-27); MHLW's 法人名 joins it for
every MHLW city (2026-10-05; moot here, no MHLW source); (6) **no page says
"currently operating"**. Also: fault-based cost clauses accepted for all of
Japan (2026-09-24), and Funabashi's clause ５ accepted by name (below);
English station names from OSM `name:en`, numerals as figures before 丁目;
every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Funabashi carries `label_tier: "minor"` and goes in the **Japan East** view,
as Utsunomiya, Maebashi and the other Kantō cities do (`app/cities.py`; wave
4's first city retags Japan into the eight regions, Funabashi into Kanto). Its
label offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and
1200), never by eye. Funabashi's centroid sits about 8 km from Ichikawa's and
16 km from Matsudo's: measure the three labels together if they land in one
batch, and against Tokyo's.

**`mode`: `metro`.** Tokyo Metro's Tōzai Line runs inside the city (2 station
groups), so the city is `metro` without the JR test (Ichikawa's reading). The
mode holds if the owner leaves the Tōzai out (open call 1): JR is not the
largest network inside the city (6 groups against Keisei's 16), so the
backbone rule of 2026-10-02 gives `metro` as well.

---

## The one-line summary

**Personal services only, from the city's own CC BY 4.0 registers on BODIK:
314 barbers and 965 beauty salons as of 2026-08-01, 214 laundry rows (202
premises) as of 2026-07-01; 1,493 storefronts in the city, 1,473 pins, placed
at the block 99.8%, none unplaced.** Against e-Stat's FY2024 count for the
city (2025-03-31): barbers 94.9%, beauty 100.5%, laundries 97.3% by rows
(91.8% by premises). Each file is a snapshot (no closure column, no history
kept on the catalogue). Food stays off (the master list: MHLW's file holds
3,220 open restaurant permits, 70% of the 4,616 in force, but only 52.4%
publish an address). Rail: **30 N02 station groups** (Keisei 16, JR 6, Tōyō
Rapid 5, Tōbu 4, Tōzai 2, Hokusō 1; the master list's "JR 8" counts JR per
line: Sōbu 4, Keiyō 2, Musashino 2).

---

## Business leg — the city's 生活衛生関係営業施設一覧 (BODIK organisation 122041)

| | Barbers | Beauty salons | Laundries |
|---|---|---|---|
| **Dataset** | `https://data.bodik.jp/dataset/122041_20260401_seikatsueisei-eigyoushisetsu_riyousyo` | `…_biyousyo` | `…_kuri-ninngu` |
| **Title** | 生活衛生関係営業施設一覧（理容所） | （美容所） | （クリーニング所） |
| **Resource name** | `20260801_生活衛生関係営業施設一覧（理容所）.csv` | `20260801_…（美容所）.csv` | `20260701_…（クリーニング所） .csv` |
| **File** | `…/dataset/deb35006-3f85-4626-a2ea-c65823dae612/resource/73e5f3c8-4a05-4056-9f00-2b6b249402ce/download/riyouroichiranall.csv` | `…/dataset/89b146c9-d7c4-4820-921e-edeee4f396d9/resource/ff85f1bb-95c1-42f4-b176-8c4c5b43f50d/download/biyouroichiranall1.csv` | `…/dataset/f75f7b70-0657-4188-9ffa-ccecec143a6b/resource/acc812a0-ba5e-4cf1-bdd2-13d8556d8d75/download/kurininngu202607.csv` |
| **Bytes** (catalogue = served) | 43,498 | 182,360 | 47,069 |
| **Rows** | **314** | **969** | **215** |
| **As of** (resource name) | **2026-08-01** | **2026-08-01** | **2026-07-01** |
| Newest 確認（許可）日 | 2026-05-08 | 2026-07-21 | 2026-05-19 |
| Rows confirmed after 2026-03-31 | 1 | 18 | 1 |
| Resource created / file replaced | 2026-04-17 / 2026-09-28 | 2026-04-20 / 2026-09-28 | 2026-04-17 / 2026-08-13 |
| `frequency` extra | 不定期 | １か月 | (blank) |
| Datastore | active | active | active |

- **Format**: UTF-8 with BOM, comma-separated, CRLF, one header row, every
  row 9 cells. `city_rows` reads all three as they are.
- **Columns** (the same nine in all three): **業態**, **施設_名称**,
  **施設所在地**, 施設電話番号, **申請者_氏名** (the operator), **代表者_氏名**
  (a company's representative), 申請者所在地, 申請者電話番号, 確認（許可）日.
- **業態 is the kind and holds one value per file**: 理容所 314, 美容所 969,
  クリーニング業 215. ⚠️ `japan_register` reads 業態 as a FORM column, not a
  TYPE column (`TYPE_COLS` has no 業態), so every row reads type "". The
  bucket is still right (`japan_eigyo` decides Personal services by source),
  but the name rule's pin shows the TYPE: the scratch measure copied 業態 into
  業種. At build, `source_rows` maps it (or `TYPE_COLS` gains 業態, a shared
  change with the Minato control; Fukuoka's and MHLW's 業態 is a form, so the
  `source_rows` route is the safer one).
- **The laundry list carries no kind**: no 取次所 / 無店舗取次店 / リネン column
  (Matsudo's クリーニング種別１ has no counterpart here), so a storeless pick-up
  or a linen plant cannot be told apart by type. No row's name or address
  carries 無店舗, リネン or 移動; 8 names carry 工場 (each a company's), kept as
  laundries as Matsudo kept its 洗い場.
- **Dates**: 確認（許可）日 in the era-letter dot form without padding
  (`H1.1.30`, `S63.8.11`); `japan_register.wareki_date` reads H and R and
  returns None for every Shōwa date (80 barber, 89 beauty, 29 laundry rows).
  Nothing in the build reads it (no expiry on a 生活衛生 confirmation).
- **Its notes**: mobile phone numbers (premises and operator) were removed as
  likely personal information; characters outside Shift-JIS in the trade
  name, operator or representative are shown as 「・」. 16 barber, 36 beauty
  and 3 laundry trade names contain a 「・」 (some are real punctuation):
  `_name_key` strips 「・」, so the rule's comparison is unaffected, but the pin
  shows it (`cjk-text`).

### Snapshot, not rebuild

Each dataset is **one resource replaced in place** (created April 2026, the
file swapped since: the dataset ids say 20260401, the resource names
20260801 and 20260701). The catalogue keeps no earlier edition and no closure
file, and no row carries a closure field. So each file is **a snapshot of the
premises on file at its date**: a premises closed before then is presumably
gone from it, one closed after is invisible until the next file. Not an upper
bound in Kyoto's sense; the page's standard "may include premises that have
closed" covers it. **No dataset states that any premises are withheld** (no
consent filter, unlike Chiba Prefecture's and Maebashi's).

### Rows that are not Funabashi premises

| | Barbers | Beauty | Laundries |
|---|---|---|---|
| Address starting 千葉県船橋市 | 314 | 966 | 214 |
| Address naming another municipality | 0 | **3** (市川市, 鎌ケ谷市, 佐倉市) | **1** (八千代市) |
| Address that is the city's name alone | 0 | **1** | 0 |
| **In-city storefronts** | **314** | **965** | **214** |

- Every address starts with the prefecture (`千葉県船橋市…`), and none uses
  丁目: the lists write `町名1-2-3`.
- **Four rows name another municipality** in 施設所在地. Funabashi's health
  centre licenses only Funabashi, so these are probably a wrong address in
  the premises column; either way they are not on this map. A
  `source_rows` that keeps addresses starting `千葉県船橋市` drops them.
- **One beauty row's address is `千葉県船橋市` and nothing else.**
  `permits_from_rows` does not flag it (its `citywide` rule matches only
  `…市内`), so it reaches the join as town "" and falls unplaced. Count it as
  not a premises in `source_rows` (a salon with no address: possibly a
  visiting service, read at build).
- No 移動, 一円 or 訪問 in any address or name; no welfare-facility salon by
  name (病院, ホーム, 厚生, 施設内: none in barbers or beauty).

### Counts that matter (in-city rows)

| Kind | Storefronts | Repeated (address, trade name) | Pins |
|---|---|---|---|
| 理容所 (barbers) | **314** | 0 | |
| 美容所 (beauty) | **965** | 0 (11 addresses hold two different salons) | |
| クリーニング業 (laundries) | **214** | **12** (below) | |
| **Personal services** | **1,493** | | **1,473** |

- **One pin per premises and bucket**: 8 (address, trade name) pairs are a
  barber and a beauty salon at one premises under one name (e-Stat's
  重複開設; FY2024 counts 1 for the city), and 12 laundry rows repeat, so
  step 2 draws **1,473 pins**.
- ⚠️ **One laundry address holds 15 rows**: 11 under one trade name and 3
  under another (each group with one confirmation date, its operator blank,
  so a person), plus 1 company's. Either duplicated records or several
  registrations at one base; e-Stat counts 18 無店舗取次店 operators in the city
  apart from its 220 facilities, so these may be storeless pick-ups
  registered at the operator's own address. One pin per (address, name)
  already collapses them to 3. **Read them at build, in memory**: if they are
  storeless (or the address is a home), drop the two groups as not premises
  (and the privacy check must see them; a person's address with a pin is the
  case the name rule exists for).
- `japan_eigyo` buckets every row Personal services; nothing falls out by
  rule.

### Coverage — against e-Stat's count for the city

Funabashi is a 中核市, so 衛生行政報告例 FY2024 第10表 (理容・美容) and 第11表
(クリーニング) carry its own row, 千葉県船橋市
(`data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, on disk, read here, not downloaded):

| Kind | Official FY2024 (2025-03-31) | The city's list (in-city) | Share | Same date? |
|---|---|---|---|---|
| 理容所 | **331** | **314** (2026-08-01) | **94.9%** | 16 months later |
| 美容所 | **960** (重複開設 1) | **965** (2026-08-01) | **100.5%** | 16 months later |
| クリーニング所 (施設) | **220** (取次所 151, 指定洗濯物 4) | **214** rows, **202** premises (2026-07-01) | **97.3%** rows, **91.8%** premises | 15 months later |
| 無店舗取次店 (operators, not premises) | 18 | (not separable) | | |

- **Barbers read 94.9%** (17 fewer) on a list 16 months younger than the
  count, with no withholding stated: consistent with closures (barbers are a
  shrinking trade), not a defect of the list. Beauty's 100.5% says the city's
  lists are complete registers. Stated on the page as numbers if the template
  asks for a share; otherwise no call (open call 3 covers the wording).
- **Laundries: 91.8% by premises** if the 12 repeated rows are one premises
  each, as the pin rule treats them. No call needed below Maebashi's 82%
  (built and stated, owner 2026-10-05).
- FY2025's tables, when e-Stat publishes them, are a closer control (a year
  nearer the files).

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 12204)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12204-24.0a.zip` (280,138 B) and
`…/19.0b/12204-19.0b.zip` (9,646 B): **22,805 block keys, 327 town-chōme
keys.** One municipality, no wards (`"wardless": True`). Measured with
`japan_register` and `WAVE2_RULES` unchanged (no Minato re-run needed), on
the 1,493 in-city storefronts:

| Tier | Barbers (314) | Beauty (965) | Laundries (214) | All (1,493) |
|---|---|---|---|---|
| Block | **99.7%** (313) | **100.0%** (965) | **99.1%** (212) | **99.8%** (1,490) |
| Town-chōme centroid | 0.3% (1) | 0 | 0.9% (2) | 0.2% (3) |
| Unplaced | 0 | 0 | 0 | **0** |

- **The shifted-chōme rule carries it**: the lists write `町名1-2-3` without
  丁目, and 1,403 of 1,493 rows take `join_city`'s chōme shift (barbers 295,
  beauty 920, laundries 188); one beauty row uses rule C's affix.
- **Chōme tier**: 高野台5丁目 (a barber), 海神町南1丁目 and 印内3丁目 (two
  laundries), each "block not in file". Read them at build.
- Before the in-city filter, the four out-of-city rows and the city-name-only
  row are the only misses (5 of 1,498): the filter is what makes it 0.
- **Independent check**: the lists carry no coordinates. GSI's address search
  on a sample at build (`screen_japan_join.py`'s `gsi_check`, 150 rows, one
  request per second).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (12204)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_12_GML.zip`, N03 code 12204
(85.6 km²; extent W 139.9387, S 35.6562, E 140.0897, N 35.7997). **38 station
records inside, 30 `N02_005g` groups**; no name in two groups. N02-24 and
N02-25 agree on every station here; use N02-25.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | First beyond the line |
|---|---|---|---|---|
| 松戸線 (京成電鉄, 12) | Keisei Matsudo Line | **9 / 24** (38%) | 二和向台, 三咲, 滝不動, 高根公団, 高根木戸, 北習志野, 習志野, 薬園台, 前原 | 鎌ヶ谷大仏 (鎌ケ谷市, 0.1 km), 新津田沼 (習志野市, 0.1 km) |
| 本線 (京成電鉄, 12) | Keisei Main Line | 7 / 42 | 京成中山, 東中山, 京成西船, 海神, 京成船橋, 大神宮下, 船橋競馬場 | 鬼越 (市川市, 0.5 km), 谷津 (習志野市, 0.5 km) |
| 総武線 (東日本旅客鉄道, 11) | JR Sōbu Line | 4 / 48 | 下総中山, 西船橋, 船橋, 東船橋 | 津田沼 (習志野市, **0.0 km**), 本八幡 (市川市, 1.5 km) |
| 東葉高速線 (東葉高速鉄道, 12) | Tōyō Rapid Railway Line | **5 / 9** (56%) | 西船橋, 東海神, 飯山満, 北習志野, 船橋日大前 | 八千代緑が丘 (八千代市, 0.6 km) |
| 野田線 (東武鉄道, 12) | Tōbu Urban Park Line | 4 / 35 | 船橋, 新船橋, 塚田, 馬込沢 | 鎌ヶ谷 (鎌ケ谷市, 1.0 km) |
| 京葉線 (東日本旅客鉄道, 11) | JR Keiyō Line | 2 / 19 | 西船橋, 南船橋 | 二俣新町 (市川市, 0.3 km), 新習志野 (習志野市, 0.7 km) |
| 武蔵野線 (東日本旅客鉄道, 11) | JR Musashino Line | 2 / 27 | 船橋法典, 西船橋 | 市川大野 (市川市, 2.1 km) |
| 5号線東西線 (東京地下鉄, 12) | Tokyo Metro Tōzai Line | **2 / 23** (9%) | 原木中山, 西船橋 (its eastern terminus) | 妙典 (市川市, 1.8 km) |
| 北総線 (北総鉄道, 12) | Hokusō Line | **1 / 15** (7%) | 小室 | 白井 (白井市, 1.1 km), 大町 (市川市, 2.4 km) |

- **30 groups by operator**: Keisei 16, JR 6, Tōyō Rapid 5, Tōbu 4, Tokyo
  Metro 2, Hokusō 1 (34 operator memberships across 30 groups). The master
  list's "JR 8" counts JR per line; the total, 30, is the same.
- **Interchanges N02 groups**: 西船橋 (JR's three lines, Tōzai, Tōyō; 159 m),
  船橋 (JR, Tōbu; 49 m), 北習志野 (Keisei, Tōyō; 40 m). **Kept apart, as N02
  keeps them** (trap 1): JR's 船橋 and 京成船橋 (217 m), 京成中山 and JR's
  下総中山 (318 m), each a walking interchange under two names. Median gap to
  the nearest group **777 m** (closest pair 217 m): standard rings (the
  spacing rule halves them at about 550 m or less).
- **An urban line cut to a stub (open call 1)**: **the Tōzai Line keeps 2 of
  23** (原木中山 and 西船橋, its eastern terminus; the rest runs through
  Ichikawa and central Tokyo). It is a subway, so the standing call does not
  settle it: **the same question as Ichikawa's open call 1** (the Tōzai 3 of
  23 there), one answer serving both.
- **One-station stub, kept as cut (standing call)**: **the Hokusō Line at
  小室 (1 of 15)**, a commuter railway (class 12) through Chiba New Town, not
  an urban line, as Matsudo's and Ichikawa's briefs treat it. 小室 is served
  by no other line, so its ring exists through this stub alone. The Keisei
  Narita Sky Access runs on the Hokusō track past 小室 without stopping (its
  timetable lists only 普通 and 特急 there, with connections to the アクセス特急
  at 新鎌ヶ谷 and 印旛日本医大); N02 has no Sky Access station inside, so step 1
  needs no entry for it.
- **Stub test, the rest**: the Keisei Matsudo Line keeps 9 of 24 in one run
  (鎌ヶ谷大仏 to 前原; Matsudo's 8 are the other end), the Tōyō Rapid 5 of 9,
  the Keisei Main Line 7 of 42, the Tōbu Urban Park Line 4 of 35 (its western
  terminus, 船橋). None is a stub; nothing else goes back to the owner.
- ⚠️ **津田沼 sits on the city line** (0.0 km, in 習志野市 by N03), and
  新津田沼 0.1 km beyond: out by the standing call, so the Sōbu Line's and the
  Matsudo Line's ends inside Funabashi sit next to an unringed major station.
  Listed in `excluded_stations.csv` like any cut station.
- ⚠️ **Services over N02's legal lines (trap 2)**: N02's 総武線 carries the
  Chūō-Sōbu local (all four) and the Sōbu Rapid (船橋 only here). **Tokyo
  built JR East's Sōbu services as routes; reuse them** (and Tokyo's public
  names for the Tōzai Line).
- ⚠️ **N02's 京葉線 (trap 3)**: 南船橋 is on the main line; 西船橋 is reached
  by the branches the Musashino Line's through trains use. Read the sections
  at build and split or route them as Ichikawa's build does (its brief has
  the same item); the Musashino through trains need no line of their own.
- **Tōzai and Tōyō through-running** (ASSERTED): the Tōyō Rapid's trains run
  through onto the Tōzai Line at 西船橋. N02 files them as two lines; draw
  them as two, each under its own public name.
- **The Shinkansen**: no station inside.
- **The light-rail / rail test**: one subway line (Tokyo Metro) makes the city
  `metro`; the rest are railways (classes 11 and 12). No tram or light rail.
- **Frequency** (no floor applies to JR or private lines in Japan): read for
  the line most likely to raise the question, **the Hokusō at 小室**, by curl
  from the timetable the operator's own station page links
  (`https://www.hokuso-railway.co.jp/railway/station/komuro.html` →
  `https://hokuso.ekitan.com/jp/pc/T5?USR=PC&dw=0&slCode=200-11&d=1` and
  `&d=2`, the operator's timetable service, titled 「時刻表 | 北総鉄道」;
  weekday, 「2025年12月13日現在」): **86 departures toward 京成上野・押上・羽田**
  (5:09 to 0:00) and **87 toward 印旛日本医大** (5:42 to 0:35); **three an hour
  each way from 10:00 to 15:59** (about every 20 minutes), five to nine an
  hour at the peaks. **ASSERTED, not read**: JR, Keisei, Tōbu, the Tōzai and
  the Tōyō Rapid run several trains an hour through Funabashi.
- **Gate 3**: the Hokusō's site links **14 station pages** (all its stations
  but 京成高砂, Keisei's), as N02 has 15 with 京成高砂. JR East, Keisei, Tōbu,
  Tokyo Metro and the Tōyō Rapid at build.
- ⚠️ **OSM `name:en`** for the 30 groups at build (no Overpass at Step 0): one
  station query in the N03 box. Read every name: 飯山満 (Hasama), 二和向台,
  滝不動, 高根公団, 船橋日大前, 大神宮下, 船橋競馬場 (OSM may translate it:
  Fukuoka's trap), 京成西船, 原木中山, and the Keisei Matsudo Line's stations,
  renamed from Shin-Keisei in 2025 (OSM may carry the old operator or line
  name).

## Scope

**Funabashi City (12204), one municipality, no wards.** The lines run on into
Ichikawa, Narashino, Kamagaya, Yachiyo, Shiroi and Tokyo; cut at the line,
the stations beyond named by N03 municipality at build
(`excluded_stations.csv`). Ichikawa and Matsudo are their own pages
(`ichikawa.md`, `matsudo.md`): the Tōzai's 妙典, Keisei's 鬼越, JR's 本八幡,
二俣新町 and 市川大野 belong to Ichikawa; the Keisei Matsudo Line's other 8
stations to Matsudo.

## Licences — as read (the full read is recorded)

- **The city's three registers**: read 2026-10-05 (`docs/decisions_drafts/
  staging.md`, "Maebashi's two BODIK lists read: permitted with conditions;
  one label conflict", the Funabashi bullet; that entry is the verdict, this
  brief only cites it). As declared: all three datasets `cc-by-40-intl`
  (`package_show` and `package_search`, 2026-10-05); 船橋市オープンデータ利用規約
  (`https://odcs.bodik.jp/122041/tos/`) ２ grants CC BY 4.0 「注記があるものを除いて」,
  and no 注記 was found. What it requires of the build, as recorded there:
  - **MUST DISPLAY** the prescribed 改変 form,
    「この[作品・アプリ・データベース等]は以下の著作物を改変して利用しています。[タイトル]、船橋市、クリエイティブ・コモンズ・ライセンス表示 4.0（URL）」.
    Proposed, for the notice:
    `この地図は以下の著作物を改変して利用しています。生活衛生関係営業施設一覧（理容所）、生活衛生関係営業施設一覧（美容所）、生活衛生関係営業施設一覧（クリーニング所）、船橋市、クリエイティブ・コモンズ・ライセンス表示 4.0（https://creativecommons.org/licenses/by/4.0/deed.ja）`
    (the licence URL may be a hyperlink on the words, as ２ allows).
  - **Links**: label any link as going to the city's catalogue (３:
  「本ページへのリンクである旨を明示」), and never frame it. **Link the
    catalogue (`odcs.bodik.jp/122041` or the `data.bodik.jp` dataset pages),
    never the city website**, whose link-notification request covers
    city-site links only.
  - **No completeness, accuracy or currency claim** (４). **Clause ５**
    (reimbursing the city's costs, judgments included, arising from the
    user's own breach or infringement): **accepted by the owner 2026-10-05**
    (calls 12 and 30, the fault-based class).
- **Not fetched, so not governing**: the city website's copyright page.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.
- **MHLW open data**: not used (food is off).
- **The brief checks make one BODIK request** (a single `package_search`
  covering all three datasets) so that a run never puts two BODIK requests
  less than 15 s apart (owner, 2026-10-05). The terms page on
  `odcs.bodik.jp` is therefore not re-checked by `brief_check.py`: re-read it
  by hand at build, 15 s or more after any other BODIK request.

## Privacy

Read only the trade name, the kind (業態) and the premises address. **No row
value was printed or stored for this brief**: every count comes from
in-memory comparisons.

- **The city publishes the operator only where it is a company.**
  **申請者_氏名** is filled on 52 barber, 400 beauty and 139 laundry rows,
  **every one with a company or cooperative marker** (`NOT_A_PERSON`), and
  blank on the other 262, 569 and 76; 申請者所在地 and 申請者電話番号 follow the
  same pattern. So the rule's comparison sees companies only, and a company
  is never an individual: **the name rule cannot see a sole trader here**
  (open call 2).
- **代表者_氏名 is a person's name** (a company's representative), filled on
  52 / 402 / 139 rows (2 beauty rows carry one with no operator). It is not in
  `japan_register.OPERATOR_COLS` (which has 代表者氏名 and 代表者, not the
  underscore spelling); **add `代表者_氏名` at build** so the rule compares a
  salon named after its company's representative (then the Minato control).
  `申請者_氏名` is already there.
- **The name rule flags 0 rows** in the 1,498, with OPERATOR_COLS as it is or
  with 代表者_氏名 added; no trade name contains a representative's name.
- **The blind spot, measured (open call 2)**: among the 907 rows with no
  operator, **5 trade names (1 barber, 2 beauty, 2 laundries) are 2 to 5
  kanji with no business word**, the shape of a bare personal name (some may
  be place names; not read).
- **Never selected**: 施設電話番号, 申請者所在地 (a company's address),
  申請者電話番号; 申請者_氏名 and 代表者_氏名 beyond the rule's in-memory
  comparison.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0, and **the verdict must say it is blind where the operator
  is blank** (907 of 1,498 rows), and what was done about the 5 shapes and
  the 15-row laundry address.

## Region

`"region": "Japan East"`, `"country": "Japan"`, `label_tier: "minor"`.
Project to **UTM 54N (EPSG:32654)**: the city's centroid lies at longitude
140.019 and its western edge at 139.9387, both inside the 138-144 band
(computed here, never copied).

**Scaffold**: `scaffold_city.py --slug funabashi --name Funabashi
--system-name "Keisei, JR East, Tōyō Rapid, Tōbu, Tokyo Metro and Hokusō"
--taxonomy japan_eigyo --lat 35.727 --lon 140.019 --region "Japan East"
--country Japan --mode metro --page-number <N>` (`--dry-run` first), with the
page number claimed in `docs/session_roles.md` at build, not here. A
`japan.CITIES` entry: `"funabashi": {"name": "船橋市", "pref": "12", "epsg":
32654, "n02": "25", "rules": WAVE2_RULES, "wardless": True, "wards":
["12204"]}`.

## Findings — recorded, not downloaded

- **The same family's other three datasets** on BODIK (one `package_search`,
  2026-10-05; each `cc-by-40-intl`, one resource each): 公衆浴場
  (`122041_20260401_seikatsueisei-eigyoushisetsu_kousyuuyokujyou`,
  `kousyuuyokujyou202607.csv`, 8,079 B by the catalogue), 旅館・ホテル・簡易宿所
  (`…_ryokann`, `ryokann2026071.csv`, 20,313 B, as of 2026-07-01) and 興行場
  (`…_kougyoujyou`, `20260401_seikatsueisei-eigyoushisetsu_kougyoujyou.csv`,
  1,798 B, as of 2026-04-01). None is a storefront type on any Japanese page
  so far; not proposed.
- **Food** (the master list's numbers, not re-measured): MHLW 12204 (3,220
  open restaurant permits, 52.4% addressed) and BODIK's old-law food list (at
  most 704 restaurants). Food stays off by the owner's band.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-04); the Step 0
downloads (owner, 2026-10-05, call 10); the city's licence read (2026-10-05)
and clause ５ accepted (owner, 2026-10-05, calls 12 and 30); the standing
Japanese calls above; the minor label tier and the Japan sub-region (owner,
2026-10-02); `metro` (a subway inside, Ichikawa's reading; the backbone rule
agrees); the Hokusō Line at 小室 kept as cut by the standing call (a commuter
railway, not an urban line).

**Open:**

1. **The Tōzai Line cut to 2 of 23** (原木中山, 西船橋). An urban line cut to a
   stub goes back to the owner; it is Ichikawa's open call 1 (Tōzai 3 of 23
   there), and one answer should serve both. Recommendation: **draw it as
   cut**, labeled and in the legend, as the city-line rule draws JR. 西船橋 is
   a ring through JR and the Tōyō Rapid anyway, and 原木中山 is served by no
   other line. Tradeoff: a subway drawn only from its terminus to the city
   line (妙典 lies 1.8 km beyond) reads oddly, against leaving it out, which
   loses 原木中山's ring and the Tōzai's label at its own terminus.
2. **The name rule cannot see a sole trader**: the city leaves the operator
   blank wherever it is a person (907 of 1,498 rows), so the rule compares
   companies only and flags 0. Recommendation: **build it, and apply the
   Liège / Brussels rule to the 5 trade names shaped like a bare personal
   name** (a sign that reads as a person's name shows its category; owner,
   2026-10-05, call 15, for Gelsenkirchen), read in memory at build; the
   page's name-rule bullet takes a variant (a proposal: "The city's lists
   name the operator only where it is a company; where a trade name reads as
   a person's name, the dot shows its permit type instead."). Tradeoff: a
   shape heuristic may hide a few real shop names (a place name in kanji),
   against Fukuoka's acceptance for MHLW's rows (no operator column, nothing
   done), which leaves the 5 as they are.
3. **Page wording**: the one-bucket bold line is approved (Yokohama's,
   Hakodate's: "**This map shows personal services only: barbers, beauty
   salons and laundries.**"), but Hakodate's next sentence ("publishes … no
   register of food businesses") is untrue here: Funabashi's food lists exist
   and are off on coverage (MHLW's addresses). A sentence outside the
   template, a proposal for the drafts file at build. Recommendation: "From
   Funabashi City's registers of barbers and beauty salons (as of August 1,
   2026) and of laundries (as of July 1, 2026). Restaurants, cafés and shops
   are not on this map: the national food-permit filings publish too few
   addresses here to place them." Plus, if the template wants the laundry
   share, Maebashi's answer (state it as a number).

## What the build must still measure

- The Kōchi config shape: `SOURCE_FILES` for the three resources (URLs
  above; the barber and beauty file names do not change between editions,
  so pin each edition by its resource name date and size, as the brief check
  does), `SOURCE_AS_OF` per kind (2026-08-01, 2026-08-01, 2026-07-01, or the
  newer editions' dates), `REQUIRED_COLUMNS` naming 業態, 施設_名称, 施設所在地,
  申請者_氏名 and 代表者_氏名, and a **`source_rows`** that keeps addresses
  starting `千葉県船橋市` with something after it (314 / 965 / 214 on these
  files), counts the city-name-only row as not a premises, and carries 業態
  as the type. Fail if the counts drift without a new file.
- ⚠️ **Shared code**: `OPERATOR_COLS` += 代表者_氏名, then the Minato control
  (`screen_japan_join.py minato`, 98.0 / 0.2 / 1.8) and every city screen.
- **The 15-row laundry address** (11 + 3 + 1), read in memory: duplicates,
  storeless pick-ups or a home; and the 5 bare-name shapes (open call 2).
- The newest edition of each file (BODIK replaces them in place; barbers
  「不定期」, beauty monthly).
- The 3 chōme-tier rows; GSI on a sample.
- Gate 3 for JR East, Keisei, Tōbu, Tokyo Metro and the Tōyō Rapid; N02's
  京葉線 sections at 西船橋; JR's Sōbu services as Tokyo's routes; OSM `name:en`
  for 30 groups; line colours on both basemaps (9 lines, four meeting at
  西船橋).
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`)
  measures 飲食店, which this page does not carry; e-Stat's per-city 生活衛生
  counts (above) are the control here. Record them at build.

```brief-checks
[
  {
    "id": "funabashi-bodik-packages",
    "claim": "One BODIK request (the owner's 15 s spacing): the city's three 生活衛生 registers still declare cc-by-40-intl and still serve the editions measured 2026-10-05 (barber 43,498 B and beauty 182,360 B, both 2026-08-01; laundry kurininngu202607.csv 47,069 B, 2026-07-01). A changed size means a new edition: re-measure. ASCII strings only: the API escapes Japanese as unicode escapes",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:122041+name:122041_20260401_seikatsueisei-eigyoushisetsu*&rows=10",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "122041_20260401_seikatsueisei-eigyoushisetsu_riyousyo", "122041_20260401_seikatsueisei-eigyoushisetsu_biyousyo", "122041_20260401_seikatsueisei-eigyoushisetsu_kuri-ninngu", "73e5f3c8-4a05-4056-9f00-2b6b249402ce/download/riyouroichiranall.csv", "ff85f1bb-95c1-42f4-b176-8c4c5b43f50d/download/biyouroichiranall1.csv", "acc812a0-ba5e-4cf1-bdd2-13d8556d8d75/download/kurininngu202607.csv", "\"size\": 43498", "\"size\": 182360", "\"size\": 47069"]
  },
  {
    "id": "funabashi-isj-live",
    "claim": "MLIT's block-level address file for Funabashi (12204) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12204-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "funabashi-hokuso-stations",
    "claim": "The Hokusō Railway's own site links its 14 station pages (all 15 N02 stations but Keisei's 京成高砂; gate 3), 小室 (komuro) among them",
    "kind": "http_contains",
    "url": "https://www.hokuso-railway.co.jp/",
    "present": ["/railway/station/shinshibamata.html", "/railway/station/yagiri.html", "/railway/station/kitakokubun.html", "/railway/station/akiyama.html", "/railway/station/higashi_matsudo.html", "/railway/station/matsuhidai.html", "/railway/station/oomachi.html", "/railway/station/shin_kamagaya.html", "/railway/station/nishi_shiroi.html", "/railway/station/shiroi.html", "/railway/station/komuro.html", "/railway/station/chiba_newtown_chuo.html", "/railway/station/inzaimakinohara.html", "/railway/station/imbanihonidai.html"]
  },
  {
    "id": "funabashi-hokuso-komuro-timetable",
    "claim": "小室's weekday timetable toward Tokyo, linked from the operator's own station page, is still the 2025-12-13 edition where 86 departures and three an hour at midday were read (2026-10-05); a new date means re-read the frequency",
    "kind": "http_contains",
    "url": "https://hokuso.ekitan.com/jp/pc/T5?USR=PC&dw=0&slCode=200-11&d=1",
    "present": ["北総鉄道", "小室", "2025年12月13日現在"]
  },
  {
    "id": "funabashi-projected-crs",
    "claim": "Funabashi projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.019,
    "expect": "EPSG:32654"
  }
]
```
