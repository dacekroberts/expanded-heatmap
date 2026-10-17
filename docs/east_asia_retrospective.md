# GTBA | Japan, South Korea and Taiwan: 115 maps on three national shapes

Written 2026-10-16 from the record; committed 2026-10-17 on the owner's word.
Companion to [`mexico_retrospective.md`](mexico_retrospective.md),
[`spain_retrospective.md`](spain_retrospective.md) and
[`geocoding_retrospective.md`](geocoding_retrospective.md), which was written
on 2026-09-23 to prepare Japan. The first build here was Seoul on
2026-09-25; the last was Naha, landed with phase 2 at f89bb728 on
2026-10-12. Per-city figures are in `DECISIONS.md` and `docs/decisions/`;
this file is what the three countries cost and changed. Anything not traced
to a file or commit is marked UNVERIFIED.

**Cities built:** Japan 94, South Korea 18, Taiwan 3 (the `country` field in
`app/cities.py`, 2026-10-16). **Left out:** Japan 22 in Band R and 16
discarded; Korea 20 discarded and 14 in the commuter-rail tier; Taiwan 1 in
Band R and 2 discarded (`docs/city_master_list.md`).

---

## The short answer

**East Asia is 115 of the 237 maps, and it got there because two of its
three countries turned out to be one national file.** Korea's SEMAS
storefront file and Taiwan's tax register are Mexico's shape: one source,
so each city after the first is a config. Japan is the exception. Its rail,
city lines, address points and taxonomy are national, but every city
publishes its own permit lists in its own format. So Japan is Spain's shape
in the business leg and Mexico's in everything else (`japan-city` skill,
opening).

Japan alone holds 94 maps, 39.7% of the site. That count rests on three
things: a join instead of a geocoder, shared modules that a new city mostly
configures, and batches run by one lead with up to three subagents. The
cost was carried by privacy and by shared code. The Japanese name rule was
repaired four times after its first version, and at least three repairs
reached maps already live.

The honest limit: Japan's maps carry no general retail, and Tokyo covers 8
of 23 wards for food.

## How the three countries were chosen

**Korea and Taiwan were chosen on measured data; Japan was chosen early and
built last on purpose.** On 2026-09-21 Seoul's food register downloaded
with no account (60fd60bc), and Taiwan's register measured premises-level
(f81be168). Japan's rail was already solved by MLIT's N02 file: 10,235
stations under PDL 1.0 (`docs/global_country_shortlist.md`). Its permits
carried coordinates on 0% of rows (973b1847).

On 2026-09-22 the owner decided Japan would be built last, on the argument
that shared machinery would make it cheaper (`docs/decisions/2026-09-20.md`,
"Japan is a BUILD, and it goes last"). That held, though not as predicted:
no geocoder was written, and what transferred was the lesson to look for
the address file first.

## Japan

### Screening: the health-center lists, MHLW and N02

**A Japanese city passes or fails on its own permit lists, measured against
an official count.** A city with its own health center publishes its own
list; other towns sit in their prefecture's. MHLW's national file of online
filings is the first measure (`japan-city`, "Screening a Japanese city").
It proved an opt-in slice that completed only Fukuoka and Hiroshima; it
serves elsewhere as a points donor and a partial food-shops layer.

Placement needs about 70% of rows addressed. Matsumoto's MHLW file was
35.4% addressed, so its page uses the city's own registers instead.

**Japan publishes no general-retail register, so "Retail" is food shops
only.** The legend says "Food shops" (78499fd8). Of the 94 Japanese pages,
55 carry more than one bucket and 39 carry one (`coverage` in
`app/cities.py`).

### Rail: JR and private lines, no frequency floor

**Japan is the one country where commuter rail is drawn by default.** The
owner included JR and the private railways on 2026-09-24 (ffbb983e), the
third exception after Dublin's DART and Copenhagen's S-tog. The Shinkansen
is out, and lines served only by limited expresses count (2026-09-28).

