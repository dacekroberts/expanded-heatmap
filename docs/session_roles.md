# Working in more than one session

How concurrent Claude sessions divide this repo without colliding. Written
2026-09-21, after a period of two sessions sharing one working tree, which
cost an unreviewed commit (`38d4bd0` swept another session's uncommitted work
into a `git add -A`), an explicit-path staging discipline on every commit, and
several stretches where one session sat idle waiting for the other.

## If only one session is running, it does all of this

**This file describes a division of labour, not a division of capability.** A
single session reads `CLAUDE.md`, then `add-country` if the country is new,
then `add-city`, then `scaffold-city`, and builds the city end to end. Nothing
below is a precondition, a handoff gate, or a thing to wait for.

In particular: **a build brief is a cache, not a requirement.** If
`docs/build_briefs/<city>.md` exists, it is Step 0's answers already banked. If
it does not, `add-city` Step 0 says how to produce the same facts. Never stall
waiting for a staging session to materialise.

## Roles, not windows

A session is not "the Canada window". It **claims a role**, and any window can
claim any role — including after a restart, or as a third window opening later.
The role is declared once, in the first message of the session ("you are the
build session for Vancouver"), and it grants a set of paths.

**Ownership is by path.** That is the part that actually prevents collisions,
and it is why the scheme scales: two build sessions can run at once provided
they hold different cities, because their paths do not intersect.

| Role | Owns |
|---|---|
| **Staging / research** | `docs/`, `.claude/skills/`, screening `scripts/`, country profiles, Step 0 evidence, build briefs |
| **Build `<city>`** | `pipeline/<city>/`, `outputs/<city>/`, that city's `app/pages/` file, its row in `app/cities.py`, its taxonomy module |
| **App / chrome** | `app/` chrome, `pipeline/map_common.py`, `pipeline/theme.py`, `.streamlit/`, shared helpers under `pipeline/` |
| **Cleanup / audit** | **No exclusive paths** — see below. Owns the *checks*: `scripts/check_*.py` |

Shared pipeline code — `map_common.py`, `drift_check.py`, `pipeline/theme.py`,
anything under `pipeline/taxonomies/` that is not one city's module — belongs
to whoever claimed the app/chrome role, or to the staging session when no third
window exists. **It is never edited opportunistically mid-build by a session
that does not own it**, because it is the surface every other session's output
depends on.

## The cleanup role owns no paths, and that is deliberate

Its job is cross-cutting by nature — stale prose in `docs/`, a drifted count in
a licence table, a heading that stopped describing its contents, an empty
worktree directory. Allocating it paths would either take `docs/` away from the
research session or give it nothing to do. So it runs on different rules:

- **Sweep narrow and commit immediately.** Its only protection against a
  collision is a short window between reading a file and committing the fix. A
  two-hour sweep across nine files will meet somebody.
- **Verify against `origin/master`, never the local tree.** It reports on other
  sessions' work, so it is the role most likely to be reading a stale checkout.
  On 2026-09-22 two of three findings relayed between sessions were stale rather
  than wrong — both described a file that had changed by 339 lines since the
  reporting session branched.
- **It never merges a branch it does not own**, and reads the commit message
  before drawing conclusions from the branch graph. A branch held off master
  deliberately looks exactly like an abandoned one.
- **It does not edit a file another session has uncommitted**, and does not
  rewrite pipeline, taxonomy or step logic. A real bug there is handed over.
- **Its preferred output is a check, not a correction** — which is why it owns
  `scripts/check_*.py`. A correction fixes one instance; a check keeps finding
  the class after the session ends. `scripts/check_provenance.py` was written
  to close a gap a reader had already found by hand, and immediately found five
  more.

The skill is `.claude/skills/consistency-sweep/`, and it carries the defect
taxonomy — eight shapes, each with the real instance that produced it.

## Each non-primary session works in its own worktree

The primary session keeps the main checkout. Every other session gets one:

```bash
git worktree add .claude/worktrees/<role> -b worktree-<role>
```

Git refuses to check out `master` in two worktrees at once, so each is on its
own branch and merges back. That is the point: the merge is an explicit review
step instead of an implicit race.

**The standing assignments** - current state, so update this when one changes:

| Role | Worktree | Branch |
|---|---|---|
| Staging / research | `.claude/worktrees/staging` | `worktree-staging` |
| Cleanup / audit | `.claude/worktrees/cleanup` | `worktree-cleanup` |
| France kit, then the France builds (2026-09-29 kit; builds approved 2026-09-30) | `.claude/worktrees/france-kit` | `worktree-france-kit` for docs, skills and scripts; `france-build` for the builds, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's |
| Czech kit (2026-09-30: `docs/handoff_czech_batch_2026-09-30.md`) | `.claude/worktrees/czech-kit` | `worktree-czech-kit`; `data/` and `.venv-lean` are junctions to the main checkout's |
| UK six builds (released 2026-10-02: `docs/handoff_uk_six_2026-10-01.md`; one lead session with agents; registered 2026-10-02) | `.claude/worktrees/uk-six` | `uk-six-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-02:** pages **156** Manchester (Regional), **157** Birmingham (Regional), **158** Edinburgh, **159** Sheffield, **160** Nottingham (Regional), **161** Blackpool (Regional) (staging's pre-assignment); notices **84-96**, assigned in build order and kept contiguous (`check_provenance.py` D): Manchester 84 (Food Standards Agency) and 85 (Ordnance Survey), 86 NaPTAN for all six, then each city's Food Standards Agency or Food Standards Scotland notice and its Ordnance Survey one where it places at centroids |
| Japan batch builds, twelve cities (released 2026-10-02: `docs/handoff_japan_batch_2026-10-02.md`; one lead session with agents; registered 2026-10-02) | `.claude/worktrees/japan-batch` | `japan-batch-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-02:** pages **162-173** as pre-assigned (Matsuyama 162, Toyama 163, Kumamoto 164, Fukui 165, Nagasaki 166, Utsunomiya 167, Kitakyushu 168, Sakai 169, Hakodate 170, Kagoshima 171, Okayama 172, Kōchi 173); notice numbers **97-108**, one per city in the same order (Matsuyama 97 ... Kōchi 108), each city's list, MHLW where used, and MLIT, as notices 50-56, 75 and 76; claimed after the UK six's 84-96 |
| Seattle (Regional), then Tbilisi (released 2026-10-02: `docs/handoff_seattle_tbilisi_2026-10-02.md`; one lead session, Tbilisi queued) | `.claude/worktrees/seattle-tbilisi` | `seattle-tbilisi-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's |
| Japan wave 2, fourteen cities (released 2026-10-02: `docs/handoff_japan_wave2_2026-10-02.md`; one lead session with agents) | `.claude/worktrees/japan-wave2` | `japan-wave2-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's |
| Four extensions to built cities (released 2026-10-02: `docs/handoff_extensions_2026-10-02.md`; one lead session) | `.claude/worktrees/extensions` | `extensions-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's |
| Tram kit, the ten other T1 cities (2026-09-30: `docs/handoff_tram_kit_2026-09-30.md`; holding before builds) | `.claude/worktrees/tram-kit` | `worktree-tram-kit`; `data/` and `.venv-lean` are junctions to the main checkout's |
| Build `<city>` | `.claude/worktrees/<city>` | `<city>-build` - the name every build since Dublin has actually used, rather than the `worktree-<role>` form above. Delete the branch when the worktree goes: merged build branches have tended to outlive their worktrees |

**The cleanup role is moving to its row.** Until 2026-09-23 it ran in
`.claude/worktrees/practical-leakey-12a8a2` on `claude/practical-leakey-12a8a2`
- a name the desktop app generates for a session it expects to be short-lived.
That session became the standing role and never got a proper home. The next
cleanup session starts in `.claude/worktrees/cleanup`, created from `master`
with the command above, and the old one is **retired rather than moved**:
Windows refuses to move a directory a running process is using, and a session's
scratchpad and transcript are keyed to its worktree's path. Retire it by
closing that session, then, from the main checkout:

```bash
git pull --ff-only
git worktree remove .claude/worktrees/practical-leakey-12a8a2
git branch -d claude/practical-leakey-12a8a2
```

`-d`, never `-D`: it refuses to delete a branch holding commits that are not in
the branch you are on - `master`, from the main checkout - which makes the
deletion its own check. **Hence the pull first.** The branch has no upstream,
so `-d` compares it with the main checkout's LOCAL `master`, which is often
behind GitHub because sessions push from their worktrees and nobody pulls
there. Without the pull it refuses, correctly - those commits really are not in
that `master` yet - but it reads like a warning of data loss.

**Never remove a session's own launch worktree from inside that session.**
On 2026-09-23 a cleanup session that the app had launched in the wrong
worktree moved itself to `.claude/worktrees/cleanup`, then ran `git worktree
remove` on the worktree it had been launched in. Windows refused to delete the
folder, which the session still held open, but only after git had deleted
everything inside it and unregistered the worktree. A session loads its hooks
and skills from the `.claude/` of the folder it was **launched** in, not the
one it moved to, so that session lost `block_heredoc.py`. Every Bash call
failed from then on, and skills were at risk. Nothing was lost, because the
worktree was clean and at `master`, but the session could not continue.
Remove a launch worktree **after closing its session**, from the main
checkout, with the same commands as above.

`.claude/worktrees/` is gitignored. It is also worth adding to
`.git/info/exclude` on a working machine, because `.gitignore` only takes
effect in a tree that has this commit, and the main checkout may not yet.

**Commits survive a removal; gitignored files do not.** Commits live in the
shared object store, so `git merge worktree-<role>` followed by `git worktree
remove` loses no commit. But `git worktree remove` deletes ignored files without
asking, and `data/` is ignored - so a city's cache can exist ONLY in the
worktree that built it. On 2026-09-23 `lille` held the only Rennes and Lille
caches, and Rennes' feed is quota-limited. Before removing a worktree:

1. **Unlink every junction first, on its own, without recursion.** A worktree
   may link `data/<country>/raw` to the one shared national file instead of
   copying gigabytes - `lille`'s `data/france/raw` pointed at the 3 GB SIRENE
   pair in the main checkout. PowerShell 5.1's `Remove-Item -Recurse` can
   follow a junction and empty its TARGET, which here would have deleted the
   file every French city is built from. List them, then remove each link
   alone - `cmd /c rmdir <link>` deletes a junction and never its target:

   ```powershell
   Get-ChildItem -LiteralPath <worktree> -Recurse -Force -Attributes ReparsePoint
   ```

   **The WHOLE worktree, not just `data\`.** On 2026-09-24 five of seven
   retired worktrees also had `.venv-lean` as a junction to the main
   checkout's lean venv - a recursive delete through it would have emptied
   the environment every deploy check runs in. A pre-check that filtered on
   `data\` (or skipped `.venv*` by name) did not see them.

   That day the leftover folder was deleted recursively BEFORE its junction
   was noticed. The target survived - both SIRENE files kept their size and
   timestamps - which was luck, not procedure.
2. **Save the worktree's WHOLE `data/` first - every folder, not only built
   cities.** Copy what the main checkout lacks into the main checkout's
   `data/`, no-clobber (`cp -rn`), then run
   `python scripts/check_worktree_data.py <worktree>` until it passes: it
   refuses while any file is absent from main or has a different size there.
   A research worktree holds caches that no `fetch_sources.py` re-creates:
   national files (`data/japan`, `data/mhlw`), unbuilt cities, one-off probe
   downloads, archive-recovered files and stitched registers. **On
   2026-09-27 the old staging worktree was found gone with ~1.2 GB that
   existed nowhere else** - Japan's city registers, the ISJ/N02/N03/e-Stat
   files, and Helsinki, Tallinn, Vienna and part of Riga. The rule then
   read "any `data/<city>/`", which a national folder does not match.
   Copenhagen's cache (2026-09-24) was saved because someone looked. The
   same applies to a worktree removed by any other route (a session's
   worktree cleanup, a manual delete): run the check first.
3. Then the three commands above. If Windows leaves an empty folder behind,
   re-run step 1's listing on it before deleting it.
4. **`Filename too long` stops `git worktree remove` partway.** A worktree
   with its own `.venv-lean` holds Streamlit template paths over Windows'
   260-character limit, 263 in the first case (2026-09-24). Git unregisters
   the worktree and deletes what it can, then stops. Re-run step 1's listing
   over the WHOLE folder, then delete the rest with the long-path prefix:
   `cmd /c rmdir /s /q "\\?\<full path>"`. **An idle session that is still
   open keeps its launch folder locked**: the contents go and an empty
   folder stays until that session is closed. Leave it, and remove the empty
   folder afterwards.

**Page numbers pre-assigned (staging, 2026-10-02)**, so two batches building
at once never take the same "next free" number: the UK six **156–161**
(build order), the Japan batch **162–173** (its kit's table order),
Seattle (Regional) **174** and Tbilisi **175**. Notice numbers are claimed
here, by the session, before one is written, and the claims open are Japan
wave 2's notices 115–128 and the four extensions' notices 129–136 (both
pre-assigned 2026-10-02), and lane-app (cleanup batch, 2026-10-03): notices
137-140; the next claim starts at 141. Every block before those landed
2026-10-02 (the last notice landed then is 114; Tbilisi's unused 115–116 were
released and pre-assigned to Japan wave 2). Pages pre-assigned 2026-10-02:
Japan wave 2 176–189; the four extensions take no new pages.
Check D of `check_provenance.py` reads every range in that sentence and lets
a branch skip exactly those numbers; any other gap still fails. Keep the
ranges in that one sentence, and delete a batch's range once it lands.
**Scaffold with the reserved number:** `scaffold_city.py ... --page-number
<N>`. Without it the script takes one past the highest page on the session's
own branch, which is the collision. It refuses a number already taken. The
three info pages carry no number since 2026-10-02 (`About_the_Data.py`,
`What_Is_Excluded.py`, `Why_the_Maps_Differ.py`), so no block ever reaches
them.

## The shared files everyone appends to

`PLAN.md` and `CLAUDE.md` have no owner — every session writes to them.
**`DECISIONS.md` is written by the cleanup session only, since 2026-09-30
(owner).** Every other session keeps its entries in its own drafts file,
`docs/decisions_drafts/<session-or-branch>.md`: the `decisions-entry` format,
newest first, each entry exactly as it should land. A build session commits
it on its own branch; a docs session may push its own file to master, since
one file per session never conflicts. Cleanup folds every drafts file into
`DECISIONS.md` in one pass when the owner hands them off, then empties them.
Until then, anything that must cite a DECISIONS verdict (a continuity
exception, a privacy verdict, a publish gate) cites the draft's heading;
`check_category_continuity.py` reads drafts headings too.

Why: the same-day `DECISIONS.md` conflicts between branches cost a merge per
branch, and on 2026-09-30 one of them committed conflict markers when the
merge tool hit a Windows file lock. For a conflict that still happens, the
resolution is always **keep both**
(`python scripts/merge_append_only.py DECISIONS.md`).

One courtesy that avoids most of it: **do not edit a shared file that another
session currently has modified and uncommitted.** `git status` in the main
checkout shows this. Leave the line for them, or add it after they commit.

## At most two heavy jobs, each admitted by the gate

Every session shares one 16 GB machine. On 2026-09-28 heavy jobs from several
sessions overlapped, the machine ran out of memory, and Windows closed the
Claude app twice, ending every session's turn (DECISIONS; `CLAUDE.md`
`[#memory]`). The owner's rule of 2026-09-28 was one heavy job at a time,
announced by message. **Since 2026-09-30 (owner) two may run at once, each
admitted by `scripts/heavy_job.py`** against the memory actually available.

- **A heavy job** is anything likely to pass 2 GB or run for minutes: a
  multi-city drift check, a full re-render, `deploy-verify`, a join or read
  of a national or prefecture-wide file, a whole-document PDF extraction,
  and a single city whose step 2 loads a large register (Oslo's peaks near
  5.4 GB). A streamed read is not: France's SIRENE step 2 measured 0.37 GB.
- **Run it through the gate:**
  `python scripts/heavy_job.py run --label "<city> <step>" --peak-gb <N> --session <you> -- <command>`.
  It admits the job only if fewer than two are running and available memory,
  less what running jobs have yet to claim, covers the peak plus 2 GB. It
  removes the entry when the job ends and records the MEASURED peak, so state
  the last measured figure next time (`heavy_job.py status` lists them). An
  unknown peak counts as 8 GB.
- **Why measured, not a fixed budget:** on 2026-09-30 the apps alone (eight
  Claude sessions, a browser) held about 8 GB and an orphaned `grep` 4.7 GB
  more, with 2.3 GB free. A sum of declared peaks would have admitted a job
  into that.
- **Refused?** `--wait <minutes>` retries every 30 s. Tell the other sessions
  you are waiting and on what; `status` names every process over 1.5 GB, which
  is how a stray process gets found. Start and end notices are otherwise no
  longer needed: the gate's ledger (`data/_heavy_jobs.json`, shared through
  the `data/` junction) is the notice.
- **A job you cannot wrap** (a subagent's, a browser run): `heavy_job.py start
  --pid <its pid> ...` before, `end --pid <pid>` after. A dead pid drops off
  on its own, so a crash never blocks anyone.
- `drift_check.py` enforces its own share: one run per machine, `--jobs 2`
  at most. The Python cap (8 GB a process, 12 GB with its children) stays as
  the backstop: it turns a runaway into a `MemoryError` instead of a crash.
- Light work needs no gate: greps, git, `check_all.py`, one small city's
  steps.

## Subagents are not sessions, and the split is not the same one

A **session** is a long-lived role with owned paths, its own worktree and its
own commits. A **subagent** is one bounded errand inside somebody's turn: it
starts cold, returns a report, and writes nothing anybody has to merge.

**Give a subagent work that is deep, bounded, and mostly negative** — where a
large amount of fetching and reading collapses to a short answer, and the
intermediate dead ends are worth keeping out of the caller's context.

| Agent | Why it is the right shape |
|---|---|
| `licence-read` | One source, four possible verdicts. Most pages opened say nothing about reuse; Spain's two cities cost more licence reading than the nine US cities combined, and most of it was irrelevant pages |
| `deploy-verify` | A noisy start/check/stop sequence with a short findings list, and it needs the browser rather than the repo |
| `cleanup-sweep` | The cleanup role's recurring errands (a city landed, stale claims, retiring a worktree, trimming PLAN, the process review): many small reads and check runs that collapse to rows added and drafts for the owner. Never commits; removes a worktree only on stated owner and session confirmation |

### An agent's `description` has a length ceiling, and exceeding it fails SILENTLY

**Measured 2026-09-22, by breaking it.** `deploy-verify`'s frontmatter
`description` was extended from **755** characters to **1038**, and the agent
**stopped being offered at all** - no error, no warning, no entry in the
available agent types. It simply was not there, and the thing that was not
there is the publish gate.

Known points: **670 registers** (`licence-read`), **755 registers**
(`deploy-verify` before the edit), **1038 does not**. The exact ceiling is
unknown and is probably 1024.

**Keep a `description` at or under 750 characters**, and put everything else in
the body, which has no such limit. The description exists to help a caller
decide whether to invoke the agent; the reasoning belongs where the agent reads
it, not where the harness parses it.

**And check the agent is still listed after editing one.** A skill that fails
to load is usually noisy; an agent that fails to register is not, and the only
symptom is an absence you have to notice.

### Country screening is NOT one of them, and this is a measured position

It looks like a perfect fan-out — many countries, independent probes, a table
at the end — and it is the wrong shape for three reasons:

1. **It is already a session's standing role.** The staging session owns
   `docs/city_master_list.md` and `docs/global_country_shortlist.md`, and a
   subagent writing the same files is the collision this whole document exists
   to prevent.
2. **Parallel work on the append-only files has a real price.** One afternoon
   in 2026-09-22 cost **three separate `DECISIONS.md` merges** between two
   participants. A fan-out of screeners multiplies that by the fan.
3. **Screening is cumulative, not bounded.** `add-country`'s own discipline is
   that a negative from one method is not a finding, that the exhaustive base
   is built before filtering, and that a discard list names its evidence per
   row. A cold agent cannot know what the previous probe already ruled out, so
   it re-derives — and worse, it re-derives *differently*, which is how the
   same country ended up in two tiers at once.

**The screening work that a subagent CAN take is one probe with a stated
question** — "does this endpoint return premises rows with a street address and
an activity code" — handed back as an answer, with the caller doing the
banding. That is bounded. "Screen these five countries" is not.

## Handing work over: label every claim

The Canada screen reversed five conclusions, each because something was
asserted from a column's existence, a dataset title or a plausible-looking flag
rather than measured. A receiving session cannot tell the difference by
reading. So state it:

- **MEASURED** — carries a number and the query or command that produced it,
  with the date. Build on it.
- **ASSERTED** — plausible, not checked. **Verify before building on it.**
  Saying so costs nothing; discovering it three files later costs a day.

Anything handed between sessions — a build brief, a status message, a summary —
marks its claims this way, and an "open questions" section is not optional.
A brief with no unknowns listed is a brief that has not been audited.

## Sync points

Merge at natural boundaries rather than continuously: when a brief is finished,
when a build goes green, before a deploy. Between merges the sessions are
genuinely independent, which is the whole benefit — no holding, no waiting, no
staging by explicit path.

Before merging, the owning session pulls the other's work in first
(`git merge master` into the branch), resolves on its own ground, and only then
merges back. Conflicts are cheaper to handle in a worktree than in the tree
someone is mid-build in.
