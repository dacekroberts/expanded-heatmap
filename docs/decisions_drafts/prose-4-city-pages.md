# DECISIONS drafts - prose-4-city-pages (`prose-4-city-pages`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-01 - City pages: the stations left out are listed on the page itself; eight sentence fixes (owner)

- **What Is Excluded shows a count per city, not station names.** Three of
  the six writers found it. The pass had replaced "listed in
  `outputs/<slug>/excluded_stations.csv`" with "listed on the What is
  counted page", which was not true. Before the pass, the names were only in
  that repository file, which no site reader could open either.
- **The owner chose to list them on the city page (2026-10-01).**
  `components.render_excluded_stations` draws the city's file under the
  bullets, in a collapsed "Stations left out (N)" list with the columns
  Station, Lines and Why. "Why" is the file's own `reason`, or its place
  column, or "outside the city" for the boundary-only files (Madrid, the
  `distance_outside_m` files).
  - The 41 pointers now read "listed below".
  - Washington D.C.'s per-state claim, Boston's per-reason claim and
    Minneapolis's and Pittsburgh's per-municipality claims hold through the
    Why column, so the writers' "counts them" proposals were not needed.
  - Both page templates carry the call.
- **Applied with the owner's approval (2026-10-01)**, from the writers'
  proposals:
  - Edmonton, Lille and Miami drop a repository path. The substance stays
    on the page.
  - Liberec and Most compare OpenStreetMap "in the two towns". The
    2026-09-30 restaurant control counted inside each regional polygon, and
    the register side was both towns' sum (448 + 139; 212 + 55).
  - Toulouse loses "the closest of the three French cities".
  - New York now says "most cities on this site".
  - Göteborg now "shows food only, not three categories".
- **Fixed without a proposal, as consequences of the layout:**
  - "Below" became "above" where a caption now sits above the prose
    (Daegu, Busan, and Göteborg's date fallback).
  - Riga's and Hiroshima's map help names their two categories again, as
    their old controls paragraphs did.

### 2026-10-01 - City pages: one format for all 124, approved on three samples (owner)

- **The format** (owner, set in the prose-pass plan, `docs/prose_pass_2026-10-01.md`):
  - the city's name, centred, with the subtitle "Transit-centered
    commercial density heatmap" (`components.render_city_title`);
  - the map next, nothing in between, still embedded at height 650;
  - the date and credit captions directly under the map;
  - the prose as bullets under short headings;
  - "Using the map" (`components.render_map_help`), the same on every page;
  - links to What Is Excluded and About the Data with `?country=<country>`
    (`components.render_country_links`, the contract with agent 2);
  - `render_site_notices()` last, inline as before.
- **Samples shown 2026-10-01**: Le Mans (the French template), Chicago and
  Seoul, at 375 and 1200 px, light and dark
  (`data/_review/prose-4-city-pages/samples*/`).
- **The owner's calls on the samples (2026-10-01)**:
  - **Long pages are shortened like Seoul's**: detail that a reference page
    already carries is left there, and every claim moved off a page is
    listed in this pass's report.
  - **Credits and dates under the map, notices in the footer.** The owner
    asked for a later look at how the footer notices are presented.
  - **"Using the map" approved**, with the layer control's icon shown in
    the text. The icon is Leaflet 1.9.3's own `layers.png`, from the CDN
    every map already loads Leaflet from, on a light tile so it reads in
    both themes. The "Top right: a Cities menu ..." sentence, on 6 pages
    before, is now on every page: it describes controls every map shares.
  - **A date caption for every page.** The 30 pages that read no provenance
    file show `cities.py`'s `data_age` (`components.render_data_age`).
  - **Link labels kept for now**: "What is counted, and what is not:
    <country>" and "Where this data comes from: <country>".
- **Also changed**: the empty space above the title on city pages, from 6rem
  of padding and four invisible 16 px elements to 3.5rem. Measured at 375 px,
  the map's top moved from 248 px to 184 px. The map's Global View button,
  which clicks the hidden city links, still works. The OSM credit inside the
  map is clear at 375 px with the legend forced open (clamp 24/24).
- **Repository paths left the page text.** The sentence "listed in
  `outputs/<slug>/excluded_stations.csv`" became "listed below" (see the
  entry above).
- **The rollout.**
  - **Layout:** a restructuring script moved the blocks on 101 pages
    (`data/_review/prose-4-city-pages/restructure_pages.py`), and
    `france_page.py` regenerated the 21 French template pages. Every
    sentence and figure was kept; only the station-list pointer changed.
  - **Bullets:** six writers, one family each, converted the prose. Only
    `st.markdown` text changed, which was checked against HEAD by AST.
  - **Claims moved:** 117 claims left the pages for the reference pages,
    plus Seoul's 3. All are listed in
    `data/_review/prose-4-city-pages/claims_moved.md`.
- **Found on the way:** `france_page.py` matched New Orleans's page when
  writing Orléans's, because its glob had no page number. It now matches the
  number as well as the name.
