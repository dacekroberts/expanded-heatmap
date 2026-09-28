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
| Meguro | 52% of 4,370 | **first permits only** (measured 2026-09-24, below): premises that moved from an old-law permit onto the revised law since 2021 are in neither list. The share falls as the remaining old-law permits expire | **Nothing.** The monthly 「新規、更新、届出」 lists are first permits only too |
| **Minato** | **31%** of 15,939 | **consent-filtered** (the resource says so); new-law permits only | **Nothing.** No old-law list exists anywhere (ward site, both catalogues, web archive). The ward's own report: 16,073 restaurants in force at 2026-03-31, 11,631 new-law and 4,442 old-law |
| **Chūō** | **12%** of 11,056 | permits of 2021-06 to 2022-12 only, published 2024-03 and never updated | **Nothing.** No other list in any format. Side find: **complete personal-services lists** (August 2026) on the ward's site. **Not used**: they are not open data, and the site's copyright clause bars reuse without permission (licence read 2026-09-24, `data_sources.md`) |
| **Kōtō** | **9%** of 6,102 | consent-only new permits, 2021-06 to 2022-11 | Monthly lists of the last 12 months, but under site terms that bar reuse. Health bureau FY2024: 3,760 new-law + 2,285 old-law restaurants |

**Why Tokyo differs from the designated cities:**
- Each of the 23 wards runs its own health centre, so there are 23
  publishers.
- Four publish their own register (Shibuya, Taitō, Setagaya, Meguro).
- Three publish an export in the national recommended format that is **opt-in
  or consent-filtered**, the same shape as MHLW's national open data.
- Taitō and Setagaya also leave out premises that declined publication.
  (Meguro was grouped with them here until 2026-09-24. Its page says nothing
  of the kind; its gap is a different one, below.)
- Meguro publishes first permits only.
- Chūō's is a one-off snapshot.

**Meguro's 52%, measured 2026-09-24.** It publishes two lists as at
2026-04-01: revised-law `all_new_8.csv` and old-law `all_old_8.csv`. Read
by exact column name, with 営業者氏名 and 施設電話番号 never read:
- **No overlap.** The two lists share no 施設NO or 許可番号. Together they hold
  2,279 restaurant rows (1,443 revised-law and 836 old-law), which is 52.2% of
  4,370. No row has expired.
- **Every revised-law row is a first permit.** 新規更新の別 is 新規 on all
  2,495 rows, where the old-law list has 590 新規 and 497 更新.
- **The flow is flat.** Revised-law restaurant permits by fiscal year: 274
  (FY2021, from June), 250, 314, 316, 289. Across Tokyo, the revised-law
  count grew by **27,419 in FY2024 alone** (94,354 → 121,773) while the old-law
  count fell by 27,277, because holders moved across as their old permits
  expired. On Tokyo's split, Meguro held about 2,730 revised-law restaurants
  at 2025-03-31, and the list has 1,154 permitted by then.
- **The monthly lists confirm it.** Seven monthly 「新規、更新、届出施設一覧」
  files (令和7年9月 to 令和8年3月) have 255 rows, **all 新規**, despite the
  title. 252 are in `all_new_8.csv`.
- **So a premises that moved onto the revised law is in neither list.** How
  the ward records a move-over is not published: it may be a renewal-type
  record the export leaves out. The ward has not said.
- **Not opt-outs.** The ward's list page
  (`/seikatsueisei/kenkoufukushi/eisei/seikatueisei_opendata.html`) warns
  only that closed or changed premises and staff canteens may be included.
- **The share will fall.** The 1,087 old-law permits still in the list
  expire by 2029 (584 in 2026, 423 in 2027). Each one that moves across drops
  out of both lists.
- **No own-time fix.** Nothing else Meguro publishes carries them. MHLW's
  slice added at most about 3% in the four wards probed, and it holds new
  online filings, not move-overs. Meguro ships at its measured share,
  disclosed, like the other partial wards (owner, 2026-09-24).

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

## Ward cards — all 23 wards, food leg (from 2026-09-28)

**ON** = full, current, permitted food list: the ward is built. **OFF** = not
built, for the reason given: its stations are drawn hollow and labelled "no
business data" (owner, 2026-09-28). **OPEN** = not yet decided, with what is
still unknown. Personal services (生活衛生 registers, Tokyo catalogue, CC BY
4.0) are listed separately, because a ward can be OFF for food and still have
them. Updated as each ward is settled; the detailed card for each settled
missing ward follows the table.

