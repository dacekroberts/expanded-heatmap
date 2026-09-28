# Data sources — Spain

Part of [`data_sources.md`](../data_sources.md), the project's provenance
record, which was split by country on 2026-09-27. This file holds the
Spain rows of the tables there and the source sections about its cities,
moved verbatim under the same headings. The numbered notices this project must
display, the removal-request commitment and the deploy gate are in the entry
point, not here.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Madrid | Ayuntamiento de Madrid **Censo de locales, sus actividades y terrazas de hostelería y restauración** (CKAN package `200085-0-censo-locales`, resource `200085-5-censo-locales` — the locales × actividades join, 225,660 rows × 47 columns) | All three buckets, via the city's own `epigrafe` scheme — a **premises field survey**, not a licence register, so the Montréal and Barcelona shape rather than the Philadelphia one | **Resolved at fetch time**, not hardcoded: `https://datos.madrid.es/api/3/action/package_show` is queried for the package and the download URL taken from the resource whose id is `200085-5-censo-locales`. **THE DOWNLOAD URL ROTS** — it embeds a build timestamp (`200085_20260922_053829.csv`) that changes on every refresh, so a hardcoded URL 404s silently within days. The first source in this project whose URL is not durable. Note `datos.madrid.es` is **CKAN 2.9.11 at the bare host**; an earlier screen recorded it unreachable on the path `/egob`, which was a fact about the guess rather than about the portal | none server-side (CKAN serves the whole file). **UTF-8 WITH BOM and SEMICOLON-delimited**, both declared in `config.py` rather than inferred — a BOM read as data corrupts the first column name. Step 2 keeps `desc_situacion_local == 'Abierto'`, which is also the residence filter: the register carries **`Uso vivienda` (8,486)** as its own status, so residence is answered by the source rather than inferred, Canada's licence-level pattern rather than the US parcel join. **This register carries NO registrant name at all** — all 47 columns were listed on 2026-09-22 and not one is an owner, titular, NIF/CIF, razón social or contact field, the same structural position as Edmonton's register; step 2 asserts twelve personal column names stay absent and **raises** if a kept premises lacks its `rotulo` | 2026-09-22 |
| Barcelona | Ajuntament de Barcelona **Cens de locals en planta baixa amb activitat econòmica** (CKAN package `cens-locals-planta-baixa-act-economica`, resource `99764d55-b1be-4281-b822-4277442cc721`) | All three buckets, via the census's own four-level Catalan activity scheme — a **premises field survey**, not a licence register, so the Montréal and Madrid shape rather than the licence cities'. **THE YEAR IS A DECISION:** the **2022** survey holds 66,088 rows and is complete; the **2024** resource (`38babeec-5c47-43d3-84e7-b13a4b89004f`) holds 44,000 and is **geographically incomplete** — Sant Andreu −83%, Nou Barris −76%, Horta-Guinardó −69% against 2022, while Ciutat Vella is −5%, so a map built on it would show the periphery as commercially dead | `https://opendata-ajuntament.barcelona.cat/data/api/3/action` — `datastore_search`, paged at 10,000 | `fields=` restricted to **11 of the census's 50 columns**, and that list IS the privacy control. `Nom_Local` is a trade name and 100% populated, so there is **no registrant-name column to fall back to**; `Referencia_Cadastral` exists in the source and is deliberately never requested. **The vacancy filter is applied in step 2 and is mandatory**: `Nom_Principal_Activitat` is `Actiu` on 58,908 rows and `Sense activitat Econòmica` on 7,180 — empty units for sale or to let. Licence **CC BY 4.0** plus the Open Data BCN terms — notice **21**, and the outstanding duty to notify the Council | 2026-09-22 |

### Madrid — endpoints and findings, verified 2026-09-22

**The first Spanish city, and the first anywhere in this project whose rail
comes from an operator's ArcGIS feature services rather than a feed.** Country
profile: `docs/spain_step0_endpoints.md`. Step 0 evidence and its checks:
`docs/build_briefs/madrid.md` (13/13).

**Businesses** — Ayuntamiento de Madrid, *Censo de locales, sus actividades y
terrazas de hostelería y restauración*. `datos.madrid.es` is **CKAN 2.9.11 at
the bare host** (an earlier screen recorded it unreachable on the path
`/egob` — a fact about the guess). Package `200085-0-censo-locales`, resource
**`200085-5-censo-locales`**, the locales × actividades join: 225,660 rows ×
47 columns, **UTF-8 with BOM, semicolon-delimited**, coordinates in
**EPSG:25830**.

