# DECISIONS drafts - branch `drift-render-only` (drift and render agent)

Kept here under the owner's rule of 2026-09-30: build sessions keep their
entries in their own drafts file, and the cleanup session folds every drafts
file into `DECISIONS.md` in one pass. Newest first, each entry exactly as it
should land.

### 2026-09-30 - drift_check --render-only: the map step alone, zero drift on master's 124 cities

**Built** `pipeline/drift_check.py --render-only` for changes that touch only
map rendering (a line-highlight change to `map_common.py` is next, and all 124
maps must re-render after it). It runs one step per city and diffs `outputs/`
exactly as the full check does. The full sweep stays the default and the
pre-deploy gate.

- **"The map step" is the file named `step*_map.py`, not "step 3".** Measured
  over the tree: 117 cities have step3_map.py, seven have step4_map.py after a
  step3_geocode.py (Los Angeles, New York, Sacramento, Toronto, Washington
  D.C.) or step3_place.py (Dallas, Houston). All seven of those step 3s write
  `data/<city>/processed/businesses_geocoded.csv`, a map input, and nothing in
  `outputs/`, so leaving them out loses no output. Geocoding is not rendering,
  and running it would put a network-capable step in a render check. A city
  with no map step or two is refused.
- **Refused, not passed: a city whose `data/<city>/processed/` is missing or
  empty.** It counts as a failure and names the full check to run instead.
  The map step's own "Missing ... Run the earlier steps first" still catches
  a single missing file.
- **What it assumes is printed per city**: how many processed files there are
  and when the newest was written, since `data/` is shared by every worktree
  and holds whatever the last steps 1-2 run on any branch left there.
- **Baseline counts are not checked** in render-only (no map step emits any;
  grepped), and `--update-baseline` with `--render-only` is refused, since the
  counts come from steps the mode does not run.
- **The offline guard still applies**: the map step runs with
  `HEATMAP_NO_NETWORK=1`, as every step under the full check does.
- **Selftest** `scripts/drift_check_selftest.py`, in `check_all.py`: fake
  cities in a temp tree prove the step choice (step4_map.py alone where a
  geocode or place step precedes it), each refusal, that the map step runs
  offline and alone, that the full path still runs every step in order; the
  live tree is the positive control (every city has exactly one map step).
- **Run on master (8fb44e7c) through `heavy_job.py`, `--jobs 2`: zero drift**
  on all 124 cities. Wall time 231 s; per city 1.7 s to 24.7 s (Paris; Seoul
  16.5 s). Measured peak 1.79 GB for the whole run, declared 4.5 GB on a
  Seoul-alone measurement of 1.93 GB (14.6 s). The 124 rewritten maps were
  restored with `git checkout -- outputs/`.
- **Not done: more than two cities at once.** `MAX_JOBS` stays 2; whether
  render-only may run more is an owner call, raised in the agent's report.
