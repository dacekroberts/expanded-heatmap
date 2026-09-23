# Paris — build brief

**Step 0 is banked. Nothing here needs discovering; the open items are owner
calls, and they are listed as such.**

Everything below was measured on **2026-09-22** during France's country
profile. The national facts live in `pipeline/countries/france.py` and
`docs/france_step0_endpoints.md` — **read those first**, because five more
French cities inherit them and a correction belongs there rather than here.

**Run `python scripts/brief_check.py paris` before writing any code for this
city.** A brief caches Step 0's mistakes as confidently as its findings.

---

## The one-line summary

**Paris is the only unbuilt city in the screen with no coordinate leg at all**
— SIRENE's establishments join INSEE's geolocation file on `siret`, so there is
no geocoder, no rate limit and no key anywhere in the build. What it has
instead is a **naming problem**: roughly six in ten storefronts publish no
premises-level trade name, and the fallback that closes it is a privacy guard
rather than a lookup.

---

## ✅ BOTH OWNER CALLS SETTLED 2026-09-22

They were open when this brief was written, and both were taken the same day —
**scope: commune-only. Pins: the Milan hybrid.** The reasoning and the
measurement that decided the first are below, under each original question.

### ✅ 1. Scope — COMMUNE-ONLY, and it costs no transit system

