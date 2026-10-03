# DECISIONS drafts - lane-docs (`lane-docs`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - The family wording batch: each page family made consistent with itself (owner-approved batch)

- **Tram pages (ten):** the in-ring share split 5-5 (last under The
  businesses on Odense, Daugavpils, Liepāja, Göteborg and Den Haag; last
  under Reading the density on Kansas City, New Orleans, Tucson, Florence and
  Zurich). **No majority, so the tram-city skill's template decides**: last
  under The businesses, on all ten. New Orleans's share led its band bullet;
  the share moves and the band sentence stays under Reading the density. Den
  Haag's third heading "Reading the map" becomes "Reading the density", as on
  the other nine. The skill's template note now says all ten match.
- **Japanese pages:** the no-general-license sentence is in parentheses on 17
  of 20 pages; Kobe, Osaka and Sapporo move from dashes to the majority form.
  **Kobe's "The city notes that premises which have closed may still be
  listed" stays**: it is Kobe's own statement (「既に廃業している施設が含まれる
  場合があります。」, the dataset page, read 2026-10-03), which the build
  brief's MUST NOT already relies on.
- **"Listed below" on the Japanese pages** (`docs/city_page_format.md` item
  6): every Japanese city has stations left out for lying outside it, and no
  page pointed to the list. The cut-at-the-city-line bullet gains "The
  stations left out are listed below." on 17 pages. **Fukui, Toyama and
  Okayama are lane-cats' files and were not touched**; cleanup applies the
  same sentence there after the merge. The japan-city skill's template
  carries it.
- **Taichung**: "Taiwan Railway and high-speed rail services are not drawn"
  becomes "... high-speed rail are not drawn", as Taoyuan's.
- **About the Data, 20 cells**: `outputs/<city>/excluded_stations.csv`
  becomes "listed on the city's page", to match What Is Excluded (owner,
  2026-10-02). Prague's cell, which said its file "is written EMPTY", was
  wrong since Flora was listed (2026-09-29) and now says none is left out for
  its location and Flora is listed on the city's page. Calgary, Ottawa,
  Kitchener-Waterloo and Palma still say "`excluded_stations.csv` is written
  empty"; not in the batch, left for the owner.
- **What Is Excluded, five `excluded_premises.csv` pointers** (Minneapolis,
  Pittsburgh, Kitchener-Waterloo, Palma, Ottawa): no page shows those rows,
  so the pointer is dropped rather than reworded; each list's lead now ends
  at its count or heading.
- **Palma's food sentence, broken by the prose pass** (18e4ecc7 left the old
  "(R5)" line beside the new one and dropped the end): restored to the
  approved "A premises is shown when the register lists it as active in Palma
  (4,372 of 4,375; 3 are temporarily closed)."

### 2026-10-03 - Staging's re-check corrections, each checked against its source (owner-approved batch)

- **Prague's Flora: about the end of February 2027**, not December 2026
  (expats.cz quoting DPP, 2026-08-23, read 2026-10-03). Page sentence,
  `config.FLORA_REASON` (so the excluded-stations row the page lists), the
  config comment, and `docs/project_context.md`, which still said Flora was
  drawn. Prague's step 1 re-run from the cached feed for the new reason.
  PLAN.md's date is cleanup's.
- **Amsterdam's tram 3 was discontinued on 29 March 2026**, not paused
  (mobiliteit.nl, 2026-03-26, read 2026-10-03: GVB "Zo vervalt tram 3
  volledig"; GVB's own pages answer 403). Page, What Is Excluded, About the
  Data and config reworded. No map change: it was never drawn.
- **Oslo's tram 13 west of Thune is closed for works**: Sporveien closed
  Thune - Lilleaker from 10 June 2026, overhead-line work to February 2027
  (sporveien.no, read 2026-10-03). The 2026-09-24 feed already runs 13
  Ljabru - Thune, so the map was drawn as the timetable runs and does not
  change. Added: the page sentence, What Is Excluded, the map-inconsistencies
  row, and a step-1 guard that STOPS once a rail trip calls at Hoff,
  Abbediengen, Ullern or Furulund again. **Not done, as the precedent asks:
  listing the closed stops in `excluded_stations.csv`.** Sollerud (on
  Lilleakerbanen per no.wikipedia) is not in the cached stops.txt at all, and
  Lilleaker's tram quays cannot be told from its bus quays there; a fresh
  feed or OSM read is needed, which this lane may not fetch.
- **Rome's tram 3: reactivated 7 September 2026**, Trastevere - Porta
  Maggiore (ATAC's tram status page, read 2026-10-03; 2, 5, 14 and 19 still
  bus-replaced). **No map change**: the cached Roma Mobilità GTFS (built
  2026-09-24, calendar 2026-09-17 to 2026-12-06) still has 0 trips on route
  3, and no tram 3 relation is cached. Config comment and the
  map-inconsistencies row corrected; drawing it waits on a fetch and the
  owner's call (recheck calendar: the whole network back by 23 November).
- **Denmark: DAWA closed on 1 October 2026**; it answered 410 Gone on
  2026-10-02 and 2026-10-03. Tense fixed in `docs/data_sources/denmark.md`
  (two places) and `docs/project_context.md`.
- **`docs/gated_access.md` item 12**: "Follow-up due 2026-09-28" becomes
  "Followed up 2026-09-28", no reply, next step the owner's (PLAN.md's record).
- **Not done here, by ownership:** D.C.'s config sentence (lane-cats owns
  `pipeline/washington_dc/`); Seoul's Wirye note, which lives only in PLAN.md
  (cleanup's).
