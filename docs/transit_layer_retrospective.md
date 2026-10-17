# GTBA | The transit layer - retrospective (2026-10-16, partial)

Written 2026-10-16 from the record; committed 2026-10-17 on the owner's word.

This covers how each of the 237 maps chose, sourced and drew its rail
network, from the first three US cities (2026-09-18) to the close-out to
maintenance (2026-10-16). It is partial: written from the record as it
stands, with no new measurement beyond counting committed files. It builds
on `docs/tram_kit_retrospective.md` and does not repeat it. The detail behind
each figure is in `DECISIONS.md` and `docs/decisions/<Sunday>.md`, under the
entry named beside it. The standing rules are in `CLAUDE.md`, the history of
each at `docs/rule_history.md` (#line-identity, #rail-shape, #osm-rail).

## The short answer

**The transit layer ended as a set of shared rules that every map passes
through, but most of them were written after a city got it wrong.** Labels,
thinning, the station-scope rules, gate 3 and the line registry each began
as one city's fix. Each became a rule only when a second city met the same
case. The rules that held best are the ones turned into a check that raises.
The ones that stayed prose, in a skill or a doc, drifted or were skipped.

Three results stand out:

- **Station counts were the most error-prone number, and gate 3 is what
  settled them.** The 25-city back-fill of 2026-10-01 found 10 matches, 8
  reconciled and 7 mismatches needing an owner call (DECISIONS 2026-10-01,
  "Gate 3 back-filled in 25 cities").
- **One color per line, site-wide, came late and cost a large recolor.**
  The 2026-10-07 registry made 48 lines one color on 34 maps (DECISIONS
  2026-10-07, "One colour per line on every map").
- **Trams went from excluded to 59 tram-mode maps in about three weeks.**
  `app/cities.py` (read 2026-10-16) tags 152 maps metro, 26 light rail and
  59 tram.

The layer leaves dated work behind. Eleven of the twelve rows in PLAN's
"Dated re-checks" table are rail events (`PLAN.md`, 2026-10-16).

## How the rules formed, and why

### Labels and legends: one city's hand-tuning became a shared layout

**Every drawn line gets a permanent on-map label and a legend row because
hand-placed labels could not be reused.** On 2026-09-18 the per-line degree
offsets of the first three cities were replaced by an automatic tail-end
label (DECISIONS 2026-09-18, "Line labels at tail ends"). `render_heatmap()`
now draws a label and a legend row for every line passed to it. A rule of
2026-10-08 added that no two lines may share an on-map label
(`pipeline/map_common.py`, the "lines share an on-map label" raise).

### GTFS first, OpenStreetMap on a recorded ground

**The order is agency GIS layers, then current agency GTFS, then OSM, and
the ground for OSM is written in the city's config.** The first fourteen
cities read GTFS (`osm-rail` skill). Mexico City needed OSM because every
agency host timed out; Guadalajara because its feed declared itself expired
in 2023 (`osm-rail`, "When OSM is justified"). Madrid then showed the third
source: CRTM's feature services held 243 stations where the expired GTFS
undercounted (same skill, the Madrid section).

**The skill exists for a meta-lesson, not a technique.** Mexico City's config
warned in capitals never to match on a network label. One city later,
Guadalajara's first query did exactly that and lost Línea 4's 8 stops
(`docs/rule_history.md` #osm-rail). The owner's rule since: put a lesson
where the next city must pass through it, a raising check first, then a
skill. I'd argue this is the single most reusable finding of the layer.

### Rail shape and the sub-transit-line filters

**A map keeps every station unless the network has a central corridor with
dense surface offshoots.** San Francisco's Muni Metro set the case on
2026-09-18: 74% of surface stops sat more than 0.6 mi from a subway station
(`docs/sub_transit_line_filters.md`). Keeping all 147 stops saturated the
rings; keeping only the subway dropped whole districts. So surface stops are
thinned to about one per half mile, measured along the line, with central
stations, termini and interchanges kept.

**The filter was written five times before it was shared.** One `thin()` in
`pipeline/stations.py` replaced the copies for Rome, Amsterdam and Rotterdam
on 2026-09-27 (DECISIONS 2026-09-27, "One shared thin()"). The remaining
variants moved onto it on 2026-10-04 with zero drift (DECISIONS 2026-10-04,
"San Diego's swap-meet stalls out"). On 2026-09-29 the owner added that a
thinned line must be named where a reader can find it, and
`check_scope_disclosure.py` property F decides it (DECISIONS 2026-09-29,
"Thinned lines must be named").

### The 15-minute test and the commuter-rail exception

**Commuter rail is out unless, inside the city, it runs like rapid transit.**
The rule began as "excluded everywhere." Dublin's DART and then
Copenhagen's S-tog broke it, and on 2026-09-24 it was restated as the test it
was (DECISIONS 2026-09-24, "Commuter rail is excluded everywhere retired").
The test reads spacing and frequency inside the city; Brazil added coverage,
the share of a line's stations with no drawn station nearby
(`docs/commuter_rail_list.md`, "The pattern").

**Japan is the large exception, decided once.** The owner ruled on
2026-09-24 that Japanese maps draw JR and private commuter lines. On
2026-10-06 the 15-minute floor was lifted for them entirely, with stretches
of about 11 trains a day or fewer drawn and named (DECISIONS 2026-10-06,
"Japan's lines carry no frequency floor").

**For light rail the 15-minute test is a gate only on converted railway.**
On purpose-built track a slower timetable is disclosed, not disqualifying
(the Buffalo rule, DECISIONS 2026-09-29, "Band T audited"). The owner
narrowed it further on 2026-09-30: a floor drops only an outlier route, never
a network whose norm is longer waits (DECISIONS 2026-09-30, "Daugavpils draws
its whole network"). Two maps now list stops as too infrequent: Aarhus 19 and
Shimonoseki 7 (`outputs/*/excluded_stations.csv`, rows containing
"15-minute", counted 2026-10-16).

### Trams: from excluded to their own maps

**Trams were never excluded for being trams, and the record had said they
were.** On 2026-09-23 a session claimed Zurich had no drawable network,
reading a brief's prose. The code showed seven built cities already drawing
`route_type 0` (DECISIONS 2026-09-23, "CORRECTION: a tram-only city is NOT
unbuildable"). The owner ruled "count trams" on 2026-09-27 and approved
trams-only maps on 2026-09-29, with no thinning and rings sized by spacing
(DECISIONS 2026-09-29, "Yes to trams-only maps" and "Tram audit Phases 3-4").

**The light-rail test split Band T in two before any tram was built.** Ten
cities passed a three-part test of track, frequency and spacing, read against
San Diego, Calgary and Edmonton, and left for Bands A and C (DECISIONS
2026-09-29, "Band T audited"). Only street trams waited on the trams call.

### The tram rescope of built cities

**Built cities that left trams off were rescoped in two rounds, 16 days
apart.** The light batch and Paris (Montréal's REM, Rome's tram 8, Madrid's
ML1, Paris T3a and T3b, San Francisco's F line) landed at be2e3713 on
2026-09-27. Toronto, Milan, Prague and Mexico City's cable cars landed in the
rollout push of 2026-10-13 (9736df8b, pushed with 3e16745d).

**The second round added an overlap test before any build.** Barcelona's 28
tram stops all sat inside the metro's outer ring, so ringing them moved no
storefront outside the rings; the owner left them out (DECISIONS 2026-10-13,
"Barcelona's trams stay out"). Toronto's trams brought 3,611 storefronts
inside a ring, Milan's 4,563 and Prague's 3,979 (DECISIONS 2026-10-13,
"Toronto, Milan and Prague pass the overlap test"). The label rule was per
route; Prague alone failed on phones and was drawn as ten route groups
(DECISIONS 2026-10-13, "Prague's trams are drawn in ten groups").

### Closures and openings

**A station closed for works is drawn as the timetable runs, in every
city.** Prague drew Flora while closed and Berlin left the U6 Tegel branch
off; the only difference was the expected length of the closure (DECISIONS
2026-09-29, "Stations closed for works"). The feed decides now, because
operators' reopening dates slip. Six maps list closed-for-works stations:
Toronto 56, Berlin 5, and Antwerp, Philadelphia, Prague and Sacramento one
each (`excluded_stations.csv`, counted 2026-10-16).

**A station the operator serves and OSM lacks is added by id, and the step
stops once OSM catches up.** Taoyuan set the pattern (`osm-rail`, "Three
more, from Taiwan"). Sacramento's Dos Rios, opened 2026-09-28, was placed at
Wikidata's coordinate, Q107175168 (`pipeline/sacramento/config.py`,
`ADDED_STATIONS`). OSM mapped it by 2026-10-16 (commit df61e14d). Whether
OSM's Blue Line relation carries it yet, which is what retires the entry, is
UNVERIFIED.

### One color and one name per physical line

**The registry answers a reader's problem, not a renderer's.** Each Japanese
city had chosen its own colors, so the JR Kobe Line was five colors on six
maps (`pipeline/line_registry.py`, header). The owner made it a hard line on
2026-10-07. Identity is operator plus public line, never a display name:
"Tram 1" is fifteen different lines (DECISIONS 2026-10-07, "One colour per
line on every map"). The same day a neighbor rule followed: different lines
within 2 km on two maps differ by at least CIE76 10, with three recorded
exceptions (`line_registry.NEIGHBOUR_EXCEPTIONS`).

**The CIE76 20 pin floor came from the pin colors, not the lines.** Adding
olive and violet pins on 2026-10-07 put 32 legend rows within 20 of a pin, and
27 line colors moved on 21 maps (DECISIONS 2026-10-07, "Lines within 20 of
the olive and violet pins recoloured"). The registry started at 83 shared
lines and holds 106 entries on 2026-10-16 (counted in
`pipeline/line_registry.py`).

## What each rule cost and caught

| Rule | What it cost | What it caught | Source |
|---|---|---|---|
| Automatic labels | one layout pass, later phone-width runs | labels overlapping at Muni's south end; Rennes' "Métro b" clipped on phones | DECISIONS 2026-09-18; `check_map_labels.js` header |
| OSM on a recorded ground | a skill and three raising checks | Guadalajara's lost Línea 4; Mexico City's 9 missing stations | `osm-rail` |
| Thinning, named | 896 stops cut on 13 pages | ring saturation on branching networks | `excluded_stations.csv`, 2026-10-16 |
| Closed for works | one rule, a stop-when-served guard per city | Berlin and Prague treating one case two ways | DECISIONS 2026-09-29 |
| Gate 3 | six agents for the back-fill; a config block per city | New Orleans's undrawn Canal stretch; Philadelphia's G branch | DECISIONS 2026-10-01 (both entries) |
| Line registry | 48 lines recolored on 34 maps; 73 configs rewired | a line changing color between neighboring maps | DECISIONS 2026-10-07 |
| Pin floor 20 | 27 line colors moved on 21 maps | lines too close to the new pins | DECISIONS 2026-10-07 |
| Overlap test (rescope) | one read-only measure per city | Barcelona, where trams added no reach | DECISIONS 2026-10-13 |

**The rescope's cost was estimated once and not re-measured here.** The
estimate put the whole rescope at 55 to 85% of one five-hour window
(`docs/tram_rescope_estimate.md`). Its own note says it rests on one session.
Whether the actual cost matched is UNVERIFIED.

## Where the layer was wrong, and how it was found

**Most errors were found by a measurement that did not trust the earlier
number, not by review.** The cases below are the clearest:

- **Platforms counted as stations.** Toronto's "234 stations" were 234
  platforms, 118 stations; Calgary's 83 were 45 (`add-city`, Step 4). The
  nearest-neighbor median found Calgary's: 17 m, impossible for rail.
- **A line lost to a tag filter.** Guadalajara's first query omitted Línea 4,
  which a spacing gate and a second read caught (`osm-rail`).
- **Stations lost to a whitelist.** Mexico City shipped missing nine Metro
  stations, four of them termini; a probe of the State of México found it on
  2026-10-04 (`osm-rail`, "Mexico City's whitelist").
- **A line lost to a stale national dataset.** Osaka's map uses N02-24 and
  misses the Yumeshima extension, open since January 2025
  (`docs/recheck_calendar.md`, action list). It is still open in PLAN.
- **OSM's services behind the operator.** Manchester's relations carried 11
  refs from before TfGM's September change (`osm-rail`, the Manchester
  section). The owner allowed the operator's lines routed over OSM's track.
- **A color nobody could see.** Calgary's Blue Line sat 3.3 from Retail blue
  for weeks; the render now raises below 10 (`pipeline/linecolour.py`,
  `check_line_colours`; commit a47175f5, 2026-09-21).
- **A circular gate 3.** Kansas City compared OSM with a brief count taken
  from OSM (DECISIONS 2026-09-30, "Gate 3 made required in tram-city").
- **Done work listed as open.** On 2026-10-13 Cleanup gave the owner a
  rescope scope that included five cities already landed on 2026-09-27
  (DECISIONS 2026-10-13, "Correction: five tram rescopes were already built").

**Some docs about the layer have drifted, and nothing checks them:**
- `docs/sub_transit_line_filters.md` lists eight thinning cities. The
  committed files show 13 pages, Milan, Prague, Toronto and both Brussels
  pages among the additions.
- `docs/commuter_rail_list.md` is a 2026-09-24 snapshot that says six built
  cities draw commuter rail. Its own table now bolds seven, Liverpool
  (Regional) added on 2026-10-04.

## What the checks prove, and what they do not

**They prove internal consistency well and the outside world only where an
independent source exists.**

What they prove:

- `check_line_identity.py` (in `check_all.py`) proves a registered line has
  one color in every config, and different lines within 2 km differ by 10.
- `check_line_colours()` raises when a line is within CIE76 10 of a pin the
  map draws, or of another line on it.
- `check_scope_disclosure.py` proves each excluded station has a readable
  reason and each thinned line is named.
- Gate 3, where configured, proves the station count per line equals the
  operator's own published count.
- The stop-when-served guards prove a closed station or an added station
  cannot silently stay in its interim state once the feed or OSM changes.

What they do not:

- **No script enforces the CIE76 20 pin floor that I could find.** The
  render raises at 10; 20 was applied in the 2026-10-07 recolor and in the
  registry's color choices. A new line at 15 from a pin would pass the gate.
  UNVERIFIED that no other mechanism holds it.
- **The rail-shape decision has no check.** Whether a network needs thinning
  is a judgment at Step 4; nothing fails a city that should have thinned.
- **The label checks run in a browser, not in the gate.**
  `check_map_labels.js` finds overlaps and missing legend rows, but only when
  someone runs it at phone and desktop widths.
- **Gate 3 checks counts, not service.** A station can match the count and
  still be on a route the operator no longer runs, as New Orleans's brief
  showed (`docs/tram_kit_retrospective.md`).
- **The neighbor rule sees only maps within 2 km.** Two maps far apart can
  draw different lines alike, by design.
- **I did not measure the split between GTFS and OSM rail across the 237
  maps.** A grep of configs was not reliable enough to cite. UNVERIFIED.

## Lessons

1. **Turn a city's lesson into a raising check before the next city.** It is
   the `osm-rail` meta-rule, and the record bears it out. Guadalajara's lost
   line, Calgary's invisible color and the platform counts each recurred
   until shared code refused them.
2. **A rule that two built cities answer differently is a rule waiting to be
   written.** Closed-for-works came from Berlin against Prague; the registry
   from one line in five colors. Look for those pairs on purpose rather than
   waiting for a third city.
3. **Measure the reach before drawing a line.** The overlap test settled
   Barcelona in one read. It would have saved the same-day reversal from
   "two drawn lines" to "leave it out" if it had come first.
4. **Read the log before restating parked work.** The 2026-10-13 scope error
   cost an owner decision on done work. A parked item needs its commit
   checked, not only its note.
5. **Keep counted docs counted.** The thinning list and the commuter-rail
   snapshot both hold hand-kept counts that have drifted. Either generate
   them from `excluded_stations.csv` and `app/cities.py`, or date them as
   snapshots in their first line.
6. **The transit layer is not finished when a city is.** Feeds expire, works
   end and stations open. Every interim state should carry a guard that stops
   the build, and a dated row in `docs/recheck_calendar.md`. Toronto, Milan
   and Prague show the pattern working.

**What this retrospective does not show.** It reads the record, not the
maps: no map was opened and no step was re-run. It counts committed files on
one date, 2026-10-16, so a map changed since then is not reflected. It does
not show whether the rules made the maps more accurate for a reader; that
would need an outside comparison this project never ran. And it does not
weigh what each rule cost in session time, since per-task usage was never
recorded.
