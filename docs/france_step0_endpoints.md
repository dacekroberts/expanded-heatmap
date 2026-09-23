# France — Step 0 endpoints, measured 2026-09-22

**Status: PROFILE. No French city is built yet.** When the first one is, these
rows are promoted into `docs/data_sources.md` — **rewritten from that city's
own `config.py`, not copied from here** — and this file is relabelled as the
evidence trail. That promotion is a step, not a tidy-up: it was skipped for
Canada and for Mexico, and `scripts/check_provenance.py` exists because of it.

Machine-readable form: `pipeline/countries/france.py`.

---

## Why France was profiled before the other candidates

**One profile converts into six cities.** Paris, Lyon, Marseille, Toulouse,
Lille and Rennes all come off the same national register, the same licence and
the same rail aggregator, with **one variable** changing between them
(`codeCommuneEtablissement`). That is Mexico's shape — where the second city
differed by one line — and not Spain's, where two cities shared a country and
almost nothing else.

---

## The three legs

### 1. Business — INSEE SIRENE `StockEtablissement`

| | |
|---|---|
| Dataset | `base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret` on data.gouv.fr |
| Rows | **44,064,115 établissements** |
| Formats | ZIP **2,867 MB** · **parquet 2,210 MB** — *prefer parquet* |
| Updated | 2026-09-01 (monthly; the filename carries its own date) |
| Licence | **`lov2` — Licence Ouverte 2.0** |
| Key | `siret` |

**⚠️ Use `StockEtablissement`, never `StockUniteLegale`.** The same dataset
publishes `StockUniteLegale` — **30,020,346 legal units keyed on `siren`** —
and mapping it would produce exactly the registered-office map this project
exists not to make. They sit side by side in the resource list and the wrong
one was pulled first while writing this file.

**⚠️ Match the resource title with its trailing ` -`.** Without it,
`StockEtablissementHistorique` (1,239 MB) and
`StockEtablissementLiensSuccession` also match.

**⚠️ ACTIVE is the letter `A`, not the label `Actif`.** Filtering on `"Actif"`
returned **zero rows for all six cities** and was caught only because Paris ran
first as a control against a known-good number. Keep the control.

### 2. Coordinates — a JOIN, not a geocode

| | |
|---|---|
| Dataset | `geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques` |
| Publisher | **INSEE** |
| Rows | **37,901,783**, keyed on `siret` |
| Formats | ZIP 1,177 MB · **parquet 811 MB** |
| Updated | **2026-09-21** |
| Licence | **`lov2`** |

**France needs no geocoder.** One join on `siret` and the coordinate leg is
done — no rate limit, no key, no per-address requests. This is Prague's shape,
and it holds for all six cities at once.

The file publishes **both** a projected pair (`x`, `y`) and WGS84
(`x_longitude`, `y_latitude`), each **100% populated** in the sampled row
group, plus `plg_code_commune`.

**⚠️ THE CRS IS PER ROW, NOT PER FILE.** There is an `epsg` column. A sampled
row group held **four** values:

| EPSG | Share | Where |
|---|---|---|
| **2154** | 99.3% | Lambert-93, metropolitan France — **all six cities** |
| 2975 | | Réunion |
| 5490 | | Antilles |
| 2972 | | Guyane |

Hard-coding 2154 works for these six and would put every pin in the sea if the
pipeline were ever pointed at Fort-de-France — **without erroring**. Read the
column.

**It reports its own confidence.** `qualite_xy` sampled as 11 (62.5%),
33 (17.6%), 12 (15.9%), 22, 21, alongside `distance_precision`. Class 33 is
commune-centroid grade. This makes France the third source in this screen to
publish positional quality, after Denmark's DAWA `kategori` and Hong Kong's
ALS `Score` — **use it, do not average over it.**

### 3. Rail — one national aggregator for all six cities

`https://transport.data.gouv.fr/api/datasets` — France's National Access
Point. **799 datasets, 489 of type `public-transit`**, each carrying GTFS and
usually NeTEx and SIRI.

