# Handoff - the Czech tram batch (2026-09-30)

For a FRESH session in `.claude/worktrees/czech-kit` (branch
`worktree-czech-kit`), doing for Czechia's six T1 cities what the France kit
session did for France's twenty. **Delete a section when its item is done.**

The owner asked for it on 2026-09-30, the day the France kit was approved.
Builds were approved for France that day; **for Czechia, bring the open calls
below to the owner, and wait for the go before building.**

## Read first

1. `CLAUDE.md`, then `docs/session_roles.md` (the build role, the heavy-job
   rule, explicit-path staging).
2. **The France kit as the model**: `.claude/skills/france-tram-city/SKILL.md`,
   `scripts/scaffold_france_batch.py`, and one French brief
   (`docs/build_briefs/brest.md`). DECISIONS "The France batch kit" and "The
   France batch's eight calls approved" record how it was done and what the
   owner approved. Copy the method, not the French facts.
3. **The six Czech briefs** (staging's; see section 3), first written on 2026-09-30, each passing
   `brief_check.py`: `docs/build_briefs/brno.md`, `ostrava.md`, `plzen.md`,
   `olomouc.md`, `liberec.md` and `most.md`. DECISIONS "The six Czech tram
   cities briefed" has their calls.
4. **Prague, the built Czech city**: `pipeline/prague/`,
   `pipeline/countries/czechia.py`, `czechia_register.py`,
   `pipeline/taxonomies/czech_nace2025.py`, `docs/data_sources/czechia.md`.
   Czechia is Mexico's shape, like France: one national register chain
   (ROS02 establishments, RES activity, the RÚIAN address join).
5. `docs/tram_city_list.md`, the Czech T1 rows, and `docs/ring_rules.md`.

## Done (2026-09-30)

Sections 1 and 2 are done. The skill is `.claude/skills/czech-tram-city/SKILL.md`,
and there is no batch scaffold, decided on the measurement (DECISIONS "The
Czech batch kit"). **Every open call, the page text and the notices were
approved as recommended** (owner, 2026-09-30: DECISIONS "The Czech batch's
calls and prose approved as recommended"), and the skill carries them. What
is left is the owner's go on builds, which that approval did not give.

## 3. The briefs - STAGING's, not this session's

**The staging session owns the Czech briefs** (owner, 2026-09-30). Do not edit
them here. When the skill or a build needs a brief changed, finished or
re-checked, ask staging for it (`ListAgents`, then `SendMessage` to the
staging session), and pull its commits from `origin/master`. Reading them and
running `python scripts/brief_check.py brno ostrava plzen olomouc liberec
most` is fine. **Asked of staging on 2026-09-30, and open until its commits
land**: the dangling palette reference in five briefs; Brno's stations as the
feed's parents, and its count; the `vs_config` mappings; Jablonec's and
Litvínov's RÚIAN controls; Ostrava's relation recount. It was also told the
approved calls, so the briefs can carry them.

## Standing rules (same as the France kit)

- **Feeds are fetched at build, never cached across weeks.** `brief_check.py`
  refetches a GTFS older than 7 days since 2026-09-30.
- **One heavy job machine-wide**, announced to the other live sessions first
  (a Czech step 2 reads the national ROS02 file). The France build session
  runs in `.claude/worktrees/france-kit`.
- **Push docs, skills and scripts only**, with the push ritual in `CLAUDE.md`
  (fetch, merge, push `HEAD:master`) and commit messages written through a
  file. **Builds go on a separate branch**, because landing `app/` is
  deploying; `app/` waits for review time.
- Log judgment calls in `DECISIONS.md`; bring owner calls in chat with a
  recommendation.
