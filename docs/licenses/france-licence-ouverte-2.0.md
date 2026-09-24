# Licence Ouverte 2.0 (Etalab) — five French sources

**Read 2026-09-23.** One read discharges five sources:

| # | Source | Used for |
|---|---|---|
| 1 | **SIRENE `StockEtablissement`** (INSEE) | the business register, every French city |
| 2 | **INSEE geolocation file** | the `siret` coordinate join |
| 3 | **Marseille GTFS** (Métropole d'Aix-Marseille-Provence) | rail |
| 4 | **Lille GTFS** (Métropole Européenne de Lille) | rail |
| 5 | **MEL WFS** — tram geometry, metro stations, line colours | Lille's line geometry |

---

## VERDICT: PERMITTED WITH CONDITIONS

> « Le "Concédant" concède au "Réutilisateur" un droit non exclusif et gratuit
> de libre "Réutilisation" de l'"Information" … **à des fins commerciales ou
> non**, dans le monde entier et pour une durée illimitée »

and expressly for derived works:

> « de l'adapter, la modifier, l'extraire et la transformer, **notamment pour
> créer des "Informations dérivées"** »

**No share-alike of any kind.** LO 2.0 defines *Information dérivée* and
attaches **no licensing obligation** to it. **No revocation clause** — the
grant is *"pour une durée illimitée"*, and a new version does not claw back.
**No indemnity.** No fee, no registration.

---

## ✅ The date-of-last-update duty is LO 2.0's OWN

This answers a question this project asked three times. The operative clause:

> « mentionner la paternité de l'«Information» : sa source (a minima le nom du
> « Concédant ») **et la date de la dernière mise à jour de l'« Information »
> réutilisée** »

**MEL is not adding it.** Its `gmd:useLimitation` is a near-verbatim
restatement, down to *« a minima »*. Confirmed independently a third time on
`transport.data.gouv.fr`'s own legal page, and a fourth by INSEE with a
softener (*« lorsque celle-ci est connue »*).

**So the duty found in Licence Mobilités Art. 5.7, Grand Lyon CGU 6.1 and
MEL's WFS is ONE duty restated, not three publishers each inventing one.**

⚠️ **A link is optional.** It is one offered way to discharge the *source*
element; **name-plus-date is the obligation.**

---

## MUST DISPLAY

1. ⚠️ **`Source : Insee`** — **verbatim, the only prescribed string in the
   five.** INSEE: reuse permitted *« sous réserve de mentionner la source
   **sous la forme « Source : Insee »** »*. Covers both SIRENE and the
   geolocation file.
2. **The date of last update, PER SOURCE.**
3. **Marseille GTFS** — the Concédant's name (see carve-out B) + date.
4. **Lille GTFS** — `Métropole Européenne de Lille` + date.
5. **MEL WFS** — `Métropole Européenne de Lille` + date; the ilévia layers
   name **Ilévia** as co-producer, so *« a minima le nom du producteur »*
   points at ilévia too.

⚠️ **A combined attribution block must still carry name-and-date for EVERY
`lov2` source individually.** One shared line naming several publishers under
a single date does not discharge it.

---

## MUST NOT SAY

- **No official character** — must not confer *« un caractère officiel »* on
  the reuse.
- **No endorsement or affiliation** — *« ni suggérer une quelconque
  reconnaissance ou caution par le "Concédant", ou par toute autre entité
  publique »*.
- **Must not mislead** as to the content, **its source, or its date of
  update**.
- ⚠️ **INSEE goes further, into interpretation**: *« de ne pas altérer le sens
  des informations ou **induire en erreur quant à leur interprétation** »*.
- ⚠️ **No logos.** `data.gouv.fr` CGU 5.1.3 excludes logos and iconographic
  representations from the Licence Ouverte; INSEE bars reproducing its marks;
  the ministry's marks are INPI-registered. **Render no publisher's logo.**

**Notably absent:** no accuracy/completeness/timeliness gag of the MTA/WMATA
kind. The bar is *"don't mislead"*, which is narrower.

---

## ⚠️ MUST DO — a STANDING refresh duty, not a one-off

INSEE, on the SIRENE dataset:

> « **il est ainsi de votre responsabilité de tenir compte du statut de
> diffusion le plus récent de chaque personne physique**, qui tient compte des
> oppositions formulées par certaines d'entre elles »

**`statutDiffusion` changes as people exercise opposition**, so a committed
`outputs/` snapshot can contain someone who has since opted out. **This is a
recurring obligation and argues for a stated refresh cadence.** It is not
discharged by anything on the page.

**No notification, registration, permission gate or statistics duty exists** —
searched across all five publishers. **Nothing blocks publication.**

### ✅ Privacy: the upstream work is better than assumed

`statutDiffusion = P` masks the name, the address within the commune **and the
geolocation** — and **the geolocation file is built only from
« les établissements dont les données sont diffusibles »**. So **the coordinate
join cannot reintroduce a masked establishment's location.** That materially
narrows what `check_personal_exposure.py` must catch.

---

## Compatibility — and the trap in it

> « compatible avec … "Open Government Licence" (OGL) du Royaume-Uni,
> "Creative Commons Attribution" (CC-BY) … et "Open Data Commons Attribution"
> (**ODC-BY**) »

⚠️ **ODC-BY is NOT ODbL.** ODbL is the share-alike member of that family and
is **not named**. **Do not read this clause as blessing Toulouse's or Rennes'
ODbL feeds.**