On 2026-10-06 the owner set no frequency floor for JR or private lines
(calls 46 and 86; `docs/decisions/2026-10-04.md`, "Wave 5"). Maebashi's Jōmō
line runs every 30 minutes and was approved. A stretch with about 11 trains
a day or fewer is drawn and named on its page. N02 carries no timetable, so
no check can enforce this; the brief is where the stretch is named.

Stations collapse on N02's group code, never the name: in Kobe a name
collapse joined two stations 1.5 km apart ("Kobe pipeline built").

### Tokyo, wards and prefecture legs

**Tokyo is 23 publishers, and only 8 publish a usable food list.** Tokyo's
step 2 read 25 sources into 63,989 storefronts at 99.7% block level
(`docs/decisions/2026-09-27.md`, "Tokyo step 2 on the roster"). The 15 wards
without a food list draw hollow stations: 293 of 490 inside the wards
("Tokyo's rail"). Each ward's share of the official count is on the page,
from 9% (Kōtō) to 101% (Shibuya) (`docs/japan_city_list.md`).

The same ward-by-ward pattern reached the suburbs as shared modules:
`tokyo_tama.py` for the Tama ledgers, `saitama_pref.py`, and `chiba_pref.py`
(East-1 and East-2 handoffs). Ageo (Regional) is the one multi-town
Japanese page, with Ina. Chiba Prefecture's food set is old-law only, so
its towns top out at personal services.

## South Korea

