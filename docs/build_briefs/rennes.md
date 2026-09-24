# Rennes — build brief

**Step 0 measured 2026-09-23.** France's national facts are in
`pipeline/countries/france.py` and `docs/france_step0_endpoints.md` — **read
those first**; a correction belongs there, not here. Run
`python scripts/brief_check.py rennes` before writing code.

---

> ✅ **BUILT 2026-09-23, commune-only.** Two claims below did not survive the
> build, and both are corrected where they stand. **Scope:** "the métro is
> city-contained" is half true - Métro a keeps 15 of 15 stations inside
> commune 35238, **Métro b keeps 11 of 15 and loses both termini** (Atalante
> and Cesson - Viasilva to Cesson-Sévigné, La Courrouze and Saint-Jacques -
> Gaîté to Saint-Jacques-de-la-Lande). Commune-only was the owner's call anyway,
> because the worst line survives better than Toulouse's T1. **Masking:** 9.8%
> was low - 15.9% on the same denominator. Gate 3 is exact on both lines
> against STAR's own `tco-metro-topologie-dessertes-td` (15 = 15), read the
> night after the build because the portal API refused every call that day on
> a spent domain-wide quota; OpenStreetMap agrees. See `DECISIONS.md`.

## The one-line summary

**The smallest of the six and the cleanest feed in France.** ~4,833 storefront
rows — an order of magnitude below Paris — but **the best-named city in the
country (53.5%)**, the lowest distance-selling share, and a GTFS that carries
everything Paris's does not: `shapes.txt`, `feed_info.txt`, and a real
`feed_end_date`.

---

## Business leg — SIRENE, commune `35238`

| | |
|---|---|
| Source | `StockEtablissement` **parquet**, `codeCommuneEtablissement` **= `35238`** (a single code, not a prefix) |
| Active in NAF 47/56/96 | **≈4,833** (611 counted in 12.6% of the file) — a **floor**; scaling undercuts |
| **Named** | **53.5% — the highest of the six** (Paris 39.6%) |
| Masked (`statutDiffusion` ≠ `O`) | ~~9.8%~~ **15.9%** measured at the build on the same denominator (active rows in 47/56/96); 17.5% of all active rows. The sample was low, as Toulouse's was |
| Distance selling to exclude | **14.2% — the lowest of the six** |

**Rennes is the best-quality French city and the smallest.** Whether ~4,800
rows makes a worthwhile map is a scale question, not a data question — Boston
shipped on 3,164 premises.

**Inherited unchanged**: active is `"A"` not `"Actif"`; use
`StockEtablissement`, never `StockUniteLegale`; match the resource title with
its trailing ` -`.

---

## Coordinates — the join

`siret` against INSEE's geolocation parquet. **Read the `epsg` column** —
Rennes is metropolitan so **2154**, but the column is per row.

✅ **The geolocation file is built only from diffusible establishments**, so
the join cannot reintroduce a masked establishment's location.

---

## Taxonomy — sous-classe, like all six

| Level | Rennes | All six |
|---|---|---|
| groupe (3) | 46.0% | 44.1–50.7% |
| classe (4) | 35.7% | 27.9–38.1% |
| **sous-classe (5)** | **22.6%** | **19.8–23.0%** |

**Key at sous-classe.** 0% unlabelled. Rennes sits at the high end of the
band but well inside it.

---

## Rail — 2 métro lines, the cleanest feed in France

**`https://eu.ftp.opendatasoft.com/star/gtfs/GTFS_STAR_BUS_METRO_EN_COURS.zip`**
— 13.4 MB, 10 files.

| | |
|---|---|
| `shapes.txt` | ✅ |
| `feed_info.txt` | ✅ — publisher **Keolis Rennes**, `feed_end_date` **2026-10-18** |
| Rail drawn | **2 `route_type 1`** — métro lines **a** and **b** |
| Excluded | 150 bus routes |

**It SELF-ATTESTS**, which Paris's IDFM feed cannot. ⚠️ But the window is
**short — expires 2026-10-18**, so `brief_check` will flag it sooner than
Marseille's (2026-12-31). A stale-feed failure here means refetch, not alarm.

⚠️ **A second resource exists**: `GTFS (version à venir)`, the *forthcoming*
timetable. **Use `EN_COURS`** — the current one — or the map shows services
that do not yet run.

---

## ✅ Licence — ODbL, and the publisher's CGU is CLEAN

