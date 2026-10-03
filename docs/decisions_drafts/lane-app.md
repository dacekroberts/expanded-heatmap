# DECISIONS drafts - lane-app (`lane-app`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - GitHub and LinkedIn icons in the page header, on every page (owner)

- **The owner approved both links** (2026-10-03): the repository,
  github.com/dacekroberts/expanded-heatmap, and the LinkedIn profile staging
  relayed. The GitHub one also puts the repository link in the header, which
  IDFM Art. 5.8 and ODbL §4.6 lean on; the footer link stays.
- **Built in `set_base_font()`,** which every page calls, so no page file
  changed: one Markdown element of inline SVG (Octicons' mark-github, MIT;
  Simple Icons' LinkedIn glyph, CC0), no icon font, no CDN. Each link opens a
  new tab (`rel="noopener noreferrer"`) and carries an `aria-label` saying so;
  the SVGs are `aria-hidden`.
- **Placed in the left end of Streamlit's header strip,** fixed, not the
  right: run locally, Streamlit's Deploy button sits left of its menu and the
  icons overlapped it there. The left end is empty while `MAP_ONLY_NAV` hides
  the sidebar's expand control; turning that off brings the control back to
  that corner (noted in the CSS).
- **Measured in the lean venv, one local server:** at 375 and 1200 the city
  title and the map start at the same y with and without the icons (the
  fixed container leaves the flow), no sideways scroll at 375, and the icons
  take the theme's text color in light (rgb 28,43,42 on white) and dark
  (rgb 230,237,247 on rgb 11,18,32). `check_city_page_format.py` passes:
  `set_base_font` is already in its silent set.

### 2026-10-03 - Staging's eight licence reads written in: notices 115-118 and seven licence rows (owner-approved batch)

- **Notices, each on its own city's pages and the Required notices page:**
  - **115, DLCP and OCTO (Washington D.C.):** CC BY 4.0 on both ArcGIS items
    (their titles and credits re-read 2026-10-03); both offices credited, the
    licence and each item linked, the changes said, the boundary "reprojected
    ... not drawn".
  - **116, National Transport Authority (Dublin):** the NTA's sentence
    verbatim, the licence link, data.gov.ie linked (its `nta-gtfs` page
    re-read 2026-10-03), the changes, "as is", no endorsement. The developer
    portal's indemnity is recorded as NOT accepted (owner).
  - **117, geo.api.gouv.fr, Contours administratifs and IGN (France),** on
    all 26 French pages: the ODbL §4.3 notice and the Licence Ouverte
    source-and-date line (owner: both). The date is the Contours
    administratifs record's last update, 2025-05-05, read on data.gouv.fr
    2026-10-03.
  - **118, MassGIS (Boston):** requested, not required; the credit in
    MassGIS's own FAQ words, read 2026-10-03 on mass.gov through the browser
    pane (its server refuses plain fetches): "MassGIS (Bureau of Geographic
    Information), Commonwealth of Massachusetts EOTSS".
- **No credit, by the reads:** LA County Planning's boundaries (none
  required; the row says never to call the outline a legal boundary) and
  SanGIS's boundaries (a credit is prohibited at this scale).
- **Rows:** united-states.md gains five licence rows (D.C.'s two, MassGIS, LA
  County, SanGIS boundaries) and drops the SanGIS boundaries' "Terms not read"
  row; it now names SanGIS as publisher of the boundaries and the parcels,
  SANDAG as host. ireland.md and france.md gain a licences section each.
  `pipeline/san_diego/` comments still say "SANDAG" for the boundary file;
  not this lane's files.
- **Numbering:** 115-118, as cleanup directed. docs/session_roles.md
  pre-assigns 115-128 to Japan wave 2, so the two collide if wave 2 numbers
  from 115; for cleanup to settle at the merge.

### 2026-10-03 - SFMTA's notice 3 is four sentences plus clause 4's disclaimer, on the cautious reading (owner-approved batch)

