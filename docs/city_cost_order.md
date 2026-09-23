# Remaining candidates, ordered by what they COST

**This file answers a different question from `docs/city_master_list.md`, and
the difference is the reason it exists separately.** The master list bands each
city by **what is stopping it** — the blocker, which is a fact about the city.
This one bands by **what it would cost to finish** — which depends on what this
project has already built, and therefore changes every time a city lands even
though nothing about the remaining cities changed.

Keeping them in one file would force one ordering to hide the other. A city can
be **unblocked and expensive** (Milan: nothing stops it, and it buys one city)
or **blocked and cheap** (Bucharest: its portal is down, and everything else
about it is measured).

- **Read the master list to decide whether a city is possible.**
- **Read this to decide which possible city to do next.**
- When the two disagree about a *fact*, the master list wins and this file is
  stale. When they disagree about an *order*, that is not a disagreement.

**Current state, 2026-09-23 — 30 candidates.** Dublin, Milan and **Paris** are BUILT and
are not counted here; Göteborg was added by the 2026-09-23 discard sweep.

---

## The one thing that drives cost more than anything else

**A country profile converts into cities at a rate that varies by an order of
magnitude, and that rate — not the difficulty of any single city — decides
what is worth doing next.**

Mexico is the measured precedent: the country was profiled once and the second
city's config differed by **one line** (`DENUE_STATE_CODE`). Spain is the
counter-example and is documented as such in `docs/spain_retrospective.md` —
two cities that shared a country and almost nothing else.

So every row below carries **how many cities the work buys**, and that column
is why the order is what it is.

---

## Cost band 1 — nothing left to discover, and no geocoding leg (0 cities — EMPTIED)

| City | Buys | Why it is cheapest | What is actually left |
|---|---|---|---|
| **Paris** 🇫🇷 ▲ | **6** | **99.96% already geolocated** — 148,576 of 148,633. There is no coordinate leg at all, which no other unbuilt city can say | France country facts, NAF taxonomy, OSM rail |

**Milan was the other member of this band and is now BUILT (2026-09-22).**
It was the same class of work as Paris and lost on the `Buys` column — one
city against six — which is the ordering this file exists to make visible.

## Cost band 2 — free riders on band 1 (4 cities)

| Cities | Buys | Marginal cost |
|---|---|---|
| **Marseille · Toulouse · Lille · Rennes** 🇫🇷 | — | **The same SIRENE, the same Licence Ouverte 2.0, the same filter.** The cheapest builds available anywhere on this list — but **strictly after Paris**, never instead of it. ⚠️ France's OSM rail composition is validated on **Paris only**; the first non-Paris build must re-validate it. ⚠️ **Lyon was REMOVED from this band 2026-09-22** — three gates (an account this project will not create, a trademark clause that collides with the on-map line-label invariant, and the project's second indemnity), so it is no longer a cheap follower. ⛔ **It was DISCARDED 2026-09-23** on four independent blockers — see the master list |

## Cost band 3 — coordinates are a JOIN (2 cities)

| City | Buys | Route | What is left |
|---|---|---|---|
| **Prague** 🇨🇿 | 1 | **99.8%** — a 3.4 MB keyless download and a dict lookup | Czech facts, CZ-NACE taxonomy, rail (Golemio key *or* OSM). ⚠️ EPSG:5513 sign-and-axis flip, verified 2026-09-22 |
| **Copenhagen** 🇩🇰 ✅ | 1 | **96.9%** of its storefront rows carry a **DAR address UUID** — a join, not a geocode | ✅ **UNGATED 2026-09-23 and MEASURED: 14,887 rows across THREE buckets** (retail 6,689 / food 5,163 / personal 3,035) at **100.0% named** — the best-named register in the project. Licence **CC BY 4.0**. Owner obtained the Datafordeler key; only `CVRPerson` is gated and this project does not want it. ⚠️ **`v/` marks a sole trader's personal name** in the trade-name field — unmeasured. ⚠️ Frederiksberg (0147) is a separate kommune inside Copenhagen — omit it and the map has a hole in its middle |

## Cost band 4 — coordinates are a keyless GEOCODE (4 cities)

