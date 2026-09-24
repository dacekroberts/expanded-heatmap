# Sendai — build brief

**Step 0 measured 2026-09-24 (after the overnight Japan run; openpyxl approved
by the owner, question 11).** Run `python scripts/brief_check.py sendai` before
writing any code. Coordinates: the `address-join` skill, measured by
`scripts/screen_japan_join.py sendai` (and `sendai-life`).

---

## The one-line summary

**A city-wide food-permit list (12,627 permanent fixed premises, as of
2026-03-31) joined to MLIT's block-level address files at 95.1%, with nothing
unplaced, and confirmed by GSI's address search at a median 34 m (150 of 150
within 250 m).** Personal services from the city's 生活衛生 lists (3,378). The
city publishes XLSX inside ZIPs, not CSV. That is the only new mechanics.
**🚫 But the lists are NOT open data**: the city's default terms bar reuse
without permission, so Sendai waits at the end of the Japanese cities for the
city's answer (owner, 2026-09-24).

---

## Business leg — Sendai City's 営業許可施設一覧 (the city's own format)

| | |
|---|---|
| **File** | `https://www.city.sendai.jp/sekatsuese-shokuhin/kyokalist/documents/r7shokuhinichiran.zip`: **1,765,521 B**, one XLSX. All facilities holding a permit at the end of FY2025 (2026-03-31). Page: `/sekatsuese-shokuhin/kyokalist/joho.html`, updated annually in late April, with monthly new-permit ZIPs beside it (newest `260910_shinkisyokuhinichiran.zip`) |
| Shape | One **summary sheet** (`仙台市`) with counts per office, then one sheet per ward office (青葉, 宮城野, 若林, 太白, 泉) plus `食品監視センター` (the wholesale market). **14,724 rows. This matches the summary sheet's own 合計 exactly** |
| Columns | No, 営業者氏名, 代表者名, 郵便番号, **営業所住所** (`青葉区中江一丁目６－３０`: ward + address, kanji chōme, full-width digits), **営業所ビル名**, 営業所電話番号, **屋号** (trade name), **営業種類**, 許可決定日, 初回許可日, 許可満了日, 指令番号 |
| ⚠️ Not premises | **1,992 rows at `仙台市内一円`** ("anywhere in the city"): vehicles 732, and festival and event stalls (仮設, 臨時). A further **105 temporary permits** (仮設, 期間申請, 臨時) carry a real venue address. Exclude both at build |
| ⚠️ One row per PERMIT | A premises holding two permits appears twice (`しんせいあん` × 2): 12,732 fixed rows are **11,446 distinct (address, trade name)** pairs. Deduplicate at build, as for the other Japanese cities |

**Personal services**: `https://www.city.sendai.jp/sekatsuese/facilitylist/documents/260331.zip`
(page `/sekatsuese/facilitylist/list.html`, as of 2026-03-31, with monthly XLSX
additions). It holds nine workbooks; three are this project's:
`4_理容所` **801**, `5_美容所` **2,104** (一般 1,848, まつエク専門店 256), and
`6_クリーニング所` **474** (取次所 387, 一般 63, 指定洗濯物取扱い 24). That is
**3,378 fixed premises**. The other six (inns, theatres, bathhouses, hot
springs, large buildings, minpaku) are out of scope. Columns: 施設名称,
**施設所在地**, 施設方書, then operator columns.

### Taxonomy — `営業種類`, first cut (permanent fixed premises)

| Bucket | Types |
|---|---|
| Food service | 飲食店営業 **10,494** · 喫茶店営業 50 (a pre-2021 permit type still running to expiry) |
| Food retail (permit types) | 魚介類販売業 265 · 食肉販売業 214 |
| Decide at build (`premises-taxonomy`) | 菓子製造業 989 · そうざい製造業 232: manufacturing permits that are often counter shops (bakeries, delis) |
| Out | 食肉処理業, 漬物 / 麺類 / 水産製品 / 豆腐 and other manufacturing, 調理機能を有する自動販売機 (vending machines), 食品の小分け業, 酒類製造業 |

**No general retail.** That is Japan's ceiling, and the page states it.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **5 wards** (04101 青葉, 04102 宮城野, 04103 若林, 04104 太白,
04105 泉): block level `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip`,
town-chōme `.../19.0b/<code>-19.0b.zip`. Keyed (ward, town, block).

| Tier | Food (12,627 permanent) | Personal services (3,378) |
|---|---|---|
| Block | **95.1%** | **96.5%** |
| Town-chōme / 大字 centroid | 4.9% | 3.3% |
| Unplaced | 0.0% | 0.1% |

**Independent check.** Sendai publishes no coordinates, so the check is GSI's
keyless address search on a seeded sample of 150 block hits: **150 answered,
median 34 m, 143 within 100 m, all within 250 m (max 232 m).**

**Rule from Sendai's misses** (the Minato control re-run after it holds at 99.8%):
the city is ringed by **字 addresses** (`福室字境４番`, `松森字中道３４`), and
**MLIT's block file keeps the 字 in its `小字・通称名` column** (21,768 of 47,466
rows here). Keying the 地番 under 大字 + 字 + 小字 moved Sendai food from
**81.3% to 95.1%** block, and it lifted **Kobe** as well (95.7% to 96.5%). What
is left at the chōme tier: 349 字 addresses whose 小字 is not in the file, and
187 blocks missing from newer land readjustments (大野田, 富沢西, 田子西, and the
post-tsunami 荒井 and 蒲生).

