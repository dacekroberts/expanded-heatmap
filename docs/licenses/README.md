# Stored licence texts

Local copies of the licence and terms documents this project relies on. Every
transit agency here reserves the right to alter or revoke its terms **without
notice**, so a URL alone does not preserve what was actually agreed to. The
clauses quoted in [`../data_sources.md`](../data_sources.md) are checkable
against these files.

**Position on storing them** (decided 2026-09-21, recorded in
[`../../DECISIONS.md`](../../DECISIONS.md)): each file is kept **unaltered,
non-commercially, for compliance reference**. These are the agencies' own
copyrighted documents, not this project's, and nothing here is republished —
the repository is the archive, not a distribution channel. Save fetched files
as-is; do not transcribe, reformat or trim them.

| File | Agency / row in `data_sources.md` | Source URL | Retrieved |
|---|---|---|---|
| `mbta-massdot-develop-license-agreement.pdf` | **MBTA / MassDOT** (Boston) | `https://cdn.mbta.com/sites/default/files/2023-08/mbta-massdot-develop-license-agreement.pdf` | 2026-09-21 |
| `sfmta-transit-data-license-agreement.html` | **SFMTA** (San Francisco) | `https://www.sfmta.com/reports/gtfs-transit-data` | 2026-09-21 |
| `la-metro-terms-conditions.html` | **LA Metro** (Los Angeles) | `https://developer.metro.net/terms-conditions/` | 2026-09-21 |
| `cta-developer-license-agreement.html` | **CTA** (Chicago) | `https://www.transitchicago.com/developers/terms/` | 2026-09-21 |
| `mta-terms-and-conditions.txt` | **MTA** (New York) | `https://new.mta.info/developers/terms-and-conditions` | 2026-09-21 |
| `septa-license-agreement.html` | **SEPTA** (Philadelphia) | `https://wwww.septa.org/license-agreement/` | 2026-09-21 |
| `wmata-transit-data-terms-of-use.html` | **WMATA** (Washington D.C.) — *not yet a row; D.C. is unbuilt* | `https://developer.wmata.com/license` | 2026-09-21 |

### Canada — screened 2026-09-21, six municipalities BUILT

Gathered during the Canadian screen, before any build, and all of it now in
use: Vancouver and Surrey as one regional map, plus Montréal, Calgary, Toronto
and Edmonton. Four of the five municipal licences are the same Open Government
Licence template; Edmonton and TransLink are the outliers, and the PROVINCE of
British Columbia is a seventh publisher that no municipal licence covers.

| File | Source | Source URL | Retrieved |
|---|---|---|---|
| `toronto-open-government-licence.txt` | **City of Toronto** — business licences *and* TTC GTFS, both of which declare "License not specified" at dataset level | `https://open.toronto.ca/open-data-licence/` | 2026-09-21 |
| `vancouver-open-government-licence.txt` | **City of Vancouver** — business licences | `https://opendata.vancouver.ca/pages/licence/` | 2026-09-21 |
| `calgary-open-government-licence.txt` | **City of Calgary** — business licences *and* Calgary Transit scheduling data | `https://data.calgary.ca/stories/s/Open-Calgary-Terms-of-Use/u45n-7awa/` | 2026-09-21 |
| `edmonton-open-data-terms-of-use.pdf` | **City of Edmonton** — business licences *and* ETS GTFS | `https://www.edmonton.ca/public-files/assets/document?path=Web-version2.1-OpenDataAgreement.pdf` | 2026-09-21 |
| `montreal-licence-donnees-ouvertes.txt` | **Ville de Montréal** — CC-BY 4.0 **plus portal conditions**; also governs STM GTFS, but STM requires attribution to *itself*, not the City | `https://donnees.montreal.ca/pages/licence-d-utilisation` | 2026-09-21 |
| `translink-gtfs-static-terms-of-use.txt` | **TransLink** (Vancouver *and* Surrey) — **the operative one.** Static GTFS has its own terms: no key, no approval gate, no request cap | `https://developer.translink.ca/ServicesGtfs/GtfsData` | 2026-09-21 |
| `translink-open-api-terms-of-use.txt` | **TransLink** Open API — *not* what governs the feed this project uses. Kept because it looked like it did, and because it requires discretionary approval | `https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources/terms-of-use` | 2026-09-21 |
| `surrey-open-government-licence.txt` | **City of Surrey** — Business Directory. Covers Surrey's own data only; its rail is TransLink's | `https://opendata-surrey.hub.arcgis.com/pages/surrey::open-data-license` | 2026-09-21 |
| `bc-open-government-licence.txt` | **Province of British Columbia** — the ABMS municipalities layer that NAMES the 30 out-of-city SkyTrain stations. The only provincial publisher in a Canadian build, so no municipal licence reaches it. **Three near-identically-named BC layers exist and two are "Access Only"** — see the file's own header | `https://www2.gov.bc.ca/gov/content?id=A519A56BC2BF44E4A008B33FCF527F61` | 2026-09-22 |

