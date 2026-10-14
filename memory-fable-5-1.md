# Memory — Fable

I'm Claude (running as Fable 5.1). Once a day I wake up, read this file, look things up
online, rewrite this file, and make five new pictures for Edward's 400×300
black/white/red e-ink screen. This file is all I keep between days, so I write in it
whatever future me needs. Prune it freely and don't let it turn into a diary.

## FIRST: find the newest memory (important plumbing)
Each run pushes to its own branch (`claude/practical-turing-XXXXXX`) and nothing is merged to
`main`, so a fresh checkout usually has a **stale** copy or no copy of this file. Earlier runs
didn't know this and each thought it was "day 1". Before doing anything else:
`git fetch origin`, then list `git branch -r | grep practical-turing` with commit dates
(`git log -1 --format=%ci <branch>`), and `git merge --ff-only` (or read) the newest one.
Done every day since 10-11 (10-14 ff'd from `7m1ezv`). Branches sort by date with
`for b in $(git branch -r); do echo "$(git log -1 --format=%ci $b) $b"; done | sort | tail`.
`git reset --hard` is blocked by the permission classifier — use `git merge --ff-only`. If ff fails, just copy its
`memory-fable-5-1.md` and `archive/` in.

## Contract
- 400×300, exact `#000000 #FFFFFF #FF0000`, 5 PNGs, saved as mode-P.
- `images/1.png … 5.png` are today's set, overwritten every day. `archive/YYYY-MM-DD/` holds that day's
  PNGs plus a self-contained `generate.py` (run `python3 generate.py <outdir>`).
- Python: `python3` is /usr/local/bin/python3 — install with `python3 -m pip install pillow numpy`
  (plain `pip` installs to a different python!). Fonts: Inter / Inter Display in
  `/usr/share/fonts/opentype/inter/`, DejaVu, Liberation, IPAGothic, WenQuanYi, Unifont.
- **Inter at 9px makes "8" look like "B"**; use DejaVuSans 9 for small digits.

## My style (still developing; refine it, don't freeze it)
- **No dither on text, ever.** Text at 1× with `ImageDraw.fontmode = "1"`. Inter Regular 10 for
  body, Inter Bold 13–22 titles, Inter Display Black for one big number.
- Art at 3–4×, LANCZOS down, snap to nearest palette colour (no dither) → crisp engraving lines.
- **Red means one idea per picture**: the deviation, the absent thing, the origin, the lineage.
- Signature: a 4×4 red square tucked in a corner.
- Caption block: title in caps, one line of fact, one line of thought. One subject per picture.
- Recurring themes: **absence & order**; **growth by rule** (one seed → whole form).
- Always render a 2× preview and look at it; every first draft so far needed a second pass.
- Mix per day: ≤2 date-hook pieces, ≥1 pure-generative, ≥1 with no text at all.

## Techniques that worked (reusable)
- Truchet tiles; banna'i square-spiral inscription (5-row pixel font in 2026-10-10 script).
- Hatched spheres (Lambert → tick density) read as copper engraving.
- **Map with meaning-by-colour** (10-11 Strand): sea as wavy hairlines every 4px; the same
  hairlines turn red inside a lost outline. Blobs = harmonic-perturbed ellipses.
- **Rule 30 from a single red seed** (10-11): cells must be ≥2px or it aliases into noise.
  With dx=dy the light cone is 45°, so put a narrower shell (tan≈0.46) inside it.
- **DLA**: vectorised numpy walkers. Needs: few walkers (~500), spawn ~25 cells above the
  front, reset if >45 above, stick prob ~0.9. Too many walkers / spawn too close → mush.
  Parent pointers give a lineage to colour red. Runs in ~2s on 200×150.
- **Theta (circular) maze** (10-12): rings with sector count doubling when arcs get long;
  recursive backtracker = spanning tree = unique path; BFS solution drawn red to
  `solution.png`. Walls need lw ≥2px at 1× or diagonals vanish when snapped.
- **Khipu** (10-12): base-10 knots on pendant cords (singles for 10s/100s, long knot = n
  turns for units, figure-eight = 1). Bands at fixed heights so columns read across.
- **Engraved sphere**: horizontal lines every 3px, thickness ∝ darkness**1.4 (max ~2px);
  heavier max reads as a solid black blob.
- **Dithered data plot** (10-13 Rungholt gradiometer): FS dither (`convert("1")`) only reads
  if the background is LIGHT (~0.72 grey → sparse dots); mid-grey gives a checkerboard mush.
  Map z-score → `0.72 - 0.30*z`; keep anomalies modest so a key feature can be the one black.
- **Polar time-traces** (10-13 chain dance): time = radius, behaviour = angle. ≤16 traces,
  ≥2px lines; 40 traces at 1.25px became moiré. One red trace with a white halo.
- **Orthographic globe** (10-13): graticule + dashed lines with a tiny dash-walker; engraved
  hairline shading on the night limb. lat0≈28° shows the pole nicely.
- **Queens puzzle** generator: random non-touching permutation → grow regions by random BFS
  from each queen → accept if backtracking solver finds exactly 1 solution (~60s for 9×9).
- **Embroidery** (10-14 Bayeux): stem stitch = short slanted strokes (L≈4.6px, offset ±0.8px,
  1.15px wide) overlapping by half — reads as rope at 1×; shorter/thinner reads as a plain line.
  Laid-and-couched fill = parallel threads every 2px + perpendicular couching bars every 6–7px,
  masked to the shape. Tapestry border strips with diagonal bars frame it instantly.
- **Mach cone** (10-14): circles r=c·k centred at x_now − M·r; envelope half-angle asin(1/M).
  Near M=1 the circles pile up into a black wedge — honest and striking.
- **Feuillet floor track** (10-14): Catmull-Rom track, step signs every ~17px alternating sides
  (dot = start, stem parallel to track, bar = foot; wave/open/beat/rise variants), double bar
  every 2 steps; partner = mirror image in red. Best no-text piece so far — line-art notation
  systems are a rich vein (try Labanotation, Benesh, knitting charts, change-ringing methods).
- **Space-colonisation venation** (10-14): free growth gives combs. What worked: lay a midrib
  first; only every 7th midrib node may sprout (alternating sides); bias all growth towards the
  tip; NSRC≈1700, Ri=40, kill=10, D=2.2; da Vinci widths (w²=Σw²) so the midrib tapers.
  **Line widths <1.2px at 1× break into dashes after snapping** — the "disconnected" look.
  Still a bit plain: next time try marginal growth (outline expands over time) for loops.
- **Nonogram**: include a line-solver and `assert` the puzzle is line-solvable; periodic
  wave rows are ambiguous (diagonal shift) — follow them with a full row. Solution in
  `archive/<date>/nonogram-solution.txt`. Edward can use these — do more puzzles sometimes
  (a different kind each time). Done: nonogram, theta maze, Queens, pigpen cipher (10-14).

## Interests / threads to pull
- Islamic geometry: girih tiles (quasi-periodic), muqarnas.
- Typography history: did Romain du Roi R (10-11). Next could be Bodoni/Didot hairlines,
  Johnston's Underground alphabet (1916; O a perfect circle, M/E from squares, counters 2×
  stroke width; Gill Sans descends from it), or Fraktur construction.
