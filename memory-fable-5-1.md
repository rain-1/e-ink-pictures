# Memory — Fable 5.1

I am Claude (Fable 5.1). Once a day I wake up, read this file, wander the web, and make five
fresh pictures for the 400×300 black/white/red e-ink screen on Edward's desk. This file is how
I remember myself between days. Future me: read all of it, then prune and rewrite freely.
There is an older `memory.md` from a predecessor run (2026-07-07, Tanabata); I read it on my
first day and folded what mattered into this file. Leave it alone; it isn't mine.

## The screen & the contract

- 400 × 300 pixels, three colours only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to `rain-1/e-ink-pictures`. The routine gives me a branch
  (`claude/…`) to push to; Edward merges or points the screen where he likes.
- Conventions (stable, don't break them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of the five + the `generate.py` that made them.
  - `generate.py` in the repo root is always the latest day's script; it is self-contained.
- Toolchain: `pip install pillow numpy` is needed each session (the box starts bare).
  Fonts: DejaVu (sans/serif/mono), Liberation (sans/serif/mono, has italics).

## Technique notes (hard-won, keep)

- Two finishing paths and they matter:
  - **hard**: draw at 3× with AA → LANCZOS to 1× → nearest-colour, *no dither*. For line art,
    posters, type. Lines must be ≥3 px at 3× or they thin to nothing.
  - **soft**: same but Floyd–Steinberg into the palette. For gradients, moons, photos.
- Never draw text directly onto an already-dithered 1× image: the AA greys get thresholded
  into gravel. Render captions at 3× on a solid strip and paste the strip in (see day-2 image 3).
- Dithered dark fields look speckled; subtract a floor (~0.04) before quantising so true black stays black.
- Small text: 7 px sans is the floor for legibility; 6 px is not.
- Red reads *bright* on this panel. One red thing per picture is usually enough; it becomes
  the subject whatever else is going on.
- Rotated type: draw on an RGBA layer, `rotate(expand=True)`, paste with itself as mask.

## Style I'm developing

- I like the picture to be *about* something true today (an anniversary, the sky), and to carry
  one fact you didn't know, in small type at the bottom.
- Diagram-as-art: engraved instruction diagrams (Golden Record cover), almanac cards, poster
  geometry. Line + one flat red shape on a black or white field. Very little grey.
- I want to push next toward: generative textiles/tilings, big single-glyph typography, and
  photos reduced to dither (the Pale Dot piece worked — dither *is* the medium here).

## Standing interests

- Sky almanac data — the screen can quietly tell you what the sky is doing tonight.
- Deep-space probes as characters: Voyager 1 hits **one light-day** from Earth on
  **18 Nov 2026, 10:16 UTC** (25.902 bn km). Its signal already takes ~23 h. Make something for it.
- Japanese textile/print mathematics — hitomezashi (done on day 1), kumiko lattices, kamon crests,
  seigaiha waves, asanoha.
- Aperiodic tilings: the **hat** (Smith/Kaplan/Myers/Goodman-Strauss, arXiv:2303.10798) is a
  polykite on the hex grid; the **spectre** is its chiral cousin. A hat tiling with one red hat
  would be gorgeous — needs the H/T/P/F substitution system implemented, ~1–2 h of code.
- Constructivism / Lissitzky — the black/white/red palette *is* that movement. Did one today.

## Upcoming hooks (dates are UTC)

- **Sep 8** — Moon <1° from Jupiter, pre-dawn
- **Sep 11** — New Moon 03:27
- **Sep 18** — Venus at peak brilliance, evening
- **Sep 23** — Equinox 00:06
- **Sep 26** — Full Moon 16:50 · Neptune at opposition 02:00 (in Pisces)
- **Oct** — Orionids ~21st; Draconids ~8th
- **Nov 18** — Voyager 1 one light-day
- Anniversaries I noticed: Sep 8 Star Trek premiere 1966; Sep 12 "we choose to go to the Moon"
  1962; Oct 4 Sputnik 1957. (Verify dates before using them.)

## Ideas backlog (unmade)

- Hat monotile tiling, one red hat.
- Great Wave / sumi-e generative sea with red sun.
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300.
- Truchet / Wang tiles / cellular-automaton maze.
- "Word of the day": one beautiful word huge, etymology in small print.
- Moon-phase dashboard on notable moon days (new/full/eclipse).
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo.
- A dithered photograph day: a public-domain photo reduced to the three inks (Hubble? Apollo?).
- Typographic "80" worked; try a single kanji or a single letterform filling the screen.

## Run log

### 2026-07-07 — (predecessor) Tanabata
Milky Way scene, hitomezashi, moon almanac, Summer Triangle chart, ridgelines. Established the folder conventions.

### 2026-09-05 — Voyager Day (my first day)
Voyager 1 launched 49 years ago today; Freddie Mercury born 80 years ago. Made:
1. **The Cover** — Golden Record cover re-engraved: red disc with grooves, stylus, the video-signal wave and raster, the 14-spoke pulsar map with binary ticks, the hydrogen spin-flip clock and its "1".
2. **Red Wedge** — Lissitzky, re-aimed: red wedge from the lower left pierces the white heliosphere circle into black interstellar space; VOYAGER along the wedge; 1977 → ∞.
3. **That Dot** — Pale Blue Dot with no blue: three diagonal sunbeams of Floyd–Steinberg dither on black, one 4×4 red pixel, Sagan's line beneath.
4. **September Sky** — almanac card: waning crescent (~40%), six dated events with red day numbers, and a red progress bar to one light-day (74 days to go).
5. **Eighty** — huge "80" under a red crown, a piano keyboard with one red key, Farrokh Bulsara / Stone Town, and the day's other anniversaries in a footnote.
Lessons: captions on dithered images need their own solid strip; the almanac card format is
reusable (moon + events + one countdown). Next time: don't make five things about one subject;
two is plenty. Try a tiling or a textile piece, and something with no words at all.
