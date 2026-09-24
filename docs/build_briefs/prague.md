# Prague — build brief

**Step 0 measured 2026-09-22/23.** Run `python scripts/brief_check.py prague`
before writing code.

---

> ⏸ **PAUSED 2026-09-24 AT STEP 0 — THE BUSINESS LEG FAILED THE PREMISES
> TEST.** RES records a subject's **registered seat** (*sídlo*), not where it
> trades, and the build measured what that means: the restaurant control reads
> **8.02x** OpenStreetMap (NACE 5610* 20,829 vs `amenity=restaurant` 2,596,
> node+way) against France's 1.26-1.80x on a premises register; **767**
> registrants sit at one address (Rybná 716/24, 668 of them s.r.o. - a virtual
> office), 44 addresses hold 50 or more; and **67.9%** of rows are `FORMA 101`
> sole traders, located at their seat - usually the owner's home - under the
> owner's own name. On RES the map would be accountants' mailboxes and people's
> homes. **Owner's call: pause, and the staging session chases a bulk source
> for RŽP's *provozovny*** (the premises register, which the 2026-09-22 screen
> found only as a per-IČO lookup). Prague resumes only if one exists. Two
> owner calls are ALREADY TAKEN and banked below for that day: **metro A, B, C
> only**, and **Flora drawn, disclosed**. See `DECISIONS.md`.

## The one-line summary

**The cheapest coordinate step in the project — and a taxonomy that cannot be
keyed at a level.** RÚIAN resolves 99.8% of rows to a coordinate by dict
lookup, but CZ-NACE is stored at **ragged depth**: only 57.9% of Prague's rows
reach the finest level and 31.4% stop at the 3-digit group.

---

## Business leg — the Statistical Office's RES

| | |
|---|---|
| File | `https://opendata.czso.cz/data/od_org03/res_data.csv` |
| Size | **543 MB**, 3,528,951 rows nationally |
| Prague filter | `OKRESLAU == "CZ0100"`, active = `DDATZAN` empty |
| Active Prague in NACE 47/56/96 | **≈85,000** (33,149 counted in the first 1.4 M rows) |
| `FIRMA` trade name | **100.0%** |
| Street + house number | **99.9%** |
| `KODADM` (RÚIAN code) | **99.9%** |

**`FIRMA` at 100% is the headline.** Milan's `insegna` is 17.6% and Paris's
premises name 42.9% — **Prague is the only one of the three with a name on
every row.**

⚠️ **CZ-NACE here is SINGLE-VALUED** (*převažující činnost*), unlike ARES's
fifteen-code array. Use RES, not ARES.

---

## Coordinates — a JOIN, 99.8%, the cheapest in the project

