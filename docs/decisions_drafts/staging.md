# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
