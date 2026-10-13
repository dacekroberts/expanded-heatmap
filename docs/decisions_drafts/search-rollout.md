### 2026-10-13 - Search rollout: the extract run's 151 cities rebuilt on the third and fourth rule passes (branch search-rollout)

- **Committed the extract run as it stood (cfa030e7), merged master at 50d551f4 (6c82294a, no conflict), then rebuilt all 151 cities in three stages, each committed whole.** Nothing rendered, nothing pushed, no shared rule code edited. The record is `data/_search_rollout/extract_rules34/summary.md` and `.json`, with the check logs beside them.
- **Re-filtered all 151 with `place_extract_fetch.py <city> --force`, from the extracts on disk.** Each run named its file with `--pbf` (two files for Gimpo and Incheon) and ran with `HEATMAP_NO_NETWORK=1`, so no request was possible; `--force` wrote over this run's own three caches only. Reason for `--pbf`: without it the script chooses a region and can ask the server for sizes. 151 of 151 exit 0, none skipped. The shared-border rule admits 243 street ways in 10 cities: Recife 48, Fortaleza 34, Porto Alegre 30, Belo Horizonte 29, Valenciennes 28, Grenoble 23, Rouen 18, Bordeaux 16, Lille 11, Nantes 6; the other 11 cities with several municipalities gain none.
- **Wikidata lookup: one job, one city after another, 1,942 entries in 118 cities, every batch answered at its first try.** 33 cities carry no entry on a work of public art or a library; nothing was asked for them and no cache file exists, so their step reads the tag alone, which gives the same result. Bordeaux has one entry Wikidata does not hold.
- **All 151 indexes rebuilt, no step stopped.** Rows across the 151, before to after: stations 6,807 to 6,479; junctions 22,426 to 22,426; landmarks 82,664 to 81,314; places 64,091 to 64,004; streets 283,931 to 284,122; intersections 573,077 to 573,849. Public art kept: 456 with a wikipedia tag, 97 without (on Wikidata); libraries 198 and 53. The split is counted from the id side file and the caches, not printed by the step. The largest first-open index is Rio de Janeiro, 640 KB gzipped.
- **Not decided here, for the owner or the eye read:**
  - Check E, 334 names carrying a leak word in 73 cities (Toulouse 38, Dijon 25, Yongin 22, Lille 20, Uijeongbu 14, Bucheon 12, Bordeaux 11, Montpellier 10): a rule, a drop or a `PLACE_REVIEWED` entry each. The list is `check_place_search.log` in the summary folder.
  - `check_place_unopened.py` B, 54 stations the builds skipped as not open and the watch file lacks: Montpellier 35, Salvador 7, Belo Horizonte 5, Gimhae 2, Anyang, Gwangju, Incheon, Rio de Janeiro and Uijeongbu 1 each. Each row needs its line and where the line came from, so none was written.
  - Most and Yamagata still carry the summaries of their failed builds (no `stations_not_open`). Neither is among the 151; both wait for `PLACE_QUIET_STATIONS`.
- **Found, not fixed: `check_barred_marks.py` reads Angers's barred mark inside Mendoza's street names.** `app/static/places/mendoza.json` holds "Hipólito Irigoyen", "Bernardo de Irigoyen", "Barrio Irigo Giorgiani" and three more, and the check matches the mark as a substring. The names were in the index before this rebuild. Whether the check should match whole words, or skip another city's index, is a call on shared code.
- **`check_all.py`: 70 of 73 pass.** Failing: `check_place_search.py` (rule A on all 151, expected with no render, and E above), `check_place_unopened.py` (above) and `check_barred_marks.py` (above).
- **Not done:** no eye read, no render, no browser test, no row written to the unopened-stations watch file.

### 2026-10-13 - Night runner: the extract source (branch search-rollout)

- **Gave the night runner a second source, `--source extract`, and left
  Overpass the default.** `scripts/place_search_night.py` now runs the
  lookup as one `place_search_area_lookup.py --source extract` child and
  each city's fetch as its own `pipeline/place_extract_fetch.py <city>`
  child, both through the job gate, with no mirror queue, no `--hosts`
  (refused with this source) and no 60 s Overpass wait. The scaffold, the
  gated index build, the checks and the report are the same code for both
  sources. Reason: Overpass was down or slow all of 2026-10-13 and the first
  night left wave 2 scaffolded and unfetched. Rejected: making the extract
  route the default, which is the owner's call and was not given.
