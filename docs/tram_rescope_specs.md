# Tram rescopes, light and medium — build specs

**Written 2026-09-27 by Staging for the build session (owner's split: Staging
specs, build implements).** The owner cleared the light and medium categories
of `docs/tram_rescope_estimate.md` for this window. Measured from the cached
feeds and live OSM/CRTM the same evening.

## Ground rules for the whole batch

- **Its own branch, held for review time.** Rescopes rewrite `outputs/`,
  which the live app reads. Nothing merges to master before the owner calls
  review time; the batch lands once, under one deploy check and one reboot
  (`publish-city`).
- **Every drawn line gets its permanent on-map label (its real public name)
  AND a legend entry.**
- **Colours**: `pipeline/linecolour.py`'s hard floor is ΔE 10 and its
  preference 45, and the renderer also checks the category pins. Measured ΔE
  is given per city below.
- **A step never fetches.** New downloads go in each city's
  `fetch_sources.py`; OSM goes through `pipeline.osm.fetch`.
- **Per city**, after its change:
  - `python pipeline/drift_check.py <city>` (the station and storefront
    counts change on purpose, so record the new baseline);
  - `scripts/check_map_view.js`, `check_map_markup.py` (dark-mode label
    contrast), `check_inline_arrays.py` and `check_scope_disclosure.py`;
  - the city's rows in `docs/map_inconsistencies.md` §4 and the
    station-scope section of `docs/excluded_categories.md`;
  - a DECISIONS entry.
- **New sources need a licence row** (`read-licence` / the `licence-read`
  agent) before anything publishes: only Montréal's REM, if it takes a GTFS.

## Status of the six

| City | Line | Verdict | Stops in scope | Source | Colour |
|---|---|---|---|---|---|
| **Montréal** | REM (A1, A3, A4) | **Build.** First in the batch | 12–14 per branch inside the agglomeration (union at build) | **New**: REM/ARTM GTFS after a licence read, else OSM (`osm-rail`) | #84BD00, ΔE 27 from Métro Line 1: passes |
| **Rome** | Tram 8 | **Build** | 16 (base) or 26 (the "8 prolungato"): pick the current service | **New OSM fetch** (the cached file has no tram relations) | #BFDF14, ΔE ≈70 from every drawn line: passes |
| **Madrid** | Metro Ligero ML1 (and see below) | **Build** | 11 of 56 Metro Ligero stations inside Madrid | CRTM `M10_Red` (same agency family as the Metro layers) | Not in the station layer; check at build |
| **San Francisco** | F Market & Wharves | **Build** (low priority) | 46, all inside | Cached Muni GTFS (route `F`, route_type 0) | #B49A36, ΔE 27 from J: passes |
| **Paris** | T3a, T3b | **Build**, with colour overrides | T3a 25, T3b 33, all inside | Cached IDFM GTFS | 🚨 **ΔE 0**: see below |
| **Washington D.C.** | DC Streetcar | **DROPPED: no longer operating** | — | — | — |

## Per city

