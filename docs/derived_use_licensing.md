# Derived use: licensing for the analyses, cards and dashboards

The reference for the **Analytics** and **Visuals** sessions on what the
sources' licences allow for material DERIVED from the maps (statistics,
rankings, chain counts, cards, dashboards), as distinct from the site itself
(owner, 2026-10-04: "save this for both analytics and visuals to refer back to").
Read from the repository's own licence records only, 2026-10-04; nothing here
changes a city's status until the owner rules on it. Update it when a position
changes, and say so in DECISIONS.

## Update, 2026-10-12 (237 cities; owner's rulings after the commercial-use audit)

This section governs where it differs from the text below, which is as of
170 cities.

- **A publicly shared piece is the same kind of use as the site**: public
  and non-commercial. The columns of `docs/commercial_use_positions.md`
  (commercial use by a third party) do not decide it. The cities left out of
  a shared piece are the ones the Visuals registry
  (`visuals/data/restrictions.json`, kept locally) holds off public pieces.
- **Held off shared pieces today (11 of 237):** Barcelona, Bucharest,
  Cluj-Napoca, Daegu, Den Haag, Los Angeles (Regional), Miami (Regional),
  Philadelphia, Seattle (Regional), Thessaloniki, Washington D.C.
- **Lifted by the owner, 2026-10-12:** the 15 SEMAS cities and Busan (audit
  rows AN-5 and AN-3: permitted with condition); Dublin and Milan (their
  sources read as CC BY 4.0, rows HC-6, HC-7, HC-32, HC-34, HC-35).
- **Thessaloniki is held pending a full read** (owner, 2026-10-12): one
  reading of the City portal's terms bars modification and redistribution
  (row EW-13). The same question touches the site's own page.
- **Den Haag, Miami (Regional), Bucharest and Cluj-Napoca stay held**: the
  audit read their registers as silent, which closes nothing.
- **Analytics' pieces** (its list of 2026-10-12, at commit 9d3a0cea), before
  Thessaloniki's hold: the dashboard's overview and per-city views, 237
  cities, 225 shareable; its chain tables, 170 cities, 161 shareable; the four
  pilot pages (Paris, San Diego, Tokyo, Toronto), all shareable once rebuilt,
  Paris with its IDFM notice; the cross-city Food service share, 167 cities,
  155 shareable. With Dublin and Milan lifted and Thessaloniki held, recount
  from the registry before sharing. **Whether any piece goes public is still
  the owner's call, piece by piece.**
- **Notices a shared piece owes**: unchanged from the list below, with
  Japanese credits saying the data was processed, and counts never presented
  as a publisher's own figures.

## In short

- **Private use is fine for all 170 cities.** No recorded licence limits derived
  statistics, rankings or chain counts only the owner sees. A private page needs
  only the AI-analysis acknowledgement, at its top and bottom.
- **Never share:** Washington D.C. (WMATA bars sharing) and Los Angeles
  (Regional) (LA Metro bars redistribution).
- **Keep private until the owner rules:** Philadelphia, Seattle (Regional),
  Barcelona, Dublin, Den Haag, Bucharest, Milan, Miami (Regional), Daegu, Busan
  and the 13 SEMAS cities. They are held off public images because a posted
  image cannot be withdrawn; a link-shared page can be, so the owner may rule
  differently for a dashboard.
- **The other ~145 can be shared with their notices:** each city's credits and
  the every-page set, the repository link, Fukui's CC BY-SA line and Taiwan's
  statements, "Figures derived by this project; not official statistics", and
  the AI acknowledgement.
- **Unresolved:** what counts as "publicly" under ODbL (until settled, treat
  anyone but the owner as the public); Barcelona's notification letter, still
  unsent; what hub.brussels' "Google Maps" credit covers; whether SEMAS's
  permission reaches shared pieces.

## The full reading

DS = docs/data_sources.md; US/JP/TW = docs/data_sources/<country>.md; ARCH = docs/decisions/2026-09-27.md.

## Verdict

**Private use is fine for all 170 cities.** No recorded licence restricts derived statistics, rankings or chain counts that only the owner sees. The record ties every notice duty to publishing ("MUST display when published", DS:532). A private page therefore owes no licence notice, only the project's AI-driven acknowledgement at the top and the bottom.

**Sharing is narrower.** A shared page should leave out the 25 cities Visuals keeps out of public pieces. Nothing recorded stops relisting chain (trade) names.

## a. Restrictions on derived analysis

