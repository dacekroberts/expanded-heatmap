# Fukuoka — build brief

**Step 0 measured 2026-09-24 (MHLW's viewer approved by the owner, question
10).** Run `python scripts/brief_check.py fukuoka` before writing any code.
Coordinates: the `address-join` skill, measured by
`scripts/screen_japan_join.py fukuoka`, `fukuoka-mhlw` and `fukuoka-life`.

**✅ Decided by the owner, 2026-09-24, for every Japanese city:** (1) **the Shinkansen does not count**, since it is long-distance travel between cities; (2) **the city line only**: only stations inside the city get rings, matching the city-only permit list, with a per-line stub test at build (any urban line cut to a stub goes back to the owner); (3) **菓子製造業 and そうざい製造業 count**, in the Retail bucket (bakeries, confectioners and delis sell over a counter), with the factory and central-kitchen share measured from trade names before publishing. Open items below that ask these questions are answered.

---

## The one-line summary

**Food comes from TWO lists that split by filing channel: the city's own list
of permits held since before 2021-06 (3,231 restaurants), and MHLW's
食品衛生申請等システム open data for everything since (21,088 restaurants).
They overlap by 1.3%, and together make 14.8 restaurants per 1,000
residents, inside the Kobe (13.0) to Osaka (19.0) range.** ⚠️ **But 24% of
MHLW's restaurants withhold their address** (per-field consent), so about 80%
of the city's restaurants can be placed. Personal services 5,846 at 99.2%
block.

---

## Business leg — two food sources, one filing split

