# Gated sources — every city that needs a key, an account, or a letter

**What this file is for.** Some cities are not blocked by data and not blocked
by code, but by something only a person can do: register an account, obtain an
API key, or send a notification to a publisher. Those items are invisible in
the master list, because a city waiting on a letter looks exactly like a city
waiting on a probe. This is the list to come back to and tick off.

**Three of these apply to cities that are already BUILT AND PUBLISHED** — items
1, 2 and 12. Items 1 and 12 are ongoing obligations rather than one-off steps;
item 2 is one act, drafted and waiting to be sent. They are first for that reason.

Status values: **OPEN** (nothing done) · **SENT** (the act was done, a
reply is awaited — carry the date, and the follow-up date if there is one) · **DONE** (satisfied, no upkeep) ·
**STANDING** (satisfied but must stay satisfied) · **MOOT** (the city or route
was dropped, kept for the record) · **OPTIONAL** (an upgrade, not a blocker).

---

## A. Live obligations on cities already published

| # | City | What is required | Status |
|---|---|---|---|
| **1** | **Washington D.C.** 🇺🇸 **BUILT** | **A live WMATA API account, for as long as the D.C. page is up.** `api.wmata.com` is the only feed in this project behind a key (401 unauthenticated). The terms are an *API agreement*: §9(i) terminates the grant when the account goes, and what lapses is the right to **publish the page**, not merely to store a file | ✅ **SATISFIED — the owner re-confirmed the account live on 2026-09-22**, stated directly. **STANDING thereafter:** do not terminate it while the site is up. Now **gate item 10** in `data_sources.md`, so it is checked before every deploy rather than remembered |
| **12** | **Philadelphia** 🇺🇸 **BUILT** | **A written request to the publisher, outstanding.** `phila.gov/terms-of-use` is incorporated by reference into the dataset page and prohibits redistribution and modification without written permission | 🟠 **SENT 2026-09-21, NO REPLY.** Not OPEN — this row said "someone has to ask" until 2026-09-22, when a sweep found it had been asked: the owner sent it to **`maps@phila.gov`** (the Open Data Program) copying **`LIGISTEAM@phila.gov`** (the Business Licenses custodian). Text at `docs/notifications/philadelphia-permission-request.md`. ⏰ **Follow-up due 2026-09-28**, tracked in `PLAN.md`. **Silence is not consent** — the map stays up on a *disclosed reasoned position* that rests on the reasoned reading and the footer disclosure, not on the City having failed to object, and it **does not strengthen with time**. It **comes down if the publisher confirms the restrictive reading** |

---

## B. Notification owed to a publisher

| # | City | What is required | Status |
|---|---|---|---|
| **2** | **Barcelona** 🇪🇸 **BUILT AND LIVE** | **Inform the City Council of the project.** Verbatim: *"Users are required to inform Barcelona City Council of every project relating to or derived from their use of the data sets."* The clause's own tail — *"so that they are open to the public"* — makes it a **reuse-showcase notification, not a permission gate**, so publishing did not wait on it | 🟠 **DRAFTED, NOT SENT.** See `docs/notifications/barcelona-city-council.md`. **Both preconditions are met**: the live terms were re-read by the owner in a browser on 2026-09-22, past the hCaptcha this project does not defeat, and the clause is unchanged word for word; and the site is public. The terms name their own channel — *"Any doubts or comments on these Terms of use may be forwarded to the following link"*, which redirects to `atencioenlinia.ajuntament.barcelona.cat`. ⚠️ **SENDING WAS ATTEMPTED TWICE ON 2026-09-22 AND BOTH FAILED**: the portal's own contact form stalled after its hCaptcha, and that named channel timed out from the owner's network and independently from a session. **The host is down, not blocking us** — `seuelectronica.ajuntament.barcelona.cat` answers HTTP 302 in 2.4s from the same /24. The fallback is closed too: the electronic registry requires a Spanish digital certificate. No email exists to fall back on either — the dataset's CKAN metadata carries no contact address and `datos.gob.es` names only a web form. **The clause sets no deadline**, so the plan is to retry when the service returns; the attempt log is in the notifications file |

---

## C. Free account or API key needed before a build can start

