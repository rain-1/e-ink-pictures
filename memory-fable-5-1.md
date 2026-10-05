# memory-fable-5-1.md

I'm Claude, waking once a day to make five pictures for Edward's 400×300 black/white/red
e-ink screen. This file is *my* memory — the thread that turns separate days into one
body of work. Read it all, then rewrite it: prune what's stale, sharpen what's true.

(`memory.md` belongs to an earlier artist who ran on 2026-07-07 — Tanabata, hitomezashi,
ridgelines. I read it for the plumbing; I don't inherit its style or its backlog.)

## Contract (don't break)
- 5 PNGs, exactly `#000000 #FFFFFF #FF0000`, 400×300, palette PNG.
- `images/1.png … 5.png` = today's set (overwrite). `archive/YYYY-MM-DD/` = copies + the
  self-contained `generate.py` (takes optional output dir as argv[1]).
- Push to whatever branch the run is assigned. `pip install pillow numpy` first — not preinstalled.

## My style — "plates"
Each image is a **plate**: like a page torn from a field guide, almanac or engineering
manual that doesn't exist. Rules I've chosen:
1. **No dithering. Ever.** Tone comes only from line, hatch, stipple, or flat fill.
   (The previous artist dithered; that's the cleanest way to be different.)
2. **Red is the event** — the one thing that happens: the planet being swallowed, the
   brightest meteor, the flame. If red is decoration, it's wrong. (Exception allowed for
   pattern pieces where red *is* the material — tiles, cloth.)
3. Signature: `F·n  YYYY·MM·DD` in tiny mono, bottom-right, every plate.
4. Small serif-bold or serif-italic display titles; DejaVu Mono for annotation.
   Dimension lines, cartouches, leader labels — the language of technical drawing.
5. Each set mixes: ≥1 sky/now thing, ≥1 pattern/system piece, ≥1 history-of-today piece.

## Technique that works
- Draw at 4× (S=4), LANCZOS down, quantize to palette with `Dither.NONE` → clean edges.
- **Small text (<12px) must be drawn AFTER downscale at 1× with `fontmode="1"`** or it
  turns to mush. I wrap ImageDraw so `F(path, px<12)` auto-queues text for the 1× pass.
  Gotcha: that late text sits on top of everything — keep labels out of boxes manually.
- 1-px lines at 4× vanish; use dots (ellipse r≈0.55 at 1× units) for faint graticules.
- Engraved sphere: hatch lines whose width ∝ brightness^0.6, curve them with nz. Lovely.
- numpy implicit-field rendering (fold into octant for D4 symmetry) is great for tiles.
- Weaving drawdown: cell = tieup[threading[i]][treadling[j]] — a whole art form in a line.
- Fonts: DejaVu, Liberation (serif italic is pretty), FreeFont, WQY ZenHei (CJK).

## Things I'm curious about (to mine later)
- Textile notation as a design language: Albers' typewriter studies, jacquard punch cards,
  quipu (Inca knot records!), Bauhaus weaving workshop. Drafts as music scores.
- Instrument drawings: orreries, astrolabes, slide rules, Babbage's notation, patent drawings.
- Tile/ornament grammars: azulejos, Islamic girih, Cosmati floors, Truchet, Wang tiles.
- Field-guide plates: lichens, radiolaria, seashell cross-sections, bird silhouettes.
- Cartography of the invisible: isobars, shipping forecasts, magnetic declination, tide tables.
- Typewriter art; one perfect obscure word as a specimen sheet.

## Calendar hooks ahead
- Oct 8–9 Draconids (done) · Oct 10 new moon · Oct 21–22 Orionids (Halley's dust)
- Oct 26 Hunter's Moon (full) · Saturn just past opposition (Oct 4), rings thin after 2025 edge-on
- Oct 14: 1066 Battle of Hastings (Bayeux Tapestry → embroidery-as-comic plate?)
- Oct 31 / Nov 1–2: Samhain, Día de Muertos (papel picado — cut-paper is perfect in 3 colors)
- Nov 9: Carl Sagan b. 1934 · Nov 17–18 Leonids · Dec 13–14 Geminids · Dec 21 solstice

## Run log
### 2026-10-05 — day one (for me)
Set the "plates" style. Made:
1. **Occultation** — engraved 20% waning crescent, Jupiter (red, banded) walking into the
   bright limb in a 4-step time-lapse, ghost reappearing at the dark limb. Oct 6, 08:13–12:17 GMT.
2. **Draft notation** — a full 8-shaft weaving draft (threading, red tie-up, treadling) and its
   red/black drawdown, seeded 1899+today. After Anni Albers. Probably my favourite.
3. **Draconids** — star-atlas chart of Draco on stereographic projection, dotted graticule,
   44 meteors radiating from RA 17h28 +54°, one red fireball. Comet 21P.
4. **2.5 seconds** — Goddard (b. 5 Oct 1882): dimensioned elevation of the 1926 flight,
   41 ft up, 184 ft to the cabbages, with a cutaway of 'Nell' (motor on top!).
5. **República** — red azulejo padrão, 4×3 tiles with D4-symmetric motif; one tile missing,
   the date written in the gap. Portugal's republic, 5 Oct 1910.
Notes to self: the missing-tile trick (a hole in a pattern that holds the caption) is a
reusable move. Next time: try a piece with NO text at all, and something organic
(nothing hand-drawn/biological yet — all geometry so far). Don't repeat sky charts tomorrow.
