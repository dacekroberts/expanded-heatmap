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
