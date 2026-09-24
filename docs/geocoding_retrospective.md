# Geocoding retrospective — Brazil and Taiwan, written to prepare Japan

**Written 2026-09-23**, the day both countries left the band this project
called *"geocoding at national scale"*. The evidence is in
`docs/global_country_shortlist.md` (the Brazil section and "Taiwan finished"),
the licences in `docs/data_sources.md`, and the reasoning in `DECISIONS.md`
under the same date. This file is the lesson, not the log.

**Read it before starting Japan.** Japan is the last country in that band and
the one this project has called its hardest. The single most useful thing
here is the finding that the band's premise was wrong for both of the
countries tested so far — and **why** it was wrong, which is a method that
can be applied to Japan on day one.

---

## 1. The headline: neither country needed a geocoder

The band existed on an assumption: *"the register has addresses and no
coordinates, so a geocoding leg must be built."* Both times, the country
already published **an address file that carries the coordinate**, and the
"geocoding project" became a join, or nothing at all.

| | Brazil | Taiwan |
|---|---|---|
| **What the band assumed** | CNPJ (~72M rows) + a geocoder past Toronto's scale | 商業登記 + a keyless geocoder (NLSC/TGOS) |
| **What was actually there** | IBGE's **CNEFE 2022** — the census address file — records every non-residential address with the enumerator's **description of the establishment AND a field coordinate** | Every city's **door-plate file** (門牌位置數值資料), keyless, monthly: street / lane / alley / number + coordinate |
| **Resulting shape** | **No geocoder, no register.** CNEFE is the business leg AND the coordinate leg — a *premises field survey* | **A JOIN**: the national tax register's address string, parsed, looked up in the door-plate file |
| **Measured** | 9 cities, 6,021–216,037 storefronts each; enumerator's own point on **95.1–99.9%** | **Taipei 92.4 · New Taipei 95.5 · Taoyuan 94.0 · Taichung 92.7%** |
| **Time from "start geocoding" to answer** | One afternoon | One evening |

**This is the third and fourth time**, not the first. Prague (RÚIAN,
99.8%) and Copenhagen (DAWA, 96.9%) were the same shape earlier the same
week. **Four for four.** For Japan, look for the address file before writing
a line of geocoder.

---

## 2. How each was found — the method, in order

These steps are the transferable part. Each one was necessary; skipping any
of them would have produced a wrong answer on this project at least once.

### Step 1 — Ask where the COORDINATES might already live, before where the geocoder is

A national census, a national mapping agency, or the municipal civil-affairs
office usually maintains an address-point register for its own work. It is
rarely filed under "geocoding".

- **Brazil**: the census bureau's *address* file (`ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/`), found while looking for a *join* target — its establishment descriptions were the surprise.
- **Taiwan**: 117 `門牌` (door-plate) datasets on the national catalogue, published by each city's **civil-affairs bureau** (民政局), not by any mapping or transport agency.

### Step 2 — Enumerate the whole catalogue; never trust a search, a key error, or a guessed URL

- **data.gov.tw's `ER0001: API Key錯誤` was ONE endpoint.** The portal's own
  web export (`/datasets/export/csv`) returns all **52,436 datasets** with
  download URLs, licence and field lists, keyless. The project had carried
  "Taiwan's catalogue needs a key" for two days.
- São Paulo's 483 CKAN packages were **read by eye in full**; Rio's
  **9,879** ArcGIS items were listed through `sharing/rest` by org id. Both
  measured negative for a business register — and Rio's own **metro and VLT
  layers** turned up in the same listing, never searched for before.
- **A negative from search is a statement about the search.** This is the
  project's oldest lesson and it paid out again.

### Step 3 — Treat "unreachable" as four different findings, and test which

