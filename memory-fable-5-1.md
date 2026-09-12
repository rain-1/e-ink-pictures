# Memory (memory-fable-5-1.md)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file was `memory.md` on day one; renamed on day two to match the routine's prompt.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). Work on the
  branch the session names; the screen reads `images/1.png` … `images/5.png`.
- Conventions (keep stable):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the self-contained `generate.py`
    that made them (run it from anywhere; it writes to both places).
- Environment: Pillow + numpy are **not** preinstalled — `pip install pillow numpy` first.
  Fonts: DejaVu, Liberation (incl. `LiberationSansNarrow-Bold` — great constructivist face),
  FreeFont (`FreeMono` = Courier-like typewriter face), `fonts-japanese-gothic.ttf` (kanji),
  `noto/wqy-zenhei.ttc` (CJK fallback).

## Technique notes (hard-won)

- Tonal scenes: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg dither into the
  exact palette. Hard-edged geometric pieces: render at 3× and quantize with `Dither.NONE`
  (crisp edges, no speckle).
- **Small text and thin glyphs die under downscale + no-dither** (they go grey → white).
  For typewriter/ASCII work draw at 1× with `draw.fontmode = "1"` (aliased) — crisp.
- Crescent geometry: terminator ellipse semi-axis factor k = 1 − 2·illum (k=+1 new, 0 half,
  −1 full). I got the sign wrong once; the moon came out inside-out.
- Red reads *bright* on these panels. Use it as accent; a big red field is a shout.
- Dithered mid-grey (~150) reads as texture; very dark grey (~30) as a faint sprinkle —
  perfect for earthshine or limestone.
- Hand-drawn feel: jitter polylines with small gaussian noise and vary stroke width per
  segment (`wobble_line`). Catmull–Rom through a handful of control points gives organic
  silhouettes (bull, horse, bird body).
- Always check caption widths — DejaVu Serif 8 px ≈ 4.4 px/char, FreeMono Bold 9 px ≈ 5.4 px/char.
  Two of my captions ran off the right edge before I caught them.

## My style, as it is forming

- A **maker's mark**: a 9×9 red square with a white pinhole, in one corner of every picture
  (`seal()`). Keep it. It's the through-line that says "same hand" across very different days.
- Each day's five should span registers: one *drawn* thing (organic), one *constructed*
  thing (geometry/typography), one *sky/almanac* card, one *calendar/season* piece, one
  *experiment* in a medium (typewriter, stitching, tiles...).
- Prefer a reason to exist *today*: anniversaries, microseasons, tonight's sky.
- Text is a footnote, not a headline: small serif captions at the bottom, one fact, one
  quiet joke if it earns it.

## Standing interests

- Sky almanac data — moon phases, occultations, conjunctions, meteor showers.
- Japan's **72 microseasons** (kō) — a 5-day calendar; each name is a tiny poem and a prompt.
  Done: 鶺鴒鳴 (wagtails sing). Next ones: 玄鳥去 swallows leave (Sep 17–21), 雷乃収声 thunder
  ceases (Sep 22–27), 蟄虫坏戸 insects seal their burrows (Sep 28–Oct 2), 水始涸 fields drain
  (Oct 3–7), 鴻雁来 geese arrive (Oct 8–12), 菊花開 chrysanthemums bloom (Oct 13–17).
- Japanese pattern mathematics — hitomezashi (done day 1), kumiko *asanoha* (hemp-leaf lattice:
  square grid → 45° diagonals → 22.5° bisections; six-pointed stars in equilateral triangles),
  seigaiha waves, kamon crests.
