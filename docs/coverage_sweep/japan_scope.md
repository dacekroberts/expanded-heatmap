# Japan wave 2: scoping (staging, 2026-10-02)

This is scoping, not screening. No tracked file was edited. Scripts and their
outputs are in this folder:

| File | What it is |
|---|---|
| `stations_by_muni.py` → `muni_stations.csv`, `muni_lines.csv` | Station groups per municipality, nationwide |
| `universe.py` → `universe.csv` | The candidate universe |
| `fetch_mhlw.py`, `mhlw_count.py`, `mhlw_table.py` → `universe_mhlw.csv` | MHLW permit counts per candidate |
| `bodik_city.py` → `bodik_run1.log`, `bodik_run2.log` | BODIK title searches |

## 1. Universe: 114 uncovered municipalities

The universe takes in four kinds of municipality:

- **Designated and core cities.** The list is MHLW's 衛生行政報告例 FY2024, table 3-2's 指定都市 and 中核市 sections (`data/japan/raw/estat_eisei_r6_food_5-3-2_newlaw_flow_by_city.csv`). That gives 20 + 62. Removing the cities already covered leaves **7 designated and 53 core**.
- **Municipalities of 200,000 or more.** These are the 2020 census figures, written down by hand, so the list is unverified. It adds **30**, 5 of them also in the next group. A cross-check against the 2021 Economic Census restaurant counts turned up no 200k-class city missing from the list.
- **Every municipality with a subway, tram, monorail, AGT or Linimo station** (N02-25 × N03), Tokyo's wards excluded. This adds **24 that are in no other group**. The class-21 rows of N02 that are really subways (Osaka Metro, Kita-Osaka Kyūkō, Kintetsu) are counted as subway, not tram.

**Rail inside each city.** Stations come from N02-25 (Shinkansen dropped) and are cut at the 2025-01-01 N03 line, then collapsed on `N02_005g`. Funiculars are counted separately and left out.

- Calibration: Hiroshima 124 (built: 124), Kitakyūshū 58 (its brief: 53; the brief excludes Heisei Chikuhō), Okayama 49.
- All 47 prefecture N03 zips are now in `data/japan/raw/`, in the shared cache that `japan.py` reads. 30 were new, about 210 MB from MLIT.
- The job's measured peak was 0.23 GB.
- Spread among the 114: 29 have 20 or more groups, 47 have 15 or more, and 37 have fewer than 10.

## 2. The business leg: MHLW's file splits the cities three ways

Of the 60 uncovered designated and core cities, MHLW's file (open 飲食店営業 permits ÷ e-Stat's in-force count) falls into these groups:

- **The city enters every permit (≥ 0.85 of the in-force count): 16.**
  - 11 of the 16 clear 70% addressed: Chiba, Sasebo, Kurume, Shimonoseki, Nara, Tottori, Morioka, Yamagata, Yao, Mito, Takatsuki.
  - The other 5 do not: Shizuoka 60%, Fukuyama 67%, Kure 68.5%, Kōfu 63%, Matsumoto 35%.
- **Partial (0.25 to 0.85): 6.** Funabashi, Miyazaki, Nagano, Maebashi, Takasaki, Kashiwa.
- **Opt-in online filings only (under 0.10): 35.** Their food leg depends wholly on the city's own list.
- **Notifications only, no permits: 3.** Hamamatsu, Higashiōsaka, Hachinohe.

The counter is calibrated against the batch briefs: Kitakyūshū 86.2% (brief 86.2%), Okayama 73.9% (73.9%), Kōchi 53.9% (53.9%).

**Municipalities without their own health centre sit in their prefecture's file** (`<pref>000`), and a row can be placed in a municipality only by its address:

- A blank address cannot be attributed to any municipality.
- Prefecture-wide address shares are under the bar where the files are large: Chiba Prefecture 62.7% (19,649 open permits), Shizuoka Prefecture 66.8% (25,103).
- Elsewhere the prefecture files are opt-in and thin. Saitama, Tokyo, Kanagawa, Aichi, Ōsaka and Hyōgo all show under 0.25 addressed restaurants per Economic Census establishment.
- Tokushima Prefecture is 12.7% addressed and Saga Prefecture 29.9%.

