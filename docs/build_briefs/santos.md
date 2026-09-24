# Santos (Regional) — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py santos`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Santos's.

---

## The one-line summary

**The smallest of the nine — Rennes-sized — on a modern two-line light-rail network.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED with `scripts/screen_cnefe.py`

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/35_SP/3548500_SANTOS.zip` — **3,948,134 bytes**, UTF-8, `;` |
| Establishment rows (`COD_ESPECIE = 6`) | **18,641** |
| **Mapped to the three buckets** | **6,021 (32.3%)** — Retail **3,322** · Food service **1,769** · Personal services **930** |
| Recorded **vacant** by the enumerator | 1,782 (9.6%) — excluded |
| **Unclassifiable** (catch-all + unmatched) | 4,653 (25.0%) |
| … by locality | one locality (Santos) at 19% — no within-city spread to measure at this granularity |
| Coordinate level 1 (the census's own point) | **98.1%** of mapped rows |
| One establishment per row | 96.6% of mapped rows |

**The unclassifiable rows are dropped, not assigned** — and where their share
rises, the map under-draws. The page must say so, as São Paulo's does.

---

## 🔒 Privacy — the decided rule applies unchanged

At an address that also holds a dwelling, the tooltip shows the **category,
never the description text**. Here that reaches **1,423 (23.6%)** of mapped rows; a
first name at a dwelling address is **46 (0.8%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**VLT da Baixada Santista, L1 and L2** — `route=light_rail`, 4 relations, all coloured. The **Bonde Turístico** (heritage tram, no ref, no colour) is **excluded** as a tourist service.

**Agency-hosted layers FOUND 2026-09-23 — stops and line, OWNER UNCONFIRMED.**
EMTU's own open-data and GTFS pages now redirect to its home page, and São
Paulo's state CKANs timed out. The ArcGIS Online account `CPGSTM` (*CPG
Coordenadoria de Planejamento e Gestão*, in no organisation, created 2023)
hosts `EMTU_RMBS_Estações_Paradas_VLT_SIM_Em_Operação` (**16 stops**, `Nome`,
`Status` = *Em Operação*, `Empresa` = EMTU; EPSG:4674) and
`EMTU_RMBS_Tracado_VLT_SIM_Em_Operação` (one line, *SIM - VLT Baixada*,
Barreiros–Porto), plus *Em Implantação* pairs; `licenseInfo` blank. **The
"STM" suffix suggests the state's Secretaria dos Transportes Metropolitanos,
EMTU's parent — ASSERTED from the name alone.** 16 stops against OSM's L1 +
L2 suggests the layer may predate L2 — unverified. **Recommendation: OSM
geometry; the CPGSTM layers as a status cross-check only, never the licensed
source, until their owner is confirmed.**

## Scope

**MEASURED 2026-09-23** (OSM, by município): 25 stops — **17 in Santos (68%, one of them the excluded heritage tram's), 8 in São Vicente** (3551009), including Terminal Barreiros, the lines' western hub. **REGIONAL — decided by the owner 2026-09-23: Santos (Regional)** = Santos + São Vicente. Measured the same night: **São Vicente 5,670** storefronts — **11,691 with Santos's 6,021, nearly double**, which also answers Rennes' question in the page's favour. Coordinate level 1 99.3%; catch-all 20.3%, the lowest measured in Brazil.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown


```brief-checks
[
  {
    "id": "santos-vlt-stops-layer",
    "claim": "An ArcGIS layer labelled EMTU carries the VLT's operating stops with a status field - a cross-check only; its owner (account CPGSTM) is unconfirmed",
    "kind": "arcgis_layer",
    "url": "https://services3.arcgis.com/3qsRj8hNn2xpckE0/arcgis/rest/services/EMTU_RMBS_Esta%C3%A7%C3%B5es_Paradas_VLT_SIM_Em_Opera%C3%A7%C3%A3o/FeatureServer/0",
    "expect_rows": 16,
    "present": [
      "Nome",
      "Status"
    ]
  },
  {
    "id": "santos-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Santos is keyless and live - business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/3548500_SANTOS.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "santos-cnefe-not-re-released",
    "claim": "Every figure here was measured on the May-2024 release. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/",
    "present": [
      "3548500_SANTOS.zip",
      "3551009_SAO_VICENTE.zip",
      "2024-05-2"
    ]
  },
  {
    "id": "santos-osm-rail",
    "claim": "OSM carries Santos's rail refs as counted 2026-09-23 - the geometry source; agency layers searched 2026-09-23, see Rail",
    "kind": "osm_route_refs",
    "bbox": [
      -24.0,
      -46.42,
      -23.92,
      -46.28
    ],
    "routes": [
      "light_rail"
    ],
    "require_refs": {
      "light_rail": [
        "L1",
        "L2"
      ]
    }
  },
  {
    "id": "santos-projected-crs",
    "claim": "Santos projects to its own UTM zone, never a neighbour's",
    "kind": "utm_zone_from_longitude",
    "lon": -46.33,
    "north": false,
    "expect": "EPSG:32723"
  }
]
```
