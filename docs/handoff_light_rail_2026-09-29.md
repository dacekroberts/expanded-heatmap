# Handoff: build Aarhus, Buffalo, Sacramento and Houston (Band A light rail)

Written 2026-09-29 by the Suwon/Bucheon/Bergen build session
("Suwon Bucheon build", worktree `.claude/worktrees/suwon`). The owner gave
this session Band A's five light-rail cities (relayed by the Staging
session), then chose: Bergen here, the other four in a fresh session with
this handoff.

## State when this was written

- **Built and pushed, all waiting for ONE batch review** (owner: the review is
  deferred until the light-rail cities are built, then builds pause):
  - `origin/suwon`: Suwon, page 69
  - `origin/bucheon`: Bucheon, page 70
  - `origin/bergen`: Bergen, page 71
- Each branch counts its own figures (69 built on each). The **Project cleanup
  session** reconciles page numbers, Built / Band A counts and the notices
  once, in the review merge. Record your branch's own figures and send
  cleanup a READY notice per city (push to `origin/<city>`, never master).
- **Next free page numbers: 72, 73, 74, 75** (check `app/pages/` and the
  pushed branches first). The scaffold picks the next number on ITS branch,
  so it will pick 69: rename the page and fix `app/cities.py`'s `page`.

## First things

1. Read `CLAUDE.md`, `docs/project_context.md`, then each city's brief:
   `docs/build_briefs/{aarhus,buffalo,sacramento,houston}.md`. The owner's
   final answers are on master (5e717f5 and after).
2. Tell the **Project cleanup session** and the **Staging session (trams)**
   your session name and that you build the four light-rail cities.
3. **Ask the owner for each city's downloads** before any fetch (state
   the sources and sizes). This session's approval covered Bergen only.
4. Order (Staging's recommendation, the owner's instruction): **Aarhus,
   Buffalo, Sacramento, Houston**. One branch per city, each new from
   origin/master: `git switch -c <city> origin/master`, then
   `git branch --unset-upstream`, and push with `git push -u origin <city>`.
5. `python scripts/brief_check.py <city>` before any code. Overpass timeouts
   pass on a re-run.

## Owner calls already made (2026-09-29, all in DECISIONS)

- **Aarhus**: 20 stations, the new city tramway only, halved rings
  0.05/0.1/0.2/0.3 (owner confirmed). Rail from OSM. **NEVER fetch
  Rejseplanen's GTFS**; frequency from Midttrafik's own timetables. Place
  through OSM's `osak:identifier` joined on the DAR HUSNUMMER id, not the
  adgangspunkt id (97.0% against 80.1%). Build on the cached CVR generation
  505 and DAR generation 761, **shared with Copenhagen: don't refresh**. Two
  spelling aliases: G. Clausens Vej and Lisbjerg-Terp. Copenhagen's CVR chain
  reads about 5 GB of national files: **a HEAVY JOB, announce it**.
