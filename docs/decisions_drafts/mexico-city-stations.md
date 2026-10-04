# DECISIONS drafts - Mexico City station repair (`claude/xenodochial-goodall-c3a7b7`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-04 - Guadalajara's Ávila Camacho collapsed to one station (owner, via Staging; branch, lands with Mexico City's repair)

- **Collapsed Guadalajara's doubled station: 56 stations -> 55.** OSM names
  the Línea 1 and Línea 3 stop positions at the Ávila Camacho interchange
  "Avila Camacho" and "Ávila Camacho", 98 m apart, and step 1 collapsed by
  the raw name, so the page kept two stations there. The owner asked for the
  fix through Staging the same day, on this branch, to land with Mexico
  City's. `pipeline/guadalajara/step1_stations.py` now collapses on
  `pipeline.stations.station_name_key`. That key also covers the hand-written
  " L<digit>" strip it replaces ("Independencia L3"), so Independencia is
  unchanged. Only these two names merged. The merged station sits at the mean
  of its four stop positions (20.698844, -103.354871), about 50 m from either
  old point. Businesses in a ring, of 116,945: 36,752 -> 36,751
  (`app/ring_shares.json`, Guadalajara's row only).
- **The shown name follows Monterrey's rule, the spelling with the most
  accents** ("Ávila Camacho", the operator's), rather than a per-name fix in
  config. OSM's unaccented variants are the errors in both cities, and a
  rule needs no entry to go stale. Monterrey's `PUBLIC_NAME_FIXES` remains
  the tool for a name wrong outright.
- **Gate 3 still passes:** SITEUR's 10 and 8 for Líneas 2 and 4 against
  OSM's 10 and 8. It counts route members, so the collapse cannot move it.
  `KNOWN_SAME_NAME` in `pipeline/stations.py` is empty again; the gate now
  raises on Guadalajara like any city.
- **Noted for the owner, not changed:** two pairs remain 91 m apart under
  different names, "Guadalajara Centro" (Línea 3) / "Plaza Universidad"
  (Línea 2) and "Juárez" (Línea 1) / "Juárez II" (Línea 2). They are
  interchanges, so each could be one station, or two as SITEUR names them.
  Neither is a spelling of the other, so the same-spelling gate does not
  decide them, and neither is recorded anywhere yet. Merging either is a
  station-count call for the owner.
- **Count corrected in `docs/data_sources/mexico.md`:** "56 stations across
  four municipios" -> 55.
- **Verified: `python pipeline/drift_check.py guadalajara mexico_city`
  reported zero drift against commit d4b0b383**, both cities' outputs
  identical (maps after Folium-id normalization), baselines unchanged
  (Guadalajara 8 figures, Mexico City 7), measured peak 1.40 GB. Mexico City
  was re-checked because `pipeline/stations.py` changed again.
  `check_provenance.py` names Guadalajara (Regional) and Mexico City OK.
  Master's `data/guadalajara/processed/` and `data/mexico_city/processed/`
  were restored afterwards (56 and 163 stations); the lander re-runs both
  cities' step 1 at merge, then the full drift sweep.

### 2026-10-04 - Mexico City's stations repaired: nine stop-only stations added, two interchanges collapsed, two shared checks that raise (branch, held for review time)

- **Found that Mexico City's built page was missing nine Metro stations and
  kept two interchanges twice, and repaired step 1: 163 rows kept -> 169;
  10 excluded -> 11.** Staging's probe of the State of México (2026-10-04)
  reported it; each claim was re-measured on the cached OSM
  (`data/mexico_city/raw/`, fetched 2026-09-21; no Overpass query was made).
  Eight in-city stations exist in OSM only as `railway=stop` positions on
  their line's route relation and were dropped by the `railway=station`
  whitelist: Observatorio (Línea 1), Indios Verdes, Potrero and Juárez
  (Línea 3), Mixcoac (Línea 7; Línea 12's members there are untagged),
  Tepalcates (Línea A), Buenavista (Línea B), and Talismán (Línea 4), whose
  station node exists but carries no mode tag, so the mode test dropped it.
  The ninth is Cuatro Caminos, Línea 2's terminus, a stop position only, now
  in `outputs/mexico_city/excluded_stations.csv` at 200 m outside the CDMX
  boundary. The probe found Consulado kept twice ("Consulado" and
  "Consulado L4", 329 m apart); the shared check below also found
  **Candelaria** ("Candelaria L1" and "Candelaria L4", 180 m), which the
  probe had missed. The 163 rows were therefore 161 stations, and the probe's
  "162 unique" was one high. Businesses in a ring, of 280,185: 131,667 ->
  135,284 (`app/ring_shares.json`, rewritten by `check_ring_shares.py
  --write`; its diff touched Mexico City's row only). Files:
  `pipeline/mexico_city/step1_stations.py`, `pipeline/mexico_city/config.py`
  (comment), `outputs/mexico_city/`, `app/ring_shares.json`. The
  `app/` file makes this a deploy when it lands: compute the reboot question
  from the whole push's `app/` diff then.
- **Decided that station nodes keep precedence and stop positions only fill
  gaps.** A named stop member of a drawn relation becomes a station only when
  its `station_name_key` matches no whitelisted station node. The rejected
  alternative, collapsing every stop position with the station nodes, would
  have moved all 161 existing stations' coordinates for no gain and turned a
  nine-station repair into a whole-map re-placement. Proposed Texcoco
  stations are on no route relation, so the whitelist's immunity to the
  `railway=prpopsed` typo is kept.
- **Collapse is now by `station_name_key`, not the raw name**, and the shown
  name drops a line designator ("Consulado L4" -> "Consulado"). Only
  Consulado and Candelaria change. The key also folds accents, a leading
  "Metro " and the separators "/" and "-", which makes "Garibaldi/Lagunilla"
  (a stop) match "Garibaldi-Lagunilla" (a station). No existing Mexico City
  station merged except those two (checked across the whole kept set). Kept
  names "Metro Insurgentes Sur" and "Tlahuac" are unchanged; renaming them is
  not part of this repair.
- **Per-line counts from route membership sum to 195 over the twelve Metro
  lines** (Línea 1 20, 2 24, 3 21, 4 10, 5 13, 6 11, 7 14, 8 19, 9 12, A 10,
  B 21, 12 20; Tren Ligero 18 with Tasqueña). The sum matches the probe's
  from-memory line-station total of 195. **This is not gate 3**, which stays
  unavailable (`STATION_COUNT_GATE_3 = None`, the operator's host still
  times out), so the figures are printed by step 1 and not asserted. Unique
  stations across the bbox: 180, so 163 for STC Metro alone. The probe
  expected "about 170" in the city from 164 unique STC stations; the gap of
  one is in that from-memory interchange count. It is not a missing station:
  every one of the 426 stop members of the 26 drawn relations now has a
  station (416 by name, the 10 untagged members within 250 m).
- **Added two raising checks to shared code, so the next city must pass
  through them (the osm-rail meta-rule), rather than a comment in Mexico
  City's config.** In `pipeline/stations.py`:
  `route_stop_members` + `check_route_stops_covered`, which raise when a stop
  member of a drawn route relation has no station in the whole collapsed set
  (named: by key; unnamed: within 250 m). Mexico City calls them, and the
  osm-rail skill's checklist now requires them for any tag-selected station
  set. The rejected alternative was making every OSM step 1 derive stations
  from membership: right for a new city, and Guadalajara and Monterrey already
  do, but a rewrite of built cities is not this repair. Second,
  `verify_stations` (every city's step 1 calls it) now raises on **two
  different spellings of one key within the spacing floor (400 m)**. A scan
  of all 170 committed `stations.csv` files found three hits: Mexico City's
  two (fixed here) and **Guadalajara's "Avila Camacho" / "Ávila Camacho",
  98 m apart**, a live defect outside this task, listed in
  `KNOWN_SAME_NAME` as a dated defect that prints instead of raising, and
  raises once fixed so the entry cannot linger. Identical names are only
  noted, not raised: New York keeps same-named rows per complex part and
  Amsterdam two Wibautstraat rows, on purpose. Den Haag's per-line stops
  ("Loosduinseweg (line 11)" / "(line 12)") sit 496-575 m apart, past the
  floor. The scan read the committed CSVs, not each step's in-memory frame,
  so the full drift sweep at landing is the real test for the other cities.
- **Counts corrected in `docs/data_sources/mexico.md`** (renders on About
  the Data): "163 stations kept" -> 169; "Lines A and B ... 10 stations are
  cut" -> "Lines 2, A and B ... 11 stations are cut". Facts only.
- **PROPOSAL for review time (not written):** the Mexico City page's third
  bullet under "The lines" says "Líneas A and B run north and east into the
  State of Mexico". Cuatro Caminos makes that incomplete. Proposed: "Líneas A
  and B run north and east into the State of Mexico, and Línea 2 ends just
  across the city line at Cuatro Caminos; those stations are left out because
  this map has no business data for them — their rings would sit over blank
  ground. They are listed below." An `app/` change, so it waits for review
  time with the rest.
- **PROPOSAL for review time (not written):** the station method in
  `docs/data_sources/mexico.md`'s rail row still describes the whitelist
  alone. Proposed addition after the Lechería sentence: "Nine stations exist
  in OpenStreetMap only as stop positions on their line's route, so the named
  stops of each drawn route are added wherever no station node of that name
  exists, and every stop on a drawn route must end up with a station."
- **Verified: `python pipeline/drift_check.py mexico_city` reported zero
  drift against commit 097fb3af** (`excluded_stations.csv` and
  `baseline.json` identical, `heatmap.html` identical after Folium-id
  normalization; baseline's 7 figures unchanged: 462,732 DENUE rows,
  442,146 fijo, 280,186 storefront, 280,185 clean, Retail 202,419, Food
  service 49,164, Personal services 28,603; measured peak 1.43 GB).
  `check_provenance.py` names Mexico City OK. `check_all.py`: 47 of 48, with
  `check_ring_shares.py` passing after the rewrite; the one failure is
  `check_macro_facts.py` on six Japanese cities (Hiroshima, Matsuyama,
  Toyama, Kumamoto, Fukui, Nagasaki), whose shared processed data another
  session rewrote between two runs that afternoon. Nothing here touches
  them, and no `--write` was run for them. Only Mexico City was
  drift-checked, by instruction.
- **The step re-runs on this branch wrote the shared
  `data/mexico_city/processed/stations.csv`; master's copy was restored
  afterwards** (`project_shared_data_junction`). Whoever lands this branch
  re-runs `pipeline/mexico_city/step1_stations.py` at merge, then the full
  drift sweep (the `pipeline/stations.py` change reaches every city).
