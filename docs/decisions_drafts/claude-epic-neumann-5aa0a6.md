# DECISIONS drafts - open basemap research (`claude/epic-neumann-5aa0a6`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file. The session is the research and
prototype work the owner approved on 2026-10-07 (`DECISIONS.md`, "Four ideas
assessed before the large review", item 4), narrowed the same day: the travel
app is its own project, this repo keeps the basemap switch, its hosting and an
export contract (owner, relayed by Cleanup). Nothing here is landed, pushed
or published; every proposal waits for the owner.

### 2026-10-07 - The app export contract: one versioned file per city, read-only for the app project (proposal, owner to decide)

- **Proposal, not code.** The travel app is its own project and never edits
  this repo; this repo never holds app code (owner, 2026-10-07). The
  interface is a set of files this repo publishes and the app reads, so the
  site and the app read one source.
- **What is written.** A shared module, `pipeline/export_city.py`, called at
  the end of `render_heatmap()` with the stations and lines it already holds,
  writes `outputs/<city>/export/city.json` (recommended over a step4 per city:
  no per-city edits for 170 cities, `step3_map.py` files stay thin, and the
  export can never disagree with the drawn map because it is written from the
  same objects). Being under `outputs/`, every export is committed and
  `drift_check.py` diffs it like the map. A step never fetches: station exits
  and the basemap pack's metadata are fetched by `fetch_sources.py` (exits,
  one Overpass query per city, one in flight per session) and by a new
  `scripts/build_packs.py` (packs, `pmtiles extract`), and the export reads
  their caches. A city with no exits cache exports `"exits": []` with
  `"exits_status": "not fetched"`, never a silent empty list.
- **Published how.** `scripts/publish_export.py` gathers every city's
  `city.json` plus a `manifest.json` into a GitHub release of this repo
  tagged `export-v<major>-<YYYYMMDD>`; the app project reads the release
  assets at build time. Release assets serve range requests but send no CORS
  headers (measured 2026-10-07: a preflight to a release download returns
  404), so they suit a build-time read, not a browser. Publishing a release is
  an outward action and waits for the owner each time.
- **Versioning.** `schema_version` is semver. Adding an optional field is a
  minor version; renaming, removing or changing a field's meaning is a major
  one, and a major version gets a new tag series so the app pins it. The
  schema itself lives at `docs/export_schema/city-export-1.schema.json`, and
  a new `scripts/check_export.py` validates every city's file against it,
  refuses a line without a real public name and a color, refuses a notice
  that `app/components.py`'s `_NOTICES` assigns to the city but the export
  lacks, and refuses any field from a business register.
- **Never in the export: business-register data.** No business records, no
  counts, no heat. The app's everyday places come from OpenStreetMap (owner),
  and keeping registers out keeps their licences, their notices and the
  personal-information invariant out of the contract entirely.