| What happened | What it was | How it was told apart |
|---|---|---|
| Receita's CNPJ host reset every TLS handshake | **Moved AND geo-blocked** — directory 404 since 2026-01-30 (Internet Archive), Nextcloud share since, and **1 of 16 check nodes answered: the Brazilian one** | `check-host.net`, 16 nodes in 12 countries |
| Kaohsiung's `data.kcg.gov.tw` timed out | **Geo-blocked to Taiwan** — **HTTP 200 from 3 of 3 Taiwanese probes**, a TCP timeout from Japan and the US, while `www.kcg.gov.tw` on the same network answered from everywhere. Recorded for a day as "unreachable from everywhere" because check-host.net has **no Taiwanese node** | **Globalping** (`api.globalping.io`, anonymous, one `HEAD` per probe) **has probes INSIDE the country**; also test the publisher's main site as a same-network control. Diagnosis only — nothing is fetched through a probe |
| `data.taipei` failed TLS in Python | **Our trust store** — Python's bundle lacks Taiwan's government root (GRCA); **curl on Windows verifies it** against the OS store | Try the OS store before concluding anything. **Never switch verification off** |
| The railway bureau's airport-MRT file returned an Incapsula page | **A bot challenge** — not worked around; the national layer covered those stations | Read the response body, not the status code |

**Where the country's own vantage point is missing, the finding is incomplete** — a timeout from six foreign nodes cannot tell "down" from "geo-blocked", and those two have opposite next steps (wait, or ask the publisher). Test from inside the country before recording either.

**A geo-block or bot challenge is a publisher's access control, and this
project does not route around it** — no proxy, no VPN, no disguising a
script as a browser. Receita's geo-block is why Brazil uses CNEFE rather than
CNPJ; TDX's browser/script distinction is why Taiwan's rail comes from the
agencies.

### Step 4 — Open the rows; count what a row IS

- **CNEFE's rows are one per USE-TYPE per address**, not one per business
  (IBGE's dictionary says so). `COD_INDICADOR_ESTAB_ENDERECO` flags rows that
  stand for 2–10, >10 or an unknown number of establishments; 96–97% are
  single. A shopping centre collapses to one to a few rows.
- **Rio's `Estabelecimentos Abertos` looked like a register** — 209,275 rows,
  "by street" in the title — and was **counts** per street × activity group ×
  year. The aggregate trap, caught only by opening it.
- **Taiwan's tax register is one row per trading LOCATION**, and
  `總機構統一編號` (parent ID) makes company branches their own rows — which
  the 商業登記 route it replaced does not.

### Step 5 — Measure the join with a CONTROL that must reproduce

**This caught a real regression.** A generalised Taiwanese parser read
Taipei at **91.7%** against a measured **92.5%**: its street pattern forbade
the characters stripped as district and village (`市`, `鎮`, `里`), so every
street *containing* one failed — `市民大道`, `鎮三街`. Without the control, the
three other cities' numbers would have been reported with the same silent
0.8-point hole. **Rule: run the control city first after any parser change,
and nothing else counts until it reproduces.** `scripts/screen_taiwan_join.py`
says so in its docstring.

### Step 6 — Report match TIERS, not one rate

| Tier | Brazil (CNEFE `NV_GEO_COORD`) | Taiwan (the join) |
|---|---|---|
| Exact | 1 = the census's own coordinate at the address | exact street/lane/alley/number |
| Degraded | 2–3 = modified / estimated; 4 = block face; 6 = census tract | base number (the parent plate for a `之` sub-number) |
| Unplaceable | — | unparsed / no plate |

**Never let a degraded tier hide inside an "exact" rate.** Rio's 0.2% at
census-tract level sits at a tract centroid, not the premises; the build
decides whether to keep it — deliberately, with the number in front of it.

### Step 7 — Read the misses; they are never random

| Country | What the misses were | Why it matters |
|---|---|---|
| **Brazil** | Bare trade names with no category word (`MUNDO VERDE`) — **13% of establishments in São Paulo's periphery, 31% in Pinheiros; 48% in Brasília's Asa Sul** | Dropping them **under-draws the affluent commercial districts**. A bias to state on every page |
| **Taiwan** | **Market stalls** (`環南市場１樓…攤位`) and **stalls under viaducts** (`高架橋下`) — real premises with no door plate; rural addresses with no street | Traditional markets are dense commerce; losing them understates exactly the places a density map should show |

---

## 3. The normalisation that mattered (Taiwan) — and what it predicts for Japan

| Rule | Cost of missing it |
|---|---|
| NFKC — full-width digits `９１號` → `91` | every row |
| Chinese numerals in sections `四段` → `4段` | a whole class of arterial roads |
| **One** sub-number separator from `之 － - ― — –` | **`―` (U+2015) alone was 3.4 points of Taipei** (89.1% → 92.5%) |
| Chained sub-numbers `２之３之２號` → `2-3-2` | Taichung only — a second city surfaced a form the first never had |
| Floors dropped; `39、41號` takes the first | small, steady |
| Streets may contain the characters used to strip admin units | 0.8 points, and invisible without the control |
| Pre-upgrade county names (`桃園縣`, `臺中縣`) | **zero** — checked and empty; cheap to keep |

**Every one of these was found by reading printed misses**, not by
anticipating. Budget for a second city surfacing a form the first did not.

---

## 4. Taxonomy, privacy and licences — the parts that are not geocoding but decide the build

### Taxonomy

- **Brazil: free text.** 118,684 distinct descriptions in Rio alone, so
  `premises-taxonomy`'s *explicit home for every value* cannot apply.
  `scripts/screen_cnefe.py` uses **ordered keyword rules on NAICS bucket
  boundaries**, with **the head noun winning** (the earliest match: `BAR DO
  CLUBE` is a bar) and **vacancy winning anywhere** (`LOJA FECHADA`), plus an
  edit-distance pass for enumerator misspellings. The catch-all is ~20% and
  **cannot go a level deeper — there is no deeper level**.
- **Taiwan: codes with their own names.** The tax register's 6-digit
  industry codes follow ISIC; **47/48, 56, 96** read from the register's own
  code names. **487 (online shopping) excluded** — NAICS 454's twin.

### Privacy — structural rules beat name lists, and the publisher's own refusals are evidence

- **Brazil**: at any address that **also holds a dwelling**, show the
  **category, never the description**. Structural. First names at dwellings
  were 0.8–2.3% of rows; the rule reaches 24–90% (Brasília's superquadra
  addressing puts shops and flats at one address).
- **Taiwan**: for 4.9% of Taipei's storefronts **the business name IS the
  owner's name** — and **the Fiscal Information Agency itself refuses to
  publish owners' names** (2016; again 2026-08-14, on a Ministry of Justice
  proportionality letter). Decided: **show a name only when it is a trade
  name** — companies, branches, and sole proprietors whose name carries a
  business marker. **When a publisher withholds a field, do not reconstruct
  it through another one.**
