# Load estimates — tram rescopes and wave 2

**Saved 2026-09-27 (owner), as republished with the master list that evening.**
These are judgement estimates, in % of one 5-hour usage window. No per-build
usage has ever been recorded. The anchor is one day's readings (the 5-hour
window moved about 8 points per weekly point), and that window is shared by
every session, so the anchor may overstate. **Read `get_usage` before and
after the first batch of either, and rescale the rest.**

The rescopes' longer recommendations are in `docs/tram_rescope_estimate.md`.

## To do: tram rescopes of built cities (held by the owner)

Total about **55–85% of one 5-hour window**.

| Category | Cities | Load | Recommendation |
|---|---|---|---|
| Complete the tram list | Barcelona TRAM, Hong Kong Tramways, Seoul's Wirye Line, D.C. status, Cablebús | 5–8% | **Yes, first.** It now runs with wave 2 |
| Light | **REM**, Rome 8, Madrid ML1, SF F Market, D.C. Streetcar | 10–20% | Yes, one batch, REM first; D.C. once verified |
| Medium | Paris T3a/T3b | 4–6% | Yes |
| Heavy | Toronto (18 routes), Milan (17), Prague (37) | 18–30% | Not yet: a label and legend rule first, then a Toronto pilot |
| Blind spots | Barcelona, Hong Kong Tramways | 8–10% | Barcelona likely yes; Hong Kong stays out; Cablebús yes |
| Batch overhead | — | 8–12% | Pay once, at review time |

## Wave 2 of the second-city screens (after the 10pm reset, in the order the owner agreed)

Total about **80–130% of one 5-hour window, likely more than one window**
(roughly 10–16% of the weekly limit). Wave 1's cost was never recorded.

| Order | Group | Load | Note |
|---|---|---|---|
| 1 | Tram-list count | 5–8% | Unblocks Band T's decision |
| 1 | Canada, Brazil, Ireland | 15–25% | Cheapest per city. Brazil's national modules exist; Waterloo's ION the Canadian lead |
| — | *Read usage, rescale groups 2 and 3* | | |
| 2 | Spain, Italy | 30–45% | Registers found city by city; many tram cities |
| 3 | US | 30–50% | A later window if Spain and Italy run high |

Every screen agent fetches OSM through `pipeline.osm.fetch`.
