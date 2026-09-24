# Rotterdam — build brief

**Step 0 measured 2026-09-24 (two re-probes; Band A by the owner's call, after
two licence reads).** Run `python scripts/brief_check.py rotterdam` before
writing any code. **Read `amsterdam.md` first**: this is the same two-layer
shape, and its build (`pipeline/amsterdam/`) is the template.

---

## The one-line summary

**Amsterdam's shape, with the food layer REBUILT rather than read.** Rotterdam
publishes no hospitality register. Every exploitation-permit decision is
published in its Gemeenteblad, though, with a point. Permits run five years,
so the grants since 2021-09-24 are about the permits in force: **1,937
premises**. The method recovers **97%** of Amsterdam's live register. Shops
and services come from the BAG (**6,170** shop-class units in use), and CBS
discloses the vacancy: **about 7% of shop units registered as vacant**.

---

## Layer 1 — food service, rebuilt from permit notices

| | |
|---|---|
| **Source** | KOOP's official-publications SRU API: `https://repository.overheid.nl/sru`, query `c.product-area==officielepublicaties AND dt.creator=="Rotterdam" AND dt.type=="exploitatievergunning"`. **3,354 notices** of that type; the nonsense creator returns 0. Filters on creator, rubric, title and full text all pass a nonsense control |
| **Harvest** | 6,045 Rotterdam notices since 2021 (all kinds). In the five-year window since 2021-09-24: exploitatie 2,527 · Alcoholwet 919 · **voorlopige (provisional) 832** · terrasvlonder 610 · aanwezigheid (gaming machines) 341 · kortlopende 30 · other 282 |
| **Location** | a point on **99.75%** of premises-kind notices, in RD New (EPSG:28992) and WGS84. No geocoding |
| **Validity** | an exploitation permit runs **5 years**, read in 48 sampled notices from 2017–2026 (e.g. 10-12-2025 to 10-12-2030). Coffeeshops are 1 year, and Alcoholwet permits are indefinite |
| **Premises** | **exploitatie + voorlopige**, points merged within 3 m: **1,937** (1,904 at 5 m, 2,063 exact) |
| **Leave out** | Alcoholwet-only (can be an off-licence, which is retail) · terrasvlonder (the terrace, not the premises) · aanwezigheid (gaming machines, a subset) · kortlopende (events) |

**Validated on Amsterdam**, where a live register exists. The same method on
Amsterdam's 17,598 notices finds **97%** of the register's 4,092 premises
within 10 m, and 88% of what it rebuilds is in the register. So it **recovers
almost everything and overcounts about 1.15×**, because closed premises stay
in until their permit expires, and Rotterdam's titles never mark a
withdrawal.

**Controls**: 1.12× OSM food (1,733), about **0.98×** after the implied surplus
(Amsterdam's register is 0.95×); 76% of OSM's hospitality features have a
permit premises within 25 m (bars 92%, pubs 87%, restaurants 80%, fast food
63%). Against CBS's 4,210 hospitality businesses the ratio is 0.46 (Amsterdam
0.35), so no thinner.

**What it lacks**: names (the points carry no trade name) and sub-categories:
hotels and club canteens stay inside food service.

## Layer 2 — shops and services, the BAG

**BAG verblijfsobjecten with use class `winkelfunctie`, status in use, in
municipality 0599: 6,170** (PDOK WFS; 98.6% shop-only; the same query
reproduces Amsterdam within 1.5%), **2.16× OSM shops**. As in Amsterdam, one
**"Shops and services" category**: a building register cannot tell a
hairdresser from a clothes shop, and personal-service permits are almost
absent from the notices (barbers 1, hairdressers 7, nail studios 2).
**De-duplicate against layer 1 by address**, as Amsterdam does.

## Vacancy — disclosed, from CBS

