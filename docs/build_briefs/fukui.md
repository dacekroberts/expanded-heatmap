# Fukui — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py fukui`
before writing any code. Coordinates: the `address-join` skill, measured with
the shared `japan_register` functions under this brief's own column mapping
(the shared `scripts/screen_japan_join.py` table was not edited; add a
`fukui` entry there at the build). Rail: MLIT N02-25 cut at the N03 city
line, measured the same way.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls):** (1) **the Shinkansen does not count** (2026-09-24);
(2) **lines served only by limited expresses DO count** (2026-09-28);
(3) **the city line only**: only stations inside the city get rings, with a
per-line stub test; a one-station stub stays as cut, an URBAN line cut to a
stub goes back to the owner (2026-09-24, 2026-09-27); (4) **菓子製造業 and
そうざい製造業 count, in Retail**, the factory share measured and kept
(2026-09-24, 2026-09-27); (5) **the name rule**: where the trade name IS the
operator's own name, the pin shows its permit type, the operator column read
in memory only (2026-09-27); (6) **no page says "currently operating"**. Also:
fault-based cost clauses accepted for all of Japan (2026-09-24); English
station names from OSM `name:en`, numerals as figures before 丁目.

**✅ Minor label tier (owner, 2026-10-02):** Fukui is in the 2026-10-01
Japanese batch and carries `label_tier: "minor"`, with the whole France and
Czechia precedent: a Japan sub-region (one or a split, by
`check_macro_labels.py`, never by eye), every Japanese city moved into it,
and `REGION_LABELS_ALSO["East Asia"]` gaining it. **The eight built Japanese
cities stay eligible.** The first city of the batch makes the change.

**✅ Licence decided (owner, 2026-10-01): use the current lists and offer
`outputs/fukui/` under CC BY-SA 4.0.** The build owes a line in `LICENSE` and
the data-sources row (Licences, below). It is the project's first
share-alike licence on its own output.

---

## The one-line summary

**The city's own month-end lists carry every food permit (4,333 rows as of
2026-08-31, 2,984 restaurants: 85% of the official 3,508) and the barbers,
beauty salons and laundries (1,309 rows), with closures already removed.**
All three buckets. The block join places 87.5% of food premises at the
block and leaves 1.3% unplaced. MHLW's file adds little here (90 restaurant
permits; Fukui files at the counter). Rail: the Fukubu Line (15 of its 25
stations in the city), both Echizen Railway lines, the Hapi-line and JR's
Etsumi-Hoku Line, 45 station groups inside the city.

---

## Business leg — the city's own pages, one XLSX per list

| | Food (食品衛生法に基づく営業許可施設一覧) | Personal services (環境衛生関係施設一覧) |
|---|---|---|
| **Page** | `https://www.city.fukui.lg.jp/fukusi/eisei/syokuhin/p070519.html` (updated 2026-09-07) | `https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518.html` (updated 2026-09-07) |
| **Files** | `…/syokuhin/p070519_d/fil/11syokuhin_202608.xlsx`: **3,219,681 B**; closures `…/12syokuhinhaigyo_202608.xlsx`: 68,576 B | `…/kankyo/p070518_d/fil/01riyou_202608.xlsx` **193,971 B**, `02biyou_202608.xlsx` **536,170 B**, `03cleaning_202608.xlsx` **210,210 B**; closures `07kankyohaigyo_202608.xlsx` 29,205 B. Also on the page and out of scope: 04 inns, 05 bathhouses, 06 theatres |
| **Shape** | **Twelve sheets, one per month-end** (`R8.8月末` back to `R7.9月末`; `R8.3月末 ` has a trailing space), header on row 2. **The newest sheet is the list.** | The same: twelve month-end sheets each, header on row 2 |
| Rows (`R8.8月末`) | **4,333** (4,332 distinct permit numbers) | barbers **268**, beauty **788**, laundries **253** (取次 189, 一般 55, 一般(特定洗濯) 9) |
| As of | **2026-08-31** (「令和8年8月末日現在」); newest 許可年月日 2026-08-31 | 2026-08-31 |
| Cadence | monthly, file names carry the month (`_202608`) | monthly |
| Columns | 施設名称, **施設所在地**, 施設電話番号, **申請者名(法人名)**, **法人代表者名**, **申請者住所**, 申請者電話番号, 許可年月日, 許可期限, 許可番号, 業種 | 営業所名称, **営業所所在地**, 営業所電話番号, **申請者名（法人名）** (full-width brackets), **法人代表者名**, **申請者住所**, 申請者電話番号, 確認年月日, 確認番号, 業種 (+ 詳細業種 for laundries) |