| City | Dataset | Formats |
|---|---|---|
| Paris | Réseaux urbains et interurbains d'Île-de-France Mobilités (IDFM) | GTFS, NeTEx, SIRI Lite |
| Lyon | Réseau urbain TCL | GTFS, NeTEx, SIRI Lite |
| Marseille | Réseaux urbains de la Métropole Aix-Marseille-Provence | GTFS, SIRI, gtfs-rt |
| Toulouse | Réseau urbain Tisséo | GTFS, NeTEx, gtfs-rt |
| Lille | Réseau urbain ilévia | GTFS, SIRI, gtfs-rt |
| Rennes | Réseau urbain STAR | GTFS, NeTEx, gtfs-rt |

**⚠️ The city's name is not enough to pick the feed.** Lille's match also
returns **"Navettes Aéroport de Lille"**, an airport shuttle — the identical
trap that had Dublin tested against airport coaches. Name the urban operator.

**⚠️ Do not substring-match the JSON blob.** `star` (Rennes), `mel` (Lille)
and `tcl` (Lyon) are short enough to match unrelated text; a first pass scored
Rennes at **489 of 799** datasets. Match on `title`, `slug`, `covered_area`
and `publisher`, with word boundaries.

**⚠️ GTFS licences are per operator and are UNREAD as of 2026-09-22.** The
portal's licence is not the feed's — LA Metro's CC0 registry beside its
modification-forbidding GTFS is the standing reason. Read each before its city
ships.

---

## The naming problem — measured before it could become a build surprise

Across **20,103 active rows in NAF 47/56/96**, sampled from four row groups
spread through the file:

| Field | Populated |
|---|---|
| `enseigne1Etablissement` | **29.1%** |
| `enseigne2Etablissement` | 13.4% |
| `denominationUsuelleEtablissement` | **34.2%** |
| **Either — any premises-level name** | **42.9%** |

**So roughly six in ten French storefronts publish no name at the premises
level.** This is Milan's `insegna` trap in another language, and it is written
here rather than discovered at step 2 with a taxonomy already built.

Per city, from a larger 14-row-group sample (1,735,429 rows, 3.9% of the file;
scaled estimates, not build numbers):

| City | Bucket rows, est. | Named |
|---|---|---|
| **Paris** | 136,400 | **42.9%** |
| Marseille | 26,940 | 45.8% |
| Lyon | 19,449 | 52.5% |
| Toulouse | 12,873 | 51.9% |
| Lille | 10,461 | 50.7% |
| **Rennes** | 5,002 | **54.3%** |

**Paris is the worst-named of the six**, which inverts the usual assumption
that the flagship city carries the best data. Paris's scaled 136,400 against
its independently measured **148,633** is the control passing — the ~8% gap is
sample bias, because active bucket rows get denser through a file ordered by
siret, which is seniority.

### ⚠️ The fallback that must not be used blindly

`StockUniteLegale`, joined on `siren`, would close the gap —
`denominationUniteLegale` for a company. **But for a sole trader it carries
`nomUniteLegale` and `prenomUsuelUniteLegale`, which are a person's name.**
The project's invariant is that a trade name is fair game and a registrant's
own name is not.

**Fall back to the legal name only where the legal form is a company, never
for a natural person**, and run `python scripts/check_personal_exposure.py`
before publishing any French city.

---

## Privacy — partly done upstream

France masks non-diffusible records **at source**: `statutDiffusionEtablissement`
≠ `O` hides the name, the commune address **and the geolocation**. Measured at
**13.4%** of active bucket rows, matching the 13.2% recorded for Paris.

Per `read-licence` step 6b this cuts both ways — it saves building a filter,
and it removes rows that looked available. **Check what survived, not only what
was removed.**

---

## What is NOT settled

- **Per-operator GTFS licences** — six feeds, none read.
- **The taxonomy.** NAF is NACE-shaped, but `premises-taxonomy`'s deciding
  measurement — the **catch-all share at each level** — has not been run.
  Barcelona keys at its finest level and Madrid near the top of an identically
  shaped scheme, so there is no default to inherit. Use `brief_check.py`'s
  `taxonomy_catchall`.
- **Whether `enseigne` or `denominationUsuelle` should be preferred** when both
  are present, and what a pin shows when neither is.
- **Station density per city** — the number that actually ranks the six.
- **The `etablissementSiege` flag does not separate premises from offices in
  France**: 90.8% of active bucket rows are sièges, because a sole trader's
  shop is its own siège. Recorded so nobody tries it as a filter.
