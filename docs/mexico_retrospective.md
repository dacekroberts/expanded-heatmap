# Mexico, start to finish: one national register, and rail that isn't GTFS

Companion to [`canada_retrospective.md`](canada_retrospective.md), written the
same way and for the same reason: the per-city numbers live in `DECISIONS.md`,
and this file is what the *country* cost and what it changed. Its pair is
[`spain_retrospective.md`](spain_retrospective.md) — read both if you are
choosing a fourth country, because **Mexico and Spain fail in opposite
directions** and between them they bracket what a country profile can be worth.

**Cities built:** Mexico City (15), Guadalajara (Regional) (16).
**Country shape:** one national establishment census, bespoke rail per city.

---

## The one-line version

**Mexico's business leg is the cheapest this project has ever had, and its rail
leg is the most expensive.** One register — INEGI's DENUE — covers every city
in the country with 100% coordinate population and a trade name on 99.95% of
rows. No city needs a geocoder, a parcel join, a residence inference or a
name-fallback rule. Against that, neither city could use GTFS at all, and the
two cities' *station objects were different OSM tags*.

So the marginal cost of a Mexican city is dominated almost entirely by its rail.
That is the opposite of the US and Canadian pattern, where rail was cheap
(GTFS) and business data was the problem.

---

## What made Mexico structurally different

Three firsts, each of which changed shared code:

| First | Consequence |
|---|---|
| **First city whose rail is not GTFS** | `osm-rail` skill; OSM loader in `map_common.py`; five new trap classes |
| **First outside the licence-register model** | `scian.py`; density figures that are *not comparable* with the register cities |
| **First non-English city** | `check_personal_exposure.py`'s heuristic revealed as English-shaped |

### The register is a census, not a register, and that changes what the map means

DENUE is an **establishment census** INEGI collects by surveying premises.
Toronto's register licenses food and trades but **no general retail at all**;
Vancouver's licenses businesses, not premises. So:

- Mexico City: **818 businesses per station**. Guadalajara: **659**.
- Vancouver: 206. Toronto: 81.

**Those numbers are not comparable and the city pages say so.** 818 measures
*source completeness* at least as much as commercial density. This is the
single most important thing to carry into any country with a national
establishment census (France's SIRET, Norway's `beliggenhetsadresse`): the
density figure changes meaning, and a reader will compare it anyway unless the
page stops them.

### SCIAN is *not* NAICS, and the shortlist said it was

`docs/global_country_shortlist.md` recorded "SCIAN = NAICS so the taxonomy may
transfer." Measured: **right for two buckets of three, wrong on the largest.**

- SCIAN numbers retail **46**; NAICS uses **44–45**
- Wholesale **43** against **42**
- Food service **722** and personal services **812** agree

`naics.py` pointed at DENUE would have left **212,251 retail rows — 45.87% of
the file — unclassified.** The one mercy is that `classify()` raises on unknown
values, so it would have failed loudly rather than shipping a map missing half
its retail.

**The lesson generalises past Mexico:** a classification *family* resemblance is
not transfer. Check the prefixes bucket by bucket, and do it before writing the
config, not after the first run.

### And the two-digit prefix was the obvious-looking mistake

A first pass counted `72` for food service and reported 58,167 units and "73.07%
in the three buckets". Both wrong: `72` includes **721 accommodation** (999
hotels), and crude two-digit prefixes also swept in 811 repair, 813 associations
and 812410 parking. Correct figures: **57,168** and **64.1%**.

**Accommodation hiding inside food service is now a three-country pattern** —
here as SCIAN 72, and in Barcelona as 720 `serveis d'allotjament` inside
`Restaurants, bars i hotels`. Assume it is there and look for it.

---

## The rail leg: five OSM traps, and the one that recurred

Both cities needed OpenStreetMap, for **different reasons that are worth keeping
distinct**:

- **Mexico City** — every `*.cdmx.gob.mx` host times out. Unreachable.
- **Guadalajara** — the only feed in the Mobility Database declares
  `feed_end_date = 20230128`, is published by Nubenautas rather than SITEUR, and
  carries **three** light-rail routes where SITEUR runs **four**. **Línea 4
  opened 2025-12-15**, nearly three years after the feed stopped. Building from
  it would have drawn a map missing an operating line, 8 stations and 21 km —
  *while looking complete.*

Absent and stale are different findings. Record which.

### The traps, in the order they bit

1. **Entrances outnumber stations 2.4×.** 447 `railway=subway_entrance` nodes
   against 184 stations in the same bbox. Would have inflated every ring.
2. **A misspelled tag defeats a blacklist.** 13 proposed Texcoco stations, five
   tagged `railway=prpopsed`. A blacklist on `proposed` draws rings around
   building sites while looking correct. **Whitelist what you want.**
3. **A network label is not a mode.** OSM tags Lechería — a Ferrocarril
   Suburbano station — `network=STC Metro`. Match on *what a node is*, never on
   *a label claiming who operates it*.
4. **Collapse is by name, and OSM is the fourth mechanism.** One node per line at
   an interchange: Pantitlán has 4, La Raza / Jamaica / Oceanía / Tasqueña 2
   each. After Edmonton's `parent_station`, Calgary's direction prefix and
   Toronto's three conventions.
5. **An unbounded name search is a global search.** `admin_level=6
   name="Guadalajara"` with no bbox matched **Guadalajara, SPAIN**, and the
   "keep the largest polygon" tie-breaker then chose it *on purpose* —
   26,814 km² against the real 151. **Never tie-break same-named boundaries by
   size:** the wrong candidate is usually a larger administrative unit.

### The recurrence that produced a skill

