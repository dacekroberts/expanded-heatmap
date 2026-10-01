"""Station-count verification, shared - because it was wrong in four of five
Canadian cities, in five separate copies of per-city code, differently each
time.

WHY THIS IS A MODULE AND THE COLLAPSE ITSELF IS NOT
---------------------------------------------------
The tempting version of this file owns the collapse. It should not, and the
five builds are the evidence: every feed collapses differently, and the
differences are real rather than incidental.

    Edmonton    `parent_station` populated on all 65 stops - one groupby
    Calgary     no parent_station; a DIRECTION PREFIX (NB/SB/EB/WB), three
                suffix spellings including a typo ("CTrain Staion"), and a
                hyphen that MOVES between one station's two directions
    Toronto     no parent_station; THREE naming conventions in one feed - the
                subway hyphenates, the LRT does not, and Union Station names
                its destination - plus three stations appearing twice with a
                "- Subway" suffix
    Montreal    parent_station, plus an off-island fare-zone suffix
    Vancouver   regional, spanning two municipalities' stations

A shared collapse would have to grow a flag for each of those, and the flags
would be the per-city code again with extra indirection.

**What was missing every time was not the collapse. It was the check.** So
this module owns the checks, and every city's `step1` must call
`verify_stations()` on whatever its own collapse produced. The failures were:

  Toronto   234 platforms reported as 234 stations, twice - the second time
            after a correction, because one naming convention was handled and
            the other two were not
  Calgary   83 platforms reported as 83 stations. The duplicate-NAME assertion
            PASSED, because direction prefixes make every name unique; what
            failed was physics, a 17 m median
  Edmonton  33 "stations" of which three are garages and a tail track, where
            `pickup_type` and `drop_off_type` are 1 on every stop_time

Three gates, because each of those needs a different one:

  1. SPACING - the platform-vs-station diagnostic. A name check cannot catch
     Calgary; 17 m between "stations" can.
  2. BOARDABILITY - a stop a revenue trip touches is not automatically a place
     a passenger can use. Only Edmonton has needed this so far, and only
     because somebody looked.
  3. THE OPERATOR'S OWN COUNT - the one check that is outside the data. Toronto
     at 110 agrees with the TTC's published per-line figures; its earlier 118
     and 77 agreed with nothing, and no amount of internal consistency would
     have said so.

Gate 3 is the one to reach for first when a number feels wrong. The other two
are automatic; that one requires going and reading what the agency publishes,
which is exactly why it kept being skipped.
"""

import math

import numpy as np

# Below this, points are platforms rather than stations. Measured medians:
# Calgary's uncollapsed 17 m and Toronto's 69 m against collapsed 632-713 m,
# and San Francisco's genuinely street-running 134 m, which WAS thinned.
STATION_SPACING_MEDIAN_M_MIN = 400.0
PLATFORM_SPACING_MEDIAN_M_MAX = 150.0


def nearest_neighbour_m(lon, lat, crs_projected, crs_geographic="EPSG:4326"):
    """Distance from each point to its closest neighbour, in metres.

    Projected, never computed in degrees - this project's first invariant.
    """
    import geopandas as gpd
    pts = gpd.GeoSeries(gpd.points_from_xy(lon, lat),
                        crs=crs_geographic).to_crs(crs_projected)
    pts = pts.reset_index(drop=True)
    if len(pts) < 2:
        return np.array([np.inf] * len(pts))
    return np.array([pts.drop(index=i).distance(pts.iloc[i]).min()
                     for i in range(len(pts))])


