# DECISIONS drafts - prose-4-city-pages (`prose-4-city-pages`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
  `outputs/<slug>/excluded_stations.csv`" now points to the What is counted
  page, which renders that file for the city.
