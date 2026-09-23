# France — required notices and obligations

**NOT YET PROMOTED. No French city is built.** These are held here
deliberately: `docs/data_sources.md`'s numbered notices list is the **deploy
gate**, and it stays a list of things that actually apply. When Paris ships,
these become items 23+ there — appended **without renumbering anything above
them**, because a block appended carelessly once produced two item 8s and two
item 15s, which `check_provenance.py` now fails on.

Read **2026-09-22** via the `licence-read` agent. Full chain followed: the NAP
API, both dataset pages, the 14-page licence PDF, both platform CGU, both
publishers' own licence pages, and the Legifrance articles the licence cites.

---

## The headline: `mobility-licence` is rare, and it is not ODbL

Only **2 of 799** datasets on France's National Access Point carry this code —
and they are **exactly the two cities this project wants first**. The other
797 are `lov2` (472), `odc-odbl` (212), `notspecified` (93) and `fr-lo` (20).

**There is no government-hosted legal text.** Décret n° 2020-1753, which the
licence cites, governs compensation thresholds and declaration procedures and
**does not approve this licence**. The authoritative text is a **14-page PDF,
"Version au 03.02.2021"**, reachable only through the dataset page's own
licence link → the FabMob wiki → `https://cloud.fabmob.io/s/CJCEzKosfqqNBEx`.

**It is ODbL-derived but NOT ODbL-compatible.** Art. 5.5(a)(iii) allows "une
licence compatible", but **no compatible list and no proxy has ever been
published**, so share-alike cannot be discharged by relicensing under ODbL.

---

## VERDICT: PERMITTED WITH CONDITIONS

Art. 3.1 grants « une licence mondiale gratuite, non-exclusive et résiliable
[…] d'Utilisation », and *Utiliser* is defined to include
« **l'affichage public** et la préparation d'œuvres dérivées ». **Redrawing
line geometry and station points is squarely permitted, commercial use
expressly included.**

### Which category a rendered map falls into

- The rendered heatmap HTML is a **« Création Produite »**.
- **Art. 5.6(b) is explicit that a Produced Work does NOT create a Derivative
  Database** — so the map alone triggers the Art. 5.4 notice and **not**
  share-alike.
- ⚠️ **But this project commits `outputs/<city>/` to a public repository**, and
  Art. 5.5(b) says extracting a substantial part into a new database *is* a
  Derivative Database. The station CSV is same nature, same granularity, same
  geographic footprint as `stops.txt`.

The NAP's own published interpretation — imported wholesale by Art. 5.6(d)'s
footnote — contains an example that is almost verbatim this project:

> **"Calcul de la distance à l'arrêt de bus le plus proche pour une liste de
> commerces"** — filed under **"Non"**, no resharing required.

**Resolution: do the republication anyway.** One upload as a *ressource
communautaire* moots the question entirely and costs less than the argument.

---

## MUST DISPLAY

Art. 5.4, with the licence's own safe-harbour wording (prefaced « Exemple de
mention. Le message suivant répond aux exigences », so it *satisfies* rather
than being mandated verbatim):

**Paris:**
> Contient des informations de Réseaux urbains et interurbains d'Île-de-France
> Mobilités (IDFM), présentement mises à disposition aux conditions de la
> « Licence Mobilités »

**Lyon:**
> Contient des informations de Réseau urbain TCL, présentement mises à
> disposition aux conditions de la « Licence Mobilités »

⚠️ **Art. 5.4(a) prescribes the LINKING, not just the text.** The database name
must hyperlink to the dataset URI and « Licence Mobilités » must hyperlink to
the licence text. If hyperlinks are impossible, the full text must be inlined.

**Lyon additionally — Grand Lyon CGU Art. 6.1**, three elements:
source `data.grandlyon.com`, producer `SYTRAL Mobilités`, **and the date the
reused data was last updated**.

**Both cities — règlement MMTIS Art. 8(3):** the **update interval** of the
static data must be indicated.

> ⚠️ **A date-of-update and an update-interval are NEW obligation shapes for
> this project.** No existing notice carries either. They are not attribution.

