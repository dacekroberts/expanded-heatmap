# Global country shortlist — which country to profile after Canada

**Worldwide in scope.** Every country on earth is in scope here, not a
shortlist of guesses: the screen starts from the full Mobility Database
catalogue — **87 countries, 2,476 static GTFS feeds** — so a candidate can be
ruled out, but not missed by omission. The United States and Canada are
excluded throughout as already built or screened.

The layer above [`add-country`](../.claude/skills/add-country/SKILL.md), as
[`city_shortlist.md`](city_shortlist.md) is the layer above `add-city`. This
file decides *which country is worth a profile*; the profile itself is a
separate and much larger job.

Started 2026-09-21. **No country here has been profiled and nothing has been
built.** Canada remains the only country screened end to end — see
[`canada_retrospective.md`](canada_retrospective.md) for what that cost.

Claims are labelled **MEASURED** (a number and the check that produced it) or
**ASSERTED** (plausible, unchecked — verify before acting), per
[`session_roles.md`](session_roles.md).

## The filter order, and two that were dropped

The screen was originally posed as: map coverage → transit → business data →
legal. Reordered on 2026-09-21, before running, because the first two do not
discriminate:

1. **Map coverage is free.** This project uses OpenStreetMap only as a
   basemap, and those tiles render for every populated place on earth. Tile
   quality varies; nothing is disqualified by it. **Skipped.**
2. **Rail existence barely discriminates** outside North America. Every
   candidate city in Europe and East Asia has urban rail. Rail-first was
   correct *inside* Canada, where it killed 6 of 13 candidates; globally it
   kills almost nothing.

So the order actually run was:

1. **Premises-level business data** — the real discriminator, below.
2. **Licence and privacy regime.**
3. **A readable transit feed** — confirm only. Note this is *not* the same
   question as "is there rail", and the difference turned out to matter.
4. Map coverage — free, skipped.

### The sharper form of the business-data question

> Does the country record **where commerce physically happens** — premises —
> or only where companies are **registered**?

