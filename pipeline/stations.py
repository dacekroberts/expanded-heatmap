"""Station-count verification, shared: it was wrong in four of five Canadian
cities, in five separate copies of per-city code, differently each time.

WHY THIS IS A MODULE AND THE COLLAPSE ITSELF IS NOT
---------------------------------------------------
The collapse stays per city. In the five Canadian builds every feed collapsed
differently, and the differences are real rather than incidental.

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

**What was missing every time was not the collapse but the check.** So this
module owns the checks, and every city's `step1` must call
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
     a passenger can use (first needed in Edmonton).
  3. THE OPERATOR'S OWN COUNT - the one check that is outside the data. Toronto
     at 110 agrees with the TTC's published per-line figures; its earlier 118
     and 77 agreed with nothing, and no amount of internal consistency would
     have said so.

Gate 3 is the one to reach for first when a number feels wrong. The other two
are automatic; that one requires reading what the agency publishes, which is
why it kept being skipped.
"""

import math
import re
import unicodedata

import numpy as np

# Below this, points are platforms rather than stations. Measured medians:
# Calgary's uncollapsed 17 m and Toronto's 69 m against collapsed 632-713 m,
# and San Francisco's genuinely street-running 134 m, which WAS thinned.
STATION_SPACING_MEDIAN_M_MIN = 400.0
PLATFORM_SPACING_MEDIAN_M_MAX = 150.0


