# Tama — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5, second half", call 109: the
ledgers' skew disclosed). The Step 0 downloads were approved by the owner
2026-10-06 (calls 106, 141, 147). **Step 0 measured 2026-10-06** (staging).
Every file below was already cached, each from its publisher's own host with
the project user-agent:

- In `data/tokyo_tama/raw/` (gitignored; one copy for the four Tama cities in
  Band A), from `www.hokeniryo.metro.tokyo.lg.jp` (東京都保健医療局, the Tokyo
  Metropolitan Government's health centres for the Tama area), as of
  2026-08-31: `shokuhin-kyoka-7.csv` (4,486,267 B), `shokuhin-todokede-1-7.csv`
  (1,956,304 B), `kankyo-riyoujo-5.csv` (165,277 B), `kankyo-biyoujo-5.csv`
  (608,582 B), `kankyo-cleaning-5.csv` (173,591 B).
- In `data/tokyo_tama/raw/isj/`, from `nlftp.mlit.go.jp`: `13224-24.0a.zip`
  (58,889 B) and `13224-19.0b.zip` (5,988 B).

**Nothing was downloaded for this brief.** MHLW has **no file for 13224**: the
per-code request answers HTTP 404 (an error page, not saved), because Tama is
licensed by the prefecture's health centre, not its own (below).

**Run `python scripts/brief_check.py tama` before writing any code.** Then the
`japan-city` skill, with the `tokyo-ward` skill for Tokyo's sources and
credits. Shape: **Fukuyama's** for a complete list (`docs/build_briefs/fukuyama.md`),
but one source, no MHLW control and no months to merge: each ledger is ONE
file of every premises on it at its date, refreshed monthly. Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Tama entry
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, measured
through `pipeline/countries/japan.py` with an in-memory `CITIES` entry.

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
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The skew is disclosed on the page (owner, 2026-10-06, call 109)**, as the
band row says: about 20% of rows opened after the control date; the ledger
misses long-standing premises (new permits only from 2019-08; at the control
date the share is 58-75% across the eight Tama cities, **71.6% here**); laundry
about half; opt-outs and closures left out. **法人代表者氏名, the operator's
address and phone are dropped at read** (call 109).

**✅ Licence: the catalogue route, relied on (owner, 2026-10-06, call 108;
Taitō's precedent).** The page links the catalogue entries only, never the
host site below its top page (Licence, below).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Tama
carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Tama into **Kanto**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`**: the city's drawn rail is two private heavy railways
(Keiō, Odakyū), no subway, tram or light rail once the monorail's one station
is left out; Yokosuka's precedent for a private-heavy-railway backbone (owner,
2026-10-02).

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's Tama ledgers (CC
BY 4.0 by the Tokyo Open Data Terms, the catalogue route relied on).** The
permit ledger as of **2026-08-31** holds **1,005 Tama rows, 839 restaurants
(飲食店営業), 90.1% of the 931 in Tokyo's yearbook (FY2024)**, flattered: 172
of them (20.5%) were first permitted after the yearbook's date, so **at the
control date the ledger holds 71.6%**. The notification ledger adds 496 rows
(konbini 61 against the yearbook's 58, supermarkets 30 against 27). Barbers
53, beauty salons 164, laundries 38: **about 101%, 96% and 62%** of estimates
scaled from the 2021 census. Through `japan_eigyo`: **Food service 665,
Retail 580** (223 permits + 357 notifications), **Personal services 254**.
Block join **96.7%** of 1,499 bucketed rows, none unplaced. **Rail: 6 station
groups** (Keiō 3, Odakyū 3), the Tama Toshi Monorail's one station left out
(its station kept by the Keiō and Odakyū stations 187-197 m away);
frequencies ASSERTED (the operators' timetables are not readable by curl).

---

## Business leg — Tokyo's Tama ledgers

Host `https://www.hokeniryo.metro.tokyo.lg.jp`, ledger page
`/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho` (更新日 2026-09-14),
「東京都が設置している保健所等で保有する台帳一覧」. Tama is in the **南多摩保健所**
area (日野市、多摩市、稲城市). The page: 「ホームページへの公表を希望しない施設、廃止・休止している施設は除いて公表しています」;
for food, 「移動販売、臨時販売、自動車販売、自動販売機、行商、催事等期間短縮申請があったもの、届出が不要な施設及び廃業した施設は除いています」.
The catalogue entries say each ledger is published monthly, on about the
10th business day, for the premises on it at the end of the month before.

| File (under `/documents/d/hokeniryo/`) | Bytes | Whole ledger | Tama rows | What it is |
|---|---|---|---|---|
| `shokuhin-kyoka-7` 食品関係営業台帳（許可） | **4,486,267** | 28,093 | **1,005** | 「平成29年1月から令和8年8月までの新規許可施設及び平成29年4月から令和8年8月までの許可更新施設（令和8年8月31日現在）」 |
| `shokuhin-todokede-1-7` 食品関係営業台帳（届出） | **1,956,304** | 12,502 | **496** | 「令和3年6月から令和8年8月までの届出施設（令和8年8月31日現在）」 |
| `kankyo-riyoujo-5` 理容所台帳 | **165,277** | 1,427 | **53** | every barber on the register, 2026-08-31 |
| `kankyo-biyoujo-5` 美容所台帳 | **608,582** | 4,319 | **164** | every beauty salon, 2026-08-31 |
| `kankyo-cleaning-5` クリーニング所台帳 | **173,591** | 1,040 | **38** | laundries and 取次所 (無店舗取次店 none here) |

- **cp932 CSV, header on row 1.** `japan_register.city_rows` reads all five.
  Rows are cut to the city by address (`東京都多摩市…` or `多摩市…`), never
  by a code: the ledgers carry no municipality code.
- **Columns, permits**: 屋号, 営業所所在地, 営業者氏名, 営業者住所, 営業の種類,
  申請区分, 営業所電話番号, 初回許可日, 営業者電話番号, 法人代表者氏名.
  **Notifications**: the same less 申請区分 and 初回許可日, plus 届出年月日.
  **Registers**: 確認番号, (営業形態, laundry only), 施設名称, 施設TEL, 施設所在地,
  施設ビル名, 営業者氏名, 法人代表者氏名, 営業者住所, 営業者ビル名, 営業者TEL,
  確認年月日.
- **Against the shared tuples**: 営業所所在地 and 施設所在地 are in `ADDR_COLS`,
  屋号 and 施設名称 in `NAME_COLS`, 営業の種類 and 営業形態 in `TYPE_COLS`,
  営業者氏名 in `OPERATOR_COLS`. **No shared-code change is needed.** The
  barber and beauty registers have no type column: the config names the kind
  per file (`source_rows` or `SOURCE_KIND`, Hamamatsu's registers). There is
  no 業態 column: the ledger writes the form inside the type
  (飲食店営業(集団給食), (バー・キャバレー), (仕出し屋), (旅館・ホテル)), and
  `japan_eigyo` already reads those from the type.
- ⚠️ **Drop at read (call 109)**: 法人代表者氏名, 営業者住所, 営業者ビル名 and every
  phone column (営業所電話番号, 営業者電話番号, 施設TEL, 営業者TEL). 法人代表者氏名 is
  in `OPERATOR_COLS`, so the build's selection must leave it out explicitly;
  measured cost to the name rule: **0 rows** (Privacy, below).
- **Monthly, and the file names carry a CMS suffix** (`-7`, `-1-7`, `-5`)
  that may change with an edition: `japan_fetch.current_url` with a
  `SOURCE_LINKS` regex on the ledger page (Kawasaki's and Otsu's precedent),
  `as_of` = the date in the page's title line (2026-08-31), never today.

### Permits: types, dates and the share

- **申請区分**: 新規 901 · 更新 104. **Types (30)**: 飲食店営業(一般飲食店) 583,
  (そうざい店) 72, (集団給食) 68, (弁当屋) 41, 菓子製造業(パン製造業) 32,
  (その他の菓子製造業) 29, 食肉販売業(一般) 26, 魚介類販売業(一般) 24,
  飲食店営業(バー・キャバレー) 21, (すし屋) 17, 菓子製造業(生菓子製造業) 16,
  そうざい製造業(そうざい製造) 14, 飲食店営業(そば屋) 13, (仕出し屋) 10, (喫茶店) 8, …
- **The control: Tokyo's yearbook table 19-8** (`data/tokyo/raw/tn24qv190800.csv`,
  令和6, 2025-03-31; `japan_official.py` reads it): 多摩市 飲食店営業 **931**. e-Stat's
  衛生行政報告例 counts the Tama area only as part of Tokyo Prefecture, so the
  yearbook is the official count here.
- **839 restaurant rows = 90.1%** of 931. **172 (20.5%) were first permitted
  after 2025-03-31**, so they are not in the yearbook's count: **at the control
  date the ledger holds 667, 71.6%**. That is the skew the page discloses.
- **Why it misses premises**, measured on the dates: every 新規 row's first
  permit is **2019-09-05 to 2026-08-28** (6 in 2019, then 47, 136, 145, 161,
  165, 130, 111 a year); every 更新 row's first permit is **1980-04-23 to
  2015-05-13** (renewals since 2017-04 of premises first permitted before
  2015-06). Ledger-wide the earliest 新規 is 2019-08-02 and the latest 更新
  first permit 2017-05-12, and **only 32 of 28,093 rows carry a first permit
  between 2015-06-01 and 2019-08-31**. The page says new permits since 2017-01;
  the file holds none before 2019-08. So a premises first permitted from mid-2015
  to mid-2019 is absent even if it has renewed since (Higashimurayama's own
  2024 snapshot finds such premises: `docs/build_briefs/higashimurayama.md`).
  Read as measured; the cause is the publisher's.
- **Old-law coverage (Kurashiki's trap)**: old-law permits ARE in the ledger
  where they fall inside its windows (新規 2019-08 to 2021-05, renewals since
  2017-04); the gap above is the trap's shape here, and it is disclosed, not
  repaired.
- **Duplicates**: 15 exact repeats of (address, trade name, type); 873
  distinct (address, trade name) of 1,005 rows (several permits at one
  premises). One pin per premises and bucket (trap 7). 1 row has no 屋号.
- **Closures**: none in the file by the page's own rule (closed and suspended
  premises are removed each month), but a premises closed without notice
  stays: the page keeps "may include closed premises".

### Notifications (届出): the Retail side, near complete

496 Tama rows: その他の食料・飲料販売業(店舗) 147, コンビニエンスストア 61,
その他の食料・飲料販売業(電子申請（未区分）) 34, 乳類販売業(ショーケース売り) 34,
弁当販売業(自動車以外) 32, 百貨店、総合スーパー 30, 野菜果物販売業(自動車以外) 28,
その他の食料・飲料販売業(包装) 23, 集団給食施設 (several kinds, 48), … 届出年月日:
198 in 2021 (the law change), then 40-61 a year; 48 rows dated before 2021.
**Against the yearbook**: konbini **61 of 58**, supermarkets **30 of 27**,
野菜果物 28 of 31, 弁当販売 32 of 37. Notifications began in 2021-06, so this
ledger is not skewed as the permits are. Whether to read it is open call 1.

### Counts through `japan_eigyo`

**Permits: Food service 665, Retail 223** (菓子 77, そうざい製造 24, 食肉 26,
魚介 24, …). Left out: institutional catering 68 (集団給食), hostess venues 21
(バー・キャバレー), event catering 10 (仕出し屋), inside accommodation 4, and 14
rows of manufacturing types with no rule. **Not a premises: 0** (the ledger excludes
vehicles, stalls and vending). **Notifications: Retail 357**; left out:
not a premises 60 (`permits_from_rows`' mobile test), institutional
catering 51, no rule 27, mail order 1.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **335** 飲食店 establishments in 13224
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 655 distinct placed
Food-service premises is **1.96 per establishment**, at the top of the built
cities' 1.56-1.92, although the ledger misses premises: the 20% opened after
2021 carry it. Record the figure and the reading.

### Personal services: the registers

| Register | Rows | Census 2021 (9-1A) | Estimate (Hachiōji's licensed/census) | Share | (Tokyo's ratio) |
|---|---|---|---|---|---|
| 理容所 barbers | **53** | 47 | 53 | **101%** | 94% |
| 美容所 beauty salons | **164** | 109 | 171 | **96%** | 71% |
| クリーニング所 laundries | **38** (取次所 34, 一般 3, リネン 1) | 35 | 61 | **62%** | 68% |

e-Stat's FY2024 第10表 counts the Tama area only within Tokyo Prefecture, so
the official figure is an ESTIMATE: the census count times Hachiōji's ratio of
licensed premises to census establishments (277/247, 807/514, 264/151; the one
Tama-area city e-Stat lists), with Tokyo's (7,328/6,122, 28,589/13,455,
8,147/5,137) beside it. **The registers are standing registers, not
since-2017 streams**: 確認年月日 run from 1931, 1978 and 1972, so the
permits' skew does not reach them. Laundry "about half" is disclosed (call
109); the リネン row is left out by `japan_eigyo` (37 bucketed). No repeats.

## MHLW: no file for 13224, so no control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13224_food_business_all.csv`
answers **HTTP 404** (an 11,712 B error page; not saved). The Tama area's
permits sit in the prefecture's file (13000), which the scoping measured at
**55 addressed open restaurants for Tama** (`japan_universe_mhlw.csv`, cover
"13000 (prefecture)"): too thin for a control, and the ledger page says MHLW's
opt-outs are applied to the ledgers. **Not downloaded** (not named in the
approval); a control from it would be a question to staging.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13224-24.0a.zip` (58,889 B,
**3,028 block keys**), town-chōme `.../19.0b/13224-19.0b.zip` (5,988 B,
**89**). `japan.CITIES` entry at build: `"tama": {"name": "多摩市", "pref":
"13", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["13224"]}`.

⚠️ **One ISJ directory per city.** `load_city_isj` globs a directory, and
`data/tokyo_tama/raw/isj/` holds four municipalities' files that all key their
blocks under ward "" (Higashiyamato's 桜が丘 beside Tama's 桜ヶ丘). The build
reads Tama's two files from their own directory (`data/tama/raw/isj/`, copied
or fetched by `fetch_sources.py`), as the scratch measurement did.

| Tier, today's shared code (all buckets, 1,499 rows) | Block | Town-chōme | Unplaced |
|---|---|---|---|
| **All** | **96.7%** | 3.3% | **0.0%** |
| Food service, permits (665) | 96.2% | 3.8% | 0 |
| Retail, permits (223) / notifications (357) | 99.1% / 94.4% | 0.9 / 5.6 | 0 |
| Barbers (53) / beauty (164) / laundry (37) | 98.1% / 99.4% / 100% | 1.9 / 0.6 / 0 | 0 |

Staging's permits-and-registers measurement (`wave5/isj_measure`) gave 97.5%
on 1,142 rows; the notifications bring it to 96.7%. **The misses, read**
(towns only): the chōme tier is (a) Tama's 地番 areas, 乞田, 東寺方, 貝取 and
和田 (`和田字十三号`), whose numbers MLIT's block file lacks, and (b) 落合一丁目
and 鶴牧三丁目's large-lot numbers around 多摩センター. Plus two addresses
written "…付近" (near). No rule is proposed: each takes its town's centroid.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13224
(**21.00 km²**, extent W 139.394, S 35.605, E 139.474, N 35.658; centroid
139.440, 35.631). Read with `stub_test()`'s method and an in-memory `CITIES`
entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 京王線 (京王電鉄, 12) | Keiō Line | **1 / 35** | 聖蹟桜ヶ丘 |
| 相模原線 (京王電鉄, 12) | Keiō Sagamihara Line | **2 / 12** | 京王永山, 京王多摩センター |
| 多摩線 (小田急電鉄, 12) | Odakyū Tama Line | **3 / 8** | 小田急永山, 小田急多摩センター, 唐木田 |
| 多摩都市モノレール線 (多摩都市モノレール, 23) | Tama Toshi Monorail | **1 / 19** | 多摩センター (**left out**) |

- **7 station records, 7 N02_005g groups; 6 drawn.** N02 gives the Keiō and
  Odakyū stations of one place their own groups: **京王永山 / 小田急永山 38 m
  apart, 京王多摩センター / 小田急多摩センター 38 m.** The standing rule collapses
  on the group code, never the name, and `GROUP_JOIN` joins only platforms of
  ONE name, so they stay two stations each. **Decided by precedent, no owner
  question:** the built cities keep such pairs apart (Kyoto's Yamashina and
  Keihan-Yamashina, 6 m; Osaka's Nippombashi and Kintetsu-Nippombashi, 9 m;
  N02-25 holds 25 such pairs under 60 m nationally). The build checks the two
  pairs' labels in a scratch render.
- **The monorail's one station, left out (calls 54, 92).** 多摩センター is the
  only monorail station inside the city (1 of 19; the rest in 立川市 7, 日野市 5,
  八王子市 3, 東大和市 3), its own group, **187 m from 小田急多摩センター and 197 m
  from 京王多摩センター**. Other lines serve the place, so the urban line is left
  out (`config.LEFT_OUT_LINES`) and the Keiō and Odakyū stations keep the
  ring; it is not Urayasu's or Suita's case (no other line there), so it is not
  drawn cut. Its station is printed by step 1, not written to
  `excluded_stations.csv` (a left-out line's stations never are). The page says
  so in a bullet under **The lines** (the wording: Urayasu's and Suita's built
  bullet, or a proposal in the drafts file).
- **Stubs kept as cut (standing call 3):** the Keiō Line keeps ONE station of
  35, 聖蹟桜ヶ丘, a private line, so it is drawn as cut with no owner question
  (Kobe's JR Takarazuka Line); its trains run on to 府中 and 新宿 one way, 高幡不動
  and 八王子 the other. The Sagamihara Line (2 of 12) and the Tama Line (3 of
  8, 唐木田 its terminus) are cut at the line.
- **Cut at the line** (named by N03 municipality at build): the Keiō Line 34
  beyond (調布市 8, 世田谷区 7, 府中市 6, 日野市 4, …), the Sagamihara Line 10
  (Kanagawa 3, 稲城市 2, 八王子市 2, 調布市 2, 町田市 1), the Tama Line 5 (all in
  Kanagawa).
- **Spacing**: 聖蹟桜ヶ丘 2,284 m from 京王永山; 唐木田 1,291 m from the monorail's
  多摩センター (about 1.4 km from the Odakyū station). Rings by the spacing rule
  at build.
- **The light-rail/rail test**: Keiō and Odakyū are heavy rail (class 12,
  private). The monorail (class 23) is the only urban line, and it is left out.
- **Frequency: ASSERTED, not read.** Keiō's timetables are a NAVITIME app
  (`transfer-train.navitime.biz/keio/…`) that renders in the browser, so curl
  gets no departures; Odakyū's are per-station PDFs whose text does not
  extract (`/station/pdf/odakyu_nagayama.pdf`, `…/odakyu_tama_center.pdf`,
  `…/karakida.pdf`). As stated by the probe (wave 5, `japan_j6`): Keiō and
  Odakyū at every station here several trains an hour all day; **no stretch
  is expected at or under about 11 trains a day** (call 86). ⚠️ The build reads
  the counts (a whole-page reader, counting marked trains: the jre.py trap) or
  records them as ASSERTED on the page's internal notes.
- ⚠️ **Gate 3** at build: Keiō's and Odakyū's own station counts inside the
  city (Keiō 1 + 2, Odakyū 3). **OSM `name:en`** for 6 groups (one Overpass
  query at build, in the box below; not queried here).

## Scope

**Tama City.** The Keiō Line runs on to 新宿 and 八王子, the Sagamihara Line to
調布 and 橋本, the Tama Line to 新百合ヶ丘; cut at the line. The monorail (立川北
to 多摩センター) is not drawn.

## Licences — as read by staging

- **Tokyo's Tama ledgers: PERMITTED WITH CONDITIONS through the catalogue
  route, relied on** (licence-read agent, recorded by staging in
  `docs/decisions_drafts/staging.md`, "Wave 5, second half"; owner, call 108,
  Taitō's precedent). The Tokyo catalogue's entries **`t000055d0000000361`**
  (食品関係営業台帳: the permit and notification ledgers) and
  **`t000055d0000000614`** (環境衛生施設台帳: barber, beauty, inn and laundry
  ledgers) declare `CC-BY-4.0` (maintainer 保健政策部保健政策課, 更新頻度 1か月ごと),
  under the Tokyo Open Data Terms (`portal.data.metro.tokyo.lg.jp/terms/`). The
  host site's own policy bars reuse and links below its top page, so **the page
  links the catalogue entries only**
  (`https://catalog.data.metro.tokyo.lg.jp/dataset/t000055d0000000361`, `…/t000055d0000000614`).
- **The credit**: the Terms' §2(1)イ modified-use form (title, 東京都, CC BY
  4.0 linked, and that the work was modified); take the exact wording from
  staging's record, not from here. **MUST NOT** present the map as made by
  Tokyo or a municipality (§2(1)イ). No new verdict is written in this brief.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **Tokyo's yearbook and e-Stat's census**:
  measurement sources, not drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **営業者氏名 is read IN MEMORY for the name rule only**, never written. It is
  filled mostly for companies: permits 754 of 1,005 (**747 with a company
  marker, 7 without**), notifications 392 of 496 (383, 9); the registers fill
  it only for companies (16, 70, 29, all marked). Blank otherwise (the page:
  items an applicant asked MHLW to withhold are withheld here too).
