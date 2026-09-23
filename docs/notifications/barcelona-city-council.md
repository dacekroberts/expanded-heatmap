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

## Both preconditions are met — ready to send

1. **The live terms were confirmed 2026-09-22**, by the owner, in a browser,
   past the hCaptcha this project does not defeat. **The notification clause is
   unchanged, word for word.** The reading is stored at
   `docs/licenses/barcelona-condicions-us-live.txt`; the Internet Archive
   capture it confirms is kept beside it, because that is the text Barcelona
   was actually built and published against.
2. **The site is public.** Live since 2026-09-22 at
   <https://expanded-heatmap-daceroberts.streamlit.app>, with Barcelona and
   Madrid both rendering. The URL is filled in below.

---

## Where it goes — the terms name the channel themselves

This was an open question until the live reading, and it has a clean answer.
The terms' own introduction says:

> *"Any doubts or comments on these Terms of use may be forwarded to the
> following link"* — `http://www.bcn.cat/cgi-bin/consultesIRIS?id=241`

That 301-redirects twice, ending at the Council's online enquiry service
pre-categorised to city data:

> <https://atencioenlinia.ajuntament.barcelona.cat/en/fitxa/alta?origen=DADES_CIUTAT&cbDetall=5163>

**Use that rather than an email address, because there is no email address to
use.** Checked three ways on 2026-09-22: the dataset's CKAN metadata carries
`author: Gerència de Turisme, Comerç i Mercats` and **no** `maintainer_email`
or `author_email` field at all; `datos.gob.es`, the Spanish government's own
catalogue, names the *Oficina Municipal de Dades* as contact point and gives a
**web form** as the method; and the portal's `/en/contacte` returns the same
hCaptcha bot-check. Anything of the shape `opendata@bcn.cat` would be
invention, and a formal notification sent to a guessed address can bounce
silently or reach the wrong team — which matters here, because the only
evidence this obligation was discharged is the record written afterwards.

### Send attempts — NOT YET DELIVERED

| Date | Channel | Result |
|---|---|---|
| 2026-09-22 | Open Data BCN portal's own dataset contact form | Passed the hCaptcha, then the form **stalled** |
| 2026-09-22 | `atencioenlinia.ajuntament.barcelona.cat` (the link the terms name) | **Timed out**, from the owner's network and independently from a session: HTTP 000 after 20 s, no response |

**The host is down, not blocking us.** Measured 2026-09-22:
`seuelectronica.ajuntament.barcelona.cat` answers HTTP 302 in 2.4 s from
`212.15.228.45`, and `atencioenlinia` sits in the **same /24** and answers
nothing at all. Two independent networks, one symptom. So this is neither the
CAPTCHA nor the owner's connection, and retrying from elsewhere will not help
until the service returns.

**The plan is to wait and retry that channel**, because it is both the one the
terms name and the only one that does not require Spanish electronic
identification. The clause sets **no deadline** — *"Users are required to
inform Barcelona City Council of every project"*, with no time limit attached
— so a documented good-faith attempt now and a successful send when the
service returns discharges it fully.

**The fallbacks were checked and are closed.** Barcelona's *Registre
electrònic* would be the more formal channel, since an instància carries a
registry number, but it states *"Per cursar-la, cal identificar-se amb
certificat digital"* — a digital certificate, idCAT or Cl@ve, which a
non-resident does not hold. Its only non-electronic route is presenting the
form in person at one of 26 municipal offices in Barcelona. Email is not an
option because no email address is published, as above; guessing one is worse
than waiting.

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
> Barcelona is one of eighteen cities included. It is available at:
>
> > <https://expanded-heatmap-daceroberts.streamlit.app>
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
> divuit ciutats incloses. Es pot consultar a:
>
> > <https://expanded-heatmap-daceroberts.streamlit.app>
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
