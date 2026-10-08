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
- **Not done:** a drift check over all 170 cities (this worktree has no
  `data/` junction; the default path is unchanged by construction and was
  shown equal on Mendoza), a deploy-verify (review time), the switch's
  wording on the published pages (to the owner), and the style-asset licence
  read above.
