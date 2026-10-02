# Toyama — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py toyama`
before writing any code. Coordinates: the `address-join` skill, measured with
the shared `japan_register` functions under this brief's own column mapping
(the shared `scripts/screen_japan_join.py` table was not edited; add a
`toyama` entry there at the build). Rail: MLIT N02-25 cut at the N03 city
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

**✅ Minor label tier (owner, 2026-10-02):** Toyama is in the 2026-10-01
Japanese batch and carries `label_tier: "minor"`, with the whole France and
Czechia precedent: a Japan sub-region (one or a split, by
`check_macro_labels.py`, never by eye), every Japanese city moved into it,
and `REGION_LABELS_ALSO["East Asia"]` gaining it. **The eight built Japanese
cities stay eligible.** The first city of the batch makes the change.

---

## The one-line summary

**One city list carries every food permit (5,616 rows as of 2026-06-30, 4,286
restaurants: 99.9% of the official 4,292), and three CC BY 4.0 registers carry
the barbers, beauty salons and laundries (1,659 rows, 2026-03).** All three
buckets. The block join places 86.5% of fixed food premises at the block, but
**12.2% only at a town centroid that sits a median 360 m from the premises**;
MHLW's file lists the same premises with its own coordinates, and it has a
point for 614 of the 738 rows the block join misses. Rail: the Chitetsu tram
and Portram (39 stops in N02), four Chitetsu railway lines, Ainokaze and JR
Takayama, 74 station groups inside the city.

---

## Business leg — the city's own CKAN (`opdt.city.toyama.lg.jp`)

Toyama City's own portal, not Toyama Prefecture's (whose catalogue
`ckan.tdcp.pref.toyama.jp` answers 403 to this machine; not used, not routed
around). No datastore on any resource, so the checks below are `http_ok` and
`package_show` reads.

