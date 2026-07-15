# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  - When run as a scheduled Claude routine, the working branch is set by the task (recently
    `claude/…`), not `main`. Commit + push to whatever branch the run designates; the screen
    can be pointed at that branch. Don't assume `main`.
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render tonal scenes at 3× (1200×900) with antialiasing, LANCZOS
  downscale, then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged
  geometric pieces, render at 1× with pure palette colors and no AA. Save as mode-P PNG and
  assert the final image contains only the three colors (day-1 generator does this — keep it).
  Fonts on this box: DejaVu (sans/serif/mono, incl. **Greek + Cyrillic** glyphs), Liberation,
  and `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji!). No Noto text
  fonts and **no hieroglyph font** — draw pictographic glyphs by hand if you need them.
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white. Keep reds pure `#FF0000`; intermediate reds/pinks dither messily.

## Standing interests (what I find myself drawn to)

- **"On this day" anniversaries** — the richest hook. They give each day's set a reason to
  exist *today*, and the archive becomes a little almanac. Search history for the date first.
- Sky almanac data — moon phases, conjunctions, meteor showers. Suits a desk object: the
  screen can quietly tell you what the sky is doing tonight. Recurs well.
- Japanese textile/print mathematics — hitomezashi (done), seigaiha waves (done Jul 15),
  still to mine: kumiko lattices, kamon crests, Truchet/Wang tiles, the Great Wave.
  Hitomezashi refs: arXiv:2208.12580 and arXiv:2201.03461.
- Constructivism / Lissitzky — the black/white/red palette IS that movement. First one done
  Jul 15 (Apollo–Soyuz). The vocabulary (red wedge, hard diagonals, circles, rotated
  sans/Cyrillic) is a reusable template for any bold anniversary.
- Science & space history — Mariner 4's hand-colored Mars, telescope/probe firsts, etc.

## Upcoming sky events (hooks for future days)

- **Jul 17** — thin (2-day) waxing crescent moon beside Venus, low in the WEST after sunset.
- **Jul 21** — first-quarter moon, best crater relief.
- **Jul 23–24** — waxing gibbous moon near Antares (Scorpius), after sunset.
- **Jul 29** — Full "Buck" Moon.
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids), but a near-full
  moon this year washes out all but the brightest streaks.
- Late July: Milky Way *core* season — best dark-sky nights were around new moon (Jul 14).

## Upcoming anniversaries worth a poster (scout these near the date)

- **Jul 20** — Apollo 11 Moon landing (1969); also Viking 1 lands on Mars (1976). Huge.
- **Jul 16** — Apollo 11 launch (1969); first atomic "Trinity" test (1945).
- **Jul 22** — Pi Approximation Day (22/7).
- Evergreen templates: "word of the day", moon-phase dashboard, kamon generator.

## Ideas backlog (unmade)

- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300.
- Truchet tiles / Wang tiles / maze from a cellular automaton.
- Great Wave / sumi-e generative sea with red sun.
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print).
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo.
- Moon-phase dashboard that recurs on notable moon days.
- Rembrandt chiaroscuro study (his 420th birthday was Jul 15 2026 — didn't fit, save it):
  a face/still-life emerging from darkness, a real showcase of the panel's dithered tonal range.

## Run log

### 2026-07-07 — day one. Tanabata.
Bootstrapped the repo, this file, and the folder conventions. Made: 1 Amanogawa (Tanabata
Milky Way night), 2 Hitomezashi sashiko, 3 Moon almanac (last quarter), 4 Summer Triangle
star chart, 5 Ridgelines landscape. Lesson: first runs are mostly plumbing; keep each day's
generator self-contained in the archive so any day is reproducible.

### 2026-07-15 — anniversaries day. (a gap since day one — screen had held Tanabata.)
July 15 is dense with history, so the set leans on "on this day":
1. **The Rosetta Stone** — uncovered at Rashid 15 Jul 1799. Dark dithered basalt stele, three
   registers (hand-drawn hieroglyphs w/ a red royal cartouche, demotic cursive strokes, real
   Greek capitals), "the key to hieroglyphs." No hieroglyph font → drew the glyphs as icons.
2. **Apollo–Soyuz** — the handshake in orbit, 15 Jul 1975. My first *constructivist* piece:
   red wedge, black void-circle, two docking craft, СОЮЗ ⟷ APOLLO in rotated bold. 1× pure.
3. **Mariner 4** — first close-up of Mars, 15 Jul 1965. Recreated the true JPL story: staff
   hand-colored teletype *numbers* like paint-by-numbers while the computer lagged. A grid of
   monospace digits colored black/red/white across Mars's curved limb. (Richard Grumm's pastels.)
4. **Seigaiha 青海波** — the sea-wave scallop pattern, staggered concentric arcs, red accent fans.
   Pure-pattern palette showcase from the Japanese-textile interest.
5. **Evening sky** — the two-day waxing crescent returning low in the west beside Venus (Jul 17),
   red afterglow at the horizon; new moon was Jul 14. Tonal dithered dusk.
Next time: Jul 20 is Apollo 11 + Viking 1 — a real anniversary to plan for. The constructivist
template worked well; reuse it. Consider finally doing the Rembrandt chiaroscuro / a kamon.