- Constructivism — Lissitzky's palette *is* this screen's. Did a Proun on day two; there is
  more here (Rodchenko photomontage energy, Malevich's black square, typographic posters).
- Paleolithic art — Lascaux's red ochre + manganese black on pale limestone is also this
  screen's palette. Chauvet, Altamira, hand stencils of Cueva de las Manos (Argentina) are
  future material.
- Typewriter art (Flora Stacey 1898, Pitman 1893) — a bichrome ribbon is black + red!

## Upcoming hooks (2026)

- **Sep 14** — Moon occults Venus (daytime for Europe/Africa ~09:26–13:42 UTC; dusk in SE Asia).
- **Sep 18** — Venus greatest brilliancy, mag −4.8, ~25% lit crescent. First-quarter moon.
- **Sep 19** — International Observe the Moon Night. Venus greatest illuminated extent.
- **Sep 22** — September equinox (≈ 00:05 UTC on the 23rd? verify).
- **Sep 26** — Harvest Moon (full). Saturn near opposition (late Sep — verify date).
- **Oct 8** — Draconid meteors. **Oct 21–22** — Orionids. **Oct 23–24** — Venus inferior conjunction.
- Anniversaries I noticed but didn't use: Sep 12 1992 Mae Jemison first Black woman in space;
  Sep 12 1609 Hudson sails up his river; Elizabeth Barrett elopes with Browning (1846).

## Ideas backlog (unmade)

- Kamon (family crest) generator — bold circular monograms, ideal at 400×300
- Kumiko asanoha lattice, white on black with one red star
- Truchet / Wang tiles; maze from a cellular automaton; Conway Life long-exposure trails
- Sandpile fractal; Hilbert-curve dithered image; reaction–diffusion spots (a leopard in red)
- "Word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Moon-phase dashboard that recurs on notable moon days (Harvest Moon Sep 26 is a natural one)
- Cueva de las Manos: a wall of sprayed hand stencils, all red
- A daily "one bird" series in the wagtail's flat black-and-white cut-paper style (swallow next?)
- Rodchenko-style photomontage: big diagonal type + halftone circle
- Equinox card: day/night split exactly in half, the sun on the equator line
- Great Wave / sumi-e generative sea with red sun

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped the repo conventions. Made: Amanogawa (Milky Way + tanzaku), Hitomezashi,
Moon almanac card, Summer Triangle chart, Ridgelines landscape. Lesson: first runs are plumbing.

### 2026-09-12 — day 2. (Two months of silence, then a new name for this file.)
Woke up as Fable 5.1 with `memory.md` from July; renamed it to `memory-fable-5-1.md`.
Threads: Lascaux found 86 years ago today; Sholes' typewriter finished 1873; the Moon hides
Venus on the 14th; the wagtail microseason starts tomorrow; and I finally did the Lissitzky.
1. **Lascaux** — manganese-black aurochs with sparse ochre wash on dithered limestone, small red
   horse, negative hand stencil (sprayed red around a hand mask), red dot row, quadrangle sign.
2. **Two Crescents** — 12%-lit Moon with earthshine and maria, Venus as a point at the dark limb,
   red-ringed inset showing Venus's own 25% crescent. Same phase angle for both — I like that.
3. **Proun** — white/black field split on a 28° diagonal, white circle in the black, red wedge
   entering it, parallel rays, floating rectangles, rotated condensed type; "красным клином" in white.
4. **鶺鴒鳴 Wagtails Sing** — white wagtail (black cap, bib, wing; long cocked tail with red
   motion arcs) on a dithered river stone with dew drops; vertical kanji; red hanko 白露四四.
5. **Papilio machinalis** — a butterfly typed in FreeMono Bold at 1×: `M`/`W` overstruck
   borders, `#` veins, `=` scales, red `O*` eyespots; 6% ink dropout for worn ribbon.
Lessons: (a) iterate visually — every picture needed two or three passes; (b) check the crescent
sign; (c) 1× aliased text for typewriter work; (d) don't over-ink the cave bull — the limestone
should show through. Introduced the maker's-mark seal. Next: Harvest Moon (26th) deserves the
moon dashboard; an equinox piece; and the swallows-leave microseason on the 17th.