---

## MUST DO — acts no notice discharges

| # | Obligation | Channel | Blocking? |
|---|---|---|---|
| **a** | Republish a qualifying Derivative Database on the NAP, « sous le jeu de données initial, dans le format d'origine » (Art. 5.6(d)) | ressource communautaire; needs a data.gouv.fr account | No — but do it to moot the share-alike question |
| **b** | **Report errors found in the source data**, « sans délai » (Art. 5.6(d) + MMTIS 4(5)) | IDFM `contact-prim@iledefrance-mobilites.fr` · SYTRAL `contactopendata@tcl.fr` | **No** — a data-quality duty, not a permission gate |
| **c** | **Supply modifications to recipients** (Art. 5.8) — the whole derived DB, or all modifications, **or the method (« comme un algorithme »)** | A public repo with the pipeline code and derived CSVs, **linked from the site** | No — already nearly satisfied, but must be deliberate |
| **d** | **Annual déclaration de conformité** (L. 1115-5 code des transports) | `demarche.numerique.gouv.fr` · regulator `donnees-mobilite@autorite-transports.fr` | ⚠️ **Applicability UNRESOLVED** — see below |
| **e** | **Lyon: create an account on `data.grandlyon.com` before any download** | `data.grandlyon.com/portail/fr/connexion` | ⚠️ **HARD BLOCKER** |

**Art. 5.8's trigger is broader than share-alike's.** It fires on « une Base de
données dérivée **ou une Création obtenue depuis une Base de données
dérivée** » — so a published map made from a derived station table triggers it
**even though 5.6(b) says the map is not a Derivative Database**.

---

## MUST NOT SAY — and here it is the INVERSE of MTA/WMATA

**There is no clause forbidding claims of accuracy or completeness.** Art. 9.1
disclaims warranties but binds the *Concédant*, not this project's speech.

Instead, Art. 5.7 « Neutralité et loyauté » imposes the opposite duty, and it
bites twice:

> « Le Licencié ne doit pas procéder à une utilisation […] qui aurait pour
> effet ou pour objet d'induire en erreur les tiers quant au contenu de
> l'information **et à sa date de mise à jour** »

1. **A pre-rendered static map built from a frozen GTFS snapshot is precisely
   "misleading as to the update date" unless the snapshot date is shown.** That
   makes the date element above a *substantive requirement*, not a courtesy.
2. Art. 5.7 also requires reuse founded on « l'**exhaustivité** des données
   disponibles », qualified by a relevance proviso. This project's deliberate
   exclusions — commuter rail, `sub_transit_line_filters.md`, dropped route
   types — are covered by the proviso, **but the page should state what was
   excluded rather than leave it implicit.**

---

## ⚠️ Three things deliberately NOT resolved

**1. Lyon's bar on distinctive signs collides with a project invariant.**
Grand Lyon CGU Art. 6.2:

> « Tout usage des marques, logos, ou signes distinctifs de la Métropole de
> Lyon ou des Producteurs de données, associés ou non à l'utilisation des
> données, est interdit sauf autorisation préalable. »

**Far broader than SEPTA's**, which claimed only its Logo: this covers
*signes distinctifs* of the **producers** too, and applies « associés ou non ».
This project's invariant requires **every drawn line to carry its real public
name plus a legend entry** — and Lyon's would say **TCL**.

- *Permits:* nominative use identifying the thing depicted; licence Art. 2.3(c)
  says the licence does not extend to trademarks, leaving ordinary nominative
  reference intact; SYTRAL's own page declares **"LIMITE D'UTILISATION: Non
  renseigné"**.
- *Does not permit:* "TCL" is plainly a *signe distinctif* of the producer,
  Art. 6.2 has no nominative-use exception, and « associés ou non » is as close
  to "including on a map made from our data" as the clause gets.

**Prior authorisation is obtainable at `contactopendata@tcl.fr` — a cheap
request relative to the exposure.**

