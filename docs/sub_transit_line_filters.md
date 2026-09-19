# Sub-transit-line filters

A station-selection pattern for **offshoot/surface-running lines**, not
for a system's central/main corridor. Built for San Francisco's Muni
Metro (2026-09-18) and written up here so it's reused deliberately on a
future city, not reinvented or - worse - applied somewhere it doesn't
fit.

## When this applies

San Diego's Trolley has sparse, evenly-spaced stations (roughly a
quarter- to half-mile apart) for its entire length - every station is
worth its own ring, so the default pattern is simply: take every station,
filter to city limits, done.

Muni Metro doesn't fit that shape. It runs underground/grade-separated
through a compact central spine (the Twin Peaks Tunnel corridor plus the
Chinatown Central Subway), then surfaces onto ordinary street track with
stops every 1-2 blocks for the rest of each line's length - out to Ocean
Beach, the Bayview/Visitacion Valley corridor, and the Ingleside/Ocean
Ave area. A real check (2026-09-18) found 74% of surface stops
are more than 0.6 miles - this project's own outermost ring - from the
nearest subway station, median 1+ mile. Two bad options followed from
that:

- **Keep every stop (147 for Muni Metro alone).** Rings overlap almost
  continuously along the surface segments, which defeats the point of a
  ring *gradient* - nearly everywhere reads as "within 0.1mi of a
  station." The map is also visually saturated with markers.
- **Keep only the subway/central stations (~12).** Misses the Sunset,
  Bayview/Visitacion Valley, and Ingleside/Ocean Ave districts entirely -
  not a thinner version of the full picture, a meaningfully smaller one.

**Use this pattern when a city's rail system has this same shape**: a
central corridor with sparse, meaningful stations, plus one or more
offshoot/branch/surface segments with much denser stop spacing than the
central corridor. Don't apply it to a system that's uniformly
sparse-stationed end to end (San Diego's Trolley) - the simpler "keep
everything, filter to city limits" pattern already fits those correctly,
and this pattern's extra machinery would be solving a problem that doesn't
exist there.

## The four filters, in order

Applied per line, to that line's own real, in-order stop sequence (from
one representative GTFS trip - see the reasoning in
`pipeline/san_diego/step1_stations.py` for why one direction is enough to
get a line's real path).

1. **Central-corridor stations are always kept, never thinned.** These
   are usually a system's real interchange points already - identify them
   however fits the city's own system shape (San Francisco's config.py
   uses a keyword list, `SUBWAY_STATION_KEYWORDS`, matching canonical
   station names against the underground/grade-separated segment).
2. **Each line's own two terminals are always kept** - "as far as the
   city boundary permits," i.e. the actual first/last stop in that line's
   real GTFS sequence within the covered service area.
3. **Remaining (surface/offshoot) stops are thinned to roughly one per
   a target spacing** (San Francisco used 0.5 miles -
   `STATION_SPACING_MILES` in that city's config.py), **measured along
   the line's real stop-to-stop path, not straight-line distance**,
   counting fresh from whichever stop was most recently kept by ANY
   filter (a terminal, a central-corridor station, or an interchange) -
   never from the line's start regardless of what's already been kept.
   This filter never runs before filters 1/2 have marked their keeps -
   it needs those reset points to measure from.
4. **Any stop shared by 2+ lines is force-kept**, even where filter 3's
   spacing alone would have dropped it - a real transfer point stays on
   the map regardless of how close it happens to sit to its neighbors.

## What this is not

Not a general-purpose station-thinning tool to apply everywhere for
visual tidiness. It exists specifically to keep a *branching* system's
distant districts on the map without drowning the whole map in
closely-spaced surface stops. A system without that branching/central-vs-
surface shape doesn't need it.

## Implementation notes (from San Francisco's build)

- **Canonicalize direction-suffix duplicates before running any of
  this.** GTFS records each direction of a station as a separately-named
  stop (`"Metro Church Station/Downtown"` vs `".../Outbound"`,
  `"Van Ness Station Outbound"` vs no suffix at all) - these need to
  collapse to one physical station first, or the selection logic reasons
  about platforms instead of stations. A regex catches the common
  suffix patterns; it will not catch every inconsistency (San Francisco's
  GTFS named the same physical Van Ness platform two genuinely different
  ways across different lines' own trips, with no shared suffix pattern
  to detect at all) - **run a real physical-distance check across the
  final selected list** (any two distinct names within ~100-200 feet are
  almost certainly the same physical station under inconsistent raw
  naming) and hand-curate the remainder into a `STATION_NAME_ALIASES`
  dict, the same way `GTFS_NAME_ALIASES` handles simpler cases elsewhere
  in this project. San Francisco's build needed 4 such hand-curated
  aliases after the regex pass.
- **Document every cut station**, not just the kept list. A thinning
  filter that takes 147 stops down to 49 stations (San Francisco's actual
  result) needs to be auditable - which station, which line, why,
  and what it ended up closest to instead. San Francisco's
  `step1_stations.py` writes this to `outputs/<city>/excluded_stations.csv`
  (committed, not a gitignored intermediate - it's a citable record of a
  real design decision, not scratch output).