- **Closures are already out**: none of the 26 August, 15 July or 36 June
  closures (by permit number) is in the `R8.8月末` sheet; 6 of August's were
  in `R8.7月末`. The month-end list is the register in force.
- **Restaurants**: 飲食店営業 **2,891** + 飲食店 **90** + 喫茶店 **3** =
  **2,984**, against the official FY2024 **3,508** (e-Stat 衛生行政報告例):
  **85%**. The list has no vehicle or 市内一円 rows, which the official count
  includes; the rest of the gap is unexplained (Osaka's list was 67% and
  accepted with approved wording).
- ⚠️ **飲食店 (90) and 喫茶店 (3) are old-law permits** (granted 2020-03 to
  2021-05, still in term) under short spellings that `japan_eigyo` does not
  match: as it stands they fall to "no rule" and **93 restaurants would be
  dropped**. Add Fukui's spellings (`^飲食店$`, `^喫茶店$`) to the taxonomy
  at build, with an import-time assert.
- **Food retail (permit types)**: 菓子製造業 461 · そうざい製造業 300 ·
  魚介類販売業 139 · 食肉販売業 107 = **1,007**. Out: manufacturing (342
  "no rule" besides the 93 above).
- **Personal services**: 268 + 787 + 253 = **1,308** fixed (one beauty row is
  市内一円).

### MHLW's file — counter filing dominates in Fukui

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=18201_food_business_all.csv`:
**398,312 B, 967 rows** (届出 832, 許可 135), newest 許可年月日 2026-08-05.
Only **90 open restaurant permits** (72 with an address); 46 of the 58 at the
block tier are in the city's list under the same town, block and trade name
(**79%**). Fukui evidently files most permits at the counter, and its own list
carries them. **The city's list is the food source** (the Kobe / Osaka shape);
MHLW's file is a count control only. Its 832 notifications (vending 367,
other food sales 131, supermarkets 55) would make a thin partial retail
bucket; recommended: leave them out, as for every city with a complete own
list.

### Operator columns and the name rule

- **Neither spelling is in `japan_register.OPERATOR_COLS`**: the food list's
  **申請者名(法人名)** (half-width brackets), the registers' **申請者名（法人名）**
  (full-width), and **法人代表者名** in both. Add all three at the build, or
  the rule compares nothing; then re-run the Minato control.
- **The city publishes operators' names only for companies.** The three
  operator columns are blank on 2,124 of 4,333 food rows, and 2,118 of the
  2,209 filled carry a company marker; the registers fill them on 26 of 268,
  182 of 788 and 167 of 253 rows, all but 11 of them companies. The sheets have no merged
  cells. **With the columns mapped, the rule flags 20 food rows and no
  register row**; it cannot see a sole trader whose trade name is their own
  name. This is the position the owner accepted for MHLW's rows in Fukuoka.
- **申請者住所 is an operator's own address**: never select it.

### What the shared code does not read yet (build-time)

- ⚠️ **`xlsx_rows` reads every sheet with an address column**, so each
  workbook would be read twelve times over. Read the newest month-end sheet
  only (by name, `R8.8月末`, or the first sheet), and pin `as_of` to its date.
- ⚠️ `NAME_COLS` lacks **営業所名称** (the registers' trade-name column).
- ⚠️ The ward regex: one beauty address with 「森田北東部土地区画整理事業」 parses
  `…土地区` as a ward; a ward-less flag (Toyama's brief has the same item).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 18201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/18201-24.0a.zip` (278,561 B) and
`…/19.0b/18201-19.0b.zip` (16,613 B): 25,782 block keys, 728 town-chōme.

| Tier | Food list (4,333) | Registers (1,308) | MHLW, addressed (798) |
|---|---|---|---|
| Block | **87.5%** | **87.3%** | 81.6% |
| Town-chōme / 大字 centroid | 11.1% | 11.2% | 15.2% |
| Unplaced | 1.3% | 1.5% | 3.3% |

**Independent check** (MHLW's own point for the same premises, matched on
town and trade name): block-tier city rows sit a **median 36 m** away (146
rows, 97.9% within 250 m); chōme-tier rows a median 113 m (27 rows). MHLW's
own block hits against its own coordinates: median 39 m, 94.5% within 250 m
(651). MHLW has a point for only 31 of the 541 city rows off the block tier,
so no fallback is worth building here.

The misses: rural 大字 at the chōme tier (茱崎町, 鮎川町, 蒲生町 on the coast,
上野本町), and the unplaced are newer land readjustments (石盛, 東森田, 栗森)
that MLIT's files do not key yet.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (18201)