### Mexico — profiled 2026-09-22, CDMX being built

**Two documents, and the split is the whole point.** INEGI publishes its
website terms and its *information* terms as separate PDFs, so
`read-licence`'s step-4 question - does this govern web pages or data? - is
answered by the publisher rather than inferred. `terminos_info` is the
operative one; `terminos_sitio` is kept for the contrast, because reading a
site-terms document as though it governed the data is exactly the mistake that
made New York look prohibited.

| File | Source | Source URL | Retrieved |
|---|---|---|---|
| `inegi-terminos-libre-uso-informacion.pdf` | **INEGI** — DENUE, and every other INEGI product. **The operative document.** Grants copying, publication, adaptation, extraction and *commercial* exploitation (§1a-e); requires prescribed attribution (§1f), **disclosure of any analysis or transformation** (§1g), and non-endorsement (§1h) | `https://www.inegi.org.mx/contenidos/inegi/doc/terminos_info.pdf` | 2026-09-22 |
| `inegi-terminos-sitio.pdf` | **INEGI** — the *website* terms. NOT what governs the data; kept so the distinction is checkable rather than asserted | `https://www.inegi.org.mx/contenidos/inegi/doc/terminos_sitio.pdf` | 2026-09-22 |

**Mexico City's rail geometry is OpenStreetMap, not an agency feed**, because
every `*.cdmx.gob.mx` host times out and the feed's S3 `direct_download`
returns 403 (re-confirmed 2026-09-22). OSM is ODbL 1.0. No file is stored here
for it: ODbL is a published public licence rather than an agency document that
can be revoked or rewritten without notice, which is the reason this directory
exists. What it changes is the **scope of an attribution the project already
carries** - see `../data_sources.md`.

## SHA-256, as retrieved

```
03171dc15145af12c15781d121df4bac9713d025d57b919ae4798bdfb7acb473  cta-developer-license-agreement.html
aaf555af500679ae73f72d5495896ed27f9bf51c75f922c08a24bdc13b2860ac  la-metro-terms-conditions.html
e791e24e86b9e974de060c3b238abfc392260cad54ccc0d2d3d4f0a61846b91a  mbta-massdot-develop-license-agreement.pdf
6aa68ab9d19242d275fda71f36e2cb3165d23d545eb5494a9bea9597439ae746  mta-terms-and-conditions.txt
f7c07583af9880189c1df55fac2349378dc659016b7ce927dbd3f2900c3c220a  septa-license-agreement.html
ad6db26b111e58813aa41747c4b958d844befc664609cc7e2147b955a12c04b8  sfmta-transit-data-license-agreement.html
9df073bf2819a257e44cd9ad7961cac9d418c7fc4e100a625c8e4605dff516d3  wmata-transit-data-terms-of-use.html
dec36b71e5a02476bc633bb2959e5a3b970ac62520ab3f15d0ccec6dd0ec733b  toronto-open-government-licence.txt
05ee1aeea7df733ffe7d775de73841e9d79028fe7462deb2cbf8f11f5b4820bf  vancouver-open-government-licence.txt
99e69435cb5200e6f6af7a317e6cd82678f0f16b8ef0dd1469b6be28138de0d2  calgary-open-government-licence.txt
44e3fe0cf057fbdae30014eef02f9bc82952722388dcbc5c979befc19483e158  edmonton-open-data-terms-of-use.pdf
b01f632def2c6d4d56211dfb4519f1238c458ab188c1d4483bb12375465453a3  montreal-licence-donnees-ouvertes.txt
db8ad88e1e4a4b61f5c7fae7a1c593cf605402ebaed9886102dbdca0f97f3a08  translink-open-api-terms-of-use.txt
c389fcab88815aee4b2b39b76350a5bac85e080c52ccd794f9c647911fbeae37  translink-gtfs-static-terms-of-use.txt
7030261bb53846ed58187b724f23b343e692c7a34bff01e3f69042848e44a472  ipc-ontario-interpretation-bulletin-personal-information.pdf
6da9228708efa429399ad12f2fd028eb27be453adb71ae2fce68cf5fe75425e5  surrey-open-government-licence.txt
21fbab65a693dc264d38f2cb7002ab1ecd1a4fd2d1276cbab9168192e980d113  bc-open-government-licence.txt
8900206bbe4a2b8cf461e7e7ff111564cf4de2f863c7cd00b99ac19a4b925d62  inegi-terminos-libre-uso-informacion.pdf
4496431cc92fef99add789b6fdbb6d1494bd2397e4a05f79f49bd4fd0ab63359  inegi-terminos-sitio.pdf
```

