# Handoff — the UK six (2026-10-01)

For the build session that builds the six UK tram and light-rail cities.
Written by staging, and approved by the owner the same day.

**✅ RELEASED by the owner, 2026-10-02**, to ONE build session that runs
agents ("whichever you think is more efficient"). It works in the worktree
`.claude/worktrees/uk-six` on branch `uk-six-build`, where `data/` and
`.venv-lean` are junctions to the main checkout's.

**What came first, both landed by 2026-10-02 (Cleanup):**
- The site-wide prose and UI pass, built and deployed. It covers code
  comments, the What Is Excluded and About pages, the Overview city list
  and the city-page format, plus a final audit.
- Then the city-building and page skills, reworked to the new page format.

**Build on the reworked skills, and re-read them before starting.** Where
this handoff's page and prose steps disagree with them, the skills win.

**Delete this file** once all six have landed.

---

## How this session runs: one lead, agents for five (staging, 2026-10-02)

**Why one session.** Manchester pilots the shared code and the other five
become config, so a second session would mostly wait on the first. Every
city also touches the same shared files: `app/cities.py`, the notices,
What Is Excluded, `docs/data_sources/united-kingdom.md`, the macro facts and
the labels. One integrator applying them in order avoids five merges of the
same lines.

**Phase 0, the lead alone:**
1. Confirm the worktree and branch, `git fetch`, merge `origin/master`.
2. Register the session in `docs/session_roles.md`'s table.
3. Claim six page numbers, and the notice numbers, there in one edit.
4. Run `python scripts/brief_check.py <city>` for all six, one at a time.
   Each makes Overpass calls; wait 60 s after a RETRY.
5. Settle the 🚨 items below: the ECL and Newhaven relations, and whether
   Dudley's Line 2 is in service.

**Phase 1, the lead alone: Manchester (Regional), the pilot.**
- Build it end to end: fetch, steps 1 to 3, the page and the gates.
- Make every shared-code change here, proven against London's and
  Newcastle's drift checks.
- Commit when it is green. The other five start from that commit.

**Phase 2: five agents, one city each, in parallel.**
- The lead first runs each city's OpenStreetMap fetch itself, one at a time
  (the one-query-per-session rule covers the agents). It then spawns the
  five agents in this same worktree (no `isolation`), each with its brief,
  this kit and the Manchester commit to copy.
- **An agent owns only its city's files:**
  - `pipeline/<slug>/`;
  - `data/<slug>/`;
  - `outputs/<slug>/`;
  - its claimed `app/pages/` file.
- **An agent never queries Overpass and never commits.** It also never
  edits a shared file. It returns the shared-file entries as text for the
  lead to apply:
  - the `cities.py` entry;
  - the privacy-verdict row;
  - the provenance record;
  - its What Is Excluded section;
  - its licence rows and notices;
  - its inconsistency rows;
  - its master-list line;
  - its drafts entries;
  - its prose proposals.
- **The agent's run covers:**
  - Step 0's measurements;
  - steps 1 to 3 for its own city only;
  - `check_personal_exposure.py <slug>`;
  - the page from `scaffold_city.py`.
- **An agent stops and reports**, rather than guessing, on:
  - a failing brief claim;
  - a gate 3 mismatch;
  - a placement share under the brief's figure;
  - a change it would need to make in shared code.
- Five agents running light jobs is within the memory rules. The FSA files
  are small; Manchester's step 2 is the largest.

**Phase 3, the lead: integrate in build order** (Birmingham, Edinburgh,
Sheffield, Nottingham, Blackpool).
- For each city in turn, apply its returned entries, run the gate order
  below, and commit it on its own.
- Then make the region and label pass below once, for all nine UK cities.
- Last, one drift check (`--jobs 2`), merge master, `check_all.py`, and
  push `uk-six-build`. **Not to master** until review time.

## The UK sub-region and the minor label tier (owner, 2026-10-02)

