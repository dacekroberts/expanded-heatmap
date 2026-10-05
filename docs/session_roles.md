# Working in more than one session

How concurrent Claude sessions divide this repo without colliding. Why it
exists: `docs/rule_history.md#sr-why`. The stories behind the rules below are
in `docs/rule_history.md`, "Session roles", at the anchor each rule names.

## If only one session is running, it does all of this

**This file describes a division of labour, not of capability.** A single
session reads `CLAUDE.md`, then `add-country` if the country is new, then
`add-city`, then `scaffold-city`, and builds the city end to end. Nothing
below is a precondition, a handoff gate, or a thing to wait for. **A build
brief is a cache, not a requirement**: without one, `add-city` Step 0
produces the same facts. Never stall waiting for a staging session.

## Roles, not windows

A session **claims a role**, and any window can claim any role, including
after a restart. The role is declared once, in the session's first message
("you are the build session for Vancouver"), and it grants a set of paths.

**Ownership is by path.** That is what prevents collisions: two build sessions
can run at once provided they hold different cities.

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
that does not own it**, because every other session's output depends on it.

## The cleanup role owns no paths, and that is deliberate

Its job is cross-cutting (stale prose, a drifted count, an empty worktree
directory), so it runs on different rules (`#sr-cleanup`):

- **Sweep narrow and commit immediately.** Its only protection against a
  collision is a short window between reading a file and committing the fix.
- **Verify against `origin/master`, never the local tree.** It reports on other
  sessions' work, so it is the role most likely to read a stale checkout.
- **It never merges a branch it does not own**, and reads the commit message
  before drawing conclusions from the branch graph. A branch held off master
  deliberately looks exactly like an abandoned one.
- **It does not edit a file another session has uncommitted**, and does not
  rewrite pipeline, taxonomy or step logic. A real bug there is handed over.
- **Its preferred output is a check, not a correction**, which is why it owns
  `scripts/check_*.py`: a check keeps finding the class after the session
  ends.

The skill is `.claude/skills/consistency-sweep/`, with the defect taxonomy.

## Each non-primary session works in its own worktree

The primary session keeps the main checkout. Every other session gets one:

```bash
git worktree add .claude/worktrees/<role> -b worktree-<role>
```

Git refuses to check out `master` in two worktrees at once, so each is on its
own branch and merges back: the merge is an explicit review step instead of an
implicit race.

**The standing assignments** - current state, so update this when one changes.
A landed row shrinks to one line; the full rows as of 2026-10-04 are at
`#sr-registry`. Rows marked "gone" were not in `git worktree list` on
2026-10-04.

| Role | Worktree | Branch |
|---|---|---|
| Staging / research | `.claude/worktrees/staging` | `worktree-staging` |
| Cleanup / audit | `.claude/worktrees/cleanup` | `worktree-cleanup` |
| France kit, then the France builds; gone | `.claude/worktrees/france-kit` | `worktree-france-kit`; `france-build` |
| Czech kit; gone | `.claude/worktrees/czech-kit` | `worktree-czech-kit` |
| UK six builds; gone; claims landed 2026-10-02 | `.claude/worktrees/uk-six` | `uk-six-build` |
| Japan batch, twelve cities; gone; claims landed 2026-10-02 | `.claude/worktrees/japan-batch` | `japan-batch-build` |
| Seattle (Regional), then Tbilisi; gone | `.claude/worktrees/seattle-tbilisi` | `seattle-tbilisi-build` |
| Japan wave 2, fourteen cities: **LANDED 2026-10-03** | `.claude/worktrees/japan-wave2` (removed) | `japan-wave2-build` |
| Four extensions to built cities: **LANDED 2026-10-03** | `.claude/worktrees/extensions` (removed) | `extensions-build` |
| Belgium builds, six pages: **LANDED 2026-10-04** | `.claude/worktrees/belgium` (removed) | `belgium-build` (removed) |
| Liverpool (Regional), Tacoma, Mendoza: **LANDED 2026-10-04** | `.claude/worktrees/new-cities` (removed) | `new-cities-build` (removed) |
| Korea sweep, Daejeon, Gwangju, Gimhae: **LANDED 2026-10-04** | `.claude/worktrees/korea-sweep` (removed) | `korea-sweep-build` (removed) |
| Tram kit, the ten other T1 cities; gone | `.claude/worktrees/tram-kit` | `worktree-tram-kit` |
| Build `<city>` | `.claude/worktrees/<city>` | `<city>-build`; delete the branch when the worktree goes |