**RÚIAN's Praha export: `https://vdp.cuzk.gov.cz/vymenny_format/csv/
20260831_OB_554782_ADR.csv.zip` — 3.4 MB zipped, keyless.**

| | |
|---|---|
| Addresses | **134,627**, every one a unique `Kód ADM` |
| With coordinates | **99.99%** (134,621) |
| Measured join rate | **99.8%** on 6,000 active Prague bucket rows |

The old `vdp.cuzk.cz` host **redirects** rather than dying — unlike `rzp.cz`,
which moved to `rzp.gov.cz`.

### ⚠️ The CRS needs a sign flip AND an axis swap — verified, not reasoned

RÚIAN publishes `Souřadnice X` ≈ 1,042,569 and `Souřadnice Y` ≈ 744,384, both
**positive**. Transforming the first row — Hrad I. nádvoří, Prague Castle —
against its known position:

| Interpretation | Result |
|---|---|
| **`EPSG:5513` with (X, Y) as published** | **50.08948, 14.39861** ✅ |
| **`EPSG:5514` with (−Y, −X)** | **identical** ✅ |
| `EPSG:5514` with (−X, −Y) | 52.27849, 9.47158 — **Germany** |
| `EPSG:5514` with (Y, X) | 68.51016, 41.59194 — **the Arctic** |

**The wrong orderings produce plausible numbers and fail silently**, which is
why this was settled before any pipeline code existed to inherit it.

---

## ⚠️ Taxonomy — CZ-NACE is RAGGED, and no level can be chosen

`premises-taxonomy` assumes a level can be picked — Barcelona keys at its
finest, Madrid near the top. **Prague supports neither**, because the codes are
not all the same depth. Measured on 12,000 active Prague bucket rows:

| Code depth | Rows | Share |
|---|---|---|
| 2 chars — division | 532 | **4.4%** |
| **3 chars — group** | 3,773 | **31.4%** |
| 4 chars — class | 746 | 6.2% |
| **5 chars — national sub-class** | 6,949 | **57.9%** |

**Only 57.9% reach the finest level. Keying at class (4) covers 64.1%** — the
other 35.9% are too short even for that.

`4725` and `47250` both appear. So do `47`, `471` and `47190`. **RES stores
whatever depth the subject declared.**

### So the taxonomy must match on PREFIX, not on a level

Classify at the deepest level a row actually has, falling back up the
hierarchy. A fixed-level key would either discard a third of the city or
collapse it into one bucket.

**And the largest single code is `471` at 30.2%** — *retail sale in
non-specialised stores*, at group level. **Nearly a third of Prague's rows say
only that.** `56100` (restaurants) is another 29.4%, so two codes are 59.6% of
the city.

Catch-all share, for the record: division 25.7%, group 63.7%, class 39.7%.
**All three are worse than Paris's 19.3%**, and the raggedness is why.

---

## Rail — ✅ OSM, and the Golemio key is NOT needed

Measured 2026-09-23 over Prague's bounding box:

| | |
|---|---|
| Relations | **85** |
| Tram | 79 |
| Subway | 6 (Metro A, B, C — both directions) |
| **Named** | **85 / 85 = 100%** |
| Coloured | 61 (72%) |

~~**This settles gate item 4.** `api.golemio.cz` returns 401 and needs a key;
**it is not required** — OSM carries the whole network, fully named. Use
`osm-rail`.~~ **CORRECTED 2026-09-24: use PID's own GTFS, not OSM.** This
section checked only Golemio's keyed API - Madrid's failure in its general
form. osm-rail's order is agency GIS, then GTFS, then OSM, and **PID publishes
a keyless GTFS**: `https://data.pid.cz/PID_GTFS.zip`, 50,040,395 bytes,
`shapes.txt` present, **self-attesting** (`feed_info.txt`: ROPID, 2026-09-23 to
2026-10-06 - a two-week window, refetch not alarm). Route types: metro `1` x3,
tram `0` x37, funicular `7` x1 (Petřín), ferry `4` x5, trolleybus `11` x6, rail
`2` x96, bus `3` x741. The metro carries its official livery: **A `#00A562`,
B `#F8B322`, C `#CF003D`**.

**Metro per line, measured 2026-09-24:** A **16**, B **24**, C **20** station
names in PID's feed; OSM's route relations (`network=Pražské metro`, six, one
per line per direction) give 16 / 24 / 20 - **gate 3 exact**. **All 60 are
inside obec 554782** (ČÚZK INSPIRE AU polygon, 496.2 km²), so commune scope
costs the metro nothing - Paris's and Marseille's shape.

**Line A is 17 stations, not 16: Flora is CLOSED FOR RECONSTRUCTION.** Its
metro platforms (`U118Z101P`/`Z102P`, parent `U118S1`) are in `stops.txt`, but
no metro trip calls - line A runs Želivského > Jiřího z Poděbrad directly. DPP's
own press release (23. 01. 2026): closed *"po ukončení provozu metra v neděli
1. února 2026"*, *"na zhruba deset měsíců"*, reopening *"na přelomu listopadu a
prosince 2026"*. OSM's relations omit it too.

