# Decisions drafts: the Japan batch build session (`japan-batch-build`)

Entries in the `decisions-entry` format, newest first, each exactly as it
should land in `DECISIONS.md`. Cleanup folds them in when the owner hands
them off.

### 2026-10-02 - Matsuyama built, the pilot of the Japan batch

- **Matsuyama built on the shared Japanese steps: 9,285 storefronts (Food
  service 5,572, Retail 1,707, Personal services 2,006), 60 stations, 5
  lines; 5,136 pins within a ring (55%).** Page 162, notice 97, `mode: tram`,
  `label_tier: "minor"` (owner, 2026-10-02), East Asia until the Japan
  region pass. Files: `pipeline/matsuyama/`, `outputs/matsuyama/`,
  `app/pages/162_Matsuyama_Heatmap.py`, its `app/cities.py` entry, notice 97
  in `app/components.py` and `docs/data_sources.md`, its rows in
  `docs/data_sources/japan.md`, `docs/excluded_categories.md`,
  `docs/map_inconsistencies.md` and `docs/privacy_verdicts.md`.
- **The business leg is the brief's, as the owner decided it ("approve all
  recommendations", 2026-10-02).** The city's two food lists (577 old-law and
  7,110 new-law permits, every permit in force on 2026-03-31) and its full
  barber, beauty and laundry lists (old `.xls`, 2026-03-31). MHLW's file adds
  only its 4,205 notifications (届出, the partial food-retail bucket, as
  Fukuoka and Hiroshima) through `config.source_rows`, and, as a point
  DONOR (`POINT_DONORS`), its own point for 699 city rows the block join
  missed (the brief estimated 797 by trade name alone; the donor also
  requires the same town). MHLW's permits are not added: the city's list
  holds 103% of the official count. 136 city rows that duplicate an MHLW
  notification row in the same bucket give way to it (`SUPERSEDES`).
- **The join:** block 80.8%, MHLW's point 10.2% (363 notifications on their
  own point, 699 city rows on the donor's), town-chōme 8.2%, unplaced 84
  (0.8%: 甲 / 乙 地番 and rural 大字). Against MHLW's own coordinates the block
  hits sit a median 40 m away, 96.9% within 250 m (1,029 rows).
- **Rail:** N02-25, 60 stations by group code, 11 excluded (6 in Tōon, 5 in
  Masaki). The city tram's six legal sections (城北線, 城南線, 大手町線, 本町線,
  花園線, 連絡線) are drawn as ONE line, "Iyotetsu City Tram", on Sapporo's
  precedent for its streetcar: the operator's routes 1 to 6 share nearly all
  their track, so drawing each would stack five lines on one street. Gate 3:
  the Takahama Line, 10 = 10 against Iyotetsu's station index; the operator
  publishes no tram stop count (the brief found the same), so the tram's 28
  stops are N02's, as Hiroden's are. Median station gap 374 m: halved rings
  and gate 1's 200 m floor, Hiroshima's precedent (357 m). English names:
  OSM with 9 aliases and 20 cited overrides in Hiroshima's style; OSM had
  TRANSLATED six stops ("Police Station", "Red Cross Hospital", "Matsuyama
  City Hall", "Ehime Pref. Office", "Dogo Park", "Ishitegawa Park") and gave
  the railway's 松山市 and the tram's 松山市駅 the same name. Line colors from
  `line_colour_search.py` (closest pair 18.4).
- **Economic Census join control: 2.73 Food service pins per 2021 census
  飲食店 establishment, above the built cities' 1.56-1.92, EXPLAINED.** The
  official permits in force per census establishment (e-Stat FY2024 against
  the 2021 census) run 2.24 (Fukui) to 3.96 (Osaka) across the built and
  batch cities, Matsuyama 2.91, beside Fukuoka 2.96 and Kyoto 3.10. The built
  cities map fewer pins than the official count (lists that leave out
  vehicles, counter-only lists, de-duplication), so their map ratio sits
  lower; Matsuyama's list is complete and its 5,572 pins are 94% of the
  official 5,924. The ratio is the permit structure, not the join. The batch's
  benchmark for this control is therefore official / census, not the built
  cities' map ratios.
- **Privacy verdict: publish.** `check_personal_exposure.py matsuyama`: the
  Japan pass prints 0 operator's own names shown as a trade name (5 in the
  raw files, the brief's 4 food rows and 1 laundry row; 3 pins show their
  permit type). That laundry row needed `開設者法人名` / `営業者法人名` read by the
  name rule (next entry). No pin at a residential unit.
