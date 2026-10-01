# DECISIONS drafts - tram kit (`worktree-tram-kit`, then `tram-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - Liepāja built on tram-build; Riga's step 2 lifted into latvia_register.py

- **Riga's step 2 was lifted into `pipeline/countries/latvia_register.py`,
  and Riga's output did not move.** Riga's step 2 is now a thin call into
  the module.
  - **The control** is `scripts/latvia_register_control.py`. It rebuilds
    Riga's frame through the module and compares it with Riga's
    `businesses_clean.csv`. All 6,725 rows are identical, and all 11 step 2
    figures match `outputs/riga/baseline.json`.
  - **Rejected: running `drift_check.py riga` as the control**, which the
    skill had named. It would re-run Riga's steps from a branch into the
    shared `data/` junction, and the in-memory control answers the same
    question without writing.
  - **The classification stays in `pipeline/riga/config.py`**, and later
    Latvian configs import it from there. `category_continuity_table.py`
    reads those rules by their text in Riga's config, so moving them would
    break that check. One set of rules for the country, decided once.
  - **Measured peak: 0.34 GB.**
- **Liepāja built: 18 stations, 702 storefronts, 69.7% in a ring** (the
  screen's figure).
  - **Stations: the 15 stop names on OSM's two ref-1 relations, plus three
    added by node.** All three lie on the relations' own track:
    - Brīvības iela, the terminus, is a platform member whose stop
      position carries no name;
    - Klaipēdas iela, between Tukuma iela and Ventas iela, has a stop
      position each way but is on neither relation;
    - Rožu laukums, between Pētertirgus and Koncertzāle, is a platform
      member each way with no stop position.
  - **The approved call named only Brīvības iela and Klaipēdas iela**, but
    the brief's own count of 18 needs Rožu laukums too. So it was read as
    the brief's prose missing one stop, not as a new call.
  - **`osm_tram`'s `station_add` now accepts a named platform node**, for
    an add only, and refuses an add whose name is already a route stop. The
    Aarhus control still passes, and Odense still has zero drift.
  - **Spacing and frequency.** The median gap is 313 m (the brief: 329 over
    15). No gate 3: no operator count was read. The approved call's "about
    every 7 minutes" is stated on the page.
  - **Food** comes from the excise register (Riga's national cache), placed
    on VZD's address register `aw_eka.csv` (fetched 2026-09-30, 7,839
    existing addresses in Liepāja): 131 premises, 123 placed (93.9%: 110
    exact, 13 with the unit dropped). This matches the screen.
  - **Shops and services** come from the premise groups in ATVK 0005000:
    771 premise groups, 579 kept, all placed. The screen counted 583 before
    the 2026-09-29 name-rule changes (fuel stations kept, repair and stands
    dropped).
  - **Step 2's measured peak was 0.30 GB.**
- **Liepāja privacy verdict: publishable.** 489 pins, 0 contact details and
  0 person-like names. No holder column is ever read: food shows the kind
  and street address, shops show the cadastre's own word.
- **Notice 42 widened to "VZD (Riga, Liepāja)", FOR THE OWNER'S APPROVAL AT
  REVIEW TIME.** It names Liepāja's cadastral map and VZD's State Address
  Register, with the elements the brief requires:
  - VZD's own source wording and the year, "Izmantoti Valsts adrešu
    reģistra informācijas sistēmas dati, 2026. gads";
  - VZD named, and CC BY 4.0 linked;
  - the changes described: addresses matched and points used to place each
    premises, and the file not shown;
  - "VZD has not approved these changes or this map."

  The OpenStreetMap rail-geometry notice now names Liepāja's tram, its
  stops and the city boundary.
- **Liepāja is left out of Europe's zoom fit (`REGION_ZOOM_WITHOUT`), as
  Riga, Stockholm and Bucharest are.** Fitted to it, the zoom dropped and 57
  label problems appeared at every width, whatever Liepāja's own offset. It
  lies inside the frame Riga and Bucharest already set, so the centre does
  not move. Its label is 48.2 px, measured, placed below the dot (dy 14-34
  pass): PROBLEMS 0.
- **The template's "{this city's ratio to OpenStreetMap}" is left unfilled
  for Odense and Liepāja.** Neither template city's page has one: Aarhus's
  CVR wording and Riga's two-layer wording are what section 6 says to
  reuse. Measuring one is an Overpass count of shops and food per city, with
  its own caveats about OSM's tagging. **For the owner: fill it per city, or
  drop it from the template?**

### 2026-09-30 - Odense built on tram-build; osm_tram.py written, its Aarhus control passing