def boardable_stop_ids(stop_times, *, pickup="pickup_type",
                       drop_off="drop_off_type", boardable=("0", "2", "3")):
    """Stop ids where at least one stop_time allows boarding or alighting.

    GTFS uses 0/blank for "regularly scheduled" and 1 for "not available". A
    stop where BOTH are 1 on EVERY stop_time is infrastructure - Edmonton's two
    garage access points and its Health Sciences tail track, 1,947/1,947/1,430
    stop_times apiece and not one boardable.

    2 ("phone the agency") and 3 ("coordinate with the driver") are boardable
    too: a REQUEST STOP, which a reader can use. Until 2026-09-30 only 0 counted,
    and KORDIS JMK, which codes every Brno request stop 3/3, lost 25 of Brno's
    149 tram stations to it - with nothing to flag a station that is simply
    absent. The default now follows the GTFS spec (owner, 2026-09-30). A scan
    of the ten built cities that call this found 2/3 only on lines their maps
    do not draw (Prague's buses, trams and regional rail; the Dutch buses and
    international trains; Paris's demand-responsive buses). Eight of them
    drift-checked at zero drift; Oslo's and Bergen's feeds have no stop the old
    rule dropped, so the set is identical (docs/map_inconsistencies.md, theme
    13). Pass `boardable=("0",)` only to reproduce the old behaviour.
    """
    if pickup not in stop_times.columns or drop_off not in stop_times.columns:
        return None      # the feed does not say; caller must not infer
    ok = (stop_times[pickup].fillna("0").astype(str).isin(boardable)
          | stop_times[drop_off].fillna("0").astype(str).isin(boardable))
    return set(stop_times.loc[ok, "stop_id"])


def projected_xy(names, lon, lat, crs_projected, crs_geographic="EPSG:4326"):
    """{name: (x, y)} in metres, for `thin()`."""
    import geopandas as gpd
    pts = gpd.GeoSeries(gpd.points_from_xy(lon, lat),
                        crs=crs_geographic).to_crs(crs_projected)
    return {n: (p.x, p.y) for n, p in zip(names, pts)}


def thin(seqs, xy, *, spacing_m, keep_always=(), interchange=()):
    """The sub-transit-line thinning filter (docs/sub_transit_line_filters.md),
    San Francisco's rule: along each ordered stop-name sequence, keep both
    ends, every name in `keep_always` or `interchange`, and the first stop at
    or past `spacing_m` of track since the last kept one; cut the rest.

    Distance is summed stop to stop over `xy` ({name: (x, y)}, projected
    metres - never degrees). Which sequences to thin is the CITY's call:
    thinning both directions of a line and keeping the union barely thins
    (Rome: 4 of 16 cut, against 9), so each city passes only as many as cover
    the line. So is the reason's wording, which must keep the word "spacing"
    for app/station_scope.py.

    Returns (kept, cuts): the kept names, and one dict per cut not kept by
    another sequence in this call - {station, nearest_kept, metres_since_kept}
    - in sequence order. A caller thinning line by line still filters the
    cuts against every line's kept set.
    """
    kept, cuts = set(), []
    for seq in seqs:
        if not seq:
            continue
        mark = [n in keep_always or n in interchange for n in seq]
        mark[0] = mark[-1] = True
        since, last = 0.0, seq[0]
        for i in range(1, len(seq)):
            (x0, y0), (x1, y1) = xy[seq[i - 1]], xy[seq[i]]
            since += math.hypot(x1 - x0, y1 - y0)
            if mark[i]:
                since, last = 0.0, seq[i]
            elif since >= spacing_m:
                mark[i], since, last = True, 0.0, seq[i]
            else:
                cuts.append({"station": seq[i], "nearest_kept": last,
                             "metres_since_kept": since})
        kept |= {n for n, m in zip(seq, mark) if m}
    return kept, [c for c in cuts if c["station"] not in kept]