This is the whole game, and it is what splits the world. A national company
register (Companies House, Registro Imprese, Handelsregister, Bolagsverket,
Australia's ABN) publishes a **registered office**, which is frequently an
accountant's address or a holding company's mailbox. Mapping those produces a
map of bookkeepers. A municipal licence register, a national *establishment*
register, or a commercial-premises survey records the actual shopfront.

Four shapes qualify:

| Shape | Example |
|---|---|
| Municipal licence register | US, Canada, **South Korea** |
| National **establishment** register | **France** (SIRET), **Mexico** (DENUE) |
| Commercial premises field survey | Montréal, **Barcelona** |
| Sector inspection register | UK FSA — **one bucket only**, Boston's shape |

## Master ranking, by tier

Tiers rather than a numbered order: the candidates differ in *which leg is
unproven*, which is not a thing a single score can express. Rail figures are
`scripts/screen_rail.py` output against real `routes.txt`, run 2026-09-21.

### Tier 1 — both legs measured. Ready for a country profile.

| | Rail (MEASURED) | Business (MEASURED) | The open question |
|---|---|---|---|
| **France** / Paris | **subway 16, tram 17, funicular 1** (IDFM) | SIRENE, établissement-level, geolocated, **Licence Ouverte 2.0**, non-diffusible masked at source | **Design, not data:** a national register is not the per-city municipal shape this project is built around |

France is the only candidate with no *evidential* gap. What it has instead is
an architectural one, and that is a decision to take before a profile rather
than a fact to discover during one.

### Tier 2 — one leg excellent, the other genuinely open

| | Data | Rail | What is missing |
|---|---|---|---|
| **Spain** | **MEASURED** — Barcelona's 68,024-premises ground-floor census | **MEASURED** — Madrid subway 13, Barcelona FGC subway 4 + funicular 3, plus Bilbao, Málaga, Valencia, Sevilla: **six metro cities, more than any other candidate** | **The licence.** Open Data Barcelona's terms have not been read. That is the only gap, and it is one document |
| **Mexico** | **MEASURED** — DENUE, 6M+ establishments, coordinates, **SCIAN = NAICS** so the taxonomy may transfer | **Partial** — Guadalajara LRT 3 measured and current; **Mexico City unreachable** (S3 403, city portal refuses connections) | A working CDMX feed. Viable through Guadalajara regardless |
| **South Korea** ↑↑ | **MEASURED and the best found anywhere** — `상가(상권)정보`: active premises nationwide, 상호명 + 업종 + both address forms + **경도/위도**, KSIC 10/75/247, quarterly, CSV UTF-8, free, **이용허락범위 제한 없음 (no restriction)**. One register, all three buckets | **MEASURED** — national urban-railway **station** and **line** standard datasets on `data.go.kr` (15013205 / 15013203), plus Seoul's own lines 1–9 set updated 2026-09-22 (Open API, free key) | Download and verify the schema live; confirm the station datasets carry coordinates |

**Spain overtook Mexico this round.** Its business leg was already the
Montréal model and its rail leg is now the deepest measured anywhere in this
screen — six metro cities in one country, against Canada's six *candidate*
cities of which only two had a metro. What stands between Spain and Tier 1 is
a single unread licence, not a data question.

### Tier 3 — rail measured, business data unknown

All confirmed to have real urban rail; none has had its business register
probed. These are cheap to advance and could move up or out quickly.

**The widened re-probe added ten European capitals to this tier**, several of
which were initially and wrongly reported rail-free: **Vienna** (subway 35,
tram 185 — the largest measured anywhere in this screen), **Amsterdam /
Rotterdam** (subway 14, tram 46), **Berlin** (urban rail 9, tram 48),
**Stockholm** (metro 7, tram 21), **Copenhagen** (subway 4, tram 4),
**Oslo** (metro 5, tram 9), **Prague** (subway 3, tram 40), **Helsinki**
(subway 4, tram 26), **Lisbon** (subway 10) and **Naples** (subway 3, tram 3,
funicular 3). Each still needs its business register probed, and **each sits
under GDPR**, which is the expensive half.

| City | Country | Rail (MEASURED) |
|---|---|---|
| **Vienna** | AT | **subway 35**, tram 185 — the deepest measured in this screen |
| **Amsterdam / Rotterdam** | NL | subway 14, tram 46 |
| **Berlin** | DE | urban rail 9, tram 48 |
| **Stockholm** | SE | metro 7, tram 21 |
| **Santiago** | CL | **subway 7**, tram 2 |
| **São Paulo** | BR | **subway 6** |
| **Bucharest** | RO | subway 5, tram 15 |
| **Oslo** | NO | metro 5, tram 9 |
| **Lisbon** | PT | **subway 10** |
| **Singapore** | SG | **subway 13** — but a city-state, and its register is likely registered-office shaped |
| **Sofia** | BG | subway 4, tram 24 |
| **Copenhagen** | DK | subway 4, tram 4 |
| **Bangkok** | TH | subway 4, LRT 5 |
| **Helsinki** | FI | subway 4, tram 26 — *feed expired* |
| **Budapest** | HU | subway 4, tram 42 — *feed expired* |
| **Hamburg** | DE | underground 4 — *feed expired* |
| **Prague** | CZ | subway 3, tram 40 — *feed expired* |
| **Athens** | GR | subway 3 |
| **Naples** | IT | subway 3, tram 3, funicular 3 |
| **Hyderabad / Kochi** | IN | subway 3 / subway 1 |
| **Cairo** | EG | subway 2 — *feed 11 months expired* |
| **Tokyo** | JP | **subway 4, tram 1** (Toei) — rail is fine; **Japan's blocker is its business data** |
| Tram-only | — | Riga 7, Tallinn 5, Zagreb 19, Bratislava 6, Poznań 22, Messina 1 |

#### Tier 3 business probes — started 2026-09-21

Two countries moved materially; the rest are still asserted.

**Norway — MEASURED, and it is premises-level.** The Brønnøysund open API
answers with **no key, no login, no registration**:

```
https://data.brreg.no/enhetsregisteret/api/underenheter?kommunenummer=0301
```

**152,060 sub-units in Oslo alone.** Each record carries `navn`,
`naeringskode1` (NACE code *and* description), `organisasjonsform`,
`oppstartsdato`, and critically **`beliggenhetsadresse`** — the *physical
location* address, which the register keeps distinct from the registered
business address. That distinction is the whole filter-3 question, and Norway
answers it the right way.

**No coordinates**, so a geocoding leg would be needed. Kartverket publishes an
open national address register, untested. Oslo measures metro 5, tram 9.
GDPR applies, and the sample already shows the familiar shape — a law firm
named after a person, at what reads like a house.

**Austria — a strong lead, not yet a finding.** GISA
(*Gewerbeinformationssystem Austria*) is a national **business licence**
register — the US/Canada model, not a company register — carrying the name,
**the location**, and the wording of each licence. Reportedly published on
`data.gv.at` as **open data in CSV and JSON, with personal data removed at
source**, free and without registration. That combination, paired with
**Vienna's subway 35 / tram 185 — the deepest rail in this screen** — would
make Austria a Tier 1 candidate.

**ASSERTED: the dataset URL guessed for it returned 404.** Find the real
resource before believing any of this.

**Still asserted, unprobed:** Denmark's CVR *produktionsenheder*, Czechia's
ARES (3.4M subjects, open, NACE — but subjects, not premises), Poland's
CEIDG/REGON, Sweden's Bolagsverket (company-level), Germany, Italy, Portugal,
Greece, Finland, the Netherlands.

**Germany, Italy, Sweden and Portugal were moved here from Tier 4.** They had
been ruled out on the EU-default company-register pattern — which was
**ASSERTED and never probed for any of them** — while Berlin, Naples,
Stockholm and Lisbon were simultaneously being rail-confirmed into this tier.
They were in two tiers at once. Ruling a country out on a pattern rather than
a probe is exactly the error this file exists to avoid.

### RE-ANALYSIS under the corrected framework — most of Tier 4 is not safe

Applying the rules that came out of this screen to the screen itself. Korea is
the proof: it sat in Tier 2 on "**zero feeds in the catalogue**", and the
national standard dataset turned out to hold **1,099 stations with WGS84
coordinates, free and unrestricted**. The catalogue was simply the wrong place
to look.

**Every Tier 4 entry ruled out on "no feed anywhere in the catalogue" was
tested against a transit catalogue — the wrong source for a GIS question.**
Those rulings are therefore **ASSERTED, not measured**, and the countries below
move back into the running pending a national-mapping-agency probe:

| Country | Ruled out on | Where to actually look |
|---|---|---|
| **Hong Kong** | no MTR feed | Lands Department **iB1000** topographic map (transport layer), CSDI portal |
| **Taiwan** | no Taipei/Kaohsiung feed | **NLSC**, and **TDX** (MOTC) |
| **Indonesia** | no MRT Jakarta feed | Badan Informasi Geospasial |
| **Brazil / Rio** | no MetrôRio feed | IBGE |
| **Malaysia** | no Prasarana feed | JUPEM |
| **Israel** | no Tel Aviv feed | Survey of Israel, `data.gov.il` |
| **Peru, Colombia** | no Lima/Medellín/Bogotá feed | IGN, IGAC |

**None of these has been probed at its national mapping agency.** Given Japan
and Korea both flipped on exactly this, the prior should be that several of
them flip too.

#### Sweep status, 2026-09-21 — routing established, schemas not yet

Reachability tested; **no schema has been verified for any of the eight**, so
every row below is a *route*, not a finding.

| Host | Result |
|---|---|
| `tdx.transportdata.tw` | **200** — Taiwan's transport exchange is live |
| `data.gov.tw` (and dataset `102985`) | **200** |
| `www.csdi.gov.hk` | **200** — Hong Kong's official spatial data infrastructure, "free download, machine-readable" |
| `data.gov.hk` | 302 |
| `portal.nlsc.gov.tw` | **000** — down; TDX is the route for Taiwan, not NLSC |

**Taiwan is the one worth doing first**, and the reason is business data rather
than transit: it is **the only one of the eight with plausible premises-level
business data *and* a metro**. `data.gov.tw` carries 商業登記 (commercial
registration) exports with business addresses, so a transit flip there could
move a whole country rather than just correcting a table. Expect TDX to be
registration-gated, like Korea's and WMATA's.

**Hong Kong is the opposite case and should be deprioritised despite CSDI being
live.** Its business data is the FEHD food-licence register — **food only**,
so Hong Kong is a two-bucket city at best whatever its rail data shows. Fixing
its transit would not fix its ceiling.

**Still entirely unprobed:** Indonesia (BIG), Malaysia (JUPEM), Israel
(`data.gov.il`).

#### Latin America, probed 2026-09-21 — and the national agencies were the wrong place

The national mapping agencies (IGAC, IGN/IDEP, IBGE) were the obvious target
after Japan. **The layers are at city level instead**, which is the Mexico and
Korea pattern again: national portal blocked or irrelevant, city portal
serving.

**Bogotá — good data, wrong mode.** `datosabiertos-transmilenio.hub.arcgis.com`
serves GeoJSON unauthenticated: **153 stations, all `Point`, EPSG:4326**, with
`longitud`/`latitud` and station names. But these are **TransMilenio BRT**
stations, and BRT is not urban rail here. Bogotá's Metro Line 1 is still under
construction, so Colombia is out **on mode, not on data** — and worth
revisiting when Line 1 opens, because the publishing infrastructure is
evidently good.

**Mexico City — unreachable, and this is now durable.** The metro's own
`Líneas y Estaciones de STC Metro (SHP)` sits on `datos.cdmx.gob.mx`, which
failed again **after the prober's retry** — roughly the sixth failure across
the session, while `inegi.org.mx` answered instantly throughout. Recorded as a
fact about the host, not the data: **the layer exists and is named**, and
Guadalajara continues to carry Mexico meanwhile.

**Located but not yet probed:**

- **Lima** — `MTC - AATE ESTACIONES DE METRO DE LIMA - LINEA 1` on
  `datosabiertos.gob.pe`, JSON and Excel, under an **Open Data Commons
  Attribution** licence. Line 1 is genuine urban rail.
- **São Paulo** — GeoSampa (`download.geosampa.prefeitura.sp.gov.br`) publishes
  the operating stations of Metrô and its concessionaires as shapefiles. Brazil
  already has the CNPJ business register, so São Paulo is the strongest Latin
  American candidate after Mexico.

#### Taiwan, probed 2026-09-21 — business leg MEASURED

`data.gov.tw`'s catalogue API answers **GET by dataset id without a key**;
only search needs one (`ER0001: API Key錯誤`).

**`商業登記(依營業項目別)`** (dataset `102985`, Ministry of Economic Affairs),
downloaded and parsed — **45,819 rows for the single category 其他餐飲 (other
food service)**, monthly updates:

| Column | Content |
|---|---|
| `統一編號` | unified business number |
| `商業名稱` | business name |
| **`商業地址`** | **premises address**, e.g. `高雄市鼓山區濱海一路２３號１樓` — down to floor |
| `登記狀態` | `核准設立` (approved) / `歇業／撤銷` (closed or revoked) — so active filtering works |

**It is premises-level.** 商業登記 registers sole proprietorships and
partnerships **at their operating address**, unlike 公司登記 (dataset `13861`),
which is a company register with the registered-office defect.

**Three costs, none fatal:**

- **No coordinates.** Address only, so Taiwan needs a geocoding leg — the
  Toronto problem. TGOS (內政部) is the candidate; NLSC is down.
- **Split one dataset per category** (`依營業項目別`), so coverage is an
  assembly job — `multi-source-city`, at national scale.
- **Full-width numerals** in addresses (`２３號`) will need normalising before
  any geocode match. A quiet trap of exactly the kind Toronto's title-case
  `ADDRESS_FULL` was.

**Transit leg — MEASURED, complete, and NOT registration-gated.** TDX's
`v2/Rail/Metro/*` endpoints answered plain unauthenticated requests:

| Endpoint | MEASURED |
|---|---|
| `Station/TRTC` | **122 stations**, each with `StationPosition.PositionLat/Lon` (WGS84), `StationAddress`, city and town codes, and `StationName` in **Zh_tw, En, Ja and Ko** |
| **`Shape/TRTC`** | **5 lines as `MULTILINESTRING` WKT**, plus `EncodedPolyline` |
| `Line/TRTC` | 5 lines with `LineName`, `LineSectionName`, `IsBranch` and **`LineColor`** |
| `StationOfLine/TRTC` | station-to-line mapping |
| `Network/TRTC` | operator and network metadata |

**This passes both halves of the points-and-lines check**, and gives more than
GTFS would: official **line colours**, which this project otherwise researches
by hand per city, and English station names, which removes the label-language
question exactly as Korea's `영문역사명` did.

**So Taiwan's ruling is reversed.** It was in Tier 4 on "the 9 Taiwanese feeds
are all rural bus operators" — true of the catalogue, and irrelevant, because
the national transport exchange publishes a first-class rail API that the
catalogue does not mirror. **Taiwan's only real cost is the business leg:
geocoding, and per-category assembly.**

Taiwan's food-hygiene register (`食品業者登錄資料集`, dataset `8938`) is
separately available as CSV/JSON/XML from `data.fda.gov.tw`.

#### A refinement the Korea probe produced: stations are not lines

Japan's N02 carries **both** — 10,235 station points *and* 21,932 line
segments. Korea's station standard dataset carries **stations only**, and this
project draws and labels every transit line, which is an invariant.

So the national-GIS check is **two questions, not one**:

1. Does the layer carry **station points** with coordinates?
2. Does it carry **line geometry**?

A country can pass the first and fail the second, and a screen that asks only
the first will record a false pass. Add the line question to `add-country`
before the next country is profiled.

### Tier 4 — ruled out, with the evidence

| | Why | Basis |
|---|---|---|
| **United Kingdom** | Business data is the wrong object — VOA is property without names, Companies House is registered offices, FSA is food-only | MEASURED |
| **Japan** | Business data is **aggregate counts by area**, not an establishment register. **Its transit is fully solved** — see below | MEASURED |
| **Taiwan** | **Nothing for Taipei, Kaohsiung, Taoyuan or TDX anywhere in the catalogue.** The 9 Taiwanese feeds are rural bus operators | MEASURED |
| **Hong Kong** | **No MTR feed anywhere in the catalogue.** The Transport Department feed carries tram/LRT 7 and no subway | MEASURED |
| **Jakarta** | **No MRT Jakarta or LRT Jakarta feed anywhere.** Transjakarta is BRT | MEASURED |
| **Rio de Janeiro** | **No MetrôRio or SuperVia feed anywhere** | MEASURED |
| **Kuala Lumpur, Tel Aviv, Lima, Medellín, Bogotá** | No metro operator feed anywhere in the catalogue | MEASURED |
| **Dubai** | The catalogue's feed is an **anonymous personal GitLab job artefact** returning a non-zip; the transitland fallback 404s | MEASURED |
| **Manila** | The LRTA feed codes its four rail lines as **commuter rail (type 2)**, which this project excludes. A coding question, but it fails as published | MEASURED |
| **Belgium** | Establishment units exist; **bulk access requires application and payment** | MEASURED |
| **Australia, New Zealand** | Auckland is commuter-only. **Melbourne's PTV feed is a nested zip** the screen cannot read, so its rail is *unverified rather than absent*. Business licensing is not municipal — **ASSERTED** | MIXED |
| **Russia, Ukraine** | Access and conflict, not data | — |

### Japan's rail data is solved, and not by GTFS

Worth stating separately because it breaks the screen's own assumption. This
project needs **station coordinates and line geometry**, not timetables, and
GTFS is only one vehicle for those. Japan publishes a better one.

**国土数値情報 N02 鉄道データ** (MLIT National Land Numerical Information,
railway data), verified by download 2026-09-21:

| | MEASURED |
|---|---|
| Endpoint | `https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip` (12.4 MB; 2020–2024 all return `application/zip`) |
| Stations | **10,235**, across **178 operators** |
| Line segments | **21,932**, across 179 operators |
| JR coverage | JR East **1,803 stations**, JR West 1,264, JR Kyushu 621, JR Central 439, JR Hokkaido 343, JR Shikoku — **all six JR companies** |
| Also | Tokyo Metro, Toei, Osaka Metro, Kintetsu, Meitetsu, Tobu |
| Attributes | `N02_001` rail class, `N02_002` operator category, `N02_003` line name, `N02_004` operating company, `N02_005` station name |
| CRS | **EPSG:6668** (JGD2011) |
| Formats | Shapefile **and GeoJSON**, supplied in **both Shift-JIS and UTF-8** — so no encoding trap |
| Licence | **PDL 1.0**, the Japanese Government Standard Terms — commercial use, redistribution and derived works all permitted |

Attribution: `出典：国土交通省国土数値情報ダウンロードサイト`, and for a derived
work `「国土数値情報（鉄道データ）」（国土交通省）をもとに作成`.

**THE TRAP: station geometry is `LineString`, not `Point`** — all 10,235 of
them. A Japanese station record is the platform centreline, so it must be
centroided before any ring buffer. A pipeline that assumed points would fail
or, worse, silently buffer from a line end.

ODPT (`api-public.odpt.org`) is the second route and also works — Toei's feed
downloaded without a key — but N02 is national, covers JR, and needs no
registration.

**So Japan is ruled out on business data alone.** Only the Economic Census was
checked, and it is aggregate. Japanese municipalities publish
食品関係営業許可施設 (food-business permit premises) as open data, which would
be a one-bucket source at best — worth a probe before the ruling is final.

### THE METHOD THIS SCREEN GOT WRONG: transit data is not GTFS

The single most useful thing to come out of this screen, and it invalidates
part of the screen itself.

**This project uses no timetables.** It needs **station coordinates and line
geometry**. GTFS carries those, but so does any national railway GIS layer —
and national mapping agencies publish those routinely, at better quality, with
national coverage and clearer licences.

Every country ruled out above for "no readable feed" was ruled out on a
**GTFS** question, when the real question is a **GIS** one. Japan proves the
gap is real and large: the Mobility Database has 18 Japanese feeds, almost all
volunteer-run village buses, and **no JR at all** — while MLIT publishes every
railway station in the country, JR included, for free.

**So the probe order for transit should be:**

1. The national mapping or statistics agency's railway layer — MLIT in Japan,
   and its equivalent elsewhere. Usually shapefile/GeoJSON, usually a clear
   government licence, usually national.
2. The national open-data portal's transit standard datasets.
3. The city or agency's own GTFS.
4. The Mobility Database catalogue — **last**, being a mirror of a mirror,
   and demonstrably incomplete and stale.

The screen ran that list backwards.

#### Countries this reopens

| Blocked on GTFS | The GIS route to check |
|---|---|
| **South Korea** | `data.go.kr` carries **전국도시철도역사정보표준데이터** (national urban railway *station* standard data, ID 15013205) and **전국도시철도노선정보표준데이터** (*line* standard data, ID 15013203) |
| **Hong Kong** | Lands Department **iB1000** digital topographic map, which includes a transportation layer, via the CSDI portal and `data.gov.hk` |
| **Taiwan** | NLSC and TDX, neither in the catalogue |
| Jakarta, Kuala Lumpur, Rio, Lima, Bogotá, Medellín, Tel Aviv | National spatial agencies, all unchecked |

#### Reachability is its own finding — and a transient outage is not one

Three government portals refused connections, tested from **two independent
networks** on 2026-09-21 to separate "site is down" from "this path is
blocked". **One of those readings was wrong within the hour**, and the
correction matters more than the original table.

| Host | First reading | Retested ~1h later |
|---|---|---|
| `www.data.go.kr` | unreachable, 21s timeout, both networks | **HTTP 200 in 1.15s** |
| `apis.data.go.kr` | not tested | HTTP 400 — live, wants parameters |
| `datos.cdmx.gob.mx` | unreachable, 21s timeout | **still 000 at 21s** — four attempts over two hours |
| `s3.amazonaws.com/setravi/…` | 403 | still 403 |
| `www.inegi.org.mx` | — | HTTP 200 |
| `data.seoul.go.kr` | HTTP 200 | HTTP 200 |
| `nlftp.mlit.go.jp` | HTTP 200 | HTTP 200 |

**Korea's national portal was suffering a transient outage and is fine.** It
was recorded here as a hard finding, on evidence from two networks, and it was
wrong about an hour later.

**Mexico City's is not transient** — four failures across two hours, while
INEGI on the same day answered instantly. That one is a durable finding *as of
2026-09-21*, and still not a permanent one.

**The lesson, and it is the same one this file keeps producing.** A negative
result is a measurement of *one moment* as well as one method. Two networks
agreeing says nothing about two *times*. The evidence-discipline rule in
`add-country` — treat a negative as ASSERTED until a second differently-shaped
probe agrees — needs "differently-*timed*" alongside "differently-shaped", and
an infrastructure failure should never be written down as a property of the
data.

**Do not record a country as "no data" on the strength of an unreachable
portal.** Retry it, and try the city portal, which is this project's scope
anyway.

### What in these tables is an artefact rather than a finding

Kept visible so nobody reads the tables as settled fact:

- **Resolved.** Barcelona and Madrid were first tested against *bus* operators.
  Both have since been measured properly — Madrid subway 13, Barcelona FGC
  subway 4. **TMB's own feed still 404s**, so Barcelona is understated.
- **Resolved.** Berlin, Hamburg, Stockholm and Oslo were reported rail-free by
  a tool that could not read extended route types. Fixed.
- **Still open.** Mexico City's feed exists and will not download.
  Buenos Aires' SUBTE feed exists at the city's own CDN and **contains no
  `routes.txt`**. Melbourne's is a nested zip. Istanbul's IETT URL is a
  landing page, not a file.
- **Still open.** Manila's rail exists and is typed 2; Hong Kong's MTR exists
  and is published nowhere the catalogue reaches.

Every one is the Toronto lesson: **what a catalogue says about a city is not
what the city runs** — and, added this round, **what a screening tool cannot
parse, it reports as absent.**

## What screening 87 countries showed — five patterns

Synthesis rather than findings. Each is drawn from the measurements above and
each changes how the next screen should be run.

### 1. The transit catalogue has a Western bias, and it distorted this screen

**US 1,180 feeds. South Korea 0.** That is not a fact about transit.

Korea runs one of the world's best metro systems and publishes **1,099
stations with WGS84 coordinates, free and unrestricted**, from its own
government, the whole time. Japan shows 18 feeds of volunteer-run village
buses while MLIT publishes **10,235 stations and 21,932 line segments**.

The Mobility Database measures **GTFS adoption**, which tracks Anglophone and
European open-transit advocacy culture — not transit, and not data
availability. Screening on it **systematically underrates exactly those
countries with the strongest state data infrastructure**.

The screen opened on an instinct that Europe and East Asia were the targets.
That instinct was right; the catalogue made it look wrong.

### 2. The best business registers are national, not municipal

This project's US and Canadian experience taught "municipal licence register"
as the shape to look for. The three strongest sources found globally are all
**national statistical or small-business agencies**: **DENUE** (INEGI),
**SIRENE** (INSEE), **상가(상권)정보** (소상공인시장진흥공단).

All three come from states that run a serious economic census. **The
municipal-licensing model is a North American peculiarity rather than the
norm**, which is why `add-country`'s question 2 mis-sorted half the world
until it was rewritten.

### 3. Licence burden correlates with nothing predictable

| | |
|---|---|
| **Korea** | **이용허락범위 제한 없음** — no restriction at all |
| **Mexico** | attribution **and** disclosure of any transformation |
| **Canada** | OGL, **automatic termination on breach** |
| **UK, much of the EU** | fee-gated registers |

All comparable democracies with strong open-data programmes. Licence looseness
is a **policy choice, not a development indicator**, so it cannot be predicted
from region or wealth — only read. That is the entire case for the
`read-licence` skill.

### 4. The aggregate trap is the most common single failure

Istanbul (counts per district), Japan's Economic Census (counts per area),
Seoul's 상권분석서비스 (per commercial district per quarter), the UK's VOA
(property without names). **Every one looked viable from its title and
description.**

Seoul's was the best disguised, because its categories split into **외식업 10
/ 서비스업 47 / 소매업 43** — this project's own three buckets, exactly.

**The tell is always the same question: is a row a premises, or a summary?**

### 5. Screening cost is highest where the payoff is highest

The cheapest countries to screen — the UK, Australia — **failed**. The richest
— Korea, Japan, Mexico — cost the most, because their data sits outside the
channels the screen knew about and often behind another language.

That argues directly against breadth-first screening and reinforces the
existing depth-per-country rule: the marginal country is expensive precisely
when it is worth having.

## Probe log — every city rail-screened, 2026-09-21

`scripts/screen_rail.py` against real `routes.txt`. **77 feeds fetched across
40 countries.** Counts are route counts in the feed, not stations. Commuter
rail (basic type 2, extended 109) is excluded throughout, as in every built
city.

### Urban rail confirmed

| City | Country | Measured | Feed health |
|---|---|---|---|
| **Paris** | FR | subway 16, tram 17, funicular 1 | current |
| **Vienna** | AT | **subway 35**, tram 185 | current |
| **Madrid** | ES | **subway 13** | current |
| **Singapore** | SG | **subway 13** | current |
| **Lisbon** | PT | subway 10 | current |
| **Amsterdam / Rotterdam** | NL | subway 14, tram 46 | current |
| **Berlin** | DE | urban rail 9, tram 48 | current |
| **Stockholm** | SE | metro 7, tram 21 | current |
| **Santiago** | CL | subway 7, tram 2 | current |
| **São Paulo** | BR | subway 6 | current |
| **Bucharest** | RO | subway 5, tram 15 | current |
| **Oslo** | NO | metro 5, tram 9 | current |
| **Barcelona** | ES | **FGC subway 4, funicular 3** | current — *TMB 404s* |
| **Sofia** | BG | subway 4, tram 24 | current |
| **Hamburg** | DE | underground 4 | **expired 20251213** |
| **Helsinki** | FI | subway 4, tram 26 | **expired 20260731** |
| **Copenhagen** | DK | subway 4, tram 4 | current |
| **Budapest** | HU | subway 4, tram 42 | **expired 20260704** |
| **Bangkok** | TH | subway 4, LRT 5 | current |
| **Prague** | CZ | subway 3, tram 40 | **expired 20260616** |
| **Athens** | GR | subway 3 | current |
| **Naples** | IT | subway 3, tram 3, funicular 3 | current |
| **Hyderabad** | IN | subway 3 | current |
| **Málaga** | ES | subway 2 | **expired 20250226** |
| **Cairo** | EG | subway 2 | **expired 20251027** |
| **Bilbao** | ES | subway 1 | current |
| **Kochi** | IN | subway 1 | current |
| **Guadalajara** | MX | tram/LRT 3 | current |
| **Zagreb** | HR | tram 19 | **expired 20190616** |
| **Poznań** | PL | tram 22 | **expired 20260605** |
| **Riga** | LV | tram 7 | current |
| **Bratislava** | SK | tram 6 | **expired 20221231** |
| **Tallinn** | EE | tram 5 | **expired 20260831** |
| **Hong Kong** | HK | tram/LRT 7, funicular 1 | current — **no MTR in feed** |
| **Messina** | IT | tram 1 | current |

### No urban rail in the feed tested

| City | Country | What came back |
|---|---|---|
| **Manila** | PH | **commuter rail 4** — the LRT/MRT lines, typed as commuter and so excluded |
| **Rio de Janeiro** | BR | bus only — MetrôRio is a separate operator, absent |
| **Auckland** | NZ | commuter rail 5, bus 194 |
| **Jakarta** | ID | bus 252 — Transjakarta is BRT; the MRT is absent |
| **Bogotá** | CO | bus 1000, aerial 1 |
| **Buenos Aires** | AR | bus 1052 — *and the Subte feed has no `routes.txt` at all* |
| **Vilnius, Ljubljana, Belgrade** | LT/SI/RS | bus and trolleybus |

### Fetch failed

**TMB Barcelona**, **MetroValencia**, **Metro de Sevilla**, **SL Stockholm**,
**Istanbul IETT**, **Kyiv**, **Casablanca**, **Mexico City** (403 on S3;
`datos.cdmx.gob.mx` **would not connect**, twice, 21s each), **Dubai RTA**
(the catalogue URL is an anonymous personal GitLab job artefact returning a
non-zip).

### The tool was wrong, and is now fixed

Berlin, Hamburg, Stockholm and Oslo first came back **"no urban rail"**.
They publish **GTFS Extended Route Types** — the TPEG-derived 3- and 4-digit
set where a metro is `401`, an underground `402` and a tram `900` — and
`screen_rail.py` knew only the basic 0–12 values, so it silently discarded
them into "other".

Decoded, the counts matched the real networks exactly: Berlin `400:9` against
9 U-Bahn lines, Hamburg `402:4` against 4, Stockholm `401:7` against 7
tunnelbana lines, Oslo `401:5` against 5 T-bane lines. Four European capitals
were one dictionary away from being wrongly ruled out.

`screen_rail.py` now handles both sets, and treats extended `109` (Suburban
Railway, the S-Bahn family) as commuter rail — excluded, for the same reason
basic type 2 is.

**Wrong-feed selection is the other recurring fault.** Barcelona and Madrid
were first tested against bus operators; Dublin against two airport coach
services; Malaysia against a bus company in Kuala Terengganu rather than
anything in Kuala Lumpur; Australia against Magnetic Island and Maryborough.
Picking "a feed that names the city" is not the same as picking the rail
operator, and in a country with 169 feeds it is close to random.

## Filter 3 — transit feeds, MEASURED 2026-09-21

One fetch of the Mobility Database catalogue (`bit.ly/catalogs-csv`), **3,511
feeds**. Counts are static GTFS feeds registered per country.

| Region | Counts |
|---|---|
| Americas | US 1,180 · CA 156 · BR 16 · MX 12 · CL 9 · CO 7 · AR 4 |
| Europe | **ES 169** · FR 123 · IT 77 · SE 61 · DE 60 · PL 54 · IE 50 · GB 46 · PT 35 · EE 26 · FI 22 · RO 19 · LV 17 · HU 11 · BE 10 · LT 10 · CZ 8 · CH 5 · **NL 2 · AT 2 · DK 1 · NO 1** |
| Asia-Pacific | AU 53 · TR 24 · IN 19 · JP 18 · NZ 10 · TH 10 · MY 10 · TW 9 · SG 4 · AE 3 · HK 2 · IL 2 · **KR 0** |

**A feed count is not a rail count.** Spain's 169 are mostly regional bus.
Per-city rail confirmation is still owed for every candidate below.

### The finding that inverted the working assumption

East Asian *transit* and East Asian *transit data* are different things:

| Country | Feeds | What is actually in them |
|---|---|---|
| **South Korea** | **0** | Nothing. Not one feed in the catalogue. |
| **Taiwan** | 9 | **All rural bus** — Changhua, Nantou, Taichung, Miaoli, Yunlin. No Taipei MRT. |
| **Japan** | 18 | Almost all **local bus and ferry** — Aomori city bus, volunteer-run buses across Shizuoka, an island ferry. Only Kobe Subway and Tokyo's municipal bureau are urban rail; **JR East, Tokyo Metro and the private railways are absent**. |
| **Singapore** | 4 | **SMRT / SBS Transit / LTA** — the MRT is there. |
| **Hong Kong** | 2 | Transport Department. |

**Absence from the Mobility Database is not absence of a feed.** This measures
*catalogue coverage*, which is precisely the trap that produced the Toronto
error — a mirror three months stale and silently missing an entire mode. Korea,
Taiwan and Japan are **catalogue-blind, not ruled out**; each needs a direct
national-source probe, listed at the end.

## The candidates

### Mexico — the strongest shape found anywhere

**MEASURED.** INEGI's **DENUE** (Directorio Estadístico Nacional de Unidades
Económicas), 2024 Economic Census edition: **over 6 million establishments**
with identification, location, economic activity and size, and **geographic
coordinates explicitly published for display on cartography**. Classified by
**SCIAN**, which *is* NAICS — the trilateral US/Canada/Mexico standard.
Available as bulk download and API.

