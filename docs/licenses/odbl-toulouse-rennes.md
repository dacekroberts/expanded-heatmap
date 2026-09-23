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

## ⚠️ NOT READ — the publishers' own conditions

**Both publishers' portal terms remain unread**, and the reason matters:

- `data.toulouse-metropole.fr` and Rennes' portal are Opendatasoft instances,
  which usually carry their own CGU.
- An automated read hit a **Cloudflare interactive challenge carrying a Ray
  ID** and **refused to complete it** — correctly, since this project does not
  defeat bot detection. It then spent 47 minutes seeking legitimate alternate
  routes before being stopped.

**This is a real gap, and it is the gap that defers Lyon.** Grand Lyon's CGU
added two things the base licence did not: **an open-ended indemnity (9.4)**
and **a bar on the producers' *signes distinctifs* (6.2)** which collides with
this project's invariant that every drawn line carries its real public name —
Toulouse's would say **Tisséo**, Rennes' **STAR**.

**Until those CGU are read, neither city should ship.** Read them in a browser,
where the challenge can be passed legitimately by a person, or ask the
publishers directly.

---

## What transfers, and what does not

| | Paris | Toulouse / Rennes |
|---|---|---|
| Licence | `mobility-licence` | **`odc-odbl`** |
| Share-alike on the map | no (Art. 5.6(b)) | **no (§4.5(b))** |
| Offer the method | yes (Art. 5.8) | **yes (§4.6(b))** |
| Notice wording | prescribed, French | **prescribed, English safe harbour** |
| Snapshot date required | **yes** (Art. 5.7) | **no** |
| Publisher gloss on derivatives | **yes**, NAP's | **none** |
