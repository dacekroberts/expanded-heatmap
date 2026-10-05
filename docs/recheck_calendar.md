# Re-check calendar: every built city (2026-10-02)

The owner asked for a dated re-check calendar "across all currently-built
cities" (2026-10-02), on the model of staging's watch items. Each row is a date
on which something about a built city's map may change: a rail opening,
closure or timetable change on the drawn network, a feed that expires, a
business snapshot crossing the currency ceiling, or a licence or account duty.
Four research agents wrote the regional sections below from the project's own
record, the cached feeds' metadata and operators' pages. Staging merged them
and wrote the action list.

**How to use it.** Work the action list from the top. When an item is done or
superseded, strike it through with its date, as `docs/city_master_list.md`
does. A new event goes into its region's table in date order. Re-run the
research for a region when its table runs out, or after a large landing.

**Coverage gaps, stated by the agents:**
- **Rail news was not web-searched for 14 American cities** (New York,
  Boston, Washington D.C., Miami, Calgary, San Diego, San Francisco,
  Houston, Kansas City, Tucson, New Orleans, Kitchener–Waterloo, Recife and
  Porto Alegre). Their rows rest on project docs and feed metadata only.
- **Lightly searched:** Edinburgh, Strasbourg's north tram, and the Brno,
  Plzeň and Liberec extensions. Some Europe B rows rest on news reports, and
  say so.
- **Tbilisi** (built 2026-10-02, West Asia) is in no regional share. Its
  Geostat register is updated continuously; no dated event is known.

## Action list: the next 120 days, and anything already due

| When | City | What | Who |
|---|---|---|---|
| **Now** | Osaka | **Yumeshima (Chūō Line, open since 19 Jan 2025, regular service since the 2025-10-14 timetable) is missing.** The map uses N02-24; N02-25, already cached, has it. `docs/excluded_categories.md`'s claim that every line with a station in the city is drawn is therefore wrong. Re-run steps 1 and 3 on N02-25. | a build session; Cleanup for the doc |
| **Now** | Hiroshima | Check the map against Hiroden's loop, opened 2026-03-28, after the rail data the map reflects. | a build session |
| **Now** | São Paulo | **Linha 17 has carried passengers since 2026-03-31**, 06:00–22:00 Monday to Saturday, about every 9 minutes; the page and config say "under construction". Linha 6's first six stations have been in free assisted operation since 07-03, until about 12-30. Drawing them is the owner's call (Salvador's VLT precedent). | **owner** |
| **Now** | Los Angeles, San Francisco | LA's cached rail GTFS ended 2026-10-02, and its upstream file is already replaced. SF's stored Muni GTFS had expired (2026-08-28) before it was fetched (09-18), and the configured mirror still serves that file. Refetch before any re-run. | a build session |
| 2026-10-07 | Prague | PID's two-week feed window ends; refetch before any re-run. | — |
| ≈10-13 | Philadelphia | Re-read the licence table (PLAN item d, "frozen since 08-17?"). | staging (`licence-read`) |
| from 10-15 | Sacramento | **The Green Line and the new 7th & Railyards station reopen** ("by mid-October", SacRT). Re-run steps 1 and 3. | a build session |
| 10-18 | Tainan (watch) | Underground switchover; a timetable read decides whether it leaves the commuter-rail group. | staging |
| 10-19 | Milan | The cached ATM GTFS ends (metro colours only); its brief check may fail until AMAT republishes. | — |
| 10-20 | Zurich | VBZ publishes the detail of its 13 December change. | staging |
| after 10-25 | Salvador, Teresina (watch) | Salvador's VLT is in free trial to year-end; Teresina's all-day service may return after the works. | staging |
| 10-25 / 10-31 | Montréal, New York, Toronto | Feeds end (STM 10-25; NY and TTC 10-31). | — |
| 10-31 | 13 Korean cities | SEMAS's next edition; one re-run covers Incheon, the Gyeonggi cities, Daejeon, Gwangju and Gimhae (the full list in the Asia table below). | a build session |
| 10-31 | Japan | MHLW's permit system maintenance; check the downloads still work afterwards. | — |
| ≈11-01 | Birmingham (Regional) | Line 2 to Dudley: "autumn 2026" (TfWM); 1 November only from Dudley Council. Dudley joins if it opens (pre-approved). | a build session |
| 11-23 | Rome | ATAC's trams return in phases, the whole network by 11-23 (news). Drawing trams 2, 3, 5, 14 and 19 is the owner's call. | **owner** |
| 11-23 | Rotterdam | Temporary trams 14 and 18 end; the timetable the build measured starts. | — |
| 11-25 | Mexico City, Guadalajara, Monterrey | DENUE 11/2026 is published. | — |
| 11-28 / 11-30 | Edmonton, Chicago | Feeds end. | — |
| Dec 2026 | Newcastle (Regional) | The Metro goes to every 10 minutes on each line. | — |
| 12-12 / 12-13 | Amsterdam, Rotterdam, Berlin, Göteborg; Czechia (Brno, Liberec, Ostrava); Zurich | National and city timetable changes and feed ends. Liberec's lines 2 and 3 closure is due to end; Ostrava's diversion ends; **Zurich's rebuild** (a second re-run on 2027-05-10). | a build session |
| 12-26 | Seoul, Seongnam | The Wirye tram's target opening. PLAN counts only Seoul, but both ends are in Seongnam. | a build session |
| end 2026 | Taoyuan; Sydney | Taoyuan's Green Line opens its first 7 stations (a scope call); Sydney's Southwest Metro opens (second half of 2026). | **owner** (Taoyuan) |
| **2027-01-05/06** | **all 26 French cities** | **SIRENE's `activitePrincipaleEtablissement` switches to NAF 2025.** A re-run on a new SIRENE file would silently empty every French map. A NAF 2025 mapping is needed before any refresh (`pipeline/countries/france.py`'s watch item, now dated by INSEE). | **a build session; high priority** |
| 2027-01-15 | Copenhagen, Aarhus, Odense | Datafordeler retires its old tabular extracts; confirm the Danish cities use the successor service before any re-run. DAWA already answers 410 Gone. | — |
| 2027-01-27 | Kumamoto | The extended terms on its food permits lapse. | — |

**Corrections to project docs** found by the agents (for Cleanup):
- Prague's Flora station reopens about the end of February 2027, not
  December 2026 (PLAN.md and the rendered page `app/pages/28_Prague_Heatmap.py`).
- Amsterdam's tram 3 was discontinued on 2026-03-29, not paused.
- Oslo's tram 13 (Thune–Lilleaker) has been bus-replaced since 2026-06-10,
  until about February 2027; no doc mentions it.
- Rome's tram 3 was reactivated on 2026-09-07 (Trastevere–Porta Maggiore).
- `docs/data_sources/denmark.md`: DAWA "closes 1 October 2026", but it
  already answers 410.
- São Paulo's Linha 17 is no longer "under construction" (above).
- D.C.'s config says other cities' feeds "can sit for months", but five end
  within eight weeks.
- `docs/gated_access.md` item 12's "follow-up due 2026-09-28" was done.
- Jaén's tram is not open; the Hazel McCallion Line's "early 2028" is the
  end of construction, not its opening.
- Birmingham's brief still tags Line 2 "[Aug 2026]".
- France's 26 tram cities use the operators' GTFS, not OSM (Lille: MEL's GIS
  plus OSM). Staging's prompt said otherwise; no doc does.

## The Americas
Research only; no tracked file edited. Feed windows were read from the zips
already in `data/<city>/raw/` (`feed_info.txt`, else `calendar.txt` /
`calendar_dates.txt`) with `am_feeds.py` in this folder. Business-register
metadata was read from each portal's metadata endpoint. "Read" dates are
2026-10-02 unless stated.

**Coverage caveat.** The session's shared web-search budget ran out partway
through this share. Rail news was searched for Vancouver, Minneapolis, Los
Angeles, Ottawa, Montréal, Edmonton, Monterrey, São Paulo, Seattle,
Sacramento, Belo Horizonte, Brasília, Fortaleza, Santos, Salvador, Buenos
Aires, Mexico City, Guadalajara, Toronto, Chicago, Philadelphia, Buffalo,
Dallas and Pittsburgh (Rio by one fetch). **Not searched for rail:** New
York, Boston, Washington D.C., Miami, Calgary, San Diego, San Francisco,
Houston, Kansas City, Tucson, New Orleans, Kitchener–Waterloo, Recife and
Porto Alegre; their rows below rest on project docs and feed metadata only.