| | Food (`seikatsu-eisei01`, 食品営業許可施設) | Barbers (`-02`, 理容営業許可施設) | Beauty (`-03`, 美容営業許可施設) | Laundries (`-06`, クリーニング営業許可施設) |
|---|---|---|---|---|
| **File** | `https://opdt.city.toyama.lg.jp/dataset/fb1198c6-3ac2-42fc-ae99-81ea5ba09a2d/resource/fa38003f-accd-4690-b71b-96b1d78e1c45/download/syokuhin.xlsx`: **791,048 B**, one sheet `6月末` | `…/dataset/afafefa1-ec7c-4c1e-97c9-ab91ccf9b55f/resource/e6b559f9-d951-4e09-a6b6-15292cb9a96c/download/riyosyo202603.xlsx`: **41,212 B** | `…/dataset/9d0ead57-7589-40bf-be73-0d550360e389/resource/8848e4a0-e719-4708-b33d-908a856714f3/download/biyosyo202603.xlsx`: **164,787 B** | `…/dataset/8a268965-69f8-4a49-a8eb-bd00696950a1/resource/b2ab3395-a04d-43f1-be83-0ef860776524/download/cleaning202603.xlsx`: **31,574 B** |
| Rows | **5,616** | **372** | **1,052** | **235** (取次所 169, クリーニング所 59, 無店舗取次店 7) |
| As of | **2026-06-30** (resource 「食品営業許可施設(令和8年6月）」, uploaded 2026-07-06; newest 許可年月日 2026-06-30) | 2026-03 (file name; uploaded 2026-05-18) | 2026-03 | 2026-03 |
| Cadence | 年４回 (quarterly) | 年２回 | 年２回 | 年２回 |
| Columns | 営業者名, **営業者住所** (merged header over 5 columns), 施設名, **施設住所** (merged header over 4 columns: municipality, town, number, building), 営業の種類, 許可番号, 初回許可年月日, 許可年月日, 許可満了日 | 施設名, **所在地**, ビル名, 営業者名, **営業者住所**, 開設日年月日, 確認番号 | as barbers | 業種, 施設名, **施設住所** (+ an unheaded building column), 営業者名, **営業者住所**, 開設年月日, 確認番号 |

- **Restaurants**: ① 飲食店営業 **4,286** rows (138 of all rows are 市内一円
  mobile vendors); **4,141 fixed**. The official FY2024 count (e-Stat
  衛生行政報告例) is **4,292**: the list holds 99.9% of it.
- **Food retail (permit types)**: ⑪ 菓子製造業 604 · ㉕ そうざい製造業 168 ·
  ④ 魚介類販売業 182 · ③ 食肉販売業 124 = **1,078 fixed**. Out by
  `japan_eigyo`: manufacturing (237, "no rule") and vending (15).
- **Personal services**: 372 + 1,052 + 226 fixed (the 7 無店舗取次店 and 2
  市内一円 laundry rows are not premises) = **1,650**.
- ⚠️ **Lapsing rows**: 208 rows (158 restaurants) carry a 許可満了日 between
  2026-07-22 and 2026-10-01, after the list's as-of date. 53 of those
  restaurants reappear in MHLW's file under a renewed permit. The next
  quarterly edition drops or renews them; pin `as_of` to the list's own date
  (Kyoto's rule).

### MHLW's file — the same permits, with coordinates

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=16201_food_business_all.csv`:
**2,810,448 B, 8,168 rows** (許可 5,578, 届出 2,572, 許可(廃業) 18), newest
許可年月日 2026-08-31. **Toyama enters its permits there too**: 4,258 open
restaurant permits against the city's 4,286, and **94.8% of MHLW's block-tier
restaurant permits (2,933 of 3,093) are in the city's list with the same
town, block and trade name**. Only 82.0% of MHLW's restaurants carry an
address (by consent), against the city list's 100%.

**So the city's list is the food source** (the Kobe / Osaka / Sapporo shape:
a complete own list), and MHLW's file is used for two things only, both at
the build: the count control above, and **its own points as the fallback for
city rows the block join misses** (Coordinates, below). Its 2,572
notifications (konbini, supermarkets) would add a partial food-retail bucket;
the precedent for a city with a complete own list is to leave them out and
say so in the page's standing bullet. Recommended: leave them out.

### Operator columns and the name rule

- The food list's operator column is **営業者名**, which
  `japan_register.OPERATOR_COLS` **already covers**. The registers spell it
  the same.
- **The city publishes operators' names only for companies.** 営業者名 is
  blank on 2,703 of 5,616 food rows, and 2,855 of the 2,913 filled carry a
  company marker; the registers fill it on 24 of 372, 188 of 1,052 and 181 of
  235 rows, nearly all companies. The blank cells are not merges (the sheet
  has none in its data area). **So the name rule can compare only the few
  individuals the list names: it flags 13 food rows**, and cannot see a sole
  trader whose trade name is their own name. This is the position the owner
  accepted for MHLW's rows in Fukuoka (no individual-operator column).
- **営業者住所 is an operator's own address**: never select it (food columns
  1-5, registers' 営業者住所).

### What the shared code does not read yet (build-time)

- ⚠️ **The food workbook's 施設住所 header is merged over four columns**
  (H1:K1: municipality, town, number, building) and the operator's address
  over five (B1:F1). `xlsx_rows` zips the header to the cells, so the
  address would read as 「富山市」 alone (measured: every row then joined
  nowhere). Read by position, or a reader that joins the merged columns; the
  numbers above come from columns H+I+J.
- ⚠️ `ADDR_COLS` lacks **所在地** and **施設住所**; `NAME_COLS` lacks **施設名**.
  Add Toyama's spellings (never 営業者住所), then re-run the Minato control.
- ⚠️ **The ward regex on a city without wards**: `permits_from_rows` splits
  `^(\D+?区)` off as a ward, and Toyama's neighbourhood names end in 区
  (`太田北区`, `五福六区`, `大泉一区`, `上大久保三区`): 9 food rows, 6 register rows
  and 9 MHLW rows misparse. A config flag for a ward-less city, with the Minato
  control re-run.

---

## ⚠️ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 16201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/16201-24.0a.zip` (555,530 B) and
`…/19.0b/16201-19.0b.zip` (25,024 B): 56,997 block keys, 1,281 town-chōme.

| Tier | Food list (5,471 fixed) | Registers (1,650) | MHLW, addressed (6,676) |
|---|---|---|---|
| Block | **86.5%** | **80.5%** | 84.3% |
| Town-chōme / 大字 centroid | **12.2%** | **14.6%** | 13.9% |
| Unplaced | 1.3% | 4.8% | 1.8% |

**Independent check** (MHLW's own point for the same premises, matched on
town and trade name): city rows at the **block** tier sit a **median 34 m**
away (3,923 rows, 95.3% within 250 m); rows at the **chōme** tier a **median
360 m** (559 rows, 37.2% within 250 m, 78 over 1 km). Toyama's merged
municipalities (婦中町, 八尾町, 水橋, 大沢野) are 大字 with 地番 addresses
that MLIT's block file does not key, and a 大字 centroid is a poor point.

⚠️ **Recommended at build (measured grounds)**: where a city row misses the
block tier and MHLW lists the same premises with its own point, use MHLW's
point. **614 of the 738** non-block food rows have one. This is
`OWN_POINT_FALLBACK` taken from a second source rather than the row's own;
shared code, with the Minato control re-run. The registers have no such
fallback; their 14.6% stays at the centroid and the page's standing bullet
covers it.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (16201)

The city is large (the Ōyama mountains to 有峰): bbox S 36.3697, W 137.0282,
N 36.7667, E 137.7055. **84 station records inside, 74 N02_005g groups.**
Shinkansen: 富山 on the 北陸新幹線, dropped.

| Operator | N02 line (class) | Inside / total | Reading |
|---|---|---|---|
| 富山地方鉄道 (tram) | 本線 (21) 14/14 · 支線 4/4 · 安野屋線 3/3 · 呉羽線 3/3 · 富山都心線 5/5 · 富山駅南北接続線 1/1 | all inside | **The city tram: 25 stop groups** in N02 |
| 富山地方鉄道 (Portram) | 富山港線 (12) 11/11 · 富山港線 (21) 4/4 | all inside | **14 more groups**: 39 with the tram |
| 富山地方鉄道 | 上滝線 (12) | 10/11 | passes |
| 富山地方鉄道 | 不二越線 (12) | 5/5 | passes |
| 富山地方鉄道 | 本線 (12) | 6/41 | cut at the line (電鉄富山 to 越中三郷) |
| 富山地方鉄道 | 立山線 (12) | 2/14 | 本宮 and 有峰口 only: a mountain fragment far from the urban area, drawn as cut by the standing call |
| あいの風とやま鉄道 | あいの風とやま鉄道線 (12) | 5/23 | cut at the line |
| 西日本旅客鉄道 | 高山線 (11) | 10/10 | passes (the Hida limited express counts) |
| 東海旅客鉄道 | 高山線 (11) | 1/36 | 猪谷 only, the JR West / JR Central boundary, already served by JR West's line: **leave it out** (`LEFT_OUT_LINES`, Fukuoka's Hakata-Minami precedent) |

- **The screen's "25 stops, the Port line included" was wrong**: N02 has 25
  groups for the city tram WITHOUT the Port line, 39 with it.
- ⚠️ **Gate 3, the operator's own stop counts**: not read. Chitetsu publishes
  its tram routes and timetables as PDFs (`https://www.chitetsu.co.jp/?page_id=656`);
  read them at build. N02 files the tram under seven legal sections; the
  public names are the operator's routes (系統, including 富山港線 / Portram
  and the 環状線 loop), so `config.LINES` needs Tokyo's `route` mechanism or
  one entry per legal section under its public route name.
