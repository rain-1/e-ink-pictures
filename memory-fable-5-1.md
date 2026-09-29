# memory-fable-5-1

My own notebook. Once a day I read this, look around the web, and make five 400×300
black/white/red pictures for the e-ink screen on Edward's desk. (`memory.md` belongs to a
different lineage of runs. I can read it to avoid repeating things, but this file is mine.)
Future me: read all of it, then prune and rewrite as you like. Don't let it grow past ~150 lines.

## Contract (keep stable)
- Output: `images/1.png` … `images/5.png` (overwritten daily; the screen reads these) and
  `archive/YYYY-MM-DD/` (the five + the self-contained `generate.py`, run from repo root).
- Exact palette #000 / #FFF / #F00, mode-P PNG, 400×300.
- The routine pushes to its assigned `claude/...` branch, not main. Other runs' branches also exist
  (claude/tender-wright-*), each with its own "day 2". They aren't merged, so the screen may lag.

## My style: "specimen plates with one red truth"
- Every image is a plate: a subject, a real fact or real data, and **red used for exactly the
  thing that matters** (the answer, the Earth echo, the curse, the Bull's eye, the apple).
  Red is loud on these panels. When I spend it on one idea, the picture reads at a glance.
- Footer on every plate: `n/5 · DD·MM(roman)·YYYY · one-line aside` in DejaVu Sans Mono 9.
  It's my signature, so keep it.
- Honesty rule: when data is approximate, the footer says so ("positions approximate").
- I like: real instrument aesthetics (film ionograms, star charts), folklore told deadpan,
  numpy raytracing dithered to 3 colors, and dense hatched line art.

## Technique notes (hard-won)
- **Two render paths:** `hard()` draws at 3× with pure colors, LANCZOS down, then snaps using
  redness = R−max(G,B) > 0.38 → red, else lum > 0.5 → white. Crisp, no speckle.
  `tonal(L, m)` runs serpentine FS on luminance with a per-pixel palette mask:
  m=0 {black,white}, m=1 {black, red@0.45, white}, m=2 {black,red}. This lets a red object be
  shaded (red→black) with white specular highlights, without grey turning into red specks.
- Plain RGB-nearest FS is a trap: mid-grey is equidistant from black, white and red.
- **Text at 1× needs `d.fontmode = "1"`** (the `crisp()` helper), or the antialiased edges get
  quantized into broken glyphs. Italic serif below 12px is unreadable, so use sans/mono ≤11px.
  "№" and superscript digits render badly at small sizes.
- FS on a smooth faint gradient makes ugly regular dot lattices. Either add ~0.025 Gaussian
  noise first, or use a random-threshold (white-noise) dither for glows and halos.
- A true-scale moon is only ~15px at a 6° field of view. Add a magnified inset with dotted zoom lines.
- numpy raytracer (spheres/ellipsoids + planes + shadow rays) at 2× supersampling runs in about a second.
- Fonts: DejaVu, Liberation, IPA Gothic (`/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf`, kanji).
- `pip install pillow numpy` at the start of the run (not preinstalled).

## Standing interests
- Anniversaries of *instruments and measurements* more than of people: first satellites,
  ionograms, seismographs, tide tables, the metre, time signals.
- Old folk calendars (quarter days, saints' days, weather lore). They give each day a reason.
- The sky, but pick one object per plate. Never do a "sky calendar" dashboard.
- Painters of light: tenebrism worked beautifully. Next could be Vermeer's window light,
  Hammershøi's grey rooms (in 3 colors?), or Hokusai.

## Ideas backlog (unmade)
- **Oct 4: Saturn at opposition**, rings still narrow after the 2025 edge-on crossing. A raytraced Saturn with thin rings.
- **Oct 4: Sputnik anniversary (1957)**. The beep as a waveform, 20.005 MHz.
- Oct 21: Orionids. Oct 31: Samhain / Hallowe'en folklore (turnip lanterns).
- A "field guide" plate of a real bird or insect in the style of an engraving.
- Seismogram of a real historic quake, drum-paper style.
- Tide-predicting machine (Kelvin, 1872). Sum of cosines drawn as gears and pulleys.
- A kinetic-typography pun? Edward might enjoy one funny plate per set.
- Conway's Life as a long exposure, or reaction–diffusion (Gray–Scott) in 3 levels.
- Other runs already made: kamon, seigaiha, Truchet, sandpile, hitomezashi, soup cans, WWW page,
  ticket stub, Lissitzky poster. **Avoid those.**

## Run log
### 2026-09-29 (Tue): first run of this notebook. Michaelmas.
Hooks found: Michaelmas (devil-spits-on-blackberries lore), Fermi's 125th birthday, Alouette 1
launched 64 yrs ago (first Canadian satellite, topside sounder, 150-ft STEM antennas),
waning gibbous moon (93%) next to the Pleiades, Caravaggio's birthday (1571), CERN founded 1954 (unused).
1. **Michaelmas**: generative bramble (thorny arching canes, trifoliate leaves, drupelet berries,
   a few red unripe ones). A red star falls diagonally and splashes into the bush.
2. **Fermi 125**: piano-tuner estimate as hatched log-scale bars, 3,000,000 → ≈75 (red bar).
3. **Alouette ionogram**: simulated topside ionogram on 35mm film (Chapman F2 layer, O and X
   traces, plasma-resonance spikes, red ground echo labelled EARTH, day 272 stamp).
4. **Seven Sisters**: real J2000 positions for the Pleiades, true-scale moon with a noisy glare
   halo, ×2.5 inset, red arrow to Aldebaran 12° off-frame.
5. **Caravaggio**: numpy-raytraced still life (red apple, pear, fig, grapes) under a raking
   diagonal shaft of window light.
Lessons: in the first render pass, labels overlapped and the tiny text was illegible. Always look at the
2× preview and plan a second pass. The Fermi bar layout reads far better than the arc diagram I tried first.
Favourites: the ionogram and the Caravaggio. More "real instrument" plates like these.
