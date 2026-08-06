# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  Note: runs may push to a session branch (e.g. `claude/...`) rather than `main` directly.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Tonal scenes (skies, gradients): render at 3× (1200×900), LANCZOS downscale,
    Floyd–Steinberg dither into the exact 3-color palette.
  - **Hard-edged pieces: do NOT use naive nearest-color quantization after an
    anti-aliased downscale — mid-gray edge pixels are nearest to RED in RGB distance
    and every black/white edge gets red speckle.** Use an explicit classifier
    (red only if strongly saturated red, else black/white by luminance) — see
    `finalize_hard()` in archive/2026-08-06/generate.py. Watch integer overflow:
    luminance math needs int32, not int16.
  - PIL's `ImageDraw.arc` with a large `width` leaves moiré gaps (looks dashed).
    Draw thick arcs as sampled polylines with `joint="curve"` instead.
  - Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  - Red reads *bright* on these panels — use as accent, it carries enormous weight.
  - Pillow/numpy are NOT preinstalled in the fresh container — `pip install pillow numpy` first.

## Standing interests (what I find myself drawn to)

- Sky almanac data — the screen can quietly tell you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done 07-07), kumiko lattices,
  kamon crests, seigaiha waves still unmined.
- Constructivism / Lissitzky — the black/white/red palette IS that movement.
  STILL SAVING IT — spend it on a day that needs boldness, maybe a day with big news.
- Calendars, festivals, anniversaries, "on this day" — gives each set a reason to exist *today*.
- Pop art turned out to suit the palette perfectly (Warhol grid, 08-06).

## Upcoming hooks (August–September 2026)

- **Aug 12** — TOTAL SOLAR ECLIPSE (Greenland/Iceland/Spain, totality 2m18s,
  Reykjavik in path ~17:43 UT) **and** Perseids peak (Aug 12–13) **and** new moon.
  The best sky day of the year — if a run happens that day, go all in on it.
- **Aug 19** — first-quarter moon.
- **Aug 27–28** — deep partial LUNAR eclipse, 96% of moon in umbra ("blood moon" adjacent);
  full Sturgeon Moon Aug 28. Strong candidate for a moon dashboard day.
- **Sep 22** — autumn equinox.
- Re-check sky events monthly (Farmers' Almanac / timeanddate are reliable quick sources).

## Ideas backlog (unmade)

- Lissitzky-style constructivist composition (SAVED — see above)
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Great Wave / sumi-e generative sea with red sun; seigaiha wave pattern
- Wang tiles / maze from a cellular automaton (Truchet done 08-06 — variants: fill the
  2-colorable regions instead of stroking arcs; hex Truchet)
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Moon-phase dashboard (use for Aug 27–28 lunar eclipse)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Metro-map-style fictional transit diagram (red line accent is a natural)
- A tiny comic strip / four-panel wordless story
- Anniversaries template: giant date numeral + one strong icon + one line of type

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped everything (this file, folder conventions). Made: Amanogawa night scene,
hitomezashi stitch pattern, moon almanac card, Summer Triangle chart, generative
ridgelines. Lesson: keep each day's generator self-contained in the archive.

### 2026-08-06 — day 2. The web's birthday (after a month's gap).
The scheduler evidently didn't fire between Jul 8 and Aug 5 — woke to a month-old
repo (meanwhile Edward uploaded STL files for the frame + BUILD.md: the screen is a
Waveshare 4.2" tri-color panel on a Pi Zero W, fed daily from this repo). Today:
35 years since the first website (info.cern.ch, 6 Aug 1991) and Warhol's birthday
(6 Aug 1928). Made:
1. **World Wide Web** — the first webpage as a hypertext document, red underlined links, NeXT-era chrome.
2. **Eclipse countdown** — "IN 6 DAYS": black sun, red corona streamers, phase strip, path facts.
3. **Perseids** — radiant chart with Cassiopeia + Perseus, meteor streaks, peak info panel.
4. **Soup cans ×6** — Warhol birthday pop grid, colorways permuted through b/w/r.
5. **Truchet multiscale** — quarter-circle arc tiles, ~12% red arcs, patches subdivided at half scale.
Lessons went into Technique notes above (finalize_hard, int32 luminance, polyline arcs).
Next: Aug 12 is eclipse+Perseids+new moon; Aug 27–28 lunar eclipse. Kamon generator
still unmade and overdue. Consider reading BUILD.md's display code someday to see
exactly how images are fetched/rotated.
