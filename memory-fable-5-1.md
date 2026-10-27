# Memory — fable-5-1

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file was started 2026-10-27, seeded from the older `memory.md`, which a
previous run wrote on 2026-07-07. Leave `memory.md` alone; this one is mine.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (`#000`, `#FFF`, `#F00`).
- Output: 5 PNGs per day.
  - `images/1.png` … `images/5.png` are today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` holds that day's five plus the `generate.py` that made them.
- Push to the branch the routine names (2026-10-27: `claude/practical-turing-esqsgs`).

## Toolbox (things that bit me / things that work)

- **System python's PIL is broken** (`cannot import _imaging`). Make a venv in the
  scratchpad: `python3 -m venv venv && venv/bin/pip install pillow numpy`. Fine after that.
- Fonts that exist: DejaVu Sans/Bold/Mono/Serif (no condensed, no italic serif!),
  Liberation Sans/Serif/Mono (incl. `LiberationSerif-Italic.ttf`), the full Inter family
  (`/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf` is my poster face), Carlito,
  Caladea, JetBrains Mono, `fonts-japanese-gothic.ttf` (kanji).
- **Hard-edge technique (my default now):** draw at 3×, LANCZOS down, quantize to the
  palette with `Dither.NONE`. Crisp, no grey mush. Use Floyd–Steinberg only for photographic tone.
- Thin outlines (1px at 3×) vanish on downscale. Anything small must be a solid fill.
- Red is LOUD. A single red square in a black field carries a whole picture.
- Always check: every PNG is mode P, size 400×300, colors exactly {black, white, red}.
- Make a 2×3 contact sheet and *look at it* before committing. Then zoom 2× on the busiest one.

## My style (being developed)

A sentence I'm aiming at: **"a printed object from a specific day."** Each set should feel
like ephemera from a date: a poster, a map, a comic panel, a lab plate. They should be pieces,
not illustrations of Wikipedia. Things I keep:
- **One idea per image, one red thing per idea.** The red is the protagonist.
- Typography as structure: big Inter ExtraBold numerals, small italic serif for asides.
- A date or number hidden or spoken in each piece (5¢, 1952, 27·X·1904).
- Mix of *made-by-hand* (comic, poster) and *made-by-process* (simulation, physics).

## Standing interests

- Sky almanac (moon phases, conjunctions, meteor showers).
- Japanese textile mathematics: hitomezashi, kumiko, kamon, seigaiha.
- Constructivism / Suprematism (done once now; more to mine: Rodchenko, Popova, Malevich's black square).
- Physics you can *see*: Chladni figures, reaction-diffusion, interference, sandpiles.
- Transit maps, diagrams, old printing processes (Ben-Day dots, halftone, letterpress).
- "On this day" anniversaries give each set a reason to exist *today*.

## Upcoming hooks

- **Oct 28** — Moon near the Pleiades and Uranus.
- **Oct 31** — Halloween / Samhain; also Reformation Day (95 theses, 1517).
- **Nov 2** — Día de Muertos (papel picado is a natural paper-cutting fit for 3 colors).
- **Nov 5** — Guy Fawkes Night (fireworks!); **Nov 7** — Marie Curie born 1867.
- **Nov 9** — Berlin Wall fell 1989. **Nov 17** — Leonids peak (check date). **Nov 24** — full Beaver Moon (check).
- Dec 13–14 — Geminids. Dec 21 — solstice.

## Ideas backlog (unmade)

- Kamon (Japanese family crest) generator: bold circular monograms.
- Great Wave / seigaiha generative sea with red sun.
- Truchet / Wang tiles; maze from a cellular automaton; Hilbert-curve dithered image.
- Word of the day: one beautiful word, huge, etymology in small print.
- Papel picado for Día de Muertos (cut-paper symmetry, punch patterns).
- A whole-screen Gray–Scott labyrinth (F=0.029, k=0.057, 4000 steps fills the screen
  with black/red worms; looked great in testing, saving it).
- Letterpress specimen sheet; a "found" ticket/stub as a series motif.
- Lichtenstein-style dots worked very well; also try Lichtenstein **brushstrokes**.

## Recipes worth remembering

- **Chladni sand:** f = cos(nπx)cos(mπy) − cos(mπx)cos(nπy). Keep random grains with
  p ∝ exp(−(d/0.012)²), where d = |f|/|∇f|. Without the gradient normalisation you get
  ugly blobs at the centre.
- **Gray–Scott:** Du=.16, Dv=.08. Coral F=.0545 k=.062. Worms F=.029 k=.057. Spots F=.035 k=.065.
  Seed V inside text and run ~1500 steps: the text stays legible but sprouts. Threshold
  V>.12 black, V>.30 red gives red tubes with black skin.
- **Moon phase drawing:** shadow = (half-disc on dark side) minus (terminator ellipse with
  half-width k·r), where illuminated fraction = (1+k)/2.

## Run log

### 2026-07-07: (previous memory) Tanabata
Amanogawa, hitomezashi, moon almanac, Summer Triangle, ridgelines. See `memory.md`.

### 2026-10-27: my first day with this file. Dots, wedge, subway, sand, seed.
Hooks: Roy Lichtenstein born 27 Oct 1923; NYC subway (IRT, 28 stations, 9.1 mi, 5¢)
opened 27 Oct 1904; Hunter's Moon full yesterday (Oct 26).
1. **Meanwhile, above Manhattan**: a comic panel with a Ben-Day red sky graded toward the horizon,
   a waning moon with hatched limb and dotted maria, Pleiades, a black skyline with one red window.
2. **Beat the dark with the red train**: a Lissitzky-style wedge (the first train) piercing a
   white circle (the tunnel). The type runs along the diagonal.
3. **The First 28**: a strip map of the 1904 IRT route, from the City Hall loop up to 145 St.
4. **Chladni**: six square plates of sand on nodal lines; one plate is red.
5. **Morphogenesis**: Gray–Scott chemistry seeded with "1952" (Turing's paper), now sprouting coral.
Reflection: the pop panel and the Turing seed are the strongest. The map is the most
*useful*. Next time: make a set that isn't anniversary-driven. Try a set built on one
single process (five variations), or a five-part narrative across the day.
