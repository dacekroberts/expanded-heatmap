# DECISIONS drafts - Overpass 60 s backoff (`claude/trusting-hugle-d35474`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - Overpass callers wait 60 s after a 504, 429 or timeout

- **`pipeline/osm.py`'s `fetch()` backed off 5 s after its first failed
  round, against the owner's rule of 60 s after a 504 or 429.** The tram-kit
  session saw it on Tucson's `fetch_sources.py` the same day: both mirrors
  504 or timed out, "backing off 5s", then a retry. Decided: a round whose
  failures include a 504, a 429 or a timeout (an HTTP timeout, or a remark
  saying the query timed out) now waits `OVERLOAD_WAIT_S` = 60 s, escalating
  60, 120, ... per round. When the `deadline` cannot fit that wait plus a
  10 s request, `fetch()` gives up and says so; it does not retry early.
  Rounds whose failures are an empty 200, a remark or all-zero counts are not
  load, so they keep the old 5 s, 20 s backoff. Timeouts count as load
  because a read timeout came alongside the 504s each time both mirrors
  were struggling (Lille 2026-09-23, Tucson 2026-09-30). Rejected: a flat
  `max(60, 5 * n**2)`, which does not climb above 60 until the fourth round.
- **`fetch()` also remembers which host refused, for the rest of the
  process.** A later `fetch()` that reaches that host within the minute
  waits out the remainder. If the deadline is too short for the wait, it
  skips that host for the next one. Without this, a fetch script making
  several queries would send the second query to a host that 504'd seconds
  earlier on the first, whenever the other mirror had answered the first.
  Host order is unchanged. Rejected: putting a refusing host last, which
  would change which mirror answers. The mirrors disagree, so that changes
  what gets cached.
- **The same rule now applies to the three other places that retry Overpass
  themselves.** `scripts/brief_check.py`'s second-mirror confirmation in
  `osm_route_refs` could re-ask a host that 504'd moments earlier. It now
  keeps the same per-host minute. `scripts/screen_stop_spacing.py` retried
  the same mirror after 20 s on a 504 or 429 and after 8 s on any exception.
  It now waits 60 s after a 504, a 429 or a timeout. The address loop in
  `pipeline/aarhus/fetch_sources.py` slept 30 s and 60 s between rounds.
  It now sleeps 60 s and 120 s, the shape Odense's copy on `tram-build`
  already had. These callers were left alone because each tries every host
  once and never retries one: the Hong Kong, Seoul, Taichung, Taipei,
  Taoyuan, Mexico City and Bucharest fetch scripts. Every other Overpass
  caller goes through `osm.fetch()`.
- **`brief_check.py` reports a claim it could not check because Overpass was
  overloaded as RETRY, not FAIL** (the staging session asked for this when
  told of the change). Before this, every mirror 504ing printed FAIL under
  "a brief to correct", although it says nothing about the brief. Now, when
  every mirror refused with a 504, a 429 or a timeout, the check raises
  `MirrorsOverloaded`. That includes an unconfirmed mismatch whose second
  mirror refused. The runner counts these separately and prints "re-run, at
  least 60 s apart". The exit code is still non-zero, so nothing can read
  a RETRY as a pass. Any other failure is still a FAIL.
- **Verified offline.** Seven cases ran against a fake clock and fake mirrors:
  a 504 plus a timeout waits 60 s and then answers; 429s and 504s escalate
  60 then 120; empty 200s still wait 5 s; a 60 s deadline gives up after
  two requests and no sleep; no deadline still waits 60; a second fetch
  waits out the refusing host's minute; a 30 s deadline skips that host for
  kumi. Three brief_check cases: all mirrors 504 gives RETRY, a 400 is still
  a FAIL, and the confirmation waits 60 s. `check_overpass_hosts.py
  --selftest` passed and `check_all.py` passed 29 of 29. No drift run: no
  step imports `osm.py` (`check_no_fetch_in_steps.py` enforces that), and
  no step or output changed.
