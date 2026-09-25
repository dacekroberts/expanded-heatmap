---
name: address-join
description: Place a register's rows on the map by JOINING them to an address file that already carries coordinates, instead of writing a geocoder - find that file, measure the join against a control that must reproduce, report tiers, read the misses. Use when a business register has addresses but no coordinates (Taiwan, Japan, Rome), before any geocoder is written, and when choosing between a join and a per-row geocode. Not for registers that already carry coordinates.
---

# Joining a register to an address file instead of geocoding it

Distilled from four countries in two days - **Prague** (RÚIAN), **Copenhagen**
(DAWA), **Brazil** (CNEFE) and **Taiwan** (door-plate files) - each of which
looked like a geocoding project and turned out to be a join or nothing. The
long form, with every number, is `docs/geocoding_retrospective.md`; this is the
checklist the next country must pass through. **Japan is the one it was written
for.**

## Step 1 — Find the address file FIRST. It is four for four

Before any geocoder, ask which agency already publishes **every address with a
coordinate**: the national mapping or cadastre office, the statistics office,
the basic-registers agency, the city's civil-affairs bureau.

| Country | The file that made it a join |
|---|---|
| Czechia | RÚIAN's per-obec address export (`Kód ADM`) — and ROS02 for *establishments* |
| Denmark | DAWA access addresses, keyless |
| Brazil | CNEFE 2022 — carries the establishment AND its coordinate; no join at all |
| Taiwan | each city's `門牌位置數值資料` (door plates, TWD97) |
| Japan | MLIT `位置参照情報` (block and town-chōme level); Digital Agency アドレス・ベース・レジストリ |
| Italy | ANNCSU (`COORD_X_COMUNE` / `COORD_Y_COMUNE`, `CODICE_COMUNALE`) — fill varies by comune, **check the city's own rows** |

**A register's premises may be published by a DIFFERENT agency than the
register.** Prague's trade register (RŽP) owns the establishments; the
basic-registers agency publishes them as open data (ROS02), without the legal
problem the register's own API carried. Ask who else publishes it before
settling for the owner's copy.

## Step 2 — Enumerate the catalogue; never trust a search, a key error, or a guessed URL

- **Send a nonsense term first.** `data.go.jp` returned **18,140** results for
  `zzqqxxkw` — its full count, because it ignores `q`. Seoul's portal did the
  same. When search is ignored, **page the whole catalogue** and filter
  locally.
- A key error is a statement about one endpoint (`data.gov.tw`'s `ER0001`; the
  CSV export needed no key).
- Rio's metro layers and Taiwan's door plates were both found by listing, not
  searching.

## Step 3 — "Unreachable" is four different findings; test which

1. **Our trust store** — use the OS store (`truststore`), never switch
   verification off. Python's bundle lacks Taiwan's GRCA root.
2. **Moved** — the old host redirects or a new one exists (`rzp.cz` →
   `rzp.gov.cz`).
3. **Geo-blocked** — test from **inside the country**: Globalping
   (`api.globalping.io`) has in-country probes where check-host.net has none,
   and test the publisher's main site as a same-network control. Kaohsiung
   answered 3 of 3 Taiwanese probes and no foreign one. A geo-block is the
   publisher's access control: **never routed around** (no proxy, no VPN).
4. **A method refusal, not a block** — ANNCSU answers `403` to `HEAD` and `200`
   to `GET`. Retry with a small ranged `GET` before recording anything.

## Step 4 — Open the rows; the header is not the schema

- Count **fill per column** on real rows. Japan's permits declare `緯度`/`経度`
  and `町字ID` — **0% populated** on 5,722 Minato rows.
- A big file does not need downloading to read its schema: a `Range` request, the
  first 64 KB of a zip inflated with `zlib.decompressobj(-15)`, or a GeoParquet
  footer read from the tail.
- **Downloads need the owner's permission** (name, source, size). Metadata and
  partial reads for the schema do not.

## Step 5 — The join, with a CONTROL that must reproduce

- Parse the register's address into the address file's components; join on the
  finest shared key.
