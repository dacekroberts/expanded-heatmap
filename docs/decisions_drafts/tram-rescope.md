# Decisions drafts: tram-rescope

Newest first. Cleanup folds these into `DECISIONS.md` at review time.

### 2026-10-13 - Tram rescope: Rome's trams parked as one decision after 2026-11-23; Barcelona drawn as two lines (owner)

- **Rome, the owner: "yes one rome decision sounds good as a parked
  item"**, to the recommendation below it: one decision on trams 2, 3, 5, 14
  and 19 after ATAC's network is back (due 2026-11-23), none drawn before.
  Rome's rail is final as it stands until then, so the rescope no longer
  holds Rome out of the search rollout; a later tram build rebuilds its
  index.
- **Barcelona, the owner, on the color call: "option sounds best, note the
  page shade add"**, to option 1: two drawn lines, "Trambaix (T1, T2, T3)"
  and "Trambesòs (T4, T5, T6)", one in TRAM's green and one in a shade of
  this project's, the page saying the shade is the project's. Rejected: one
  key over two disconnected pieces of track (this map split L9 and L10 for
  that reason); three keys, which needs two project shades.
- **The shade, measured, not yet approved:** TRAM's #007165 moved in HSL
  lightness only, the smallest 0.02 step that clears Delta-E 13 from it
  (Rome's and Oslo's rule): #00524a at -0.06, 13.3 from TRAM's green, 18.6
  from the Montjuïc funicular, 45.5 from the nearest pin (Personal
  services). The lighter side clears 13 only at +0.08 (#009a89) and sits
  22.0 from that pin.
- **Measured the same day, and it changes the case for drawing them: no
  tram stop inside Barcelona is beyond the metro's reach.** Of the 28
  stops, 0 are farther than the 966 m outer ring from a drawn metro or
  funicular station (median 302 m, farthest 807 m; 6 beyond 0.3 mi, 9
  within 0.1 mi). Rome's tram 8 had 15 of 16 beyond it. With rings on all
  28, the storefronts beyond 0.6 mi stay at 22 of 35,309; 2,341 storefronts
  (6.6%) change ring, all inward (0-0.1 mi 7,257 to 8,192; 0.3-0.6 mi 3,215
  to 2,093). Read from `data/barcelona/processed/` as it stood, not
  re-run. Stop spacing inside the city: Trambaix median 417 m, T4 527 m,
  T5 and T6 about 510 m. The estimate's reason ("reach districts beyond the
  metro") holds for the networks' outer ends, which are outside the city
  and off this map. Brought to the owner before any build.

### 2026-10-13 - Tram rescope: Rome's tram 3 not built on its own; Barcelona TRAM measured (branch)

- **Rome's tram 3 was offered as a go-ahead "if it's an overall small
  addition" (owner, 2026-10-13) and is NOT built: the session judged it not
  small overall, and brought it back.** Mechanically it is small: one
  relation pair fetched under a new file name, one more key beside tram 8,
  the same half-mile thinning. What makes it larger: tram 3 runs only
  Trastevere - Porta Maggiore today, with buses on Porta Maggiore - Valle
  Giulia; and ATAC's trams 2, 5, 14 and 19 return in phases with the whole
  network due by 2026-11-23 (`docs/recheck_calendar.md`, whose row already
  names drawing them as the owner's call). Drawing 3 alone now means a
  partial line redrawn in six weeks, and a map that shows one returned tram
  and not the four that follow. Recommended instead: one Rome tram decision
  after 2026-11-23, for all five. Not measured: tram 3's stop count, color
  and distance from the metro; no Rome query was run.
- **Barcelona TRAM, measured from OpenStreetMap** (one Overpass query,
  2026-10-13, overpass.kumi.systems, bbox `41.30,2.03,41.50,2.30`, cached
  as `data/barcelona/raw/osm_tram_routes_2026-10-13.json`; the metro cache
  is untouched): 12 route relations, two per line, networks `Trambaix` (T1,
  T2, T3) and `Trambesòs` (T4, T5, T6), operator TRAM. Distinct stop names
  inside the municipal boundary: T1, T2 and T3 the SAME 9 (Francesc Macià to
  Zona Universitària and Ernest Lluch); T4 10 (Verdaguer to El Maresme and
  Fòrum); T5 and T6 the SAME 10 (Ciutadella | Vila Olímpica to Besòs);
  Glòries is on T4 and on T5/T6, so 28 distinct stops. The count of
  2026-09-27 (9 to 10 each) stands.
- **Color:** all six carry `colour=#007165`. Against the 16 drawn lines the
  nearest is the Montjuïc funicular (#006847), Delta-E 13.9, over
  `pipeline/linecolour.py`'s floor of 10. Two tram keys in that one green
  would be Delta-E 0 from each other, which the check refuses. Whether TRAM
  itself publishes per-line colors was not checked.
- **Nothing built, no step run, no output changed.** The color rule and how
  many lines are drawn go to the owner.

### 2026-10-13 - Tram rescope: the light batch and Paris were already built; two docs corrected (branch)

- **The session's handoff named Montreal's REM as the first build. It is
  built, with the other four: all five landed on 2026-09-27.** Commits
  c8c1c53a (REM, 78 stations), eedeb329 (Rome tram 8, 94), 5f9106e5
  (Madrid ML1, 200), 821ca1a9 (Paris T3a and T3b, 280), f3e051d7 (San
  Francisco F Market & Wharves, 57), merged in be2e3713. Measured
  2026-10-13 on origin/master 1b5f4df8: `git log --since=2026-09-26
  --until=2026-09-29`, and each committed `outputs/<city>/heatmap.html`
  carries its line's label.
- **What that changes for place search** (sent to Cleanup the same day, the
  owner having approved the message): no index rebuild is owed for trams in
  Montreal, Paris or San Francisco. Paris's search area counts 280 stations.
  Montreal's counts 79 across five municipalities against 78 rows in
  `stations.csv`; the difference is not traced (lead: a station counted in
  two overlapping municipal polygons).
- **Corrected on this branch, at Cleanup's request:** a status block at the
  top of `docs/tram_rescope_estimate.md` and `docs/tram_rescope_specs.md`,
  and the "Trams left off built maps" item of
  `docs/plan_detail/city_watch.md`. `DECISIONS.md` and `PLAN.md` are
  Cleanup's.
- **Downstream inputs changed by this branch so far:** none.
