# Lille — build brief

**Step 0 measured 2026-09-23.** France's national facts are in
`pipeline/countries/france.py` and `docs/france_step0_endpoints.md` — **read
those first**. Run `python scripts/brief_check.py lille` before writing code.

---

## The one-line summary

**The only French city whose rail geometry cannot come from its own feed.**
Lille's GTFS has **no `shapes.txt`**, so its two VAL métro lines and one tram
have no line geometry in it. Half the gap closes first-party — MEL's WFS
carries **tram** geometry — and the métro must come from OSM. It also carries
the **only unresolved licence question** among the five `lov2` sources.

---

## ⚠️ TWO OWNER CALLS

### 1. Where does rail geometry come from?

**Lille's GTFS has no `shapes.txt`** (verified: 7 files, `shapes.txt` absent).
The project's invariant requires every drawn line to carry real geometry plus
a permanent on-map label plus a legend entry.

| Mode | First-party? | Source |
|---|---|---|
| **Tram** | ✅ | `mel_mobilite_et_transport:tramway_lignes` — **4 LineStrings**, lines **R** (Lille↔Roubaix) and **T** (Lille↔Tourcoing), with `nom`, `ligne`, `exploitant` |
| **Métro** | ❌ | **Nothing but points** — `stations_metro` and `dsp_ilevia:entree_sortie_metro`. **Both VAL lines need OSM** |

**Hybrid** (MEL tram + OSM métro) gives better tram data and mixes sources;
**all-OSM** is consistent and discards a first-party layer. Either is
defensible — it has not been decided.

🎁 **Either way, take MEL's colours.** `dsp_ilevia:couleurs_lignes` exists, and
`ilevia_traceslignes` carries `rgbhex_fond`, `rgbhex_texte` and `color`.
Lille's GTFS may not carry route colours, and **every drawn line needs a legend
entry.**

### 2. ⚠️ Is the GTFS ilévia's site content, or MEL's open data?

The feed is served from **`media.ilevia.fr`**, and ilévia's Mentions légales
§5 bars *« pas de modification ni altération d'aucune sorte »* and commercial
use of *« les contenus des Services en ligne »*.

- **Permits**: *Services en ligne* is a **defined term** — ilévia's websites
  and apps. The GTFS is **MEL's `lov2` publication** on the national access
  point, and MEL's own catalogue declares the ilévia layers Licence Ouverte.
  **This is the SEPTA pattern** — a web-contents notice mistaken for a data
  licence.
- **Does not**: `media.ilevia.fr` is an ilevia.fr property, and this project
  both modifies and publishes.

⚠️ **The obvious mitigation FAILS.** The PAN's stable
`data.gouv.fr/api/1/datasets/r/c9e5dd3f-…` URL **302s to `media.ilevia.fr`** —
a redirect, not a mirror, so the bytes come from ilévia's host either way.
*Checked specifically so this is not recorded as solved when it is not.*

**Third "no modification" bar this project has met**, after LA Metro and
Philadelphia. **Cheap close: email `opendata@lillemetropole.fr`** to confirm
the GTFS is MEL's publication rather than ilévia site content.

---

## Business leg — SIRENE, commune `59350`

| | |
|---|---|
| Source | `StockEtablissement` **parquet**, `codeCommuneEtablissement` **= `59350`** |
| Active in NAF 47/56/96 | **≈8,076** (1,021 counted in 12.6% of the file) — a **floor** |
| **Named** | **47.5%** (Paris 39.6%, Rennes 53.5%) |
| Masked | 9.6% |
| Distance selling to exclude | 16.7% |

⚠️ **Scope is a live question here, more than anywhere else in France.**
Lille's commune is small against the **Métropole Européenne de Lille**, and its
**métro serves Villeneuve-d'Ascq, Roubaix and Tourcoing** — the tram's own name
says so. **Paris's commune-only answer rested on all 16 métro lines surviving
its boundary; Lille's will not.**

---

## Coordinates — the join

`siret` against INSEE's geolocation parquet. **Read the `epsg` column** —
**2154**, per row.

---

## Taxonomy — sous-classe

| Level | Lille | All six |
|---|---|---|
| groupe (3) | 44.1% | 44.1–50.7% |
| classe (4) | 38.1% | 27.9–38.1% |
| **sous-classe (5)** | **23.0%** | **19.8–23.0%** |

**Key at sous-classe.** 0% unlabelled. Lille is at the top of the band on all
three levels — the noisiest French city taxonomically, though still far better
than *groupe*.

---

