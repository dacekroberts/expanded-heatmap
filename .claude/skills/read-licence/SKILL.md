---
name: read-licence
description: Establish what a data source's terms actually permit, before building on it or publishing anything derived from it. Follows every pointer a licence makes, separates website terms from dataset terms, and looks for terms incorporated by reference. Use when adding a source, when a licence position is recorded as unresolved, or before a public deploy - not for re-reading a source whose terms are already established in docs/data_sources.md.
---

# Reading a data source's licence

Every correction this project has made to a licence position came from opening
a page an earlier review had merely **cited**. Not from misreading a document —
from not reading a document that the first one pointed at. This skill is that
one failure mode, turned into a procedure.

Record the outcome in `docs/data_sources.md` as you go, per `add-city` Step 0.4.
Terms are not established until they are written there with the date.

## The three corrections this exists to prevent

Read these first. They are the same mistake three times, and knowing the shape
is most of the skill.

**New York.** The nyc.gov footer says "All Rights Reserved", which made the
city's datasets look prohibited. The footer covers **nyc.gov's own website
content**. Local Law 11 of 2012 in fact *forbids* the City from attaching a
licence or usage restriction to its open data — so the missing licence field
was compliance, not an omission.

**SEPTA.** Its licence carries one restrictive-looking sentence: "Licensee may
not use SEPTA's trademarks and copyrighted materials for any commercial or
profit-making use." A portfolio site looked exposed. But that sentence points
at SEPTA's Copyright and Trademark Notice, which nobody had opened, and:

- the **Trademark Notice is one sentence** — "The SEPTA Logo is a registered
  trademark" — so line names and route colours are not claimed at all;
- the **"informational and non-commercial purposes only"** wording lives in the
  same notice's *Web Contents and Materials* section, governing "documents and
  related graphics from this ... Server", i.e. septa.org's pages;
- meanwhile the **datasets carry an express grant** in the paragraph above:
  "a non-exclusive, non-assignable, non-transferable, limited and revocable
  right to **use, reproduce and redistribute** the datasets".

So the dataset was licensed the whole time, and the constraint that looked
fatal belonged to a different document about a different thing.

**Philadelphia.** The named "City of Philadelphia License" grants nothing and
forbids nothing, so this was filed as a silence question. What had not been read
is the sentence its dataset page **opens** with: "Browsing City data on this
site constitutes acceptance of the license, **the City's terms of use** and
your agreement to be bound by them." That incorporates `phila.gov/terms-of-use`
by reference, and those terms prohibit "distribution or republication in any
other form or for any other purpose ... and any modification whatsoever"
without written permission. The position inverted from *silence* to
*prohibition*.

And one in the other direction, which is why step 2 below matters even when you
expect nothing: **Miami-Dade** was recorded as "the only one where no agency
document exists to read, so settling it means asking the County." One does —
the Open Data Hub's own Terms of Use, two clicks from the portal footer. It
contains only an accuracy disclaimer, which turns "we found nothing" into "the
County's own terms impose no restriction": a materially stronger position,
reached by reading.

## Procedure

### 1. Get the declared licence from the machine, not the page

- **Socrata**: `curl -s "<domain>/api/views/<id>.json"` and read `license`,
  `licenseId`, `attribution`, `attributionLink`. `SEE_TERMS_OF_USE` means go
  read the terms page. **A missing `license` does not mean permissive.**
- **ArcGIS**: `<service>?f=json` and read `licenseInfo`, `accessInformation`,
  `copyrightText`. `licenseInfo` is very often an *accuracy* disclaimer with
  nothing about reuse — note that explicitly rather than treating it as terms.
- **CKAN**: `package_show` and read `license_id`, `license_title`.
- **GTFS**: `feed_info.txt` almost never carries a licence (LA Metro's
  `feed_license` column is empty), so go to the agency's developer terms. Line
  geometry gets redrawn into the map, so these bear directly on what is
  published — and they have been the loosest end of every review here.

### 2. Follow every pointer, and treat a citation as unread

Any of these phrases means there is another document and you have not read it:

> "see our X notice" · "subject to" · "in accordance with" · "as described at"
> · "governed by" · "for the full text"

**Open it. Every time.** SEPTA's trademark question was answered by one
sentence on a page its own licence linked.

### 3. Grep the dataset page for incorporation by reference

This is the step that would have caught Philadelphia, and the one most easily
skipped because the dataset already has a named licence.

Search the dataset's page text for:

> "constitutes acceptance" · "agree to be bound" · "by using this site" ·
> "your use of" · "terms of use" · "acceptance of"

If any of them names a second document, **that document is part of the terms**,
and it may be far more restrictive than the licence field. Read it, and quote
the operative sentence.

### 4. Ask, for every document: does this describe web pages, or data?

The single most useful question in this skill. Tells apart a site footer from a
dataset licence, and it is answerable from the document's own language.

**Written for web pages** — treat as governing the website, not the data:

