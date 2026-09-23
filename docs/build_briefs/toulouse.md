# Toulouse — build brief

**Step 0 measured 2026-09-23.** France's national facts are in
`pipeline/countries/france.py` and `docs/france_step0_endpoints.md` — **read
those first**. Run `python scripts/brief_check.py toulouse` before writing
code.

---

## The one-line summary

**Second-best-named French city, and the one whose data is most withheld.**
52.8% carry a premises name — but **20.2% of rows are masked at source**
(⚠ this brief estimated 16.0% from a sample; the build measured 20.2% over the
whole file, so the estimate was LOW), well over double Paris's 8.5%, so its
usable set shrinks by more than its row count suggests. Its feed also carries **an aerial cable car**, which is a
judgment call this project has never had to make.

---

## Business leg — SIRENE, commune `31555`

| | |
|---|---|
| Source | `StockEtablissement` **parquet**, `codeCommuneEtablissement` **= `31555`** |
| Active in NAF 47/56/96 | **≈12,853** (1,625 counted in 12.6% of the file) — a **floor** |
| **Named** | **52.8%** — second only to Rennes; Paris is 39.6% |
| ⚠️ **Masked** (`statutDiffusion` ≠ `O`) | **20.2% measured at build** — brief said 16.0%; highest of the six either way |
| Distance selling to exclude | 18.2% |

⚠️ **The masking matters more than the headline count.** A sixth of Toulouse's
rows have name, address **and geolocation** withheld — France masks all three
together. **Budget ~10,800 usable rows, not 12,853.**

---

## Coordinates — the join

`siret` against INSEE's geolocation parquet. **Read the `epsg` column** —
**2154** here, but it is per row.

✅ The geolocation file is built only from diffusible establishments, so the
join cannot reintroduce a masked location.

---

## Taxonomy — sous-classe

| Level | Toulouse | All six |
|---|---|---|
| groupe (3) | 46.8% | 44.1–50.7% |
| classe (4) | 37.5% | 27.9–38.1% |
| **sous-classe (5)** | **21.8%** | **19.8–23.0%** |

**Key at sous-classe.** 0% unlabelled.

---

## Rail — 2 métro, 1 tram… and a cable car

**`https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/`**
— 12.0 MB, 11 files.

| `route_type` | Count | What |
|---|---|---|
| `1` | **2** | Métro A and B |
| `0` | **1** | Tram |
| **`6`** | **1** | ⚠️ **Aerial lift — the Téléo cable car** |
| `3` | 120 | Bus, excluded |

`shapes.txt` ✅ · **`feed_info.txt` ❌ MISSING** — same gap as Paris, so
**`fetch_sources.py` must record the download date** or staleness is
unknowable from the artifact.

### ⚠️ OWNER CALL — draw the Téléo?

`route_type 6` is an aerial lift. **This project has never drawn one.**

⚠️ **CORRECTED 2026-09-23, during the build.** This section originally read
"It does draw a **funicular** (Paris), so 'not a train' is not itself a reason
to exclude." **That is false, and it was the whole case for inclusion.**
`pipeline/paris/config.py:176` says "WHAT COUNTS: the Metro, and only the
Metro", and the feed inventory it prints beside that line — "1,966 bus routes,
24 rail/RER, 17 tram, 16 metro, **1 funicular, 1 cable**" — lists the
funicular among what Paris *excluded*. **No built city draws a non-rail mode.**

So the decision has no precedent in either direction, and Paris's exclusion is
not one: the Montmartre funicular is a 108 m two-station lift inside one
arrondissement, where Téléo is a 3 km ticketed crossing serving a hospital, a
university and the Oncopole. Generalising from it would repeat the error
`dd4ced8` corrected — treating an exclusion as a rule when the excluded thing
shared an unstated condition the new one does not.

- **For**: Téléo is urban transit on the Tisséo network, ticketed like the
  métro, and it crosses the Garonne where no other line does.
- **Against**: it is one line, and every built city's rail set has been
  rail-on-rails plus Paris's funicular.

