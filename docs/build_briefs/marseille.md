# Marseille — build brief

**Step 0 measured 2026-09-23.** France's national facts are in
`pipeline/countries/france.py` and `docs/france_step0_endpoints.md` — **read
those first**; a correction belongs there, not here. Run
`python scripts/brief_check.py marseille` before writing code.

---

## The one-line summary

**The cheapest follower — and the first proof that France's profile
transfers.** The taxonomy level holds (21.1% catch-all at sous-classe against
Paris's 19.8%), and Marseille is **better-named than Paris**, 43.4% against
39.6%. What is genuinely new is the **rail feed's scope: it is the whole
Métropole, not the city**, and that turns Marseille's boundary question into a
real one.

---

## ⚠️ THE OWNER CALL — the feed covers more cities than the register

**The GTFS is "Référentiel complet (tous les réseaux)" — every network of the
Métropole Aix-Marseille-Provence**, and it is not hypothetical. One of its
four tram entries is:

> `T` — **Le Charrel ⇄ Gare** — which is **Aubagne's** tram, not Marseille's.

And its 17 `route_type 2` routes include **"Lyon Part-Dieu – Genève"**,
**"Grasse – Cannes – Nice"** and **"Ambérieu – Saint-Étienne"** — TER services
spanning most of south-east France.

So a naive "draw everything rail in the feed" would put Aubagne's tram and
half the national TER network on a Marseille map.

**Two decisions, and the business leg does not constrain either:**

1. **Scope** — Marseille commune (`132xx`, 16 arrondissements) or the
   Métropole? `codeCommuneEtablissement` is a prefix list either way, so the
   register does not care. **Paris's commune-only answer does not transfer** —
   it rested on a measurement (all 16 métro lines survived the boundary), and
   Marseille's feed spans separate cities with their own networks.
2. **Ferries** — the feed carries **6 `route_type 4` routes**: Vieux-Port
   shuttles (`NAV1` Vieux Port–La Pointe Rouge, `NAV2` Vieux Port–L'Estaque),
   the **Frioul islands** service, and cross-harbour hops. **Not rail**, and
   this project has never drawn a ferry. Marseille's are genuine urban transit
   though, so it is a judgment call rather than an automatic exclusion.

---

## Business leg — SIRENE, inherited, re-measured for this city

| | |
|---|---|
| Source | `StockEtablissement` **parquet**, filter `codeCommuneEtablissement` prefix **`132`** |
| Active in NAF 47/56/96 | **≈25,430** (3,215 counted in 12.6% of the file) — a FLOOR; scaling undercounts |
| **Named** (`enseigne1` or `denominationUsuelle`) | **43.4%** — better than Paris's 39.6% |
| Masked (`statutDiffusion` ≠ `O`) | **12.2%** |

⚠️ **CORRECTED 2026-09-23 — Marseille IS better-named than Paris, and an
earlier note in this brief said otherwise.** That note compared Marseille's
fresh 11.2% measurement against Paris's **old 3.9%** figure and concluded they
were "statistically the same city". **A comparison across different samples is
not a comparison.** Re-scanned with all six cities in one 12.6% pass:
**Marseille 43.4%, Paris 39.6%** — a real four-point advantage, and the
country-wide spread runs 39.6% to 53.5%. See `docs/france_step0_endpoints.md`.

**Everything else is the country profile's**: active is `"A"` not `"Actif"`,
use `StockEtablissement` never `StockUniteLegale`, match the resource title
with its trailing ` -`.

---

## Coordinates — the join, unchanged

`siret` against INSEE's geolocation parquet. **Read the `epsg` column** —
Marseille is metropolitan, so **2154**, but the column is per row. No
geocoder, no key, no rate limit.

---

## Taxonomy — keys at sous-classe, confirming Paris

Measured on **Marseille rows**, against INSEE's own labels:

| Level | Catch-all | Paris | All six |
|---|---|---|---|
| **groupe (3)** | **48.1%** | 47.7% | 44.1–50.7% |
| classe (4) | 36.3% | 27.9% | 27.9–38.1% |
| **sous-classe (5)** | **21.1%** | **19.8%** | **19.8–23.0%** |

**0% unlabelled at every level** — INSEE's list slices French codes correctly,
unlike the Norwegian case where SN2007 could not be sliced by a NACE list.

**Key at sous-classe** — and **all six French cities land in a 19.8–23.0%
band**, measured on one sample. *Groupe* is catastrophic everywhere (44–51%).
**So the level choice genuinely transfers across France**, which is the first
country in this project where that has been shown rather than assumed.
⚠️ But *classe* ranges 27.9–38.1%, so the transfer is **level-specific, not
wholesale** — a city keying elsewhere in the scheme would need its own
measurement.

### ⚠️ Exclude distance selling — **16.4%** here, LOWER than Paris

`47.91A`, `47.91B`, `47.99A`, `47.99B` — **16.4%** on the 12.6% sample, against Paris's 18.2%. No storefront; inside the retail division. Across the six cities the range is **14.2% (Rennes) to 18.3% (Lyon)**.

---

## Rail — 2 métro + 3 tram lines, all named, all coloured

From the Mecatran feed, `route_type` 0 and 1 only:

| Mode | Ref | Line | Colour |
|---|---|---|---|
| subway | **M1** | La Rose – La Fourragère | `009FE3` |
| subway | **M2** | Gèze – Sainte-Marguerite Dromel | `E30613` |
| tram | **T1** | Noailles – Les Caillols | `F28C00` |
| tram | **T2** | Arenc Euroméditerranée – La Blancarde | `F4E718` |
| tram | **T3** | Gèze – La Gaye | `95C11F` |
| tram | `T` | *Le Charrel ⇄ Gare* — **AUBAGNE, not Marseille** | `FF0000` |

**Every line has a real name and a colour**, so the legend and on-map label
requirements are satisfiable without invention.

**The feed SELF-ATTESTS**: `feed_info.txt` gives publisher **Mecatran** and
`feed_end_date` **2026-12-31**. Better than Paris's, which carries no
`feed_info.txt` at all.

⚠️ **17 `route_type 2` routes are TER regional rail and are EXCLUDED** by the
standing commuter-rail rule — the same rule that drops Boston's `CR-*`,
Chicago's Metra, Madrid's Cercanías and Philadelphia's Regional Rail.

---

## ⚠️ Marseille owes France's OSM composition validation

`PLAN.md` records that France's storefront composition was validated against
OSM **on Paris only** — 50,156 against OSM's 54,198 (92.5%), and 10,595
against 10,642 on restaurants alone. **The first non-Paris build must re-run
that comparison**, and since Lyon is deferred, **that is Marseille.**

If it holds here, the country is settled; if it does not, the SIRENE filter
needs work before four more cities inherit it.

---

## Licence — `lov2`, and one read would cover FIVE sources

The GTFS declares **`lov2` — Licence Ouverte 2.0** on the National Access
Point. Attribution is the condition.

⚠️ **Licence Ouverte 2.0's own terms are NOT recorded in
`docs/data_sources.md`** — flagged during Paris's licence read and still open.
It now governs **SIRENE, the INSEE geolocation file, Marseille's GTFS, Lille's
GTFS and MEL's WFS**. **One read discharges all five**, which makes it the
highest-leverage licence item outstanding.

⚠️ **The `apiKey` in the feed URL is published by the NAP and is not a
credential gate** — a truncated copy of it returned `403 Invalid access key`,
which is the server telling you the key is wrong, not that you are refused.

---

## Region

`"region": "Europe"`.

---

## Still unknown — the honest list

- **Both owner calls above** — scope, and ferries.
- **Licence Ouverte 2.0's terms**, covering five sources.
- **The OSM composition validation**, which Marseille owes for all of France.
- **Exact bucket count.** 25,430 is scaled from 12.6% of the file, and
  **scaling undercounts**: Paris scales to 117,730 against its measured
  148,633, because bucket rows get denser through a file ordered by `siret`.
  **Treat 25,430 as a floor.**
- **Station counts per line**, and whether any métro or tram station falls
  outside whichever scope is chosen.

```brief-checks
[
  {
    "id": "marseille-gtfs-downloads",
    "claim": "The Aix-Marseille-Provence referentiel complet GTFS downloads with the NAP-published apiKey, ~34 MB. Note the key is PUBLISHED, not a credential gate - a truncated copy returns 403 'Invalid access key', which names the key you sent",
    "kind": "http_ok",
    "url": "https://app.mecatran.com/utw/ws/gtfsfeed/static/mamp?apiKey=60327e505a214c77303f52206f11483069257343",
    "min_bytes": 20000000
  },
  {
    "id": "marseille-gtfs-has-shapes-and-feed-info",
    "claim": "The feed carries shapes.txt so the 2 metro and 3 tram lines can be drawn, AND feed_info.txt so staleness is checkable from the artifact - which Paris's IDFM feed cannot do",
    "kind": "gtfs_files",
    "url": "https://app.mecatran.com/utw/ws/gtfsfeed/static/mamp?apiKey=60327e505a214c77303f52206f11483069257343",
    "present": ["routes.txt", "trips.txt", "stops.txt", "stop_times.txt", "shapes.txt", "feed_info.txt"],
    "absent": []
  },
  {
    "id": "marseille-gtfs-is-current",
    "claim": "The feed declares feed_end_date 2026-12-31. When this FAILS the Metropole has republished and the snapshot date shown on the page is stale",
    "kind": "gtfs_feed_window",
    "url": "https://app.mecatran.com/utw/ws/gtfsfeed/static/mamp?apiKey=60327e505a214c77303f52206f11483069257343",
    "expect": "current"
  },
  {
    "id": "sirene-stock-etablissement-parquet",
    "claim": "The SIRENE dataset still publishes a StockEtablissement parquet. Marseille filters it on codeCommuneEtablissement prefix 132 - the same file Paris uses, which is the whole point of the France profile",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/",
    "min_bytes": 5000
  },
  {
    "id": "insee-geolocation-dataset",
    "claim": "INSEE's geolocation file is still published - it is what makes Marseille's coordinate leg a JOIN rather than a geocode, exactly as for Paris",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/",
    "min_bytes": 3000
  },
  {
    "id": "nap-declares-lov2-for-marseille",
    "claim": "The National Access Point still declares lov2 on the Aix-Marseille-Provence dataset. If it changes to mobility-licence, Marseille inherits Paris's Art. 5.4 notice obligations instead of plain attribution",
    "kind": "http_ok",
    "url": "https://transport.data.gouv.fr/api/datasets",
    "min_bytes": 1000000
  },
  {
    "id": "naf-labels-available",
    "claim": "INSEE's NAF label file is still served. Marseille's catch-all (20.8% at sous-classe, 0% unlabelled) was measured against it, confirming Paris's level choice transfers",
    "kind": "http_ok",
    "url": "https://www.insee.fr/fr/statistiques/fichier/2120875/int_courts_naf_rev_2.xls",
    "min_bytes": 200000
  }
]
```