---

## 🚇 Rail — MLIT N02, commuter rail INCLUDED (owner, 2026-09-24)

`https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip`. Per general
knowledge (not yet read from N02), it should cover the Sendai Subway (Namboku,
Tōzai) and JR East (Tōhoku Main Line, Senseki, Senzan, Jōban), plus the Sendai
Airport line, which runs mostly outside the city. ⚠️ Stations are LineStrings,
so centroid them. ⚠️ Open: intercity-only services (the Tōhoku Shinkansen). See
`docs/commuter_rail_list.md`.

## Scope

**Sendai City (the 5 wards).** The lists are city-wide. JR lines run on to
Natori, Tagajō and Shiogama, and the airport line is almost entirely in Natori
and Iwanuma. Check which stations fall outside at build; the scope is the
owner's call.

## 🚫 Licences — READ 2026-09-24: the city's lists need PERMISSION

⏸ **Sendai goes to the END of the Japanese cities (owner, 2026-09-24).** The
terms are clear, so a written request has been drafted for the owner to send.
It stays unbuilt until the city answers.

- **Sendai City permit lists: NOT PERMITTED without permission.** Sendai has
  not adopted CC BY 4.0 or 政府標準利用規約 site-wide, which is where it differs
  from Osaka, Kobe and Sapporo. Its copyright page
  (`/sesakukoho/chosakuken/index.html`) is the default:
  「「私的使用のための複製」や「引用」など著作権法上認められた場合を除き、無断で複製・転用することはできません。」
  The override is 「ただし、…各ページに特段の定めがある場合には、その取り扱いが優先されます。」
  **Neither list page has one.** Files the city releases as open data carry a
  `class="openDataFile"` link with a CC BY 4.0 badge, as on the statistics
  pages, and these links carry neither. **Neither list is in the city's
  catalogue** (5,907 rows: 5,885 CC BY 4.0, 22 not copyrighted) **or on
  Miyagi's joint portal.** The files carry no notice of their own either:
  document properties, title rows and every cell were checked, and the only
  footer is page numbers. The city's open-data policy names 食品等営業許可・届出一覧
  as a recommended dataset but has not released it, probably because the lists
  carry 営業者氏名 and its policy excludes 個人情報.
  - **The reading that would permit it**: a ledger of permits is facts, and
    the project republishes extracted facts, not files; the city's own policy
    says 「著作物とならない公共データについては、…二次利用の制限はない」.
    **Not relied on**: whether the lists are 著作物 is for the city or a court
    to decide, and the skill's rule is never to resolve that in this project's
    favour.
  - **Deep links are gated by request**: 「その他のページへリンクを希望される場合は、それぞれの担当課へお問い合わせください。」
    The drafted request asks this too.
  - **No cost or indemnity clause.** The disclaimer limits the city's
    liability only.
  - **The way through**: written permission from 健康福祉局生活衛生課
    (`fuk005530@city.sendai.jp`, listed on the city's organisation page;
    食品衛生係 022-214-8205, 生活衛生係 022-214-8206). A formal request is drafted
    for the owner to send. Nothing sent yet.
- **MLIT 位置参照情報: PERMITTED WITH CONDITIONS** (PDL 1.0), as in the Osaka
  brief. **MUST DISPLAY**:
  `出典：位置参照情報ダウンロードサービス（国土交通省）（https://nlftp.mlit.go.jp/isj/）`
  and `…を加工して作成`. **MUST NOT** present placements as MLIT's own.
- **MLIT N02**: PDL 1.0; `「国土数値情報（鉄道データ）」（国土交通省）をもとに作成`.

## Privacy

The food list carries **営業者氏名 and 代表者名 (people's names), 郵便番号 and
営業所電話番号**. The 生活衛生 lists carry **開設者名, 法人代表者肩書・氏名, 開設者住所
(an operator's home address), 開設者方書 and 開設者TEL**, or 営業者名. **Read only
屋号 / 施設名称, 営業種類 / 種別, and 営業所住所 / 施設所在地 (+ ビル名 / 方書)**,
never an operator column. Run `check_personal_exposure.py`.

## Region

`"region": "East Asia"`. Project to **UTM 54N (EPSG:32654)**.

## Still unknown

- 🚫 **The city's permission**: request drafted; the owner sends it. Sendai waits at the end of the Japanese cities until the city answers.
- ⚠️ 菓子製造業 / そうざい製造業: which are counter shops.
- ⚠️ Scope beyond the city line; the Shinkansen; N02's line list for Sendai (general knowledge above, not read).
- ⚠️ A like-for-like food control (the Economic Census per ward), as for Tokyo.

```brief-checks
[
  {
    "id": "sendai-food-list-live",
    "claim": "Sendai City's food-permit list (FY2025 year-end, one XLSX in a ZIP) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.sendai.jp/sekatsuese-shokuhin/kyokalist/documents/r7shokuhinichiran.zip",
    "min_bytes": 1000000
  },
  {
    "id": "sendai-life-list-live",
    "claim": "Sendai City's 生活衛生 facilities ZIP (barber, beauty, laundry among nine workbooks) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.sendai.jp/sekatsuese/facilitylist/documents/260331.zip",
    "min_bytes": 300000
  },
  {
    "id": "sendai-isj-aoba-live",
    "claim": "MLIT's block-level address file for Aoba ward (04101) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/04101-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "sendai-projected-crs",
    "claim": "Sendai projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.87,
    "expect": "EPSG:32654"
  }
]
```