- **`city.json`, version 1.0.0.** Fields marked **[L]** carry a licence
  obligation that travels with the data:

  | Field | Contents | Obligation |
  |---|---|---|
  | `schema`, `schema_version` | `"expanded-heatmap/city-export"`, `"1.0.0"` | none |
  | `generated_utc`, `source_commit` | when written, the commit the pipeline ran at | none |
  | `city` | `slug`, `name` (the page's name), `country`, `lang` (BCP 47, as `render_heatmap` takes it), `bbox` [w, s, e, n] | none |
  | `systems[]` | `id`, `name` (as the layer names it, "Metrotranvía"), `operator` | none |
  | `lines[]` **[L]** | `id`, `name` (the real public name, the legend's), `label` (the on-map label, a line code where the map uses codes, as Tokyo's do), `color` (hex, as drawn), `system`, `source` (a `licences[].id`), `geometry` (GeoJSON MultiLineString, one part per alignment, WGS84, 5 dp) | the source's: attribution; for OSM-derived lines ODbL share-alike on the database; for a feed, whatever its row in `docs/data_sources.md` says |
  | `stations[]` **[L]** | `id` (stable: the feed's stop id or the OSM node id), `name`, `names` {lang: name} where the source has them, `lines` [line ids], `lat`, `lon`, `no_data` (Tokyo's hollow stations), `source` | as for lines |
  | `exits[]` **[L]** | `id` (OSM node id), `station_id` (nearest station within 300 m, measured in the city's own UTM zone, never EPSG:4326), `name`, `ref` (exit number or letter), `wheelchair`, `level`, `lat`, `lon` | ODbL: attribution, share-alike on the database |
  | `exits_status` | `"fetched"`, `"none in OSM"` or `"not fetched"` | none |
  | `data_dates` **[L]** | per source: `retrieved_utc`, `valid_from`/`valid_to` where a feed declares them, `update_interval` where a licence requires one shown; `osm_retrieved_utc` | Licence Mobilités Art. 5.7 (Paris) requires the data's date and update interval displayed; CRTM requires the update-date metadata kept unaltered; so these fields are required, not optional, for those sources |
  | `basemap_pack` **[L]** | `file`, `bytes`, `sha256`, `build` ("20261007"), `osm_replication_utc` (from the pack's metadata: 2026-10-07T04:00:00Z for Mendoza's), `bbox`, `maxzoom`, `credit` ("© OpenStreetMap") | a produced work under ODbL: the credit must be shown wherever the map is |
  | `notices[]` **[L]** | `number` (as `docs/data_sources.md` numbers it), `publisher`, `text`, `verbatim` (true where the wording is prescribed), `applies_to` (`lines`, `stations`, `exits`, `basemap`) | verbatim texts must be reproduced unaltered; only the notices for the exported layers, never a register's |
  | `licences[]` **[L]** | `id`, `source` (publisher and dataset), `licence`, `url`, `obligations` [`attribution`, `share-alike`, `no-modification`, `date-display`, `termination-deletion`, `app-terms-unread`] | the list the app project starts its own reading from; `app-terms-unread` marks a feed whose terms for shipping inside an app this repo has not read (WMATA, LA Metro, IDFM and CRTM went to the app project, 2026-10-07) |

- **The full rail network, not the site's cut (owner, 2026-10-07, at the
  app project's request; relayed by Cleanup).** The export carries every line
  and station of a city's network, including what the site leaves off or
  cuts short: stub lines, lines cut at the city boundary, and lines left out
  by other rules (frequency floor, scenic, trial service). The site's maps
  keep their scope; only the export gains these. Fields, all in 1.0.0:

  | Field | Contents |
  |---|---|
  | `lines[].on_site_map` | true when any part of the line is drawn on the site |
  | `lines[].segments[]` | the line as stretches: `geometry` (GeoJSON LineString), `on_site_map`, `exclusion`; a line drawn whole is one segment |
  | `lines[].geometry` | the full network geometry, the union of the segments (as before) |
  | `lines[].geometry_status` | `"full"`, or `"cut_only"` (only the site's cut survives; a fresh source is pending), never a cut passed off as whole |
  | `lines[].color_source`, `lines[].name_source` | `"site"` (the site draws it), `"feed"` (the feed's `route_color` and name) or `"osm"` (the relation's `colour` and `name`); a line the site never drew has no site color, and `"none"` is allowed for color only |
  | `stations[].on_site_map`, `stations[].exclusion` | the same flag and object for stations, from each city's committed `excluded_stations.csv` |
  | `exclusion` | null when drawn, else `rule`, `detail` (the reason as the city records it, verbatim), `decided` (the `DECISIONS.md` date and title, or the skill or rules section that sets the rule) |

  `exclusion.rule` is one of: `stub`, `city_boundary`, `other_network` (a
  neighboring town's own line in the same feed, as Aubagne's tram in
  Marseille's), `frequency_floor` (the 15-minute test or a country's rail
  test), `scenic` (heritage or tourist service), `trial_service`,
  `closed_for_works`, `spacing` (stations only: thinned by
  `pipeline/stations.py`'s `thin()`, the line itself is drawn), `mode` (a
  mode outside the page's scope, such as a heavy-rail line on a trams-only
  page), or `other` (with `detail` required). The station rules map one to
  one onto `app/station_scope.py`'s `classify()` vocabulary (`thinned` ->
  `spacing`, `infrequent` -> `frequency_floor`, `outside` -> `city_boundary`
  or `other_network`, `closed` -> `closed_for_works`), and the export
  imports that function rather than keeping a second vocabulary; a reason it
  returns `other` for fails `check_export.py` until a rule is named. The 12
  `excluded_stations.csv` files (of 162) that carry boundary columns instead
  of a `reason` (`located_in`, `commune`, `distance_outside_m` and the rest,
  counted 2026-10-07) map to `city_boundary`.
- **Where full geometry comes from, per line class.** Measured from the
  committed step 3 files, 2026-10-07: 27 cities draw lines from a GTFS feed
  (`load_line_shapes`), 48 from OSM route relations
  (`load_osm_line_shapes`), 56 from a GeoJSON file
  (`load_geojson_line_shapes`, MLIT N02 among them), the rest through shared
  modules (`osm_tram`, the Japanese and country steps).

  | Line class | Full geometry from | Held now? |
  |---|---|---|
  | Cut at the city boundary, GTFS city | the cached feed's `shapes.txt`, read before the clip | yes where `data/<city>/raw/` holds the zip (274 zips are cached across cities); else a re-download from the publisher's own host |
  | Cut at the city boundary, OSM city | the cached relation: every OSM query in the pipelines uses plain `out geom`, never `out geom(bbox)`, so member ways come back whole whatever the query's bbox | lines yes; stop nodes only where they were fetched as relation members rather than by bbox, checked per city |
  | Cut at the city line, Japanese city | MLIT N02, a national file, before `japan_step1`'s cut at the N03 line | yes, while the N02 cache is held |
  | GeoJSON-fed city | the raw file the GeoJSON was made from | at risk: where the GeoJSON in `data/<city>/processed/` is itself the cut, and no raw file survives, only the cut is held |
  | Stub, scenic, trial or frequency-floor line left out whole | GTFS: the same cached feed (its other routes), using the route's own shape, never a line joined through its stops; OSM: the cached relations, if the query selected that route type | at risk where the query filtered route types (`OSM_ROUTES` of tram and light_rail leaves out a funicular or heritage line), or a feed omits shapes for the route |
  | Station thinned by spacing | nothing to fetch: the line is drawn whole and `excluded_stations.csv` keeps the coordinates | yes |

- **Cleanup's list (`data/_app_requests/rail_scope_2026-10-07.md`, master
  at bd0e9a8a) settles most of it.** 16 stub lines in 11 cities, 111 cities
  with lines cut or stations outside (76 outside Japan, 34 Japanese), 82 rows
  left out for other reasons. The raw caches hold whole GTFS feeds, whole OSM
  relations, the whole national N02 file and whole CRTM layers; only
  `data/<city>/processed/lines.geojson` and the map are cut. So the export
  reads the raw caches, never `processed/lines.geojson`, and computes each
  segment's `on_site_map` by overlaying the drawn geometry on the full one
  (a buffer in the city's own UTM zone). That also closes the list's open
  gap, "drawn versus cut not traced for most GTFS cities": the export never
  needs to know how the site cut a line, only what it drew.
- **Lines needing a fresh source.** Held means the export can be written from
  caches already on this machine. Fresh means nothing cached has the line.

  | City | Lines | Held? | Fresh source |
  |---|---|---|---|
  | Chicago | Metra | no (CTA feed only) | OSM relations (recommended) or Metra's feed |
  | Los Angeles | Metrolink | no (`gtfs_rail.zip` is Metro rail only) | OSM, or Metrolink's feed |
  | Montréal | exo commuter trains | no (STM and REM only) | OSM, or exo's feed |
  | Washington DC | MARC, VRE | no (WMATA only) | OSM, or the two agencies' feeds |
  | Madrid | Cercanías | no (CRTM M4 and M10 layers only) | OSM, or the CRTM Cercanías layer (same publisher, a new layer) |
  | Den Haag | RandstadRail E | held under another city: `data/rotterdam/raw/gtfs-openov-nl.zip` (RET metro E); Den Haag's own query is `route=tram` only | none; Den Haag's `fetch_sources.py` names the national file, so its export does not depend on Rotterdam's cache |
  | Incheon | Seoul Line 1's southern branches | partial: the query returns only relations touching Incheon | OSM, by relation id |
  | Korean cities | lines leaving the cached bbox | partial (inferred from the bbox query) | OSM, by relation id |
  | Commuter and regional rail named in the mode-scope row (BART, Caltrain, Coaster, Sprinter, GO, LIRR, Trenord and Passante, SNCB, National Rail, Pendeltåg, Korail, Taiwan Railway and HSR, V/Line, NSW TrainLink, Buenos Aires commuter railways, and the rest) | per city | held where the city cached a whole agency or national feed (Paris RER and Transilien, Berlin S, MBTA, Dublin, Marseille TER, Sounder, Tri-Rail, WCE, NS, Vivi, Prague S); unknown elsewhere | the export's own check decides it, by looking each named line up in the caches, rather than this table guessing; where absent, OSM |
  | Japan, 34 cities | stations beyond 3 km of the city line | held: N02 is national, and the 3 km cut is `DRAW_BEYOND_M` in `japan_step1`, not the file | none |
  | Brno, Le Havre, Montpellier, Strasbourg, Plzeň | geometry of undrawn routes (their feeds carry no `shapes.txt`) | held where each city's OSM query matched the route | OSM, by relation id, where it did not |

- **Recommended fresh source: OpenStreetMap, for every gap.** It is a source
  this project already uses under ODbL with its credit shown, so the gaps
  need no new licence, only one Overpass query per city in that city's
  `fetch_sources.py` (one in flight per session, 60 s after a 504 or 429).
  An agency feed would add a new source (owner first, a licence read, a
  `docs/data_sources.md` row), and its only gain over OSM would be
  timetables, which version 1 does not carry. Until fetched, such a line
  exports with `geometry_status: "cut_only"` if a cut exists, or
  `"not_held"` with no geometry, never silently left out.
- **How far is "in full" (owner, 2026-10-07, relayed by Cleanup: yes to
  the proposal).** Urban lines (metro, tram, light rail) go whole to their
  termini; mainline and commuter lines are carried to the edge of the city's
  basemap pack (its extent plus 10 km, the area the app can draw offline),
  with the part beyond marked `geometry_status: "clipped_to_export_extent"`.
  The reason: a Japanese JR line, the Tōkaidō or the Sanyō, runs hundreds of
  kilometres beyond the city, and every line whole would make some Japanese
  exports carry much of the national network.
- **Out of rail scope altogether:** aerial lifts (Cablebús, the Maokong
  Gondola) are not rail; whether the app wants them is the app project's
  question, and the export leaves them out unless the owner says otherwise.
- **`manifest.json`.** One file for all cities, so a reader's device fetches
  the same thing whichever cities it holds: per city `slug`, `schema_version`,
  `sha256` of `city.json`, `generated_utc`, the basemap pack's `build`,
  `bytes` and `sha256`, and `flags` [`removed` (a removal request honored:
  the app deletes its copy), `rail_changed` (a line opened or closed since
  the last release), `licence_review_by` (a date a licence must be re-read
  by)]. The flags carry the "urgent flags per city" item 4 named.
- **Not in version 1.** Timetables (stations and lines only; a timetable's
  expiry dates and its feed's terms belong to the app project), everyday
  places from OSM (the app project's own extract), the Overview's data.
- **Open for the owner:** (a) the release route versus a separate public
  repository for the exports; (b) whether `city.json` is ODbL as a whole
  (it is, wherever OSM data is in it: the simplest statement is that the
  export is published under ODbL with each feed's own terms noted per
  source); (c) whether `_NOTICES` moves from `app/components.py` into a data
  file both the app and the export read, rather than the export parsing app
  source as `check_provenance.py` does.

### 2026-10-07 - Hosting the open basemap: Cloudflare R2, about nothing a month for 3-6 GB (recommendation, owner to decide)

- **Recommended: Cloudflare R2**, behind a custom domain if the owner has or
  buys one (about $10 a year), else behind a Cloudflare Worker on
  `workers.dev`. R2 charges no egress, $0.015/GB-month beyond 10 GB free,
  and $0.36 a million reads beyond 10 million free a month
  (developers.cloudflare.com/r2/pricing, read 2026-10-07). All 170 packs
  are 2.70 GB at the map extent and 5.94 GB with 10 km more (measured
  2026-10-07), so both fit the free storage; the measured Mendoza view read
  5 ranges, so 10 million free reads is of the order of a million views a
  month. Protomaps names R2 its recommended store "because it does not have
  bandwidth fees" (docs.protomaps.com/pmtiles/cloud-storage).
- **The domain question is the real choice.** R2's `r2.dev` address is
  "rate-limited and should only be used for development purposes", and
  Cloudflare's cache needs a custom domain that is a zone in the same
  account (developers.cloudflare.com/r2/buckets/public-buckets). Without a
  domain, Protomaps' Worker serves the tiles from R2 (100,000 requests a
  day free, or $5 a month for 10 million; developers.cloudflare.com/workers/
  platform/pricing), though its cache "must be assigned a zone on your own
  domain, not workers.dev" (docs.protomaps.com/deploy/cloudflare). A
  Worker also turns ranges into ordinary tile URLs, so the browser needs no
  pmtiles library. Protomaps warns that R2's latency can be 500 ms or more.
- **Compared, for 3 GB and 6 GB stored and an assumed 50 GB a month read:**

  | Host | Storage | Reads and egress | A month |
  |---|---|---|---|
  | Cloudflare R2 | free to 10 GB, then $0.015/GB | egress free; reads free to 10 M | $0 (domain optional, ~$10 a year) |
  | Backblaze B2 | free to 10 GB, then $6.95/TB | egress free to 3x storage (9 or 18 GB), then $0.01/GB; free through Cloudflare and others; reads free | $0.32-0.41; HTTP/1.1 only (Protomaps) |
  | AWS S3 | $0.023/GB ($0.07-0.14) | 100 GB/month free across AWS, then $0.09/GB; GETs $0.0004 per 1,000 | about $0.10-0.55; about $81 at 1 TB |
  | GitHub Pages | site capped at 1 GB | soft 100 GB/month; not a file host | unsuitable |

  Sources: backblaze.com/cloud-storage/pricing, aws.amazon.com/s3/pricing,
  docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits,
  all read 2026-10-07. GitHub is out three ways: the packs exceed Pages' 1 GB,
  git refuses London's 113 MB pack (over 100 MB), and release assets send no
  CORS headers, so a browser cannot range-read them.
- **One alternative for the site alone:** the whole planet build is 138.7 GB
  (2026-10-07), about $1.93 a month on R2, and pans seamlessly anywhere,
  where a city pack goes blank beyond its extent. Per-city packs are what an
  offline reader needs, and they cost nothing, so they are recommended for
  both.
- **CORS:** allow any origin (the maps are embedded in Streamlit iframes),
  allow the `range` and `if-match` headers, expose `etag`
  (docs.protomaps.com/pmtiles/cloud-storage).
- **Before release, a licence read for the style assets** (fonts and sprites
  from protomaps.github.io/basemaps-assets), with the read-licence skill,
  and a `docs/data_sources.md` row for the basemap itself (Protomaps' code
  BSD-3, styles CC0, tiles ODbL produced work). Neither is done.

### 2026-10-07 - Basemap switch prototype on Mendoza: works, default unchanged, Open costs about 5 s and 7 MB on a phone (measured)

- **Built on the shared renderer.** `pipeline/map_common.py` gains an
  `OpenBasemap` layer and an optional `open_basemap=` argument to
  `render_heatmap()`; omitted, a map renders exactly as before (Mendoza's
  scratch render matched the committed `outputs/mendoza/heatmap.html` once
  Folium's random ids were normalized). Given, the layer menu offers two base
  layers, "Standard" (OSM's tiles, still the default) and "Open". A city
  passes it from its config in one line, so `step3_map.py` files stay thin.
  The prototype rendered from a scratch script; no city file and nothing
  under `outputs/` changed.
- **The pack.** go-pmtiles v1.31.2 from github.com/protomaps/go-pmtiles
  releases (zip sha256 a658baa4...785a1), `pmtiles extract` of the
  2026-10-07 planet build over Mendoza's extent plus 10 km, zoom 0-15:
  4,129,904 bytes, 845 tile entries, 7.8 s, 52 requests, matching the
  index-only estimate (4.1 MB). OSM data as of 2026-10-07T04:00Z.
- **How it loads.** MapLibre GL 5.24.0 (version 6 ships ES modules only,
  which maplibre-gl-leaflet 0.1.4 cannot read), pmtiles 4.5.0 and
  @protomaps/basemaps 5.7.2 load only when a reader picks Open, so the
  default view pays only 3.3 KB of page. The GL canvas sits in Leaflet's tile
  pane, so the dark theme's existing invert filter applies to it unchanged.
  The credit is the existing `OSM_ATTRIBUTION`, carried by the outer layer;
  the GL layer adds none, so it never doubles.
- **Measured** in headless Edge at 375 x 812, Lighthouse's mobile profile (4x
  CPU slowdown, 150 ms, 1.6 Mbps), cold cache, three runs each, medians:

  | | Today's map | Switch page, Standard | After picking Open |
  |---|---|---|---|
  | Load event | 4.33 s | 4.41 s | |
  | Basemap ready | 4.41 s | 4.49 s | 5.18 s after the click |
  | JS heap after GC | 6.1 MB | 6.1 MB | 12.7 MB |
  | Browser, all processes | 537 MB | 537 MB | 634 MB |
  | Bytes for the basemap | 182 KB (6 PNG tiles) | same | 297 KB libraries, 170 KB glyphs and sprites, 129 KB of pack in 5 ranges |

  Of the 5.18 s, 2.7 s is the libraries arriving. Self-hosting them beside
  the packs, or preloading on the layer menu's first opening, is the obvious
  saving; making Open the default would add the same bytes to every load.
  The GPU was a desktop one (the headless run used the machine's own); a
  phone's GPU memory is not in these figures.
- **Credit check.** `scripts/check_map_attribution.js`, with Open selected,
  at 375 x 650, 375 x 812, 1280 x 650 and 1280 x 900: no problems, the credit
  uncovered at all five points, the legend clamp in force, OSM's tiles gone
  from the page.
- **The line highlight survives the switch (owner, 2026-10-07: it applies
  to every interactive map, "unless the map is a static copy").** Tested with
  real input in headless Edge on Mendoza: desktop 1280 x 800 with a mouse
  (hover and fine pointer), and 375 x 812 with touch emulation (coarse
  pointer, no hover), on today's map, the switch page on Standard, and the
  switch page on Open. All three gave identical results in both modes:
  hovering the line lights it and its legend row, and moving off clears it;
  a click or tap on the line selects it, and on empty map clears it; a
  station shows its name (tooltip on hover, the tap panel on touch); the
  legend opens and a row picks its line; the line label is drawn in the
  frame; the credit is on top with its link opening a new tab; dragging
  moves the map. Embedded in a parent page with a Global View link, the map's
  own Global View button shows and navigates the parent, on both basemaps
  and both inputs. Why the GL canvas does not intercept: maplibre-gl-leaflet
  puts it in Leaflet's tile pane (z-index 200), under the overlay pane (400)
  where the lines are drawn, and its canvas has `pointer-events: none`; at
  the tested line point the topmost element was the line's own path on
  every basemap. One behaviour seen on all three and so not new: on desktop,
  a second click on a legend row unpicks the line, but it stays lit while
  the mouse is still over the row, because hovering a row previews its line
  by design.
- **Not done:** a drift check over all 170 cities (this worktree has no
  `data/` junction; the default path is unchanged by construction and was
  shown equal on Mendoza), a deploy-verify (review time), the switch's
  wording on the published pages (to the owner), and the style-asset licence
  read above.