## Rail — what the feed does and does not have

`https://media.ilevia.fr/opendata/gtfs.zip` — 9.2 MB, **7 files**.

| | |
|---|---|
| `shapes.txt` | ❌ **MISSING** — see owner call 1 |
| `feed_info.txt` | ❌ missing — record the download date |
| Rail routes | **2 `route_type 1`** (métro) + **1 `route_type 0`** (tram) |
| Bus | 154, excluded |

⚠️ **`L1` in ilévia data is *Liane 1*, a BUS**, not Métro Ligne 1. The
`dsp_ilevia:ilevia_traceslignes` layer is titled *"lignes de bus"* and its
`type_ligne` values are `Urbaine`, `Suburbaine`, `Scolaire`, `Ligne de nuit` —
all bus. **The title was honest; the line code was the trap.**

---

## Licence — `lov2`, with one open carve-out

Both the GTFS and MEL's WFS declare **Licence Ouverte 2.0**. Full analysis at
`docs/licenses/france-licence-ouverte-2.0.md`.

**MUST DISPLAY** — `Métropole Européenne de Lille` **+ the date of last
update**, per source. The MEL WFS ilévia layers name **Ilévia** as co-producer,
so *« a minima le nom du producteur »* points at ilévia too.

⚠️ **`tramway_lignes` carries NO citation date** — only a `dateStamp` of
2024-06-03 and a revision of 2024-05-29, **neither of which is literally *la
date de dernière mise à jour***. Its `fileIdentifier` still reads
`reseau-transpole`, ilévia's pre-2019 name. **Cite the `dateStamp` or the
retrieval date and say which.**

⚠️ **MEL's catalogue is MIXED.** Of 427 records, **13 require a signed *acte
d'engagement*** and **1 is ODbL**. The five layers in scope are clean —
**verified individually**. **Any new MEL layer must be checked per-record.**

**No logos.** **No indemnity.** **No share-alike.**

---

## Region

`"region": "Europe"`.

---

## Still unknown

- ⚠️ **Both owner calls above** — geometry source, and the ilévia carve-out.
- ⚠️ **Scope** — commune vs MEL, and here it changes which métro stations exist.
- **`tramway_lignes`'s true last-update date.**
- **Exact bucket count** — 8,076 is scaled and is a floor.

```brief-checks
[
  {
    "id": "lille-gtfs-downloads",
    "claim": "Ilevia's GTFS downloads with no key, ~9.2 MB. NOTE the open licence carve-out: it is served from media.ilevia.fr, whose Mentions legales bar modification of 'les contenus des Services en ligne' - and the PAN's stable URL 302s here rather than mirroring, so that is not a mitigation",
    "kind": "http_ok",
    "url": "https://media.ilevia.fr/opendata/gtfs.zip",
    "min_bytes": 5000000
  },
  {
    "id": "lille-gtfs-has-NO-shapes",
    "claim": "THE DEFINING FACT: the feed carries NO shapes.txt and no feed_info.txt, so line geometry cannot be drawn from it at all and staleness is not checkable from the artifact. If shapes.txt ever appears, owner call 1 is moot and this check should fail loudly to say so",
    "kind": "gtfs_files",
    "url": "https://media.ilevia.fr/opendata/gtfs.zip",
    "present": ["routes.txt", "trips.txt", "stops.txt", "stop_times.txt"],
    "absent": ["shapes.txt", "feed_info.txt"]
  },
  {
    "id": "mel-wfs-serves-tram-geometry",
    "claim": "MEL's geOrchestra WFS is live and is where Lille's TRAM line geometry comes from - mel_mobilite_et_transport:tramway_lignes, 4 LineStrings for lines R and T. The portal is geOrchestra, NOT Opendatasoft: its 404 body names itself, which is why /api/datasets paths all miss",
    "kind": "http_contains",
    "url": "https://data.lillemetropole.fr/geoserver/wfs?service=WFS&request=GetCapabilities&version=2.0.0",
    "contains": "tramway_lignes"
  },
  {
    "id": "sirene-stock-etablissement-parquet",
    "claim": "The SIRENE parquet is still published. Lille filters it on codeCommuneEtablissement = 59350 - but see the scope question: the commune is small against MEL, whose metro serves Villeneuve-d'Ascq, Roubaix and Tourcoing",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/",
    "min_bytes": 5000
  },
  {
    "id": "insee-geolocation-dataset",
    "claim": "INSEE's geolocation file is still published - the coordinate join, built only from diffusible establishments",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/",
    "min_bytes": 3000
  }
]
```
