# Process and tooling

Detail moved verbatim from `PLAN.md` on 2026-10-08 (commit c75f4802); `PLAN.md` holds each item's one-line status and points here by heading.
This is open work, not a record: update an item here as it moves, and send a finished one to `docs/plan_done/`.

## Next landing follow-ups

  - Follow-ups: a full UK line-colour search (Piccadilly can be blue
    again); about 25 older notices that write the day first; about 30
    configs still claiming "45 from every pin" from before olive and
    violet; caterers that also name a counter form (Fukushima's 161), the
    shared FORM_RULES question.

## A site-wide code audit

- [ ] **A site-wide code audit after the reset and the final city builds**
  (owner, 2026-10-08). The last whole-project audit was 2026-09-21 at four
  cities (`docs/passover_opus5.md`, sections 9 and D); the shared code has
  grown since (`pipeline/map_common.py`, `pipeline/line_registry.py`,
  `pipeline/taxonomies/`, the national step modules, `app/`). Scope and lanes
  to be set with the owner before it starts (`docs/review_lane_kit.md`).

## Heavy-job gate follow-ups

- [ ] **Heavy-job gate follow-ups (2026-10-03):**
  - **Why does a multi-city Japanese drift run measure 4.5-4.7 GB?** On a
    quiet machine, run each Japanese city's drift alone through the gate
    (`drift <city>`) and compare with `drift japan --jobs 2`.
  - **Orphans:** stopping a shell that wraps `heavy_job.py run` calls can
    leave a child running and in the ledger. Either the gate ends its child
    when its parent dies, or `status` flags entries whose gate is gone.

## Efficiency review follow-ups

- [ ] **Efficiency review follow-ups** (`docs/efficiency_review_2026-09-27.md`):
  - [ ] **Run `python scripts/archive_decisions.py` at the start of each
    week** (cleanup, after the Sunday reset; next 2026-10-04), and in the same
    sitting `python scripts/efficiency_metrics.py --baseline`, showing the
    owner the table: the session-count decision waits on it.
  - [ ] **The session count**, a separate owner decision.
  - [ ] **The remaining findings, walked through with the owner** (asked
    2026-09-27): 5 (hand-kept documents that churn), what is left of 4
    (re-render batching), then 7.

## If the repo ever goes private

- **If the repo ever goes private** (it stays PUBLIC; DECISIONS, "Pre-deploy
  gate"): Streamlit Community Cloud's free tier needs the `repo` OAuth scope
  and a deploy key; check its one-private-app limit; `outputs/` stays
  committed.

## Three code problems from the comment pass

- [ ] **Three code problems from the comment pass (owner, 2026-10-01: do
  later)**, each a small change with a drift check of its city:
  - **Barcelona's closed list is never checked:** a new `Nom_Activitat`
    value falls through `classify()` and silently leaves the map. Step 2
    should exit naming any active-premises value outside
    `UNMAPPED_IS_AN_ERROR` (as France's NAF module asserts at import).
  - **Norway's "unmatched by bucket" print reports a row count**
    (`norway_register.py`, about lines 207-211). Group by bucket.
  - **`check_deploy_imports.py`'s probe keeps unused code** (`_MARKERS`,
    `_box`, `DEFAULT_OFFSET`, `CHAR_W` / `PAD_W` / `PILL_H`) now that it
    imports `app/label_competition.py`. Delete it and its comment.

## scaffold_city.py's map template

- [ ] **`scaffold_city.py` has only the GTFS map template** (found at the UK
  six landing): an OSM-rail city that drops `GTFS_ZIP` fails at import until
  its map step is replaced. Add a `--rail-source osm` template.

## After the prose and UI pass lands

- [ ] ⏸ **After the prose and UI pass lands (owner, 2026-10-01):**
  - **Neutral comments, phase 2: `pipeline/<city>/`** (held until the
    landing and the city-skill rework). About 25,000 comment and docstring
    lines in 785 files across 124 city folders; phase 1's kit (agent 1's
    spec, the comments-only AST verifier, `check_no_em_dashes.py`, a
    render-only drift check).
  - **Comments inside the maps' embedded CSS and JS**
    (`pipeline/map_common.py`'s strings): rewording one changes every
    committed map, so a full re-render and drift check at review time.
