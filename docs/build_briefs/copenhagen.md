# Copenhagen — build brief

**Step 0 measured 2026-09-23, from the real files rather than from metadata.**
The four CVR downloads are on disk at `data/copenhagen/raw/` (2.00 GB,
gitignored). Run `python scripts/brief_check.py copenhagen` before writing any
code for this city.

---

## The one-line summary

**The best-named register in this project — 100.0% — and the only city whose
business data arrives as FOUR files that must be joined before it is a table
at all.** `Produktionsenhed` on its own carries a `pNummer` and nothing else
useful: the address, the activity and the name each live in a separate
national file, joined on `CVREnhedsId`.

---

## Business leg — CVR via Datafordeler, MEASURED

| | |
|---|---|
| Source | **Datafordeler** `GetFile?Register=CVR&LatestTotalForEntity=<E>&type=current&format=CSV` |
| Files | **4**, national, 2.00 GB total — no per-municipality split (`Kommuneopdelte fildownload: Nej`) |
| Encoding / delimiter | **UTF-8, comma** — verified, not assumed |
| København filter | `CVRAdresse_kommunekode` = **`101`** |
| **Storefront rows** | ✅ **14,887** |
| **Named** | ✅ **100.0%** |
| Active production units, national | 958,606 of 958,843 |

### The four files and what each one is for

| Entity | Size | Carries | Why it is needed |
|---|---|---|---|
| `Produktionsenhed` | 212 MB | `id`, `pNummer`, `produktionsenhedOphoersdato` | **The spine** — which `CVREnhedsId`s are premises, and which are still open |
| `Adressering` | 836 MB | `CVRAdresse_*`, **`Adresse`** (a DAR UUID) | **Location** |
| `Branche` | 442 MB | `sekvens`, **`vaerdi`** + **`vaerdiTekst`** | **Activity — the code AND its label, in one file** |
| `Navn` | 556 MB | `vaerdi` | Trade name |

### 🚨 The join key is `CVREnhedsId`, and `Produktionsenhed` calls it `id`

**Verified, not assumed**: of Copenhagen's 330,246 current
`beliggenhedsadresse` rows, **133,530 (40.4%) appear as a `Produktionsenhed.id`**
— a real overlap, so the two are the same identifier space. The rest are
`Virksomhed` rows, which is expected.

⚠️ **`pNummer` is NOT the join key.** It is the production unit's own business
key and appears in no other file. Joining on it would fail *partially and
silently* — the shape of the Oslo `kommunenummer` trap.

### The filter, in order

```
Produktionsenhed :  produktionsenhedOphoersdato IS EMPTY          -> active
Adressering      :  AdresseringAnvendelse = "beliggenhedsadresse"
                    CVRAdresse_kommunekode = "101"
                    virkningTil IS EMPTY                          -> current
Branche          :  sekvens = "0"                                 -> hovedbranche
                    virkningTil IS EMPTY
                    vaerdi[:2] IN (47, 56, 96)
```

✅ **`beliggenhedsadresse` is a first-class value, not a guess** — 2,800,921
rows against **928** `postadresse`. **This is the same location-vs-registered-
office distinction that made Norway pass**, and Denmark makes it explicitly.

⚠️ **`sekvens` matters.** A unit may carry up to four branches; without
`sekvens = 0` every multi-branche premises is counted more than once.

⚠️ **`virkningTil` matters even in a `current` download.** CVR never
de-registers superseded rows — it only inserts new ones — so several rows per
entity are normal. **This is Prague's `DDATZAN` again.**

### The buckets

| | Rows | Share |
|---|---|---|
| **47 — retail** | **6,689** | 44.9% |
| **56 — food service** | **5,163** | 34.7% |
| **96 — personal services** | **3,035** | 20.4% |
| **Total** | **14,887** | |

**Between Toulouse (12,853) and Marseille (25,430) in size, and ahead of every
French city on naming by 46 points.**

---

## Coordinates — a JOIN, not a geocode

**`Adressering.Adresse` is a DAR address UUID**, present on **96.9%** of
Copenhagen rows. It joins to Denmark's address register (DAWA,
`api.dataforsyningen.dk`), which is **keyless** and serves all **85,351**
Copenhagen access addresses with **100%** WGS84 coordinates.

**So there is no geocoder, no rate limit and no key on the coordinate leg** —
the same shape as Paris, and the reason Copenhagen was in the coordinates band
at all.

---

## Taxonomy — DB07, and ONE of the two measurements is valid

**DB07 codes are SIX digits** (`561110`, `962100`), not NACE's four. A taxonomy
keyed at NACE class depth would be two levels too shallow — **Oslo's SN2007
problem, same family.**

### ✅ The catch-all share at full depth: **23.4%**