**Use N02-25** (`"n02": "25"`, Hiroshima's precedent): N02-24 still files the
former Hokuriku Main Line under JR West; N02-25 has the Hapi-line Fukui
(since 2024-03-16). City bbox S 35.9204, W 135.9638, N 36.1729, E 136.4672.
**49 station records inside, 45 N02_005g groups.** Shinkansen: 福井 on the
北陸新幹線, dropped (福井 stays as a Hapi-line, Echizen and tram station).

| Operator | N02 line (class) | Inside / total | Reading |
|---|---|---|---|
| 福井鉄道 | 福武線 (12, railway) 9/19 · 福武線 (21, 軌道) 6/6 | **15/25** | cut at the line (on to Sabae and Echizen) |
| えちぜん鉄道 | 三国芦原線 (12) | 10/22 | cut at the line |
| えちぜん鉄道 | 勝山永平寺線 (12) | 8/23 | cut at the line |
| ハピラインふくい | ハピラインふくい線 (12) | 4/19 | cut at the line |
| 西日本旅客鉄道 | 越美北線 (11) | 12/22 | cut at the line (a rural line; Fukui City reaches far up the valley) |

- **The screen's "18 of 25 stations in the city" was wrong**: N02 puts 15 of
  the Fukubu Line's 25 inside (たけふ新 to 鳥羽中, 10 stations, lie in
  Echizen and Sabae).
- ⚠️ **Track**: the Fukubu Line is 18.3 km of railway (class 12) and 3.1 km
  of 軌道 (class 21, the street section through the centre with its 福井駅
  and 田原町 ends; the screen's "2.8 km on the street" is not confirmed by
  N02's legal classes). By general knowledge its trams also run through onto
  Echizen's 三国芦原線 to 鷲塚針原. **Frequency not read**: the light-rail
  test's gate (15 minutes by day) applies on its railway track. Under the
  Japanese standing calls the line is drawn in any case; the gate decides
  what it is called and `mode`. Read the operators' timetables at build.
- ⚠️ **Gate 3, the operators' own stop counts**: not read (Fukui Railway,
  Echizen Railway). Read at build.
- ⚠️ OSM `name:en` for every station and tram stop at build (no OSM was
  queried for this brief); the street stops need `TRAM_OSM_JSON`.

## Scope

**Fukui City (18201), one municipality, no wards.** Every railway runs on
out of the city (Sabae, Echizen, Eiheiji, Sakai, Awara, Ōno); cut at the line.

## Licences — read 2026-10-01 (licence-read agent) and 2026-10-02

