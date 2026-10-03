# DECISIONS drafts - extensions (`extensions-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

Proposals (sentences no approved template covers) are listed at the end, for
the owner at review time.

### 2026-10-03 - Burnaby, New Westminster and Coquitlam: the OGL personal-information exemption read cautiously (owner)

- **The owner, relayed by Cleanup and confirmed in this session's chat
  (2026-10-03):** "Accept cautious reading and note as such with our notice
  and privacy related tools", then "Tables/logs". Asked in this session
  whether that meant removing pins, the owner chose "Keep, record as
  cautious": no pin is removed.
- **The question.** All three municipal OGL variants grant no right to use
  "Personal Information" (FOIPPA Schedule 1: information about an
  identifiable individual other than business contact information). A
  licence issued under a sole proprietor's own name, or a business at a
  home, can be read either way (the licence-read agents, 2026-10-03).
- **The treatment, now the recorded reading:** a licence issued under a
  person's own name (printed surname first) shows only its business type
  (8 dots: New Westminster 7, Coquitlam 1); no holder-name, mailing,
  phone or email column is ever fetched (ACCOUNT_NAME, LICENCEE_NAME,
  MAILING_ADDRESS, COL_BUSINESSPHONE, EMAILADDRESS). Home-based licences
  are out wherever the register says so (Burnaby's and Coquitlam's own
  home-occupation types); New Westminster's register carries no home flag.
- **Recorded in:** `docs/privacy_verdicts.md` (Vancouver (Regional)'s
  row), `docs/data_sources/canada.md` (the three licence rows),
  `docs/licence_positions.md` (2.37a-c), `docs/map_inconsistencies.md`
  (table C, Vancouver (Regional)'s exclusions), What Is Excluded (one
  sentence, proposal 15). `check_personal_exposure.py` is unchanged: the
  rule is a name shape applied in the loaders, not a list of keys, so there
  is no key list to add.
- **Consequence:** the open terms question below is closed; the three
  cities are no longer held off the Visuals cards.

### 2026-10-03 - Vancouver (Regional) extended: Burnaby, New Westminster and Coquitlam on their own registers

- **Fourth of the four extensions**, on the owner's three approved calls
  (2026-10-02). The name stays "Vancouver (Regional)"; Richmond (Band R)
  and Port Moody (no addresses) stay out.
- **Proved off first** (de1528d2): zero drift (Vancouver emits no baseline
  figures, so the files are the whole check), peak 0.31 GB.
- **Built in three legs by agents** (no commits, no repository edits),
  then integrated: `pipeline/vancouver/burnaby.py`, `coquitlam.py`,
  `new_westminster.py`; Burnaby's 142 and Coquitlam's 64 values mapped in
  `pipeline/taxonomies/vancouver.py` with a reason each; New Westminster
  through `naics.naics_group`, shown as "NAICS <code>". One generic paged
  ArcGIS fetch in `fetch_sources.py` with explicit field lists:
  **ACCOUNT_NAME, LICENCEE_NAME, MAILING_ADDRESS, COL_BUSINESSPHONE and
  EMAILADDRESS are never requested**, and fetch and step 2 raise if one
  arrives. Stations are scoped and named by the BC ABMS layer already in
  the build.
- **Burnaby** reproduces staging exactly: 2,143 (964 / 746 / 433) after
  one-licence-one-point dedup; the placeholder point (2,179 contractor and
  mobile rows) holds no bucketed row, asserted. RETAIL SALE, RENTAL &
  REPAIR is Retail (owner). **Pending for the owner:** `HEALTH SERVICES -
  OPTOMETRIST/OPTICIAN` (39) is out, as Surrey's optometrists and
  Melbourne's opticians (filed in health), against the rule that keeps
  opticians Retail; about 6 of the 39 read as optical shops. A `pending()`
  row in the continuity table.