| Code | Rows | Share | |
|---|---|---|---|
| `561110` | 2,574 | 17.3% | Servering af mad i restauranter og caféer |
| `962100` | 1,107 | 7.4% | Drift af frisør- og barbersaloner |
| `477110` | 1,010 | 6.8% | Detailhandel med tøj |
| `962200` | 849 | 5.7% | Skønhedspleje og anden skønhedsbehandling |
| `563020` | 719 | 4.8% | Udskænkning af alkoholiske drikkevarer |
| `477800` | 618 | 4.2% | Detailhandel med **andre** nye varer |
| `969900` | 542 | 3.6% | **Andre** personlige serviceydelser **i.a.n.** |

**66 distinct codes.** ✅ **0% unlabelled** — `vaerdiTekst` ships inside
`Branche`, so no external code list is needed. **That is what Oslo's taxonomy
cost (SSB's 1,785 SN2007 codes) and what Hong Kong got for free.**

### 🚨 The LEVEL comparison was attempted and is NOT a valid measurement

`premises-taxonomy` asks for the catch-all share **at each level**, and the
honest answer is that **I could not produce one.** A first pass reported
division 20.4% / gruppe 19.6% / klasse 18.3% / full 23.4%, **and those three
shallower figures should not be used.**

**Why they are wrong:** the only labels in the file are the **6-digit** ones.
Truncating a code to 4 digits and then judging it by a 6-digit sibling's label
is order-dependent — whichever row happened to be seen first decides whether
the whole truncated group counts as a catch-all. **It is a statement about
row order, not about the scheme.**

**To do it properly, DB07's own hierarchy labels are needed** (Danmarks
Statistik publishes them per level). **Until then the only defensible number
is 23.4% at full depth**, and keying at full depth is the safe default because
it is the only level whose labels are in hand.

---

## 🚨 Privacy — the sole-trader marker is `v/`

| | Rows | Share |
|---|---|---|
| Name containing **` v/ `** — *ved*, "by" | **1,077** | **7.2%** |
| Carrying a **`coNavn`** (c/o) | **3,878** | **26.0%** |
| Carrying a company form (`ApS`, `A/S`, `I/S`…) | 5,984 | 40.2% |

**`v/` is Denmark's sole-trader marker** and the names after it are people:
`FISKEFORRETNINGEN V/LARS JOOST OLSEN`, `Restaurant Fridas v/Lene Palmberg`.

⚠️ **7.2% is a FLOOR, not the rate.** A sole trader may register under a bare
personal name with no marker at all — the `Navn` file's own sample includes
`John Kongerslev` — so the true share is higher and **unmeasured**. France is
**8.7%** and Oslo **28.6%**; Copenhagen's floor sits below both.

⚠️ **`coNavn` is a separate exposure at 26.0%** and is not in the trade-name
field at all. **It must not reach an output**, and nothing about the project's
existing checks would notice it, because no other city has this column.

**`check_personal_exposure.py` needs a Danish-aware pass before Copenhagen
ships** — the same standing item Seoul has for Korean.

---

## Rail — 4 metro lines, and the master list's figure was wrong

Counted in OSM 2026-09-23 inside Københavns Kommune (relation 2192363):

| Mode | OSM | Draw? |
|---|---|---|
| **Metro** `route=subway` | **8 relations, refs M1–M4, ALL named, ALL coloured** | ✅ **Yes** |
| **S-tog** `route=light_rail` | 16 relations, refs A · B · Bx · C · E · F · H, all named and coloured | ⛔ **No — S-Bahn family** |
| Regional / InterCity `route=train` | 28 relations, **0 coloured** | ⛔ No |
| **Tram** | **0** | — |

⚠️ **`docs/city_master_list.md` carried "subway 4, tram 4". The tram count is
WRONG — Copenhagen has no tram.** The system closed in 1972 and the
Hovedstadens Letbane is not open. **An inherited, unverified count**, which is
the class of error that gave Dublin four wrong claims in one row.

✅ **M1–M4 all carry a distinct `colour`**, so the legend is satisfiable from
OSM alone — unlike Oslo, where every metro line shares one colour.

### ⚠️ OWNER CALL — excluding S-tog leaves a thin network

The standing rule excludes commuter rail in every built city, and
`add-country` names **the S-Bahn family explicitly**. S-tog is that. But
applying it leaves Copenhagen with **four metro lines** against a city whose
actual backbone is the S-tog — a larger consequence than the same rule had in
Boston, Chicago or Madrid, where the metro was already the dominant network.
**Recorded as a call rather than silently applied.**

---

## Licence — CC BY 4.0, and only the personal-data entity is gated

**Read 2026-09-23** at `datafordeler.dk/vejledning/brugervilkaar/det-centrale-virksomhedsregister-cvr/`:

> *"Som bruger kan du i henhold til licensen **frit hente, dele og tilpasse**
> frie grunddata. Du skal **kreditere Det Centrale Virksomhedsregister (CVR)**
> på et passende sted."*

**MUST DISPLAY:** credit to **Det Centrale Virksomhedsregister (CVR)**.
Same licence as Madrid and Milan — it adds a notice and nothing else.

