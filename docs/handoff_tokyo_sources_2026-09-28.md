# Handoff - Tokyo's missing wards: licence reads, PDF extraction, re-probes (from "Fukuoka handoff", 2026-09-28)

Written for a FRESH research session in the `tokyo-sources` worktree. Read it
once and follow the pointers. When a section is done, delete it rather than
adding an addendum.

## Why this exists

Tokyo is the last Japanese city (owner). Its brief
(`docs/build_briefs/tokyo.md`) found food-permit lists for 8 of the 23 special
wards; the rest are PDF-only, stale, partial, request-only or not found. The
build session (`worktree-japan`, "Fukuoka handoff") is writing the
`tokyo-ward` skill and a per-ward share check meanwhile. **This session finds
out, ward by ward, whether any missing ward can join the map** - before the
Tokyo build starts. The owner's decision of 2026-09-28: **stations in a ward
with no business data are drawn hollow and labelled "no business data"**,
unless this session finds the data.

## The job, in the owner's order

1. **Licence reads** (the `licence-read` agent, ONE source per call; never a
   batch). The PDF-only full lists first, since only a permitted licence makes
   extraction worth doing:
   - **Ōta** (13111): full list, 93 + 16 pages.
   - **Arakawa** (13118): 55 pages.
   - **Sumida** (13107) and **Adachi** (13121): new permits only - read them
     only if a full list turns up beside them; new-only lists fail the owner's
     rule below.
   - **Kita** (13117): its page says "not open data". Confirm that in one
     read; if it holds, it is out.
2. **PDF extraction**, only for a ward whose licence permits reuse and
   modification. Write a `pdf-register` skill from the first one: extract the
   table rows to CSV (the tool, the page-by-page row count checked against
   the PDF's own totals, header rows repeated per page, wrapped cells), then
   the JOIN with `scripts/screen_japan_join.py` (add a key per ward) and the
   share of the official count (yearbook table 19-8,
   `data/tokyo/raw/tn24qv190800.csv`). Operator columns in a PDF are read in
   memory for the name rule only, never kept (owner 2026-09-27).
3. **Re-probes** (`reprobe-city`) for the three wards where nothing was found:
   **Bunkyō** (13105), **Suginami** (13115), **Katsushika** (13122). Ask each
   ward's OWN host, enumerate its whole catalogue, read who a 403 is for, look
   for a second shape. Bunkyō first: it is central (with Chiyoda and Toshima
   it is the hole in the middle of the map).
4. If time allows: re-check the stale and partial wards for a newer full list -
   **Nakano** (to 2023-06), **Shinagawa** (since 2024-04), **Itabashi** (since
   2025-04), and **Shinjuku** (a 2026 CSV on its portal would replace the 2023
   snapshot).

## What NOT to do (the owner's standing calls)

- **Outreach is the last resort.** Chiyoda, Toshima, Nerima and Edogawa
  release their lists only on request: the drafted requests stay PARKED
  (`docs/gated_access.md`). Do not contact any agency.
- **A ward joins the map only with a full, current list** (2026-09-24).
  Partial, first-permit-only or stale lists are recorded, not used (Meguro's
  first-permits list is the one accepted exception, at its measured share).
- **The COVID-era lists are not used** (2026-09-24), whatever their licence.
- **Downloads need the owner's OK**: name the file, source and size first.
- Published prose waits for the owner; so do judgment calls (recommend, then
  wait).

## The output: one ward card per ward

The build reads these; write them into a new section of
`docs/build_briefs/tokyo.md`, "Ward cards", one table row or block per ward,
so the `tokyo-ward` skill can consume them unchanged:

| Field | Meaning |
|---|---|
| ward, code | 大田区, 13111 |
| verdict | **ON** (full, current, permitted) / **OFF** (why, in one phrase) / **OPEN** (what is still unknown) |
| file(s), host, size | exact URLs; the host is the ward's own, or one the ward's own pages name |
| format | CSV / XLSX / PDF (pages); encoding; header shape; address layout (split / one string / starts at the town) |
| as of | the list's own date |
| closures | a closure column (Shibuya's 廃業日) or none |
| operator columns | their exact names - the name rule reads them in memory |
| own coordinates | columns, if any (a check on the join, never the map's source) |
| licence | the verdict shape from `licence-read`, and the credit it prescribes |
| join | block / chōme / none, from `screen_japan_join.py <key>` |
| share | of the yearbook's FY2024 飲食店営業 count for the ward |
| personal services | the ward's barber / beauty / laundry registers, if any, and their date |

## Where things stand

- **Worktree:** `.claude/worktrees/tokyo-sources`, branch
  `worktree-tokyo-sources`, from `origin/master` at `a21bf37`. `data/` and
  `.venv-lean` are junctions to the main checkout's - **unlink them alone
  before any removal** (`docs/session_roles.md`). Ward files belong in
  `data/tokyo/raw/<code>/`.
- **Paths this session owns**: `docs/build_briefs/tokyo.md` (the Ward cards
  section and corrections), the Tokyo rows of `docs/data_sources/japan.md`,
  `docs/gated_access.md`, new keys in `scripts/screen_japan_join.py`,
  `data/tokyo/raw/`, and a new `.claude/skills/pdf-register/`. **Not**:
  `pipeline/countries/*`, `.claude/skills/japan-city/`, `.claude/skills/tokyo-ward/`
  and `scripts/japan_ward_table.py`, which the build session is changing on
  `worktree-japan`.
- **Pacing:** `get_usage` between wards; at 90% of the 5-hour window finish the
  current ward, commit clean and stop with a one-line next action.

## Before starting

- **Tell "Fukuoka handoff" (the build session) and "Project cleanup session"
  your session name** (`ListAgents`).
- **Git:** identity per command only
  (`git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`);
  never change git config, amend or force-push; stage by name; commit messages
  with backticks through a file (`git commit -F`). Trailer:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Never push this branch to master.** Back it up with
  `git push origin worktree-tokyo-sources`. Each finding is logged in
  `DECISIONS.md` as it is made (`decisions-entry`), and
  `python scripts/decisions_index.py` run after.
