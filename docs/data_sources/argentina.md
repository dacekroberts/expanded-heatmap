# Data sources — Argentina

<!-- internal -->The Argentina part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country. The numbered
notices this project must display, the removal-request commitment and the
deploy gate apply to every country and are kept in that record. Buenos Aires'
build brief is in the project's repository (`docs/build_briefs/buenos-aires.md`);
Argentina was screened as Tier 4 in the project's country shortlist
(`docs/global_country_shortlist.md`).<!-- /internal -->

**Country profile (<!-- internal -->add-country, <!-- /internal -->one source, one city).** Argentina has no
national premises register in use here; Buenos Aires is built on the city's own
open-data portal, BA Data (`data.buenosaires.gob.ar`, CKAN). Its API refuses
non-browser clients with a 245-byte "Request Rejected" page; the files it links
are served by `cdn.buenosaires.gob.ar` to any client, and every download below
comes from the CDN. License: BA Data's datasets declare **CC BY 2.5 AR**.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Buenos Aires | **Relevamiento Usos del Suelo 2022-2024** (Gobierno de la Ciudad de Buenos Aires; Dirección General de Antropología Urbana, Subsecretaría de Planeamiento) — a street survey: one row per use observed at an address, 417,764 rows, each block surveyed once in 2022, 2023 or 2024. **No names, no coordinates** | All three buckets via `pipeline/taxonomies/ba_usos_suelo.py` (385 `TIPO2` subtypes, enumerated): **63,596 storefronts** built 2026-09-28 from the 87,028 active single-use shopfronts (`TIPO1 == "UNICOMERCIAL"`, `ESTADO == "ACTIVO"`) | `https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-de-desarrollo-urbano/relevamiento-usos-suelo/relevamiento-usos-del-suelo-2022-2024.csv` (39,492,398 bytes, sha256 `5743336654ff9034a2f54129dd7c89011aa401c151828319b7fa1b06367fa2f1`, keyless); dataset page `https://data.buenosaires.gob.ar/dataset/relevamiento-usos-suelo` | None server-side (the file has no personal columns; step 2 exits if one appears). Out: 593 active malls and arcades (MULTICOMERCIAL, shops not itemised), 6,243 "SIN IDENTIFICAR" shopfronts, homes with an economic activity (a RESIDENCIAL subtype) — owner, 2026-09-28. Accented vowels are cp437 mojibake in the published file, repaired by the taxonomy. License **CC BY 2.5 AR** — notice **60** | 2026-09-28 |
| Buenos Aires | **Parcelas** (Gobierno de la Ciudad de Buenos Aires; Subsecretaría de Registro, Interpretación y Catastro) — not businesses: the cadastral parcels, JOINED on the survey's SMP (section-block-parcel) key | The placement: each storefront at its parcel's centroid, taken in UTM 21S. **63,503 (99.8%) exact, 93 (0.1%) at their block's centroid, 3 unplaced**. 318,046 parcels, WKT polygons in WGS84 | `https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-de-desarrollo-urbano/parcelas/parcelas_catastrales.csv` (329,396,024 bytes, sha256 `f3debefdaccc02e59f0d417e60531ad95c9adefbe301c91ae9ca39099e5d7019`); dataset page `https://data.buenosaires.gob.ar/dataset/parcelas` | Only `smp` and `geometry` read, in chunks. Key normalized by removing spaces and upper-casing. License **CC BY 2.5 AR** on the dataset, 4.0 on its resources: the credit satisfies both — notice **60** | 2026-09-28 |

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Buenos Aires | **Subte: Estaciones** (Subterráneos de Buenos Aires, SBASE) — the Subte's station points (90, one per line served) and track (98 segments) | `https://cdn.buenosaires.gob.ar/datosabiertos/datasets/sbase/subte-estaciones/estaciones_de_subte.geojson` (17,133 bytes, sha256 `e392abf0d923e5ea7cebc1c463f9b7471f062ad22527fb628fe0f480d2f32cc3`) and `https://cdn.buenosaires.gob.ar/datosabiertos/datasets/sbase/subte-estaciones/red_subte.geojson` (40,850 bytes, sha256 `aef377072b153f7e1093c146b1fa70cf07ae66866f1589bee2180d3041b407ad`), both last modified 2026-09-01; dataset page `https://data.buenosaires.gob.ar/dataset/subte-estaciones` | 2026-09-28 | **Positions and track** (owner's download OK 2026-09-28). Agency layers rank ahead of OSM<!-- internal --> (`osm-rail`)<!-- /internal -->; the city's Subte GTFS ships without a `routes.txt`. Gate 3 exact on six lines: A 18, B 17, C 9, D 16, E 18, H 12. Every segment lies within 30 m of OSM's route; Línea E's are drawn twice and dissolved. License **CC BY 2.5 AR** — notice **60** |
| Buenos Aires | **OpenStreetMap route relations** for the Subte (`network=Subte de Buenos Aires`, 12 `route=subway` relations) and the Premetro (4 `route=tram`, ref P) | The Overpass mirrors in `pipeline/osm.py`: the relations with geometry, and their stop nodes (211 elements) | 2026-09-28 | **The cross-check and the station names.** OSM's per-line counts equal SBASE's; each SBASE point takes the name of the nearest OSM stop on its line (all 90 within 150 m, median 24 m), because SBASE drops accents and carries one out-of-date name. The Premetro is measured, not drawn (owner). OSM, **ODbL 1.0** — notice 1 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Buenos Aires | **OpenStreetMap relation 3082668** (Ciudad Autónoma de Buenos Aires, admin_level 4), polygonised from its outer ways | The Overpass mirrors in `pipeline/osm.py`, `relation(3082668);out geom;` | **CABA - 205.6 km²** in UTM 21S, gated at 190-215; name and level asserted. Scopes stations (all 89 inside). The survey covers exactly CABA. OpenStreetMap, ODbL 1.0 — notice 1 |