| # | City / source | What is required | Status |
|---|---|---|---|
| **3** | **Copenhagen** 🇩🇰 | **A free Datafordeler account — and the route is NOT `distribution.virk.dk`.** CVR is distributed through **Datafordeler**, Denmark's official platform, which is **not Cloudflare-challenged** and states its terms openly | 🟢 **RE-READ 2026-09-23, and the gate is far lighter than recorded.** **(1) Licence is CC BY 4.0** — *« frit hente, dele og tilpasse »*, credit *Det Centrale Virksomhedsregister (CVR)*. Same licence as Madrid and Milan. **(2) Only the entity `CVRPerson` is access-restricted**: *« De øvrige entiteter hos CVR er ikke adgangsbegrænsede, og du kan hente data uden at anmode registeret om adgang »* — so **production units need NO access request, no approval, no agreement**. ✅ **The gated entity is the personal-data one, which this project does not want**, so the restriction runs with the privacy invariant rather than against it. **(3) What remains is a free account** on Datafordeler Administration (e-mail or MitID Erhverv) plus an IT-system with an API key or OAuth. **No indemnity, no payment, no 30-day reconfirmation** — none of Lyon's four blockers. ⚠️ **Do NOT use `datacvr.virk.dk`'s basket (`kurv`)**: that is the legacy self-service extract route and it is a paid-order shape. ⚠️ The coordinate leg was already keyless (DAWA, 85,351 addresses, 100% coordinates) ⚠️ **A NEW API KEY 401s FOR ~15 MINUTES AFTER CREATION, identically to a wrong one.** `DAF-AUTH-0005`: *"Unrecognized Authentication key. Please verify: 1) The APIkey or ClientId is correct 2) **At least 15 minutes have passed since creation**"*. **Recorded because the obvious response makes it worse** — deleting the key and creating another RESTARTS the 15 minutes and produces the same 401, which reads as confirmation that the key was wrong. The path is not in doubt: every FileDownloads path returns 401 unauthenticated and **none returns 404**, so a 401 here is always the credential, never the URL. **Wait, then retry the same key.** 🔧 **Auth mechanism: API-key, NOT OAuth** — the Administration UI is explicit that API-Keys serve *« tjenester med frie data »* while OAuth Shared Secret serves *« fortrolige data ... anvendes sammen med ansøgning om adgang og oplysning af IP-adresser »*, both of which are ruled out here. **Key travels in the URL**, so it must never be echoed and belongs in an env var. **Download via `GetFile?Register=CVR&LatestTotalForEntity=<Entity>&type=current&format=CSV`** — no filename guessing. ⚠️ **Weekly generation, 7-day retention**, so a committed snapshot expires: WMATA's window again. |
| **4** | **Prague** 🇨🇿 | **An API key** — `api.golemio.cz` returns **401**. The business leg (`rzp.cz`, the *živnostenský rejstřík*) is live and is the right shape: Czech trade licences are issued **per premises**. Golemio is the transit half | 🟡 **OPEN** — Czechia is the strongest of the four Tier 4 probes |
| **5** | **Barcelona** 🇪🇸 — TMB | **A free TMB developer account** at `api.tmb.cat` (`app_id` + `app_key`); unauthenticated it returns *"Authentication failed. Authentication parameters missing"* | 🟢 **OPTIONAL** — the brief **chose OSM instead** and validated it (TMB 22 relations, TRAM 22, FGC 10). A key would be an upgrade to first-party geometry, not a prerequisite |
| **6** | **Spain — National Access Point** | **A free account**; `nap.mitma.es` answers **401**, the WMATA shape | 🟢 **MOOT for Sevilla** (city discarded — and it published its own metro openly anyway). Kept because it is the fallback rail route for any *other* Spanish city |
| **16** | **Taiwan** 🇹🇼 — `data.gov.tw` | **An API key** for the dataset API — a POST to `/api/v2/rest/dataset` returns `ER0001:API Key錯誤` for every query. Its **web pages are reachable**, and `addr.tgos.tw` answers but has historically required registration | 🟡 **OPEN — added 2026-09-22 when the Band B probe failed.** NLSC's keyless API is **reverse** geocoding only, and no bulk 門牌 address-point file was reached, so the recorded *"NLSC's geocoder is keyless"* did not survive. **Four cities ride on this** (Taipei, Kaohsiung, Taoyuan, Taichung), now in Band C |
| **17** | **Lyon** 🇫🇷 — `data.grandlyon.com` | **A free account, and it is a HARD BLOCKER on the data itself.** SYTRAL's page: *"Pour les récupérer, il est nécessaire de créer un compte sur la plateforme data.grandlyon.com"*. CGU 5.1 requires clicking to accept the terms; CGU 5.5 makes first access rights valid **30 days maximum** before the user must reconfirm; Licence Mobilités Art. 4.2 requires **one account per Licensee** and multiple accounts trigger termination. ⚠️ **The NAP copy is not a fallback — it is DEAD**: 0% availability, last modified **2022-04-14**, while SYTRAL's own portal is current to 2026-09-22 | 🟡 **OPEN — the owner must register.** This project does not create accounts. Added 2026-09-22 |
| **18** | **Lyon** 🇫🇷 — TCL trademark | **Grand Lyon CGU Art. 6.2 bars use of the producers' *signes distinctifs* "associés ou non à l'utilisation des données"** — far broader than SEPTA's, which claimed only its Logo. **This collides with a project invariant**: every drawn line must carry its real public name, and Lyon's is **TCL**. Nominative use and Art. 2.3(c) argue it is fine; the clause has no nominative exception | 🟠 **UNRESOLVED, deliberately — an owner decision.** Prior authorisation is obtainable at `contactopendata@tcl.fr`, which is cheap relative to the exposure |
| **19** | **France** 🇫🇷 — déclaration de conformité | **An ANNUAL declaration** under L. 1115-5 code des transports, which binds « les détenteurs **et les utilisateurs** de données ». The NAP says flatly that all data users must file it once data is published. Channel: `demarche.numerique.gouv.fr`; regulator `donnees-mobilite@autorite-transports.fr` | 🟠 **APPLICABILITY UNRESOLVED.** The regulation is written around route planners and travel-information services; a static density map is neither. **Worth asking rather than assuming — the answer creates a RECURRING obligation** |