- **The name rule, measured in memory** (answers only, never a value): **0
  rows** withheld in Tama in any ledger (the sign rule 0, the operator
  comparison 0). **Dropping 法人代表者氏名 costs 0**: no trade name equals it
  where the other tests pass (680 permit rows fill it).
- **Never selected**: 法人代表者氏名, 営業者住所, 営業者ビル名, every phone column.
  Select the trade name, the premises address, the type and its date.
- Run `check_personal_exposure.py tama` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.394-139.474 E, centroid 139.440:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (35.60, 139.39, 35.66, 139.48). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A with the
skew disclosed (call 109); the catalogue route (call 108); 法人代表者氏名,
addresses and phones dropped at read; `mode: metro`; the minor tier and Japan
East (Kanto after the retag); the monorail's one station left out (calls 54,
92); the Keiō Line's one station drawn as cut (standing call); the 38 m pairs
kept apart (precedent); no frequency floor.

**Answered by the owner on 2026-10-06:** call 169, **MHLW's rows the ledgers lack added** for all four Tama cities (Tokyo wards' precedent of 2026-09-24: the ledger's row kept where both hold a premises, `SUPERSEDES`; MHLW's PDL 1.0 notice line added; the share the page states stays without MHLW's rows). The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **Read the notification ledger into Retail** (357 bucketed rows: konbini,
   supermarkets, greengrocers, packaged-food shops). *Recommend yes*: it is
   the same catalogue entry and licence as the permits, and the Tokyo wards'
   own 許可・届出 lists already put notifications in Retail; against the
   yearbook it is near complete (konbini 61 of 58, supermarkets 30 of 27). The
   tradeoff: Retail then mixes a complete notification stream with the skewed
   permit stream, which the page's businesses bullet says. Without it Retail
   is 223 permit shops and no konbini (Toyota's "Retail thin"). Decide it once
   for the four Tama cities.

## What the build must still measure

- The per-city ISJ directory; `SOURCE_LINKS` for the monthly files and their
  suffixes; `as_of` 2026-08-31 from the page, never today.
- The share every build (`OFFICIAL_SHARES`, the yearbook through
  `japan_official.py`): 839 of 931, and the at-control-date share the page
  states (71.6%), measured, never typed.
- Keiō's and Odakyū's frequencies (or ASSERTED); gate 3; OSM `name:en`; the
  two 38 m pairs' labels; the Keiō Line's label on its one-station stub; line
  colours on both basemaps; the opening view (`map-view`); the factory share;
  the census ratio (1.96) and its reading; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "tama-ledger-page",
    "claim": "The ledger page names Tama in the 南多摩保健所 area, the 2026-08-31 date, the permits' windows and the opt-out and closure rule",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["南多摩保健所（日野市、多摩市、稲城市）", "令和8年8月31日現在", "平成29年1月から令和8年8月までの新規許可施設", "廃止・休止している施設は除いて公表"]
  },
  {
    "id": "tama-ledger-edition",
    "claim": "The edition measured here: the five CSVs under these names (a failure means a new edition or new suffixes: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "tama-permits-file",
    "claim": "The permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 4000000
  },
  {
    "id": "tama-notifications-file",
    "claim": "The notification ledger (1,956,304 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-todokede-1-7",
    "min_bytes": 1500000
  },
  {
    "id": "tama-barber-file",
    "claim": "The barber register (165,277 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-riyoujo-5",
    "min_bytes": 120000
  },
  {
    "id": "tama-beauty-file",
    "claim": "The beauty register (608,582 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 450000
  },
  {
    "id": "tama-laundry-file",
    "claim": "The laundry register (173,591 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-cleaning-5",
    "min_bytes": 120000
  },
  {
    "id": "tama-catalogue-food",
    "claim": "The catalogue entry the page links for the food ledgers declares CC-BY-4.0 and points at the ledger page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "t000055d0000000361", "shokuhineigyokyokadaicho"]
  },
  {
    "id": "tama-catalogue-registers",
    "claim": "The catalogue entry the page links for the barber, beauty and laundry ledgers declares CC-BY-4.0",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "t000055d0000000614"]
  },
  {
    "id": "tama-no-mhlw-file",
    "claim": "MHLW has no per-city file for 13224 (HTTP 404): the prefecture licenses Tama, so no MHLW control",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13224_food_business_all.csv",
    "expect_status": 404
  },
  {
    "id": "tama-isj-block-live",
    "claim": "MLIT's block-level address file for Tama (13224) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13224-24.0a.zip",
    "min_bytes": 50000
  },
  {
    "id": "tama-isj-chome-live",
    "claim": "MLIT's town-chōme file for Tama (13224) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13224-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "tama-projected-crs",
    "claim": "Tama projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.44,
    "expect": "EPSG:32654"
  }
]
```
