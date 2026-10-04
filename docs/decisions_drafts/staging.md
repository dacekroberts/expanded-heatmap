# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - Seven licence reads for the sweep's first group; Brussels and Tacoma to A (owner)

- **The owner: "license readings look good"**, on staging's four
  recommendations, and "update the master list". One `licence-read` agent
  per source, all 2026-10-03:
  - **hub.brussels's inventory (City of Brussels): permitted with
    conditions**, CC BY 4.0 (the portal adopts the producer's licence). The
    "Google Maps" contributor credit sits on 79 portal datasets and matches
    two link columns built from each record's own point; 21 of 24
    comparable points lie within 0.03-0.35 m of UrbIS address points (CC0),
    and hub.brussels describes the inventory as its field agents' own. The
    publisher never states what the credit covers. **The City to Band A**:
    the build drops `google_maps` and `google_street_view`, never links a pin
    to Google, and names the publisher's listed contributors in the credit.
    No City logo or "BXL" mark (portal terms 3.1).
  - **Tacoma's business licences: permitted with conditions.** Resolution
    39378 (2016) and the City's open-data page: no restrictions on reuse.
    The disclaimer (115 words, text kept in the staging scratchpad) must be
    displayed site-wide, and the City may require any use to end for any
    reason: Chicago's template, without Chicago's indemnity or IP
    reservation. **Tacoma from C to A.** The licenseInfo link's host
    (data.cityoftacoma.org) is dead; cite data.tacoma.gov. The pins are
    "active business license accounts", never "currently licensed".
  - **FAVV's operator list: permitted with conditions**, CC BY 4.0, credit
    with the extract date, no implied endorsement, nothing misleading. The
    file has no name or street column. **FAVV is credited through its home
    page** (a deep link asks for the webmaster's say first), and the site
    terms' "prior approval for downloadable documents" is read as the Dutch
    text limits it, to brochures and the like (owner). The site terms are
    non-commercial only, no conflict for this project.
  - **VKBO: permitted with conditions**, Flanders' Modellicentie gratis
    hergebruik v1.0, its prescribed Dutch credit line; KBO's purpose limit
    binds registrants only and does not carry over. The build adds the
    extract date to the credit, which also meets KBO 2.8 if the federal
    terms ever reached the KBO-derived fields.
  - **LoGIC 2024: permitted with conditions** for the downloaded GeoPackage
    (CC BY 4.0, the prescribed SPW citation verbatim, a statement of
    modifications). The MapServer brings in SPW's services terms (art. 5 §4,
    no altering): the build uses the download only. The citation's
    geodata.wallonie.be URI answers 404; link the catalogue page beside it.
  - **Mendoza: permitted with conditions**, CC BY 4.0 at every level; credit,
    licence link, a modification statement, no endorsement. Ley 25.326 is
    outside the licence: the name rule and the privacy check apply.
  - **KBO/BCE Open Data: permitted with conditions** for companies'
    establishment units; acts for the owner if registering: the declared
    purpose (2.3), the registration e-mail watched for term changes (9.1,
    15 days), a download at least yearly (10.5); the project is the GDPR
    controller (2.1). **Companies' establishments only** if the owner
    registers (sole traders' establishment addresses are personal data).
- **A lesson from the run:** several agents shared the one built-in browser
  pane and navigated it under each other, and two KBO PDFs and a catalogue
  PDF were saved to the main checkout's root by browser downloads (moved to
  the staging scratchpad). One browser-using agent at a time.

### 2026-10-03 - The sweep's first group banded: eleven cities on the owner's approval

- **The owner: "i approve"**, every move as staging recommended:
  - **Daejeon, Gwangju, Gimhae: Band R to A.** SEMAS's cached national file
    (2026-06-30 edition, the built Korean cities' terms): Daejeon 50,939
    storefronts (food 23,402, retail 20,100, personal 7,437), Gwangju 47,214
    (20,701 / 18,706 / 7,807; district codes 12210, 12240, 12270, 12300,
    12330 after the 2026 merger into 전남광주통합특별시, so the build keys on
    codes, never names), Gimhae 17,879 (8,558 / 6,662 / 2,659); every row
    placed. Rail: Daejeon Line 1, 22 stations, every 10 minutes at midday;
    Gwangju Line 1, 20 stations, every 10 off-peak (Line 2 not open, phase 1
    reported for 2028-12); Busan-Gimhae LRT, 12 stations in Gimhae, every
    5-6 minutes all day, elevated track, median spacing 729 m. **Gimhae is
    its own page** (the Gyeonggi satellites' precedent; a Busan regional map
    would change a live page).
  - **Liverpool (Regional): Band B, food only** (the UK six's scope),
    Liverpool, Sefton, Knowsley and Wirral: FSA storefronts 3,451 / 1,682 /
    517 / 1,750; Merseyrail 59 stations. **Merseyrail is a commuter-rail
    exception**: every branch every 15 minutes by day Monday to Saturday,
    the trunks every 2-6, against the written "by day" test; evenings and
    Sundays every 30 minutes. The City Line (3 trains an hour, uneven) is
    named on the page as not drawn.
  - **City of Brussels: Band A once its licence read passes.** hub.brussels's
    inventory: 6,880 rows, all placed in the commune, dated 2025-10-17; food
    1,908, retail 2,459, personal 508; 1,068 vacant dropped. Its metadata
    credits Google Maps: the licence read decides whether the points stand;
    the fallback, an address join to the Brussels address register, is a new
    source for the owner. 25 metro and premetro stations; trams drawn and
    thinned (Amsterdam's and Oslo's precedent).
  - **Antwerp and Ghent: Band B**, food service from FAVV's operator list
    joined to Flanders' VKBO points: Antwerp 3,100 of 3,231 placed (95.9%),
    Ghent 1,810 of 1,905 (95.0%); food shops as a Retail partial
    (Göteborg's precedent), 1,764 and 932. Caterers out by the category
    rules (Coquitlam's precedent).
  - **Charleroi and Liège: Band B with the gap disclosed.** Wallonia's LoGIC
    2024 survey has four classes only, so no personal services: Charleroi
    retail 980 and horeca 450, Liège 1,477 and 868. Its horeca is 53% and
    68% of FAVV's registered food service by postcode, because the survey
    covers commercial perimeters only; unlike Wakayama's opt-in list (51%,
    discarded) the gap is structural. The build measures coverage inside the
    station rings first.
  - **Tacoma: Band C** until its licence read.
  - **Mendoza: Band A** (the owner's earlier call).
- **Belgium leaves "Countries ruled out"**: the Brussels inventory confirms
  the condition the owner set. The Brussels-Capital Region beyond the City
  is Band D: KBO's free Open Data account, the owner's act. The owner asked
  for the sign-up link the same evening; staging runs a licence read of
  KBO's terms alongside the other new sources.

### 2026-10-03 - Mendoza's placement measured: every business has a point; Band A

- **The owner approved the download** ("1 yes"): `comercios_limpio.json`,
  12,239,392 bytes, sha256 `ca6af57c...707fd17`, cached at
  `data/mendoza/raw/comercios_limpio.json` (gitignored).
- **Measured (gate peak 0.01 GB):** 41,179 activity rows, 8,309 distinct
  `comercio_id` (the CSV's count; at most 30 activity rows per business).
  Fields: `comercio_id`, `nombre_fantasia`, `calle`, `numero`,
  `tipo_actividad`, `desc_full`, `fecha_inicio`, `x`, `y`. **Every business
  has a nonzero x/y (8,309, 100%)**; read as Gauss-Krüger zone 2 (EPSG:5344
  and 22182 agree within 0.0001 degrees), the median falls at the city
  centre and all 8,309 sit inside a rough box around the capital. The build
  checks against the department's own boundary.
- **Mendoza to Band A** on the owner's call of the same evening (the capital
  alone, seven stations). The JSON is the build's source: it carries the
  points and the activity rows together.
- **Privacy flag for the brief:** `nombre_fantasia` holds a sole trader's own
  name in the surname-comma-forename form on some rows, so the build's
  privacy check and a name rule (Vancouver's, 2026-09-21) apply.
- **Probe slip:** reading the file's first 200 bytes to confirm its shape
  printed one row to the console, and that row's trade name is a person's
  name. Nothing was written to a file or a doc. The rule (never print a row
  from a register that names people) holds; the next read of a new file
  prints field names only.

### 2026-10-03 - Mendoza approved for a build: the capital alone, seven stations (owner)

- **The owner: "mendoza can be built"**, answering whether a seven-station
  map is worth building. The Metrotranvía has 25 stations; 7 are in the
  Ciudad de Mendoza (capital department), about 8 in Godoy Cruz, 5 in Las
  Heras and 5 in Maipú. Every 7 minutes at peak and 11-12 off-peak, on a
  converted railway with stops about 700 m apart: it passes the light-rail
  test, so it is not a tram question.
- **Scope: the capital alone.** No neighbouring department publishes a
  business register (Godoy Cruz publishes monthly totals only).
- **The business leg:** "Listado Comercios por Actividad 2025", 8,309
  businesses (41,179 activity rows), all active as of June 2025, CC BY 4.0.
  First mapping at the business-type level: Retail 3,350, Food 721, Personal
  services 331; catch-alls 601 (mostly offices); 3,155 out of scope.
- **Open:** placement. The CSV has no coordinates; `comercios_limpio.json`
  (12,239,392 bytes) carries x/y in Argentina's zone-2 grid (POSGAR), fill
  rate unmeasured. Mendoza goes to Band A when placement measures.

### 2026-10-03 - Probe slip in the Mendoza screen: a whole file arrived from a 4 KB request

- **The screen asked Mendoza's open-data host for the first 4 KB** of the
  capital's "Listado Comercios por Actividad 2025" CSV, to read its header.
  The server ignored the Range header and sent the whole file (7.9 MB). No
  download beyond the two Belgian files had been approved.
- **Where it sits:** the staging scratchpad only, never `data/` or the
  repository. The screen's Mendoza counts (8,309 businesses, all active as
  of June 2025) come from it. Raised with the owner the same evening, and
  **deleted on the owner's yes** once the approved JSON had reproduced the
  count (8,309 distinct `comercio_id`).
- **The lesson:** a Range request is not a header read; a server may ignore
  it. Read the schema from the catalogue's metadata or a records API, or
  stop the transfer by byte count in the script.

### 2026-10-03 - The sweep's first group screened, two Belgian downloads, Belgium off the ruled-out list (owner)

- **The owner: "all three approved"**, the three calls staging put after the
  coverage sweep, each as recommended:
  1. **Step 0 screens for the first group**: Daejeon, Gwangju and Gimhae
     (Band R on a stale reason: SEMAS's keyless national file, cached since
     2026-09-29, holds Daejeon 80,704 rows and Gimhae 26,700; Gwangju sits in
     the merged member 전남광주통합특별시), Liverpool (never recorded; the
     FSA steps carry over, Merseyrail meets the commuter-rail test or not),
     the City of Brussels (hub.brussels's shop inventory, 6,880 points, CC BY
     4.0), Mendoza and Tacoma.
  2. **Two downloads approved**: the FAVV operator list
     (`inter_actieve_actoren_EN.csv`, 87.9 MB, static.favv.be), to measure
     its join to Flanders' VKBO for Antwerp and Ghent; and Wallonia's
     `LOGIC_2024_GEOPACKAGE_3812.zip` (3.2 MB, geoservices.wallonie.be), for
     Charleroi and Liège.
  3. **Belgium leaves "Countries ruled out"** once the Brussels screen
     confirms the inventory. The ruling ("bulk access paid") rested on one
     national method and is out of date: KBO/BCE's open data file is free
     behind a free account (a Band D act for the owner), and only the Public
     Search web service is paid.
- **Not approved by this**: registering any account, including KBO's; a
  download the screens find beyond the two named goes to the owner first.

### 2026-10-03 - A coverage sweep before any new screen, Belgium's cities first (owner)

- **The owner: "yes start"**, on staging's recommendation, with the
  candidate list about to empty when Japan wave 2 lands (158 built, 0
  candidates).
- **Why a sweep first:** a spot check of about 60 cities with rail against
  the list found two kinds of hole. **Belgium is ruled out on one national
  method** (KBO/BCE bulk access is paid), the shape the 2026-09-24 audit
  reversed for eight countries; Brussels, Antwerp, Ghent and Charleroi were
  never screened at city level. **Six rail cities appear nowhere** in the
  list, its evidence file or the country shortlist: Jerusalem, İzmir, Quito,
  Almaty, Yerevan and Košice.
- **The sweep:** agents compare the world's metro, light-rail and tram
  systems against every row (built, Band R, discards, countries ruled out,
  the commuter-rail group), by region, and Belgium's cities get a Step 0
  read of their own catalogues. Catalogue and dataset-page reads only; a
  bulk file goes to the owner first. A city the sweep finds is screened
  normally afterwards.
- **Ranked below it, not started:** a third Japanese wave, the commuter-rail
  group (staging's lean: keep the rule) and Band R re-checks.
