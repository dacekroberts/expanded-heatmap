# Tokyo — build brief

**Step 0 measured 2026-09-24 (the overnight Japan run).** Run
`python scripts/brief_check.py tokyo` before writing any code. The coordinate
method is the `address-join` skill; the measurement is
`scripts/screen_japan_join.py`. **This brief is deliberately PARTIAL on
coverage** — see *Scope*, which is the owner's call before a build.

**✅ Decided by the owner, 2026-09-24, for every Japanese city:** (1) **the Shinkansen does not count**, since it is long-distance travel between cities; (2) **the city line only**: only stations inside the city get rings, matching the city-only permit list, with a per-line stub test at build (any urban line cut to a stub goes back to the owner); (3) **菓子製造業 and そうざい製造業 count**, in the Retail bucket (bakeries, confectioners and delis sell over a counter), with the factory and central-kitchen share measured from trade names before publishing. Open items below that ask these questions are answered. **Tokyo's own scope** was decided the same day: the 8 wards now, with the missing wards named on the page and the owner requesting Chiyoda's ledger (`docs/gated_access.md` item 22).

---

## The one-line summary

**Premises-level permits joined to MLIT's block-level address file at 99%+ —
no geocoder — but only 4 of the 23 special wards publish food permits as files,
and three central wards (Chiyoda, Shibuya, Toshima) do not publish them as open
data at all.** Personal services cover 11 wards.

---

## Business leg — ward permit files (national recommended schema, 推奨データセット)

Catalogued on Tokyo's CKAN (`catalog.data.metro.tokyo.lg.jp`), each ward an
organization `t` + its six-digit municipal code (Minato `t131032`).

| Ward | Food file | Fixed premises | Encoding / quirk | Vintage |
|---|---|---|---|---|
| **Minato** | `food_business_all.csv` (opendata.city.minato.tokyo.jp), 2,332,997 B | **5,618** (+103 mobile) | UTF-8; split address columns 98% | **2026-07-31** |
| **Shinjuku** | `000399975.csv` (www.city.shinjuku.lg.jp), 4,445,074 B | **14,418** (+309 mobile) | **UTF-16 LE**; whole address in 町字 (`新宿3-14-1`) | ⚠️ **2023-01-01 snapshot**: use it with the vintage disclosed (owner, 2026-09-24); check the ward's page for a newer file at build |
| **Chūō** | `syokuhineigyoukyoka.csv` (www.city.chuo.lg.jp), 513,187 B | **2,548** | cp932; split columns EMPTY — parse `所在地_連結表記` | catalogue 2025-12 |
| **Kōtō** | `131083_015_food_business_all.csv` (metropolitan portal), 867,166 B | **1,713** (+43 mobile) | UTF-8 | catalogue 2025-12 |

**Personal services** — the 生活衛生 registers (美容所 / 理容所 / クリーニング所),
same address columns, on the metropolitan portal (`www.opendata.metro.tokyo.lg.jp`)
or Minato's own: **11 wards, 16,299 premises** — Chiyoda, Minato, Bunkyō,
Taitō, Shinagawa, Ōta, Shibuya, Toshima, Arakawa, Katsushika, and Meguro
(on BODIK, measured 2026-09-24: 1,412). Beauty 11,341 · barber 2,042 ·
laundry 2,916.

### Taxonomy — `営業の種類`, first cut

| Bucket | Types |
|---|---|
| Food service | 飲食店営業 (Shinjuku 12,603 · Minato 4,781 · Chūō 1,319 · Kōtō 525), 喫茶店営業 |
| **Food retail — only where a ward publishes 届出**: a disclosed PARTIAL retail bucket, never extrapolated to wards that don't publish it (owner, 2026-09-24) | Chūō / Kōtō: その他の食料・飲料販売業 (467 / 437), コンビニエンスストア (127 / 138), 百貨店、総合スーパー (38 / 65), 野菜果物販売業, 魚介類販売業, 食肉販売業 |
| Personal services | the 生活衛生 registers |
| **Out** | 飲食店営業（自動車）and 都内一円 (food trucks), （臨時）, （屋形船）, 集団給食施設 (institutional catering), 行商, manufacturing (菓子製造業, そうざい製造業… — `premises-taxonomy` decides which sell over a counter), vending machines |