| City | Buys | Rate | Cost driver |
|---|---|---|---|
| **Hong Kong** 🇭🇰 ▲▲▲ | 1 | ALS answers, returns a confidence `Score` | **Best rail in the whole screen** — 126 relations, 125 named, 117 coloured. ✅ Indemnity ACCEPTED 2026-09-22 |
| **Singapore** 🇸🇬 ⛔ | 1 | **98.8%** of answered lookups | ⛔ **MOVED TO THE ONE-BUCKET BAND 2026-09-23.** Its big register — NEA eating establishments, 36,687 rows — **covers 2015-06-11 to 2016-09-06**, and the rows confirm it (`suspension_start_date` returns 2016). Only tobacco 4,235 and pharmacies 243 are current: **~4,478 rows, all retail.** `lastUpdatedAt` 2024 is a metadata touch, not a refresh |
| **Oslo** 🇳🇴 | 1 | **97.8%** two-stage | ✅ **13,481 bucket sub-units measured 2026-09-23, names 100% usable after a trim.** 🚨 But **28.6% of parent entities are `ENK` sole traders** against Paris's 8.7%, and the guard needs a JOIN to the parent `enhet` — the sub-unit's own `organisasjonsform` is never `ENK` and would report 0% |
| **Seoul** 🇰🇷 | 1 | Partial | 8 datasets, 197,276 premises — multi-source |

## Cost band 5 — complete, but one bucket: an owner call rather than work (3 cities)

| Cities | Buys | The decision |
|---|---|---|
| **Stockholm** 🇸🇪 · **Zurich** 🇨🇭 · **Göteborg** 🇸🇪 | 1 each | Three measured, licensed, **food-service-only** cities. Cheap to build; the open question is whether a one-bucket city belongs on the site at all. **That is a scope decision, not a task — and it is now ONE decision covering three cities rather than two.** ⚠️ Göteborg's main register `Livsmedelsverksamheter` has **no measured row count**: its DCAT node exposes no `accessURL`. Until it is taken, Stockholm's measured 8,146 premises is the stronger number |

## Cost band 6 — blocked or keyed (5 cities)

| Cities | Buys | Blocker |
|---|---|---|
| **Bucharest** 🇷🇴 ▲▲ | 1 | `data.gov.ro` blackholes on both ports — **still down two days running**, which weakens the original *outage, so retry* reading. OSM fallback re-measured **146,228** addressed objects; rail re-counted at **13 relations, 12 coloured, 64 stations**. ⛔ **Moved to the one-bucket band**: Romania's catalogue has no second bucket |
| **Taipei · Kaohsiung · Taoyuan · Taichung** 🇹🇼 | **4** | **Needs a `data.gov.tw` API key** — gate item 16. High `Buys`, so this is the best-value item in the blocked tier once the key exists |

## Cost band 7 — national geocoding is a project, not a step (12 cities)

| Cities | Buys | |
|---|---|---|
| **São Paulo · Rio de Janeiro** 🇧🇷 | **2** | CNPJ, past Toronto's scale. Write the Brazilian geocoder once, get both |
| **Tokyo · Osaka · Nagoya · Yokohama · Sapporo · Fukuoka · Kyoto · Kobe · Sendai · Hiroshima** 🇯🇵 | **10** | Block-based addressing (chōme/ban/gō), `町字ID` 0% populated. **The hardest met** — and the highest `Buys` on the list, which is the whole reason it stays |

---

## Counts

| Band | Cities |
|---|---|
| 1 — no geocoding leg | 0 |
| 2 — free riders | 4 |
| 3 — a join | 2 |
| 4 — a keyless geocode | 4 |
| 5 — one bucket, owner call | 3 |
| 6 — blocked or keyed | 5 |
| 7 — national geocoding project | 12 |
| **Total** | **30** |

Against `city_master_list.md`'s bands: **A 9 + B 16 + C 5 = 30.**
⚠️ **Bucharest and Singapore both moved to the ONE-BUCKET band on 2026-09-23**
— each has a measured coordinate route and only one bucket, and **where both
are true the ceiling is what is actually stopping the city.** Their COST bands
are unchanged: this file orders by what a build costs, not by what blocks it.

⚠️ **The master list renumbered on 2026-09-23** — the coordinates band
closed by SUCCEEDING (all four members ended up measured and brief-ready) and was
absorbed into **A**, so the old `C` and `D` became **B** and **C**. **Name the
condition, not the letter** — a sentence saying *"moved to the one-bucket band"*
survives a renumber and one saying *"moved to Band D"* does not.
**The two files must always sum to the same number**, and that is the check to
run when either is edited.
