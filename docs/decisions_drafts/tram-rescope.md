# Decisions drafts: tram-rescope

Newest first. Cleanup folds these into `DECISIONS.md` at review time.

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
