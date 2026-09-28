# Handoff - one shared thin() (from "Tram rescopes", 2026-09-27, late)

Written for a FRESH session on a fresh branch. Read it once and follow the
pointers. Delete this file in the commit that finishes the job.

## Start only when the tram batch is on master

```bash
git fetch origin
git merge-base --is-ancestor eedeb32 origin/master && echo ready || echo "not yet - stop"
```

`eedeb32` is the commit that added Rome's copy of `thin()`, on
`worktree-trams`. If it is not an ancestor of `origin/master`, stop: the owner
has not called review time yet. Doing this on master first would leave two
copies to refactor and a conflict when the tram batch merges.

Once it is, make a new worktree and branch from `origin/master` (e.g.
`worktree-thin`). Commit on the branch, and don't push: the owner reviews it.

## The job

San Francisco's sub-transit-line thinning filter
(`docs/sub_transit_line_filters.md`: one stop per half mile along the line's
own route, every terminus and interchange kept) exists as three per-city
copies:

| City | Where | Distance | Returns |
|---|---|---|---|
| Amsterdam | `pipeline/amsterdam/step1_stations.py` `thin()` | **haversine on lat/lon** | `(kept set, [ {station, line, nearest_kept, miles_since_kept} ])` |
| Rotterdam | `pipeline/rotterdam/step1_stations.py` `thin()` | **haversine on lat/lon** | same as Amsterdam |
| Rome | `pipeline/rome/step1_stations.py` `thin()` | projected (`config.CRS_PROJECTED`) | `{name: reason}` |

**Lift one `thin()` into `pipeline/stations.py`**, beside `verify_stations`.
It takes:
- ordered stop-name sequences;
- a lookup from name to projected x/y (metres);
- the keep-always and interchange sets;
- a spacing in metres.

It returns the kept set and the cuts, each with the nearest kept stop and
the metres since it. Port all three cities to it. Measuring in the projected
CRS is the invariant (CLAUDE.md: never measure distance in EPSG:4326), so
Amsterdam and Rotterdam change method.

**Keep in the cities, not the shared function:**
- **Sequence choice.** Amsterdam and Rotterdam pick patterns with their own
  `sequences()` until every regular stop is covered. Rome walks OSM relations
  with the same coverage break. Thinning both directions and keeping the union
  barely thins: measured on Rome, it cut 4 of 16 against 9.
- **Reason wording, byte for byte**, so nothing drifts that the method change
  does not force:
  - Amsterdam and Rotterdam print `round(since, 3)`, so "0.33 mi" has no
    trailing zero;
  - Rome prints `:.3f`;
  - every reason must keep the word **"spacing"**, which
    `app/station_scope.py` classifies on.
- **Cut post-processing.** A station can be cut on two sequences; each city
  already filters cuts that some other sequence kept. Keep what each does.

## The drift you should expect (measured 2026-09-27)

Measured by wrapping each city's `thin()` during a real step 1. See the
DECISIONS entry "Measured before the shared thin() refactor".

- **No stop moves** in Rotterdam or Amsterdam: every line's kept and cut sets
  are identical under the two methods. The closest margin was Amsterdam's
  Inaristraat, 6.8 m from the threshold.
- **The cut reasons' mileage changes in 62 strings**: 21 in Rotterdam and 41
  in Amsterdam, each by 0.001–0.002 mi. Projected distances run about 0.2%
  longer here.
- **Rome should drift zero.**

So after porting:
- `python pipeline/drift_check.py rome` should report zero drift. Anything
  else is a port bug.
- `python pipeline/drift_check.py amsterdam` and `rotterdam` should show
  `excluded_stations.csv` changes **only in the reason column's mileage
  digits**. Confirm that before accepting it:
  - the station, lines and coordinate columns are identical;
  - the row count is identical;
  - about 41 and 21 reason strings differ, by 0.001–0.002.
- **If ANY stop moves** (a row appears or disappears, or `heatmap.html`
  changes beyond Folium's ids), stop and report which, for the owner. Don't
  accept it.
- Record the intended reason-text change with `--update-baseline` only if a
  baseline figure moved; row counts should not.
- Then `git checkout -- outputs/` for anything left modified with no real
  drift (CRLF churn).

## Also

- `python scripts/check_all.py` should pass, `check_scope_disclosure.py`
  above all.
- **Log it in DECISIONS.md with the `decisions-entry` skill.** Name the 62
  reason strings and point to the measurement entry; then run
  `python scripts/decisions_index.py`.
- **Out of scope, flag it rather than doing it:** San Francisco's own filter,
  `select_line_stations()` in `pipeline/san_francisco/step1_stations.py`, is a
  fourth implementation, also haversine. Porting it is a separate owner call,
  since SF's thinned set is the pattern's origin.
- **Hong Kong** also has a thinning function
  (`pipeline/hong_kong/step1_stations.py`). Check whether it is the same
  filter before claiming there are only three copies.
- **Git rules** as in `docs/handoff_build_2026-09-27.md`:
  - identity per command;
  - stage by name;
  - the Co-Authored-By trailer;
  - never amend or force-push.