**✅ OWNER CALLS TAKEN 2026-09-24, before the pause:**
- **Draw metro A, B, C only.** Prague's trams are a dense overlay on the metro
  across the whole centre, not a separate corridor (Toulouse's T1, Marseille's
  trams); the Petřín funicular, ferries and S-trains go on the standing rules,
  as in Paris.
- **Draw Flora, disclosed.** Located from PID's own `stops.txt`, with a page
  note that it is closed for reconstruction until about December 2026, and a
  step-1 assertion that STOPS the build once the feed serves Flora again, so
  the override cannot outlive the closure.

**✅ PID's licence READ 2026-09-24: CC BY 4.0, PERMITTED WITH CONDITIONS.**
`pid.cz/o-systemu/opendata/`: *"Data, která lze stáhnout přímo zde z webu, jsou
... opatřena licencí CC-BY, tedy je lze dále šířit, avšak je nutné uvést autora
a případné provedené změny."* The national catalogue's record for this exact
download URL names the same terms. **MUST DISPLAY**: author **ROPID**, a notice
of modification (a third transformation disclosure for this city, after ČSÚ
and ČÚZK), the CC BY 4.0 link and `pid.cz/o-systemu/opendata/` - **on the
committed station CSV too**. **MUST NOT**: the PID/ROPID/IDSK logos
(*"je nutný vždy souhlas organizace ROPID"*), or any implied endorsement. Line
letters and colours are not claimed. **MUST DO: nothing** - `opendata@pid.cz`'s
*"napište nám prosím"* is an invitation, not a condition.

⚠️ 24 relations carry no `colour`. Every drawn line needs a legend entry and an
on-map label regardless, so assign colours for those rather than dropping them.

---

## ✅ Licence — BOTH READ 2026-09-23, both CC BY 4.0

**Nothing licence-shaped blocks this city any more.** Both are PERMITTED WITH CONDITIONS, and between them they impose **five display obligations**.

- ✅ **RES / ČSÚ — READ 2026-09-23. CC BY 4.0, PERMITTED WITH CONDITIONS.**
  The national catalogue's DCAT record resolves a `podmínky-užití`
  distribution per dataset, and ČSÚ's own terms page carries the operative
  text. ⚠️ **Read the DATA paragraph, not the website one** — the CC BY
  sentence is about `csu.gov.cz` *web pages*; the data conditions follow it
  under *"Další podmínky použití dat ČSÚ"*, and impose **two obligations
  this build triggers**:
  - **MUST DISPLAY** — *"v případě šíření dat ČSÚ vzniká povinnost uvést
    podmínky této licence, nejlépe přímým odkazem na tuto webovou stránku"* —
    state the licence conditions, preferably as a direct link to that page.
  - **MUST DISCLOSE, and MUST NOT SAY** — *"upravené nebo odvozené údaje musí
    být označeny jako upravené nebo odvozené a nesmí být prezentovány jako
    nezměněné oficiální statistiky Českého statistického úřadu"* — modified or
    derived data must be **marked as such** and must **not** be presented as
    unchanged official ČSÚ statistics. **This project's ring density, bucketing
    and storefront filtering are all transformations**, so this fires every
    time — the Montréal and INEGI family.
