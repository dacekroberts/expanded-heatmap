# Aarhus — build brief

**Step 0 measured 2026-09-27 (the Denmark screen) and 2026-09-29 (the
light-rail test; this brief).** Run `python scripts/brief_check.py aarhus`
before writing code.

---

## The one-line summary

**Copenhagen's CVR chain on kommune 751, placed through OSM's DAR address
points, with ONE real scope call: which of the Letbane's 39 stations count.**
The call also decides the ring size. The business leg is measured and every
licence is read. The rail is OSM's, as Copenhagen's is.

| | Copenhagen (built) | **Aarhus** |
|---|---|---|
| Kommune | 101 + 147 | **751** (Aarhus Kommune, 471.2 km² in OSM) |
| Rail | Metro + S-tog, from OSM | **Letbanen L1 + L2, from OSM** (`route=light_rail`, operator Keolis, network Midttrafik) |
| Storefronts (screen) | 14,978 | **5,283**: retail 3,122 · food 1,220 · personal services 941 |
| Placement | DAR via Datafordeler (98.3%) | **OSM's DAR address points, 97.0%** (5,125), keyless (owner, 2026-09-27) |
| Personally owned (name suppressed) | 39% | **43.8%** |
| Projected CRS | EPSG:25833 | **EPSG:25832** (UTM 32N, 10.2° E), which is also DAR's national CRS |
| Rings | standard | **standard at 32 or 39 stations; halved at 20** (below) |

**Region: `"Europe"`. Band A** (master list, 2026-09-29).

---

## ✅ THE SCOPE — 20 stations (owner, confirmed 2026-09-29)

Measured 2026-09-29 from OSM's six Letbane route relations (7463675,
8603279, 9907095, 9907096, 14973317, 14973318) against Aarhus Kommune's OSM
boundary (relation 1784663). **41 stop names inside, 39 stations**: two
names are spelling variants of one stop, `G. Clausens Vej` / `Gunnar Clausens
Vej` and `Lisbjerg-Terp` / `Lisbjerg - Terp`, and need `STATION_NAME_ALIASES`.

The 39 are three pieces of track:

| Piece | Stations in the kommune | Lines | Track |
|---|---|---|---|
| **The new city tramway**, Aarhus H – Nørreport – Universitetet – Skejby – Lisbjerg – Lystrup | **20** | L2 (L1 shares Aarhus H, Dokk1, Skolebakken, Lystrup) | purpose-built, 2017 |
| **Odderbanen**, Kongsvang – Viby J – Tranbjerg – Mårslet – Beder – Malling | **12** | L2 through-running | converted single-track railway |
| **Grenaabanen**, Østbanetorvet – Risskov – Skødstrup – Løgten | **7** | L1 only | converted railway |

**The light-rail test makes frequency a gate on converted railway** (15 min
or better by day, at the median stop's worst daytime hour; owner,
2026-09-29). **Read 2026-09-29 from Midttrafik's own timetables**, the
operator's published PDFs, weekdays:
- **L2**: `l2_k26_20261009-20270403_normal-ua.pdf`, the normal plan valid
  from 9 October 2026;
- **L1**: `l1_k26_20260925-20270320_helaar-ua.pdf`, the year plan valid from
  25 September 2026;

both linked from `midttrafik.dk/rejsemuligheder/?search=L2` and `?search=L1`.

| Piece | What the timetable shows | Test |
|---|---|---|
| New city tramway | Aarhus H northbound every **7–8 min** (6.01, 6.08, 6.16, 6.23…) | **passes** |
| Odderbanen | Odder trains every **30 min** (x.04, x.34). The extra trips that start at Mårslet (`S7.07`, `S7.37`) **run through without stopping** (`|`) at Mølleparken, Nørrevænget, Kongsvang and the stops between, so those stops get **2 an hour through the morning**; Malling gets 2 an hour all day | **fails** at the section's median stop |
| Grenaabanen (L1) | every **30 min** (Aarhus H x.18, x.48); peak extras run only to Skødstrup and skip Løgten | **fails** |

**By the owner's test, the scope is the 20 stations on the new tramway**,
with the halved rings its 499 m median gap takes. That is the lean the
master row carried before this read. **Confirmed by the owner,
2026-09-29.**