**Recorded rather than silently dropped.** Either way the decision belongs in
`docs/sub_transit_line_filters.md` if it splits from the default.

---

## ✅ Licence — ODbL, and the publisher's CGU is CLEAN

**`odc-odbl`** on the National Access Point. Full analysis at
`docs/licenses/odbl-toulouse-rennes.md`.

### MUST DISPLAY — §4.3

```
Contains information from Réseau urbain Tisséo, which is made available
here under the Open Database License (ODbL).
```

⚠️ **The existing OpenStreetMap ODbL notice does NOT discharge this** — §4.3
requires naming *which* database.

### MUST DO — §4.6

Offer the derivative **or the method**. **The public repo satisfies it**,
**provided it is LINKED from the site.**

### ✅ The publisher's CGU adds nothing harmful

Read 2026-09-23 at `data.toulouse-metropole.fr/terms/terms-and-conditions/`:

- **No indemnity** — unlike Grand Lyon's CGU 9.4.
- **The marks clause is Opendatasoft's**, expressly excluding *« les données
  publiées sur le DOMAINE »*. ✅ **So naming *Tisséo* on the map is not
  barred** — which was the specific risk, since Grand Lyon's equivalent is why
  Lyon is deferred.
- The express extraction bar applies only *« en dehors d'une LICENCE
  consentie »* — **this project is inside one.**

### ⚠️ Open — the station CSV under §4.4

Unresolved, and **no publisher gloss exists** as it did for Paris. **Cheap
discharge: an ODbL notice on the station CSV.**

---

## Region

`"region": "Europe"`.

---

## Still unknown

- ⚠️ **The Téléo** — owner call above.
- **Scope** — Toulouse commune, or Toulouse Métropole?
- **§4.4** — the station CSV question.
- **Exact bucket count** — 12,853 is scaled and is a floor; **and ~16% of it
  is masked**, so the usable figure is lower again.
- **Station counts per line**, and whether any falls outside the chosen scope.

```brief-checks
[
  {
    "id": "toulouse-gtfs-downloads",
    "claim": "Tisseo's GTFS downloads from the Toulouse Metropole Opendatasoft portal with no key, ~12 MB. The file id is long - a truncated copy returns 404 'Unknown image', which names the id you sent rather than refusing you",
    "kind": "http_ok",
    "url": "https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/",
    "min_bytes": 8000000
  },
  {
    "id": "toulouse-gtfs-has-shapes-no-feed-info",
    "claim": "The feed carries shapes.txt so the metro, tram and cable car can be drawn - and carries NO feed_info.txt, the same gap as Paris, so fetch_sources.py must record the download date. The absence is pinned deliberately",
    "kind": "gtfs_files",
    "url": "https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/",
    "present": ["routes.txt", "trips.txt", "stops.txt", "stop_times.txt", "shapes.txt"],
    "absent": ["feed_info.txt"]
  },
  {
    "id": "tisseo-cgu-still-clean",
    "claim": "Toulouse Metropole's portal CGU is live and was read 2026-09-23: no indemnity, and its marks clause is Opendatasoft's own with published data expressly excluded, so naming Tisseo on the map is not barred. That was the specific risk - Grand Lyon's equivalent clause is why Lyon is deferred",
    "kind": "http_contains",
    "url": "https://data.toulouse-metropole.fr/terms/terms-and-conditions/",
    "present": ["OPENDATASOFT"]
  },
  {
    "id": "sirene-stock-etablissement-parquet",
    "claim": "The SIRENE parquet is still published. Toulouse filters it on codeCommuneEtablissement = 31555",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/",
    "min_bytes": 5000
  },
  {
    "id": "insee-geolocation-dataset",
    "claim": "INSEE's geolocation file is still published - the coordinate join. Built only from diffusible establishments, which matters more here than anywhere: Toulouse masks 16.0% of its rows, the highest of the six",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/",
    "min_bytes": 3000
  }
]
```