**2. Lyon carries an INDEMNITY — the project's second, after Hong Kong.**
Grand Lyon CGU 9.4: a third-party claim against the Métropole or a data
producer arising from the user's use leaves the user to bear the financial
consequences alone. Open-ended, attached to an otherwise free grant. **IDFM has
no equivalent** — only sole-responsibility wording.

**3. Whether this project is an « utilisateur de données » under L. 1115-5**,
and so owes the annual declaration. The NAP's framing is broad ("toute autre
entité"), but the regulation is written around route planners and travel-
information services. **A static commercial-density map is neither.** Worth
asking rather than assuming, because the answer creates a *recurring annual*
obligation.

---

## The publisher divergence to record, not adopt

**IDFM's own licences page contradicts the NAP**, in this project's favour:

> « Île-de-France Mobilités a choisi de mettre à disposition ses données de
> référence, décrivant notamment la structuration du réseau de transport
> (référentiel des arrêts et des lignes, **tracés du réseau ferré**, etc.) sous
> « licence Ouverte » »

…reserving Licence Mobilités for « données de passages théoriques ou en temps
réel », **which this project does not publish**. The NAP nonetheless stamps
`mobility-licence` on the whole dataset. **SYTRAL does the opposite**, folding
« les informations géographiques associées (topographie du réseau) » into its
Licence Mobilités declaration.

**Posture: comply with Licence Mobilités for both.** It is the stricter reading
for Paris, it is satisfiable, and it avoids depending on a divergence that
could be tidied either way.

⚠️ **IDFM's network maps and plans are CC BY-NC-ND 3.0 France** — no commercial
use, no modification. Redrawing from *data* avoids this entirely, but **no IDFM
plan or schematic may be used as a source or overlay.**

---

## Website-terms vs data-terms — both found, both reported

Per `read-licence` step 4, neither is picked silently:

- **Grand Lyon mentions légales** reads « Les reproductions, les transmissions,
  les modifications, les réutilisations à des fins publicitaires, commerciales
  ou d'information, de tout ou partie du site, sont totalement interdites. »
  **Read in isolation this looks fatal. It is not** — its scope is « dudit site
  et des œuvres qui y sont reproduites », and databases sit under a separate
  heading that imposes **no reuse position**. **This is the New York footer
  again.**
- **IDFM CGU Art. 8** prohibits extraction of a substantial part of **the
  PLATFORM** and expressly carves out the data: « A l'exception des DONNÉES
  mises à disposition ». Art. 4 confirms the right « De corriger, modifier,
  enrichir les DONNÉES ».
- Hierarchy is declared at IDFM CGU Art. 12.1: **Convention > Licence > CGU.**

**Incorporation by reference was found in three places and all were opened** —
the licence preamble subordinates reuse to the platform CGU, and both CGU
assert acceptance by use.

---

## Two feed facts that are not licence questions but block the build

- ⚠️ **Lyon's NAP feed is DEAD.** Its GTFS, NeTEx and PDF resources all show
  **0% availability**, last content modification **2022-04-14**. SYTRAL's own
  portal shows the data current at **2026-09-22**. **The NAP copy is a stale
  mirror** — the exact trap Toronto's TTC feed set. Lyon must come from
  `data.grandlyon.com`, behind the account wall.
- ⚠️ **Paris's GTFS provenance needs settling.** The agent reports the NAP
  dataset carries no *official* GTFS — only NeTEx, SIRI Lite, and a community
  "GTFS modifié" published by Google from an Apigee URL. A direct read of the
  API did list `eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip` alongside the
  ITO World and Apigee copies. **These two readings disagree and it is not
  settled**: the difference is whether those sit in `resources` or in
  `community_resources`. **Building Paris from a third party's modified copy
  under an unverified licence is not acceptable** — resolve before fetching.

---

## Revocability

Art. 11.1 terminates the licence **de plein droit, sans préavis** on any breach
of conditions. Art. 5.2 requires reuse compatible with the authority's mobility
strategy (IDFM names the SDRIF and the PDUIF), with a remediation window of
**not less than three working days** before suspension. A transit-accessibility
map aligns with « le développement du transport collectif », so the risk is
low — **but this is a revocable grant, unlike Licence Ouverte.**