### Montréal — REM
- **What exists**: OSM relations 19668643 and 19668926 (A1: Deux-Montagnes
  → Brossard, Anse-à-l'Orme → Brossard), 19669299 (A4) and 19672327 (A3).
  `route=light_rail`, operator Pulsar, colour #84BD00. The Deux-Montagnes and
  Anse-à-l'Orme branches are now in OSM as running.
- **Scope**: Montréal is built at AGGLOMERATION scope
  (`agglomeration.geojson`). The Brossard end (South Shore) and the Laval and
  Deux-Montagnes stops fall outside, as excluded stations with the lines drawn
  to their ends.
- **Source decision (build, not owner)**:
  - STM's feed carries only the Métro. Try the operator's or ARTM's GTFS
    first, run `licence-read` on it, and add a `docs/data_sources/` row.
  - If its terms are unclear, fall back to OSM through `osm-rail`, as Mexico
    City and Seoul did.
- **Labels**: the lines' public names (A1, A3, A4 per the relations) under the
  network name REM. **Check the REM's own current line numbering against the
  operator before labelling**: OSM's refs may lag a renumbering.
- **Rail test**: automated, grade-separated, high frequency. It passes
  without a timetable read, and it is a light metro rather than a tram.

### Rome — tram 8
- **Cached OSM (`osm_rail.json`) has no tram relations** (subway 13,
  light_rail 2). Add a tram fetch to `fetch_sources.py`.
- **Live OSM relations**:
  - base: 385213 (→ Venezia) and 1674659 (→ Casaletto), 16 stops;
  - "8 prolungato": 5376334 (→ Casaletto) and 5376335 (→ Labicano/Porta
    Maggiore), 26–27 stops.
  - All are ATAC, colour #bfdf14.
- 🚨 **Pick the relation pair that matches current service.** The cached
  GTFS (`rome_static_gtfs.zip`, read only as a check, since its terms were
  put to the owner) has 3,207 trips on route 8, and PLAN recorded 40 distinct
  stop names. Compare its stop sequence with both pairs, and key on relation
  ids, never on ref (Rome's rule).
- **Do not draw 2, 3, 5, 14 or 19**: they are in OSM but have 0 trips in the
  GTFS (19 is not in it at all). They are bus-replaced during works.
- **Label**: "Tram 8".

### Madrid — Metro Ligero
- **CRTM service `M10_Red`** (layers: 0 `M10_Estaciones`, 1 Accesos, 2
  Vestíbulos, 3 Andenes, 4 `M10_Tramos`). Also `M10_Lineas` and
  `Red_MetroLigero` exist on the same host.
- **Stations**: 56 in the layer, and **11 inside Madrid's municipal boundary**
  (`termino_municipal.zip`). PLAN recorded ML1 as 9, so **two more stations
  inside Madrid belong to another line**, most likely ML2's Aravaca end or
  the Colonia Jardín interchange.
- **Build steps**:
  - attribute stations to lines from `M10_Tramos`;
  - draw **ML1**;
  - if ML2 keeps real stations inside Madrid, it is a **stub question for
    the owner** (the recommendation covered ML1 only).
  - ML3 and the Parla tram are outside Madrid.
- **Colour**: not in the station layer. Read it from `M10_Lineas` or the
  operator. ML1's light blue may sit close to Metro Line 1's #30A2DA, so
  check ΔE.
- The comment in `pipeline/madrid/config.py` ("Metro Ligero is left out …
  a layer away") becomes the history line in DECISIONS.

### San Francisco — F Market & Wharves
- **Cached Muni GTFS**: route_id `F`, "MARKET & WHARVES", route_type 0, 852
  trips, 3 shapes, **46 stops, all inside the county boundary**.
- **The config's exclusion comment** ("a separate branded service - different
  rolling stock") is the reason the owner's "trams count" rule reversed.
  Replace it with the new decision.
- **Cable cars (PH, PM; route_type 5) stay out** (a reason that still
  stands). They share #B49A36 with the F, so match on the exact route_id.
- **Colour**: #B49A36, ΔE 27.0 from J Church (#A96614), 55 from M: passes
  the floor.
- **Label**: "F Market & Wharves".

### Paris — T3a and T3b
- **Cached IDFM GTFS**:
  - T3a: `IDFM:C01391`, 25 stops, all inside Paris;
  - T3b: `IDFM:C01679`, 33 stops, all inside Paris;
  - they meet at Porte de Vincennes.
- 🚨 **IDFM gives the trams the Métro's colours: T3a #FF5A00 is IDENTICAL to
  Ligne 5 (ΔE 0), and T3b #00643C to Ligne 12 (ΔE 0).**
  - Override both, as the bis lines were overridden (`LINE_COLOURS` comment
    in `pipeline/paris/config.py`).
  - Each override must clear the Métro lines AND the three category pins.
  - Record the choice as this project's, not RATP's.
- **T2 and T9 are LEFT OUT (owner's call, 2026-09-27)**: stubs, with 3 of
  24 and 1 of 19 stops inside Paris. Draw T3a and T3b only.
- **Match on route_type 0 AND the exact short name** (`T3a`, `T3b`), never a
  substring. The config already warns that "1" matches too much.
- **Labels**: "T3a", "T3b".

### Washington D.C. — DC Streetcar: dropped
- **DDOT ended DC Streetcar service on 2026-03-31**, a year earlier than
  planned, after the D.C. Council cut its FY2026 funding. Sunday service had
  already stopped on 2026-01-04. Sources: DDOT's release "DDOT Announces DC
  Streetcar Service to End March 31, 2026" and its "End of Service" page;
  WTOP, 2025-10 and 2026-03.
  - DDOT's own pages refused a scripted request (403/406), so this rests on
    the search results naming DDOT's release. A human glance at
    `ddot.dc.gov` confirms it.
- OSM already carries no streetcar relation in D.C.
- 🚨 **Do not draw the Capitol's "Rayburn", "Russell" and "Dirksen-Hart"
  lines**: OSM tags them `route=light_rail`, but they are private
  people-mover subways (Architect of the Capitol), with no public stops.
- **Docs**: PLAN's "status unverified" line and the D.C. "—" in
  `docs/map_inconsistencies.md` become "no longer operating (ended
  2026-03-31)". No map change for D.C.

## Order

REM → Rome 8 → Madrid ML1 → Paris T3 → SF F Market. The top three reach
districts the metro does not; Paris needs the colour decision; SF is the
lowest value.
