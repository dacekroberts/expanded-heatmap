# Spain, start to finish: two cities that shared a country and almost nothing else

Companion to [`canada_retrospective.md`](canada_retrospective.md) and
[`mexico_retrospective.md`](mexico_retrospective.md). Per-city numbers are in
`DECISIONS.md`; this is what the *country* cost and what it changed.

**Cities built:** Madrid (17), Barcelona (18). **Candidates screened:** six,
reduced to two by measurement.
**Country shape:** bespoke per city. No national register, no national feed.

---

## The one-line version

**Spain is the country that proves a country profile can be worth almost
nothing.** Mexico's second city inherited a register, a taxonomy, a licence and
a loader. Spain's second city inherited **the accent-and-encoding discipline**
and essentially nothing else:

| | Madrid | Barcelona |
|---|---|---|
| Business source | Censo de locales (Ayuntamiento) | Cens de locals (Ajuntament) |
| Rail source | **CRTM ArcGIS feature services** | **OpenStreetMap** |
| Projected CRS | EPSG:25830 | EPSG:25831 |
| Taxonomy | own 3-level scheme | own 4-level scheme, **keyed at the opposite end** |
| Language | Spanish | **Catalan** |
| Licence | CC BY + binding *Condiciones generales* | CC BY + terms behind **hCaptcha** |
| Terms carry | last-update-date duty, re-identification ban | ⚠️ **a duty to notify the Council** |

Both are premises field surveys, which is the one deep thing they share — and it
is why Madrid's **261 per station** sits beside Montréal's 252 rather than
beside Mexico City's 818.

### The reasoning that chose Spain was half wrong, and the wrong half matters

Spain was chosen over France partly because *"the Mexico build gives context
strength with Spanish text."* Measured:

- **SCIAN does not transfer** — Madrid uses its own three-level scheme.
- **Barcelona is Catalan**, not Spanish.
- **Spain is bespoke per city** where Mexico was one national register.

What *did* transfer was the accent and encoding discipline, `character_set="auto"`
included. **Linguistic adjacency is not data adjacency.** Do not let it stand in
for a measured prior again.

---

## Six candidates to two, and the correction that matters

Spain was carried as *"2 now, 6 total"* on the argument that *"two of the three
Spanish cities probed have had a premises census, which raises the prior
sharply."* All three remaining Band B cities were then probed, and **all three
are negatives**:

- **Valencia** — CKAN, **290 packages** enumerated in full. The only
  commercial-adjacent names are container locations, noise monitors and
  `zones-dactivitats` (zoning polygons).
- **Málaga** — CKAN, **1,377 packages**. `empresas-y-sectores` is explicitly
  *"empresas que se encuentran en parques empresariales"*; the rest are
  `equipamientos` layers covering a handful of malls and municipal markets.
- **Bilbao** — 344 datasets across 35 pages with **no search box at all** (its
  only form control is a sort order). Enumerated via `datos.gob.es` instead:
  600 datasets, whose entire commercial holding is *"Barómetro del comercio
  minorista"* — survey aggregates by employment stratum.
- **Sevilla — UNREACHABLE, recorded as that rather than as a negative.** Four
  routes failed: `sevilla.org` does not resolve, nor `datosabiertos.sevilla.org`
  or `.es`; its ArcGIS Hub answers *"Can't access this content … Sign In"*; and
  `datos.gob.es` has **no Ayuntamiento de Sevilla publisher at all**. *Nothing
  was learned about whether Sevilla licenses premises* — only that four ways of
  asking failed.

**Madrid and Barcelona are the exceptions in Spain, not the rule.** A prior
carried as a reason rather than a measurement inflated a country threefold.

### The right primitive for any future Spanish city

Not the city's own portal. **`datos.gob.es`** federates every municipal portal
and speaks DCAT over a documented API, so one publisher enumeration
(`/catalog/dataset/publisher/<id>`) reaches a city whose own site is paginated,
searchless or dead.

**With one caution that will otherwise cost a day:** searching that catalogue by
*title* returns almost entirely INE (publisher `EA0042823`) aggregate
statistical tables — *Locales por provincia y condición jurídica*, hotel
occupancy — which look exactly like premises data and are not. **Enumerate by
publisher, never by title.**

---

## Madrid: a third rail loader, and a coordinate field that lies quietly

**Rail comes from a regional authority's ArcGIS feature services** — the first
city whose operator publishes its network that way. `load_geojson_line_shapes()`
returns the same contract as the GTFS and OSM loaders, carrying the OSM one's
empty-file guard. **Third time the don't-fork-`render_heatmap` rule has been
paid for and held.**