The currency ceiling is five years (`docs/city_master_list.md`, "Five
rules", rule 5.3).

### Calendar

| Date | City | What changes | What to re-run or re-check | Source (URL, date read) |
|---|---|---|---|---|
| 2026-08-28 (passed) | San Francisco | The cached Muni GTFS's calendar ran 2026-07-23 to 2026-08-28, so it had expired before the 2026-09-18 fetch. The mirror linked from SFMTA's page still serves the same file (Last-Modified 2026-08-19, 10,447,937 bytes, identical size) | Any re-run: fetch from SFMTA's own host (`sfmta.com/reports/gtfs-transit-data`), not the mirror, and read the feed dates first | local `data/san_francisco/raw/gtfs.zip`; HEAD `https://muni-gtfs.apps.sfmta.com/data/muni_gtfs-current.zip`, 2026-10-02 |
| 2026-09-25 (passed) | Washington D.C. | WMATA's `feed_info.txt` window (2026-09-15 to 09-25, ten days) has lapsed; `fetch_sources.py` refuses a stored copy past it | Any re-run needs a fresh keyed fetch (`WMATA_API_KEY`) | local `data/washington_dc/raw/feed_info.txt` |
| 2026-10-02 (today) | Los Angeles | Cached LA Metro rail GTFS calendar ends (2026-09-18 to 10-02); the upstream file has already been replaced (1,667,829 bytes against 1,560,117 cached) | Any re-run: refetch; the map itself is frozen | local zip; HEAD `https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip`, 2026-10-02 |
| ≈2026-10-13 | Philadelphia | PLAN's date fix (d): is the L&I licence table frozen since 2026-08-17? | Re-read the Carto table's newest row date | `PLAN.md`, "Published-city date fixes" (d) |
| From 2026-10-15 (SacRT: "by mid-October") | Sacramento | Green Line reopens after the Railyards works, with the new 7th & Railyards station | PLAN's four steps: Green to `LINE_REFS`, clear `CLOSED_FOR_WORKS`, add 7th & Railyards if OSM has it, read the Green Line timetable against 15 min, re-run, update the page sentence. Also retire `ADDED_STATIONS` (Dos Rios) once OSM maps it | https://www.sacrt.com/greenline/ (post dated 2026-09-14; read 2026-10-02); `PLAN.md` |
| 2026-10-25 | Montréal | STM GTFS calendar ends (REM's own feed runs to 2026-12-31) | Refetch both feeds at any re-run | local `gtfs.zip`, `rem_gtfs.zip` |
| 2026-10-31 | New York | MTA NYCT subway feed ends (`feed_end_date`) | Refetch at any re-run | local `gtfs.zip` |
| 2026-10-31 | Toronto | TTC feed calendar ends (no `feed_info.txt`) | Refetch at any re-run; note PLAN's run-date item (step 2 measures Cancel Date against today) | local `gtfs.zip`; `PLAN.md` |
| ≈Q4 2026 (due now) | New York; Buffalo | NYS Retail Food Stores (`9a8c-vfzj`) posts "Annually"; rows last updated 2025-09-30 and unchanged on 2026-10-02, so the 2026 refresh is due | When `rowsUpdatedAt` moves: refetch the retail layer for both cities, drift-check | https://data.ny.gov/api/views/9a8c-vfzj.json (rowsUpdatedAt 1759245315 = 2025-09-30), 2026-10-02 |
| November 2026 (pre-trial running; opening no date) | Ottawa | O-Train East Extension (Line 1, Blair to Trim): pre-trial running moved from early October to November; "no date for LRT opening" | Watch; when it opens, re-run step 1 (the stations are inside the City) and gate 3 | https://www.ctvnews.ca/ottawa/article/oc-transpo-to-provide-update-on-o-train-east-extension-launch-timeline-today/ (2026-09-10; read 2026-10-02) |
| 2026-11-25 | Mexico City; Guadalajara (Regional); Monterrey (Regional) | INEGI publishes DENUE 11/2026; the pages state the May 2026 edition | Optional refresh: one edition for all three (entidad 09, 14, 19), re-run step 2, update `data_age` | INEGI's own account, https://x.com/INEGI_INFORMA/status/2026681676231803168 (DENUE 05/2026 on 2026-05-20, 11/2026 on 2026-11-25), read 2026-10-02 |
| 2026-11-28 | Edmonton | ETS feed ends | Refetch at any re-run | local `gtfs.zip` |
| 2026-11-30 | Chicago | CTA feed calendar ends | Refetch at any re-run (State/Lake stays closed until 2029, outside this window) | local `gtfs.zip`; https://news.wttw.com/2025/12/04/cta-statelake-station-will-be-demolished-january-gleaming-replacement-open-2029 |
| 2026-12-12 | Boston | MBTA "Fall 2026" feed ends | Refetch at any re-run | local `gtfs.zip` |
| ≈2026-12-15 | Montréal | Next vintage of `locaux-commerciaux` (occupation commerciale 2026) expected: 2024's resources were created 2024-12-17, 2025's 2025-12-15; "Annual" | `package_show` for the new resource id (config says re-check rather than trust the id), re-run step 2, page's "2025 survey" | https://donnees.montreal.ca/api/3/action/package_show?id=f8582c4d-a933-4306-bb27-d883e13dd207, 2026-10-02 |
| 2026-12-20 | Calgary | Calgary Transit feed calendar ends | Refetch at any re-run | local `gtfs.zip` |
| ≈2026-12-30 | São Paulo | Linha 6-Laranja's 180-day free assisted operation (six stations, João Paulo I to Perdizes, weekdays 10:00-15:00, from 2026-07-03) ends; commercial operation of the first section expected "second half of 2026" | Owner call: draw L6 (and L17, already running 06:00-22:00; see corrections) under the Salvador VLT precedent; step 1 stops when GeoSampa's operating layer lists them | https://www.cnnbrasil.com.br/nacional/sudeste/sp/governo-de-sp-entrega-primeira-etapa-da-linha-6-laranja-de-metro/ (2026-07-02; read 2026-10-02) |
| 2026-12-31 | Montréal | REM GTFS calendar ends | Refetch at any re-run | local `rem_gtfs.zip` |
| End of 2026 | Salvador | VLT: free assisted operation to "o final deste ano", then paid service (carried over) | Draw once in revenue service with all-day 15 min | staging `watch_items/STATUS.md` |
| 2027-01-03 | Vancouver (Regional) | TransLink feed ends | Refetch at any re-run | local `gtfs.zip` |
| 2027-01-30 | San Diego | MTS feed ends | Refetch at any re-run | local `gtfs.zip` |
| 2027-02-20 | Philadelphia | SEPTA feed ends | Refetch at any re-run | local `gtfs.zip` |
| Spring 2027 | Los Angeles | D Line Section 2: Wilshire/Rodeo (Beverly Hills, outside the City) and Century City/Constellation (inside) | Re-run steps 1-3 and gate 3 once it opens | Metro's project page gives no date (https://www.metro.net/projects/westside/, read 2026-10-02); "spring 2027" per LAist and Wikipedia's Century City station article (secondary) |
| 2027-06-12 | Minneapolis | METRO Green Line Extension opens, Target Field to Eden Prairie, 16 new stations (the first few beyond Target Field are in Minneapolis) | Re-run steps 1-3; gate 3 counts change; confirm which stations fall inside the City's TIGER boundary | https://www.mprnews.org/story/2026/09/26/green-line-extension-to-eden-prairie-southwest-twin-cities-begins-june-2027 (2026-09-26); Met Council project page https://metrocouncil.org/transportation/Projects/Light-Rail-Projects/METRO-Green-Line-Extension.aspx |
| ≈2027-07/08 | São Paulo; Rio de Janeiro; Belo Horizonte; Brasília; Salvador; Fortaleza (Regional); Porto Alegre (Regional); Recife (Regional); Santos (Regional) | CNEFE 2022 reaches the five-year ceiling (Census 2022 fieldwork began August 2022; the master list says "up for re-check in 2027") | The owner's call under rule 5: published cities leave only on the owner's call; look for a newer IBGE address product first | `docs/city_master_list.md`, "Five rules" 3 and the paragraph after it |
| 2027-08-30 | Philadelphia | The L's 11th St reopens (SEPTA release 2026-08-06) | Clear `CLOSED_FOR_WORKS`, re-run, drop the page's 11th St sentence; step 1 stops when the feed serves it | `PLAN.md`; `docs/data_sources/united-states.md` |
| During 2027 (month not stated) | Buenos Aires | The blocks surveyed in 2022 pass five years (survey 2022-2024) | Ceiling check; look for a newer Relevamiento Usos del Suelo; refetch SBASE layers (dated 2026-09-01) when BA Data updates them | `docs/data_sources/argentina.md`; page 58; `PLAN.md` |
| Fall 2027 | Vancouver (Regional) | Broadway Subway (Millennium Line, VCC-Clark to Arbutus, six new stations, all in the City of Vancouver); "scheduled to open for passenger service in fall 2027" | Re-run steps 1-3, gate 3 against TransLink | https://news.gov.bc.ca/releases/2026TT0101-001113 (BC Government, 2026-09-21; read 2026-10-02) |
| Before October 2027 | Monterrey (Regional) | Metrorrey Líneas 4 and 6 (monorail) "entrarán en operación en 2027", before the state administration ends in October 2027 | Re-run; the monorail precedent is São Paulo's Linha 15, drawn | https://mvsnoticias.com/nuevo-leon/2026/9/8/anuncian-que-lineas-4-y-6-del-metro-operaran-en-2027-745134.html (Secretaría de Movilidad, 2026-09-08) |
| 2027 (no month) | Los Angeles | D Line Section 3, Westwood/UCLA and Westwood/VA Hospital (inside the City) | Re-run when open | Wikipedia "D Line Extension", citing LA Metro's The Source (2025-07-23), read 2026-10-02 |
| 2027 (no month) | Montréal | REM airport station (YUL-Aéroport-Montréal-Trudeau): "la mise en service du REM sur ce segment en 2027" | Re-run when it opens (inside the agglomeration) | https://rem.info/fr/aeroport, read 2026-10-02 |
| 2027 (no month; secondary) | Ottawa | Line 1 west to Algonquin and Line 3 to Moodie (Stage 2 west) | Re-run when open | Secondary only (search summaries, Wikipedia); no City date found |
| 2027 | São Paulo | Linha 6 full line to São Joaquim; Maristela by end 2027 | Re-run with the L6 decision above | CNN Brasil 2026-07-02; Gazeta SP |
| End of 2027 | Belo Horizonte | Linha 2's next three stations (Nova Cintra, Vista Alegre, Nova Gameleira); Barreiro mid-2028 | Re-run; gate 3 (L2 now 2 stations) | https://www.otempo.com.br/cidades/2026/9/21/metro-bh-inicia-segunda-fase-das-obras-da-linha-2-com-construcao-de-tres-estacoes-veja (Metrô BH's director-general, 2026-09-21) |
| End 2027 to early 2028 | Fortaleza (Regional) | Metrofor Linha Leste may start phased operation (Seinfra) | Re-run when open | https://diariodonordeste.verdesmares.com.br/negocios/linha-leste-do-metro-de-fortaleza-tem-previsao-para-iniciar-operacao-no-fim-de-2027-diz-secretario-1.3794086 ; O Povo 2026-09-25 |
| Before every deploy (standing) | Washington D.C. | WMATA API account must stay live (gate item 10; last confirmed 2026-09-22) | Owner confirms before each deploy | `docs/data_sources.md` gate item 10; `docs/gated_access.md` item 1 |
| Standing (no date) | Philadelphia | Permission request sent 2026-09-21, followed up 2026-09-28, no reply; owner to choose wait, chase or call | Owner's call; on refusal the city comes down | `PLAN.md`, "Before deploying"; `docs/gated_access.md` item 12 |

### Cities with no dated event (to end 2027)

- **Chicago**: daily licence register; CTA feed rolls (row above); State/Lake back 2029.
- **New York**: four registers, NYS ones yearly (row above); feed rolls; rail not searched.
- **Miami (Regional)**: tax-year register (2026); feed calendar runs to 2027-12-31, no `feed_info.txt`; rail not searched.
- **Boston**: CKAN registers, live; feed rolls; rail not searched.
- **San Diego**: register fetched 2026-09-18 with no source date; feed to 2027-01-30; rail not searched.
- **Calgary**: daily register; feed rolls; Green Line is a 2030s project; rail not searched.
- **Edmonton**: register with expiry dates; feed rolls; Valley Line West is 2028+ (secondary sources); Blatchford Gate still not in service.
- **Toronto**: daily register; feed rolls; Line 5 opened 2026-02-08 and Line 6 are drawn.
- **Guadalajara (Regional)**: DENUE twice a year (row above); OSM rail; Línea 5 is a bus system, not rail.
- **Mexico City**: DENUE (row above); OSM rail; Línea 12 to Observatorio now 2029 (Infobae 2026-07-22).
- **Rio de Janeiro**: CNEFE (row above); Gávea station has no forecast.
- **Brasília**: CNEFE (row above); Samambaia and Ceilândia stations are 2028+.
- **Salvador**: CNEFE; VLT row above; Campo Grande station 2029.
- **Recife (Regional)**, **Porto Alegre (Regional)**: CNEFE; OSM rail; not searched.
- **Santos (Regional)**: CNEFE; VLT L2 open since 2025-12-01 and drawn.
- **Buffalo**: daily register with expiry (Chicago's rule) plus the NYS rows above; OSM rail; DL&W station opened 2025-12-08.
- **Houston**: Comptroller register, live; OSM rail; not searched.
- **Dallas**: Comptroller register, live; OSM rail; Silver Line (opened 2025-10-25) still 30 min peak, 60 off-peak, so it stays out.
- **Kansas City**: register frozen 2026-01-15 (unchanged on 2026-10-02; five-year mark 2031); OSM rail; not searched.
- **Tucson**, **New Orleans**: daily registers; OSM rail; not searched.
- **Pittsburgh**: County list "as of 2025" (2025-08-27; still the newest on WPRDC on 2026-10-02; five-year mark 2030); OSM rail; Mt. Washington tunnel reopened December 2025.
- **Kitchener–Waterloo (Regional)**: inspection files of 2026-07-03, two-year window; OSM rail; ION Stage 2 has no date.
- **Seattle (Regional)**: nightly and daily registers; Snohomish food static to 2025-11-19 (five-year mark 2030); Pinehurst opened 2026-09-30 and is drawn; nothing dated found to end 2027.

### What project docs state wrongly

1. **São Paulo's page and rail record: "Linhas 6 and 17, under construction"**
   (`docs/excluded_categories.md` São Paulo "Stations"; `pipeline/sao_paulo/config.py`,
   `NOT_YET_OPEN_REFS`). Linha 17-Ouro has carried passengers since
   2026-03-31, and from 2026-09-30 it runs 06:00-22:00 Monday to Saturday,
   with the average interval cut from 18 to 9 minutes (still fare-free).
   Linha 6-Laranja's first six stations have been in free assisted operation
   since 2026-07-03 (weekdays 10:00-15:00, 180 days). Both were already
   running when the city was built on 2026-09-24. Whether they are drawn is an
   owner call (the Salvador VLT precedent); "under construction" is wrong
   either way. Sources: https://www.metropoles.com/sao-paulo/linha-17-ouro-6h-as-22h-e-aos-sabados
   (2026-09-29); the CNN Brasil article above (2026-07-02).
2. **San Francisco's feed went unremarked.** The stored Muni GTFS had expired
   (calendar to 2026-08-28) before its 2026-09-18 fetch, and the mirror named
   in `pipeline/san_francisco/config.py` still serves that file. Nothing in
   the config or `docs/data_sources/united-states.md` says the feed was out of
   date. This needs a check, not a rewording: which lines and stations the
   current feed serves.
3. **`pipeline/washington_dc/config.py`: "Every other city's feed can sit in
   `data/<city>/raw/` for months."** Los Angeles's rail feed covers two weeks
   (2026-09-18 to 10-02), Kansas City's cached RideKC feed ends 2026-10-03,
   and four more end within eight weeks (New York and Toronto on 10-31,
   Montréal's STM on 10-25, Edmonton on 11-28).
4. **`docs/gated_access.md` item 12 still reads "Follow-up due 2026-09-28"**.
   `PLAN.md` records the follow-up as done on 2026-09-28, with no reply and
   the next step the owner's to choose.
5. **SacRT's own Green Line page is internally inconsistent.** It says service
   resumes "by mid-October" and that the station opens in "summer 2026". The
   project's PLAN date (check from 2026-10-15) follows the first statement,
   which is right; recorded so nobody reads the second as a slip.

## France, Czechia, the United Kingdom and Ireland
Research only, 2026-10-02. No tracked file edited. 43 built cities: France 26,
Czechia 7, United Kingdom 9, Ireland 1 (Dublin).

How it was gathered:
- **Feed end dates** come from the cached zips in `data/<city>/raw/`
  (`feed_info.txt` where present, otherwise the last `calendar.txt` end date
  or the last added `calendar_dates.txt` date), read by
  `scratchpad/calendar/ea_feeds.py`. Nothing downloaded.
- **Rail and register events**: web search and fetch. The session's shared
  web-search budget ran out part-way (200 calls), so Edinburgh, Strasbourg's
  Tram Nord and the Brno, Plzeň and Liberec extension questions got one
  search or none. See the "nothing dated" list for what that means.

**A correction to this task's own brief**: the French cities are NOT built
from OSM rail. 24 of the 26 take their stops from the city's own GTFS feed
(some take track geometry from OSM), Paris from IDFM's GTFS, and Lille from
MEL's GIS layers plus OSM for the métro lines (`docs/map_inconsistencies.md`
rows 574-599). That is why France has so many feed rows below.

### Table

Feed rows: every French and Czech feed here rolls (it is republished as it
runs out), so a feed end date is not a defect. It is the date after which a
re-run must fetch a fresh copy, and where `fetch_sources.py` records the
window it refuses the expired copy.

| Date | City | What changes | What to re-run or re-check | Source (URL, date read) |
|---|---|---|---|---|
| 2026-10-07 | Prague | PID GTFS `feed_info.txt` window ends (a two-week rolling feed, 2026-09-24 to 2026-10-07) | Any Prague re-run after this date: refetch first; `fetch_sources.py` refuses the expired copy. Keep the Flora override (Flora is still closed, see Feb 2027) | `data/prague/raw/pid_gtfs.zip` feed_info (fetched 2026-09-24), read 2026-10-02 |
| 2026-10-18 | Rennes, Avignon | Feed ends: STAR `EN_COURS` (feed_info end 2026-10-18); Orizo (calendar end 2026-10-18, no feed_info) | Refetch before any re-run. Rennes: still `EN_COURS`, never `A_VENIR` | `data/rennes/raw/gtfs.zip`, `data/avignon/raw/gtfs.zip`, read 2026-10-02 |
| 2026-10-22 | Paris | IDFM GTFS calendar ends (no feed_info.txt) | Refetch before any re-run | `data/paris/raw/gtfs.zip` (fetched 2026-09-23), read 2026-10-02 |
| 2026-10-26 | Toulouse | Tisséo feed's last service date (calendar_dates only) | Refetch before any re-run | `data/toulouse/raw/gtfs.zip`, read 2026-10-02 |
| 2026-10-28 | Nice | Lignes d'Azur `feed_info` end (calendar runs to 2026-12-31) | Refetch before any re-run | `data/nice/raw/gtfs.zip`, read 2026-10-02 |
| 2026-10-31 | Le Havre | LiA feed's last service date | Refetch before any re-run | `data/le_havre/raw/gtfs.zip`, read 2026-10-02 |
| 2026-11-01 | Reims | Grand Reims Mobilités `feed_info` end | Refetch before any re-run | `data/reims/raw/gtfs.zip`, read 2026-10-02 |
| **2026-11-01 (unofficial)** | **Birmingham (Regional)** | **West Midlands Metro Line 2, Wednesbury - Dudley.** TfWM/WMCA still say only "autumn 2026"; 1 Nov is the Dudley Council leader's date, with his own caveat. Carried from the staging watch items | After it opens: re-run step 1 and step 3; Dudley joins as a 4th authority (pre-approved 2026-10-01); drop Line 2 from the not-drawn list and the page bullet "Line 2 ... is not drawn: it is not yet open to passengers" (`app/pages/157_Birmingham_Heatmap.py:74`) | https://www.britishtramsonline.co.uk/news/?p=64552 and https://www.expressandstar.com/news/i-wont-hold-my-breath-dudley-council-leader-reveals-new-date-for-long-delayed-west-midlands-metro-line-8960961 (both via search, 2026-10-02); `../watch_items/STATUS.md` |
| 2026-11-08 | Grenoble (Regional) | M réso feed calendar ends | Refetch before any re-run | `data/grenoble/raw/gtfs.zip`, read 2026-10-02 |
| 2026-11-11 | Le Mans | SETRAM `feed_info` end | Refetch before any re-run | `data/le_mans/raw/gtfs.zip`, read 2026-10-02 |
| 2026-11-27 | Besançon | Ginko `feed_info` end | Refetch before any re-run | `data/besancon/raw/gtfs.zip`, read 2026-10-02 |
| ≈ Dec 2026 (phased) | Newcastle (Regional) | Tyne and Wear Metro goes to every 10 minutes on each line in the weekday daytime (6 trains/h a line, 12 through the core), phased in from December 2026 | No re-run (the map is frequency-blind). Record it where the rail test is written up: it raises the Sunderland branch, which runs on Network Rail track, to 6/h | https://bdaily.co.uk/articles/2026/06/21/mayor-announces-more-metro-services (mayor and Nexus, 2026-06-21), read 2026-10-02 |
| 2026-12-12 | Olomouc | DPMO GTFS `feed_info` end (Olomouc is built from OSM; the feed is cross-check only) | None unless gate 3 is re-taken | `data/olomouc/raw/dpmo-olomouc-cz.zip`, read 2026-10-02 |
| 2026-12-12 / 13 | Liberec (Regional) | Lines 2 and 3 end at Fügnerova and Šaldovo náměstí is closed "to at least 2026-12-12" (the map draws the regular network) | After the 13 Dec timetable change: re-check IDOS for whether lines 2 and 3 run through Šaldovo náměstí again. If the closure is extended, nothing changes on the map | `docs/data_sources/czechia.md` line 31; `pipeline/liberec/config.py:90` (not re-verified on the web: search budget spent) |
| 2026-12-12 / 13 | Ostrava | DPO's diversion timetable (line 6 not running, 13 and 19 instead) ends "about 2026-12-12"; gate 3 was "partial (IDOS, diversion)" | After 13 Dec: re-take gate 3 against IDOS on the regular timetable; it should then be exact | `docs/data_sources/czechia.md` line 30; `docs/map_inconsistencies.md` row Ostrava |
| **2026-12-13** | Prague, Brno, Plzeň, Olomouc, Ostrava, Liberec, Most | Czech annual timetable change (European change date, Sunday 13 Dec 2026). KORDIS's Brno feed calendar ends 2026-12-13; PID's calendar 2026-12-12 | Refetch Brno's feed before any re-run; read each city's new timetable for line changes; Most's Litvínov closure (from 2026-03-01, no end date) to be re-read then | `data/brno/raw/gtfs.zip`, `data/prague/raw/pid_gtfs.zip` (calendar ends), read 2026-10-02; date as VBZ's in `../watch_items/STATUS.md` |
| 2026-12-20 | Brest, Saint-Étienne | Feeds end: Bibus `feed_info` 2026-12-20; STAS calendar 2026-12-20 | Refetch before any re-run | `data/brest/raw/gtfs.zip`, `data/saint_etienne/raw/gtfs.zip`, read 2026-10-02 |
| 2026-12-28 / 29 | Nantes (Regional), Angers, Bordeaux (Regional) | Feeds end: Naolib calendar 12-28; Irigo `feed_info` 12-28; TBM `feed_info` 12-29 | Refetch before any re-run | `data/{nantes,angers,bordeaux}/raw/gtfs.zip`, read 2026-10-02 |
| 2026-12-31 | Marseille, Dijon, Montpellier, Valenciennes (Regional) | Feeds end: RTM/Mecatran `feed_info` 12-31; Divia calendar 12-31; TaM last date 12-31; Transvilles calendar 12-31 | Refetch before any re-run | `data/{marseille,dijon,montpellier,valenciennes}/raw/gtfs.zip`, read 2026-10-02 |
| ≈ late Dec 2026 or early 2027 | Toulouse | New tram shuttle "Ligne Aéroport", Jean-Maga - Toulouse-Blagnac airport (2.5 km). Tisséo moved it from "end of 2026" to "early 2027", no date. Both stops are in Blagnac, outside the commune the map covers; T2 does not return | At the next Toulouse re-run: check whether Tisséo's feed carries it as a new tram route and that the commune scope keeps it off the map (or draws it, if the owner wants the line shown). No new station in scope | https://laclepublique.fr/haute-garonne/articles/2026/2026-09-16-rames-ligne-aeroport/ (2026-09-16), read 2026-10-02 |
| 2027-01-01 | Tours | Fil Bleu calendar ends | Refetch before any re-run | `data/tours/raw/gtfs.zip`, read 2026-10-02 |
| 2027-01-03 | Orléans | TAO `feed_info` end | Refetch before any re-run | `data/orleans/raw/gtfs.zip`, read 2026-10-02 |
| ≈ early Jan 2027 (about 11 months) | Prague | **Hradčanská (line A) closes** for escalator replacement from "the beginning of January 2027", about 11 months; for about two months both it and Flora are closed | Before any Prague re-run in 2027: decide Hradčanská the way Flora was decided (listed as closed for works, owner 2026-09-29). Otherwise the feed drops it and gate 3 (58 against Wikipedia) moves. Watch DPP for the exact date; no DPP release found | https://www.expats.cz/czech-news/article/prague-metro-closures-flora-reopening-delayed-as-hradcanska-shuts-for-2027 (2026-08-23), read 2026-10-02 |
| **2027-01-01, then 2027-01-05/06** | **All 26 French cities** | **SIRENE switches to NAF 2025.** The 1 Jan 2027 files still carry both codings. In the files of 5-6 Jan 2027, `activitePrincipaleNAF25Etablissement` disappears and `activitePrincipaleEtablissement` and `nomenclatureActivitePrincipaleEtablissement` hold **NAF 2025 only**. `pipeline/taxonomies/france_naf.py` keys on rev. 2 sous-classes (`47.11B` style); NAF 2025 writes different codes (`01.11Y` against `01.11Z`), so per `pipeline/countries/france.py`'s own note `classify()` would return None for every row and **empty the map without raising** | **Before any French step 2 runs on a SIRENE stock released from January 2027 on:** build the NAF 2025 mapping from INSEE's 2025 label file, re-measure the catch-alls (96.09Z, 56.29B, 96.03Z have NAF 2025 counterparts), and add a raising check that the rev. 2 codes are present. Until then, the cached national parquet (`data/france/raw/`) must not be refreshed. Every rendered SIRENE description ("NAF rév. 2 at the sous-classe") changes with it | https://www.data.gouv.fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret (read 2026-10-02); https://www.insee.fr/fr/information/8181066 (updated 2026-02-12, read 2026-10-02) |
| **≈ end of Feb 2027** | **Prague** | **Flora (line A) reopens**, about three months later than planned: inspections found more of the platform ceiling needs replacing (DPP transport director, quoted). Its lifts follow later (DPP: end of February 2028) | When PID's feed serves Flora again, step 1 STOPS the build on purpose: remove the override and re-run (PLAN item). Update the page text that says "until about December 2026" | https://www.expats.cz/czech-news/article/prague-metro-closures-flora-reopening-delayed-as-hradcanska-shuts-for-2027 (2026-08-23); DPP release 2026-09-09, https://www.dpp.cz/spolecnost/pro-media/tiskove-zpravy/detail/278_3440-stanice-metra-flora-je-fyzicky-propojena-s-povrchem-novymi-vytahovymi-sachtami; both read 2026-10-02 |
| 2027-03-25 / 26 | Plzeň, Strasbourg | Feeds end: PMDP GTFS 2027-03-25 (gate 3 cross-check only; Plzeň is built from OSM); CTS calendar 2027-03-26 | Strasbourg: refetch before any re-run. Plzeň: only if gate 3 is re-taken | `data/plzen/raw/pmdp_gtfs.zip`, `data/strasbourg/raw/gtfs.zip`, read 2026-10-02 |
| ≈ Q2 2027 | Dublin | New Alstom battery-electric DART units enter service from Q2 2027 for DART+ Coastal North (Drogheda); not the drawn Bray - Howth service | No map change expected. At the next re-run, check that the NTA feed still has the drawn DART route (`BRAY-HOWTH-I`, whitelisted on `ref`) and has not split or renamed it | https://irishcycle.com/2025/10/22/expansion-of-dart-to-drogheda-using-battery-electric-trains-delayed-until-2027/ (news, 2025-10-22, citing Iarnród Éireann), read via search 2026-10-02 |
| 2027-06-25 | Mulhouse | Soléa calendar ends | Refetch before any re-run | `data/mulhouse/raw/gtfs.zip`, read 2026-10-02 |
| 2027-09-22 | Dublin | NTA national GTFS `feed_info` end (2026-09-22 to 2027-09-22) | Refetch before any re-run | `data/dublin/raw/gtfs_all.zip`, read 2026-10-02; `pipeline/dublin/config.py:132` |
| ≈ autumn 2027 (target, not decided) | London | TfL wants to take over the Great Northern inner services (Moorgate - Alexandra Palace, Hertford North, Welwyn) as a London Overground route. Business case with the DfT; no decision | If approved and run: a 7th Overground line inside Greater London, to be drawn with its real name and a legend entry; re-run London step 1 and step 3 | https://www.timeout.com/london/news/a-new-overground-line-could-open-in-north-london-by-2027-120525 (2025-12-05) and https://www.railnews.co.uk/news/2026/01/29-tfl-reveals-ambitions-for-more.html (2026-01-29), read via search 2026-10-02 |
| ≈ Q4 2027 | Toulouse | Métro line B extension south to Labège. Its new stations are outside the commune of Toulouse | No new station in scope; at the next re-run check that the drawn line B is still cut at the commune boundary | https://www.ici.fr/occitanie/haute-garonne-31/toulouse/ligne-c-du-metro-malgre-les-critiques-tisseo-garde-le-cap-pour-une-ouverture-fin-2028-7079518 (via search 2026-10-02; Tisséo's dates as reported) |
| ≈ end of 2027 | Nantes (Regional) | **Tram lines 6 and 7** (Rezé Hôtel-de-Ville - Babinière, La Chapelle-sur-Erdre; Rezé - François-Mitterrand, Saint-Herblain), "à horizon fin 2027". All four communes are in the map's six. Busway line 8 (Sept 2027) is not drawn | After opening: re-run step 1 and step 3; two new drawn lines need their real names on the map and in the legend; ring and storefront counts change | https://metropole.nantes.fr/actualites/comprendre-les-lignes-6-7-8-en-une-minute (updated 2026-05-04), read 2026-10-02 |
| 2027 (no month) | Birmingham (Regional) | Eastside extension's last section to Digbeth: Curzon Street, Meriden Street, Digbeth High Street (excluded now as not yet open); depends on HS2 handing over the Curzon Street site | After opening: re-run step 1 and step 3; take the three stops off `EASTSIDE_REASON` in `pipeline/birmingham/config.py` | https://www.wmca.org.uk/news/plans-brought-forward-to-open-first-section-of-birmingham-eastside-metro-extension/ (2023-11-10, read 2026-10-02); https://www.railmagazine.com/news/network/2023/01/24/birmingham-s-eastside-metro-delayed-until-2027 |
| ≈ end 2027, passengers 2028 | Le Havre | Tram line C (Vallée Béreult - Montivilliers via Graville and Harfleur, 14 km): works end "end of 2027"; the metropole's mobility vice-president puts passenger opening in 2028 | Re-check at the end of 2027; on opening re-run step 1 and step 3 (Graville is in the commune of Le Havre) | https://lehavre.fr/ma-ville/le-havre-ville-en-mouvement/notre-tram-avance-ligne-c and https://fr.wikipedia.org/wiki/Ligne_C_du_tramway_du_Havre (via search 2026-10-02) |

Beyond the window, for the record (no row needed before 2028): Toulouse métro
line C (end 2028), Tours tram line 2 (March 2028, mayor says possibly end
2028), Caen tram line 4 (summer 2029), Ostrava Poruba tram (trial running
2028-29), Nice tram line 4 (2030-31, outside the commune), Dijon T3 (2030),
Manchester Metrolink to Stockport (construction 2030). Toulouse's,
Tours's and Caen's lines are inside their communes.

### Cities with no dated event (one line each)

Business data first, rail second. Every business snapshot in this share is
from 2026, so none crosses the five-year ceiling (master list, "A source must
be current") before 2031; the NAF 2025 row above is the only register change
announced.

- **Paris, Marseille, Lille (Regional), Rennes, Avignon, Reims, Besançon, Dijon, Orléans, Mulhouse, Brest, Saint-Étienne, Montpellier, Bordeaux (Regional), Grenoble (Regional), Valenciennes (Regional), Angers, Rouen (Regional), Caen**: monthly SIRENE (each release is an image of the last day of the month before); rolling operator GTFS (Lille: MEL GIS + OSM); nothing scheduled on the drawn network before 2028 beyond the feed dates and the NAF 2025 switch above. Brest's tram B (opened 2026-02-14), Marseille's T3 extensions (7 and 10 Jan 2026), Montpellier's line 5 (20 Dec 2025), Bordeaux's lines E and F (6 Dec 2025) and Saint-Étienne's Outre-Furan stop (21 Jan 2026) all predate the builds. Lille's 52 m métro trains (from 14 Feb 2026) and Grenoble's and Le Mans's new or longer trams (2026-2030) change no station. Avignon's phase 2 has no date. Caen and Rouen read the Normandy aggregate feed, which runs to 2028-06-30.
- **Strasbourg, Nice, Le Mans, Tours, Le Havre, Toulouse, Nantes (Regional), Orléans**: as above for business data; their only dated items are the feed rows and the extensions in the table.
- **Brno**: monthly ROS02, RES and RÚIAN; KORDIS feed republished weekly (Sundays); nothing scheduled beyond the 13 Dec timetable change (the Kampus line opened in 2022). Extension search thin (budget).
- **Plzeň**: monthly ROS02, RES and RÚIAN; OSM trams; nothing scheduled (Borská pole opened 2019). Extension search thin.
- **Olomouc**: monthly ROS02, RES and RÚIAN; OSM trams; Povel - Slavonín tram awaits a building permit, no opening date.
- **Most (Regional)**: monthly ROS02, RES and RÚIAN; OSM trams; the Litvínov closure has no published end date.
- **Glasgow**: daily FSA register; OSM rail; unattended train operation on the Subway in the second half of 2026 changes no station.
- **Manchester (Regional)**: daily FSA register; OSM rail; no new Metrolink stop has a date (Sandhills, Elton Reservoir and Cop Road are unscheduled).
- **Edinburgh**: daily FSA register; OSM rail; nothing scheduled found (searched only lightly).
- **Sheffield**: daily FSA register; OSM rail; Supertram renewal closures run into 2027 but are temporary, and the map draws the regular network.
- **Nottingham (Regional)**: daily FSA register; OSM rail; nothing scheduled (an extension feasibility study has no published result).
- **Blackpool (Regional)**: daily FSA register; OSM rail; nothing scheduled (the North Station spur opened 2024-06-16, as the docs say).
- **London**: daily FSA register; OSM rail; Code-Point Open postcode centroids (edition 2026-08, new editions through the year; the OS metadata endpoint gives no date). Only the GN Inners target in the table.
- **Dublin**: Tailte Éireann's live valuation register. Reval 2027 (new lists 22 Sep 2027) covers Cork City and Cork County only, not the four Dublin councils. The feed and DART rows are in the table.
- **All four countries**: no key, account, notification or periodic re-read is owed for any source in this share (`docs/gated_access.md` lists none here). Marseille's Mecatran `apiKey` is public and published by the operator.

### What project docs state wrongly

1. **Prague's Flora date is out of date, in three places.** It reopens about the **end of February 2027**, not December 2026 (DPP via expats.cz, 2026-08-23):
   - `PLAN.md:187`: "Flora reopens around December 2026";
   - **`app/pages/28_Prague_Heatmap.py:70` (rendered)**: "closed for reconstruction until about December 2026".
   The rendered line is page text, so its wording goes to the owner at review time.
2. **France's NAF 2025 watch item is now a dated event.** The note at `pipeline/countries/france.py` lines 73-95 says the decision reverses only "if INSEE deprecates rev. 2 in a future monthly release", to be spotted by the 37.5% fill rate rising. INSEE has fixed the date: from the files of 5-6 January 2027, `activitePrincipaleEtablissement` is NAF 2025 only (data.gouv.fr SIRENE dataset page, read 2026-10-02). The note's reasoning, that rev. 2 is "100% populated everywhere", stops being true then.
3. **Birmingham's brief tags Line 2 stops "[Aug 2026]"** (carried from `../watch_items/STATUS.md`). That date was missed; the current unofficial date is 1 Nov 2026.
4. **Not a project doc, but this task's brief:** "France's 26 tram cities use OSM rail" is wrong. They use the operators' own GTFS feeds (see the top of this file), which is why their feed end dates matter.

No other dated claim in this share's docs was found wrong. Liberec's "to at least 2026-12-12" and Ostrava's "about 2026-12-12" could not be re-verified on the web (search budget spent); they are re-checked after the 13 Dec timetable change in the table.

## The rest of Europe
Share "europe_b", 2026-10-02. Research only; no tracked file edited. Cities
(22): Madrid, Barcelona, Palma, Milan, Rome, Florence, Berlin, Oslo, Bergen,
Copenhagen, Aarhus, Odense, Stockholm, Göteborg, Riga, Liepāja, Daugavpils,
Bucharest, Amsterdam, Rotterdam, Den Haag, Zurich. Tbilisi is not in
`cities_europe.txt`, so it is not covered here.

Every source below was read 2026-10-02 unless a date is given. "News" marks
a secondary source used because the operator's page refused a fetch or
none was found; the session's web-search budget ran out before a primary
source was found for every row.

### Calendar

| Date | City | What changes | What to re-run or re-check | Source (URL, date read) |
|---|---|---|---|---|
| 2026-10-05 → 2026-11-23 | Rome | ATAC's tram network comes back in phases after the summer works: trams 5 and 14 Porta Maggiore-Termini 5 Oct, Termini-Largo Preneste 19 Oct, the whole network 23 Nov. Tram 3 already runs Trastevere-Porta Maggiore (since 7 Sep) and tram 8 its whole route (since 21 Sep) | After 23 Nov: re-check trams 2, 3, 5, 14 and 19, which the tram rescope left out as "bus-replaced during works" (`pipeline/rome/config.py`); an owner call on whether any is drawn, then step 1 and step 3 | ATAC, https://www.atac.roma.it/tempo-reale/rete-tram--stato-del-servizio-aggiornato----tutte-le-info (3 on 7 Sep, 8 on 21 Sep); 23 Nov from news only: https://canaledieci.it/2026/09/20/tram-a-roma-la-linea-8-riparte-per-lintera-rete-bisogna-aspettare-il-23-novembre/ |
| 2026-10-19 | Milan | The cached ATM/AMAT GTFS ends: `calendar_dates` 20260914-20261019 (`mm_end_date` 20261015). Milan reads it for the five metro colours only; the rail is ATM's GIS layers | Run `python scripts/brief_check.py milan` after 19 Oct: `atm-gtfs-is-current` reads the live stable URL. The live file was last modified 2026-09-21, so the check may fail until AMAT republishes. The map is unaffected | `data/milan/raw/gtfs.zip` feed_info and calendar_dates; HEAD on https://dati.comune.milano.it/gtfs.zip |
| 2026-10-20 | Zurich | VBZ publishes the line detail of the 13 December change (carried watch item) | Read it, and plan the 13 Dec re-run | https://fahrplanwechsel.vbz.ch/ (staging `watch_items/STATUS.md`) |
| 2026-11-19 | Oslo | Nearly the whole T-bane closes for four days of CBTC tests, with buses elsewhere | No map change. Do not judge a re-run on a feed fetched for that week | https://www.sporveien.no/prosjekter-og-arbeid/t-baneprogrammet/ |
| 2026-11-23 | Rotterdam | RET's temporary trams 14 and 18 (works service 2026-09-22 to 11-22) end. The regular timetable the build measured (`REGULAR_ROUTE_DATES` 20261123-20261212) starts | Check that RET runs as measured; re-run only if it does not | `pipeline/rotterdam/config.py` |
| 2026-12-12 | Amsterdam, Rotterdam | The OVapi national GTFS window ends (feed_info 20260923-20261212). `fetch_sources.py` refuses an expired copy | Any re-run needs a fresh copy. The live file was last modified 2026-10-01 | `data/amsterdam/raw/gtfs-openov-nl.zip` feed_info; HEAD on https://gtfs.openov.nl/gtfs-rt/gtfs-openov-nl.zip |
| 2026-12-12 | Berlin | VBB's `calendar.txt` ends (2026-09-24 to 2026-12-12) | A fresh VBB feed for any re-run | `docs/data_sources/germany.md` |
| 2026-12-12 | Göteborg | Västtrafik's line timetables used for gate 3 (valid 2026-08-17 to 12-12) expire | Re-read gate 3 at the next re-run | `pipeline/goteborg/config.py` |
| 2026-12-13 | Zurich | VBZ's timetable change (carried watch item): the Bahnhofquai reopens, temporary trams 50 and 51 end, 4, 11, 13, 14 and 17 return via the Bahnhofquai, 5 gets peak extensions, 17 runs via Paradeplatz to Bahnhof Wiedikon. ZVV's timetable for gate 3 (2025-12-14 to 2026-12-12) also expires | Re-run step 1 and step 3, then drift-check (PLAN, owner call C1) | https://fahrplanwechsel.vbz.ch/; https://www.bahnonline.ch/90298/vbz-verschieben-verlaengerungen-der-linien-6-und-10-auf-fruehling-2027/ (via STATUS.md) |
| 2026-12-13 | Amsterdam | GVB's Jaarplan Vervoer 2027 starts. No tram-line change was found. Tram 3 was already discontinued on 29 Mar 2026 (see corrections) | Re-check the drawn line list against the new feed at the next re-run | https://www.mobiliteit.nl/ov/2026/03/26/gvb-verandert-dienstregeling-meer-ritten-maar-ook-lijnen-die-verdwijnen/ (news; gvb.nl and over.gvb.nl answer 403) |
| 2026-12-13 | Berlin | VBB/DB timetable change: regional lines only (Stadtbahn closure re-routing). No U-Bahn or S-Bahn station or line change was found | None | https://www.berliner-linienchronik.de/fahrplanwechsel-regio.html |
| 2026-12-13 | Göteborg | Västtrafik's Trafikplan 2027 starts: tram running-time adjustments, no route change | None | https://www.vasttrafik.se/globalassets/media/dokument/trafikplan-2027/nr-11.3-trafikplan-2027.pdf (board paper 2026-06-12) |
| ≈ early Jan 2027 | Den Haag | HTM's 2027 timetable: more frequent trams 9, 2/2k and 17; new low-floor trams on line 1 from spring 2027. No route change. HTM's 2026 timetable started 5 Jan 2026 | None. Gate 3 read HTM's timetable for 2026-10-01 | https://www.denhaag.nl/nl/nieuws/denk-mee-over-dienstregeling-tram-en-bus-in-2027/ (2026-03-24) |
| ≈ early Jan 2027 | Rotterdam | RET's Vervoerplan 2027 (concept public 2026-03-25). No metro or tram route change found; RET's 2026 plan started 5 Jan 2026 | Re-check the line list at the next re-run | https://corporate.ret.nl/nieuws/concept-vervoerplan-ret-2027-openbaar |
| 2027-01-15 | Copenhagen, Aarhus, Odense | Datafordeler retires its tabular "Filudtræk" (file extracts), DAR among them. The builds read `FileDownloads` (`GetFile`, `GetAvailableFileDownloads`), which looks like the successor "Fildownload" service, so they are probably unaffected | Before any Danish re-run, confirm that the endpoint and the owner's key still serve CVR and DAR. CVR keeps each generation for only 7 days | https://confluence.kds.dk/pages/viewpage.action?pageId=16056696 ("Filudtræk med tabulære data udfases 15. januar 2027") |
| ≈ late Jan 2027 | Florence | Tramvia T3.2.1 Libertà-Bagno a Ripoli opens: 7.2 km, 17 stops, after pre-service from the end of 2026 | Owner call "T3 not drawn until it opens": re-run step 1 (OSM stops), step 3 and gate 3 once OSM carries the stops | `pipeline/florence/config.py` (Comune di Firenze, read 2026-09-30); https://www.comune.firenze.it/novita/notizie/linea-3-tramvia-liberta-bagno-ripoli |
| ≈ Feb 2027 | Oslo | Lilleakerbanen (tram 13): Thune-Lilleaker has been bus-replaced since 10 Jun 2026, with overhead-line work to Feb 2027. The 2026-09-24 build has no Lilleaker stop (see corrections) | Re-run step 1 and step 3 once trams return; until then, decide whether to disclose the gap | https://www.sporveien.no/prosjekter-og-arbeid/lilleakerbanen/ |
| 2027-03-21 | Aarhus | Midttrafik's L1 year plan (`l1_k26_20260925-20270320`) ends. It is the source of Grenaabanen's 30-minute frequency, the reason that section is not drawn | Read the next L1 plan's daytime frequency against the 15-minute light-rail test | `docs/build_briefs/aarhus.md` |
| 2027-04-04 | Aarhus | Midttrafik's L2 normal plan (`l2_k26_20261009-20270403`) ends: Odderbanen's frequency | Read the next L2 plan the same way | `docs/build_briefs/aarhus.md` |
| 2027-04-30 | Daugavpils | The operator's GTFS ends (feed_end_date 20270430). It is not used for the build (no licence), but its timetable was gate 3's check | Gate 3 re-read only, at a re-run | `data/daugavpils/raw/GTFS.zip` feed_info |
| 2027-05-10 | Zurich | VBZ's tram 6 (to Letzigrund) and tram 10 (to Bahnhof Enge) extensions, postponed from December (carried watch item) | Second re-run: step 1 and step 3, then drift-check | https://www.bahnonline.ch/90298/vbz-verschieben-verlaengerungen-der-linien-6-und-10-auf-fruehling-2027/ (via STATUS.md) |
| 2027-06-11 → 2027-09-02 | Berlin | No S-Bahn Friedrichstraße-Tiergarten (S3, S5, S7, S9), at times to Zoologischer Garten or Charlottenburg | Do not re-run step 1 on a feed covering the closure without checking that the 10% served-share rule keeps the Stadtbahn | https://www.tagesspiegel.de/berlin/dpa-berliner-nahverkehr-16050452.html (news; S-Bahn Berlin's page not read) |
| 2027-08-16 | Berlin | The U6 Kurt-Schumacher-Platz-Alt-Tegel reopens (BVG's target, the start of the school year): the five Tegel stations | Re-run step 1 and step 3. Gate 3 returns to BVG's 175, and the "about August 2027" notes are retired | https://www.entwicklungsstadt.de/u6-in-tegel-soll-2027-wieder-fahren-das-ist-der-neue-zeitplan/; https://www.berliner-zeitung.de/article/u6-in-berlin-erst-ab-sommer-2027-faehrt-die-u-bahn-wieder-nach-alt-tegel-10248327 (news citing BVG) |
| 2027-09-01 | Riga | The build's monthly GTFS (`marsrutusaraksti08_2026`) calendar ends | Any re-run takes the newest monthly file (`fetch_sources.py` does) | `data/riga/raw/gtfs_rigas_satiksme.zip` calendar (20250501-20270901) |
| 2027-09-29 | Copenhagen | A new metro operator, KBH Metro Partner, takes over M1-M4 | No map change; noted only | https://metroselskabet.dk/da/kontakt-og-presse/presse/pressemeddelelser/kbh-metro-partner-bliver-ny-operatoer-af-metroen-i-koebenhavn/ |
| ≈ autumn (Nov) 2027 | Oslo | The Briskeby line reopens: line 11 returns via Briskeby, and the feed's temporary line 15 (this project's teal) should go | Re-run step 1 and step 3; review `LINE_COLOURS` for 15 and 11 | https://www.sporveien.no/prosjekter-og-arbeid/briskeby-tilpasning/ ("planlagt til høsten 2027") |
| 2027 (year) | Barcelona | The 2022 premises census crosses the five-year currency ceiling. The CKAN package holds no 2025 or 2026 resource (newest 2024, which is incomplete); frequency "PETICIO_NEGOCI" | Re-read the package for a new complete census, and bring the currency question to the owner (rule 3 of the master list's "Five rules": "up for re-check in 2027") | https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_show?id=cens-locals-planta-baixa-act-economica |
| ≈ end 2027 | Barcelona | L9/L10 La Sagrera-Hospital de Sant Pau: four new stations (Guinardó / Hospital de Sant Pau, Maragall, La Sagrera, La Sagrera-TAV) | Re-run step 1 (OSM) and step 3 when they open | https://www.elconfidencialdigital.com/articulo/dinero/barcelona-abrira-4-estaciones-l9-metro-finales-2027/202610020107441490009.html; https://metropoliabierta.elespanol.com/vivir-en-barcelona/20260801/nuevas-estaciones-l9-metro-barcelona-linea-larga/1003742784024_0.html (news) |
| ≈ Nov 2027 (works end); opening ≈ 2028 | Madrid | Line 11 Plaza Elíptica-Conde de Casal: works end about Nov 2027; Comillas and Madrid Río expected to open in 2028 | When CRTM's `M4_Red` carries the new stations, re-run step 1 and step 3 | https://noticiasparamunicipios.com/comunidad-madrid/cuenta-atras-para-el-fin-de-las-obras-de-la-l11-de-metro-entre-plaza-eliptica-y-conde-de-casal/; https://www.eldiario.es/madrid/somos/paso-tuneladora-linea-11-seis-barrios-madrid-perfora-metro-ampliar-red_1_13108108.html (news; metromadrid.es refused the fetch) |
| 2027-12 | Stockholm | Blå linjen Akalla-Barkarby opens: Barkarbystaden and Barkarby, both in Järfälla | Re-run step 1 and step 3: line 11 extends, two stations go to `excluded_stations.csv`, gate 3's per-route counts change | https://nyatunnelbanan.se/barkarby/ |
| 2027-12-07 | Madrid | Brief checks `crtm-metro-network-layer` and `crtm-metro-line-geometry` (`max_age_days` 550 from the layers' last edit, 2026-06-05) start failing unless CRTM edits the layers | Run `brief_check.py madrid`. A stale layer reopens the rail-source decision (CRTM's "siempre actualizada" clause) | `docs/build_briefs/madrid.md` |
| ≈ end 2027 (doubtful) | Odense | Hospital Syd opens with the new OUH. The Region's target is patients by end 2027, which the main contractor calls unrealistic | Step 1 already stops when OSM puts the stop on a route; then re-run and gate 3 to 26 | https://ouh.dk/til-samarbejdspartnere/presse/nyheder-fra-odense-universitetshospital/2024/ny-tidsplan-klar-patienter-kan-rykke-ind-pa-det-nye-ouh-i-2027; https://fredericiaavisen.dk/aabning-af-nyt-ouh-hospital-rykker (news) |
| ≈ 2027 | Bergen | Nonneseter's outbound platform has been closed since 23 Feb 2026 until demolition works end in 2027; the inbound platform is in use | None (one station, still served) | https://www.skyss.no/reise/aktuelt/bybanen-linje-1-og-2-stenging-av-haldeplass-nonneseter/ |

**33 dated rows.** Outside the window, for completeness, are the dates a
frozen register crosses the five-year ceiling: Den Haag's horeca layer
(last edited 2025-05-23) in May 2030, Rome's SUAP (July 2025, declared
monthly, nothing newer published) in July 2030, Stockholm's inspections
(2025-10-21) in October 2030. Gul linjen in Stockholm (2028) and Bucharest's
M6 also fall outside it: M6 has no official opening date (the Metrorex
director says the airport line will be ready in 2027; the official forecast
is operation in 2029).

### Cities with no dated event

- **Palma**: GOIB's register, re-dated by its resource (2026-09-07); Catastro addresses; OSM M1 (ParcBit extension open since 3 Jul 2025, already built). Nothing scheduled.
- **Liepāja**: the national VID excise and VZD cadastre files, daily or monthly; OSM tram. A 1.55 km line reconstruction is funded but undated. Nothing scheduled.
- **Bucharest**: DSVSA files dated 2026-08-25, fetched by the owner (an act each time, behind a browser challenge); OSM metro. M6 has no official date. Nothing scheduled.
- **Riga** (besides the feed): the VID register is daily and the cadastre monthly. The Skanste tram is to be built from Q1 2027 to Q4 2030. Tram 7's extension to Višķu iela (1 Jun 2026) is already in the build's feed.
- **Daugavpils** (besides the feed): national files; OSM tram. Nothing scheduled.
- **Milan** (besides the GTFS): six CKAN registers; M1 to Baggio (2032), M1 north (2029) and M5 to Monza (2033) are all outside the window.
- **Bergen** (besides Nonneseter): a shared 2026-09-24 Brønnøysund cache (daily register; recent API additions, nothing retired); Entur, no window; Bybanen to Åsane is not before 2027.
- **Den Haag**, **Amsterdam**, **Rotterdam** (registers): the horeca layer is frozen at 2025-05-23. Amsterdam's DSO API still answered keyless on 2026-10-02 (a "becomes mandatory" date is still unset on its API docs page). The Gemeenteblad and BAG are continuous.
- **Copenhagen, Aarhus, Odense** (registers): CVR weekly, with 7-day retention; the owner's Datafordeler account is not load-bearing (CC BY 4.0). Nothing else dated.
- **Zurich** (register): `Gastwirtschaftsbetriebe` updated continuously; CC0.
- Standing obligations with no date: **Barcelona's** notification to the City Council, drafted and never sent (`docs/gated_access.md` row 2).

### What the project's docs state that no longer holds

1. **Amsterdam: tram 3 is discontinued, not "not running".** `docs/excluded_categories.md` (Amsterdam's stations paragraph: "Tram 3, which is not running") and `pipeline/amsterdam/config.py` ("Tram 3 is on GVB's 31 August map but runs no trip in the feed's window") both read as a pause. GVB dropped the line in its 29 March 2026 network ("Zo vervalt tram 3 volledig"), with 12 and 25 replacing it. Source: https://www.mobiliteit.nl/ov/2026/03/26/gvb-verandert-dienstregeling-meer-ritten-maar-ook-lijnen-die-verdwijnen/ (news; GVB's own pages answer 403). The claim that the 31 August map still shows a 3 was not re-checked.
2. **Oslo: tram 13 is drawn as it runs during works, and nothing says so.** Sporveien has bus-replaced Lilleakerbanen Thune-Lilleaker since 10 Jun 2026, with work to Feb 2027 (https://www.sporveien.no/prosjekter-og-arbeid/lilleakerbanen/). The rendered `outputs/oslo/heatmap.html` names no Lilleaker stop, and no doc (config, What Is Excluded, map inconsistencies) mentions the closure. This is an omission, not a wrong statement. Briskeby, by contrast, is recorded.
3. **Rome: tram 3 was running when the rescope called it bus-replaced.** `pipeline/rome/config.py` says trams 2, 3, 5, 14 and 19 are "bus-replaced during works (spec, 2026-09-27)". ATAC says tram 3 was reactivated on Trastevere-Porta Maggiore on 7 September 2026 (https://www.atac.roma.it/tempo-reale/rete-tram--stato-del-servizio-aggiornato----tutte-le-info). The others were still bus-replaced on that page.
4. **Denmark: DAWA has closed.** `docs/data_sources/denmark.md` says `api.dataforsyningen.dk` "closes 1 October 2026" and "DAWA closes 1 October 2026", in the future tense. On 2026-10-02 it answered **410 Gone**. Nothing in `pipeline/`, `scripts/` or the briefs' checks calls it.
5. **Odense: "due 2027" for Hospital Syd is now uncertain.** The Region's target is end 2027, and the main contractor has called it unrealistic (https://fredericiaavisen.dk/aabning-af-nyt-ouh-hospital-rykker, news). `pipeline/odense/config.py` and `docs/data_sources/denmark.md` say "opens 2027" or "due 2027".
6. **Berlin: a refinement, not an error.** "About August 2027" for the U6 Tegel branch is now a dated BVG target, **16 August 2027** (news citing BVG, above).

## Asia and Oceania
Share: Japan (20, the twelve batch cities of 2026-10-02 included), South Korea
(12), Taiwan (3), Hong Kong, Sydney, Melbourne, Tbilisi. Research only; no
tracked file edited. Rows come from the project's docs and configs, a local read
of the cached N02-24 and N02-25 zips, and web pages read 2026-10-02 (one or two
searches per city). "(doc)" = dated by a project doc; "(derived)" = follows from
a stated cadence or the five-year rule; "news" = no primary page found.

No city in this share is built on a GTFS feed (all rail is MLIT N02, OSM or an
agency station table), so item 2 (feed expiry) is empty. No dated account or
licence duty was found (no API key, no live-account gate item; Hong Kong's
indemnity and Taiwan's OGDL v1 are accepted standing terms, not periodic).

### Table

| Date | City | What changes | What to re-run or re-check | Source (URL, date read) |
|---|---|---|---|---|
| 2026-10 (now) | Osaka | **The map is missing an open station.** Osaka reads N02-24, which predates Chuo Line's Yumeshima (夢洲, opened 2025-01-19); the map ends the line at Cosmo Square. Yumeshima keeps regular service after the Expo: from the 2025-10-14 revision about every other train turns at Cosmosquare, the rest run to Yumeshima | Move Osaka to N02-25 (`japan.CITIES["osaka"]["n02"] = "25"`, which has 夢洲), re-run step 1 and 3, drift-check | Osaka Metro, https://subway.osakametro.co.jp/news/news_release/20250909_r4_dia_kaisei.php (2026-10-02); local read of `data/japan/raw/N02-24_GML.zip` (0 hits) and `N02-25_GML.zip` (1); `outputs/osaka/heatmap.html` (2026-10-02) |
| 2026-10 (now) | Hiroshima | Hiroden's 循環線 (loop, 的場町 and 段原一丁目 back in use) opened 2026-03-28, after N02-25's reference date (2025-12-31) | Check the drawn Hiroden network against the loop now; if N02-25 lacks the new track, it waits for N02-26 (below) or a disclosed note | https://www.hiroden-hiroshima-st.jp/ (2026-10-02); MLIT N02 page (below) |
| 2026-10 (now; since April 2026) | All 20 Japanese cities | MLIT N03 行政区域 2026 edition (as of 2026-01-01) is out; the project reads N03-2025. N03 only picks stations and anchors labels, and no municipal change in these cities is known | Low priority: move to N03-2026 at the next Japan re-run | https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2026.html ("2026年4月：2026年（令和8年）版に更新") (2026-10-02) |
| 2026-10-10 | Osaka, Sakai | Hankai Tramway timetable change: Funao–Hamadera-ekimae single-tracked (Sakai), Ebisuchō trips cut by two round trips, one extra weekday-morning trip; no stop added or removed | Nothing to re-run; note only if the Hankai Line's frequency is ever questioned | Hankai's own site states the new timetable from 2026-10-10 (https://www.hankai.co.jp/); railf.jp 2026-09-05 (2026-10-02) |
| ≈ 2026-10 (from the 15th) | Kagoshima | City's old-law food list renews quarterly on the 15th of Jan/Apr/Jul/Oct; the build read the 2026-06-30 edition | Re-read the page; a new file name means a config change | `docs/build_briefs/kagoshima.md` (city page: 「1月、4月、7月、10月の15日」) (doc) |
| ≈ 2026-10 | Hakodate | City page announces its next update 「令和8年10月」 for the barber, beauty and laundry registers (build read 2026-08-31) | Re-read `https://www.city.hakodate.hokkaido.jp/docs/2019072900024/`; new file names are a config change | `docs/build_briefs/hakodate.md` line 62 (doc) |
| 2026-10-31 (scheduled) | Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang, Daejeon, Gwangju, Gimhae | SEMAS 상가(상권)정보, quarterly: 차기 등록 예정일 2026-10-31 (the 2026-06-30 edition was posted 2026-08-05, so the 2026-09-30 edition may land in early November) | One shared re-run of the ten cities: step 2, privacy check, drift check | https://www.data.go.kr/data/15083033/fileData.do (2026-10-02) |
| 2026-10-31 | Fukuoka, Tokyo (4 wards), Hiroshima, Matsuyama, Toyama, Kumamoto, Nagasaki, Utsunomiya, Kitakyushu, Sakai, Kagoshima, Okayama (MHLW users) | MHLW 食品衛生申請等システム maintenance, announced for account registration and profile changes; nothing says the open-data downloads change | After that date, confirm one `opendatadownload.jsp` GET still answers | https://i2fas.mhlw.go.jp/ (notice dated 2026-09-30) (2026-10-02) |
| Monthly | Fukui, Utsunomiya, Kitakyushu (personal), Sakai (new and closure files ~25th), Kyoto (new permits), Kōchi (new premises), Fukuoka (BODIK), Taoyuan, Taipei, Taichung (door plates), Daegu (D-데이터허브 edition) | Monthly editions with new file or dataset ids; Fukui's file names carry the month (`_202608`), Daegu's every month is a new set of dataset ids | No row needed unless re-running; a re-run is a config change, never "the newest" | configs `pipeline/<slug>/config.py` (doc) |
| By end of 2026 (ROC 115) | Taoyuan | **New line inside the city**: Taoyuan Metro Green Line priority section G11–G15b, 7 stations (Arts Center to Kengkou), transfer to the Airport MRT at A11/G15b; preliminary inspection 2026-09-08/09 | Scope call (the map is Airport MRT only); if added: step 1, label and legend entry, scope disclosure, re-render | https://dorts.tycg.gov.tw/cp.aspx?n=23132 「預估於115年優先通車段(G11-G15b)通車」 (2026-10-02); "年底" per udn/storm news |
| ≈ 2026-12 | Busan (edge) | Yangsan Line (Nopo–Bukjeong, 7 stations) targets December; Nopo, already drawn on Line 1, is its only Busan station | Probably nothing: confirm no new station falls inside Busan's cut | news: newspim 2026-07-20, nate 2026-07-13 (2026-10-02) |
| 2026-12-26 (target) | Seoul, **Seongnam** | Wirye Line tram, Macheon (Seoul, Songpa) to Bokjeong and Namwirye (Seongnam, Sujeong), 12 stops, 5.4 km; business test running Oct–Dec | January 2027 (PLAN): confirm it opened, count its stops inside Seoul AND Seongnam for the tram rescope | Seoul mediahub https://mediahub.seoul.go.kr/archives/2017377; redaily https://www.redaily.co.kr/news/articleView.html?idxno=16441 (2026-10-02) |
| H2 2026 (no date) | Sydney | Southwest Metro (Sydenham–Bankstown) opens; M1 runs through to Bankstown. No new station in the City of Sydney | Next re-run: check M1's relations and legend; T3's pattern and name may change | https://www.sydneymetro.info/citysouthwest/sydenham-bankstown ("will open in the second half of 2026") (2026-10-02) |
| ≈ 2027-01 | Taichung | Door-plate data is one dataset per ROC year (115年 now); a 116年 dataset with a new id and title is expected | Next re-run: find the 116年 dataset by search (titles vary year to year), update the rid and notice 45's 顯名聲明 | `docs/data_sources/taiwan.md`, taiwan-city skill (derived; the yearly pattern seen in the 114年 dataset on opendata.taichung.gov.tw) |
| 2027-01-27 | Kumamoto | Food permits expiring 2026-08-31 or 2026-11-30 were extended to 2027-01-27 (令和8年熊本地震); unrenewed ones lapse after it, but the list keeps them until its next edition | Read the 2027-03-31 edition (≈ Apr–Jun 2027) rather than dropping rows on 期限満了日 | `docs/build_briefs/kumamoto.md` line 60 (doc) |
| ≈ March 2027 | Okayama | Okaden extends ~100 m into Okayama Station's east plaza; the Okayama-Ekimae stop moves to a new 2-platform, 3-track stop | N02-26 (as of 2026-12-31) will not carry it: move the stop by hand with a note, or wait for N02-27 | Okaden, https://www.okayama-kido.co.jp/tram/tram-status-info/post-2255/ ("2026年度末開業(予定)"); railfromokayama2.com 2026-07-15 ("2027年3月開業へ") (2026-10-02) |
| ≈ mid-March 2027 | All 20 Japanese cities | JR group's annual timetable revision (not yet announced; usually released in December). No JR station change inside a drawn city found for it, apart from JR Kaizuka below | Read each JR company's December release | Wikipedia 2027年の鉄道 (2026-10-02) |
| ≈ Apr–Jun 2027 | Japan: Kobe, Osaka, Sapporo, Fukuoka, Kyoto, Tokyo, Yokohama on N02-24; the 13 others on N02-25 | MLIT's next N02 edition (N02-26, reference date 2026-12-31). MLIT updated in June 2025 (N02-24) and April 2026 (N02-25); it will carry Hiroden's loop | Diff it against N02-25 as for Yumeshima; move cities only on a measured change | https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-2025.html ("2026年4月：2025年度版に更新") (2026-10-02) |
| ≈ May–Jun 2027 | All 20 Japanese cities | MLIT 位置参照情報 next yearly edition (令和8年度). The 令和7年度 edition came out 2026-05-29 and the previous one 2025-06-30; the project's 24.0a / 19.0b are most likely the 令和7年度 edition (version numbers inferred from the series' start years, not printed by MLIT) | At the next Japan re-run, take the newest edition and re-measure each city's join tiers | https://nlftp.mlit.go.jp/isj_news.html (2026-10-02) |
| ≈ Apr–Jun 2027 | Kobe (food), Osaka (registers), Sapporo (food), Hiroshima (annual full list), Matsuyama (年1回), Kumamoto, Kitakyushu (old-law food, yearly), Sakai (standing list as of 2027-04-01), Yokohama (registers as of 2027-04-01), Kyoto and Kōchi (complete lists as of 2027-03-31), Fukuoka (laundry) | Japan's fiscal-year editions as of 2027-03-31 or 04-01 | One Japan batch re-run on the new editions; a new file name is a config change | configs (`SOURCE_AS_OF`) and briefs (derived) |
| 2027 (no month) | Fukuoka | New JR Kyushu station **JR Kaizuka** (JR貝塚), Kagoshima Main Line between Chihaya and Hakozaki, inside Fukuoka City (Higashi-ku), by the subway's Kaizuka | Re-run step 1 once N02 carries it (N02-27 at the earliest) or add it by hand with a note | JR Kyushu, https://www.jrkyushu.co.jp/news/__icsFiles/afieldfile/2025/12/25/251225_thenameofthenewstationhasbeendecided.pdf (2027 opening) (2026-10-02) |
| 2027 (no month) | Hong Kong | Kwu Tung station opens on the East Rail Line's Lok Ma Chau spur | Step 1 (East Rail stations), re-render | HyD, https://www.hyd.gov.hk/en/our_projects/railway_projects/nol/index.html ("expected to come into operation in 2027 as scheduled") (2026-10-02) |
| ≈ 2027 | Melbourne | CLUE is released yearly (2002–2024 now); the 2025 census year is the next | Re-fetch once census year 2025 appears; step 2, re-render | data.melbourne.vic.gov.au / DataVic CLUE pages ("releases ... data yearly") (2026-10-02) |
| 2027 | Sydney | FES 2022 fieldwork reaches the five-year ceiling; a 2027 survey fits the cycle (2007, 2012, 2017, 2022) but none is announced | Watch the FES layer for a 2027 survey year; if none by the ceiling, the owner's call | data.nsw.gov.au FES pages (no 2027 notice found); `docs/city_master_list.md` rule 3 (2026-10-02) |
| ≈ 2027 (may slip to 2028) | Busan | Sasang–Hadan light rail (6.9 km, Sasang to Hadan, both on drawn lines), target 2027 | Q4 2027: draw it once open (label, legend) | news: redaily https://www.redaily.co.kr/news/articleView.html?idxno=13658 (2026-10-02) |
| ≈ 2027-11 | Seoul | Dongbuk Line LRT (Wangsimni–Sanggye, 16 stations) moved from July 2026 to November 2027 | Q4 2027: confirm opening, step 1, label and legend | news: seongdongnews https://www.seongdongnews.com/news/articleView.html?idxno=31975; Seoul councillor, 2026-03-05 (2026-10-02) |
| 2027-11-30 | Tokyo (Koto) | Koto's frozen food list (permits to 2022-11-30) crosses the five-year ceiling | Owner's call: the frozen part sits beside MHLW's current filings by rule; state or drop | `pipeline/tokyo/config.py` `_FOOD_AS_OF["13108"]` (derived) |
| ≈ end of 2027 (completion; opening may be 2028) | Taipei (Regional) | Wanda Line phase 1 (LG): 9 stations, CKS Memorial Hall to Zhonghe, in both cities; 82% complete, completion target ROC 116 | Q4 2027: on opening, step 1 with a label and legend entry, re-render | CNA 2025-11-21 citing Taipei DORTS; gov.taipei release on the 2026-07-21 track milestone (2026-10-02) |
| 2027-12-28 | Tokyo (Chuo) | Chuo's frozen list (to 2022-12-28) crosses the ceiling | As Koto | `pipeline/tokyo/config.py` `_FOOD_AS_OF["13102"]` (derived) |
| 2028-01-01 (just past window) | Tokyo (Shinjuku) | Shinjuku's stated snapshot (2023-01-01) crosses the ceiling | As Koto | `pipeline/tokyo/config.py` `_FOOD_AS_OF["13104"]` (derived) |
| 2028-03-31 / 2028-06-30 (past window) | Nagasaki | Personal registers (2023-03-31) and food list (2023-06-30) cross the ceiling | Look for a newer BODIK edition before 2028 | `pipeline/nagasaki/config.py` (derived) |
| ≈ 2028-04-30 (past window) | Utsunomiya | Old-law food list empties as its last permits expire; MHLW carries the rest | None before then | `docs/build_briefs/utsunomiya.md` (doc) |

### Cities with no dated event

- Kobe: annual lists; N02; Port Liner Sannomiya platform widening completes at the end of FY2029 (Kobe City page, updated 2026-06-05; some news says FY2027), and no station moves.
- Osaka: Yumeshima row only; no other 2027 opening found.
- Sapporo: streetcar extension judged "extremely difficult", subway Kiyota extension undecided; no date.
- Kyoto, Yokohama, Tokyo: no 2027 opening found (Tokyo's Yurakucho and Oedo extensions are mid-2030s).
- Matsuyama: JR Matsuyama-ekimae stop relocation FY2028; no date in window.
- Toyama: all Chitetsu lines kept, with public support from FY2027 (no line change).
- Utsunomiya: LRT west extension, works from 2027-11, opens 2036-03.
- Kumamoto: tram 東町線 FY2031; the JR Hōhi new station is outside the city.
- Kitakyushu: Nishi-Kurosaki closure (2026-07-31) is handled; nothing else.
- Fukui, Nagasaki, Hakodate, Kagoshima, Kōchi: nothing dated (Kagoshima's tram extension stalled).
- Daegu: monthly edition (rows end 2025-08-31); Line 4 targets 2030.
- Incheon: Line 7 Cheongna slipped to ≈2030; Geomdan extension (opened 2025-06-28) is already on the map.
- Goyang, Bucheon, Namyangju, Anyang, Yongin, Suwon, Ansan, Uijeongbu: SEMAS row only. Shinbundang Gwanggyo–Homaesil is 2029, Indeokwon–Dongtan 2028–29, the Sinansan Line 2028–29 and Line 7 to Tapseok ≈2029 (news).
- Daejeon: SEMAS row; Line 2, a tram under construction, is not drawn: re-read when it opens (no opening date read).
- Gwangju: SEMAS row; Line 2, under construction (phase 1 reported for 2028-12), is not drawn: re-read when it opens. OSM's 광주광역시 relation was gone after the merger (2026-10-04): if one returns, compare it with the five 구 union.
- Gimhae: SEMAS row; the LRT is Busan's line too, so a change to it moves both maps.
- Seoul and Busan registers: MOIS has published the LOCALDATA categories as daily data.go.kr APIs since 2025-11-27 (e.g. 15154916); no retirement date for the current routes was found.
- Hong Kong: FEHD daily. CSDI retired its DQS on 2026-06-30, but the pipeline uses `portal.csdi.gov.hk/csdi-webpage/file-api`, not DQS. Tung Chung extension 2029.
- Taoyuan (Airport MRT): A23 Zhongli ≈2029.
- Tbilisi: Geostat register live; the Line 1 extension (one station each way) is at market survey, no date.

### What a project doc states wrongly

1. **Osaka**: `docs/excluded_categories.md` says every line with a station in the city is drawn, but the map omits Yumeshima (opened 2025-01-19, regular service), because Osaka reads N02-24 (evidence in the first table row).
2. **Seoul's Wirye note** (`PLAN.md` lines 720-727) counts only stops "inside Seoul", but the line's Bokjeong and Namwirye ends are in Seongnam, a built city. The re-check should cover Seongnam too (Seoul mediahub; redaily, 2026-10-02).
3. Checked and NOT wrong: Kumamoto's "2026 earthquake" (令和8年熊本地震) is the city's own name for it. `pipeline/countries/japan.py`'s N02-25 publication date (2026-04-07) agrees with MLIT's "2026年4月".

## The screen itself: far-future items (owner, 2026-10-04)

Not about any built city: the global screen that feeds `docs/city_master_list.md`.
The rail-city listing closed on 2026-10-04; these rows say when to reopen it.

| When | Scope | What | Who |
|---|---|---|---|
| ≈2027-10 (one year on; earlier only on the owner's word) | Every country | **A global re-probe after a prolonged gap** (owner, 2026-10-04): re-run the coverage sweep's universe (Wikipedia's metro and tram and light-rail lists, plus openings since 2026-10-03) against the master list for new entries and openings; re-check each Band R row's blocker (a geo-block, a sign-in, a request-only register, a portal that refused this machine); and re-ask each held or left-out country whether the owner lifts the hold (Russia, Ukraine, Belarus, Iran, Israel, North Korea, Myanmar; China's ruling on its own terms). Start from `docs/coverage_sweep/README.md` (the universe, its reports and `scripts/coverage_sweep/recount.py`) | staging; the owner for any hold |
| Whenever the owner opens a commuter-rail overhaul | Commuter-only cities outside Japan | Never listed: a fresh listing of several hundred cities, the commuter-rail tier on the master list as its seed | staging |
