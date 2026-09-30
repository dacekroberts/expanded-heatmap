# DECISIONS drafts - Czech kit (`worktree-czech-kit`, then `czech-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - czechia_register reads several obce and RES in chunks; Prague reproduced byte for byte at a 0.37 GB peak

- **The Czech builds have the owner's go, confirmed in this session**
  ("Go ahead", 2026-09-30). The tram kit relayed it with six working rules,
  and this session asked the owner to confirm before scaffolding anything.
  The builds follow the rules: business legs first, and the Czech rail steps
  once `pipeline/osm_tram.py` is on the tram build branch. Every entry goes
  here, not in `DECISIONS.md`.
- **`pipeline/countries/czechia_register.py` now reads one RÚIAN file per
  obec.** A city that spans two obce (Liberec with Jablonec, Most with
  Litvínov) declares `OBEC_CODES`, `RUIAN_ZIPS` and `RUIAN_CRS_CONTROLS`,
  each keyed by obec. Every file runs its own coordinate control, and the
  files concatenate, with an exit if an address code repeats. Such a city's
  output gains an `obec` column and a per-obec count for its page. Prague's
  one-obec config (`OBEC`, `RUIAN_ZIP`, `RUIAN_CRS_CONTROL`) takes the same
  path as a single entry, so its output is unchanged. **Rejected:** a
  regional step 2 per city that calls the module twice and concatenates.
  That would put the obec loop in two city folders instead of one shared
  place.
- **RES is read in 500,000-row chunks, keeping only the owners the city's
  establishments point to**, rather than the whole 543 MB file at once.
  Filtering before the dedupe keeps each ICO's first row in file order, as
  the whole-file dedupe did.
- **The control: Prague, run from the build branch into the scratchpad.**
  The shared `data/prague/processed/` was not touched (the shared-junction
  rule). The output's SHA-256 matched the saved baseline (`9153d4d0…`), and
  all five baseline counts matched `outputs/prague/baseline.json`:
  84,192 in obec, 27,327 bucket rows, 26,711 storefront rows, 25,185 placed
  and 12,932 named. **Measured peak 0.37 GB RSS in 17 s**, so a Czech step 2
  is not a heavy job under the owner's 2 GB margin rule. The Czech step 2s
  run one at a time, each announced as a 0.5 GB job. `drift_check.py prague`
  was not run, because it would rewrite the shared processed files from a
  branch; the byte-identical step 2 output is the same test for this change,
  and the lander re-runs it at merge.