**CBS Landelijke Monitor Leegstand 2025, Tabel 1: Rotterdam shops 6,200
units, 6,060 in scope, 430 vacant, 7% by count** (6% by floor area),
1 January 2025. It replaces the Locatus figure on `rotterdam.incijfers.nl`,
which is geo-blocked (NL and DE only). **Wording**: "registered as vacant",
since CBS's vacancy is administrative
(「er is niet in de praktijk getoetst…」). CBS's "winkels" are single-use
winkelfunctie units, the same stock as layer 2. ⚠️ Amsterdam keeps its Locatus
4.6% (the owner's choice), and CBS itself publishes Amsterdam as **4%**. The
4.4% in the re-probe was our own calculation from rounded counts, never
CBS's.

---

## ✅ Licences — READ 2026-09-24

- **KOOP official publications — PERMITTED WITH CONDITIONS.**
  - **The grant**: `overheid.nl/help/officiele-bekendmakingen/bestanden-en-hergebruik`:
    "Artikel 11 van de Auteurswet bepaalt dat er geen auteursrecht rust op wetten, besluiten en verordeningen … Dit betekent dat deze informatie vrij mag worden hergebruikt, tenzij dat in de publicatie anders is aangegeven."
    The catalogue declares CC0 1.0, and the Databankenwet art. 8 denies a
    public body a database right in its own decisions.
  - **Conditions, all on the HARVEST**: the API's fair-use policy (its text was
    not found, so keep the rate polite); no reservation inside a notice (none
    in three sampled); and handle privacy-sensitive notices (`/noindex/`
    links) the same way KOOP does. The harvested records keep ids, not links,
    so **check `/noindex/` at build**.
  - **Nothing to display.**
- **CBS — PERMITTED WITH CONDITIONS** (CC BY 4.0, `cbs.nl/nl-nl/over-ons/website/copyright`).
  - **MUST DISPLAY**: CBS as the source, the CC BY 4.0 link, and a note if a
    figure is recalculated. For example: *Source: CBS (Statistics Netherlands),
    Landelijke Monitor Leegstand 2025, table 1, 1 January 2025 — CC BY 4.0.*
  - **MUST NOT**: imply CBS endorses the map or is affiliated with it; use the
    CBS logo.
- **BAG** — Public Domain Mark (Kadaster), as in Amsterdam.
- **OpenStreetMap** (rail and basemap): ODbL, the standing credit.

## 🚇 Rail — RET metro (A–E) and trams, from the national GTFS as in Amsterdam

**Corrected at build (2026-09-24):** this section said "from OSM as in
Amsterdam", and Amsterdam in fact read OVapi's national GTFS
(`gtfs-openov-nl.zip`, CC0), agency GVB. Rotterdam reads the same file, copied
from Amsterdam's cache, agency RET. Built: metro A–E and trams 1–8 and 11,
gemeente only (52 stops outside it; metro E keeps 12 of 23), trams thinned.
**The feed opened on a works timetable** - temporary trams 14 and 18 (to
2026-11-22) while 4, 6 and 8 are shortened - so regular routes are measured
from 2026-11-23; neither of RET's own maps carries a 14 or an 18.

## Scope

**Gemeente Rotterdam (0599) only**, as Amsterdam. The BAG query and the notices
are both municipal.

## Privacy

