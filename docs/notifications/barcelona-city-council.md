# Notification to Barcelona City Council — draft, NOT YET SENT

**Why this file exists.** Open Data BCN's terms of use impose an obligation no
other source in this project does — an **affirmative act owed to the
publisher**, not a line of text on a page:

> *"Users are required to inform Barcelona City Council of every project
> relating to or derived from their use of the data sets, so that they are open
> to the public for the purpose of encouraging policies for reusing information
> from the public sector."*
> — Open Data BCN, *Terms of use*, stored at
> `docs/licenses/barcelona-condicions-us.txt`

The tail of that sentence is what settles its nature. The Council wants derived
projects **visible so it can point at them**: this is a reuse-showcase
notification, not a permission gate. Publishing does not wait on a reply.

---

## Before sending — two things, in this order

1. **Confirm the live terms.** They were read from the Internet Archive
   (newest capture 2025-03-28) because `opendata-ajuntament.barcelona.cat`
   serves **hCaptcha**, and this project does not defeat CAPTCHAs. The terms
   also amend themselves with effect on publication. **A human has to open
   `https://opendata-ajuntament.barcelona.cat/en/condicions-us` and confirm the
   clause still reads as above.** The *declared licence* needs no such step —
   it is live-verifiable through the API and read `CC-BY-4.0` on 2026-09-22.
2. **Send it once the site is public.** The notification names a project the
   Council is meant to be able to look at, so it needs the live URL. Sending it
   before the deploy would mean notifying them of something they cannot see.

**Where it goes:** the portal's own contact form. CKAN names the publishing
department as **Gerència de Turisme, Comerç i Mercats** (organization
`comerc`), and publishes no address for it, so the form is the channel. It sits
behind the same CAPTCHA.

---

## English

> **Subject:** Notification of a reuse project based on Open Data BCN — Cens de
> locals en planta baixa
>
> Dear Open Data BCN team,
>
> I am writing to notify you of a project derived from your data, as the Terms
> of use require.
>
> **The project.** *Storefronts Near Transit* is a non-commercial portfolio
> project that maps the density of ground-floor commercial premises around
> urban rail stations, so that the same measure can be compared across cities.
> Barcelona is one of seventeen cities included. It is available at:
>
> > &lt;URL&gt;
>
> **The dataset used.** *Cens de locals en planta baixa amb activitat
> econòmica*, the 2022 survey (resource `99764d55-b1be-4281-b822-4277442cc721`),
> retrieved 22 September 2026 under CC BY 4.0.
>
> **What was done to the data**, as the Terms require modifications to be
> identified: premises recorded as having no economic activity were removed;
> the remainder were filtered to retail, food service and personal services
> using the census's own activity classification; those were grouped into three
> categories of the project's own; and each premises was measured by distance
> from the nearest metro station. Accommodation was excluded from food service.
> No individual premises record is republished in full, and no address is
> displayed — only the trade name, the activity and the location.
>
> The page states the survey year, credits the data as *"Source of the data:
> Barcelona City Council"*, and states that the Council does not endorse the
> project.
>
> I am happy to provide reuse statistics should you wish, as the Terms of use
> contemplate.
>
> With thanks for publishing the data,
>
> &lt;NAME&gt;

---

## Català

> **Assumpte:** Notificació d'un projecte de reutilització basat en Open Data
> BCN — Cens de locals en planta baixa
>
> Benvolguts,
>
> Em poso en contacte amb vosaltres per notificar-vos un projecte derivat de
> les vostres dades, tal com requereixen les Condicions d'ús.
>
> **El projecte.** *Storefronts Near Transit* és un projecte de portfoli, sense
> ànim de lucre, que cartografia la densitat de locals comercials en planta
> baixa al voltant de les estacions de transport ferroviari urbà, de manera que
> la mateixa mesura es pugui comparar entre ciutats. Barcelona és una de les
> disset ciutats incloses. Es pot consultar a:
>
> > &lt;URL&gt;
>
> **Conjunt de dades utilitzat.** *Cens de locals en planta baixa amb activitat
> econòmica*, enquesta del 2022 (recurs
> `99764d55-b1be-4281-b822-4277442cc721`), obtingut el 22 de setembre de 2026
> sota llicència CC BY 4.0.
>
> **Modificacions realitzades**, atès que les Condicions exigeixen que
> s'identifiquin: s'han exclòs els locals sense activitat econòmica; la resta
> s'han filtrat a comerç al detall, serveis de menjar i begudes i serveis
> personals, emprant la classificació d'activitats del mateix cens; aquests
> s'han agrupat en tres categories pròpies del projecte; i cada local s'ha
> mesurat per distància a l'estació de metro més propera. Els serveis
> d'allotjament s'han exclòs dels serveis de menjar i begudes. No es republica
> cap registre individual complet ni es mostra cap adreça: només el nom del
> local, l'activitat i la localització.
>
> La pàgina indica l'any de l'enquesta, cita les dades com a *"Source of the
> data: Barcelona City Council"* i fa constar que l'Ajuntament no dona suport
> al projecte.
>
> Restem a la vostra disposició per facilitar-vos dades estadístiques de
> reutilització, tal com preveuen les Condicions d'ús.
>
> Agraint-vos la publicació de les dades,
>
> &lt;NOM&gt;

---

## After sending

Record the date and the channel in `DECISIONS.md`, and change notice **21** in
`docs/data_sources.md` from *outstanding* to *sent*. The obligation is
discharged by the act, not by the page — so the only evidence it happened is
the record you write.