> **THE DOWNLOAD URL ROTS.** It embeds a build timestamp
> (`200085_20260922_053829.csv`) that changes on every refresh, so
> `step2_clean_businesses.py` resolves it from `package_show` by **resource
> id** at fetch time. This is the first source in the project whose URL is not
> durable, and a hardcoded one 404s silently within days.

A **premises field survey**, not a licence register — the Montréal and
Barcelona shape — so the "79% of this register is landlords" correction that
Philadelphia and Washington D.C. need does not apply.

**This register carries no registrant name at all** - the same structural
position as Edmonton's, where no pin can be a person's name. All 47 columns
were listed on
2026-09-22 and not one is an owner, titular, NIF/CIF, razón social or contact
field; the only name-shaped column is `nombre_agrupacion`, which names a
**market or shopping centre** a unit sits inside, and step 2 does not load it.
New York, Philadelphia, Miami and Boston all HAVE such a column and decline to
download it. Madrid has none to decline. Step 2 asserts twelve personal column
names stay absent, loads columns by name, and **raises** if any kept premises
lacks a `rotulo` (shop sign) — so there is no fallback path even in principle.

**Residence is answered by the source, not inferred.** `desc_situacion_local`
carries **`Uso vivienda` (8,486)** — the unit reverted to residential use — as
its own status value, and step 2 keeps only `Abierto`. Canada's licence-level
pattern rather than the US parcel join.

> **THE COORDINATE COLUMNS ARE 100% POPULATED AND PARTLY INVALID**, and the
> zeros are stored as the **string `'0.0'`**, so an is-it-populated test passes
> them. In EPSG:25830 a zero projects to the Atlantic off West Africa and
> vanishes on a station-radius map rather than erroring. Measured on the full
> download: **34,316 of 159,787 open rows (21.48%)**, but only **9.21%** once
> the storefront filter is applied — the zeros concentrate in tourist flats
> (85.9%), hostales (74.7%) and offices, categories this project does not map.
> **Unlike Los Angeles the loss is biased AWAY from the mapped rows**, so no
> geocoding leg is needed and Spain's CartoCiudad stays unprobed.

**Rail** — Consorcio Regional de Transportes de Madrid (CRTM),
`services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/M4_Red/FeatureServer`,
layer **0 `M4_Estaciones`** (293 station-per-line points) and layer
**4 `M4_Tramos`** (560 polylines). Both natively **EPSG:25830**, the same CRS as
the premises data, so the build never reprojects for geometry.

> **NOT the GTFS, and that is a LICENCE consequence rather than a preference.**
> CRTM publishes the same network twice: a GTFS feed it stopped refreshing in
> **2025-05-30**, and feature services it still edits (**2026-06-05**). Its
> licence obliges a reuser to keep displayed information *"siempre
> actualizada"*, which a feed abandoned sixteen months ago cannot satisfy.
> `scripts/brief_check.py` watches the feature layers' `editingInfo.lastEditDate`
> with the `arcgis_layer` check kind, because the pre-existing tripwire watched
> the FEED and would have kept passing while the decision it guarded went stale.

**Boundary** — *Término municipal de Madrid*,
`geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/LIMITES_ADMINISTRATIVOS/Termino_Municipal/Termino_Municipal.zip`
(shapefile, EPSG:25830). Step 1 checks its **area (604.0 km²)** and its
coordinate magnitudes rather than its declared CRS — Surrey's declared
EPSG:4326 and contained UTM metres.

**Licences — both PERMITTED WITH CONDITIONS, both `Ley 37/2007` reuse
licences**, which is Spain's country-level pattern.

