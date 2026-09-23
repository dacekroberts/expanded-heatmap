# Stockholm — build brief

**Screening closed 2026-09-22; rail counted 2026-09-23.** Run
`python scripts/brief_check.py stockholm` before writing any code.

⚠️ **One-bucket city.** It shares a single owner decision with **Zurich** and
**Göteborg** — *does a food-density page belong in a project whose other
cities carry three buckets?* **Answer it once and three cities move.**

---

## The one-line summary

**The largest of the three one-bucket cities, with a real metro — and the only
one whose licence had to be argued rather than read off a field.**

---

## Business leg — a public ArcGIS FeatureServer

| | |
|---|---|
| **Distinct premises** | **8,146** |
| Derived from | **289,742 inspection rows** — ⚠️ **the register is INSPECTIONS, not premises** |
| Trade names | **100%** |
| Addresses | **96.9%** |
| Coordinates | **WGS84 points** |
| Refresh | **daily**, from Ecos 2 |
| Publisher | **Stockholms stad, miljöförvaltningen** |

🚨 **8,146 is a DISTILLED figure, not a row count.** The source serves
**289,742 inspection records**; the premises are what remains after
de-duplication. **Göteborg's equivalent register needs no dedupe at all**
(*"Alla aktiva livsmedelsverksamheter"* — active businesses, not inspections),
which is the single biggest structural difference between the two Swedish
cities.

⚠️ **The dedupe key has not been decided.** Trade name is 100% and address is
96.9%, so a name+address key would drop ~3% — but whether the same premises
appears under varying name spellings across years is unmeasured.

### ⚠️ Its own catalogue confirms there is no second bucket

Stockholms stad publishes **291 datasets** and **exactly one** commercial
register. Inside its own catalogue, `restaurang` and `företag` both return
**0**, and **Sweden has no general business licence**. **The absence is
measured, not unexplored.**

---

## ✅ Licence — SILENT, and it took step 5 to get there

**Resolved 2026-09-22**, and the reasoning matters more than the verdict:

| Source | Says |
|---|---|
| `dataportal.se` | `Åtkomsträttigheter: **Begränsad**` (restricted) |
| The ArcGIS item | `access: public`, serves without credentials, `licenseInfo` **empty** |
| **The publisher's OWN Hub DCAT feed** | ✅ **`accessLevel: public` on all 109 datasets**, `license` **CC0 on 8** |

🚨 **`dataportal.se` is a HARVESTER, not the publisher** — `read-licence`
step 5. **A contradiction between a catalogue and a publisher is decided in
favour of the publisher**, and the publisher says public.

💡 **And the blank licence field is meaningful precisely BECAUSE 8 of 109
carry CC0.** A missing licence can mean *"no mechanism"* or *"declined to
license"* — here **the mechanism is demonstrably in use**, which is what makes
the blank a silence rather than a refusal.

**Verdict: SILENT, with the pages named.** Weaker than Göteborg's and
Zurich's **CC0**, and established rather than assumed.

---

## ✅ Rail — a real metro, and this project's own figure was wrong

Counted 2026-09-23 inside **Stockholms kommun**, OSM relation **398021**:

| Mode | Relations | Named | Coloured | Refs |
|---|---|---|---|---|
| **`subway`** | **15** | **15** | **15** | **8** — 10·11·13·14·17·18·19 + one unref'd |
| `tram` | 6 | 6 | ⚠️ **4** | 4 — 12 · 7 · 7N · ? |
| `light_rail` | 6 | 6 | 6 | 3 — 21 · 30 · 31 |
| **Rail station nodes** | **92** | | | |

🚨 **This project carried *"metro 7, tram 21"*. The tram figure was wrong by
more than 3×.** It came from the same screen that gave Copenhagen a tram it
does not have.

⚠️ **One subway relation and one tram relation carry NO `ref`.** A `ref`-keyed
build drops them silently; a count-keyed build draws a line it cannot label.
**Fourth city in one day with this** — see Bucharest, Singapore, Seoul.

⚠️ **Two of six tram relations have no `colour`**, so a partial palette must
be invented if trams are drawn.

### 🚨 Resolving the boundary is a trap

`["name"="Stockholm"]["admin_level"="7"]` matches **NOTHING** — the Swedish
municipality is **`Stockholms kommun`**. Widening the search returns **nine**
candidates including **two US "Stockholm Township" relations at the same
admin_level 7**. **A looser selector picks one of those and reports a real,
wrong, confidently-zero rail network.**

**Use relation 398021.**

---

## Region

`"region": "Europe"`.

## Still unknown

- 🚨 **The dedupe key** — 8,146 from 289,742 is distilled, and how is undecided.
- ⚠️ **The one-bucket owner decision** — shared with Zurich and Göteborg.
- ⚠️ **Stop spacing**, if trams are drawn — the test's control failed on
  2026-09-23 and it is unmeasured for all three cities.
- ⚠️ **What the unref'd subway relation is.**
- ⚠️ **Non-storefront share** — Göteborg's equivalent register was **26.5%**
  schools, wholesalers and head offices. Stockholm's is unmeasured, and an
  inspection register has every reason to carry the same.

```brief-checks
[
  {
    "id": "stockholm-publisher-feed-says-public",
    "claim": "THE LICENCE POSITION RESTS ON THIS FEED. dataportal.se says Begransad (restricted) but is a HARVESTER; the miljoforvaltning's own Hub DCAT feed declares accessLevel public across its datasets, with CC0 on 8 of 109. read-licence step 5 decides a contradiction in favour of the publisher. If this feed changes, the SILENT verdict must be re-argued",
    "kind": "http_contains",
    "url": "https://open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json",
    "present": ["accessLevel"]
  },
  {
    "id": "stockholm-osm-boundary-is-stockholms-kommun",
    "claim": "OSM relation 398021 is Stockholms kommun, the area the rail was counted in. Pinned because name=Stockholm at admin_level 7 matches NOTHING - the kommun is 'Stockholms kommun' - and widening the search returns two US 'Stockholm Township' relations at the same admin_level, either of which would report a confidently wrong rail network",
    "kind": "http_ok",
    "url": "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A60%5D%3Brel(398021)%3Bout%20ids%3B",
    "min_bytes": 100
  }
]
```