- **Coquitlam**: the layer lists every licence twice (and holds Web
  Mercator metres in LAT/LONG); 6,002 licences, 1,026 kept (454 / 332 /
  240). Mall kiosks out (owner): 9 by subtype and 1 with a "Kiosk" unit,
  10 in all. Renewal folders read as current (the coming year's renewal,
  most businesses' only record). By precedent, not owner calls: the
  fee-level catch-alls "Level 1" and "Level 2" (211) out (R2, Surrey's
  Miscellaneous); one "Massage (non-registered) Parlour" licensed as a
  high-impact business out (R3, San Diego's massage parlors); 7 contract
  caterers (R1) and a mobile hairdresser out. **Left for the owner:**
  grooming licences sharing a full address under different names (possible
  chair renters the register does not flag) and about 31 grooming licences
  alone at an address with no unit (possible home salons) are kept as
  published; telling either apart would be a new rule.
- **New Westminster**: 2,736 resident licences, 856 in the buckets (not
  staging's 907: the 2026-09-29 caterer and catch-all exclusions), placed
  by joining CIVIC_ADDRESS to the City's Address_Point layer: 846 exact, 8
  at the building with the unit missing, 2 unmatched; postal-code control
  826 agree, 0 conflict. 853 placed.
- **Names**: 7 New Westminster licences and 1 Coquitlam licence issued
  under a person's own name, printed surname first, show the business type
  (Vancouver's rule of 2026-09-21); a trade name with "&" or a digit never
  counts. Burnaby's and Coquitlam's other names are the licence's business
  name and are left as published (San Diego's and Surrey's precedent).
- **What moved** (drift check, every change the extension's): stations 24
  → 44 (Burnaby 11, New Westminster 5, Coquitlam 4; 10 left out);
  storefronts 11,525 → 15,436 (Burnaby 2,115, Coquitlam 1,016, New
  Westminster 780 after the per-source name-and-address dedup; Vancouver's
  and Surrey's unchanged); in-ring 4,618 → 7,010, the share 40.1% →
  45.4%; every extension point inside its own city (100%). The sanity box
  widens to Coquitlam (49.48 N, -122.58).
- **Privacy: publish.** The shared check's residential-unit figure is
  Vancouver's own "Unit" artifact (the 2026-09-21 verdict; it read master's
  processed file); measured directly on the three new registers: 0
  person-like names at a residential-unit token, 0 emails or phone numbers.
- **Brief**: a checks block added (4 claims, all passing); its figures
  corrected to Staging by message.

### 2026-10-03 - Los Angeles (Regional): Long Beach added on its own licence layer, its holder names never loaded

- **Third of the four extensions.** Los Angeles becomes "Los Angeles
  (Regional)"; page file and slug stay. LA becomes a two-publisher city, the
  Vancouver + Surrey shape: a dispatching taxonomy, no cross-source dedup
  (the two registries cover disjoint cities).
- **Proved off first** (b27d6ad7): zero drift, baseline 2 figures
  unchanged, peak 0.44 GB.
- **Source:** the City of Long Beach's "Business Licenses Public View"
  (MapsLB), fetched by `pipeline/los_angeles/fetch_long_beach.py` (not a
  step) with the server-side filter LICSTATUS 'Active', OUTSIDECITY 'No',
  HOMEBASED 'No': 20,204 rows, the same as the server's own count. Only the
  listed columns are requested; **`FULLNAME` is never fetched**, and both the
  fetch and step 2 raise if it arrives.
- **Licence: PERMITTED WITH CONDITIONS, nothing required to display**
  (licence-read agent, 2026-10-03, matching staging's read of 2026-09-30):
  the MapsLB Terms of Use grant copying, publishing, adapting and
  redistributing; the bar is any use that "suggests City's endorsement";
  the indemnity is breach-only and was accepted by the owner (2026-09-30).
  The terms page carries no revision date. Recorded in
  `docs/data_sources/united-states.md` (registry row and licence row) and
  as **notice 129**, displayed by choice with a no-endorsement sentence, as
  Seattle's 113 is.
- **Classification:** `pipeline/taxonomies/los_angeles.py` dispatches on
  `source`. LA's rows go through `naics.naics_group()` exactly as before
  (the tooltip now reads "Category: NAICS <code>", the legend plain bucket
  names); Long Beach's 232 `LICCATDESC` values are mapped by a NAICS anchor
  and `docs/category_rules.md`, each with its reason: booth and practitioner
  licences out (232 + 9 + 25, the person-licence rule); cannabis
  dispensaries Retail (Boston, Calgary, Edmonton); estheticians and
  boarding kennels Personal services (Vancouver, Calgary, Edmonton);
  caterers, carts, stands, sidewalk vendors and farmers' markets out (R1,
  mobile units); "General Services - Other" out as the catch-all (R2); a
  dry-cleaning plant Personal services on its NAICS code (no precedent).
  Registered, with its column in `scripts/category_continuity_table.py`
  (51 taxonomies, check OK).
- **What moved** (drift check, every change the extension's): stations
  56 → 64 (the A Line's eight in Long Beach; 46 left out, in 21 other
  cities and unincorporated land); storefronts 57,494 → 60,740 (+3,246,
  all Long Beach: 4,078 in the buckets → 3,264 one per licence → 3,246
  inside the City, 18 placeholder points in the Pacific dropped; Retail
  1,327, Food service 1,160, Personal services 759); in-ring 13,892 →
  14,642 (750 of them Long Beach's), the share 24.2% → 24.1%; LA's own
  rows unchanged.
- **Names:** a Long Beach licence with no trade name (520) shows its street
  address, unit removed, the rule this page already applies to LA's
  registrant-name rows (owner, 2026-10-01). LA's parcel home filter does
  not reach Long Beach's rows; the City's own HOMEBASED flag, applied at
  download, does that job.
- **Privacy: publish.** `check_personal_exposure.py los_angeles`: 0
  person-like names at a residential unit of 14,642 pins; person-like pins
  1,572 (10.7%), all chosen trade names.
- **Macro label** 153.8 px. West of the dot is still the only side with
  PROBLEMS 0 (east, above and below cover or graze San Diego, Tucson or San
  Francisco), but the wider pill is now clipped 43% at 375 px in Global and
  United States: **flagged for the owner at review time**.
- **`data_age`** now names Long Beach's fetch date; table D carries it.
  `record_kind` stays "Tax register" (LA's, 95% of the pins).
- **Regional processed files** in `data/los_angeles/processed/regional/`
  from the start.

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
- **Brief check 8/8**: the OSM refs claim (the colour source) passed on the
  third run, after two Overpass refusals.
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

## For the Visuals session's city cards (Cleanup's rule, "Downstream sessions")

**Notice placement, by each licence's own words on where it must appear.**

| Source added | City | Notice | Card face or caption | The licence's words |
|---|---|---|---|---|
| IBGE CNEFE 2022 (Contagem, Duque de Caxias) | Belo Horizonte (Regional), Rio de Janeiro (Regional) | the existing "IBGE (Brazil)" notice | unchanged: as the city's existing IBGE notice | no new source or notice: the same national file the city already uses |
| City of Long Beach, Business Licenses Public View | Los Angeles (Regional) | 129, displayed by choice | **caption only** | nothing must be displayed; the bar is "any way that suggests City's endorsement of your use", so nothing on the card face may read as the City's (no seal, no "official") |
| City of Burnaby, Business Licences | Vancouver (Regional) | 130 | **caption, travelling with the card** | "where you do any of the above [copy, publish, adapt, distribute]: Acknowledge the source of the Information by including any attribution statement ... and, where possible, provide a link to this licence": a statement must accompany every use, the card included, but no place is named, so the caption suffices; the link where the medium allows |
| City of New Westminster, Business Licenses (Residents) and Address Points | Vancouver (Regional) | 131 | **caption, travelling with the card** | the same OGL clause, word for word; the statement keeps "licenced" and the hyphen |
| City of Coquitlam, Business_Licenses | Vancouver (Regional) | 132 | **caption, travelling with the card** | the same OGL clause; the statement keeps the en dash, with "© City of Coquitlam" beside it |

None of the four new licences names the face of a derived product, so none
requires the card face; each OGL statement must not be dropped from a card
that is shown or shared without the site around it.

**Open terms questions (each keeps its city or extension off public pieces
until the owner rules):**

- **Vancouver (Regional)'s extension (Burnaby, New Westminster, Coquitlam):
  CLOSED (owner, 2026-10-03).** The OGL personal-information exemption is
  read cautiously, which is the build's treatment (8 own-name licences show
  the business type); see the entry above. The three cities may go on
  public pieces.
- **Los Angeles (Regional)'s Long Beach: no open question** (the breach-only
  indemnity was accepted by the owner, 2026-09-30). Los Angeles is already
  held off public visuals for its own terms ruling.
- **Belo Horizonte (Regional) and Rio de Janeiro (Regional): no new
  question** (no new source).

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
7. Los Angeles (Regional), page, The lines: "Only stations inside the City
   of Los Angeles and the City of Long Beach are shown. The lines also serve
   Pasadena, Santa Monica and many other cities, whose businesses come from
   separate city registries."
8. Los Angeles (Regional), page, The businesses (new): "Businesses in the
   City of Los Angeles come from its Office of Finance's list of active
   businesses; those in Long Beach come from the City of Long Beach's
   business licenses, sorted into the same three categories from each
   license's type." and "In Long Beach, a license that gives no trade name
   shows its street address."
9. Notice 129 (City of Long Beach), displayed by choice: "Long Beach business
   licenses: City of Long Beach, Business Licenses Public View (MapsLB), used
   under the City's MapsLB Terms of Use. This map selects, categorizes and
   aggregates the City's records; it is not a City of Long Beach product, and
   the City does not endorse it."
10. What Is Excluded, the new section "Los Angeles (Regional) — Long Beach's
    licenses, and licenses to work in someone else's shop" (its four
    paragraphs, all counts from the 2026-10-03 file).
11. The macro label clip: Los Angeles (Regional) clipped 43% at 375 px in
    Global and United States (no clean side exists).
12. Vancouver (Regional), page, The lines: "This map covers five cities:
    Vancouver, Surrey, Burnaby, New Westminster and Coquitlam. SkyTrain is
    regional, so a Vancouver-only map would cut the network at a line no rider
    recognizes." and "Of 54 stations, 44 are in those five cities: ... The
    other 10, in Richmond and Port Moody, are left out: Richmond's business
    directory may be used only for research and private use, and Port Moody's
    license list carries no addresses. All 10 are listed below."
13. Vancouver (Regional), page, The businesses (new): "Each city's businesses
    come from its own license register. New Westminster's licenses carry no
    map point, so each is placed at its address from the City's own address
    points."; Reading the map: "The five cities are licensed by five
    different authorities, so read them as five measurements that share a
    map rather than one continuous surface."
14. What Is Excluded, the new section "Vancouver (Regional) - Burnaby, New
    Westminster and Coquitlam, three more registers" (all counts from the
    build), and two shared sentences: "Vancouver with four neighbors" and
    "92 pins across Vancouver (Regional) display their business type".
15. Vancouver (Regional), What Is Excluded, "Shown, but not named" (added to
    the paragraph): "The three cities' licenses exclude personal information
    from what they grant, and this map reads that cautiously." **APPROVED**
    by the owner (2026-10-03): relayed by Cleanup ("Sentence approved,
    likely for regional declarations") and confirmed in this session's chat
    ("Confirmed"). It is the template for the same declaration
    on a regional page whose licence exempts personal information; none of
    the other three extensions has one (Long Beach's terms and CNEFE carry no
    such exemption), so no sentence was written from it.