✅ **No access request was needed**, and the reason is worth keeping:

> *"Du skal **kun** søge om adgang til CVR, hvis du skal have adgang til
> entiteten **CVRPerson**. De øvrige entiteter hos CVR er **ikke
> adgangsbegrænsede**."*

**The gated entity is the personal-data one, which this project does not
want** — so the restriction runs *with* the privacy invariant rather than
against it.

⚠️ **Access is an owner-held API key** (gated-access item 3). Free, e-mail
account, no MitID needed because e-mail users reach exactly the unprotected
data this build uses. **The key travels in the URL**, so `fetch_sources.py`
must read it from the environment and never echo a built URL.

🚨 **Weekly generation, 7-day retention** — *"Genereringstid: natten til
lørdag… Arkiveringstid: 7 dage."* **A committed snapshot expires before it is
eight days old.** `fetch_sources.py` must record the download date and treat an
expired copy as an **error, not a warning** — WMATA's ten-day window taught
this, and a stale feed still parses and still builds a map.

### ⚠️ The 401 diagnostic, recorded here because no check kind can hold it

**Every `FileDownloads` path returns 401 unauthenticated and NONE returns
404.** So **a 401 with a key attached is always the credential, never the
URL** — which is worth knowing before anyone starts editing parameters.

**And a NEWLY CREATED key 401s identically for about 15 minutes**
(`DAF-AUTH-0005`: *"At least 15 minutes have passed since creation"*). The
obvious response makes it worse — deleting the key and making another
**restarts the 15 minutes** and reproduces the same 401, which then reads as
confirmation that the key was wrong. **Wait, then retry the same key.**

*This is prose rather than a `brief-checks` entry because there is no check
kind for "expect this exact status", and inventing one is not an option: the
kinds are a fixed set and a brief that names a kind outside it simply fails.
That mistake was made twice in one day here — first as `http_status_in`, then
as `http_status_expected`.*

---

## ⚠️ Scope — Frederiksberg is a hole in the middle

**Frederiksberg (kommunekode `0147`) is a separate kommune entirely surrounded
by Copenhagen.** Scoping to `101` alone puts a hole in the centre of the map.
Its addresses come from the same national files at no extra cost — it is a
one-value change to the filter, not a new source. **Owner call.**

---

## Region

`"region": "Europe"`.

---

## Still unknown

- 🚨 **The true sole-trader share.** `v/` gives a floor of 7.2%; bare personal
  names are not counted.
- 🚨 **The taxonomy LEVEL choice** — needs DB07's own hierarchy labels from
  Danmarks Statistik. 23.4% at full depth is the only valid figure today.
- ⚠️ **Frederiksberg** — in or out.
- ⚠️ **S-tog** — the exclusion is the standing rule; the consequence is larger
  here than anywhere it has been applied.
- **Exact DAWA join rate** — 96.9% carry a UUID; the share that *resolves* is
  untested.

```brief-checks
[
  {
    "id": "cvr-licence-is-cc-by-4",
    "claim": "CVR's own terms page on Datafordeler states CC BY 4.0 with attribution to Det Centrale Virksomhedsregister. This is the whole licence position, and it is NOT read at datacvr.virk.dk, which serves a Cloudflare interactive challenge - the obstacle there was the host, not the document",
    "kind": "http_contains",
    "url": "https://datafordeler.dk/vejledning/brugervilkaar/det-centrale-virksomhedsregister-cvr/",
    "contains": "CC BY 4.0"
  },
  {
    "id": "only-cvrperson-is-access-restricted",
    "claim": "THE SENTENCE THE WHOLE ACCESS POSITION RESTS ON: only the entity CVRPerson needs an access request, and the other CVR entities are not access-restricted. If this ever changes, Produktionsenhed becomes gated and the build stops",
    "kind": "http_contains",
    "url": "https://datafordeler.dk/vejledning/brugeradgang/anmodning-om-adgang/det-centrale-virksomhedsregister-cvr/",
    "contains": "CVRPerson"
  },
  {
    "id": "dawa-address-api-keyless",
    "claim": "DAWA answers without a key and returns WGS84 coordinates. This is the coordinate leg: Adressering.Adresse is a DAR UUID on 96.9% of Copenhagen rows, so coordinates are a JOIN rather than a geocode",
    "kind": "http_ok",
    "url": "https://api.dataforsyningen.dk/adresser?kommunekode=0101&side=1&per_side=1",
    "min_bytes": 200
  },
  {
    "id": "frederiksberg-is-a-separate-kommune",
    "claim": "Frederiksberg is kommunekode 0147 and Kobenhavn is 0101 - two kommuner, with 0147 entirely surrounded by 0101. Scoping to 0101 alone puts a hole in the middle of the map. This check confirms DAWA still treats them as separate codes",
    "kind": "http_contains",
    "url": "https://api.dataforsyningen.dk/kommuner?kode=0147",
    "contains": "Frederiksberg"
  }
]
```