---

## D. Licence questions only the publisher can answer

These are not access problems. The data fetches; what is unknown is whether we
may publish it. `read-licence` step 8: **do not resolve an ambiguity in this
project's favour.**

**Both entries here are now settled, in opposite directions** — Stockholm's ambiguity dissolved on reading (the publisher outranks the harvester, and it says *public*), while Tel Aviv's resolved into a prohibition and the city was discarded rather than appealed. **Neither outcome came from more fetching.**

| # | City | The question | Status |
|---|---|---|---|
| **7** | **Stockholm** 🇸🇪 | ~~`dataportal.se` says restricted while the ArcGIS item says public~~ — **re-read 2026-09-22 and the conflict mostly dissolves.** `dataportal.se` is the **harvester**; the publisher's own Hub DCAT feed declares **`accessLevel: public` on all 109 datasets**, with CC0 on 8 and blank on the rest. `read-licence` step 5 gives the publisher precedence over a third-party catalogue | 🟢 **NOT a letter — position is SILENT** (the Miami-Dade shape). Still unread: the walled `dataportalen.stockholm.se` record (**try the Internet Archive**) and any city-wide policy. A note to the publisher is now optional courtesy, not a gate |
| **8** | **Tel Aviv** 🇮🇱 | ~~A written request to the Municipality~~ — **the request will not be made.** The Terms forbid copying, distributing, publishing and **creating a database**, extend to non-commercial use, and require explicit prior written consent; the open-data portal's footer reads *all rights reserved* | ⚫ **CLOSED 2026-09-22 — owner's decision: a letter written IN ADVANCE and AGAINST explicit prohibitions is not worth the effort against its likelihood.** City discarded **on terms, not on data** — its 22,176 licensed businesses with activity, location and EPSG:2039 coordinates remain the strongest measurement of any unbuilt city, and are retained in `docs/city_master_list.md` under the closed Band B. **Nothing needs re-probing if it is ever revisited except the terms themselves** |

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