- **Ayuntamiento de Madrid**: CKAN declares `cc-by` / **CC BY 4.0**, but CC BY
  is not the whole instrument — the portal's *Condiciones generales* are
  **binding by use** (*"obligan a cualquier persona y/o empresa que reutilice
  datos por el mero hecho de hacer uso"*). Reuse for commercial purposes is
  authorised, expressly including *modificación, adaptación, extracción,
  reordenación y combinación*. Conditions: do not distort the sense of the
  information; **cite the source** (a form is offered — *"Origen de los datos:
  Ayuntamiento de Madrid"*); **state the last-update date**; do not suggest the
  Ayuntamiento sponsors the reuse; preserve reuse metadata; and
  **re-identification of anonymised data is expressly prohibited**.
  `/pages/aviso-legal` is a **website disclaimer** written for web pages rather
  than data, so it is recorded as read and not as governing.
- **CRTM**: `https://www.crtm.es/licencia-de-uso`, a *licencia-tipo* under
  Ley 37/2007 art. 4.2(b). Commercial reuse and modification granted.
  Share-alike binds **the data**; *"las obras derivadas añadiendo valor pueden
  ofrecerse bajo licencias diferentes"*, and a ring-density map is a
  value-added derivative rather than a redistribution. Conditions: cite CRTM
  **"especificando si son datos en bruto o explotados"** (a
  disclosure-of-transformation duty, the Montréal and INEGI family — a bare
  credit does not satisfy it); display **"Powered by CRTM"** with a link to
  `http://www.crtm.es/`; do not falsify or damage CRTM's image; preserve reuse
  metadata; do not imply sponsorship. **CRTM monitors access** and may block a
  reuser whose fetching degrades its systems.

> **A CITED LICENCE URL THAT 404s IS NOT AN ABSENT DOCUMENT.** CRTM's own
> dataset metadata points at `datos.madrid.es/egob/catalogo/aviso-legal`, which
> returns 404; the live pages are `/pages/aviso-legal` and
> `/pages/condiciones-de-uso`, found by listing the portal's own links rather
> than guessing a second path.

> ### ✅ RESOLVED 2026-09-22 — the "siempre actualizada" clause is a
> misrepresentation rule, not a liveness requirement
>
> Raised as an owner decision and settled by reading the clause **in place**
> rather than in isolation. It is not free-standing: it is one of **four
> sub-obligations** under a single governing prohibition —
>
> > *"El agente reutilizador tiene expresamente prohibido **desnaturalizar el
> > sentido de la información**, estando obligado a:"*
> > — no manipular con mala fe ni falsear la información
> > — **garantizar que la información mostrada en su sistema esté siempre actualizada**
> > — no menoscabar o dañar la imagen pública del CRTM
> > — no utilizar la información en sitios … actos ilegales
>
> Its three siblings are all about **misrepresentation and reputational harm**,
> so the clause targets presenting stale data *as though it were current* — not
> a requirement that the system be live. No static derivative could satisfy the
> literal reading, and a licence expressly granting *"copia, difusión,
> modificación, adaptación, extracción, reordenación y combinación"* plainly
> does not intend to forbid every static product.
>
> **The next clause confirms the mechanism**: *"Deben conservarse, no alterarse
> ni suprimirse los metadatos sobre **la fecha de actualización**"*. The licence
> expects the data to carry a date and the reuser to preserve it, which is
> exactly how a dated snapshot meets a currency obligation.
>
> **What this project does, which is stricter than the clause requires.** It
> rejected CRTM's own Metro GTFS — which downloads cleanly — precisely BECAUSE
> CRTM stopped refreshing it in May 2025, and took the maintained feature
> layers instead. The notice states CRTM's own last-update date (5 June 2026)
> and that the map shows the network as recorded then. And
> `scripts/brief_check.py`'s `arcgis_layer` check carries `max_age_days` on
> both layers, so this is a commitment a check FAILS on rather than one a
> comment promises.
>
> This is a reasoned position on a clause that is clear once read in context,
> not a generous reading of an ambiguous one — the distinction `read-licence`
> step 8 draws. The full text is stored at
> `docs/licenses/crtm-licencia-de-uso.txt` so the reading can be checked against
> the document rather than against this summary.

**Gate 3 — the operator's published count — RUNS for Madrid and reconciles.**
`metromadrid.es/es/quienes-somos/metro-de-madrid-en-cifras`: **303 estaciones**,
296,78 km, updated 2026-05-18. Against CRTM's 293 station-per-line records plus
Metro Ligero ML1's 9, that is 302 — a residual of **one**, consistent with
Pinar de Chamartín being counted by the operator in both networks. Two of the
operator's own conventions have to be applied first: it counts a station **once
per line** (which is why 303 sits against 242 distinct names) and it **includes
ML1**, which it operates. **303 must never reach the page**: this project maps
**193 distinct stations inside the término municipal**, a different quantity in
three ways at once.

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Madrid | **CRTM Metro — ArcGIS feature services, NOT a GTFS feed** (Consorcio Regional de Transportes de Madrid) | `https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/M4_Red/FeatureServer` — layer **0 `M4_Estaciones`** (293 station-per-line points) and layer **4 `M4_Tramos`** (560 polylines) | 2026-09-22 | **The first rail in this project from an operator's feature services rather than a feed, and the reason is a LICENCE condition rather than a preference.** CRTM publishes the same network twice: a Metro GTFS it stopped refreshing on **2025-05-30**, and these services it still edits (**2026-06-05**). Its licence obliges a reuser to keep displayed information *"siempre actualizada"*, which a feed abandoned sixteen months ago cannot satisfy — so the feed is rejected although it downloads cleanly. `scripts/brief_check.py` watches these layers' `editingInfo.lastEditDate` with its `arcgis_layer` check kind, because the pre-existing tripwire watched the FEED and would have kept passing while the decision it guarded went stale. Both layers are natively **EPSG:25830**, the same CRS as the premises register, so the build never reprojects for geometry |
| Madrid | **CRTM Metro Ligero — ArcGIS feature services** (added 2026-09-27, the tram rescope; held for review time) | `https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/M10_Red/FeatureServer` — layer **0 `M10_Estaciones`** (57 station-per-line points) and layer **4 `M10_Tramos`** (100 polylines) | 2026-09-27 | **The Metro layers' sibling, under the same terms**: the ArcGIS item "Datos Abiertos: Elementos de la Red de Metro Ligero" declares the same `http://www.crtm.es/licencia-de-uso` and "© CRTM" as `M4_Red`, and was last edited the same day (**2026-06-05**), so the existing CRTM notice and its stated date cover it unchanged. Same schema, EPSG:25830. **Only ML1 is read** (owner, 2026-09-27): ML2 and ML3 are stubs inside Madrid and ML4 is Parla's tram. Parla's stations carry `LINEAS` "4" while its tramos are "4-1"/"4-2". ML1's colour is not in these layers: it is read from the sibling `M10_Lineas` service's renderer (rgb 39, 84, 211) |
| Barcelona | **OpenStreetMap** — 14 metro refs (L1–L12, with L9 and L10 each split into two disconnected segments) plus the **Montjuic (TMB)** and **Vallvidrera (FGC)** funiculars: 16 drawn lines across **two operators** | The three Overpass mirrors in `pipeline/osm.py`, bbox `41.30,2.03,41.50,2.30` | 2026-09-22 | **Why not the agency feed:** TMB's GTFS is registration-gated (`api.tmb.cat` returns **401** unauthenticated, watched by `brief_check.py`), and the agency route would need **four feeds** — TMB, FGC, TRAM and TRAM Besos — with four licences and four cadences. OSM returns the network in one query with **every line carrying its own name and colour**, so no palette is invented. **Scope is the operators' own `network` tag**: the 14 metro refs and both funiculars are tagged `Metro de Barcelona` or `Metro del Valles`; **FT (Tibidabo)** carries no network tag and is run by the municipal parks company, and trams T1–T6 are `Trambaix`/`Trambesos` — both excluded. ⚠️ **The mirrors disagree about this bbox** (tram/funicular counts, and `L10N` vs `L10 Nord`), so the fetch is cached and the build normalises refs. ODbL 1.0 — notice **1** and the rail-geometry notice |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Madrid | **Término municipal de Madrid** (Ayuntamiento geoportal, zipped shapefile) | `https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/LIMITES_ADMINISTRATIVOS/Termino_Municipal/Termino_Municipal.zip` | Whole city, native **EPSG:25830**. Step 1 checks its **area (604.0 km², accepted only within 500-700)** and the magnitude of its coordinates rather than its declared CRS — Surrey's layer declared EPSG:4326 while containing UTM metres, and a district polygon would pass a feature-count check. 49 stations fall outside the city and are excluded |
| Barcelona | **OpenStreetMap** — the `admin_level=8` relation named `Barcelona`, polygonised from its `outer` member ways | The three Overpass mirrors in `pipeline/osm.py`, bbox `41.30,2.03,41.50,2.30` | Whole municipality. **The bbox is load-bearing**: an unbounded name search for `Barcelona` also matches the province and the comarca, which is the shape of the error that selected *Guadalajara, Spain* during that build. Step 1 gates the **area at 101.4 km² ± 4** and measured **101.3**. It matters more here than in most cities — L8 and L10 Sud run to Cornellà, Sant Boi and El Prat and L9 Sud to the airport, so **50 of 162 stations fall outside** and are recorded in `outputs/barcelona/excluded_stations.csv` rather than silently kept |

## Licences and terms of use

### Explicit and permissive — confirmed

#### Madrid — `censo de locales`, read 2026-09-22 (**BUILT 2026-09-22**)

**PERMITTED WITH CONDITIONS.** Two documents apply and both were read.

**1. The declared licence.** `datos.madrid.es` CKAN gives `license_id = "cc-by"`,
`"Creative Commons Attribution 4.0 International (CC BY 4.0)"`, `isopen: true`,
author `Ayuntamiento de Madrid`, on both `200085-0-censo-locales` and its
historical twin. **A deliberate choice**: the portal's `license_list` also
offers `cc-by-nc` and `cc-by-nc-sa`, which would forbid this project, plus four
bespoke restrictive sets (Madrid Destino, Bibliotecas, EMT, the general
conditions below).

**2. The general conditions, which bind by conduct.** *Condiciones de uso*
links *"Condiciones generales para la modalidad general de puesta a disposición
de los documentos reutilizables del Ayuntamiento de Madrid"*, and that document
opens by making itself binding **without any acceptance step**:

> "Las presentes condiciones generales **obligan a cualquier persona y/o empresa
> que reutilice datos por el mero hecho de hacer uso** de los documentos
> sometidos a ellas."

Structurally this is Philadelphia's shape — terms incorporated by the act of
use rather than by a licence field. **The content is the opposite.** The grant
is broad and explicit:

> "permiten la reutilización de los documentos y datos sometidos a ellas **para
> fines comerciales y no comerciales** … la reutilización autorizada incluye
> actividades como la **copia, difusión, modificación, adaptación, extracción,
> reordenación y combinación** de la información."

plus a free, non-exclusive assignment of any IP rights, worldwide, for the
maximum term the law allows. It expressly covers data "en sus niveles más
desagregados o 'en bruto'".

**Six obligations, and four of them go beyond CC-BY:**

| | Obligation |
|---|---|
| 1 | **Prescribed attribution wording** — *"Origen de los datos: Ayuntamiento de Madrid"*. CC-BY wants attribution; Madrid says what it must say |
| 2 | **State the last-update date** of the documents reused, where the original carried one. **CC-BY does not require this** |
| 3 | **No implied endorsement** — must not "indicar, insinuar o sugerir que el Ayuntamiento de Madrid participa, patrocina o apoya" the reuse |
| 4 | **Do not distort the meaning** — *"Está prohibido desnaturalizar el sentido de la información"* |
| 5 | **Preserve the metadata** on update date and reuse conditions; do not alter or delete it |
| 6 | **Re-identification is expressly prohibited** — "está expresamente prohibido realizar labores de re-identificación de personas a partir de estos datos y otras fuentes" |

**Obligation 4 is the fourth appearance of the transformation family** — after
INEGI, Montréal and Seoul's KOGL. Ring density, bucketing and storefront
filtering are all interpretation, so the notice must say the map interprets the
data rather than merely crediting the source. **Obligation 6 is the first time
a licence has contractually forbidden what this project's privacy invariant
already forbids voluntarily**, and it bears directly on the `rotulo` field:
combining a trade name with a precise address is exactly the operation the
clause is about, so the existing `check_personal_exposure.py` gate is a licence
obligation here, not only a house rule.

Also recorded: the disclaimer is ordinary (no warranty, no guarantee of
continuity, reuser bears the risk), and reusers are placed under the sanctions
regime of **article 11 of Ley 37/2007** on public-sector information reuse.

**6b — privacy work already done at source?** Not applicable in the French or
Edmonton sense: the census carries premises, not people. `rotulo` is a shop
sign. Obligation 6 above makes the project's own residence check contractual.

#### CRTM (Consorcio Regional de Transportes de Madrid) — read 2026-09-22 (**BUILT 2026-09-22**)

**Source:** `http://www.crtm.es/licencia-de-uso`, the *Licencia de datos
estáticos del CRTM*, which `mdb-794` (Metro de Madrid GTFS) declares. Read in
the browser because it is the licence Madrid's rail leg depends on, and no
transit licence is ever assumed from the city's business licence — LA Metro's
GTFS forbids modifying data while the same city's registry is CC0.

**Verdict: PERMITTED WITH CONDITIONS.** The granting sentence:

> *"Las presentes condiciones generales definidas en esta licencia permiten la
> reutilización de los documentos sometidos a ellas para fines comerciales y no
> comerciales"*

and reuse is defined to include *"la copia, difusión, modificación,
adaptación, extracción, reordenación y combinación de la información"* — so
redrawing line geometry onto a map is squarely inside it. Rights are ceded
*"gratuita y no exclusiva"*, worldwide.

**On share-alike — it applies to the DATA, not to this project's map.** The
scope section requires sharing CRTM data *"bajo el mismo tipo de licencia"*,
but says in the next breath that **"las obras derivadas añadiendo valor pueden
ofrecerse bajo licencias diferentes"** — value-added derivative works may be
offered under different licences. A ring-density map is a derivative work
adding value, not a redistribution of the feed. Recorded explicitly because
ODbL-style share-alike is a live question elsewhere in this project (CDMX).

**The condition that decides Madrid's rail route:**

> *"Garantizar que la información mostrada en su sistema esté siempre
> **actualizada**"*

**Displaying an expired feed is in direct tension with this.** `mdb-794`'s
calendar ended 2026-05-27. The build brief had listed "use the expired feed
anyway, since station positions do not expire" as a defensible third option.
**It is no longer defensible on these terms** — not because station geometry
goes stale, but because the licence obliges the reuser to keep what is shown
up to date, and this project cannot honour that with a feed CRTM has stopped
refreshing. Madrid's rail leg must come from a current CRTM item or from
OpenStreetMap.

**Obligations, all of them conditions rather than courtesies:**

| | |
|---|---|
| 1 | **Prescribed wording — "Powered by CRTM"**, with a link to `http://www.crtm.es/`. The licence says it *"debe quedar claramente"* on digital platforms: *"webs, foros, blogs, apps"*. **This is a sixth prescribed notice for this project, and the first from a Spanish source** |
| 2 | **Cite CRTM as the data source, stating whether the data is raw or processed** — *"especificando si son datos en bruto o explotados"*. This is the disclosure-of-transformation family, like Montréal's and INEGI's: a bare credit does not satisfy it, the notice has to say the data was processed |
| 3 | **Keep the information shown up to date** (above) |
| 4 | **Do not distort the meaning**, manipulate in bad faith, or falsify |
| 5 | **Preserve the metadata** on update date and reuse conditions; do not alter or delete it |
| 6 | **No implied endorsement** — must not *"indicar, insinuar o sugerir que el CRTM … participa, patrocina o apoya"* the product |
| 7 | Must not be used to damage CRTM's public image or the public transport system, nor placed alongside illegal acts |
| 8 | CRTM **monitors access** and may block a reuser whose fetching degrades its systems. A pipeline that re-downloads politely is fine; a tight retry loop is not |

**What this project must therefore display for Madrid:** *"Powered by CRTM"*
linked to crtm.es, plus a statement that the data is processed rather than
raw. Both are in addition to the Ayuntamiento de Madrid wording already
recorded above for the business leg — **Madrid owes two separate attributions
from two separate licences.**

#### Barcelona — Open Data BCN, read 2026-09-22 **from the Internet Archive** (**BUILT 2026-09-22**)

**How it was read, and the limit on that.** `opendata-ajuntament.barcelona.cat`
serves **hCaptcha** on `/en/avis-legal`, `/ca/avis-legal` and
`/es/aviso-legal` alike, and this project does not defeat CAPTCHAs. The legal
notice and the terms it points to were therefore read from the **Internet
Archive**: the notice at snapshot **2025-01-18**, the terms of use
(`/en/condicions-us`) at **2025-03-28** — the newest capture of that page that
exists. That is a public archive of a public page, not a bypass.

⚠️ **An archived copy is not the live document**, and these terms explicitly
reserve the right to change: *"Barcelona City Council may at all times add to,
remove or amend the data sets published as well as these Terms of use … any
change that is made shall take effect as soon as it is published."*

### ✅ DECIDED 2026-09-22 — Barcelona is published on a DISCLOSED POSITION

This section previously said a human should confirm the live page before
publishing. That was attempted on 2026-09-22 and **the page returned
hCaptcha** — *"PLEASE PROVE THAT YOU ARE HUMAN"* — which this project does not
defeat. The owner's decision was to publish anyway, on a disclosed position,
rather than hold the city. Recorded here because **a precondition that is
knowingly not met has to say so**, rather than sit in the file reading like a
plan somebody will get to.

**What IS verified, live, today.** The *declared licence* needs no CAPTCHA:
`package_show` on the CKAN API returns `license_id: CC-BY-4.0`, `license_title:
Creative Commons Attribution 4.0`, with the package last modified 2025-12-02.
So the grant this project relies on is confirmed current from the publisher's
own machine-readable metadata. It is only the *terms page* that is unconfirmed.

**What the gap actually risks, stated plainly.** The stored terms impose four
obligations; this project meets three on the page and records the fourth as an
owner action. If the live terms have since become **more permissive**, nothing
is wrong. If they have become **more restrictive**, this project would be
complying with a superseded version — and that is the real exposure, sized by
the fact that no capture since March 2025 shows any change at all.

**Why that is tolerable here and was NOT in Philadelphia.** Philadelphia's
operative sentence is a flat prohibition on redistribution, read from the live
page; the question there is what a clause MEANS. Here the clause is not in
doubt and neither is the grant — the question is only whether a page has
changed since its last capture, and the licence field says it has not. Same
shape of answer as Philadelphia (publish on a disclosed reasoned position), a
weaker premise required to reach it.

**What happens if that turns out to be wrong.** The standing commitment applies
unchanged and is the reason this is safe to decide rather than agonise over: a
removal request from Barcelona City Council is honoured, not argued — the layer
or the whole city comes down first and the reasoning is recorded afterwards.
**Re-read the live terms whenever the CAPTCHA can be passed**, and record the
result here either way.

**Verdict: PERMITTED WITH CONDITIONS.** The granting text:

> *"… the conditions of Creative Commons-Attribution (CC-BY 4.0) licence,
> under which such data are allowed: to be copied, distributed and published
> … to provide the basis for derived works as a result of their analysis or
> study … to be used for commercial or non-commercial purposes, provided that
> such use does not constitute a public-authority activity … to be amended,
> changed and adapted."*

"Derived works as a result of their analysis or study" describes this project
directly.

⚠️ **A carve-out that must be checked per dataset: CC BY-ND.**

> *"However, any data involving third-party participation may be reused under
> a Creative Commons Attribution-**NoDerivs** (CC BY-ND 4.0) licence"*

The census declares `CC-BY-4.0` in the CKAN API, so it is not in the ND class
on its own metadata — but the carve-out exists and any *second* Barcelona
source has to be checked for it separately. (The clause is also internally
odd: it lists *"to be amended, changed and adapted"* among the permissions
**under a NoDerivs licence**, which NoDerivs by definition forbids. Treat the
named licence as controlling, not the bullet list.)

**Obligations — four of them, and two are unusual:**

| | |
|---|---|
| 1 | **Prescribed attribution wording**: *"Source of the data: Barcelona City Council"*, with suggested HTML markup linking `barcelona.cat/opendata` |
| 2 | **Modifications must be identified at distribution** — *"Any amendment or change made to the data sets … shall be identified as such at the time of their distribution."* The disclosure-of-transformation family again: ring density and storefront filtering are changes, so a bare credit does not satisfy this |
| 3 | ⚠️ **Users must NOTIFY the Council of the project** — *"Users are required to inform Barcelona City Council of every project relating to or derived from their use of the data sets."* **This is a new obligation class for this project**: an affirmative action owed to the publisher, not a line of text on a page. Nothing in the built cities has required it |
| 4 | Council **may require reuse statistics** from the user |

**Plus the Spanish Act 37/2007 Article 8 general conditions**, which the terms
incorporate expressly:

- the content of the information **may not be altered**
- the meaning **may not be distorted**
- **the source must be cited**
- ⚠️ **"the most up-to-date data are referred to"**

**That last one bears directly on the census-year decision.** The build brief
recommends the **2022** resource because the 2024 one is geographically
incomplete (down 69–83% in four districts). Article 8 pulls the other way.
The two are reconcilable — using the most recent *complete* survey, and saying
so on the page — but it must be a stated decision, not a silent one, and the
page must name the census year either way.

**Not claimed:** the *"Open Data BCN"* denomination and logo are registered
trademarks (M 3713011, M 3746181) and are excluded from reuse, as are images
and icons. Line names and category labels are not claimed.

**No warranty**: the Council disclaims integrity, updating and accuracy, and
excludes liability.
