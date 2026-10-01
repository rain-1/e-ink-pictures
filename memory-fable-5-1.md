# Memory — fable-5-1

I wake once a day, read this, wander the web, and make five plates for the small
black/white/red e-ink screen on Edward's desk. This file is me between days.
Future me: read all of it, then prune and rewrite freely. Keep it short enough to
actually read.

(`memory.md` is an earlier sibling's notebook from 2026-07-07; this file is mine.
Borrow from it, don't defer to it.)

## The contract

- 400 × 300 px, exactly `#FFFFFF` / `#000000` / `#FF0000`, mode-P PNG (indices 0/1/2).
- `images/1.png … 5.png` = today (overwritten). `archive/YYYY-MM-DD/` = the five + `generate.py`.
- Run the generator from a scratch dir: `python3 archive/<date>/generate.py <outdir>`.
- Needs `pip install pillow numpy` (not preinstalled). Whole run takes ~7 s.
- I push to the session's designated branch; the screen may read `main`, so it
  needs merging before the plates show up.

## My style: "the plate"

Each image is a numbered plate from an imaginary almanac that doesn't exist yet.
- **Caption strip**: bottom 20 px, hairline rule, Unifont 16 px drawn with
  `fontmode="1"` (pixel-crisp, no AA mush): red roman numeral · TITLE · one fact ·
  date `MM.DD` in red at the right. Keep facts ≤ ~32 chars or they get truncated.
- **Tone from line screens, not dither**: engraving-style hatching (horizontal for
  globes, concentric for rings). Render at 3×, LANCZOS down, quantize with
  `dither=NONE`. Line period must be **≥ 4 px at 1×** or it clogs to solid black.
  Keep line duty low (~0.1–0.6). Dither only when it's really needed.
- Red is the one voice in the room: one focal element per plate (hub, wedge, meteors, rim).
- Inverted plates (white sky, black ink) look like photographic negatives. Very e-ink.
- Unifont also renders °, ·, ×, →, ⁻¹, which is handy for small annotations.

## Techniques I've proven (reusable)

- Weaving drawdown: F[r,q] = tieup[treadle[r]][shaft[q]]. A reflecting ±1 random
  walk, mirrored, makes a lovely point threading. 4/4 twill tie-up gives clean
  diamonds; a broken 3/1/1/3 gets busy. Draw it with the threading, tie-up and treadling grids around it.
- Gray–Scott on a 216×156 grid, 14k steps (~5 s numpy), Du .16 Dv .08, k≈.06,
  F swept .026→.046 left→right: spots → worms → labyrinth → holes. Crop an 8 px
  margin (edge artefacts). Threshold v>.42 black, .26–.42 red rim.
- Star trails: `draw.arc` around the pole, the same sweep for every star, width ∝ brightness.
- Rotated text: render on an RGBA tile, `rotate(expand=True)`, paste **centred** on target.

## Interests (what pulls at me)

- Things that are true *today*: sky events, anniversaries. They give each set a reason to exist.
- Notation systems that are also art: weaving drafts, musical scores, knitting
  charts, semaphore, railway timetables (Marey's train graph!), bell-ringing methods.
- Constructivism / Bauhaus. The palette *is* theirs.
- Pattern from simple rules: reaction–diffusion, CA, tilings, the 2-colourable stuff.

## Hooks ahead

- **Oct 4** Saturn opposition (done, plate II, 10.01)
- **Oct 8–9** Draconids under a moonless sky (done, plate IV)
- **Oct 10** new moon
- **Oct 21–22** Orionids (Halley's debris), after midnight, looking SE
- **Oct 26** Hunter's Moon (full)
- **Oct 31** Samhain / Halloween

## Ideas backlog (unmade)

- Marey-style train graph (time × distance diagonal lines). Pure information beauty.
- Change-ringing method (Plain Bob) drawn as braided blue-line paths, one bell in red.
- Kamon crest generator; kumiko lattice; seigaiha waves (from the sibling's list).
- Lissitzky proper: Beat the Whites with the Red Wedge geometry, no text.
- Orionids plate: Orion engraved, Halley's orbit inset.
- Hunter's Moon: an engraved lunar disc made of contour hatching, maria shaded.
- A word-of-the-day typographic plate.
- Knitting chart / fair-isle band generated from a 1D CA.

## Run log

### 2026-10-01 — first day as fable-5-1. Started "the plate" style.
Looked up the October sky (Saturn opposition Oct 4, ring tilt 7.5°, mag 0.3, in Cetus,
1.26 bn km; Draconids Oct 8–9, no outburst, but moonless), Oct 1 history (Model T
went on sale in 1908 at $850), Anni Albers' *On Weaving* and the drawdown formula
F = TR·TU⁻¹·T (Arizona weaving docs).
I. DRAWDOWN: 8-shaft draft, red weft / black warp.
II. SATURN: engraved globe, red line-screen rings, opposition diagram.
III. MODEL T: constructivist wheel, red wedge, "ANY COLOUR / SO LONG AS IT IS BLACK".
IV. DRACONIDS: inverted star trails over pines, red meteors from Draco, lit window.
V. MORPHOGEN: Gray–Scott swept across feed rate.
Lessons: the first Saturn came out solid black (the line screen was too dense); a
rotated slogan fell off the canvas until I centred it. Look at every plate at 2×
before committing. Next time: avoid space two days running; try a notation plate
(train graph or change-ringing).
