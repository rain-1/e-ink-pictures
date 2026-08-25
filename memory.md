# Memory

I am Claude. Once a day (though gaps happen — 49 days passed between runs 1 and 2!)
I wake up, read this file, wander the web a little, and make five fresh pictures for
the small e-ink screen on Edward's desk. This file is how I remember myself between
days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). I work on a
  `claude/...` branch the scheduler assigns; Edward merges to `main`. The screen reads `main`.
- Conventions (keep stable):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Tonal scenes: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg dither
    into the exact 3-color palette. Hard-edged graphic pieces: still render at 3× but
    quantize with `dither=False` for clean edges. Save as mode-P PNG.
  - **Palette indices after quantizing: 0 = WHITE, 1 = BLACK, 2 = RED.** Text drawn
    after `finalize()` uses these indices — I lost a whole render cycle on day 2 by
    assuming 0 was black. Check every `fill=` against the background it sits on.
  - Fonts: DejaVu (sans/serif/mono), Liberation, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (IPAGothic — renders kanji).
    For vertical Japanese text, rotate ー 90°.
  - Red reads *bright* on the panel — use as accent; red-on-black is legible, red text
    crossing a red shape is not (mind overlaps).
  - Pillow isn't preinstalled in the fresh container: `pip install pillow` first.
  - Chord-by-chord horizontal lines with a latitude function = easy shaded planet discs.
  - Always Read the 5 PNGs before committing; every bug I've shipped was visible at a glance.

## Standing interests (what I find myself drawn to)

- Sky almanac data — image slot 3 has become the recurring "almanac card". Keep that.
- Space-history anniversaries — Aug 25 turned out to be Voyager Day (Neptune '89 +
  heliopause '12, same calendar date). Dates like this are gold; check "on this day"
  for space events each run.
- Japanese textile/print mathematics — hitomezashi (done day 1), seigaiha wave-scales
  (done day 2, as the sea of a map — pattern-as-terrain works great). Still to mine:
  kumiko lattices, kamon crests, asanoha, 雷紋 meander borders (used one on a ramen bowl).
- Constructivism — did the red-wedge homage (Voyager 1 piercing the heliosphere).
  The vocabulary (big circle, wedge, diagonal type) is deeply right for this palette;
  can return with different subjects, e.g. an eclipse as circle-eats-circle.
- Maps with story routes on them (Channel swim worked well — route lines in red over
  patterned sea). Other candidates: Cook's voyages, Voyager grand tour trajectory,
  Shackleton, the Tokaido road's 53 stations.

## Upcoming sky events (hooks for future days)

- **Aug 27–28** — deep partial lunar eclipse, 96% umbral, "blood moon", greatest 04:13 UT
  Aug 28 (Americas best; also Europe/Africa). Featured on today's almanac. If a run
  lands Aug 27/28, make it the lead image.
- **Sep 1** — Venus–Spica conjunction (evening)
- **Sep 8–14** — best stargazing window (new moon Sep 11)
- **Sep 23** — equinox, 00:05 UTC
- **Sep 25** — Neptune at opposition (nice callback to the Voyager Neptune piece)
- Look further ahead next run: October brings harvest moon + Orionids (verify dates online).

## Ideas backlog (unmade)

- **Voyager Golden Record** — the etched cover diagram (pulsar map, hydrogen hyperfine,
  playback instructions) is a ready-made black-line diagram; would be stunning. Saved it
  deliberately — good for a slow-news day.
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology small)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Great Wave / sumi-e generative sea with red sun
- Anniversaries skipped on 8/25 (usable next Aug 25 or as templates): Galileo demos the
  telescope to Venice (1609), Wizard of Oz premiere (1939), Cook sails on first voyage
  (1768), National Park Service founded (1916)
- Eclipse-as-constructivism: black disc devouring white disc, red lune

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Made: Amanogawa night scene; hitomezashi;
moon almanac; Summer Triangle star chart; generative ridgelines. Lesson: keep each
day's generator self-contained in the archive.

### 2026-08-25 — day 2. Voyager Day.
Woke after a 49-day gap (my July sky-events list was entirely stale — hence the
"verify dates online" habit). Learned Aug 25 = Voyager 2's Neptune flyby (1989) AND
Voyager 1 crossing the heliopause (2012), exactly 23 years apart. Made:
1. **Neptune** — dithered banded disc, red Great Dark Spot, Voyager 2 silhouette, dotted flyby arc.
2. **Interstellar** — constructivist red wedge piercing a black heliosphere circle (Lissitzky homage, finally).
3. **Almanac: blood moon** — the Aug 27–28 96% eclipse, red moon with white sliver + September preview.
4. **The first Channel swim** — Dover–Calais map, seigaiha sea, dashed 21-mi course vs Webb's red 39-mi tide-bent path (1875).
5. **即席ラーメン** — Momofuku Ando invents instant ramen (1958): hinomaru, black bowl with 雷紋 band, chopsticks lifting noodles.
Lessons: palette-index gotcha (see technique notes); place text before checking, then
actually LOOK at all five renders — three images had invisible text on first pass.
Next time: consider the Golden Record piece, and whatever October's sky offers.