- ⚠️ **Converted railway: 富山港線's class-12 section** (6.6 km, 11 stops,
  岩瀬浜 to 奥田中学校前) is the former JR Toyamakō Line; its class-21
  section (1.2 km) is street track. The light-rail test's frequency gate
  (15 minutes by day) applies to the converted part. By general knowledge it
  runs every 15 minutes by day; **not yet read from the operator's
  timetable**. Under the Japanese standing calls the line is drawn in any
  case; the gate decides what it is called and `mode`.
- ⚠️ OSM `name:en` for every station and tram stop at build (no OSM was
  queried for this brief). Several tram stops carry naming-rights names
  (`トヨタモビリティ富山Gスクエア五福前（五福末広町）`, `粟島（大阪屋ショップ前）`):
  read each English name. The tram stops need `TRAM_OSM_JSON` (railway=tram_stop).

## Scope

**Toyama City (16201), one municipality, no wards.** Ainokaze, Chitetsu's
main and Tateyama lines and JR Central run on to Takaoka, Namerikawa,
Kamiichi, Tateyama and Hida; cut at the line.

## Licences — read 2026-10-02

- **Toyama City's four datasets — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - **The grant**: each `package_show` records `license_id: cc-by`
    (ライセンス extra "CC-BY"); the portal's terms
    (`https://opdt.city.toyama.lg.jp/pages/terms`) 第１条１ apply CC BY 4.0
    International to the city's works unless a resource sets its own. None
    does.
  - **MUST DISPLAY** (第１条２(2), for edited content): 「この[作品]は以下の著作物を改変して利用しています。」
    then, per dataset, `［データのタイトル］、富山市、クリエイティブ・コモンズ・ライセンス 表示4.0国際`
    with the licence URL (or a link on the licence words). Titles:
    食品営業許可施設, 理容営業許可施設, 美容営業許可施設, クリーニング営業許可施設.
  - **MUST NOT**: present edited data as if the city made it (第１条１); use
    the city's logos (第３条).
  - **Cost** (第４条４): complaints from our own breach are resolved at our
    own cost. The fault-based class, ✅ accepted for every Japanese source
    (owner, 2026-09-24). Japanese law, the court for the city's seat (第６条).