What makes it stronger than France or Korea is the third leg:
`pipeline/taxonomies/naics.py` may transfer largely unchanged, the same
argument that makes Montréal cheap. National coverage, real coordinates **and**
the classification this project already implements is a combination nothing
else here has.

**The licence clears — MEASURED 2026-09-21.** INEGI's terms permit copying,
distributing, publishing, adapting, reordering and extracting its information,
and **commercial exploitation is explicitly allowed**. Three conditions:

- **Attribution in prescribed form:** `Fuente: INEGI, <name of the product the
  information is taken from>`, with the update date where applicable — the
  example INEGI itself gives is `Fuente: INEGI, Censos Económicos 2009`.
- **Derived works must notify the end user of any analysis or transformation
  applied** (*"notificar al usuario final de cualquier análisis o
  transformación que haga a la información"*). This is **Montréal's
  interpretation clause in another language**, and this project plainly
  triggers it — ring density, category buckets, storefront filtering. A bare
  source credit would not satisfy it.
- **No suggestion that INEGI made the modifications or endorses the result.**

No restriction on republishing or on displaying the data on a map.

So Mexico now passes filters 3 and 4 on measured evidence. **What remains is
the transit leg:** 12 catalogue feeds, and whether Metro CDMX is among them is
**unverified**.

### France — strongest at scale, wrong shape

**MEASURED.** SIRENE publishes *établissements* — SIRET is per establishment,
not per company — with addresses and a monthly geolocated file carrying SIRET,
X/Y, commune code and geolocation quality variables, under **Licence Ouverte /
Open Licence version 2.0**. 123 catalogue feeds.

**Its privacy problem is solved upstream.** Establishments with diffusion
status `P` have the entrepreneur's name, commune address **and geolocation
masked** by INSEE. That is Edmonton's `<REDACTED FOR PRIVACY>` at national
scale. Reuse still requires GDPR and *Loi CNIL* compliance and respect for
individual opposition declarations.

**The catch is structural, not legal**, and `add-country` already names it: a
national register covering every city at once is *not* the shape this project
is built for. Scoping and taxonomy were both designed around per-city municipal
registers, and SIRENE includes every office, depot and administrative site
alongside the shopfronts. That is a design question to settle **before** a
screen, not after.

### South Korea — ideal data, no catalogued feed

**MEASURED.** **195 local-government permit types** consolidated onto
`data.go.kr` by the Ministry of the Interior and Safety, including a national
standard dataset (`전국 일반음식점 표준데이터`, ID 15096283) and per-category
ministry files. Carries operating / suspended / closed status, licence and
closure dates, business-type classification, and road-name **and** lot-number
addresses. Licence is **KOGL Type 1** — commercial use and derived works
permitted, attribution required (source, year, institution, URL).

This is the US/Canada municipal-licence model, nationally standardised — the
best structural match to what this project already does.

**Two blockers:**

- **Zero transit feeds in the catalogue**, above. Unresolved.
- **The portal moved on 2026-04-16.** LOCALDATA (`localdata.go.kr`) was closed
  and everything consolidated into `data.go.kr`. The old host **refuses
  connections** (verified). Every endpoint is five months old and all
  documentation written against LOCALDATA is stale.

**ASSERTED:** that coordinates are published in EPSG:5174 (Korea Central Belt
TM). This came from documentation of the *closed* system. The project would
reproject to per-city UTM regardless — Seoul ≈ 127°E is UTM 52N, EPSG:32652.

#### Seoul's own portal, probed 2026-09-21 — the route around the blocker

With `data.go.kr` unreachable, **`data.seoul.go.kr` answers 200** and carries
both legs. MEASURED:

| | |
|---|---|
| Catalogue size | **8,258 datasets** (6,479 data, 1,779 statistics) |
| Direct file downloads | **1,179** carry a `FILE` tab; 5,646 offer `OPENAPI` |
| Freshness | The licensing datasets were updated **2026-09-21**; the subway dataset **2026-09-22** |
| Publisher | Seoul Metropolitan Government, © *Some Rights Reserved* |

**Transit — exists, but API-gated.** `서울교통공사_노선별 지하철역 정보`
(Seoul Transportation Corporation, stations by line, `OA-15442`) covers **lines
1–8 plus line 9 stages 2–3**, published 2018 and updated 2026-09-22. Its file
tab reads **파일이 없습니다** — *no file* — so it is **Open API only, with a
free key**. That is WMATA's gate exactly, which this project has cleared once
before. Note the scope: Seoul Transportation Corporation runs lines 1–9, not
the Korail and Shinbundang lines that also serve the metropolitan network.

**Business — present, and it is a MULTI-SOURCE city.** The national "195 permit
types" resolve at city level into separate per-category datasets, not one
register:

- `서울시 식품위생업소 현황` — food service premises, **and it has a `FILE`
  tab**, the one bucket that is directly downloadable
- `서울시 공중위생업소 현황` — 이·미용 (hair and beauty), 숙박 (lodging),
  목욕업 (bath houses): **the Personal services bucket**
- `서울시 위생처리업`, `세척제 제조업`, `기타 위생용품 제조업`, `대부업체`
  and others

**So at Seoul-portal scope this is Boston's and New York's shape** — coverage
assembled from several registers via `multi-source-city`. But the Retail probe
below found something better, and something worse.

#### The Retail probe — one trap avoided, one source found, and it is out of reach

**REJECTED: `서울시 우리마을가게 상권분석서비스`.** It looks perfect — a
100-category taxonomy split natively into **외식업 10 (food service),
서비스업 47 (services), 소매업 43 (retail)**, the project's own three buckets,
with GRS80TM coordinates. It is **aggregate**: "aggregated by commercial
district (상권) per quarter, not individual store-level data… **no individual
store coordinates**", and its spatial unit changed again in 2024. Seoul's
portal also carries a 소상공인시장진흥공단 extract at **행정동 단위**
(administrative-dong level) — aggregate for the same reason.

That is Istanbul's defect and Japan's Economic Census defect, and this one was
better disguised than either, because the category split matched what this
project needs exactly.

**FOUND: `소상공인시장진흥공단_상가(상권)정보`** — the Small Enterprise and
Market Service's store register, and it is premises-level:

| Field | |
|---|---|
| `상호명` | business name |
| `업종코드` / `업종명` | category code and name |
| `지번주소` / `도로명주소` | lot address and road address |
| **`위도` / `경도`** | **latitude / longitude** |
| `표준산업분류명` | KSIC standard industrial classification |

Nationwide, CSV in UTF-8, on a **10 major / 75 middle / 247 subcategory**
hierarchy. That is one register covering all three buckets with real
coordinates — **comparable to Mexico's DENUE**, and far better than assembling
Seoul's per-category hygiene registers.

**Dataset `15083033` on `data.go.kr` — and the portal came back up, so this is
now MEASURED from the source page rather than from search results:**

| | |
|---|---|
| Title | `소상공인시장진흥공단_상가(상권)정보_20260630` |
| Scope | **영업 중인 전국 상가업소** — active commercial premises, nationwide |
| Classification | KSIC-based (표준산업분류 10th revision), **대분류 10 / 중분류 75 / 소분류 247** |
| Update cycle | **분기** — quarterly. Registered 2026-08-05 |
| Format | **CSV, UTF-8**, explicitly stated, with reading instructions shipped in the zip |
| Legal basis | 소상공인 보호 및 지원에 관한 법률 제13조 |
| Cost | **무료** — free |
| **이용허락범위** | **제한 없음 — no restriction on use** |

**That is the strongest business source found anywhere in this screen.** It is
premises-level with real coordinates, nationally complete, classified on a
247-subcategory standard, refreshed quarterly, and its stated licence scope is
*unrestricted* — which is a lighter obligation than Mexico's DENUE, whose terms
require attribution **and** disclosure of any transformation.

It also **collapses the multi-source problem**: one register covers all three
buckets, so Seoul does not need `multi-source-city` after all, and the
per-category hygiene registers become a cross-check rather than the plan.

**Third-party mirrors exist** (a Seoul extract dated 202506 is on Hugging
Face). **Do not build on one** — that is exactly how the Toronto error
happened. A mirror is acceptable to confirm a schema, never to source a build.

**How to actually get it, traced 2026-09-21.** `data.go.kr` *catalogues* this
dataset but does not host the file — its own metadata says `atachFileYn = N`,
and the bulk CSV lives on **`bigdata.sbiz.or.kr`, which is down** (connection
refused in 0.65s, twice, an hour apart, while `www.sbiz.or.kr` answers 302).

The **Open API is live**:
`apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong` returns **401**, i.e.
the endpoint exists and wants a key. `B553077` is 소상공인시장진흥공단's
institution code, matching the `insttCode` in the dataset's own metadata.

So the business leg needs **a free API key** — WMATA's gate, already cleared
once by this project — not a bulk download.

#### Korea's transit leg — MEASURED, and it is excellent

`전국도시철도역사정보표준데이터` (dataset **15013205**), from
**국가철도공단** under MOLIT, legal basis 도시철도법:

| | |
|---|---|
| Rows | **1,073 stations** |
| Scope | Urban railway nationwide, **including 광역철도** (metropolitan rail), so beyond Seoul Metro's own lines |
| Fields | 역번호, 역사명, 노선번호, 노선명, English and Hanja names, **환승역 여부 및 환승 노선** (transfer flag and lines), **역의 위도·경도**, 운영기관명, 도로명주소, 데이터기준일자 |
| Format | XLSX |
| Update | 연간 (annual) |
| Cost / licence | **무료**, **이용허락범위 제한 없음** |
| Host | `data.kric.go.kr` — **HTTP 200**, and the dataset page `id=32` also 200 |

**Downloaded and parsed 2026-09-21** — `전체_도시철도역사정보_20260630`, via
`data.kric.go.kr/rips/dataset/download.file?type=filedata&id=32&operation=1`
(313 KB XLSX, no key, no login):

**1,099 stations.** Columns exactly as advertised:

| Column | Verified content |
|---|---|
| `역위도` / `역경도` | **WGS84 to 15 dp** — e.g. `37.516125263312901, 127.019760916726` |
| `역사명` / **`영문역사명`** / `한자역사명` | Korean, **English** and Hanja names |
| `노선번호` / `노선명` | line number and name |
| `환승역구분` / `환승노선번호` / `환승노선명` | transfer flag and the lines transferred to |
| `운영기관명` | operating body |
| `역사도로명주소` | road address |

Sample rows are 신분당선 (Shinbundang) stations tagged 수도권 광역철도, so
coverage extends past Seoul Metro to private and metropolitan operators, as
the metadata claimed.

**`영문역사명` is an unplanned win.** It answers the foreign-language label
question for free — Montréal needed a taxonomy decision about label language,
and Korea ships English station names in the file.

**THE REMAINING GAP: this is stations only, with no line geometry.** This
project *draws* every transit line and labels it — an invariant — and in a
GTFS city that geometry comes from `shapes.txt`. A companion dataset
(**15013203**) supplies line *information*, but whether it carries geometry or
only attributes is **unverified**. If it does not, Korea needs a line-shape
source before a build, most likely from 국가공간정보포털. That is the one
open question on this leg, and it is a build blocker rather than a screening
one.

**So both Korean legs are reachable and unrestricted**, and the only gate left
is a free API key for the business register. That moves Korea into Tier 1
contention: premises-level business data with coordinates and a 247-category
standard, national station points with coordinates and transfer information,
and **"제한 없음" on both** — a lighter licence position than any other
candidate in this screen.

**Two corrections to the earlier Tier 2 entry.** Korea was recorded as having
"the ideal single-register shape"; at the scope this project actually works at,
it is multi-source. And its transit leg is reachable but key-gated rather than
absent.

### Spain / Barcelona — the strongest single city

**MEASURED.** The *Cens de locals en planta baixa* — a census of **ground-floor
premises intended for economic activity** — **68,024 premises**, of which
**61,875 active**, split **21,167 retail / 33,740 services**, a 90.9%
occupancy rate, run by the City Council for about ten years and published on
Open Data Barcelona.

This is Montréal's `locaux-commerciaux` exactly, and the Canada retrospective's
argument applies unchanged: a field survey of actual storefronts is arguably a
*better* answer to this project's premise than a licence register, because it
records what is on the street rather than who registered. Spain also leads
Europe on feed count at 169.

**ASSERTED:** that Madrid's *censo de locales y actividades* is the same shape.
Not checked.

### Brazil — real, and expensive

**MEASURED.** CNPJ open data from Receita Federal, published monthly:
**~72 million establishments** with company name, **trade name**, full address,
postcode and **CNAE** classification. 16 catalogue feeds.

Two costs that no city in this project has yet paid:

- **No coordinates.** Geocoding at a scale far beyond Toronto's 159,872.
- **The *sócios* (partner) list is personal data** — names, qualification, age
  range — and must never be downloaded. Toronto's `Client Name` problem at
  national scale.

### Newly surfaced by the exhaustive sweep

The catalogue sweep put 60 further countries on the table. Three were probed;
the rest are listed below rather than silently dropped.

**Dubai (UAE) — the best of the new ones.** **MEASURED:** Dubai Pulse
publishes `ded_license_master` (described as the primary reference for
business licences in **mainland Dubai, excluding the Free Zones**),
`ded_license_activities`, `ded_business_activities` and `ded_commerce_registry`
— CSV plus an API-key-gated API, updated into 2026. That is a municipal
licence register with an activity taxonomy, the US/Canada shape. Dubai Metro
has 3 catalogue feeds.
**Unverified and decisive:** whether the licence records carry **addresses or
coordinates** at all, and what the reuse terms are. A register without a
location is not mappable.

**Chile — right model, fragmented and stale.** **MEASURED:** `datos.gob.cl`
carries *Patentes Comerciales* — municipal commercial licences, exactly the
model this project is built on, since a *patente municipal* is required for any
commercial activity at a fixed location. But it is published **per
municipality** (La Reina, San Antonio and others) rather than as a national
standard, availability is uneven, and **Santiago's own directory is active
licences as of May 2016** — a decade stale. Santiago's metro is excellent and
Chile has 9 feeds, so this is worth a second look at the *current* municipal
portals rather than the national aggregator.

**Istanbul — fails on the data, despite everything else fitting.**
**MEASURED:** İBB runs a real open data portal (`data.ibb.gov.tr`) under its
own Open Data Licence, granting a worldwide, royalty-free, permanent,
non-exclusive right to reuse. But the business-licence dataset is **"the number
of first-class non-food establishments … on a district and sector basis"** —
**aggregate counts per district**, not premises records. Same defect as Japan's
Economic Census: a statistic, not a register. Turkey has 24 feeds and Istanbul
has one of the largest metro networks in Europe, so if a premises-level source
exists elsewhere on that portal this flips — **ASSERTED that it does not**,
based on one dataset.

**Has a metro and feeds, business data unprobed:**

| Country | Feeds | Cities in the catalogue |
|---|---|---|
| India | 19 | Delhi, Mumbai, Bengaluru, Hyderabad, Kochi |
| Romania | 19 | București, Brașov, Constanța, Oradea, Sibiu |
| Hungary | 11 | Budapest, Pécs, Szeged, Miskolc |
| Thailand | 10 | Bangkok, Chiang Mai |
| Malaysia | 10 | (municipality not recorded) |
| Greece | 4 | Athens, Thessaloniki |
| Bulgaria | 4 | Sofia, Pleven |
| Egypt | 5 | Cairo, Port Said |
| Indonesia | 3 | Jakarta, Bogor, Bali |
| Philippines | 3 | Manila |
| Israel | 2 | (municipality not recorded) |
| Ukraine | 7 | Kyiv, Lviv, Odesa — **excluded for now**, active war |
| Russia | 2 | Moscow Oblast, St Petersburg — **excluded**, sanctions and access |

**Has feeds but no urban rail**, so out on filter 2 regardless of data quality:
Estonia (26 — Tallinn is trams only), Latvia (17), Lithuania (10), Cyprus (6),
Slovenia (6), Slovakia (5), Croatia (4), Serbia (7), Luxembourg (3),
North Macedonia (2), Moldova (2), Montenegro, Georgia, Bosnia, Greenland (2).
Several of these run tram networks that would qualify as `route_type 0`, so
"no urban rail" here means **no metro or light-rail system of the scale this
project maps** — worth revisiting only if the project ever takes tram-only
cities.

**Thin coverage, mostly single-city bus feeds**, no further work proposed:
Cameroon (4), Morocco (4), Nicaragua (3), Ethiopia (3), Albania (3), Ghana (2),
Côte d'Ivoire (2), Tunisia (2), Rwanda (2), DR Congo (2), South Africa (2),
Peru (2), Costa Rica (2), Bolivia (2), and fifteen countries with a single
feed each — Algeria, Mali, Sierra Leone, Uganda, Kenya, Dominican Republic,
Zimbabwe, Nigeria, Uruguay, Sri Lanka among them. Addis Ababa, Abidjan, Lagos
and Lima all have rail that the catalogue does not carry, so these are
**catalogue-blind in the same way Korea is** — but none has a known open
premises-level business register, so the business leg would fail first.

### Ruled weak

| Country | Why |
|---|---|
| **United Kingdom** | **MEASURED:** VOA's rating list "records property, not people: an address, a description, a floor area and a value" — premises-level but **no trade name and no category**. Companies House gives registered offices. The FSA food-hygiene register would work and is **food only** — Boston's two-bucket shape. |
| **Japan** (data) | **MEASURED:** the Economic Census publishes **aggregate counts by area**, not an establishment register with addresses. |
| **Belgium** | **MEASURED:** KBO/BCE does carry *vestigingseenheden* at specific addresses, but **full bulk data and API access require formal application and payment**. |
| **Germany, Italy, Sweden, Ireland, Portugal, Austria, Switzerland, Czechia** | **ASSERTED**, none individually probed: the EU default is a *company* register — Handelsregister, Registro Imprese, Bolagsverket, CRO — recording registered offices, usually behind a fee. |
| **Australia** | **ASSERTED:** 53 feeds, but business licensing is not municipal in the US/Canada sense, so filter 3 likely fails despite the good feed coverage. |

Everything else the catalogue knows about is covered under "Newly surfaced by
the exhaustive sweep" above, including the countries ruled out on rail and the
long tail of single-feed coverage. **New Zealand** (10 feeds — Auckland,
Wellington, Christchurch) belongs with Australia: good feeds, and business
licensing that is not municipal in the US/Canada sense. **Colombia** (7 —
Bogotá, Cali) runs BRT rather than metro in Bogotá; Medellín's metro is not in
the catalogue.

## GDPR is filter 4 for all of Europe, and it is the expensive half

The live question is whether **a sole trader's business address is personal
data**. Ontario answered its version explicitly — business-capacity information
is excluded *even when the business is run from a dwelling* — and the Canadian
screen still cost days across four provinces that **did not agree with each
other**.

France answers it *structurally*, by masking non-diffusible records at source,
which is why France is cheap here. No other European candidate is known to.
Expect per-country statutory reading rather than one EU-wide answer, and expect
it to dominate the cost of any European profile.

## Open probes, cheapest decisive first

1. ~~INEGI's licence terms for DENUE.~~ **Done 2026-09-21 — it passes.** The
   remaining Mexican question is the transit leg: **is Metro CDMX in the
   catalogue, and does a readable feed exist?** That is now the single check
   standing between this project and its strongest candidate.
2. **Taiwan → TDX** (Transport Data eXchange, MOTC). Does it serve **static
   GTFS for Taipei Metro and Kaohsiung MRT**, and under what licence?
   Registration-gated, like WMATA — a known cost, not a new one.
3. **Japan → ODPT** (Open Data Platform for Transportation) and the GTFS-JP
   standard. Does it serve static GTFS-JP for **Tokyo Metro, Toei and JR
   East**? The catalogue holds neither the private railways nor JR, which is
   where most of Tokyo's ridership is.
4. **South Korea's transit data**, from the national source rather than the
   catalogue. This single question decides whether the best-matched business
   data in the world for this project is reachable at all.
5. **Barcelona's census schema, live** — columns, coordinates, licence,
   and whether the activity codes resolve to the project's three buckets.
6. **Re-verify Korea's endpoints on `data.go.kr`**, since everything predates
   the April 2026 migration.
7. ~~Dubai's `ded_license_master`.~~ **Moot for now — Dubai fails on transit
   first.** The catalogue's Dubai feed is an anonymous personal GitLab
   repository returning a non-zip, and the transitland fallback 404s. The
   business register may well be excellent; there is no agency feed to pair it
   with until one is found.
7b. **Barcelona's real rail feed.** TMB was never tested — the catalogue's
   Barcelona entry is a bus operator. This is the single cheapest check that
   could promote Spain to Tier 1, since its business leg is already measured.
7c. **Mexico City's feed, retried.** `datos.cdmx.gob.mx` timed out and the S3
   mirror returns 403 with an XML error body. Worth one retry from a different
   network before concluding anything: Guadalajara already carries Mexico on
   its own, but CDMX is the prize.
8. **Istanbul, second look.** One dataset was aggregate; İBB's portal is large
   enough that a premises-level source may exist, and Istanbul's metro would
   make it a strong candidate if one does.
9. **Chile's municipal portals directly**, rather than the national
   aggregator — Santiago's national-portal copy is a decade stale, which says
   nothing about what the municipality publishes today.

## Two framings this screen reversed

Recorded because the pattern matters more than the individual errors, and both
were mine.

| Asserted | Actually |
|---|---|
| Rail is the cheapest disqualifier, so screen it first | True in Canada, false globally — every candidate city has rail. **The readable-feed question is the real one**, and it is a different question |
| East Asia is the obvious target, being transit-rich | Transit-rich and **open-transit-data-poor**. Korea has 0 catalogued feeds, Taiwan's 9 are all rural bus, Japan's 18 are mostly volunteer-run village services |

The second is the more useful lesson: **"has good public transit" and "publishes
a feed this project can read" are independent properties**, and conflating them
would have pointed the whole effort at the wrong continent.