| Ward | Code | Food | Why / next step | Licence | Personal services |
|---|---|---|---|---|---|
| Chiyoda | 13101 | **OFF** | on request only; request parked (`gated_access.md` 22) | — | ✓ |
| Chūō | 13102 | **ON** (12%) | 2021-06 to 2022-12 snapshot, share disclosed (owner, 2026-09-24) | Tokyo catalogue, CC BY 4.0 | — |
| Minato | 13103 | **ON** (31%) | consent-filtered, share disclosed | Tokyo catalogue, CC BY 4.0 | ✓ |
| Shinjuku | 13104 | **ON** (84%) | 2023-01-01 CSV, vintage disclosed; the 2026 PDF is not permitted. Re-checked 2026-09-28: no newer CSV (the server re-stamped the 2023 file 2026-08-31; the content is unchanged) | Tokyo catalogue, CC BY 4.0 | — |
| **Bunkyō** | 13105 | **OFF** | **no list exists in any format; MHLW's slice is 2.4% (re-probed 2026-09-28)** | — | ✓ |
| Taitō | 13106 | **ON** (81%) | opt-outs left out | ward's own, CC BY 4.0 | ✓ |
| Sumida | 13107 | **OFF** | PDF of new permits only (FY R5 to R8.8); re-checked 2026-09-28: no full list anywhere, so the licence is not read | not read | — |
| Kōtō | 13108 | **ON** (9%) | consent-only new permits, share disclosed | Tokyo catalogue, CC BY 4.0 | — |
| Shinagawa | 13109 | **OFF** | partial, since 2024-04 (the page still says so); re-checked 2026-09-28: no full list anywhere | — | ✓ |
| Meguro | 13110 | **ON** (52%) | first permits only, the accepted exception | BODIK, CC BY 4.0 | ✓ (BODIK) |
| **Ōta** | 13111 | **OFF** | **full list is PDF only and not open data; the site policy bars reuse (owner, 2026-09-28)** | 🚫 not permitted | ✓ |
| Setagaya | 13112 | **ON** (63%) | opt-outs left out | ward's own, CC BY 4.0 | — |
| Shibuya | 13113 | **ON** (101%) | the ward's own register | ward's own, CC BY 4.0 | ✓ |
| Nakano | 13114 | **OFF** | stale, to 2023-06-27; re-checked 2026-09-28: unchanged. ⚠️ wagmap now labels it データ作成基準日 2026/6/30, but the file is still the 2023 one (Last-Modified 2023-10-04) | — | — |
| **Suginami** | 13115 | **OFF** | **no list exists in any format; MHLW's slice is 3.0% (re-probed 2026-09-28)** | — | — |
| Toshima | 13116 | **OFF** | in-person viewing only; parked | — | ✓ |
| **Kita** | 13117 | **OFF** | **PDF list "not open data", site terms bar reuse; the CC BY CSV holds 52 permits, 2022–2024 (read 2026-09-28)** | 🚫 not permitted (PDF) | — |
| **Arakawa** | 13118 | **OFF** | **site terms bar all reuse; no open-data route (read 2026-09-28)** | 🚫 not permitted | ✓ |
| Itabashi | 13119 | **OFF** | partial, new permits since 2025-04; re-checked 2026-09-28: no full list anywhere | — | — |
| Nerima | 13120 | **OFF** | on request only (password after application); parked | — | — |
| Adachi | 13121 | **OFF** | PDF of new permits only (R7.4 to R8.8); re-checked 2026-09-28: no full list anywhere (catalogue: 2,435 entries), so the licence is not read | not read | — |
| **Katsushika** | 13122 | **OFF** | **no list exists in any format; MHLW's slice is 3.5% (re-probed 2026-09-28)** | — | ✓ |
| Edogawa | 13123 | **OFF** | on request only (password after application); parked | — | — |