def verify_stations(*, city, platforms, stations, crs_projected,
                    expected_per_line=None, actual_per_line=None,
                    non_revenue=0, spacing_min=STATION_SPACING_MEDIAN_M_MIN,
                    platform_max=PLATFORM_SPACING_MEDIAN_M_MAX,
                    lat="latitude", lon="longitude"):
    """Run all three gates over one city's collapsed station set.

    `platforms` and `stations` are DataFrames with lat/lon columns. Prints the
    measurements, RAISES when the collapsed set is still platform-spaced, and
    returns a dict of what it measured so a caller can record it.

    `expected_per_line` / `actual_per_line`: {line name: count}, the operator's
    published figures against the feed's. This is gate 3, and it is optional
    only because a handful of agencies publish nothing usable - pass it
    whenever it exists, because it is the one check that can see an error every
    internal check agrees with.
    """
    raw_nn = nearest_neighbour_m(platforms[lon], platforms[lat], crs_projected)
    st_nn = nearest_neighbour_m(stations[lon], stations[lat], crs_projected)
    raw_med, st_med = float(np.median(raw_nn)), float(np.median(st_nn))

    print(f"  station check ({city}):")
    print(f"    {len(platforms):>4} platforms : median {raw_med:>6.0f} m  "
          f"min {raw_nn.min():>5.0f}")
    print(f"    {len(stations):>4} stations  : median {st_med:>6.0f} m  "
          f"min {st_nn.min():>5.0f}")
    if non_revenue:
        print(f"    {non_revenue} non-revenue stop(s) dropped - a trip stops "
              f"there but no passenger can board")

    if st_med < spacing_min:
        raise ValueError(
            f"{city}: the collapsed set has a {st_med:.0f} m median "
            f"nearest-neighbour distance, under {spacing_min:.0f} m - **these "
            f"are still platforms, not stations.** This is what went wrong in "
            f"Toronto (234 reported as stations, twice) and Calgary (83, whose "
            f"duplicate-NAME check passed because direction prefixes make "
            f"every name unique). Fix the collapse, not this threshold: check "
            f"for a direction prefix, a platform or destination suffix, more "
            f"than one naming convention in the same feed, and a `parent_"
            f"station` column you may not be using."
        )
    if raw_med > platform_max and len(platforms) > len(stations):
        print(f"    NOTE: uncollapsed median {raw_med:.0f} m is wide for "
              f"platforms - confirm the right stops were selected.")

    # THE MEDIAN CANNOT SEE A HANDFUL OF UNCOLLAPSED NAMES, and a handful is
    # the usual number. Barcelona passed gate 1 at a 520 m median while two of
    # its busiest interchanges sat in the set TWICE - FGC writes
    # "Barcelona-Placa Catalunya" where TMB writes "Catalunya", 178 m apart,
    # and the same for Espanya at 198 m. Two names out of 114 move a median not
    # at all. It was the nearest-neighbour MINIMUM that showed it.
    #
    # Printed rather than raised, because a genuinely close pair does exist -
    # Barcelona's own Sant Gervasi and Placa Molina are two real FGC stations
    # 40 m apart, and L11's Casa de l'Aigua sits 230 m from Trinitat Nova. So
    # this cannot be a threshold; it is a prompt to go and look.
    close = int((st_nn < spacing_min / 2).sum())
    if close:
        print(f"    NOTE: {close} station(s) within {spacing_min / 2:.0f} m of "
              f"another (minimum {st_nn.min():.0f} m). Some cities really do "
              f"have close pairs - but this is also what ONE STATION UNDER TWO "
              f"NAMES looks like, and the median will not show it. Check the "
              f"closest pairs by name before accepting the collapse.")

    mismatched = {}
    if expected_per_line and actual_per_line:
        print("    against the operator's own published counts:")
        for line, want in expected_per_line.items():
            got = actual_per_line.get(line)
            mark = "" if got == want else "   MISMATCH"
            print(f"      {line:<28} feed {str(got):>4}  operator {want:>4}{mark}")
            if got != want:
                mismatched[line] = (got, want)
        if mismatched:
            print(f"    {len(mismatched)} line(s) disagree with the operator. "
                  f"This is the gate that catches what the others cannot: "
                  f"Toronto's 118 and 77 were internally consistent and agreed "
                  f"with nothing published.")
    else:
        print("    NOTE: no operator counts supplied - gate 3 not run. It is "
              "the only check outside the data, and the one that caught "
              "Toronto. Pass expected_per_line wherever the agency publishes "
              "station counts.")

    return {"platforms": len(platforms), "stations": len(stations),
            "platform_median_m": round(raw_med, 1),
            "station_median_m": round(st_med, 1),
            "non_revenue": non_revenue,
            "per_line_mismatches": mismatched}