- **Re-read** on SFMTA's own page (`sfmta.com/reports/gtfs-transit-data`,
  "updated" 2024-10-01), which matches the stored copy in `docs/licenses/`
  word for word.
- **Clause 12:** "All Data derivative versions prepared by the Licensee shall
  bear the following notice:" is followed by TWO paragraphs before clause 13,
  the second the "does not guarantee ... 'as is'" disclaimer. Nothing marks
  where the notice ends, so on the cautious reading it ends at clause 13, and
  both paragraphs are displayed verbatim. Only the first was shown before.
- **Clause 4:** "The Licensee shall display or include this disclaimer in any
  use agreement for any application of the Data created or provided by
  Licensee." The Visuals session's reading: the duty attaches to a use
  agreement, and the site has none, so licence_positions row 2.16 may have
  overstated it. The sentence parses both ways: "display or include [it] in
  any use agreement", or "display [it], or include it in any use agreement".
  The second is the cautious reading, and costs one sentence; it is taken.
  "This disclaimer" is read as clause 4's own first sentence (clause 3's
  warranty disclaimer is covered in substance by clause 12's second
  paragraph).
- **What the site displays,** on San Francisco's page and the Required notices
  page: clause 12's two paragraphs, then a lead-in of this project's own
  ("SFMTA's license, under which this site is the Licensee, also asks for
  this disclaimer to be displayed:") and clause 4's first sentence in quotes.
- **Rows updated:** data_sources.md item 3, united-states.md's GTFS table,
  licence_positions 2.16 and Appendix A's US-SFMTA entry, and the two flags
  that named the gap.

### 2026-10-03 - Notice 1's rail list gains the UK nine and nine more cities found by a scan (owner-approved batch)

- **The UK nine**, whose rail and boundaries are all OpenStreetMap
  (`docs/data_sources/united-kingdom.md`), added to `_OSM_RAIL` and to notice
  1's sentence as be7d026b added sixteen.
- **A scan of every `docs/data_sources/*.md` table row** naming OpenStreetMap
  or Overpass, against `_OSM_RAIL`, found nine more whose rail or boundary
  comes from OSM: Stockholm (Tunnelbana, kommun boundaries), Bucharest
  (metro, city and sector boundaries), Tbilisi (metro, city boundary), the
  five French cities whose feeds carry no shapes (Montpellier, Strasbourg,
  Le Havre, Caen, Rouen (Regional)), and Philadelphia (one station node,
  11th Street, closed for works; it places a row of the excluded-stations
  file and is not drawn).
- **Left out on reading:** the French GTFS cities whose rows name OSM only as
  gate 3's cross-check; Berlin, Milan, Dublin, Riga and Paris, where OSM is a
  cross-check or explicitly not used; and the twenty Japanese cities, whose
  rail is MLIT N02 and which take only English station names from OSM
  (recorded as "credited by the map's OSM notice"). The Japanese names are an
  open question for the owner: rail data in the loose sense, not geometry or
  a boundary.

### 2026-10-03 - Check C checks both directions with no exemption; New York's notice 5 displayed (owner-approved batch)

- **The gap:** check C already failed a numbered notice no `_NOTICES` entry
  carried, but `NOT_DISPLAYED` exempted New York's 5 as "met by the About the
  Data and What Is Excluded pages", so a numbered notice the site did not
  display passed.
- **The fix:** `check_notice_bijection()` holds both directions with no
  exemption list. Its four cases (complete, a numbered notice displayed
  nowhere, a displayed notice not numbered, a displayed notice under another
  publisher's number) run before every check and alone with `--selftest`.
  `check_all.py` is not this lane's file, so the cases ride on the run it
  already makes.
- **Notice 5 displayed** on New York's page and the Required notices page, in
  this project's own words: the Technical Standards Manual reserves the
  right to require source, version and modifications, and prescribes no
  sentence. Version is the fetch date the city entry records (2026-09-21).