A build worktree's `data/` and `.venv-lean` are junctions to the main
checkout's; a build branch is never pushed to master, and its `app/` lands at
review time.

**Retiring a worktree.** Close its session first, then, from the main
checkout (`#sr-cleanup-move`):

```bash
git pull --ff-only
git worktree remove .claude/worktrees/<name>
git branch -d <branch>
```

`-d`, never `-D`: it refuses to delete a branch holding commits that are not
in the main checkout's LOCAL `master`, which makes the deletion its own check.
**Hence the pull first**: without it `-d` refuses correctly, but reads like a
warning of data loss.

**Never remove a session's own launch worktree from inside that session.** A
session loads its hooks and skills from the `.claude/` of the folder it was
launched in, so it loses them (`block_heredoc.py` included) and cannot
continue (`#sr-launch-worktree`). Remove it after closing that session.

`.claude/worktrees/` is gitignored; also add it to `.git/info/exclude` on a
working machine, since the main checkout may lack that commit.

**Commits survive a removal; gitignored files do not.** `git worktree remove`
deletes ignored files without asking, and `data/` is ignored, so a cache may
exist ONLY in the worktree that built it. Before removing a worktree
(`#sr-worktree-removal` has the incident behind each step):

1. **Unlink every junction first, on its own, without recursion**, across
   the WHOLE worktree, not just `data\` (`.venv-lean` is often one too).
   PowerShell 5.1's `Remove-Item -Recurse` can follow a junction and empty
   its TARGET. List them, then remove each link alone; `cmd /c rmdir <link>`
   deletes a junction and never its target:

   ```powershell
   Get-ChildItem -LiteralPath <worktree> -Recurse -Force -Attributes ReparsePoint
   ```
2. **Save the worktree's WHOLE `data/` first - every folder, not only built
   cities** (national files and probe downloads no `fetch_sources.py`
   re-creates). Copy what the main checkout lacks, no-clobber (`cp -rn`),
   then run `python scripts/check_worktree_data.py <worktree>` until it
   passes, whatever route removes the worktree.
3. Then the three commands above. If Windows leaves an empty folder behind,
   re-run step 1's listing on it before deleting it.
4. **`Filename too long` stops `git worktree remove` partway.** Re-run step
   1's listing over the WHOLE folder, then delete the rest with
   `cmd /c rmdir /s /q "\\?\<full path>"`. An open session keeps its launch
   folder locked; leave the empty folder until it is closed.

**Page and notice numbers** (`#sr-numbers` has the full paragraph of
2026-10-04). Notice numbers are claimed
here, by the session, before one is written; no claims are open;
133–136, released unused by the four extensions on 2026-10-03, stay
unassigned; the next free notice is 154. Every earlier block has landed:
the coverage sweep's on 2026-10-04 (the Korean three, pages 190–192 and no
notices; Mendoza, Tacoma and Liverpool (Regional), pages 193–195 and
notices 141–143 and 153; Belgium, pages 196–201 and notices 144–152);
Japan wave 2's 115–128, the extensions' 129–132 and lane-app's 137–140 on
2026-10-03, and everything up to 114 on 2026-10-02. Pages reserved for the ranked
list (2026-10-04; `docs/staged_cities.json`): the Copenhagen line 202, the
owed-act seven 203–209, Japan wave 4 210–289, rank 4 290–299; the next free
page outside them is 300.
Check D of `check_provenance.py` reads every range in that sentence and lets
a branch skip exactly those numbers; any other gap still fails. Keep the
ranges in that one sentence, and delete a batch's range once it lands.
**Scaffold with the reserved number:** `scaffold_city.py ... --page-number
<N>`. Without it the script takes one past the highest page on the session's
own branch, which is the collision. It refuses a number already taken. The
three info pages carry no number (`About_the_Data.py`, `What_Is_Excluded.py`,
`Why_the_Maps_Differ.py`), so no block ever reaches them.

## The shared files everyone appends to