- ✅ **RÚIAN / ČÚZK — READ 2026-09-23. CC BY 4.0, PERMITTED WITH
  CONDITIONS.** The document exists and **five earlier attempts searched the
  wrong subtree**: it lives under **`/Predpisy/`** (Regulations), not under
  `/Uvod/Produkty-a-sluzby/` or the geoportal —
  `www.cuzk.gov.cz/Predpisy/Podminky-poskytovani-prostor-dat-a-sitovych-sluzeb/Podminky-poskytovani-prostorovych-dat-CUZK.aspx`,
  updated **30.06.2023**, reached by one link from the cuzk.gov.cz homepage.

  > „ČÚZK poskytuje prostorová data spadající do kategorie otevřených dat
  > (včetně metadat) **bezúplatně na základě licence Creative Commons
  > CC-BY 4.0**."

  Its **first enumerated bullet names this exact resource** — *"data vedená v
  RÚIAN formou výměnného formátu RÚIAN"*. The grant lists `vytěžovat`,
  `užívat komerčně i nekomerčně`, `kombinovat`, `kopírovat, distribuovat,
  šířit`, `transformovat a upravovat`. **Two independent machine records
  agree** — `data.gov.cz`'s SPARQL and ČÚZK's **own** DCAT-AP record at
  `atom.cuzk.cz` — CC BY 4.0 on all three rights axes.

### ⚠️ MUST DISPLAY — three, and Prague now needs TWO transformation notices

1. **Prescribed wording**: *"uvedení zdroje ve formátu:* **`ČÚZK, [rok]`**
   *"* — the year being the data file's currency. For the 2026-08-31 file:
   **`ČÚZK, 2026`**.
   ⚠️ **The English page prescribes a DIFFERENT string** (*"ČÚZK ‹month
   year›"*) and is **version 1.0 dated 2016**, against the Czech version's
   2023 — and it never mentions CC BY. **Unreconciled.** Use the Czech form and
   state the file date, which serves the clause's own stated purpose under
   either reading.
2. **A link to the conditions page** above.
3. **A description of the modification** — *"v případě šíření upraveného
   díla, uvést popis úpravy"*. Projecting S-JTSK, joining to RES and filtering
   to storefronts are all *úprava*. **This is the Montréal/INEGI family, and
   ČSÚ requires its own version independently** — so **Prague carries two
   transformation disclosures**, which may share one sentence only if it names
   both publishers.

**MUST DO: nothing.** No notification, registration, statistics duty or
permission request — checked against the whole phrase family. This is not a
Barcelona.

**MUST NOT SAY**: no endorsement or affiliation (CC BY §2(b)(5)), and no
accuracy claim — the English version adds that ČÚZK is not liable for damages
from *"improper or unprofessional interpretation of this data"*, and a
ring-density map is an interpretation.

### ⚠️ RAISED, NOT RESOLVED — and it changes the FETCH, not the publication

The link this brief previously dismissed as *"Podmínky užívání aplikace a
cookies"* **is not only cookie terms.** Its real text, at
`vdp.cuzk.gov.cz/help/topics/cookies.htm` (the `?id=` URL returns a 2,338-byte
HelpSmith frameset, which is why it read as a bare cookie notice), says:

> „Aplikace je určena pro interaktivní práci uživatelů … **Není povoleno
> jakékoli vytěžování údajů automatizovanými prostředky.**"

*Any extraction of data by automated means is not permitted* — and it binds
every user. **Two ČÚZK documents use `vytěžovat` in opposite directions**: the
spatial-data conditions grant it, the application terms forbid it. **Nothing
reconciles them, and this is not resolved in the project's favour.**

**But it is about HOW THE FILE IS FETCHED, not what may be published** — the
reuse verdict holds either way. **Step out of it rather than argue it**: take
the URL from ČÚZK's **INSPIRE ATOM download service**, which its own
documentation calls *"určeno především pro strojové zpracování"* — intended
primarily for machine processing — and which hands out **precisely these
URLs**:

```
https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_554782
```

It returns one entry: the Praha file, **3,395,881 bytes**, tagged
**`EPSG/0/5513`** — which independently corroborates this brief's CRS finding.
**It also fixes the hard-coded `20260831`, which goes stale on the 1st of
every month.**

⚠️ A **third** rights statement exists and is deliberately NOT taken: the
ATOM feed carries `<rights>žádné podmínky neplatí</rights>` — *no conditions
apply* — which is more permissive than CC BY 4.0 and would be the convenient
quote. It is standard INSPIRE boilerplate and conflicts with two first-party
documents. **The conservative reading governs: conditions apply.**

### Privacy — the publisher already did this work

ČÚZK declares `osobní-údaje = neobsahuje-osobní-údaje` on both its own record
and the national catalogue's — **contains no personal data**, consistent with
the field list. **RÚIAN contributes nothing to Prague's personal-exposure
surface**; whatever `check_personal_exposure.py` finds will come from RES
trade names.

---

## Region

`"region": "Europe"` — per `docs/scaling_thresholds.md`.

---

## Still unknown — the honest list

- ~~ČÚZK / RÚIAN's licence~~ — ✅ **read 2026-09-23, CC BY 4.0.** What replaces it as open: **whether the VDP application's ban on automated extraction reaches the static file URLs.** Sidestep it via the ATOM service rather than deciding it.
- **The prefix-matching taxonomy has no precedent in this project** — four
  cities needed a local taxonomy and all four had uniform depth.
- ~~**Scope** — Prague's `OKRESLAU CZ0100` is the whole city (all 22 městské
  části). Whether the tram network's reach justifies a wider scope is unasked.~~
  ✅ **Settled 2026-09-24**: metro only (owner), and all 60 metro station-line
  pairs are inside obec 554782, so the city scope costs nothing.
