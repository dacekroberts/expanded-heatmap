# Recife — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py recife`
before writing any code. **Read `sao-paulo.md` first** — the national facts
(why CNEFE and not CNPJ, the free-text taxonomy, the privacy rule, the
licence, what every Brazilian page must say) are argued there once and hold
here unchanged. This brief carries what is Recife's.

---

## The one-line summary

**A three-line metro, all coloured, on a register whose catch-all is the highest in Brazil — and a network that mostly runs outside the city.**

---

## Business leg — IBGE's CNEFE 2022, MEASURED with `scripts/screen_cnefe.py`

| | |
|---|---|
| **File** | `Arquivos_CNEFE/CSV/Municipio/26_PE/2611606_RECIFE.zip` — **17,729,524 bytes**, UTF-8, `;` |
| Establishment rows (`COD_ESPECIE = 6`) | **72,760** |
| **Mapped to the three buckets** | **25,212 (34.7%)** — Retail **14,968** · Food service **5,622** · Personal services **4,622** |
| Recorded **vacant** by the enumerator | 4,629 (6.4%) — excluded |
| **Unclassifiable** (catch-all + unmatched) | 21,225 (29.2%) |
| … by locality | 19% (São José) → 32% (Boa Viagem), median **29% — the highest median of the nine** |
| Coordinate level 1 (the census's own point) | **99.0%** of mapped rows |
| One establishment per row | 95.0% of mapped rows |

**The unclassifiable rows are dropped, not assigned** — and where their share
rises, the map under-draws. The page must say so, as São Paulo's does.

---

## 🔒 Privacy — the decided rule applies unchanged

At an address that also holds a dwelling, the tooltip shows the **category,
never the description text**. Here that reaches **10,309 (40.9%)** of mapped rows; a
first name at a dwelling address is **301 (1.2%)**.

---

## 🚇 Rail — OpenStreetMap, counted 2026-09-23 (one query, Curitiba as the negative control)

**Metrô do Recife**: `route=subway` Linha Centro 1 & 2 and Linha Sul (6 relations, refs `1`, `2`, `Sul`, all coloured); `route=light_rail` **VLT Curado–Cajueiro Seco** (2 relations) — ⚠️ a **diesel** line; confirm service pattern before drawing.

⚠️ **Agency layers have NOT been searched.** `osm-rail` puts them first, and
Rio's metro and VLT layers turned up only when its city's ArcGIS org was
enumerated. **Enumerate Recife's own portals before building from OSM.**

## Scope

Linha Centro runs to Camaragibe and Jaboatão dos Guararapes, Linha Sul to Cajueiro Seco in Jaboatão — **much of the network is outside município 2611606**. Almost certainly the **regional shape**; measure station share per município.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ Scope — Jaboatão dos Guararapes, Camaragibe
- ⚠️ The VLT's service pattern (diesel)
- ⚠️ Why the catch-all runs highest here (29.2%) — a regional vocabulary the rules lack?

```brief-checks
[
  {
    "id": "recife-cnefe-file-live",
    "claim": "The CNEFE 2022 file for Recife is keyless and live - business leg and coordinate leg in one",
    "kind": "http_ok",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/26_PE/2611606_RECIFE.zip",
    "min_bytes": 1000000,
    "content_type_contains": "zip"
  },
  {
    "id": "recife-cnefe-not-re-released",
    "claim": "Every figure here was measured on the May-2024 release. When this FAILS, IBGE has re-released it: re-run scripts/screen_cnefe.py",
    "kind": "http_contains",
    "url": "https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/26_PE/",
    "present": [
      "2611606_RECIFE.zip",
      "2024-05-2"
    ]
  },
  {
    "id": "recife-osm-rail",
    "claim": "OSM carries Recife's rail refs as counted 2026-09-23 - the geometry source until agency layers are found",
    "kind": "osm_route_refs",
    "bbox": [
      -8.16,
      -35.02,
      -7.93,
      -34.85
    ],
    "routes": [
      "subway",
      "light_rail"
    ],
    "require_refs": {
      "subway": [
        "1",
        "2",
        "Sul"
      ]
    }
  },
  {
    "id": "recife-projected-crs",
    "claim": "Recife projects to its own UTM zone, never a neighbour's",
    "kind": "utm_zone_from_longitude",
    "lon": -34.9,
    "north": false,
    "expect": "EPSG:32725"
  }
]
```
