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

**Current state, 2026-09-22 — 32 candidates.** Dublin moved to BUILT this day
and is not counted here.

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

## Cost band 1 — nothing left to discover, and no geocoding leg (2 cities)

| City | Buys | Why it is cheapest | What is actually left |
|---|---|---|---|
| **Paris** 🇫🇷 ▲ | **6** | **99.96% already geolocated** — 148,576 of 148,633. There is no coordinate leg at all, which no other unbuilt city can say | France country facts, NAF taxonomy, OSM rail |
| **Milan** 🇮🇹 ⚠️ | **1** | Three layers = three buckets, coordinates 99.1%, CC-BY, all three schemas captured 2026-09-22 | Italy facts, ATECO taxonomy, OSM rail. **Owner decision open:** ~82% of retail pins carry no trade name |

**Paris and Milan are the same class of work.** Paris wins on the `Buys`
column alone.

## Cost band 2 — free riders on band 1 (4 cities)

| Cities | Buys | Marginal cost |
|---|---|---|
| **Marseille · Toulouse · Lille · Rennes** 🇫🇷 | — | **The same SIRENE, the same Licence Ouverte 2.0, the same filter.** The cheapest builds available anywhere on this list — but **strictly after Paris**, never instead of it. ⚠️ France's OSM rail composition is validated on **Paris only**; the first non-Paris build must re-validate it. ⚠️ **Lyon was REMOVED from this band 2026-09-22** — three gates (an account this project will not create, a trademark clause that collides with the on-map line-label invariant, and the project's second indemnity), so it is no longer a cheap follower. It is not discarded; see Band 6 |

## Cost band 3 — coordinates are a JOIN (2 cities)

| City | Buys | Route | What is left |
|---|---|---|---|
| **Prague** 🇨🇿 | 1 | **99.8%** — a 3.4 MB keyless download and a dict lookup | Czech facts, CZ-NACE taxonomy, rail (Golemio key *or* OSM). ⚠️ EPSG:5513 sign-and-axis flip, verified 2026-09-22 |
| **Copenhagen** 🇩🇰 | 1 | **100%** of 85,351 access addresses carry WGS84 | ⚠️ **Business leg still gated** by the free CVR account. ⚠️ Frederiksberg (0147) is a separate kommune inside Copenhagen — omit it and the map has a hole in its middle |

## Cost band 4 — coordinates are a keyless GEOCODE (4 cities)

| City | Buys | Rate | Cost driver |
|---|---|---|---|
| **Hong Kong** 🇭🇰 ▲▲▲ | 1 | ALS answers, returns a confidence `Score` | **Best rail in the whole screen** — 126 relations, 125 named, 117 coloured. ✅ Indemnity ACCEPTED 2026-09-22 |
| **Singapore** 🇸🇬 ▲▲ | 1 | **98.8%** of answered lookups | Four registers → `multi-source-city`. **7,767 distinct lookups, not 35,064.** Retail narrow by construction |
| **Oslo** 🇳🇴 | 1 | **97.8%** two-stage | ⚠️ Physically-in-Oslo share unmeasured — settle with the bulk download, not the API |
| **Seoul** 🇰🇷 | 1 | Partial | 8 datasets, 197,276 premises — multi-source |

## Cost band 5 — complete, but one bucket: an owner call rather than work (2 cities)

| Cities | Buys | The decision |
|---|---|---|
| **Stockholm** 🇸🇪 · **Zurich** 🇨🇭 | 1 each | Both measured, both licensed, both **food service only**. Cheap to build; the open question is whether a one-bucket city belongs on the site at all. **That is a scope decision, not a task** |

## Cost band 6 — blocked or keyed (6 cities)

| Cities | Buys | Blocker |
|---|---|---|
| **Bucharest** 🇷🇴 ▲▲ | 1 | `data.gov.ro` blackholes on both ports — an **outage, so retry**. OSM fallback measured at 146,116 addressed objects |
| **Lyon** 🇫🇷 | 1 | ⚠️ **Moved here from Band 2 on 2026-09-22.** Data is fine — 19,449 est. bucket rows, 52.5% named, better than Paris. Blocked by **three** gates: a `data.grandlyon.com` account the owner must create, CGU Art. 6.2's bar on the producers' *signes distinctifs* (collides with naming TCL on the map), and CGU 9.4's open-ended indemnity. Its NAP feed is also **dead since 2022-04-14** |
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
| 1 — no geocoding leg | 2 |
| 2 — free riders | 4 |
| 3 — a join | 2 |
| 4 — a keyless geocode | 4 |
| 5 — one bucket, owner call | 2 |
| 6 — blocked or keyed | 6 |
| 7 — national geocoding project | 12 |
| **Total** | **32** |

Against `city_master_list.md`'s bands: A 9 − Dublin = 8, B 6, C 16, D 2 = 32.
**The two files must always sum to the same number**, and that is the check to
run when either is edited.
