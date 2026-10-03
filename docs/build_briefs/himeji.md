# Himeji — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live). Run `python scripts/brief_check.py himeji` before writing any code.
Then the `japan-city` skill. Coordinates: the `address-join` skill, measured
with `pipeline/countries/japan_register.py`'s own functions from a scratch
script (`scripts/screen_japan_join.py` has no Himeji entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line, from the
shared cache.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the city get
rings, JR and the private lines are cut at the line, a one-station stub stays
as cut, and an URBAN line cut to a stub goes back to the owner (2026-09-24,
2026-09-27); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**: where
the trade name IS the operator's own name, the pin shows its permit type, the
operator column read in memory only (2026-09-27); (6) **no page says
"currently operating"**. Fault-based cost clauses are accepted for all of
Japan (2026-09-24); English station names from OSM `name:en`, numerals as
figures before 丁目.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Himeji
joins them as the 2026-10-01 batch did: `label_tier: "minor"` (dot and tooltip
in every view, pill only in its own region), in the Japan sub-region that
batch creates. Wave 2 adds no region of its own.

**✅ `mode`: `metro`.** The owner's rule (2026-10-02): Dublin's precedent
unless JR is the city's largest rail network by stations inside the city line.
Here JR West has 16 station groups against Sanyō Electric Railway's 15, and
there is no tram or light rail to weigh: both networks are heavy rail, so the
backbone reads `metro` either way.

---

## The one-line summary

**All three buckets from the city's own CC BY 4.0 catalogue
(`city.himeji.gkan.jp`): a full food-permit list (8,347 rows as of 2026-09-10;
6,893 restaurant rows, 103% of the official 6,706) and full barber (380),
beauty (1,336) and laundry (189) registers of the same date.** The block join
places 79.8% of fixed premises at the block and 17.6% at a town centroid
(central towns are small: the median town around a centroid-tier row spans
222 m), 2.6% unplaced. Rail: JR West and Sanyō, 31 station groups. **Band A
recommended.**

---

## Business leg — the city's catalogue (姫路市・播磨圏域連携中枢都市圏オープンデータカタログサイト)

A CKAN under `/gkan/` (API `https://city.himeji.gkan.jp/gkan/api/3/action/…`);
the resource URLs sit under `/admin/gkan/` and answer a plain keyless GET.
Each dataset keeps about a year of monthly 全件 (full) resources, the newest
last; **the build reads the newest**, pinned by resource id. Organisation
姫路市健康福祉局 (保健所衛生課). Every latest resource is datastore-backed.

| | Food (`shokuhinn`, 食品営業許可施設一覧) | Barbers (`riyousyo`, 理容所一覧) | Beauty (`biyousyo`, 美容所一覧) | Laundries (`kuriininngu`, クリーニング所一覧) |
|---|---|---|---|---|
| **File** | `https://city.himeji.gkan.jp/admin/gkan/dataset/3868a36d-3029-4502-817b-3094e3ed4806/resource/0738c22f-2527-43d7-a96f-df2d6abb8f9f/download/282014_kyoka-syokuhinn_20260910.xlsx` | `https://city.himeji.gkan.jp/admin/gkan/dataset/7d4810cc-723a-46a8-b2e2-98cb859cb65c/resource/f7d723fa-d1f6-4dbf-8291-6acb6cccc1aa/download/282014_kyoka-riyou_20260910.xlsx` | `https://city.himeji.gkan.jp/admin/gkan/dataset/77e05f08-cefc-4a8d-8749-e4e239256059/resource/6b9230ee-715e-4b34-a424-8abb84a96f82/download/282014_kyoka-biyou_20260910.xlsx` | `https://city.himeji.gkan.jp/admin/gkan/dataset/66a768cb-5017-4e4b-8998-2479035b9dd3/resource/8d3ab779-8035-4dfd-9b5d-2d91c6418aad/download/282014_kyoka-kuriininngu_20260910.xlsx` |
| Bytes | **741,824** | **49,996** | **144,029** | **31,045** |
| Rows | **8,347** (one sheet, `食品`) | **380** (`理容所`) | **1,336** (`美容所`) | **189** (`クリーニング所`) |
| As of | **2026-09-10** (resource 「（全件）（令和8年9月10日時点）」; newest 許可日 2026-09-09; uploaded 2026-09-24) | 2026-09-10 | 2026-09-10 | 2026-09-10 |
| Cadence | monthly, a new 全件 resource each month (as of the 10th, posted mid-month) | monthly | monthly | monthly |
| Columns | **業種**, 氏名, **施設名称**, **所在地**, 方書, 電話番号, 許可番号, 許可日, 有効期限 | **業種**, 氏名, **施設名称**, **施設所在地**, 方書, 電話番号, 確認番号, 確認日 | as barbers | as barbers |

The header is the first row in every file; the address column is
`ADDR_COLS`' 所在地 (food) and 施設所在地 (registers), the name `NAME_COLS`'
施設名称, the type `TYPE_COLS`' 業種. The food list's own notes: vending
machines are left out, and premises that have closed may remain.

**Counts that matter** (`japan_eigyo` as it stands, fixed premises with an
address that is not 市内一円):

| Bucket | Types | Rows |
|---|---|---|
| Food service | 飲食店営業 5,694, 喫茶店営業 12, 簡易な営業 3, 住宅宿泊事業 1 | **5,710** fixed; **6,893** restaurant rows in all, of which **1,161** are 市内一円 stalls and vehicles (露店 / 自動車 in the type) |
| Retail | 菓子製造業 613, 魚介類販売業 212, 食肉販売業 198, そうざい製造業 130 | **1,153** fixed |
| Personal services | 理容所 380, 美容所 1,336, クリーニング所 189 (取次所 123, 一般 66) | **1,905** |
| Out | manufacturing (麺類, 水産製品, …), stalls, vehicles | 320 fixed rows |

- **Official counts** (e-Stat 衛生行政報告例 FY2024, year end 2025-03-31): 飲食店営業
  **6,706** (old law 2,016 + new law 4,690), so the list's 6,893 restaurant
  rows are **103%**; 理容所 **398** (list 95%), 美容所 **1,308** (102%),
  クリーニング所 **202** (94%). A complete register.
- **Expiry**: 有効期限 runs 2026-11-30 to 2033-08-31; no row is past its date
  on 2026-09-10 (300 lapse in 2026-11). Pin `as_of` to the list's own date
  (Kyoto's rule).
- 理容所 / 美容所 carry a second type, 「（市条例第３条第２項該当）」 (4 barbers, 182
  beauty salons): a premises under the city ordinance's article 3(2). ⚠️ Read
  what it covers at build; `japan_eigyo` counts both as Personal services
  (the source decides), and nothing suggests they are not shops.

### MHLW's file — not needed

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28201_food_business_all.csv`:
660,350 B, 2,313 rows (許可 167, 届出 2,146); **132 open restaurant permits,
2% of the official count** (opt-in online filings), and **94 of the 104 it
places are already in the city's list** (same town, block and trade name). The
city's list is the food source (the Kobe and Toyama shape). Its notifications
would add a partial food-retail bucket; recommended left out, as Toyama's, and
the page's standing bullet covers notified shops. No MHLW credit is then
needed.

### Operator columns and the name rule

- **The operator column is 氏名** (all four files), filled on every row, for
  individuals and companies alike (company markers on 3,223 of 8,347 food
  rows, 33 / 278 / 145 of the registers'). **`japan_register.OPERATOR_COLS`
  does NOT cover 氏名**: add it (shared code; re-run the Minato control), or
  the name rule compares nothing.
- Measured in memory with 氏名 mapped to a known spelling: **18 food rows**
  whose trade name is the operator's own name; barbers, beauty and laundries 0.
- 電話番号 (the premises' phone) is never selected.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 28201)

Block `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28201-24.0a.zip`
(513,893 B; 62,806 block keys) and town-chōme `…/19.0b/28201-19.0b.zip`
(18,755 B; 859). **Ward-less**: Himeji has no wards, and its town names begin
with the former towns' 区 (飾磨区, 網干区, 広畑区, 大津区, 勝原区, 余部区), so the
address must never be split at a 区: `japan.CITIES` needs `"wardless": True`
(the batch's flag, unchanged).

| Tier | Food (7,183 fixed) | Barbers (380) | Beauty (1,336) | Laundries (189) | All (9,089) |
|---|---|---|---|---|---|
| Block | **79.4%** | 82.1% | 81.6% | 80.4% | **79.8%** |
| Town-chōme / 大字 centroid | 17.9% | 15.8% | 16.7% | 15.3% | **17.6%** |
| Unplaced | 2.7% | 2.1% | 1.7% | 4.2% | **2.6%** |

**Why the centroid tier is large, and why it is mostly near block precision.**
- **The central business district's small towns** (南町, 塩町, 魚町, 駅前町, 立町)
  file large 地番 that MLIT's block file lacks (南町1 alone, 49 rows). Those
  towns are a few blocks each: of the 1,601 centroid-tier rows, **662 sit in
  towns whose blocks all lie within 250 m of the centroid** (90th
  percentile), 892 within 500 m; the median town radius over these rows is
  **222 m**.
- **364 rows are in rural 大字 with no MLIT block at all** (家島町 islands,
  夢前町, 安富町, 香寺町): a 大字 centroid, far from any station.
- **Unplaced (233)**: mostly **甲 / 乙 / 丙 地番** (白浜町甲1920, 阿保甲611,
  西庄甲): MLIT files 白浜町's numbers without the 甲 (8 of 1,201 keep it). A
  rule that drops a trailing 甲乙丙丁 from the town and looks the number up in
  the bare town finds 193 of 221 such rows, 60 of them in numbers MLIT places
  more than 500 m apart; ⚠️ a shared-code rule at build (block for the
  unambiguous 133, the bare town's centroid for the rest), with the Minato
  control re-run.

**Independent check**: the city list has no coordinates. MHLW's own points
for its Himeji rows against the block point: **median 43 m, 93.8% within
250 m** (632 rows, 10 over 1 km); at the centroid tier a median 196 m (207
rows).

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (28201)

N03 extent S 34.5929, W 134.4222, N 35.0944, E 134.8136 (534 km², the 家島
islands included). **34 station records inside, 31 N02_005g groups** (widest
91 m). **The Shinkansen's 姫路** is dropped; 姫路 stays as a JR station.

| Operator | N02 line (class) | Inside / N02 total | Stations inside |
|---|---|---|---|
| 山陽電気鉄道 | 本線 (12) | 9 / 43 | 大塩, 的形, 八家, 白浜の宮, 妻鹿, 飾磨, 亀山, 手柄, 山陽姫路 |
| 山陽電気鉄道 | 網干線 (12) | **7 / 7** | 飾磨, 西飾磨, 夢前川, 広畑, 山陽天満, 平松, 山陽網干 |
| 西日本旅客鉄道 | 山陽線 (11) | 7 / 131 | 網干, 英賀保, 姫路, 東姫路, 御着, ひめじ別所, はりま勝原 |
| 西日本旅客鉄道 | 播但線 (11) | 7 / 18 | 姫路, 京口, 野里, 砥堀, 仁豊野, 香呂, 溝口 |
| 西日本旅客鉄道 | 姫新線 (11) | 4 / 36 | 姫路, 播磨高岡, 余部, 太市 |

- **31 groups: JR West 16, Sanyō 15** (飾磨 is one group on both Sanyō lines).
  JR 姫路 and 山陽姫路 are separate groups; the closest pair of groups is 219 m
  apart.
- **Stub test: passes.** No line is cut to a stub: the shortest in-city
  stretch is the 姫新線's 4 (a rural line running on to Tatsuno and Sayō).
- **Median gap to the nearest station 1,377 m**: standard rings (0.6 mi
  outer) on the spacing rule.
- **Gate 3**: Sanyō's own station index lists all 15 in-city stations (the
  check below names the Aboshi Line's six beyond 飾磨). JR West's per-line
  counts are a build read.
- ⚠️ **OSM `name:en`** for every station at build (one Overpass query, the
  session's single slot; none was run for this brief). 山陽姫路 / 姫路,
  山陽網干 / 網干 and 山陽天満 need readable English forms.

## Scope

**Himeji City (28201), one municipality, no wards.** JR's three lines and
Sanyō's main line run on to Takasago, Tatsuno, Fukusaki and Ibo; cut at the
line.

## Licences — read 2026-10-02

- **Himeji City's four datasets — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - **The grant**: each `package_show` records `license_id: CC-BY-4.0`
    (「クリエイティブ・コモンズ・ライセンス 表示 4.0 国際」), shown on each dataset
    page. The catalogue's terms
    (`https://city.himeji.gkan.jp/gkan/base/doc/Terms_of_use_260430.pdf`,
    施行 2026-03-06) apply PDL 1.0 by default and give way to a CC BY 4.0
    marking (1.4(1)); 1.7: where the same content is published on another
    site, the catalogue's terms prevail over that site's own.
  - **MUST DISPLAY** (the terms' 1.1, filled in, per dataset, with the CC BY
    4.0 link):
    `出典：「食品営業許可施設一覧」（姫路市）（https://city.himeji.gkan.jp/gkan/dataset/shokuhinn）を加工して作成`,
    and likewise 「理容所一覧」 (`…/dataset/riyousyo`), 「美容所一覧」
    (`…/dataset/biyousyo`), 「クリーニング所一覧」 (`…/dataset/kuriininngu`).
  - **MUST NOT** present edited data as if the city made it (1.1 ２). CC BY 4.0
    itself: no endorsement implied.
  - **No cost or indemnity clause** in the catalogue terms.
- **MLIT 位置参照情報 and N02**: PDL 1.0 (the skill's notice lines). **MLIT
  N03**: CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

Every file carries **氏名** (individual operators' names) and 電話番号. Select
施設名称, 業種 and the premises address (所在地 / 施設所在地, 方書 if used);
read 氏名 in memory for the name rule only. Run
`check_personal_exposure.py` with `japan=True`. No row value was printed for
this brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 53N (EPSG:32653)**.

## Open items

- No 🚨 item: every call follows a standing call or a built precedent.
- ⚠️ **Shared code**: `OPERATOR_COLS` + 氏名; the 甲乙丙 地番 rule (above); a
  `japan.CITIES` entry (`"pref": "28"`, `"n02": "25"`, `"wardless": True`,
  wards `["28201"]`, EPSG 32653). Each re-runs the Minato control.
- ⚠️ **`japan_eigyo`**: 複合型そうざい製造業 (3 rows) reads "no rule" and stays
  out; whether it is そうざい for the standing call is a taxonomy line at build.
  飲食店営業（住宅宿泊事業） (1) reads Food service.
- ⚠️ 「市条例第３条第２項該当」 (186 register rows): read the ordinance at build.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`):
  the 2021 census counts **2,297** 飲食店 establishments in 28201; **5,528**
  distinct placed restaurant premises is **2.41 per establishment**, inside
  the complete lists' band (2.0 to 3.3; Kobe 2.38).
- ⚠️ The 菓子 / そうざい factory share, printed by step 2.
- ⚠️ OSM `name:en`, gate 3 for JR, line colours on both basemaps.

```brief-checks
[
  {
    "id": "himeji-food-live",
    "claim": "Himeji's full food-permit list (as of 2026-09-10) is keyless and live on the city's catalogue",
    "kind": "http_ok",
    "url": "https://city.himeji.gkan.jp/admin/gkan/dataset/3868a36d-3029-4502-817b-3094e3ed4806/resource/0738c22f-2527-43d7-a96f-df2d6abb8f9f/download/282014_kyoka-syokuhinn_20260910.xlsx",
    "min_bytes": 500000
  },
  {
    "id": "himeji-food-rows",
    "claim": "The food list of 2026-09-10 holds 8,347 rows",
    "kind": "ckan_rows",
    "domain": "city.himeji.gkan.jp/gkan",
    "resource_id": "0738c22f-2527-43d7-a96f-df2d6abb8f9f",
    "expect": 8347
  },
  {
    "id": "himeji-barber-rows",
    "claim": "The barber register of 2026-09-10 holds 380 rows",
    "kind": "ckan_rows",
    "domain": "city.himeji.gkan.jp/gkan",
    "resource_id": "f7d723fa-d1f6-4dbf-8291-6acb6cccc1aa",
    "expect": 380
  },
  {
    "id": "himeji-beauty-rows",
    "claim": "The beauty-salon register of 2026-09-10 holds 1,336 rows",
    "kind": "ckan_rows",
    "domain": "city.himeji.gkan.jp/gkan",
    "resource_id": "6b9230ee-715e-4b34-a424-8abb84a96f82",
    "expect": 1336
  },
  {
    "id": "himeji-laundry-rows",
    "claim": "The laundry register of 2026-09-10 holds 189 rows",
    "kind": "ckan_rows",
    "domain": "city.himeji.gkan.jp/gkan",
    "resource_id": "8d3ab779-8035-4dfd-9b5d-2d91c6418aad",
    "expect": 189
  },
  {
    "id": "himeji-barber-live",
    "claim": "The barber register's file is keyless and live",
    "kind": "http_ok",
    "url": "https://city.himeji.gkan.jp/admin/gkan/dataset/7d4810cc-723a-46a8-b2e2-98cb859cb65c/resource/f7d723fa-d1f6-4dbf-8291-6acb6cccc1aa/download/282014_kyoka-riyou_20260910.xlsx",
    "min_bytes": 30000
  },
  {
    "id": "himeji-beauty-live",
    "claim": "The beauty-salon register's file is keyless and live",
    "kind": "http_ok",
    "url": "https://city.himeji.gkan.jp/admin/gkan/dataset/77e05f08-cefc-4a8d-8749-e4e239256059/resource/6b9230ee-715e-4b34-a424-8abb84a96f82/download/282014_kyoka-biyou_20260910.xlsx",
    "min_bytes": 100000
  },
  {
    "id": "himeji-laundry-live",
    "claim": "The laundry register's file is keyless and live",
    "kind": "http_ok",
    "url": "https://city.himeji.gkan.jp/admin/gkan/dataset/66a768cb-5017-4e4b-8998-2479035b9dd3/resource/8d3ab779-8035-4dfd-9b5d-2d91c6418aad/download/282014_kyoka-kuriininngu_20260910.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "himeji-food-licence",
    "claim": "The food dataset's catalogue record says CC-BY-4.0 and still points at the 2026-09-10 file",
    "kind": "http_contains",
    "url": "https://city.himeji.gkan.jp/gkan/api/3/action/package_show?id=shokuhinn",
    "present": ["\"license_id\": \"CC-BY-4.0\"", "282014_kyoka-syokuhinn_20260910.xlsx"]
  },
  {
    "id": "himeji-barber-licence",
    "claim": "The barber dataset's catalogue record says CC-BY-4.0 and points at the 2026-09-10 file",
    "kind": "http_contains",
    "url": "https://city.himeji.gkan.jp/gkan/api/3/action/package_show?id=riyousyo",
    "present": ["\"license_id\": \"CC-BY-4.0\"", "282014_kyoka-riyou_20260910.xlsx"]
  },
  {
    "id": "himeji-beauty-licence",
    "claim": "The beauty dataset's catalogue record says CC-BY-4.0 and points at the 2026-09-10 file",
    "kind": "http_contains",
    "url": "https://city.himeji.gkan.jp/gkan/api/3/action/package_show?id=biyousyo",
    "present": ["\"license_id\": \"CC-BY-4.0\"", "282014_kyoka-biyou_20260910.xlsx"]
  },
  {
    "id": "himeji-laundry-licence",
    "claim": "The laundry dataset's catalogue record says CC-BY-4.0 and points at the 2026-09-10 file",
    "kind": "http_contains",
    "url": "https://city.himeji.gkan.jp/gkan/api/3/action/package_show?id=kuriininngu",
    "present": ["\"license_id\": \"CC-BY-4.0\"", "282014_kyoka-kuriininngu_20260910.xlsx"]
  },
  {
    "id": "himeji-catalogue-terms",
    "claim": "The catalogue's terms of use (PDF, 施行 2026-03-06) are live",
    "kind": "http_ok",
    "url": "https://city.himeji.gkan.jp/gkan/base/doc/Terms_of_use_260430.pdf",
    "min_bytes": 50000,
    "content_type_contains": "pdf"
  },
  {
    "id": "himeji-mhlw-opt-in",
    "claim": "MHLW's open-data file for Himeji (28201) answers a plain keyless GET (the count control; 132 open restaurant permits on 2026-10-02)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28201_food_business_all.csv",
    "min_bytes": 300000
  },
  {
    "id": "himeji-sanyo-stations",
    "claim": "Sanyō Electric Railway's station index lists the in-city Aboshi Line stations (gate 3)",
    "kind": "http_contains",
    "url": "https://www.sanyo-railway.co.jp/railway/station/",
    "present": ["西飾磨", "夢前川", "広畑", "山陽天満", "平松", "山陽網干", "白浜の宮", "妻鹿"]
  },
  {
    "id": "himeji-isj-live",
    "claim": "MLIT's block-level address file for Himeji (28201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28201-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "himeji-projected-crs",
    "claim": "Himeji projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 134.69,
    "expect": "EPSG:32653"
  }
]
```