def nearest_neighbour_m(lon, lat, crs_projected, crs_geographic="EPSG:4326"):
    """Return the distance from each point to its closest neighbour, in metres.

    Projected, never computed in degrees: this project's first invariant.
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
    """Return the stop ids where at least one stop_time allows boarding or
    alighting.

    GTFS uses 0/blank for "regularly scheduled" and 1 for "not available". A
    stop where BOTH are 1 on EVERY stop_time is infrastructure: Edmonton's two
    garage access points and its Health Sciences tail track, 1,947/1,947/1,430
    stop_times apiece and not one boardable.

    2 ("phone the agency") and 3 ("coordinate with the driver") are boardable
    too: a REQUEST STOP, which a reader can use. Until 2026-09-30 only 0 counted,
    and KORDIS JMK, which codes every Brno request stop 3/3, lost 25 of Brno's
    149 tram stations to it, with nothing to flag a station that is simply
    absent. The default now follows the GTFS spec (owner, 2026-09-30). In the
    ten built cities that called this then, 2/3 appear only on lines their maps
    do not draw (Prague's buses, trams and regional rail; the Dutch buses and
    international trains; Paris's demand-responsive buses), and none of their
    station sets changed (docs/map_inconsistencies.md, theme 13). Pass
    `boardable=("0",)` only to reproduce the old behaviour.
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


def check_operator_counts(expected_per_line, actual_per_line):
    """Gate 3 on its own: the operator's published per-line station counts
    against the build's. Prints the comparison and returns {line: (build,
    operator)} for each line that disagrees. `verify_stations` calls it; a step
    1 that predates `verify_stations` (the early US cities) calls it directly
    with its own per-line counts. It never raises: a caller that must stop on a
    mismatch (a tram step 1) checks the return value."""
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
    return mismatched


# --- One station under two names --------------------------------------------
#
# OSM names an interchange's nodes per line ("Consulado" and "Consulado L4",
# 330 m apart; "Candelaria L1" and "Candelaria L4", 180 m), and a register
# spells one station two ways ("Avila Camacho" and "Ávila Camacho", 98 m). A
# collapse by the raw name keeps both. Mexico City shipped two such pairs and
# Guadalajara one before this gate existed (2026-10-04,
# DECISIONS.md).

_LINE_DESIGNATOR = re.compile(
    r"\s*\((?:l[ií]nea|line|l)\s*[0-9A-Za-z]{1,3}\)$"   # "Tacubaya (Línea 7)"
    r"|\s+L[0-9]{1,2}$",                                # "Consulado L4"
    re.IGNORECASE,
)


def strip_line_designator(name):
    """The name without a trailing per-line tag: "Consulado L4" -> "Consulado",
    "Tacubaya (Línea 7)" -> "Tacubaya". Anything else is returned unchanged."""
    return _LINE_DESIGNATOR.sub("", str(name)).strip()


def station_name_key(name):
    """A collapse key under which spellings of one station agree: the line
    designator dropped, accents folded, case folded, a leading "Metro " and the
    separators "/" and "-" ignored. Non-Latin letters are kept (only combining
    marks are dropped), so a Han or Hangul name never folds to an empty key."""
    s = strip_line_designator(name)
    s = "".join(c for c in unicodedata.normalize("NFKD", s)
                if not unicodedata.combining(c)).casefold()
    s = re.sub(r"^metro\s+", "", s)
    s = re.sub(r"[/\-–]", " ", s)
    return " ".join(s.split())


# Same-key pairs a built city still carries, each a DATED DEFECT rather than a
# pass (check_provenance's KNOWN_GAPS pattern): verify_stations prints them
# instead of raising, and raises once the pair is gone so a fixed entry cannot
# linger. {city: {frozenset of names: note}}. Empty since Guadalajara's Ávila
# Camacho was collapsed (2026-10-04).
KNOWN_SAME_NAME = {}

NAME_COLUMNS = ("station", "name", "stop_name", "station_name")


def same_name_pairs(stations, crs_projected, *, within_m, name_col,
                    lat="latitude", lon="longitude"):
    """[(name_a, name_b, metres)] for every two rows of `stations` whose
    `station_name_key` agrees and which lie within `within_m` of each other."""
    keys = stations[name_col].map(station_name_key)
    dup = stations[keys.duplicated(keep=False) & (keys != "")]
    if dup.empty:
        return []
    xy = projected_xy(range(len(dup)), dup[lon], dup[lat], crs_projected)
    names, dkeys = list(dup[name_col]), list(keys[dup.index])
    pairs = []
    for i in range(len(dup)):
        for j in range(i + 1, len(dup)):
            if dkeys[i] != dkeys[j]:
                continue
            d = math.dist(xy[i], xy[j])
            if d < within_m:
                pairs.append((names[i], names[j], round(d)))
    return pairs


# --- Route-relation coverage, for a station set selected by tag --------------
#
# THE GAP A TAG WHITELIST LEAVES. Mexico City's step 1 kept `railway=station`
# nodes only, and nine Metro stations exist in OSM only as `railway=stop`
# positions on their line's route relation (Observatorio, Indios Verdes,
# Potrero, Juárez, Mixcoac, Tepalcates, Buenavista, Cuatro Caminos; Talismán's
# station node carries no mode tag). Four termini among them, and no internal
# gate saw it: spacing, the whitelist and cross-direction agreement all passed
# (2026-10-04). Any step 1 that selects stations by node tag passes its
# collapsed set, in scope or not, through `check_route_stops_covered`.

ROUTE_STOP_TAGS = (("public_transport", "stop_position"), ("railway", "stop"),
                   ("railway", "station"), ("railway", "halt"),
                   ("railway", "tram_stop"))

# An unnamed stop member counts as covered by a station this close. Mexico
# City's ten untagged members sit 4-110 m from their station (measured
# 2026-10-04); a missing station sits 470 m or more from the nearest kept one
# (Juárez to Hidalgo), so the gate has room on both sides.
UNNAMED_STOP_WITHIN_M = 250.0


def route_stop_members(relations, nodes_by_id, *, refs):
    """One row per (line, stop node) of the route relations whose `ref` is in
    `refs`: line, node, name ("" when the node is untagged or unnamed),
    latitude, longitude, network (the RELATION's, since node-level network
    tags are absent or wrong in OSM; see the osm-rail skill).

    A node member counts when it carries a stop tag (ROUTE_STOP_TAGS), or when
    the cache has no tags for it at all, which `check_route_stops_covered`
    then places by distance. Member roles are not trusted: Mexico City's
    Línea 9 lists five stop positions under the role "" or "stops"."""
    import pandas as pd
    rows = []
    for rel in relations:
        ref = rel.get("tags", {}).get("ref")
        if ref not in refs:
            continue
        for m in rel.get("members", []):
            if m.get("type") != "node" or "platform" in (m.get("role") or ""):
                continue
            node = nodes_by_id.get(m["ref"])
            tags = (node or {}).get("tags") or {}
            if tags and not any(tags.get(k) == v for k, v in ROUTE_STOP_TAGS):
                continue
            lat_ = m.get("lat", node and node.get("lat"))
            lon_ = m.get("lon", node and node.get("lon"))
            if lat_ is None or lon_ is None:
                raise ValueError(f"route {ref}: node member {m['ref']} has no "
                                 f"coordinates in the relation or the node cache")
            rows.append({"line": ref, "node": m["ref"],
                         "name": (tags.get("name") or "").strip(),
                         "latitude": lat_, "longitude": lon_,
                         "network": rel["tags"].get("network", "")})
    return pd.DataFrame(rows, columns=["line", "node", "name", "latitude",
                                       "longitude", "network"])


def check_route_stops_covered(*, city, route_stops, stations, crs_projected,
                              name_col="station",
                              unnamed_within_m=UNNAMED_STOP_WITHIN_M,
                              lat="latitude", lon="longitude"):
    """RAISES unless every stop member of a drawn route relation has a station:
    a named stop, one whose `station_name_key` is in `stations`; an unnamed
    one, a station within `unnamed_within_m`. `stations` is the WHOLE
    collapsed set, out-of-scope stations included, so a stop cut by the
    boundary still counts as accounted for.

    Returns the station each route stop belongs to, aligned with
    `route_stops`, so a caller can count stations per line."""
    st_names = list(stations[name_col])
    by_key = {station_name_key(n): n for n in st_names}
    named = route_stops[route_stops["name"] != ""]
    missing = named[~named["name"].map(station_name_key).isin(by_key)]
    unnamed = route_stops[route_stops["name"] == ""]
    station_of = route_stops["name"].map(
        lambda n: by_key.get(station_name_key(n)) if n else None)
    far = []
    if len(unnamed):
        st_xy = projected_xy(range(len(stations)), stations[lon],
                             stations[lat], crs_projected)
        un_xy = projected_xy(range(len(unnamed)), unnamed["longitude"],
                             unnamed["latitude"], crs_projected)
        for i, (idx, r) in enumerate(unnamed.iterrows()):
            j, d = min(((j, math.dist(un_xy[i], p)) for j, p in st_xy.items()),
                       key=lambda jd: jd[1])
            station_of[idx] = st_names[j]
            if d > unnamed_within_m:
                far.append(f"line {r['line']}: node {r['node']} (unnamed), "
                           f"{d:,.0f} m from the nearest station")
    problems = [f"line {r['line']}: {r['name']!r} (node {r['node']})"
                for _, r in missing.drop_duplicates(["line", "name"]).iterrows()]
    problems += far
    print(f"  route coverage ({city}): {len(route_stops)} stop members of the "
          f"drawn relations, {len(named)} named, {len(unnamed)} unnamed; "
          f"{len(problems)} without a station")
    if problems:
        raise ValueError(
            f"{city}: {len(problems)} stop member(s) of a drawn route relation "
            f"have no station. A tag whitelist dropped them (Mexico City lost "
            f"nine Metro stations, four termini, to `railway=station` only), "
            f"or a name differs beyond station_name_key. Add the stop, or "
            f"correct the name; never drop the member:\n  "
            + "\n  ".join(problems))
    return station_of


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
    # its busiest interchanges sat in the set TWICE: FGC writes
    # "Barcelona-Placa Catalunya" where TMB writes "Catalunya", 178 m apart,
    # and the same for Espanya at 198 m. Two names out of 114 do not move a
    # median; the nearest-neighbour MINIMUM shows them.
    #
    # Printed rather than raised, because genuinely close pairs exist:
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

    # ONE STATION UNDER TWO SPELLINGS, which the NOTE above only prompts for.
    # Raised, because two spellings of one key this close are never two
    # stations: the close real pairs above (Sant Gervasi and Placa Molina)
    # have different keys. Den Haag's per-line stops ("Loosduinseweg (line 11)" and "(line
    # 12)") sit 496-575 m apart, past this distance.
    name_col = next((c for c in NAME_COLUMNS if c in stations.columns), None)
    if name_col is None:
        print(f"    NOTE: no name column ({', '.join(NAME_COLUMNS)}) - the "
              f"same-name gate did not run.")
    else:
        pairs = same_name_pairs(stations, crs_projected, within_m=spacing_min,
                                name_col=name_col, lat=lat, lon=lon)
        # IDENTICAL names are a city's own choice and only noted: New York
        # keeps a "Canal St" per complex part and Amsterdam two Wibautstraat
        # rows, on purpose (scan of every stations.csv, 2026-10-04).
        same = [p for p in pairs if p[0] == p[1]]
        if same:
            print(f"    NOTE: {len(same)} pair(s) of identically named "
                  f"stations within {spacing_min:.0f} m (e.g. {same[0][0]!r}, "
                  f"{same[0][2]} m) - deliberate only if the city says so.")
        pairs = [p for p in pairs if p[0] != p[1]]
        known = KNOWN_SAME_NAME.get(city, {})
        found = {frozenset((a, b)) for a, b, _ in pairs}
        stale = [sorted(k) for k in known if k not in found]
        if stale:
            raise ValueError(
                f"{city}: KNOWN_SAME_NAME lists {stale}, no longer a pair in "
                f"the collapsed set. Remove the entry; a fixed defect stays "
                f"listed only by mistake.")
        new = [p for p in pairs if frozenset(p[:2]) not in known]
        for a, b, d in pairs:
            if frozenset((a, b)) in known:
                print(f"    KNOWN DEFECT: {a!r} and {b!r}, {d} m apart - "
                      f"{known[frozenset((a, b))]}")
        if new:
            raise ValueError(
                f"{city}: {len(new)} station(s) kept twice under two spellings, "
                f"within {spacing_min:.0f} m: "
                + "; ".join(f"{a!r} / {b!r} {d} m" for a, b, d in new)
                + ". Collapse on pipeline.stations.station_name_key, not the "
                  "raw name (Mexico City's Consulado and Candelaria).")

    mismatched = check_operator_counts(expected_per_line, actual_per_line)

    return {"platforms": len(platforms), "stations": len(stations),
            "platform_median_m": round(raw_med, 1),
            "station_median_m": round(st_med, 1),
            "non_revenue": non_revenue,
            "per_line_mismatches": mismatched}