**Measured 2026-09-22 from IDFM's own feed and France's own commune contour**
(`geo.api.gouv.fr/communes/75056`, 105.4 km², matching Paris's ~105 km²) —
not from OpenStreetMap, whose mirrors 504'd on both real hosts mid-probe,
which is a fact about the host rather than about the city.

| Mode | Inside commune | Outside | % inside |
|---|---|---|---|
| **Métro** (`route_type 1`) | **245** | 76 | **76.3%** |
| Tram (`0`) | 60 | 227 | 20.9% |
| RER / Transilien (`2`) | 38 | 437 | 8.0% |
| Funicular (`7`) | 2 | 0 | 100% |

**All 16 métro lines survive the boundary.** Every line has stations inside and
none is lost; the worst-truncated are M14 (12 of 21) and M13 (19 of 32), and
M2, M6, M3B and M7B are entirely inside. **Paris's own system is kept whole.**

**The two modes that are mostly outside would not be drawn at any scope.**
RER and Transilien are commuter rail, excluded by the standing rule in every
built city — Boston's `CR-*`, Chicago's Metra, Madrid's Cercanías, Miami's
Tri-Rail, Philadelphia's Regional Rail, Vancouver's West Coast Express — so
scope is not what decides them. Trams are excluded in Barcelona, Milan and
Toronto already; drawing Paris's would be the exception rather than the rule.

**So regional scope would buy Paris almost nothing, which is the OPPOSITE of
Dublin.** Dublin went regional because its *register* is published per local
authority and the city alone held 8,016 of 13,945 storefronts; the rail was a
consequence, not the reason. Paris's register does not care — 
`codeCommuneEtablissement` is a prefix list — and its rail gains only modes the
project excludes. *(Re-measured at build time 2026-09-23 against the feed the
build actually downloaded: **76 outside, 321 total**, where this table first
recorded 77 and 322. One station left the excluded set; the inside count, which
is what the map is built on, reproduced exactly at 245 and all 16 lines still
survive.)* The 76 out-of-commune métro stations go to the build's
excluded-stations record, as every other city's do, rather than anchoring rings
over communes this build has no business data for. *(The path is deliberately
not cited here: `check_provenance.py` requires every `outputs/` path named in
prose to exist and be committed, and Paris is not built — the promise would be
to a file no reader could open.)*

<details><summary>The original question, kept for the reasoning</summary>

### 1. Scope — commune, or regional?

Paris's commune (`751xx`, 20 arrondissements) is **far smaller than the IDFM
network it would be mapped against**. Dublin answered the same question by
going regional across four local authorities; Copenhagen needs Frederiksberg or
its map has a hole in the middle.

- **Commune-only** is the cheap, defensible default and matches every built
  city except Dublin, Vancouver, Miami and Guadalajara.
- **Regional** would mean adding the petite couronne communes — a one-line
  change on the business side, because `codeCommuneEtablissement` is just a
  prefix list, but a real change to the rail filter and the boundary layer.

**The business leg does not care. The rail and boundary legs do.**

</details>

### ✅ 2. What a pin shows when there is no name — THE MILAN HYBRID

**Settled 2026-09-22: show the premises name where it exists, the address
otherwise, and do not build the legal-name join at all.**

This is the option the original list below omitted, and it is what **both**
recently built cities converged on independently. Milan shows `insegna` on the
~20% of rows that carry one and `Ubicazione` on the rest; Dublin shows the
address on all of them, because its register has no name column at all. Paris
sits between them, so it takes Milan's shape.

**Why not the guarded legal-name fallback, which is measured as safe?**
Because "safe if the guard is built" is doing real work in that sentence. The
guard is the only thing between the build and roughly **ten thousand
individuals' names** — 9.4% of ~108,000 unnamed rows — against the ~4,000 Los
Angeles nearly published. The hybrid needs no guard, carries **zero** residual
exposure, and is strictly less work. The fallback's benefit is a nicer label on
rows where the register itself declined to record one; that is not worth
standing up a suppression rule whose failure mode is publishing people.

⚠️ **Keep the measurement anyway** (below): it is what makes this a decision
rather than an avoidance, and it is the number to re-read if the fallback is
ever reconsidered for another French city.

**One open sub-question is now moot for the build**: "whether `enseigne1` or
`denominationUsuelle` wins when both are present" still wants an answer for the
tooltip, but it no longer gates anything, because neither path reaches a
person's name.

<details><summary>The original question, kept for the reasoning</summary>

### 2. What a pin shows when there is no name

This affects **~57% of rows**. Three options, and Milan faces the identical
call:

- **Show the address** — Dublin's answer, and the honest one.
- **Fall back to the legal name**, guarded (see below) — recovers ~9 in 10 of
  the unnamed, and is now measured as safe *if the guard is built*.
- **Drop unnamed rows** — would discard most of the city; not recommended.

</details>

---

## Business leg — SIRENE `StockEtablissement`, MEASURED

| | |
|---|---|
| Dataset | `base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret` |
| Rows | **44,064,115 établissements** nationally |
| Format | **parquet, 2,210 MB** (ZIP is 2,867 MB — prefer parquet) |
| Licence | **`lov2` — Licence Ouverte 2.0** |
| Key | `siret` |
| Paris filter | `codeCommuneEtablissement` starts with **`751`** |
| Paris in NAF 47/56/96 | **149,166** active — re-measured 2026-09-23 over the whole file (was 148,633; 0.36% drift, a month's churn) |
| …after the employee filter | ⚠️ **SUPERSEDED — 50,156 IS NOT REPRODUCIBLE** |
| Built storefronts, 2026-09-23 | **87,164** |

### ⚠️ The employee filter does not exist, and 50,156 cannot be recovered

**Measured 2026-09-23 over all 149,166 bucket rows.** `trancheEffectifsEtablissement`
is `NN` (non déterminé) on **115,248 of them — 77.3%**, so *every banded row put
together is 33,918*. The largest cut this column can produce falls **16,000
short** of 50,156, and the smallest meaningful one gives 32,419. No predicate on
it yields the recorded number.

**Dropping `NN` would also be wrong on its own terms**: only **1,425** rows
record `00` (zero employees), so SIRENE does not code a sole trader as "zero" —
it codes them `NN`. That band is where every owner-run boulangerie lives.

**The build therefore applies NO employee filter**, and the OSM comparison was
re-established from scratch rather than inherited:

| Bucket | OSM (commune) | SIRENE | Ratio |
|---|---|---|---|
| Retail | 27,278 | 41,507 | 1.52× |
| Food service | 16,829 | 33,558 | 1.99× |
| Personal services | 4,866 | 12,099 | 2.49× |
| **Total** | **48,973** | **87,164** | **1.78×** |

⚠️ **The sharp test disproves the old SIRENE figure directly.** `amenity=restaurant`
and NAF `56.10A` mean nearly the same thing: OSM gives **9,058** (against the
recorded 10,642 — the OSM side reproduces), SIRENE gives **16,280** (against the
recorded **10,595**). So the recorded SIRENE count is 1.54× below what SIRENE
contains, on the one definition where both schemes agree — the same shortfall
shape as 50,156 against ~97,000.

**What this does and does not overturn.** France is still a build: the register,
the join, the coverage and the licence are all unaffected. What is overturned is
the *claim* that SIRENE lands at 92.5% of OSM. It does not; it is about 1.78× of
it, and `docs/global_country_shortlist.md`'s France row rests on the old figure.
The residual is **disclosed on the city page**, not filtered away — tuning until
the number matched OSM is what produced 50,156 in the first place.

**Use the PARQUET.** It is columnar, so step 2 reads the ten columns it needs
instead of fifty-four, and its footer can be read over HTTP range requests —
which is how every figure in this brief was obtained without downloading 3 GB.

### Three traps in the resource list itself

- ⚠️ **`StockUniteLegale` is not `StockEtablissement`.** It sits beside it in
  the same dataset — **30,020,346 legal units keyed on `siren`** — and mapping
  it produces the registered-office map this project exists not to make. **It
  was pulled first by mistake while writing the profile.**
- ⚠️ **Match the title with its trailing ` -`.** Without it,
  `StockEtablissementHistorique` and `StockEtablissementLiensSuccession` also
  match.
- ⚠️ **ACTIVE is the letter `A`, not the label `Actif`.** Filtering on
  `"Actif"` returned **zero rows for all six French cities** and was caught
  only because Paris ran first as a control against a known-good number.
  **Keep the control.**

### The siège flag does NOT separate premises from offices here

**90.8%** of active bucket rows are `etablissementSiege`, because a sole
trader's shop is its own siège. Recorded so nobody tries it as a filter.

---

## Coordinates — a JOIN, and there is no geocoding step

| | |
|---|---|
| Dataset | `geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques` |
| Publisher | **INSEE** |
| Rows | **37,901,783**, keyed on `siret` |
| Format | **parquet, 811 MB** |
| Licence | **`lov2`** |
| Coverage | **99.96%** of Paris's bucket rows — 148,576 of 148,633 |

Both a projected pair (`x`, `y`) and WGS84 (`x_longitude`, `y_latitude`), each
**100% populated** in the sampled row group.

### ⚠️ The CRS is per ROW, not per file

There is an `epsg` column, and a sampled row group held **four** values:
**2154** (Lambert-93) on 99.3%, plus 2975 Réunion, 5490 Antilles, 2972 Guyane.

Paris is uniformly **2154**. A pipeline that hard-codes it works here and would
put every pin in the sea if pointed at Fort-de-France — **without raising.**
Read the column.

### It reports its own confidence — use it

`qualite_xy` sampled as **11 (62.5%)**, 33 (17.6%), 12 (15.9%), 22, 21, with
`distance_precision` alongside. **Class 33 is commune-centroid grade** — those
rows are not at a street address and should not be drawn as though they are.
France is the third source in this screen to publish positional quality, after
Denmark's DAWA `kategori` and Hong Kong's ALS `Score`. **Do not average over
it.**

---

## Taxonomy — NAF, keyed at the FINEST level

`premises-taxonomy`'s deciding measurement, run on **6,895 active Paris rows**
against INSEE's own label file (`int_courts_naf_rev_2.xls`, 1,707 codes):

| Level | Distinct | Catch-all |
|---|---|---|
| division (2) | 3 | 18.7% |
| **groupe (3)** | 13 | **49.4%** |
| classe (4) | 46 | 27.8% |
| **sous-classe (5)** | 62 | **19.3%** |

**Key at the sous-classe — Barcelona's shape, not Madrid's.** Grouping at
*groupe* would put half of Paris in "other".

The residual is concentrated: **`96.09Z` *Autres services personnels n.c.a.* is
8.6% alone**, a third of the whole catch-all and entirely inside the personal-
services bucket. The 19.3% is an **upper bound** — the keyword test also
catches labels where *autres* appears incidentally, like
`47.52A quincaillerie, peintures et verres`.

### ⚠️ Exclude distance selling — 15.5% of bucket rows have no storefront

| Code | Share | Label |
|---|---|---|
| `47.91B` | **8.5%** | Vente à distance sur catalogue spécialisé |
| `47.91A` | **4.7%** | Vente à distance sur catalogue général |
| `47.99A` | 2.0% | Vente à domicile |
| `47.99B` | 0.3% | Vente par automates |

These sit **inside the retail division** and are not premises. An earlier note
that 47.91B was "24% of the retail division" understated the problem by looking
at one code of four.

---

## The naming problem, and the guard that makes the fallback safe

| Field | Populated |
|---|---|
| `enseigne1Etablissement` | 29.1% |
| `denominationUsuelleEtablissement` | 34.2% |
| **Either — any premises name** | **42.9%** |

**Paris is the worst-named of France's six cities** (Rennes is 54.3%), which
inverts the usual assumption that the flagship carries the best data.

### The fallback is worth building — and the guard is load-bearing

Measured via `recherche-entreprises.api.gouv.fr` (official, keyless), 750
active Paris rows:

| | |
|---|---|
| Natural persons (`nature_juridique` **1000**) | **8.7%** |
| **Of the UNNAMED rows, natural persons** | **9.4%** |

**So ~nine in ten unnamed rows are companies**, where `denominationUniteLegale`
is a company name and the fallback is safe.

⚠️ **Applied blindly across Paris's ~148,600 bucket rows, the fallback would
publish on the order of TEN THOUSAND individuals' names** — against the ~4,000
Los Angeles nearly shipped. `nature_juridique == "1000"` /
`categorieJuridiqueUniteLegale == "1000"` is the suppression test, and it is
not optional.

⚠️ **Both figures are LOWER BOUNDS.** That API exposes `liste_enseignes` and
`nom_commercial` but not `denominationUsuelleEtablissement`, so rows counted
unnamed there are disproportionately companies.

⚠️ **That API's `total_results` SATURATES AT 10,000**, and it produced a wrong
answer before being caught — every bucket returned exactly 10,000 and two
reported "100% personne physique", plainly false for Paris retail. The control
had tested that the filter was *validated* (a nonsense value 400s), not that
the count was *truthful*. **A cap is a plausible number.** Take shares from
sampled records, never from its counts.

⚠️ **It is also RATE-LIMITED** — it returned HTTP 429 to a single request
during this brief's own check. Fine for a 750-row sample; **not a route for
148,600 rows.** No check is pinned against it for that reason: a flaky check is
worse than none. **The build's guard reads `categorieJuridiqueUniteLegale` from
the `StockUniteLegale` parquet instead** — which is the file this brief warns
against *mapping*, and simultaneously the file the guard *needs*. Named rather
than avoided.

---

## Privacy — partly done upstream

France masks non-diffusible records **at source**:
`statutDiffusionEtablissement` ≠ `O` hides the name, the address **and the
geolocation**. Measured at **13.4%** of active bucket rows.

Per `read-licence` 6b this cuts both ways — it saves building a filter, and it
removes rows that looked available. **Check what survived, not only what was
removed.**

**Run `python scripts/check_personal_exposure.py paris` before publishing**,
and record the verdict in `DECISIONS.md`.

---

## Rail leg — IDFM, and the feed choice is settled

**`https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip`** — IDFM's own,
updated **2026-09-22**.

### ⚠️ Two other GTFS appear beside it and BOTH are third-party

The NAP API's `resources` array **includes** the entries that also appear in
`community_resources`, which is why two readings of it disagreed about whether
an official feed exists at all. Subtracting the arrays settles it:

| Feed | Source | Updated | Available |
|---|---|---|---|
| **`eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip`** | **IDFM's own** | **2026-09-22** | ✅ |
| `gtech-transit-prod.apigee.net/.../odbl/...` | Google | 2023-11-17 | stale 3 y |
| `opendata.itoworld.com/fr/paris/...` | ITO World | 2025-08-21 | ❌ `is_available: false` |

**Building from a modified third-party copy is not acceptable**, and in any
case both are stale or dead.

### ⚠️ CORRECTED by `brief_check.py` — the feed does NOT self-attest

This brief first said the feed "self-attests", which `add-country` requires
before trusting any feed. **It does not.** The check found **14 files and no
`feed_info.txt`**, so the artifact declares no validity window at all.

The `end_date` **2026-10-21** is real but comes from
**`transport.data.gouv.fr`'s metadata ABOUT the feed** — the NAP's assertion,
not the file's. That is a weaker thing, and the distinction is exactly the one
`add-country` draws: *a mirror is usable when the artifact self-attests, and is
not when you must take the mirror's word.*

**It is still the right feed** — the host is IDFM's own (`stif/` on
Opendatasoft), so provenance is not in question. What changes is **how
staleness is detected**: not from the zip, but from the NAP metadata or a
content hash. **`fetch_sources.py` must record the date it downloaded**,
because nothing inside the file will.

⚠️ **This also bears on the licence.** Art. 5.7 requires the page to state the
data's date and update interval — and **neither is inside the artifact**, so
both must be captured at fetch time or they cannot be displayed honestly.

The feed does declare, in NAP metadata, `features` including *position des
stations*, *topologie du réseau* and *tracés de lignes*, and `modes` including
subway, tramway, rail and funicular.

⚠️ **IDFM's network maps and plans are CC BY-NC-ND 3.0 France.** Redrawing from
*data* avoids this entirely, but **no IDFM plan or schematic may be used as a
source or overlay.**

---

## Licence — Licence Mobilités, PERMITTED WITH CONDITIONS

Read in full 2026-09-22; the operative document is
`docs/licenses/france-required-notices.md`. **`mobility-licence` covers exactly
2 of 799 NAP datasets** and Paris is one of them. There is no government-hosted
text — the authoritative document is a 14-page PDF behind a community wiki. It
is **ODbL-derived but NOT ODbL-compatible**.

Art. 3.1 grants worldwide, free, commercial use including **« l'affichage
public »**. **Redrawing is permitted.**

### MUST DISPLAY

> Contient des informations de Réseaux urbains et interurbains d'Île-de-France
> Mobilités (IDFM), présentement mises à disposition aux conditions de la
> « Licence Mobilités »

⚠️ **Art. 5.4(a) prescribes the LINKING too** — the database name hyperlinks to
the dataset URI, « Licence Mobilités » to the licence text.

⚠️ **Plus two obligation shapes this project has never carried**: the **date
the data was last updated**, and its **update interval**. Art. 5.7 forbids use
misleading « quant … à sa date de mise à jour », and **a pre-rendered static
map from a frozen snapshot is exactly that** unless the snapshot date is shown.
The feed's declared `end_date` supplies the interval.

### MUST DO

- **Report source errors** to `contact-prim@iledefrance-mobilites.fr`
  « sans délai ». A data-quality duty, **not** a permission gate.
- **Supply modifications to recipients** (Art. 5.8) — a public repo with the
  pipeline code and derived CSVs, **linked from the site**, satisfies it.
- **Republish the derived station table on the NAP** as a *ressource
  communautaire*. Art. 5.6(b) says a rendered map is a *Création Produite* and
  not a Derivative Database, and the NAP's own published example —
  *"Calcul de la distance à l'arrêt de bus le plus proche pour une liste de
  commerces"* — is filed under **"Non"**. But this project commits
  `outputs/<city>/`. **One upload moots the argument.**

### MUST NOT SAY

**No MTA/WMATA accuracy clause here — the duty is the inverse.** Art. 5.7
requires currency and « l'**exhaustivité** des données disponibles », with a
relevance proviso that covers this project's deliberate exclusions. **The page
should state what was excluded rather than leave it implicit.**

### ⚠️ Revocable

Art. 11.1 terminates **de plein droit, sans préavis** on breach. Unlike
Licence Ouverte, this is a revocable grant.

---

## Region — `Europe`, not `France`

Tag `"region": "Europe"` in `app/cities.py`. Owner's decision 2026-09-22; ten
European countries remain on the screen and describe one readable view between
them. See `docs/scaling_thresholds.md`.

---

## Still unknown — the honest list

- **Both owner calls above** — scope, and the no-name pin.
- **Station density.** Paris measured ~430 OSM rail stops / 317 bucket rows per
  stop, but that is an **estimate from OSM, not the GTFS feed**, and the
  commune/network mismatch makes it non-comparable across French cities.
- **Whether `enseigne1` or `denominationUsuelle` wins** when both are present.
- **Whether the annual *déclaration de conformité* applies** to a static
  density map (L. 1115-5). Creates a *recurring* obligation — worth asking
  `donnees-mobilite@autorite-transports.fr` rather than assuming.
- **IDFM's own licences page contradicts the NAP**, saying its *tracés du
  réseau ferré* are Licence **Ouverte**, reserving Licence Mobilités for
  timetables this project does not publish. **The stricter reading was adopted
  deliberately.** If it were ever relied on, Paris's notice changes.
- **OSM composition validation** — France's is validated on Paris only, and
  the first non-Paris build (now **Marseille**, since Lyon is deferred) must
  re-validate it.

```brief-checks
[
  {
    "id": "sirene-stock-etablissement-parquet",
    "claim": "The SIRENE dataset still publishes a StockEtablissement parquet resource whose title carries the trailing ' -'. If this fails, the resource was renamed or the monthly release changed shape - and the near-misses StockEtablissementHistorique and StockEtablissementLiensSuccession are in the same list",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/",
    "min_bytes": 5000
  },
  {
    "id": "sirene-geolocation-dataset",
    "claim": "INSEE's separate geolocation file is still published and is what makes Paris's coordinate leg a JOIN rather than a geocode. If this fails, Paris needs a geocoder and the band placement changes",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/",
    "min_bytes": 3000
  },
  {
    "id": "idfm-gtfs-is-the-official-feed",
    "claim": "IDFM's own GTFS downloads with no key. THIS IS THE RAIL SOURCE - the two other GTFS on the NAP are third-party (Google, stale since 2023-11-17; ITO World, is_available false) and must not be used",
    "kind": "http_ok",
    "url": "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip",
    "min_bytes": 10000000
  },
  {
    "id": "idfm-gtfs-has-shapes-and-no-feed-info",
    "claim": "The feed carries shapes.txt so the lines can be drawn - and carries NO feed_info.txt, so it declares no validity window and CANNOT be staleness-checked from the artifact. This brief originally claimed it self-attested; brief_check.py disproved that. The absence is pinned here deliberately: if feed_info.txt ever appears, the staleness story gets simpler and this check should be revisited",
    "kind": "gtfs_files",
    "url": "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip",
    "present": ["routes.txt", "trips.txt", "stop_times.txt", "stops.txt", "shapes.txt"],
    "absent": ["feed_info.txt"]
  },
  {
    "id": "transport-nap-idfm-licence",
    "claim": "The NAP still declares mobility-licence on the IDFM dataset. If this changes to lov2, IDFM's own characterisation won and Paris's required notice changes from the Art. 5.4 text to an Etalab attribution",
    "kind": "http_ok",
    "url": "https://transport.data.gouv.fr/api/datasets",
    "min_bytes": 1000000
  },
  {
    "id": "sirene-stock-unite-legale-for-the-guard",
    "claim": "StockUniteLegale is published as parquet and is where categorieJuridiqueUniteLegale lives - the field the natural-person suppression test reads. It is the file this brief warns AGAINST mapping, and simultaneously the file the guard needs, which is why it is named rather than avoided",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/",
    "min_bytes": 5000
  },
  {
    "id": "excluded-stations-count",
    "claim": "76 metro stations fall outside the commune of Paris. THE FIRST NUMERIC CHECK IN THIS PROJECT, and it exists because this brief said 77 and 322 while the feed gave 76 and 321 - and a 7/7 pass that same morning could not see it, since every other check kind here tests liveness rather than a number. If this fails, correct the brief to what the build measured; do not widen the tolerance",
    "kind": "row_count",
    "path": "outputs/paris/excluded_stations.csv",
    "expect": 76
  },
  {
    "id": "excluded-stations-communes",
    "claim": "The 76 excluded stations lie across 34 communes, each named rather than counted - Los Angeles' standard. A drop here means the Ile-de-France commune layer stopped resolving names and stations are being recorded as '(outside Ile-de-France)'",
    "kind": "row_count",
    "path": "outputs/paris/excluded_stations.csv",
    "column": "commune",
    "distinct": true,
    "expect": 34
  },
  {
    "id": "naf-labels-available",
    "claim": "INSEE's NAF label file is still served. The taxonomy's catch-all measurement (19.3% at sous-classe) was taken against it, and a residual detected by CODE SHAPE instead reported 0.0% - a broken test, not a low share",
    "kind": "http_ok",
    "url": "https://www.insee.fr/fr/statistiques/fichier/2120875/int_courts_naf_rev_2.xls",
    "min_bytes": 200000
  }
]
```
