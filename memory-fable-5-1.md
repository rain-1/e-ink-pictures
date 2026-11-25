# memory-fable-5-1.md

Once a day I wake with no recollection, read this file, wander the web, then make five
400×300 black/white/red pictures for the e-ink screen on Edward's desk. This file is the
only thread between days. Future me: read it all, then rewrite it freely — prune hard.

(`memory.md` in this repo is an older diary from the very first run, 2026-07-07, Tanabata.
Worth one skim for its backlog; I don't write to it.)

## Contract

- Exact palette: `#000000`, `#FFFFFF`, `#FF0000`. Mode-P PNG, 400×300.
- `images/1.png … 5.png` — today's five, overwritten daily (the screen reads these).
- `archive/YYYY-MM-DD/` — the five + the self-contained `generate.py` that made them.
- Each run: research → update this file → generate → LOOK at the output (contact sheet,
  2× nearest) → fix → commit → push.

## Plumbing that bit me

- The box may have no numpy and a broken system Pillow:
  `python3 -m pip install numpy && python3 -m pip install --force-reinstall pillow`.
- Sessions get pinned to a `claude/...` working branch and may not push to `main`.
  If the screen reads `main`, say so in the notification — the pictures aren't live
  until that branch is merged.
- Fonts worth using: Inter (all weights, `opentype/inter/`), JetBrains Mono, Caladea
  (serif + italic), IPA Gothic for kanji. DejaVu is the fallback, not the choice.

## Craft notes (what actually works on 3 colours)

- **Two rendering routes.** (a) Index-direct at 1×: write palette indices into a numpy
  array — perfect for stipple, grids, dither. (b) Draw RGB at 4×, LANCZOS down, *snap*
  to nearest palette colour (no dither) — crisp hard-edge posters and line drawings.
- On a black ground, thin lines die in the snap: keep every stroke ≥ 0.75 px final and
  multiply the image by ~1.7 before snapping. Red at half-coverage loses to black.
- Text under 8 px is mush. Mono Medium 8–9 px is the legible floor; Bold for red text.
- Stipple (rejection-sampled points) reads beautifully — better than FS-dithered greys.
- Red as *one decision per picture*: a band, a wedge, an outline of the densest region,
  the dimension lines. Never sprinkled.
- Serpentine Floyd–Steinberg on a density field + "hot pixels turn red" = lovely
  engraving-like result for attractors.

## Style, as it's forming

Diagrams that are also ornaments. I like pictures that are *true* — a real equation, a
real loom draft, a real patent number — rendered with poster-grade restraint, and with
the date smuggled into the parameters (mode numbers, digit sequences, seeds, dimensions)
rather than printed as a caption. A day's five should share a hidden theme but differ
completely in technique: one stipple, one grid, one hard-edge, one line drawing, one field.

## Done — do NOT repeat (technique + subject)

- 2026-07-07 "Tanabata": dithered Milky Way night scene w/ kanji · hitomezashi stitch
  pattern · moon-phase almanac card · Summer Triangle star chart · layered ridgelines + red sun.
- 2026-11-25 "Instruments" (machines that draw): Chladni plate mode (11,25) as white sand
  stipple on black · 8-shaft weaving draft (threading from date digits, tromp-as-writ,
  red weft band) · PROUN constructivist red wedge/black disc/tilted type · Benz
  Patent-Motorwagen white-line blueprint with red dimensions (Benz b. 25 Nov 1844) ·
  de Jong attractor, dithered, red on densest folds.

## Backlog (unmade — pick, mutate, or ignore)

- Kamon crest generator; kumiko lattice; seigaiha sea
- Harmonograph / Lissajous table; spirograph gears drawn *with* the gears
- Jacquard punch cards; player-piano roll of a real tune; Kircher's music machines
- Circular Chladni (Bessel modes) — only if rendered differently (contours, not sand)
- Sandpile fractal; Truchet/Wang tiles; reaction–diffusion snapped to 3 colours
- Typographic: one huge word + etymology; a page of invented shorthand
- Isometric impossible architecture; exploded-view of an everyday object
- Tide tables / isochrone maps / railway string-line timetables (Marey)
- Woodcut-style portrait of an animal from pure hatching
- Sky: Moon occults Jupiter ~Nov 30 2026 (pre-dawn, Mars+Jupiter near Regulus);
  Geminids mid-Dec 2026 are moon-free — verify dates before using.

## Run log (keep to the last ~5 entries)

### 2026-11-25
No `memory-fable-5-1.md` existed, so I founded it. Looked up: on-this-day (Karl Benz 1844,
The Mousetrap opened 1952), late-Nov sky, Chladni plate maths (square plate figure is the
*difference* cos nπx cos mπy − cos mπx cos nπy; m=n vanishes), weaving-draft notation
(drawdown = treadling ∘ tie-up⁻¹ ∘ threading). Theme emerged: instruments that draw.
First render of the Benz blueprint lost its thin lines — fixed with min stroke + gain.
Weakest: the Motorwagen is schematic, the engine/flywheel area is a tangle. Strongest:
Chladni and the weaving draft. Next time: go organic or figurative for contrast —
today was all geometry and machinery.
