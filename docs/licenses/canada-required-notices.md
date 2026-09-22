# Notices Canada requires — PROMOTED, and this file is now the trail

**SUPERSEDED 2026-09-22.** Written 2026-09-21 during the screen, when no
Canadian city was built. It is no longer the place to read a Canadian notice
from: all six municipalities are built, and the live obligations are
`docs/data_sources.md`, "Notices this project MUST display when published",
**items 9–17**, with the exact strings in `app/components.py`'s `_NOTICES`.
**Where this file and those disagree, those win.**

The promotion it asked for happened, and it took a day longer than it should
have, which is the part worth keeping. This file said: "**promote the relevant
entries into that list the moment a Canadian city is committed**, and not
before, so the gate stays a list of things that actually apply." The cities
were committed on 2026-09-21 and the notices did go in that day. What did not
was everything else — the endpoints never reached the three provenance tables,
the feeds never reached the GTFS licence table, and one publisher was never
read at all. **An instruction that names one artefact gets that one artefact
done.** `scripts/check_provenance.py` now checks all of them at once, and
`.claude/skills/add-country/` says to run it.

**One notice was MISSING entirely, not merely unpromoted.** This file lists the
municipal publishers and TransLink. It does not mention the **Province of
British Columbia**, whose ABMS municipalities layer names the 30 out-of-city
SkyTrain stations — because the screen looked for business, transit and
boundary sources per city, and the naming layer is a fourth kind of input that
belongs to no city. It is now item 17. That is the single most useful thing in
this file's history: a country profile organised by city will miss a source
that is not a city's.

What is still worth reading below: the TransLink two-legends trap, the
municipal OGL wording differences (en dash versus hyphen, "Licence" versus
"License"), and Montréal's two-owners split. Those were right when written and
are unchanged.

---

## What this file got right, and what the live list corrected

| Claim here | Status |
|---|---|
| TransLink mandates two different legends; the GTFS one is "Route and arrival data…" | **Held.** Item 11 |
| Four municipal OGLs, each with its own prescribed sentence, none interchangeable | **Held.** Items 9, 10, 14, 16 |
| Montréal needs TWO credits, City and STM, because the owners differ | **Held.** Items 12 and 13 |
| Toronto, Vancouver, Calgary and Surrey all terminate automatically on breach | **Held**, and BC's does too |
| Edmonton requires nothing | **WRONG.** Corrected 2026-09-21: the obligation is the URL clause, not the credit clause. Item 15 |
| Canada's publishers are municipal | **INCOMPLETE.** The Province of British Columbia is one too. Item 17 |

---

## TransLink — Vancouver AND Surrey, as one regional build

Surrey has no rail of its own; SkyTrain is TransLink's, so **one transit
licence covers both cities** and a regional build inherits it once, not twice.

**1. The Legend, prominently displayed, in exactly this wording:**

> "Route and arrival data used in this product or service is provided by
> permission of TransLink. TransLink assumes no responsibility for the accuracy
> or currency of the Data used in this product or service."

**THE TRAP: TransLink has two different mandated wordings, and this is the GTFS
one.** The Open API terms mandate a *different* legend beginning "Some of the
data used in this product or service…". This project uses static GTFS, so the
"Route and arrival data" wording is the correct one. Using the API wording
would not satisfy the GTFS terms. Both texts are stored here —
`translink-gtfs-static-terms-of-use.txt` is the operative one;
`translink-open-api-terms-of-use.txt` is kept only because it *looks* like it
governs and does not.

**2. No TransLink marks beyond that legend.** "Other than displaying the
Legend, you are not authorized and are prohibited from, making use of
TransLink's domain name or any trademarks or official marks, which are owned by
TransLink or any confusingly similar variation of the domain name or those
marks." The project satisfies this by construction — it draws its own geometry
from `shapes.txt` and reproduces no roundel — but SkyTrain line names in plain
text are the thing to keep an eye on.

**3. Be responsive if TransLink asks who you are.** "You must provide TransLink
sufficient information as TransLink may request to identify you, your
organization or company, who will be using the Data, where it will be
distributed and whether the use of the data is for non-commercial or commercial
purposes."

This is an obligation to answer, **not a precondition of use** — the GTFS terms
contain no counterpart to the Open API's "In the event that TransLink, in its
entire discretion, approves you as a user of the Data…". That reading is a
judgment call of the same class as LA Metro's modification clause and CTA's
purpose limitation, both of which the project owner decided explicitly. **It
should be recorded in `DECISIONS.md` as a stated position before Vancouver or
Surrey is built**, not left as an assumption inherited from this file.

---

## Municipal business-data notices, per city

Four of the five are the same Open Government Licence template, each with its
own prescribed sentence. Use the city's own wording; they are not
interchangeable.

| City | Required? | Exact wording |
|---|---|---|
| **Toronto** | Yes | `Contains information licensed under the Open Government Licence – Toronto.` |
| **Vancouver** | Yes | `Contains information licensed under the Open Government Licence – Vancouver.` |
| **Calgary** | Yes | `Contains information licensed under the Open Government Licence – City of Calgary.` |
| **Surrey** | Yes | `Contains information licensed under the Open Government License - City of Surrey.` |
| **Edmonton** | **No** | Credit is "not required" but is "encouraged". Edmonton instead requires that if you distribute the *datasets*, you include the Terms of Use URL and bind recipients "without introducing any further restrictions of any kind" |
| **Montréal** | Yes, and broader than the others | See below |

**Toronto, Vancouver, Calgary and Surrey all also terminate automatically on
breach** — "if you fail to comply with any of them, the rights granted to you
under this licence… will end automatically." The notice is not cosmetic.

---

## Montréal — two attributions, and a broader condition

**Two different credits are required for one city**, because the business data
and the transit data have different owners:

- **Business data** (`locaux-commerciaux`, CC-BY 4.0) — credit the **Ville de
  Montréal**.
- **STM transit data** — the dataset's own notes state it is STM's property
  and that "selon la clause d'attribution de la licence Creative Commons 4.0,
  la paternité des données doit être attribuée à la Société de transport de
  Montréal." Credit **STM**, not the City.

**Montréal's attribution condition is broader than standard CC-BY.** The portal
licence requires that you "créditer les données et les contenus que vous
utilisez et préciser si des modifications ont été effectuées **ou si des
interprétations en ont été tirées**" — state whether modifications were made
*or interpretations drawn*. This project plainly draws interpretations: ring
density, category buckets, storefront filtering. A bare "data from the Ville de
Montréal" would not meet it; the notice has to say that the map interprets the
data.

Montréal also requires no suggestion of endorsement, and prohibits restricting
access to the original data by legal or technical means.

---

## Summary: what a Canadian build adds to the gate

| If you build | Notices added |
|---|---|
| Montréal | 2 — Ville de Montréal (with the interpretation clause), STM |
| Vancouver | 2 — OGL–Vancouver, TransLink Legend |
| Surrey | 2 — OGL–City of Surrey, TransLink Legend *(shared with Vancouver)* |
| Vancouver **+** Surrey as one regional build | 3 — both city licences, **one** TransLink Legend |
| Calgary | 1 — OGL–City of Calgary (covers business data *and* Calgary Transit) |
| Edmonton | 0 required |
| Toronto | 1 — OGL–Toronto (covers business data *and* TTC) |

The US cities already require four notices, one of which is satisfied. Canada
would roughly double that, so the notices section needs to stay a list rather
than becoming prose.
