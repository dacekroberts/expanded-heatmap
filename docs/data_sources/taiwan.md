# Data sources — Taiwan

<!-- internal -->The Taiwan part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country on 2026-09-27.
The numbered notices this project must display, the removal-request
commitment and the deploy gate apply to every country and are kept in
that record.<!-- /internal -->

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Taichung | **Taiwan's national business tax register** (全國營業(稅籍)登記資料集, Fiscal Information Agency, daily; one row per trading location) - the rows whose address is in Taichung and whose industry code is in 47/48, 56 or 96 (487 online shopping out), JOINED to Taichung's door-plate file (臺中市115年1月至各月份GIS門牌資料, 臺中市政府數位發展局, monthly; the newest month's CSV, a Google Drive link from the portal's index) by district code, street, lane, alley and number | Retail, Food service and Personal services: **66,115** storefronts; 1,521 office-like company head-office rows dropped (owner's rule); 92.2% placed, 5,599 unplaced (market stalls, intersections, rural addresses); names shown by industry on 11,907 sole proprietors (owner's name rule) | `https://eip.fia.gov.tw/data/BGMOPEN1.zip` (shared cache `data/taiwan/raw/`); `https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=03d9c01c-4a7c-4bd8-ae88-12ed011391b3` (the index) | none server-side; address prefix 臺中市 and the code divisions in step 2 | 2026-09-25 |
| Taoyuan | **Taiwan's national business tax register** (the shared cache) - the rows whose address is in Taoyuan and whose industry code is in 47/48, 56 or 96 (487 out), JOINED to Taoyuan's door-plate file (桃園市門牌位置坐標資料, 桃園市政府民政局, data.gov.tw 157689, monthly; the August 2026 edition `TGOS_A68000_11508`, TWD97 TM2 reprojected) by district code, street, lane, alley and number - the shared step 2 (`pipeline/countries/taiwan_step2.py`) | **45,014** storefronts; 1,177 office-like head-office rows dropped; 93.6% placed, 3,097 unplaced; names shown by industry on 7,230 sole proprietors | `https://opendata.tycg.gov.tw/api/dataset/ec47dbd5-9ed8-4c8d-8ce1-ccb63b1b72e6/resource/d00ecba4-dec2-4a62-bfc7-989a8359cebe/download` | none server-side; address prefix 桃園市 | 2026-09-25 |
| Taipei (Regional) | **Taiwan's national business tax register** (the shared cache) - the rows whose address is in Taipei or New Taipei, each city JOINED to its own door-plate file by the shared step 2: Taipei's 臺北市門牌位置數值資料 (臺北市政府民政局, edition 20260902) and New Taipei's 新北市門牌位置數值資料 (新北市政府民政局, data.gov.tw 168887, edition 11509), both TWD97 TM2 | **133,335** storefronts (Taipei 64,526, 91.8% placed; New Taipei 68,809, 95.0%); 10,138 office-like head-office rows dropped; about 3,600 market and viaduct stalls unplaced (owner: left off); names shown by industry on 17,890 sole proprietors | `https://data.taipei/api/dataset/b7c8e724-1e98-45ee-a0bd-f3840623ed97/resource/ce76ca0c-7f94-4935-ab47-1d2a41ca2abb/download`; `https://data.ntpc.gov.tw/api/datasets/d7b568ab-3819-40c8-a6e7-a6b199443101/csv/file` | none server-side; address prefixes 臺北市 and 新北市 | 2026-09-25 |

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Taichung | **Taichung Metro's Green Line**: stations from the operator's own table (臺中捷運綠線車站資訊, 臺中捷運股份有限公司, data.gov.tw 144164; code, Chinese and English names, coordinates) and the route from OpenStreetMap (relations 11330355/11330356, 臺中捷運綠線) | `https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=f9511cc5-4799-4df9-98b7-0b0f89fc2be9`; OSM via the Overpass mirrors in `pipeline/taichung/config.py` | 2026-09-25 | Gate 3 exact: OSM's 18 stops against the operator's 18, every station within 23 m of the route. The operator's table repeats code G17 (烏日, 高鐵臺中站); keyed by name. No color in either source: this project's green (owner). Station table OGDL v1 - notice 45; OSM, ODbL 1.0 - notice 1 |
| Taoyuan | **The Taoyuan Airport MRT**: station points from the national 捷運車站 layer (內政部國土測繪中心, data.gov.tw 73233; the rows 桃園機場捷運…站_A<n>, whose ADDRESS says which city each is in), the route from OSM's all-stop relation (6937083, `#2C5AA5`), and gate 3 against Taoyuan Metro's own list (桃園捷運路線車站基本資料, data.gov.tw 128390) | `https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/63A7BA62-C429-4F2D-8B73-21AAB9E6EAE0/resource/4C11DFAE-ED20-4843-89E7-08D23CADAA16/download`; `https://opendata.tycg.gov.tw/api/dataset/8c1fe832-fe4a-4033-a283-25ab39a99d93/resource/5535111f-9af5-40b9-9e58-a4d382fb8b2c/download`; the network record (128388, the line and its operator 桃園大眾捷運股份有限公司) `https://opendata.tycg.gov.tw/api/dataset/434a3d9f-ebc1-474b-b8b7-da53eb340b48/resource/35cd3ed3-42a4-401d-90bd-7f5b82588169/download`; OSM via the Overpass mirrors in `pipeline/taoyuan/config.py` | 2026-09-25 | Gate 3 exact, 22 against 22, after one recorded addition: the operator's XML is dated 2018-10-01 and lacks A22 老街溪 (opened 2023), which the national layer and OSM both carry. Every station point within 57 m of the route. 15 stations in Taoyuan kept; A1-A6 and A9 outside. The operator's "StationList.xml" resource (128394) is byte-identical to the route file and has no coordinates. All OGDL v1 - notice 46, Taoyuan City Government, NLSC and Taoyuan Metro; OSM, ODbL 1.0 - notice 1 |
| Taipei (Regional) | **OpenStreetMap** - every metro and light-rail line in the two cities (owner): Taipei Metro's BR, R, G, O and BL with the Xinbeitou and Xiaobitan branches, New Taipei's Circular (Y) and Sanying (LB) lines and the Danhai (V) and Ankeng (K) light rail, and the Airport MRT; relations matched on `ref`, stations by route membership, English names from `name:en` | the Overpass mirrors in `pipeline/taipei/config.py` (subway, light_rail and monorail relations in the metro's box); Taipei Metro's list `https://data.taipei/api/dataset/8bf00fa8-86a5-437e-b5c7-9bc0fe0e2971/resource/e3c0e67f-5916-405f-ad9a-41f52a65c2d2/download` (臺北捷運路線車站資料服務, data.gov.tw 131326) | 2026-09-25 | **Why not the agency:** Taipei's network map carries no colors and may lack New Taipei's lines (owner, 2026-09-25). **Gate 3 exact on all seven Taipei Metro lines and branches** (24/28/2/19/2/26/23). R01 kept: in the operator's list and tagged an active stop, only OSM's English label said "under construction" (owner). `colour=orange` resolved through the CSS table to #FFA500. 153 stations in the two cities (74 Taipei, 79 New Taipei), 15 Airport MRT stations in Taoyuan outside. Scope by door plates within 300 m - no boundary read. Station list OGDL v1 - notice 47, Taipei and New Taipei City Governments and Taipei Metro; OSM, ODbL 1.0 - notice 1 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Taichung | **None** - the register is scoped by its address prefix (臺中市), and every station's address in the operator's table begins with it. Overpass 504ed on OSM's boundary from all three mirrors (2026-09-25) and nothing needed it | - | The whole Green Line is in the city |
| Taoyuan | **None** - the register is scoped by its address prefix (桃園市), and each station's city is the national layer's own ADDRESS | - | 15 of the line's 22 stations are in Taoyuan |
| Taipei (Regional) | **None** - the register is scoped by address prefix, and a station is in the region when either city's own door-plate file has plates within 300 m | - | Overpass 504ed on every boundary query on 2026-09-25 |

## Licenses and terms of use

### 🇹🇼 Taiwan<!-- internal --> — read 2026-09-23 and 2026-09-25 by the `licence-read` agent<!-- /internal -->

| Source | Verdict | What it requires |
|---|---|---|
| **Taipei door plates** — `臺北市門牌位置數值資料` (民政局, data.taipei, dataset 155472), used as the GEOCODING REFERENCE | **PERMITTED WITH CONDITIONS — 政府資料開放授權條款-第1版 (OGDL v1)**, declared on the publisher's own portal and on data.gov.tw. Grant §二(一): *"不限目的、時間及地域、非專屬、不可撤回、免授權金進行利用 ... 編輯、改作 ... 衍生物"* | **The annex's attribution statement (顯名聲明), and it is LOAD-BEARING**: §三(二) — failing it means *"視為自始未取得開放資料之授權"*, never licensed at all — and it covers **derivatives**, so the published coordinates carry it though the door-plate table is never published. Form: `提供機關／臺北市政府民政局 [2026] [臺北市門牌位置數值資料 20260902]` + *"此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。"* + `https://data.gov.tw/license`. No patents or trademarks licensed |
| **The national business tax register** — `全國營業(稅籍)登記資料集` (財政部財政資訊中心 / FIA, `eip.fia.gov.tw/data/BGMOPEN1.zip`, data.gov.tw 9400) — the BUSINESS leg for every Taiwanese city | **PERMITTED WITH CONDITIONS — OGDL v1** (`license: "1"`), plus the FIA's own *政府網站資料開放宣告*, which repeats the grant and adds: cite the source (*"應註明出處"*); no marks or emblems; no implied endorsement; and **§二(二): personal data that is public must still be handled under the Personal Data Protection Act by the user** | The same prescribed 顯名聲明, e.g. `財政部財政資訊中心 2026 全國營業(稅籍)登記資料集（資料日期 YYYY-MM-DD）` — the CSV's first data row carries its own date. ⚠️ **Do not present the filtered, geolocated points as the register itself** (FIA 四) |
| **TDX** (交通部運輸資料流通服務平臺) metro endpoints | ⛔ **NOT USED.** Its own terms (not OGDL): scripted access needs a **registered member key**; keyless is a browser-only visitor mode, 20 calls/day per IP; registration wants a Taiwanese mobile number or manual review. The server now enforces it (curl 401, browser 200) and **it is not worked around** | — |
| **Taichung door plates** — `臺中市115年1月至各月份GIS門牌資料` (臺中市政府數位發展局, opendata.taichung.gov.tw, monthly CSVs on Google Drive) | **PERMITTED WITH CONDITIONS — OGDL v1**, read 2026-09-25 off the dataset's own page (授權方式) | The 顯名聲明 - notice 45 |
| **Taichung Metro's Green Line stations** — `臺中捷運綠線車站資訊` (臺中捷運股份有限公司, data.gov.tw 144164) | **PERMITTED WITH CONDITIONS — OGDL v1** (`license: "1"`), read 2026-09-25 | The 顯名聲明 - notice 45. No line color published on the pages read |
| **Taoyuan door plates** — `桃園市門牌位置坐標資料` (桃園市政府民政局, data.gov.tw 157689) | **PERMITTED WITH CONDITIONS — OGDL v1**, read 2026-09-25; plus the portal FAQ's condition (accepted, notice 46) | The 顯名聲明 - notice 46 |
| **The national 捷運車站 layer** (內政部國土測繪中心, data.gov.tw 73233) | **OGDL v1** (`license: "1"`), 2026-09-25 | The 顯名聲明 - notice 46 |
| **Taoyuan Metro's station list** — `桃園捷運路線車站基本資料` (桃園捷運公司, data.gov.tw 128390) | **PERMITTED WITH CONDITIONS — OGDL v1**, read 2026-09-25 | The 顯名聲明 - notice 46. No line color on the pages read |
| **New Taipei door plates** — `新北市門牌位置數值資料` (新北市政府民政局, data.gov.tw 168887) | **PERMITTED WITH CONDITIONS — OGDL v1**, read 2026-09-25; the portal FAQ adds nothing | The 顯名聲明 - notice 47 |
| **Taipei Metro's station list** — `臺北捷運路線車站資料服務` (臺北大眾捷運股份有限公司, data.gov.tw 131326) | **PERMITTED WITH CONDITIONS — OGDL v1**, plus the company's own open-data declaration (accepted, notice 47), read 2026-09-25 | The 顯名聲明 - notice 47. No line color on the pages read |

**A fault-based liability clause — RAISED, owner call.** OGDL v1 §六(三):
*"使用者...因故意或過失，致資料提供機關遭受損害，或第三人因此向資料提供機關請求賠償損害，使用者應對各機關負賠償責任。"*
The same class as Rio's SIURB clause and IBGE's portal terms — liability for
damage the user causes deliberately or negligently, narrower than Hong Kong's
indemnity. **It rides on every OGDL v1 source in Taiwan**, so one decision
covers them. ✅ **ACCEPTED by the owner 2026-09-23, for all of Taiwan.**

**The personal-name question — the one ambiguity that mattered, DECIDED.**
For small sole proprietors (獨資) the registered business name IS the owner's
name (`黃信雄`, `陳雅娟`); in Taipei, **3,763 storefronts (4.9%)** read that way,
63% of them market stalls. **The FIA itself refuses to publish owners' names**
— it removed them in 2016 and refused again on 2026-08-14: *"如將負責人姓名無任何
限制下全數公開，恐有過度揭露個人資料、侵害資訊隱私、違反比例原則之疑慮"* —
relying on Ministry of Justice letter 法律字第10503516500號. The Personal Data
Protection Act reaches a foreign reuser of Taiwanese residents' data (第51條
第2項). **Decided 2026-09-23: a name is shown only when it is a TRADE name** —
for companies and branches (legal entities), and for sole proprietors only
when the name carries a business marker (行/店/社/館/坊…); otherwise the tooltip
shows the category. It errs toward hiding, which the publisher's own refusal
argues for. Removal requests under PDPA 第3條/第19條 are honored, which the
project's standing commitment already says.

**Taiwan's rail comes from the agencies instead**, keyless and under OGDL v1
(one read covers the license; each source still needs its attribution line):
Taipei's `臺北都會區大眾捷運系統路網圖` and `車站點位圖`, Taichung Metro's
Green Line stations, the national land-survey center's `捷運車站` layer.