**No general retail anywhere** — Boston's and Toronto's shape, disclosed.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, 99%

| | |
|---|---|
| **Files** | per ward: `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip` (block level, ~33–150 KB) and `.../19.0b/<code>-19.0b.zip` (town-chōme, ~6 KB). cp932 CSV |
| **Join key** | (大字・丁目名, 街区符号) ← (町字, the first number of 番地以下); representative point (`代表フラグ`) where flagged |
| **Normalisation, each rule from a ward's misses** | NFKC; the 丁目 number in digits on BOTH sides (`八重洲二丁目` = `八重洲2丁目`); the hyphen form `5-2-1` = 五丁目 2番 when that town-chōme exists; the whole address in the town field (Shinjuku: 0% → 99.2%); UTF-8 / cp932 / UTF-16 |

| Ward | Block | Town-chōme | None |
|---|---|---|---|
| **Minato (control — re-run after every change)** | **99.8%** | 0.2% | 0.0% |
| Shinjuku | 99.2% | 0.7% | 0.1% |
| Chūō | 99.1% | 0.2% | 0.7% |
| Kōtō | 99.6% | 0.1% | 0.3% |
| **Food, 24,297** | **99.3%** | 0.5% | 0.1% |
| Personal services, 16,299 | 98.8–100% | | |

**Independently confirmed**: where wards publish their own coordinates, the
block point sits a **median 22–43 m** away, **95–100% within 250 m**. (GSI's
AddressSearch returns the same block point, so it is not an independent check.)
The Address Base Registry has **moved** (`dataset.address-br.digital.go.jp`,
with an official geocoder) — not needed at these rates.

### 🚩 The food control — 6.02× OSM

Shinjuku: **12,446** distinct 飲食店営業 premises vs OSM **2,068**
(restaurant + fast_food + cafe + food_court + ice_cream) = **6.02×**; 4.77×
with bars and pubs. OSM is plausibly thin in multi-storey bar districts —
ASSERTED. **Use the Economic Census's per-ward 飲食店 count as the
like-for-like control at build**, not OSM. **Decided by the owner, 2026-09-24**,
for every Japanese city.

---

## 🚇 Rail — MLIT N02, commuter rail INCLUDED (owner, 2026-09-24)

`https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip` (12.4 MB,
GeoJSON inside, UTF-8 and Shift-JIS): 10,235 stations, 21,932 segments, every
JR company, Tokyo Metro, Toei and the private railways. **JR and private
railways are drawn** — the third exception after Dublin's DART and
Copenhagen's S-tog (`docs/commuter_rail_list.md`). ⚠️ **Station geometry is a
LineString (the platform), not a point — centroid it before any ring.**
⚠️ Open: whether intercity-only services (Shinkansen, limited-express-only
lines) count.