It also passes both halves of the rail question, which is the trap `osm-rail`
names: Korea's station dataset has 1,099 stations and **no lines**, which passes
a stations-only screen and fails this project. CRTM publishes *Elementos de la
Red* **and** *Líneas de la Red* as separate layers — and `accesos` as a third,
so the entrances trap is avoided by **layer choice** rather than de-duplication.

**21.48% of coordinates are a literal zero.** `coordenada_x_local`/`_y_local`
are non-empty on every row; 34,316 of them are `0`, which projects to the
Atlantic off West Africa and **vanishes silently rather than erroring**. The
rate had been disputed across three denominators (19.99%, 13.2%, 5.85%) and was
deliberately deferred to step 2, on the principle that **the rate is not the
deliverable — the distribution is.** Los Angeles' bad coordinates were 22% of
businesses registered since 2020 against ~1% of older ones; if Madrid's zeros
had clustered by district or `desc_epigrafe` they could not simply be dropped.

**Station names are re-cased for display**, and `.title()` is wrong in Spanish:
it yields "Plaza De Castilla" and "Puerta Del Sur", which no sign in Madrid
says. A stopword list keeps prepositions lower case; tokens with digits survive
("Aeropuerto T-4"); the register's own string is kept in `station_source`. This
is the *display* half of normalise-for-joins-never-for-display.

---

## Barcelona: a four-level taxonomy keyed at the opposite end from Madrid's

**Keyed on `Nom_Activitat`, the FINEST of the census's four levels — the
opposite of Madrid, on measured grounds.** `Nom_Grup_Activitat` puts **20,693 of
58,908 active rows (35%) into `Altres`**, and its `Restaurants, bars i hotels`
group is the accommodation trap in Catalan: **10,722 rows of which 720 are
`serveis d'allotjament`.** Keying on the group would have published 720 hotels,
hostales and pensiones as food service — *the error the Mexico City build made
once with SCIAN 72.*