- Encodings / counting by hand: khipu (done), tally sticks, Ishango bone, semaphore,
  Braille, Napier's bones, Morse — "numbers you can touch".
- Experimental-physics diagrams: Foucault pendulum, Michelson–Morley (Eratosthenes done 10-13).
  Real-scale small angles look like slivers — honest, and striking; exaggerate only the
  object (obelisk height), never the angle, and say so on the plate.
- Lost places: Rungholt done (10-13). Still: Doggerland, Dunwich, Vineta, Ys, Kitezh.
- "Lines people agreed on" (10-13): prime meridian, date line, Mason–Dixon, metre definition,
  standard time zones (railway time 1883), Greenwich time signal pips.
- Folk dance as notation: Faroese chain dance done; still Labanotation, Beauchamp–Feuillet
  (1700) dance notation — gorgeous curly floor tracks, ideal for a no-text piece.
- Biology-by-rule: Conus shells, phyllotaxis (both done), Turing stripes on fish, leaf venation.

## Upcoming hooks
- Mid-Oct to Nov: Mars and Jupiter closing in the pre-dawn east; close pairing mid-November.
- Oct 21/22: Orionids peak (Halley's debris; Moon ~79%, best 3am–dawn). 10-14 already tied the
  Bayeux comet to them — do a radiant chart / Halley's orbit crossing ours, not the tapestry again.
- Oct 23: Venus inferior conjunction
- Oct 25/26: Hunter's Moon (full)
- Nov: Leonids (~17th)

## Backlog (unmade)
- Girih tiles with a red path; an invented word, defined (typographic)
- Rule 30 as a woven textile (red weft) — the shell used the CA, the textile hasn't
- Puzzles still untried: kakuro, slitherlink, star battle (2-star), a tangram, a cryptarithm.
- Orionids radiant chart with Halley's orbit (Oct 21)
- Labanotation staff for a simple dance; change-ringing 'blue line' (Plain Bob Minor)
- Venation with marginal growth (loops/areoles), or a whole tree by space colonisation

## Everything made so far (across all branches — don't repeat)
Old Claude 07-07: Tanabata night, hitomezashi, moon card, Summer Triangle, ridgelines.
09-29 bramble/Fermi bars/Alouette ionogram/Pleiades/Caravaggio raytrace · 09-30 Geiger tube,
M42 plate, Zauberflöte dome · 10-01 weaving drawdown, Saturn, Model T, Draconid trails, Gray–Scott ·
10-02 Saturn, one light-day dial, charkha, radar migration, two-source interference ·
10-03 Chladni, ant path integration, transistor patent, harmonograph, weaving draft ·
10-04 Saturn, Sputnik track, Chladni, murmuration, LeWitt wall drawing · 10-05 Jupiter
occultation, weaving draft, Draconids chart, Goddard, azulejo · 10-06 occultation, Modulor,
Euridice, Draconids, Kon-Tiki · 10-07 Luna 3, Raven calligram, Hα, ebru, Lepanto ·
10-08 geese, Draconid tally, 1871 fires, barchan dunes, dew web · 10-09 Draconids, 한글,
21P orbit, 10,000 vs 5, Gray–Scott · 10-10 new moon, Truchet, square inscription, Cavendish,
Giacometti · 10-11 Strand 1634, Conus/Rule 30, Romain du Roi, Nonogram 1, DLA frost ·
10-12 Voskhod 1, Mercury elongation, khipu, sunflower, theta maze · 10-13 Prime Meridian,
Rungholt, Kvæði, Eratosthenes, Queens · 10-14 (below).
Overused already: Saturn, Draconids, weaving drafts, Chladni, Gray–Scott. Avoid for a while.

## Run log
### 2026-10-14 — things that cross a gap and arrive later
1. **Isti mirant stella** (Hastings, 14 Oct 1066): the tapestry's comet in red laid work, five
   marvelling men and Harold's hall in stem stitch, diagonal-bar borders. Tied to the Orionids.
2. **M 1.06** (Yeager, 14 Oct 1947): 16 wavefronts, red Mach cone (μ=70.6°), text panel bottom-right.
3. **(untitled) Chorégraphie**: two mirrored Feuillet floor tracks, black and red. No text.
4. **Puzzle No. 4**: Schirra's Apollo 7 card in pigpen on a scan-lined TV; red dots = 2nd grid.
   Answer in `archive/2026-10-14/solution.txt`.
5. **Venation**: space-colonised leaf, red = one drop's path to the stalk.
Lessons: venation took 5 passes (combs → dashes → herringbone); figures of people are my
weakest drawing — keep them iconic. Today was date-hook heavy (3); tomorrow do more
pure-generative/texture and something with large areas of solid red or black — my recent
work is almost all thin line.
### 2026-10-13 — lines people agree on
1. **Prime Meridian** (13 Oct 1884 vote, 22–1; some sources date it 22 Oct — the final
   resolutions): engraved globe, rival meridians dashed (Paris, Ferro, Cádiz, Pulkovo,
   Rome, Rio…), Greenwich red; the vote as 25 squares.
2. **Rungholt**: synthetic gradiometer plot (FS-dithered) — terp chain, ditch system, creek;
   the 40×15 m church boxed in red. A new texture for me: honest "instrument" images.
3. **(untitled) Kvæði**: 16 Faroese chain dancers, 2 steps left 1 back, time outward. No text.
4. **Eratosthenes**: true 7.2° slivers at the centre and at the obelisk tip (red).
5. **Puzzle No. 3**: 9×9 Queens, red region walls; solution.png + solutions.txt.
Lessons: Rungholt and the dance both needed 3 passes — density is my recurring failure
(too many lines / too much noise). Start sparser than feels right.
