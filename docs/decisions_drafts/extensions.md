# DECISIONS drafts - extensions (`extensions-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

Proposals (sentences no approved template covers) are listed at the end, for
the owner at review time.

### 2026-10-03 - Rio de Janeiro (Regional): Duque de Caxias added, the Saracuruna line drawn to its end

- **Second of the four extensions.** Rio becomes "Rio de Janeiro
  (Regional)"; page file and slug stay.
- **Proved off first** (commit with the switch off): zero drift, baseline
  11 figures unchanged, peak 0.58 GB.
- **The shuttle, on the owner's call of 2026-09-30** (PLAN "Wave-2
  follow-ups" (5)): beyond Gramacho the Gramacho-Saracuruna shuttle fails
  the rail test (SuperVia's notices: the 12-minute peak runs
  Central-Gramacho only; a 50-minute average beyond). Its OSM relations
  (6018221, 9963666) stay out of the station reader; their geometry is
  appended to SuperVia Saracuruna's line, so the line is drawn to
  Saracuruna, and Campos Elíseos, Jardim Primavera and Saracuruna go to
  `excluded_stations.csv` as not ringed. **Departure noted for review:**
  `docs/category_rules.md`'s station rule for a light-rail stretch under
  the 15-minute test is "not drawn"; this is a commuter line under
  Brazil's rail test and the owner's own call drew it, so the reason
  string carries "fails the rail test", not "15-minute", and What Is
  Excluded counts the three under "other".
