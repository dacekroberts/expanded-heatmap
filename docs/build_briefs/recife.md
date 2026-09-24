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

**Metrô do Recife**: `route=subway` Linha Centro 1 & 2 and Linha Sul (6 relations, refs `1`, `2`, `Sul`, all coloured); `route=light_rail` **VLT Curado–Cajueiro Seco** and **VLT Cajueiro Seco–Cabo** (4 relations) — ⚠️ **diesel** lines; confirm service pattern before drawing.

**Agency layer FOUND 2026-09-23 — stations and lines in one small file.**
`dados.recife.pe.gov.br`, *Malha Viária de Trens do Grande Recife* (author
CBTU, maintainer EMPREL): `estacoes-de-trem-do-grande-recife.geojson`, 11,899 B
— **36 station points** (`name` only; OSM also counts 36) and **six line
strings whose `name` carries line, length and status** (*"Linha Sul (diesel)
- 17,6 km / Cajueiro Seco - Cabo / Operação em VLT"*). Declared licence
**ODbL** in CKAN and the data dictionary — **not read**. ⚠️ **It reads like a
planning map**: one segment is labelled *"Expansão - 4,7 km / Rodoviária -
Camaragibe"* while OSM shows Camaragibe in service, so its status text is not
evidence of today's service. **Recommendation: OSM for geometry and stations
(per-line relations, colours); the CBTU file as the cross-check.**

## Scope

**MEASURED 2026-09-23** (OSM route members, by município): **36 stations — only 19 in Recife (53%)**, Jaboatão dos Guararapes 12, Cabo de Santo Agostinho 4 (the diesel VLT's southern end), Camaragibe 1. **Regional recommended — the owner's call.** The neighbours' CNEFE files are not yet downloaded: Jaboatão 7,528,738 B, Cabo 2,470,937 B, Camaragibe 1,592,566 B.

## Region

Brazil's — the first Brazilian city adds it (see `sao-paulo.md`).

## Still unknown

- ⚠️ Scope — regional recommended, **owner's call**; the neighbours' storefronts are unmeasured
- ⚠️ The VLT's service pattern (diesel)
- ⚠️ Why the catch-all runs highest here (29.2%) — a regional vocabulary the rules lack?

```brief-checks
[
  {
    "id": "recife-agency-rail",
    "claim": "CBTU's station-and-line file on Recife's CKAN is keyless and live, with line status in the names - the cross-check for OSM, declared ODbL",
    "kind": "http_contains",
    "url": "https://dados.recife.pe.gov.br/dataset/9a4d7113-f4e0-448f-b62f-05cd2fab5c1d/resource/c029fbdd-8b62-4308-bf73-27de9a931554/download/estacoes-de-trem-do-grande-recife.geojson",
    "present": [
      "Operação em VLT",
      "Estação Cajueiro Seco",
      "Camaragibe"
    ]
  },
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
    "claim": "OSM carries Recife's rail refs as counted 2026-09-23 - the geometry source; agency layers searched 2026-09-23, see Rail",
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
