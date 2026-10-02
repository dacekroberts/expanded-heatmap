# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Twelve Japanese briefs written; the owner's calls on Matsuyama, Okayama, Sakai, Hakodate and Nagasaki (owner)

- **The owner: "start the japan briefs, 12 as one batch okay".** There are
  four agents with three cities each, every one writing only its own brief
  files. None queried Overpass, edited shared code or committed. All 12
  briefs are in `docs/build_briefs/`. Staging re-ran every check: 122 of 122
  claims hold (http, CKAN and UTM only).
- **The owner's calls ("approve all recommendations", then "nagasaki b,
  download ok"):**
  - **Matsuyama:** MHLW is a second source. Its own points go where the
    block join misses (81.9% to 92.7%), and its notifications become a
    partial food-retail bucket, disclosed (Fukuoka and Hiroshima).
  - **Okayama:** with MHLW as its only source, the name rule cannot run. The
    precedent extends: Hiroshima's MHLW bullet covers the whole page.
  - **Sakai:**
    - The Midōsuji Line is drawn cut at the city line (3 stations, not 2).
    - The monthly new and closure files are covered by the page's
      open-data notice (Hiroshima's precedent).
  - **Hakodate:** the e-Stat download was approved. The FY2024 counts total
    1,122 against the excerpt's 1,100 (98.0%), so 抜粋 means columns, not
    rows.
  - **Nagasaki: (b)**, the 2023 BODIK snapshot plus MHLW's current filings
    (Tokyo's precedent). One agent downloaded the city's current list, which
    needs the city's permission, to measure it only. The owner approved that
    after the fact. It is not a source.
- **Master-list corrections from the briefs (2026-10-02):**
  - Matsuyama's and Nagasaki's coordinate columns are empty.
  - Nagasaki's lists date from 2023-06-30 and 2023-03-31; 2025-03 is the
    upload. Its tram has 38 stops.
  - Kōchi has 1,415 premises (barbers 321 were missing).
  - Toyama's tram has 39 stops with the Port line.
  - Fukui's Fukubu Line has 15 stations in the city.
  - Sakai has 15 Hankai stops.
  - No band changes.
- **Build-time shared-code items, listed in each brief:**
  - column spellings for `japan_register` (address, name, operator);
  - Sakai's 1丁 rule;
  - Fukui's 飲食店 / 喫茶店 old-law types (93 rows);
  - Kagoshima and Fukui on the 2025 N02 edition.

  Each is followed by the Minato control.
- **Slips, logged as before:** two agents printed register rows to their
  consoles. One showed a shop name and address, plus two operator names; the
  other showed an operator's own name and phone number. Nothing reached a
  file. Separately, N03 boundary zips (the skill's own source) were saved
  under each city's `data/<slug>/raw/`.
- **Open with the owner:**
  - Toyama's and Fukui's lists name only company operators, so the name rule
    tests almost nothing. Staging recommends accepting it, as for MHLW's
    rows.
  - Each city's `mode`. Staging recommends Dublin's precedent (commuter rail
    drawn beside trams does not make a city metro): tram for nine,
    light_rail for Utsunomiya and Kitakyushu, metro for Sakai (the
    Midōsuji).

### 2026-10-02 - The UK six released to one build session with agents; the UK takes the minor label tier (owner)

- **The owner released the builds:** "send off the uk six to either two
  separate sessions to build or one session using multiple agents",
  leaving the choice to staging ("whichever you think is more efficient").
- **Staging's choice: one lead session, with agents for five cities.**
  - Manchester pilots the shared code, so a second session would wait on
    the first.
  - All six write the same shared files: `cities.py`, the notices, What Is
    Excluded, the macro facts and the labels. A single integrator avoids
    merging the same lines five times.
  - Agents own only their city's files, never query Overpass (they share the
    session's one slot) and never commit. The lead integrates in build
    order.
- **The owner:** "implement the high-density cluster rule to UK, like
  Japan, France, Czechia".
  - The UK gets a region of its own, and every UK city moves into it.
  - The six (all tram or light rail) carry `label_tier: "minor"`, on
    France's line between metro and the rest.
  - London, Glasgow and Newcastle stay eligible.
  - `REGION_LABELS_ALSO["Europe"]` gains the region.
  - The region shape is decided by `check_macro_labels.py`.
  - Japan takes the same rule when its batch is built ("japan coming up,
    not currently implemented").
- **Set up:**
  - the worktree `.claude/worktrees/uk-six` on `uk-six-build`, with the
    `data/` and `.venv-lean` junctions;
  - a row in `docs/session_roles.md`;
  - the kit's new sections;
  - the session prompt, given in chat.

### 2026-10-02 - The UK six's prose hold lifted: page text to the new format (owner, via Cleanup)

- **The owner asked staging to message Cleanup about the new prose
  guidelines.** Cleanup confirmed that nothing pending keeps the hold. The
  builds stay held until the owner releases them.
- **The kit's prose hold is replaced** by a "Page text" section
  (`docs/handoff_uk_six_2026-10-01.md`). Each of the six briefs' banners and
  final bullets is replaced the same way. The pointers:
  - `docs/city_page_format.md`;
  - `add-city` step 8, then `scaffold-city`, `publish-city` (step 5a),
    `premises-taxonomy` step 8 and `read-licence` step 9;
  - `scaffold_city.py`'s template, which is the new format and is run for
    real.
- **Cleanup's corrections to the old hold:**
  - London's, Glasgow's and Newcastle's converted bullets are now the
    approved FSA and FHIS wording.
  - A city-specific sentence is a proposal, and does not stop the build.
  - The template pre-permission applies again.
  - What Is Excluded has a section per city, with its stations "listed on
    <City>'s page".
  - The OGL title, the FSA's and FHIS's business-type names and line and
    station names stay as published.
- **The Japan batch's minor-tier bullet stays where it is** (Cleanup, after
  its rework).
- **For the record (Cleanup):** city pages' maps are now centered on wide
  screens (`components.py`, 33f2a379, owner; rebooted and checked live).
  The builds have nothing to do; `render_city_title` applies it.

### 2026-10-02 - Takaoka's licence is CC BY 4.0, but its food list can no longer be reached; to Band R (owner)

- **The owner asked for a faster re-check by new methods** after the agent
  stalled ("go ahead with the takaoka"). It was run in the main session,
  with sites and executes permitted.
- **Licence: PERMITTED WITH CONDITIONS, CC BY 4.0.**
  - The old portal's dataset page (`opendata.pref.toyama.jp/dataset/syokuhin`,
    Wayback Machine 2026-05-21) gives the licence as 「クリエイティブ・コモンズ
    表示」. The creator is 生活衛生課, the list was last updated 2026-03-02,
    and the frequency is given as 月単位.
  - The portal's terms (Wayback Machine 2026-03-16) apply CC BY 4.0 to all
    content. The exceptions are logos and content marked with other rules,
    and the food list carries no such mark. The 出典 example is
    「出典：[データタイトル]富山県ホームページ（当該ページのURL）」, with
    「を加工して作成」 added for edited data.
  - The new platform's public front page (`ckan-front.tdcp.pref.toyama.jp`)
    says all its data is under CC BY 4.0, with credit.
  - The first screen's API read (2026-09-30) recorded `cc-by` on the
    barber, beauty-salon and laundry lists too.
  - The archive was read only because the old portal was retired: its host
    no longer resolves. Archived copies of the blocked platform were not
    looked for.
- **Access is the blocker now.**
  - The 2026-03-01 CSV on `toyama-pref.box.com` answers 404. It was read on
    2026-09-30.
  - The new platform's catalogue (`ckan.tdcp.pref.toyama.jp`) answers 403 to
    the built-in browser as well as to the fetchers, while its front page
    answers 200. The likeliest cause is a block on access from outside Japan.
    It was not worked around.
  - The national catalogue has ministry data only. A search found no other
    public link to the list.
- **Staging's recommendation is R, by the Kraków, Brescia, Catania and
  Alicante precedent** (portals that refuse the built-in browser). It would
  reopen when the platform answers or the prefecture publishes a public link.
- **Owner: "yes move takaoka to R"** (2026-10-02). The list holds
  A 7 · B 12 · C 1 · D 0 · R 24 = 44 candidates, with 121 discards.

### 2026-10-02 - The Japan batch goes to the minor label tier, as France and Czechia did (owner)

- **The owner:** "for this new batch of japanese cities, carry over an item
  to eventual build session that these need to be implemented like france
  and czechia where the smallest cities lose their macro-view pills to
  reduce clutter".
- **The batch:**
  - Band A's seven: Matsuyama, Toyama, Kumamoto, Fukui, Nagasaki,
    Utsunomiya, Kitakyushu.
  - Band B's five: Sakai, Hakodate, Kagoshima, Okayama, Kōchi.
  - Takaoka, if it leaves R.
  - Each carries `label_tier: "minor"`. The eight built Japanese cities stay
    eligible.
- **The precedent is the whole France and Czechia mechanism, not the tag
  alone.** The tag removes a pill only outside the city's own region, and
  every Japanese city is tagged East Asia today. So:
  - a Japan sub-region, one or split, measured by `check_macro_labels.py`;
  - every Japanese city moved into it, as Prague moved with Czechia;
  - `REGION_LABELS_ALSO["East Asia"]` gains it, so the anchors keep their
    pills there (Seoul's case).
- **Recorded for the build session** in the `japan-city` skill's standing
  calls and in the master list's "Before building". Nothing in `app/`
  changes now: it lands with the batch's first city at review time.

### 2026-10-01 - Brisbane to the discards on rail; a commuter-rail revisit group of twelve (owner)

- **The owner: "stays in discard, create commuter rail discard group to
  revisit (considering they are fully buildable)".**
- **Brisbane's only rail is Citytrain.**
  - **Spacing passes:** 83 stations in the city, median gap 1,012 m.
  - **Frequency fails:** 30 minutes off-peak on every line under the 2026
    reduced timetable. The normal one is at best 15 minutes, on five trunk
    sections, weekdays 7am–7pm.
- **The owner asked whether Buffalo's precedent applies. It does not.**
  - Buffalo's slower timetable was disclosed because its track is
    purpose-built.
  - On railway track the frequency gate holds: Aarhus L1, and Sheffield's
    Tram-Train the same week.
  - Commuter rail must also run at metro frequency to be drawn.
- **Brisbane's discard row:** kind `rail`, reopening when Cross River Rail
  opens (2029). The Council's food permits (8,050, CC BY 4.0) are recorded
  on it.
- **New section, "Commuter-rail revisit group"**, after the discard table
  (a view, not a band). It holds twelve discards whose only blocker is
  commuter or suburban rail and whose business leg is buildable:
  - Brisbane;
  - Tainan and Hsinchu (TRA locals);
  - Austin (the Red Line) and Fort Worth (TEXRail), both on the
    Comptroller file;
  - Cork (Luas Cork pending);
  - Teresina, Maceió, João Pessoa and Natal (CBTU suburban);
  - Sobral and Juazeiro do Norte / Crato (diesel VLTs on railway).
- **Left out of the group, because their blocker is not commuter rail:**
  - Cincinnati (a streetcar, food only);
  - Brampton and Bologna (lines not yet open);
  - the guided buses (Clermont-Ferrand, Padua, Venice-Mestre);
  - the one-to-three-station cases (Longueuil, Brossard, Vaughan,
    Berkeley, Saint-Louis);
  - Trondheim and Aubagne (reach and size);
  - Bogotá (BRT);
  - Jaén (no register).
- **The list now holds A 7 · B 12 · C 2 · D 0 · R 23 = 44 candidates, with
  121 discards.** The count, evidence, self-test and provenance checks pass.

### 2026-10-01 - Tempe to the discards: its licence list has no address (owner)

- **The owner: "save evidence, delete root, discard".**
- **The evidence is saved** at
  `data/tempe/raw/Tempe_General_Business_License_List_2026-09-03.pdf`
  (gitignored, so local and never committed). It is byte-identical to the
  owner's browser download.
- **The owner's root copy is deleted** (`expanded-heatmap/tempe.pdf`, at
  the main checkout's root).
- **Tempe moves from Band D to the discards**, a `measured` row. The list
  carries licence number, business name, business activity and website,
  and no address, so nothing can be placed. The City's ArcGIS app covers
  short-term rentals and tobacco only. It would reopen with a list that has
  premises addresses.
- **Band D is empty.** The list now holds **A 7 · B 12 · C 3 · D 0 · R 23 =
  45 candidates, with 120 discards.** The count, discard-evidence and
  self-test checks pass.

### 2026-10-01 - Fukui takes the CC BY-SA 4.0 offer (owner); Tempe's licence list has no address

- **Fukui (owner: "use the SA 4.0").** The current lists are used: food,
  2026-08, with closures; and 理容/美容/クリーニング. The site default is
  CC BY-SA.
- **What the Fukui build owes:**
  - **The share-alike offer itself:** a line in `LICENSE` and in the
    data-sources entry, offering `outputs/fukui/` (the map and any derived
    Fukui data) under CC BY-SA 4.0. It is the project's first share-alike
    licence on its own output.
  - **The credit:** 福井市, the list titles and page URLs, CC BY-SA (with no
    version claimed for the city's licence), and a statement that the data
    was processed.
  - **What never appears:** no endorsement, no claim of accuracy on the
    city's authority.
  - **The site policy's open-ended prohibited acts (§4) are accepted
    knowingly**, Taoyuan's pattern.
  - **Privacy:** `check_personal_exposure.py` covers the policy's privacy
    clause (6).
- **Tempe's General Business License List was read.**
  - The owner fetched it in their browser (`tempe.pdf`, at the main
    checkout's root). Staging copied it to its scratchpad.
  - It is a 33-page PDF, as of 2026-09-03, with four columns: licence
    number, business name, business activity and website. **There is no
    address**, so nothing can be placed (Denver's original failure).
  - The City's ArcGIS app covers short-term rentals and tobacco only.
  - **Staging recommends the discards on a measured negative**, the owner
    to confirm. The row stays in Band D until then.

### 2026-10-01 - Seattle regional: the Liquor Board's off-premise licences become a partial retail layer (owner)

- **The owner said "yes"** to staging's recommendation.
- **The layer:** the active off-premise rows (grocery stores, spirits
  retailers, beer/wine and wine shops) become a partial retail layer in
  every city outside Seattle and Bellevue. They are disclosed as shops
  licensed to sell alcohol only (Zurich's precedent).
- **On premise** is a check on the Snohomish food layer, not a layer.
- **Recorded in `docs/build_briefs/seattle.md`**, "What the build has to
  pull", items 4–7.

### 2026-10-01 - Seattle regional: the 2025 Snohomish layer approved for Lynnwood and Mountlake Terrace food (owner, 4a); the Liquor Board lists screened (4b)

- **4a approved (owner: "use").** Lynnwood's and Mountlake Terrace's food
  comes from Snohomish County's "Food Service Establishments (2025)" layer
  (598 and 92 points), under the currency rule's "a frozen part may sit
  beside a current whole, its date on the page" (Tokyo's precedent).
  Conditional on two build-time checks:
  - **It is a complete snapshot.** Check it against the county's published
    count of permitted establishments, and against the Liquor Board's
    on-premise rows (Lynnwood 113, Mountlake Terrace 24).
  - **Its date comes from more than the catalogue's "(2025)" label.**

  If it proves partial, those stations are drawn hollow.
- **4b probing (owner: "ok to fetch and screen")**: the Washington Liquor
  and Cannabis Board's Off Premise and On Premise lists, dated 2026-09-29,
  1.5 and 1.9 MB, kept in the staging scratchpad.
  - **Off premise:** 8,793 rows statewide (7,791 active), mostly grocery
    stores (beer/wine), spirits retailers, beer/wine specialty shops and
    wine resellers.
  - **On premise:** 9,993 rows (9,511 active), mostly restaurants, lounges,
    taverns and nightclubs.
  - **Both** carry status, expiry, a premises address and city (no
    coordinates), plus `Licensee`, phone and mailing columns that are never
    published.
  - **Terms:** the page says records "may not be used for commercial
    purposes" (RCW 42.56.070(8)), which the owner's non-commercial
    confirmation meets. A formal licence read is owed at build.
- **The finding: a partial retail layer exists in every suburb**: shops
  licensed to sell alcohol, in both counties (Lynnwood 133, Kent 134,
  Federal Way 106, Shoreline 66, Redmond 64, Tukwila 48, SeaTac 40,
  Mountlake Terrace 25, Des Moines 24, Mercer Island 16, all statuses).
  That is Zurich's precedent: alcohol-licensed shops as a partial layer
  beside a full food register, disclosed.
- **Staging recommends** adding the active off-premise rows as that partial
  layer, and using on-premise only as a check on the Snohomish layer.
  **The owner's call is pending.**
- **Personal services remain unpublished outside Seattle and Bellevue**,
  disclosed per city (4b).

### 2026-10-01 - Five licence reads: Seattle and Geostat permitted; Bellevue and King County ambiguous and read as permitted (owner, option 1); Fukui's share-alike to the owner

- **Seattle's business register: PERMITTED WITH CONDITIONS.**
  - The layer is federated on data.seattle.gov (`wmtg-dzy4`). Its Open Data
    Terms of Use ("by using data made available through this site the user
    agrees…") and Open Data Policy V1.0 support reuse.
  - No attribution is required, and nothing is owed.
  - The condition: data configurable as "a list of individuals" may not be
    used "for a commercial purpose". The owner confirmed the project is
    non-commercial ("no commercial, nothing sold", 2026-10-01), and it must
    stay so.
- **Bellevue's licences (all): ambiguous.**
  - The data's licence field bars only commercial use or sale without
    written authorization.
  - The portal's linked Terms of Use allow only "own personal,
    non-commercial use", with all other rights reserved.
- **King County food inspections: ambiguous.**
  - The Socrata dataset is declared Public Domain. The portal's own data
    terms granted reuse, but they are now a 404 (last archived 2023).
  - The live site-wide terms forbid publishing without written permission.
- **The owner chose option 1 for both, "defensible": read as permitted.**
  - The data's own declarations govern.
  - King County: display "Public Health – Seattle & King County" and the
    legend "Data provided by permission of King County"; no marks, no
    implied endorsement; no USPS-derived fields (`CTYNAME`,
    `POSTALCTYNAME`, ZIP+4) from the address points.
  - Bellevue: credit the City of Bellevue.
  - The removal rule is the safety net for both.
  - The owner also noted a **separate Seattle-only build already exists**.
- **Geostat's Business Register: PERMITTED WITH CONDITIONS.**
  - The terms allow any use "without prior permission". The condition is
    to name Geostat as the source, which the statistics law also requires
    (Art. 43(6)). No logo.
  - Two points stand, neither a prohibition:
    - statistical confidentiality: public-registry data is exempt under
      Art. 34(4);
    - Georgia's personal-data law: processing public data is lawful, and a
      restriction request is honoured, as the removal rule already does.
  - Tbilisi needs `add-country` for Georgia next.
- **Fukui's site-default CC BY-SA: PERMITTED WITH CONDITIONS.**
  - Share-alike would oblige offering `outputs/fukui/` under CC BY-SA 4.0
    (in `LICENSE`), the project's first share-alike licence on its own
    output.
  - The personal-services lists exist only under BY-SA, so only a food-only
    page on the older CC BY copy avoids it.
  - **The owner's call.**
- **Recorded in `docs/build_briefs/seattle.md`** ("What the build has to
  pull") and on the master list's Seattle, Tbilisi and Fukui rows.

### 2026-10-01 - The owner's calls 5-10: downloads approved, NaPTAN for the UK six, Dudley pre-approved, Atlanta's note filed, Richmond to R (owner)

- **5. Downloads approved:**
  - **Tempe's business licence list**: staging fetches and screens it.
  - **Burnaby's licence layer and Arlington's licence list**: for main's
    Vancouver (Regional) and D.C. + Arlington add-on builds. Recorded in the
    master list's add-ons note.
- **6. NaPTAN** (the Department for Transport's stop register, OGL) is gate
  3's independent source in all six UK briefs. It is the only one for
  Sheffield and Blackpool, whose operators refuse scripts. It needs a
  licence row and its notice at build.
- **7. Birmingham:** if West Midlands Metro's Line 2 is in passenger service
  at build, **Dudley (FSA 409) joins as a fourth authority**, pre-approved.
  It is written into the brief and the handoff.
- **8. Atlanta:** a note telling the City its 2024 licence layer exposes
  reported revenue is **drafted and filed, not to be sent**
  (`docs/notifications/atlanta-revenue-exposure.md`). The owner: "unlikely
  to send". It quotes no revenue value.
- **9. Dublin's vacant premises and the three undatable sources** (NYS food
  stores, Milan, Surrey): "disclose the lack of info where we need".
  - That is page text, so under the prose hold it goes to the prose pass,
    not to staging.
  - Cleanup was told the same day.
- **10. Richmond (BC) is in Band R, request only** (owner: "is request
  required? if so put into R").
  - It is: the City's business directory carries no open-data licence, and
    its copyright notice allows "research purposes and private use only",
    with written permission required.
  - The request (`buslic@richmond.ca`) is the owner's to send. Nothing is
    drafted.
  - **The list now holds A 7 · B 12 · C 3 · D 1 · R 23 = 46.**
- **Approved to run, and started the same day:**
  - licence reads of Seattle's register, King County's food inspections,
    Bellevue's licences and Geostat's register (plus Fukui's, from call 2);
  - the four UK brief re-runs that printed RETRY;
  - Brisbane's commuter-rail test;
  - a re-check of Takaoka's licence page.

### 2026-10-01 - The owner's calls on the fresh list: discards confirmed, Tbilisi to B, Fukui and Seattle conditional (owner)

- **1. The 19 new discards are confirmed** (owner: "confirm all"). The
  master list's notes now read "confirmed by the owner the same day".
- **2. Fukui uses the current CC BY-SA list, if a licence read clears
  share-alike for the map.** Otherwise it uses the older CC BY 2.1 JP copy.
  The `licence-read` agent was started the same day.
- **3. Tbilisi moves from C to B.**
  - The owner accepts Geostat's business register as the source, with the
    undercount disclosed: it lists enterprises, not premises, so a chain
    appears once.
  - Individual entrepreneurs are shown as **unnamed dots, category only**,
    on Taichung's precedent.
  - Personal ID columns are dropped at fetch.
  - The next steps are a licence read of Geostat's terms and `add-country`
    for Georgia.
- **4b. Seattle's retail and personal services outside Seattle and
  Bellevue** are accepted as unpublished and disclosed per city, **if
  further probing finds no further bucket**.
- **4c. Bellevue's never-expiring licences** get an issue-date cutoff,
  measured at build and brought to the owner.
- **4a is still open.** The owner asked whether the 2025 Snohomish layer is
  acceptable with its currency disclosed. Staging's answer: yes, under the
  rule "a frozen part may sit beside a current whole, its date on the page"
  (Tokyo's precedent), provided two things measure true at build:
  - it is a complete snapshot, checked against the county's published
    count of permitted establishments;
  - its date comes from more than the catalogue's "(2025)" label.

  The owner's yes is pending.
- **The list now holds A 7 · B 12 · C 3 · D 1 · R 22 = 45, with 119
  discards.** The count, discard and provenance checks pass.

### 2026-10-01 - The UK six briefed, with a prose hold; builds held (owner)

- **The owner (2026-10-01)**: "no, I want to wait on builds. generate the
  briefs now". And: "have the sessions wait on drafting prose. I'm currently
  in the middle of reworking site prose and want that to complete before
  these builds resort to generating the old prose."
- **Six briefs** are in `docs/build_briefs/`: `manchester.md`,
  `birmingham.md`, `edinburgh.md`, `sheffield.md`, `nottingham.md` and
  `blackpool.md`. **The handoff** is `docs/handoff_uk_six_2026-10-01.md`.
- **Every brief and the handoff open with the prose hold.**
  - Draft no page text: no description, scope sentence, What Is Excluded
    entries, notice wording beyond the licensor's attribution, or
    README/Overview copy.
  - Do not copy London's, Glasgow's or Newcastle's page text.
  - Leave `TODO(prose-hold)` markers and do not scaffold `app/pages` text.
  - The 2026-09-30 approved-template pre-permission is suspended for this
    round.
- **Measured for the briefs, 2026-10-01**: FSA per-authority counts and
  file sizes (HEAD); one Overpass query per city, run in sequence (tram
  relations, stop names, council boundaries with GSS codes); and which
  operator pages answer scripts.
- **Each brief carries the checks the tram kit's retrospective said
  briefs lacked**:
  - every authority's FSA file is listed;
  - the FHRS terms still name the OGL;
  - the operator's own stop list, where it answers scripts (TfGM, West
    Midlands Metro, Edinburgh Trams, NET);
  - OSM relations and refs;
  - the CRS fallback.
- **Found while briefing:**
  - **Nottingham (Regional) is 3,702 storefronts, not 4,723**, an addition
    error at the screen. The master list and the approval entry above are
    corrected.
  - **West Midlands Metro's Line 2 (Wednesbury–Dudley) is in OSM**, its
    stops marked "[Aug 2026]". Whether it is open is a Step 0 check, and
    adding Dudley is the owner's call.
  - **Sheffield's and Blackpool's operator sites refuse scripts** (a
    Radware CAPTCHA; 403). Gate 3's proposed source is NaPTAN (DfT, OGL),
    a new source that needs the owner's OK.
  - **Blackpool:** select Wyre (207), not Wyre Forest (153).
  - **Nottingham:** the city is a unitary authority at admin_level 6 beside
    three admin_level 8 districts. Union the four, never the county.
  - **Colours:** Sheffield's Yellow (`#FFFF00`) will need darkening. NET's
    two lines share one colour. Blackpool and Edinburgh carry none in OSM.

### 2026-10-01 - The UK six approved with their scopes: four regional pages, two city pages (owner)

- **The owner: "yes to the set"**, on staging's recommendations. All six
  are food-only pages on the FSA register, London's filter and Glasgow's
  privacy rules.

  | # | Page | Scope | Storefronts | Why |
  |---|---|---|---|---|
  | 1 | **Manchester (Regional)** | the 7 Metrolink districts | 12,451 | Manchester alone holds 42 of 99 stops, a stub |
  | 2 | **Birmingham (Regional)** | Birmingham, Sandwell and Wolverhampton, built now | 9,827 | Birmingham alone holds 16 of 35 stops |
  | 3 | **Edinburgh** | the city | 3,933 | Every stop is inside it |
  | 4 | **Sheffield** | the city, without the Rotherham Tram-Train | 3,447 | The Tram-Train runs every 30 minutes on converted railway (Aarhus L1's precedent); food first, the city's rates list a later screen |
  | 5 | **Nottingham (Regional)** | the city, Broxtowe, Rushcliffe and Ashfield | 3,702 (first written 4,723, an addition error; corrected the same day) | Beeston's 9 stops and the line ends draw filled rings |
  | 6 | **Blackpool (Regional)** | Blackpool and Wyre | 1,744 | Keeps Cleveleys and Fleetwood, the terminus |

- **The Dudley branch** (West Midlands Metro, about late 2026) becomes a
  dated watch item, not a reason to wait.
- **The build order is largest first**, so the first city pilots the shared
  code and the rest become configs.
- **Recorded in the master list's Band B** (the rows reordered, two renamed
  "(Regional)"). `check_master_list_counts.py` passes.

### 2026-10-01 - MHLW's food file counted for five Japanese cities: Utsunomiya and Kitakyushu to A; Kagoshima, Okayama and Kōchi to B (owner approved the downloads)

- **The owner approved the five downloads (2026-10-01).** Each is from
  `i2fas.mhlw.go.jp` (PDL 1.0, read for Fukuoka), 2.9–7.2 MB, and is kept
  in the staging scratchpad, never in the repo.
- **MHLW's file carries 85–91% of each city's restaurant permits in force.**
  - The rows are permits from 2021-06 on, all 許可.
  - Each city appears to enter every new permit there, not only the online
    filings.
  - The counts are open 飲食店営業 rows against the FY2024 in-force count.

  | City | Open permits | In force | Share | With an address |
  |---|---|---|---|---|
  | Utsunomiya | 4,901 | 5,761 | 85% | 99% |
  | Kitakyushu | 10,760 | 12,733 | 85% | 86% |
  | Kagoshima | 5,914 | 6,823 | 87% | 76% |
  | Okayama | 7,582 | 8,409 | 90% | 74% |
  | Kōchi | 4,564 | 4,999 | 91% | 54% |

  MHLW publishes an address only by consent (Fukuoka's precedent).
- **The verdicts**, on the reduced-bucket bar's placement rule (about 70%):
  - **Utsunomiya to A.** Food plus the CC BY personal-services lists.
  - **Kitakyushu to A.** Personal services have no laundry list, which is
    disclosed.
  - **Kagoshima to B, food only.** Its personal lists are a new-openings
    stream.
  - **Okayama to B, food only.** Its personal lists need the city's
    permission.
  - **Kōchi to B, personal services only.** Its food places 54%, under the
    bar.
- **The list now holds A 7 · B 11 · C 4 · D 1 · R 22 = 45.**
  `check_master_list_counts.py` passes.
- **No row values were printed.** The counting script printed counts,
  column names and years only.

### 2026-10-01 - The master list rebuilt fresh: 45 candidates from the post-review screens; Band R and the discards carried over (owner)

- **The owner's ask (2026-10-01)**: run the Job 2 probes, then "generate a
  fully fresh master list", since the review had emptied the old one, and
  carry over Band R and the discards.
- **The old list is archived word for word** at
  `docs/city_master_list_2026-09-30.md`. The new one carries these over
  verbatim:
  - the Built table (124);
  - Band R, with four new rows;
  - the discards, with a new table of 19 rows;
  - Countries ruled out, the Five rules, and Before building.
- **New: A 5 · B 8 · C 9 · D 1 · R 22 = 45 candidates; 119 discards.**
  - **A:** Matsuyama, Toyama, Kumamoto, Fukui, Nagasaki.
  - **B:**
    - the UK six, food only on the FSA register: Manchester (Regional),
      Birmingham (Regional), Sheffield, Nottingham, Edinburgh, Blackpool;
    - Sakai, food only;
    - Hakodate, personal services only.
  - **C:**
    - Seattle (Regional);
    - five Japanese cities hinging on one count of MHLW's file:
      Utsunomiya, Kitakyushu, Kagoshima, Kōchi, Okayama;
    - Takaoka (its licence);
    - Tbilisi (enterprise rows and individual entrepreneurs);
    - Brisbane (found in passing; the commuter-rail test).
  - **D:** Tempe (one download to approve).
  - **R:** the 18 carried, plus Kraków, Brescia, Catania and Alicante, whose
    portals refuse the built-in browser too.
- **The 19 new discards are staging's recommendations, for the owner to
  confirm**:
  - Toyohashi;
  - Dresden, Leipzig, Graz, Luxembourg City, Wrocław, Adelaide, the Gold
    Coast, Canberra;
  - Belgrade, Sarajevo, Santo Domingo, Casablanca, Rabat–Salé, Tunis, Lagos,
    Addis Ababa;
  - Cagliari, Alcobendas.

  Each row passes `check_discard_evidence.py`.
- **Band T is retired, not deleted.** Its section stays at 0 and names the
  tram list. That keeps `check_master_list_counts.py` reading the tram
  list's counts, and keeps the self-test's tram cases live: 24 of 24.
- **Japan's Kōchi is spelled with its macron.** "Kochi" is already a discard
  row: India's, in Kerala. The count check caught the collision.
- **The per-city screens behind each row** are in this session's report to
  the owner, and in the subagent notes in the staging scratchpad. The Seattle
  regional screen is in `docs/build_briefs/seattle.md`.

### 2026-10-01 - Probe slips during the post-review screens: one Overpass query, three console prints of personal data

- **One Overpass query beyond the session's own.**
  - The UK screen's agent ran `brief_check.py newcastle`, whose
    `osm_route_refs` claim queries Overpass. It passed 4/4.
  - Staging's own Link query had finished, so only one query was ever in
    flight.
  - Lesson: a screening agent's rules should name `brief_check.py` as an
    Overpass client.
- **Personal data printed to agents' consoles; nothing was saved or
  repeated:**
  - the UK screen's group-by on Birmingham's Gambling Act register printed
    licence holders' names and addresses;
  - the pattern screen's group-by on ACT's licence table printed its
    `Licensees` column;
  - a Japan helper's header reader printed one Toyama row (a business name
    and address).
- **Band B's retrospective lesson stands**: select columns before printing
  anything from a register with personal columns. The screening prompts
  said so, and the slips came from group-bys on a column the agent had not
  inspected first.
- **A looping REPL from the north-end Seattle agent** left about 290 MB of
  error output in this session's temp folders. Its process is stopped. The
  files are left for the owner to clear.

### 2026-10-01 - Seattle's regional screen: 37 stations in 11 cities; only Seattle and Bellevue publish all three buckets (owner's scope)

- **The owner (2026-10-01)**: Seattle stays held for a regional build with
  multiple city registers. Research every city along the 1 and 2 Lines.
- **Stations (OSM, one query)**: 37 stations in 11 cities.
  - Seattle 17, Bellevue 6, Redmond 4, Shoreline 2, SeaTac 2, Kent 2, and
    one each in Lynnwood, Mountlake Terrace, Tukwila, Federal Way and
    Mercer Island.
  - The cross-lake 2 Line opened 2026-03-28.
  - The rings also reach Des Moines (42% of Kent Des Moines' ring) and
    unincorporated King County.
- **What is published**:
  - Seattle and Bellevue each have their own register with all buckets.
  - Redmond's layer is frozen at about 2020, and Federal Way's is a 2024
    shopping-centre extract.
  - Nothing is published for Shoreline, Kent, Des Moines, Tukwila, SeaTac,
    Mercer Island, Lynnwood or Mountlake Terrace.
- **Food everywhere in King County**: Public Health – Seattle & King
  County's inspections (12,296 businesses, parcel-joinable). Its licence
  conflicts between the two published copies.
- **Snohomish food fails currency**: the only layer is a 2025 snapshot with
  no dates.
- **Retail and personal services outside Seattle and Bellevue**: only by
  public-records requests. That is outreach, the owner's last resort.
- **Recorded in full** in `docs/build_briefs/seattle.md`, "The regional
  screen". Seattle sits in Band C of the fresh list.