- **`pipeline/osm_tram.py` written to the tram-city skill's section 4
  contract (commit 17f906c on `tram-build`), and its control passes:
  `scripts/osm_tram_control.py` reproduces Aarhus's `stations.csv` exactly**
  on Aarhus's cache: 20 stations, the same names, lines and kommune, and
  coordinates within 1e-9 degrees. It is Aarhus's `stop_rows()` generalised:
  - `select_relations` keeps relations on ref + route (+ operator), and exits
    on any relation that is neither kept nor in `not_drawn`, on a stale
    `not_drawn` id, and on a ref with no kept relation. It is also the
    lines-only mode.
  - `stop_rows` takes stop members tagged `stop_position` or `tram_stop`,
    unions a ref's relations, takes `station_add` by node with its expected
    name, and applies aliases whose two spellings must both be present.
  - `collapse` is Aarhus's name collapse at 200 m.
  - `split_by_places` scopes over a union of polygons.

  Aarhus's own step 1 was not rewired: its output is the independent answer
  the control compares against. The signature, return shape and branch went
  to the Czech kit (which was waiting on them) and to the France build
  session. Staging, the app/chrome owner while no third window runs, was told
  before the file was written.
- **Odense built: 25 stations, 2,834 storefronts placed (98.4%).**
  - **Rail.** OSM's two `route=tram` relations (ref L, operator Keolis)
    carry 24 stop names on 48 stop positions. SDU Syd/Hospital Nord was added
    by its two direction nodes (7942163365, 7942163366), as the approved
    call. Gate 3 ran against the operator's figure: 25 against 25, the
    operator's 26 stops less Hospital Syd. Every station is in Odense Kommune
    (304.7 km² as OSM draws it). The line is drawn whole with
    `load_osm_line_shapes`.
  - **Spacing.** The median gap measured 430 m, not the brief's 441, and
    holds the halved rings; step 1 stops outside 380-500 m.
  - **Stray node.** Idrætsparken's node 9034508024 is also on no relation.
    It is a second stop position 10 m from Idrætsparken's member node, not a
    station, so it was left alone.
  - **Businesses.** CVR generation 505 through Aarhus's chain: 3,208 rows in
    divisions 47/56/96 and 221 structurally excluded, leaving 2,987. `969900`
    was dropped (108 rows, 3.6%, 84% personally owned against 46%), leaving
    2,879, of which 2,834 were placed. The screen of 2026-09-27 counted 210
    structural exclusions and 2,998 storefronts. The build's filter is the
    shared one, so the build's figure stands.
  - **Rings.** 1,154 storefronts sit within a ring (40.7%), in-ring
    R/F/P 603/343/208.
- **Hospital Syd is a watch item, not a row in `excluded_stations.csv`.**
  The approved call was "out until it opens in 2027". Listing it failed
  `check_scope_disclosure.py`: What Is Excluded has no category for a stop
  not yet in service, and adding one is an `app/station_scope.py` change and
  an owner call. A stop that is not yet in service is not part of the
  network, so no category is needed. Step 1's `check_not_yet_open` stops the
  build when OSM puts Hospital Syd on a route or drops its tag. The page does
  not mention it. **For PLAN.md: add Hospital Syd when the new OUH opens
  (due 2027).** Rejected: a new "not yet open" category, which is new public
  wording for one stop.
- **The frequency sentence is left out of Odense's page.** It is optional in
  the template (braces). Odense Letbane's own køreplan page, valid from
  10 August 2026, states Saturday (7.5 min), Sunday (10 min) and Friday
  evening (10 min), but no weekday figure. The brief's 7.5 minutes came from
  the screen, so it is not stated. Rejseplanen is never read. The owner's
  per-city interval value (sent to cleanup) can carry it later.
- **Line colour `#b8860b` (dark goldenrod)**, this project's own, since OSM
  records none. CIE76 74.8 from the nearest pin (Personal services);
  `check_map_markup.py` PROBLEMS 0. Aarhus's `#30556E` was tried first and
  scored 42.7 against Retail, under the preferred 45.
- **Macro label.** The width measured 50.6 px in a browser tab with Google
  Fonts' Space Grotesk. Seven built cities' widths reproduced exactly:
  Aarhus 46.9, Prague 47.3, Oslo 29.0, Riga 29.5, Bergen 48.3, Boston 48.4
  and Chicago 55.0. The offset is `("start", 11, 6)`: only dy 5-8 on the
  right passes. Above the dot, the label covered Aarhus's marker and
  overlapped Copenhagen's label; below, it overlapped Amsterdam's and
  Berlin's. `check_macro_labels.py` PROBLEMS 0.
