# Osaka — build brief

**Step 0 measured 2026-09-24 (the overnight Japan run).** Run
`python scripts/brief_check.py osaka` before writing any code. Coordinates:
the `address-join` skill, measured by `scripts/screen_japan_join.py osaka`.

**✅ Decided by the owner, 2026-09-24, for every Japanese city:** (1) **the Shinkansen does not count**, since it is long-distance travel between cities; (2) **the city line only**: only stations inside the city get rings, matching the city-only permit list, with a per-line stub test at build (any urban line cut to a stub goes back to the owner); (3) **菓子製造業 and そうざい製造業 count**, in the Retail bucket (bakeries, confectioners and delis sell over a counter), with the factory and central-kitchen share measured from trade names before publishing. Open items below that ask these questions are answered.

---

## The one-line summary

**One city-wide food-permit list (61,752 fixed premises, as of 2026-06-30)
joined to MLIT's block-level address files at 99.1% — and independently
confirmed against Osaka's own coordinates at a median 38 m.** Personal
services from the city's barber, beauty and laundry registers (15,775). The
strongest Japanese city measured.

⚠️ **The list holds about 67–72% of the restaurant permits Osaka reports to
national statistics, and the evidence says the COUNT is inflated, not the
list short** (probed 2026-09-24). The list has 54,289 飲食店営業 rows, vehicles
included, against **81,418** in MHLW's 衛生行政報告例 at FY2024-end. The same
measure puts Kobe, Sapporo, Fukuoka, Kyoto, Hiroshima and Sendai at 93–101%.

- **The gap is steady and even.** Every quarterly file the city has published
  since 2023 reads 69–76% of the matching year-end count. All 24 wards are
  present in each, and the page states no exclusion or opt-out.
- **Not the cause**: temporary and event permits. Events file a 臨時出店届
  (a notification, no permit), and stalls hold ordinary permits and are in
  the list.
- **The official old-law count exceeds what can exist.** No old-law permit
  could be issued after 2021-05-31, and the city's own mid-2021 old-law
  register has 62,451 restaurant permits.
  - Assuming no closures at all, at most **25,620** could still be valid at
    2025-03-31. Osaka reported **37,779**, 12,159 over that ceiling.
  - The same held in FY2022 and FY2023. FY2023's count also fell by 21,595
    where at most 10,301 could expire, which looks like a clean-up.
- **A third count agrees.** Against the 2021 Economic Census's
  accommodation-and-food establishments by ward, the list is even across all
  five health offices, while the official count is not. The eastern office
  (東部) holds 61% of the gap and 45% of the count.
- **Best-supported reading, not confirmed by the city**: Osaka's national
  count includes expired or closed permits that each health office clears to
  a different degree. The list, of permits valid on its date, is the more
  accurate of the two. That holds for the **old-law two-thirds** of the gap.
  The new-law third (about 9,000 restaurants) is undetermined; see below.
- **Partly settled (e-Stat flow tables, probed 2026-09-24): the permit
  numbers no list shows are real permits, and the national count still holds
  them.** Each year 20–32% of the permit-number sequence never appears in any
  year-end file.
  - **Not withdrawn numbers.** Osaka's reported issued count matches each
    year's number sequence to within 3%, FY2020–FY2024, all permit types.
    (Kobe's sequences run 2–7% over its count.)
  - **Not closed in the count either.** Osaka's reported closures match the
    permits visibly leaving the list (FY2024: 2,674 against 2,565).
  - **So the restaurant gap at FY2024-end (24,976) has two parts.**
    - **Old law, 16,260: almost all dead.** The list's 21,519 already sits
      below the no-closure ceiling of 25,620.
    - **New law, about 8,700–9,300 restaurants: undetermined.** Osaka counts
      them as live and has never published them. This part grew from 2,837
      (all types, FY2022) to 5,159 to 9,497.
  - **What the new-law part might be.**
    - **About a third are runs** of 5–38 consecutive numbers. That is the
      shape of the only short-lived permits the lists show: department-store
      event stalls at Abeno and Umeda, valid for days to weeks, which expire
      with no closure filed.
    - **The rest are scattered**, and they have risen from 15% of FY2020's
      numbers to 32% of FY2024's. Only the city can say what they are.
      Contacting it is the owner's last resort.
  - **Controls.**
    - Kobe lists 88–99% of each year's permits.
    - Sapporo lists 56–64% but books the rest as closures, so its list still
      equals its count.
    - Osaka kept 41% of its FY2020 old-law permits at FY2024. Kobe, Kyoto,
      Sapporo, Fukuoka and Yokohama kept 30–34%.
  - **Tables**: e-Stat 第1表-2 and 第3表-2 (FY2023–24), 第E1表 and 第E3表
    (FY2020–22), and 第2表 and 第4表. The per-city flow tables cover all permit
    types combined; restaurants are 87% of Osaka's new-law count. Credit:
    「衛生行政報告例」（厚生労働省）を加工して作成.
- **What the page must say** (✅ **revised wording approved by the owner,
  2026-09-24**, after the flow probe): "Osaka City's published list holds
  about 70% of the restaurant permits Osaka reports to national statistics.
  Most of the difference appears to be expired permits still counted
  nationally; the rest, about a tenth of the count, are permits the city
  counts but does not list, some of them short-lived event permits. The city
  has not confirmed either." The 2,149 permits with no fixed address are not
  mapped.
  - It replaces the first draft, whose "not to restaurants missing from the
    list" became stronger than the evidence once the new-law part (about 11%
    of the count) proved undetermined.
