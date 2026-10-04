# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-04 - The reset wave's calls: a user-agent rule, 31 discards, 11 to R, Konya to D, five open-gap rows, New Zealand back on the map (owner)

- **The owner said yes to each of staging's recommendations**, listed by
  number in chat. Eskişehir's discard could not pass the discard check (its
  portal refuses every visitor, so the city's own host never answered);
  **the owner: "open gap"**, Antalya's shape. The calls:
- **A user-agent rule (all probes and builds):** a host that refuses curl's
  own user agent is a refusal, recorded as one; a browser user-agent string
  is never used to get past it. The project's own identified user agent
  (`brief_check.py`'s, which names the project) is honest and allowed. Five
  repository files send a browser string (`scripts/probe_geodata.py`,
  `scripts/screen_rail.py`, `scripts/rank_canada_storefront_density.py`,
  `pipeline/montreal/fetch_sources.py`, `pipeline/dublin/fetch_sources.py`):
  handed to Cleanup to check whether any of their hosts refuse curl.
- **A token the site's own script sends every visitor** (Palembang's API) is
  not used as evidence: the 637-dataset figure is dropped, and the discard
  rests on the city's two other catalogues.
- **Deleted:** the ARCSA file (7,592,002 bytes, no location below the
  agency's zone, 62% of Quito's rows an individual's name, fetched past a
  curl refusal) and both scratchpad copies of Gaziantep's shopping feed
  (AlisverisNoktalari, 4,957,363 bytes, fetched by the probe and the licence
  read without a brief naming it; ruled out the same day).
- **Gaziantep's question, catalogued and NOT sent (owner: "no emails being
  sent"):** to the published contact, should the owner ever send it: "We
  would like to reuse the 'Ticari Yerler' and 'Yemek Yerleri' datasets from
  the Gaziantep Open Data Platform under the Gaziantep Açık Veri Lisansı.
  Could you tell us whether these points of interest were compiled by the
  Municipality, or come from a third-party (commercial) POI database? The
  licence excludes third-party rights, so we want to be sure the licence
  covers them. Could you also tell us when these datasets were last
  updated?" Gaziantep stays in D.
- **Macau:** one Overpass query of OSM addresses approved, to test placing
  IAM's three food lists (the government GIS points are "All rights
  reserved"). Over 70% placed: C, then B as a food-only page; under it, R.