Whether ODbL's share-alike reaches a database built partly from LO 2.0 sources
is an **ODbL** question and remains open — see
`docs/licenses/odbl-toulouse-rennes.md`.

---

## ⚠️ CARVE-OUT A — Lille's GTFS host. OWNER DECISION

The feed is served from **`media.ilevia.fr`**, and ilévia's Mentions légales
§5 says:

> « La reproduction des contenus des Services en ligne est autorisée à
> condition de respecter l'intégrité des documents reproduits (**pas de
> modification ni altération d'aucune sorte**) … ne peuvent être utilisées …
> **à des fins commerciales ou publicitaires** »

- **Permits**: *« Services en ligne »* is a **defined term** — ilévia's websites
  and mobile apps. Every restriction is scoped to their *contenus*. The GTFS is
  published by **MEL** on the national access point under `lov2`, and MEL's own
  catalogue declares the ilévia layers LO 2.0. **This is the SEPTA pattern** — a
  web-contents notice mistaken for a data licence.
- **Does not permit**: `media.ilevia.fr` is an ilevia.fr property, so the zip is
  arguably *contenu des Services en ligne*, and this project both modifies and
  publishes.

⚠️ **The obvious mitigation does NOT work**: the PAN's stable
`data.gouv.fr/api/1/datasets/r/c9e5dd3f-…` URL **302s to `media.ilevia.fr`** —
a redirect, not a mirror, so the bytes come from ilévia's host either way.

**Third "no modification" bar this project has met**, after LA Metro and
Philadelphia. **Cheap close: email `opendata@lillemetropole.fr`** to confirm
the GTFS is MEL's `lov2` publication rather than ilévia site content.

## ⚠️ CARVE-OUT B — who is Marseille's Concédant?

The PAN declares **Métropole d'Aix-Marseille-Provence**; the feed's own
`feed_info.txt` self-attests **Mecatran**. The Concédant is the body that
granted the licence — **the Métropole**. Naming Mecatran alone would be wrong.
**Record the choice** so the brief and the notice do not drift apart.

---

## ⚠️ MEL's catalogue is MIXED, and its own terms say so

> « Respecter strictement la LICENCE OUVERTE **ou PARTICULIERE** correspondant
> au JEU DE DONNEES consulté … **Il appartient ainsi à chaque utilisateur de
> consulter la LICENCE concernant chaque JEU DE DONNEES avant tout
> téléchargement** »

Across **all 427 records**:

| Constraint | Records |
|---|---|
| Licence Ouverte 2.0 (four spelling variants) | ~360 |
| ⚠️ *« transmissibles **après signature d'un acte d'engagement** »* | **13** |
| ⚠️ **ODbL 1.0** | **1** |
| Third-party botanical citation | 38 |
| No constraint at all | 2 |

**The five layers in scope are all clean — verified individually, not inferred
from the majority**: `tramway_lignes`, `stations_metro`,
`dsp_ilevia:couleurs_lignes`, `ilevia_traceslignes`, `entree_sortie_metro`.

⚠️ **If a later session adds a MEL layer, check its record individually.** A
signature requirement and a share-alike layer sit one layer away. **This
belongs in a check, not in prose.**

**MEL's institutional site is a New York.** `www.lillemetropole.fr` says
*« Tous droits réservés »* and *« Seule une utilisation à des fins strictement
personnelles est autorisée »* — but it is **web-page-only**, a **different
host**, and the data portal does not link it. The tell: the institutional
version claims rights *« ou en tant que base de données »*; **the data portal's
version drops that phrase.**

---

## Two text divergences, neither changing an obligation

**The canonical URL moved**: `etalab.gouv.fr/licence-ouverte-open-licence` now
301s to `data.gouv.fr/pages/legal/licences/etalab-2.0`. Etalab's own domain no
longer serves it.

Two Etalab-sanctioned French renderings differ in wording (*« au moins »* vs
*« a minima »*; hyperlink vs URL as the discharge example; a stronger IP
warranty in the HTML). **No difference changes a reuser's obligation.** An
official English version exists but follows the **PDF** lineage, so it does not
match the current canonical French page — **and the licence is governed by
French law, so the French text controls.**

The canonical page's own worked example is **this project's primary source**:

> « Dans le cas d'une réutilisation de la base SIRENE de l'INSEE, mentionner
> l'URL du "Concédant" : www.insee.fr + la date de dernière mise à jour »

---

## What could NOT be established

1. ⚠️ **`tramway_lignes` has NO citation date** — the very layer Lille would
   draw. Only a `dateStamp 2024-06-03` and a revision `2024-05-29`. **Neither
   is literally *la date de dernière mise à jour***, and INSEE's *« lorsque
   celle-ci est connue »* softener is INSEE's, not MEL's. Its
   `fileIdentifier` still says `reseau-transpole` — ilévia's pre-2019 name — so
   the record is not freshly maintained.
2. **Whether `media.ilevia.fr` falls inside ilévia's *Services en ligne*** —
   carve-out A.
3. **Whether ODbL's share-alike reaches a mixed ODbL + LO 2.0 database.**
4. INSEE's retired `www.sirene.fr` CGU — **NXDOMAIN**, so the browser cannot
   help either.
5. Which 13 layers carry the acte d'engagement, beyond confirming none is ours.
6. **Marseille's Concédant name** — carve-out B.
