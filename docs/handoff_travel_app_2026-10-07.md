# Handoff: the travel app, a separate project (2026-10-07)

For the first session of a NEW project, in its own folder and repository:
`C:\Users\dacek\Documents\Portfolio\transit-globe` (owner, 2026-10-07).
The owner's decisions and the measurements behind them are in this repo's
`DECISIONS.md`, entry "Four ideas assessed before the large review" (item 4).

## What the app is (owner)

- **Free**, so non-commercial licence terms do not block it.
- **Transit-first**: lines with their real names and colours, stations in
  English and the local script, station exits, place search, and a small set
  of everyday places (convenience stores, pharmacies, ATMs, toilets).
- **Everyday places come from OpenStreetMap, not the business registers.**
  One licence, the same meaning in every city, no privacy question. The
  website's register data stays on the website.
- **Offline by city pack**: online the app streams; before a trip the reader
  downloads a city (Kyoto measured 23 MB for its map area, 48 MB with 10 km
  around it, at street-level zoom).
- **A separate front end.** Streamlit cannot run offline; a phone-installable
  web app (PWA) first, native later only if it earns it.

## The interface rule (owner: "would not want to have it constantly competing for files")

- The app project **never edits** the expanded-heatmap repo, and that repo
  never holds app code.
- The app reads the website project's **export contract**: a versioned
  per-city set of files (stations, lines with names and colours, station
  exits, every required notice, the data's dates, a version), published for
  reading, e.g. as release assets. The website project is specifying it now
  (its "open basemap switch" session); ask its owner-facing report for the
  schema before writing a reader.
- A change the app needs in the export is a request to the website project,
  never an edit.

## Refresh and alerts (owner: "sounds good")

- Packs refresh **every 6 months**; at **12 months** the pack still opens with
  an "outdated, may be inaccurate" banner until updated.
- **Urgent flags per city** skip the wait: a rail opening, closure or renaming;
  a removal request (the website project honours one first, and it must reach
  offline copies); a licence date (Paris and Madrid require the data's date
  shown; Brussels' register needs a yearly re-download).
- **Timetables expire on their feeds' own dates** (WMATA's feed is valid ten
  days): the map stays usable, the schedule says "may be out of date".
- **Private by design**: the app downloads ONE manifest of every city's latest
  version and flags, the same for everyone, so the server never learns which
  cities a reader holds; alerts are in-app banners and locally scheduled
  reminders, with no push accounts or device identifiers.

## Established, do not redo

- **Basemap tiles**: CARTO's Basemap Terms 9.c forbid bulk download,
  redistribution and device caching over 30 days; tile.openstreetmap.org
  forbids offline use. The open route: **Protomaps basemaps** (code BSD-3,
  styles CC0, tiles an ODbL produced work; credit "© OpenStreetMap" only) in
  **PMTiles**, rendered with **MapLibre GL JS** (BSD-3). OpenMapTiles-schema
  builds add a mandatory "© OpenMapTiles" credit.
- **Pack sizes**, measured from the Protomaps planet build 20261007's index
  (station extent padded 1 km, zoom 0-15): Tokyo 92 MB, London 113 MB (the
  largest), Mendoza 1.2 MB, median 10.1 MB, all 170 cities 2.70 GB; 10 km
  more around each city: Tokyo 164 MB, median 27.8 MB, all 5.94 GB. Zoom 14 is
  about a third of zoom 15. A style of the app's own can drop layers.
- **Place search**: Nominatim's public service forbids autocomplete; search
  in the device over a per-city index from OpenStreetMap, an ODbL derivative
  database published under ODbL. The website project's search pilot (Kyoto)
  measures the index size; reuse its index format.

## Inputs still coming from the website project

Two of its sessions, started 2026-10-07, produce what the app builds on.
Their reports reach the owner; read them before designing the matching part:

- **"Prototype open basemap switch and app groundwork"**: the export
  contract's schema (the app's data input), the hosting comparison for
  PMTiles files (Cloudflare R2 and similar, costs), and a measured
  open-basemap page at phone width. Its drafts file:
  `docs/decisions_drafts/claude-epic-neumann-5aa0a6.md`.
- **"Pilot privacy-first place search on one map"** (Kyoto): the search
  index's format and size, and which queries work. The app's search should
  read the same index files.

## Open, the app project's first work

1. **Transit operators' terms for shipping in an app**, one licence read per
   source: WMATA, LA Metro, IDFM (Paris), CRTM (Madrid). Their current
   readings are in the website repo's `docs/data_sources/united-states.md`
   (WMATA :361, LA Metro :356), `docs/data_sources.md` (:310) with
   `docs/data_sources/france.md` (:75-76), and `docs/data_sources/spain.md`
   (:117-140). Where a feed may not ship, the fallback is rail from
   OpenStreetMap (no timetables).
2. **Hosting** for packs and the manifest, served by HTTP range request.
3. **A one-city prototype** reading the export contract, offline-capable.
4. **Notices**: every required notice ships inside the app beside the data
   it covers (the website repo's `docs/data_sources.md`, "Notices this
   project MUST display when published").

The website project's hard lines that carry over: ridership is out of scope;
publish public commercial information, never a person's own name; a removal
request is honoured first, not argued.
