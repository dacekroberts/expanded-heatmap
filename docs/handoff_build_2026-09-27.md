# Handoff - build role (Main Building Session, 2026-09-27)

Written for the session that takes over this worktree. Read it once and follow
the pointers for detail. When a priority is done, delete its section rather
than adding an addendum.

## Before starting

- **Work in `.claude/worktrees/monterrey` on `worktree-monterrey`.** Check with
  `git branch --show-current` and `git worktree list`. The branch is committed
  and NOT pushed. Its base is `b90e1af`, and origin/master has moved since
  (mobile mode removed, whole-city layers restored, renderer changes).
- **`data/` in this worktree is a JUNCTION** to the main checkout's `data/`,
  where Monterrey's raw files live. Remove a junction only with
  `[System.IO.Directory]::Delete(path, $false)`, never recursively.
  `git status` shows it as `?? data/`. That is the junction, not uncommitted
  work: never stage it.
  `.venv-lean` is NOT linked yet: link it the same way before
  `check_deploy_imports.py` or `deploy-verify`.
- **A temporary `monterrey-static-tmp` entry** (port 8823) in the MAIN
  checkout's `.claude/launch.json` serves this worktree's `outputs/`. The
  owner's standing OK covers stepping out of the worktree to add or remove
  `-tmp` entries: `ExitWorktree` keep, edit, then `EnterWorktree` with the path.
  A session STARTED inside this worktree may not be able to step out that way.
  If so, put the preview entry in this worktree's own `.claude/launch.json`.
- **Never check out `master` here.** The main folder has it checked out, and
  git will not put one branch in two worktrees. It is never needed: merge
  `origin/master` into this branch, and publish with
  `git push origin worktree-monterrey:master`.
- **The main folder's local `master` is ~310 commits behind origin.** Never
  read the main folder's files as current. Use `origin/master` (`git show`,
  `git diff`) after a `git fetch`.
- **Tell Staging and Cleanup your session name** (from `ListAgents`) so their
  relays reach you. They addressed the old one as "Main Building Session".
- Check `get_usage` before big work, and confirm this week's cap with the owner.

## Priorities, in order

1. **Next builds: the owner's small-city picks.** Staging is screening; the
   owner relays the picks. They join Monterrey's batch. Where each lives is
   the owner's call; the recommendation is this branch, pages from 48.
   Monterrey needed these records, and each city will too: provenance rows,
   scope disclosure, inconsistency rows, privacy entry, label width and
   placement, DECISIONS, PLAN.
2. **Waiting on the owner's yes (asked, not answered): merge origin/master
   into this branch now.** Then:
   - **Fix two lines** made stale when master restored Mexico City's and
     Guadalajara's whole-city layers. In `docs/excluded_categories.md`'s
     Monterrey section: "ON here, unlike the other two Mexican cities". In
     `docs/project_context.md`'s Monterrey bullet: "Unlike the other two
     Mexican cities...".
   - **Resolve conflicts** with Staging's notes in PLAN's Monterrey item
     (brief line 111 → take master's; band counts → take master's numbers,
     then A −1, Candidates −1, Built +1). Resolve DECISIONS with
     `scripts/merge_append_only.py`.
   - **Re-check** with `check_render_current.py` and `check_inline_arrays.py`,
     and re-render Monterrey if the renderer changed. Re-run
     `check_macro_labels.py`, because Monterrey moved Guadalajara's and Mexico
     City's pills.
3. **Batch publish, when the owner says.** The steps are in PLAN's Monterrey
   item and the `publish-city` skill. A reboot is needed, because
   `cities.py` and `components.py` changed.

## Where the detail lives

- **Monterrey:**
  - DECISIONS 2026-09-27, "Monterrey (Regional) built..." (its counts are the
    drift baseline, `outputs/monterrey/baseline.json`)
  - PLAN's Monterrey item
  - `docs/data_sources.md` (three rows)
  - `docs/build_briefs/monterrey.md`
- **iPhone blank maps:** resolved. See memory `project_mobile_map_memory.md`
  and `docs/handoff_2026-09-27.md` (cleanup).

## Rules this session worked under, beyond CLAUDE.md and memory

- **Git:**
  - Identity per command only:
    `git -c user.name=dacekroberts -c user.email=49654908+dacekroberts@users.noreply.github.com commit ...`
  - Never change git config, amend, or force-push.
  - Stage by name after reading `git status`.
  - Push with `git push origin <branch>:master`, `git fetch` immediately
    before.
  - Trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Downloads** need the owner's explicit OK every time (file, source, size).
- **Page and notice prose** is drafted in chat for approval before it is
  written.
- **Forbidden columns:** Riga's excise columns `Nodoklu_maksatajs` and
  `NMR_kods` are never read. Seoul's `전화번호` is never read or published.
- **Leave alone:**
  - `opd.pdf` at the main checkout's root (a stray from another session; the
    owner decides)
  - the Taipei PDF in `data/taipei/raw` ("leave pdf")
  - the two personal files in the home directory

## If the owner asks for a summary of a past day's work

Sources, most authoritative first:

- `DECISIONS.md`'s dated sections (118 for 2026-09-24 alone)
- `git log --all --since=... --until=...` (191 commits that day)
- PLAN's ticked items and the dated `docs/handoff_*.md` files (in git history)
- the raw session transcripts: `.jsonl` files under `~/.claude/projects/`, one
  folder per worktree, searchable with the app's transcript tools

Three caveats:

1. **A date is several sessions.** Build, staging and cleanup run in parallel,
   so a summary by date combines them unless the owner names one ("the build
   session's 9/24 work", "Riga's build"). Ask which, or say that it combines
   them.
2. **Hand the reading to a subagent and keep only its summary.** A day can be
   100+ DECISIONS sections and ~200 commits, and a transcript is far larger.
   Reading that in the main session spends the context the builds need. Have
   an `Explore` or `general-purpose` agent read the sources and return a
   summary with citations. Go to the transcripts only when the owner wants the
   conversation itself, not the decisions.
3. **Cite, so it can be checked.** DECISIONS and git are the record;
   transcripts are raw. Every claim in a summary names the DECISIONS entry or
   commit behind it.

## A correction for other handoffs

This session has no live Riga work. The `riga` worktree was removed on
2026-09-27 with everything on master (`20af557`). Riga's re-render for
`JSON.parse` is free for any session.
