# Rio de Janeiro — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py
rio-de-janeiro` before writing any code. **Read `sao-paulo.md` first**: the
national facts — why CNEFE and not CNPJ, the taxonomy, the privacy rule, the
licence — are the same and are argued there. This brief carries what is Rio's.

---

## The one-line summary

**105,350 storefronts from the census, 95.1% on the enumerator's own point,
and a complete agency rail leg under CC BY 4.0 — with one table that codes
the same field two different ways.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED

**Rio's own register is the aggregate trap.** Its ArcGIS org holds **9,879
public items**, and the business-shaped ones lead to `Fazenda/ISSQN`, whose four
tables (`Estabelecimentos Abertos por Logradouros...`, 209,275 rows) are
**counts per street × activity group × year of concession** — no address, no
name, four coarse groups, and a flow of openings rather than the businesses
operating now.

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/33_RJ/3304557_RIO_DE_JANEIRO.zip` — **94,594,981 bytes**, last modified **2024-05-20** |
| Member | `3304557_RIO_DE_JANEIRO.csv`, 538,975,143 bytes, **UTF-8**, **`;`**, **3,276,028 addresses** |
| Establishment rows (`COD_ESPECIE = 6`) | **264,714** — 118,684 distinct descriptions |
| **Mapped to the three buckets** | **105,350** — Retail **50,423** · Food service **35,509** · Personal services **19,418** |
| Recorded **vacant** | **22,954 (8.7%)** — fourth of the nine Brazilian cities, behind Belo Horizonte 10.3%, Porto Alegre 9.9% and Santos 9.6% |
| Coordinate level 1 | **95.1%** of mapped rows — the lowest of the nine; the rest are the census's modified or estimated points (levels 2–4) and 0.2% at census-tract level |
| One establishment per row | **96.9%** |

`BAR` alone is **10,295 rows** — the single most common description.

### 🚨 The catch-all is 20.0%, and Barra da Tijuca loses 36%

| | Rows | Share |
|---|---|---|
| Unmatched | 45,094 | 17.0% |
| Generic catch-all | 7,915 | 3.0% |
| Rescued by the edit-distance pass | 2,345 | — |

**By locality: 15% in Santíssimo, 16% in Anchieta, 29% in Recreio dos
Bandeirantes, 36% in Barra da Tijuca.** Rio's spread is the widest of the
first two cities, and it points the same way: **the affluent west-zone
districts are under-drawn.** Barra is also where the mall problem lives —
`SHOPPING DOWNTOWN` at Av. das Américas 500 is **22 rows** for a centre far
larger.

---

## ✅ Coordinates — there is NO geocoding leg

As São Paulo. **Project to EPSG:32723 (UTM 23S)** — Rio's longitude (−43.2)
sits in the same zone, and its agency rail layers are already EPSG:31983,
SIRGAS 2000 / UTM 23S.

---

## 🔒 Privacy — the rule reaches 55% of pins here

The decided rule (category, never description text, at an address that also
holds a dwelling) applies to **58,342 mapped rows — 55.4%**, against São
Paulo's 37.3%. **2,229 (2.1%)** carry a first name at a dwelling address —
`SALAO DA VANESSA`, `BAR DO ZE`, `MERCEARIA DO CHICO`, `BAZAR DO LUIZINHO`.
**Rio's tooltips will mostly show categories.** That is the rule working, not
a defect — Milan runs at ~82% without a trade name.

---

## 🚇 Rail — the city's own layers, CC BY 4.0

`pgeo3.rio.rj.gov.br/arcgis/rest/services/Transporte_Trafego/Transporte_publico/MapServer`
— found by enumerating the org, **never searched for until 2026-09-23**; the
country screen had only OSM. `osm-rail`'s order puts agency layers first.

| Layer | Features | |
|---|---|---|
| **19** `Estações de Metrô` | **41** | EPSG:31983. Line membership as **integer flags**: `flg_linha1` 20 · `flg_linha2` 26 · `flg_linha4` 6 = **52 station-line pairs** (Lines 1 and 2 share track). `flg_ativa` = 1 on all 41 |
| **18** `Linhas de Metrô` | **3** | Linha 1, 2, 4. ⚠️ **`flg_ativa` is NULL on two of the three** — never filter lines on it; the stations' flags are the reliable field |
| **9** `Paradas de VLT` | **31** | `em_operação` = 1 on all |
| **10** `Linhas de VLT` | **4** | Linha 1-Azul · 2-Verde · 3-Amarela · 4-Laranja, all operating |

🚨 **The VLT stops table codes line membership TWO WAYS.** `linha_1`–`linha_3`
use **`1` / `2`** (1 = yes); **`linha_4` uses `Sim` / `Não`** — and one row
reads `1`. A build that tests `== "1"` everywhere **drops Line 4 entirely**
and raises nothing. Normalise all four to a boolean first.

**OSM cross-check agrees on the network:** subway refs **1, 2, 4**, all
coloured (Line 1 `#e77405`, Line 2 `#028F34`); VLT Carioca refs **1–4**, with
colours as **CSS names** (`blue`, `green`) — resolve through the CSS
named-colour table, as Guadalajara did. **Use OSM for colour, the agency for
geometry and membership.**