**The owner:** "implement the high-density cluster rule to UK, like Japan,
France, Czechia". This follows the France and Czechia mechanism (the
DECISIONS.md entry of 2026-09-30 on the label tiers' first and second
slices):
- **A UK region of its own.** Every UK city moves into it, the built three
  (London, Glasgow, Newcastle (Regional)) included, as Prague moved with
  Czechia. Use one region or a split, as France North and South, decided by
  `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.
  Dublin stays in Europe unless that measurement says otherwise.
- **The minor tier, on France's line.** France's minor cities are its
  non-metro ones, and the same line here is metro against tram and light
  rail. All six new cities are tram or light rail, so each carries
  `label_tier: "minor"`. London, Glasgow and Newcastle stay eligible. A
  minor city keeps its dot and tooltip in every view; its pill shows only in
  its own region.
- **`REGION_LABELS_ALSO["Europe"]` gains the UK region,** so Europe still
  names London, Glasgow and Newcastle (Seoul's case in East Asia). Europe's
  re-centred frame may need a label re-placed (Stockholm's case in the Czech
  move). Measure; do not tune by eye.
- **Add the UK region (or both halves) to `cities.COUNTRY_VIEWS`** as well as
  `REGION_ORDER` (owner, 2026-10-02): the country views go last in the region
  menu, after every larger view.
- **It lands with the six, at review time.** The region move changes `app/`.

**The Japan batch takes the same rule when it is built.** It is recorded in
the `japan-city` skill and is not part of this round.

---

## Page text: the new format (prose hold lifted 2026-10-02)

The owner's prose pass and the skills rework have landed (18e4ecc7,
7202719c, 797afd01). Cleanup confirmed on 2026-10-02 that nothing pending
keeps the hold. A build writes its page text to these:

1. **`docs/city_page_format.md`, the spec.** It covers:
   - the page order and bullets;
   - the reference-doc sections that name the city;
   - process notes kept off rendered docs, or between `<!-- internal -->`
     markers (`check_internal_markers.py`, in `check_all`);
   - US spelling, names and approvals.
2. **The reworked skills.** `add-city` step 8 comes first. Then:
   - `scaffold-city`;
   - `publish-city`, whose gate step 5a checks the page against the format;
   - `premises-taxonomy` step 8, for labels;
   - `read-licence` step 9, for rows and notices.
3. **Scaffold with the reserved page number**, `--page-number 156` to `161`
   in build order (`docs/session_roles.md`): it is what keeps the Japan
   batch's 162-173 from colliding with these.
4. **`scripts/scaffold_city.py`'s page template is the new format.** Run it
   for real, not as a dry run.

**Rules for this round (Cleanup, 2026-10-02):**
- **London's, Glasgow's and Newcastle's pages were converted in the pass.**
  Their current bullets are the approved wording for the FSA and FHIS
  family, and a build may reuse a shared sentence from them.
- **A sentence specific to the city, which no template covers, is a
  proposal.** Flag it in the drafts file. The build does not stop for it.
- **The approved-template pre-permission** (CLAUDE.md, 2026-09-30) applies
  again.
- **What Is Excluded:**
  - The city has its own section, under a heading that names it.
  - Its stations are "listed on <City>'s page", never an `outputs/` path
    (owner, 2026-10-02).
  - Its gaps and limits go in its own section.
- **Keep exactly as published:**
  - the OGL title ("Open Government Licence");
  - the FSA's and FHIS's own business-type names;
  - line and station names.

  Everything else reader-facing is in US spelling.
- **Any `TODO(prose-hold)` marker** left from earlier work in a UK branch can
  now be filled under these rules.

---

## The six, in build order (owner, 2026-10-01)

| # | Page | Scope (FSA codes) | Storefronts | Brief |
|---|---|---|---|---|
| 1 | **Manchester (Regional)** | 7 districts: 405, 415, 418, 419, 422, 430, 431 | 12,451 | `docs/build_briefs/manchester.md` |
| 2 | **Birmingham (Regional)** | 402, 423, 436 | 9,827 | `docs/build_briefs/birmingham.md` |
| 3 | **Edinburgh** | 773 (FHIS) | 3,933 | `docs/build_briefs/edinburgh.md` |
| 4 | **Sheffield** | 425, without the Tram-Train | 3,447 | `docs/build_briefs/sheffield.md` |
| 5 | **Nottingham (Regional)** | 899, 261, 266, 259 | 3,702 | `docs/build_briefs/nottingham.md` |
| 6 | **Blackpool (Regional)** | 898, 207 | 1,744 | `docs/build_briefs/blackpool.md` |

**All six are food only** (food service plus food shops), on the FSA register
and the OGL. They use the shared `pipeline/fsa.py` (the flat, childminder
and trading-as rules) and London's storefront filter. Placement uses
Code-Point Open centroids, as London and Newcastle do.

**Manchester is the pilot.** Whatever it adds to shared code, the other
five take as config.
- Pilot every generator or shared change on Manchester alone first, and
  read its whole output (the France batch's lesson).
- Prove each shared change against a control. London's and Newcastle's
  drift checks must stay clean.

---

## Before each build

1. **Run `python scripts/brief_check.py <city>`.**
   - A FAIL on a real claim is a brief to correct, never a check to relax.
     Staging corrects briefs.
   - A RETRY means Overpass was busy. Re-run it later, at least 60 s apart.
2. **Resolve the brief's 🚨 items.** These need the owner:

   | City | Item | Needs |
   |---|---|---|
   | All six | **Gate 3's source: NaPTAN** (DfT, OGL), approved by the owner 2026-10-01. Sheffield's and Blackpool's operators refuse scripts, so it is their only independent source | A licence row and its notice; the build downloads it without asking |
   | Birmingham | **Line 2 (the Dudley line) is in OSM** | **Pre-approved (owner, 2026-10-01):** if it is in passenger service at build, add Dudley (FSA 409) as a fourth authority |
   | Manchester | The **ECL** relation | Identify it before drawing |
   | Edinburgh | The **"Tram Extension to Newhaven"** relation | Identify it before drawing |

3. **Gate 3 in every city** (the `tram-city` rule since 2026-09-30): the
   operator's per-line stop counts go in config before step 1, and a
   mismatch stops the step. It ran in one city of ten in the tram kit. Do
   not repeat that.
4. **The light-rail test** (`docs/tram_city_list.md`). The track share
   and spacing are measured at Step 0, one Overpass query per city.
   - Frequency gates converted railway only: Manchester's three branches
     and Birmingham's Snow Hill section pass; Sheffield's Tram-Train is out.
   - Spacing is evidence, not a gate.

## Build each city

Use the gate order Band B fixed (`docs/band_b_retrospective.md`):
1. personal exposure, plus a row in `docs/privacy_verdicts.md`
   (`check_privacy_verdicts.py` fails a city without one);
2. provenance;
3. scope disclosure, its section written to the format;
4. the inconsistency rows and `cities.py` fields;
5. the master list;
6. macro facts and the macro label (the label after the region pass above);
7. the decisions entry;
8. commit;
9. then the drift check, its baseline and ring shares;
10. then merge master, `check_all.py`, and push at 0 behind.

**Not to master** until the owner's review time. Landing `app/` is
deploying.

## Session rules (CLAUDE.md, 2026-09-30)

- **Decisions go to the drafts file**, `docs/decisions_drafts/uk-six.md`,
  never to `DECISIONS.md`.
- **Overpass:** one query in flight per session, one per city; wait 60 s
  after a 504 or 429. `brief_check.py`'s `osm_route_refs` claims are
  Overpass queries too. **Only the lead queries.** The session's agents
  share its one slot, so they read the lead's cache.
- **`data/` is one shared junction across worktrees.** Never re-run another
  city's step from this branch. Another session's re-render can make
  `check_macro_facts` or `check_ring_shares` fail on a city that is not
  yours: tell Cleanup, and never write that city's facts.
- **These are light jobs.** The FSA files run 0.8–10 MB, so the heavy-job
  gate is not needed. An unknown peak still counts as 8 GB.
- **Read registers carefully.** Select columns before printing anything
  from a register with personal columns. Three agents printed names to
  their consoles on 2026-10-01.
- **No backslash or backtick in a Bash command.** Write a script file.

## Notices

Newcastle's precedent is two notices per city: the FSA's and Ordnance
Survey's (Code-Point Open). **Their wording follows Newcastle's converted
notices and `read-licence` step 9.**
Record each notice's number and licensor attribution string. Claim notice
numbers early in `docs/session_roles.md`, so parallel work does not
collide (the tram kit's lesson 5). **Pages are pre-assigned: 156–161 in
build order** (Manchester 156 … Blackpool 161); the Japan batch, building
at the same time, has 162–173 (staging, 2026-10-02).