`pipeline/mexico_city/config.py` says, in capitals, *"MATCH ON THE MODE, NEVER
ON THE NETWORK LABEL ALONE"*. Guadalajara's first Overpass query was
`node["railway"]["network"="Mi Tren"]` — which returned 96 nodes and **silently
omitted every one of Línea 4's 8 stops**, whose nodes carry no `network` tag
because the line is nine months old. Result: a 49-station set with zero stations
in Tlajomulco de Zúñiga — *the same missing line as the rejected feed, reached a
different way.*

**The cause is placement, not forgetfulness.** A warning in the previous city's
config is not a file anyone opens while writing the next one. This produced the
ordering rule that now opens `osm-rail`:

> a raising check in shared code → then a skill → then the shared module →
> and a city's own config **last**, and only for facts about that city.

### The finding nobody would have predicted

**The station object itself differs between two cities in one country.** Mexico
City has **184** `railway=station` nodes. Guadalajara has **one** — its stations
are `railway=stop` positions, 110 of them collapsing to 56 names. Mexico City's
whitelist finds a single station in Guadalajara, and *the failure would have
looked like a boundary or scope problem rather than a tagging one.*

This is the sharpest argument the project has for `pipeline/stations.py` sharing
the **checks** and leaving the **collapse** per city.

---

## Gate 3 could not be run, and that was disclosed rather than worked around

`pipeline/stations.py` calls the operator's published station count *"the one
check that can see an error every internal check agrees with"* — it corrected
Edmonton 33→30 and Toronto 118→110.

- **Mexico City: impossible.** `metro.cdmx.gob.mx` ConnectTimeout on every host
  and scheme; the whole domain is dead. No block page names an IP, so the
  browser does not help either. `STATION_COUNT_GATE_3 = None` records *why*.
  **No remembered figure was typed into the config** — a number from memory
  looks exactly like gate 3 and is worthless.
- **Guadalajara: runs and passes.** SITEUR publishes *"10 estaciones
  subterráneas"* for Línea 2 and *"Estaciones: 8"* for Línea 4; OSM
  route-relation membership gives 10 and 8. **Both match.** No count is
  published for Líneas 1 or 3, so none is recorded — *a partial gate 3 with its
  gaps named is worth more than a complete-looking one filled in from memory.*

---

## Privacy: the strongest position in the project, and the publisher earned it

INEGI omits `raz_social` entirely when the owner is a *persona física* — its own
dictionary says *"para proteger la confidencialidad de la información"* — and
defines `nom_estab` as the name on the shopfront, *"visible y escrito en
rótulos, fachadas o anuncios luminosos"*, present on 99.95% of rows.

**So Los Angeles' failure has no mechanism here.** There is no personal name to
fall back to, because the publisher withheld it rather than substituting it.
Step 2 forbids `telefono` (35.6% populated), `correoelec` (22.6%), `www`
(10.6%) and `raz_social` (25.9%) and *asserts they never arrive*.

### The check reported 32.2% and the finding was about the check

`check_personal_exposure.py` flagged 32.2% of pins as "look like a person". A
hand-sample of 26 found **none** that were a person presented as a person:
`ABARROTES LIZ`, `ESTÉTICA MARIFER`, `ZAPATERÍA SOFI`, `POLLERÍA BACHOCO` — the
Spanish shop-sign convention of trade type plus a given name — and `COCINA
ECONÓMICA`, two common nouns, trips it too.

`looks_personal` is tuned for English `SMITH JOHN` forms. **The first
non-English city turns a tool's assumptions into a measurement.** Expect this
for every new language, and sample before believing a rate.

---

## What Mexico gave the whole project

- **`.claude/skills/osm-rail/`** — the OSM branch of `add-city` Step 4, and the
  meta-rule about where a lesson has to live.
- **`pipeline/taxonomies/scian.py`** — differing from `naics.py` in exactly two
  prefixes. Rejected: a country flag on `naics.py`, which would put the most
  consequential constant in the project behind an argument.
- **`all_city_heat=False`** — the opt-in whole-city heat layer, off for both
  Mexican cities. 25.7 → 19.0 MB.
- **Indexed classification values in every rendered map.** Mexico City made the
  cost visible — **106 distinct values across 283,345 rows**, one 73-character
  string appearing **12,462 times in one file**. Total committed output
  **43.17 → 33.31 MB (−22.8%)**, from −1.1% (San Diego, short NAICS codes) to
  −15.7% (Toronto). *The spread is the point:* the saving tracks how long a
  register's category vocabulary is, so measured on the US cities alone it would
  have looked negligible and been skipped.
- **A line-vs-line colour failure.** `linecolour.py` stopped a build for the
  first time, on a case it was not written for: Línea 2 `#005EB8` against Tren
  Ligero `#0554ba` at Delta-E **9.8**, and Línea 3 against Línea 12 at **8.5**.
  Every previous finding had been line-vs-*category*.

---

## What a third Mexican city would cost

**Cheap, and the cheapness is real rather than assumed** — Guadalajara proved it
by separating national from local. What transfers untouched: the register,
`scian.py`, the licence and its notice, the encoding, the forbidden columns, the
`Fijo` filter, the OSM line loader.

What does not, and must be re-derived every time:

1. **The state code and the projected CRS** (32614 against 32613).
2. **The municipio scope** — and whether the build is regional. SITEUR's own
   description put three municipios on one line; a city-only build would have
   truncated two of four lines.
3. **The station object** — `railway=station` or `railway=stop`, per city.
4. **Gate 3's availability** — per operator, not per country.

Budget the rail leg. Assume the business leg is solved.