**City lists.** I looked on BODIK and ran a web search, about 2 minutes per city, top tier only. I opened no files and counted no rows.

## 3. Ranking

### Likely A: rail passes, food placeable, and a city list seen

| City | Station groups inside (by class) | MHLW open restaurant permits (share of in-force; share with an address) | City lists seen |
|---|---|---|---|
| **Kawasaki** (designated) | 53: JR 25, private 31 (Odakyū 11, Tōkyū 10, Keikyū 8, Keiō 2) | 1,200 (10%; 79.5%), opt-in. Official count 12,073 | A full food-permit list updated monthly (as of the end of the previous month), under a Creative Commons licence, plus barber and beauty open data (`city.kawasaki.jp/350/page/0000093741.html`, `…0000120745.html`) |
| **Chiba** (designated) | 47: monorail 18, JR 19, Keisei 13 | **8,212 (89%; 73.8%)** | 保健所関係台帳 (barber and beauty in Excel). Licence unread |
| **Takamatsu** | 46: Kotoden 33, JR 13 | 56 (1%), opt-in. Official 5,439 | A full month-end food list, and barber and beauty 開設一覧 (CSV/JSON), on オープンデータたかまつ |
| **Ōtsu** | 40: Keihan 24 (the street-running Keishin and Ishiyama-Sakamoto lines), JR 16; 4 funicular groups out | 67 (2%), opt-in. Official 3,115 | Food list (as of 2025-08: stale), barber 2026-07, beauty 2025-06, laundry 2025-09 (BODIK 252018) |
| **Himeji** | 31: JR 16, Sanyō 15 | 132 (2%), opt-in. Official 6,706 | Food list (full and new), barber, beauty in XLSX (`city.himeji.gkan.jp`) |
| **Kurume** | 25: Nishitetsu 16, JR 9 | **3,861 (89%; 77.6%)** | Barber and beauty lists, and a food list of new permits (BODIK) |
| **Yokosuka** | 21: Keikyū 17, JR 4 | 133 (4%), opt-in. Official 3,461 | A full food-permit list, and barber, beauty and laundry lists as of 2026-06-30 (BODIK 142018) |
| **Nishinomiya** | 22: Hanshin 10, Hankyū 8, JR 5 | 134 (3%), opt-in. Official 4,505 | Food (2025-12) and beauty on the city portal; barber not seen |
| **Nara** | 14 (thin): Kintetsu 10, JR 4 | **4,071 (90%; 78.0%)** | An old-law food list, and barber and beauty lists as of 2024-04-01 |

### Likely B: one bucket

- **Sasebo.** 28 groups (Matsuura 22, JR 7); MHLW 2,316 (92%; 77.2%). Food list on BODIK; no personal-services list seen.
- **Shimonoseki.** 21 groups, all JR; MHLW 2,632 (94%; **98.9%**). Personal services are published only as monthly new openings.
- **Hamamatsu.** 54 groups (Enshū 18, Tenhama 19, JR 18). MHLW holds notifications only, and the city's food list is new permits only. Barber and beauty lists exist, so this would be a personal-services page (Yokohama's precedent). ⚠️ The 2024 ward reorganisation (codes 22138–22140) needs checking against ISJ.
- **Food only, from a list seen on BODIK.** Row counts are unmeasured for all four:
  - Toyota: 25 groups (Meitetsu 12, Aikan 12, Linimo 2); the list is full, as of 2026-08-31.
  - Yokkaichi: 35 groups (Kintetsu 15, Asunarō 9, Sangi 7, JR 5).
  - Wakayama: 31 groups (JR 12, Nankai 11, Wakayama Dentetsu 10).
  - Higashiōsaka: 26 groups (Kintetsu 18, JR 7, subway 2).
- **Maebashi and Takasaki.** 19 and 16 groups. MHLW holds 52% and 59% of the in-force count, at 98% and 94% addressed, and each has a city food list. Food could pass if those lists fill the gap.
- **Shizuoka and Fukuyama** (borderline). 26 and 18 groups. MHLW holds 94% and 90%, but only 60.3% and 67.0% carry an address. Shizuoka also has a pre-2021 ledger.