`PLAN.md` and `CLAUDE.md` have no owner — every session writes to them.
**`DECISIONS.md` is written by the cleanup session only, since 2026-09-30
(owner)** (`#sr-shared-files`). Every other session keeps its entries in its
own drafts file, `docs/decisions_drafts/<session-or-branch>.md`, in the
`decisions-entry` format, newest first, each entry as it should land. A build
session commits it on its own branch; a docs session may push its own file to
master. Cleanup folds every drafts file into `DECISIONS.md` in one pass when
the owner hands them off, then empties them. Until then, anything citing a
DECISIONS verdict (a continuity exception, a privacy verdict, a publish gate)
cites the draft's heading; `check_category_continuity.py` reads drafts
headings too. A conflict is resolved **keep both**
(`python scripts/merge_append_only.py DECISIONS.md`).

**Do not edit a shared file that another session currently has modified and
uncommitted.** `git status` in the main checkout shows this. Leave the line
for them, or add it after they commit.

## At most three heavy jobs, each admitted by the gate

Every session shares one 16 GB machine, and overlapping heavy jobs have run it
out of memory and closed the Claude app (`#sr-heavy-jobs`, `#memory`).
**Since 2026-10-04, three heavy jobs at most (owner, with no other heavy
processes open on the machine), each admitted by `scripts/heavy_job.py`**
against the memory actually available; the memory test, not the count, is
what usually refuses a job. If other heavy programs come back onto the
machine, return `MAX_JOBS` to 2.

- **A heavy job** is anything likely to pass 2 GB or run for minutes: a
  multi-city drift check, a full re-render, `deploy-verify`, a national or
  prefecture-wide file, a whole-document PDF extraction, a step 2 loading a
  large register (Oslo's near 5.4 GB). A streamed read is not.
- **Run it through the gate:**
  `python scripts/heavy_job.py run --label "<city> <step>" --peak-gb <N> --session <you> -- <command>`.
  It admits the job only if fewer than three are running and available memory,
  less what running jobs have yet to claim, covers the peak plus 2 GB. It
  removes the entry when the job ends and records the MEASURED peak
  (`heavy_job.py status` lists them). An unknown peak counts as 8 GB.
- **Refused?** `--wait <minutes>` retries every 30 s. Tell the other sessions
  you are waiting and on what; `status` names every process over 1.5 GB. The
  gate's ledger (`data/_heavy_jobs.json`, shared through the `data/`
  junction) is the notice; no start and end messages.