- **What moved** (drift check, every change the extension's):
  - stations 95 → 98 in scope (Duque de Caxias, Corte Oito, Gramacho),
    still 3 excluded (now the shuttle's three); gate 3 unchanged;
  - storefronts 106,723 → 125,440 (+18,717; staging's probe said 18,698):
    Retail 59,995, Food service 42,058, Personal services 23,387;
  - in-ring 30,293 → 33,029, the share 28.4% → 26.3% ("more than a
    quarter" stands); unreadable 32.8% overall, 34.6% within the rings
    (the page's "about a third" and "about 35 in a hundred" stand);
  - scope 1,202.1 → 1,668.8 km2; 57.4% of dots at a dwelling address.
- **The sanity box widens north to -22.45** (Duque de Caxias reaches
  -22.476); 0 rows dropped by it. The fetch box stays: OSM returned the
  whole município and the shuttle relations' whole geometry.
- **Duque de Caxias's CNEFE file** is staging's cache (10,850,283 bytes),
  the server's length matching, Last-Modified 2024-05-20, in provenance.
  No new source, so no licence row and no notice; IPP's notice 39 follows
  the page's new name in `components.py`.
- **Privacy: publish.** `check_personal_exposure.py rio_de_janeiro`: no
  registrant column, 0 emails, phone numbers or c/o markers; the
  heuristic's 10.9% is the upper-case Portuguese misfire; `person_name_in`:
  4,140 with a first name, 2,786 hidden at a dwelling address, 1,354 shown
  as trade names.
- **Macro label** 168.6 px (the Belo Horizonte run). Right of the dot is
  still the only side with PROBLEMS 0 (above covers Belo Horizonte's dot;
  below and left meet São Paulo and Santos), clipped 24% at 375 px only.
- **Brief check 7/8**; the eighth (OSM's MetrôRio and VLT refs, the colour
  source) was not checked: every Overpass mirror refused. To retry.
- **Regional processed files** in `data/rio_de_janeiro/processed/regional/`
  from the start.

### 2026-10-03 - Belo Horizonte (Regional): Contagem added, Linha 1's two western stations ringed

- **The extension the owner released on 2026-10-02**
  (`docs/handoff_extensions_2026-10-02.md`), first of four. Belo Horizonte
  becomes "Belo Horizonte (Regional)"; the page file and slug stay.
- **Proved off first.** A `REGIONAL` switch in
  `pipeline/belo_horizonte/config.py`, committed off (8ca5d522): the
  city-alone build re-rendered with zero drift (baseline 11 figures
  unchanged).
- **Switched on, what moved** (drift check, every change the extension's):
  - stations 20 → 22 (Eldorado and Novo Eldorado, in Contagem; none left
    out now), gate 3 unchanged at 21 + 2 = 22;
  - storefronts 45,597 → 58,552 (+12,955): Retail 22,758 → 29,414, Food
    service 13,523 → 17,168, Personal services 9,316 → 11,970;
  - in-ring 8,404 → 9,346, so the ring share falls 18.4% → 16.0% (the
    page now says one in six);
  - the unreadable share 38.6% city-wide and 42.3% within the rings, so
    the page's "about four in ten" and "slightly more near the stations"
    stand;
  - scope 331.0 → 525.8 km2 (Contagem 194.8); 40.2% of dots share an
    address with a dwelling (35.8% before).
- **The sanity box widens west to -44.20**, since Contagem reaches -44.162,
  past the fetch box's -44.15. The fetch box stays: OSM's `out geom`
  returned Contagem's whole outline and Linha 1 ends at -44.04. The box
  dropped 0 rows.
- **Contagem's CNEFE file** is staging's cache (7,697,598 bytes), copied to
  `data/belo_horizonte/raw/` with its timestamp; IBGE's server answered
  200 with the same length and Last-Modified 2024-05-20, recorded in
  provenance. A brief claim for it was added (`contagem-cnefe-file-live`).
  No new source: CNEFE and OSM are the city's own, so no licence row and no
  notice.
- **Privacy: publish**, as before. `check_personal_exposure.py
  belo_horizonte`: no registrant column, 0 emails, phone numbers or c/o
  markers; its person heuristic reads 17.6%, the known misfire on
  upper-case Portuguese (brazil-city trap 7). The module's own
  `person_name_in`: 1,528 descriptions with a first name, 802 hidden at a
  dwelling address, 726 shown as trade names elsewhere (605 and 607
  before).
- **Macro label** measured at 171.5 px (canvas, local app, six controls
  reproduced). Above the dot it grazed Brasília's marker, below it covered
  Rio's, right of it was clipped 21% at 375 px; left of the dot scores
  PROBLEMS 0 with no graze or clip.
- **Gate measurements:** the job gate measured 0.34 GB (off) and 0.41 GB
  (on) for this city's drift check, against 2.5 GB declared with no history.
- **A shared-data slip, caught by Cleanup and fixed.** The scope-on drift
  check wrote the regional files into `data/belo_horizonte/processed/`,
  the shared junction master's checks read, so `check_macro_facts` failed
  for every session (memory rule: no step re-run from a branch for a city
  on master). Master's state was restored by re-running steps 1-2 with the
  switch off (45,597 again), and the regional build now writes
  `data/belo_horizonte/processed/regional/` (ignored) until it lands; Rio's
  config does the same from the start. Rio's own `processed/` was rewritten
  only by its scope-off run, which matched master. **Consequence:** on this
  branch `check_macro_facts` reads master's files and fails for Belo
  Horizonte (Regional) until it lands, so the pre-push hook holds the
  branch; asked of Cleanup, who owns the check.
- **Docs moved with it:** its What Is Excluded section (counts from the
  step 2 log; unreadable 36,922), its three rows in
  `docs/data_sources/brazil.md`, map_inconsistencies tables A, B and D and
  the under-25% list (in-ring 5,105 / 2,616 / 1,625, by nearest-station
  distance, reproducing the map's 9,346), `docs/ring_rules.md`, the
  master list's Built row, README, `app/macro_facts.json`,
  `app/ring_shares.json` (only this city's entry; master's other blob ids
  are stale but pass), `scripts/check_provenance.py`'s slug override.

## Proposals for the owner (sentences no template covers)

1. Belo Horizonte (Regional), page, The lines: "The map covers **Belo
   Horizonte and Contagem**, where Linha 1's two western stations stand."
   (replaces "The map covers the município of Belo Horizonte; Linha 1's two
   western stations, in Contagem, are not counted.")
2. Belo Horizonte (Regional), What Is Excluded, Stations: "the map covers
   Contagem with Belo Horizonte, so Linha 1's two western stations, Eldorado
   and Novo Eldorado, are counted."
3. Rio de Janeiro (Regional), page, The lines (new): "Beyond Gramacho the
   Saracuruna line runs on to Saracuruna as a shuttle, a train about every
   50 minutes: it is drawn to its end, but its three stations there are not
   counted (listed below)."
4. Rio de Janeiro (Regional), page, The lines: "The map covers **Rio de
   Janeiro and Duque de Caxias**, where the Saracuruna line runs on to
   Gramacho." (replaces "The map covers the município of Rio de Janeiro;
   the Saracuruna line's stations in Duque de Caxias are not counted.")
5. Rio de Janeiro (Regional), What Is Excluded, Stations: "the map covering
   Duque de Caxias with Rio, so the Saracuruna line's stations there up to
   Gramacho are counted. Beyond Gramacho the line runs on as a shuttle, a
   train about every 50 minutes: it is drawn to Saracuruna, but its three
   stations there (Campos Elíseos, Jardim Primavera and Saracuruna) are
   left out."
6. What Is Excluded, the stations sentence (all cities): "are on light-rail
   or suburban stretches that run less often than every 15 minutes" (was
   "on light-rail stretches"). Rio's three shuttle stations are counted as
   too infrequent: app/station_scope.py now reads "fails the rail test" as
   that category, beside "15-minute". If the owner prefers, they can be a
   category of their own instead.