**Tally, 2026-09-28 — every ward settled**: ON 8 · OFF 15 · OPEN 0. No
missing ward can join the map from its own publications. The ways in are all
requests (`docs/gated_access.md` and each card's "route in"), and all are
parked.

### Arakawa 荒川区, 13118 — OFF (read 2026-09-28)

| Field | |
|---|---|
| verdict | **OFF**: the site terms bar reuse, and no open-data route reaches the list |
| file(s), host, size | page `https://www.city.arakawa.tokyo.jp/a032/jigyousha/toroku/syokuhinnshisetu.html` (ID 4207, updated 2026-09-15). Full list `…/documents/4207/r08kyokarisuto.pdf`, 1,563,829 B, 55 pages. New permits: `r7sinnki.pdf`, `r8sinnki.pdf`. Closures: `r7haigyou.pdf`, `r8haigyou.pdf` |
| format | PDF only. The ward says there is no CSV or Excel version because names use characters outside Shift_JIS (注釈2); `.csv`, `.xlsx` and `.xls` all return 404. Address layout: 町名 / 丁番号 / 所在地 / ﾋﾞﾙ名 |
| as of | 2026-03-31 (full list, updated each 4月15日); the new-permit and closure lists are updated monthly |
| closures | none in the full list; separate closure PDFs. The page warns closed premises may be included (注釈1) |
| operator columns | 営業者氏名, 営業者住所, 住所電話, which are unmasked (注釈2) |
| own coordinates | none |
| licence | 🚫 **NOT PERMITTED, or ambiguous in a way that matters**. 著作権について (`/a004/aboutwebsite/tyosakuken.html`): 「本サイト上の文書・画像等の各ファイルの無断使用・転載・引用は禁じます」. That covers the files and their contents, and is stricter than Shinjuku's (it bars even 引用). 荒川区オープンデータ利用規約 (CC BY 4.0) covers only the catalogue at `/opendata/index.php`: 204 items, none of them food. The Tokyo catalogue (`t131181`, 33 packages) and BODIK hold no food list either. The facts-are-not-copyrightable reading is not relied on (the Shinjuku precedent) |
| join / share | not measured: the list is not used |
| personal services | 美容所, 理容所 and クリーニング所 台帳 on the Tokyo catalogue (`t131181`), CC BY 4.0: already in the 11-ward layer |
| route in | permission from 広報・シティプロモーション課 (the channel the copyright clause names), or publication on the ward's catalogue. Outreach is the owner's act and the last resort: **parked** |

### Bunkyō 文京区, 13105 — OFF (re-probed 2026-09-28)

| Field | |
|---|---|
| verdict | **OFF**: no food-premises list exists, in any format, current or historical. No page offers one on request, so this is not Chiyoda's shape. The ward is silent |
| where it was looked for | **The ward's own host**: every page in the food-hygiene block (`/kenkou/seikatsueisei/shokuhineisei/`, `b026/p002876` to `p002934`, and the newer `p0075xx` / `p0076xx` pages) holds forms, plans and leaflets only. **The ward's catalogue** (`b004/p006286.html`, index `documents/6059/metadata.csv`): 69 datasets, none food, and no 自治体標準オープンデータセット bundle. **The Tokyo catalogue** (`t131059`): 57 packages, none food. **BODIK**: no Bunkyō organisation. **Web Archive**: 128 captured URLs under the old `/hoken/seikatsueisei/syokuhin*` tree (2015–2024) and about 16,600 `/documents/` URLs; no premises list among them |
| the section's other lists | the sibling page `b026/p002833.html` (環境衛生営業施設一覧, as of 2026-08-31) publishes XLSX lists for 理容所, 美容所, クリーニング所, 旅館業, 公衆浴場 and 興行場, with no food counterpart |
| second shapes | **MHLW 食品衛生申請等システム** (`13105_food_business_all.csv`, PDL 1.0, to 2026-08): 1,100 rows, but only 97 live permits, 88 of them 飲食店営業, so **2.4% of the yearbook's 3,716**. The rest are notifications (office snack freezers, vending machines, canteens). **Not used**. The 食品衛生優良施設 award lists (9 and 8 premises) are negligible |
| personal services | 美容所 372, 理容所 109, クリーニング所 208 and 旅館 55 on the Tokyo catalogue (`t131059`, CC BY): already in the 11-ward layer. The ledgers carry 営業者氏名 and 法人代表者氏名, never read |
| route in | a request to 文京保健所生活衛生課食品衛生担当 (03-5803-1228). Outreach is the owner's act and the last resort: **parked**, and not drafted |

### Suginami 杉並区, 13115 — OFF (re-probed 2026-09-28)

| Field | |
|---|---|
| verdict | **OFF**: no food-premises list exists, in any format, current or historical, and no page offers one on request |
| where it was looked for | **The ward's own host**: all 16 pages of the 食品の衛生 block (`/kenkou/eisei/shokuhineisei/`), which hold guides and leaflets only. **The ward's catalogue** (`/opendata/index.php`): 5,988 files on 519 dataset pages, none food, and no 生活衛生課 among its 19 departments. Its index `documents/8444/open-data-list.csv` has 142 titles. The only ZIP is a GTFS feed. **The Tokyo catalogue** (`t131156`): 103 packages, none food. BODIK: none. **Web Archive**: 372 archived documents under the old food and hygiene pages, none of them a list |
| the section's other lists | 旅館業営業許可施設一覧 (`/documents/870/ryokan202608.pdf`) and the 民泊 届出住宅 list (`/documents/871/todokede.pdf`, with a no-commercial-use request). No food, barber, beauty or laundry list |
| control | the ward's own statistics table 10-12 (`/documents/25287/r7-10-12-01.csv`): 飲食店営業 3,631 new-law + 2,221 old-law = **5,852** at FY2024 end, the same as the yearbook |
| second shapes | **MHLW 食品衛生申請等システム** (`13115_food_business_all.csv`): 1,246 rows, 175 live 飲食店営業 permits dated 2022-02 to 2026-08, so **3.0%**. **Not used** |
| 403 | `suginami.geocloud.jp` (すぎナビ, the map open-data list): a bare nginx 403 with no statement of who it is for. The ward describes it as map layers. Not worked around |
| personal services | none published (no 生活衛生 packages on `t131156`) |
| route in | a request to 杉並保健所 生活衛生課. Outreach is the owner's act and the last resort: **parked**, and not drafted |

### Katsushika 葛飾区, 13122 — OFF (re-probed 2026-09-28)

| Field | |
|---|---|
| verdict | **OFF**: no food-premises list exists, in any format, current or historical, and no page offers one on request. The ward is silent |
| where it was looked for | **The ward's own host** (`www.city.katsushika.lg.jp`): the whole food-hygiene block (`/kenkou/1030184/1001799/`, 90 pages and 72 files) and the food download block (`/online/…/1007410/`, 12 pages). They hold leaflets, newsletters and forms, and no list. **Catalogues**: the ward has none of its own; its page says its open data is on the Tokyo catalogue only. Tokyo catalogue `t131229`: 32 packages, none food, and the gaps in the ID series return 404. BODIK: none. **Web Archive**: no food list ever captured on the host |
| the section's other lists | 環境衛生関係施設一覧表 (`/online/1007359/1030292/1007374/1007411/1026096.html`): seven monthly PDFs as of 2026-08-31 (理容所 to 住宅宿泊事業), with no food counterpart |
| second shapes | **MHLW 食品衛生申請等システム** (`13122_food_business_all.csv`, PDL 1.0): 1,282 rows, 161 live 飲食店営業 permits dated 2021-10 to 2026-08, so **3.5% of the yearbook's 4,599**. **Not used**. 「かつしかの元気食堂」 (a certification list of about 150 shops, PDF, 2026-05-20) is not a permit register |
| personal services | クリーニング所, 理容所, 美容所 and 旅館 台帳 on the Tokyo catalogue (`t131229`, CC BY): already in the 11-ward layer |
| route in | a 情報公開請求 for the 食品営業許可台帳, via 生活衛生課. Outreach is the owner's act and the last resort: **parked**, and not drafted |

### Ōta 大田区, 13111 — OFF (owner, 2026-09-28)

| Field | |
|---|---|
| verdict | **OFF**: the full list is PDF only and on no open-data list, so the site policy governs it and bars reuse. The open-data terms' site-wide preamble is not relied on |
| file(s), host, size | page `https://www.city.ota.tokyo.jp/seikatsu/hoken/eisei/shokuhin/ippan/syokuhinsisetuitiran.html` (updated 2026-09-02; the host is `city.ota.tokyo.jp`, not `.lg.jp`). Full list `…/syokuhinsisetuitiran.files/r0809.zip`, 14,650,229 B, holding `新法施設一覧（2026年9月1日現在）.pdf` (35.8 MB) and `旧法施設一覧（2026年9月1日現在）.pdf` (5.3 MB), probably the 93 + 16 pages. Monthly new-premises PDFs `r0709.pdf` to `r0808.pdf` |
| format | PDF only (in a ZIP); `.csv` / `.xlsx` siblings return 404. Address layout: 町名 / 番 / 号 / ビル名 |
| as of | 2026-09-01; updated monthly (by the 10th). Includes 届出 premises |
| closures | none; the page says closures after compilation are not reflected |
| operator columns | 申請者氏名 (unmasked), 所在地電話番号 (from the monthly PDF; the ZIP's PDFs unverified) |
| licence | 🚫 **NOT PERMITTED, or ambiguous in a way that matters**. The site policy (`/aboutweb/policy.html`) bars 無断での使用・転載、二次利用, except for 「大田区がオープンデータとして公開しているもの」. The open-data terms (`/kuseijoho/opendata/open-data.files/riyoukiyaku.pdf`, 政府標準利用規約 2.0, adopted about 2021-09-28) literally cover the whole site. **Why OFF**: the policy's exception dates from 2019-05, when open data meant the Tokyo catalogue, and was left unwidened in the 2021-09-26 and 2025-11-27 edits. The terms are framed around downloaded data. No page carries a site-wide badge. The same 生活衛生課 put its barber, beauty, laundry and inn registers on the Tokyo catalogue as CC BY CSV, and left the food list as PDF. The ward's own definition of open data requires 機械判読. Not on the ward's list (175 rows) or the Tokyo catalogue (`t131113`, 280 packages) |
| join / share | not measured: the list is not used |
| personal services | 美容所, 理容所, クリーニング所 and 旅館 台帳 on the Tokyo catalogue (`t131113`), CC BY 4.0: already in the 11-ward layer |
| route in | permission from 生活衛生課 食品衛生 (03-5764-0697), or publication on the catalogue. Outreach is the owner's act and the last resort: **parked** |

### Kita 北区, 13117 — OFF (read 2026-09-28)

| Field | |
|---|---|
| verdict | **OFF**: the full list is PDF and "not open data", and the site terms bar reuse. The open CSV is partial and stale |
| file(s), host, size | page `https://www.city.kita.lg.jp/socialcare-health/hygiene/1009013/1017183.html` (the old `city.kita.tokyo.jp/…/sisetuitiran.html` returns 301 to it; updated 2026-09-11). Full list under `…/_res/projects/default_project/_page_/001/017/183/`: `r8-3-31-shinhou2.pdf` (新法, 2,464,505 B) and `r8-3-31-kyuhou2.pdf` (旧法, 1,589,766 B), probably the 335 + 155 pages. Monthly 新規, 更新 and 廃業 PDFs alongside |
| format | PDF only for the full list; 12 guessed `.csv` / `.xlsx` / `.xls` names return 404 |
| as of | 2026-03-31; the monthly lists run to 2026-08 |
| operator columns | not seen (the PDFs were not opened). The page: an individual operator's address and phone are not published, and operators who asked are omitted |
| licence | 🚫 **NOT PERMITTED, or ambiguous in a way that matters**. The page: 「このページは、東京都北区情報公開条例に基づいて公開するもので、オープンデータとは異なります。」 The site terms (`/about/1016811.html`) forbid 転載、複製、改変 without permission, beyond 私的使用 and 引用. 北区オープンデータ利用規約 (2020-07-03) says itself that it does not cover the whole site: 「本規約は、北区公式ホームページ掲載の全ての情報に該当するものではありません。」 That is the opposite of Ōta's terms |
| the open CSV | `15.食品等営業許可・届出一覧.csv` inside the 自治体標準オープンデータセット zip (`…/001/014/461/hyo-jun.zip`, 293,787 B, 2026-08-26), CC BY 4.0, national 34-column format with 緯度/経度. **Only 515 rows**: 届出 459, 許可 52, 届出(廃業) 4; 46 are 飲食店営業; permits dated 2022-04-19 to 2024-10-29. It fails the full-and-current rule: **recorded, not used** |
| join / share | not measured: the list is not used |
| personal services | none found on the Tokyo catalogue (`t131172`: 7 packages, none 生活衛生) |
| route in | permission from 政策経営部広報課 or 保健所生活衛生課; the page itself points to a 情報公開請求 for anything more. Outreach is the owner's act and the last resort: **parked** |

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
