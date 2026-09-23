# Global city master list — CURRENT STATE

**This is the operative list: which cities this project could build next, and
what is stopping each one.** It is rewritten as things change, like
`docs/project_context.md` and unlike `DECISIONS.md`.

**The evidence lives in [`docs/global_country_shortlist.md`](global_country_shortlist.md)** —
87 countries screened, every probe logged, every negative with the measurement
behind it. That file is the trail; this file is the answer. When they disagree,
the trail wins and this file is stale.

**Drift-corrected 2026-09-23**, after Marseille was built: counts, the band
table, Marseille's row, Hong Kong's geocode rate, Göteborg's row count, Cairo
(moved out of the discards onto the open screening gap, by this file's own
rule) and the by-country view, which had stopped being current a day earlier.

Last reordered **2026-09-22**, after the browser sweep — Tier 5 closed
(7 negatives, no survivors), Tier 6 reached for the first time, and three
food-authority probes run. **Stockholm** and **Bucharest** were promoted out
of the band that used to read *"never actually reached"*; five cities moved to
discarded on measurement.

**The method that produced all of it:** open the portal in a real browser
*before* concluding anything about it, then enumerate providers rather than
search keywords. Both are written up in `.claude/skills/add-country/`
(§3 and §2) and `add-city` Step 0.

---

> ## ✅ Settled state — 2026-09-22
>
> **Every candidate on this list has a measured business leg, a named next
> step, and no unexamined route.** Nothing here is carried on a guess, a
> search result, or a host that was never asked properly.
>
> | | |
> |---|---|
> | **Built** | **22** across 7 countries |
> | **Candidates** | **29**, all at least partially viable — A 8 · B 16 · C 5 |
> | **Open screening gap** | **3**, unscreened — neither candidates nor discards |
> | **Discarded** | **32**, each naming its evidence |
>
> *Counts corrected 2026-09-23. This box had read 20 / 33 / 30 since
> 2026-09-22 while the sections below moved on — **the hand-kept summary is
> the first thing to drift, which is why the band sections are the ones to
> trust.***
>
> **What this day changed.** Four bands closed because their condition stopped
> being true of their members. **Seven cities were reached by going to a
> different HOST rather than a different network** — Sofia, Sevilla, Tel Aviv,
> Tallinn, Prague, Dublin and Hong Kong — and *unreachable* turned out to mean
> *not yet asked properly* in every single case.
>
> **Three recorded negatives turned out to be statements about a SEARCH rather
> than about the data**: Stockholm's register is called `Tillsynsverksamheter`,
> a word no query contained; Zurich's catalogue was matched over 938 of 1,128
> names; Hong Kong's bulk export was on `data.gov.hk` the whole time and the
> dataset list had never been requested. **Each cost one HTTP call to
> disprove.** India was then swept in full — 288,011 titles — specifically so
> it would not become the fourth.
>
> **This claim is dated because it will stop being true.** The next probe, the
> next build, or the next licence read changes it, and the counts in the table
> below are the ones to trust over any prose that repeats them.

## Built — 24

| Country | Cities |
|---|---|
| **United States** (9) | San Diego · San Francisco · Los Angeles · Chicago · New York · Philadelphia · Miami · Boston · Washington D.C. |
| **Canada** (5, complete) | Vancouver *(with Surrey)* · Montréal · Calgary · Edmonton · Toronto |
| **Mexico** (2) ✅ | **Mexico City** · **Guadalajara (Regional)** — built 2026-09-22, live in the app |
| **Europe** (8) ✅ | 🇪🇸 **Madrid** · **Barcelona** · 🇮🇪 **Dublin (Regional)** · 🇮🇹 **Milan** · 🇫🇷 **Paris** · **Marseille** · **Toulouse** · **Lille (Regional)** — the first four built and deployed 2026-09-22, Paris deployed 2026-09-23, **Marseille built and deployed the same day** (`pages/22_Marseille_Heatmap.py`; **18,177 storefronts, 66 stations**), **Toulouse** likewise (`pages/23_Toulouse_Heatmap.py`; **8,635 storefronts, 48 stations**), and **Lille (Regional) built the same day, not yet deployed** (`pages/24_Lille_Heatmap.py`; **11,833 storefronts, 91 stations**) — **the first French city scoped regionally**, to the eleven communes its network serves, because the commune alone would have drawn the tram as a three-stop stub. **France is the first country here where the second city was materially cheaper than the first**: Marseille inherited the national register, the NAF taxonomy, the parquet cache and the Lambert-93 grid, and its own work was the scope measurement and the rail leg. That is Mexico's retrospective repeating, and the opposite of Spain's. **Toulouse made the third city cheaper again**: it downloaded nothing at all, because the 3 GB national parquet pair was already cached for the country, and its own work was one scope decision, one owner call, and a gate-3 run that matched the operator exactly on all four lines. It is also the first city anywhere here to draw a **non-rail mode** — the Téléo cable car — which was the owner's call after the brief's stated precedent for it turned out not to exist. **One macro-map region, not one per country**: Spain, Ireland and Italy were three regions holding four cities until they were collapsed the same day, which is what let France join without adding a sixth region. Spain is complete at two cities, Ireland at one, and Italy is a Milan-only country — so the countries are still the research unit, and only the MAP groups them. ⚠️ **France's own viability figure was corrected on the day Paris was built**: the recorded "50,156 storefronts, 92.5% of OSM" is not reproducible and the real ratio is about 1.78× — see `docs/build_briefs/paris.md`. France remains a build; `docs/global_country_shortlist.md`'s France row still carries the old number |

✅ **Mexico is the first country built outside North America's anglophone
pair**, and the first where the rail leg came from **OpenStreetMap** rather
than an agency feed — the per-city exception approved for CDMX, which
validated at 195/195 stops exact.

✅ **Spain is the first country in EUROPE**, and the first where the two cities
did not generalise to each other in any leg. Different rail sources (Madrid
takes CRTM's own ArcGIS layers, Barcelona OpenStreetMap), different projected
CRS (25830 against 25831), different taxonomy LEVELS of similar four-level
schemes — Madrid keys on its division, Barcelona on its finest level, and each
for a measured reason. Both carry the same accommodation trap and it bites at a
different depth in each. Barcelona is also the first source in the project to
impose an obligation that is **an act rather than a notice**: its terms require
the City Council to be informed of every derived project.

## Candidates — 29

Re-tiered 2026-09-22 after the browser sweep closed Tier 5 and reached Tier 6.
**Eight cities moved to discarded on measurement** and **two were upgraded**.

**Four of those were sitting in Band D as "unreachable", and all four were
reached by going to a different HOST rather than a different network** —
Sofia via `data.europa.eu`, Sevilla and Tel Aviv via the ArcGIS service host
behind a walled portal, Tallinn via a bulk export its catalogue entry named.
Three then measured negative and **one, Tel Aviv, is now the strongest
unbuilt candidate outside Band A.** *Unreachable* turned out to mean *not yet
asked properly* in every single case.

**Re-banded 2026-09-22 so that every caption names the kind of work that
unblocks its cities**, after an audit found five rows whose text named a
blocker their band did not. Band D dissolved: its two live sub-tiers were
about different things and were siblings only because both arrived through
the same screen.

**The one-bucket band (now D) was added the same day** for a state the scheme
could not express: a city whose screening is **complete and successful** but
which yields only one bucket. Those two were sitting in "a decision to make"
beside a city waiting on a licence read, which conflated *we have not looked
yet* with *we looked at everything and this is what is there*.

| Band | What these cities ARE | Cities |
|---|---|---|
| 🟢 **A** | **Ready to build.** Register measured, licence read, coordinates answered, rail answered, brief written | **8** *(+ 8 built)* |
| 🟠 **B** | **Geocoding at national scale.** The address work is a project, justified only by reuse across many cities | **16** |
| 🟣 **C** | **One bucket only.** Screening complete and successful; the map would be narrower than the others | **5** |
| | **Candidates** | **29** |
| *Open gap* | Unscreened — a row resting on an absence, so not a discard | *3* |
| *Discarded* | Measured negative, evidence named | *32* |

⚠️ **This table read A 9 / B 10 / C 12 / D 2 until 2026-09-23** — the
pre-renumber counts, left standing under two renumbers that each updated the
section headings below and not this summary. **The headings were right; the
table summarising them was not.**

**Renumbered 2026-09-22 to close the gaps left by four band closures.** The
live set is now contiguous, and **the closed bands have lost their letters
rather than keeping them** — a closed band's letter was never the interesting
part of it, the condition that stopped being true is.

| Old letter | Now | Why it changed |
|---|---|---|
| A | **A** | unchanged |
| **C** | **B** → *(2026-09-23: absorbed into A)* | Hong Kong, Prague, Taiwan ×4, Bucharest, Singapore, Oslo, Copenhagen |
| **E** | **C** → **B** *(2026-09-23)* | Brazil ×2, Japan ×10 |
| **F** | **D** → **C** *(2026-09-23)* | Stockholm, Zurich |
| B | *(closed)* | **awaiting permission** — Tel Aviv, discarded on terms |
| D | *(closed)* | **coordinates and unfinished screening** — Bucharest finished its screening |
| G | *(closed)* | **access blocked** — Hong Kong left upward, Hyderabad and Kochi measured out |

**Rule this renumber established: a LETTER is for a heading, a CONDITION is
for a sentence.** Prose that says *"moved to the coordinates band"* survives
any renumber; prose that says *"moved to Band C"* does not, and four such
sentences went stale the moment the letters shifted. They have been rewritten
to name conditions.

**Renumbered again 2026-09-23, and this time a band closed by SUCCEEDING.**
The coordinates band existed to hold cities whose coordinate route was
unmeasured. All four of its last members ended up with the route measured AND
a brief written, so the condition stopped being true of every one of them and
the band was absorbed into **A** rather than re-captioned. `C` and `D` moved
up to `B` and `C` behind it.

⚠️ **Several sentences written on 2026-09-23 named LETTERS and went
stale within hours of being written** — including two in the Bucharest and
Singapore sections added that same day. They have been rewritten to name
conditions. **The rule above is easy to agree with and easy to break in the
next paragraph.**

⚠️ **`DECISIONS.md` is append-only and names bands by their letter at the time
of writing.** Those entries remain true of the moment they describe; this
table is how a reader resolves them. **Nothing in the log was edited.**

**Re-banded 2026-09-22 so each caption describes what its cities ARE**, not
how they were found. The previous Band C had grown to 21 cities whose only
shared property was "needs coordinates" — while the **cost** of that step
ranges from Prague's RÚIAN lookup to Japan's chōme/ban/gō. That is the
largest single ranking fact in this list, and one band was hiding it.

**Band D held Bucharest alone** while its business leg was unfinished. On
2026-09-22 it finished — **rail counted (12 relations, M1–M5), licence read
(SILENT), Romania's catalogue enumerated (4,693 datasets, no second
bucket)** — so the city moved to C and the band closed. **A band whose
condition stops being true of its last member should close, not be
re-captioned around the occupant.**

**A caption names a blocker, never a date or a status.** `D-a` was briefly
captioned *"all four PROBED 2026-09-22"*, which reads as progress and is
unauditable — Rio's misfiling was caught only because the sub-tier beside it
still declared what it was *for*.

✅ **Guadalajara and Mexico City left Band A by being built**, not by being
ruled out. Their rows are kept below, marked, because a built city's Band A
entry is the only place the screening promise and the delivered build sit
side by side.

**Net: the screen got smaller and more honest.** Nothing was lost that was
ever measured as viable — the five drops were all cities whose business leg
had never been tested, and testing it is what removed them.

**Two cities were promoted the same day**, both by the same method and both
out of the band that used to read "never actually reached": **Stockholm** to B
and **Bucharest** to C. The tier that looked deadest produced the two best new
results in the sweep.

---

## 🟢 Band A — ready to build (6 ready + 10 ✅ BUILT)

**The six:** Seoul · Rennes · Prague · Copenhagen · Hong
Kong · Oslo — **every one has a brief** in `docs/build_briefs/`.

**Every question these cities carry is answerable inside the build**, not
before it. Nothing here needs a probe, a document or a decision first.

**▲ France's other five cities were added on 2026-09-22.** The Tier view had
said *"France — 6 cities"* since the country was resolved, while the band
view showed only Paris — **so this list understated France by five cities for
as long as both views existed.** They share one national register, one
licence and one filter with Paris, and their geolocation was measured per
commune rather than inherited.

> ⚠️ **Dublin's row was wrong in four places until 2026-09-22**, corrected
> from `docs/build_briefs/dublin.md` after Step 0 measured it live. All four
> errors share one root: **the screening probe reported the slice it happened
> to query as if it were the whole.** It queried **one** authority and **six**
> categories, then quoted the total as Dublin's; it quoted the length of the
> *national* category list as the number present in Dublin; it computed 100%
> coordinates over only the rows it had pulled; and it counted colours across
> all 42 OSM relations including the Commuter and InterCity services a build
> would drop. **Every number was true of the query and false of the city.**

Ordered by how little stands in the way. **Built cities keep their row**,
struck through and marked ✅, so the band still shows what screening promised
and whether it held.

