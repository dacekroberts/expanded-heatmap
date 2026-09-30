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

## 1. The France batch kit - DONE 2026-09-30

The `france-tram-city` skill, `scripts/scaffold_france_batch.py` and 20
briefs (Angers held); DECISIONS "The France batch kit". Builds wait for the
owner's go and the calls in each brief.

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

## 3. Page text by template - APPROVED 2026-09-29, now in the skill

Word for word in `.claude/skills/france-tram-city/SKILL.md`, section 6.

## 4. Macro-map changes - the APP/CHROME role (an `app/` branch, review time) - HELD

**HELD (owner, 2026-09-29) until the France kit has made real progress.**
The cleanup session is to claim this role (sections 4 and 5) and was told to
wait; the owner or staging says when to start.

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