- 🚨 **THE BLOCKER: a bulk source for RŽP's *provozovny*** - establishment
  records with a location address and an activity. RES is a seat register
  (see the note at the top); nothing else on this list matters until this
  is answered.
- **The employee filter.** `KATPO` is an employee-count band and 46,447 of
  85,022 are `000`; applying it would leave **38,575**. Whether to apply it is
  an owner call, unresolved. ⚠️ **The Paris precedent this used to
  cite is VOID** — it read *"Paris's equivalent took 148,633 to 50,156"*,
  and the Paris build disproved that on 2026-09-23: **no employee filter is
  applied in France at all**, and 50,156 is not reachable from the column it
  was attributed to. **Prague's question stands on its own evidence**, which is
  actually stronger than France's was: `KATPO` is `000` on **54.6%** of rows
  against France's `NN` at 77.3%, so the Czech column genuinely discriminates
  where the French one does not. 🚨 **But check what `000` MEANS here
  before applying it** — in SIRENE the equivalent band turned out to hold
  every sole trader, and an owner-run shop is exactly what this map is for.
  ✅ **CHECKED 2026-09-24 - and the filter is WRONG.** ČSÚ's own codebook
  (číselník 579, `KATPOECD`) reads **`000` = *Neuvedeno*, NOT STATED**; "no
  employees" is a different code, `110` *Bez zaměstnanců* (29.8% of rows). And
  `000` does not discriminate: its legal-form mix is 68.3% sole traders against
  67.9% for the whole set. **So "the Czech column genuinely discriminates"
  above is false** - it is France's `NN` again, and filtering on it would drop
  54.6% of the city at random. Recommend: no employee filter.
- **`EXPDATE`-style currency** — RES has no per-row validity window; the file
  is dated 2026-09-17 as a whole.

