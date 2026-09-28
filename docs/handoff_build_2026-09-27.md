# Handoff - build role (from "Main Build", 2026-09-27, late)

Written for a FRESH build session. Read it once and follow the pointers.
When a priority is done, delete its section rather than adding an addendum.

## Where things stand

- **Monterrey (Regional), Daegu and Busan are LIVE** (pushed `9dc08de`,
  rebooted by the owner, live-checked; record `0deab2e`). DECISIONS
  2026-09-27 has the build, publish and live entries for each.
- **Worktrees:** `daegu` and `busan` are retired, with their branches deleted
  and both confirmed contained in master. `monterrey` remains only because the
  old session ran in it. Its branch is fast-forwarded to master and holds
  nothing unmerged. **Retire it** once no session uses it: run
  `scripts/check_worktree_data.py` on it, remove its `data/` junction with
  `[System.IO.Directory]::Delete(path, $false)` (never recursively), then
  `git worktree remove` and delete the branch.
- **Leftover for the owner or Cleanup:** the `monterrey-static-tmp` entry in
  the MAIN checkout's `.claude/launch.json`. A session started inside a
  worktree cannot reach it.
- **New shared code:** `pipeline/countries/korea.py`, Seoul's step-2 rules for
  every later Korean city. It raises on a renamed column, an unguarded phone
  column (`전화` or `...tel`), a blank sub-type column, a 구-only address
  regex and undeclared address masking. Seoul keeps its own step 2.

## The next job: tram rescopes (owner's instruction, relayed by Staging)

**The specs are in `docs/tram_rescope_specs.md`** (Staging wrote them; you
implement them). The owner's pacing for this job is to **start cheap and
monitor `get_usage` until the 5-hour window reaches 90%**. Check between
cities. At 90%, finish the current step, commit clean, and stop with a
one-line note naming the next action.

- **Use one new worktree from master** (e.g. `worktree-trams`), **HELD for
  review time.** It rewrites `outputs/`, so nothing merges to master until the
  owner calls review time (`docs/review_time.md`).
- **Order:** REM → Rome 8 → Madrid Metro Ligero → Paris T3a/T3b → SF F Market.
- **Every drawn line gets a label AND a legend entry.** New downloads go in
  `fetch_sources.py` with the owner's OK (file, source, size). OSM goes through
  `pipeline.osm.fetch`.
- **Traps named in the relay** (the specs have the detail):
  - **REM:** needs a new source. Try the operator's or ARTM's GTFS with a
    `licence-read` first, else OSM via `osm-rail`. The scope is the
    agglomeration, so the Brossard and Laval stops are excluded. Check the
    current line numbering before labelling.
  - **Rome 8:** the cached OSM has no tram relations, so fetch them. Pick the
    relation pair (base, 16 stops; or "prolungato", 26) that matches the
    GTFS's route 8, and key on relation ids. Don't draw 2/3/5/14/19, which
    have 0 trips.
  - **Madrid:** attribute stations to lines from CRTM's M10_Tramos. An ML2
    stub inside Madrid is an owner call. Take the colour from M10_Lineas and
    check it against Metro Line 1.
  - **Paris:** T3a and T3b are ΔE 0 against Lignes 5 and 12, so override both
    colours, clearing the lines and the pins (as with the bis lines). T2 and
    T9 are stubs, recommended out, and are an owner call at review. Match
    `route_type` 0 plus the exact short name.
  - **SF:** match `route_id` F exactly. The cable cars share its #B49A36 and
    stay out.
  - **D.C. Streetcar:** dropped (DDOT ended service 2026-03-31). Change its
    "—" in `docs/map_inconsistencies.md` to "no longer operating". Don't draw
    the Capitol's private people movers, which OSM tags `light_rail`.
- **Re-rendering touches live cities.** Run `drift_check.py` per city, and
  `git checkout -- outputs/` after a zero-drift run.

## Before starting

- **Tell Staging and Cleanup your session name** (from `ListAgents`). The
  old one was "Main Build".
- **Never check out `master` in a worktree.** Merge `origin/master` into the
  branch, and publish with `git push origin <branch>:master` after a
  `git fetch` in the same breath.
- **Previews:** the preview tool reads `.claude/launch.json` in the worktree
  the session STARTED in (gitignored there). Put a `-tmp` entry in that file,
  and remove it when done.
- **A worktree needs `data/` (and, for `check_deploy_imports.py`,
  `.venv-lean`) linked as junctions** to the main checkout's. `git status`
  shows `?? data/`: never stage it.
- **No weekly cap this week** (owner). Raise the cap and efficiency together
  once the weekly passes 60%; it was 22% at this handoff.

## Rules this session worked under, beyond CLAUDE.md and memory

- **Git:**
  - Identity per command only:
    `git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`
  - Never change git config, amend, or force-push.
  - Stage by name after reading `git status`.
  - Trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
  - A commit message with backticks goes in a file (`git commit -F`); the
    heredoc hook refuses them inline.
  - `git branch -d` judges "merged" against the current branch, not master.
    Confirm with `git merge-base --is-ancestor <branch> origin/master` before
    `-D`.
- **Downloads** need the owner's explicit OK every time (file, source, size).
- **Published prose** (pages, blurbs, notices, `excluded_categories.md`) is
  drafted in chat and waits for the owner's review.
- **Forbidden columns:** Riga's `Nodoklu_maksatajs` and `NMR_kods`, Seoul's
  `전화번호`, Daegu's `소재지전화` and Busan's `sitetel` are never read.
- **Leave alone:** `opd.pdf` at the main checkout's root, the Taipei PDF in
  `data/taipei/raw`, and the two personal files in the home directory.

## If the owner asks for a summary of a past day's work

- **Sources, in order:**
  - `DECISIONS.md`, with past weeks in `docs/decisions/`
  - `git log --all --since=... --until=...`
  - PLAN's ticked items
  - the transcripts, only if the owner wants the conversation itself
- **Hand the reading to a subagent**, one per day, and cite a DECISIONS entry
  or commit for every claim.
- **A date is several sessions**, so say the summary combines them.