| Scope | Median gap | Rings (spacing rule) | Within the outer ring |
|---|---|---|---|
| **20**, new tramway (the test's answer) | **499 m** | **halved: 0.05 / 0.1 / 0.2 / 0.3 mi** | **25.4%** at 0.3 mi |
| 32, tramway + Odderbanen | 634 m | standard 0.1 / 0.2 / 0.3 / 0.6 mi | 49.1% (2,516) |
| 39, all | 669 m | standard | 55.4% (2,837) |

*(Shares over the screen's 5,125 placed points; UTM 32N; the 20-station
scope also shown at 0.6 mi for comparison: 40.4%.)*

### Where the frequency comes from — Midttrafik, not Rejseplanen

The tram audit's first figures (2026-09-29) were read from Rejseplanen's
national GTFS (`rejseplanen.info/labs/GTFS.zip`), which **Copenhagen's build
declined to download** (owner, 2026-09-24). Rejseplanen's Labs guidelines ask
that the data not be changed and describe access as by request with the
guidelines accepted, and this project never made that request. **The owner's
call (2026-09-29): if the guidelines do not permit our use, drop the item or
find another source.** Another source was found: the frequency above rests
on **Midttrafik's own published timetables** and nothing else. The audit's
cached copy of Rejseplanen's feed was deleted from the staging scratchpad.
**The build never fetches Rejseplanen.**

---

## ✅ Rail — OSM, as Copenhagen's

**Rail from OSM, not Rejseplanen**: Copenhagen's precedent and ground (above,
and `docs/data_sources/denmark.md`). The six relations carry `ref` L1 / L2,
`route=light_rail`, `operator=Keolis`, `network=Midttrafik`. **Whitelist on
ref + route + operator**, Copenhagen's rule, never `network` alone.

- **Stations**: the kept relations' `stop` members inside the kommune,
  collapsed by name, plus the two aliases above. Stop spellings differ
  between the two directions' platform nodes, which is where the variants come
  from.
- **Colours: all six relations carry `#30556E`.** One colour for both lines
  (Oslo's and Bergen's shape). L1 keeps it at 39 stations; L2 takes a colour
  that clears `pipeline/linecolour.py`. At 20 or 32 stations, L2 is the main
  line drawn and keeps `#30556E`, while L1's in-scope track (shared with L2)
  is drawn only if kept at all. A build-time detail.
- **Names**: OSM names them "Light rail L1" / "Light rail L2"; riders call it
  *Letbanen*. `LINE_NAMES = {"L1": "Letbane L1", "L2": "Letbane L2"}`, with
  the mode word, as Copenhagen's "S-tog A". The page says light rail.