### Owner calls, not probes

- **Bonde de Santa Teresa** (OSM: tram, 2 relations) and the **Trem do
  Corcovado** (light_rail, `ESFECO`) — a heritage tram and a tourist rack
  railway. **Recommend excluding both**, as Santos' tourist tram is.
- **Teleférico** — the city publishes `Estações Teleférico`; whether any line
  operates is **unmeasured**. Toulouse draws its cable car, so an operating
  one would be in scope.
- **SuperVia** (commuter) and **BRT** (bus) are out by standing rule.

**Scope:** MetrôRio and the VLT lie inside the município — the commune scope
holds, as in São Paulo.

## Region

Shares São Paulo's: the first Brazilian city adds it.

## What the page must say

São Paulo's six items, plus **the rail credit CC BY 4.0 requires** — READ
2026-09-23, **PERMITTED WITH CONDITIONS**. No wording is prescribed; the
licence needs the creator, the licence link, a link to the data, and a
**statement that it was modified**:

> Metro and VLT stations and lines: Prefeitura da Cidade do Rio de Janeiro /
> Instituto Pereira Passos (IPP), via DATA.RIO, licensed under CC BY 4.0.
> Reprojected, filtered and redrawn by this project; station rings and density
> figures are this project's own analysis.

The *"sem alteração"* clause found on other Data.Rio items is **absent from
all four rail items**. Operator names and colours (MetrôRio, VLT Carioca) are
not licensed by it.

## Still unknown

- ✅ ~~**One raised clause**~~ — the SIURB Termo de Uso's damage-liability
  clause (§6 iv) was **ACCEPTED by the owner 2026-09-23**: fault-based, may
  bind only logged-in users, prohibits nothing the build does. Rio's rail
  comes from the agency layers. See `docs/data_sources.md`.
- ⚠️ **Teleférico** — operating or not.
- ⚠️ **Vacancy at 8.7%** — whether it is concentrated near stations is
  unmeasured.
- ⚠️ **The 0.2% at census-tract level** (`NV_GEO_COORD = 6`) sit at a tract
  centroid, not the premises — drop them or keep them, but decide.

```brief-checks
[
  {
    "id": "rio-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Rio (3304557) is keyless and live - 94,594,981 bytes, a zip. Business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/33_RJ/3304557_RIO_DE_JANEIRO.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "rio-cnefe-not-re-released",
    "claim": "Every figure here was measured on the file dated 2024-05-20. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/33_RJ/",
    "present": ["3304557_RIO_DE_JANEIRO.zip", "2024-05-20 19:53"]
  },
  {
    "id": "rio-metro-stations-41",
    "claim": "The city's own metro station layer holds 41 stations",
    "kind": "http_contains",
    "url": "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Transporte_Trafego/Transporte_publico/MapServer/19/query?where=1%3D1&returnCountOnly=true&f=json",
    "present": ["\"count\":41"]
  },
  {
    "id": "rio-vlt-lines-4",
    "claim": "The VLT line layer holds 4 lines, all in operation",
    "kind": "http_contains",
    "url": "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Transporte_Trafego/Transporte_publico/MapServer/10/query?where=1%3D1&returnCountOnly=true&f=json",
    "present": ["\"count\":4"]
  },
  {
    "id": "rio-vlt-line-4-coded-differently",
    "claim": "The VLT stops table codes linha_1-3 as 1/2 but linha_4 as Sim/Nao. A build testing == 1 everywhere silently drops Line 4. When this FAILS the coding changed: re-read before trusting the normaliser",
    "kind": "http_contains",
    "url": "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Transporte_Trafego/Transporte_publico/MapServer/9/query?where=1%3D1&outFields=linha_3%2Clinha_4&returnGeometry=false&f=json",
    "present": ["\"linha_4\":\"Sim\"", "\"linha_3\":\"2\""]
  },
  {
    "id": "rio-rail-declared-cc-by",
    "claim": "The metro station item declares CC BY 4.0 in its licenseInfo - the declared licence only; the full read is recorded separately",
    "kind": "http_contains",
    "url": "https://www.arcgis.com/sharing/rest/content/items/7a0b22723c5a458faaae79f046163504?f=json",
    "present": ["creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "rio-osm-colours-and-refs",
    "claim": "OSM carries MetroRio refs 1, 2, 4 and VLT Carioca refs 1-4 - the colour source, since the agency layers carry none",
    "kind": "osm_route_refs",
    "bbox": [-23.08, -43.80, -22.75, -43.10],
    "routes": ["subway", "tram"],
    "expect_refs": {"subway": 3},
    "require_refs": {"subway": ["1", "2", "4"], "tram": ["1", "2", "3", "4"]}
  },
  {
    "id": "rio-projected-crs",
    "claim": "Rio projects to UTM 23S, the same zone as Sao Paulo and as its agency layers' EPSG:31983",
    "kind": "utm_zone_from_longitude",
    "lon": -43.2,
    "north": false,
    "expect": "EPSG:32723"
  }
]
```
