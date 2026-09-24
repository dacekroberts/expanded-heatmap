# Kyoto — build brief

**Step 0 measured 2026-09-24. Band A by the owner, with disclosures.** Run
`python scripts/brief_check.py kyoto` before writing any code. Coordinates:
the `address-join` skill, measured by `scripts/screen_japan_join.py kyoto`
and `kyoto-life`. **The register is REBUILT, not downloaded**:
`pipeline/countries/japan_register.kyoto_permit_stream()` does it, and the
build imports that function rather than copying it.

**✅ Decided by the owner, 2026-09-24, for every Japanese city:** (1) **the Shinkansen does not count**, since it is long-distance travel between cities; (2) **the city line only**: only stations inside the city get rings, matching the city-only permit list, with a per-line stub test at build (any urban line cut to a stub goes back to the owner); (3) **菓子製造業 and そうざい製造業 count**, in the Retail bucket (bakeries, confectioners and delis sell over a counter), with the factory and central-kitchen share measured from trade names before publishing.

**✅ Decided by the owner for Kyoto, 2026-09-24:**
- **Band A, on the rebuilt register**, with the disclosures below
  (Rotterdam's precedent).
- **Rail:**
  - Keihan Keishin passes the stub test.
  - The two funiculars are drawn.
  - The Sagano scenic line is left out.

---

## The one-line summary

**Kyoto has published no full food-permit list since the 2021 reform, only
each month's new permits. Stitching the 2021-03-31 list to every monthly list
since, and keeping permits still in their term, gives 22,259 fixed restaurants:
15.5 per 1,000 residents.** That sits inside the complete-list yardstick
(Sendai 9.5, Kobe 13.0, Osaka 19.0), just under Kyoto's own complete 2021 list
(16.7). ⚠️ **Closures are invisible**: a premises that closed stays until its
permit expires, 5–6 years after issue. The count is an upper bound, and the
page must say so. Personal services come from the city's own complete lists:
**5,828 premises**. The join places **92.7%** of food premises and **94.4%**
of personal services at block level.

---

## Business leg — a register rebuilt from its permit stream

| | |
|---|---|
| **Portal** | `data.city.kyoto.lg.jp`, the City's own. Its registering department is 保健福祉局 医療衛生企画課 |
| **00414** | 食品営業許可施設一覧: the **2021-03-31 full list** (resource 15447, an old `.xls`, 11 ward sheets, **35,019 rows**), plus the monthly lists for 2021-04 and 2021-05 |
| **00541** | The monthly lists of permits granted, 2021-06 to 2026-07: 62 XLSX (each also as PDF, not fetched) |
| **00530** | 理容所・美容所・クリーニング所 施設一覧: **complete lists as of 2026-03-31** (resources 21186, 21188, 21190), plus 11 monthly new-premises files for 2026-04 to 07. The 2025-03-31 lists are used for churn only |
| **Columns read** | Food: 営業所＿所在地１/２, 営業所＿名称（屋号・商号）１, 業種, 許可開始日, 許可終了日, 許可年月日. Personal: 施設名称, 施設所在地. **Operator columns are never read** (申請者＿申請者名, 役職名, 代表者, 申請者氏名) |
| **How to fetch** | ⚠️ **There is no API.** The portal is not CKAN, and it closed its SPARQL endpoint and API in 2023. Each file comes through the portal's own **download button**: GET the resource page (`/resource/?id=<n>`), then POST its form fields with the session cookie. The owner approved this as equivalent to a GET (`reprobe-city`). Check the magic bytes (`PK` or OLE2) and refuse HTML. 82 spreadsheets, 14.1 MB. `xlrd` reads the `.xls` |

**The stitch**, in `kyoto_permit_stream(raw_dir, as_of)`:
- **Read** the full list, then every monthly list, oldest first: 69,651 rows.
- **Deduplicate** on (address, trade name, type), each normalised. Where a
  key repeats, the permit ending latest wins: **50,178 rows**.
- **Keep** permits whose term runs on `as_of`: **30,351**.
- **Why it works:** renewals arrive as ordinary monthly rows, issued before
  the old term ends and starting the day after it. 12,528 of the 2021 list's
  permits reappear with a continuous start date. Expiry dates are filled on
  about 100% of rows. Terms run 5–6 years.
- ⚠️ **`as_of` must be pinned by the build, never today.** A step that
  filtered on today's date would drift every day, and the drift check could
  not tell that from a real change. The screen uses 2026-09-24, the download
  date.

**What survives, as of 2026-09-24:**

| Type | Rows in term | Bucket |
|---|---|---|
| 飲食店営業 | 24,121, of which **22,259 fixed** once 1,814 vehicle permits (blank address) and 48 short-term permits (under a year) are dropped | Food service |
| 菓子製造業 | 2,759 | Retail (owner's call) |
| そうざい製造業 | 1,186 | Retail (owner's call) |
| 魚介類販売業 | 512 | Retail |
| 食肉販売業 | 483 | Retail |

**Plausibility, 22,259 restaurants = 15.5 per 1,000** (population 1.44
million, ASSERTED):
- **Kyoto's own complete 2021 list** gave **16.7** (24,306 fixed, counting
  喫茶店).
- **A pessimistic closure floor.** Suppose everything not renewed at term end
  (48.2%) had closed evenly across its term. Then about 5,524 of the 22,259
  are closed but still listed, which gives **11.6**. That is still inside the
  yardstick. It is a floor, because non-renewal also counts renames and moves.

**Other sources:**
- **MHLW's open data adds nothing.** Its Kyoto slice (26 restaurants, 0.12%)
  lies wholly inside the stitch: all 29 MHLW permits that carry a name or an
  address are found in it.
- **The 2021 reform reshaped food retail.**
  - Packaged-only sale became a notification, which these lists do not carry.
  - 乳類販売業 (2,390 in 2021) disappears.
  - 魚介類 and 食肉販売業 shrink from 1,686 to 512 and from 1,632 to 483.
  - So Retail is **food retail by permit type only**.
- **Personal services are the city's complete lists**, not a rebuild: 理容所
  1,009, 美容所 4,017, クリーニング所 802. They churn 2.4%, 3.9% and 6.8% a
  year respectively.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, 11 wards

MLIT files for **26101–26111** (北, 上京, 左京, 中京, 東山, 下京, 南, 右京, 伏見,
山科, 西京): block level 24.0a and town-chōme level 19.0b, 22 zips, 1.4 MB.

| Tier | Food, all types (28,459 fixed) | Restaurants (22,306) | Personal services (5,828) |
|---|---|---|---|
| Block | **92.7%** | **93.1%** | **94.4%** |
| Town-chōme | 6.0% | 5.7% | 4.1% |
| Unplaced | 1.3% | 1.3% | 1.6% |

*The restaurant column is every fixed 飲食店 and 喫茶店 permit, including the 48
short-term ones.*

**Kyoto needed four rules, now in `japan_register.py`:**
- **Without them the shared join placed 61.4%** at block level and left
  35.5% unplaced.
- **A: strip the street intersection** (Kyoto only). Addresses name the
  corner before the town: `河原町通三条上る下丸屋町123` is 下丸屋町 123. The town
  follows the last 上る/下る/入る, and a block count between them
  (`四条下る4丁目小松町`) is a distance, not a town.
- **B: character variants.**
  - 祇/祗, and Kyoto's own private-use codes for 祇, which are read in
    Kyoto's files only.
  - 藪/薮, 壷/壺, 桧/檜, 篭/籠, 竃/竈, 竜/龍, 渕/淵 and 祓/秡.
  - 鍛治→鍛冶, 廻リ→廻り, and ゝ expanded.
- **C: a known-town fallback.**
  - Suffix matches: `八坂新地清本町` → 清本町.
  - Prefix matches: `朱雀分木町市有地…` → 朱雀分木町.
  - Where a prefix match lands on a 大字 that has 小字, the 地番 is looked up
    under that 小字 or not at all. That correction came from Hiroshima (see
    DECISIONS).
- **D: twin towns left unplaced.** 123 town names occur twice in one ward, in
  上京, 中京 and 下京, their twins a median 1.27 km apart. 237 food rows
  (0.8%) where nothing picks the twin are unplaced rather than misplaced.

**Independent check**: Kyoto publishes no coordinates. GSI's address search,
given the stripped form (ward + town + 地番), agrees with the join within 0–1
m on 12 of 12 sampled rule-C rows. Given the full intersection-style address,
GSI matches only a fragment (the ward, or 八坂上町), so the stripped form is
the one to check against.

## 🚇 Rail — MLIT N02, the city line, stub test PASSED

`pipeline/countries/japan.py` has Kyoto (prefecture 26, the 11 wards,
EPSG:32653). The N03 file for prefecture 26 is in the shared cache. The stub
test (N02 stations, Shinkansen excluded, against the ward polygons):

| Group | Stations inside the city line |
|---|---|
| **Subway**: Karasuma, Tōzai | 15 of 15; 16 of 17 (六地蔵 is in Uji) |
| **Randen trams**: Arashiyama main line, Kitano line | 13 of 13; 10 of 10 |
| **Wholly inside the city**: Eizan main and Kurama lines, Keihan Ōtō, Hankyū Arashiyama | 8 of 8, 10 of 10, 3 of 3, 4 of 4 |
| **Keihan Keishin** (legally a tramway) | 3 of 7, the rest in Ōtsu. **Passes (owner)**: half a line, as the Hankai tram in Osaka |
| **Funiculars**: 京福 鋼索線 (Eizan cable), 鞍馬山鋼索鉄道 | 2 of 2 each. **Drawn (owner)** |
| **Sagano scenic line** (嵯峨野観光線) | 3 of 4. **Left out (owner)**, as a tourist line |
| **JR and the private railways**, cut at the line as intended | Keihan main line 15 of 41, Kintetsu Kyōto 9 of 26, Hankyū Kyōto 7 of 27, Keihan Uji 4 of 8, JR Nara 5 of 19, JR San'in 9 of 161, JR Tōkaidō 4 of 59, JR Kosei 1 of 21 |

⚠️ Stations are LineStrings: `japan.stations()` takes their centroids in a
projected CRS.

## Scope

**Kyoto City (11 wards)**, matching the city-wide lists.

## ✅ Licences — READ 2026-09-24

- **The City's lists (00414, 00541, 00530) — PERMITTED WITH CONDITIONS**
  (CC BY 4.0).
  - **The grant**: the portal's 京都市オープンデータ利用規約 (第3版, 2023-06-01)
    clause 1 applies each dataset's own licence. All three dataset pages, and
    all 340 of their resource pages, declare `CC-BY 4.0（表示）` with 著作権者
    京都市. CC BY 4.0 §2(a)(1) grants making and sharing adapted material.
  - **No click-through**, and the government standard terms (政府標準利用規約)
    are not adopted.
  - The City's website copyright page governs its web pages, not portal data.
  - **MUST DISPLAY**:
    - 京都市 as the creator;
    - the name **京都市オープンデータ**, which the portal asks for, binding
      through CC §3(a)(1)(A)(i);
    - the dataset names and URLs;
    - CC BY 4.0 with a link;
    - that the data was processed (CC §3(a)(1)(B)).

    A draft, **in this project's wording, not the City's**:
    `出典：京都市オープンデータ「食品営業許可施設一覧について」「食品営業許可施設一覧について（令和3年6月以降）」「理容所・美容所・クリーニング所の施設一覧について」（京都市、CC BY 4.0 https://creativecommons.org/licenses/by/4.0/legalcode.ja）を加工して作成`
  - **MUST NOT**:
    - imply the City's endorsement (CC §2(a)(6));
    - use the City's emblem or logos (clause 3);
    - describe the map as currently operating businesses. The datasets' own
      notes say the 2021 list may include closed businesses, and the rebuild
      cannot see closures.
  - **MUST DO**: nothing. Remove the credit if the City asks (CC §3(a)(3)).
  - **Governing law**: Japanese law, Kyoto District Court.
  - ⚠️ **Fetch only from `data.city.kyoto.lg.jp`.** Older copies of some lists
    sat on `www.city.kyoto.lg.jp`, whose copyright page bars copying.
- **MLIT 位置参照情報, N02 and N03**: PDL 1.0, as in every Japanese brief.

## Must disclose on the page

- **A rebuilt register**: Kyoto's 2021-03-31 full permit list plus every
  monthly list of permits granted since, keeping permits still in their term
  on the build's `as_of` date.
- **Closures are not published.** A premises that closed before its permit
  expired stays until the permit expires, so the count is an **upper bound**.
- **Left out**: vehicles (1,814 restaurants with no address), permits with a
  term under a year (48), and the 0.8% of premises in twin-named towns.
- **Food retail is by permit type only** (菓子, そうざい, 魚介類, 食肉). Packaged-only
  sale has been a notification since 2021 and is not in these lists.

## Privacy

- The operator columns are never selected (see the table above). The stitch
  reads its columns by name.
- **The publisher did the privacy work for only one dataset.** 00541 leaves
  blank any item the applicant did not consent to publish. 00414 and 00530
  say nothing about consent, and the 2021 `.xls` carries applicant-name and
  representative columns.
- Run `check_personal_exposure.py`, because a trade name can be a person's own
  name.

## Region

`"region": "East Asia"`. Project to **UTM 53N (EPSG:32653)**.

## Still unknown

- ⚠️ **Same-address successors.** An older permit at an identical address
  with a newer permit of the same type under another name is probably a
  predecessor, which would lower the upper bound. Measure it at build, and
  do not drop anything without that measurement.
- ⚠️ **Short-term permits (under a year).** The rebuild's count dropped all
  48. The step-2 filter reads `許可開始日` and `許可終了日` from the stitch.
- ⚠️ **The factory and central-kitchen share of 菓子 and そうざい**, from
  trade names, before publishing (the owner's Japan-wide condition).
- ⚠️ **Small residuals.** About 5 rows use a private-use character not
  mapped (U+E0EE in a 上京区 town name). Some 東山区 addresses name
  `三条通大橋東N丁目`, which MLIT spells differently.
- ⚠️ **Population 1.44 million is ASSERTED.** Read the 推計人口 for the
  build month before quoting a per-1,000 figure.

```brief-checks
[
  {
    "id": "kyoto-00414-cc-by",
    "claim": "Dataset 00414 (the 2021 full list and early monthly lists) declares CC BY 4.0 with 京都市 as copyright holder",
    "kind": "http_contains",
    "url": "https://data.city.kyoto.lg.jp/dataset/00414/",
    "present": ["CC-BY 4.0", "京都市"]
  },
  {
    "id": "kyoto-00541-cc-by",
    "claim": "Dataset 00541 (monthly permits since 2021-06) declares CC BY 4.0",
    "kind": "http_contains",
    "url": "https://data.city.kyoto.lg.jp/dataset/00541/",
    "present": ["CC-BY 4.0", "京都市"]
  },
  {
    "id": "kyoto-00530-cc-by",
    "claim": "Dataset 00530 (barber, beauty and laundry lists) declares CC BY 4.0",
    "kind": "http_contains",
    "url": "https://data.city.kyoto.lg.jp/dataset/00530/",
    "present": ["CC-BY 4.0", "京都市"]
  },
  {
    "id": "kyoto-terms-credit-request",
    "claim": "The portal's terms ask users to state that 京都市オープンデータ was used - the prescribed name in the notice",
    "kind": "http_contains",
    "url": "https://data.city.kyoto.lg.jp/contents.php?category=0",
    "present": ["京都市オープンデータ", "利用した旨"]
  },
  {
    "id": "kyoto-no-ckan-api",
    "claim": "The portal has no CKAN API - downloads go through the resource pages' download button",
    "kind": "endpoint_absent",
    "url": "https://data.city.kyoto.lg.jp/api/3/action/status_show"
  },
  {
    "id": "kyoto-isj-nakagyo-live",
    "claim": "MLIT's block-level address file for Nakagyō (26104) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/26104-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "kyoto-n03-live",
    "claim": "MLIT's N03 boundaries for Kyoto prefecture (26) answer keyless - the city line",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2025/N03-20250101_26_GML.zip",
    "min_bytes": 1000000
  },
  {
    "id": "kyoto-projected-crs",
    "claim": "Kyoto projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.76,
    "expect": "EPSG:32653"
  }
]
```