- **Placement is unaffected**, and the build is not blocked.

---

## Business leg — Osaka City's food-permit list (the city's own format)

| | |
|---|---|
| **File** | `https://www.city.osaka.lg.jp/contents/wdu280/260630zenku.csv` (linked from `/kenko/page/0000575579.html`), **10,455,741 B**, 63,902 rows. As of **2026-06-30** |
| Columns | 都道府県コード, No, 都道府県, 市区町村 (大阪市), **屋号** (trade name), **業種分類**, **営業所所在地** (`北区池田町１番２３号` — ward + address in one string), 経度, 緯度, 営業者名, 許可満了日, 指令番号, 申請区分 |
| ⚠️ **Coordinates are MISLABELLED** | the column headed **経度 holds latitudes (34.7)** and 緯度 longitudes (135.5) — 96.6% filled. Swap before use; the join does not need them |
| Mobile | 2,150 rows are 市内一円 / vehicles — not premises |
| ⚠️ Stale twin | the portal's `data-00000382` copy is **2021-12-31** — use the city page's file |

**Personal services** (the city's own pages, 2026-03-31): 理容所
`/kenko/cmsfiles/contents/0000431/431136/ri20260331.csv`, 美容所 `…/bi20260331.csv`,
クリーニング所 `/kenko/cmsfiles/contents/0000552/552712/cleaning20260331.csv` —
**15,775 premises**.

### Taxonomy — `業種分類`, first cut (38 types)

| Bucket | Types (fixed premises) |
|---|---|
| Food service | 飲食店営業 **52,140** |
| Food retail (permit types) | 食肉販売業 1,682 · 魚介類販売業 1,457 |
| Decide at build (`premises-taxonomy`) | 菓子製造業 3,580 · そうざい製造業 1,209 — manufacturing permits that are often counter shops (bakeries, delis) |
| Out | 食肉処理業, 麺類 / 水産製品 / 漬物 / 添加物 manufacturing, vending machines, 食品の小分け業 |

**No general retail** — Japan's ceiling; stated on the page.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files per ward (codes 27102–27128, **24 wards**): block level
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip`, town-chōme
`.../19.0b/<code>-19.0b.zip`. Keyed (ward, town, block).

| Tier | Food (61,752) | Personal services (15,775) |
|---|---|---|
| Block | **99.1%** | **99.4%** |
| Town-chōme centroid | 0.9% | 0.5% |
| Unplaced | 0.0% | 0.1% |

**Independent check**: against Osaka's own (swapped) coordinates, the block
point sits a **median 38 m** away, **98.6% within 250 m** (61,172 rows).
**Rules from Osaka's misses** (Minato control re-run after each): **kanji
variants** — `曽根崎新地` against MLIT's `曾根崎新地` was **1,807 permits**
(Kitashinchi) on its own; `靭`/`靱`, `ヶ`/`ケ`. The unplaced are underground
malls (梅田地下街, アベノ地下街) — premises with no block number.

---

## 🚇 Rail — MLIT N02, commuter rail INCLUDED (owner, 2026-09-24)

`https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip`: Osaka Metro,
JR West, and the private railways (Hankyu, Hanshin, Keihan, Kintetsu, Nankai)
are all in it. ⚠️ Stations are LineStrings — centroid them. ⚠️ Open: intercity-only
services (Shinkansen). See `docs/commuter_rail_list.md`.

**✅ Stub test, measured 2026-09-24** (`pipeline/countries/japan.py` `stub_test()`: N02 stations, Shinkansen excluded, against the city's N03 ward polygons): **PASSES.** Osaka Metro keeps 80–100% of each line's stations (Midōsuji 16 of 20, Tanimachi 23 of 26, Chūō 12 of 14; Sakaisuji, Yotsubashi, Sennichimae and the New Tram 100%). The Hankai tram keeps 17 of 32 (it runs into Sakai): half a line, not a stub. JR and the private railways are cut at the line, as the owner's scope intends (Hankyu Kōbe 5 of 17, Keihan 8 of 41, the Loop Line 19 of 19).

## Scope

**Osaka City (the 24 wards)** — the list is city-wide. Osaka Metro reaches
neighbouring cities (Sakai, Higashiōsaka, Moriguchi…) and the private
railways run far beyond — check which stations fall outside at build; the
Oslo *kommune only* precedent or a regional scope is the owner's call.

## ✅ Licences — READ 2026-09-24

- **MLIT 位置参照情報 — PERMITTED WITH CONDITIONS** (PDL 1.0). **MUST
  DISPLAY**: `出典：位置参照情報ダウンロードサービス（国土交通省）（https://nlftp.mlit.go.jp/isj/）`
  and `…を加工して作成`; **MUST NOT** present placements as MLIT's own.
- **Osaka City permit data — PERMITTED WITH CONDITIONS.** The city's
  著作権・免責 page (`/main/site_policy/0000000124.html`, Government Standard
  Terms 2.0, usable equally under CC BY 4.0): 「複製、公衆送信、翻訳・変形等の翻案等、自由に利用できます」,
  commercial use allowed; each of the three source pages says
  「CC-BY4.0で提供いたします。」 **MUST DISPLAY** (examples, not fixed wording):
  `「食品営業許可施設一覧」（大阪市）（https://www.city.osaka.lg.jp/kenko/page/0000575579.html）を加工して作成`,
  likewise for pages 0000431136 and 0000552712. **MUST NOT**: present the map as
  the city's own (「あたかも大阪市が作成したかのような態様で」); city logos. No cost
  clause. ✅ **ACCEPTED (owner, 2026-09-24)**: the current food CSV's licence
  rests on the CC-BY notice on its own page. The portal's food record points to
  a dead page and a 2021 file, and the terms' appendix bars reuse of attachments
  that show no licence. The notice sits on the page that links the file, so it
  covers it.
- **MLIT N02** — PDL 1.0; `「国土数値情報（鉄道データ）」（国土交通省）をもとに作成`.
- **MLIT N03** (the ward boundaries that decide which stations count): CC BY
  4.0, read 2026-09-24. Permitted for picking stations and anchoring labels.
  ⛔ **Never draw it**: showing its boundaries as a map may need GSI's
  approval under the Survey Act (`docs/data_sources.md`, Japan section).

## Privacy

The list carries **営業者名 — individuals' names** (e.g. a café's owner) and
the barber / beauty lists an operator-name column. **Read only 屋号,
業種分類 and 営業所所在地**; never 営業者名. Run `check_personal_exposure.py`.

