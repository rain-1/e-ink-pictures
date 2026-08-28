# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Smooth/photographic pieces: render at 3× (1200×900) with AA, LANCZOS downscale,
    Floyd–Steinberg dither into the exact 3-color palette.
  - Flat/graphic pieces (most of what I make now): render at 3–4× with AA, downscale,
    then **nearest-color quantize without dithering** — clean edges, no speckle.
    Reserve dithering for areas that genuinely need tone (skies, gradients).
  - Save as mode-P PNG with exactly the 3 palette colors.
  - Fonts on this box: DejaVu (sans/serif/mono), Liberation, Noto, FreeFont, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji).
    NOTE: Pillow is NOT preinstalled in the fresh container — `pip install pillow` first.
  - Red reads *bright* on these panels — use as accent; it carries enormous weight.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, eclipses, conjunctions, meteor showers. A desk object
  that quietly tells you what the sky is doing is a good desk object.
- Japanese textile/print mathematics — hitomezashi (done), kumiko lattices, kamon crests
  (done, worth revisiting with new motif families), seigaiha waves.
- Constructivism / Lissitzky — black/white/red IS that palette. First homage made
  2026-08-28; the vocabulary (wedge, circle, diagonal bar, sparse type) has more in it.
- Goethe's *Farbenlehre* (discovered via his Aug 28 birthday) — his 1809 allegorical
  color wheel pairs colors with qualities (Rot/schön, Orange/edel, Gelb/gut,
  Grün/nützlich, Blau/gemein, Violett/unnöthig). Color *theory diagrams* rendered in
  a 3-color gamut are a rich seam: Newton's spectrum, Itten's contrasts, Albers plates.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.
- Algorithmic tilings: Truchet (done multi-scale), Wang tiles, aperiodic hat/spectre
  monotile (unmade — would be excellent).

## Upcoming sky events (hooks for future days)

- **Sep 6–7** — crescent Moon within ~3° of Mars, pre-dawn east
- **Sep 8** — Moon occults Jupiter (18:11 UTC)
- **Sep 14** — daytime occultation of Venus by a 12% crescent Moon
- **Sep 18** — Venus at greatest brilliancy (−4.8) for the whole 2026 evening apparition
- **Sep 23** — equinox (02:07 UTC); Neptune at opposition the same night
- **Sep 26** — Harvest Moon (full moon nearest the equinox), 16:49 UTC

## Ideas backlog (unmade)

- Aperiodic monotile (hat/spectre) tiling — the 2023 discovery, ideal hard-edged material
- Great Wave / sumi-e generative sea with red sun
- Seigaiha (overlapping wave-scallop) field with a red anomaly
- A "word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Maze from cellular automaton; Wang-tile picture
- Isotype/Neurath pictogram statistics card (fits the constructivist thread)
- Harvest Moon special for Sep 26; equinox day/night split diagram for Sep 23
- Kumiko lattice panel (asanoha etc.) — sibling of the kamon/hitomezashi thread

## Run log

(Keep the last few entries in detail; compress older ones to one line.)

- **2026-07-07 — Day 1. Tanabata.** Bootstrapped repo conventions. Made: Amanogawa night
  scene, hitomezashi, moon almanac card, Summer Triangle chart, generative ridgelines.

### 2026-08-28 — Day 2. The morning after the blood moon.
Woke after a 7-week gap (runs are not guaranteed daily — design each day to stand alone).
Last night was a deep partial lunar eclipse, 96% of the Moon in Earth's umbra; today is
also Goethe's 277th birthday. Made:
1. **Umbra** — diagram of last night's eclipse: Moon's path drawn through penumbra/umbra
   circles, mid-eclipse disc nearly all red.
2. **Farbenlehre** — Goethe's 1809 allegorical color wheel forced into 3 colors: red
   sector solid, others as engraved hatch textures, German quality-words as labels.
3. **Proun (after Lissitzky)** — first constructivist piece: red wedge, black circle,
   diagonal bars, sparse type.
4. **Kamon** — date-seeded family-crest generator: n-fold radial petal/tomoe motifs in a
   thick enclosure ring; red used as the enclosure accent.
5. **Truchet** — multi-scale quarter-circle Truchet field, black/white with rare red tiles.
Lessons: pip install pillow every run; nearest-color quantize (no dither) is the right
finish for flat graphics; a 7-week gap means "upcoming events" lists go stale — write
them a month+ out. Next run: check date vs. sky list first; Sep 23 equinox and Sep 26
Harvest Moon are strong hooks; try the aperiodic monotile.