- Both countries' data-protection laws **reach a foreign reuser** (LGPD art.
  3 III; PDPA 第51條). Removal requests are honoured — the project's standing
  commitment already says so.

### Licences — two recurring shapes

- **The grant is a LAW, not a document** (Brazil): no IBGE licence exists;
  Decree 8.777 art. 4 and Lei 14.129 art. 29 grant free use. Look for the
  statute when the dataset page says nothing.
- **Fault-based liability clauses** (Rio's SIURB terms, IBGE's portal,
  Taiwan's OGDL v1 §六(三)) — liability for damage *you* cause. **All
  accepted by the owner, as a class distinct from Hong Kong's open-ended
  indemnity.** Expect one in Japan's terms too.
- **Attribution that voids the grant if missing** (Taiwan's OGDL v1
  §三(二)) — the notice is load-bearing, and it covers derived coordinates.
- **A share-alike licence with no Produced-Work carve-out** (São Paulo's
  GeoSampa, CC BY-SA 4.0) was **avoided** by drawing from OSM, whose ODbL
  §4.5(b) the project had already settled.

---

## 5. Japan — what is already known, and the order to work in

### Known, from the trail (`global_country_shortlist.md`)

| | |
|---|---|
| **Business leg** | Premises-level **food permits** on a national standard schema (推奨データセット), CC BY. Personal services from **理容所 / 美容所** registers (916 and 917 datasets across Tokyo's municipalities). **No general retail** — a two-bucket cap, Boston's and Toronto's precedent |
| **Coordinates in the permits** | `緯度`/`経度` **0%** (Minato Ward, 5,722 rows); **`町字ID` 0%** — the machine join key exists in the schema and is empty |
| **What IS populated** | `所在地_連結表記` 100%; **split components `都道府県` / `市区町村` / `町字` / `番地以下` 98%**; `施設方書` (building/floor) 95% |
| **Address system** | Block addressing — `赤坂一丁目１番１２号` (chōme / ban / gō), full-width numerals. Not street-based |
| **Geocoder** | GSI `msearch.gsi.go.jp/address-search/AddressSearch` — keyless, **block level**, normalises full-width itself. Per-request: a fallback and a cross-check, not a bulk route |
| **Bulk candidates** | MLIT **位置参照情報** (`nlftp.mlit.go.jp/isj/`) — block-level location reference; Digital Agency **アドレス・ベース・レジストリ** — **refused connections on 2026-09-21** |
| **Rail** | Solved: MLIT N02 — 10,235 stations and 21,932 line segments, PDL 1.0 |
| **Coverage** | Tokyo, Sapporo, Yokohama, Kyoto portals found; **Osaka, Nagoya, Kobe unresolved at guessed URLs — not absent** |

### What this retrospective predicts — ASSERTED until measured

**Japan is probably a JOIN too, at BLOCK level.** The permits already split
the address into prefecture / municipality / town-chōme / 番地以下 on 98% of
rows, and MLIT's 位置参照情報 is a published table of exactly those
components with a coordinate per block (街区). That is Taiwan's door-plate
join, one level coarser. **Block precision is ample for this project's
160–960 m rings** — the GSI probe already noted it.

### The order of work, applying the method above

1. **Find the address file first.** Download MLIT's 位置参照情報 for one
   ward (block level and 大字・町丁目 level) and read its columns and fill.
   **Retry the Address Base Registry from several check nodes** before
   recording anything — "refused" on one day from one network is Step 3's
   first row, not a finding. Enumerate its catalogue; do not guess URLs.
2. **Pick a control ward — Minato** (5,722 permits, already profiled) — and
   join on (市区町村, 町字 with 丁目, 街区符号 from the first number of
   `番地以下`). **Cross-check a sample against GSI's geocoder**: two methods
   agreeing is what turns a rate into a finding.
3. **Expect Japanese normalisation to be where the points go**, as in
   Taiwan — and find the forms by reading misses, not by anticipating. Known
   candidates: NFKC; kanji numerals in `一丁目`; `番` / `番地` / `号` / `-`
   variants; `ヶ` / `ケ` / `が` (霞が関 / 霞ヶ関); old kanji variants (`﨑`/`崎`);
   `大字` / `字` prefixes; **住居表示 vs 地番 areas** (parcel-numbered areas may
   need a different table or a 町丁目-centroid tier); **Kyoto's `上ル` /
   `下ル` / `東入` / `西入` street directions**, where the 町名 carries the
   location; **Sapporo's `条` / `丁目` grid**.
4. **Report tiers from the first run**: block (街区) / town-chōme centroid
   (町丁目) / unmatched — and never average them into one number.
5. **Read the misses by neighbourhood**, as Brazil taught — which districts
   lose more, and whether that biases the map.
6. **Privacy before tooltips**: check whether `施設名称` / `法人名` carry
   individuals' names for sole proprietors, and whether any publisher
   withholds a name field — Taiwan's rule transfers directly.
7. **Coverage by enumeration**: Osaka, Nagoya and Kobe need their catalogues
   *found*, not guessed.
8. **Licences**, one `licence-read` per source: the permit datasets (CC BY
   declared), 位置参照情報, the Address Base Registry. Expect a fault-based
   liability clause and an attribution requirement.

### The machinery to reuse, not copy

The master list's standing warning — *deferring Japan is only cheaper if the
machinery is built SHARED* — now has something concrete to share:

| Reusable piece | Where it is now |
|---|---|
| Component join with tiers, a control city, printed misses by class | `scripts/screen_taiwan_join.py` |
| Free-text classification with head-noun ordering, vacancy, edit-distance | `scripts/screen_cnefe.py` |
| Neighbourhood-skew measurement of the unmatched share | `screen_cnefe.py` section 6 |
| Multi-node reachability test before calling a host dead | `check-host.net`, as used in Step 3 |

**Before Japan's parser is written, lift the join harness — tiers, control,
miss sampling — out of the Taiwan script into shared code**, leaving only the
key-building (how an address becomes components) per country. Japan's
key-building is the hard part; the harness around it should not be written a
third time.