- **The 菓子 / そうざい factory share** (owner, 2026-09-24): 33 of 729 rows
  (4.5%), kept.
- **Page prose: proposals for review time** (sentences no template covers):
  "The city tram's routes share most of their track, so the tram is drawn as
  one line."; the Reading the map bullet's ending "where that fails, the dot
  sits at the ministry's own coordinates for the same premises, or else at its
  district's center" (Hiroshima's bullet extended to the donor); the notice's
  English gloss "(This map modifies the City of Matsuyama's lists of food
  permits, barbers, beauty salons and laundries as of 31 March 2026, used under
  CC BY 4.0.)" (Yokohama's form).

### 2026-10-02 - The name rule reads a register's 法人名 column where it holds a sole trader's own name (Matsuyama)

- **`japan_register.OPERATOR_COLS` gained 開設者法人名 and 営業者法人名.** In
  Matsuyama's barber, beauty and laundry lists the 法人名 column is filled on
  every row and carries no company marker on 443 of 485 barbers: it holds a
  sole trader's own name, and 開設者氏名 / 営業者氏名 holds only a company's
  representative (44 of 485 filled). Without it the rule found 0 laundry rows;
  with it, 1, the brief's count. Company names never count (`KYOTO_CORP`'s
  markers), so a company whose trade name is its own name is still shown.
  Measured in memory, counts only. The eight built cities' step 2 re-run in
  memory: no withheld-name count moved (none of their files has the column).
- **`事業場食堂` (a workplace canteen) joined the institutional-catering form
  rule** in `japan_eigyo.FORM_RULES` beside 社員食堂: Matsuyama's old-law 業態
  (22 rows); no built city's files carry it.

### 2026-10-02 - Japan batch: the shared code in one pass, proven on Minato and the eight built cities

