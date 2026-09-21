# Philadelphia: drafted permission request (NOT YET SENT)

**Status: drafted 2026-09-21, awaiting the owner to send.** Nothing in this
project claims a request is outstanding until it actually is — the site footer
and `data_sources.md` say only that the question is unresolved, which stays
accurate either way.

## Why this exists

The City of Philadelphia's open datasets carry a named "City of Philadelphia
License" that grants nothing and forbids nothing. But each dataset page opens
with:

> "Browsing City data on this site constitutes acceptance of the license, **the
> City's terms of use** and your agreement to be bound by them."

That incorporates <https://www.phila.gov/terms-of-use/> by reference, and those
terms say:

> "Permission is granted to residents and citizens of the City of Philadelphia
> to copy electronically and to print single pages from the Website for the sole
> purpose of sharing information on the Website with other citizens and
> residents … exactly as presented on the Website, without any addition or
> modification. **Distribution or republication in any other form or for any
> other purpose, including any commercial purpose or use, and any modification
> whatsoever, are strictly prohibited without the prior written permission of
> the City.**"

Applied to a dataset and read literally, that does not permit this project's
Philadelphia map, which filters the licence register and redraws it. The City's
own terms name written permission as the route, so this asks for it.

**The interim position while this is outstanding** is recorded in
`DECISIONS.md`: the map stays up under a reasoned reading, the footer discloses
that the question is unresolved, and Philadelphia comes off the site if the City
confirms the restrictive reading. See `data_sources.md`, "what does silence
mean?".

## Where to send it

**To: `maps@phila.gov`** — the contact the City publishes on its Open Data
Program page (1234 Market St, 15th Floor). This is a question about City-wide
terms, so it belongs with the programme rather than with one dataset's
custodian.

**CC: `LIGISTEAM@phila.gov`** — the L&I GIS team, maintainer of the Business
Licenses dataset, so the custodian of the data actually used sees it.

Checked 2026-09-21. An earlier draft of this file sent it to `LIGISTEAM` alone,
which was the right address for the wrong desk: a dataset maintainer cannot
speak to what the City's terms of use cover. The other dataset used, City
Limits, has a different custodian again — a named officer in the Department of
Planning and Development, listed publicly on its dataset page with a phone
number — who is worth contacting only if Planning specifically needs to weigh
in. That dataset is also the one marked "Usage: Public use; Free".

**Do NOT send this to `info@opendataphilly.org`.** OpenDataPhilly is not the
City: by its own About page it is "built by Azavea, a Philadelphia-based
geospatial software firm" and catalogues "both municipal and non-municipal
data". It cannot grant or interpret the City's permissions — and see the note
below, because that fact cuts the other way too.

## A factor that came out of checking the contacts, and then collapsed

**Raised and then withdrawn the same day — recorded because the withdrawal is
the useful part.** The sentence this question rests on ("Browsing City data on
this site constitutes acceptance of the license, the City's terms of use ...")
appears on an **OpenDataPhilly** dataset page, and OpenDataPhilly is not the
City: it is "built by Azavea, a Philadelphia-based geospatial software firm".
That looked like it weakened the hook — terms asserted by a private catalogue
rather than by the City in its own voice.

**It does not hold up.** The City runs its own data catalogue at
`metadata.phila.gov`, a phila.gov subdomain on the City's own infrastructure,
and that catalogue's own "Terms of use" link points straight at
<https://www.phila.gov/terms-of-use/> — the same document containing the
prohibition. So the City does make the connection in its own voice, on its own
property, independently of Azavea. The third-party-portal argument is dead and
should not be revived.

**This made the case for asking stronger, not weaker**, which is the opposite of
what checking it was expected to do.

## Draft

> Subject: Permission request — reuse of L&I Business Licenses and City Limits
> open data in a non-commercial mapping project
>
> Hello,
>
> I maintain a small non-commercial project that maps how retail, food-service
> and personal-service businesses cluster around rail-transit stations across
> nine US cities. Philadelphia is one of them. It is a portfolio piece: there is
> no advertising, no fee, nothing is sold, and no user data is collected.
>
> It uses two of the City's open datasets:
>
> - Licenses and Inspections Business Licenses (`business_licenses`, via the
>   Carto SQL API)
> - City Limits (`City_Limits`, Department of Planning and Development)
>
> What the project does with them: it filters the licence register to active
> storefront categories, classifies each licence type into one of three
> categories, drops records it judges not to be storefronts, and renders the
> result as a density map showing each business's registered trade name at its
> mapped location. The rendered map is published on a public website and its
> generated output files are committed to a public GitHub repository. It states
> plainly that the data is a snapshot of a public register on a retrieval date
> rather than a complete or current picture, and it lists every exclusion it
> makes.
>
> My question is about which terms govern that use. The datasets carry the
> "City of Philadelphia License", which reserves the City's rights but does not
> address reuse. The dataset pages also state that browsing City data
> constitutes acceptance of the City's terms of use, and those terms prohibit
> "distribution or republication in any other form or for any other purpose …
> and any modification whatsoever" without the City's prior written permission.
>
> Read literally and applied to a dataset, that appears to prohibit what this
> project does. Read as terms written for the pages of phila.gov — which is how
> they are drafted, referring to printing single pages exactly as presented —
> they would not reach the open data at all, and the dataset licence would
> govern instead.
>
> So, two questions:
>
> 1. Do the phila.gov Terms of Use apply to datasets published through
>    OpenDataPhilly, or does the "City of Philadelphia License" govern their
>    reuse?
> 2. If the Terms of Use do apply, may I have written permission for the
>    non-commercial use described above — filtering, classifying and publishing
>    a derived map, with the generated output committed to a public repository?
>
> If the answer to the second is no, I will remove Philadelphia from the
> project promptly and without argument; I would rather ask than assume. If
> there is attribution wording the City would like displayed, I will add it
> exactly as given.
>
> Thank you for your time, and for running the Open Data Program.
>
> [your name]
> [your contact email]
> [link to the site]
> [link to the repository]

## When a reply arrives

- **Permission granted, or the Terms of Use confirmed not to apply:** record it
  in `DECISIONS.md`, move the Philadelphia rows in `data_sources.md` from "open
  question" to established, quoting the reply, and delete the Philadelphia
  clause from `components._UNSETTLED_TERMS` — at which point that footer
  paragraph has no live subject and should come out entirely.
- **Permission declined, or the restrictive reading confirmed:** Philadelphia
  comes off the site. That means its page, its `cities.py` entry, its
  `outputs/philadelphia/` directory and its macro-map marker — and the label
  offsets of the remaining eastern cities want re-checking at 854/1200 px
  afterwards, because removing a marker changes `fit_view`'s bounds. Record what
  was removed and who asked, per the standing commitment.
- **No reply:** the interim position already covers this. Do not let silence
  harden into a claim that permission was given.