- **Bands:** Quito from C to R (the city's portals refuse this machine).
  To R: Nonthaburi, Samut Prakan, Shah Alam, Khu Khot (sources inside
  Thailand or Malaysia only), Parañaque and Caloocan (scripts refused
  everywhere), Quezon City (open data behind a sign-in, Almaty's
  precedent), Bursa, Kocaeli, Kayseri (portals geo-blocked to Türkiye).
  Konya to D (a Cloudflare check from outside Türkiye; one visit in the
  owner's browser). Open screening gap: Constantine, Sétif, Ouargla (own
  hosts never answered, no probe inside Algeria; staging's reason: the
  2026-09-24 audit reversed national-pattern rulings), Antalya (portal
  down everywhere) and Eskişehir (portal answers 403 to everyone).
- **Discards:** Parramatta and Newcastle, New South Wales (no register);
  Auckland (rail: suburban lines, 1.4 km median spacing, 15 to 30 minutes
  off-peak; a watch item for the City Rail Link) and Wellington (rail);
  Cuenca (the national file cannot place it); Petaling Jaya, Subang Jaya,
  Kajang, Klang, Ampang Jaya (no council register); Pathum Thani and
  Putrajaya (rail); Oran, Mostaganem, Maracaibo, Alexandria, Lusail (no
  reachable register); Palembang, Bekasi, Bogor, Makati, Pasay,
  Mandaluyong, San Juan (Metro Manila), Antipolo, Marikina, Pasig (no
  register, or rail); Depok (rail, one station); Yerevan (its permit system
  is applications and payments, no holder list); İzmir and Samsun.
- **New Zealand leaves "Countries ruled out":** its ruling ("licensing is not
  municipal") was wrong; food businesses register with their council or
  MPI under the Food Act 2014. Its cities now stand on their own results.
- **Thessaloniki's eight build calls, all as recommended:** canteens out
  (R1); ψιλικά convenience shops kept as food shops (convenience stores are
  food retail everywhere else; bends Antwerp's complementary-retail rule);
  patisseries and bakery coffee food shops; the operator's own line name,
  the Kalamaria branch cut at the city line; gate 3 from Elliniko Metro;
  the OSM city boundary from the build's one Overpass query; headway read
  at build or the gap recorded; the operator's site may be read with the
  project's identified user agent.
- **Not acted on, for the owner:** a public layer in Makati's ArcGIS
  organization carries person-name and birthday fields (field names read
  only). Not this project's data; telling the city would be outreach.

### 2026-10-04 - Gaziantep to Band D: its data's origin is a question for the publisher (owner, conditional)

- **The desk check came back unresolved**, which triggers the owner's
  conditional yes of the same day ("if it settles nothing, D with a
  question to the published contact as the owner's act").
- **Towards a vendor:** the API's 24 OnemliYerler endpoints match 24 of
  Başarsoft's 27 published top-level POI categories, with the same Turkish
  labels, and its tracked-sector list matches the subcategories; a
  navigation-style entry/centre field; rows cover Kilis and Pazarcık
  (Kahramanmaraş) on one interleaved id sequence while three Gaziantep
  districts (İslahiye, Araban, Karkamış) are missing; Ankara ASKİ's
  Başarsoft-built POI layers used the same field set (search-index snapshot
  only). Yandex, HERE, TomTom and NAVTEQ schemes do not match.
- **Towards municipal compilation:** the Ministry's TUCBS Altyapı v2.1
  standard (2022) uses the same subcategory labels, so a municipality could
  compile in this scheme without buying; "Fake" test rows and Turkish QA
  notes show in-house editing; the web-service PDF says the municipal IT
  branch built the services from its own units' data. No tender or
  statement of origin found (EKAP's detailed search needs a login, not
  tried).
- **The owner's act:** ask the published contact whether the POIs were
  compiled by the municipality or come from a licensed vendor base.
  Municipal: back to C on the currency rule. Vendor: a discard on terms
  (the licence excludes third-party rights it cannot grant).
- **One more user-agent note:** this check's early requests also used a
  browser string; every host was re-checked with curl's own agent, and the
  one that timed out (sayistay.gov.tr) is recorded as a refusal, its copy
  deleted and unused.

### 2026-10-04 - Probe slip in the Ecuador fetch: a browser user-agent string past a refusal

- **What happened:** fetching the owner-approved ARCSA file
  (`BASE-DE-DATOS-DE-PERMISOS-DE-FUNCIONAMIENTO-VIGENTES-Y-CANCELADOS-CON-CORTE-15-09-2026.xlsx`,
  7,592,002 bytes, controlsanitario.gob.ec), the host cut off curl's default
  user agent and the agent retried with a browser's user-agent string, which
  the host served. The download was approved; the way past the refusal was
  not, and it sits close to the standing rule against bypassing.
- **What the file holds:** 60,185 current permits, no address, province,
  canton, parish or coordinates (the agency's zone only); 62% of Quito's
  rows carry an individual's tax number, so the business-name field there
  is a person's name. Nothing from it was printed beyond counts.
- **Brought to the owner** with a recommendation to delete it (unusable for
  placement, and personal data). Future briefs and probe prompts say: a
  refusal of curl's user agent is a refusal, never retried as a browser.
- **The same, found in the Thailand and Malaysia probe:** its first requests
  sent a browser user-agent string by default. Once told the rule, it
  re-checked every host it relied on with curl's own agent; all answered
  the same except `pakkretcity.go.th` (Cloudflare 520), now recorded as a
  refusal, and nothing read from it earlier is used.
- **And in the Algeria, Maracaibo, Alexandria and Lusail resume:** some early
  reads used a browser string; `nfsa.gov.eg` and `wilayasetif.dz` refuse
  curl's own agent and are recorded as refusals, nothing read from them
  that way counted as evidence. One retry on `apc-constantine.dz` with
  browser headers was refused anyway.
- **And in the Indonesia and Philippines probe:** browser strings until the
  rule arrived; every source was re-read with plain curl and all answered
  the same.

### 2026-10-04 - Geneva (Regional)'s three build calls, and Thessaloniki's licence reading (owner)

- **Geneva (Regional), "yes to geneva three"**, each on its precedent, for
  the build of `docs/build_briefs/geneva.md` (12 tram communes, 5,885
  establishments after the home-based and itinerant rows are dropped):
  1. **The 1,848 company rows in scope with no establishment row are left
     out, disclosed.** A company row has no premises type, so a home-based
     seat cannot be told from a shop. Tradeoff accepted: a gap about a third
     the size of what is kept, stated on the page.
  2. **Sole traders' names withheld where they read as the registrant's
     own** (1,498 kept rows belong to an "Entreprise individuelle"), as
     Tucson and Kansas City.
  3. **The taxonomy:** Stand ambulant (22) out on R1 and the mobile-units
     row; traiteurs (562100) out on R1 and Georgia's precedent, not France's;
     the 326 storefront-coded rows typed Bureau/étude/cabinet split by code
     at build and brought to the owner as a count.
- **Thessaloniki, "recommended reading sounds good":** the licence read found
  CC BY 4.0 on the layer's own data.gov.gr record (a harvester default
  applied under the City's organization, matching the City portal's default
  and Decision 11654/2026, Art. 8(3)). The map portal's splash ("in no case
  are modification and/or redistribution permitted") is read as the web
  app's terms only, so **the build reads `sdi.thessaloniki.gr/geoserver/wfs`
  only, never the MapServer copy.** Tradeoff accepted: if the City meant the
  splash for all its GIS data, the page comes down on request (the removal
  rule). The layer carries no date, so the page gives the retrieval date and
  never calls the data current or complete. Thessaloniki stays B (food shops
  a partial Retail layer); a brief is next.

### 2026-10-04 - Gaziantep's licence read: catalogued sets only, and one desk check of the data's origin (owner)

- **The licence read** (the Gaziantep Açık Veri Lisansı, Turkish only, no
  licensor named): worldwide, royalty-free, commercial use, publication and
  derived works granted, on condition of a source credit and a link to the
  licence where possible; nothing to do beyond that. It grants no rights in
  personal data, third-party rights or trademarks.
- **The owner: "yes 2 and 3"**, on staging's two recommendations:
  1. **Retail from the two catalogued datasets only**, "Ticari Yerler" and
     "Yemek Yerleri". The shopping endpoint (AlisverisNoktalari, 4.96 MB) is
     in the API's swagger and the web-service PDF but in none of the 252
     catalogued packages, so whether the licence reaches it is unclear.
     Tradeoff accepted: a thinner retail layer.
  2. **One desk check of the data's origin before anything else.** 1,206
     commercial rows lie in other provinces (Kilis, Kahramanmaraş), the
     category codes look like a vendor's and some rows are test rows, so the
     set may be a licensed navigation vendor's POI base, whose rights the open
     licence cannot pass on. The check compares the codes against Turkish
     navigation vendors' published schemas. If it settles nothing, Gaziantep
     moves to D with a question to the published contact as the owner's act
     (outreach last). Gaziantep stays in C meanwhile; the currency rule (no
     date field, catalogue stamp 2025-04-25) is still open.
- **Not a call, for the build:** personal data falls to
  `check_personal_exposure.py` as usual (sole traders' shops named after
  their owners among the hairdressers and barbers), and the `aciklama` field
  is dropped (its test-row notes hold an editor's first name).

### 2026-10-04 - The next probe items after the reset's work (owner)

- **The owner, on the country census's "where new cities could still come
  from": "these would be good next items after our current work
  finishes".** Queued, to start once the reset's ten agents report:
  1. **Inside built countries:** Germany's tram and Stadtbahn cities (about
     55, never asked), Japan's third wave (about 13 cities scoped in wave 2's
     notes), Korea's regional expansions (Busan, Daegu, Seoul, Anyang),
     Switzerland's Bern and Lausanne, Norway's Trondheim, Sweden's Lund, and
     Mexico City's State of México municipios as an extension.
  2. **Sibling cities never asked in probed-but-negative countries:**
     Austria (Linz, Innsbruck), Hungary (Debrecen, Szeged, Miskolc), Croatia
     (Osijek), Slovakia (Košice), Poland's tram cities, Israel's Red Line
     cities, and India's other metros.
- The reset's own work (the paused probes, Southeast Asia, greater Oceania,
  the Macau and Ecuador downloads, two licence reads, three briefs) runs
  first.

### 2026-10-04 - The paused wave's results banded; probes stay stopped (owner)

- **The owner: "1. yes 2. all sound good 3. yes 4. yes 5. yes, do not
  continue probes or other processes though. just republish the master
  list, you can include an ongoing probes section".** Recorded in the master
  list, each as staging recommended:
  1. **Geneva:** the narrow indemnity (SITG CU 7.2) accepted; ge.ch's
     website terms read as the website's only. Geneva stays A. The
     indemnity joins `docs/data_sources.md`'s accepted indemnities at build.
  2. **Thessaloniki to B** (a licence read first); **Macau, Quito and Cuenca
     to C**, with Macau's API download and ARCSA's health-permit file
     (7,592,002 bytes) approved but not fetched (probes stopped);
     **Jerusalem, Almaty, Astana and Ahmedabad to R**.
  3. **Lahore to R; Karachi, Islamabad and Dhaka discarded.**
  4. **Cochabamba, La Paz / El Alto and San Juan discarded; Santa Cruz de la
     Sierra a watch item.**
  5. **Port Louis (Regional) discarded; Gaziantep to C**; Valparaíso / Viña
     del Mar, Concepción, Valencia (Carabobo), Los Teques and Sidi Bel Abbès
     discarded. İzmir waits on its district check.
- **Counts after:** 158 built (the new-cities build's three sit on its
  branch); 25 candidates (A 9 · B 7 · C 6 · D 3); 29 restricted; 155
  discards. The probes stay stopped until the owner resumes them; every
  partial report's resume steps are in the handoff.

### 2026-10-04 - Four never-probed countries screened; the probe wave paused for the builds (owner calls pending)

- **Pakistan:** Lahore's Orange Line passes (26 stations); every host that
  could hold a register (the city corporation, the Punjab portal, the
  business-registration system, the Punjab Food Authority) answers a probe
  from inside Pakistan only and times out or returns 403 elsewhere: **R**,
  Hyderabad's shape. Karachi and Islamabad: **discard on rail** (commuter
  rail and BRT only).
- **Bangladesh:** Dhaka's MRT Line 6 passes (16 stations); no list at any
  level (trade licences behind login portals; data.gov.bd frozen in 2018;
  the food authority's grading PDFs image-only): **discard on absence**,
  Kolkata's shape. RAJUK's token-protected layers are a lead only by
  request.
- **Bolivia:** Cochabamba **discard** (Mi Tren every 15-30 minutes on a
  converted railway; no list at any level); La Paz / El Alto **discard on
  rail** (cable car); Santa Cruz de la Sierra a watch item (its
  metropolitan train's first stage began 2026-09-02). The shortlist's "no
  urban rail" filing gets a correction note, as Algeria's did.
- **Puerto Rico:** San Juan **discard on absence** (Tren Urbano passes, 12
  stations in the city, every 12 minutes off-peak; the only premises data is
  2011-2015 use permits with no category), Honolulu's shape.
- **A probe slip:** the Pakistan and Bangladesh probe downloaded two
  Bangladesh Food Safety Authority PDFs (588 KB and 507 KB) without the
  owner's OK; scratchpad only, no extractable text.
- **The owner: "if we can pause those now at a point where we won't lose
  anything do so, so belgium build can finish".** The two probes still out
  (Mauritius with Armenia, the one-city countries) were told to write what
  they had to their reports and stop; their partial reports sit in the
  staging scratchpad's `probe2\` for a later run to resume.
- **The paused probes' partial results** (both stopped cleanly, reports and
  resume steps written):
  - **Mauritius:** Metro Express passes (22 stations, purpose-built, median
    788 m); licensing is municipal and none of the five councils publishes
    its register (each document library read), the national portal's 856
    datasets hold single-category lists only: **discard on absence**, or R
    if the owner would ask the councils.
  - **Armenia:** Yerevan Metro passes (10 stations, every 7.5 minutes at
    midday); no national portal, the company and licence registers carry
    no business type (pharmacies only). Unread: Yerevan's own alcohol,
    tobacco and catering permit holders, ArmStat's business register, the
    tax service. Pending.
  - **One-city countries:** Valparaíso/Viña, Concepción, Valencia (VE),
    Los Teques and Sidi Bel Abbès proposed **discards on absence**; İzmir a
    discard after a district check; **Gaziantep Band C** (the city's open
    API: 4,937 food and 15,413 commercial points with addresses, 2,562 hair
    and barber; no date field, some rows outside the province; its own
    licence to read; the currency rule is the owner's call). Not reached:
    Maracaibo and Alexandria (hosts unreachable or 503), Oran, Constantine,
    Sétif, Ouargla, Mostaganem, Bursa, Kocaeli, Antalya, Kayseri, Samsun,
    Konya, Eskişehir, Lusail. Merval passes the 15-minute test (every 12
    minutes all day on weekdays).
- All bands and discards above wait on the owner's answer before they enter
  the master list.

### 2026-10-04 - Geneva's REG read, and the second group outside Europe screened (owner calls pending)

- **Geneva's Répertoire des entreprises (REG), `licence-read` 2026-10-04:
  PERMITTED WITH CONDITIONS.** Level A ("Accès libre") under SITG's
  "Conditions d'utilisation des données du Portail SITG" (19 May 2026; the
  copy inside the zip is byte-identical): reproduce, publish, adapt,
  combine, commercially too. Display: "Source : Portail des données SITG
  (État de Genève), téléchargé et/ou extrait en date du […]." verbatim
  (CU 5.3.1), a derived-use statement (5.3.2), a sentence linking the CU
  (5.5); no re-identification (5.4.2); data-protection law applies; no
  resale (RIRT art. 62). **For the owner:** an indemnity (CU 7.2) limited to
  the user's own infringements, personality and data-protection rights
  named (narrower than Hong Kong's accepted one); and ge.ch's website terms,
  applied by SITG's footer to its subdomains, which a strict reading would
  stretch to the download (the read finds the permissive reading much
  stronger). The register is not pre-filtered: 23,164 sole traders among
  63,224 company rows; 2,082 home-based and 3,655 itinerant establishments.
- **The second group outside Europe (probe, 2026-10-04):** Thessaloniki B
  (the city's active-shop-licence layer, 8,103 points, no names; a licence
  read first); Macau C (IAM's licensed food-and-drink list, addresses only;
  one API download for the owner); Quito and Cuenca D on ARCSA's national
  health-permit file (7,592,002 bytes, the owner's download), else Quito R
  and Cuenca a discard; Jerusalem, Almaty, Astana and Ahmedabad R (hosts
  refusing scripts, or the national register behind a sign-in). Pending the
  owner's answer.

### 2026-10-04 - The probe wave's first results: Korea and Europe banded; Korean regional expansions marked (owner)

- **The owner: "approve all"** on staging's recommendations, then "mark the
  potential korean regional expansions":
  - **Korea (SEMAS, cached; gate peak 0.18 GB):** **Gimpo** (Goldline, 9
    stations, every 6 minutes; 13,398 storefronts) and **Siheung** (9
    stations; 15,206) to **A**. Gimpo returns from the owner's earlier
    Gyeonggi scope ("the smaller 시군") on this call. **Yangsan** (Busan
    Line 2, 5 stations) and **Gyeongsan** (Daegu Lines 1 and 2, 5) to **C**:
    a page of its own or a Busan or Daegu regional page. **Gunpo, Hanam,
    Guri, Gwacheon and Gwangmyeong stay out** on the Gyeonggi scope.
  - **Discards (21):** fifteen Korean cities on rail (Pyeongtaek, Osan,
    Yangju, Dongducheon, Cheonan, Asan, Paju, Chuncheon, Gyeonggi-Gwangju,
    Icheon, Yeoju, Ulsan, Gumi, Uiwang, Hwaseong), five with no urban rail
    open (Changwon, Sejong, Cheongju, Pohang, Jeju), and Basel on absence
    (the canton's 364 datasets; its commercial register has no activity
    code).
  - **Geneva to A**: the canton's business register (REG, 100,588 active
    rows, NOGA codes, LV95 points, daily), regional scope leaning, the
    download approved and cached (`data/geneva/raw/`, 11,344,581 bytes,
    sha256 `45aff219...fa3d616`); a licence read of SITG's terms runs.
  - **Timișoara, Iași and Cluj-Napoca to D**: each county's DSVSA site
    answers scripts with a browser check, so the owner saves the
    "Unități înregistrate" lists in their own browser (Bucharest's route).
  - **Norrköping to R** (request only: a public-records request; outreach
    the last resort).
- **Potential Korean regional expansions marked** in the master list's
  add-ons: Busan (Regional) + Yangsan; Daegu (Regional) + Gyeongsan; Seoul
  (Regional) + Gwacheon, Gwangmyeong, Hanam and Guri; Anyang (Regional) +
  Gunpo and Uiwang. Seoul, Busan and Daegu read LOCALDATA, so theirs join
  two sources (`multi-source-city`); Anyang's is a district-code list on
  `korea_sbiz` once the Korea build's code filter lands.
- **Raised with Cleanup:** Namyangju's Gyeongchun line (every 22-24 minutes
  at midday) and Goyang's Gyeongui-Jungang line (2.0 km spacing) fail the
  tests the probe applied to Chuncheon and Paju; recorded calls or defects.

### 2026-10-04 - The "TEC" name on the Charleroi and Liège pages; the never-probed countries' wave (owner)

- **The owner: "recommendation for TEC approved".** Notice 150 credits the
  operator as "LETEC" (the name the Belgian Mobility Company portal and the
  feed's agency use): "Source: LETEC – Open Data – [date of dataset
  update]". Lines are labelled by their public names (M2, M3, M4, T1); no
  "TEC" in legends or prose, and no TEC logo. TEC's website terms (art. 8,
  8.1) claim the name and logo, scoped to letec.be and the app; the
  ruling keeps the pages clear of either reading. Passed to the Belgium
  build session the same night.
- **The never-probed countries (staging's list, 2026-10-04):** Ecuador and
  Kazakhstan (screens running), Bolivia, Puerto Rico, Mauritius, Armenia,
  Pakistan and Bangladesh; rail likely failing in Costa Rica, Kenya, South
  Africa and Senegal; one-city countries with other rail cities never asked:
  Chile, Venezuela, Egypt, Algeria, Türkiye, Israel, Qatar. Russia, Ukraine,
  Belarus and Iran stay left out (owner, 2026-09-28).
- **The owner: "we can run the wave after heavy jobs slow down too, i'm not
  worried about hitting the cap"**: the wave started at once, the heavy-job
  gate holding one 0.2 GB job: one `add-country` probe each for Bolivia with
  Puerto Rico, Mauritius with Armenia, and Pakistan with Bangladesh, and one
  reprobe of the one-city countries' other rail cities.

### 2026-10-04 - TEC's GTFS read: permitted with conditions; the "TEC" name raised

- **`licence-read`, 2026-10-04: PERMITTED WITH CONDITIONS.** The Belgian
  Mobility Company portal's CC BY 4.0 (art. 3, TEC the sole licensor);
  TEC's own transportdata.be entry declares CC0 for the same BMC URL.
  Complying with CC BY 4.0 and art. 4 satisfies either reading, so no
  owner decision on the licence. letec.be answered every path with a
  Cloudflare challenge and was not read past it; its website terms were
  read in the Wayback copy of 2026-05-02.
- **Display (notice 150):** "Source: LETEC – Open Data – [date of dataset
  update]" (the update date, not the fetch date), the modified-data line,
  the CC BY 4.0 title and link, the portal; no TEC logo; no implied
  endorsement. The feed's `route_color` is licensed data (Charleroi uses
  the project's palette anyway, owner).
- **Raised with the owner:** TEC's website terms (art. 8, 8.1) claim the
  "TEC" name and logo. They are scoped to letec.be and the app, and naming
  the operator in a required credit is their stated exception; staging
  recommends crediting "LETEC" and labelling lines by their public names
  (M2, M3, M4, T1), with no "TEC" in legends or prose.

### 2026-10-04 - De Lijn's GTFS read: permitted with conditions

- **`licence-read`, 2026-10-04: PERMITTED WITH CONDITIONS.** On the Belgian
  Mobility Company portal, CC BY 4.0 governs (art. 3, De Lijn the sole
  licensor; nothing states otherwise on its card). De Lijn's own portal
  (data.delijn.be) uses the Flemish Licentie Gratis Hergebruik (2024), and
  transportdata.be lists ODC-BY on all eight De Lijn records: all three are
  attribution-only, none restricts modifying, combining or displaying.
- **Display (notice 149):** "Source: De Lijn – Open Data – [feed date]",
  the modified-data line, the portal, the CC BY 4.0 title and link (which
  also meets the Flemish licence's "bron: De Lijn"); no official status or
  approval implied.
- **delijn.be's website terms** allow private and personal use only and ask
  for the webmaster's say before a link: no delijn.be link or content on a
  page; its line pages may be consulted privately for gate 3.
- **Rail from De Lijn's feed for Antwerp and Ghent stands** (the owner's
  call 2 of the same night, subject to this read).

### 2026-10-03 - Belgium's build calls, and Brussels (Regional) from C to B (owner)

- **The owner: "i say yes to all"**, twelve calls as staging recommended:
  1. **The two fetched feeds ratified**: the owner accepts the Belgian
     Mobility Company portal's terms for De Lijn's and TEC's feeds (the
     same CC BY 4.0 terms approved for STIB); the cached copies stand.
  2. **Rail from De Lijn's feed** (Antwerp, Ghent) **and TEC's** (Charleroi,
     Liège), subject to their `licence-read` passes (running); OSM if either
     comes back restrictive.
  3. **Modes:** Antwerp `tram` (trams in tunnels, Den Haag's precedent),
     Ghent `tram`, Charleroi `light_rail` (Edmonton's and Pittsburgh's
     shape), Liège `tram`.
  4. **No stop thinning in Antwerp** (the trams-only standing call).
  5. **Platform names merged into one station** where the feed has no
     parent station (Antwerp, Ghent) and Liège's one stop with two parent
     ids.
  6. **"Complementary retail" out** (FAVV PL29 with AC95: Antwerp 238,
     Ghent 95 placed).
  7. **Charleroi's M2 drawn to Anderlues**, 13 of 23 stops inside, the 10
     outside listed (Den Haag's tram 1).
  8. **Charleroi's lines in the project's own palette** (M2-M4 share one
     color in TEC's feed; Dijon's precedent).
  9. **Hotels inside LoGIC's HoReCa disclosed, not split.**
  10. **Dot names in Charleroi and Liège: the shop sign** (`ENSEIGNE`), a
      sign read as a person's own name withheld by the privacy check.
  11. **Antwerp's scope includes Borsbeek** (merged 2025-01-01).
  12. **Brussels (Regional) from Band C to B**: Retail and Food service
      full, Personal services off. KBO companies' units in the 18 communes
      outside the City, joined to BeST-Address Brussels (96.8% placed at a
      number, 88.5% exact), filtered by four rules (catch-all-only MAIN
      codes; addresses holding five or more units, fewer than half in a
      bucket; a plain-number box; ten or more MAIN codes with one outside
      the buckets). Against hub.brussels in the City: Retail 78.2%
      precision / 76.1% recall, Food 84.4% / 84.0%, counts 1.09 and 1.22
      times the survey's. After the filter: Retail 9,124 (8,754 placed),
      Food 5,209 (5,007). The page says it uses a different method from the
      City's (registered companies' units, filtered; sole traders excluded;
      about four in five pins confirmed by the survey). It joins the Belgium
      kit as page 201.
- **Coverage inside the rings (Charleroi, Liège):** LoGIC's perimeters
  cover 11% and 16% of the ring area, and 97-100% of the survey's points in
  the rings fall inside them.

### 2026-10-03 - Probe slip in the Flemish and Walloon briefs: two feeds fetched from a portal whose terms count access as acceptance

- **The briefs' agent ran `gtfs_*` checks against De Lijn's and TEC's
  static GTFS** on the Belgian Mobility Company portal, which cached both
  feeds (307 MB) in `data/_brief_check/raw/`. The portal's Terms of Use
  (art. 2) make accessing the data an acceptance of those terms, and the
  owner had approved acceptance for STIB's feed only, at the build's first
  fetch. Nothing was registered and no consent box was ticked; the terms are
  the same CC BY 4.0 portal terms the owner approved for STIB.
- **Raised with the owner the same evening**, with the choice of ratifying
  the acceptance or deleting the cached feeds. Two `licence-read` passes
  (De Lijn, TEC) run on the operators' own terms meanwhile.
- **The lesson:** a brief check that fetches from a click-through portal is
  an acceptance; brief agents are told to skip fetching checks on any source
  whose terms count access as acceptance until the owner approves it.

### 2026-10-03 - Brussels: STIB's GTFS with the owner's acceptance; the page named "Brussels" (owner)

- **STIB-MIVB's static GTFS, `licence-read` 2026-10-03: PERMITTED WITH
  CONDITIONS.** The Belgian Mobility Company portal's Terms of Use (art. 3)
  put every dataset under CC BY 4.0 with each operator the sole licensor;
  art. 4 prescribes "Source: STIB-MIVB – Open Data – [date of dataset
  update]" and recommends a modified-data line, which CC BY 4.0 makes
  mandatory; art. 2 makes access an acceptance (a consent box before the
  download); art. 8 lets the terms change, continued use accepting them;
  anonymous limits 100 requests a day. The FAQ asks for a Belgian Mobility
  Company credit with a portal link: the notice names both. Nothing taken
  from stib-mivb.be itself (its site terms are private use only): no logo,
  network map or brand material.
- **The owner: "recommendation accepted"**, both calls as recommended:
  1. **STIB's GTFS is the rail source**, and the owner approves accepting
     its terms at the build's first fetch; a re-fetch after the terms change
     comes back to the owner. OSM (osm-rail) stays the fallback. All 25
     metro and premetro stations are kept by name (Anneessens, Bourse and
     Lemonnier are tram-served in the premetro).
  2. **The page is named "Brussels"**; its text says it covers the City of
     Brussels, the commune, beside a later Brussels (Regional).

### 2026-10-03 - BeST-Address Brussels read: permitted with conditions; data.gov.be's research request read as not applying (owner)

- **`licence-read`, 2026-10-03: PERMITTED WITH CONDITIONS.** BOSA's DCAT
  record, landing pages, licence PDF and the data.gov.be record all declare
  CC BY 4.0; BeST-in-a-Box's conditions (section 6) make reuse free with a
  source credit under CC BY 4.0, and section 8 defers to the region's
  licence, which for Brussels (Paradigm's own record) is CC0. Display: the
  licensor, the licence title and link, and a statement that business
  addresses were matched to the points; no endorsement, no accuracy claim,
  no Paradigm or datastore.brussels marks. No act owed.
- **The owner: "i agree with recommended reading"** on data.gov.be's
  general terms, which ask the author of research use to send FPS BOSA the
  results: read as not applying. The clause covers data on data.gov.be's
  site, the file came from opendata.bosa.be under its own licence, it is a
  request rather than a condition, and a map is not a study. No message is
  sent (outreach stays the last resort).
- **A build trap recorded:** from 2026-10-11 BOSA's files move from Lambert
  72 to Lambert 2008 (the EPSG:31370 x/y columns become EPSG:3812 x/y, shifts
  up to 20 cm), so a fresh fetch renames the coordinate columns.

### 2026-10-03 - KBO measured: Belgian bands kept; Brussels (Regional) D to C; notice 86's sentence (owner)

- **The KBO full file** (extract 501, snapshot 2026-10-02; fetched by the
  owner under their own account, cached at `data/belgium/raw/`) was measured
  for companies' establishment units in the buckets (`czech_nace2025` plus
  `france_naf`'s laundry and heating-fuel exclusions; "any MAIN code in a
  bucket", food over retail over personal, since 36% of establishments list
  five or more unordered MAIN codes). Brussels-Capital Region 20,992 /
  9,252 / 2,489; City of Brussels 4,477 / 2,765 / 443; Antwerp 8,510 /
  3,596 / 861; Ghent 4,483 / 1,987 / 561; Charleroi 2,462 / 856 / 137; Liège
  2,691 / 1,303 / 179. Sole traders, excluded, are 61-83% of personal
  services. Antwerp and Ghent place 94-96% on VKBO points; elsewhere 99.8%
  of rows carry a full street address.
- **It counts registered establishments, not storefronts:** only 73-74% of
  its food-service units appear on FAVV's list, and in the City of Brussels
  it holds 1.9 times hub.brussels's retail and 1.5 times its food.
- **The owner: "i accept all calls including the download"**, each as
  staging recommended:
  1. **The City of Brussels keeps hub.brussels** (A); KBO is a cross-check.
  2. **Antwerp and Ghent stay B** (food, food shops as a partial); KBO's
     retail and personal layers are not added.
  3. **Charleroi and Liège stay B.**
  4. **Brussels (Regional): D to C.** The account cleared D; what remains is
     a storefront filter measured against hub.brussels inside the City (the
     field survey as the ground truth) and an address join. **The download
     was approved:** BeST-Address Brussels, `openaddress-bebru.zip`
     (17,941,521 bytes, sha256 `f558a29d...df24d76`, dated 2026-09-30,
     stated CC BY 4.0, FPS BOSA), cached at `data/belgium/raw/`; a licence
     read follows.
  5. **Sole traders: each source keeps its own rule.** KBO's licence makes
     natural-person entity data personal data, so its layers take companies
     only; FAVV's list carries no names and its points come from VKBO under
     Flanders' licence, so the FAVV route places every food premises. The
     pages say so.
  6. **Notice 86's sentence approved** as staging drafted it: "Stop and
     station counts on the UK's tram, light-rail and Merseyrail maps are
     checked against NaPTAN, the National Public Transport Access Nodes
     dataset published by the Department for Transport." The licence
     sentence and the no-endorsement sentence are unchanged.

### 2026-10-03 - Liverpool (Regional) on the metro mode; notice 86 reworded for Merseyrail (owner)

- **The owner: "1. metro 2. reword".** Liverpool (Regional)'s map mode is
  `metro`. The Department for Transport, NaPTAN notice 86 is reworded to
  cover Merseyrail rather than a new notice added; its current text names
  "the UK's tram and light-rail maps". The new sentence is drafted in chat
  for the owner's approval before the build writes it (a rendered string,
  in `app/components.py` and `docs/data_sources.md`).

### 2026-10-03 - Mendoza's Metrotranvía drawn to its end (owner)

- **The owner: "yes draw mendoza line to end".** The whole line, Gutiérrez
  (Maipú) to Avellaneda (Las Heras), is drawn; the 7 stations in the capital
  are counted and the 18 outside it are listed on the page as out of scope
  (Florence's T1, Göteborg's 4 and 12, and the Brazilian regional lines'
  precedent). Recorded in `docs/build_briefs/mendoza.md`.

### 2026-10-03 - Three build sessions for the twelve candidates (owner)

- **The owner: "eventual sessions: one korean, one belgium, one for the
  other cities".** Staging writes one kit per session once the briefs pass:
  - **Korea:** Daejeon, Gwangju, Gimhae (SEMAS, Incheon's module).
  - **Belgium:** the City of Brussels, Antwerp, Ghent, Charleroi, Liège, and
    Brussels (Regional) now that the owner holds the KBO file; their bands
    wait on the KBO measurement.
  - **The other cities:** Mendoza, Tacoma, Liverpool (Regional).
- Each kit claims its own page and notice numbers from the next free ones
  (`docs/session_roles.md`'s claims sentence; notices from 141).

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
