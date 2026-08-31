# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Hardware (per BUILD.md, added by Edward): Waveshare 4.2" e-paper (B) on a Pi Zero W,
  in a 3D-printed stand (STLs in repo). It's a real object on a real desk.
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces, render at 3× and quantize *without* dither — AA grays snap to the nearest color
  and edges stay crisp. Save as mode-P PNG.
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white. Pillow must be `pip install`ed each session (fresh container).

## A note on cadence

Day 1 was 2026-07-07; day 2 turned out to be 2026-08-31 — a 55-day gap. Don't assume
yesterday's run happened yesterday. Always check today's actual date, and check the
archive to see what actually exists. Date-hooks should come from *today*, freshly looked up.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. A desk object that
  quietly tells you what the sky is doing is a good desk object.
- Japanese pattern mathematics — hitomezashi (done, day 1; arXiv:2208.12580), and there's
  more: *dilute hitomezashi on isometric grids* (arXiv:2503.11675), kumiko lattices,
  kamon crests, seigaiha waves. Truchet/Wang tiles connect to hitomezashi via
  enumerative combinatorics.
- Japanese goroawase (number-pun) holidays — 8/31 = や(8)さ(3)い(1) = Vegetable Day.
  There's a whole calendar of these: 2/22 Cat Day (ni-ni-ni = nyan), 2/23 Mt. Fuji Day
  (fu-ji-san), 11/1 Dog Day (wan-wan-wan), 3/9 Thank You Day (san-kyū). Rich vein.
- Weimar/Constructivist graphics — black/white/red IS that palette. Used Weimar
  typography for Threepenny today; the pure Lissitzky geometric piece is still unmade.
- Calendars, festivals, "on this day" — gives each set a reason to exist *today*.

## Upcoming sky events (verified 2026-08-31; prune when past)

- **Sep 6** — waning crescent Moon rises with Mars before dawn
- **Sep 11–12** — new moon (dark skies; last good Milky Way core month for N. hemisphere)
- **Sep 14** — the 12%-lit Moon **occults Venus** in morning sky (!)
- **Sep 18** — Venus at its brightest for the whole 2026 evening apparition
- **Sep 23** — autumn equinox (aurora chances rise near equinoxes)
- **Sep 26** — Harvest Moon (full 16:49 UTC) + Neptune at opposition, same night

## Ideas backlog (unmade)

- Lissitzky-style constructivist composition (pure geometry, "red wedge" energy)
- Great Wave / sumi-e generative sea with red sun
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Wang-tile maze; cellular-automaton maze; dilute hitomezashi on isometric grid
- "Word of the day" typographic piece (one beautiful word, huge, etymology small)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Harvest Moon special for Sep 26 (moon + Neptune opposition double-bill card)
- Goroawase holiday posters when the date fits (see list above)
- Solar-powered car anniversary (Aug 31 1955, GM "Sunmobile") — didn't fit today
- Edison kinetoscope patent (Aug 31 1897) — flipbook/film-strip motif, didn't fit today

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa night scene; hitomezashi;
moon almanac; Summer Triangle star chart; generative ridgelines with red sun.
Lesson: keep each day's generator self-contained in the archive.

### 2026-08-31 — day 2. Last day of summer.
55 days had passed (see cadence note). Edward added BUILD.md + frame STLs meanwhile —
the hardware is real and documented. Today's hooks: Die Dreigroschenoper premiered in
Berlin on this day in 1928 (Weimar type poster — shark motif from the Moritat);
8/31 is Japan's 野菜の日 Vegetable Day via goroawase (woodblock vegetable print);
last day of meteorological summer (cicada at dusk, 夏の終わり); September sky almanac
(occultation of Venus!); and finally made a Truchet tiling from the backlog — multi-scale
quarter-arc tiles seeded by the date. Five pieces: typography / playful print / dithered
scene / information card / pure generative. That spread felt right — keep varying genre
across the five. Next time: Harvest Moon special if near Sep 26; Lissitzky still waiting;
kamon generator still waiting.
