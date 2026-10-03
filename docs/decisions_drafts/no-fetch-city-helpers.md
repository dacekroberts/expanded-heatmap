# DECISIONS drafts - no-fetch check follows city helpers (`no-fetch-city-helpers`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - check_no_fetch_in_steps.py follows every module a step imports

- **`scripts/check_no_fetch_in_steps.py` now follows a step's imports
  transitively into every module under `pipeline/`, not only
  `pipeline/*.py` one level deep.** The Seattle (Regional) build's gap
  ("A gap in a shared check", `docs/decisions_drafts/seattle-tbilisi.md`):
  `pipeline/seattle/lcb_offpremise.py` and `sno_food.py`, imported by Seattle's
  step 2, were never read, and neither were `pipeline/countries/`,
  `pipeline/taxonomies/` or another city's step a step imports. The walk
  resolves `pipeline.<city>.x`, bare sibling imports (a step run as a script
  has its own folder first on `sys.path`) and relative imports, and counts
  each parent package's `__init__.py`. Reaching `pipeline.taxonomies` counts
  as reaching every taxonomy module, because `load_taxonomy_module()` imports
  them through importlib. A step's reach is 4 to 65 modules (Seattle's step 2:
  63). The verdict on the tree did not change: 382 steps, 0 unguarded, the
  same 6 guarded through `census_geocoder.py`.
- **The one exception is an HTTP import FENCED inside a module-level function
  named exactly `fetch`, and it holds only while nothing a step reaches
  references that `fetch`** (`m.fetch`, `from m import fetch`, or the module
  calling its own `fetch` outside its `__main__` block); a step file gets no
  fence. That is the shape `lcb_offpremise.py` already has (`import requests`
  inside `fetch()`, called by `fetch_sources.py` only), now listed as FENCED.
  Rejected: failing any module that holds an HTTP client anywhere, which
  would force the Liquor Board download out of the helper that reads it; and
  exempting by convention or comment, which no check can hold.
- **`check_no_fetch_in_steps_selftest.py` grew from 6 cases to 12**: a city
  helper fetching at import, the same reached by a bare sibling import, the
  fence's HTTP import hoisted to module level, a step calling the helper's
  `fetch()`, the helper's own `load()` calling it, and a taxonomy module
  fetching; all 13 runs (12 cases and the unmodified copy) behave. The tree is
  now copied once per run and each case restores what it broke (the
  unmodified run comes last and proves it), since copying the whole pipeline
  tree (about 900 files) per case took 65 s; one copy takes 25 s.
- Prose that described the old reach was brought up to date:
  `docs/rule_history.md` (no-fetch, and the selftest's count),
  `.claude/skills/consistency-sweep/SKILL.md`'s check table, and
  `pipeline/osm_cache.py`'s docstring ("one level deep"). CLAUDE.md's
  "including through shared `pipeline/*.py` modules" is still true and was
  left for the owner.