- **Fukui City's lists — PERMITTED WITH CONDITIONS (CC BY-SA, site default).**
  - **The grant**: the site policy (`https://www.city.fukui.lg.jp/sisei/kohou/hp/site-p.html`,
    last updated 2017-10-23), 1 著作権: use is allowed within the CC licence
    shown, and 「…基本ライセンスは、写真、画像、映像及び個別に設定する場合を除き、CC－BY－SA（表示－継承）とします。」
    No version is named (the policy links creativecommons.jp). Neither list
    page sets a licence of its own (read live 2026-10-02: no licence words on
    either page).
  - **Share-alike, accepted (owner, 2026-10-01)**: offer `outputs/fukui/`
    (the map and any derived Fukui data) under **CC BY-SA 4.0** in
    `LICENSE`, and say so in the data-sources entry. The personal-services
    lists exist only under BY-SA, so the open-data park's older CC BY 2.1 JP
    food copy (`/sisei/tokei/opendata/p018973.html`, fixed stores) would not
    avoid it; not used.
  - **MUST DISPLAY**: 福井市, the two list titles with their page URLs, CC
    BY-SA (no version claimed for the city's licence), and that the data was
    processed. Proposed form, in the Japanese pattern:
    `出典：福井市「食品衛生法に基づく営業許可施設一覧」（https://www.city.fukui.lg.jp/fukusi/eisei/syokuhin/p070519.html）、「環境衛生関係施設一覧」（https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518.html）を加工して作成（CC BY-SA）`.
  - **MUST NOT**: imply endorsement; claim accuracy on the city's authority.
  - **§4's open-ended prohibited acts accepted knowingly** (owner,
    2026-10-01; Taoyuan's pattern). §3 is a disclaimer only.
- **MHLW open data** (control only): PDL 1.0, as read for Fukuoka.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

Read only 施設名称 / 営業所名称, 業種 and the premises address. The three
operator columns are read in memory by the name rule and never kept;
**申請者住所 and 申請者電話番号 are never selected**. Run
`check_personal_exposure.py` with `japan=True` (it also covers the site
policy's privacy clause). No row value was printed for this brief.

## Region

`"region"`: the Japan sub-region (minor tier, above); `"country": "Japan"`.
Project to **UTM 53N (EPSG:32653)**.

## Open items

- 🚨 **The name rule on a list that withholds sole traders' names**: Fukui
  names operators for companies only, so the rule flags 20 food rows and
  cannot see the rest. Recommendation: accept it as the owner accepted MHLW's
  rows for Fukuoka, with the matching page bullet.
- 🚨 **`mode`**: no metro; railways (JR, Hapi-line, Echizen, Fukubu) and a
  street section. The skill's rule (the highest-order mode drawn) would say
  `metro`; the urban backbone says `tram`. The owner's call; no built
  precedent.
- ⚠️ **The share-alike build items**: `LICENSE` line, data-sources row and
  notice (above). The credit wording is a proposal for the drafts file.
- ⚠️ `japan_eigyo`: 飲食店 and 喫茶店 (93 old-law restaurants).
- ⚠️ `OPERATOR_COLS` (three spellings), `NAME_COLS` (営業所名称), the
  newest-sheet reader, the ward-less flag; each re-runs the Minato control.
- ⚠️ N02-25 for this city.
- ⚠️ Gate 3 and the Fukubu Line's frequency, from the operators.
- ⚠️ OSM `name:en` for 45 station groups.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`,
  after step 2): the census has **1,569** 飲食店 establishments in 18201.
  Before de-duplication about 2,950 Food service rows are placed (with the 93
  added), about 1.9 per establishment (Hiroshima's built figure: 1.80).
- ⚠️ The 菓子 / そうざい factory share, printed by step 2.
- ⚠️ The monthly file names change (`_202608` becomes `_202609`): the checks
  below fail when the city publishes the next month, which means the brief's
  file names need updating, not the check relaxing.

```brief-checks
[
  {
    "id": "fukui-food-live",
    "claim": "Fukui City's food-permit workbook (month-end sheets, newest 2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.fukui.lg.jp/fukusi/eisei/syokuhin/p070519_d/fil/11syokuhin_202608.xlsx",
    "min_bytes": 2000000
  },
  {
    "id": "fukui-food-closures-live",
    "claim": "Fukui City's monthly food-closures workbook is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.fukui.lg.jp/fukusi/eisei/syokuhin/p070519_d/fil/12syokuhinhaigyo_202608.xlsx",
    "min_bytes": 30000
  },
  {
    "id": "fukui-barber-live",
    "claim": "Fukui City's barber list (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518_d/fil/01riyou_202608.xlsx",
    "min_bytes": 100000
  },
  {
    "id": "fukui-beauty-live",
    "claim": "Fukui City's beauty-salon list (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518_d/fil/02biyou_202608.xlsx",
    "min_bytes": 300000
  },
  {
    "id": "fukui-laundry-live",
    "claim": "Fukui City's laundry list (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518_d/fil/03cleaning_202608.xlsx",
    "min_bytes": 100000
  },
  {
    "id": "fukui-food-page-current",
    "claim": "The food page still offers the 2026-08 workbook (a newer month means the brief's file names are stale)",
    "kind": "http_contains",
    "url": "https://www.city.fukui.lg.jp/fukusi/eisei/syokuhin/p070519.html",
    "present": ["11syokuhin_202608.xlsx", "12syokuhinhaigyo_202608.xlsx"]
  },
  {
    "id": "fukui-personal-page-current",
    "claim": "The 環境衛生 page still offers the 2026-08 barber, beauty and laundry workbooks",
    "kind": "http_contains",
    "url": "https://www.city.fukui.lg.jp/fukusi/eisei/kankyo/p070518.html",
    "present": ["01riyou_202608.xlsx", "02biyou_202608.xlsx", "03cleaning_202608.xlsx"]
  },
  {
    "id": "fukui-site-policy-by-sa",
    "claim": "The site policy is live and still points at the CC licences. Its CC BY-SA sentence cannot be pinned here: the server sends no charset, so the check reads the UTF-8 page as Latin-1; re-read the sentence by eye at build",
    "kind": "http_contains",
    "url": "https://www.city.fukui.lg.jp/sisei/kohou/hp/site-p.html",
    "present": ["creativecommons.jp/licenses/"]
  },
  {
    "id": "fukui-mhlw-live",
    "claim": "MHLW's open-data file for Fukui City (18201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=18201_food_business_all.csv",
    "min_bytes": 200000
  },
  {
    "id": "fukui-isj-live",
    "claim": "MLIT's block-level address file for Fukui City (18201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/18201-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "fukui-projected-crs",
    "claim": "Fukui projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 136.22,
    "expect": "EPSG:32653"
  }
]
```
