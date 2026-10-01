# France tram batch - retrospective (2026-09-30)

Twenty-one French tram cities were built in one session on 2026-09-30. The
kit came first: a skill, a batch scaffold, 20 briefs, the probes and the
pure-extract station tables. Then the builds, on `france-build` (group 1,
11 cities), `france-build-2` (group 2, 9) and `france-build-3` (Angers, built
mark-free). This file answers one question: **did quantity cause mistakes, or
did the French pipeline carry the batch?** The detail behind each figure is
in `docs/decisions_drafts/france-build.md`, which is on the build branches
until the cities land. It was written before landing; the landing itself is
not covered here.

## The short answer

**The pipeline carried it.** No wrong figure reached a page uncaught. Every
error was caught by a gate, a check or a peer session before landing.

Quantity changed the kind of mistake, not its rate. A defect in a template or
a generator was copied to every city it ran over. So the errors that cost
the most were few in number but wide in reach: one bug, ten or twenty fixes.
City-specific data traps were caught one city at a time by the gates, as they
would be in a single build.

## Timeline (commit times, local)

| Step | Time | Cities |
|---|---|---|
| Shared tram module | 15:49 | - |
| Le Mans, the pilot | 15:57 | 1 |
| Group 1 through step 3 | 16:26 | 10 more |
| Group 1 artefacts (baselines, facts, rows) | 16:36 | - |
| Group 2 through step 3 | 16:45 | 9 |
| Group 2 artefacts, zero drift | 16:54 | - |
| Angers, from fresh probe to commit | about 18:30-18:47 | 1 |

After the shared module, twenty cities took about an hour from scaffold to
zero drift. Angers took about a quarter of an hour, brief included, once the
kit existed.

## What ran smoothly

- **The SIRENE chain** (`france_register.py`) ran unchanged on all 21. Every
  step 2 peaked near 0.4 GB, so none needed the heavy-job gate. Every
  `96.09Z` share fell in or near the precedent's 9-14%; only Nantes, at
  15.6%, sat above it.
- **The gates did their job.** Gate 3 (OpenStreetMap's per-line stop
  counts) and the commune asserts caught every data trap below. None was
  found by reading output.
- **The checks caught the bookkeeping:** `check_provenance`,
  `check_macro_facts`, `check_macro_labels`, `check_deploy_imports` and
  linecolour.
  - Personal exposure passed on all 21: 0 contact details, and 0 person-like
    names at a residential unit.
  - Every city recorded zero drift against its baseline.
- **The approved page template** meant no page text needed reading back. The
  three approved departures (Rouen, Brest, Nice) and two proposals (Reims's
  two lines, the OSM-track sentence) were the only prose decisions.

## The mistakes, by cause

### 1. Defects multiplied by the batch (the cost of quantity)

| Defect | Reach | Caught by |
|---|---|---|
| Step 2 template: `"\n"` escaped wrongly in a string | would have hit all 20 | the first city's run |
| `france_fill_build_day.py` turned an apostrophe into a quote (`feed"s`) | 10 configs | reading what it wrote |
| Source rows quoted the Overpass query, whose pipe broke the markdown tables | every row | `check_provenance` |
| The page generator nested « Source : Insee » inside the provenance block, so a bad file would drop it | 20 pages | a peer session (fix 6fcda94), then check M |
| Retag script wrote CRLF line endings | 2 files | diff size, before commit |

**Lesson**: run a generator on one city, read every line it wrote, and only
then let it run over the batch. Le Mans was that pilot for the steps but not
for the doc generators, which were written mid-batch and run on ten at once.

### 2. City-specific data traps (one at a time, as in any build)

- **Reims is two public lines, T1 and T2, on one feed route** (since
  2025-11-24). The brief said one line, and gate 3 caught it.
  - The split first matched 0 trips for T2, because the parent's name
    differs from the platform's.
  - Short workings then counted 22 on T1, so they are now assigned by each
    branch's own stops.
  - The kit's brief research missed the renaming; that is the one miss
    traced to the kit itself.
- **Tours: gate 3 read 31**, from duplicate relation members. Counting
  distinct positions gave 29, a fix to the shared module.
- **OSM refs differ from the feeds' route names:**
  - Montpellier 4 is 4A and Rouen's Métro is M in OSM;
  - Bordeaux B and Reims carry no ref;
  - Brest C is an aerialway.

  Each was handled per city.
- **Two colour clashes:** Tours's line and Dijon's shared colour, both
  refused by linecolour and darkened.
- **Two expected counts moved** (Caen, Bordeaux) once the Licence Ouverte
  same-name rule was applied: the rule's own consequence.

### 3. Coordination across sessions (a cost of the day's parallelism, not of the batch)

- **Page numbers collided** with Band B (76-86), so France moved to 100-120
  on every branch. Notice numbers 69-72 will renumber at landing.
- **Five group-2 fetches exited** because their scaffolds moved branches
  while `fetch_batch` was still running. This session's own sequencing
  error; they were re-fetched.
- **A drift check was refused** while the tram kit's run held the machine.
  It was retried later, as the gate intends.

### 4. Environment friction (constant, not caused by the batch)

The worktree isolation guard refused computed loops, `git -C`, globs and
arithmetic repeatedly (five times in the last two hours alone). The heredoc hook refused inline Python with
backslashes. Each refusal cost a rewrite into a plain command or a scratch
script, never a wrong result. One sequencing slip followed from the same
setup: `check_deploy_imports` reads the committed tree, so running it before
committing reported a false FAILED. It passed after the commit.

## Was the error rate higher because of quantity?

**Per city, no; per defect, yes.**
- City-specific problems ran at about one per city, the same rate as the
  single builds before them.
- Generator defects were fewer than ten, but each reached 10 to 20 files.
  None reached a published page, because nothing lands before review time.
- Mistakes fell as the batch went on:
  - the pilot and group 1 carried most of the generator fixes;
  - group 2's only real error was the fetch sequencing;
  - Angers's two slips were the UTC-versus-local fetch date, caught by
    `check_macro_facts`, and a label overlap found by the label check.

## What to carry to the next batch (Czech, the other T1 trams)

1. **Pilot every generator on one city** before a batch run, the doc
   generators included, and read its whole output.
2. **Write dates in UTC from the start**, as `provenance.json` already
   does, so the app entries agree with it.
3. **One branch move at a time**: never move a scaffold while a fetch over
   it is running.
4. **Claim page and notice numbers early** in `docs/session_roles.md`, so
   parallel batches do not collide.
5. **Trust the gates and the checks.** Every data trap here was caught by a
   gate that already existed or by one added for the first case (Reims's
   branch split, Tours's distinct positions). Put a new trap's lesson in the
   shared module, as with `ROUTE_BRANCHES`, not in one city's comments.
