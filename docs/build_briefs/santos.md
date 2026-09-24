# Santos — build brief

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

⚠️ **Agency layers have NOT been searched.** `osm-rail` puts them first, and
Rio's metro and VLT layers turned up only when its city's ArcGIS org was
enumerated. **Enumerate Santos's own portals before building from OSM.**

## Scope

L1 runs west into **São Vicente** (município 3551009) — a regional question, and at 6,021 storefronts the city alone may be too thin to earn a page.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ Scope — São Vicente
- ⚠️ Whether ~6,000 storefronts earn a page (Rennes' question)

```brief-checks
[
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
      "2024-05-2"
    ]
  },
  {
    "id": "santos-osm-rail",
    "claim": "OSM carries Santos's rail refs as counted 2026-09-23 - the geometry source until agency layers are found",
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