- **Normalisation is found by READING MISSES, not by anticipating.** Taiwan's:
  NFKC; Chinese section numerals; one sub-number separator set `之 － - ― — –`
  (`―`, U+2015, alone was **3.4 points**); chained sub-numbers; floors dropped;
  streets that contain `市`/`鎮`/`里`. Japan's candidates: NFKC, kanji numerals,
  `番`/`番地`/`号`/`-`, `ヶ`/`ケ`/`が`, `大字`/`字`, 住居表示 vs 地番 areas.
- **Pick one control city, measure it once, and re-run it after EVERY parser
  change.** Nothing else counts until it reproduces (Taipei: 92.4%). A
  generalised parser read the control at 91.7% and exposed a bug no other city
  showed.
- Put the measurement in `scripts/screen_<country>_join.py`, modelled on
  `scripts/screen_taiwan_join.py`. If you lift a shared harness out of it, the
  Taipei control must still read 92.4%.

## Step 6 — Report TIERS, never one rate

Exact / base number / block or town centroid / unmatched — each its own figure.
An average hides which tier the map is standing on.

## Step 7 — Read the misses by class and by place

- Taiwan's retail misses were **market stalls and stalls under viaducts** —
  real premises with no door plate (6.8% of Taipei's storefronts).
- Brazil's unclassifiable rows rose in the **richest districts** — a bias to
  disclose.
- **Cross-check a sample against a second method** (Japan: GSI's keyless
  `AddressSearch`, ≤100 requests at 1/s). Two methods agreeing turns a rate into
  a finding. **Never fuzzy-match**: Oslo's `fuzzy=true` placed a shop at a
  different building and still returned a confident coordinate.

## The traps that fail silently

- **The key can be coarser than the address.** Brasília names a *block*, not a
  door: 98.5% of "shared with a dwelling" rows had no door number, so street +
  number merged whole blocks (89.7% → 68.9% once keyed on the `LOTE`).
- **A measurement that returns about zero usually means the MATCHER is wrong.**
  Taipei's department-store test found no rows until the match tolerated the
  `里` / `鄰` the register inserts between district and street.
- **Coordinates in the wrong axis order look plausible.** Prague's S-JTSK needs
  a sign flip AND a swap; the wrong orders land in Germany and the Arctic.
  Transform one known landmark before trusting a CRS.
- **The first page of a register is its oldest rows** — sample several pages.
- **A street name can recur across districts, and a key without the district
  joins to the wrong one — silently, at a HIGHER rate.** Taichung's 2010
  city-county merger left 14,723 street/number keys in more than one district
  (Taoyuan: 11,301). The screen's district-free key read 92.7%; the build keys
  on district too and reads 92.2%, and the half point it gave up was wrong
  answers. Count the keys that occur in more than one district before
  trusting any rate.
- **The two files can name the same district differently.** Taiwan's door-plate
  files carry a district CODE (`鄉鎮市區代碼`, 6600100…) and the register a
  NAME (`西屯區`). Do not hand-type the mapping: learn it from keys that exist
  in ONE district only, print the table, and refuse any district below 90%
  agreement (`pipeline/countries/taiwan_step2.py`, `district_codes`). All 42
  districts of the first two cities mapped at 96.6–100%.
- **An address file may carry projected coordinates only.** Taichung's has
  WGS84 beside TWD97; Taoyuan's has TWD97 (EPSG:3826) alone. Reproject in one
  batch after the keys are built (a per-row transform on 500,000 plates is
  the slow way), and check a landmark.

## Before the join is published

- Run `read-licence` (or the `licence-read` agent) on **every** file in the join —
  the address file carries its own terms (Taiwan's OGDL makes the attribution
  statement load-bearing).
- Privacy: a publisher's "no personal data" declaration does not settle sole
  traders; apply the name rule (trade names only) and `check_personal_exposure.py`.

## Record it where the next session will look

A dated evidence section in `docs/global_country_shortlist.md`, the city's row in
`docs/city_master_list.md`, a `DECISIONS.md` entry, and the brief in
`docs/build_briefs/<city>.md` with a `brief-checks` block that can fail.
