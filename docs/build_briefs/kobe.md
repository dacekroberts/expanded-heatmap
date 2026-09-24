# Kobe — build brief

**Step 0 measured 2026-09-24 (the overnight Japan run).** Run
`python scripts/brief_check.py kobe` before writing any code. Coordinates:
the `address-join` skill, measured by `scripts/screen_japan_join.py kobe`.

**✅ Decided by the owner, 2026-09-24, for every Japanese city:** (1) **the Shinkansen does not count**, since it is long-distance travel between cities; (2) **the city line only**: only stations inside the city get rings, matching the city-only permit list, with a per-line stub test at build (any urban line cut to a stub goes back to the owner); (3) **菓子製造業 and そうざい製造業 count**, in the Retail bucket (bakeries, confectioners and delis sell over a counter), with the factory and central-kitchen share measured from trade names before publishing. Open items below that ask these questions are answered.

---

## The one-line summary

**A city-wide food-permit list (24,761 fixed premises, as of 2026-03-31)
joined to MLIT's block-level address files at 96.5% (99.0% placed); the misses
are mountain addresses on Rokkō-san.** Personal services 4,993. ⚠️ The list
leaves out notification-only food businesses (届出), which the city's own page
says; MHLW's national open data is the route to them.

---

## Business leg — Kobe City's 生活衛生関係許可施設等の情報提供

| | |
|---|---|
| **File** | `https://www.city.kobe.lg.jp/documents/6359/20260407150739.csv`, **3,866,747 B**, 26,704 rows, all permitted facilities at the end of 2026-03 (page: `/a99427/kenko/health/hygiene/dataset.html`) |
| Columns | No, 許可番号, **業種情報公開名称**, **営業所所在地** (`東灘区魚崎北町１丁目６‐７` — ward + address; note the U+2010 hyphen), 営業所方書, **屋号**, 営業者名, 営業所TEL, 許可決定日, 許可満了日 (Reiwa dates), 申請区分 |
| Also | monthly new-permit CSVs; a stale 2021 full list (`r30531_all_.csv`) beside it — do not use |

**Personal services**: `r7_riyousho.csv`, `r7_biyousho.csv`, `r7_cleaning.csv`
(same folder, **tab-separated** despite the .csv name) — **4,993 premises**
(plus 21 storeless laundry pick-up services at `神戸市内一円`, not premises).

### Taxonomy — `業種情報公開名称` (43 types)

| Bucket | Types |
|---|---|
| Food service | 飲食店営業 **19,660** |
| Food retail (permit types) | 食肉販売業 688 · 魚介類販売業 497 |
| Decide at build | 菓子製造業 2,024 · そうざい製造業 611 |
| Out | 飲食店営業（集団給食）194 (institutional), vending machines, manufacturing, 食品の冷凍又は冷蔵業 |

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **9 wards** (28101 東灘, 28102 灘, 28105 兵庫, 28106 長田,
28107 須磨, 28108 垂水, 28109 北, 28110 中央, 28111 西).

| Tier | Food (24,761) | Personal services (4,993) |
|---|---|---|
| Block | **96.5%** | **97.3%** |
| Town-chōme / 大字 centroid | 2.6% | 2.2% |
| Unplaced | 1.0% | 0.5% |

*(Re-measured 2026-09-24 after Sendai's rule below: block was 95.7% / 96.3%.)*

**Rules from Kobe's misses**: hill addresses name a 字 inside the 大字
(`山田町上谷上字古々山`). **Sendai's rule placed a share of them at block
level**: MLIT's block file keeps the 字 in its `小字・通称名` column, so the
地番 is also keyed under 大字 + 字 + 小字. The rest take the 大字's
town-chōme centroid. The unplaced are **Rokkō-san** (六甲山町北六甲 / 南六甲) and
`新港町1丁目` (reclaimed land) — far from any station either way.

## 🚇 Rail — MLIT N02, commuter rail INCLUDED (owner, 2026-09-24)

Kobe Municipal Subway, Port Liner, Rokkō Liner, JR West, Hankyu, Hanshin,
Sanyo, Kobe Electric — all in N02. ⚠️ Stations are LineStrings — centroid
them. ⚠️ Open: the Shinkansen (Shin-Kobe). See `docs/commuter_rail_list.md`.

## Scope

**Kobe City (9 wards)**. The JR / Hankyu / Hanshin corridor runs on to
Ashiya and Nishinomiya — the stations beyond the city line fall outside;
owner's call at build.

## ✅ Licences — READ 2026-09-24

- **MLIT 位置参照情報 — PERMITTED WITH CONDITIONS** (PDL 1.0) — the prescribed
  出典 and 「…を加工して作成」; never presented as MLIT's own.
- **Kobe City permit data — PERMITTED WITH CONDITIONS, no owner decision.**
  **CC BY 2.1 JP governs** (the city page's badge on each CSV; the portal
  policy's 「表示」 links 2.1 JP and adds 「必ず神戸市の著作物あるいはデータを使用した旨を記載してください」);
  Kobe's website terms (Government Standard Terms 2.0: 「…商用利用も可能です。」)
  also plausibly apply and do not conflict. **MUST DISPLAY**:
  `出典：「生活衛生関係許可施設等の情報提供」（神戸市）（https://www.city.kobe.lg.jp/a99427/kenko/health/hygiene/dataset.html）`,
  `…を加工して作成`, the CC BY 2.1 JP link, and © City of Kobe kept intact.
  **MUST NOT**: look as if the city made it (「あたかも本市が作成したかのような態様で…」);
  city logos; **claim the pins are businesses currently open** (the page warns
  closed ones may remain). **If the city asks, remove the credit** (2.1 JP
  art. 5). **No indemnity or cost clause.** CC BY 2.1 JP bars sublicensing —
  **already covered**: the repository's `LICENSE` (lines 27–59) limits the MIT
  grant to the project's own code and says nothing in it permits
  redistributing any third party's data.
- **MLIT N02** — PDL 1.0.

## Privacy

**営業者名 carries individuals' names.** Read only 屋号, 業種情報公開名称 and
営業所所在地. Run `check_personal_exposure.py`.

## Region

`"region": "East Asia"`. Project to **UTM 53N (EPSG:32653)**.

## Still unknown

- ⚠️ Notification-only businesses (届出) are missing — MHLW's national open data.
- ✅ decided 2026-09-24 (owner): see the block at the top (菓子製造業 / そうざい製造業 count, in Retail).
- ✅ decided 2026-09-24 (owner): see the block at the top (city line only; Shinkansen out).

```brief-checks
[
  {
    "id": "kobe-food-list-live",
    "claim": "Kobe City's food-permit list (end of 2026-03, 26,704 rows) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kobe.lg.jp/documents/6359/20260407150739.csv",
    "min_bytes": 2000000
  },
  {
    "id": "kobe-beauty-list-live",
    "claim": "Kobe City's beauty-salon list is keyless and live - personal services",
    "kind": "http_ok",
    "url": "https://www.city.kobe.lg.jp/documents/6359/r7_biyousho.csv",
    "min_bytes": 200000
  },
  {
    "id": "kobe-isj-chuo-live",
    "claim": "MLIT's block-level address file for Chuo ward (28110) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28110-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "kobe-projected-crs",
    "claim": "Kobe projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.19,
    "expect": "EPSG:32653"
  }
]
```