## Two files here are NOT licences

`canada-privacy-regimes-note.md` works through what each province's statute
actually says, because every Canadian licence here carves out Personal
Information and defines it by pointing at its own province — and **the four
provinces do not say the same thing**. Ontario and BC exclude business-capacity
information from the definition outright (Ontario expressly covering a business
run from a dwelling; BC not). Alberta's licence cites a statute **repealed in
June 2025**. Québec narrows the Act's reach rather than excluding the
information, and frames its exemption around a function *within* a business,
which does not obviously reach a sole trader. Read it before building any
Canadian city.

The second is:

`ipc-ontario-interpretation-bulletin-personal-information.pdf` is the Ontario
Information and Privacy Commissioner's interpretation bulletin on "personal
information". It is kept here because every Canadian Open Government Licence
carves **Personal Information** out of the grant and defines it by reference to
the province's own access-and-privacy statute — so the carve-out cannot be read
without it.

It is load-bearing, and it corrected a wrong reading made during the screen.
MFIPPA s.2(2.1) / FIPPA s.2(3) say personal information "does not include the
name, title, contact information or designation of an individual that
identifies the individual in a business, professional or official capacity",
and s.2(2.2) / s.2(4) add that this applies "even if an individual carries out
business, professional or official responsibilities from their dwelling and the
contact information for the individual relates to that dwelling". So a
home-based sole trader's business name at their home address is **inside** the
Ontario grant, not outside it — the opposite of what was first assumed.

What survives is the IPC's second limb: information in a business capacity can
still be personal "if disclosed, [it] would reveal something of a personal
nature about the individual". So this project's residence filtering stays a
deliberate choice above the legal floor, which is how `DECISIONS.md` already
frames it for the US cities — not a compliance obligation.

**Ontario only.** British Columbia, Alberta and Québec carve out Personal
Information the same way but define it under their own statutes, and those
definitions are not verified. Québec is the least safe to assume, being civil
law with Law 25 layered on, and it governs the strongest candidate (Montréal).

Re-fetch and compare to detect a changed agreement. The HTML files are whole
pages, so an unrelated site redesign changes the hash without changing the
terms — a hash mismatch means *read it again*, not *the terms changed*.

## Four files are not raw fetches, and why

Every one of them says so at the top of the file itself, so this list is a
convenience and the file's own header is the authority.

- **`mta-terms-and-conditions.txt`** is a rendered-text capture. `mta.info`
  returns HTTP 403 to curl even with full browser headers, so the page was read
  in the browser pane and its text copied unaltered.
- **`mbta-massdot-develop-license-agreement.pdf`** is the raw PDF, but reaching
  it needed the browser: `mass.gov` also 403s automated fetches.
- **`translink-gtfs-static-terms-of-use.txt`** and
  **`translink-open-api-terms-of-use.txt`** are rendered-text captures of pages
  that serve their terms inline.
- **`bc-open-government-licence.txt`** is text extracted from the page's own
  HTML — tags stripped and list bullets preserved, nothing transcribed or
  summarised. `www2.gov.bc.ca` serves 145 KB of chrome around 4.9 KB of
  licence, so storing the raw HTML would bury the thing being preserved.

**This was a count of two until 2026-09-22**, which is worth naming rather than
quietly fixing: TransLink's two files had carried their own CAPTURE NOTE since
2026-09-21 and were never added here, so the section under-reported itself by
half. A list that has to be maintained by hand alongside the thing it
describes will drift — the file headers are what a reader should trust.

## Retrieval gotchas worth keeping

- **SEPTA's host really is `wwww.septa.org`, with four w's.** It is not a typo
  in their repo README, as `data_sources.md` previously recorded — SEPTA serves
  both `www` and `wwww`, each returning 200 independently with no redirect.
- **SFMTA's licence page is `/reports/gtfs-transit-data`.** The plausible
  `/reports-documents/gtfs-transit-data` is a 404. The agreement text sits
  inline on the page above the download link; there is no separate document.
- **MTA's landing page is not its terms.** `mta.info/developers` carries the
  "Our data feeds are free to use" line; the actual obligations are at
  `/developers/terms-and-conditions`, and they are substantive.