- **Capped extract fetches at three at once, and counted a build as one of
  them.** `--workers` takes 1 to 3 and defaults to 3: the gate admits four
  heavy jobs on this machine and one place stays free for other sessions
  (owner's brief). An index build is started beside the fetches only while
  fewer than `--workers` of them run, so the runner never holds more than
  three places. Rejected: four workers with builds deferred, which would
  have left no place for another session's job.
- **Declared 3.5 GB a fetch to the gate, as an estimate.** Measured peaks
  were 0.9 GB for a 102 MB file and 2.5 GB for 696 MB (osm-extract skill),
  close to linear in the file's size; 3.5 GB is that line at the fetch
  script's own cap of 1,000 MB. Left unstated, the gate takes its default of
  8 GB for a label it has never measured and would refuse the second of
  three children. The lookup child declares the same figure, an upper
  bound: its peak was not measured. To re-measure if `MAX_MB` rises.
- **Ordered fetches by regional file: the first city of a region runs alone
  for that region.** The runner works out each city's region offline, the
  way `choose_extract` does (the outline cache when there is one, else the
  stations), from the region index on disk and with no request. One city of
  a region is started; the others of that region wait until a child has
  printed the file's data date, then run side by side. Cities of other
  regions fill the remaining places meanwhile. A region that cannot be
  worked out offline is treated as one shared unknown, one city at a time.
  A wrong grouping costs a wait on the download lock, never a wrong cache:
  the child chooses its file for itself. Rejected: starting three cities of
  one region at once, two of which would sit on the download lock for the
  length of the download.
- **A first city stopped by its regional file fails the rest of that region
  with no child started.** Three kinds are the file's own: over the size
  cap, refused by the download ledger, a download the server did not
  complete. The next city would be stopped the same way, and each try
  costs the server a request. No failure is tried twice in one run;
  `--retry-failed` is the second try, and it clears these with the rest.
- **Kept each failure with the script's own last line.** Classes, read from
  the wording in `pipeline/osm_extract.py` and
  `pipeline/place_extract_fetch.py`: region (none covers the city, or the
  area reaches past its region), size cap, ledger, download, stale (an
  extract older than 7 days), scope stop, lock, timeout, other. A refusal by
  the job gate is not a failure: the city is left waiting and a plain rerun
  fetches it, as a refused build already was. The selftest fails if one of
  the phrases the classifier reads leaves those two files.
- **Added `--skip-cities` for either source.** The named cities are taken
  out of the waves before any step and listed in the report as held out; a
  name in no wave is said, not refused. Built for the owner's ruling that
  Madrid, Rome, Milan and Toronto go last as one batch (2026-10-13). The
  state file keeps what it already held for a skipped city.
- **The report names the source.** With the extract source it carries one
  line saying no Overpass request was made, a table of each regional file
  read (region, data date, bytes, downloaded or held, the cities that read
  it) and a table of each city's seconds and peak memory as the script
  printed them, with the gate's measured peak beside. The seconds are the
  script's whole run, so the city that fetched a file carries its download.
  An Overpass run's report is unchanged.
- **Did not pass `--max-mb` through.** The size caps stay the scripts' own
  (1,000 MB for a fetch, 800 MB for a lookup): a larger file is a person's
  call by the extract route's own rule, and a city stopped by the cap lands
  in the report under its own heading.
- **Selftest 41 to 66 cases; no network and no extract in any.** The 25 new
  cases drive stand-in children through every class above, the three-place
  limit, the first-city rule, `--skip-cities` on both sources, the argument
  refusals, a rerun, `--retry-failed`, a state file switched from Overpass
  to extract, and the dry run.
- **Dry run on the real waves file, wave 2 (25 cities, all scaffolded, none
  fetched):** ten regional files, none held: six Czech regions with one city
  each (ustecky, olomoucky, liberecky, plzensky, moravskoslezky,
  jihomoravsky), south-korea for 16 cities, islas-baleares, argentina and
  noord-holland. Written to
  `data/_search_rollout/extract_2026-10-13_dryrun.txt`. No real run was
  started and no file was downloaded by this work.
- **Merged origin/master (86aadced) and place-extract into the branch
  first, after committing wave 2's scaffold as it stood.** Both merges were
  clean. `scripts/regen_generated.py` rewrote `app/ring_shares.json` after
  the master merge: 19 `map_blob` hashes, the 19 maps re-rendered by
  86aadced, whose own copy of that file still carries the old hashes. For
  Cleanup: master's `ring_shares.json` is one regeneration behind.
- **`scripts/check_all.py`: 72 of 73, the one failure not this change's.**
  `check_place_unopened.py` fails for the 25 wave 2 cities, each for an
  `outputs/<city>/place_search.json` that does not exist yet: they are
  scaffolded and not built. It clears when their index steps have run.