| # | City | Business leg | What remains |
|---|---|---|---|
| ✅ | ~~**Guadalajara**~~ 🇲🇽 | DENUE, SCIAN = NAICS, INEGI licence cleared | **BUILT 2026-09-22** — `pages/16_Guadalajara_Heatmap.py`, region *Mexico*. Screening said "nothing outstanding" and that held |
| ✅ | ~~**Madrid**~~ 🇪🇸 | **53,355 clean storefront rows** — retail 36,224 · food 18,194 · personal 9,974 (from 225,660 join rows → 159,787 open → filtered). Three-level taxonomy on `division`, EPSG:25830, CC BY 4.0 | **BUILT 2026-09-22** — `pages/17_Madrid_Heatmap.py`, region *Spain*. Rail from **CRTM's feature layers**: 13 lines, 293 station-line records, 49 stations excluded, 0 filter disagreements. Screening said the rail leg was the open question and CRTM answered it |
| ✅ | ~~**Dublin**~~ 🇮🇪 ▲▲ **REGIONAL** | **38,265 rateable rows across FOUR local authorities → 13,945 storefront** (Dublin City alone: 19,810 → **8,016**). **13 use categories region-wide, 12 in Dublin City.** **99.87% carry `Xitm`/`Yitm`** — Irish TM, already in metres; 51 of 38,265 missing, **46 of them pubs**. Per-row `Category` **and** `Uses`, plus `ValuationReport[].FloorUse`. `Eircode`. **CC BY 4.0, no key** | **No geocoding leg.** Build is the **Vancouver + Surrey shape** — four authorities, not one city. Rail: the three drawn lines (**Luas Red, Luas Green, DART**) all already carry an OSM colour; Commuter and InterCity are **dropped**. ⚠️ **36% of its storefronts are near no rail of any kind** — a scope fact to state on the page, not a defect. Brief: `docs/build_briefs/dublin.md`, **6/6**  — **✅ BUILT 2026-09-22** — the regional shape (four local authorities) held |
| 2 | **Seoul** 🇰🇷 | 197,276 active premises over 8 datasets, EPSG:5174, status field, KOGL Type 1 | Build work — partial geocoding for 일반음식점 (90.7%), Korean-aware `check_personal_exposure.py` ✅ **BRIEF WRITTEN 2026-09-23, 2/2 — `docs/build_briefs/seoul.md`, and it is deliberately PARTIAL.** ✅ **Rail is the best in the project: 149 subway relations, 149 named, 149 coloured, 10 refs, ZERO without a `ref`.** 🚨 **Two rail measurements FAILED rather than answered** — `light_rail` errored, and the station query returned an implausible **0** for a city with hundreds, so both are recorded as UNKNOWN. 🚨 **Seven Step-0 items have never been done**, chiefly: the **8 datasets have never been enumerated individually** (197,276 is a country-screen total), the **taxonomy has never been measured**, and the **non-storefront share is unknown**. ⚠️ The portal's search is **INERT** — enumerate, never search |
| ✅ | ~~**Milan**~~ 🇮🇹 | **Three layers, one per bucket — the bucket comes from WHICH LAYER a row is in, not from a code.** `ds49` **28,131** retail · `ds59` **3,799** food service · `ds62` **5,732** personal services. All three **CC-BY**, all updated **2026-08-31**, all with `LONG_X_4326`/`LAT_Y_4326` | **Schemas captured 2026-09-22 — and the fill rates correct this row's old claim.** Coordinates are excellent (99.1% / 92.2% / 98.8%) and location is complete (`Ubicazione` 100%). **But the columns that were cited as making this the richest source in the screen are mostly EMPTY**: `insegna` **17.6%** on retail and **9.1%** on food, `codice_ateco` **7.1%**, and `ds62` has **no name field at all**. `settore_merceologico` is 99.5% but binary — *alimentare / non alimentare*; `tipologia` is 100% and single-valued. **Owner decision: a map where ~82% of retail pins carry no trade name.** Not a blocker — bucketing works by layer, and fewer published names is a privacy asset — but it is a choice, not a detail — **✅ BUILT 2026-09-22** |
| ✅ | ~~**Mexico City**~~ 🇲🇽 | Same DENUE. **Rail from OSM** — 195/195 stops exact, 6,468 geometry points | **BUILT 2026-09-22** — `pages/15_Mexico_City_Heatmap.py`. The ODbL share-alike decision was taken during the build; see `DECISIONS.md` |
| ✅ | ~~**Paris**~~ 🇫🇷 | SIRENE établissement-level, **Licence Ouverte 2.0**, **99.96% already geolocated**. Built storefronts **87,164** from **149,166** active bucket rows | **BUILT 2026-09-23 — the 21st city, and the first in France.** 🚨 **Its screening figures did NOT survive the build.** This row read *"50,156 rows vs OSM's 54,198, and on one class 10,595 vs 10,642"*, attributed to an **employee filter**. **There is no employee filter**: `trancheEffectifs` is `NN` on 77.3% of rows and only 1,425 record `00`, so SIRENE codes a sole trader as `NN` — that band holds every owner-run shop, and the largest cut the column can make falls **16,000 short** of 50,156. Re-established: **87,164 SIRENE vs 48,973 OSM = 1.78×**; on restaurants the **OSM side reproduced** (9,058 vs a recorded 10,642) and the **SIRENE side did not** (16,280 vs a recorded 10,595). **When one side of a comparison reproduces and the other does not, the non-reproducing side is where the tuning happened.** France remains a build; the 92.5% claim does not |
| ✅ | ~~**Marseille**~~ 🇫🇷 | The same SIRENE, estimated at **25,430** bucket rows | **BUILT 2026-09-23 — the 22nd city, and France's second.** `pages/22_Marseille_Heatmap.py`. **18,177 storefronts, 66 stations.** Scope was **measured rather than inherited from Paris**: all five RTM lines sit 100% inside commune 13055, so the commune costs it nothing; Aubagne's tram excludes itself by having zero stations inside; ferries dropped by owner's decision and recorded as revisitable. See `DECISIONS.md`, *"Marseille built, and a region now labels only its own cities"* |
| ✅ | ~~**Toulouse**~~ 🇫🇷 | The same SIRENE, estimated at **12,853** bucket rows | **BUILT 2026-09-23 — the 23rd city, France's third.** `pages/23_Toulouse_Heatmap.py`. **8,635 storefronts, 48 stations.** Commune-only, and it costs Tram T1 twelve of its twenty-five stations; the Téléo cable car is drawn, the project's first non-rail mode. Gate 3 exact on all four lines. See `DECISIONS.md` |
| ✅ | ~~**Lille (Regional)**~~ 🇫🇷 ▲▲ **REGIONAL** | The same SIRENE, estimated at **8,076** bucket rows for the commune alone | **BUILT 2026-09-23 — the 24th city, France's fourth, and its first regional one.** `pages/24_Lille_Heatmap.py`. **11,833 storefronts, 91 stations**, eleven communes. Both owner calls in the brief dissolved: métro geometry from OSM, everything else first-party from MEL, and ilévia's GTFS never read. See `DECISIONS.md` |
| **3** | **Rennes** 🇫🇷 *(Toulouse and Lille built — rows above)* | **The same SIRENE, the same Licence Ouverte 2.0, the same filter** — one national register, so nothing about their business leg is separately open. **Country profiled 2026-09-22**: `pipeline/countries/france.py`, `docs/france_step0_endpoints.md`. Coordinates are a **JOIN** on `siret` against INSEE's 37,901,783-row geolocation file, so there is no geocoding leg for any of them. **Est. bucket rows, RE-MEASURED 2026-09-23** on one 12.6% pass over all six cities: Marseille **25,430**, Toulouse **12,853**, Lille **8,076**, Rennes **4,833** — every one a **floor**, since active rows get denser through a file ordered by `siret`. Named share **43.4% / 52.8% / 47.5% / 53.5%**, all above Paris's 39.6% | **Each is one variable (`codeCommuneEtablissement`) — and Marseille, the first to try it, took more than that**: its scope had to be measured, because its feed covers the whole Métropole. Expect the same per city. Briefs written for all three: Toulouse **budgets ~10,800** after 16.0% masking; Lille carries **two owner calls** (rail geometry — métro from OSM, tram from MEL's WFS — and the ilévia licence carve-out); Rennes is **the smallest and best-named**. Licences read: Marseille and Lille `lov2`, Toulouse and Rennes **`odc-odbl` share-alike**. ⚠️ France's OSM rail composition is validated on **Paris only** — the first non-Paris build must re-validate. ⚠️ **Scope undecided**: the commune is far smaller than the transit network, so these may need Dublin's regional shape |
| ✅ | ~~**Barcelona**~~ 🇪🇸 | **58,908 active premises** (2022 census — the 2024 one is geographically incomplete), 0.00% bad coordinates, CC-BY-4.0. Build brief, 9/9 | **BUILT 2026-09-22** — `pages/18_Barcelona_Heatmap.py`. All four owner decisions were settled before the build: census year **2022**, drawn scope **16 lines** (14 metro refs + funiculars FM and FV, decided on the operators' own `network` tag), mall and market interiors **kept**, and the brief's OSM breakdown corrected to tram 20 / funicular 6. ⚠️ **The duty to notify the Council is still OUTSTANDING** — see `docs/gated_access.md` item 2 |

⇄ **Paris left Band A and came back the same day, measured both times.**
The demotion was right on the evidence then available (86.6% of the bucket are
sièges, i.e. largely home addresses); the return is right on evidence that did
not exist yet — an **OSM composition comparison**. ⚠️ **That comparison was later re-established and its headline figure withdrawn** (see Paris's row): the reversal was right, the number supporting it was not. The
reversal is recorded rather than tidied away, because the thing that changed
was the measurement, not the opinion. See "Paris / SIRENE" below. The architecture question it was holding ("national register vs
per-city") turned out to be **closed already**: Mexico shipped two cities from
the national DENUE on the same day, so `pipeline/countries/` is the answer and
national registers are fine. What fails is **SIRENE's composition**, which is
a different objection and a measured one.

▶ **Madrid's pipeline is DONE and on master; only its app wiring is held.**
As of 2026-09-22 `pipeline/madrid/`, `outputs/madrid/`, its taxonomy module and
its provenance rows are all merged, and `scripts/check_provenance.py` reports
it ready. What is not merged is `app/cities.py` and its page, deliberately:
they sit on `spain-app-wiring`, because Streamlit Cloud pulls master
automatically and landing an imported module there would publish the city and
serve it broken until a reboot. **It waits for Barcelona so the two ship
together** — see that branch's own commit message, which is the authority on
the hold.

So the next *unstarted* city is the question.
**Barcelona** is the obvious answer — same country, brief done, licence read,
and only owner decisions left. After that the screen has no city whose
"what remains" column is empty.

### ▲ Four cities joined this band 2026-09-23, when the coordinates band closed

**Their coordinate route was the thing being measured, and all four now have it MEASURED and a brief written** — Prague 5/5, Oslo 5/5, Hong Kong 8/8, and Copenhagen's data in hand with its licence read. **A band whose condition stops being true of every member should close, not be re-captioned around them** — the same reasoning that closed the old Band D when Bucharest finished screening.

**Every route in this band was probed on 2026-09-22 and answered.** The band
used to say the method was "identified and cheap", which is a description of a
plan rather than of a measurement. It is now a hit rate per city, taken against
each register's **own** addresses rather than hand-typed landmarks.

**The band splits in two, and the split is the useful thing:**

- **A JOIN** — the whole address table downloads, and coordinates come from a
  dict lookup. No per-row requests, no rate limit, no geocoder to be wrong.
  **Prague and Copenhagen.**
- **A GEOCODE** — one request per distinct address, against a service that
  answers. **Oslo and Hong Kong**, both keyless. *(Singapore's geocode was
  measured here too, at 98.8%, before the city moved to the one-bucket band.)*

**Taiwan left this band** for the national-geocoding band: its route was the one claim here that did
**not** survive probing. **Bucharest's primary is down** but its fallback is
measured.

| Cities | Country | The coordinate step — MEASURED | Rate |
|---|---|---|---|
| **Prague** ▲▲ *(1)* | 🇨🇿 | **A JOIN, confirmed.** RÚIAN's Praha export is **3.4 MB zipped, keyless** (`vdp.cuzk.gov.cz`; the old `cuzk.cz` redirects rather than dying) and holds **134,627 addresses, every one a unique `Kód ADM`, 99.99% carrying coordinates**. Measured on **6,000 active Praha rows** in CZ-NACE 47/56/96 streamed from RES | **99.8%** — 99.9% carry a code, 100.0% of those resolve |
| **Copenhagen** *(1)* | 🇩🇰 | **A JOIN, confirmed — and the account gate was on the wrong leg.** DAWA (`api.dataforsyningen.dk`) is **keyless**; the `distribution.virk.dk` 401 gates the BUSINESS register only. The whole city downloads as CSV: **85,351 access addresses, 100% with WGS84**, joinable on `vejnavn` + `husnr`. ⚠️ **Frederiksberg (0147) is a separate kommune entirely surrounded by Copenhagen** — scope to 0101 alone and the map has a hole in its middle; its 9,584 addresses come from the same call | **100%** of addresses carry coordinates ✅ **BRIEF WRITTEN 2026-09-23, 4/4 — `docs/build_briefs/copenhagen.md`.** **14,887 storefront rows** (retail 6,689 / food 5,163 / personal 3,035) at **100.0% named**, measured from the real 2.00 GB download rather than from metadata. **96.9% carry a DAR address UUID**, so coordinates are a JOIN. ⚠️ **Four files joined on `CVREnhedsId`** — `Produktionsenhed` alone is almost empty. 🚨 **`v/` marks a sole trader: 7.2%, a FLOOR**; `coNavn` is a second exposure at 26.0%. ⚠️ **Rail: M1–M4 only** — this list's "tram 4" was WRONG, Copenhagen has no tram |
| **Hong Kong** ▲▲▲ *(1)* | 🇭🇰 | **A GEOCODE, confirmed keyless.** The government **Address Lookup Service** (`als.gov.hk/lookup`) answers without a key and returns **lat/long AND HK1980 Grid easting/northing AND a confidence `Score`** (76.15, 88.75, 97.69 on three test premises). ✅ **INDEMNITY ACCEPTED by the owner 2026-09-22** — the project's only uncapped liability, priced deliberately. Three conditions bind the build: display source + Government IP acknowledgement + DATA.GOV.HK attribution exactly; run `check_personal_exposure.py` and exclude catch-alls; the dated record in `data_sources.md`. ⚠️ Re-reading the live clause corrected this project's OWN earlier quote twice: it arises **directly or indirectly**, and there is **no notice-and-defend right** | ✅ **100.0% — RE-MEASURED 2026-09-23 on 200 random register rows, as a TWO-STAGE lookup.** This cell read *"per-row rate not yet measured"* for a day after the brief measured it. **Brief 8/8 — `docs/build_briefs/hong-kong.md`** |
| **Oslo** *(1)* | 🇳🇴 | **A GEOCODE, keyless — with two traps.** Kartverket (`ws.geonorge.no/adresser`) answers and returns `representasjonspunkt`. ⚠️ **`fuzzy=true` MUST NOT BE USED**: it "rescued" `Karenslyst allé 8B` as **`allé 1B`** — a different building — and turned `7-Eleven` into `Ellen Gleditsch' vei 7`. It returns plausible coordinates for the wrong place. ⚠️ The API caps at **10,000 rows** (offset 9,900 works, 15,000 returns nothing), so it cannot enumerate the city | **97.8%** via two stages: exact `adressetekst`, then plain `sok`. Never fuzzy |

**⚠️ Two facts here that are NOT about coordinates and change build scope:**

- **Oslo's register is not filtered by the address you read.** Bronnoysund's
  `?kommunenummer=0301` does **not** guarantee `beliggenhetsadresse` is in
  Oslo — a sample turned up Bergen, Copenhagen, Paris and Malmö, and
  `adresse` is a **list** whose first line is sometimes `c/o Osnordic AS`.
  **This is the registered-office trap in a third costume**, after ONRC, ACRA
  and SIRENE's *sièges*. The generalisation worth keeping: **a filter
  parameter and the field you read are two different addresses until proven
  otherwise.** How much of Oslo's 152,128 is physically in Oslo is **still
  unmeasured** — brreg's API stops paging past ~10,000, so both samples came
  from the alphabetical head and disagreed (24.5% vs 4.3%). **Settle it with
  the bulk download at build time, not with the API.**
- **Three of these services report their own confidence; Oslo's does not.**
  DAWA returns a `kategori` (A exact / B normalised / C ambiguous — it
  returned **B** for `Raadhuspladsen 1 1550 Kobenhavn` with the diacritics
  stripped, and **C with 30 results** for an ambiguous one) plus a
  per-address `nøjagtighed`; ALS returns a `Score`. **A geocoder that says
  when it is guessing is worth more than one with a higher raw hit rate** —
  which is exactly what Oslo's `fuzzy` lacked.

## 🟠 Band B — geocoding at national scale (16 cities)

**The investment tier.** These share one property that separates them from
the buildable band: the address work is a project rather than a step, and it is worth
doing only because the machinery, once written, is reused across many
cities. Japan is ten cities from one schema; Brazil is two from one register.

| Cities | Country | Business leg | The coordinate step |
|---|---|---|---|
| **São Paulo** *(1)* | 🇧🇷 | CNPJ — trade name, address, CNAE | **Hard, past Toronto's scale** |
| **Rio de Janeiro** ▲ *(1)* | 🇧🇷 | **The same CNPJ** — one national register, so nothing about its business leg is open. Rail confirmed: **20 OSM relations, all named and coloured** | Same as São Paulo's, and shares its cost: write the Brazilian geocoder once, get both cities |
| **Taipei**, Kaohsiung, Taoyuan, Taichung *(4)* | 🇹🇼 | 商業登記 — premises, active/closed status, per-category assembly | ⚠️ **MOVED HERE FROM BAND B 2026-09-22, on a probe rather than on a resemblance.** The row used to read *"moderate — NLSC's geocoder is keyless"*, and **that claim did not survive**: NLSC's API is alive and keyless, but the keyless endpoint is **reverse** geocoding (point → 村里) and administrative lists, not forward geocoding, and **no bulk 門牌 address-point file was reached**. `data.gov.tw`'s dataset API **requires an API key** (`ER0001:API Key錯誤`); its web pages are reachable, and `addr.tgos.tw` answers but has historically required registration. **Blocked, not negative** — and the Prague-shaped bulk join is still the thing to look for |
| **Tokyo**, Osaka, Nagoya, Yokohama, Sapporo, Fukuoka, Kyoto, Kobe, Sendai, Hiroshima *(10)* | 🇯🇵 | Premises-level food permits, CC BY, one national schema. **Two buckets — no general retail** | **Hardest met** — chōme/ban/gō, full-width numerals, `町字ID` 0% populated |


*(A paragraph here said Bucharest's rail was uncounted and its licence unread.
**Both were done on 2026-09-22/23** — 13 relations counted, licence SILENT —
and Bucharest now sits in the one-bucket band, where its full record is. The
paragraph was removed from this band on 2026-09-23 because Bucharest is not
in it.)*

**▶ Brazil is the next geocoding work, by the owner's choice (2026-09-23)** —
São Paulo and Rio from one CNPJ register and one geocoder.

**Japan is ten cities from one schema** — the best marginal-city cost in the
screen — against the worst geocoding problem and a two-bucket ceiling.
**Still the biggest open decision in this list**, and a judgment call rather
than a probe.

## ⚠️ OPEN SCREENING GAP — rows that rest on an absence (3 cities unscreened)

**Not candidates yet and not discards — unscreened.** `global_country_shortlist.md`
records *"Italy stays a Milan-only country"*, but that rests on **Naples** and
**Messina** measuring out. **Rome and Turin appear nowhere in any list**, which
`add-country` is explicit about: a row whose reason is "not reached" is not a
discard.

| City | What the catalogue holds | What is still unknown |
|---|---|---|
| **Rome** 🇮🇹 | `dati.comune.roma.it`, CKAN, **365 datasets**. Carries **`elenco-delle-attivita-produttive-del-suap-di-roma-capitale-anno-2025`** and its 2024 edition — SUAP is the *Sportello Unico Attività Produttive*, the one-stop business register every comune runs, and **2025 is current** | **Schema unread** — the host failed its TLS handshake *after* the catalogue answered. The **LOCATION and ACTIVITY** columns have not been checked separately |
| **Turin** 🇮🇹 | `aperto.comune.torino.it`, CKAN, **2,118 datasets**, 143 with a commerce term. Its naming makes the Messina distinction itself: `aperte`/`chiuse` are the FLOW, **`presenti` is the STOCK**. Geoportale also publishes **SHP**, so geometry exists. **CC-BY** | ⚠️ **The series STOPS AT 2019** — latest `presenti` is 2019, geoportale layer last modified 2019-05-17. Six years stale against a project mapping *current* density. Schema unread; `risorse.comune.torino.it` timed out at TCP connect |
| **Cairo** 🇪🇬 ▼ *moved here from the discards 2026-09-23* | **One probe, of one national host:** CAPMAS, the statistics agency, *"serves HTML only"* — recorded in `global_country_shortlist.md` as **NO OPEN API**. No city-level host has ever been asked | **Everything.** It sat in the discard table as *"No open-data infrastructure"* while this file's own 2026-09-23 sweep recorded it **STILL UNPROBED**. **A national statistics agency not having an API is not a finding about Cairo's premises**, and `add-country` says to try the city's own host before recording a negative — which was never done. **Moved by this file's own rule**, not re-judged |

**Neither Italian city changes the Italy profile answer** — Italy is bespoke per city, so
each would be its own Step 0 regardless. See `DECISIONS.md`, 2026-09-22.

### The sweep, 2026-09-23 — what else rests on an absence

**Audited the whole discard record** for rows whose stated reason is *"not
reached"*, *"unprobed"*, *ASSERTED*, or a regional pattern. `add-country` is
explicit that such a row **is not a discard**, and records that exact error
happening twice — once to a group including **Italy, which then passed**.

| Row | What its reason actually was | Probed 2026-09-23 |
|---|---|---|
| **Göteborg** 🇸🇪 | *"Unprobed candidate"* — named twice in this file and **placed in no band at all** | ✅ **REAL, and it is a candidate.** `catalog.goteborg.se/store/search?type=solr` — EntryStore, the same platform as Stockholm's. **`Livsmedelsverksamheter`** is *"Alla aktiva livsmedelsverksamheter"* — **active food BUSINESSES, not inspections**, so no dedupe, where Stockholm's 8,146 premises had to be distilled from 289,742 inspection rows. **`Restauranger med serveringstillstånd`** declares **CC ZERO** — stronger than Stockholm's SILENT. Rail is trams, not a metro: **better data, weaker map** |
| **Lisbon** 🇵🇹 | On *"Countries ruled out"* with **no parenthetical evidence at all** | ⚠️ **Discard now EVIDENCED, and it holds.** `dados.gov.pt` returns 430 for *estabelecimentos*, but they are **aggregate hotel statistics** (*"Proporção de estabelecimentos hoteleiros que utilizam computador (%)"*) and prison establishments. The aggregate trap |
| **Warsaw** 🇵🇱 | Same — **no evidence** | ⚠️ **Discard now EVIDENCED, and it mostly holds.** Control passes (`zzqqxx` → 0, so the search filters). `CEIDG` is company-level, as recorded elsewhere. **One premises-shaped lead survives**: *Wykaz punktów sprzedaży napojów alkoholowych* — licensed alcohol sales POINTS, the Singapore-tobacco shape. One bucket at best |
| **Cairo** 🇪🇬 | Same — **no evidence** | ⛔ **STILL UNPROBED.** Recorded as an absence rather than a finding — ▼ **and on 2026-09-23 moved OUT of the discard table onto the open screening gap**, where this finding says it belongs |
| **Zagreb** 🇭🇷 | *"identical 1,291-byte SPA shell at four paths"* | ~~⛔ **Confirmed BLOCKED, not negative.** Three more paths tried 2026-09-23, all shells~~ ⚠️ **SUPERSEDED — this row contradicted the discard table, and the discard is the measured one.** `data.gov.hr`'s CKAN lives at **`/ckan/api/3/...`**, not at the paths tried here; through it Grad Zagreb's **210 datasets** were enumerated on 2026-09-22 and the only commercial one is a grants list. **Three more shells at the wrong paths are not evidence of a block** — the discard stands |

**The generalisable result: a "ruled out" list is only as good as its weakest
row, and three of this one's rows carried no reason at all.** Two of those now
do. Göteborg was never ruled out — it was simply never placed anywhere, which
is how a candidate disappears without anyone deciding to drop it.

## 🟣 Band C — one bucket only: complete, but narrower than the others (5 cities)

**Screening is COMPLETE for all five, and all five passed.** Each has a real
premises-level register with coordinates, current data and a usable licence.
What none of them has is a **second bucket** — and the owner's bar is that two
is acceptable and one is not. **Göteborg joined Stockholm and Zurich here on
2026-09-23**, probed to the same depth, which is why this caption no longer
says "both".

**This is not "we could not find a second register".** All these negatives were
re-established on 2026-09-22 by **enumerating the whole catalogue** rather
than searching it, because the original negatives rested on keyword searches
and that is the method that has failed this project most often — Stockholm's
own food register is called *Tillsynsverksamheter*, "supervision activities",
which matches neither `restaurang` nor `livsmedel`.

| | Stockholm 🇸🇪 | Zurich 🇨🇭 |
|---|---|---|
| **Catalogue enumerated** | **309 datasets** (Entryscape, by resource-URI prefix) | **1,128 dataset names** (CKAN `package_list`) |
| **The one register** | `Tillsynsverksamheter - Livsmedel` — **8,146 distinct premises** from 289,742 inspection rows, 100% trade names, 96.9% addresses, daily from Ecos 2 | `Gastwirtschaftsbetriebe` — licensed by the city police's *Bewilligung Gastro* unit |
| **Licence** | **SILENT** — the publisher's own feed says `accessLevel: public` on all 109 of its datasets | ✅ **CC0** |
| **What a second bucket would have been** | `Salutorg`, `Torghandelsplats` — **polygons**, *"i form av ytor"*: zones where trading is permitted, not traders | `geo_bauernhofladen` — **not shops**: *"Betriebszentren von Haupterwerbslandwirten"*, farmers' operating centres |
| **Everything else that matched** | 3 × social care (`Daglig verksamhet`), 1 utility service area | `standorte` of counting stations, contaminated sites, historic cinemas, tram ticket offices |

**Why neither is discarded.** Nothing here is unresolved or unreachable —
the work is done and the answer is *one bucket*. That is a **product
judgement**, not a data defect, and it can change: a second source may
appear, or a food-density page may become worth shipping. **A discard would
throw away two complete screenings to record a preference.**

**Both countries are structurally one-bucket, which is why no further probe
helps.** Sweden has **no general business licence** at all, so retail and
personal services have no municipal source to find; Switzerland's national
**STATENT is aggregate**. This is the Hong Kong distinction inverted — there
the register exists and we cannot reach it; here we have reached everything
and only one register exists.

**If one is ever taken, take Stockholm first on size, and Göteborg or Zurich
first on licence** — Stockholm's **8,146** premises against Göteborg's
**5,063** and Zurich's **3,488**; Göteborg and Zurich are both CC0 against
Stockholm's silence. *(Updated 2026-09-23, when Göteborg joined this band and
all three were measured.)* **One owner decision moves all three**: does a
food-density page belong in a project whose other cities carry three buckets?


---

### 🇸🇬 Singapore — moved here from the coordinates band 2026-09-23

**Two buckets on paper, ONE on current data.** Four keyless premises registers
exist and the licence permits everything this project does — but **the big
one is a 2016 snapshot.**

| Register | Coverage | Rows | |
|---|---|---|---|
| **NEA Licensed Eating Establishments** | 2015-06-11 → **2016-09-06** | **36,687** | ⛔ **TEN YEARS STALE** |
| **List of Supermarket Licences** | **2016-06-26 only — a single day** | 478 | ⛔ stale |
| **Licensed Tobacco Retailers** | updated **2026-08-07** | **4,235** | ✅ current |
| **Listing of Licensed Pharmacies** | updated **2026-08-07** | **243** | ✅ current |

**The ROWS confirm the metadata rather than merely repeating it**, which is
what makes this solid rather than a metadata artefact: the only dated column in
the eating-establishments file, `suspension_start_date`, returns **2016-02-21**
and **2016-04-13**, while tobacco's `ValidPeriod` returns **2025 / 2026 /
2027**. **Two files a decade apart in the data itself.**

⚠️ **`lastUpdatedAt` says 2024-06-06 for both stale files and it is a
METADATA TOUCH, not a data refresh.** Reading that field alone would have
recorded Singapore as two years old rather than ten. **`coverageEnd` is the
honest field and the rows are the honest check.**

**So the current position is ~4,478 rows, all RETAIL** — comparable to
Göteborg's volume and narrower than Stockholm's. **This is Turin's shape,
four years worse**: Turin sits in the open screening gap for a series that
stops in 2019, *"six years stale against a project mapping CURRENT density."*

✅ **The licence is NOT the problem and was read in full 2026-09-23** —
**Singapore Open Data Licence v1.0, PERMITTED WITH CONDITIONS.** Grant is
*"worldwide, perpetual, royalty-free"* covering *"modify and adapt ... or any
derived analyses"*, commercially. ⚠️ **It carries an INDEMNITY of
Hong Kong's class and wider** — its third limb reaches *"any claim made by
a third party in connection with the third party's Use of ... any derived
analyses or applications which you have provided"*, and it **survives
termination**. **That decision is HELD, not taken**: there is no reason to
accept an open-ended liability for a city whose main register is from 2016.

🚨 **`Listing of Licensed Pharmacies` carries `Pharmacistincharge`, a
named individual on all 243 rows**, and the licence expressly grants **no
rights over** *"any personal data in the dataset"* — so publishing it would
be outside the licence, not merely against project policy.

⚠️ **Provenance decides the terms: take these ONLY from
`data.gov.sg`.** HSA's and NEA's own site terms restrict commercial reuse of
their sites' contents, and both HSA datasets point at HSA's InfoSearch page.
**The same rows from the agency's own site would carry different terms.**

**Rail was counted 2026-09-23 and carries three traps** — recorded because
they would each have surfaced mid-build: **MRT 21 relations, 21 named, only 16
coloured** (the **`JRL` Jurong Regional Line has NO colour** across all 5 of its
relations — Bucharest's `Extensie M4` in a second city, the same day); **only
ONE of three LRT lines** appears under `route=light_rail`, Sengkang, so Bukit
Panjang and Punggol are tagged some other way; and **the station counts do not
reconcile** — MRT 54 + LRT 13 against 90 rail stations total, so 23 are
tagged as neither and the naive query undercounts badly.

**Reinstatement is cheap and well-defined: if NEA refreshes the eating-
establishment register, Singapore returns to the buildable band immediately.** Everything
else about it is already done — licence read, geocode measured at 98.8%,
rail counted, registers enumerated. **It is parked on ONE fact.**

### 🇷🇴 Bucharest — moved here from the coordinates band 2026-09-23

**Nothing about Bucharest got worse. The band it was in was measuring the
wrong thing.** The band it sat in described a **measured coordinate route**, and Bucharest's is
genuinely measured. This band describes the **one-bucket ceiling**, and
Bucharest has one. **Where both are true, the ceiling is what is actually
stopping the city** — which is what these bands exist to say.

⚠️ **This project had already recorded the finding and left the row
where it was.** The 2026-09-22 entry that closed Bucharest's screening states
that **Romania's national catalogue holds no second bucket**: 4,693 datasets
enumerated from the Internet Archive, and the only commercial register in them
is ~40 dated snapshots of ONRC's **company** register. **It has been in the
wrong band since its own screening finished.**

| | |
|---|---|
| **The one bucket** | **DSVSA** — the sanitary-veterinary authority, so its **31,299 rows are FOOD**. `bucuresti.dsvsa.ro` |
| **Licence** | **SILENT**, and established rather than assumed — no terms page exists at all; the footer's *"Toate drepturile rezervate"* is a **website** footer, the New York situation |
| **Coordinates** | **OSM fallback, re-measured 2026-09-23: 146,228 addressed objects** in relation 377733 (132,478 nodes + 13,750 ways), within 112 of the earlier figure |
| **Rail** ✅ | **RE-COUNTED 2026-09-23: 13 subway route relations, 13 named, 12 coloured**, refs M1–M5, and **64 station nodes** against the *"~63 claimed, unverified"* this list carried |
| ⚠️ **The 13th relation** | **`Extensie M4` carries NO `ref` and NO `colour`.** A build keying on `ref` silently drops it; a build keying on relation count draws a line it cannot label |
| ⚠️ **Fetch is browser-assisted by necessity** | Plain curl against the XLSX returns **503 with the challenge interstitial**; the same URL **inside the browser that legitimately passed the challenge** returns 200 and real `PK` magic bytes. Never a replayed clearance cookie |
| ⚠️ **Primary portal still dead** | `data.gov.ro` resolves to 85.120.75.35 and **blackholes on 443 and 80**, now **two days running** — which weakens the original "outage, not refusal" reading. Its catalogue was read from the Internet Archive instead |

**Bucharest is the strongest-RAILED city in this band** — a real five-line
metro against Stockholm's, Zurich's and Göteborg's trams — and the
weakest on access. **The opposite trade from Göteborg**, which has the best
licence and the weakest map.

### 🇸🇪 Göteborg — promoted into this band 2026-09-23

**It was never ruled out. It was never PLACED.** The master list named it
twice — *"Unprobed candidate"*, *"Better data, weaker map"* — and put it in no
band, which is how a candidate disappears without anyone deciding to drop it.
Probed to the same depth as Stockholm and Zurich on 2026-09-23.

| | |
|---|---|
| **Catalogue** | **EntryStore**, `catalog.goteborg.se/store/search?type=solr` — the same platform as Stockholm's. Three guessed CKAN bases returned a 662-byte HTML shell first: **a wrong endpoint, not a verdict** |
| **The one bucket** | ✅ **FOOD ONLY, and the control proves it.** `livsmedel` → 1, `restaurang` → 6, but **`handel` → 0, `butik` → 0, `företag` → 0, `detaljhandel` → 0, `frisör` → 0.** The search filters, so these are real absences |
| **`Restauranger med serveringstillstånd`** | **1,043 rows**, **CC ZERO**. Carries `Namn` (trade name) and **`Besöksadress`** — the *visiting* address, kept distinct from `Fakturaadress`, the invoice address. **That is the location split done right**, the same distinction that made Norway pass |
| **`Livsmedelsverksamheter`** | *"Alla aktiva livsmedelsverksamheter"* — **active food BUSINESSES, not inspections**, so no dedupe, where Stockholm's 8,146 premises had to be distilled from **289,742** inspection rows. `accrualPeriodicity: DAILY` |
| ✅ **Row count MEASURED 2026-09-23: 5,063** | The `accessURL` **was on the DISTRIBUTION, not the dataset** — in DCAT the property you want is on the child, and the licence (**CC0 1.0**) was there too. ⚠️ **Take the CSV** (`utf-8-sig`, `;`): the rowstore JSON returns **4,786** — it drops the 279 blank-`typ` rows, swaps x and y, and BOM-mangles `namn`. Brief **2/2 — `docs/build_briefs/goteborg.md`** |
| **Rail** | **Trams, no metro — INHERITED, not measured.** It comes from the same screen that gave Copenhagen a tram it does not have and Stockholm 21 trams against a measured 6. **Verify before building.** Better data on a weaker map — the trade Toronto lost on |

**Göteborg does NOT displace Stockholm, and now that is measured**: **5,063
against 8,146**. Its advantages are structural — businesses rather than
inspections (no dedupe), CC0 rather than SILENT — and they are real, but the
count settles the size question in Stockholm's favour. *(This paragraph read
"the count that would settle it has not been taken" until 2026-09-23.)*

### Stockholm and Zurich in full

**▲ Stockholm** 🇸🇪 — **upgraded from D-c on 2026-09-22.** Screening is
DONE: a public ArcGIS FeatureServer carrying **8,146 distinct food premises**
with WGS84 points, 100% trade names and 96.9% addresses, updated daily. It
carried two questions; **the licence one was answered on 2026-09-22 — SILENT,
see item 2** — so **one remains, and it is an owner decision rather than a
probe**. ⚠️ **Item 2's text went stale the day it was answered and sat
contradicting this very sentence until 2026-09-23**, so a reader arriving at
the list saw "one remains" above a list of two. It is struck through rather
than deleted, because the superseded reasoning is what makes the resolution
legible:

✅ **RAIL COUNTED 2026-09-23, and this list's figure was wrong.** It carried *"metro 7, tram 21"*. Measured inside **Stockholms kommun** (OSM rel 398021): **subway 15 relations / 8 refs**, all named and all coloured; **tram 6 relations / 4 refs**, only **4 of 6 coloured**; **light_rail 6** (refs 21, 30, 31); **92 rail station nodes**. ⚠️ **One subway relation and one tram relation carry NO `ref`** — a `ref`-keyed build drops them silently. ⚠️ The boundary lookup matched nothing on `name=Stockholm` because the kommun is **`Stockholms kommun`**, and widening it returned **two US "Stockholm Township" relations at the same admin_level**.

1. **Scope.** It is **one bucket** — food. Stockholms stad has 291 datasets
   and exactly one commercial register; `restaurang` and `företag` both
   return **0** inside its own catalogue, and Sweden has no general business
   licence. A Stockholm page would be a food-density map.
2. ~~**Licence.**~~ ✅ **RESOLVED 2026-09-22 — SILENT, and this item
   was left standing after its own intro said it was answered.** The
   superseded text read: *"`dataportal.se` says `Åtkomsträttigheter:
   Begränsad`; the ArcGIS item says `access: public`... ambiguous in a way
   that matters, so it needs the publisher asked."* **It does not.**
   `dataportal.se` is a **HARVESTER, not the publisher** — `read-licence`
   step 5 — and the miljöförvaltning's **own** Hub DCAT feed
   (`open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json`, **109
   datasets**) declares **`accessLevel: public` on all 109**, with `license`
   **CC0 on 8** and blank on the rest. **Step 5 decides a contradiction in
   favour of the publisher, and the publisher says public.** 💡 **And
   the blank is meaningful precisely BECAUSE 8 of 109 carry CC0**: a missing
   licence field can mean *"no mechanism"* or *"declined to license"*, and here
   the mechanism is demonstrably in use.

**▲ Zurich** 🇨🇭 — **moved here on 2026-09-22 out of the one-probe-each
band, and it is the same decision as Stockholm's.** It sat in the probe band while its open item
was described as "no second bucket found". That is now **measured absent**,
which is an answer rather than a question:

✅ **RAIL COUNTED 2026-09-23 — ZURICH HAS NO METRO, AND THAT IS NOT A BLOCKER.** Zero `route=subway` relations inside the Stadt boundary (OSM rel 1682248); its network is **42 tram relations across 18 refs, all named and ALL COLOURED**, plus **4 `light_rail`, ref S18** (the Forchbahn). ⚠️ **An earlier version of this row said Zurich therefore had "no drawable network at all". That was WRONG** — asserted from prose, corrected against the code. **`route_type 0` is DRAWN in at least seven built cities**: San Diego, San Francisco, Los Angeles, Edmonton, Calgary, Miami and Dublin. **Every tram EXCLUSION is a city that also has a metro**, where the trams are a dense street-running overlay — Milan's config calls its own exclusion *"a costed extension, not a discard"* and *"reversible"*. **Zurich has no metro for a tram to overlay, so its trams ARE the rapid-transit system**, and all 42 carrying a colour removes Milan's invented-palette objection. **The live question is the Muni Metro SPACING test** — are stops one or two blocks apart, needing `docs/sub_transit_line_filters.md`? **A cost, not a disqualification.**

| Term searched on `data.stadt-zuerich.ch` | Hits | What they actually are |
|---|---|---|
| `zzqqxxnonsense` **(control)** | **0** | the filter is real |
| `detailhandel` | **1** | a **traffic count** |
| `verkauf` | 12 | tram ticket offices, apartment sale prices |
| `laden` | 31 | a farm shop, population surveys, tariffs |
| `gewerbe` | 28 | zoning land, 3D roof models |
| `firmen` | 16 | **every one a `Firmenbefragung`** — a company *survey*, 2005–2025 |

Only **`Gastwirtschaftsbetriebe`** is a register: premises-level, GeoJSON,
food. The national STATENT is aggregate. **So Zurich is a one-bucket food
city, exactly Stockholm's shape**, and the question it now carries is the
same one — *does a food-density page belong in a project whose other cities
carry three buckets?* **Answer it once and two cities move together.**

---

## ✗ Closed bands — kept in full as evidence, not as candidates

### ✗ CLOSED — access blocked (formerly Band G)

**The band's premise was that the register exists and we cannot reach it, so
none of its members was a data negative.** That premise was correct and all
three left it in different directions. **Hong Kong** left upward: its bulk
export had been published on `data.gov.hk` all along and one `package_list`
call found it. **Hyderabad and Kochi** left downward: India's entire national
catalogue — **288,011 titles** — was walked, and every trade-licence dataset
in it is an aggregate. **A band for unreachable registers is only honest
while the reaching has not been exhausted.**

#### The band as it stood — access blocked, the register exists and we cannot reach it (2 cities)

> ⚠️ **▲▲▲ Hong Kong left this band on 2026-09-22, and it was never
> actually blocked.** It was recorded here as *"the portal is a measured
> negative (statistics only), but FEHD's register exists and is queryable —
> no bulk export found"*, and described as **the single most valuable open
> thread in the screen**. It was. **`data.gov.hk`'s CKAN `package_list`
> returns 3,821 datasets and nobody had pulled it** — the recorded negative
> was a search result. Enumerating found FEHD's own licensing system
> published as bulk XML: `LP_Restaurants_EN.XML`, `LP_OtherFood_EN.XML` and
> `LP_NonFood_EN.XML`, regenerated daily. **A negative from search is a
> statement about the search**, which Stockholm demonstrated the same morning
> and which cost this city several sessions of being called unreachable.

**None of these is a data negative, and the distinction is the whole point of
the band.** Rail is answered for all three. What is missing is a route to a
register that is known to exist — which is a different thing from a register
that was looked for and was not there.

**Five cities left this sub-tier on 2026-09-22** — Santiago, Kuala Lumpur,
Jakarta, Medellín and Lima — all to *discarded*, each with a measured reason.
What remains is the set whose business leg is genuinely still open.

⚠️ **Rio de Janeiro left too, and it was a FILING error rather than a new
measurement.** Its row read *"CNPJ, no coordinates → geocoding at São Paulo's
scale"* — which describes a **geocoding** blocker, while this sub-tier means
*the business leg is the blocker*. Rio's business leg is **CNPJ, the same
national register as São Paulo**, which sits in the coordinates band as
viable, and the Tier
view already paired them. **Rio had been banded by how it was DISCOVERED — the
OSM rail screen, which is what populated D-b — rather than by what is stopping
it**, and was never re-filed once the business leg resolved. That is the one
thing this band exists to encode, so the row was moved to the coordinates
band.

Rail screened via OSM. **Relation counts are upper bounds** — see the caveat
below.

> ⚠️ **None of these five is a discard candidate, and two rows were wrong.**
> Checked 2026-09-22 by fetching each host *and* asking the Internet Archive
> whether it has seen it recently — a recent snapshot behind a failing fetch
> means **the site is alive and the failure is ours**. That test has corrected
> this project three times in one session (Sevilla, Sofia, Bulgaria's 403).
> Here it found Hyderabad's portal recorded as "dead" when it is alive,
> Kochi's row describing a **live lead nobody had followed**, and Tel Aviv's
> city portal alive behind a block aimed at us. **Unreachable is not a
> finding.**

| City | Rail (OSM) | Business leg |
|---|---|---|
| ▲▲ **Tel Aviv** 🇮🇱 | *(later discarded — see the closed awaiting-permission band)* | **PROMOTED OUT OF BAND D 2026-09-22 — to Band B. Both legs measured.** The WAF-blocked portal was never the only host: `gisn.tel-aviv.gov.il` answers, and carries **22,176 licensed businesses** with activity *and* location. See the closed awaiting-permission band below |
| **Hyderabad** 🇮🇳 | 6 rel, all named + coloured | ⚠️ **RE-PROBED 2026-09-22; every remaining route is now closed too.** `ghmc.gov.in` — the licensing body — returns **403 in a real browser**, an F5 WAF page that names itself. `data.telangana.gov.in` resolves but is unroutable for us; it runs **DKAN**, and **the Archive holds ~200 URLs but not the dataset-list endpoint**, so the route that enumerated Romania does not work here. `tgbpass` is a false friend — *building* permits. And **`api.data.gov.in`'s `q` parameter is INERT**: `Telangana` and `zzqqxxnonsense` both return the identical **288,011**, so the national API cannot be filtered at all — only its website search can, and that was already measured negative. **Blocked, not negative** |
| **Kochi** 🇮🇳 | 2 rel, named + coloured | ⚠️ **PROBED 2026-09-22, and the lead was a FALSE FRIEND.** `go.lsgkerala.gov.in/pages/query.php?t=establishment` is a **Government Orders and Circulars search** — "establishment" matches 6,526 orders about *staffing*; Kochi's own `/establishment/396` is ജീവനക്കാര്യം, its **personnel** page. In Indian government usage "establishment" means staff posts, not premises. The real route is **K-SMART** (`tax.lsgkerala.gov.in` redirects to `ksmart.lsgkerala.gov.in`) and **Sanchaya** — both live, both **transactional citizen portals** for paying tax and renewing licences, **no bulk export found**. Kerala's local bodies do issue the licences, so the register exists. **The Hong Kong shape: blocked, not negative** |

#### Paris / SIRENE — the measurement, 2026-09-22

**The architecture question was answered by Mexico, not by argument.**
`pipeline/countries/mexico.py` holds the national facts and the two city
configs differ by one line (`DENUE_STATE_CODE`). Milan is already in Band A on
`codice_ateco`, the same NACE family as France's NAF. So "a national register
is not the shape this project is built around" is **no longer true**, and the
France entry had been carrying an objection the project had outgrown.

**What Mexico does NOT answer is the kind of source.** DENUE is a **field
survey** — INEGI enumerators visit, so a row is a place that exists. SIRENE is
an **administrative register** — a row is a declaration. Measured on Paris
(commune codes 751xx, `etatadministratifetablissement = Actif`), via the
uncapped SIRENE v3 établissement stock (43,896,818 rows):

| | |
|---|---|
| All active établissements | **1,335,566** — one per 1.6 residents. Not premises |
| ...of which **sièges** | **1,231,822 (92.2%)** |
| NAF 47+56+96 buckets | **148,633** |
| ...of which sièges | **128,655 (86.6%)** |
| ...non-siège secondary premises | **19,978** |
| NAF **47.91B**, online retail | **20,542** — 24% of the whole retail division |
| Masked (`statut P`) | **176,404 (13.2%)** |

**The 148,633 is a trap.** It sits almost exactly on Madrid's 148,814, which
makes it read as a pass — but that is a coincidence of magnitude, not of
shape. 86.6% of it is sièges, and this project's invariant is explicit that
*a registrant's own name at what looks like their home* is not publishable
**even from a public registry**. This is the registered-office trap that
disqualified Germany, Austria, Latvia and Slovakia, arriving through a source
that passes every legal and access test.

**Paris has no municipal premises survey to substitute.** `opendata.paris.fr`
enumerated in full — **490 datasets** — and the closest things to a commerce
layer are `terrasses-autorisations` (24,287 terrace and display permits),
`commerces-eau-de-paris` (1,500 shops stocking the water utility's product),
`commerces-semaest` (311 units owned by a city property company) and
`plub_protcom` (5,107 **zoning** protections on commercial frontages). None is
a register of businesses. Note `marchés` here is a false friend — it means
public procurement.

**UNRESOLVED, and recorded as such:** whether APUR's **BDCom** — the Paris
commercial-premises survey, the Montréal `locaux-commerciaux` shape — is
published anywhere. `apur.org`'s site search **silently ignores the query
term**: `BDCom` returns **131 pages** of unrelated studies. So this is "could
not confirm", not "absent". It is no longer needed, but it would still be a
better source than a filtered register if it exists.

#### ✅ RESOLVED the same day: the filter works, and Paris is back in Band A

**The question was "can a NAF + siège + employee filter produce a defensible
storefront layer without mapping homes?" The answer is yes — and the siège
half of that question was the wrong lever.**

| Candidate filter, Paris NAF 47/56/96 | Rows |
|---|---|
| base | 148,633 |
| minus 47.91 online retail | 115,889 |
| **non-siège only** | **19,978 — far too aggressive** |
| not a sole trader, minus online | 79,359 |
| **A: `caractereemployeuretablissement = "Oui"`, minus online** | **50,156** |
| both employee and not-sole-trader | 47,833 |

**Filtering on siège is wrong and would have been a quiet disaster.** An
independent shop *is* its company's siège, so "non-siège only" keeps chain
branches and discards every independent — the exact inverse of what this map
is for. The **employee** filter is the right one: it keeps the boulangerie run
as an *entreprise individuelle* with staff, and drops the consultant
registered at home.

**Validated against OpenStreetMap**, which has no relationship to SIRENE:

| | OSM | SIRENE filtered | |
|---|---|---|---|
| One class — restaurants | **10,642** (`amenity=restaurant`) | **10,595** (56.10A + employer) | **0.4% apart** |
| Whole layer | **54,198** (`shop=*` 34,801 + food amenities 19,397) | **50,156** (candidate A) | **92.5% of OSM** |

Landing just *under* a volunteer map in a city as well-mapped as Paris is
where a register-derived layer should sit. The ~4,000 gap is the price of
dropping genuine zero-employee shops, and it is small next to the 65,733 rows
the filter removes.

**And there is no geocoding leg.** **148,576 of 148,633 (99.96%)** carry
`geolocetablissement` coordinates. France was being priced as if addresses
needed geocoding; they do not.

**What is still owed, and it is not a formality.** `employer = Oui` removes
home registrations **by proxy, not by proof** — a home-based business can
employ someone. So `check_personal_exposure.py` is load-bearing for Paris in a
way it is not for a municipal licence register, and a residential-address
check belongs in its Step 2. Separately, the Opendatasoft mirror used here
omits `enseigne1Etablissement` and `denominationusuelleEtablissement` — the
shop-sign fields, which are the strongest storefront signal available. INSEE's
own file carries them and would improve the filter further.

> **The relation counts are upper bounds.** The construction filter flagged
> unbuilt routes in Jakarta but returned **zero** for Tel Aviv, Bogotá and Rio —
> and Tel Aviv proves zero does not mean zero: its Green and Purple lines are
> under construction and OSM carries them as plain `light_rail` with no status
> marker. **A filter returning zero can mean "nothing to flag" or "this
> convention is not used here", and the result alone cannot tell you which.**


### ✗ CLOSED — awaiting permission (formerly Band B; Tel Aviv, discarded on terms)

**Band B held cities whose blocker was answerable at a desk.** Its last
member's desk work was done — the licence was read — and the answer was a
prohibition, which is not a desk problem. **The owner's call, 2026-09-22: a
written request made in advance and against explicit restrictive clauses is
not worth the effort.** That is a judgement about cost and likelihood, not
about the data, and the full measurement is kept below precisely so the
distinction survives.

**▲▲ Tel Aviv** 🇮🇱 — **promoted from Band D-b on 2026-09-22, and it is the
strongest unbuilt result outside Band A.** It had been carried as
*unreachable*: `opendata.tel-aviv.gov.il` and `www.tel-aviv.gov.il` both
return **HTTP 472**, Imperva's block code, and an earlier pass recorded the
host printing our own IP back — the one unambiguous IP-level refusal in this
project.

**The portal was never the only host.** `gisn.tel-aviv.gov.il` answers us
normally and serves `IView2`, the city's public map viewer — **254 layers**,
no key, no account. Third city in one day where the portal was walled and the
GIS service host was not.

| Layer | Rows | |
|---|---|---|
| **[964] `מאגר עסקים ברשיון או בהיתר`** | **22,176** | businesses holding a licence or permit — **the candidate** |
| [925] `עסקים` | **37,392** | businesses, with street + house number and floor area |
| [433] `רישיונות בביצוע` | 2,466 | licences in progress |
| [679] `מתחמי רישוי עסקים` | 29 | licensing zones (polygons) |

**Both halves of the location/activity split are present**, which is what
disqualified Tallinn, Colombia and Jakarta:

- **Activity** — `t_hesber_mahut_esek` in plain Hebrew (*grocery*, *building
  materials and paints*, *baking powder and pudding*) **plus** `mahuiot`,
  the numeric licensing-item code (406300, 407202, 1007200…).
- **Location** — `shem_rechov` (street), `ms_koma` (floor), and **point
  geometry in `wkid=2039`, Israeli TM — already projected in metres**, so
  no reprojection guesswork and no EPSG:4326 buffering trap.
- **Freshness** — `date_import` reads **20/09/2026**, two days old.

**Two questions, and both are owner decisions rather than probes:**

1. **Which business layer, and a privacy check.** [925] is larger (37,392)
   but carries **`shem_machzik_rashi` — "name of main holder"**, which is
   squarely the *registrant's own name* category this project's invariant
   excludes. [964] carries `t_shem_esek`, a **trade name**, which is the
   safe field. Recommendation: **build on [964]** and treat [925] as a
   cross-check only. `check_personal_exposure.py` must run either way.
2. **Licence — READ 2026-09-22, and it is the opposite of what "unread"
   suggested.** This was recorded as a gap to fill. It is filled, and what
   was behind it is a **prohibition**, not a silence.

   Read from the Internet Archive, because every page that carries terms is
   on the 472-blocked host — the same route that read Barcelona's and
   Sevilla's licences.

   | Source | What it says |
   |---|---|
   | **Municipal Terms of Use** (`/About/Pages/TermsofService.aspx`, captured 2026-04-21) | *"**אין להעתיק, לשחזר, לשנות, לעבד… להפיץ, לשכפל… לפרסם ו/או לאחסן את תוכן האתר**"* — do not copy, reproduce, modify, process, distribute, duplicate, publish and/or store the site's content |
   | The same document | *"**אין להשתמש בתוכן האתר ליצירת מאגר מידע ו/או לקט**"* — **do not use the content to create a database or compilation** |
   | The same document | forbids use on **other websites**, for any purpose, ***בין מסחרית ובין שאינה מסחרית*** — whether commercial or non-commercial — **without explicit prior written consent** |
   | Its definition of *"contents"* | explicitly includes **`מאגר נתונים`** — a database |
   | **`opendata.tel-aviv.gov.il`** footer (captured 2019-10-14) | ***כל הזכויות שמורות לעיריית תל-אביב-יפו*** — **All rights reserved** |
   | `data.gov.il` | Tel Aviv is **not** among its four municipal publishers — nothing to inherit |
   | ArcGIS server root, `/rest/info`, service | **no `licenseInfo`, no `copyrightText`** at any level |

   **The counter-reading, stated rather than resolved.** The Terms are titled
   *terms of use of the **website***, say *"תוכן האתר"* throughout, and the
   data sits on a **different host** (`gisn.tel-aviv.gov.il`). That is the
   **New York** situation from `read-licence`: an "All Rights Reserved"
   footer covering site content while the data itself was unrestricted.

   **But New York had an affirmative law — Local Law 11 of 2012 — forbidding
   the City to attach restrictions to its open data. Nothing equivalent is
   established for Tel Aviv**, the Terms explicitly name databases, and the
   open-data portal **asserts** rights rather than granting them. On the
   evidence the restrictive reading is materially stronger, and
   `read-licence` step 8 forbids resolving it in this project's favour.

   ⛔ **So Tel Aviv is not buildable on what is known.** The remedy is not
   more reading — it is **explicit prior written consent from the
   Municipality**, which the Terms name as the route. That is the
   **Philadelphia shape**, with one difference that matters: Philadelphia was
   already built and stands on a disclosed reasoned position, while Tel Aviv
   **has not been built and should not be** until permission exists. Tracked
   as `docs/gated_access.md` item 8.

**Rail is present but needs a scope decision, not a probe.** The city
publishes its own: Red Line stations **12**, Green **33**, Purple **19**,
with alignments. **Green and Purple are still under construction** — drawing
them would map lines that carry no passengers, the inverse of the
Guadalajara problem. Red is the operating line, and its 12 stations are the
in-city segment of a 34-station route that runs to Petah Tikva and Bat Yam,
so a boundary decision is needed too.

▼ **Valencia, Bilbao and Málaga left this band on 2026-09-22** — all three
probed, all three measured negative, all three now in *Discarded*. The
reasoning that put them here was *"two of the three Spanish cities probed have
had a register, which raises the prior sharply."* **The prior was wrong.**
Madrid and Barcelona are the exceptions in Spain, not the rule — see
"Spain is a two-city country" below.


**These two were sub-tiers of the former Band D**, which dissolved on
2026-09-22 when its live halves became Bands D and E. Both closed the same
day, and their contents are the evidence behind three discards — **Tallinn,
Sofia and Sevilla**. Kept whole, including the parts that turned out to be
wrong, because a superseded reading is how the corrected one gets checked.

### Former D-c — ✗ CLOSED (Tallinn and Sofia, both measured out)

**Finalised 2026-09-22.** These were "genuinely unreached, no finding either
way". All six are now reached and the sub-tier is closed out:

| | |
|---|---|
| ▲ **Stockholm** | promoted out — **now in the one-bucket band** |
| ▲ **Bucharest** | promoted out — **now in the coordinates band** |
| ✗ **Budapest** | **discarded** — both routes measured closed |
| ✗ **Zagreb** | **discarded** — 210 Grad Zagreb datasets, one commercial, and it is a grants list |
| ✗ **Sofia** | **discarded** — the block was routed around, and Sofia publishes no premises register |
| **Tallinn** | **parked on value**, with the äriregister half now measured |

**Sofia was the load-bearing example of "unreachable is not a negative" — and
it stopped being one.** Going around the 403 via the EU portal's SPARQL
endpoint turned it into a firm data negative, which is the outcome that
distinction exists to make possible: *reach it, then judge it.* **Tallinn is
now the only genuinely-unjudged city left in this band.**

| City | What the host actually does |
|---|---|
| ✗ **Tallinn** 🇪🇪 | **DISCARDED 2026-09-22 — MTR reached, downloaded whole, and measured.** No longer parked: the register that was going to be Tallinn's route has **no location data of any kind.** See below |
| ✗ **Sofia** 🇧🇬 | **DISCARDED 2026-09-22 — and on data, not on the block.** See the section below: the entire Bulgarian catalogue was enumerated from outside, and **Sofia does not publish a commercial-premises register.** The 403 was never what stopped it |

#### 🇪🇪 Tallinn: MTR reached and measured — 2026-09-22

The äriregister was already known to be company-shaped. **MTR**
(Majandustegevuse register) was the remaining hope, recorded as *"live HTML
with no API found, so it needs the browser"*. It needed no browser. Its
`andmed.eesti.ee` catalogue entry names a bulk export outright —
`mtr.ttja.ee/opendata/avaandmed_ettevotjad.xml`, `access: PUBLIC`,
`accrualPeriodicity: DAILY`, `applicableLegislation: ODD_LEGAL_ACT`.

**Note the recorded blocker was also wrong.** The search API was filed as
*"contract unpinned — 400 on empty `search` and on `limit=1000`"*.
`search=<term>&limit=5&page=1` answers fine; the contract simply rejects an
*empty* term. A parameter that refuses one value is not an unpinnable API.

The export is **102 MB**. It was downloaded in full and every element name
counted, rather than sampled — the head of the file is unrepresentative
(the first records are French and Polish cross-border filings, which would
have no Estonian premises anyway, and reading those two would have produced
the right answer by the wrong method).

| | |
|---|---|
| Undertakings | **56,401** |
| Licences | **100,431** |
| Estonian | **97.8%** (55,184) |
| Distinct element names in the whole file | **17** |
| **Elements naming a place** | **ZERO** |

The complete tag census is `ettevotja · registrikood · nimi · riik_kood ·
url · load · luba · tyyp · number · staatus · valdkond · tegevusala ·
emtak · emtak2025 · kood · kehtiv_alates · kehtiv_kuni`. No address, no
tegevuskoht, no coordinates. *(`vald` appears only inside `valdkond` —
a substring, not a field.)*

**This is the pure Colombia-RUES shape**: complete activity classification
(114 distinct `tegevusala`, plus EMTAK 2008 and 2025 codes) attached to no
location at all. And it fails the composition test independently — the
largest category is **`Teenindajakaart`, 25,130 service-worker cards**,
followed by freight-transport community licences and taxi vehicle cards.
**Personal and vehicle certifications, not premises.** Only `Toitlustamine`
(5,576) and `Jaekaubandus` (4,120) are storefront-shaped, and those are
Estonia-wide, not Tallinn.

Tallinn was parked on *value* — trams only, ~450k, the thinnest map in the
screen. It is now closed on *data*, which is the better reason.

#### 🇧🇬 Sofia resolved by going around the 403 entirely — 2026-09-22

`data.egov.bg` returns **403 in the browser as well as to curl**, resolves
fine via DoH (213.91.191.234), and the Internet Archive holds a 2026-04-02
snapshot — so the host is up and the refusal is **aimed at us**. That was
where this sat: *blocked, nothing learned.*

**`data.europa.eu`'s SPARQL endpoint harvests `data.egov.bg`, and it is a
different host.** Querying it recovered **11,635 Bulgarian datasets**
(ids 3–23,557) without ever touching the blocked origin. What they contain
settles Bulgaria:

| | Found | |
|---|---|---|
| `Регистър на търговските обекти` — commercial premises | **141** | across ~50 municipalities: Враца, Мадан, Костинброд, Карлово, Дупница, Тервел, Етрополе, Драгоман, Ихтиман… |
| `заведения за хранене и развлечения` — food & entertainment | **72** | the same shape again |
| **Столична община (Sofia)** | **76 datasets** | **neither register among them** |

Sofia publishes budgets, school and kindergarten lists, parking and
**taxi permits**, dams, war memorials, donations, municipal enterprises.
**No premises register of any kind.**

**So Bulgaria fails structurally, not administratively.** Its municipalities
publish exactly the register this project needs — routinely, ~50 of them —
but every one is a small town. **Sofia is the only Bulgarian city with a
metro.** The data exists where there is no rail; the rail exists where there
is no data. No amount of access changes that, which is why this is a
discard rather than a park.

**One limit on the technique, measured rather than assumed:** **0 of 20**
sampled records carry any `dcat:distribution`. The harvest is
**metadata-only** — titles and descriptions, no download URLs. The EU portal
is a **catalogue, not a bypass**: it can tell you what exists anywhere in the
EU, and the files stay behind whatever wall they were behind. That is enough
to *screen* a blocked country, and not enough to *build* one.

### Former D-d — ✗ CLOSED (Sevilla, reached and discarded)

**The whole sub-tier is closed.** Its single city was reached, measured and
discarded on the same day it was written up as unreachable. Read the section
below top-to-bottom: it is kept in full *because* the first two thirds are
wrong, and the correction at the end is the only part that stands.

▼ **Sevilla** 🇪🇸 — **downgraded 2026-09-22.** The rail half is unchanged
and still cheap: Spain's National Access Point answers **401**, the WMATA
shape, a free account. **The business half got worse.** Every route into the
city's own data failed:

| Route | Result |
|---|---|
| `www.sevilla.org`, `sevilla.org` | **do not resolve** — curl *and* browser |
| `datosabiertos.sevilla.org`, `.es` | do not resolve |
| `sevilla-ayuntamientodesevilla.opendata.arcgis.com` | live, but **"Can't access this content … Sign In"** — the Medellín shape |
| `datos.gob.es` federated catalogue | **no Ayuntamiento de Sevilla publisher exists.** The publishers returned for "Sevilla" are CIS (opinion surveys), **IGME (geological maps)** and the Junta de Andalucía |

**⚠️ DNS-over-HTTPS, 2026-09-22 — and it splits the failure in two:**

| Host | Cloudflare DoH | Meaning |
|---|---|---|
| `www.sevilla.org` / `sevilla.org` | **resolves → 94.198.88.169** | The host exists. Our 000 is a **routing failure on our side**, not DNS |
| **`datosabiertos.sevilla.org`** | **NXDOMAIN** | **The open-data subdomain genuinely no longer exists — for anyone.** The 521-dataset portal at that address has been retired |

**So Sevilla is two problems, not one.** The city's main site is reachable in
principle and blocked only to us; the open-data portal we were trying to reach
is **actually gone**. Whatever replaced it has not been found — and the ArcGIS
Hub, which is the obvious successor, is the sign-in-walled one. **That is the
thread to pull**, not the dead subdomain.

> ### ✅ RESOLVED 2026-09-22 — the thread was pulled, and it led all the way
>
> **Sevilla is now a measured negative on the business leg and a SOLVED rail
> leg.** Both halves above are superseded. How it opened:
>
> The last Archive capture of the dead portal (2024-04-25, already serving
> **503**) contains, in its own JavaScript, a KML link to
> `sevilla.idesevilla.opendata.arcgis.com/datasets/5df7320…_0.kml`. **A dead
> page named its successor** — that is the general lesson, and it cost one
> CDX query.
>
> **The sign-in wall was the HUB, not the DATA, and that reading was wrong.**
> Recorded above as "the Medellín shape", i.e. genuinely private. In fact
> `www.arcgis.com/sharing/rest` serves the city's public items **anonymously**,
> from org **`hcmP7kr0Cx3AcTJk`** on `services1.arcgis.com` — a host that
> answers us, while every `sevilla.org` address is retired or unroutable.
> Enumerating by owner returned **1,260 public items, 413 Feature Services.**
>
> **🚇 The rail leg is SOLVED, and the 401 is now irrelevant.** The city
> publishes its own metro:
>
> | Layer | Rows | |
> |---|---|---|
> | `METRO_Estacion` | **21** | `NOMBRE` — Ciudad Expo, Cavaleri, San Juan Alto… real named stations |
> | `METRO_Linea` | **20** | polylines with `ID_EST_INI`/`ID_EST_FIN` segment topology |
>
> No account, no NAP, no OSM. **Spain's National Access Point and its 401 are
> not on Sevilla's critical path at all.**
>
> **✗ The business leg is a firm negative**, and `Locales` is a **false
> friend** — the same trap as Kochi's "establishment", caught the same way,
> by opening it:
>
> | Layer | Rows | What it actually is |
> |---|---|---|
> | `Locales` + 10 district copies | **150** | `USO = VACÍO`, `ENTIDAD_CESIÓN_USO`, `ADSCRITO_A`, `Editor = 6_Empleo` — the city's own **vacant municipally-owned units offered for assignment**, published by the Employment directorate |
> | `BIENES INMUEBLES` × 11 districts, `Naves Industriales` | — | municipal **property holdings**, same family |
> | `APP_Mercados` / `Centros_Comerciales` | 18 / 120 | market *buildings* and shopping centres — **the Málaga shape**, `equipamientos` facility layers |
> | `Veladores_2023` | **389** licences (2,897 furniture items) | pavement-terrace occupation, EPSG:25830 |
>
> **Row count is what caught it.** `Locales` returns 150 city-wide and **1 for
> Triana**; Madrid's censo has 225,660. A name that matches Madrid's word for
> the right dataset, at 0.07% of the scale.
>
> All 413 Feature Services were scanned by title, not just keyword-filtered —
> the Bulgarian sweep's lesson about partial scopes applied to my own work.
> Nothing else is business-shaped. **Sevilla is DISCARDED on data.** The one
> real premises signal, 389 terrace licences, is a single narrow bucket far
> below Stockholm's 8,146 food premises, which is itself only a one-bucket
> city.

**And the Internet Archive confirms the portal was real while it lasted:**

| | |
|---|---|
| `www.sevilla.org` snapshot | **2026-09-12** — ten days old. **The site is alive** |
| `datosabiertos.sevilla.org` snapshot (2023) | **521 datasets, 1,345 distributions** — a real municipal portal |
| Enumerable from the archive? | **No.** The crawl is 347 URLs deep, 11 of them datasets, none commercial |

**This is unreachable, not a measured negative**, and the distinction is the
one this list's maintenance rule exists to protect. **Discarding Sevilla would
mean throwing away an unexamined 521-dataset catalogue because of our own
DNS.** Nothing has been learned about whether Sevilla licenses premises; only
that every route to asking is blocked on this side. **One attempt from a
different network settles it.**

**↑ That paragraph was right to refuse the discard and wrong about what it
would take.** It concluded a different *network* was needed; what it actually
took was a different *host* — `services1.arcgis.com`, reachable all along.
The rule held and protected the city from a premature discard; the cost
estimate attached to it was guesswork. **See the resolution above.**

## DISCARDED — 32 cities, each naming its evidence

▼ **Cairo left this table on 2026-09-23** for the open screening gap. Its row
read *"No open-data infrastructure"*, which rests on one probe of one national
host, and the file's own sweep had already recorded it as unprobed. **A discard
row has to survive being read against the probe log; that one did not.**


**Two rows added 2026-09-23 by the discard sweep.** Both had sat on *"Countries
ruled out"* with **no parenthetical evidence at all**, which `add-country` says
is not a discard. Both were probed, and **both discards hold** — which is worth
stating plainly rather than treating the audit as vindication.

| City | Evidence, 2026-09-23 |
|---|---|
| **Lisbon** 🇵🇹 | **The aggregate trap.** `dados.gov.pt` returns **430** hits for *estabelecimentos*, and they are **aggregate hotel statistics** — *"Proporção de estabelecimentos hoteleiros que utilizam computador (%)"* — plus prison establishments. No premises register |
| **Warsaw** 🇵🇱 | **Control passes** (`zzqqxx` → 0, so the search genuinely filters). `CEIDG` is **company-level**, the registered-office shape. **One premises-shaped lead survives** — *Wykaz punktów sprzedaży napojów alkoholowych*, licensed alcohol sales points, the Singapore-tobacco shape — **one bucket at best**, and narrower than Göteborg's |

| City | Why |
|---|---|
| **Lyon** 🇫🇷 | **DISCARDED 2026-09-23 on FOUR independent blockers, not one.** Its DATA is fine — ~18,082 bucket rows, **51.4% named**, better than Paris — which is why this is a discard on terms and access rather than on data. **(1)** An account on `data.grandlyon.com` is required before any download, and this project does not create accounts. **(2)** Grand Lyon CGU **9.4** is an open-ended indemnity. **(3)** CGU **6.2** bars the producers' *signes distinctifs* *« associés ou non à l'utilisation des données »* — which collides with the invariant that every drawn line carries its real public name, Lyon's being **TCL**. **(4)** Its National Access Point feed is **DEAD since 2022-04-14** (0% availability) while the source portal is current, so even with the account the rail must come from behind it. ⚠️ **Toulouse's and Rennes' CGU were read 2026-09-23 and are CLEAN** — Opendatasoft template, no indemnity, marks clause excluding the data — so **Lyon's clauses are Grand Lyon's own, not a French pattern.** **Reinstatement template in `DECISIONS.md`, 2026-09-23** |
| **Tel Aviv** 🇮🇱 | **DISCARDED ON TERMS, NOT ON DATA — owner's decision 2026-09-22.** The data is the strongest of any unbuilt city: **22,176 licensed businesses** with activity *and* location, **EPSG:2039 already in metres**, refreshed within two days. **The municipal Terms forbid it** — no copying, distributing or publishing, **no using the content to create a database**, extending to other websites and to non-commercial use, and requiring **explicit prior written consent**; the open-data portal's footer reads *all rights reserved*. The only remedy was a written request, made **in advance and against explicit prohibitions** — judged not worth the effort against its likelihood. **Not a data negative**, and the full measurement is retained below |
| **Hyderabad** 🇮🇳 | **India's ENTIRE national catalogue walked — 288,011 titles, 58 calls, zero failed pages — and not one premises-level trade-licence register exists.** All three trade-licence datasets in it are **aggregates**: Ahmedabad's is *No of Gumasta License* per ward per year, Karnataka's is *District wise ULB wise*, Kohima's is *Total* per ward. **Nothing for Telangana, Hyderabad or GHMC at any level.** GHMC itself 403s in a real browser (F5 WAF, names itself); `data.telangana.gov.in` is unroutable and runs DKAN, whose dataset-list endpoint the Archive does not hold; `tgbpass` is *building* permits. **Every route measured, not merely blocked** |
| **Kochi** 🇮🇳 | **Same national sweep, same result** — India publishes trade-licence **counts**, never premises. Kerala's own route is transactional: K-SMART and Sanchaya renew licences one at a time with no bulk export, and the `?t=establishment` lead was a **false friend** — in Indian government usage *establishment* means **staff posts**, and that search returns 6,526 orders about staffing |
| **Tallinn** 🇪🇪 | **MTR downloaded whole — 102 MB, 56,401 undertakings, 100,431 licences — and its complete tag census is 17 element names, NONE of which is a place.** Full activity classification, zero location: the Colombia-RUES shape. Composition fails too — the largest category is 25,130 service-worker cards |
| **Sofia** 🇧🇬 | **11,635 Bulgarian datasets enumerated via `data.europa.eu`'s SPARQL endpoint, around a 403 aimed at us.** 141 municipal premises registers exist nationally; **Sofia's 76 datasets include none.** Its registers are all small towns — Sofia is Bulgaria's only metro city |
| **Sevilla** 🇪🇸 | **1,260 public ArcGIS items / 413 Feature Services enumerated** from org `hcmP7kr0Cx3AcTJk` after the dead portal's last Archive capture named its successor. **Rail is solved** (`METRO_Estacion` 21, `METRO_Linea` 20, no account). **No premises register**: `Locales` is 150 *vacant municipally-owned units*, the rest are property holdings and facility layers |
| **Berlin** 🇩🇪 | `Gaststätten` → 0 on `datenregister.berlin.de`; the Gewerberegister is not open data |
| **Hamburg** 🇩🇪 | `Gewerberegister` → 7 irrelevant hits on `suche.transparenz.hamburg.de`; building-permit PDFs and planning polygons |
| **Naples** 🇮🇹 | Only commercial dataset is "per procedimento e Municipalità" — aggregate |
| **Messina** 🇮🇹 | SCIA/DIA are business-*start notifications* — a flow, not a stock |
| **Helsinki** 🇫🇮 | Addresses fine (89.8%) but composition is 53% real estate, 4.8% retail |
| **Bogotá** 🇨🇴 | **Fails on rail** — one unnamed-ref, zero-colour relation; its only mass transit is BRT |
| **Vienna** 🇦🇹 | GISA strips the street address by design |
| **Amsterdam / Rotterdam** 🇳🇱 | Register is aggregate |
| **Athens** 🇬🇷 | Sector-only |
| **Poznań** 🇵🇱 | Specific negative |
| **Riga** 🇱🇻 | Addressed but unclassified |
| **Bratislava** 🇸🇰 | No activity classification at all |
| **Santiago** 🇨🇱 ↓ | **Coverage.** Chile licenses per *comuna*; **5 of ~33** Metro comunas publish patentes and the **Santiago comuna is absent from the portal entirely**. The Daegu shape, 3rd occurrence |
| **Kuala Lumpur** 🇲🇾 ↓ | **Sample, not register.** `lookup_premise` passes every structural test — premises rows, 100% populated, keyless CSV — and holds **3,916 rows nationally, 372 in KL**. It is PriceCatcher's survey frame |
| **Medellín** 🇨🇴 ↓ | **Three closed doors.** The city's ArcGIS Hub is **credential-walled**; the chamber of commerce publishes comuna×CIIU **crosstabs**; RUES has **6,369,877** premises rows and **no address, municipality or city column at all** |
| **Lima** 🇵🇪 ↓ | **Coverage.** 78 licence datasets under ODC-BY, keyless CSV — but licensing is per *distrito* and **1 of Línea 1's 9** publishes usable data. La Victoria's 135,982 rows are excellent and alone |
| **Jakarta** 🇮🇩 ↓ | **No activity field.** The live OSS register has 53,827 rows and full street addresses across **exactly 9 columns**; the two that look like classification are legal form and business size |
| **Valencia** 🇪🇸 ↓ | **No premises register.** `opendata.vlci.valencia.es` is CKAN with **290 packages**, read in full. The only commercial-adjacent names are container locations, noise-monitoring stations and *zones d'activitats* — zoning polygons, not businesses |
| **Málaga** 🇪🇸 ↓ | **Business parks and facility layers only.** `datosabiertos.malaga.eu` is CKAN with **1,377 packages**. `empresas-y-sectores` is explicitly *"empresas que se encuentran en **parques empresariales**"*; `centros-comerciales` and `mercados` are `equipamientos` layers — a handful of malls and municipal markets. Licence is CC **BY-SA** |
| **Budapest** 🇭🇺 ↓ | **Both routes closed.** Portal: `kozadat.hu` is a search tool over data inventories, not a data portal. Food authority: Nébih's FELIR is **CAPTCHA-gated** and is a one-customer lookup, not a register; its *Approved Establishments* holding is **two PDFs of processing plants** — slaughterhouses, dairies, egg packers, cold stores. Retail and catering are only *registered*, by county offices, unpublished |
| **Zagreb** 🇭🇷 ↓ | **210 datasets, one commercial, and it is a grant list.** `data.gov.hr`'s CKAN lives at **`/ckan/api/3/...`**, not `/api/3/...` — 3,889 packages once found. **Grad Zagreb** publishes 210 of them; the only commercial one is *Lista za dodjelu potpora … obrtničke djelatnosti*, a grants register. Croatia devolves to municipalities and the only business databases belong to villages — `baza-poduzetnika-i-obrtnika` is **Grad Ivanec** (pop. 13,000) and carries `adresu sjedišta`, the **registered office** |
| **Bilbao** 🇪🇸 ↓ | **Aggregate barometers only.** Its own portal holds 344 datasets behind a paginated list with **no search** (its one form control is a sort order). Enumerated instead via `datos.gob.es`: **600 datasets** under publisher `A16003011`, whose entire commercial holding is *"Barómetro del comercio minorista"* — retail-trade survey aggregates by employment stratum, sector and territory |

Plus the no-urban-rail set (Winnipeg, Hamilton, Québec City, Halifax,
Mississauga, Ottawa, ~30 single-feed countries) and access-not-data
(Russia, Ukraine).

**Germany is a country-level negative**, on two cities measured independently
at two different portal hosts.

**The five added on 2026-09-22 each failed differently**, which is the useful
part: coverage (Santiago, Lima), sampling (Kuala Lumpur), no location column
(Medellín), no activity column (Jakarta). Four distinct ways for a
premises-shaped table to be unusable, and **not one of them is visible from a
dataset title**.

---

---

# BY COUNTRY — for country-by-country implementation

## ✅ Current by country — 2026-09-23

**This table is current. The Tier sections below it are the 2026-09-22 view,
retained as evidence and NOT current** — they still say Spain is in progress,
that Taiwan's geocoder is keyless, and that Hong Kong is blocked, all of which
changed. When a tier below disagrees with this table or with the bands above,
the tier is stale.

| Country | Built | Candidates | Band | What stands between it and the next city |
|---|---|---|---|---|
| 🇺🇸 United States | **9** | — | — | Complete for now |
| 🇨🇦 Canada | **5** | — | — | **Complete** — the rest have no urban rail |
| 🇲🇽 Mexico | **2** | — | — | Complete |
| 🇪🇸 Spain | **2** | — | — | **Complete** — Valencia, Bilbao, Málaga, Sevilla measured out |
| 🇮🇪 Ireland | **1** | — | — | Complete |
| 🇮🇹 Italy | **1** | Rome, Turin *(open gap)* | — | Neither is screened; Turin's series stops in 2019 |
| 🇫🇷 France | **4** | **1** — Rennes | A | Nothing but the build. Lyon discarded |
| 🇨🇿 Czechia | — | **1** — Prague | A | Build |
| 🇩🇰 Denmark | — | **1** — Copenhagen | A | Build; the Danish API key closes when it starts |
| 🇭🇰 Hong Kong | — | **1** | A | Build; indemnity accepted; map-region call |
| 🇳🇴 Norway | — | **1** — Oslo | A | Build |
| 🇰🇷 South Korea | — | **1** — Seoul | A | Build, but its brief is **deliberately partial** — seven Step-0 items undone |
| 🇧🇷 Brazil | — | **2** — São Paulo, Rio | B | **The geocoder — NEXT, by the owner's choice** |
| 🇹🇼 Taiwan | — | **4** | B | **Blocked, not negative** — no forward geocoder or bulk address file reached |
| 🇯🇵 Japan | — | **10** | B | The hardest geocode; **decided: last** |
| 🇸🇪 Sweden | — | **2** — Stockholm, Göteborg | C | One owner decision (food-only pages) |
| 🇨🇭 Switzerland | — | **1** — Zurich | C | The same decision |
| 🇷🇴 Romania | — | **1** — Bucharest | C | The same decision, plus a browser-assisted fetch |
| 🇸🇬 Singapore | — | **1** | C | **Parked on one fact** — NEA refreshing its 2016 register; indemnity held |
| 🇪🇬 Egypt | — | Cairo *(open gap)* | — | Unprobed at city level |
| **Total** | **22** | **29** | | *(+ 3 in the open gap)* |

---

## The 2026-09-22 tier view — RETAINED AS EVIDENCE, NOT CURRENT

The same 48 candidates, cut the other way. **Ordered by cities gained per unit
of work**, because that is what country-by-country optimises for, and it
reorders things sharply: Japan is mid-table by city and near the top by
country.

"Missing link" = the single thing that would move the country up a tier.

## Tier 1 — build now, nothing to discover (3 countries, 4 cities ready; ✅ Mexico DONE)

| Country | Cities | Source shape | Missing link |
|---|---|---|---|
| 🇲🇽 **Mexico** ✅ **COMPLETE** | **2** — Mexico City, Guadalajara (Regional) | **DENUE**, national, coordinates, SCIAN **is** NAICS — and the taxonomy **did** transfer from the US builds | **Nothing. Both cities are built and live in the app** (`pages/15_`, `pages/16_`, region *Mexico*), 2026-09-22. The ODbL share-alike decision was taken during the build |
| 🇪🇸 **Spain** ▶ **IN PROGRESS** | **2, not 6** — Madrid building now, Barcelona next | Bespoke **per city**, and the bespoke-ness cuts both ways | **Re-scoped 2026-09-22.** Valencia, Bilbao and Málaga all probed and all measured negative. Sevilla is unreachable. **Nothing left to find; Spain is a two-city country.** Both remaining cities have briefs and 9/9 checks |
| 🇰🇷 **South Korea** | **1** — Seoul | 8 datasets, EPSG:5174, KOGL Type 1, daily | **Two build items, not probes:** partial geocoding for 일반음식점 (90.7% coords) and a Korean-aware `check_personal_exposure.py` |
| 🇮🇹 **Italy** | **1** — Milan | Bespoke per city. Naples and Messina measured out | **Step 0 schemas** for the two newly found Milan layers. Nothing to discover |

## Tier 2 — ⇄ France: demoted and restored the same day, measured both times (1 country)

| Country | Cities | Missing link |
|---|---|---|
| 🇫🇷 **France** ▲ | **6 cities, all six now MEASURED** — Paris, Lyon, Marseille, Toulouse, Lille, Rennes | **RESOLVED 2026-09-22, and it went in favour.** Mexico closed the architecture half; the composition half was closed by an **employee filter validated against OpenStreetMap** — 50,156 rows vs OSM's 54,198, and 10,595 vs 10,642 on restaurants alone. **No geocoding leg in any of the six** — see the per-city table below. Owed: `check_personal_exposure.py` is load-bearing here, since the filter removes homes by proxy, not proof |

#### 🇫🇷 The five non-Paris cities, measured 2026-09-22

The list had been carrying *"the filter is national, so it carries to all six
cities"*. **That was an inference from a one-city sample** — and it is the
same shape as the claim that collapsed Spain from six cities to two
(*"two of the three probed had a register, which raises the prior sharply"*).
France's risk was genuinely lower, because one national register covers every
commune where Spain was bespoke per city, but lower risk is not a measurement.

Source: `economicref-france-sirene-v3` on `public.opendatasoft.com` —
**43,896,818 records**, the same uncapped v3 stock this file already cites.
**Paris was run as a control first**, because a per-city rate from a query
that cannot reproduce a known answer only looks like evidence.

| City | Active | Geolocated | **Rate** | **Storefront layer** |
|---|---|---|---|---|
| **Paris** *(control)* | 1,335,566 | 1,335,333 | **99.98%** | **50,156** ✅ |
| **Marseille** | 239,997 | 239,781 | 99.91% | **8,065** |
| **Lyon** | 190,995 | 190,941 | 99.97% | **7,354** |
| **Toulouse** | 153,407 | 153,179 | 99.85% | **4,833** |
| **Lille** | 77,416 | 77,190 | **99.71%** | **3,272** |
| **Rennes** | 64,973 | 64,906 | 99.90% | **2,089** |

**The control reproduces the recorded 50,156 exactly**, so the storefront
column is the project's own filter (NAF 47/56/96, employer, minus 47.91
online) and the six numbers are directly comparable.

**Verdict: the inference held.** No city falls below **99.71%** geolocated,
so **France genuinely has no geocoding leg in any of its six cities** and
keeps its cities-per-unit-of-work ranking. Two caveats that are now visible
only because the cities were measured separately:

- **The OSM composition validation is still Paris-only.** Geolocation is
  confirmed everywhere; that the employee filter selects the *right rows* was
  checked against OpenStreetMap in Paris alone. Cheap to repeat per city, and
  worth doing for the first non-Paris build rather than all five.
- **Rennes at 2,089 and Lille at 3,272 are thin.** Not disqualifying — Rennes
  has a two-line metro and the density question is what the map exists to
  show — but these are an order of magnitude below Paris, and whether a
  ~2,000-point city earns a page is a scope call, not a data problem.

## Tier 3 — a geocoding leg buys several cities (5 countries, 18 cities)

The investment tier. Each needs pipeline work written once, then cities are
cheap.

| Country | Cities | Business leg | Missing link |
|---|---|---|---|
| 🇯🇵 **Japan** ⏸ **DECIDED — BUILD, BUT LAST** | **10** | Food permits, CC BY, **one national schema** | **Verdict taken 2026-09-22: do the hard geocode, but not yet.** Build the easier geocoding countries first and let the shared machinery accumulate. Its own obstacles are unchanged — chōme/ban/gō, full-width numerals, `町字ID` 0% populated, and a **two-bucket ceiling** with no general retail |
| 🇹🇼 **Taiwan** | **4** | 商業登記, per-category assembly | A geocoding pass. **NLSC's geocoder is keyless**, so this is the cheapest Tier 3 entry |
| 🇧🇷 **Brazil** | **2** — São Paulo, Rio | CNPJ, no coordinates | Geocoding **past Toronto's scale**. Rio's rail is confirmed (20 relations, all named and coloured) |
| 🇳🇴 **Norway** | **1** — Oslo | 152,060 sub-units, `beliggenhetsadresse`, open API no key | A geocoding pass. Nothing else |
| 🇩🇰 **Denmark** | **1** — Copenhagen | CVR **P-enheder** with their own address + `industrycode` | A geocoding pass **and a free account** (`distribution.virk.dk` 401) |

**If you write one geocoder, write Taiwan's** — keyless, systematic addresses,
four cities. Japan's is a research project by comparison.

### Japan's cost is not fixed — it falls as the others are built

**Decided 2026-09-22: Japan gets built, and it goes last.** The reasoning is
not "postpone the hard thing", it is that **the hard thing gets cheaper while
you do the others**, so the same work costs less later.

Geocoding machinery this project already owns, from **Toronto**
(`pipeline/toronto/step3_geocode.py`) — the only Canadian city of six that
needed it, because its register carries no coordinate field and **Canada has no
national bulk geocoder**:

- a geocode step that sits between clean and map, with its own processed output
- the join-against-a-published-address-layer pattern, used instead of a geocoder
- **match-rate measurement by row type**, which is what caught the brief's
  71.4% being the wrong denominator: storefront rows matched **92.8%** while
  person-held licences dragged the all-rows figure to 73.1%
- the lesson that **the normalisation that matters is rarely street
  normalisation** — Toronto's real obstacle was units written into the address
  line (`"280 SPADINA AVE, #308"`), not abbreviations

Each Tier 3 country adds to that pool before Japan needs it:

| Build | What it contributes to Japan |
|---|---|
| **Taiwan** | A **keyless third-party geocoder** integration — request shaping, caching, rate limiting, failure handling. Japan's GSI geocoder is the same shape |
| **Norway / Denmark** | European street addresses at national scale, and the **free-account** pattern for Denmark's CVR |
| **Brazil** | **Scale** — CNPJ is ~72M rows, well past anything attempted so far |

By the time Japan is reached, what is left that is genuinely Japan-specific is
**block-address parsing** (chōme/ban/gō), **NFKC normalisation** of full-width
numerals, and the **join on `町字` by name** because the `町字ID` that exists to
make it machine-clean is 0% populated. That is a real problem, but it is a
smaller one than "write geocoding for this project".

**The risk to watch:** deferring is only cheaper if the machinery is actually
built *shared* rather than per-city. Toronto's step is city-specific today. If
Taiwan, Norway and Brazil each grow their own private copy, Japan inherits
nothing and the argument collapses. **Whoever builds the second geocoding city
should lift the common parts into `pipeline/` rather than copying Toronto's
file** — that is the decision that makes this ordering pay.

## Tier 4 — all four probed 2026-09-22; **Ireland passes** (4 countries, 4 cities)

| Country | City | State after the probe |
|---|---|---|
| 🇨🇿 **Czechia** ▲ | Prague | **Still the best probe left, and both its hosts had MOVED.** `rzp.cz` is 000 but **`www.rzp.cz` redirects to `rzp.gov.cz`**, which answers; `opendata.praha.eu` redirects to **`lkod.cz/catalog/praha`**. Two successor moves nobody had followed. **`data.gov.cz/sparql` answers SPARQL** — the Bulgarian technique applies directly. Next: enumerate for *provozovny* (premises) |
| 🇮🇪 **Ireland** ▲▲ **PASSES** | Dublin | **The probe was run on 2026-09-22 and Ireland passed — Dublin is now Band A.** `valoff.ie` was not down but **RETIRED**, and `api.valoff.ie` is **NXDOMAIN**; the API had moved twice, ending at **`opendata.tailte.ie`**, named on the *Valuation API Explorer* page and found by watching that JS page load its own link. **The deciding question is answered YES: the rateable register carries 16 use categories**, including `RETAIL (SHOPS)` and `HOSPITALITY`, plus a finer `Uses` string and `FloorUse` per floor. **Ireland is not the UK** — the NNDR's missing use category was never a property of rateable registers as such. Dublin City Council: **7,207 shops, 735 hospitality, 100% carrying Irish Transverse Mercator coordinates**, CC BY 4.0, no key |
| 🇨🇭 **Switzerland** ✗ | Zurich | **The second bucket is MEASURED ABSENT.** Control passes (`zzqqxxnonsense` → 0). Every commerce term returns noise or surveys: `detailhandel` **1** (a traffic count), `verkauf` 12 (tram ticket offices, apartment prices), `laden` 31 (a farm shop, population surveys), `gewerbe` 28 (zoning land, 3D roof models), `firmen` 16 — all **Firmenbefragung**, company *surveys* 2005–2025. Only `Gastwirtschaftsbetriebe` is real. **Zurich is a one-bucket food city — the Stockholm shape**, and it inherits Stockholm's open scope question rather than a data one |
| 🇸🇬 **Singapore** ⚠️ | Singapore | **The recorded description understated it: the search is not loose, it is INERT.** `zzqqxxnonsense` returns the **identical 10 datasets** as `licence`, `food establishment` and `business` — the query parameter is ignored entirely, and only the nonsense control tells that apart from a loose search. The catalogue is **4,628 datasets over 463 pages** and does page properly, so the route is **enumeration, not search** — the Montréal lesson, forced. Not yet done |

**Three of today's four probes hit the same thing: a host that had moved.**
`rzp.cz` → `rzp.gov.cz`, `opendata.praha.eu` → `lkod.cz`, `valoff.ie` →
`tailte.ie` — on top of Sevilla's `datosabiertos.sevilla.org` → an ArcGIS org.
**A 000 or a 404 is a question about the address, not an answer about the
data**, and this project has now spent retries on four corpses in one day.

## Tier 5 — 🇸🇪 Sweden: screening done, two owner decisions (1 country, 1–2 cities)

**New tier, 2026-09-22.** Sweden was in the old Tier 6 ("never actually
reached"). It is the only country that came out of that sweep alive, and it
sits here rather than higher because what it yields is **one city with one
bucket** — not because anything remains to probe.

| Country | City | Rail | State |
|---|---|---|---|
| 🇸🇪 **Sweden** ▲ | **Stockholm** | T-bana, ~100 stations — the strongest rail in the unbuilt set after Hong Kong | **Screening COMPLETE.** Public ArcGIS FeatureServer, **8,146 distinct food premises**, WGS84 points, trade names 100%, addresses 96.9%, daily refresh |
| 🇸🇪 Sweden | *Göteborg* | Trams | **Unprobed candidate.** Publishes **two** registers to Stockholm's one — `Livsmedelsverksamheter` (businesses, not inspections, so no dedupe) and `Restauranger med serveringstillstånd`. Better data, weaker map |

**Neither remaining question is a probe.** (1) **Scope** — food only; Sweden
has no general business licence and Stockholms stad's own catalogue returns 0
for `restaurang` and `företag`. (2) **Licence** — `dataportal.se` says
`Begränsad`, ArcGIS says `access: public`, `licenseInfo` is empty; ambiguous
in a way that matters, so the publisher gets asked.

**Cost per marginal city is poor** — one city, maybe two, and the second needs
its own probe. Ranked below Tier 4 for that reason, despite being further
along than any of Tier 4's four.

## Tier 6 — reached; one promoted out, two closed, two left (4 countries, 4 cities)

Reached 2026-09-22; what each host actually does is recorded in Band D-c
above. **Bulgaria has since become a data finding** — enumerated around its
403 via the EU portal — so the "no finding either way" caveat now covers only
Estonia and Croatia.

| Country | City | Host state |
|---|---|---|
| 🇪🇪 **Estonia** | Tallinn | API found (`andmed.eesti.ee/api/datasets/search`), contract unpinned — **400** on empty `search` and on `limit=1000`. **MTR** is the likely real route, unprobed |
| 🇭🇷 **Croatia** | Zagreb | `data.gov.hr` — **identical 1,291-byte SPA shell** at four paths incl. `data.json` |
| 🇭🇺 **Hungary** ✗ **CLOSED** | Budapest | **Firm negative on both routes.** Portal: `kozadat.hu` is a search tool over data inventories. Food authority: FELIR is CAPTCHA-gated and lookup-only; approved-establishment lists are PDFs of processing plants |
| 🇧🇬 **Bulgaria** ✗ **CLOSED** | Sofia | **Firm negative, reached around the 403.** `data.europa.eu`'s SPARQL endpoint harvests `data.egov.bg`; **11,635** Bulgarian datasets enumerated from outside. **141** municipal premises registers exist — none of them Sofia's **76**. Bulgaria's registers are all small towns; Sofia is its only metro city |

## CLOSED — the former Tier 5 (8 countries, 9 cities)

**Kept in full below as evidence, not as candidates.** This was "rail is
answered, the business leg is the hunt". The hunt finished on 2026-09-22:
**seven firm negatives, one blocked, one unreachable, no survivors.**

| | Country | Outcome |
|---|---|---|
| ⏸ | 🇭🇰 **Hong Kong** | **BLOCKED, not negative** — FEHD's register exists and is queryable, no bulk export found. **The one worth returning to** |
| ✗ | 🇨🇱 **Chile** | Coverage — 5 of ~33 comunas, Santiago absent |
| ✗ | 🇮🇳 **India** | 288,011 resources searched; nothing premises-level. GHMC and Kochi Municipal Corporation unprobed |
| ✗ | 🇲🇾 **Malaysia** | Sample, not register — 372 rows in KL |
| ✗ | 🇨🇴 **Colombia** | Hub credential-walled; crosstabs; 6.4M rows with no address column |
| ✗ | 🇵🇪 **Peru** | Coverage — 1 of Línea 1's 9 districts |
| ✗ | 🇮🇩 **Indonesia** | No activity field in a 53,827-row addressed register |
| — | 🇮🇱 **Israel** | Unreachable — IP-level refusal, browser shares the block |

The full evidence for each is below and in
`docs/global_country_shortlist.md`.

### The evidence — retained

| Country | City | Rail | Missing link |
|---|---|---|---|
| 🇭🇰 **Hong Kong** | Hong Kong | **126 relations**, 125 named | **The register EXISTS and is queryable — but no bulk export found.** See below |
| 🇨🇱 **Chile** ↓ **FAILS** | Santiago | **30 relations**, all named + coloured | **Coverage failure, measured.** Chile licenses per *comuna*; only **5 of ~33** Metro comunas publish patentes, and **the Santiago comuna itself is not on the portal at all**. See below |
| 🇲🇾 **Malaysia** ↓ **FAILS** | Kuala Lumpur | 14 relations, all named + coloured | **Sample, not register.** `lookup_premise` is a genuine premises table with **372 rows in KL** — it serves a price survey. See below |
| 🇮🇩 **Indonesia** ↓ **FAILS** | Jakarta | 9 operating of 11 | **No activity field.** The live OSS register has 53,827 rows and full addresses across exactly 9 columns, none of which says what a business sells. See below |
| 🇨🇴 **Colombia** ↓ **FAILS** | Medellín | 6 relations, **only 2 coloured** | **Three closed doors:** the city's Hub requires credentials, the chamber publishes comuna×CIIU crosstabs, and the 6.4M-row national register has **no address column**. See below |
| 🇮🇳 **India** ↓ | Hyderabad, Kochi | 6 and 2 relations | **National portal measured negative** — 288,011 resources searched, nothing premises-level. Municipal corporations (GHMC, Kochi) unprobed. See below |
| 🇵🇪 **Peru** ↓ **FAILS** | Lima | 4 relations, all named + coloured | **Coverage, not existence.** 78 licence datasets under ODC-BY, but licensing is per *distrito* and **1 of Línea 1's 9** publishes usable data. See below |
| 🇮🇱 **Israel** | Tel Aviv | 6 relations but **realistically 1** — Green and Purple are under construction | **Two problems:** the city portal returns **HTTP 472**, the documented IP-level refusal, and one operating line is thin for this project |

### Hong Kong, chased to the department — 2026-09-22

The furthest any Tier 5 city has been taken, and the verdict changed twice.

**1. `data.gov.hk` is a measured negative, by the strongest available check.**
Keyword search had returned statistics tables, which proves little. The
provider route is decisive: `organization_list` shows **129 organisations and
`hk-fehd` is one of them**, and `organization_show?id=hk-fehd` returns
**`package_count: 1`** — a single dataset, *"Products exempted from nutrition
labelling"*. So the licensed-premises register is **definitively not on the
open-data portal**. Searching by *provider* rather than *keyword* is the
generalisable move here: a keyword search cannot distinguish "absent" from
"named differently", and an org listing can.

**2. The register does exist, on FEHD's own site.**
`fehd.gov.hk/english/licensing/list_licensed_premises.html` →
**Lists of Licensed / Permitted Premises**, and it covers **two buckets**:

- **Food premises** — searchable by Shopsign/Address and by Licence/Permit Type
- **Non-food premises** — the same two routes. This is the **Personal services**
  bucket, which the earlier "food-only ceiling" claim said did not exist

The by-type form carries exactly the selectors a bulk extract needs:
`Licence Type` (General Restaurants · Light Refreshment · Marine · Factory
Canteens), `Special Endorsement` including **"All Licensed General
Restaurants"**, and **`District` including "- All districts -"** across all 19.

**3. But it is a QUERY INTERFACE, not a download.** No CSV, XLS, PDF or JSON
link exists anywhere on those pages — checked. Extraction would mean iterating
the form across licence types and districts and **scraping HTML**.

**So the honest verdict is neither "no data" nor "buildable".** It is: *a real
two-bucket premises register, publicly queryable, with no bulk route found.*
That is the **Seoul shape** — Seoul's food register also looked closed until the
page's own JS revealed a keyless POST — so the next step is to watch what the
form actually submits rather than to conclude from the absence of a download
link. Not yet done: the submit is JS-driven and did not navigate on click.

**This upgrades Hong Kong's prior considerably.** It has the largest rail
system in Tier 5 by a wide margin (126 relations, 125 named, 117 coloured) and
now a confirmed two-bucket register. What it lacks is a *route*, which is a
smaller problem than lacking data.

### Santiago — the Daegu failure, third occurrence — 2026-09-22

Provider enumeration settled this outright, and it took one pass. Chile issues
commercial licences (`patentes comerciales`) **per comuna**, so the question was
never "does Chile publish" but "how many of the ~33 comunas the Metro serves do".

`datos.gob.cl` lists **272 organisations, 67 of them municipalities**. Of those,
**15 are Metro-area comunas**, and asking each what it holds:

| | |
|---|---|
| Publish patentes | **5** — Independencia, La Florida, La Reina, Pedro Aguirre Cerda, Peñalolén |
| Present but publish none | Maipú, Puente Alto (245 datasets, no patentes), Recoleta, San Bernardo, Pudahuel, Huechuraba |
| Present with **zero** datasets | El Bosque, Ñuñoa, Quinta Normal, San Miguel |
| **Absent from the portal entirely** | **Santiago comuna itself** — the downtown — plus Providencia, Las Condes, Estación Central |

**5 of ~33, and the central comuna is missing.** Santiago's Metro converges on
the Santiago and Providencia comunas; a commercial-density map without them is
not a map of Santiago.

**This is the third time this exact shape has appeared** — Busan (4 of 16
districts), Daegu (4 of 9, with 중구 the downtown absent), now Santiago. The
generalisable rule is already in `add-country` and this confirms it: **where
licensing is devolved below the city, ask how many sub-units publish AND
whether the central one is among them, before believing a country count.** The
capital-aggregates case — Seoul, 25 of 25 — is the exception, not the rule.

### The Tier 5 remainder — where each one now stands, 2026-09-22

| Country | Method that worked | Result |
|---|---|---|
| 🇮🇳 **India** | `api.data.gov.in/lists` **enumerates — 288,011 resources** | **MEASURED NEGATIVE.** Searched properly: `trade licence` 209, `shops and establishment` 112,346, `commercial establishment` 316, **`Kochi` 1** (port exports). Every premises-shaped hit is either **one city that is not ours** (*Shops And Establishment Licence : **Ahmedabad***) or **aggregate** (*Vyapar **District wise ULB wise** Trade License Details*). Hyderabad's 192 hits are all census tables. **The national portal does not carry it**; GHMC and Kochi Municipal Corporation are the remaining route |
| 🇲🇾 **Malaysia** ↓ | Catalogue read in the browser — 292 datasets | **MEASURED NEGATIVE, and a new trap.** `lookup_premise` is a *genuine* premises table — `premise`, `address`, `premise_type`, `state`, `district`, **100% populated**, direct CSV, no auth. And it holds **3,916 rows nationally, 372 in Kuala Lumpur.** See below |
| 🇨🇴 **Colombia** (Medellín) ↓ | Browser, then provider enumeration on `www.datos.gov.co` | **MEASURED NEGATIVE, and a new trap.** The Hub is **private** — it renders *"Please sign in. This site requires credentials to access."*, which is why `data.json` 404'd and `api/search/v1` 401'd. The register-holder publishes **crosstabs**; the national register has **no address column at all**. See below |
| 🇵🇪 **Peru** (Lima) ↓ | Browser identified **DKAN**; `package_list` enumerated 4,687 datasets | **MEASURED NEGATIVE on coverage — the Daegu shape, 4th occurrence.** 78 licence datasets exist, keyless CSV, **ODC-BY**. But licensing is per *distrito*, and of Línea 1's **nine** districts exactly **one** publishes usable data. See below |
| 🇮🇩 **Indonesia** (Jakarta) ↓ | Browser read its own API off the network panel | **MEASURED NEGATIVE, and the other half of the new trap.** The live OSS register has **53,827 rows and full street addresses** — and **no activity field**, so there is nothing to filter storefronts on. See below |
| 🇮🇱 **Israel** (Tel Aviv) | — | **Not reachable by either method.** HTTP 472 and the host printed our own IP back — an IP-level refusal, so the browser shares the blocked address |

**Tier 5 is now closed: seven firm negatives, one unreachable, zero survivors.**

> **NEW TRAP — a real premises table can still be a SAMPLE, not a register.**
> Malaysia's `lookup_premise` passes every structural test this project
> applies: rows are individual premises, not aggregates; `premise`, `address`,
> `premise_type`, `state` and `district` are **100% populated**; it downloads
> as CSV with no account. It is nonetheless unusable, because it exists to
> support **PriceCatcher**, a price-monitoring programme — so it lists the
> premises whose prices are *surveyed*, and there are **372 in Kuala Lumpur**.
>
> For scale, this project's built and Band A cities carry 80,110 (Toronto,
> storefront rows), 148,814 (Madrid) and 197,276 (Seoul). **372 is three
> orders of magnitude short.**
>
> This is not the aggregate trap — the rows genuinely are premises. It is a
> **coverage** trap: the right shape at the wrong scale, and **only the row
> count reveals it**. Schema inspection passes it cleanly. The check that
> catches it is the one this project already runs for a different reason —
> *count the rows and compare against the city's plausible premises count*
> — which until now was about spotting truncation. Add sampling to what that
> check is for. Malaysia's composition also gives it away on a second look:
> 131 supermarkets and 69 mini-markets in a city of 1.8 million.

> **NEW TRAP, second half — a located register with nothing to classify, and
> a classified register with nothing to locate.** A premises table needs *two*
> columns to be a map: **where** and **what**. Both halves failed on the same
> day, in different countries, and each looked like a pass right up to the
> column list:
>
> | | Rows | Location | Activity |
> |---|---|---|---|
> | Colombia, RUES `nb3d-v3n7` | **6,369,877** | **nothing** — not even a city | CIIU codes |
> | Jakarta, OSS register | 53,827 | full street `ALAMAT` | **nothing** usable |
>
> Colombia's is the harder one to catch, because *6.4 million premises* reads
> as a decisive pass. The rows are the right entity — `ESTABLECIMIENTO DE
> COMERCIO`, the shop, expressly distinct from the company that owns it — and
> there is no address, no municipality, no city name. The finest unit in the
> file is `camara_comercio`, a chamber-of-commerce region spanning provinces.
> (It also carries owner `CEDULA DE CIUDADANIA` numbers, which this project
> would not publish in any case.)
>
> Jakarta's has exactly **9 columns**, checked against the portal's own
> component list rather than the rendered table: `periode_data`, `wilayah`,
> `kecamatan`, `kelurahan`, `nama_perusahaan`, `alamat`, `nib`,
> `uraian_jenis_perusahaan`, `skala_perusahaan`. The last two are **legal
> form** (KOPERASI, PT) and **size** (USAHA MIKRO) — neither says what the
> business sells, so `filter_to_storefront()` has nothing to act on.
>
> **Ask the two questions separately.** "Is it premises-level?" does not imply
> either one.

#### Colombia — three doors, all closed

1. **GeoMedellín's ArcGIS Hub is private.** The browser settled in one load
   what two HTTP codes had left ambiguous. No path exists to find, and this
   project does not create accounts.
2. **The register-holder publishes crosstabs.** The *Cámara de Comercio de
   Medellín para Antioquia* has nine distinct datasets on `datos.gov.co` and
   every commercial one is an *Estructura empresarial* table with the **16
   comunas as columns** and CIIU as rows — 2,349 rows of counts. Textbook
   aggregate, and CC BY-**SA** into the bargain.
3. **The national register has no location.** RUES, above.

No *Alcaldía de Medellín* business-licence dataset exists on the national
portal, which is where Ley 1712 requires publication.

#### Peru — excellent data, in one district out of nine

Peru's portal is the best-run of the group: **4,687 datasets**, keyless CSVs,
**ODC-BY** (attribution only, no share-alike). **78** carry *licencia* or
*funcionamiento*. It fails on coverage alone.

| Línea 1 district | State |
|---|---|
| **La Victoria** | **135,982 rows**, `Direccion` **100%** populated, `Giros` 54.3%, licence type and status. A genuine register — and the Gamarra garment district shows plainly in its composition |
| Cercado de Lima (Mun. Metropolitana) | 5,613 rows — **no address column, no trade name**. Administrative fields only |
| San Borja | Publishes a **metadata sheet**, not data: 20 rows × 3 columns |
| Surco · S.J. de Miraflores · V.M. del Triunfo · Villa El Salvador · El Agustino · San Juan de Lurigancho | **Nothing** |

**One of nine.** The southern four districts and the northern two — more than
half the line's stations — would be blank. Chorrillos does publish a good file
(9,767 rows, addresses) and Ate publishes a poor one (1,546 rows, no address),
but neither is on Línea 1.

Two notes for any future attempt: the CSVs are **double-quoted with `;;`
record terminators**, needing a two-stage parse; and `Nombre` carries
**sole traders' personal names**, so the project's personal-exposure check
would be load-bearing here rather than a formality.

**The method is doing its job, and the honest summary is that it mostly
closes things.** All eight Tier 5 countries are now settled: **seven firm
negatives** — Hong Kong's portal, Chile, India, Malaysia, Colombia, Peru,
Indonesia — **one upgrade** (Hong Kong's department, which turned out to have
*two* buckets but no bulk route), and **one unreachable** (Tel Aviv).
**No survivors.**

**A parameter-encoding note that cost a pass:** India's API ignores
`filters[title]=x` with literal brackets and honours `filters%5Btitle%5D=x`.
The unencoded form returns **HTTP 200 with the full unfiltered 288,011** and no
error — the same silent-ignore failure as `data.seoul.go.kr`, and the reason a
control term is not optional. The first search read as "no results" when it was
actually "no filter".

### The old Tier 6, reached — the evidence, 2026-09-22

**This is the evidence behind the new Tier 5 (Sweden) and Tier 6 (host
failures) above**, retained in full. It was "never actually reached"; the
browser sweep reached all six. One is a **partial pass** and was promoted; the
rest are host failures of varying finality.

| Country | City | State after the browser |
|---|---|---|
| 🇸🇪 **Sweden** ▲ | **Stockholm** | **PARTIAL PASS — best unbuilt result outside Band A.** A public ArcGIS FeatureServer with **8,146 distinct food premises**, real WGS84 coordinates, trade names, addresses and a usable activity field. **One bucket only** (food), and one licence conflict to resolve. See below |
| 🇪🇪 **Estonia** | Tallinn | API **found** — `andmed.eesti.ee/api/datasets/search?page&limit&search&type&sortBy&sortOrder&lang` — but it rejects an empty `search` and a large `limit` with **HTTP 400**, so the parameter contract is not pinned. `toitlustus` returns 16 datasets, all school-catering statistics. The real route is almost certainly **MTR** (Majandustegevuse register), which is unprobed. Lowest-value city in the tier: trams only, ~450k |
| 🇭🇷 **Croatia** | Zagreb | `data.gov.hr` answers 200 at **every** path with the **identical 1,291-byte** body — an SPA shell. Confirmed by four paths including `data.json`. **Still needs the browser** |
| 🇭🇺 **Hungary** | Budapest | **Misidentified until now.** `kozadat.hu` is not a data portal — it is a *search tool over public bodies' data inventories*. `budapest.hu` loads 425 KB with **two** data-ish links, one of them a privacy PDF. No catalogue found |
| 🇷🇴 **Romania** | Bucharest | `data.gov.ro` **times out** at the connection (21 s, both root and API); `portal.onrc.ro` does not resolve; `www.pmb.ro` is a 2,483-byte shell |
| 🇧🇬 **Bulgaria** | Sofia | **CORRECTION: the browser fails too.** `data.egov.bg` returns the same **403** in a real browser as to curl, so the earlier reading — that a stock Apache page implied a *client-signature* refusal worth retrying — was wrong. `data.sofia.bg` and `opendata.sofia.bg` **do not resolve**. `www.sofia.bg` and `portal.registryagency.bg` are live and unprobed |

### 🇪🇸 Spain is a TWO-city country — measured 2026-09-22

Spain had been carried as *"2 now, 6 total"* on the reasoning that it licenses
bespoke per city and **two of the three cities probed had a premises census**,
which *"raises the prior sharply"*. That prior is now measured, and it was
wrong: **Madrid and Barcelona are the exceptions, not the rule.**

| City | Portal | Enumerated | Verdict |
|---|---|---|---|
| **Valencia** | `opendata.vlci.valencia.es` (CKAN) | **290 packages** | ✗ The only commercial-adjacent names are container locations, noise stations, and *zones d'activitats* — **zoning polygons, not businesses** |
| **Málaga** | `datosabiertos.malaga.eu` (CKAN) | **1,377 packages** | ✗ `empresas-y-sectores` is explicitly businesses **in business parks**; `centros-comerciales` and `mercados` are `equipamientos` facility layers. CC **BY-SA** |
| **Bilbao** | own portal + `datos.gob.es` | 344 own / **600 federated** | ✗ Entire commercial holding is **"Barómetro del comercio minorista"** — retail-trade survey aggregates by employment stratum, sector, territory |
| **Sevilla** | ArcGIS org `hcmP7kr0Cx3AcTJk` | **1,260 items / 413 Feature Services** | ✗ **Measured negative** (was "unreachable" — the Hub's sign-in wall hid nothing; `sharing/rest` is public). `Locales` is **150 vacant municipally-owned units**, not businesses. Rail *is* solved: `METRO_Estacion` 21, `METRO_Linea` 20 |

**A method note worth carrying.** Bilbao's own portal holds 344 datasets across
35 pages and offers **no search** — its only form control is a sort order. Paging
it 35 times would have been the obvious move and the wrong one. Spain federates
every municipal portal into **`datos.gob.es`**, which speaks DCAT over a
documented API, so one publisher enumeration (`/catalog/dataset/publisher/<id>`)
covers any Spanish city at once. That is the primitive to reach for next time a
Spanish city comes up.

**And a caution about the national catalogue**: searching it by *title* returns
almost entirely **INE** (publisher `EA0042823`) aggregate statistical tables —
*Locales por provincia y condición jurídica*, hotel occupancy, and so on. Those
look like premises data and are not. Enumerate by **publisher**, not by title.

### 🇸🇪 Stockholm — a real register, found four hops deep

The route is the argument for navigating rather than guessing; no step of it
was predictable from the outside:

`dataportal.se` → organisation **Stockholms stad** (291 datasets, 101 open,
190 *skyddade*) → the **one** commercial hit, *Tillsynsverksamheter -
Livsmedel* → its page links the miljöförvaltning's ArcGIS Hub → the Hub item
id resolves through `arcgis.com/sharing/rest` to a **public** FeatureServer.

| Measured | |
|---|---|
| Rows | **289,742** — but a row is an **inspection**, carrying `TillsynsDatum` and `Anmarkning`. "Nyko Kitchen, Nybrogatan 61" repeats across dozens |
| **Distinct premises** (`ObjektId`) | **8,146** |
| Geometry | `esriGeometryPoint`, real WGS84 — `(18.0804, 59.3388)` — plus SWEREF99 northings/eastings |
| `Adress` | 280,760 of 289,742 rows non-empty (**96.9%**) |
| `AnlaggningsNamn` | **100%** — trade names |
| `VerksamhetsTyp` | 22 values, **29.5%** of rows non-null: *Restaurang-, catering- och barverksamhet* 65,858 · *Detaljhandel* 11,103 · *Partihandel* 2,810 |
| `AnlaggningsTyp` | **0% — entirely `'None'`.** The field exists and is empty |
| Update | daily/weekly, from Ecos 2 |

**The row-count discipline cuts both ways.** Malaysia's count was too *small*
to be a register; Stockholm's is too *large*. Both are answered by asking what
a row **is** before trusting the number — and here the answer is good news,
because 8,146 premises with coordinates is a real city leg.

**The activity field is recoverable but not free.** `VerksamhetsTyp` is null on
70.5% of rows because it describes the *inspection*, not the premises — so it
has to be lifted to premises level by taking any non-null value per `ObjektId`
during dedupe. That is ordinary work, not a blocker, but it is work, and it is
the difference between this and Jakarta, where no activity field existed at all.

**Two open questions before Stockholm could be built:**

1. **One bucket.** This is food only. Stockholms stad has **291 datasets and
   exactly one** commercial register — `restaurang` and `företag` both return
   **0** within its catalogue. Sweden has no general business licence, so
   retail and personal services have no municipal source to find. This is the
   Hong Kong shape, improved: a real bulk route exists, but a Stockholm page
   would be a **food-density map**, not the three-bucket map the built cities
   carry. That is a scope call, not a data problem, and it belongs to the
   owner. `multi-source-city` is the relevant process if a second source is
   ever found.
2. **A licence conflict that must not be resolved in this project's favour.**
   The `dataportal.se` metadata record says `Åtkomsträttigheter: **Begränsad**`
   (restricted); the ArcGIS item says `access: **public**` and serves the data
   without credentials. `licenseInfo` is **empty**; `accessInformation` reads
   only *"Stockholms stad, miljöförvaltningen"*. Per `read-licence` step 8 this
   is **ambiguous in a way that matters** and needs the publisher asked — the
   fact that it fetches is not a finding that it is licensed.

   > **⚠️ SUPERSEDED 2026-09-22 — the pointers were followed, and the conflict
   > mostly dissolves.** The paragraph above jumped to step 8 ("ask the
   > publisher") while steps 2, 3 and 5 were still undone: it treated a
   > **harvester's** metadata field as the last word and never opened the
   > documents that record names. What reading found:
   >
   > | Source | Says | Weight |
   > |---|---|---|
   > | `dataportal.se` (the **harvester**) | `accessRights: RESTRICTED`; `license:` the category **`otherlicense`**, not a licence | weakest — a third-party catalogue |
   > | **Miljöförvaltningen's own Hub DCAT feed** — `open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json`, **109 datasets** | **`accessLevel: public` on all 109**; `license` **CC0 on 8**, blank on 101 incl. this one | **strongest — the publisher asserting** |
   > | ArcGIS item `8447f7af…` | `access: public`; **no `licenseInfo` field at all** | publisher |
   > | FeatureServer root | `copyrightText: "Stockholms stad, miljöförvaltningen"`; `licenseInfo` empty | publisher |
   > | `dataportalen.stockholm.se` deep link | redirects to **`catalog.signin`** — walled, and this project does not create accounts | unread |
   >
   > **`read-licence` step 5 decides the contradiction: the publisher outranks
   > the catalogue**, and the publisher says *public* on all 109 datasets.
   > That the publisher **declares CC0 on 8 of them** matters too — it shows
   > the licence field is one they use and chose not to fill here, so the
   > blank is a genuine silence rather than a missing capability. Those 8 are
   > a single thematic cluster (ArtArken, biotopes, substrates, landscape),
   > which reads as one team licensing its own outputs.
   >
   > **One tempting over-reach, declined.** Stockholm's traffic office states
   > at `openstreetgs.stockholm.se`: *"Datainnehåll i dessa tjänster får
   > vidareutnyttjas fritt och tillhandahållas **'Licensfritt'** om inget
   > annat anges"* — freely reusable, licence-free unless otherwise stated.
   > **That is Trafikkontoret's statement about *dessa tjänster*, its own
   > services — not miljöförvaltningen's**, and extending one department's
   > terms to another's data is exactly the move this skill exists to stop.
   > It is evidence about the city's posture, not a licence for this dataset.
   >
   > **Position now: SILENT, not restricted** — the Miami-Dade shape, where
   > the authoritative pages were read and impose no reuse position. Still
   > genuinely unread: the **walled GeoNetwork record** (try the Internet
   > Archive, as Barcelona's and Sevilla's were read) and any city-wide open
   > data policy page. **A letter is no longer the next step, and never was
   > the first one.**

**A second Swedish city worth noting:** `dataportal.se` shows **Göteborgs
stad** publishing *both* `Livsmedelsverksamheter` ("alla aktiva
livsmedelsverksamheter", JSON + CSV) and `Restauranger med serveringstillstånd`
(CSV) — i.e. **two** food-adjacent registers where Stockholm has one, and
`Livsmedelsverksamheter` is a register of *businesses* rather than of
inspections, so it needs no dedupe. Gothenburg's rail is trams rather than a
metro, so it is a weaker map for a stronger dataset. Unprobed.

## Countries ruled out

🇩🇪 **Germany** *(two cities measured at two hosts — the Gewerberegister is not open data)* ·
🇦🇹 **Austria** *(GISA strips the street address)* · 🇳🇱 **Netherlands** *(aggregate)* ·
🇬🇷 **Greece** *(sector-only)* · 🇵🇹 **Portugal** *(aggregate — Lisbon, 2026-09-23)* ·
🇵🇱 **Poland** *(company-level CEIDG — Warsaw; Poznań)* ·
🇱🇻 **Latvia** *(unclassified)* · 🇸🇰 **Slovakia** *(no classification)* ·
🇬🇧 **UK** *(NNDR is a tax register with no category)* ·
🇦🇺 **Australia**, 🇳🇿 **New Zealand** *(licensing is not municipal)* ·
🇧🇪 **Belgium** *(bulk access paid)* · 🇦🇪 **Dubai** *(no agency feed)*

*🇪🇬 **Egypt left this list on 2026-09-23** with Cairo: one probe of CAPMAS is
not a country ruling. See the open screening gap.*

## The order, as decided

> **Current position, 2026-09-23.** Mexico, Spain, Ireland and Italy's Milan
> are built; France is **two of five** (Paris, Marseille). **The eight Band A
> cities are build-ready now.** In the geocoding band, **Brazil goes first by
> the owner's choice** — Taiwan, which the list below puts first, turned out to
> have no forward geocoder or bulk address file reachable — and **Japan stays
> last**. The numbered order below is the 2026-09-22 plan, kept because its
> reasoning (lift shared geocoding machinery into `pipeline/`, let Japan
> inherit it) still holds even though the country it named first changed.

1. ✅ **Mexico** — **DONE, 2026-09-22.** Two cities from one source, as
   predicted. It was also the project's first country outside anglophone North
   America and its first OSM-sourced rail leg, so it proved two things the
   screen had only asserted.
2. ▶ **Spain — NEXT, and it is exactly two cities.** Madrid and Barcelona are
   ready now, each with a build brief whose claims re-run green. The "other
   three likely rather than speculative" line was wrong: Valencia, Bilbao and
   Málaga were probed on 2026-09-22 and are measured negatives, and Sevilla is
   unreachable. **Plan Spain as two cities, not six.**
3. **Korea** and **Italy** — one city each, nothing to discover, both with
   named build work rather than open questions.
4. **Taiwan** — the first geocoding build, chosen because it is the cheapest:
   keyless geocoder, systematic addresses, four cities. **Lift the shared parts
   into `pipeline/` here**, not later.
5. **Norway**, **Denmark**, **Brazil** — the rest of Tier 3, in rising
   difficulty.
6. ⏸ **Japan** — **last, by decision.** Ten cities, and by then the geocoding
   machinery is built.

**France no longer sits outside this order awaiting a decision** — it was
made on 2026-09-22 and, after one reversal, went **in favour**. The employee
filter yields a defensible storefront layer, validated against OpenStreetMap,
and SIRENE arrives geolocated. That makes France **six cities on one national
integration with no geocoding leg** — on cities-per-unit-of-work, the
strongest unbuilt country in this screen. It belongs in the order, and where
it goes is the owner's call.

Tier 4's four probes (**Czechia** strongest) are cheap enough to run alongside
any of the above rather than competing with them.

**Sweden sits outside the numbered order too**, for the opposite reason to
France: its work is not architecture but a **scope call** — whether a
one-bucket, food-only city page belongs in this project at all. Settle that and
Stockholm is close to ready; leave it unsettled and there is nothing to build.
**Hong Kong is the one closed country worth reopening**, since its register is
known to exist and only the bulk route is missing.

---

## Two rules this list is maintained by

**A row reading "not reached", "unprobed" or a regional pattern is not a
discard.** Eleven cities were once sitting in the discard list on exactly those
grounds, against evidence in the same document. Every discard row above names
the finding that disqualified it, so a contradiction is visible rather than
inferable.

**A country ruling needs two cities measured, not one asserted onto a region.**
Germany qualifies — Berlin and Hamburg, at two different portal hosts. Italy
does not fail merely because Naples did, which is why Milan sits in Band A.

## Before building any city on this list

- `docs/build_briefs/<city>.md` if one exists, then
  `python scripts/brief_check.py <city>` — a brief caches Step 0's mistakes as
  confidently as its findings.
- **A city outside every existing region needs one added.** `app/cities.py`
  raises on a city whose region is not a leaf of `REGION_ORDER`. **Europe is
  already ONE region**, so a new European country (Czechia, Denmark, Norway,
  Sweden, Switzerland, Romania) does not add one; **Seoul, Hong Kong, Brazil,
  Taiwan, Japan and Singapore each would**, and `check_macro_labels.py` is the
  measurement for whether a region frames its cities. *(This bullet said
  `REGION_ORDER` was still `["United States", "Canada"]` until 2026-09-23 — it
  now holds seven entries.)*
- `add-country` first for any country this project has never built in — every
  candidate country except France.
