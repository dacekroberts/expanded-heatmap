# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
