# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-01 - The master list's history written: `docs/city_master_list_history.md`, published as an artifact (owner)

- **The owner's ask, from the 2026-09-30 handoff**: a detailed history of
  how the list reached its state. The outline was drafted in chat on
  2026-09-30. The owner deferred the file until after review time, then
  said to start.
- **Placement, the owner's call, as recommended**: the file sits beside the
  list and its evidence file, with pointers from the list's head and from
  `docs/project_context.md`. It is also a private artifact.
- **It describes the list after the review landed**: 124 built, 18
  candidates (all Band R), 100 discards. Every count is dated.
- **Two dates settled from git**:
  - The discard audit's commits are 22:39 and 22:56 on 2026-09-23 local
    (UTC−7). The log dates it 09-24, and both are right.
  - Berlin went back to the discards between the reband of 2026-09-21
    21:33 and the list's first version (2026-09-22 00:46), on one keyword
    search.
- **Zaragoza's 36% is the share of addresses with a house number**, not a
  placement rate. The history states it that way.
- **Two stale figures were found and are not corrected there; they go to
  Cleanup**:
  - the master list's Yokohama row (17,408 against the 7,896 measured);
  - `add-country`'s station-density table (Canada's pre-correction
    figures).

### 2026-09-30 - Most and Liberec briefs: as-built stop counts added beside the screen's

- **The Czech kit reported both briefs' prose behind the build** (czech-build,
  6366a912). `brief_check --vs-config` still passes for both; no check
  changed.
- **Most: 28 stops and 1,025 storefronts as built, against the screen's 27
  and 1,030.** Litvínov, Vrchlického was added on lines 1, 3 and 4. It is
  closed for works, but the map shows the regular network (owner).
- **Liberec: 40 stations as built, against the screen's 39.** Šaldovo
  náměstí is on lines 2 and 3.
- **The screen's figures stay, with the as-built ones beside them.** A brief
  records what Step 0 measured.
- **`docs/tram_city_list.md` still says Most 27 and Liberec 39.** It was not
  edited here: Cleanup's review rehearsal rewrites that table, and the
  correction goes to Cleanup to fold in.
