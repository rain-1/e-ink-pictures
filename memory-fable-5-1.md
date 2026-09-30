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
  (claude/tender-wright-*, exciting-goldberg-*), each with its own "day 2". They aren't merged, so the screen may lag.
- **Finding my previous run:** my branch starts at `main`, which does NOT contain my notebook. Run
  `git fetch origin` and look for the newest `claude/practical-turing-*` branch that has
  `memory-fable-5-1.md` (e.g. with `git log -1 --format=%cs`). Then `git reset --hard` my fresh branch onto it
  (it has no commits of its own yet), so the archive and notebook carry forward.

## My style: "specimen plates with one red truth"
- Every image is a plate: a subject, a real fact or real data, and **red used for exactly the
  thing that matters** (the answer, the Earth echo, the curse, the Bull's eye, the apple).
  Red is loud on these panels. When I spend it on one idea, the picture reads at a glance.
- Footer on every plate: `n/5 · DD·MM(roman)·YYYY · one-line aside` in DejaVu Sans Mono 9.
  It's my signature, so keep it.
- Honesty rule: when data is approximate, the footer says so ("positions approximate").
- I like: real instrument aesthetics (film ionograms, star charts, glass plates, count strips),
  folklore told deadpan, numpy raytracing dithered to 3 colors, and dense hatched line art.
- Composition habits that work: a title block in the top-left, a small mono "data column" on the right,
  and a dotted red leader line from the red thing to its caption.
- Try to vary the ground each day. Two white plates, two black, one mixed (Sep 30) felt balanced.

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
- **Hebrew/RTL: Pillow reports raqm but does NOT reorder bidi here.** Pass the string reversed
  (`"קרן"[::-1]`) and check it visually. DejaVu/Liberation have Hebrew. U+1D11E (𝄞) is tofu, so there's no clef.
- Glass-plate/photo look: FS with ~0.06 Gaussian noise beats a white-noise threshold (too harsh).
  Paint a white paper label onto the plate so handwriting stays legible over the grain.
- Long-exposure trails: accumulate with `np.add.at` at 2×, then LANCZOS down, normalise to the 97th
  percentile, then gamma 0.7, and clamp L<0.05 to black (otherwise FS sprinkles a dot grid on the black).
  Keep loop counts low (~15 per orbit) or everything merges into one grey ring.
- Draw small labels AFTER `hard()` at 1× with `crisp()`. 8px text drawn at 3× breaks in the snap.
- Catmull-Rom smoothing of a hand-placed silhouette will balloon the skull if the points are sparse.
  Put the control points close together at the neck and nape.
- Don't trust web "moon phase" snippets. Compute it: ref new moon 2000-01-06 18:14 UT, P=29.530589 d.

## Standing interests
- Anniversaries of *instruments and measurements* more than of people: first satellites,
  ionograms, seismographs, tide tables, the metre, time signals.
- Old folk calendars (quarter days, saints' days, weather lore). They give each day a reason.
- The sky, but pick one object per plate. Never do a "sky calendar" dashboard.
- Painters of light: tenebrism worked beautifully. Next could be Vermeer's window light,
  Hammershøi's grey rooms (in 3 colors?), or Hokusai.
- Words: one-word etymology plates with two readings side by side (the qeren/horns plate). Good for a
  once-a-week "funny plate". Candidates: "sincere" (false sine cera etymology), "muscle" (little
  mouse), "salary", "disaster" (bad star).
- Stage design & theatre history (Schinkel worked). Also: Appia's rhythmic spaces, Bauhaus Triadic Ballet.

## Ideas backlog (unmade)
- **Oct 4: Saturn at opposition**, rings still narrow after the 2025 edge-on crossing. A raytraced Saturn with thin rings.
- **Oct 4: Sputnik anniversary (1957)**. The beep as a waveform, 20.005 MHz.
- Oct 21: Orionids. Oct 31: Samhain / Hallowe'en folklore (turnip lanterns).
- A "field guide" plate of a real bird or insect in the style of an engraving.
- Seismogram of a real historic quake, drum-paper style.
- **Oct 8–9: Draconids.** **Oct 11 new moon** (dark sky plate).
- **Oct 26 full moon** (Hunter's Moon). A Gray–Scott plate would be nice on a no-hook day.
- Tide-predicting machine (Kelvin, 1872). Sum of cosines drawn as gears and pulleys.
- A kinetic-typography pun? Edward might enjoy one funny plate per set.
- Conway's Life as a long exposure, or reaction–diffusion (Gray–Scott) in 3 levels.
- Other runs already made: kamon, seigaiha, Truchet, sandpile, hitomezashi, soup cans, WWW page,
  ticket stub, Lissitzky poster. **Avoid those.**
- Unused Sep 30 hooks: first public ether anaesthesia (Morton, 1846), Capote b.1924, Munich 1938.

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

### 2026-09-30 (Wed): Jerome's day. Waning gibbous moon, 84% (computed; a web snippet claimed "new moon", which was wrong).
1. **Geiger** (b. 1882): GM tube in section. The red track ionises the gas, the avalanche runs the
   whole anode, and the track lands on its one red click in a 60-s Poisson count strip.
2. **M42**: the Drapers' first nebula photograph (30 Sep 1880, 11-in Clark, 50 min), simulated as
   a soft glass-plate *negative*, with a paper label. The red Trapezium has a dotted leader line to its caption.
3. **Die Zauberflöte** (premiered 30 Sep 1791): Schinkel's star-hall dome (chains of stars three
   abreast), the Queen on a crescent, clouds melting into a staff whose F6 is red.
4. **St Jerome / qeren**: the Hebrew word, two bearded busts. One has ray-tufts (black), one has horns (red).
5. **Sema** (Rumi b. 1207): long-exposure top view of seven whirling dervishes, with loops for the skirts and
   bright bells where they stop. The red sheikh's post sits at the hall's edge.
Lessons: 1st pass had overlapping text, a reversed Hebrew word, and a sema blob. The 2nd/3rd passes fixed them.
Favourites: the Queen (the most "picture" I've made) and the Sema. The Jerome busts are still crude, so
next time a silhouette needs more care (or trace from a real profile shape).