- **Boundary**: OSM's kommune boundaries, as Copenhagen's `kommuner.py`
  reads them (ref `751`; OSM's area 471.2 km²).
- **Stations outside**: Odder's three (Assedrup, Rude Havvej, Odder) are in
  Odder Kommune, and Grenaabanen's eight beyond Løgten are in Syddjurs and
  Norddjurs. Each is named in `excluded_stations.csv`, the Los Angeles rule.

---

## ✅ Business leg — Copenhagen's CVR chain, run on Aarhus by the screen

`data/_staging_scratch_2026-09-27/second_cities/denmark/biz_out.txt`, on the
**cached national CVR generation 505** (`data/denmark/raw/cvr/`, 2.8 GB):

| Stage | Aarhus |
|---|---|
| P-units with a current `beliggenhedsadresse` in the kommune | 60,113 |
| divisions 47 / 56 / 96 | 5,884 |
| after Copenhagen's structural exclusions | 5,448 |
| **`969900` excluded** (165 rows, 3.0%; personally owned 78% against 45% overall) | **5,283** |
| retail / food / personal services | **3,122 / 1,220 / 941** |
| personally owned: Enkeltmandsvirksomhed, PMV, I/S (Copenhagen's rule) | **43.8%**, name shown on 56.2% |

**The catch-all verdict carries over on Aarhus's own numbers**, as `96.990`
did from Oslo to Bergen.

### ⚠️ Placement — join on the HUSNUMMER id, not the adgangspunkt id

The chain: CVR `Adressering.Adresse` → DAR Adresse (cached nationally, 97.5%
found) → **Husnummer id** → OSM's address point whose `osak:identifier`
equals it (`osak_aarhus.tsv`, 113,739 points, keyless, ODbL).

| Joined on | Placed |
|---|---|
| **Husnummer id** | **5,125 of 5,283 (97.0%)** |
| adgangspunkt id | 4,230 (80.1%) |

**`osak:identifier` is the DAR Husnummer id** (DECISIONS 2026-09-27). The
adgangspunkt id coincides with it on most rows, so the wrong key still
places four in five storefronts. That is a plausible-looking 80%. The control
(central Copenhagen, where both sources exist) put OSM's points at a median
**0.03 m** from DAR's own.

**Why OSM and not Datafordeler's `Adressepunkt_0751`**: the owner's call,
2026-09-27: *"OSM unless we need the data account, then let me know."* 97.0%
does not need it. Copenhagen's per-kommune `Adressepunkt` files came through
the owner's key; **no key is needed for Aarhus**, because the national CVR
and DAR files are already cached.

⚠️ **The CVR and DAR caches are NATIONAL and SHARED with Copenhagen.** A
refresh needs the owner's key and changes Copenhagen's inputs. **Build on
generation 505 (CVR) and 761 (DAR)**, with the date on the page (the currency
rule's clock is five years). **Heavy job**: the chain reads about 5 GB of
national files. Announce it machine-wide (`docs/session_roles.md`).

⚠️ **OSM's address points are a support source** and need their own row in
`docs/data_sources/denmark.md` (CLAUDE.md `[#support-sources]`): ODbL 1.0,
used for pin coordinates. The basemap's OSM credit covers attribution, as for
the rail.

---

## ✅ Licences — all read

| Source | Licence | Notice |
|---|---|---|
| CVR (Datafordeler) | CC BY 4.0 | 30 (Copenhagen's) |
| DAR Adresse / Husnummer (Datafordeler), credit Klimadatastyrelsen | CC BY 4.0 | 31 |
| OpenStreetMap rail, boundary and address points | ODbL 1.0 | OpenStreetMap's notice 1 and the rail-geometry notice |

---

## Build-time calls

1. **Scope: 20 stations**, the answer the owner's test gives on Midttrafik's
   own timetables (above), with the halved rings. **Confirmed by the owner, 2026-09-29.**
   Record the timetable read on the page as the reason the converted
   railways are not drawn.
2. **Line colours** through `linecolour.py` (both lines are `#30556E` in OSM).
3. **The two spelling aliases**: explicit, never a rule.

**Flag for the cleanup role (held macro-map work)**: Aarhus takes the
light-rail network colour, as Bergen does; Copenhagen is metro.

## Still unknown — the honest list

- ~~L2's frequency at each Odder-section stop~~ ✅ read 2026-09-29 from
  Midttrafik's normal plan: every 30 min at the intermediate stops through
  the morning, Malling all day.
- Whether OSM's relations match Midttrafik's current service pattern (the
  L2 short branch to Lisbjergskolen appears in OSM as its own relation pair).

```brief-checks
[
  {
    "id": "letbane-osm-relations",
    "claim": "OSM carries the Letbane as six route=light_rail relations in two refs, L1 and L2 (operator Keolis, network Midttrafik) - the rail source, as Copenhagen's; Rejseplanen's GTFS is not downloaded for the build",
    "kind": "osm_route_refs",
    "bbox": [56.0, 9.9, 56.5, 10.95],
    "routes": ["light_rail"],
    "expect_relations": {"light_rail": 6},
    "expect_refs": {"light_rail": 2},
    "require_refs": {"light_rail": ["L1", "L2"]}
  },
  {
    "id": "aarhus-is-utm-32",
    "claim": "Aarhus (10.2 E) is in UTM zone 32: EPSG:25832 (ETRS89), which is also DAR's national CRS - Copenhagen's 25833 must not be copied. The check derives the WGS84 twin, 32632",
    "kind": "utm_zone_from_longitude",
    "lon": 10.2,
    "expect": "EPSG:32632"
  }
]
```