- **A job you cannot wrap** (a subagent's, a browser run): `heavy_job.py start
  --pid <its pid> ...` before, `end --pid <pid>` after. A dead pid drops off
  on its own, so a crash never blocks anyone.
- `drift_check.py` enforces its own share: one run per machine, `--jobs 2`
  at most. The Python cap (8 GB a process, 12 GB with its children) stays as
  the backstop: it turns a runaway into a `MemoryError` instead of a crash.
- Light work needs no gate: greps, git, `check_all.py`, one small city's
  steps.

**Measured figures are the norm (owner, 2026-10-03).** With `--peak-gb`
omitted the gate declares the label's last measured peak. A job never
measured declares an estimate scaled from measured ones and says so
(`--estimate "scaled from Kyoto 0.33 GB by raw size"`). In a series of like
jobs, the first runs alone and measures for the rest. Keep labels stable
(`<city> step 2`, `drift <city>`, `drift japan --jobs 2`); a multi-city run is
its own label, never declared from one city's figure.

**The RAM is overclocked since 2026-10-03** (capacity unchanged). A crash
with memory available, or a `MemoryError` or corrupted output with no cap
reached, points to the overclock before the script: tell the owner.

## Subagents are not sessions, and the split is not the same one

A **session** is a long-lived role with owned paths, its own worktree and its
own commits. A **subagent** is one bounded errand inside somebody's turn: it
starts cold, returns a report, and writes nothing anybody has to merge.

**Give a subagent work that is deep, bounded, and mostly negative** — where a
large amount of fetching and reading collapses to a short answer, and the
intermediate dead ends are worth keeping out of the caller's context.

| Agent | Why it is the right shape |
|---|---|
| `licence-read` | One source, four possible verdicts; most pages opened say nothing about reuse |
| `deploy-verify` | A noisy start/check/stop sequence with a short findings list, and it needs the browser rather than the repo |
| `cleanup-sweep` | The cleanup role's recurring errands, collapsing to rows added and drafts for the owner. Never commits; removes a worktree only on stated owner and session confirmation |

**An agent's `description` has a length ceiling, and exceeding it fails
SILENTLY**: the agent is simply not offered (1038 characters failed; 755
registered; the ceiling is probably 1024; `#sr-agent-description`). **Keep a
`description` at or under 750 characters**, put everything else in the body,
and **check the agent is still listed after editing one.**

**Country screening is NOT a subagent's job** (`#sr-screening`): it is the
staging session's standing role and files, parallel writers multiply the
append-only merges, and screening is cumulative (a cold agent re-derives
what earlier probes ruled out, differently). **A subagent CAN take one probe
with a stated question** ("does this endpoint return premises rows with a
street address and an activity code"), handed back as an answer, with the
caller doing the banding. "Screen these five countries" is not bounded.

## Handing work over: label every claim

A receiving session cannot tell a measured claim from an asserted one by
reading (`#sr-handover`). So state it:

- **MEASURED** — carries a number and the query or command that produced it,
  with the date. Build on it.
- **ASSERTED** — plausible, not checked. **Verify before building on it.**

Anything handed between sessions (a brief, a status message, a summary) marks
its claims this way and has an "open questions" section: a brief with no
unknowns listed has not been audited.

## At most three build sessions, and no catch-up merges

**At most three build sessions at once** (owner, 2026-10-04, the efficiency
review's second change), besides Cleanup, Staging and the two downstream
sessions; the same three the heavy-job gate admits. A fourth build waits for
one to land.

**A branch takes origin/master in only right before its own push**, or when it
needs something master has; never just to keep up after someone else's push.
Catch-up merges ran 28 a day in the week of 2026-09-27 and made 103 of 176
conflicted merges (`docs/efficiency_review_2026-10-04.md`).

## Sync points

Merge at natural boundaries: a brief finished, a build green, before a
deploy. Before merging, the owning session pulls master into its branch,
resolves on its own ground, then merges back: conflicts are cheaper in a
worktree than in a tree someone is mid-build in.

## Downstream sessions: Visuals and Analytics are told when their inputs move

Two sessions build FROM what master holds, without landing anything the site
renders: **Visuals** (`.claude/worktrees/visual`, city cards, decks, print)
and **Analytics** (`.claude/worktrees/analytics`, private analysis in
`data/_analysis/`). Neither sees master move, so Cleanup tells them (owner,
2026-10-03), **once per review time** rather than after every push (owner,
2026-10-04, the efficiency review's second change: up to 26 messages a day,
each waking a session on its full context).

- **At the end of each review time**, Cleanup runs
  `python scripts/downstream_changes.py <the last noted master> origin/master`.
  The last noted master is the commit in the line below, which Cleanup
  updates after each note. A removal request carried out is noted at once.
  **Last noted: a0995945 (2026-10-04).**
  If it prints anything but "nothing downstream", it sends that output,
  unchanged, to both sessions ("Expanded Heatmap Visuals" and "Expanded
  Heatmap Analytics", found with ListAgents), with one line on WHY the
  inputs changed (the DECISIONS heading is enough).
- **What counts** is listed in the script's docstring: a city added or
  removed, any `outputs/<city>/` change, the city registry, the notices and
  credits, the macro facts, category rules and taxonomies, licence rows, and
  the shared map code and theme.
- **A new city always counts**, and so does a removal request carried out:
  a city or layer taken down must leave the cards and analyses too.
- **For each new city** (Visuals' request, 2026-10-03) the note carries its
  slug, its own notices and whether its rail or station names come from
  OpenStreetMap (the script prints these when run from the pushed commit),
  plus two things the sender adds from the build's drafts file: for each
  notice, **card face or caption only** (the licence's own words on where
  the notice must appear decide it), and **any open terms question**, which
  keeps that city off the cards and public pieces until the owner rules. A
  build session records both in its drafts file for every source it adds.
- **The message informs; it never instructs.** Each session decides what to
  regenerate, on its own branch, and lands through cleanup as usual.
- **A build session's branch** says in its drafts file which downstream
  inputs it changes, so the lander can check the script's output against it.
