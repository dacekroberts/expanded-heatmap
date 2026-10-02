# Decisions drafts: the Japan batch build session (`japan-batch-build`)

Entries in the `decisions-entry` format, newest first, each exactly as it
should land in `DECISIONS.md`. Cleanup folds them in when the owner hands
them off.

## 2026-10-02 — Japan batch: the shared code in one pass, proven on Minato and the eight built cities

**Context:** Every one of the twelve briefs named a "shared code at build"
item in `pipeline/countries/japan_register.py`, `japan_step2.py`,
`japan.py` or `pipeline/taxonomies/japan_eigyo.py`. The kit
(`docs/handoff_japan_batch_2026-10-02.md`, Phase 1) has them made together,
by the lead, before any agent starts.

**Decision:** One pass, each change naming the city that taught it:
- **Columns.** `ADDR_COLS` += 所在地＿連結表記 (full-width low line), 施設所在地１,
  営業所所在地1, 営業所の所在地, 施設住所名称, 所在地, 施設住所, 営業所 (after every
  older spelling, so a built city's choice of column cannot change).
  `NAME_COLS` += 施設名称1, 施設名称１, 施設名, 営業所名称, 屋号名称, 営業所の名称,
  営業所の名称、屋号又は商号. `OPERATOR_COLS` += 申請者個人名, 開設者氏名,
  代表者氏名（法人のみ）, 申請者名(法人名), 申請者名（法人名）, 法人代表者名, 開設者,
  代表者, 代表者氏名.
- **Readers.** `city_rows` reads an old `.xls` through `workbook_tables`
  (Matsuyama), finds a CSV's header by its address column below title rows or
  an empty first line (Hakodate, Matsuyama), strips header cells (Utsunomiya's
  ` 　名称`); `xlsx_rows` takes `sheet=` (Fukui's twelve month-end sheets, the
  newest first) and an opt-in `merged_header=` that joins a merged header's
  unnamed columns into it (Toyama: 施設住所 over four columns). Opt-in because
  a built city's unnamed column is not a merge.
- **Addresses.** A `wardless` flag in `japan.CITIES` (eight of the twelve):
  an address is never split at a 区 (Toyama's 太田北区, Fukui's 土地区画整理事業).
  `norm_town`: a town ENDING in N丁 reads N丁目 (Sakai's 780 town-chōme, MLIT
  writes 翁橋町一丁; only end-anchored, so 八丁堀, 六丁の目, 三丁町 are untouched);
  katakana ニ before 丁目 / 番町 reads 二 (Matsuyama, Okayama); a hyphen between
  katakana reads ー (Utsunomiya's インタ-パ-ク). Kōchi's 高埇 (outside JIS X
  0208) and MHLW's 高そね both read MLIT's 高埆. A line break inside an address
  is dropped (Utsunomiya). 保健所管内 / 保健所管轄内 is not a premises
  (Matsuyama's 277 vehicles and stalls). `in_term()` drops an old-law row past
  its expiry against a pinned as-of (Kitakyushu, Utsunomiya).
- **Step 2.** `POINT_DONORS` (Toyama's brief, recommended on measured
  grounds): where the block join misses a row and another publisher (MHLW)
  lists the same premises (ward, town, trade name) with one point, that point
  places it, tier "own". The donor is read for points only, never drawn.
- **Taxonomy.** `japan_eigyo` reads Fukui's old-law short types 飲食店 and
  喫茶店 (93 restaurants), with import-time asserts.
- **Rail.** The twelve `japan.CITIES` entries, each on N02-25.
- Not made: Utsunomiya's 新里町甲 / 丙 地番 (about 24 rows): the 地番 restart in
  each sub-area and MLIT keys only 新里町, so a join would guess. They stay
  unplaced.

**Verification:**
- **Minato control:** block 98.0 / chōme 0.2 / none 1.8, byte-identical
  output. 23 of the 24 older screens byte-identical; `fukuoka-mhlw` moved 4
  rows from unplaced to block (桜坂ニ丁目, 立花寺ニ丁目, 竹丘町ニ丁目, 博多駅前三丁).
- **The twelve screens reproduce their briefs:** Matsuyama 82.0 / 17.2 / 0.8
  (brief 81.9 / 17.2 / 0.9; the ニ番町 rows), Toyama 86.6 / 12.1 / 1.3 and
  registers 80.6 / 14.6 / 4.8 (the merged-header reader), Kumamoto 97.0 and
  96.8, Fukui 87.5 and 87.3, Nagasaki 88.6 and 90.1, Utsunomiya 93.2, 95.1
  and registers 96.2 (brief 93.5: the line-break and katakana rules), Sakai
  96.0 (brief 95.8 by its bucket count), Hakodate 94.0, Kagoshima 93.7,
  Kōchi 95.8 / 4.2 / 0.0 (brief 95.4 / 4.2 / 0.4: the 高埇 rows now place).
- **The eight built cities' step 2, re-run in memory against their processed
  output:** Hiroshima, Yokohama, Kobe, Sapporo, Kyoto and Osaka identical, and
  every baseline count unmoved (peaks 0.17-0.62 GB). **Fukuoka and Tokyo
  move, by fixes only, accepted on Kobe's precedent (a shared fix that moves
  a built city is recorded with its diff):** Fukuoka's 4 MHLW rows above
  now join at the block instead of MHLW's own point, and one of those points
  was wrong by about 12 km (立花寺ニ丁目's konbini sat at 130.342 E; the block
  is 130.467 E). Tokyo: the same for 2 rows (佐賀二丁, 新橋ニ丁目), and 2 Kōtō
  shop pins that were MHLW duplicates of Kōtō's own rows (有明ニ丁目, 豊洲ニ丁目)
  now collapse under `SUPERSEDES`: storefronts 61,377 to 61,375.
- **Drift checks:** Hiroshima, Yokohama, Kobe, Sapporo, Kyoto, Osaka: zero
  drift (`heavy_job.py`, measured peak 0.64 GB). Fukuoka and Tokyo with
  `--update-baseline`: their maps drift by exactly the rows above
  (`join_block` +4, `join_own` -4, Tokyo `storefronts` -2; measured peak 1.46
  GB).
- **A mistake, corrected the same hour:** that drift check rewrote Tokyo's and
  Fukuoka's `data/*/processed/` in the shared folder with this branch's code,
  so master's `check_macro_facts` failed for every session (Tokyo 61,375
  against master's 61,377; Cleanup caught it). Both were re-run from a
  temporary `origin/master` checkout and master's check passes again. **So
  this branch does NOT commit Fukuoka's and Tokyo's new outputs, baselines or
  `app/macro_facts.json`: at landing, after the merge to master, re-run
  their steps 2-3 (`drift_check.py fukuoka tokyo --update-baseline`) and
  `check_macro_facts.py --write`, and commit those with the batch.** Never
  re-run a built city's step from this branch without restoring it.

## 2026-10-02 — Japan batch: session registered, briefs re-checked, numbers claimed

**Context:** The owner released the twelve Japanese cities of the 2026-10-01
screen to one build session with agents (`docs/handoff_japan_batch_2026-10-02.md`).

**Decision:** The session registered in `docs/session_roles.md` and claimed
notices 97-108, one per city in the kit's table order, after re-reading the
table (the UK six hold 84-96). Pages 162-173 as pre-assigned.

**Verification:** `python scripts/brief_check.py <slug>` for all twelve:
122 of 122 claims pass on 2026-10-02 (Matsuyama 10, Toyama 12, Kumamoto 12,
Fukui 11, Nagasaki 12, Utsunomiya 14, Kitakyushu 11, Sakai 9, Hakodate 10,
Kagoshima 9, Okayama 5, Kōchi 7). Master merged at 5310fe44.