| | City's own list | MHLW open data |
|---|---|---|
| **File** | `https://data.bodik.jp/dataset/5925a9fb-3326-4499-9acd-7b18c03d5e32/resource/70d22acf-2353-4bc1-b45d-f12d45da5216/download/r8.7.csv`: **855,886 B**, 3,977 rows, as of 2026-07-31. BODIK is the city's designated open-data site (`odcs.bodik.jp/401307`) | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40130_food_business_all.csv`: **14,880,467 B**, 40,390 live rows (27,815 permits, the rest notifications), as of 2026-08 end. A plain GET, no session |
| ⚠️ **BODIK is flaky** | The same URL downloaded at 07:37 and answered HEAD, ranged GET and GET at 200 at 07:55. Over the same day it returned **HTTP 500 twice and 502 once to `brief_check`**, and **504s and timeouts** to both licence reads. A build-time risk, not a blocker: `fetch_sources.py` must retry with backoff, and a failure is not a dead source. **If this check fails, re-run it before correcting anything** | |
| **What it holds** | **Only permits granted before 2021-06-01 and still held.** The dataset's own note sends everything since to MHLW | **Online filings where the applicant agreed to open-data publication**, field by field. Fukuoka evidently routes nearly all filings through the system: 2,175–4,426 restaurant permits a year since 2021 |
| Columns | 営業所所在地, 営業所所在地ビル名, **屋号**, **業種**, 業態, permit dates | 営業施設名称、屋号又は商号, **営業の種類**, 業態, **営業施設所在地**, 営業施設方書, **緯度 / 経度** (the publisher's own), 申請区分 (許可 / 届出), dates |
| Restaurants (飲食店営業, fixed) | **3,231** | **21,088**, of which **16,110 (76%) carry an address** |

- **Overlap, measured at block level** (same ward, town and block, same
  normalised trade name): 200 of MHLW's addressed restaurants (**1.3%**). The
  two lists are disjoint by construction: a renewal since 2021-06 moves a
  premises from the city's list to MHLW's.
- **Combined**: 24,319 restaurants, **14.8 per 1,000 residents**. **Placeable**
  (own list + addressed MHLW): 19,341, **11.8 per 1,000**. ⚠️ **The ~20%
  shortfall is premises that chose not to publish their address.** Whether
  they cluster spatially is unmeasured. It is a disclosed defect, like
  Amsterdam's vacancy.
  - ✅ **What the page says, approved by the owner 2026-09-24** (the short
    version, chosen over a fuller draft): "About one restaurant in five in
    Fukuoka chose not to publish its address in the national filing system
    and is not on this map. Where they are is not known." The basis: 4,978 of
    24,319 restaurants (MHLW's 21,088 less the 16,110 with an address), so
    19,341 placeable (79.5%). The two lists together read 101% of the
    official count.
- **Food retail**: MHLW's notifications add a PARTIAL, opt-in food-retail
  bucket (その他の食料・飲料販売業, コンビニエンスストア, 百貨店・総合スーパー…).
  Disclose as partial, per the owner's rule for Tokyo.
- **Personal services** (BODIK, the city's own): 理容所 `…/download/202609011129.csv`
  (901), 美容所 `…/download/202609011112.csv` (3,929), クリーニング所
  `…/download/202604011019.csv` (1,019) — **5,846 fixed premises**. Columns:
  施設名称, **施設所在地**, 施設ビル名, 業務種別 / 種別, then operator columns.

### Taxonomy — first cut

| Bucket | Types |
|---|---|
| Food service | 飲食店営業 (own) · ① 飲食店営業 (MHLW), excluding vehicles (業態 自動車) · 喫茶店営業 (own, pre-2021 type) |
| Food retail (partial, opt-in) | MHLW notifications: ⑬ その他の食料・飲料販売業, ⑩ コンビニエンスストア, ⑪ 百貨店・総合スーパー, ⑦ 野菜果物販売業, ① 魚介類 / ② 食肉 (包装済み) |
| Decide at build | 菓子製造業, そうざい製造業 |
| Out | vending machines (⑤, ⑫), 集団給食施設, manufacturing, on-train sales (列車内), 廃業 rows |

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **7 wards** (40131 東, 40132 博多, 40133 中央, 40134 南,
40135 西, 40136 城南, 40137 早良).

| Tier | Own food list (3,977) | MHLW, addressed (25,982) | Personal services (5,846) |
|---|---|---|---|
| Block | **98.1%** | **96.8%** | **99.2%** |
| Town-chōme / 大字 centroid | 0.4% | 0.8% | 0.3% |
| Unplaced | 1.5% | 2.4% | 0.6% |

*(Re-measured 2026-09-24 after Kyoto's rules A–D in `japan_register.py`: was
98.1 / 96.7 / 99.1% block, 1.6 / 2.5 / 0.6% unplaced.)*

**Independent check**: MHLW's own coordinates against the block point sit a
**median 36 m** apart, **97.1% within 250 m** (25,120 rows). So an MHLW row the
join misses can use the publisher's point. The unplaced are rural 大字
(元岡, 西浦, 志賀島) and on-train sales (not premises).

## 🚇 Rail — MLIT N02, commuter rail INCLUDED (owner, 2026-09-24)

`https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip`. By general
knowledge (not yet read from N02): the Fukuoka City Subway (Kūkō, Hakozaki,
Nanakuma), JR Kyushu and Nishitetsu. ⚠️ Stations are LineStrings, so centroid
them. ⚠️ Open: the Shinkansen (Hakata). See `docs/commuter_rail_list.md`.

**✅ Stub test, measured 2026-09-24** (`pipeline/countries/japan.py` `stub_test()`: N02 stations, Shinkansen excluded, against the city's N03 ward polygons): **PASSES.** All three subway lines are 100% inside, and Nishitetsu Kaizuka 9 of 10. JR and Nishitetsu Tenjin-Ōmuta are cut at the line as intended. The two-station Hakata-Minami line keeps only Hakata, which is served anyway: drop it.

## Scope

**Fukuoka City (7 wards).** JR and Nishitetsu run on to Kasuga, Ōnojō and
Dazaifu; check which stations fall outside at build. The scope is the owner's
call.

## ✅ Licences — READ 2026-09-24

- **MHLW open data — PERMITTED WITH CONDITIONS** (PDL 1.0, CC BY 4.0-compatible).
  - **The grant**: the system's own site terms (`https://i2fas.mhlw.go.jp/termsofuse.htm` §2):
    「…権利表記の記載がない限り「公共データ利用規約（第1.0版）」（PDL1.0）が適用されています。」,
    and PDL 1.0 says 「商用利用も可能です」.
  - **The system's 利用規約 binds applicants and authorities only** (第3条), so
    its 第7条 ban on 改変・編集・頒布 does not reach reusers.
  - **MUST DISPLAY** the source, AND that it was processed and by whom
    (重要情報 1.1). For example:
    `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
    naming this project as the processor and what it did (filtered by type,
    placed by coordinates, deduplicated against the city list, aggregated
    around stations). Link the top page only, as the site asks.
  - **MUST NOT**: present processed data as MHLW's own or unprocessed; use
    MHLW's logo; **claim the list is complete** (it is opt-in, online filings
    only); state or imply accuracy (免責 1) ウ).
  - **Cost**: 免責 1) エ, the user resolves at its own cost any damage from
    using the site. No express indemnity. Japanese law, Tokyo courts.
    ✅ **ACCEPTED (owner, 2026-09-24)** with every Japanese cost clause of
    this class (`docs/data_sources.md`, Japan section).
  - ⚠️ **OPEN (owner, minor)**: 免責事項・著作権 2) ウ, 「営利目的での複製・頒布等、再利用しないことに同意する」,
    could be read to cover the data rather than the site's articles and
    photos. **This project is non-commercial, so it is fine under both
    readings today.** It matters only if the site ever becomes commercial.
    Only MHLW can settle it.
- **The city's lists on BODIK — PERMITTED WITH CONDITIONS** (CC BY 4.0, read
  2026-09-24).
  - **The grant**: the city's own terms, `https://odcs.bodik.jp/401307/tos/`
    第１条: 「…本市等が著作権を有する著作物の利用…については、クリエイティブ・コモンズ・ライセンス…の表示4.0国際…によるものとします。」
    BODIK defers to each municipality's terms. The city does not adopt
    政府標準利用規約.
  - **MUST DISPLAY (第７条)**: each dataset's **作成者** as recorded (food:
    `保健医療局 食品安全推進課`; beauty and barbers: `福岡市保健福祉局`; cleaning:
    `保健福祉局 生活衛生課`), the **resource name**, which carries its as-of date
    so generate it from the file used, and the **resource URL**. Also "CC BY
    4.0" linked, and a statement that the data was modified.
  - **MUST NOT**: claim completeness, accuracy or currency (第４条); imply
    affiliation or endorsement (CC BY §2(a)(6)); use city logos (第３条).
  - **Cost (第４条)**: complaints from our own breach or infringement are
    resolved at our own cost. This is **the fault-based class the owner
    accepted for Tokyo §6 and Sapporo 第9条3**. No indemnity. Japanese law,
    Fukuoka District Court. ✅ **ACCEPTED (owner, 2026-09-24)**: one decision
    for every Japanese source.
  - Beauty and barber files mask some fields at source (＊＊＊＊＊＊). The live
    CKAN records timed out, so the licence fields come from search.ckan.jp's
    harvest and web-archive copies: re-run `package_show` when BODIK answers.
- **MLIT 位置参照情報 and N02**: PDL 1.0, as in the Osaka brief.
- **MLIT N03** (the ward boundaries that decide which stations count): CC BY
  4.0, read 2026-09-24. Permitted for picking stations and anchoring labels.
  ⛔ **Never draw it**: showing its boundaries as a map may need GSI's
  approval under the Survey Act (`docs/data_sources.md`, Japan section).

## Privacy

MHLW's file carries **法人名, 法人住所 and 営業施設電話番号**. The BODIK
personal-services lists carry **開設者法人名（開設者氏名）** (an individual's name
for sole traders), **開設者法人住所** and phones. **Read only the trade name,
type and premises address** (plus MHLW's lat/lon). Run
`check_personal_exposure.py`.

## Region

`"region": "East Asia"`. Project to **UTM 52N (EPSG:32652)**.

## Still unknown

- ✅ Both licences read: BODIK (CC BY 4.0) and MHLW (PDL 1.0), each PERMITTED WITH CONDITIONS. MHLW has one minor commercial-use OPEN point.
- ⚠️ **Privacy**: per MHLW's FAQ, sole traders may enter 「個人名及び自宅住所」 as their 屋号 in their account. Whether that reaches `営業施設名称` is unchecked, so `check_personal_exposure.py` must look at trade names that are personal names.
- ✅ **The ~20% of restaurants with no published address**: disclosed on the page in the owner's approved wording (2026-09-24, above). Whether they cluster spatially stays unmeasured, and the wording says so.
- ✅ decided 2026-09-24 (owner): see the block at the top (菓子製造業 / そうざい製造業 count, in Retail).
- ✅ decided 2026-09-24 (owner): see the block at the top (city line only; Shinkansen out). ⚠️ Still open: N02's line list for Fukuoka.
- ⚠️ The Economic Census food control (the owner's chosen control).

```brief-checks
[
  {
    "id": "fukuoka-own-food-live",
    "claim": "Fukuoka City's own food-permit list (permits held since before 2021-06) is keyless and live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/5925a9fb-3326-4499-9acd-7b18c03d5e32/resource/70d22acf-2353-4bc1-b45d-f12d45da5216/download/r8.7.csv",
    "min_bytes": 400000
  },
  {
    "id": "fukuoka-mhlw-live",
    "claim": "MHLW's open-data file for Fukuoka City (40130) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40130_food_business_all.csv",
    "min_bytes": 5000000
  },
  {
    "id": "fukuoka-isj-chuo-live",
    "claim": "MLIT's block-level address file for Chuo ward (40133) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/40133-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "fukuoka-projected-crs",
    "claim": "Fukuoka projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 130.40,
    "expect": "EPSG:32652"
  }
]
```
