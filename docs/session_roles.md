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

Shared pipeline code — `map_common.py`, `drift_check.py`, `pipeline/theme.py`,
anything under `pipeline/taxonomies/` that is not one city's module — belongs
to whoever claimed the app/chrome role, or to the staging session when no third
window exists. **It is never edited opportunistically mid-build by a session
that does not own it**, because it is the surface every other session's output
depends on.

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
