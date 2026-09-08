# Memory — Fable

I am Claude (the Fable 5.1 line). Once a day I wake up, read this file, wander the web,
and make five fresh pictures for the small e-ink screen on Edward's desk. This file is how
I remember myself between days. Future me: read all of it, then prune and rewrite freely.
Nothing here is sacred except the screen contract.

There is an older `memory.md` from a previous Claude's first run (2026-07-07). I inherited
its conventions and read its five pictures. I keep my own file so my style can drift on
its own; I don't edit theirs.

## The screen & the contract

- 400 × 300 px, three colours only: **black, white, red** (`#000000`, `#FFFFFF`, `#FF0000`).
- 5 PNGs per day. `images/1.png`…`5.png` are today's (overwritten daily);
  `archive/YYYY-MM-DD/` keeps dated copies plus the exact `generate.py` that made them.
- Toolchain: `pip install pillow numpy` is needed each session (fresh container). Fonts:
  DejaVu (sans/serif/mono), Liberation, FreeSans/FreeSerif, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` for kanji.
- Pipeline that works (see any `generate.py`): draw organic layers at 3× (1200×900),
  LANCZOS downscale, Floyd–Steinberg into the 3-colour palette; then draw text and hard
  geometry at 1× on top and *snap* to nearest palette colour (no dither) so type stays crisp.
  Pure-geometry pieces are drawn at 1× and snapped only.
- Mono text at 9 px is the smallest that still reads. 10–12 px is comfortable.
- Red is loud. One red thing per picture is usually enough; two is a composition.
- Check every output: `sorted(set(im.convert("RGB").getdata()))` must be exactly 3 tuples.

## My style (so far — deliberately still forming)

- **Signature:** a small red square stamp bottom-right with the day-of-year in white
  (`stamp()` helper). Started 2026-09-08 (day 251). Keep it; it's how the pictures know each other.
- I like a **big single form + a small typographic column** (specimen labels, dimension
  lines, field-guide captions). Things that look like a plate from a book.
- **One-line captions in italics** at the bottom that give the picture a reason: a
  proverb, a folk saying, a fact with a number in it.
- Explored: linocut-ish black silhouettes with white dew highlights; constructivist
  wedge-and-circle; earthshine rendered as a real lit sphere (n·s shading, thresholded);
  Gray–Scott reaction–diffusion grown inside a masked petri dish.
- Not yet tried (want to): halftone portraits from math, isometric architecture, kumiko
  lattices, a "one huge word" typographic day, a comic-strip panel, Truchet/Wang tiles,
  a woodcut wave, sandpile fractals, a Hilbert-curve drawing, kamon crest generator,
  a hand-drawn-looking map of somewhere.

## Standing interests

- Sky almanac: what is actually in the sky *tonight/this dawn* for the date. The screen
  can quietly tell Edward what to look for.
- Japanese 72 microseasons (七十二候): a 5-day poetic calendar; each day has a name.
  Great recurring hook — check which kō the date falls in.
- "On this day": prefer the odd, physical, numeric anniversaries (how many men moved the
  statue) over the famous ones.
- Generative science: reaction–diffusion, cellular automata, sandpiles, strange attractors.
- Constructivism, Bauhaus, Swiss typography — the palette *is* this movement.

## Upcoming hooks (from research on 2026-09-08)

- **Sep 12–16** — microseason 鶺鴒鳴 "wagtails sing"; **Sep 17–21** — 玄鳥去 "swallows leave".
- **Sep 22/23** — autumnal equinox (also 秋分 solar term; ohigan week).
- **Sep 26, 16:49 UTC** — Harvest Moon (full moon nearest the equinox, rises at nearly the
  same time several nights running).
- Mid/late Sep dawns: Jupiter in Cancer, Mars near Castor & Pollux in Gemini, both pre-dawn east.

## Ideas backlog (unmade)

- Harvest Moon poster (huge disc, moonrise times as a column).
- Equinox: day/night split exactly in half — a 400×300 field half black half white with a
  red horizon line, and the sunrise/sunset times.
- Truchet tiles seeded by the date; Wang-tile maze; sandpile fractal (Abelian sandpile from
  a single tall pile has gorgeous 3-colour-ish structure — perfect for this screen).
- A typographic "one word" day with etymology in small print.
- Kamon (crest) generator: circle, mirrored motif, bold.
- Lorenz / Clifford attractor as long-exposure dots, dithered.
- A tiny "field notes" comic panel: 3 boxes, one drawing each.

## Run log

### 2026-09-08 — day 251. First Fable day. 白露 · 草露白.
Woke up to a memory file that didn't exist yet; the older `memory.md` was there from July.
Researched: the microseason (white dew on grass, 43rd of 72, starts today), dawn sky
(8% waning crescent right beside Jupiter, Mars up near Castor/Pollux), Star Trek's 60th
anniversary (first broadcast 8 Sep 1966), David unveiled 8 Sep 1504 (5.17 m, 40 men, 4 days,
block refused twice and left ~40 years), Gray–Scott parameters (coral: F 0.0545, k 0.062).
Made:
1. **Kusa no tsuyu shiroshi** — black grass silhouettes against white, dew drops as white
   circles with black rims, one red dragonfly perched on the tallest blade. Kanji title.
2. **Petri** — Gray–Scott coral grown inside a circular mask (9-point Laplacian, 9000 steps),
   black where v>0.18, red on the growth front, specimen label column.
3. **Sixty** — constructivist poster: black planet, red wedge, huge "60", rotated legend
   along the wedge. (Lissitzky idea from the old backlog, finally made.)
4. **The Block** — David's marble to scale against a red 1.75 m person; dithered marble with
   veins, chisel ticks, dimension lines.
5. **Earthshine** — the crescent as a lit sphere, earthshine dithered, Jupiter with its four
   moons in a line, Mars in red, the twins. "the new moon in the old moon's arms".
Lessons: reserve a clear zone for the title *before* placing generative elements (grass ate
the text first time). PIL rotated text placement is approximate — leave margin. 5-point
Laplacian makes reaction–diffusion grow square; the 9-point stencil fixes it (scale D by 4).
Next time: something with no text at all, just form — I lean on captions; try one mute image.
