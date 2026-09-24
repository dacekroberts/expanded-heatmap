# Taoyuan — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py taoyuan`
before writing any code. **Read `taipei.md` first** — the national argument
is there once and holds here unchanged.

---

## The one-line summary

**49,282 storefronts joined at 94.0%, on a metro built to reach an airport —
and the one Taiwanese city whose rail agency hides a file behind a bot
challenge.**

## Business leg — the national tax register

**49,282** storefronts — Retail **27,635** · Food **15,324** · Personal
**6,323** (online shopping excluded). **No row still carries the pre-2014
county name `桃園縣`** — checked, empty.

## ✅ Coordinates — the join, 94.0%

| | |
|---|---|
| **File** | `TGOS_A68000_11508.CSV` — **August 2026**, **94,461,884 bytes**, `opendata.tycg.gov.tw`, monthly (56 editions listed) |
| Keys | 516,049 |
| Coordinates | TWD97 TM2 |
| **Joined** | **94.0%** — retail 92.6 · food 95.3 · personal 96.9 |

Misses: rural addresses in villages still written `村`, sub-alleys (`衖`), and
building letters (`Ａ棟`). A second measurement read 94.9% with a stricter
street pattern; **94.0% is the conservative figure**, from the pattern that
reproduces Taipei's control.

## 🚇 Rail

**Taoyuan Metro** (the airport MRT) — the operator's own network, route and
station datasets as XML on data.gov.tw (128388, 128390, 128394), and the
national `捷運車站` layer as the cross-check. 🚨 **The railway bureau's own
airport-MRT station-coordinate file sits behind an Incapsula bot challenge —
NOT worked around**; the national layer covers those stations.

## Scope

⚠️ **The airport MRT runs from Taipei Main Station through New Taipei to
Taoyuan** — most of its length is outside the city. Taoyuan's page draws the
in-city segment; whether it joins **Taipei (Regional)** instead is a scope
question worth one sentence of owner time.

## Still unknown

- ⚠️ The Taoyuan Metro XML's schema — not yet read.
- ⚠️ Scope against Taipei (Regional).
- ⚠️ Line colours.

```brief-checks
[
  {
    "id": "taoyuan-doorplates-live",
    "claim": "Taoyuan's August-2026 door-plate file is keyless and live - the join target, 94.0%",
    "kind": "http_ok",
    "url": "https://opendata.tycg.gov.tw/api/dataset/ec47dbd5-9ed8-4c8d-8ce1-ccb63b1b72e6/resource/d00ecba4-dec2-4a62-bfc7-989a8359cebe/download",
    "min_bytes": 1000000
  },
  {
    "id": "taoyuan-metro-network-live",
    "claim": "Taoyuan Metro publishes its own network dataset keyless - a rail source instead of TDX",
    "kind": "http_ok",
    "url": "https://opendata.tycg.gov.tw/api/dataset/434a3d9f-ebc1-474b-b8b7-da53eb340b48/resource/35cd3ed3-42a4-401d-90bd-7f5b82588169/download"
  },
  {
    "id": "taoyuan-projected-crs",
    "claim": "Taoyuan projects to UTM 51N",
    "kind": "utm_zone_from_longitude",
    "lon": 121.3,
    "expect": "EPSG:32651"
  }
]
```
