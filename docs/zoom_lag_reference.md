# Zoom lag reference - cluster animation off

The reference figures for how quickly a map settles after a zoom, with cluster
animation **off** (every city's setting since 2026-09-23, confirmed by the owner on
2026-09-27). Compare a future measurement against the "Off" column: a map that
settles markedly slower than this, under the same conditions, has regressed.

**Measured 2026-09-27** on the owner's Windows machine with
`scripts/profile_zoom.mjs`: headless Edge, trusted input, a 1280x900 window, and the
median of three fresh loads per case. "Settle" is the time from the first input to
the last map event handled. The maps are the committed ones after the JSON.parse
rework, and the "On" column is the same map re-rendered with
`animate_clusters=True`. The decision and its reasoning are in DECISIONS.md,
"Cluster animation stays off".

## Paris (84,125 dots, 8.7 MB) - the reference map

| Scenario | Off (reference) | On | Animation adds |
|---|---|---|---|
| `button+1` - one +/- click | 371 ms | 655 ms | +284 ms |
| `wheel1` - one wheel notch | 443 ms | 715 ms | +272 ms |
| `cluster` - click a cluster | 436 ms | 987 ms | +551 ms |
| `wheel3fast` - three quick notches | 953 ms | 1,642 ms | +689 ms |
| `wheel45` - notches 45 ms apart | 889 ms | 2,151 ms | +1,262 ms |
| `wheel5` - five notches | 1,432 ms | 1,938 ms | +506 ms |
| `wheel5out` - five notches out | 1,046 ms | 1,048 ms | +2 ms |
| `button+3` - three +/- clicks | 1,464 ms | 2,181 ms | +717 ms |
| `wheelslow` - a slow roll | 2,423 ms | 3,638 ms | +1,215 ms |
| `trackpad` - a trackpad gesture | 2,677 ms | 2,903 ms | +226 ms |

Paris's `button+1` was 366 ms off and 647 ms on in the 2026-09-23 run, so the figures
held across the JSON.parse rework.

`wheel45` and `trackpad` reached different zoom levels with and without animation,
so their deltas mix speed with distance travelled. Every other pair reached the same
levels.

## Seoul (224,381 dots, 24.2 MB) - the heaviest map, partial

| Scenario | Off (reference) | On | Animation adds |
|---|---|---|---|
| `button+1` | 381 ms | 636 ms | +255 ms |
| `wheel1` | 448 ms | 687 ms | +239 ms |
| `wheel3fast` | 865 ms | 1,158 ms | +293 ms |
| `button+3` | 1,246 ms | 1,734 ms | +488 ms |
| `cluster` | 440 ms | not measured | |
| `trackpad` | 3,296 ms | not measured | |
| `wheel45` | 1,435 ms | not measured | |
| `wheel5` | 1,441 ms | not measured | |
| `wheel5out` | 1,218 ms | not measured | |
| `wheelslow` | 1,987 ms | not measured | |

With animation off, Seoul's single-step zooms settle as fast as Paris's, despite 2.7
times the dots.

## Reproducing it

Serve the maps, then run the profiler against them. Timings depend on the machine,
so re-measure the reference on the same machine before comparing.

```bash
python -m http.server 8831 --directory outputs
```

```bash
node scripts/profile_zoom.mjs http://localhost:8831 paris,seoul 3
```

The profiler prints one JSON line per run on stdout and a median table per city and
scenario on stderr.
