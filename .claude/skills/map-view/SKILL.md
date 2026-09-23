---
name: map-view
description: Make sure a city map opens at the right zoom, and verify it the way that actually catches the failure. Use when a map looks zoomed out (or in) on load, after any change to the fit logic in pipeline/map_common.py, when publishing a city, and when checking the live site after a reboot. Covers the recurring fit race, the self-correcting guard that answers it, and scripts/check_map_view.js.
---

# A map that opens at the wrong zoom

Distilled from three incidents, each fixed where it broke - which is exactly
why there was a third.

## The failure, three times

| When | City | Seen | Baked | What fixed it |
|---|---|---|---|---|
| 2026-09-21 | **Edmonton** | zoom **8.25**, whole region in one cluster | 11.5 | an `else` branch restoring the baked view at full width |
| 2026-09-23 | **Paris** | zoom **9**, labels flung to the edges; also a **blank** 0px map | 12.5 | `FITTED_AT`, and refusing a zero width |
| 2026-09-23 | **Lille** | zoom **8.25** | 11.75 | nothing targeted - it would not reproduce, which is what led to the guard |

**Every time: intermittent, not specific to the city, and a reload fixed it.**
Calgary rendered correctly beside the broken Edmonton. That signature is a
RACE in `PHONE_FIT_SCRIPT`: a fit pass runs while the embedded iframe is still
laying out, fits the network into whatever size the frame has at that moment,
and nothing afterwards undoes it.

**A clue worth keeping, not yet a finding.** Edmonton and Lille both broke to
exactly **8.25** from different baked zooms, and Paris - a network about half
their size - one step tighter at 9. A browser gives an iframe a **default size
of 300x150** before its parent sizes it, and fitting a ~20 km network into
300x150 lands near zoom 8. It fits all three; nobody has proved it.

## What answers it: the guard (2026-09-23)

Chasing triggers had been tried twice and a third appeared. So the guard
checks the **outcome** instead: until the reader first touches the map, it
compares the live zoom with what the view should be for the frame's current
width, and re-fits when they differ.

- **"Should be" is exactly what `apply()` produces**: the baked view (`HOME`)
  at full width, `fitBounds(BOUNDS, padding)` when narrower. It is computed with
  `getBoundsZoom`, so a correct view is never touched and a normal load is
  pixel-identical.
- **It runs** every 500 ms for the first 20 s, and on `visibilitychange`,
  `pageshow`, resize and when the map scrolls into view - so a page opened in a
  background tab, or an embed below the fold, is covered too.
- **It stops for good at the first pointer, wheel, touch or key event** inside
  the map. A guard that restored the view under a reader's hand would be a new
  bug. Never weaken this.
- **`PAD` is shared by `apply()` and the guard.** If the two paddings drifted
  apart, the guard would "correct" a right view on every tick.
- It exposes `window.__HEATMAP_VIEW` - the inputs (home view, bounds, padding,
  map width) and its own `corrections` count - for the check below.

Proven on a served map before it shipped: a clean load was left alone; a
programmatic jump to 8.25 (a simulated race) was corrected within 1.2 s; a
simulated reader click followed by a zoom to 9 stayed at 9; and at 375 px
Edmonton held its bounds fit (11.75) rather than wrongly restoring the baked
11.5.

**Do not answer the next variant with one more timed pass.** The fit already
runs at 0 ms, rAF, 120, 400 and 1200 ms, and each extra pass was added after a
variant slipped past the previous set. If the guard ever fails, fix the guard.

## Verifying a map's view: `scripts/check_map_view.js`

Read it, then run its contents with the browser `javascript_tool`. It finds the
map itself, standalone or two frames deep inside the live app, and recomputes
the expected zoom from the guard's INPUTS rather than trusting the guard's own
verdict.

**Every rule here is a way this has already been got wrong:**

1. **Read the map object, never judge the picture.** Edmonton's broken view
   was first read as "mid-load", then as "the bounds are correct" - both wrong,
   both would have shipped it. `getZoom()` after the page settles is the
   number that decides.
2. **Load fresh at each size.** Resizing a loaded page measures a stale layout.
3. **Do not touch the map before measuring** - no click, no wheel, no key. A
   touched map shows the reader's view; the check reports it UNMEASURED.
4. **Run it more than once.** It is a race: one clean load proves little.
   `corrections > 0` on any load means the race FIRED and the guard repaired it
   - record that, it is the only measure there is of how often it happens.
5. **Check the live app, not only the local file.** The race lives in the
   embed; every incident above was seen on the deployed site. A hidden browser
   pane (`document.hidden: true`) pauses rendering and may not exercise the
   same timing - note it when reporting a clean result.
6. **Measure at the embedded width AND at phone width.** The expected zoom
   differs between them, and only the phone width exercises the bounds fit.

## Reproduce an explanation before recording it

On 2026-09-23 Lille's 8.25 was first put down to a mouse wheel landing on the
map while the page scrolled, and the owner was told so. It was never
reproduced. Repeating the exact action - a fresh load, ten wheel ticks at the
same point - left the zoom untouched at 11.75, and the explanation died. The
record already held the answer: Edmonton's identical 8.25, and "a reload fixed
it". **Search the record for the number before inventing a cause for it, and
re-run the action you are blaming before you blame it.**

## Related, and not this skill

Wheel zoom and cluster-click zoom feel laggy compared with the +/- buttons.
That is a PERFORMANCE question about how many fractional zoom levels a wheel
gesture walks through (`zoomSnap` is 0.25), and it is separate from whether the
map opens at the right view. Do not tune the guard to address it.