**No licence in use is no-derivatives or view-only.** Barcelona's BY-ND clause "does not apply" (DS:1240). **Four sources hold only while the use stays non-commercial** (corrected 2026-10-11; this said none did): the City of Seattle's register, the WA Liquor and Cannabis Board's list, Bellevue's portal terms and MHLW's filings (licence_positions.md rows 2.7, 2.8, 1.6 and 2.10). That does not limit the private or non-commercial derived use this file covers; commercial use is a separate question, to be answered in `docs/commercial_use_positions.md` once the final batch lands (owner, 2026-10-11).

**The counts in this file are as of 170 cities, 2026-10-04.** 206 are built at 2026-10-11 and the final batch adds more; the list of cities kept off public pieces is the Visuals registry's, not this file's.

Terms that bear on it:
- **INEGI:** must disclose "cualquier análisis o transformación" (DS:694).
- **Barcelona:** must "inform Barcelona City Council of every project" (spain.md:413). Not yet sent.
- **Philadelphia:** bars "Distribution or republication in any other form" (US:524).
- **LA Metro:** forbids "unauthorized redistribution and publication" (US:356).
- **WMATA:** bars "sharing (except with your Application's users)" (US:361).

## b. Share-alike and attribution

- **OpenStreetMap and the French ODbL feeds:**
  - ODbL §4.3 requires a notice when a work is "Publicly Use[d]" (licenses/odbl-toulouse-rennes.md:69).
  - §4.6 is met by linking the repository, as the site does (app/components.py:367).
  - A station table with coordinates reopens §4.4, still OPEN (licence_positions.md:241).
  - The French feeds' publisher guidance exempts shop-to-station calculations from re-sharing (odbl-toulouse-rennes.md:114-123).
- **Fukui:** "offered under CC BY-SA 4.0" (JP:207) on any shared piece.
- **Taiwan:** without the attribution statement the data is "never licensed at all" (TW:41).
- **Chicago, Kansas City and Tacoma:** their disclaimers attach to any application that uses the data (DS:574; US:237; DS:3566-3576).
- **Japan:** each credit must say the data was processed (加工).

## c. Map display versus relisting names

**No recorded licence draws that line.**
- **hub.brussels:** credits "Google Maps" as a contributor, and the publisher never says what that covers (build_briefs/brussels.md:256-260).
- **Den Haag:** the site terms name database rights (DS:2565).
- **SEMAS:** counts must never be presented as "SEMAS's figures" (DS:2262).
- **Names:** trade names only, never a person's own (CLAUDE.md).

## d. Held cities

Source: memory note, ARCH:4941-4947, 5562-5570 (registry file unreadable).

**Private use is fine for every held city.** Sharing:
- **Never share:**
  - Washington D.C.: WMATA forbids sharing.
  - Los Angeles (Regional): LA Metro forbids redistribution.
- **Keep private until the owner rules:**
  - Philadelphia, Seattle (Regional), Barcelona, Dublin, Den Haag, Bucharest, Milan and Miami (Regional).
  - Daegu, Busan and the 13 SEMAS cities. Held because a posted image cannot be taken down; a shared link can.
- **Paris:** shareable with its IDFM notice and links.

## e. Newest cities and Japan

- **Belgium:**
  - **KBO:** reuse only "within the purpose the owner declared" (DS:3731). The owner ruled "KBO is fine" (2026-10-04, in the Visuals session; its log is kept locally since then). The source and update date are still owed, with no alteration and no direct marketing.
  - **The other sources:** CC BY 4.0, each with a statement of changes. VKBO's credit must be verbatim, and the transit operators' credits are dated.
- **Daejeon, Gwangju, Gimhae:** SEMAS; held with the other SEMAS cities.
- **Liverpool:** OGL credits for the FSA and Ordnance Survey; no ratings.
- **Tacoma:** notice 142 in full. The City may require termination "for any reason".
- **Mendoza:** CC BY 4.0 with a statement of the modifications.
- **Japan:**
  - MHLW's terms hold only while non-commercial (licence_positions.md:86).
  - N03 city outlines are never drawn (JP:184).
  - Sapporo, Fukuoka and Kobe forbid calling the businesses current or operating.

## Lists

- **Safe to share as-is:** none; every city owes a credit.
- **Share with these notices:** the other 145 cities, with:
  - each city's notices and the every-page set;
  - the repository link;
  - Fukui's CC BY-SA line and the Taiwan statements;
  - "Figures derived by this project; not official statistics";
  - the AI acknowledgement.
- **Keep private until the owner rules:** the 8 public-hold cities, the 13 SEMAS cities, Daegu and Busan.
- **Never share:** Washington D.C. and Los Angeles (Regional).

## Unresolved

- What counts as sharing "Publicly" under ODbL: not recorded.
- hub.brussels' Google Maps credit.
- The Barcelona notification, still unsent.
- Whether SEMAS's permission covers shared pieces.
