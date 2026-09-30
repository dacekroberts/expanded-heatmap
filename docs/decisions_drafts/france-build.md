# DECISIONS drafts - the France builds (branch `france-build`)

Entries for `DECISIONS.md`, newest first, each exactly as it should land
(owner's rule of 2026-09-30: build sessions keep drafts; cleanup folds them
in when handed off). Anything that must cite a DECISIONS verdict cites this
file until then.

### 2026-09-30 - Le Mans built on the shared French tram module: 35 stops, 1,991 storefronts; a French step 2 peaks at 0.37 GB

- **The first of the France batch, and the shared module's control.**
  `pipeline/countries/france_tram.py` (steps 1 and 3) and
  `france_tram_fetch.py` (downloads) now carry the owner's station rule, the
  commune and regional scopes, gate 3 from OpenStreetMap, and both geometry
  sources. A city's fetch, step 1 and step 3 are three-line wrappers, which
  `scripts/scaffold_france_batch.py --go` writes. Le Mans took SETRAM's
  `gtfs_setram_lmm_auto` resource. It self-attests: Mecatran, 2026-09-25 to
  2026-11-11, fetched 2026-09-30.
- **Rail:** route_ids `T1` and `T2`, colours `#E4151E` and `#0D65AE` (the
  feed's own). 70 platforms become 35 stations (every platform has a parent);
  all 35 are inside commune 72181, T1 24 and T2 18. **Gate 3 is exact**
  against OpenStreetMap's route relations (24 and 18). Median gap 437 m (min
  238), so the half-size rings. Geometry is the feed's `shapes.txt`, two
  shapes per line.
- **Business:** SIRENE, September 2026 edition. The funnel: 85,363 rows
  under 72181, 29,395 active, 24,765 diffusible (**15.8% masked**), 3,624 in
  divisions 47, 56 and 96, 1,283 structurally excluded, 2,341 storefronts,
  and 1,992 after the precedent's catch-alls. **96.09Z at 13.0%** is inside
  the five cities' 9.6-14.0% range, and 56.29B is at 1.9%. Coordinates joined
  for 100.00%, one centroid-grade row dropped: **1,991 storefronts** (900
  retail, 632 food, 459 personal). Premises name on 59.7%. Food is 1.79
  times the screen's OpenStreetMap count. 1,462 (73%) sit within a ring.
  Legacy codes: none under 72181 (geo.api.gouv.fr's communes associées and
  déléguées, with Lille's 59298 and 59355 as the control).
- **`check_personal_exposure.py le_mans`: PASS on the structural guarantee.**
  No registrant-name column is loaded. 0 contact details; 0 of 1,462 pins
  are a person-like name at a residential unit. The heuristic flags 18.5% as
  person-like, against Rennes's 17.9% on the same code. The twenty batch
  cities are registered in the script in one entry.
- **A French SIRENE step 2 is not a heavy job**: a measured peak of
  **0.37 GB** (psutil, the process and its children), because it streams
  row groups of at most 7 MB uncompressed for the columns it reads. It was
  announced to every live session with the measured figure.
- **The page** is the approved template with Le Mans's braces. No line leaves
  the commune, so the template's bracketed "where a line runs past it"
  sentence is left out as the template intends. The density paragraph ends
  at this city's ratio; Rennes's comparison with its siblings was Rennes's
  own fact. The page also adds a business caption carrying INSEE's
  prescribed « Source : Insee » with the SIRENE edition. None of the five
  built French pages carries that string; a separate task was raised for
  them, since it is an `app/` change to published pages.
- **Still to do before Le Mans lands** (at review time, with its landing
  group):
  - `map_inconsistencies.md` rows and `macro_facts.json`;
  - its macro label width, measured in a browser, in one pass for the group;
  - `ring_shares.json` and the README list;
  - its `excluded_categories.md` section;
  - its `docs/data_sources/france.md` rows (feed, contour, OSM);
  - the cities.py `mode` once macro-legend lands.