## Region

`"region": "East Asia"`. Project to **UTM 53N (EPSG:32653)**.

## Still unknown

- ✅ decided 2026-09-24 (owner): see the block at the top (菓子製造業 / そうざい製造業 count, in Retail).
- ✅ decided 2026-09-24 (owner): see the block at the top (city line only; Shinkansen out).
- ⚠️ The like-for-like food control's figures: the Economic Census per ward (source decided by the owner, 2026-09-24).

```brief-checks
[
  {
    "id": "osaka-food-list-live",
    "claim": "Osaka City's food-permit list (2026-06-30, 63,902 rows) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.osaka.lg.jp/contents/wdu280/260630zenku.csv",
    "min_bytes": 5000000
  },
  {
    "id": "osaka-beauty-list-live",
    "claim": "Osaka City's beauty-salon list is keyless and live - personal services",
    "kind": "http_ok",
    "url": "https://www.city.osaka.lg.jp/kenko/cmsfiles/contents/0000431/431136/bi20260331.csv",
    "min_bytes": 300000
  },
  {
    "id": "osaka-isj-kita-live",
    "claim": "MLIT's block-level address file for Kita ward (27127) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27127-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "osaka-projected-crs",
    "claim": "Osaka projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.5,
    "expect": "EPSG:32653"
  }
]
```
