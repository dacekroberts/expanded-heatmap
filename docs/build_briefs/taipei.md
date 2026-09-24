# Taipei (Regional) — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py taipei`
before writing any code. **Taiwan has never been built**: read "Taiwan
finished" in `docs/global_country_shortlist.md` and the Taiwan section of
`docs/data_sources.md` first. This brief carries the national argument;
`taichung.md` and `taoyuan.md` carry only what is theirs. The method behind
all three is in `docs/geocoding_retrospective.md`.

---

## The one-line summary

**152,839 storefronts across Taipei and New Taipei, placed by a keyless JOIN
at 93.9% — no geocoder, no API key — with rail geometry from the city's own
network map, and two display rules the publisher's own conduct decided.**

---

## Scope — REGIONAL: Taipei City + New Taipei City

**Two special municipalities, one metropolis.** New Taipei (formerly Taipei
County, ~4M) **completely surrounds** Taipei (~2.5M), and the metro crosses the
boundary on several lines (Tamsui, Xindian, Zhonghe, Tucheng/Banqiao,
Xinzhuang/Luzhou; the Circular Line is New Taipei's own). A Taipei-only page
would cut the network where no rider notices — **the Dublin and Lille shape**.
Owner's framing, 2026-09-23.

---

## Business leg — the national BUSINESS TAX REGISTER, MEASURED

| | |
|---|---|
| **Source** | `全國營業(稅籍)登記資料集`, Fiscal Information Agency (FIA) — `eip.fia.gov.tw/data/BGMOPEN1.zip`, **66,338,224 bytes**, **refreshed daily** (the CSV's first data row carries its own date) |
| Rows | **1,713,627** operating locations nationally — **one row per trading LOCATION**; `總機構統一編號` (parent ID) makes company branches their own rows |
| Fields used | `營業地址` (business address), `營業人名稱` (name), `組織別名稱` (organisation type), `行業代號` + `名稱` (6-digit industry code and its name) |
| **Buckets** | read from the register's own code names — ISIC's divisions: **47/48 Retail · 56 Food service · 96 Personal services**; **487 `經營網路購物` (online shopping) EXCLUDED**, NAICS 454's twin |
| **Taipei** | **76,519** — Retail 44,634 · Food 23,684 · Personal 8,201 (4,954 online-shopping rows excluded) |
| **New Taipei** | **76,320** — Retail 43,945 · Food 23,457 · Personal 8,918 |

**Not 商業登記** (the per-category business registration the screen first
found): it omits companies entirely. **Not New Taipei's own 商業登記清冊**: it
carries `res_name`, the responsible person's name.

### 🚨 The head-office trap — measured, confined to companies

| Organisation type | Taipei storefront rows | On 3F+ or with a room (`室`) |
|---|---|---|
| Sole proprietor (獨資) — the control | 45,851 | **7.1%** |
| **Company, head office or single site** | **19,491** | **38.7%** |
| Branch (分公司) | 4,794 | 8.2% |

**About 7,500 company rows look like offices, not shops.** Build decision, not
taken here: exclude company head-office rows that are office-like — **but
department-store counters sit on upper floors too**, so test the rule on a
known department store before trusting it. Clustering found **markets**, not
registered-office services (環南市場 893 rows, 士林市場 513) — genuine premises.

---

## ✅ Coordinates — a JOIN against door-plate files, no geocoder

| | Taipei | New Taipei |
|---|---|---|
| **File** | `臺北市門牌位置數值資料` (民政局, data.taipei) — **124,547,303 bytes**, edition `_20260902` | `新北市門牌位置數值資料` (data.ntpc.gov.tw) — **192,881,415 bytes**, monthly |
| Keys | 251,607 | 422,048 |
| Coordinates | TWD97 (EPSG:3826) | `x_3826` / `y_3826`; **columns in English** (`street、road、section`, `lane`, `number`) |
| **Joined** | **92.4%** — food 94.9 · retail 89.9 · personal 98.8 | **95.5%** — retail 94.8 · food 95.6 · personal 98.4 |
| **Together** | **93.9% of 152,839** | |

**`scripts/screen_taiwan_join.py` is the method. Taipei is its CONTROL — run
it first after any parser change; nothing else counts until 92.4% reproduces.**
The normalisation that mattered, each priced: NFKC; Chinese section numerals;
**one sub-number separator from `之 － - ― — –` (`―` alone was 3.4 points)**;
floors dropped; streets may contain `市`/`鎮`/`里` (0.8 points, caught only by
the control).

**The misses are market stalls and stalls under viaducts** (`高架橋下`) — real
premises with no door plate — and rural addresses with no street. A build
could place a stall at its market's address; **decide it deliberately**.

⚠️ **Certificates**: Python's bundle lacks Taiwan's government root (GRCA);
use the OS store (`truststore`, as `brief_check.py` now does). **Never switch
verification off.**

---

## 🔒 Names — DECIDED 2026-09-23

**Show a business name only when it is a TRADE name**: companies and branches
(legal entities), and sole proprietors only when the name carries a business
marker (行/店/社/館/坊…). Otherwise the tooltip shows the category.

Why: for **3,763 Taipei storefronts (4.9%)** the registered name reads as the
owner's — all sole proprietors, **63% market stalls** — and **the FIA itself
refuses to publish owners' names** (2016; again 2026-08-14, on Ministry of
Justice letter 法律字第10503516500號). Taiwan's PDPA reaches a foreign reuser
(第51條). `check_personal_exposure.py` needs a Taiwan entry that tests this
rule, not a name list.

---

## Licence — OGDL v1 on every Taiwanese source

**PERMITTED WITH CONDITIONS** (read 2026-09-23; full record in
`docs/data_sources.md`):

- **The attribution statement is LOAD-BEARING** — OGDL v1 §三(二): without it
  the grant is *"視為自始未取得"*, never granted. It covers derived coordinates.
  One statement **per source** (tax register, each door-plate file, each rail
  dataset), in the prescribed form:
  `提供機關／臺北市政府民政局 [2026] [臺北市門牌位置數值資料 20260902]` +
  *"此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。"* + `https://data.gov.tw/license`.
- **Fault-based liability (§六(三)) — ACCEPTED by the owner** for all of Taiwan.
- FIA's own declaration: cite the source, no emblems, no implied endorsement,
  and **do not present the filtered points as the register itself**.

---

## 🚇 Rail — the agencies' own data, keyless. NOT TDX

| Dataset | What it is |
|---|---|
| `臺北都會區大眾捷運系統路網圖` (臺北市政府捷運工程局, data.gov.tw 121208) | **Line geometry** — GeoJSON `MultiLineString` with `RouteName`, EPSG:3826, updated 2025-12-12 |
| `臺北都會區大眾捷運系統車站點位圖` (121140) | **Station points**, EPSG:3826 |
| Taipei Metro's `路線車站資料服務` (131326) | Station order per line (`BR01 動物園站` …), updated 2026-09-04 |
| National `捷運車站` (內政部國土測繪中心, 73233) | A national station layer (shapefile, 2026-04) — the cross-check |

**TDX is not used**: every operator returns `401 Valid API Key Required` to
scripts; its terms allow keyless use only as a browser visitor mode (20
calls/day), and registration wants a Taiwanese mobile number. **A check below
fails the day that changes.** Colours: TDX carried `LineColor`; the agency
map's colour source is unmeasured — resolve before building, never invent.

## Region

**None exists** — the first Taiwanese city adds one (`"Taiwan"`, or an East
Asia region shared with Seoul and Hong Kong). Owner call, measured with
`check_macro_labels.py`.

## Still unknown

- ⚠️ **New Taipei's own lines** (Circular Line, Danhai and Ankeng light rail):
  whether Taipei's network map carries them.
- ⚠️ **Line colours** — the agency map's `RouteName` has no colour field seen.
- ✅ **The head-office rule — TESTED 2026-09-24 on ten department stores and
  malls** (Shin Kong Mitsukoshi A4/A8/A9/A11, Breeze, SOGO, Uni-Ustyle, Q
  Square, ATT 4 FUN, Bellavita): the register holds only **1–4 rows per
  store — the operator, not its counters** — so the rule drops **0 of 20**.
  Counter brands are not registered at the store at all, which means **a
  department store draws as ONE point**: disclose it, as Brazil discloses
  shopping centres. Refinement measured: of 7,534 rows the rule flags, 884 sit
  at addresses with 20+ storefront rows (markets, malls); exempting those, the
  rule drops **6,650**. ⚠️ The first run matched nothing because the register
  inserts `里`/`鄰` between district and street — match on district + street
  + number.
- ⚠️ **Market stalls — COUNTED 2026-09-24: 5,239 storefront rows (6.8%)** —
  2,796 with a stall number (`攤`/`攤位`), 1,522 in a market without one, 921
  under a viaduct (`高架橋下`). Biggest: 環南市場 900, 南門市場 246, 成功中繼市場
  147. Placing them at the market's own door plate is the build's call.

```brief-checks
[
  {
    "id": "tw-tax-register-live",
    "claim": "The national business tax register is keyless and live - one row per trading location, refreshed daily. It is the business leg for every Taiwanese city",
    "kind": "http_ok",
    "url": "https://eip.fia.gov.tw/data/BGMOPEN1.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "taipei-doorplates-live",
    "claim": "Taipei's door-plate coordinate file is keyless and live - the join target, 92.4% (the control)",
    "kind": "http_ok",
    "url": "https://data.taipei/api/dataset/b7c8e724-1e98-45ee-a0bd-f3840623ed97/resource/ce76ca0c-7f94-4935-ab47-1d2a41ca2abb/download",
    "min_bytes": 1000000
  },
  {
    "id": "new-taipei-doorplates-live",
    "claim": "New Taipei's door-plate file is keyless and live - 95.5%, the best of the five cities",
    "kind": "http_ok",
    "url": "https://data.ntpc.gov.tw/api/datasets/d7b568ab-3819-40c8-a6e7-a6b199443101/csv/file",
    "min_bytes": 1000000
  },
  {
    "id": "taipei-agency-line-geometry",
    "claim": "Taipei's own metro network map carries line geometry with route names - the rail source instead of TDX",
    "kind": "http_contains",
    "url": "https://data.taipei/api/dataset/afccd2ac-75b1-4362-9099-45983e332776/resource/1139b06e-8128-4a07-8148-f27f038bd8b4/download",
    "present": ["MultiLineString", "RouteName", "EPSG:3826"]
  },
  {
    "id": "tdx-still-key-gated",
    "claim": "TDX refuses scripted access without a member key, which is why rail comes from the agencies. When this FAILS, TDX's access changed: re-read its terms before using it",
    "kind": "http_contains",
    "url": "https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/Station/TRTC?%24format=JSON",
    "expect_status": 401,
    "present": ["Valid API Key Required"]
  },
  {
    "id": "taipei-projected-crs",
    "claim": "Taipei projects to UTM 51N; the door plates' EPSG:3826 (TWD97 TM2) is also metric",
    "kind": "utm_zone_from_longitude",
    "lon": 121.52,
    "expect": "EPSG:32651"
  }
]
```
