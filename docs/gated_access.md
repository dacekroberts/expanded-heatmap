# Gated sources — every city that needs a key, an account, or a letter

**What this file is for.** Some cities are not blocked by data and not blocked
by code, but by something only a person can do: register an account, obtain an
API key, or send a notification to a publisher. Those items are invisible in
the master list, because a city waiting on a letter looks exactly like a city
waiting on a probe. This is the list to come back to and tick off.

**Three of these apply to cities that are already BUILT AND PUBLISHED** — items
1, 2 and 12. Items 1 and 12 are ongoing obligations rather than one-off steps;
item 2 is one act, drafted and waiting to be sent. They are first for that reason.

Status values: **OPEN** (nothing done) · **DONE** (satisfied, no upkeep) ·
**STANDING** (satisfied but must stay satisfied) · **MOOT** (the city or route
was dropped, kept for the record) · **OPTIONAL** (an upgrade, not a blocker).

---

## A. Live obligations on cities already published

| # | City | What is required | Status |
|---|---|---|---|
| **1** | **Washington D.C.** 🇺🇸 **BUILT** | **A live WMATA API account, for as long as the D.C. page is up.** `api.wmata.com` is the only feed in this project behind a key (401 unauthenticated). The terms are an *API agreement*: §9(i) terminates the grant when the account goes, and what lapses is the right to **publish the page**, not merely to store a file | ✅ **SATISFIED — the owner re-confirmed the account live on 2026-09-22**, stated directly. **STANDING thereafter:** do not terminate it while the site is up. Now **gate item 10** in `data_sources.md`, so it is checked before every deploy rather than remembered |
| **12** | **Philadelphia** 🇺🇸 **BUILT** | **A written request to the publisher, outstanding.** `phila.gov/terms-of-use` is incorporated by reference into the dataset page and prohibits redistribution and modification without written permission | ⚠️ **OPEN** — the map stays up on a *disclosed reasoned position*, and **comes down if the publisher confirms the restrictive reading**. Not resolvable by more reading; someone has to ask |

---

## B. Notification owed to a publisher

| # | City | What is required | Status |
|---|---|---|---|
| **2** | **Barcelona** 🇪🇸 **BUILT AND LIVE** | **Inform the City Council of the project.** Verbatim: *"Users are required to inform Barcelona City Council of every project relating to or derived from their use of the data sets."* The clause's own tail — *"so that they are open to the public"* — makes it a **reuse-showcase notification, not a permission gate**, so publishing did not wait on it | 🟠 **DRAFTED, NOT SENT.** See `docs/notifications/barcelona-city-council.md`. **Both preconditions are met**: the live terms were re-read by the owner in a browser on 2026-09-22, past the hCaptcha this project does not defeat, and the clause is unchanged word for word; and the site is public. The terms name their own channel — *"Any doubts or comments on these Terms of use may be forwarded to the following link"*, which redirects to `atencioenlinia.ajuntament.barcelona.cat`. ⚠️ **SENDING WAS ATTEMPTED TWICE ON 2026-09-22 AND BOTH FAILED**: the portal's own contact form stalled after its hCaptcha, and that named channel timed out from the owner's network and independently from a session. **The host is down, not blocking us** — `seuelectronica.ajuntament.barcelona.cat` answers HTTP 302 in 2.4s from the same /24. The fallback is closed too: the electronic registry requires a Spanish digital certificate. No email exists to fall back on either — the dataset's CKAN metadata carries no contact address and `datos.gob.es` names only a web form. **The clause sets no deadline**, so the plan is to retry when the service returns; the attempt log is in the notifications file |

---

## C. Free account or API key needed before a build can start

| # | City / source | What is required | Status |
|---|---|---|---|
| **3** | **Copenhagen** 🇩🇰 | **A free account** for Danish CVR bulk distribution — `distribution.virk.dk` answers **401**. The data itself is right (P-enheder, each with its own address and `industrycode`) | 🟡 **OPEN** — blocks the build entirely. Tier 3, one city |
| **4** | **Prague** 🇨🇿 | **An API key** — `api.golemio.cz` returns **401**. The business leg (`rzp.cz`, the *živnostenský rejstřík*) is live and is the right shape: Czech trade licences are issued **per premises**. Golemio is the transit half | 🟡 **OPEN** — Czechia is the strongest of the four Tier 4 probes |
| **5** | **Barcelona** 🇪🇸 — TMB | **A free TMB developer account** at `api.tmb.cat` (`app_id` + `app_key`); unauthenticated it returns *"Authentication failed. Authentication parameters missing"* | 🟢 **OPTIONAL** — the brief **chose OSM instead** and validated it (TMB 22 relations, TRAM 22, FGC 10). A key would be an upgrade to first-party geometry, not a prerequisite |
| **6** | **Spain — National Access Point** | **A free account**; `nap.mitma.es` answers **401**, the WMATA shape | 🟢 **MOOT for Sevilla** (city discarded — and it published its own metro openly anyway). Kept because it is the fallback rail route for any *other* Spanish city |