**`odc-odbl`** on the National Access Point. Full analysis at
`docs/licenses/odbl-toulouse-rennes.md`.

### MUST DISPLAY — §4.3, the licence's own safe-harbour wording

```
Contains information from Réseau urbain STAR, which is made available
here under the Open Database License (ODbL).
```

⚠️ **The existing OpenStreetMap ODbL notice does NOT discharge this** — §4.3
requires naming *which* database.

### MUST DO — §4.6

Offer recipients the derivative **or the method**. **The public repo already
satisfies it** — the pipeline code *is* the method — **provided it is LINKED
from the site.**

### ✅ The publisher's CGU adds nothing harmful

Read 2026-09-23 at `data.explore.star.fr/terms/terms-and-conditions/`:

- **No indemnity** — unlike Grand Lyon's CGU 9.4.
- **The marks clause is Opendatasoft's**, expressly excluding *« les données
  publiées sur le DOMAINE »*. ✅ **So naming *STAR* on the map is not barred.**
- The express extraction bar applies only *« en dehors d'une LICENCE
  consentie »* — **this project is inside one.**

### ⚠️ Open — the station CSV under §4.4

Whether the committed station table is itself a *Derivative Database* is
unresolved, and **unlike Paris there is no publisher gloss to lean on.**
**Cheap discharge: put an ODbL notice on the station CSV.**

---

## Region

`"region": "Europe"`.

---

## Still unknown

- ~~**Scope** — Rennes commune only, or Rennes Métropole? The métro is
  city-contained, so this is lower-stakes than Marseille's.~~ **Settled
  2026-09-23: commune-only, and the premise was wrong** - Métro b loses 4 of
  15 stations, both termini among them. See the note at the top.
- **§4.4** — the station CSV question above.
- **Exact bucket count** — 4,833 is scaled and is a floor.
- **Whether ~4,800 rows is worth a page.** A scale judgment for the owner;
  Boston shipped on 3,164.

```brief-checks
[
  {
    "id": "rennes-gtfs-downloads",
    "claim": "STAR's current GTFS downloads with no key, ~13.4 MB. Use GTFS_STAR_BUS_METRO_EN_COURS - the sibling A_VENIR resource is the FORTHCOMING timetable and would draw services that do not yet run",
    "kind": "http_ok",
    "url": "https://eu.ftp.opendatasoft.com/star/gtfs/GTFS_STAR_BUS_METRO_EN_COURS.zip",
    "min_bytes": 8000000
  },
  {
    "id": "rennes-gtfs-complete",
    "claim": "The feed carries shapes.txt so both metro lines can be drawn, AND feed_info.txt so staleness is checkable from the artifact - which Paris's IDFM feed cannot do",
    "kind": "gtfs_files",
    "url": "https://eu.ftp.opendatasoft.com/star/gtfs/GTFS_STAR_BUS_METRO_EN_COURS.zip",
    "present": ["routes.txt", "trips.txt", "stops.txt", "stop_times.txt", "shapes.txt", "feed_info.txt"],
    "absent": []
  },
  {
    "id": "rennes-gtfs-is-current",
    "claim": "The feed declares feed_end_date 2026-10-18 - a SHORT window, so this will flag sooner than Marseille's 2026-12-31. A failure here means refetch, not alarm",
    "kind": "gtfs_feed_window",
    "url": "https://eu.ftp.opendatasoft.com/star/gtfs/GTFS_STAR_BUS_METRO_EN_COURS.zip",
    "expect": "current"
  },
  {
    "id": "star-cgu-still-clean",
    "claim": "STAR's portal CGU is live and was read 2026-09-23: no indemnity, and its marks clause is Opendatasoft's own with the published data expressly excluded, so naming STAR on the map is not barred. If this changes, re-read before shipping",
    "kind": "http_contains",
    "url": "https://data.explore.star.fr/terms/terms-and-conditions/",
    "present": ["OPENDATASOFT"]
  },
  {
    "id": "sirene-stock-etablissement-parquet",
    "claim": "The SIRENE parquet is still published. Rennes filters it on codeCommuneEtablissement = 35238, a single code rather than a prefix",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/",
    "min_bytes": 5000
  },
  {
    "id": "insee-geolocation-dataset",
    "claim": "INSEE's geolocation file is still published - the coordinate join, built only from diffusible establishments so it cannot reintroduce a masked location",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/",
    "min_bytes": 3000
  }
]
```
