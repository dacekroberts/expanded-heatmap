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

**Removing one is clean.** Commits live in the shared object store, so
`git merge worktree-<role>` followed by `git worktree remove` leaves nothing
behind. Nothing ever exists only in a worktree.

## The shared files everyone appends to

`DECISIONS.md`, `PLAN.md` and `CLAUDE.md` have no owner — every session writes
to them. Same-day `DECISIONS.md` entries will conflict occasionally; the
resolution is always **keep both**, since the file is append-only by
convention. A visible conflict is a better failure than the silent overwrite
the shared tree produced.

One courtesy that avoids most of it: **do not edit a shared file that another
session currently has modified and uncommitted.** `git status` in the main
checkout shows this. Leave the line for them, or add it after they commit.

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