```brief-checks
[
  {
    "id": "czso-res-downloads",
    "claim": "The Statistical Office's RES file downloads with no key. 543 MB, 3,528,951 rows nationally. This is the business leg - use RES, not ARES, because CZ-NACE here is single-valued",
    "kind": "http_ok",
    "url": "https://opendata.czso.cz/data/od_org03/res_data.csv",
    "min_bytes": 1000000
  },
  {
    "id": "ruian-praha-addresses",
    "claim": "RUIAN's Praha address export is 3.4 MB zipped and keyless - 134,627 addresses, every one a unique Kod ADM, 99.99% with coordinates. This is what makes Prague's coordinate step a JOIN rather than a geocode, measured at 99.8%",
    "kind": "http_ok",
    "url": "https://vdp.cuzk.gov.cz/vymenny_format/csv/20260831_OB_554782_ADR.csv.zip",
    "min_bytes": 3000000
  },
  {
    "id": "cuzk-atom-download-service",
    "claim": "CUZK's INSPIRE ATOM service resolves the Praha file and is the channel its own documentation calls 'intended primarily for machine processing'. USE THIS, not a hard-coded vymenny_format path: it sidesteps the VDP application's ban on automated extraction without anyone having to decide whether that ban reaches static files, AND it fixes the hard-coded 20260831 date, which goes stale on the 1st of every month",
    "kind": "http_ok",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_554782",
    "min_bytes": 300
  },
  {
    "id": "cuzk-spatial-data-conditions-live",
    "claim": "CUZK's spatial-data conditions page is live. It lives under /Predpisy/ - five earlier attempts searched /Uvod/Produkty-a-sluzby/ and the geoportal and found only application and cookie terms. There is no PDF or versioned artefact, so a change here is SILENT; the page's 'Datum posledni aktualizace: 30.06.2023' is the drift signal",
    "kind": "http_contains",
    "url": "https://www.cuzk.gov.cz/Predpisy/Podminky-poskytovani-prostor-dat-a-sitovych-sluzeb/Podminky-poskytovani-prostorovych-dat-CUZK.aspx",
    "present": [
      "CC-BY 4.0"
    ]
  },
  {
    "id": "cuzk-old-host-redirects",
    "claim": "The old vdp.cuzk.cz host REDIRECTS rather than dying, unlike rzp.cz which moved to rzp.gov.cz. Pinned so a future 404 is recognised as a move rather than a removal",
    "kind": "http_ok",
    "url": "https://vdp.cuzk.cz/vymenny_format/csv/20260831_OB_554782_ADR.csv.zip",
    "min_bytes": 3000000
  },
  {
    "id": "pid-gtfs-downloads",
    "claim": "PID's own GTFS downloads with no key, ~50 MB - the rail source, ahead of OSM by osm-rail's order. The brief first checked only Golemio's keyed API",
    "kind": "http_ok",
    "url": "https://data.pid.cz/PID_GTFS.zip",
    "min_bytes": 30000000
  },
  {
    "id": "pid-gtfs-complete",
    "claim": "PID's feed carries shapes.txt so the metro can be drawn from first-party geometry, and feed_info.txt so staleness is checkable from the artifact",
    "kind": "gtfs_files",
    "url": "https://data.pid.cz/PID_GTFS.zip",
    "present": [
      "routes.txt",
      "trips.txt",
      "stops.txt",
      "stop_times.txt",
      "shapes.txt",
      "feed_info.txt"
    ],
    "absent": []
  },
  {
    "id": "pid-gtfs-is-current",
    "claim": "PID's feed self-attests a two-week window (2026-09-23 to 2026-10-06 when measured). A stale result means refetch, not alarm",
    "kind": "gtfs_feed_window",
    "url": "https://data.pid.cz/PID_GTFS.zip",
    "expect": "current"
  },
  {
    "id": "pid-licence-cc-by",
    "claim": "PID's open-data page licenses its downloadable data CC BY and requires naming the author AND any changes made",
    "kind": "http_contains",
    "url": "https://pid.cz/o-systemu/opendata/",
    "present": [
      "CC-BY",
      "případné provedené změny"
    ]
  },
  {
    "id": "czso-katpo-000-is-not-stated",
    "claim": "ČSÚ's codebook 579 defines KATPO 000 as 'Neuvedeno' (not stated), distinct from 110 'Bez zaměstnanců' - so an employee filter on 000 drops unrecorded sizes, not premises-less subjects",
    "kind": "http_contains",
    "url": "https://apl.czso.cz/iSMS/do_cis_export?kodcis=579&typdat=0&cisjaz=203&format=2&separator=%2C",
    "present": [
      "\"000\",\"Neuvedeno\"",
      "\"110\",\"Bez zaměstnanců\""
    ]
  }
]
```
