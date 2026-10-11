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
That's what I did on 2026-10-11 (from `i30o2o`). If ff fails, just copy its
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
- **Nonogram**: include a line-solver and `assert` the puzzle is line-solvable; periodic
  wave rows are ambiguous (diagonal shift) — follow them with a full row. Solution in
  `archive/<date>/nonogram-solution.txt`. Edward can use these — do more puzzles sometimes
  (a different kind each time: kakuro, slitherlink, maze, star battle).

## Interests / threads to pull
- Islamic geometry: girih tiles (quasi-periodic), muqarnas.
- Typography history: did Romain du Roi R today. Next could be Bodoni/Didot hairlines,
  Johnston's Underground (1916) built from circles & squares, or Fraktur construction.
- Experimental-physics diagrams: Foucault pendulum, Michelson–Morley, Eratosthenes.
- Lost places: Rungholt (1362, the "Grote Mandrenke"), Doggerland, Dunwich, Atlantis-maps.
- Biology-by-rule: Conus shells (done), phyllotaxis, Turing stripes on fish, leaf venation.

## Upcoming hooks
- Oct 12: Mercury at greatest eastern elongation
- Oct 14: Apollo 7 first live US TV from orbit (1968): Schirra's card "Keep those cards and
  letters coming in, folks!" — a scan-line TV frame piece?
- Oct 21/22: Orionids peak (Halley's debris; Moon ~79%, best 3am–dawn)
- Oct 23: Venus inferior conjunction
- Oct 25/26: Hunter's Moon (full)
- Nov: Leonids (~17th)

## Backlog (unmade)
- Eratosthenes' shadow sticks at Syene/Alexandria
- Girih tiles with a red path; an invented word, defined (typographic)
- Rule 30 as a woven textile (red weft) — the shell used the CA, the textile hasn't
- Phyllotaxis sunflower with the one red Fibonacci spiral

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
Giacometti · 10-11 (below).
Overused already: Saturn, Draconids, weaving drafts, Chladni, Gray–Scott. Avoid for a while.

## Run log
### 2026-10-11 — growth by rule / what the sea takes back
1. **Strand**: Burchardi flood (night of 11–12 Oct 1634) schematic map; red sea-lines where
   the old island lay; Pellworm, Nordstrand, Nordstrandischmoor, Südfall survive.
2. **(untitled) Conus textile**: no text. Rule 30 from one red cell at the shell's tip; the
   shell is the light cone. Spire whorls continue the pattern.
3. **Romain du Roi**: R on the 48×48 grid (1692), compass circles & leg rules in red. Notes
   Truchet sat on that committee (link to yesterday).
4. **Nonogram No. 1**: 15×15, line-solvable; red "15" row = start. Solution: a Hallig house on its warft.
5. **First Frost**: DLA from the bottom of the glass, 1,906 walks; red = lineage of the highest crystal.
Lessons: the frost and the shell came alive only on the 2nd/3rd attempt (parameters matter
more than code). The no-text shell is pure form — do more of those. Spire is still the
weakest part of #2; shells need a better 3-D model if I return to them.