**`Altres` means five different things depending on its parent**, so it is
dispatched on two further columns (Chicago's `EXTRA_COLUMNS`, reused): 625 rows
under `Quotidià alimentari` are food retail, 458 under `Comerç al detall
/Engròs` are retail/wholesale *with no activity detail at all*, 323 are
genuinely other, 115 are services, 24 are food service. **The 458 are excluded
rather than assigned to Retail** — "it is in a sector whose name contains
retail" is not evidence about a premises, and that sector explicitly mixes in
wholesale.

**The publisher's own hierarchy settled two bucket calls that were about to go
the other way.** `Plats preparats (no degustació)` sits under `Quotidià
alimentari` beside the butcher and the greengrocer, so it is food *retail*; and
`Fotografia` sits under `Comerç al detall`, making it the camera shop rather
than the portrait studio. **Both readings came off the published hierarchy
instead of off a reading of the Catalan.** When a taxonomy has levels, the
levels are evidence.

**The fresher resource was rejected, and the reason is the shape of its
error.** The 2024 resource holds 44,000 rows against 2022's 66,088, and its
shortfall is wildly uneven — Sant Andreu −83%, Nou Barris −76%, Horta-Guinardó
−69%, against Ciutat Vella's −5%. A map built on it would show the periphery as
commercially dead, *which is roughly what a reader expects and therefore would
not look broken.* The page states the survey year.

---

## The licence work, which was the most expensive in the project so far

Four obligations across two cities, and **two new categories**.

**Madrid** — CKAN declares `cc-by`, but CC BY is not the whole instrument. The
portal's *Condiciones generales* bind by use (*"obligan a cualquier persona y/o
empresa que reutilice datos por el mero hecho de hacer uso"*) and require citing
the source verbatim, **stating the last-update date**, non-endorsement, and
expressly **prohibit re-identification** of anonymised data.

**CRTM** — a Ley 37/2007 *licencia-tipo* requiring **"Powered by CRTM"** with a
link, plus citation *"especificando si son datos en bruto o explotados"* — a
disclosure-of-transformation duty in the same family as Montréal's and INEGI's.
⚠️ **And one clause raised rather than resolved:** CRTM requires displayed
information be *"siempre actualizada"*, while this site is a deliberately
pre-rendered snapshot. Raised for the owner rather than read generously.

**A cited licence URL that 404s is not an absent document.** CRTM's metadata
points at `datos.madrid.es/egob/catalogo/aviso-legal`, which 404s; the live
pages are `/pages/aviso-legal` and `/pages/condiciones-de-uso`. Found by listing
the portal's own links rather than by guessing a second path.

### The first affirmative obligation owed to a publisher

Barcelona's terms require reusers to **inform the City Council of every derived
project**. Not a line of text on a page — **an act**. The clause's own tail
gives its purpose (*"so that they are open to the public…"*), which makes it a
reuse-showcase notification rather than a permission gate, so publishing did not
wait on it.

**As of this writing it is still undelivered**, and the reason is itself a
finding: the portal's contact form stalls after its hCaptcha, and the enquiry
channel the terms themselves name times out from two independent networks while
a host in the **same /24** answers in 2.4 s. The fallback is closed too — the
electronic registry requires a Spanish digital certificate. There is **no email
to fall back on**: the dataset's CKAN metadata carries no contact address, and
`datos.gob.es` names only a web form. Logged with dates in
[`notifications/barcelona-city-council.md`](notifications/barcelona-city-council.md).

### Terms behind a CAPTCHA, and what was decided

`opendata-ajuntament.barcelona.cat` serves **hCaptcha**, and this project does
not defeat CAPTCHAs — so Barcelona was **published on a disclosed position**,
with the terms read from the Internet Archive (newest capture 2025-03-28) while
the *declared licence* was verified live through `package_show`, which needs no
CAPTCHA. The exposure was therefore never "we do not know if we may use this"
but "we may be complying with a superseded revision."

**The owner later passed the CAPTCHA and read the live page, and it paid twice
over.** The notification clause was unchanged word for word; the terms **named
the notification channel**, which no earlier reading had found; and they carry a
clause nobody had seen:

> *"any data involving third-party participation may be reused under a Creative
> Commons Attribution-**NoDerivs** (CC BY-ND 4.0) licence"*

**ND would forbid this project outright** — every map is a derivative. It does
not bind, because the terms say each dataset states its own terms and the Cens
de locals declares `CC-BY-4.0` in its own metadata. But it is now on the record
as *checked*, and afterwards an unnoticed clause looks exactly like a checked
one.

**Article 8 of Act 37/2007** (*"the content of the information may not be
altered"*) is recorded as a **disclosed position**, Philadelphia's shape:
published on the contextual reading, stated openly, down if the Council reads it
the other way.

---

## The deploy, which is where the interesting failure was

Madrid shipped a map with **"Línea 2" drawn underneath the Ramal label and
invisible at every width** — three overlapping label pairs, caught by a rendered
screenshot in `deploy-verify` one commit before a real deploy.

**The cause was a discarded number.** `_layout_labels` falls back to "the
preferred spot, even if it collides" and counts each label it cannot place;
`_choose_view` then kept the cheapest view and **threw the count away**. A city
whose labels could not all be placed was indistinguishable from one whose labels
fit. It now raises.

**The label that could not be placed was Línea 6, the circular line** — and that
is why the first fix failed. Forcing a label to `"start"` or `"end"` is
meaningless for a closed loop: both ends are the same point. The fix is a
clearance tier in shared code, and Madrid needs no per-city override at all.

**One attempted fix changed a city nobody touched, and `drift_check` caught
it.** Appending clearance candidates looked provably inert — the solver takes
the first clean candidate — and that holds *within* a view and fails *across*
views, because the search stops at the first view that places everything. San
Francisco moved its map centre ~1 km. The search now runs twice.

**And the live site showed something no local check could.** At an 820 px
viewport, Madrid *and* Chicago both rendered at a far-out zoom with labels
clumped; on reload both measured their correct baked views. It is the
intermittent narrow-width re-fit race already documented in `map_common.py` —
**Chicago is what proves it is not the label change**, since it shares none of
the new code's inputs. Open in `PLAN.md`, with the mechanism labelled as a
hypothesis to instrument rather than a fact to fix from.

---

## What a third Spanish city would cost

**Nearly full price**, and that is the headline. Plan Spain as a two-city
country; it already is one. If a third is ever attempted:

1. Start at `datos.gob.es`, **by publisher id**, not at the city's portal and
   not by title.
2. Expect a **bespoke taxonomy** and decide its keying level by measuring the
   `Altres`/catch-all share at each level — the deciding measurement in
   Barcelona, and it pointed the opposite way from Madrid.
3. Expect **accommodation inside food service** and look for it by name.
4. Expect the rail leg to come from somewhere new again: GTFS, an ArcGIS
   feature service, and OSM have each been the answer once.
5. Budget real time for licences. Spain's two cities produced **two required
   notices, two disclosure duties, one raised clause, one CAPTCHA wall and the
   project's first affirmative obligation to a publisher** — more licence work
   than the nine US cities combined.
