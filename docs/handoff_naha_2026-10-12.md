# Handoff: Naha (worktree `japan-naha`, branch `worktree-japan-naha`)

Written 2026-10-12 by the Naha build session, for Cleanup (the landing) and
for whoever builds the Urasoe add-on. Nothing is pushed. The reasoning is in
`docs/decisions_drafts/worktree-japan-naha.md`.

## State

- **Built and committed**: `pipeline/naha/`, `outputs/naha/`, page 307, notice
  217, the rows in `docs/data_sources/japan.md`, `docs/data_sources.md`,
  `docs/excluded_categories.md`, `docs/map_inconsistencies.md` and
  `docs/privacy_verdicts.md`.
- **Green**: `drift_check.py naha` zero drift with a baseline recorded;
  `check_personal_exposure.py naha` (Japan pass 0); `check_scope_disclosure.py`;
  `check_line_identity.py`; `check_deploy_imports.py`; `check_map_view.js` and
  `check_map_attribution.js` at 1024 and 375 px.
- **Failing on purpose in `check_all.py`** (two checks):
  `check_provenance.py` on the master list's counts only (Staging's);
  `check_macro_labels.py` on the Kyushu-Okinawa view (parked call C,
  Cleanup's).

## At the landing

1. `app/cities.py`, `app/components.py` (notice 217, placed after Morioka's
   186), `app/osm_notice.py`, `scripts/check_personal_exposure.py`,
   `pipeline/countries/japan.py` and `app/label_competition.py` will conflict
   with the other phase 2 branches where each appends: keep both sides.
2. Run `python scripts/regen_generated.py` after the merge.
3. The Kyushu-Okinawa view needs its fit decided before `check_macro_labels.py`
   passes (parked call C).
4. `app/` changes, so the deployed app needs a reboot after the push.
5. A full `deploy-verify` has not run; one local render of the page was looked
   at (scope `city-added` at review time).

## Parked calls (five, in the drafts file)

A. One renewal file (August 2020) carries both 業種 and 営業の種類 and reads
its form as its type: 20 in-term restaurants are missing until a shared rule
reads it. After the fix, re-run steps 2 and 3 and remove the two disclosure
phrases named in the call.
B. One renewal file (October 2016) heads its type 種目; no effect today, and
the config stops the build if that changes.
C. The Kyushu-Okinawa view.
D. The page, What Is Excluded and notice sentences no template covers.
E. The line's name ("Yui Rail") and four romanised station names.

## For the Urasoe add-on

- The line is registered as `okinawa-urban-monorail` in
  `pipeline/line_registry.py` (#E84028); add `"urasoe"` or the regional slug
  to its `maps`.
- The three Urasoe stations are in `outputs/naha/excluded_stations.csv`.
- BODIK: `config.FETCH_PAUSE_S` (21 s after each real download) and
  `config.source_url` (a URL built from pinned resource ids) are available in
  `japan_fetch` for any city with many BODIK files.

## A newer month

BODIK adds a new-permit file each month and replaces the two registers whole.
A refresh is a new entry in `pipeline/naha/bodik_files.py`, a new `AS_OF`,
`python pipeline/naha/fetch_sources.py city` (one file every 21 s), and every
count on the page and in the docs re-measured.
