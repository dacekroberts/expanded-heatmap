# DECISIONS drafts - branch `hiroshima` (Band B build session)

Kept here under the owner's rule of 2026-09-30: build sessions keep their
entries in their own drafts file, and the cleanup session folds every drafts
file into `DECISIONS.md` in one pass. Newest first, each entry exactly as it
should land.

### 2026-09-30 - Shared Japanese code: a per-city N02 edition, and a per-city station-gate floor

Two backward-compatible changes for Hiroshima; the six built Japanese cities
read exactly what they read before (their configs set neither).

- **N02 editions** (`pipeline/countries/japan.py`, `N02_EDITIONS` and `n02()`;
  `japan.stations(slug=)`, `japan_step1`, `japan_fetch`). MLIT published N02-25
  on 2026-04-07 (metadata 2026-03-06). N02-24 (metadata 2025-03-26) predates
  Hiroden's 駅前大橋線 (2025-08-03): it still draws the abandoned
  的場町-猿猴橋町-広島駅 track and the closed 猿猴橋町 stop, where N02-25 has the
  new layout (猿猴橋町 gone, 皆実線's new 松川町; OpenStreetMap agrees, no
  猿猴橋町 tram stop). Same columns and CRS; the zip nests one folder deeper.
  A city names its edition in `japan.CITIES` (`"n02": "25"`); the default
  stays N02-24, so moving any built city to N02-25 is that city's own change,
  decided by its drift check. **Recommendation for the cleanup session:**
  every Japanese city could move to N02-25; none was moved here.
- **Gate 1's floor** (`japan_step1.run`): `config.SPACING_MIN_M` where a city
  sets it, else the shared 400 m. Hiroshima's in-city stations are mostly
  Hiroden's tram stops, a median 357 m apart after the group-code collapse
  (platforms 324 m), so the 400 m "still platforms" gate refused a correct
  set. Hiroshima takes 200 m, the value Paris, Marseille, Amsterdam and Riga
  take, not a new number.

### 2026-09-30 - Hiroshima built: food only, two lists, Hiroden drawn

**Built** on branch `hiroshima` (from `origin/master`, `origin/macro-legend`
merged first), page 82, region East Asia, not in the default frame. Band B
(owner, 2026-09-29): food only, since the city publishes only new barber and
salon openings, as PDFs. Downloads and page prose under the owner's
pre-approval (2026-09-30). **13,567 storefronts** (food service 10,028, food
shops 3,539), 9,134 within the halved rings (67.3%), **124 stations on 12
lines**. `coverage` one_bucket, `categories` "Food premises only" (food shops
are food, owner 2026-09-30), `rail_extra` "Both", `record_kind` "Permit
registers".

**Mode "metro"** (for the owner's review with the other per-city modes): no
subway, but JR West's suburban heavy rail is metro by Melbourne's precedent
("suburban heavy rail only"), and the Astram Line is grade-separated
(Monterrey's and Newcastle's).

**Business leg, Fukuoka's shape.** The city's 【窓口申請】食品営業許可施設一覧
（市内全て）, the annual full list as of the end of March 2026 (9,247 rows, 個人
4,393 and 法人 4,854; every 許可満了日 2026-03-31 or later, so a snapshot of permits
in force), plus MHLW's open data for Hiroshima City (12,007 rows, downloaded
2026-09-30; 67 closed). `SUPERSEDES`: 146 city rows for a premises in MHLW's;
`OWN_POINT_FALLBACK`: 242 MHLW rows at MHLW's own point; `ADDRESS_BY_CONSENT`:
4,584 MHLW rows with no published address, **1,779 of 12,682 restaurant permits
(14.0%, "one restaurant in seven" on the page)**. The page's monthly new-permit
files are not added: the full list is the snapshot. **One city-local rule**
(`config.source_rows`): the workbook marks a street stall in 許可条件
(露店による営業 / 露店の営業に限る, 130 rows) and a vehicle in 自動車登録番号 (180 rows,
none marked in its type); both are carried into 業態, where japan_eigyo's form
rules already take them out. The permit classes (一類の営業行為に限る...) match no
form rule. 1,278 菓子 / そうざい rows, 66 (5.2%) factory-like, kept (owner
2026-09-24).

