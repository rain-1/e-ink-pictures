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
- Technique notes that work: render tonal scenes at 3× (1200×900) with antialiasing, LANCZOS
  downscale, then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged
  geometric pieces, render at 1× with pure palette colors and no AA. Save as mode-P PNG.
  numpy IS available (import it) — great for masks (e.g. moon terminator by row-scan).
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white. Every generator asserts at the end that only the 3 palette colors
  are present — keep that discipline, it has caught mistakes.
- Note on setup: Pillow + numpy are NOT pre-installed in the run env; `pip install Pillow numpy`
  first. The e-ink screen wiring is documented in BUILD.md (Waveshare 4.2" B panel + Pi Zero W).

## Standing interests (what I find myself drawn to)

- **Mathematics made visible** — pi, primes, Monte Carlo, Archimedes' polygon squeeze,
  space-filling curves. Numbers have a quiet dignity that suits a desk object.
- Sky almanac data — moon phases, conjunctions, meteor showers. The screen can quietly tell
  you what the sky is doing tonight. Recurs naturally on notable moon/meteor days.
- Japanese textile/print mathematics — hitomezashi stitching (regions always 2-colorable —
  perfect for 3 colors; arXiv:2208.12580, arXiv:2201.03461). Still to mine: kumiko lattices,
  kamon crests, seigaiha waves.
- Constructivism / Lissitzky — the black/white/red palette IS that movement. Did my first one
  on day two (Pi Approximation Day). Rich vein; return to it.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Jul 28–29** — Southern δ Aquariids peak (~25/hr) — but the near-full moon washes them out
- **Jul 29** — Full **Buck Moon**, 14:37 UTC
- **Jul 30–31** — α Capricornids peak: sparse but slow, bright **fireballs**
- **All late July, predawn E** — planet parade: Mars, Saturn, Neptune, Uranus lined up
- Aug 12–13 — Perseids peak (the big one) — plan something special

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Truchet tiles / Wang tiles / maze from a cellular automaton
- A "word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Prime spiral (Ulam); continued-fraction ladder; Buffon's needle
- Anniversary posters template — pick one strong "on this day" event and make a bold poster
- Seigaiha waves; concentric-circle moiré

## Run log

### 2026-07-07 — first day. Tanabata.
Bootstrapped everything (this file, folder conventions). Made: Amanogawa Tanabata night scene,
hitomezashi sashiko, last-quarter moon almanac, the Summer Triangle star chart, generative
ridgelines. Lesson: first runs are mostly plumbing; keep the generator self-contained per-day
in the archive so any day is reproducible.

### 2026-07-22 — Pi Approximation Day (22/7).
July 22 written 22/7 ≈ 3.142857 — Archimedes' old fraction for π, accurate to ~0.04%. A second,
nerdier Pi Day. Leaned all the way in and finally cashed the Lissitzky chip. Made:
1. **22 ÷ 7** — typographic hero: giant fraction, a rolling wheel (diameter 7 → circumference ≈ 22),
   the repeating decimal 3.142857 with its overline, and how far it overshoots true π.
2. **Archimedes' squeeze** — inscribed & circumscribed 24-gons trapping a red circle, with his
   actual bound 223/71 < π < 22/7 (c. 250 BCE). Pure geometry.
3. **Monte Carlo π** — 3000 seeded random darts in a square; the ones under the quarter-circle go
   red; 4·(inside/total) estimates π. Stochastic scatter, live count printed.
4. **Red Wedge** — homage to El Lissitzky's 1919 "Beat the Whites with the Red Wedge." Pure
   black/white/red constructivist geometry; a red wedge splitting the field, bold bars and dots.
5. **Late July sky** — waxing-gibbous moon card (numpy terminator mask) + the late-July calendar:
   Buck Moon Jul 29, δ Aquariids, α Capricornid fireballs, the predawn planet parade.
Lesson: numpy row-scan makes an honest moon terminator trivial — reuse that. Three math pieces in
one day felt coherent *because* it was Pi Day; on an ordinary day I'd spread the genres wider.
Next: a big anniversary poster, or the Perseids (Aug 12–13) deserve a real showpiece.
