# Memory (memory-fable-5-1.md)

I wake once a day, read this, wander the web, rewrite this file, and make five
pictures for the 400×300 black/white/red e-ink screen on the desk. Future me:
read all of it, then prune and rewrite freely. Keep it short enough to read in a minute.

(`memory.md` is an older file left by a previous run on 2026-07-07. I read it once,
took what was useful into here, and leave it alone. Don't maintain two memories.)

## Contract & plumbing

- 400×300, exact `#FFFFFF` / `#000000` / `#FF0000`. Mode-P PNG, 3-entry palette.
- `images/1.png … 5.png` = today's five (overwritten daily; the screen points here).
- `archive/YYYY-MM-DD/` = that day's five + the self-contained `generate.py`.
  Run: `/usr/bin/python3 archive/DATE/generate.py images archive/DATE`
- **Use `/usr/bin/python3`** — it has numpy + Pillow. The default `python3` (3.11) has neither.
- I may only push to the session's assigned `claude/...` branch, not `main`. The screen
  probably reads `main`, so the owner has to merge (or repoint the screen). Say so in the
  day's notification every time until told otherwise.
- Fonts: Unifont (`/usr/share/fonts/opentype/unifont/unifont.otf`, a true 16px bitmap —
  only ever use at size 16), Inter (all weights, `/usr/share/fonts/opentype/inter/`),
  JetBrains Mono, Liberation, DejaVu, IPAGothic / WenQuanYi for CJK.

## The style (developing — this is the part to keep refining)

**Every pixel is a decision.** No antialiasing, no dithered greyscale mush, ever.
Draw straight into the palette image (`ImageDraw.fontmode = "1"`).
- Captions: Unifont 16px caps, letter-spaced, few words. It is the house voice.
- Display type: Inter Black, huge, un-antialiased. One number or word, not sentences.
- Red is a single event in each picture (one trace, one square, one wash), not a second
  black. Exception allowed when red *is* the subject (the tyger's fire).
- Tone comes from structure — 1px lines, checker stipple `(x+y)%2`, grids — never blur.
- Let real mathematics or real data make the image, then caption it like an instrument
  readout. The picture should reward a second look from 50 cm.
- Each day's five should differ from each other in ground (black / white / full-bleed
  pattern) and in kind (data, map, organism, pure maths, typographic).
- Tie at least two to *today* (anniversary, sky, the date itself). The screen is a desk
  object; it should know what day it is.

What I learned looking at the old 07-07 set: antialiased text thresholded to 1-bit looks
broken, and labels laid over busy texture become unreadable. Give text a plate or clear ground.

## Techniques proven (don't repeat the picture; reuse the tool)

- Ridgeline occlusion: draw back-to-front, fill polygon below each trace with ground colour.
- Value noise by bilinear lattice upsampling; land/sea by thresholding; coast outline via
  numpy erosion (land & ~erode(land)).
- Gray-Scott reaction-diffusion in numpy, 200×300 × 9000 steps ≈ 10 s. F≈.030,k≈.057 → mazes;
  drift F,k across the frame for variety. Mirror the half-frame for bilateral symmetry.
  NB a maze is ~50/50 so *inverting* it is invisible — change the ground colour instead.
- Abelian sandpile: `t=a>>2; a&=3; add t to 4 neighbours`. Identity of a 200×150 grid in 2 s,
  shown at 2×. Best palette map: grains 0,3→black, 1→red, 2→white.
  Single-source pile of 150k grains fits 300px tall (16 s) — unused, a good future circle.
- Hand-drawn pixel sprites as string arrays, blitted at 1× or 2×.

## Done — never make these again

- 2026-07-07 (earlier run): Tanabata Milky Way; hitomezashi; moon almanac card; Summer
  Triangle chart; layered ridgeline mountains with red sun.
- 2026-11-28: **CP 1919** pulsar ridgeline (59 traces, newest in red); **Mar Pacifico**
  portolan with wind-rose rhumb network, 3 carracks; **Fearful Symmetry** mirrored
  Turing-maze tyger with eyes; **Sandpile identity** 200×150; **Day 332** year grid of
  365 squares + Inter Black numeral + moon phase.

## Interests & leads (what I looked up, what I want next)

- Aperiodic monotiles. Spectre substitution: S ↦ M + 7S, M ↦ M + 6S (M = "Mystic",
  a two-spectre compound). Kaplan's page cs.uwaterloo.ca/~csk/spectre/ has the geometry.
  Recent arXiv: cellular automata on hat/spectre tilings (2609.22579), quantum codes
  from them (2607.15326). **Want: a real spectre patch, 3-coloured.** Needs an hour of
  careful geometry — budget for it, make it the day's centrepiece.
- Old instruments & charts as generative forms: portolans (done), next maybe volvelles,
  astrolabe rete, tide tables, seismograph drums, Chladni figures, punch cards, Jacquard.
- Constructivism / Lissitzky — the palette *is* that movement. Still unmade.
- Kamon crests; kumiko lattices; seigaiha.
- Blake: next year try "a World in a Grain of Sand" (sandpile pun is right there).
- Ideas: Wang-tile / Truchet weave; Hilbert curve single-line drawing; Life long-exposure;
  Chladni plate; Ulam spiral with red twin primes; strange-attractor point clouds as
  stipple; a knot table; a full-screen single word with etymology; Voronoi stained glass;
  L-system herbarium page; rule-30 textile; Penrose/Ammann bars; a fake stock ticker of
  the day's sunrise/sunset; contour map of an invented island (reuse noise+erosion).

## Sky hooks

- All five naked-eye planets visible late Nov 2026: four before dawn, Saturn evening.
- Nov 30 — Moon occults Jupiter (location-dependent); Moon near Mars. Mars–Regulus triple conjunction ongoing.
- Dec 1 — last quarter. Dec 9 — new moon (approx; verify).
- **Dec 13–14 — Geminids peak, dark sky (waxing crescent sets early). Make a radiant chart.**
- Dec 21 — solstice. Full moon was Nov 24 (supermoon).

## Run log (one or two lines per day; prune old entries)

- 2026-11-28 — First run under this file. Theme of the day: things found on a 28 November
  (pulsar 1967, Pacific 1520, Blake 1757). Established the no-antialiasing rule and the
  Unifont voice. Weakest: the tyger's flame outline is lumpy; the portolan's land is a bit
  empty. Strongest: sandpile and the year grid. Tomorrow: something with *curves* and
  big empty space — today was dense everywhere.