- "print single pages", "exactly as presented", "copy electronically"
- "design, text, sound recordings and images", "documents and related graphics"
- "this World Wide website", "this Server", "pages and sub pages"

**Written for data** — treat as governing reuse:

- "datasets", "the database", "redistribute", "modify", "derivative works"
- "attribution", "API", "feed"

Where a web-page document and a data licence both appear to apply, say so
plainly and record both. Do not pick the convenient one silently.

### 5. Check whether the portal is the publisher — and then check the publisher's own

A third-party catalogue asserting terms is weaker than the publisher asserting
them. But **verify the publisher separately, because it may say the same
thing.** This is a trap worth naming: for Philadelphia, noticing that
OpenDataPhilly is "built by Azavea, a Philadelphia-based geospatial software
firm" looked like it weakened the incorporation — until the City's **own**
catalogue at `metadata.phila.gov`, a phila.gov subdomain, turned out to link
the same Terms of Use. The argument collapsed within the hour of being made.

### 6. Capture what must be DISPLAYED, separately from what is permitted

This is the part that becomes work rather than a note. Anything requiring
specific text goes in `docs/data_sources.md` under "Notices this project MUST
display when published", **verbatim where the terms prescribe wording**:

- Chicago requires a verbatim disclaimer.
- SFMTA requires specific attribution wording.
- LA Metro and MassDOT require acknowledgement as provider, no wording
  prescribed.
- WMATA requires **nothing** — which corrected a prediction in this project's
  own notes that it would add a sixth notice.

And three adjacent categories that are not notices but are still work:

- **What may not be SAID.** MTA's and WMATA §6's identical clause forbids
  stating or implying the data an application provides "is accurate, complete,
  or timely". That is a cross-city prose rule, not a footnote — it has already
  caught two claims on one city page.
- **Trademark and affiliation.** Six agencies here bar implying affiliation,
  sponsorship or endorsement. Check whether the terms claim **marks** (a logo)
  or something broader; SEPTA's claims only its Logo.
- **What must be DISCLOSED about your own processing.** A recurring family,
  found by the 2026-09-21 global country screen, and **this project triggers it
  every time**: ring density, category bucketing and storefront filtering are
  all transformations and interpretations.
  - **Montréal** requires crediting the data *and* stating whether
    modifications were made **"ou si des interprétations en ont été tirées"** —
    or whether interpretations were drawn from it.
  - **Mexico's INEGI** requires you to *"notificar al usuario final de
    cualquier análisis o transformación que haga a la información"*, and
    separately that the presentation must not suggest INEGI made the change.

  **A bare source credit does not satisfy either.** The notice has to say that
  the map interprets the data. Treat "attribution" and "disclosure of
  transformation" as two different obligations and check for both, because a
  licence can require the second while granting the first freely.

### 6b. Check whether the publisher already did the privacy work

Before designing a residence filter or a name-suppression rule, check whether
the register is **already stripped at source**. Several are, and the work is
then done:

- **France** masks `diffusion status = P` records — the sole trader's name, the
  commune address **and the geolocation**.
- **Edmonton** publishes `<REDACTED FOR PRIVACY>` in place of the address on
  **9.3%** of rows.
- **Austria's GISA** publishes active trade licences **without personal data**
  — and, as it turns out, without a street address either, which is why Austria
  failed this project's premises test. Upstream stripping can remove what you
  needed along with what you did not: **check what survived, not just what was
  removed.**

This cuts both ways and is worth a minute either way: it can save building a
filter, or it can disqualify a source that looked complete.

### 7. Where a page blocks fetching, use the browser

Chicago's data terms return 403 to a plain fetch. Every item in this project's
licence review was resolvable in the browser except one. Do not record "could
not read" until the browser has failed too.

### 8. State the outcome in one of four ways

Never leave a position implied. Write one of:

- **PERMITTED** — quote the granting sentence.
- **PERMITTED WITH CONDITIONS** — quote them, and add any display requirement
  to the notices section.
- **SILENT** — the authoritative pages were read and impose no reuse position.
  Name which pages, so this is an established absence rather than an
  unexamined gap. Miami-Dade is the worked example.
- **NOT PERMITTED, or ambiguous in a way that matters** — quote the
  prohibition, say which reading would permit the use and which would not, and
  **do not resolve it in this project's favour.** Raise it. Philadelphia is the
  worked example: the map stays up on a disclosed reasoned position with a
  written request outstanding, and comes down if the publisher confirms the
  restrictive reading.

## Two standing rules this skill does not get to weaken

- **A government open-data portal is a reason to expect permissive terms, not
  evidence of them.** Los Angeles' business registry is CC0 while its GTFS
  forbids modifying the data — both from the same city.
- **A removal request is honoured, not argued.** Finding that something is
  permitted is never a reason to insist on publishing it. See
  `docs/data_sources.md`, "Commitment: removal requests are honoured, not
  argued".