**Placement.** The shared MLIT join: 96.4% block, 0.9% town-chōme, 1.7% MHLW's
point, 150 unplaced (rural outer-ward addresses, the Shareo underground mall).
MHLW's coordinates against the block point: median 34 m, 96.5% within 250 m
(the brief: 35 m, 96.3%). **Census control** (`scripts/japan_census_control.py
hiroshima`, through `heavy_job.py`, measured peak 0.11 GB): 1.80 food-service
pins per 2021 飲食店 establishment, every ward 1.56-1.92 - even, so no ward's
pins land in another's, and just under Fukuoka's 2.01, the other two-list city,
as the withheld MHLW addresses predict.

**Rail.** MLIT N02 in its 2025 edition (entry above), cut at the city line. 12
lines: the Astram Line (N02 classes 16 and 24, one pair); JR West's Sanyo (12 of
131), Kabe (14 of 14), Geibi (14 of 44) and Kure (1 of 28: 矢野, a one-station
stub kept as cut, Kobe's JR Takarazuka precedent); Hiroden's seven legal lines,
drawn (owner 2026-09-29), the Miyajima Line cut at Hatsukaichi (12 of 22). Gate
3 exact: Astram 22, Kabe 14. 13 stations beyond the line excluded. Close pairs
read and kept apart, as MLIT keeps them: JR 広島 and Hiroden's 広島駅 90 m, 五日市
and 広電五日市 40 m, 横川 and 横川駅 102 m, 西広島 and 広電西広島 150 m (different
operators' stations). **Rings halved** on the spacing rule (357 m median);
gate 1's floor 200 m (entry above).

**Station names**, signage style (Tokyo's and Yokohama's, owner 2026-09-28):
13 cited overrides - 11 macrons dropped (Hondōri, Ōmachi, Kōiki-kōen-mae...),
and two of Hiroden's stops OSM had translated or run together
(修大協創中高前 "Hiroshima Shudo University Hiroshima Kyoso Junior and High School"
to "Shudai-kyoso-chuko-mae"; 広大附属学校前 to "Hirodai-fuzoku-gakko-mae") - and
11 spelling aliases (OSM's figures before 丁目, dropped brackets, and 祗 for 祇 in
祗園新橋北, Kyoto's pair). **Line colours** from `scripts/line_colour_search.py
hiroshima`: all 12 clear 45 from the pins; closest pair within 500 m 19.4.

**Personal exposure: PASS.** `check_personal_exposure.py hiroshima` (Japan
pass): the operator's own name shown as a trade name on 0 of 13,567 rows; 3 raw
rows matched the rule and the one that reached the map shows its permit type;
person-like name at a residential unit 0 of 9,134 pins. 申請者名 (個人) and
代表者名 (法人) are read only by the rule, in memory; MHLW's rows name no
individual operator, so the rule cannot run there (Fukuoka's case, disclosed on
the page). **One slip, recorded**: a schema probe at this build printed the
first five rows of each sheet whole to the build session's own console,
operator names and one applicant address among them. Nothing was written to a
file or committed; later probes printed column names and counts only.

**Licence.** The brief's one open point (whether the city's dataset-level PDL
1.0 covers the full-list file) was decided by the owner on 2026-09-24
(`docs/decisions/2026-09-20.md`, the Japan re-banding entry); the row in
`docs/data_sources/japan.md` now says so. Notice 69: DataEye's prescribed 出典
pattern, MHLW's as in Fukuoka's, MLIT's as in Kobe's. **Macro label**: width
66.3 px (measured 2026-09-30, controls reproduced), ("middle", 0, 54) below the
dot and under Fukuoka's pill, clear from dy 48 to 62; PROBLEMS 0 on the
combined tree with Yokohama's branch.

**Left for others.** `docs/japan_city_list.md`: only Hiroshima's row was taken
from the regenerated file (Tokyo's rows drift, unrelated; reported with
Yokohama's READY); its station column counts N02-24's names (123), the map
N02-25's (124).
