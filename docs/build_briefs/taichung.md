# Taichung — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py taichung`
before writing any code. **Read `taipei.md` first** — the national argument
(the tax register, the join method and its control, the name rule, the OGDL
v1 licence and its load-bearing attribution, why not TDX) is there once and
holds here unchanged.

---

## The one-line summary

**73,227 storefronts joined at 92.7% to a door-plate file that carries WGS84
as well as TWD97 — on a one-line metro.**

## Business leg — the national tax register

**73,227** storefronts — Retail **39,862** · Food **23,749** · Personal
**9,616** (online shopping excluded). **No row still carries the pre-2010
county name `臺中縣`** — checked, empty.

## ✅ Coordinates — the join, 92.7%

| | |
|---|---|
| **File** | `臺中市115年8月GIS門牌號碼` — the city's **August 2026** release, **159,271,987 bytes**, linked from its data portal's index to the city's **Google Drive** (a normal large-file confirmation page, not a bot check) |
| Keys | 719,446 |
| Coordinates | **TWD97 AND WGS84** (`WGS84經度` / `WGS84緯度`) — the only one of the five with both |
| **Joined** | **92.7%** — food 92.9 · retail 91.9 · personal 95.1 |

⚠️ **Taichung's numbers CHAIN sub-numbers** (`２之３之２號`) — a form Taipei
never showed; `screen_taiwan_join.py` handles it. The street column is
`街、路段`. Misses include `一` written for `－` in a number (`４９６一５號`) and
several numbers in one address.

⚠️ **The hosting is a Google Drive link**, and the portal's index lists one
file per month: a build must read the index for the current month rather than
pin a file id.

## 🚇 Rail

**Taichung Metro Green Line** — the operator's own `臺中捷運綠線車站資訊`
(data.gov.tw 144164): station code, Chinese and English names, **lat/lon**,
address, updated 2026-03-18. **One line.** Line geometry is not in that
dataset — from OSM (ODbL, the settled Toulouse/Rennes precedent) or the
national layer, **decided at build**.

## Scope

The Green Line runs within the city (Beitun to Wuri); commune scope holds.

## Still unknown

- ⚠️ Line geometry and colour — the station table has neither.
- ⚠️ Whether a one-line metro earns a page (73,227 storefronts say the
  business side does).

```brief-checks
[
  {
    "id": "taichung-green-line-stations",
    "claim": "Taichung Metro publishes its Green Line stations keyless with coordinates - the rail source instead of TDX",
    "kind": "http_contains",
    "url": "https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=f9511cc5-4799-4df9-98b7-0b0f89fc2be9",
    "present": ["北屯總站", "Beitun Main Station", "G0"]
  },
  {
    "id": "taichung-doorplate-index-live",
    "claim": "Taichung's 2026 door-plate index lists a GIS door-plate file per month - read it for the current month, never pin one file id",
    "kind": "http_contains",
    "url": "https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=03d9c01c-4a7c-4bd8-ae88-12ed011391b3",
    "present": ["GIS門牌號碼", "drive.google.com"]
  },
  {
    "id": "taichung-projected-crs",
    "claim": "Taichung projects to UTM 51N",
    "kind": "utm_zone_from_longitude",
    "lon": 120.68,
    "expect": "EPSG:32651"
  }
]
```