- **Odense privacy verdict: publishable**, on Aarhus's precedent.
  `check_personal_exposure.py odense` found 1,154 pins, 0 contact details
  and 0 person-like names at a residential unit. The heuristic's 170
  distinct person-like names were read in full: brands and chains (Arnold
  Busck, Harald Nyborg, Magasin, ZARA) and company-form shops, cafés and
  salons trading under a founder's name (HENRIK GUNDTOFT, Ingvard
  Christensen, Nadja Holst). Personally owned forms are already shown by
  address. The one bracketed hit, "GreenMind Odense (Kongensgade)", is a
  chain branch.
- **Three displayed notices widened to name Odense, FOR THE OWNER'S APPROVAL
  AT REVIEW TIME** (Aarhus's were owner-approved on 2026-09-29):
  - CVR, notice 30: "(Copenhagen, Aarhus, Odense)", "Copenhagen's, Aarhus's
    and Odense's business premises";
  - Klimadatastyrelsen, notice 31: "in Aarhus and Odense the points are
    OpenStreetMap's copies of them";
  - OpenStreetMap (rail geometry): "Odense's Letbane line and its stops, the
    municipal boundary used to select them and the address points used to
    place its businesses".

  They sit on `tram-build` and ship only when `app/` lands.
- **Step 2 is not a heavy job: measured peak 0.70 GB.**
  - The gate (`scripts/heavy_job.py`) refused it first at the 5.5 GB
    declared from Aarhus's brief: 6.9 GB available, against 5.5 + 2. That
    "about 5 GB" was the size of the files read, not memory.
  - It was re-run under `HEATMAP_MEMCAP_TEST_GB=4.5`, a hard cap that can
    only lower the per-process limit. The declared 4.5 GB peak was then true
    by construction, and was admitted.
  - A Danish step 2 can be declared at 1 GB from now on.
- **Page numbers by block**, agreed between sessions so the landings don't
  collide:
  - Band B: 76-86;
  - France: 100-119;
  - tram kit: 130-139 (Odense 130);
  - Czech: 150-155.
- **Left for the landing, not done on the branch**:
  - README's city list (`readme_cities.py`);
  - the master list's built counts;
  - `map_inconsistencies.md`'s prose counts (section 6, "half the size in
    seven cities").

  Each is a shared count that every concurrent build would change on its
  own branch, so each is set once, at landing.

### 2026-09-30 - All builds activated, with six working rules for concurrent sessions (owner)

- **The owner gave the go for every build session**: Band B, the France
  builds, the Czech builds and the tram kit. The go was relayed by the tram
  kit to each live session. The Czech kit asked the owner to confirm it in
  its own session, which is the right behaviour for a relayed permission.
- **The six rules, in the owner's words where given:**
  1. **Heavy jobs**: "If two heavy jobs go under the memory thresholds we
     established, run those concurrently." The relay first set the budget at
     12 GB summed over two jobs (the 12 GB with-children cap). A measurement
     minutes later disproved it: only 2.3 GB of 15.9 was available, with
     eight Claude sessions taking 6.3 GB, Opera 1.8, and an orphaned
     staging grep 4.7 (PID 17392, started 13:54, a
     `.{0,30000}` pattern over a licence page, its parent gone). The tram
     kit was not permitted to stop another session's process, so that was
     left for the owner. **Corrected rule**: at most two heavy jobs, each
     started only when available memory is at least its peak plus 2 GB; an
     unknown peak counts as 8 GB.
  2. **Priority**: the tram kit goes before the Czech builds. So the tram
     kit writes `pipeline/osm_tram.py` first, starting with Odense.
  3. **DECISIONS.md drafts per session**: "keep drafts for decisions.md for
     each build session and pass off all at once for cleanup to implement".
     Each session writes `docs/decisions_drafts/<session>.md`, and cleanup
     folds them all in at once. That ends the append-only merge conflicts,
     four of which fell on this session's pushes on 2026-09-30 alone.
  4. **Overpass**: "stagger osm requests": one query in flight per session,
     and at least 60 s after a 504 or 429. Both mirrors were 504ing under
     several sessions' load that day.
  5. **Plan**: the owner is no longer on Pro.
  6. **Downloads and prose are pre-permitted**: the sources a brief names,
     and page text written from an approved template. A departure from a
     template is flagged, and does not stop the build.
- **Memory monitoring: a start gate, not a monitor.** The owner asked
  cleanup to "monitor all sessions for memory. Or whatever reactive protocol
  is efficient and safe". The tram kit recommended a gate,
  `scripts/heavy_job.py`, with a ledger in the shared `data/` junction that
  admits a job only if it fits in available memory, drops dead pids, and
  lists any process over 1.5 GB. Polling spends tokens all day and still
  reacts after the damage; a gate costs one call per heavy job. It was handed
  to the multi-city cleanup session to build. A second session named
  "Cleanup Session" belongs to another project (link-station-commercial),
  received the broadcast by mistake, and declined it.
- **Rejected**: a fixed summed budget (disproved by measurement above), and
  a polling monitor session.
