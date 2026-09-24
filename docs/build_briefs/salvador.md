# Salvador — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py salvador`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Salvador's.

---

## The one-line summary

**The highest share of classifiable storefronts in Brazil (42.8%) and the flattest neighbourhood skew — on a metro whose OSM relations carry no colour at all.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED with `scripts/screen_cnefe.py`

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/29_BA/2927408_SALVADOR.zip` — **52,084,744 bytes**, UTF-8, `;` |
| Establishment rows (`COD_ESPECIE = 6`) | **122,120** |
| **Mapped to the three buckets** | **52,258 (42.8%)** — Retail **25,890** · Food service **17,186** · Personal services **9,182** |
| Recorded **vacant** by the enumerator | 5,999 (4.9%) — excluded |
| **Unclassifiable** (catch-all + unmatched) | 26,371 (21.6%) |
| … by locality | **15% in Fazenda Grande do Retiro → 29% in Brotas**, median 19% — the narrowest spread of the nine |
| Coordinate level 1 (the census's own point) | **97.3%** of mapped rows |
| One establishment per row | 97.0% of mapped rows |

**The unclassifiable rows are dropped, not assigned** — and where their share
rises, the map under-draws. The page must say so, as São Paulo's does.

---

## 🔒 Privacy — the decided rule applies unchanged

At an address that also holds a dwelling, the tooltip shows the **category,
never the description text**. Here that reaches **29,134 (55.8%)** of mapped rows; a
first name at a dwelling address is **756 (1.4%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**Metrô de Salvador, L1 and L2** — 4 relations, refs `1`, `2`, all named, **0 of 4 coloured**. The invariant requires every drawn line to carry its real name and a legend entry; **colours must come from the operator** (CCR Metrô Bahia), stated as sourced, never invented.

⚠️ **Agency layers have NOT been searched.** `osm-rail` puts them first, and
Rio's metro and VLT layers turned up only when its city's ArcGIS org was
enumerated. **Enumerate Salvador's own portals before building from OSM.**

## Scope

L2 runs out past the airport toward Lauro de Freitas; measure how many stations fall outside município 2927408 before choosing commune scope.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ Line colours — from the operator
- ⚠️ Stations outside the município (L2's airport end)

```brief-checks
[
  {
    "id": "salvador-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Salvador is keyless and live - business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/29_BA/2927408_SALVADOR.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "salvador-cnefe-not-re-released",
    "claim": "Every figure here was measured on the May-2024 release. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/29_BA/",
    "present": [
      "2927408_SALVADOR.zip",
      "2024-05-2"
    ]
  },
  {
    "id": "salvador-osm-rail",
    "claim": "OSM carries Salvador's rail refs as counted 2026-09-23 - the geometry source until agency layers are found",
    "kind": "osm_route_refs",
    "bbox": [
      -13.02,
      -38.54,
      -12.78,
      -38.3
    ],
    "routes": [
      "subway"
    ],
    "require_refs": {
      "subway": [
        "1",
        "2"
      ]
    }
  },
  {
    "id": "salvador-projected-crs",
    "claim": "Salvador projects to its own UTM zone, never a neighbour's",
    "kind": "utm_zone_from_longitude",
    "lon": -38.5,
    "north": false,
    "expect": "EPSG:32724"
  }
]
```