- **Every brief's shared-code item was made in one pass by the lead, each
  change naming the city that taught it, before any agent started**
  (`docs/handoff_japan_batch_2026-10-02.md`, Phase 1).
  - **Columns.** `ADDR_COLS` += 所在地＿連結表記 (full-width low line), 施設所在地１,
    営業所所在地1, 営業所の所在地, 施設住所名称, 所在地, 施設住所, 営業所 (after every
    older spelling, so a built city's choice of column cannot change).
    `NAME_COLS` += 施設名称1, 施設名称１, 施設名, 営業所名称, 屋号名称, 営業所の名称,
    営業所の名称、屋号又は商号. `OPERATOR_COLS` += 申請者個人名, 開設者氏名,
    代表者氏名（法人のみ）, 申請者名(法人名), 申請者名（法人名）, 法人代表者名, 開設者,
    代表者, 代表者氏名.
  - **Readers.** `city_rows` reads an old `.xls` through `workbook_tables`
    (Matsuyama), finds a CSV's header by its address column below title rows
    or an empty first line (Hakodate, Matsuyama), and strips header cells
    (Utsunomiya's padded 名称); `xlsx_rows` takes `sheet=` (Fukui's twelve
    month-end sheets, the newest first) and an opt-in `merged_header=` that
    joins a merged header's unnamed columns into it (Toyama: 施設住所 over four
    columns). Opt-in because a built city's unnamed column is not a merge.
  - **Addresses.** A `wardless` flag in `japan.CITIES` (eight of the twelve):
    an address is never split at a 区 (Toyama's 太田北区, Fukui's
    土地区画整理事業). `norm_town`: a town ENDING in N丁 reads N丁目 (Sakai's 780
    town-chōme, which MLIT writes 翁橋町一丁; end-anchored, so 八丁堀, 六丁の目 and
    三丁町 are untouched); katakana ニ before 丁目 / 番町 reads 二 (Matsuyama,
    Okayama); a hyphen between katakana reads ー (Utsunomiya's インタ-パ-ク).
    Kōchi's 高埇 (outside JIS X 0208) and MHLW's 高そね both read MLIT's 高埆. A
    line break inside an address is dropped (Utsunomiya). 保健所管内 /
    保健所管轄内 is not a premises (Matsuyama's 277 vehicles and stalls).
    `in_term()` drops an old-law row past its expiry against a pinned as-of
    (Kitakyushu, Utsunomiya).
  - **Step 2.** `POINT_DONORS` (Toyama's brief, recommended on measured
    grounds): where the block join misses a row and another publisher (MHLW)
    lists the same premises (ward, town, trade name) at one point, that point
    places it, tier "own". The donor is read for its points only, never drawn.
  - **Taxonomy.** `japan_eigyo` reads Fukui's old-law short types 飲食店 and
    喫茶店 (93 restaurants), with import-time asserts.
  - **Rail.** The twelve `japan.CITIES` entries, each on N02-25.
  - **Not made:** Utsunomiya's 新里町甲 / 丙 地番 (about 24 rows). The 地番
    restart in each sub-area and MLIT keys only 新里町, so a join would guess;
    they stay unplaced.
- **Minato's control reproduces exactly (block 98.0 / chōme 0.2 / none 1.8,
  byte-identical output), and 23 of the 24 older screens are byte-identical.**
  `fukuoka-mhlw` moved 4 rows from unplaced to block (桜坂ニ丁目, 立花寺ニ丁目,
  竹丘町ニ丁目, 博多駅前三丁).
- **The twelve screens reproduce their briefs:** Matsuyama 82.0 / 17.2 / 0.8
  (brief 81.9 / 17.2 / 0.9: the ニ番町 rows), Toyama 86.6 / 12.1 / 1.3 and its
  registers 80.6 / 14.6 / 4.8 (the merged-header reader), Kumamoto 97.0 and
  96.8, Fukui 87.5 and 87.3, Nagasaki 88.6 and 90.1, Utsunomiya 93.2, 95.1 and
  registers 96.2 (brief 93.5: the line-break and katakana rules), Sakai 96.0
  (brief 95.8 by its bucket count), Hakodate 94.0, Kagoshima 93.7, Kōchi 95.8 /
  4.2 / 0.0 (brief 95.4 / 4.2 / 0.4: the 高埇 rows now place).
- **The eight built cities' step 2, re-run in memory against their processed
  output: Hiroshima, Yokohama, Kobe, Sapporo, Kyoto and Osaka identical,
  every baseline count unmoved (peaks 0.17-0.62 GB). Fukuoka and Tokyo move,
  by fixes only, accepted on Kobe's precedent (a shared fix that moves a built
  city is recorded with its diff).** Fukuoka's 4 MHLW rows above now join at
  the block instead of MHLW's own point, and one of those points was about 12
  km off (立花寺ニ丁目's konbini sat at 130.342 E; the block is at 130.467 E).
  Tokyo: the same for 2 rows (佐賀二丁, 新橋ニ丁目), and 2 Kōtō shop pins that
  duplicated Kōtō's own rows in MHLW's file (有明ニ丁目, 豊洲ニ丁目) now collapse
  under `SUPERSEDES`: storefronts 61,377 to 61,375.
- **Drift checks:** Hiroshima, Yokohama, Kobe, Sapporo, Kyoto and Osaka zero
  drift (`heavy_job.py`, measured peak 0.64 GB). Fukuoka and Tokyo with
  `--update-baseline`: their maps drift by exactly the rows above (`join_block`
  +4, `join_own` -4, Tokyo `storefronts` -2; measured peak 1.46 GB).
- **A mistake, corrected within the hour:** that drift check rewrote Tokyo's
  and Fukuoka's `data/*/processed/` in the shared folder with this branch's
  code, so master's `check_macro_facts` failed for every session (Tokyo
  61,375 against master's 61,377; Cleanup caught it). Both were re-run from a
  temporary `origin/master` checkout and master's check passes again. **So
  this branch does NOT commit Fukuoka's and Tokyo's new outputs, baselines or
  `app/macro_facts.json`: at landing, after the merge to master, re-run their
  steps 2-3 (`drift_check.py fukuoka tokyo --update-baseline`) and
  `check_macro_facts.py --write`, and commit those with the batch.** A built
  city's step is never re-run from this branch without restoring it.

### 2026-10-02 - Japan batch: session registered, briefs re-checked, numbers claimed

- **The Japan batch's build session registered in `docs/session_roles.md`,
  with pages 162-173 as pre-assigned and notice numbers 97-108 claimed, one
  per city in the kit's table order** (Matsuyama 97 ... Kōchi 108), after
  re-reading the table: the UK six hold 84-96.
- **All twelve briefs re-checked: 122 of 122 claims pass** on 2026-10-02
  (Matsuyama 10, Toyama 12, Kumamoto 12, Fukui 11, Nagasaki 12, Utsunomiya
  14, Kitakyushu 11, Sakai 9, Hakodate 10, Kagoshima 9, Okayama 5, Kōchi 7).
  Master merged at 5310fe44.
