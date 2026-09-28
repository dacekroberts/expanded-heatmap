# Handoff - build role (from "Main Build", 2026-09-27, late)

Written for a FRESH build session. Read it once and follow the pointers.
When a priority is done, delete its section rather than adding an addendum.

## Where things stand

- **Monterrey (Regional), Daegu and Busan are LIVE** (pushed `9dc08de`,
  rebooted by the owner, live-checked; record `0deab2e`). DECISIONS
  2026-09-27 has the build, publish and live entries for each.
- **New shared code:** `pipeline/countries/korea.py`, Seoul's step-2 rules for
  every later Korean city. It raises on a renamed column, an unguarded phone
  column (`전화` or `...tel`), a blank sub-type column, a 구-only address
  regex and undeclared address masking. Seoul keeps its own step 2.
- **The tram rescopes' light and medium batch is LIVE** (Montréal, Rome,
  Madrid, Paris, SF; `791fa04`). The heavy category stays held
  (`docs/handoff_staging_2026-09-27.md`, priority 5).

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