**✅ Stub test, measured 2026-09-24** (`pipeline/countries/japan.py` `stub_test()`: N02 stations, Shinkansen excluded, against the city's N03 ward polygons): **FAILS, because Chiyoda is missing from the 8 wards.** The lines are cut through the centre: Marunouchi 8 of 25, Chiyoda 6 of 20, Tōzai 9 of 23, Mita 6 of 27, Yūrakuchō 7 of 24, the Arakawa tram 2 of 30, the Monorail 1 of 11. Only Ginza (17 of 19), Hibiya (17 of 22) and Ōedo (27 of 38) keep most of their stations. **Owner, 2026-09-24: Tokyo WAITS for Chiyoda's ledger** (`docs/gated_access.md` item 22). Osaka, Kobe, Sapporo and Fukuoka build first.

**Does Tokyo truly need Chiyoda? Measured the same day** (the owner's
question), on the 19 urban lines (Tokyo Metro, Toei, the AGTs and the
monorail), with `stub_test("tokyo", wards=…)`:

| Scope | Urban station-line records inside | Lines under half |
|---|---|---|
| The 8 wards | 163 of 365 (**45%**) | 11 of 19 |
| **+ Chiyoda** | 203 (**56%**) | 6 |
| + Chiyoda, Toshima, Bunkyō | 244 (**67%**) | 4 |
| All 23 wards | 356 (**98%**) | 0 |

**Chiyoda is the most valuable single ward** (+40 records; it lifts
Marunouchi, the Chiyoda line, Hanzōmon and the Shinjuku line back above
half). **But it is not the fix**: with it, six lines stay under half (Mita 9 of
27, the Arakawa tram 2 of 30, Nippori-Toneri 0 of 13, the Monorail 1 of 11).
**A whole Tokyo needs most of the 12 missing wards**, and several are
reachable: Ōta, Kita and Arakawa publish full lists as PDFs; Shinagawa and
Itabashi partially; Nakano's list is stale; Toshima, Nerima and Edogawa are
on request. **Owner, 2026-09-24: Tokyo is the LAST Japanese city**, the
densest, and the one that benefits most from a Japan skill written off the
first four builds. The missing wards become a planned project for it, not a
blocker for the others.

## Scope — 🚩 the owner's call

Food files exist for **Minato, Shinjuku, Chūō, Kōtō** — central, but not all
of the centre. **Chiyoda releases its food ledger only on a disclosure request;
Toshima only for viewing in person; Shibuya: none found by two methods.**
Taitō publishes its own-format list with operators' home addresses (outside
this run's bounds). A "Tokyo" map of four wards would be missing Marunouchi's
ward, Shibuya and Ikebukuro. **Options**: a *core wards* regional scope that
names the gap on the page; the personal-services layer across its 11 wards
with food only where published (the page says which); or wait.

▶ **Owner, 2026-09-24: second method first.** Each of the 19 wards without a
catalogue food file gets its own site read, central wards first, and the scope
is decided after. **Taitō's own list is approved** under the raised bounds,
reading only 営業所所在地, 業種 and 屋号, never its operator columns.

▶ **Result, 2026-09-24: 11 of 23 wards now have a food-permit file** (9 full,
2 partial). **Shibuya has one; Chiyoda and Toshima do not.** Both release
theirs only on request or for in-person viewing, and so do Nerima and Edogawa
(behind a password sent after an application).

| Ward | File | Rows | Format / coordinates | As of | Host |
|---|---|---|---|---|---|
| **Shibuya** 13113 | `131130_food_businesses_list.csv`, 22.2 MB, UTF-8 | 39,304 (**16,993 open**) | national format, **coordinates 99.96%** | 2026-09-09 | ward's ArcGIS open-data site ⚠️ |
| **Taitō** 13106 | `2026ALL-IND-CSV.csv`, 1.59 MB, Shift_JIS | 7,676 | own format, coordinates 98.5%, **operator name + address columns** (individual operators masked ※ at source, 2,738 rows; the rest are mostly companies) | 2026-03-31 | ward's own |
| **Setagaya** 13112 | `zenkenr080331.csv`, 1.32 MB, Shift_JIS | 7,428 | own format, no coordinates | 2026-03-31 | ward's own |
| **Meguro** 13110 | `all_new_8.csv` + `all_old_8.csv`, UTF-8 | 2,495 + 1,087 | own format, no coordinates | 2026-04-01 | BODIK ⚠️ |
| **Nakano** 13114 | `opendata_550150.csv`, 1.98 MB | 5,790 | coordinates on all; **labels shifted** (trade name under 営業の種類) | ⚠️ **stale: to 2023-06-27** | wagmap ⚠️ |
| Shinagawa 13109 | `R6-7.csv` + 5 monthly | 2,421 | own format; 31–50% of addresses blanked | **partial: since 2024-04** | ward's own |
| Itabashi 13119 | 17 monthly XLSX | 897 | new permits only | **partial: since 2025-04** | ward's own |

**PDF only**: Ōta (full list, 93 + 16 pages), Kita (335 + 155 pages, "not open
data"), Arakawa (55 pages), Sumida and Adachi (new permits). **None found**:
Bunkyō, Suginami, Katsushika. **Three hosts are outside the ward domains**
(Shibuya's ArcGIS, Meguro's BODIK, Nakano's wagmap), each named by the ward's
own pages as its catalogue. **The owner accepted all three, 2026-09-24.**
**A ward is on the map only with a full, current list (owner, 2026-09-24)**:
Nakano (stale, to 2023-06) and the partial Shinagawa and Itabashi files are
left out, and the page names the missing wards. Files are in
`data/tokyo/raw/<code>/`.

**The four new full lists join as cleanly as the first four**
(`screen_japan_join.py shibuya / taito / setagaya / meguro`; the controls,
including Minato's 99.8%, are unchanged). Shibuya's file keeps closed premises,
so only rows with an empty 廃業日 are read (16,993 of 39,304). Taitō's addresses
start at the town, so a single-ward list defaults its ward.

| Ward | Fixed premises | Block | Independent check |
|---|---|---|---|
| Shibuya | 16,635 (+358 mobile) | **99.6%** | its own coordinates: median **23 m**, 99.6% within 250 m |
| Taitō | 7,559 | **100.0%** | its own coordinates: median **25 m**, 99.9% within 250 m |
| Setagaya | 7,428 | **100.0%** | none published |
| Meguro | 3,492 (+90 都内一円) | **99.9%** | none published |

⚠️ **CORRECTED 2026-09-24: only ONE of the eight food lists is essentially
complete, measured against an official count.** The join is unaffected; only
completeness is. The measure is each list's 飲食店 permit rows, vehicles
included, against 飲食店営業 in **Tokyo's statistical yearbook, table 19-8,
FY2024** (`data/tokyo/raw/tn24qv190800.csv`). That is the same basis every
Japanese city is measured on, since the yearbook equals MHLW's 衛生行政報告例
for 東京都. Four ward probes followed the same day.

| Ward | Of the official count | Why | What exists beyond our file |
|---|---|---|---|
| **Shibuya** | ✅ **101%** of 10,798 | the ward's own register, closed premises dropped | — |
| Shinjuku | 84% of 15,356 | complete as of 2023-01-01 (its disclosed vintage) | ⚠️ **A full list at 2026-03-31**: PDF, 1,023 pages, 15,333 permits, plus monthly new-permit PDFs. **Not on the open-data portal, so the site terms bar reuse without permission**. The PDFs also carry operator columns |
| Taitō | 81% of 8,112 | the ward's page: premises that opted out are left out | — |
| Setagaya | 63% of 9,291 | the ward's page: premises that opted out are left out | — |
| Meguro | 52% of 4,370 | new-law and old-law lists both published; **the gap is not yet explained** | — |
| **Minato** | **31%** of 15,939 | **consent-filtered** (the resource says so); new-law permits only | **Nothing.** No old-law list exists anywhere (ward site, both catalogues, web archive). The ward's own report: 16,073 restaurants in force at 2026-03-31, 11,631 new-law and 4,442 old-law |
| **Chūō** | **12%** of 11,056 | permits of 2021-06 to 2022-12 only, published 2024-03 and never updated | **Nothing.** No other list in any format. Side find: **complete personal-services lists** (August 2026) on the ward's site, licence not yet read (possibly site terms) |
| **Kōtō** | **9%** of 6,102 | consent-only new permits, 2021-06 to 2022-11 | Monthly lists of the last 12 months, but under site terms that bar reuse. Health bureau FY2024: 3,760 new-law + 2,285 old-law restaurants |

**Why Tokyo differs from the designated cities:**
- Each of the 23 wards runs its own health centre, so there are 23
  publishers.
- Four publish their own register (Shibuya, Taitō, Setagaya, Meguro).
- Three publish an export in the national recommended format that is **opt-in
  or consent-filtered**, the same shape as MHLW's national open data.
- Taitō, Setagaya and Meguro also leave out premises that declined
  publication.
- Chūō's is a one-off snapshot.

**The ways through are all requests, and all are the owner's act**
(`docs/gated_access.md`, items 29–32):
- **Chūō**: a disclosure request, ¥300 per item.
- **Kōtō**: 情報提供 from 保健所生活衛生課 食品衛生第三係, which its disclosure page
  names for facility lists.
- **Minato**: a 情報公開請求, routine there, which returns PDF on CD-R for ¥100
  with no open licence. Or ask みなと保健所 to publish the full list, since its
  own form says permits are published "in principle".
- **Shinjuku**: permission to reuse the 2026-03-31 PDF, or publication as CSV
  on its portal.

Minato stays valid as the join control. Whether the designated cities' own
lists also leave out opt-outs is being measured against MHLW's 衛生行政報告例
(PLAN.md).

**The own-time probe round, 2026-09-24 (the owner: agency contact is the
last resort, and the four drafted requests are PARKED).** Three methods were
tried for Chūō, Kōtō, Minato and Shinjuku. None fills a ward openly.

| Method | Result |
|---|---|
| **MHLW's 食品衛生申請等システム open data** per ward (PDL 1.0) | Almost nothing: new premises beyond our lists are Chūō +30, Kōtō +104, Minato +17, Shinjuku +43, i.e. **+0.1 to +3.1%** of the official count. It is an opt-in slice of online filings, mostly vending machines and office snack boxes |
| **The whole Tokyo catalogue**: 9,697 packages, 98 organisations | Two 総務局 COVID-era lists, both frozen May 2023: 徹底点検TOKYOサポート 認証店 (79,840 rows) and 感染防止徹底宣言ステッカー. With them Chūō would reach about 55%, Kōtō 51% and Minato 60% of the official count (central estimates). ⚠️ **But each dataset's own note asks users not to use it beyond COVID measures** (「それ以外の目的に用いないようにお願いします」), although the catalogue says CC BY 4.0. It is **not used** unless the owner decides otherwise. Everything else adds a few dozen rows per ward, and the 食品衛生自主管理認証 list is gone (the scheme ended 2025-03) |
| **OpenStreetMap**, calibrated in Shibuya | **Not viable.** It holds only 8–10% of the registered restaurants (15% at most). Chains are found 50% of the time and independents 7%, bars on upper floors are almost absent, and at least 1 in 9 of its points is closed. Added to the lists it lifts Chūō to about 17–20% and Kōtō to 15–18% |
| **Shinjuku's 2026-03-31 PDF list**, licence re-read | **NOT PERMITTED, or ambiguous in a way that matters.** The site terms name PDFs and forbid secondary use and modification without permission. The open-data terms reach only the portal. The "open data" wording comes from the application form, which addresses applicants, not users. **Shinjuku stays on its 2023 CSV** (84%, vintage disclosed). Any credit links the page, never a PDF (the site's linking rule) |

✅ **Decided by the owner, 2026-09-24:**
1. **The COVID-era lists are not used**, honouring their stated purpose and
   the shops' limited consent.
2. **Tokyo ships all 8 food wards, and the page gives each ward's share of
   the official count**, so the partial wards read as partial.
3. **MHLW's slice is added** to Chūō, Kōtō, Minato and Shinjuku at build,
   de-duplicated by address and name against the ward's list. The probe's
   matcher is in `scratchpad/tokyo_alt/`.

**Tokyo now: 8 wards with food lists, one essentially complete** (Shibuya;
the rest 9–84% of the official count, above), about **59,400 food permit
rows**. **The remaining hole is the very centre**: Chiyoda (Marunouchi,
Ōtemachi) and Toshima (Ikebukuro) release theirs only on request, and Bunkyō
publishes none. MHLW's open data does not fill them (Chiyoda 291 restaurants,
26% addressed). **The scope is the owner's call**: the 8 wards as a stated
"core wards" map with the centre missing, or wait for a request to Chiyoda.

## ✅ Licences — READ 2026-09-24

- **MLIT 位置参照情報 — PERMITTED WITH CONDITIONS** (PDL 1.0 via the site
  terms of 2026-03-23). **MUST DISPLAY**: `出典：位置参照情報ダウンロードサービス（国土交通省）（https://nlftp.mlit.go.jp/isj/）`
  and `「位置参照情報ダウンロードサービス」（国土交通省）（https://nlftp.mlit.go.jp/isj/）を加工して作成`,
  naming 街区レベル and 大字・町丁目レベル位置参照情報. **MUST NOT**: present the
  placements as MLIT's own.
- **Ward permits and registers — PERMITTED WITH CONDITIONS** (Tokyo Open Data
  Terms, §2: 「商用利用も可能です」; catalogue CC-BY-4.0). **MUST DISPLAY** one
  combined notice: ward, the Tokyo catalogue, dataset title, URL, **date of
  use**, that the data was **processed**, the CC BY 4.0 link. **MUST NOT**:
  present anything as the ward's or Tokyo's own; use a ward logo. Shinjuku's
  own site says CC BY **2.1 JP** for the same file — the combined notice covers
  both. ✅ **ACCEPTED (owner, 2026-09-24)**: Tokyo §6 / Chūō §5 — fault-based,
  uncapped reimbursement of the publisher's costs arising from the user's
  breach; the same class as Taiwan's OGDL §六(三), Rio's and IBGE's.
- **The four wards read from their own sites: all PERMITTED WITH CONDITIONS
  (CC BY 4.0), read 2026-09-24.** Nothing is owed to any ward. Each ward's
  default no-copying rule gives way to its open-data terms, so none is in
  Sendai's position. Each needs its OWN credit, not the catalogue's combined
  notice; the forms are in `docs/data_sources.md`, Japan section.
  - **Shibuya**: 渋谷区オープンデータ利用規約; downloading is acceptance. Credit
    `「食品等営業許可・届出一覧」（渋谷区）（URL）を加工して作成`. No cost clause.
    Re-read the terms before each republish.
  - **Taitō**: CC BY 4.0 through the ward's licence page, and the Tokyo
    catalogue's terms through its link-only entry. The ward prescribes four
    credit elements, including a no-warranty sentence. A link must name
    台東区公式ホームページ.
  - **Setagaya**: 世田谷区オープンデータ利用規約 §2, with a prescribed
    「…改変して利用しています」 form. Not on the Tokyo catalogue, so there is no
    date-of-use notice.
  - **Meguro**: BODIK's `131105/tos/`, the Tokyo template. The credit adds a
    link labelled 目黒区オープンデータカタログサイト.
  - **Cost**: Setagaya §4 and Meguro 第8項 match Tokyo §6, and Taitō inherits
    Tokyo §6. All are within the owner's Japan-wide acceptance.
- **MLIT N02** — PDL 1.0, read 2026-09-21; attribution
  `「国土数値情報（鉄道データ）」（国土交通省）をもとに作成`.
- **MLIT N03** (the ward boundaries that decide which stations count): CC BY
  4.0, read 2026-09-24. Permitted for picking stations and anchoring labels.
  ⛔ **Never draw it**: showing its boundaries as a map may need GSI's
  approval under the Survey Act (`docs/data_sources.md`, Japan section).

## Privacy

**Food files**: 法人名 carries corporate names; Minato leaves individuals blank
(12 of 5,721 non-corporate). **Personal-services registers carry 営業者氏名
and 営業者_所在地 (the operator's own address) in Taitō, Shinagawa, Shibuya
and Bunkyō** — **read ONLY 名称 and 所在地_*, never the 営業者 columns**, and
run `check_personal_exposure.py`.

## Region

`"region": "East Asia"` (with Seoul, Taipei and Hong Kong). Project to **UTM 54N
(EPSG:32654)**.

## Still unknown

- 🚩 **Scope**: which wards, and how the gap is stated. Decided after the wards' own sites are read (owner, 2026-09-24).
- ⚠️ Shinjuku's 2023 vintage: a newer file on the ward's own page? (Used with its vintage disclosed if not.)
- ⚠️ The Economic Census control's figures (the source is decided); the wards whose own sites are being read.
- ✅ decided 2026-09-24 (owner): see the block at the top (Shinkansen out). ⚠️ Still open: limited-express-only lines, and which N02 lines are commuter.
- ✅ **Meguro's 生活衛生 registers, measured 2026-09-24**: `131105_barber`,
  `131105_hairdressingshop` and `131105_cleaning_shop` on BODIK (CC BY 4.0),
  complete lists as of 2026-03-31. `screen_japan_join.py meguro-life`:
  - 143 barbers, 1,076 beauty salons, 202 laundries.
  - **1,412 premises**, after 9 storeless laundry pick-ups (無店舗取次店 at
    `目黒区内`) are dropped. **100.0% placed at block level.**
  - **Columns**: 施設名称, 施設所在地, 施設方書, 施設（種別）等, 許可日 and 許可番号.
    Also 営業者名 and ＴＥＬ１, which are never read.
  - ⚠️ **The files are tab-separated lines, each wrapped whole in CSV quotes.**
    The shared reader now unwraps them.
  - **Meguro also publishes monthly new, succession (承継) and closure (廃止)
    lists**, so a build can bring the March list up to date both ways.
- ⚠️ Nakano's food file (a vendor map host) stays deferred.

```brief-checks
[
  {
    "id": "tokyo-minato-permits-live",
    "claim": "Minato's food-permit file is keyless and live - the control ward, 5,721 permits",
    "kind": "http_ok",
    "url": "https://opendata.city.minato.tokyo.jp/dataset/54d8c582-00e2-4730-a23f-4a5befec9ae5/resource/c9d0299e-8e05-4317-877f-83055709e41f/download/food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "tokyo-catalogue-cc-by",
    "claim": "Tokyo's catalogue declares Minato's food-permit list CC BY 4.0",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t131032d0000000244",
    "present": ["CC-BY-4.0"]
  },
  {
    "id": "tokyo-terms-commercial-use",
    "claim": "The Tokyo Open Data Terms grant reuse including commercial use",
    "kind": "http_contains",
    "url": "https://portal.data.metro.tokyo.lg.jp/terms/",
    "present": ["商用利用"]
  },
  {
    "id": "tokyo-isj-minato-live",
    "claim": "MLIT's block-level address file for Minato answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13103-24.0a.zip",
    "min_bytes": 20000
  },
  {
    "id": "tokyo-isj-terms",
    "claim": "MLIT's download-service terms cover the location reference information under PDL 1.0",
    "kind": "http_contains",
    "url": "https://nlftp.mlit.go.jp/ksj/other/agreement.html",
    "present": ["位置参照情報"]
  },
  {
    "id": "tokyo-n02-rail-live",
    "claim": "MLIT N02 railway data (all JR, subway and private lines) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip",
    "min_bytes": 5000000
  },
  {
    "id": "tokyo-projected-crs",
    "claim": "Tokyo projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.7,
    "expect": "EPSG:32654"
  }
]
```