### Likely fail

- **Too few stations (rail).**
  - Food is strong in all of these, but the station count is low:
    - Tottori: 13 groups, MHLW 98.4% addressed.
    - Yamagata: 11 groups, 90.3%.
    - Morioka: 11 groups, 76.3%.
    - Yao: 11 groups, 73.2%.
    - Kure: 13 groups, 68.5%.
    - Mito: 6 groups.
    - Takatsuki: 5 groups.
    - Kōfu: 7 groups.
    - Chigasaki: 3 groups (MHLW 1,843 permits, 96.9% addressed).
  - Most Tokyo, Saitama, Ōsaka and Hyōgo satellites have under 10 groups. Examples: Kawaguchi 8, Koshigaya 8, Machida 9, Chōfu 9, Tokorozawa 10, Ibaraki 10.
- **Placement.**
  - Matsumoto: 20 groups, 35.4% addressed.
  - Funabashi: 30 groups, 70% coverage, 52.4% addressed. A BODIK food list might rescue it.
  - Miyazaki: 28% coverage, 36.8% addressed.
  - The prefecture-file satellites fall under the bar: Matsudo (20 groups), Ichihara (20), Ichikawa (15) and Fuji (17), at a prefecture-wide 62.7% or 66.8%.
  - Chiba Prefecture's own food and 環境衛生 lists (they exclude Chiba, Funabashi and Kashiwa) are an unscreened alternative for Matsudo and Ichikawa.
- **Business: opt-in MHLW and no city list found.**
  - Searched and nothing found: Saitama (31 groups; its page points back to MHLW), Niigata (29, JR only). Both look like C.
  - Not searched: Kanazawa 21, Kurashiki 21, Sagamihara 16, Naha 16 (monorail), Hachiōji 20. Status unknown.

## 4. Cost

The 2026-10-02 batch of 12 was briefed by four agents at about 25 minutes each. Wave 2's top tier is about 15 cities (9 A and 6 B), and most of them are **city-list cities**, not MHLW cities.

- **Licences.** Each needs a `licence-read` per new source, about 20 to 25 sources. Kawasaki, Takamatsu and the BODIK cities state CC BY; Chiba, Himeji and Nishinomiya are unread.
- **Joins.** Each needs an ISJ join measurement.

**Screen and briefs together:** about 5 agents × 30 to 35 minutes, plus 20 to 25 licence reads, about 4 to 5 agent-hours in parallel lanes, plus a staging read-back. The whole is roughly 1.5× the last batch's briefing.

**Build:** comparable to the current batch (a lead and 3 agents), after it lands.

**What the current batch's Phase 1 already covers** (`docs/handoff_japan_batch_2026-10-02.md`):

- The **ward-less flag** covers every core city here (Takamatsu, Ōtsu, Himeji, Kurume, Yokosuka, Nishinomiya, Nara, Sasebo, Shimonoseki, Toyota, Yokkaichi, Wakayama, Higashiōsaka).
- The **MHLW-alone shape (Okayama's) and the MHLW-plus-old-law shape (Kitakyūshū's, Utsunomiya's)** cover Chiba, Kurume, Nara, Sasebo and Shimonoseki.
- These carry over unchanged:
  - the `OPERATOR_COLS`, `ADDR_COLS` and `NAME_COLS` spellings, though each new list will add some;
  - `japan_eigyo`'s short old-law spellings;
  - the **N02-25** edition;
  - MHLW notifications as partial retail;
  - the **minor label tier and the Japan sub-region** (wave 2 only joins them).

**What would be new:**

- multi-sheet XLSX readers (Himeji, Nishinomiya, Chiba);
- Hamamatsu's post-2024 ward codes;
- a prefecture-file slicer, only if a satellite is ever wanted (not recommended).

## Notes

- Downloads were limited to MLIT N03 (30 prefectures, into the shared cache) and MHLW files: 65 city and 19 prefecture codes, held in this folder. Code 40202 (Ōmuta) answered 404.
- BODIK was read through its CKAN search API (metadata only).
- Nothing printed or stored any name; the output is counts only.
