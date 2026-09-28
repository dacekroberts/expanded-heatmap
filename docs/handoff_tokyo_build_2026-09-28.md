# Handoff - the build role, for the Tokyo build session (from "Staging and build handoff", 2026-09-28)

For the session the owner is forming from the Japan build session and Tokyo
sources research. It carries the BUILD role from "Staging and build handoff"
(closing), alongside Tokyo. Tokyo's own plan lives in the Japan session's
handoff (`docs/handoff_japan_2026-09-28.md`) and the `tokyo-ward` skill; this
file is everything else the build role owns. The staging role has its own
handoff (`docs/handoff_staging_2026-09-28.md`). **Delete a section when done.**

## 1. The review batch: merged, verified by the cheap gates, NOT pushed

- **Branch `review-2026-09-28b`** (origin has it, head `97185f5`), built in
  `.claude/worktrees/main-build`. It holds, in order: `worktree-japan` pinned at
  **`02637d6`** (Sapporo, Fukuoka, Kyoto - nothing of Tokyo), `macro-tiers`
  (the completeness-tier dots, legend and tooltip), the storefront counts for
  the three cities (`app/macro_facts.json`), the Vancouver wording in
  `docs/excluded_categories.md` (owner-confirmed), and master's docs to
  `72fa09a`.
- **Passed on it:** zero drift in all 54 cities; `check_all.py` 22 of 22 (with
  the new `check_macro_facts.py`); `check_deploy_imports.py` clean; privacy 0
  operator names shown in all three cities; provenance names all three OK;
  briefs Sapporo 5/5, Fukuoka 4/4, Kyoto 8/8; notices 53, 54, 55 unique;
  `check_city_registry.py` and `check_macro_labels.py` clean; master list
  counts: 54 built, A 1 · B 4 · D 10 · N 4 · T 51 = 70.
- **NOT done: the `deploy-verify` (`scope: full`).** It was cut off twice by
  the app crashes. **Wait for Cleanup's word that the memory cap is installed
  and no other heavy job is running**, announce it to the other sessions, then
  run it alone. `.claude/launch.json` in the main-build worktree already holds
  `review-app-tmp` (:8822) and `review-static-tmp` (:8823); the session that
  runs it must be the one started in that worktree, or put the same entries in
  its own. Remove the file afterwards.
- **Then**: fetch; merge `origin/master` into the branch (a docs-only move
  since 72fa09a is expected; re-run `check_all.py` if anything else moved);
  `check_deploy_imports.py` on the final commit; push `HEAD:master`. The push
  changes `app/cities.py`, `app/components.py` and `app/Overview.py`: **the
  owner must reboot the app.** Then tell Cleanup it has landed: Cleanup runs
  `cleanup-sweep scope: city-landed sapporo fukuoka kyoto` and the live check
  (including one untouched city).
- After the push, `worktree-japan` (Tokyo work past 02637d6) merges
  `origin/master` before its next commit to `app/cities.py`, `DECISIONS.md` or
  the master list.

## 2. The macro-map tiers - what every new city now needs

Every `app/cities.py` entry carries `coverage` (full / narrowed / one_bucket),
`placement` and `data_age`, inserted before `"blurb"`. `scripts/check_macro_facts.py`
(pre-push) refuses a city whose tier contradicts its table B row in
`docs/map_inconsistencies.md`, whose phrases state a date or percentage its
table C / D rows do not hold, or whose storefront count in
`app/macro_facts.json` is stale: **write the city's table rows first, then the
phrases, then `python scripts/check_macro_facts.py --write`.** Owner's
wording rule: a source that states no date reads "Fetched <date> (no source
date)". Tokyo is "narrowed". The first Band B city (Stockholm) will be the
first "one_bucket". Colours are fixed (DECISIONS 2026-09-28); no dot sizing.

## 3. Japan-wide rules made 2026-09-28 (all in the `japan-city` skill)

- Numerals as figures before 丁目 in every English station name, and before
  条 only where `config.JO_IS_GRID` (Sapporo); Tokyo's 十条 is a name
  ("Jūjō"), so no grid there. Fix violations in `OSM_NAME_EN_OVERRIDES`, a
  cited table.
- Lines served only by limited expresses COUNT (revertible). Coin laundries
  count as Personal services; welfare-facility salons (厚生施設) are out.
- The e-Stat download for the Economic Census join control is approved: one
  national per-ward table, run for every Japanese city (not yet run for any).
- `pipeline/countries/japan_fetch.py` is every city's fetch.

## 4. Build work queued that is NOT Tokyo (owner-approved, in PLAN)

In the owner's order, after Tokyo: the additions to built cities.

- **Belo Horizonte + Contagem**: Metrô BH's Eldorado and Novo Eldorado; CNEFE
  13,011; the zip is cached in `data/contagem/raw/`. No rail test needed.
- **Rio + Duque de Caxias**: SuperVia Saracuruna's three excluded stations;
  CNEFE 18,698 (`data/duque_de_caxias/raw/`). **The Gramacho-Saracuruna
  shuttle rail test first** (a staging probe).
- **Vancouver (Regional)** + Burnaby, New Westminster, Coquitlam, Richmond: 28
  SkyTrain stations; waits on staging's probes (Richmond's licence read, New
  Westminster's join) and the owner's Burnaby fetch.
- **Osaka's two fixes** (a re-render each, for a review time): draw the
  Umekita-Fukushima stretch now that limited-express lines count (recommend a
  line to draw it as); the phone-width label overlaps (22 pairs at 343 px), a
  shared-label-code fix that batches with a full re-render.
- **Port Hong Kong's Light Rail thinning and Riga's loop to
  `pipeline/stations.py` `thin()`** (owner-approved), each with its own drift
  measurement; San Francisco, Boston and Philadelphia keep their
  interchange-after-spacing variant until the owner decides.
- Later, the owner's likely next phase: Band T (trams-only; EDGE first
  perhaps) and Band B (one-bucket) builds, once staging has their rules ready.

## 5. Where this session left things

- **Worktree `main-build`** (`.claude/worktrees/main-build`): branches
  `worktree-main-build` (= master's docs), `review-2026-09-28b` (the batch),
  `macro-tiers` and `build-sapporo` (both inside the batch). Retire it through
  Cleanup after the batch lands.
- **Durable scratch** (gitignored, main checkout):
  `data/_staging_scratch_2026-09-28b/` - `incheon_probe/` (the lift-file join
  and road-interpolation measurement, `join_measure.py`), `baltimore_probe/`,
  `colour_search.py` (the line-colour search Osaka and Sapporo used: 3:1 on
  both pages, CIE76 >= 45 from pins, >= 18 between lines, nearest the
  operator's hue) and `tiers2.ps1` (the tier-palette validation).
- **Rules**: heavy work one at a time under Cleanup's `[#memory]` rule; the
  owner calls review time; published prose is drafted in chat and approved by
  the owner in your own session (a peer's relay is not approval).