Points only: no names from either layer. **Notice titles from 2021–2022 carry
trade names**, some possibly sole traders'. Never use titles as labels. Run
`check_personal_exposure.py`. **At build (the re-probe's OPEN-6)**: sample the
permit reference codes in the notice bodies, to see whether coffeeshop or
sex-business permits sit inside the exploitation notices, and decide their
exclusion by the Amsterdam precedent.

## Region

`"region": "Europe"`. Project to **UTM 31N (EPSG:32631)**.

## Build mechanics

- `pipeline/rotterdam/fetch_sources.py` harvests by YEAR: the SRU stops at
  10,000 records per query.
- Merge points within 3 m, keep exploitatie + voorlopige, and apply the
  five-year window from the build date.
- The notice API was unreachable once on 2026-09-24 (a TLS handshake error)
  and answered 200 an hour later: **retry, and a single failure is not a dead
  source**.

## Still unknown

- ⚠️ Rail: lines and the Line E scope.
- ⚠️ Coffeeshop and sex-business permits inside the notices (OPEN-6).
- ⚠️ The fair-use policy's actual limits (`cup@koop.overheid.nl`, untested).

```brief-checks
[
  {
    "id": "rotterdam-permit-notices",
    "claim": "KOOP's SRU API returns Rotterdam's exploitation-permit notices keyless - the source of the rebuilt food layer (3,354 on 2026-09-24)",
    "kind": "http_contains",
    "url": "https://repository.overheid.nl/sru?operation=searchRetrieve&version=2.0&query=c.product-area%3D%3Dofficielepublicaties+AND+dt.creator%3D%3D%22Rotterdam%22+AND+dt.type%3D%3D%22exploitatievergunning%22&maximumRecords=1",
    "present": ["numberOfRecords>", "exploitatievergunning"],
    "absent": ["numberOfRecords>0<"]
  },
  {
    "id": "rotterdam-permit-filter-real",
    "claim": "The SRU creator filter is real - a nonsense creator returns zero notices, so the Rotterdam count is not the whole collection",
    "kind": "http_contains",
    "url": "https://repository.overheid.nl/sru?operation=searchRetrieve&version=2.0&query=c.product-area%3D%3Dofficielepublicaties+AND+dt.creator%3D%3D%22Zzqqxxkw%22+AND+dt.type%3D%3D%22exploitatievergunning%22&maximumRecords=1",
    "present": ["numberOfRecords>0<"]
  },
  {
    "id": "rotterdam-bag-shops",
    "claim": "PDOK's BAG WFS counts Rotterdam's (0599) winkelfunctie units in use server-side - 6,170 on 2026-09-24, the shop layer",
    "kind": "http_contains",
    "url": "https://service.pdok.nl/lv/bag/wfs/v2_0?service=WFS&version=2.0.0&request=GetFeature&typeName=bag%3Averblijfsobject&resultType=hits&FILTER=%3Cfes%3AFilter+xmlns%3Afes%3D%22http%3A%2F%2Fwww.opengis.net%2Ffes%2F2.0%22%3E%3Cfes%3AAnd%3E%3Cfes%3APropertyIsLike+wildCard%3D%22%2A%22+singleChar%3D%22.%22+escapeChar%3D%22%21%22%3E%3Cfes%3AValueReference%3Eidentificatie%3C%2Ffes%3AValueReference%3E%3Cfes%3ALiteral%3E0599%2A%3C%2Ffes%3ALiteral%3E%3C%2Ffes%3APropertyIsLike%3E%3Cfes%3APropertyIsLike+wildCard%3D%22%2A%22+singleChar%3D%22.%22+escapeChar%3D%22%21%22%3E%3Cfes%3AValueReference%3Egebruiksdoel%3C%2Ffes%3AValueReference%3E%3Cfes%3ALiteral%3E%2Awinkelfunctie%2A%3C%2Ffes%3ALiteral%3E%3C%2Ffes%3APropertyIsLike%3E%3Cfes%3APropertyIsEqualTo%3E%3Cfes%3AValueReference%3Estatus%3C%2Ffes%3AValueReference%3E%3Cfes%3ALiteral%3EVerblijfsobject+in+gebruik%3C%2Ffes%3ALiteral%3E%3C%2Ffes%3APropertyIsEqualTo%3E%3C%2Ffes%3AAnd%3E%3C%2Ffes%3AFilter%3E",
    "present": ["numberMatched="],
    "absent": ["numberMatched=\"0\""]
  },
  {
    "id": "rotterdam-koop-reuse",
    "claim": "KOOP's reuse page still says official publications may be reused freely under Auteurswet art. 11 - the notices' licence position",
    "kind": "http_contains",
    "url": "https://www.overheid.nl/help/officiele-bekendmakingen/bestanden-en-hergebruik",
    "present": ["van de Auteurswet bepaalt dat er geen auteursrecht rust", "vrij mag worden hergebruikt"]
  },
  {
    "id": "rotterdam-cbs-licence",
    "claim": "CBS's copyright page still grants CC BY 4.0 with CBS credited - the vacancy figure's licence",
    "kind": "http_contains",
    "url": "https://www.cbs.nl/nl-nl/over-ons/website/copyright",
    "present": ["CC BY 4.0", "CBS als bron"]
  },
  {
    "id": "rotterdam-projected-crs",
    "claim": "Rotterdam projects to UTM 31N",
    "kind": "utm_zone_from_longitude",
    "lon": 4.48,
    "expect": "EPSG:32631"
  }
]
```
