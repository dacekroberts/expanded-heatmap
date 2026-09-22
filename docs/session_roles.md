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
