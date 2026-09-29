# Handoff - the tram batch's groundwork (2026-09-29)

For FRESH sessions picking up the owner's six groundwork items (owner,
2026-09-29: "i agree with all 6 groundwork items. implement as you see
appropriate"). The owner said yes to trams-only maps the same day (DECISIONS
"Yes to trams-only maps"). **Delete a section when its item is done.**

Read first: `docs/tram_city_list.md` (the 41 cities, T1 34 and T2 7),
`docs/ring_rules.md` (ring sizes, generated), the memo
https://claude.ai/artifact/UQ7Lsdu23HPfuZ1JFxoaxo, and PLAN's macro-map items.

## Decided, and binding on every item below

- **Ring size by the existing spacing rule** (owner): outer 0.3 mi where the
  median station gap is about 550 m or less, else 0.6. Nearly every tram
  city is under 550 m; Kansas City (~560) is measured at build.
- **No stop thinning** (owner). Riga's 0.5 mi filter does not carry over.
- **Macro map**: minor cities get no pill outside their own region; dots are
  coloured by network type (Dublin tram), completeness by fill (solid, ring,
  half-filled).
- **Station tables are pure extracts for every French ODbL feed** (owner):
  the feed's own `parent_station` and coordinates; without one, the first
  platform's coordinates, never a mean; names unchanged. No data.gouv.fr
  account. **Angers is held** (owner) until the other 20 are built: the
  France batch is 20 cities.
- **The currency rule**: the source must drop closed businesses and its
  newest row date must be under five years; the date goes on the page.

## 1. The France batch kit - a STAGING session (skills, scripts, briefs)

The 21 French T1 cities, on one register already cached nationally
(`data/france/raw/`, the September 2026 SIRENE edition).

- **A `france-tram-city` skill**, written from the five built French cities
  (Paris, Marseille, Toulouse, Lille, Rennes) per the per-country-skill rule:
  the SIRENE chain (active is the letter `A`; `codeCommuneEtablissement`
  codes differ from boundary codes; the per-row `epsg` column; `qualite_xy`
  33 is commune-centroid grade), the tram leg from the city's own feed
  (mode flags are unreliable: Reims types its tram as metro; Le Havre's
  funicular and Mulhouse's tram-train are dropped), the scope call (commune
  or regional; Bordeaux, Grenoble, Rouen and Valenciennes lean regional),
  0.3 mi rings, and the notices.
- **A batch scaffold script** (`scripts/`, dry-run first) that writes the 21
  configs from the screen's inputs:
  `data/_staging_scratch_2026-09-27/second_cities/france/` holds
  `stations/<slug>.csv` (every tram stop with its commune), `gtfs_urls.py`
  (each feed's resource and declared licence), `cities.py` (commune codes),
  `screen_results.csv` and `sirene_candidates.parquet`. Running the
  scaffolds is build work; writing the script is staging's.
- **21 build briefs** in `docs/build_briefs/<slug>.md`, each with a checks
  block for `scripts/brief_check.py`.
- Feeds are rolling (earliest end Avignon 2026-10-18): fetch at build, never
  cache a feed across weeks.

## 2. Licence reads - the five French ones DONE 2026-09-29

DECISIONS "French tram feeds read" has each verdict. In short: **Bordeaux**
(LO 1.0) credit Bordeaux Métropole and the feed's own date; **Montpellier,
Grenoble, Le Havre** (ODbL) the §4.3 notice naming the producer;
**Montpellier and Le Havre have no `shapes.txt`** (geometry from another
source, which needs its own read) and **Le Havre has no colours** (choose
them; never from transports-lia.fr). **Angers bars "Irigo" and its other
marks without consent: an owner call before its build.** **Every French ODbL
feed carries the national portal's Conditions Particulières**: keep station
tables as pure extracts (nothing renamed or merged) unless the owner creates
a data.gouv.fr account to re-share. Still to read, nearer their builds:
Plzeň's and Olomouc's GTFS, Tucson's BUSLIC terms, RideKC's GTFS, Florence's
four layers, VZD's address file, and the geometry source for Montpellier and
Le Havre. Each notice goes in `docs/data_sources/` before its page exists.

## 3. Page text by template - APPROVED by the owner 2026-09-29

The French tram-city page text, approved word for word ("approved"). It goes
into the `france-tram-city` skill; braces are per-city facts, filled at each
build from that city's own measurements. The controls paragraph and the
heat-layer caveat stay exactly as on Rennes's page
(`app/pages/25_Rennes_Heatmap.py`), and so does the transit caption, with the
operator's credit and any notice its licence read requires.

> {N} {operator} tram lines are drawn, **{lines}**, each labelled on the map
> and in the legend, from the operator's own published timetable feed. {City}
> has no metro: its trams are its rapid transit, as Riga's are, so every tram
> stop gets rings.
>
> The map covers the **{commune of City / N communes of the Métropole}**.
> {Where a line runs past it: which stops are left out and why, as Rennes's
> page does.}
>
> Businesses come from **SIRENE**, France's national register of
> établissements, joined to INSEE's geolocation file, the same sources as
> Paris, Marseille, Toulouse, Lille and Rennes. {Share} of active
> establishments here are marked non-diffusible by INSEE, which withholds
> their name, address and coordinates together, so they never reach this map.
> Where SIRENE records no shop sign or trading name, the dot shows the address
> instead.
>
> **Read the density as a register, not a street survey.** {Same paragraph as
> Rennes, with this city's ratio to OpenStreetMap's restaurants.}
>
> **Tram stops sit closer together than metro stations**, a median of
> {spacing} m here, so the rings are drawn at half the usual size (0.05 to
> 0.3 mi), as on the other French maps. **About {share} of storefronts sit
> within a ring.**

A city whose median stop gap is over about 550 m keeps the standard rings and
drops the last paragraph's first sentence (none in France is expected to).

## 4. Macro-map changes - the APP/CHROME role (an `app/` branch, review time)

PLAN, under "Macro-map completeness tiers", holds both items. **Measured
2026-09-29 for the France view** (scratch
`data/_staging_scratch_2026-09-29/band_t_audit/p4_france_labels.py`,
`p4_france_zoom.py`; `check_macro_labels.py`'s own projection, text widths
ESTIMATED at 7 px a character):
- One France region at the fitted zoom (3.52, about 9.5 km a pixel): **12 of
  26 labels cannot be placed** at any width. At zoom 5.0 every label places,
  but 3 cities are off-canvas even at 1200 px (11 at 375).
- **France North (18 cities, latitude 46.5 and up) and France South (8), each
  with a zoom override of 5.0**: every label places; nothing off-canvas at
  768 or 1200 px; 5 and 1 cities a pan away at 375 px. Recommended shape.
  The override uses the `REGIONS` `zoom` field, which exists and is None
  everywhere, and means measuring those regions' offsets.
- Seoul Capital Area is the label-tier pilot.

## 5. Streamlit Community Cloud at ~110 cities - APP/CHROME

`docs/scaling_thresholds.md` was written at 9 cities and set "~40" as the
architectural line; the site is at 68. Measure before France goes live:
memory on a cold start and on a map page, deploy clone time with
`outputs/` at ~237 MB (about 380 MB after the batch), and how the Overview's
city list reads at ~110.

## 6. Landing groups - done

`docs/review_time.md`, "Landing the tram batch": one `city-added`
deploy-verify per landing group, `full` once after the last.
