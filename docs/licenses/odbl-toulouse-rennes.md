# ODbL — Toulouse and Rennes GTFS

**Read 2026-09-23 from the canonical Open Data Commons text**
(`opendatacommons.org/licenses/odbl/1-0/`).

Applies to two of France's six cities:

| City | Dataset | Publisher |
|---|---|---|
| **Toulouse** | Réseau urbain Tisséo | Toulouse métropole |
| **Rennes** | Réseau urbain STAR | STAR / Keolis Rennes |

Both declare `odc-odbl` on `transport.data.gouv.fr`. **Neither is Paris's
`mobility-licence`**, so none of Paris's reading carries over.

---

## VERDICT: PERMITTED WITH CONDITIONS

Redrawing station points and line geometry onto a rendered map is permitted.
**But this project makes two artifacts from the feed, and ODbL treats them
differently** — that distinction is the whole read.

---

## The three-way distinction that decides it

| ODbL term | What it is here |
|---|---|
| **Database** | the GTFS feed |
| **Derivative Database** | ⚠️ **the committed `outputs/<city>/` station CSV** |
| **Produced Work** | the rendered heatmap HTML |

### ✅ The MAP does not trigger share-alike — §4.5(b), quoted

> **4.5 Limits of Share Alike.** The requirements of Section 4.4 do not apply
> in the following: … b. Using this Database, a Derivative Database, or this
> Database as part of a Collective Database **to create a Produced Work does
> not create a Derivative Database for purposes of Section 4.4**

So the rendered map need not be ODbL. **That is settled, not arguable.**

### ⚠️ But §4.6 fires on a Produced Work *from* a Derivative Database

> **4.6 Access to Derivative Databases.** If You Publicly Use a Derivative
> Database **or a Produced Work from a Derivative Database**, You must also
> offer to recipients … a copy in a machine readable form of:
> a. The entire Derivative Database; **or**
> b. A file containing all of the alterations made to the Database **or the
> method of making the alterations to the Database (such as an algorithm)**

**This is the clause that reaches this project**, because the map is produced
*from* the committed station table rather than directly from the feed.

**And it is already satisfied — by the repository.** `outputs/<city>/` is
committed publicly alongside the pipeline code, which is literally *"the
method of making the alterations"* under §4.6(b). ⚠️ **It must be LINKED from
the site** to count as an offer to recipients; an unlinked repo is not an
offer.

This is the same shape as Licence Mobilités Art. 5.8 for Paris — **two
different French licences arriving at the same requirement**, which means one
repository link discharges both.

---

## MUST DISPLAY — §4.3, with the licence's own safe-harbour wording

> **4.3 Notice for using output (Contents).** … if you Publicly Use a Produced
> Work, You must include a notice associated with the Produced Work reasonably
> calculated to make any Person that uses, views, accesses, interacts with, or
> is otherwise exposed to the Produced Work aware that Content was obtained
> from the Database … and that it is available under this License.
> **a. Example notice.** The following text will satisfy notice under Section
> 4.3: *Contains information from DATABASE NAME, which is made available here
> under the Open Database License (ODbL).*

So, verbatim per city:

```
Contains information from Réseau urbain Tisséo, which is made available
here under the Open Database License (ODbL).
```
```
Contains information from Réseau urbain STAR, which is made available
here under the Open Database License (ODbL).
```

⚠️ **This project already displays an ODbL notice for OpenStreetMap basemap
tiles. That does NOT discharge these** — different databases, and §4.3 requires
the notice to identify *which* database the content came from.

---

## ⚠️ THE OPEN QUESTION — is the station CSV a Derivative Database?

**§4.4 share-alike** requires a publicly used Derivative Database to be
offered under ODbL or a compatible licence. So whether the committed station
table *is* one decides whether it needs its own ODbL notice.

- **The reading that says YES**: it is an extraction of a substantial part of
  `stops.txt` — names, coordinates, line associations — rearranged into a new
  database. ODbL's definition reaches *"any translation, adaptation,
  arrangement, modification, or any other alteration"*.
- **The reading that says NO**: it is a filtered subset adding no information,
  and §4.5(b) already severs the map from share-alike.

**Not resolved in this project's favour.** ⚠️ **And unlike Paris, there is no
publisher gloss to lean on.** Licence Mobilités was rescued by the National
Access Point's *published interpretation*, which filed *"calcul de la distance
à l'arrêt de bus le plus proche pour une liste de commerces"* under **"Non"**,
no resharing required. **ODbL has no equivalent**, and the standard text is
stricter.

**Cheap discharge, and it is recommended**: put an ODbL notice on the station
CSV in `outputs/<city>/` for these two cities. It costs one line, it moots the
question, and it is the same move taken for Paris (republishing the derived
table) rather than an argument.

---

## MUST NOT

**§4.7(a)** — no technological measures or additional terms that restrict the
rights granted. A public repository imposes none.

---

