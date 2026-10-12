# Decisions drafts: staging (branch worktree-staging)

Started fresh after the fold of 2026-10-08 (Cleanup, 9be520f2). Newest
first. Owner calls are numbered S1 on from phase 2; a plain number is the old
series, which ended at 230.

## Changes

### 2026-10-12 - Phase 2 built in one evening; the owner's S calls; Naha's two licence reads

- **Naha's brief written (`docs/build_briefs/naha.md`, brief check 5 of 5):
  a rebuilt food register of 8,450 pins that places 99.9%, with the Yui
  Rail's 16 stations; the band is still the owner's.** Step 0 was measured
  on 2026-10-12 by a subagent from the 213 cached workbooks, the rail and
  boundary files on disk and the two MLIT address files the owner approved
  that day (S29: `47201-24.0a.zip` 162,904 B, `47201-19.0b.zip` 8,025 B).
  Kansai-2's control reproduced to one row (8,939 against 8,938; the extra
  row's expiry is an Excel serial). **One correction to Kansai-2's
  measurement:** three months are published twice (2025-03, 2025-12,
  2026-08; 394 repeat rows), so the distinct restaurant permits in term are
  8,593, 100.7% of the 8,530 in force, not 104.8%; by premises it stays
  98.8% (8,429). Storefront rows from the new-permit files: Food service
  7,390, Food shops 1,358; 8,450 pins after one per premises (8,799 with
  the renewals package). Set aside: 769 citywide stalls, 171 area-wide
  vehicles, 312 non-storefront rows. The join: 17,689 block keys, block
  98.9%, town-chōme 1.0%, 9 rows unplaced, no independent check (the files
  carry no points). Rail: the Yui Rail, 16 of 19 stations inside (3 in
  Urasoe, the add-on row), median gap 733 m, EPSG:32652. The name rule
  withholds 4 trade names; 0 bare personal names. The rebuild sits high
  against the census (2.77 placed restaurant premises per establishment
  against 1.56 to 1.92 on built cities), closures being invisible. Six
  shared-code items a build would need are listed in the brief (a reader
  argument on `rebuilt_register`, unnamed header columns in `xlsx_rows`
  that lose the 種目 form on 3,405 rows, two missing column names, one
  character variant, config keys). Seven open calls were put to the owner
  as S30 to S36 (the band; the renewals package; the excess over the
  census; `mode` for a monorail-only city; a personal-services probe; the
  macro view; three page sentences). Not measured: frequency (the master
  list's read of 2026-10-06 stands), gate 3, OSM names, any
  personal-services list. The master-list row is unchanged until the owner
  bands the city.
- **S22 answered: Kanazawa's page states no share, and IR Ishikawa's
  frequency was read (owner, "s22 no share, yes read the frequency"): 49 to
  58 trains a day each way at its three stations beside Kanazawa.** The
  share is left off because the 2024 snapshot holds 6,478 permits against an
  official 6,438 (100.6%; 100.9% against the like-for-like FY2023 count), a
  figure over 100% that would inform no reader. The frequency was counted by
  staging on 2026-10-12 from the operator's whole-line timetable of
  2026-03-14 (`ishikawa-railway.jp/timetable/pdf/20260314.pdf`, linked from
  the timetable index the brief names; the two PDFs the brief names are
  Shinkansen connection tables), as printed departure times on each station's
  row in `pdftotext -table` output: 東金沢 58 toward Tsubata and 57 toward
  Kanazawa; 森本 57 toward Kanazawa (its other direction's afternoon row did
  not extract, the morning half holds 28, the same as 東金沢's); 西金沢 49
  toward Kanazawa and 53 away. The counts take every printed time, so trains
  marked for certain days only are included, and trains of other operators
  running through on the line are counted where they stop. About three
  trains an hour each way, far from the 11 a day of a low-frequency stretch:
  the line's frequency moves from ASSERTED to MEASURED with that caveat. The
  count was not checked against a rendered page (no PDF renderer on this
  machine).
- **Phase 2 started on 2026-10-11 at about 21:48 UTC and all three sessions
  reported by 02:10 UTC on 2026-10-12: 29 Japanese cities and Cluj-Napoca
  built, nothing pushed.** East-2 (`worktree-japan-east-2`, 11 cities, pages
  240-250), Kansai-2 (`worktree-japan-kansai-2`, 7 cities on pages 251-257
  and Cluj-Napoca on 305) and Regional-2 (`worktree-japan-regional-2`, 11
  cities, pages 258-267 and 306) each started from master 33a0e5d8 on the
  prompts in `docs/build_plan_2026-10-07.md`. Each reported every city at
  zero drift with a baseline and its privacy pass at 0; none ran a browser
  check, which waits for review time. The weekly figure was 4% at the start
  and 12% when the last session reported (the one usage check-in the owner
  set for this batch, put to the owner with the reports). The per-city
  counts, slips and parked calls are in each branch's drafts file and are
  not repeated here.
- **The owner's calls S1 to S27 were relayed from the three sessions and
  answered, most in the build sessions' own chats.** S1 was put at 23:12 UTC
  on 2026-10-11. Answered in East-2's chat: S1 private-use glyphs shown as
  the permit type ("accepted"), S2 a late start with an earlier first permit
  stays ("shared rule accepted"), both Cleanup's ("leave 1 and 2 to
  cleanup"); S3 the JR Keiyo Line goes to #C81000 ("go with #C81000"; the
  #D01010 first shown sits 7.6 from Tokyo's Keikyu Main Line, and the
  dark-mode label check is not yet run); S4 two OpenStreetMap station
  spellings stay ("note internally"); S5 the label "Saitama Rapid Railway
  Line" stands. Answered in Kansai-2's chat: S6 Osaka's three Osaka Metro
  line names renamed at Osaka's re-render; S7 and S9 page sentences to
  review time; S8 Cluj-Napoca treated as Bucharest under notice 215 ("yes
  treat cluj as bucharest, publish under notice 215"); S10 the Romanian
  name rule's extensions kept; S11 and S12 accepted; S13 Naha "yes brief and
  license reads for two packages". Answered in Staging's chat on 2026-10-12:
  S14 the shared-code changes of S1, S2, S17 and S19 are Cleanup's; S15
  Naha's cost-recovery clause accepted; S16 a NEIGHBOUR_EXCEPTIONS entry
  for Okazaki's and Toyota's Meitetsu red, with a note; S17 the old-law
  vending form goes into the shared rules (83 pins on Kurashiki); S18
  Kurashiki's 特殊形態 read and checked, then a rule if needed; S19
  Tottori's area-wide rule fixed in shared code and the hook deleted; S20
  Tottori's Inbi Line accepted as drawn, against the two pieces of call
  180; S21 Matsumoto's 2026-10-01 edition kept and its brief corrected; S23
  Kure may say "about half (46%)" where that is the more accurate figure;
  S24 gate 3 with no in-city count accepted for Aomori, Tottori, Yamagata
  and Kure, with a note; S25 Aomori's clause 6 accepted; S27 Yamagata keeps
  the 10 placed Zaō Onsen rows, the oddity noted. S22 (answered the same day, the bullet above; Kanazawa.s share and
  IR Ishikawa's frequency) was answered with a question and is open; S26
  (Regional-2's page sentences) waits for review time.
- **Naha's two BODIK packages read PERMITTED WITH CONDITIONS, from the
  BODIK copies only; the cost-recovery clause was accepted by the owner
  (S15).** Two licence-read agents, one per package, 2026-10-11:
  `shinki_syokuhin` (140 resources, 2015-04 to 2026-08) and
  `472018_keizoku_syokuhin` (73 resources, 2015-04 to 2021-05, 2019-05
  absent; renewals from 2021-06 are inside the new-permit package by the
  package's own note). Both declare `cc-by-40-intl`, no resource carries
  terms of its own, and both link Naha City's open-data terms at
  `odcs.bodik.jp/472018/tos/`: CC BY 4.0 unless annotated (第3項), credit
  plus a statement of modification, modified data not presented as the
  city's, no notification owed, Naha District Court (第6項). The clause put
  to the owner is 第5項: the city bills the user for costs, damages
  included, arising from the user's own breach or infringement of a third
  party's rights, with no cap; accepted on the precedent of calls 206, 207
  and 214 (use-triggered clauses). No wording is prescribed for the credit.
  The city's own site hosts the same monthly lists with no licence under
  website terms that forbid reuse without permission, so only files taken
  from `data.bodik.jp` are covered; the cache (`data/naha/raw/shinki` 140
  files, `keizoku` 73) matches the two packages' resource counts and
  Kansai-2 reported 213 GETs from BODIK. Both packages carry applicant
  name, address and phone columns, which CC BY does not license (s.2(b)(1))
  and the build never selects. Not established: a note inside a workbook
  (no data file was opened), and whether the schemas hold across every
  month (three files' field names were read). A brief follows.
- **DSVSA Cluj's terms read a second time on ANSVSA's side: SILENT, on
  archived and harvested copies; the owner's ruling (S8) stands on both
  that day's reads.** Staging's licence-read agent was refused by
  `ansvsa.ro` (HTTP 403, a firewall page) and did not retry; it read
  Internet Archive copies (the home page of 2026-10-07, six others 13 to 15
  months old): no terms, copyright, reuse or open-data page; a privacy
  policy saying ANSVSA and DSVSA staff run the county sites; an index page
  linking Cluj's and Bucharest's registers alike. `data.gov.ro` timed out
  three times; the European data portal's harvest shows ANSVSA with two
  datasets, both livestock counts, and no county DSVSA. Kansai-2's own
  second read reached `www.ansvsa.ro` in the browser after the same 403 to
  a script, with the same finding. Staging put the difference to the owner,
  who kept Kansai-2's read in the record ("kansai 2 stays in record, we
  needed to investigate"). Not read by either: Romania's reuse law (no
  official host served it). One wording point for Bucharest's notice 67:
  its "New York situation" holds for the footer only; no law forbidding
  restrictions is established for Romania.
- **Fuji's notice 210 checked against Shizuoka Prefecture's portal terms:
  it follows the prescribed modified-use form.** Read 2026-10-12 at
  `opendata.pref.shizuoka.jp/privacy.html`, §4: 「この[作品・アプリ・データ
  ベース等]は以下の著作物を改変して利用しています。[タイトル]、静岡県[その他
  の著作権者]、クリエイティブ・コモンズ・ライセンス 表示 4.0 国際（...deed.ja)」,
  the URL allowed as a hyperlink on the licence name. One difference left
  with Regional-2: the terms write 表示 4.0 国際 with a space after 表示.
  This closes the brief's "take the exact credit wording from staging's
  record", which no earlier entry quoted.
