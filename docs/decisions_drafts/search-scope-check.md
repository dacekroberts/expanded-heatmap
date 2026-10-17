### 2026-10-13 - Place search: the scope check measures how far an index reaches (rule D; branch search-scope-check)

Owner-approved fix (2026-10-13) for the hole Mendoza fell through. Built on
`search-scope-check`, cut from `search-integration` at 73f025df. Nothing
pushed.

- **Why the check passed Mendoza.** Rule B counts the map's stations per
  NAMED AREA and asks nothing about an area's size. The scaffold named
  relation 153540, the province, where the department (2204157) was meant.
  The summary's area was one entry, "Mendoza", holding all 7 stations, so A,
  B and C passed an index of 12,470 rows, 5,693 of them more than 25 km from
  any station and the farthest 522.2 km out (search-rollout at b2e671b2, the
  commit before f04f9939). Any area that is too large and still holds a
  station passes B the same way.
- **Rule D.** `scripts/check_place_scope.py` now measures the great-circle
  (haversine) distance from each index row and each intersection row to the
  nearest station marker of the committed map (`outputs/<slug>/heatmap.html`,
  read by the marker colour the search script itself uses) and fails a city
  whose farthest row is more than 25 km out. Never a difference of degrees:
  two selftest cases at 60 N hold that. Committed files only; no fetch.
- **The recorded reason.** `config.PLACE_SCOPE_REACH_REASON`, a dated string,
  read from the config's text. A city over the limit with one passes, the
  reason printed as a note. A reason with no date fails; so does a reason on
  a city within the limit, so the reasons only shrink.
- **A map with no station marker fails**, as does no map: an unmeasured
  reach is not a pass. All 237 measured cities had markers.
- **Measured before the limit was fixed in place** (237 cities on five
  branches, 239 distinct states; `data/_search_rollout/scope_reach.md`):
  median 10.4 km, 75th percentile 19.8, 90th 30.9, largest 267.1. 202 cities
  are at or under 25 km, 35 over. This branch's 19 pass, São Paulo the
  farthest at 24.2 km and Hong Kong at 24.0.
- **The 35 are for the owner: no reason was written and the limit was not
  moved.** Two read as faults: Bremen (53.9 km; relation 62559 holds
  Bremerhaven's streets, which reads as the state for the city, Mendoza's
  fault again; the relation's admin level is not confirmed, no network) and
  Naha (267.1 km; one row, a national route's sea section, the outline
  reaching 9.7 km). Nagasaki's farthest row is the same sea-section class.
  The other 32 are a municipality's own far corner (islands, mountains,
  annexed land), each listed with a proposed reason.
- **Cost.** 3.5 s for the 19 cities; 30 s in the first form, which measured
  every point against every nearby station on a 0.05 degree grid. The
  selftest holds the grid search to a full search's answer. Selftest 11 to
  27 cases, the old Mendoza state among them.
- **Also changed:** `docs/commands.md` (the usage line, `--reach`) and the
  place-search-city skill's floor-and-ceiling bullet.
- **For the merge.** `scripts/place_search_night.py` calls `check_city`, so
  a night build of a city over the limit will report rule D until the owner
  has ruled on it.