## ✅ The publishers' own CGU — READ 2026-09-23, and BOTH ARE CLEAN

**Neither carries Lyon's two killers.** Both portals are Opendatasoft and both
serve the same CGU template at `/terms/terms-and-conditions/`:

- `https://data.toulouse-metropole.fr/terms/terms-and-conditions/`
- `https://data.explore.star.fr/terms/terms-and-conditions/`

⚠️ **They answered plain `curl` with no challenge.** The Cloudflare
interactive challenge an earlier automated read hit was **path- or
timing-specific, not a standing wall** — worth knowing before any portal is
recorded as blocked again. The real paths came from the portals' own footers.

### The acceptance clause binds — so these ARE part of the terms

> **TOUTE UTILISATION EFFECTUÉE À QUELQUE TITRE QUE CE SOIT, DU PRÉSENT
> DOMAINE IMPLIQUE OBLIGATOIREMENT L'ACCEPTATION SANS RÉSERVE … DES
> PRÉSENTES CONDITIONS GÉNÉRALES D'UTILISATION**

`read-licence` step 3 satisfied: incorporation found and followed.

### ✅ NO indemnity

**Neither CGU contains one.** Searched for *indemnis*, *indemnit*,
*supportera seul*, *conséquences financières*. Grand Lyon's **CGU 9.4 has no
counterpart here.**

### ✅ The marks clause is OPENDATASOFT'S, and it carves the data OUT

> « Les données publiées sur le DOMAINE sont la propriété de la Société [/ du
> STAR]. **À l'exception des données publiées sur le DOMAINE**, il est rappelé
> que les marques, logos, slogans … créés, publiés ou enregistrés par
> **OPENDATASOFT** sont la propriété exclusive de OPENDATASOFT »

**This protects the platform vendor's branding and expressly excludes the
published data.** It is **not** Grand Lyon's Art. 6.2, which bars the
*producers'* signes distinctifs *« associés ou non à l'utilisation des
données »* — explicitly reaching beyond the site.

✅ **So naming *Tisséo* and *STAR* on the map is not barred**, and the
invariant that every drawn line carries its real public name is safe in both
cities.

### ✅ The express prohibition is CONDITIONAL, and the condition excludes us

> « la Société interdit expressément : L'extraction … d'une partie
> qualitativement ou quantitativement substantielle du contenu du DOMAINE …
> **dès lors que l'auteur de cette extraction intervient EN DEHORS D'UNE
> LICENCE consentie** par OPENDATASOFT ou la Société »

Sui-generis database-right boilerplate **with a licence carve-out**. The GTFS
**is** licensed (ODbL, declared on the NAP and the portal), so this project
operates **inside** a granted licence and the prohibition does not bite.

### The step-4 split, both halves recorded

The restrictive paragraph governs **the PLATFORM**: *« Toute représentation
totale ou partielle de la PLATEFORME OPENDATASOFT, du DOMAINE ou de leurs
composantes »*. The permissive obligation governs **the data**: *« mentionner
la source des JEUX DE DONNÉES en cas de réutilisation »*, plus
*« il appartient à chaque BÉNÉFICIAIRE de consulter la LICENCE concernant
chaque JEU DE DONNÉES »* — **the same per-dataset-licence warning MEL gives**,
and MEL's catalogue proved it load-bearing.

---

## ⚠️ This does NOT bring Lyon back

**Lyon is a different portal with different terms.** `data.grandlyon.com` is
not Opendatasoft, and its CGU was read separately and **does** contain both
clauses:

| | Toulouse / Rennes | **Lyon** |
|---|---|---|
| Platform | Opendatasoft | Grand Lyon's own |
| Indemnity | **none** | **CGU 9.4, open-ended** |
| Marks clause | Opendatasoft's, **data excluded** | **CGU 6.2 — producers' *signes distinctifs*, *"associés ou non à l'utilisation des données"*** |
| Account to download | no | **yes** |
| NAP feed | live | **dead since 2022-04-14** |

**Three French portals, three different answers** — which is the argument for
reading each rather than inheriting a country position.

**Lyon returns only on owner decisions**, not on new evidence: create the
`data.grandlyon.com` account, accept CGU 9.4's indemnity (there is precedent —
Hong Kong's was accepted 2026-09-22), and settle whether naming **TCL** is
barred, which `contactopendata@tcl.fr` can authorise cheaply.

## What transfers, and what does not

| | Paris | Toulouse / Rennes |
|---|---|---|
| Licence | `mobility-licence` | **`odc-odbl`** |
| Share-alike on the map | no (Art. 5.6(b)) | **no (§4.5(b))** |
| Offer the method | yes (Art. 5.8) | **yes (§4.6(b))** |
| Notice wording | prescribed, French | **prescribed, English safe harbour** |
| Snapshot date required | **yes** (Art. 5.7) | **no** |
| Publisher gloss on derivatives | **yes**, NAP's | **none** |
