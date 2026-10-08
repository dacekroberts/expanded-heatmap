# DECISIONS drafts - open basemap research (`claude/epic-neumann-5aa0a6`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file. The session is the research and
prototype work the owner approved on 2026-10-07 (`DECISIONS.md`, "Four ideas
assessed before the large review", item 4), narrowed the same day: the travel
app is its own project, this repo keeps the basemap switch, its hosting and an
export contract (owner, relayed by Cleanup). Nothing here is landed, pushed
or published; every proposal waits for the owner.

### 2026-10-08 - RESUME NOTE for the next session (internal; Cleanup drops this entry when folding)

- **The Mendoza build command** (done 2026-10-08; reuse it for the next
  city with its own `--area` and `--bounds`). Run from
  `data/_basemap_build/`, since the builder reads `data/sources/`
  relative to its working directory; `--bounds` keeps the output to the
  pack extent, `-Xmx` caps the heap; `java.exe` must be an absolute Windows
  path (`cygpath -w`); the output is `<area>.pmtiles` there, so rename it:
  `python ../../scripts/heavy_job.py run --label basemap-build-mendoza --session epic-neumann --peak-gb 6 --estimate "planetiler on a 432 MB extract, -Xmx5g" -- <absolute path>/tools/jdk-21.0.12.1+1/bin/java.exe -Xmx5g -jar basemaps-main/tiles/target/protomaps-basemap-HEAD-with-deps.jar --area=argentina --bounds=-68.9700,-32.9960,-68.7260,-32.7670 --maxzoom=15`
  Measured peak 3.27 GB on a 432 MB extract; scale from it for a new
  label. Never pass `--download`: every input is already local. Scratch
  tools for the comparison: `pack_compare.py`, `pack_lowzoom.py`,
  `pair_shots.mjs`, `pair_sheet.py`.
- **Where things are.** `data/_basemap_build/` (gitignored, this worktree):
  `data/sources/` holds argentina.osm.pbf (sha256 d23c0242...c5021f14),
  water and land polygons, Natural Earth, pgf-encoding, and the two empty
  stand-ins (qrank.csv.gz, 49 bytes; daylight-landcover.gpkg, an empty
  `landcover` layer with a `class` column). `tools/` holds the unpacked JDK
  21.0.12.1 and Maven 3.9.16; `basemaps-main/tiles/target/` the compiled
  builder (1.6 min compile, 2026-10-08); `m2repo/` Maven's 127 MB library
  cache. Avignon (PACA, 390 MB) and Florence (Italy centro, 385 MB)
  extracts are not downloaded yet; the owner downloads by hand.
- **Scratch tools** (this session's scratchpad,
  `C:\Users\dacek\AppData\Local\Temp\claude\C--Users-dacek-Documents-Portfolio-expanded-heatmap--claude-worktrees-epic-neumann-5aa0a6\bd1314d5-8fea-459a-81fe-c606b5bfdae5\scratchpad\`):
  `render_mendoza.py` (today and switch renders into `site/`),
  `render_open_default.py` (Travel-default variant), `range_server.py`
  (local HTTP range server; launch entry `basemap-proto-tmp` in the
  worktree's `.claude/launch.json`, added and removed per run), headless
  Edge harnesses `measure.mjs` and `measure2.mjs` (phone load, memory,
  bytes, cold and warm), `interact.mjs` (line highlight and the rest, mouse
  and touch), `travel_check.mjs` (the half version), `offline.mjs` (no
  network), `attr_check.mjs` (runs `scripts/check_map_attribution.js`),
  `shots.mjs`; `site/offline/` holds the local libraries, fonts and
  sprites for the offline test; `basemap_baseline_2026-10-07/` the frozen
  baseline given to the travel app; `shots/` the screenshots.
- **Done 2026-10-08: the self-build comparison** (entry below; 3 min 18 s,
  peak 3.27 GB measured, same map). The gate needs an absolute `java.exe`
  path; the output is `<area>.pmtiles` in the working directory.
- **Done 2026-10-08: the shared Travel style** (`pipeline/travel_style.js`,
  entry below; five questions for the owner there). The offline test page
  takes `&travel=1` and `&world=1`; `style_shots.mjs`, `world_probe.mjs`,
  `style_test.mjs` and `crop_disputed.py` in the scratchpad.
- **Done 2026-10-08: Avignon and Florence self-built** (entry below;
  `build_pilot.sh`, `pilot_shots.mjs`, `pack_bounds.py` in the scratchpad;
  the extracts are copies, the owner's originals stay in Downloads).
  Master moved since this branch (line registry, 34 maps re-rendered,
  `map_common.py` about 160 lines): merge it only before this branch's own
  push, and re-run `check_render_current` after.
- **Done 2026-10-08: the label pill** (entry below; `lang_check.mjs` in
  the scratchpad; `render_mendoza.py` now passes `local_lang="es"`).
- **Done 2026-10-08: the build-time trim** (`--travel_trim`; entry below;
  `build_trim.sh`, `trim_shots.mjs`, `trim_diff.py`; the compiled builder
  in `basemaps-main/tiles/target/` now carries the switch, the stock jar
  is `data/_basemap_build/protomaps-basemap-stock.jar`, the stock sources
  `data/_basemap_build/_stock_src/`).
- **Done 2026-10-08: zoom 14 chosen; baselines in
  `data/_basemap_build/baselines/` (move them with the build before this
  worktree goes); `scripts/check_travel_style.mjs` (run it whenever the
  style or the trim lists change).**
- **Full version, how it differs from the site's Travel view** (laid out
  for the owner 2026-10-08): no business data at all (a check refuses
  ring, heat or business layer names); Travel only, no Business switch and
  no OSM tile server; offline (libraries, fonts, sprites and pack beside
  the page); style variant "full" (blue ferries); same pack, labels, pill,
  tooltips, line highlight; legend lines only; OSM credit plus the font
  and sprite licence files. **Decided (owner): white line casings and
  white station dots with a dark ring are built into the full version,
  designed for light and dark mode alike** (they stay a trial on the site).
  **Decided (owner): the city page first, the world map after it;
  delivery as a folder plus the small range server** (offline downloads
  will need their own host anyway for the app stores).
- **Icons and fonts (recommendation, owner to confirm, 2026-10-08).** The
  Travel style uses three sprite icons only: the one-way arrow
  (`roads_oneway`) and the town dot and capital star of `places_locality`
  below z8. Dropping both leaves no sprite to ship, so no icon licence
  (Protomaps' sprites are MIT) and one file less. Fonts cannot be dropped:
  MapLibre GL draws Latin labels from glyph files, never device fonts
  (CJK can use device fonts, measured 2026-10-07), and every usable font
  is licensed; the OFL asks only that its text travel with the glyph
  files. Recommended: keep an OFL file, and move from Noto to a font with
  no Google tie such as Inter (item 17), after a licence read and the
  owner's download.
- **Hosting costs, explained to the owner (2026-10-08; R2 prices as read
  2026-10-07, to re-check before signing up).** No server to run: the
  app reads its packs from storage, the full-version folder uses a local
  script, and the download host is R2 object storage. All 170 packs at
  z14, trimmed: about 2 GB (scaled from the three pilot cities against
  the 5.94 GB measured for stock z15 with 10 km), inside the 10 GB free
  storage; 10 million free reads a month (a download is 1 read, a site
  Travel view about 5); no egress charge. A domain, about $10 a year, is
  needed anyway (a TWA proves ownership through
  `/.well-known/assetlinks.json`; `r2.dev` is development only). A Worker
  only for Z/X/Y tiles (100,000 requests a day free, then $5 a month).
  Expected total: the domain alone until traffic is very large.
- **Open items, in order:** the full version as a renderer option (no business
  data, the hard line enforced by a check); white line casings and white
  station dots in Travel for the owner's screenshots; Protomaps' dark
  flavor in Travel; the Overview Business/Travel toggle (`app/`, branch
  only); the legend follow-up (re-enabled pins in Travel); a test of a
  non-Google font (item 17 below); the Free Worker against an R2 custom
  domain comparison (needs the owner's Cloudflare account and the
  Cloudflare terms read first).

### 2026-10-08 - The full version is the app's template: map content only; named route rows; station dots sized by zoom (owner)

- **Rule (owner, 2026-10-08): the full version is a template for the app,
  so it carries map content only.** No coverage statements, generic
  explanations or features shoehorned onto the map because this pilot has
  no surrounding app screens to hold them; those belong to the app's own
  UI (an info page, say).
- **Applied to the ferry rows:** the legend names the route itself ("Arno
  Boat", "Bac du Rocher des Doms") instead of a generic "Ferry"; what a
  dashed line or a ticked line means is for the app's info page. An
  unnamed route gets no row. `open_basemap["routes"]` is now
  `[(kind, name)]`, the name in English where OSM has one, else local.
  Re-shot: Florence's legend reads "T1 Leonardo, T2 Vespucci, Arno Boat";
  Avignon's "Tram T1, Bac du Rocher des Doms" (its crossing is too short
  for the on-map name, so the row carries it).
- **Cities with many ferry routes (Istanbul, Hong Kong, Sydney): a second
  palette, one colour per named route (owner, 2026-10-08).** The colours
  may sit close to transit line colours, since the dash already sets a
  ferry apart from the solid lines, and ferries almost never overlap
  transit (a ferry passing under a bridge that carries a line is the one
  case, and the basemap's ferries draw beneath the site's lines). Design:
  the palette's first colour is today's ferry colour (crimson on the
  site, blue in the full version), so one-ferry cities stay as they are;
  each route's legend row takes its route's colour; contrast is measured
  against the water tint and the other ferry routes, not the transit
  lines. The owner's example: Hong Kong with orange, yellow, green and
  purple dashed ferry routes (a yellow dash needs a deeper amber to read
  on the pale ground and the light-blue water; measured when Hong Kong is
  piloted). Built with the first multi-ferry city piloted, so it is tested
  on real routes.
- **Station dots sized by zoom (owner agreed, 2026-10-08).** Pilot pages
  (full version and the site's Travel view): one pass on zoom end sets
  every dot (and line width) from a zoom table, interchanges a step
  larger, each dot keeping a fixed invisible touch area of about 44 px so
  small dots stay tappable; measured on the largest network (Tokyo) before
  it is settled, and the table set on light and dark screenshots for the
  owner. The app: dots drawn in MapLibre with a zoom curve, recomputed per
  frame on the GPU, no pop during a pinch. The site's Business view stays
  as it is until the pilot proves the table (it is senior, and changing it
  re-renders 170 maps).

### 2026-10-08 - Ferries named and in the legend; line labels that follow the screen, station names, and a tap-a-line list (owner)

- **Ferries (owner: crimson stands out, so label it; a legend row under
  the transit lines).** Built, site Travel view and full version alike:
  each ferry and cable car is named along its route in its own colour
  (`travel_ferry_label`, `travel_aerialway_label`, from z12, the name in
  the pill's language), and the legend gains a row under the transit
  lines for each route kind the city's pack holds, drawn as the map draws
  it (ferry dashed, cable car a thin line with ticks), shown in Travel
  only. The kinds come from the build's pack summary
  (`open_basemap["routes"]`); the swatch colours are read from
  `travel_style.js`, so they cannot drift. In the pilot packs: Florence
  "Arno Boat", Avignon "Bac du Rocher des Doms", Mendoza none. Visible
  wording "Ferry" and "Cable car" is a proposal for review time.
  `check_travel_style.mjs` passes; `check_render_current` 170 of 170.
- **Line labels that stay on screen (owner, for the full version, no
  business data there):** each line's label follows the part of the line
  in view, like the macro map's pills, placed on pan and zoom and kept
  apart. To build in the Mendoza full page.
- **Station names on demand (owner, to consider):** a menu toggle; with a
  line highlighted its stations' names take the line's colour (a shared
  station takes the highlighted line's), otherwise a neutral colour. To
  build in the full page.
- **Tap a line to list its stations, in both directions (owner: likely
  the app only, since runs here are pilots):** north- and southbound, or
  east- and westbound. Passed to transit-globe.
- **Legend:** the owner asked to see it open in Travel to give feedback;
  shots sent (lines only, then the ferry row).

### 2026-10-08 - Packs stop at zoom 14; hidden features hidden in every layer, with a check; baselines kept (owner; built)

- **Zoom 14 chosen (owner, 2026-10-08)**, on the samples of the next
  entry: every pack is built `--maxzoom=14 --travel_trim=true`. Against the
  stock zoom-15 build that is 64-72% smaller (Mendoza 3.89 to 1.41 MB,
  Avignon 12.1 to 3.4 MB, Florence 18.1 to 6.1 MB).
- **Baselines kept (owner: "save those as baselines if we need to adjust
  the settings in the future").** `data/_basemap_build/baselines/
  zoom14_trim_2026-10-08/` (this worktree, gitignored, 119 MB): the nine
  packs (stock, trimmed, zoom 14, three cities) with SHA256SUMS, every
  trim and zoom screenshot and sheet, the offline test page with its
  libraries, fonts and the style as shot, the tools and the builder
  patch, and `BASELINE.md` (inputs, measurements, how to re-run). The
  2026-10-07 baseline given to the app was copied beside it from the
  session scratchpad. **Both must move with the basemap build before this
  worktree is removed.**
- **A hidden feature is hidden everywhere (owner, after Viale del Visarno:
  "ensure we have a check in place to fully hide accompanying
  graphics/labels for features we are removing").**
  - Structural: `travelStyle.HIDDEN` names what the Travel map hides per
    source layer (points of interest and land cover entirely; roads of
    kind rail or with a hidden `kind_detail`; county and locality lines;
    land use outside the kept kinds). A final pass applies it to EVERY
    layer reading that source layer, whatever its type (line, casing,
    label, one-way arrow, fill), so a layer added later inherits it.
  - Check: `scripts/check_travel_style.mjs <basemaps.js>
    [<TravelTrim.java>]` evaluates every layer's filter against 101
    hidden samples (each hidden kind with bridge, tunnel, one-way, link,
    shield and name variants) and 87 kept ones, in light and dark, city
    and world, site and full: every hidden sample must be rejected by every
    layer, every kept one drawn by some layer; an unknown filter operator
    fails. With `TravelTrim.java` it also requires the builder's lists to
    equal the style's. Passes. Run against a copy of the style with labels
    exempted from the rule, it fails 228 times, the Visarno label among
    them. The end-to-end gate stays the pixel test (Travel render of a
    trimmed and an untrimmed pack must match).
  - Its first run found a gap: dark mode kept 5.7.2's own land-use fills,
    which leave gardens, meadows, kindergartens and platforms undrawn. Dark
    now uses the same categories as light, in 5.7.2's dark colours (an
    INTERIM table until transit-globe's dark tints), which also closes the
    caveat of the trim entry: trimmed and untrimmed packs draw alike in
    dark.
  - Not yet in `scripts/check_all.py`: it needs `basemaps.js`, which the
    repo does not carry. Hooking it in (with a vendored copy, when the
    release self-hosts the libraries) is for landing time.

### 2026-10-08 - Zoom 14 against zoom 15: half the size again, little a rider would miss (measured, owner to decide)

- **Built** trimmed packs to zoom 14 (`--maxzoom=14 --travel_trim=true`,
  `build_z14.sh`; 2 min 10 s to 2 min 31 s, peaks 3.06 to 3.16 GB) and
  compared them with the trimmed zoom-15 packs, Travel style, on a 375 px
  phone at map zooms 14.5, 15.5, 16.5 and 17.5 (past a pack's top zoom
  MapLibre enlarges the last tiles):

  | | Zoom-15 pack | Zoom-14 pack | Smaller | Pixels differing at 14.5 / 15.5 / 16.5 / 17.5 |
  |---|---|---|---|---|
  | Mendoza | 2,836,140 | 1,414,249 | 50.1% | 0.23% / 2.16% / 1.99% / 1.04% |
  | Avignon | 8,431,735 | 3,418,524 | 59.5% | 0.06% / 2.91% / 1.92% / 1.68% |
  | Florence | 12,857,973 | 6,078,083 | 52.7% | 0.14% / 1.79% / 1.71% / 1.43% |

  Against the untrimmed zoom-15 packs that is 64-72% smaller in all
  (Mendoza 3.89 to 1.41 MB, Avignon 12.1 to 3.4 MB, Florence 18.1 to 6.1
  MB). No errors in 24 views.
- **What differs, by eye** (sheets `shots/zoom/zoom_sheet_<city>.png`):
  buildings come as merged blocks rather than single outlines (the app's
  rules already chose merged blocks); small features drop out (swimming
  pools, tiny land-use patches); street names sit in slightly different
  places, a few more of them shown. Roads, parks, water, platforms and
  every label class stay.
- **Recommendation: stop the packs at zoom 14.** Download size is the
  owner's priority, the differences are detail a transit rider does not
  read, and the app's rules leaned to a z14 stop. Owner to decide.

### 2026-10-08 - The build-time trim: packs 27-30% smaller, the Travel map unchanged to the pixel (built and measured)

- **What a pack carries that the Travel style never draws**, measured by
  re-encoding every tile without each group and re-compressing
  (`pack_trim_estimate.py`):

  | | Points of interest | Untinted land use | Hidden road details | Rail, county and locality lines | All |
  |---|---|---|---|---|---|
  | Mendoza | 12.0% | 9.3% | 3.5% | 2.2% | 26.9% |
  | Avignon | 6.2% | 14.2% | 8.5% | 1.1% | 29.9% |
  | Florence | 9.0% | 13.1% | 5.7% | 1.0% | 28.8% |

- **Built as one switch, `--travel_trim`** (owner: one switch or several,
  either; one chosen, since the rule is single, "keep only what the
  Travel style draws", and one switch means two outputs to test, not a
  grid). It skips the points-of-interest and land-cover layers, land-use
  kinds the style does not tint, roads whose `kind_detail` the style
  hides, the basemap's own rail, and county and locality lines. A new
  class `TravelTrim` holds the lists (kept in step with
  `pipeline/travel_style.js`) and four one-line checks call it, in
  `Basemap`, `Landuse`, `Roads` and `Boundaries`. Without the switch the
  builder is unchanged. The patch, 120 lines, is
  `data/_basemap_build/travel_trim.patch` (this worktree, gitignored; a
  copy in the scratchpad); where it lives for good is a hosting-time
  decision. The wards Tokyo and Seoul need later get their own
  `--keep_wards` override then, not now. The zoom stop is the builder's
  own `--maxzoom`.
- **Measured.** Packs: Mendoza 3,893,127 to 2,836,140 bytes (27.2%
  smaller), Avignon 12,127,090 to 8,431,735 (30.5%), Florence 18,133,238
  to 12,857,973 (29.1%); builds about a minute faster (about 2 min each),
  peaks unchanged (3.24 to 3.38 GB). Travel-style screenshots of trimmed
  and untrimmed packs at z11, z13 and z15 in all three cities: **0.0000%
  of pixels differ**, no errors. The first run differed at Florence z15
  by one street name: the style hid service roads but still drew their
  names, so "Viale del Visarno" floated over nothing on the untrimmed pack.
  The style now hides the labels of hidden roads too, which the trim had
  already done.
- **Caveat: the dark flavor.** It keeps 5.7.2's own land-use fills until
  the app's dark tints arrive, and some of those (grass, military) are
  trimmed, so a dark Travel map from a trimmed pack shows fewer green
  areas than from an untrimmed one. The dark tints should follow the light
  categories.
- **Next: the zoom stop** (owner: look at z14 against z15 soon). z15 alone
  is 51-56% of each untrimmed pack.

### 2026-10-08 - The label-language pill built; smaller packs made a priority (owner; built and measured)

- **The pill (owner approved the design, 2026-10-08).** `OpenBasemap`
  takes `local_lang` (the city's language as Protomaps names it: "es",
  "ja") and `local_name` (the pill's text, default the code in capitals);
  `label_lang` is gone. Labels are English by default; with `local_lang`
  set, a two-button `EN | ES` pill (a Leaflet bar, 40 by 34 px buttons,
  the chosen one dark) appears under the layer menu while Travel is on and
  is removed with it, so the Business view never shows it. The choice is
  kept in localStorage `expanded-heatmap-labels` ("en" or "local"), and a
  switch calls MapLibre's `setStyle` on the same pack: nothing is fetched.
  It sits top left, stacked under the layer menu: in the top-right corner
  the fixed Dark mode button covered it and took the phone's taps
  (measured, then moved). Tested on Mendoza (`lang_check.mjs`), desktop
  mouse and phone touch: absent in Business; English by default; one tap
  to Spanish (the label fields switch from `name:en` to `name:es`);
  remembered across a reload; gone in Business; back to English; no
  errors. Attribution check clear at 375x812 and 1280x800;
  `check_render_current` 170 of 170. Mendoza's labels read the same either
  way, since few of its features have an English name in OSM; the Tokyo
  test of 2026-10-07 shows the switch changing scripts. The owner expects
  the same toggle in the app.
- **Download size is a priority (owner, 2026-10-08), and builder changes
  are acceptable.** A pack still carries what the Travel style never
  draws (Mendoza's holds about 20,000 points of interest, all of its
  `residential`, `farmland`, `grass` and other untinted land use, and the
  road kinds the style drops). The next step measures each layer's share
  of the bytes, then trims at build time only what the style does not
  draw. Anything trimmed comes back by rebuilding with it left in (about 3
  minutes a city; packs are rebuilt on every refresh anyway), so a trim
  locks nothing in (owner).

### 2026-10-08 - Which surface yields in a clash; the Travel style questions answered; Avignon and Florence self-built (owner; measured)

- **Precedence between the surfaces (owner, 2026-10-08).** The site is
  senior to its Travel view: where they clash (a colour against the
  business pins, say), the Travel view makes the compromise, never the
  site. The full version competes with neither; it runs mostly parallel
  to the site's Travel view, but the compromises that view needs do not
  carry over. A choice made on its own merit can serve both: the plum
  station-area border stays in both because it reads better, not only
  because it clears the pins (owner). Built as `variant: "site"` (the
  default, used by `OpenBasemap`) and `variant: "full"` in
  `travelStyle()`.
- **The questions of the previous entry, answered (owner, relayed by
  transit-globe, 2026-10-08).**
  1. `unrecognized_region` and `unrecognized_macroregion`: dotted, the same
     neutral rule as `unrecognized_country`. Done.
  2. World map, country lines only: kept.
  3. Tighter dots, judged on screenshots: `[0, 3]`, `[0, 2]` and
     `[0, 1.5]` compared on world-zoom crops of Kashmir, Crimea and Cyprus,
     and the Horn of Africa; only `[0, 1.5]` (1.5 px dots 2.25 px apart
     centre to centre) keeps short segments reading as a line. Set.
  4. Aerial lift recoloured: by the same CIE76, the burnt orange #d84315
     sat 8.3 from the tram city-dot colour #c2410c (under the hard floor
     of 10) and 19.3 from Tokyo's Marunouchi red (transit-globe's
     measurement). Lifts are now told apart by pattern, the cartographic
     thin dark line (#444444) with cross ticks from zoom 13; no pilot pack
     has a cable car, so the ticks are checked for style errors only, not
     yet seen on screen. Ferries stay dashed: crimson #b0004f in the site
     variant (fine by the owner: 42.8 from Marunouchi red, 51.6 from JR red
     #e60012), and in the full variant, which has no pins, blue #1e88e5,
     chosen as at least 50 from everything the full version draws (51 from
     the plum border, 57 from the water tint).
  5. Label language, decided (owner, 2026-10-08): **English by default in
     every city, with a toggle to the local language**, on the site's
     Travel view and the full version alike; consistency matters and most
     readers need English. No extra downloads: a pack carries every name a
     feature has in OSM (`name` plus `name:en`, `name:es` and the rest),
     and the style picks one when it draws, as measured on 2026-10-07 (the
     same Tokyo pack drawn in Japanese and English, the same Mendoza pack
     in Spanish and English). Where OSM has no English name the label
     falls back to the local one. So one pack per city serves both, and
     the toggle restyles labels without fetching anything.
- **Railway land is not tinted (owner, 2026-10-08).** In Florence, OSM's
  railway-land polygons along the Pisa line overlap the Cascine park, and
  the first draft painted them lavender over the park. The owner: the rail
  corridor runs the full length of each line, the lines already get their
  own colour treatment, and the lavender was meant for station areas and
  their walksheds, so the corridor needs no tint, and with no tint no
  overlap rule is needed. Railway land is dropped from the tints; lavender
  is left to platforms (#c3b8de) and, once drawn from the export, station
  areas; #d6cfe8 is retired. Re-shot: Avignon and Florence at z13 and z15,
  no errors, no lavender corridors.
- **Grass stays plain (owner, 2026-10-08).** The racecourse under the Pisa
  line is OSM `grass`, which 5.7.2 paints park-green. A pale grass tint
  from z13 was proposed, with road verges dropped as detail past what a
  transit rider needs; the owner then set the bar: a nice-to-have only if
  it brings no conflict and no busier basemap. It fails the first test.
  - Every pale green tried between the earth tone and park green sat 4.7
    to 8.3 (CIE76) from the cemetery, wild-land or earth tint, under the
    floor of 10, so it would be one more shade readers cannot tell apart.
  - Verges cannot be told apart in the tiles (grass carries only `kind`);
    dropping them needs a builder change. It was written and compiled
    (grass under 1,000 m2, or a strip under 10,000 m2; grass under 1,000
    m2 is about three quarters of the pieces and 9-19% of the grass area
    in Mendoza, Avignon and Florence), then reverted: a modified builder
    is upkeep for non-transit detail, and an unmodified one keeps the
    packs identical to Protomaps' open-source output. The patch is kept
    in the scratchpad (`builder/Landuse_verge_filter.java`).
  Parks keep their green; grass, like pitches and farmland, stays plain.
- **Avignon and Florence built from the owner's extracts** (Geofabrik
  `provence-alpes-cote-d-azur-261006`, 390,142,851 bytes, sha256
  b02b440e...eaa226d; `centro-261006`, 384,646,965 bytes, sha256
  ff41ffef...9b01a50), each box the stations' extent plus 10 km in the
  city's UTM zone (the same method gives Mendoza's box within about 1 km):

  | | Box | Time | Peak | Size | Index estimate (planet build, 2026-10-07) |
  |---|---|---|---|---|---|
  | Mendoza | -68.9700,-32.9960,-68.7260,-32.7670 | 3 min 18 s | 3.27 GB | 3.89 MB | 4.13 MB (extracted, measured) |
  | Avignon | 4.6724,43.8408,4.9690,44.0305 | 2 min 41 s | 3.39 GB | 12.1 MB | 17.5 MB |
  | Florence | 11.0707,43.6765,11.3906,43.8904 | 2 min 17 s | 3.13 GB | 18.1 MB | 20.7 MB |

  The two estimates are for a slightly larger box and include the world's
  low zooms and land cover, so the sizes compare only roughly. Both packs
  render offline in stock and Travel style at z13 and z15 with no errors
  and no outside requests; neither carries a disputed line. Every build
  so far peaks between 3.1 and 3.4 GB under `-Xmx5g` and takes under
  3.5 min; Natural Earth's read is about half of each.
- **Store decisions from transit-globe that touch this repo (owner,
  2026-10-08; store requirements unverified).** Android first, Apple
  later, the PWA at the core. (1) Packs are never bundled into an app
  binary (ODbL 4.7, no technological protection); they stay separate,
  free downloads, so if a Worker serves Z/X/Y tiles the raw `.pmtiles`
  stay downloadable from the shared hosting with a plain public offer.
  (2) A TWA proves site ownership through `/.well-known/assetlinks.json`
  on the PWA's own domain, which favours an owned domain over
  `workers.dev` in the hosting choice. (3) An iOS version may need
  MapLibre Native: `travelStyle()` returns plain style-spec JSON (legacy
  filters, dash arrays, round caps), all supported there, so a build can
  write it out as `style.json`. (4) Each project hosts its own privacy
  page. (5) The export contract is unchanged.

### 2026-10-08 - The shared Travel style built as one filter; disputed lines dotted, world map label-free (built, owner to review)

- **Built (branch only).** `pipeline/travel_style.js`, one function that
  turns the layer list of @protomaps/basemaps 5.7.2 into the Travel style:
  `travelStyle(layers, {flavor, world})`. `pipeline/map_common.py` inlines
  it into the OpenBasemap layer, so the site's Travel view uses it now; the
  full version and transit-globe take the same file as their reference.
  Maps without `open_basemap` are unchanged (`check_render_current`: 170 of
  170 current; the Business render carries no Travel code).
- **What it does, per the app's rules** (previous entries):
  - Drops land cover, points of interest, road shields and the basemap's
    own rail; drops service roads, driveways, parking aisles, alleys,
    tracks and drive-throughs (matched on `kind_detail`, in whichever
    filter syntax each layer already uses, since MapLibre cannot mix the
    two); fades tunnels and taxiways to half opacity.
  - Land-use tints in the light flavor: earth #e2dfda; parks #a8d5b5
    (park, garden, golf course, playground, allotments, village green,
    recreation ground); wild land #c2d8b0 (national park, nature reserve,
    protected area, forest, wood, scrub, grassland, meadow, wetland, heath);
    cemetery #cad3c7; beach and sand #ece3c6; other natural #d9d5cc (bare
    rock, glacier, scree, shingle); institutions #e7dbd7 (hospital, school,
    university, college, kindergarten); aerodrome #d8dae1, runways
    #c3c6cf; railway land #d6cfe8 and platforms #c3b8de. Industrial, zoo,
    business kinds, pitches, grass, farmland and `other` stay plain.
  - Boundaries: settled country lines as 5.7.2 draws them; region lines
    only (county and locality lines, which become wards per city later,
    are off); **every line the builder flags `disputed`, or of kind
    `unrecognized_country`, moves to its own layer**: #c4c4c4, 1.5 px,
    round-cap dots (`[0, 3]`: 1.5 px dots 3 px apart), directly above the
    country lines, at every zoom.
  - Ferries (`kind=ferry`) and cable cars (`kind=aerialway`), which 5.7.2
    does not draw, get their own layers: ferries dashed crimson #b0004f,
    lifts solid burnt orange #d84315. Measured with `delta_e`: every blue
    tried sat under 45 from Retail blue or the backup teal; #b0004f is 59
    from the plum border and 63 from violet, #d84315 72 from olive.
  - `world: true` keeps only background, earth, water, country lines and
    the disputed layer: no country, sea or place names (owner, 2026-10-08).
- **Measured** (headless Edge, 375 px phone, offline page, Mendoza pack):
  no style errors and no outside requests at any zoom step, stock or
  Travel, light or dark; the self-built pack draws exactly what the
  downloaded one does under the Travel style. On the downloaded pack's
  world tile, the world view draws **29 disputed segments dotted, none left
  on the settled layer, zero labels**; crops show Kashmir's lines, the
  Crimea isthmus, Cyprus's Green Line and the Somaliland lines dotted where
  5.7.2 drew them solid. The half version (re-rendered Mendoza with the
  style) passes `travel_check.mjs` on desktop and touch unchanged; the
  attribution check passes at 375x812, 390x844, 360x740, 1280x800 and
  1440x900 with Travel selected (a 600 px tall viewport cannot hold the
  650 px map, so it reports unmeasured, not breached). Node checks of the
  rules: `style_test.mjs` in the scratchpad.
- **For the owner (and the app) to decide:**
  1. Kinds `unrecognized_region` and `unrecognized_macroregion` are neither
     region nor disputed under the decision's wording, so they are not
     drawn at all. Draw them dotted too?
  2. The world map keeps country lines only, no region lines. Keep?
  3. At world zoom a short disputed segment gets only a few dots; `[0, 2]`
     (dots 3 px apart centre to centre) reads denser. Keep `[0, 3]`?
  4. Ferry crimson and lift orange are drafts chosen by measurement, not
     taste.
  5. The site's Travel view prototype labels in Spanish (`label_lang`
     "es", local language first, as OSM's tiles do); the app's rule is
     English over the local script. Same rule on the site?
- **Not in the tiles:** station-area polygons. The builder writes no
  station kind, so the plum-bordered station areas need the export's
  platforms and exits (a footprint) or a builder change; deferred to the
  full version. The dark flavor gets the structural rules only (drops,
  filters, disputed layer); its tints wait for the app's dark drafts.

### 2026-10-08 - The self-built Mendoza pack draws the same map as the downloaded one (measured)

- **Built** with Protomaps' open-source builder (protomaps/basemaps main,
  planetiler 0.10.2, basemap 4.15.2) from the owner's local inputs and the
  two empty stand-ins, through the memory gate: `--area=argentina
  --bounds=-68.9700,-32.9960,-68.7260,-32.7670 --maxzoom=15`, `-Xmx5g`.
  **3 min 18 s** (12 min CPU), of which reading Natural Earth was 2 min, a
  fixed cost a larger build shares; **measured peak 3.27 GB** (gate label
  `basemap-build-mendoza`). `download=false` throughout: nothing fetched,
  no Protomaps host touched.
- **Same map.** Screenshots of both packs in the same offline page and
  style, at z9, z13 and z15 on a 375 px phone view: **0.00% of pixels
  differ**; rendered feature and label counts equal at every zoom step
  except one label at z12; no errors, no outside requests. Tile for tile,
  z9-15 match within 7 of 79,328 features at z15. The residue has two
  causes: a slightly older OSM snapshot (Geofabrik 2026-10-06 20:21 against
  the planet build's 2026-10-07 04:00), and the QRank stand-in, which makes
  a few points of interest (a university, an aerodrome, a peak) first appear
  one to three zooms later. The Travel style drops points of interest, so
  QRank does not matter there.
- **Size: 3,893,127 bytes against 4,129,904 (-5.7%).** The whole
  difference is at z0-8: with `--bounds` the builder keeps only features
  inside the box even in the world-scale tiles (z0: 3 features against 54),
  and the land-cover stand-in leaves no land cover. Same tile count (867).
- **Disputed borders.** The downloaded pack carries 39 boundary features
  flagged `disputed` at z0-3 (its world tile); the self-built one carries
  none, because of the same bounds clip. So a city pack built this way has
  no disputed line unless one crosses its own box, which agrees with the
  app's survey (previous entry), and the world pack must be built or cut
  from the whole world to carry the flags the dotted style needs.
- **Practical notes.** The output is named after `--area`
  (`argentina.pmtiles`, renamed `mendoza_selfbuilt.pmtiles`); `--output`
  is ignored. On Windows the gate needs an absolute path to `java.exe`.
  The builder logs 44,082 `osm_boundary_missing_way` errors, expected for a
  country extract whose boundary relations reach outside it.
- **What follows.** The self-build reproduces Protomaps' pack without
  Protomaps' hosts, QRank or the land-cover file, so the site and the app
  can share one build, and the Terms-of-Use question for scripted extracts
  falls away. Still to measure: Avignon and Florence (extracts first), and
  one world pack built whole for the label-free world map.

### 2026-10-08 - The travel app's basemap rules, shared by the Travel views (owner, via the app project)

- **Received from transit-globe, 2026-10-07/08, as the owner's choices for
  the full Travel version; the owner made one Travel basemap style shared
  by the full version and the site's Travel view (2026-10-08).** Method:
  try every change in the style first and make only the kept ones
  permanent at build time; measure each against the pinned Mendoza
  baseline; before anything is final, dark versions and a colour-blindness
  check of every tint, and z14 against z15 screenshots for the owner. Hex
  values are drafts.
- **Design rules.** Hierarchy, top to bottom: transit lines (cased) and
  station dots; station areas and platforms; labels (places, then
  streets); ferries and aerial lifts; roads (muted, few weights); land-use
  tints; land and water. "The basemap is context, never content." One tint
  per category, pale tints differing only by hue; transit owns the
  lavender family; operators' line colours never reused for areas or dots;
  the only saturated colours are transit (lines, the station-area border,
  ferries, lifts). Lines always carry a white casing (Ginza orange 1.6:1
  and Hibiya grey 1.5:1 against any light ground); station dots white with
  a dark ring (above 8:1 on every tint), interchanges larger. One look on
  every surface. Each feature is DECIDED, DEFERRED FOR SCOPE (with why,
  what would bring it back, and the decision) or EXCLUDED BY RULE. Mobile
  first: every kept feature justifies its bytes on a phone; the build
  machine pays, never the reader.
- **Layer choices.**
  - pois: dropped (a few landmarks may return later).
  - landcover: dropped everywhere (empty stand-in); the world map is plain
    land, sea and borders, so the city dots are the only colour.
  - landuse: business kinds dropped (cafe, grocery, supermarket, hotel,
    post_office). Earth #e2dfda. Parks #a8d5b5; wild land #c2d8b0;
    cemetery #cad3c7; beach and sand #ece3c6; other natural kinds #d9d5cc;
    institutions #e7dbd7; railway land #d6cfe8 (tint only); platforms
    #c3b8de; station area the same tint with a 3 px border #7e6fb0 (from
    OSM station-area polygons or a footprint around the export's platforms
    and exits; to be tested); aerodrome #d8dae1, runway #c3c6cf, taxiway
    faint; built-up, attractions and `other` plain.
  - boundaries: country and region; wards per city where useful (Tokyo,
    Seoul first); disputed borders decided below. In the builder, OSM
    admin_level 6 becomes kind `county` (from z8) and 7 or 8 `locality`
    (from z10), so Seoul's gu (level 6) and Tokyo's special wards (level 7)
    are different kinds and need their own ward settings.
  - roads: fewer, muted colours; service, driveway, parking_aisle, alley,
    track and drive-through dropped; road numbers and shields dropped to
    start; steps, corridor and pedestrian kept; basemap rail hidden to
    start; sidings, yards, crossovers, miniature and preserved dropped
    (scenic lines drawn from the export's `scenic` exclusions as a marked
    category); ferries and aerial lifts kept and prominent; tunnels faded.
  - buildings: merged blocks only (z0-14); favours a z14 stop, for the zoom
    review.
  - Excluded by rule in the app: business data, routing beyond the owner's
    line, land cover, QRank, and any download from Protomaps' hosts
    (build.protomaps.com, r2-public.protomaps.com).
- **Measured against the site** (CIE76, see the next entry): the draft
  station-area border #7e6fb0 is 24.7 from Retail blue and 26.5 from the
  planned violet, below the project's preferred 45; suggested to the app
  that the border sit at least 45 from the site's pin colours.
- **Border decided (owner, 2026-10-08): dark plum #352a4d in both
  projects**, replacing #7e6fb0. Re-measured here with
  `pipeline/linecolour.delta_e`: 46.7 from Retail blue, 47.5 from the
  violet, 49.5 from teal, 84.8 from olive (all above the preferred 45),
  24.3 from the station dots' ring #333333, 65.4 from the lavender tint.
  The owner compared both on mock station scenes with pins off and on. Tint
  #d6cfe8 and platforms #c3b8de stand; the 3 px border goes on station
  areas only, never on rail corridors; dark mode gets its own border,
  drafted by the app with its dark tints. So the site's pin colours stay as
  decided, and Cleanup's re-render needs no change for this.
- **The shared style is the app's starting point, not a binding (owner,
  2026-10-08).** The full Travel pilot will not be updated once the app is
  under way; the app may depart from it, recording each departure and its
  reason in its own DECISIONS.md.
- **Disputed borders and the world map (owner, 2026-10-08, relayed by the
  app).**
  - One neutral style everywhere: every disputed segment drawn as a lighter
    dotted grey (draft #c4c4c4, 1.5 px, round-cap dots about 1.5 on, 3
    off), distinct from the settled border's dash, on the world map and in
    every city. No claim is favoured.
  - "Disputed" is the builder's `disputed` flag (`Boundaries.java`,
    protomaps/basemaps main): Natural Earth at z0-5 (featurecla "Disputed
    (please verify)", "Indefinite (please verify)", "Indeterminant
    frontier", "Line of control (please verify)"); OSM at z6+
    (boundary=disputed or claim, disputed=yes, disputed_by, claimed_by);
    plus kind `unrecognized_country` (Unrecognized, Breakaway, Claim
    boundary).
  - Confirmed here in @protomaps/basemaps 5.7.2 (the site's Travel view):
    the `boundaries_country` layer filters on `kind_detail <= 2` alone and
    never reads `disputed`; every such line is solid below z4 and dashed
    [2,1] in #adadad from z4. So disputed lines look settled today, in the
    site's Travel view as well as the app's; the shared style filter has to
    add the dotted layer before either goes public.
  - World map label-free: no country or sea names; only land, sea, borders
    and the city dots. City and country names appear only in the dot's
    tooltip and the UI, taken from the export, so every surface uses the
    site's existing naming choices (Taiwan's cities, Hong Kong).
  - Inside city packs, OSM's names unchanged, English over the local
    script. The app reports that none of the 170 cities has a disputed land
    border within its pack extent (Tbilisi is closest; the South Ossetia
    line lies outside it); not re-measured here.
  - About statement, following OSMF's wording: borders and names follow
    OpenStreetMap's on-the-ground practice and imply no position on any
    dispute. The app reads the OSMF policy PDF
    (osmfoundation.org/wiki/File:DisputedTerritoriesInformation.pdf) before
    citing it.
  - Ruled out: a worldview per reader's country (the server would have to
    know where the reader is, against the app's privacy rule). A local view
    per city pack was offered and not chosen.
  - Open for the owner: the site's Overview stays on CARTO (decided
    earlier), whose world map carries country and sea names, so the
    Overview's Travel toggle would not be label-free unless it moves to the
    open world pack.

### 2026-10-08 - Decisions for going public (owner, one pass)

- **12. Hosting:** compare the free Worker (workers.dev) with R2 behind a
  custom domain, live, before choosing (owner). Needs the owner's
  Cloudflare account and the Cloudflare terms read first.
- **13. Packs treated as an ODbL database: yes, and it applies to the app
  too** (the app ships packs to devices: ODbL in the pack metadata and a
  README, a free download offer, no encryption or restriction, ODbL 4.7).
- **14. Separate files per source within each city** in the export: yes.
- **15. Exports as release files in this repo for now; move if needed.**
  The app builds its own packs; what it reads from here is the export
  (stations, lines, exits, notices, dates).
- **16. Notices into a data file: yes, if it conflicts with nothing.** It
  touches `app/components.py` (a deploy and a reboot) and
  `scripts/check_provenance.py`, which parses `_NOTICES` from source, so
  both move together, at review time.
- **17. The Noto trademark line: yes, unless a non-Google font avoids it,
  especially for the app.** To test in the pilot: an OFL font from outside
  Google (Inter for Latin, Greek and Cyrillic is a candidate) turned into
  glyph files with maplibre/font-maker, with its own licence read; CJK
  already comes from the device's fonts.
- **18. Notice 1's privacy text: drafted at review time** (owner: "this is
  important to get right"). App implication: the app writes its own
  privacy text for whatever its packs and exports are fetched from.
- **19. Whether the half version goes live: after the pilot,** weighing
  the legal findings together.
- **The stray file** `neutral-comment-style.md` in the main checkout is
  Cleanup's own, from a code audit; Cleanup to file it.

### 2026-10-08 - Pilot decisions (owner, one pass)

- **Maven compile:** this session runs it, quietly (owner).
- **Full version:** an option on the shared renderer, not a fork (owner).
- **Pilot cities:** Mendoza, Avignon, Florence (owner). Each needs its own
  regional OSM extract, downloaded by the owner: Avignon
  `europe/france/provence-alpes-cote-d-azur-latest.osm.pbf` (390 MB),
  Florence `europe/italy/centro-latest.osm.pbf` (385 MB); Mendoza's is in
  place. Pack sizes (2026-10-07 index read): Avignon 3.7 MB at map extent,
  17.5 MB with 10 km; Florence 7.2 MB and 20.7 MB.
- **One Travel basemap style** shared by the full version and the site's
  Travel view, on the travel app's rules (hierarchy, one tint per category,
  transit owns lavender, only transit saturated, business kinds dropped);
  **no land-cover shading** in the site's Travel view either (owner).
- **Yes to:** white line casings and white station dots tried in the site's
  Travel view only, with screenshots for the owner; Protomaps' own dark
  flavor for Travel in place of the invert filter (the app may use it too:
  BSD-3 style code, CC0 design, MIT sprites, OFL fonts, none from
  Protomaps' servers when taken from the npm package or the GitHub repo);
  solid macro dots in Travel; a Business/Travel toggle on the Overview
  (CARTO stays) passing the choice into city maps; the coverage stat as a
  plain-words note in the pilot and **exact numbers from the export in the
  final version** (owner).
- **The violet clash, measured** (CIE76, `pipeline/linecolour.delta_e`, the
  project's own measure; PREFERRED 45, HARD_FLOOR 10): against the travel
  app's draft station-area border #7e6fb0, the planned "Shops and services"
  violet #7e57c2 is 26.5 and today's Retail blue #2a78d6 is 24.7; the
  backup teal #37786e is 54.3, olive #737a00 93.8. So changing the violet
  alone would not separate the pins from Travel's lavender; the border is a
  draft and is the cheaper lever. Recommended: keep the site's pin colours,
  ask the app to place its border at least PREFERRED (45) from the site's
  pin colours, and tell Cleanup before the pin re-render lands (owner's
  option of a proposal to Cleanup).

### 2026-10-07 - The pilot adds a self-built pack test (owner)

- **Why.** protomaps.com's Terms of Use forbid "automated means to access
  the Site" without written permission, while Protomaps' guide instructs
  scripted extracts from build.protomaps.com. The travel app's owner chose
  to build its packs from OSM with Protomaps' open-source builder. This
  repo's prototyping so far is a few manual, owner-approved extracts, the
  use Protomaps documents, and continues on that basis; a SCHEDULED build
  of 170 cities would be automated. Asking Protomaps is outreach, which
  comes after the methods this project controls (owner's standing rule), so
  the pilot tests building the packs here (owner, 2026-10-07). If it works,
  the site and the app can share one build, which also keeps their figures
  comparable.
- **What the builder needs** (read from `tiles/src/main/java/.../Basemap.java`
  and `pom.xml` in github.com/protomaps/basemaps, 2026-10-07; sizes by HEAD
  request):

  | Input | Host | Size | Licence read |
  |---|---|---|---|
  | OSM extract (`--area`, Geofabrik name, or a local file) | download.geofabrik.de (Argentina: `south-america/argentina-latest.osm.pbf`) | 432 MB | **permitted**: ODbL only, nothing beyond the OSM credit; scripted downloads fine with a no-repeat guard ("Download responsibly!", 2025-09-10); "-latest" redirects to a dated file; dated daily files are deleted, so a 4.6 offer names a monthly or yearly file or keeps a copy; never the login-only "internal" extracts |
  | Water polygons, land polygons | osmdata.openstreetmap.de | 931 MB + 952 MB | **permitted**: ODbL, the OSM credit covers it; automation allowed, conditional requests asked ("we might suspend the service" on abuse); keep the cached zips between builds |
  | Daylight landcover | r2-public.protomaps.com (a Protomaps host) | 36 MB | **data permitted with ESA's credit** (CC BY 4.0, prescribed wording; plus Daylight's ODbL umbrella, probable); **the Protomaps host carries the Terms-of-Use ambiguity again**; the original publisher's frozen copy is live at `daylight-openstreetmap.s3.us-west-2.amazonaws.com/landcover/low.{shp,dbf,shx,prj}` (34.5 MB, 2023-10-05, Daylight sunset 2024) and would need converting to GeoPackage |
  | QRank (POI ranking) | qrank.toolforge.org | 106 MB | **data CC0; the host's Wikimedia Cloud Services end-user terms carry an open-ended indemnity**: an owner decision. Used only to set each POI's first zoom; no QRank data in the tiles. Not updated since 2024-03-16 |
  | pgf-encoding (script names) | wipfli.github.io | 0.8 MB | **permitted**: what reaches the tiles is CC0 (encoded Devanagari names, two metadata keys); the zip's MIT code and OFL fonts are not passed on |
  | Natural Earth | naciscdn.org | 446 MB | done: public domain, no credit needed |
  | Java 21 JDK (Eclipse Temurin 21.0.12.1, portable zip, no install) | github.com/adoptium | 205 MB | a tool, not shipped |
  | Maven 3.9.16 (portable zip) | dlcdn.apache.org | 9 MB | a tool, not shipped |

  About 3.1 GB in all, into the scratchpad or a gitignored `data/` folder,
  never committed. The Java build runs through `scripts/heavy_job.py` with
  an estimated peak, since no Java run has been measured here.
- **Downloads by the owner, not this session** (owner, 2026-10-07: "send
  links to me so as to not draw up usage"). Files go into the gitignored
  `data/_basemap_build/` of this worktree (created empty). Compiling the
  builder makes Maven fetch its libraries from Maven Central, the one step
  that cannot be done by hand: the owner runs it or approves it.
- **Recommended for the pilot, owner to confirm:** skip QRank and the
  landcover layer by giving the builder empty stand-in files made locally
  (no download, no Toolforge or Protomaps terms, no ESA credit). Costs: POI
  labels appear at slightly different zooms than in Protomaps' build, and
  low zooms lose their land-cover shading. Either can come back later (the
  original Daylight shapefile with ESA's credit; QRank with the owner's
  acceptance of the indemnity).
- **QRank: downloaded once in error, never used, deleted; resolved (owner,
  2026-10-07).** The owner's manual downloads included `qrank.csv.gz`
  (105,533,721 bytes) by mistake. It was moved out of the build inputs the
  same evening, never opened, never built from, and deleted by the owner;
  nothing derived from it exists. The owner's call: no terms were breached
  and no liability follows from a mistaken, unopened download that is not
  in the project. The pilot builds with an empty stand-in for QRank, as the
  travel app does.
- **The inputs in place** (`data/_basemap_build/data/sources/`, owner's
  downloads, 2026-10-07): `argentina.osm.pbf` (Geofabrik
  `argentina-261006.osm.pbf`, the dated file "-latest" redirected to;
  432,349,104 bytes, sha256 d23c0242...c5021f14), the water and land
  polygons, Natural Earth and pgf-encoding, sizes matching the publishers'
  exactly. Land cover and QRank: empty stand-ins, made locally.
- **What the test measures:** that a self-built Mendoza pack draws the same
  map as the downloaded one (same style, same view; screenshot and rendered
  feature counts), its size against 4.13 MB, the build's time and peak
  memory, and whether the build runs without the Protomaps-hosted landcover
  file.

### 2026-10-07 - The half Travel version built and tested on Mendoza; macro-map Travel tooltips (owner)

- **Built (commit cc1a3b04, branch only).** With `open_basemap`, the base
  layers are "Business" and "Travel". `TRAVEL_MODE_SCRIPT`, a conditional
  block, takes the pins, both heat layers and the rings off the map when
  Travel is picked, folds the legend to its lines, keeps every layer in the
  menu, restores the render-time defaults on Business, and remembers the
  viewer's choice (localStorage). Two defects found and fixed on the way:
  changes made inside the layer menu's own click were undone or left stale
  ticks (now deferred until the click is handled), and with the Travel
  layer alone Leaflet.markercluster threw "Map has no maxZoom specified"
  when a pin layer was turned back on (the Travel layer now registers its
  zoom range as tile layers do). A first legend wrap edited LEGEND_HTML's
  fixed text and `check_render_current.py` caught it; the wrap now sits in
  the slot only.
- **Tested** (headless Edge, desktop mouse and 375 x 812 touch, no console
  errors): Travel clears pins, heat and rings and the legend's business
  section, with lines kept; the line highlight works by hover and tap in
  Travel; a business layer turned back on from the menu draws; Business
  restores pins, in-ring heat and the business legend; a reload reopens in
  Travel. The full interaction suite (line highlight, station names,
  legend, line label, credit, drag, Global View) and the credit check at
  375 x 650, 375 x 812, 1280 x 650 and 1280 x 900 pass on both base layers.
  Without `open_basemap` Mendoza still renders identical to the committed
  map, and all 170 committed maps pass `check_render_current.py`.
- **Small follow-up:** a business layer turned back on in Travel draws, but
  the legend's business section stays folded until Business is picked.
- **Macro-map tooltips in Travel (owner, 2026-10-07), the same in the
  website's Travel view, the full version and the mobile app:** dots keep
  their transit-type colors (metro, light rail, tram); the tooltip reads the
  city name, the transit type, a "transit coverage" stat only where the
  rail data limits coverage, then the number of lines and stations if there
  is room. No storefront counts. Messaged to the app project.
- **Measured for the coverage stat** (the committed maps and
  `excluded_stations.csv`, 2026-10-07): 54 of 170 cities list no station
  left out; 116 list some: beyond the city limits 111, thinned for spacing
  10, closed for works 5, under the 15-minute test 3. Those files are not a
  clean coverage measure: Japanese cities list only stations within 3 km of
  the city line, and lines left out whole (commuter rail, stubs, scenic
  lines) are not counted at all. Lowest shares drawn: Anyang 7 of 113,
  Melbourne 17 of 216, Sydney 16 of 173; Mendoza 7 of 25, Washington 40 of
  98.

### 2026-10-07 - Two travel versions for the pilot, "full" and "half"; no business or ring layers in the full one (owner)

- **The owner's split, both piloted off the live site:**
  - **Full travel version, offline only.** The Travel basemap with stations,
    lines, labels, the line highlight and the OSM credit, and no business
    data at all. It is the reference handed to the travel app, and the
    version that warrants the out-of-scope call for this website.
  - **Half travel version, website scope.** The basemap changes and the
    business pins, the heat and the rings default to OFF; all stay in the
    layer menu.
- **Hard line (owner): a full travel version on the new basemap never lists
  concentric rings or a business heat layer as layer-menu items**, and
  draws no business pins. Messaged to the app project the same day.
- **Recommended implementation** (for the owner to confirm before code):
  the full version takes NO business data at all, so the register data
  cannot reach its HTML by any path: `render_heatmap(businesses=None)` (or
  a flag that refuses businesses) skips the heat, the rings, the pins and
  the legend's business section, and a check refuses a full-version file
  that contains a ring, heat or business layer name. The half version is
  the switch plus a few lines of map script: picking "Travel" unchecks the
  pins and heat (rings are already off by default, owner 2026-09-21) and
  the legend shows lines only; picking "Business" restores the business
  defaults. The half version's page still carries the register data, so
  its notices and obligations are unchanged.
- **Agreed (owner): in Travel the legend shows lines only.**
- **Required (owner): the macro-map to city-map chain also exists in the new
  format** (the Global View leads into city maps and back). Measured for it,
  2026-10-07, dry runs on the 20261007 planet build: a world pack is 6 MB at
  zoom 0-4, 15 MB at 0-5, 45 MB at 0-6 and 189 MB at 0-7. The landcover
  layer (ESA, CC BY 4.0) lives at exactly these zooms, so a macro map on the
  new basemap needs ESA's credit or a style without that layer. The site's
  Overview is pydeck with CARTO's style, and pydeck cannot register the
  pmtiles protocol, so a Travel Overview on the site needs ordinary Z/X/Y
  tile URLs (the Cloudflare Worker route) rather than raw range reads.

### 2026-10-07 - The open basemap works offline; three licence reads; repeat visits favour it; "Business" and "Travel" (owner)

- **Owner decisions, 2026-10-07.** The switch is B (Standard default), D (Open
  only) is out for good, and C (Open default) is a later option for phones
  if the open basemap earns it. A focused pilot goes ahead (3-5 cities,
  self-hosted assets, a travel style, pack builds, R2, real-phone figures),
  kept off the live site. The names are **"Business"** and **"Travel"**.
  The travel view is meant to HIDE the business layers, so it is a map MODE,
  not only a basemap; whether that mode belongs on this site at all, or only
  in the app (with the switch declared out of this site's scope), is open
  for the owner, and the names on this site wait on it.
- **Offline, measured.** A MapLibre-only page (as the app would build it)
  with every library, font, sprite and pack served locally, and every
  request to any other host failed as "internet disconnected": Mendoza
  (Spanish labels; English on the dark flavor) and a 1 km Tokyo patch
  (2.56 MB; Japanese and English labels), each zoomed to 10, 12, 15 and 17
  and panned. **No request left the machine, no errors, every step drew**,
  including zoom 17 beyond the pack's 15. Three findings for whoever builds
  on it:
  - The three Noto fonts the style uses (11.1 MB in all; sprites 0.15 MB)
    have no Han or Hangul glyphs (those range files are empty) and only
    Regular has kana. MapLibre drew the Japanese from the device's own fonts
    (its `localIdeographFontFamily`), so CJK cities depend on the device;
    which glyph forms a reader sees then follows the device's fonts (the
    cjk-text skill's Han-unification problem), untested on real phones.
  - With `lang: "en"`, the default style already labels **English over the
    local script** ("MARUNOUCHI 1" over 丸の内一丁目), which is what the app
    wants.
  - MapLibre's attribution control showed **nothing**, although the pack's
    metadata carries `© OpenStreetMap`: the credit must be set explicitly
    (the site's outer layer already does).
- **Repeat visits, measured** (headless Edge, 375 x 812, the mobile profile,
  medians of 3). "Warm" means an earlier city page cached the libraries,
  fonts and sprites but not this city's map data:

  | | Cold: page loaded / basemap drawn | Warm: page loaded / basemap drawn | Bytes cold / warm | JS heap | Browser memory |
  |---|---|---|---|---|---|
  | Standard only (today) | 4.36 / 4.42 s | 3.17 / 3.25 s | 635 / 457 KB | 6.1 MB | 551 MB |
  | Switch, reader picks Open (B) | 4.38 / 4.49 s, then 5.07 s to Open | 3.17 / 3.24 s, then 1.42 s to Open | 1,237 / 589 KB | 12.7 MB | 643 MB cold |
  | Open by default (C) | 5.50 / 7.94 s | **1.94 / 3.12 s** | 1,053 / **407 KB** | 10.8 MB | 645 MB |

  On a repeat visit an Open default is drawn sooner (3.12 s against 3.25 s)
  on fewer bytes (407 against 457 KB) than today's map; on a first visit it
  costs 3.5 s and 418 KB more, almost all of it the libraries. Its price on
  every visit is memory: about +4.8 MB of JS heap and +95 MB across the
  browser. So C on phones is plausible once the libraries are self-hosted
  with long cache lifetimes, subject to a real-phone memory check.
- **Licence reads (licence-read agent, one source each), all PERMITTED WITH
  CONDITIONS for both the site and an offline app:**
  - **Protomaps basemap, builds and style.** Hosting extracts on our own
    storage is what Protomaps asks for ("copy the tileset to your own Cloud
    Storage"), and offline use is supported. Credit `© OpenStreetMap` in the
    map corner, linked to openstreetmap.org/copyright (met). **Correction to
    the earlier note "OSM credit only":** the build's `landcover` layer
    (zooms 0-7, Daylight from ESA WorldCover) is CC BY 4.0 and, if shown,
    needs ESA's credit, "© ESA WorldCover project 2020 / Contains modified
    Copernicus Sentinel data (2020) processed by ESA WorldCover
    consortium"; the site's maps set no minimum zoom, so a reader can reach
    it. The cheaper fix is a style without the landcover layer (or a minimum
    zoom of 8 on the Open layer). Builds are kept only a week (plus one per
    patch version), so packs must be copied to our storage, never pointed at
    build.protomaps.com. A self-hosted or bundled `basemaps.js` must carry
    its BSD-3 notice (and the Mapzen MIT notice in the same LICENSE.md). A
    modified style or tileset may not be called "Protomaps". **Owner
    decisions:** protomaps.com's Terms of Use forbid "automated means to
    access the Site" without written permission and carry an open-ended
    indemnity, while Protomaps' own guide instructs scripted `pmtiles
    extract` against the build host; a one-line email to
    support@protomaps.com would settle it before a scheduled pack build.
    The same Terms forbid using "location data from the Site" for maps
    that "provide directions", which matters only if the app ever routes.
  - **Fonts and sprites (basemaps-assets).** Noto fonts under the SIL OFL
    1.1, no Reserved Font Names; the converted glyph files are a Modified
    Version, which is allowed. Ship `OFL.txt` (with "Copyright 2022 The Noto
    Project Authors") beside the fonts, and the MIT notice ("Copyright (c)
    2017 Mapzen", also given as "Mapzen, Linux Foundation") beside the
    sprites; in an app, both on a licences screen. Recommended, an owner
    call: also carry "Noto is a trademark of Google LLC", which the glyph
    format drops.
  - **ODbL for packs and the export.** The rendered site map is a Produced
    Work. OSMF's guidance does not settle whether **vector tile files** are
    a Produced Work or a database; recommended to treat the downloadable
    packs as a Derivative Database, which costs little: convey them only
    under ODbL with the licence named in the pack metadata and a README,
    keep the existing notices, and make a real, findable free download
    offer (ODbL 4.6; an unmodified extract offered as itself satisfies it).
    **The app may not encrypt or restrict the packs** (4.7). The JSON
    export is a Derivative Database (substantial, repeated) under ODbL; its
    non-OSM parts stay outside share-alike only while each data TYPE is
    all-OSM or all-non-OSM, and "regional cut" means at least a country in
    OSMF's guideline: an owner decision whether per-city purity is enough or
    each type stays single-source per country. A feed that forbids
    modification (LA Metro) could not go in a mixed file. Attribution: the
    site's corner credit already meets the 2021 guideline; an app may use a
    splash screen or a corner credit, and an info button only after the
    credit has been shown.
- **Not done:** the real-iPhone check, self-hosting, the travel style, and
  the landcover decision; the pilot carries them.

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
  | `lines[].redistribution`, `stations[].redistribution`, `exits[].redistribution` **[L]** | `"open"` (the source's terms allow redistributing it as data: ODbL for OSM, CC BY, Licence Ouverte and the like), `"restricted"` (they forbid or limit it: LA Metro's "unauthorized redistribution", WMATA's within-your-Application grant, MTA's no-modification), or `"unread"` (no read has answered the data question); plus `redistribution_basis`, the `docs/data_sources.md` row (file and anchor) the value comes from | per record, so the app can drop or replace a restricted line without re-researching it; the value is the SITE's reading for distribution as data, not a ruling on the app's own use, which the app project reads for itself |

- **Redistribution labels (owner, 2026-10-07).** Every line, station and
  exit carries `redistribution` and `redistribution_basis` (table above).
  `check_export.py` refuses a record whose source has no row, and refuses
  `"open"` where the row says otherwise. Filled first from the existing
  rows (the US table's "Redistribution" column answers many); a source no
  row answers is `"unread"` until the licence-read agent reads it, one
  source per call, when the export is built.
- **An OSM variant of each city's rail: decided when the export is built
  (owner, 2026-10-07).** Where a city's rail comes from a feed or an agency
  layer and an OSM cache exists (about 95 cities, per Cleanup's rail-scope
  list), the export may also carry an OSM-derived version, so the app can
  switch a restricted city to OSM without new work.
- **Discrepancies are disclosed in the app (owner, 2026-10-07).** Wherever
  the app shows a city's rail from a different source than the site (an OSM
  variant in place of a restricted feed), or leaves a restricted line out,
  it says so in the app. To make that possible from the export alone, a line
  or station drawn from a different source than the site's carries
  `site_source` (the source the site used) next to `source`, and the city
  carries `rail_differs_from_site: true`.

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
