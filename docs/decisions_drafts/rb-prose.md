# rb-prose: the large review's prose and records fixes (lanes 2 to 4)

Drafts for the fold. Branch `rb-prose`, cut from `review-batch-2026-10-07`
for the large review. The lanes reviewed pinned commit 779856e3; every item
below was re-found at this branch before it was applied. Lane 1 (Japan) had
not reported; its items come later.

### 2026-10-07 - Review fixes applied: lanes 2 to 4, and the owner's review-time calls

- **Applied through `scripts/prose_proposals.py apply --ids`** (each old
  text found exactly once at this branch; the log in
  `data/_review/applied.json`): **lane 2**, 3 (P1-P3, Copenhagen's S-tog Bx:
  every 20 minutes at peak only, on the page, What Is Excluded and the
  config comment); **lane 3**, 1 (P11, Why the Maps Differ's two lists that
  read as complete); **lane 4**, 97: its 80 `fix` items (lane 4's file holds
  80 fix and 45 proposal, not the 81 and 44 its report gives) and 17 tagged
  `proposal` that only take a leaked process note off a rendered doc or
  correct a stale claim, on Cleanup's direction: P205, P214-P217, P233,
  P246-P254 (japan.md's "staging", "the brief", "flagged for review", "the
  standing call"), P256 (germany.md's "owner-approved") and P611.
- **Notable ones.** London's colour sentence now names the Metropolitan
  (purple) and the Northern (gray) (P2): after rb-mapconfig the Piccadilly
  is still drawn mauve (#805878), but its TfL blue no longer sits near any
  dot colour, so the old reason was false; the mauve is now unexplained on
  the page, for the UK re-search lane 4's call 1 queued. Higashimurayama and
  Tachikawa name Higashiyamato where they named themselves (P501, P3).
  Gelsenkirchen's 362 is 359 (P306): measured read-only from the cached
  reduced fetch (`data/gelsenkirchen/raw/idb_gewerbe_*.geojson`) through the
  taxonomy, services layer 593 = 359 out by rule + 108 Personal services +
  122 blank + 4 car dealers; 362 was 359 plus the food layer's 3 hotels,
  listed apart. The abroad-batch drafts entry still says 362. Tachikawa's
  national filings count 407 (P316), the siblings' sum: 120 permits + 287
  notifications in its build entry. The data_sources.md country index
  (P107-P110) now matches app/cities.py country by country (Copenhagen
  (Regional), Tacoma, Mendoza, seven UK cities), measured by script.
  Suita's privacy row reads `publish` (P601); Thessaloniki and Bremen
  `publish-structural` (P602, P603). "health centre" is "health center" in
  all eight Tama-ledger sections (P308-P315).
- **The "Tama template" has no file of its own**: no script, skill or brief
  carries the packaged-food sentence; each later Tama city copied
  Higashiyamato's section, and all eight copies are fixed. The japan-city
  skill's "health centre" (line 542) is internal text, left as written.
- **Lane 3's F2 (P3-P10), applied with different words:** the eight pages'
  map help names the layer as the map's menu now names it, in quotation
  marks, last in a three-item list ("three business categories (Food
  service, Personal services and “Food, secondhand, electronics, tobacco
  shops”)"); lane 3 had proposed the count alone. Listed in the owner file
  for a look.
- **`country_sections.public()` strips a trailing owner tag** too: "(3.0%,
  owner)", "(the flat rule, owner 2026-09-28)", "(...; owner, call 165)",
  "(158 pending out, owner call 24)" keep their fact and lose the tag. Only a
  date or a call number may follow "owner", so "a sole owner" and "owner's
  rule" stay. 29 such tags rendered (11 on What Is Excluded, among them nine
  UK "flat rule" brackets; 18 on About the Data's country files), each read
  before and after; check_internal_prose finds none of this shape left.
- **`scripts/check_privacy_verdicts.py` FAILS on `pending`** (was report
  only): every city in app/cities.py ships, so a pending verdict is a page
  published without one. The table's definition says so.
- **Mexico City (Regional)'s data date**: "DENUE May 2026 edition, fetched
  2026-09-22; State of México 2026-10-07" (entidad 15's ZIPs and mexico.md's
  row both 2026-10-07), Los Angeles's two-date form.
- **Lane 3's O4, reference pages open on the reader's country:**
  `country_sections.origin_country()` reads `?from=` when a link carries no
  `?country=` (a city's footer, an Overview region): a city gives its own
  country, a region whose cities share one country gives that country
  (Canada East, Czechia, the Japanese regions); a region spanning several
  (Europe West, Benelux, South America) keeps the default. Measured: every
  one of the 206 cities maps to its own country.
- **Owner decisions of 2026-10-07 applied.** Notice dates month first: Tsu
  (179), Fukushima (180) and Iwaki (181) in `_NOTICES` (their ledger entries
  carry no English date), with Maebashi and Fukuyama (lane 4 P103-P104).
  About 25 older approved notices (Toyama, Fukui, Nagasaki, Sakai and
  others) still write day-first, outside this call. Hirakata's unlinked
  credit approved: one line in its notice comment, ledger entry 170 and its
  japan.md licence row. Amagasaki §6 and Suita §5, the undefined harm and
  defamation bars, accepted knowingly on the Taoyuan, Fukui and Maebashi
  precedents: ledger entries 171 and 174 and both japan.md rows say so.
  `docs/licence_positions.md` gains Tier 2 rows 2.49 to 2.52 (Amagasaki,
  Suita, Hirakata, Hyōgo); its counts move to 52 and 146.
- **Not applied: 36 proposals** for the owner in
  `data/_review/proposals_for_owner.md` (lane 2 P4 and lane 3 P2 as one
  item; lane 3's O1 drafted as nine sentences, Busan's "Retail dots" among
  them; 26 more from lane 4). Lane 4's P201 and P202 were already applied by
  rb-mapconfig (88f528e8).
- **Could not confirm or left alone:** the Piccadilly's mauve has no stated
  reason on London's page now (above). Busan's Line 4 bullet says "the
  Retail dots" (O1-9, a proposal). The abroad-batch drafts entry's "362
  services by rule" is a drafts text, left for the fold.
