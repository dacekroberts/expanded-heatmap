# Handoff — small research to-dos (2026-09-27, from Staging)

For a new session taking small, read-only research items off Staging's list.
**Owner's rules apply**: no bypassing (CAPTCHA, login, geo-block, proxy), no
accounts, no harvesting a lookup page's back end. Select columns by exact
name and never print whole rows. Official portals only. Scratch goes in YOUR
scratchpad. Outreach is the last resort. Band moves are the owner's call:
recommend, then wait.

**Work in a worktree of your own** (not `worktree-staging`, whose session is
still open). Push docs-only commits to master with the ritual in CLAUDE.md:
fetch, merge (`scripts/merge_append_only.py DECISIONS.md` on a conflict),
`scripts/decisions_index.py`, push. The pre-push hook runs `check_all.py`.
**Record each finding in `docs/city_master_list.md` (live file) and a
DECISIONS entry**, and run `scripts/check_master_list_counts.py` after any
row change.

## The items, cheapest first (each about 2–5% of a 5-hour window)

1. **Seoul's Wirye Line (위례선): is it open?** OSM has no route relation for
   it (checked 2026-09-27). Find the operator's or Seoul's official opening
   status. If it's open and inside Seoul, it joins the tram rescope list
   (`docs/tram_rescope_estimate.md`); if not, record "not open" in PLAN's
   tram item.
2. **Cablebús Línea 3's stations.** OSM maps only 1 of its stops (L1 6, L2 7,
   all inside CDMX). Find a station list from CDMX's own open data or STE.
   Toulouse's drawn Téléo is the precedent for drawing it. Record the count
   for the rescope.
3. **Kansas City streetcar frequency** (Band T row). The stub test passed on
   OSM (18 stops, all in KCMO). Read the RideKC GTFS's streetcar trips for
   the headway, and note its licence as unread unless you read it (the
   `licence-read` agent).
4. **Incheon's address join** (Band C, owner's verdict "probe first").
   `data.incheon.go.kr` lists carry addresses but no coordinates. Is there a
   keyless national road-address file with coordinates (juso.go.kr's
   downloadable address DB, or the building-register points) that a join
   could use? The `address-join` skill has the method, including a control.
   **If it needs an account or an API key, stop and report**; do not
   register.
5. **Göteborg's rail** (Band T row: "Trams, no metro — INHERITED, not
   measured"). Count Västtrafik's tram lines and stops inside Göteborgs
   kommun from OSM through `pipeline.osm.fetch`. Its colours are needed too.

## Already done today (don't redo)

- The tram list for the blind spots (PLAN), Kansas City's stub test, and the
  Linz lead (aggregate, closed).
- Daegu's and Busan's briefs (built and live).
- The tram rescope specs (`docs/tram_rescope_specs.md`), being built by the
  "Tram rescopes" session in worktree-trams.
- Wave 2's remaining groups (Canada, Brazil, Ireland; then Spain, Italy; then
  the US) are Staging's, run in the order in PLAN. Not for this session.