---

## D. Licence questions only the publisher can answer

These are not access problems. The data fetches; what is unknown is whether we
may publish it. `read-licence` step 8: **do not resolve an ambiguity in this
project's favour.**

| # | City | The question | Status |
|---|---|---|---|
| **7** | **Stockholm** 🇸🇪 | ~~`dataportal.se` says restricted while the ArcGIS item says public~~ — **re-read 2026-09-22 and the conflict mostly dissolves.** `dataportal.se` is the **harvester**; the publisher's own Hub DCAT feed declares **`accessLevel: public` on all 109 datasets**, with CC0 on 8 and blank on the rest. `read-licence` step 5 gives the publisher precedence over a third-party catalogue | 🟢 **NOT a letter — position is SILENT** (the Miami-Dade shape). Still unread: the walled `dataportalen.stockholm.se` record (**try the Internet Archive**) and any city-wide policy. A note to the publisher is now optional courtesy, not a gate |
| **8** | **Tel Aviv** 🇮🇱 | The MapServer returns **no `copyrightText` and no `licenseInfo`**, and Tel Aviv is **not** among the four municipalities on `data.gov.il` (Be'er Sheva, Haifa, Ma'ale Adumim, Petah Tikva), so there is no national statement to inherit | 🟡 **OPEN** — and awkward: the pages that would carry the terms are on the **IP-blocked** host (HTTP 472, the block names our IP). **Try the Internet Archive first** — that is how Barcelona's and Sevilla's were read — and only then ask |

---

## E. Closed, kept as evidence

| # | City / source | Why it is here | Status |
|---|---|---|---|
| 9 | **Sevilla** 🇪🇸 — ArcGIS Hub | Recorded as credential-walled, *"the Medellín shape"*. **That was wrong.** The Hub is a front-end; `sharing/rest` served 1,260 public items anonymously | ✅ **RESOLVED — never actually gated.** The correction is the lesson: **a sign-in wall on a Hub is not a verdict on the data** |
| 10 | **Barcelona** 🇪🇸 — general legal notice | CAPTCHA-walled, and **this project does not defeat CAPTCHAs** | ✅ **DONE** — read from the **Internet Archive** instead, which is a legitimate route to a public page, not a bypass |
| 11 | **Madrid** 🇪🇸 — CRTM | The *"siempre actualizada"* currency clause looked like a standing obligation | ✅ **RESOLVED 2026-09-22** — a dated snapshot meets it |
| 13 | **Medellín** 🇨🇴 | GeoMedellín's Hub is genuinely private — *"Please sign in"* — and **this project does not create accounts** | ⚫ **MOOT** — city discarded on two other grounds as well |
| 14 | **Budapest** 🇭🇺 | Nébih's FELIR is **mtcaptcha**-gated and lookup-only | ⚫ **MOOT** — city discarded |
| 15 | **Seoul** 🇰🇷 | `data.go.kr` is CAPTCHA-gated at the portal | ✅ **NOT a blocker** — the 197,276 premises across 8 datasets were obtained **with no account** |

---

## The owner's standing practice on API accounts

Recorded 2026-09-21 in `docs/data_sources.md`: **the owner registers an API
account, takes the data, then immediately terminates the account and revokes
its keys.**

**That practice is safe everywhere on this list except item 1.** WMATA's terms
are an API agreement rather than a data licence, so terminating the account
*ends the grant* — which is the point of the practice elsewhere, and a defect
here, because D.C. is published. **WMATA's account must stay live.**

**Resolved 2026-09-22: the owner reinstated the account to comply**, and it is
now **gate item 10** in `docs/data_sources.md` so the check runs before every
deploy instead of depending on someone remembering.

**A note on how this item gets verified, because it cannot be automated.**
Confirming an API account means holding its key, and **this project never
handles one** — no key is pasted into a session, and no screenshot is accepted
as proof of an account. The owner's word with a date is the record. That makes
this the rare gate item where the *only* possible check is a human one, which
is precisely why it needed a numbered slot rather than a paragraph.
