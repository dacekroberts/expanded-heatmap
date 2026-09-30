# Yokohama — build brief

**Step 0 measured 2026-09-24 (the open-gap re-probe) and 2026-09-29 (the Band
C audit; this brief).** Band B (owner, 2026-09-29): **personal services
only**, the first page not built on food (the reduced-bucket bar's amended
rule 1). **The page states that no food register is published.** Run
`python scripts/brief_check.py yokohama` before writing code, and follow the
`japan-city` skill: this is a seventh Japanese city on the shared modules.

| | |
|---|---|
| Rail | MLIT N02 on Japan's standing rule (JR, subway and private lines, no Shinkansen): **138 stations inside the city**. City subway 39, JR East 34, Keikyu 24, Tokyu 21, Sotetsu 21, Kanazawa Seaside Line 14 (an automated guideway, drawn as Kobe's Port Liner), Minatomirai 6 |
| Spacing | 836 m median gap → **standard rings 0.1 / 0.2 / 0.3 / 0.6 mi** |
| Storefronts | **7,896 premises** (register of 2026-04-01, all 18 wards): beauty 5,091, barbers 1,512, cleaning 1,293. **Not the 17,408 recorded in 2026-09**, whose source could not be traced |
| Placed | **97.8–98.7% at block level**, about 100% with town-chōme (the shared `japan_register` join, MLIT 位置参照情報 for wards 14101–14118) |
| In the rings | **82.1% within 0.6 mi**, 61.8% within 0.3 mi |
| CRS | EPSG:32654 (UTM 54N) |
| Region | `"East Asia"`; the city, 438 km² in MLIT N03 |

## Business leg — the city's 生活衛生 registers

`data/yokohama/raw/life/2026040{1}*.zip`, one CSV per ward inside each zip:

| Zip | Type | Rows |
|---|---|---|
| `20260401biyou.zip` | 美容所 (beauty) | 5,091 |
| `20260401riyou.zip` | 理容所 (barber) | 1,512 |
| `20260401cleaning.zip` | クリーニング所 (cleaning) | 1,293 |

The other six zips (bathhouses, inns, entertainment venues, pools…) are not
personal-services storefronts, so keep them out. Check `bill` and `shinki`
at build.

- ⚠️ **`city_rows` reads zipped `.xlsx` only.** These zips hold CSVs, so
  extract the members first (or teach `city_rows` a CSV-in-zip case, a
  shared-code change to test against the six built cities).
- **Columns**: `台帳番号, 許可番号, 申請者法人名称, 申請者役職, 申請者氏名,
  施設所在地, 施設名称, 施設名称２, 施設電話番号, 業種, 詳細業種, 許可等年月日`.
  **Never load `申請者氏名` or `申請者役職`** (a person), nor
  `施設電話番号`. Display `施設名称`. Run the Japanese operator-name rule
  (`same_person`) against the operator column before display, and
  `check_personal_exposure.py`.
- **No closure field**: the register's date (2026-04-01) is the clock, one
  year old. The one-clock rule's snapshot case.
- Unplaced rows are addresses like `横浜市都筑区内` (no street): mobile, and
  already dropped by `permits_from_rows`.

## Licences

| Source | Status |
|---|---|
| The city's 生活衛生 registers | **CC BY declared** (the 2026-09-24 screen). Read the version and wording at build |
| MLIT N02, N03, 位置参照情報 | Read for the Japanese builds (PDL 1.0 and MLIT terms): `docs/data_sources/japan.md` |

```brief-checks
[
  {
    "id": "yokohama-isj-block-file",
    "claim": "MLIT serves the block-level address file for Naka ward (14104), the shape the join uses for all 18 wards",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14104-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "yokohama-utm-54",
    "claim": "Yokohama (139.64 E) is in UTM zone 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.64,
    "expect": "EPSG:32654"
  }
]
```