- **Buffalo**: rail from OSM, relations 3517747 and 11364343, `#004990`.
  Disclose the 20-minute service. Every licence says "Active": filter
  `expdttm >= fetch date` (Chicago's rule). Scope the NYS food and salon rows
  by point-in-boundary; salon renters excluded. Display `businessname`
  (the trade name; `dbaname` is usually the legal entity). New York's
  multi-source pattern (`multi-source-city` skill).
- **Sacramento**: the City's Open Data Terms indemnity is ACCEPTED (owner).
  Addresses through the **US Census geocoder** (owner), NOT the City's All
  Addresses layer. **NEVER load `Principal_Owner_*`, `Primary_Phone_number`
  or `Mail_*`.** Apply the expiry date. "ON FILE" rows are unmappable by
  design. Rail from OSM. Blue and Gold every 15 min by day, 30 in the evening.
  **BUILD-TIME CHECK: SacRT lists no Green Line** - confirm whether it still
  runs before counting its 9 of the 39 stations; bring the answer to the owner.
- **Houston**: rail from OSM. Lines labelled "Red Line", "Green Line",
  "Purple Line". Build as scoped; **the in-ring share is about 7%: state it on
  the page** (owner). Comptroller `jrea-zgmq`: read only the `outlet_*`
  columns and `taxpayer_organization_type`, **never `taxpayer_name` or
  `taxpayer_address`**. Drop NAICS 454 and 812930. For organisation type IS,
  suppress the name, and drop rows whose point is Residential.
  `outlet_naics_code` is a NUMBER column. Join to the City's public-domain
  Site Addresses bulk export, the Census geocoder for the residue.
- **All five take the light-rail network colour** in cleanup's held
  macro-map work (`rail_extra`: "Trams", as Calgary and Bergen). Say so in
  each READY notice.

## Macro-map label widths, already measured

Measured 2026-09-29 in the local app's own document (lean venv), canvas
`measureText` at `600 14px "Space Grotesk"` after `document.fonts.load`,
with Prague 47.3, Tokyo 40.5, London 50.9, Glasgow 56.8 and Oslo 29.0
reproduced exactly:

| City | Width (px) |
|---|---|
| Aarhus | 46.9 |
| Buffalo | 48.8 |
| Sacramento | 81.3 |
| Houston | 56.9 |

Add each to `scripts/check_macro_labels.py`'s `TEXT_WIDTH` with that
provenance comment, and replace the scaffold's "STARTING VALUE, NOT A
MEASURED ONE" comment in `app/cities.py` with a measured-and-scored one.
The check does not model the macro map's "Light mode" button (Oslo's
lesson): look at a new region-edge city at 375 px in the browser.

## Per-city gates (what this session ran for each)

- `check_personal_exposure.py <city>` (add the city to its REGISTRIES first);
  verdict in DECISIONS.
- `check_provenance.py` must name the city OK. Its citation check wants the
  licensor's NAME in the same table row as a notice number.
- `check_scope_disclosure.py`, `check_inconsistency_list.py` (rows in tables
  A-D of `docs/map_inconsistencies.md`; table D's "Date on page" is B, T or
  —), `check_master_list_counts.py` (a built Band A city keeps its row,
  struck through and marked ✅, in the built table; fix both headings and
  the Total row).
- `readme_cities.py`, `check_macro_facts.py --write`, then commit, then
  `drift_check.py <city> --jobs 1` (announce it), `git checkout -- outputs/`
  if no drift, `check_ring_shares.py --write` (after the commit, so the
  map's blob is recorded), `check_deploy_imports.py --ref HEAD`,
  `check_all.py`.
- Draft the page text and any notice widening in chat; wait for the owner's
  yes before writing it.

## Traps hit today

- **The worktree's `.claude/launch.json` is what `preview_start` reads**
  (gitignored). This session added a static server and a lean app entry
  there, then removed them; re-create them for a browser check.
- **Overpass 504s** come in waves; a trivial query that 504s on both mirrors
  answers minutes later. Re-run the fetch; the cached files are skipped.
- **Bucheon's box brought in seven undrawn lines**: step 1 refuses any
  relation it cannot place, so name each in `NOT_DRAWN`.
- **The Norway register's shared filter changed since the screen**
  (catering now excluded): expect a screen's counts to move a little.
- **A cached file's date is not the provenance run's date**: Bergen's page
  reads `files_utc` from provenance so it shows when each file was fetched.
- No backslash or backtick in a Bash command (the hook blocks it): write a
  scratchpad script. Commit messages via `-F`. Git identity per command:
  `git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com`.
  Stage files by name.
- **Re-fetch and merge origin/master immediately before every push**; the
  master list and DECISIONS conflict often (`merge_append_only.py` for
  DECISIONS; for the master list, keep master's rows and re-apply your move).
- `data/` is shared: never re-run another city's step. One heavy job on the
  machine at a time, announced to every live session before and after.
