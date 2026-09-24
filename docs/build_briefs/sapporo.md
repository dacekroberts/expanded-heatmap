# Sapporo — build brief

**Step 0 measured 2026-09-24 (the overnight Japan run).** Run
`python scripts/brief_check.py sapporo` before writing any code. Coordinates:
the `address-join` skill, measured by `scripts/screen_japan_join.py sapporo`.

---

## The one-line summary

**A city-wide food-permit list (24,257 fixed premises, as of 2026-03-31)
joined to MLIT's address files: 84.5% at block level and 15.2% at town-chōme
— and on Sapporo's 条 grid a 条丁目 IS roughly one block, so 99.7% is placed at
near-block precision.** Personal services 5,993.

---

## Business leg — 札幌市内の食品営業許可施設一覧

| | |
|---|---|
| **File** | `https://ckan.pf-sapporo.jp/dataset/be44af14-f135-41b9-acca-08e215d8a540/resource/54618ac4-da90-493c-8a20-8df29be9d435/download/shokuhin260331.csv`, **5,708,754 B**, 25,163 rows, full list as of **2026-03-31** (dataset `sapporo_food_business_licences` on the city's CKAN; monthly new-permit CSVs beside it) |
| Columns | **区名**, 許可番号, 許可年月日, **業種名**, 申請者名, **屋号**, **施設所在地** (`北海道札幌市中央区南１６条西１０丁目３番２１号`) |

**Personal services** (`sapporo_environmental_hygiene_services`, 2026-07-31):
理容 / 美容 / クリーニング (+ coin laundries) — **5,993 premises**.

### Taxonomy — `業種名` (39 types)

| Bucket | Types |
|---|---|
| Food service | 飲食店営業 **19,828** · 喫茶店営業 80 |
| Food retail (permit types) | 魚介類販売業 516 · 食肉販売業 502 |
| Decide at build | 菓子製造業 1,853 · そうざい製造業 487 |
| Out | manufacturing (水産製品, 冷凍食品, 密封包装…), 食肉処理業, 食品の冷凍又は冷蔵業 |

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **10 wards** (01101–01110).

| Tier | Food (24,257) | Personal services (5,993) |
|---|---|---|
| Block | **84.5%** | **92.4%** |
| Town-chōme centroid | 15.2% | 7.5% |
| Unplaced | 0.3% | 0.1% |

**Sapporo's grid, and the rules its misses taught** (the retrospective
predicted it): digits before **条** as before 丁目 (`南十六条西十丁目` =
`南16条西10丁目`); an address that ENDS at 丁目, or runs straight into a
building name (`南5条西6丁目ニュー桂和ビル`), keeps its town; Shiroishi's
direction suffix (`本郷通8丁目南3-1`) joins the town only where MLIT has that
town. **Many addresses give no block number after the 条丁目** — hence the
15.2% chōme tier, which on this grid is ~100 m precision.

## 🚇 Rail — MLIT N02, commuter rail INCLUDED (owner, 2026-09-24)

Sapporo Municipal Subway (Namboku, Tōzai, Tōhō), the Sapporo streetcar, and
JR Hokkaido's Sapporo lines — all in N02. ⚠️ Stations are LineStrings —
centroid them. See `docs/commuter_rail_list.md`.

## Scope

**Sapporo City (10 wards)**; JR lines run on to Otaru, Ebetsu and the airport
(Chitose) — stations beyond the city fall outside; owner's call at build.

## ✅ Licences — READ 2026-09-24

- **MLIT 位置参照情報 — PERMITTED WITH CONDITIONS** (PDL 1.0) — the prescribed
  出典 and 「…を加工して作成」; never presented as MLIT's own.
- **Sapporo City permit data — PERMITTED WITH CONDITIONS.** The platform is
  the city's own (「札幌市が運営し」, `data.pf-sapporo.jp/tos/`, in force
  2024-06-01; use = acceptance, 第1条); it defers to each dataset's licence
  (第2条2): both `package_show` return **CC-BY-4.0**. **MUST DISPLAY** (no
  wording prescribed): credit 札幌市, the two dataset titles and URLs, the
  licence link, and that the data was processed — e.g.
  「札幌市『札幌市内の食品営業許可施設一覧』『札幌市内の環境衛生営業施設一覧』（札幌市ICT活用プラットフォーム、CC BY 4.0）を加工して作成」.
  **MUST NOT**: imply endorsement; use city logos (第4条); **call the pins
  operating businesses** — the dataset's own note says permits may differ from
  actual trading. **Fetch from `ckan.pf-sapporo.jp` only** — the city
  website's copies fall under its copyright page. ✅ **ACCEPTED (owner,
  2026-09-24)**: 第9条3 — uncapped compensation for damage from a prohibited
  act, triggered by the user's breach; the same class as Tokyo §6.
- **MLIT N02** — PDL 1.0.

## Privacy

**申請者名** (applicant) carries individuals' names; the registers carry
**開設者名 and 開設者住所** (the operator's own address) on 1,308 beauty rows.
Read only 屋号 / 施設名称, 業種名 and 施設所在地. Run `check_personal_exposure.py`.

## Region

`"region": "East Asia"`. Project to **UTM 54N (EPSG:32654)**.

## Still unknown

- ⚠️ 菓子製造業 / そうざい製造業 — counter shops or not.
- ⚠️ Stations outside the city.

```brief-checks
[
  {
    "id": "sapporo-food-list-live",
    "claim": "Sapporo City's food-permit list (2026-03-31, 25,163 rows) is keyless and live on the city's CKAN",
    "kind": "http_ok",
    "url": "https://ckan.pf-sapporo.jp/dataset/be44af14-f135-41b9-acca-08e215d8a540/resource/54618ac4-da90-493c-8a20-8df29be9d435/download/shokuhin260331.csv",
    "min_bytes": 3000000
  },
  {
    "id": "sapporo-catalogue-licence",
    "claim": "Sapporo's catalogue declares the food-permit dataset CC BY 4.0",
    "kind": "http_contains",
    "url": "https://ckan.pf-sapporo.jp/api/3/action/package_show?id=sapporo_food_business_licences",
    "present": ["cc-by"]
  },
  {
    "id": "sapporo-isj-chuo-live",
    "claim": "MLIT's block-level address file for Chuo ward (01101) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/01101-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "sapporo-projected-crs",
    "claim": "Sapporo projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 141.35,
    "expect": "EPSG:32654"
  }
]
```
