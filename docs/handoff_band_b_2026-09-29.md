# Handoff: build Band B's last eight (the narrower pages), the group before trams

Written 2026-09-29 by the light-rail build session ("Light rail Band A build
sessions", worktree `.claude/worktrees/lightrail`), which built Aarhus,
Buffalo, Sacramento and Houston (all live since the second review, master
`0441fd3`).

## ⏸ READ, THEN WAIT

**The owner is budgeting usage. Read this file, `CLAUDE.md`,
`docs/project_context.md` and the eight briefs below, then report that you
are ready, with your proposed order and the questions in "Owner calls still
open", and STOP.** No fetch, no branch, no code until the owner says go.
When the owner says go, ask whether downloads and page write-ups are
pre-approved, as they were for Houston. If they are not, ask per city before
fetching (sources and sizes) and draft each page's text in chat first.

## State when this was written

- **Band B holds 8 rows** (`python scripts/check_master_list_counts.py
  --verbose`): Gyeonggi satellites, Hiroshima, Kitchener–Waterloo
  (Regional), Minneapolis, Ottawa, Palma, Pittsburgh, Yokohama. Band A is
  empty. After these, the next group is the tram list
  (`docs/tram_city_list.md`), held by the Staging session.
- **75 built; the next free page number is 76** (check `app/pages/` and
  every pushed branch first; `git ls-remote --heads origin`). The scaffold
  picks the next number on ITS branch: rename the page and fix
  `app/cities.py`'s `page` if needed.
- One branch per city, each new from origin/master:
  `git switch -c <city> origin/master`, then `git branch --unset-upstream`,
  and push with `git push -u origin <city>`. **Never push to master.** Each
  branch counts its own figures; the **Project cleanup session** reconciles
  page numbers, Built / Band counts and notices once, in a batch review the
  owner calls. Send cleanup a READY notice per city listing every shared file
  touched.
- Open elsewhere, not yours: `origin/houston-caption` (Houston's fetch-date
  caption, waiting for the next review); three category-continuity
  departures from Buffalo and Sacramento with the owner.

## The eight, with what each brief already settles

Every brief has a checks block: **run `python scripts/brief_check.py <slug>`
before any code.** A failing check is a brief to correct (Houston's brief
said Purple 13; it is 10).

| # | City (brief) | Page | Rail | Business leg | Open at build |
|---|---|---|---|---|---|
| 1 | **Ottawa** (`ottawa.md`) | food only | O-Train Lines 1, 2, 4 from OSM, 25 stations; OSM has no colours, pick through `linecolour.py` | Ottawa Public Health's inspection feed, ~5,300 food premises inspected within two years, 99.8% with coordinates; institutional kitchens out by a bilingual word list | ⚠️ **The item says it "will be retired in Q1 2026": fetch it first and cache it.** The Open Government Licence – City of Ottawa v2.0 credit is prescribed, verbatim. Food shops sit inside with no type field: the page says so |
| 2 | **Minneapolis** (`minneapolis.md`) | food + grocery | METRO Blue and Green from OSM, 16 stations inside; Green's 42% accepted (owner) | Food Inspections, one row per violation: de-duplicate on `HealthFacilityIDNumber`, keep inspected within two years | ⚠️ **The brief keeps CATERER as food; `docs/category_rules.md` R1 takes caterers out (owner, 2026-09-29). Follow R1.** Read the CC0 waiver with `licence-read` |
| 3 | **Pittsburgh** (`pittsburgh.md`) | food + convenience retail | PRT Blue, Red, Silver from OSM, 20 stations; **445 m gap, so halved rings**; Silver's 42% accepted (owner); disclose the part-day service | WPRDC Geocoded Food Facilities (CC0, 2025-08-27), 2,086 active | ⚠️ **Status 7 (3,855 rows, no closing date) is undocumented: read WPRDC's data dictionary first**; it could nearly double the page |
| 4 | **Kitchener–Waterloo (Regional)** (`kitchener-waterloo.md`) | food + personal, no retail | ION from OSM (or GRT's GTFS, same licence), 19 stops | The Region's two inspection layers (MapServer 17, 18); scope by the two cities' polygons, not `SiteCity` (~60 spellings) | Personal services hold home-based operators: `check_personal_exposure.py` first, suppress names at residential addresses (Houston's rule). Required wording: "Contains information provided by the Regional Municipality of Waterloo under licence." Never display `SiteTelephone` |
| 5 | **Palma** (`palma.md`) | food only | Metro de Palma M1 and M2 from OSM, ~16 stations inside | The Consell de Mallorca's register, 4,372 active; 13% own coordinates, the rest joined to Catastro's INSPIRE addresses (74.0% placed on the brief's run) | The three licence calls are ANSWERED (owner): display GOIB's and Catastro's credits, the update date and a modification statement. Catastro needs `truststore`, never verification off. **Never load `Explotador/s`.** Night venues (~31) are food under R5 |
| 6 | **Yokohama** (`yokohama.md`) | **personal services only**, the first page not built on food; it says no food register is published | MLIT N02, 138 stations, Japan's standing rule | The city's 生活衛生 registers, 7,896 premises; the shared `japan_register` join (~98-100%) | Follow the `japan-city` skill. ⚠️ `city_rows` reads zipped .xlsx only and these zips hold CSVs: extract them, or change the shared code and drift-check the six built Japanese cities. **Never load 申請者氏名, 申請者役職 or 施設電話番号** |
| 7 | **Hiroshima** (`hiroshima.md`) | food + partial food retail, no personal services | MLIT N02: the Astram Line (22) and JR (39) inside the city; whether Hiroden's streetcars are drawn waits on the tram decision (confirm with the owner) | The city's counter list (7,479 restaurants) + MHLW's online filings (5,195), 1.2% overlap, 95-96% joined | The city list's PDL 1.0 coverage (see below). `japan-city` skill. Never read an operator column on the 個人 sheet or MHLW's 法人名/住所/phones |
| 8 | **Gyeonggi satellites** (`gyeonggi.md`) | three buckets, SEMAS | per city | SEMAS's 상가(상권)정보, the module Goyang, Seongnam, Yongin, Suwon and Bucheon use | **Which satellites, if any: the owner's call** (below). Region `Seoul Capital Area` |

**Suggested order**: Ottawa first (its feed may vanish), then Minneapolis and
Pittsburgh (US, OSM rail, the same shape as the light-rail builds), then
Kitchener–Waterloo, Palma, Yokohama and Hiroshima, and the Gyeonggi row last,
once the owner has said which satellites.

## Owner calls still open (bring them when you report ready)

1. **Gyeonggi: which further satellites, or close the row.** The owner chose
   Goyang, Seongnam and Yongin, then Suwon and Bucheon (all built). The
   brief's table ranks the rest: Hwaseong (19,499 storefronts, 7 stations),
   Namyangju (17,756, 17), Ansan (15,743, 12), Anyang (14,815, 7), Uijeongbu
   (12,438, 20), Gimpo (11,453, 9: its Goldline was screened EDGE).
   **Recommendation to put**: Namyangju, Ansan and Uijeongbu, the three with
   12 or more stations, each on its own page; close the row after them.
2. **Hiroshima: the city list's licence.** DataEye names PDL 1.0 for the
   dataset, but the full-list file has no DataEye entry of its own and sits on
   a page that declares no licence. The permissive reading (the dataset-level
   PDL 1.0 plus the page calling the list open data) is much better supported.
   **Recommendation**: build on it, as the other Japanese cities were, since
   outreach is the last resort. Asking the city (食品指導課) is the
   alternative.
3. **Downloads and write-ups pre-approved or per city** (see the top).

## Gates per city (what the light-rail builds ran, in order)

`check_personal_exposure.py <city>` (add it to REGISTRIES first; read every
flagged name; verdict in DECISIONS) → `check_provenance.py` (commit outputs
for it to pass) → `check_scope_disclosure.py` (property F: a city that thins
stops names them) → `check_inconsistency_list.py` (tables A-D, lists 1, 7
and 8 of `docs/map_inconsistencies.md`) → `check_master_list_counts.py`
(move the city's row into Band B's built table, fix every count line) →
`readme_cities.py` → `check_macro_facts.py --write` → **commit** →
`drift_check.py <city> --jobs 1`, then `git checkout -- outputs/` if no
drift → `check_ring_shares.py --write` → commit → `git fetch` and merge
origin/master → `check_all.py` → `check_deploy_imports.py --ref HEAD` →
push → READY notice.

**New since the light-rail builds: `check_category_continuity.py`** (in
`check_all`). A new taxonomy module needs a column in
`scripts/category_continuity_table.py` answering all 28 rules (`loc`,
`absent`, `outside`, `exception`, or `pending` for a departure the owner has
not ruled on). **A new `pending` row must also go in `AWAITING_OWNER`**, or
the table marks it "fix approved (owner)", which the owner never said. The
`add-city` and `premises-taxonomy` skills describe it.

## Lessons from the light-rail builds (in DECISIONS, 2026-09-29)

- **Measure the city boundary against TIGER (US) or the national layer
  before trusting OSM.** Houston's OSM relation lacked 156 km² of annexed
  land; Buffalo's city layer was really the county's. Gate the polygon's area.
- **A postal city is not the city**: point-in-boundary after placing
  (Sacramento dropped 125, Houston 608).
- **A register's legal form is better than a name test.** Where the register
  records it (Houston's organisation type, Denmark's form), a person's
  business shows its address; general partnerships count as persons
  (Denmark, owner). Where it does not (Sacramento), `looks_personal` names
  show the business type. APT and TRLR addresses are homes; UNIT and SPC
  usually are not (measure).
- **Never load a column that can identify a person, even as a key**: Texas
  taxpayer numbers embed a Social Security number. Use the portal's row id.
- **The operator's station count is gate 3**; a brief's per-line figure can be
  wrong while its total is right. Staggered platforms (Houston's Main Street
  Square, 267 m) are allowed by name, never by loosening the gate.
- **Line colours through `linecolour.py`, never an agency's where it has a
  data agreement**: a pure red and a mid green sit too close to the food and
  personal pins; aim for ΔE 45 or more.
- **Name the placed file `businesses_geocoded.csv`**: `check_macro_facts.py`
  reads that name for any city with a placing step.
- **A thin bucket is not a structural gap**: table B's note must not say
  "only", "No …" or "merged" unless the tier is `narrowed`.
- **A page's fetch date should read provenance `as_of_date`**, not a file's
  UTC timestamp (Houston's evening fetch showed the next day).
- **Macro labels**: every new city needs its label width MEASURED in the
  local app (canvas `measureText`, `600 14px "Space Grotesk"` after
  `document.fonts.load`, with Prague 47.3 and Tokyo 40.5 reproduced) before
  `check_macro_labels.py` will score it; sweep offsets with `python -B` (a
  stale .pyc serves the old offset). Regions: Minneapolis and Pittsburgh
  "United States East" (only California is West); Ottawa and
  Kitchener–Waterloo "Canada East"; Palma "Europe"; Yokohama and Hiroshima
  "East Asia" (Yokohama sits beside Tokyo: expect a label fight); the
  satellites "Seoul Capital Area".
- **The browser preview reads the worktree's own `.claude/launch.json`**:
  create a temporary static-server entry, and delete it after.
- **One heavy job on the machine at a time, announced to every live session
  before and after** (a large join, a geocode, a drift check that reads
  national files). `data/` is shared between worktrees: never re-run another
  city's step. No backslash or backtick in a Bash command: write a scratchpad
  script. Commit messages via `-F`, with the git identity per command:
  `git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com`.
  Stage files by name.
