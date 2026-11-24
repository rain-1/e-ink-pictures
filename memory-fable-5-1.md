# Memory (memory-fable-5-1.md)

I am Claude. Once a day I wake, read this file, wander the web, and make five fresh
pictures for the 400×300 black/white/red e-ink screen on Edward's desk. This file is how
I remember myself. Future me: read all of it, then prune and rewrite freely.
(`memory.md` is an older file from the first-ever run on 2026-07-07; this one supersedes
it. I carried over what still mattered.)

## Contract

- 400 × 300, exactly three inks: `#000000`, `#FFFFFF`, `#FF0000`. Mode-P PNG.
- `images/1.png` … `5.png` — today's five, overwritten daily (the screen reads these).
- `archive/YYYY-MM-DD/` — dated copies + the self-contained `generate.py` that made them.
- The session can only push to its assigned `claude/...` branch, not `main`. If the
  screen reads `main`, Edward has to merge — tell him via notification when that's so.

## Plumbing gotchas (cost me 5 tool calls on 11-24)

- `python3` is 3.11 in /usr/local; bare `pip` belongs to a different Python. Always
  `python3 -m pip install numpy scipy` and `python3 -m pip install --ignore-installed pillow`.
- Fonts: DejaVu has **no italic** (Sans, Sans-Bold, SansMono, Serif, Serif-Bold only).
  For italic use `liberation/LiberationSerif-Italic.ttf`. Also: freefont, jetbrains-mono,
  noto, wqy, `fonts-japanese-gothic.ttf` (kanji).
- DejaVuSansMono 9px ≈ 5.4 px/char → ~50 chars max in the caption strip's left half.

## Technique notes

- Line art: draw at 3×, LANCZOS down, then **snap to nearest ink** (no dithering) — crisp.
  Floyd–Steinberg only for genuinely tonal things. Poisson-disc stipple with
  density-dependent radius is a nicer "tone" than FS and feels hand-engraved.
- Red carries huge weight. Best use so far: red as a *category* (the living tips, the
  spots vs. the stripes, the lens glass) rather than as decoration.
- Always build a contact sheet and look at it; first renders always have clipped labels.

## Style, as it's forming

- **House plate strip**: 13px band at the bottom, mono 9px — left: `SUBJECT · algorithm`,
  right: `DD·ROMAN-MONTH·YYYY  n/5`. I like naming the algorithm like a medium
  ("oil on canvas" → "space colonization"). Keep this.
- Each day's five = five *different algorithms*, bound by the date (anniversaries + sky).
  One day, one thread running through all five, is better than five unrelated images.
- A short true sentence in the picture beats a title. Dry, exact, a little tender.
- Alternate black-ground and white-ground plates through the day's sequence.

## Algorithms used (don't repeat soon — pick from the unused list)

- 07-07: FS-dithered night scene, hitomezashi, moon card, star chart, layered ridgelines.
- 11-24: Poisson stipple, space colonization, 2-D lens ray tracing (caustic),
  Gray-Scott reaction-diffusion (F/k gradient: spots→labyrinth), Penrose rhomb deflation.
- **Unused, wanted**: differential growth line; DLA; sandpile fractal; strange attractors
  (Clifford / de Jong) as density plots; Voronoi / Lloyd-relaxed stained glass; Truchet &
  Wang tiles; L-systems; circle packing / Apollonian gasket; flow fields with streamline
  hatching; marching-squares contour maps (invented topography); cellular automata (rule
  30/110, Life trails); Hilbert/Gosper curves; Chladni figures; harmonograph; phyllotaxis;
  wave interference/moiré; isometric impossible architecture; kumiko & kamon; halftone
  type; woodcut-style hatching by normal direction; Lissitzky constructivist poster.

## Subject ideas

- Word-of-the-day typographic plate (one huge word, etymology small).
- A map plate: real coastline or invented island with contour lines and a red route.
- Musical plate: a score fragment / piano-roll of a piece premiered on the day.
- Tide/sunrise/daylight-length data plates — late Nov to Dec 21 is the dark slide to solstice.
- A portrait attempt purely from primitives (hard; try it when feeling brave).

## Sky hooks

- Nov 25 — lunar perigee. Dec 13–14 — Geminids. Dec 21 — solstice.
- **Dec 24 2026 — full supermoon, the largest of the year, on Christmas Eve.** Do something.
- Jan 2027 Wolf Moon is the third supermoon of this run.

## Run log

### 2026-07-07 — Tanabata (first run; details in old memory.md)
Night scene, hitomezashi, moon almanac, Summer Triangle, ridgelines.

### 2026-11-24 — "endless forms"
Found: Beaver supermoon full at 14:53 UTC, Moon meeting Alcyone/Pleiades that morning.
Nov 24 is also Origin of Species (1859), Spinoza's birthday (1632), Lucy's discovery (1974).
Thread: looking closely at nature. Made:
1. **LUNA** — stippled supermoon on black, the Pleiades in red at their real relative positions.
2. **I think** — Darwin's notebook-B tree regrown by space colonization; red buds, crossbar tips.
3. **Deus sive Natura** — red biconvex lens, 49 traced rays, spherical-aberration caustic.
4. **Morphogenesis** — Gray-Scott; red spots dissolve into a black labyrinth; "endless forms most beautiful".
5. **Lucy** — Penrose sky "with diamonds" (thin rhombs white/red), AL 288-1.
Self-critique: moon craters read as little "C"s — next time shade craters with stipple
density only, no drawn rims. The Darwin tree was the best plate: an algorithm that *is*
the subject. Look for more of those matches (the medium should mean something).
Next time: lean toward something non-scientific — music, a poem, a place — for contrast.
