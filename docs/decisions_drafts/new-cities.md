# DECISIONS drafts - new-cities build (`new-cities-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30). The build
is Liverpool (Regional), Tacoma and Mendoza
(`docs/handoff_new_cities_2026-10-03.md`).

### 2026-10-04 - The UK steps take heavy rail: a configurable NaPTAN stop type, a route filter and boundaries by GSS code; zero drift on the UK six

- **`pipeline/countries/uk.py`'s NaPTAN gate reads `config.NAPTAN_STOP_TYPE`,
  MET when unset; Liverpool (Regional) sets RLY.** Merseyrail's stations are
  rail access nodes (StopType RLY, ATCO area 910, prefix 9100), never the
  tram stops' MET in area 940, so the gate's hard-coded `"MET"` would have
  counted zero. The default keeps the six built UK cities on MET without a
  config edit. `norm_name` also drops NaPTAN's rail suffix "Rail Station" and
  a county qualifier left trailing once it is gone ("Walton (Merseyside) Rail
  Station"): area 910 names 95 of its 98 records in a Merseyside box that way
  (read 2026-10-04 from a scratch probe of the area file). The alternative, a
  per-city alias for every station, would have been 59 entries restating one
  suffix rule.
- **`pipeline/countries/uk_fetch.py` gains `config.OSM_ROUTE_FILTERS` and
  `config.BOUNDARY_GSS`, both fetch-only.** The first narrows a route mode to
  one network (tag filters, each its own selector, unioned), because every
  `route=train` in a Merseyside box would otherwise come back (the osm-rail
  skill's rule against box-wide train queries). The second selects the scope's
  admin relations by `ref:gss` when their relation ids are not yet known, so
  the city's one Overpass query also reads the ids, which the config then
  records; each code must match exactly one relation. `fetch_osm` now counts
  route relations by `type=route` rather than by not being a boundary id,
  the same set for every built city.
- **Proved at zero drift on the six built UK cities, twice**:
  `drift_check.py manchester birmingham edinburgh sheffield nottingham
  blackpool`, once after the stop-type change and once after `norm_name`'s,
  both "RESULT: zero drift", every baseline figure unchanged and every
  NaPTAN name match as before (Manchester 99, Birmingham 35, Edinburgh 23,
  Sheffield 48, Nottingham 50, Blackpool 40); measured peak 0.48 GB through
  `heavy_job.py`. The fetch change cannot be drift-checked (no step runs
  it), so the six cities' Overpass query strings were generated from git
  HEAD's `uk_fetch.py` and from the new one and compared: identical for all
  six. Cleanup confirmed the shape of the change before it landed
  (2026-10-03).
