# Tokyo — build brief

**Step 0 measured 2026-09-24 (the overnight Japan run).** Run
`python scripts/brief_check.py tokyo` before writing any code. The coordinate
method is the `address-join` skill; the measurement is
`scripts/screen_japan_join.py`. **This brief is deliberately PARTIAL on
coverage** — see *Scope*, which is the owner's call before a build.

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
or Minato's own: **11 wards, 14,887 premises** — Chiyoda, Minato, Bunkyō,
Taitō, Shinagawa, Ōta, Shibuya, Toshima, Arakawa, Katsushika (+ Meguro on
BODIK, deferred). Beauty 10,265 · barber 1,899 · laundry 2,723.

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
| Personal services, 14,887 | 98.8–99.8% | | |

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
reading only 営業所所在地, 業種 and 屋号, never its operator columns. The pass
was running when this was written.

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
- **MLIT N02** — PDL 1.0, read 2026-09-21; attribution
  `「国土数値情報（鉄道データ）」（国土交通省）をもとに作成`.

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
- ⚠️ Shinkansen / limited-express-only lines; which N02 lines are "commuter".
- ⚠️ Meguro's registers (BODIK) and Nakano's food file (a vendor map host) — deferred.

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
