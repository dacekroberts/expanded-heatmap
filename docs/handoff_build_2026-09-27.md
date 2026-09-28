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

## Tram rescopes: BUILT, on `worktree-trams`, HELD for review time

All five are committed on `worktree-trams` (`c8c1c53` through `f3e051d`),
one DECISIONS entry each, and `check_all.py` passes 19 of 19. Nothing is
merged. At review time the batch lands once through `publish-city`: one
deploy-verify (`scope: map-chrome` or `full`, the owner's pick), one reboot.

- **Montréal:** the REM, one line "REM (A1, A3, A4)" (owner), from the
  operator's own GTFS (CC BY 4.0, recorded). 78 stations.
- **Rome:** tram 8, the base service, thinned to 7 of 16 stops. 94 stations.
- **Madrid:** ML1 only (ML2/ML3 stubs, owner). 200 stations.
- **Paris:** T3a and T3b in this project's own colours. 280 stations.
- **SF:** the F, thinned; two stops stacked over subway stations merged.
  57 stations.

**NOT app-free:** the batch needs a new Réseau express métropolitain credit
(notice 50) and an amended CRTM credit (notice 20, now covering ML1) in
`app/components.py`. Both are written on the branch, in wording the owner
approved 2026-09-27. So the publish runs
`check_deploy_imports.py` and needs a reboot. Landing: DECISIONS.md conflicts
with master; resolve it with `scripts/merge_append_only.py`, then
`decisions_index.py` (Cleanup's review).

**Waiting on the owner at review:**
- the page text, blurbs and map titles for all five (still name the old
  networks), the REM's new CC BY notice, and the `excluded_categories.md`
  sentences: drafted in chat, not yet written;
- T3a's orange reads close to Ligne 5's in the render (ΔE 13.9);
- whether the F's Market St stretch, which runs over the subway, should
  count at all (four stops 170–282 m from subway stations).

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