- **MHLW open data** (if its points are used): **PERMITTED WITH CONDITIONS**
  (PDL 1.0), as read for Fukuoka (`fukuoka.md`): the processed-by credit, no
  completeness claim, no logo; the minor 2)ウ commercial-use point stays open.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

Read only 施設名, 営業の種類 and the premises address (columns H to K in the
food workbook). 営業者名 is read in memory by the name rule and never kept;
**営業者住所 is never selected**. Run `check_personal_exposure.py` with
`japan=True`. No row value was printed for this brief.

## Region

`"region"`: the Japan sub-region (minor tier, above); `"country": "Japan"`.
Project to **UTM 53N (EPSG:32653)**.

## Open items

- 🚨 **The name rule on a list that withholds sole traders' names**: Toyama
  publishes 営業者名 for companies only, so the rule compares almost nothing
  (13 food rows flagged). Recommendation: accept it as the owner accepted
  MHLW's rows for Fukuoka, and use the page's MHLW-style bullet ("the list
  does not say who the operator is, so this cannot be checked there") for
  the unnamed rows.
- 🚨 **`mode`**: every built Japanese city has a subway or Astram (`metro`).
  Toyama draws JR and Chitetsu railways plus a tram, and no metro; the skill's
  rule (the highest-order mode drawn) would say `metro`, the network's
  backbone says `tram`. The owner's call; no built precedent.
- ⚠️ MHLW's points as the chōme-tier fallback (614 of 738 rows), above.
- ⚠️ The merged-header reader, `ADDR_COLS` / `NAME_COLS` additions and the
  ward-less flag, above; each re-runs the Minato control.
- ⚠️ JR Central's 高山線 left out (one station, 猪谷, served by JR West).
- ⚠️ Gate 3 against Chitetsu's own stop counts; the Portram frequency read.
- ⚠️ OSM `name:en` for 74 station groups and the tram stops.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`,
  after step 2): the census has **1,695** 飲食店 establishments in 16201.
  Before de-duplication, 4,090 Food service rows are placed, about 2.4 per
  establishment (Hiroshima's built figure: 1.80); the control on the built
  pins decides whether that is the permit structure or a join problem.
- ⚠️ The 菓子 / そうざい factory share, printed by step 2.

```brief-checks
[
  {
    "id": "toyama-food-live",
    "claim": "Toyama City's food-permit workbook (as of 2026-06-30) is keyless and live on the city's CKAN",
    "kind": "http_ok",
    "url": "https://opdt.city.toyama.lg.jp/dataset/fb1198c6-3ac2-42fc-ae99-81ea5ba09a2d/resource/fa38003f-accd-4690-b71b-96b1d78e1c45/download/syokuhin.xlsx",
    "min_bytes": 500000
  },
  {
    "id": "toyama-barber-live",
    "claim": "Toyama City's barber register (2026-03) is keyless and live",
    "kind": "http_ok",
    "url": "https://opdt.city.toyama.lg.jp/dataset/afafefa1-ec7c-4c1e-97c9-ab91ccf9b55f/resource/e6b559f9-d951-4e09-a6b6-15292cb9a96c/download/riyosyo202603.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "toyama-beauty-live",
    "claim": "Toyama City's beauty-salon register (2026-03) is keyless and live",
    "kind": "http_ok",
    "url": "https://opdt.city.toyama.lg.jp/dataset/9d0ead57-7589-40bf-be73-0d550360e389/resource/8848e4a0-e719-4708-b33d-908a856714f3/download/biyosyo202603.xlsx",
    "min_bytes": 100000
  },
  {
    "id": "toyama-laundry-live",
    "claim": "Toyama City's laundry register (2026-03) is keyless and live",
    "kind": "http_ok",
    "url": "https://opdt.city.toyama.lg.jp/dataset/8a268965-69f8-4a49-a8eb-bd00696950a1/resource/b2ab3395-a04d-43f1-be83-0ef860776524/download/cleaning202603.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "toyama-food-ckan-licence",
    "claim": "The food dataset's catalogue record says cc-by and still points at syokuhin.xlsx",
    "kind": "http_contains",
    "url": "https://opdt.city.toyama.lg.jp/api/3/action/package_show?id=seikatsu-eisei01",
    "present": ["\"license_id\": \"cc-by\"", "syokuhin.xlsx"]
  },
  {
    "id": "toyama-barber-ckan-licence",
    "claim": "The barber dataset's catalogue record says cc-by and points at the 2026-03 file",
    "kind": "http_contains",
    "url": "https://opdt.city.toyama.lg.jp/api/3/action/package_show?id=seikatsu-eisei02",
    "present": ["\"license_id\": \"cc-by\"", "riyosyo202603.xlsx"]
  },
  {
    "id": "toyama-beauty-ckan-licence",
    "claim": "The beauty dataset's catalogue record says cc-by and points at the 2026-03 file",
    "kind": "http_contains",
    "url": "https://opdt.city.toyama.lg.jp/api/3/action/package_show?id=seikatsu-eisei03",
    "present": ["\"license_id\": \"cc-by\"", "biyosyo202603.xlsx"]
  },
  {
    "id": "toyama-laundry-ckan-licence",
    "claim": "The laundry dataset's catalogue record says cc-by and points at the 2026-03 file",
    "kind": "http_contains",
    "url": "https://opdt.city.toyama.lg.jp/api/3/action/package_show?id=seikatsu-eisei06",
    "present": ["\"license_id\": \"cc-by\"", "cleaning202603.xlsx"]
  },
  {
    "id": "toyama-terms-cc-by-4",
    "claim": "The portal's terms apply CC BY 4.0 International (the legal code is linked from 第１条)",
    "kind": "http_contains",
    "url": "https://opdt.city.toyama.lg.jp/pages/terms",
    "present": ["creativecommons.org/licenses/by/4.0/legalcode.ja"]
  },
  {
    "id": "toyama-mhlw-live",
    "claim": "MHLW's open-data file for Toyama City (16201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=16201_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "toyama-isj-live",
    "claim": "MLIT's block-level address file for Toyama City (16201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/16201-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "toyama-projected-crs",
    "claim": "Toyama projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 137.21,
    "expect": "EPSG:32653"
  }
]
```