**Korea became a SEMAS country because the alternative was closed.** Seoul,
Daegu and Busan were built on their cities' own LOCALDATA permit registers
(Seoul on 2026-09-25; Daegu and Busan on 2026-09-27). The national LOCALDATA
API needs a key, and data.go.kr membership needs a Korean identity check
(`docs/decisions/2026-09-27.md`, "Incheon built on SEMAS's national
storefront register").

SEMAS's 상가(상권)정보 is a keyless ZIP of 352,699,739 bytes, edition
2026-06-30, with a point on every row (same entry). Fifteen cities read it.
Placement is 100% on the register's own point, so Korea needed no join at
all (`korea-city`, trap 3).

The taxonomy is keyed at 소분류, where the catch-all share is 6.4% against
13.1% one level up (Incheon's entry): Barcelona's lesson repeated.
**A city is cut by district code, never by name.** Gwangju's district names
recur in other cities, and a 2026 merger moved its five districts to new
codes (`docs/decisions/2026-10-04.md`, "korea_sbiz: a 시군구코드 filter").

**Rail is OpenStreetMap, with tests that cut hard.** Twenty Korean cities
were discarded: fifteen on station spacing or frequency and five with no
urban rail (`docs/city_master_list.md`). Fourteen more wait in a
commuter-rail tier that has no rule yet. Anyang (Regional) took in Gunpo
and Uiwang on SEMAS's codes (09e1015a); Seoul, Busan and Daegu (Regional)
were briefed and not built, pending SEMAS's social-post scope (call 71).

## Taiwan

**Taiwan was the cleanest of the three, and the smallest.** The national
business tax register lists every trading location; each city's door-plate
file gives every door plate a coordinate (`taiwan-city`). Taichung,
Taoyuan and Taipei (Regional) were all built on 2026-09-25.

The join placed 92.2% in Taichung, 93.6% in Taoyuan, and 91.8 to 95.0% in
Taipei (Regional) (`placement` in `app/cities.py`). Its control, Taipei's
92.4%, reproduced when the parser moved into the pipeline unchanged
(`docs/decisions/2026-09-20.md`, "Taipei (Regional) built").

Two owner rules shape every Taiwanese pin. The head-office rule dropped
1,521 office-like company rows in Taichung (`taiwan-city`). The name rule
shows a sole proprietor's name only with a business marker; Taichung
measured 18.0% of storefronts shown by industry instead.

The join needed the district, because 14,723 street-and-number keys recur
across Taichung's districts (`taiwan-city`, trap 1). Kaohsiung is held in
Band R: its door-plate host answers only from inside Taiwan, and the
project did not route around it.

## Joins: block, chōme and door plate

**Japan, like Taiwan, needed no geocoder: each permit's address joins
MLIT's 位置参照情報 points on town, chōme and first block number.** The
control is Minato: 98.0% at block, 0.2% at chōme, 1.8% unplaced, all mobile
vendors (ca7e7517). Every change to `japan_register.py` re-runs it.

Where ward publishers give their own coordinates, the block point sat a
median 22 to 43 m away (`docs/decisions/2026-09-20.md`, "Japan's coordinate
step is a JOIN"). Block-level placement across the 94 pages runs from 80.2%
(Toyota) to 100% (Minoh) (`placement` in `app/cities.py`). Sapporo's grid
addresses resolve only to the 条丁目 block, about 100 m.

**The join's rules grew one city at a time, each named for the city that
taught it.** Kyoto added four rules on 2026-09-24; the foundation of
2026-10-07 added eight more join switches from 58 briefs. Uji moved from
55.0% to 92.7% at block on them (`docs/decisions/2026-10-04.md`, "The Japan
foundation"). `japan_register.py` is now 1,544 lines; Korea's SEMAS reader
is 142.

## Names and privacy

**All three countries needed their own privacy pass, because the shared
check cannot read a CJK name.** The Latin heuristic finds two capitalized
words; a Japanese, Korean or Chinese name has neither (`cjk-text`, section
5). So its zero is not a finding, and each country got a pass that must
print 0.

Korea withholds a bare personal name at an address that reads residential.
Seoul withheld 138 (`docs/city_master_list.md`, Seoul's row). Taiwan tests
the owner's rule rather than a name list: Taipei (Regional) showed 17,890 of
92,591 sole-proprietor rows by industry (`docs/privacy_verdicts.md`).

**Japan's name rule took five steps, and three reached live maps.** Each
step is in `DECISIONS.md` or `docs/decisions/2026-10-04.md`:

- **Version 1** (2026-09-27): where the trade name is the operator's own
  name, the pin shows its permit type. Operator columns are read in memory
  and never kept.
- **MHLW's 法人名** (2026-10-05): that column held 40,312 sole traders' own
  names among 190,682 filled rows. Adding it moved 17 cities, from 12 names
  withheld to 46.
- **The sign rule** (2026-10-06): a bare surname, a space and one to three
  characters is withheld whatever the operator column says. It moved 20 of
  34 cities, from 56 names withheld to 135.
- **Across premises** (call 209, 2026-10-07): six live maps showed an
  operator's own name on 13 pins. A flag now withholds every row of the
  city with the same trade-name key.
- **The eye sweep** (2026-10-12): the surname list (166 at launch; the
  skill now says about 190, a gap the record leaves unexplained) misses
  rarer names. Reading found 26 more in 13 cities, withheld by key.

**Damaged and masked names show their permit type, never a repair.** A
half-width question mark beside a non-ASCII character marks a lost
character: 1,028 rows in 30 cities (2026-10-12, "a name with a lost
character"). Kawaguchi's city masks 1,350 trade names itself
(`docs/privacy_verdicts.md`). An asterisk-only value is treated as withheld.

**Private-use characters were found late.** Kawaguchi's file uses
private-use code points for three kanji, mapped in its `"gaiji"` table. A
name holding one now shows its classification (S1). Koshigaya, Fujisawa and
Funabashi held such characters too and were caught only after the merge
(`DECISIONS.md`, "East-2 after master's S1 and S2").

## Scale and batching

**Japan went from 0 to 94 maps in 16 days.** Eight were built from
2026-09-27 to 2026-09-30, then the batch of 12 (2026-10-02), wave 2's 14
(2026-10-03), phase 1's 30 (2026-10-07) and phase 2's 30 (2026-10-11/12).

**A city's step files are a few lines; the work is in the config.** Kobe's
step 1 is 18 lines and its step 2 is 17 (`pipeline/kobe/`). Japan's shared
modules, with the taxonomy, run to about 4,200 lines (`wc -l`).

Each batch had one lead and up to three subagents, one city each. The lead
ran every Overpass query and wrote every shared file; subagents never
touched git (East-1 and Regional-1 handoffs). Regional-1 measured about 0.3M
agent tokens and 1.3% of the weekly pool per city. Regional-2 measured about
0.25M tokens and 12 to 18 minutes per city.

**The foundation is what made phase 2 possible in one evening.** Before the
phase 1 builds, every shared-code item in 58 briefs landed once, as switches
built maps did not read (`docs/decisions/2026-10-04.md`, "The Japan
foundation"). It added raising checks for the traps earlier cities found by
hand: no address, no trade name, an uncompared operator column.

**Quantity changed the kind of defect, as in France.** The France batch
retrospective found that one template defect was copied to every city. The
Japanese parallels: one header fix drifted Hiroshima's and Toyama's maps in
the foundation's first run, and the 法人名 gap sat in 17 cities. Each was
caught by a control or a drift check before or soon after landing.

## What was left out

**Tokyo's missing wards are the largest gap.** Chiyoda alone would lift
urban station coverage from 45% to 56%; all 23 wards would reach 98%
(`docs/plan_detail/japan.md`). Four ward requests were drafted in formal
Japanese and parked as the last resort, never sent (c06ad606, bb1d2362).

**Japan's Band R holds 22 cities that need permission or a request.**
Sendai joined at 95.1% block but its site terms forbid reuse without
permission. Chiba, Saitama and Takasaki are the same shape. Takaoka's list
sits on a platform that refuses this machine (`docs/city_master_list.md`).

**Sixteen Japanese cities were discarded.** Nagoya has no standing list,
and its monthly files omit renewals. Wakayama's list is opt-in, about 51% of
the in-force count. The rest fail on coverage, absence or rail.

## The skills, and the comparison with earlier countries

**Japan and Taiwan got their skill from their first city; Korea did not.**
`taiwan-city` came with Taichung (d4463940), and `japan-city` from Kobe
(843929c5). `korea-city` was drafted by staging on 2026-10-04, after 16
Korean cities, from the record rather than the builds (40654847).
`cjk-text` came from Hong Kong on 2026-09-24 (f9eef4af), before any of the
three.

**Mexico and Spain bracketed what a country profile is worth; East Asia
filled in the middle.** Korea's SEMAS and Taiwan's register behaved like
DENUE: the second city cost a config. Rail was the cheap leg here, which
reverses Mexico: N02 gave Japan every line at once.

## Lessons

1. **Look for the published address file before any geocoder.** Taiwan and
   Japan were both joins, as Brazil, Prague and Copenhagen had been.
2. **A national schema is not a national source.** Japan's permits share a
   schema, but each city decides whether and how it publishes.
3. **A CJK name rule needs both a structural test and an eye read.** Each
   structural gap and the surname list's misses were found by reading.
4. **Land shared code once, before a batch, behind switches.** The
   foundation let 60 cities build without moving the 34 already built.
5. **Check every city in a batch for a defect found in one.** The
   private-use glyph was looked for in one East-2 city and present in four.

## Honest limits

- No Japanese map shows general retail; Tokyo's food map covers 8 of 23
  wards, and three of those lists are partial.
- Density is not comparable across the three countries: SEMAS lists every
  storefront, LOCALDATA licensed trades only, Japan permits by type.
- UNVERIFIED: whether the Visuals hold on SEMAS cities was lifted. A note
  outside this repository says so for 2026-10-12.
- UNVERIFIED: a storefront total for the 94 Japanese maps; no file states
  one, and none was summed for this draft.
- The record cannot show hours spent per country, so none are claimed.
