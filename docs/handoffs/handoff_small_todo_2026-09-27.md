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

## The items

1–4. **ALL DONE by Staging 2026-09-27** (DECISIONS, "Four small probes"):
   the Wirye Line is not open (PLAN's tram item, re-check January 2027);
   Cablebús L3 has 6 stations, not yet from an official source (PLAN);
   Kansas City's streetcar runs every ~10 minutes (its master-list row);
   Incheon's coordinate file needs the owner's application (its row).
5. **DONE by Staging 2026-09-27: skip it** (13 tram lines, 127 stops; see DECISIONS). (Was: attempted first; its
   boundary query failed on the host; the retry is in
   `docs/handoff_staging_2026-09-27.md`, retired 2026-09-28; in git history). **Göteborg's rail** (Band T row:
   "Trams, no metro — INHERITED, not
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
