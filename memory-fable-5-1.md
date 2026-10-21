# Memory (fable-5-1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make five
fresh pictures for the small e-ink screen on Edward's desk. This file is how I remember
myself between days. Future me: read all of it, then prune and rewrite freely.
(`memory.md` is an older notebook from the first run, 2026-07-07. This file supersedes it.)

## FIRST: plumbing (read before anything else)

- **Each run gets a fresh branch cut from `main`, and `main` is stale (July).** So the checkout
  you wake up in does NOT have yesterday's memory. Do this first:
  `git fetch origin` then
  `for b in $(git branch -r | grep claude/); do echo "$(git log -1 --format=%ci $b) $b"; done | sort | tail -3`
  and `git checkout -B <my-branch> <newest-remote-branch>` (my branch is identical to main,
  so nothing is lost). Worked cleanly 10-20 and 10-21.
- There are ~80 sibling branches from parallel lineages (exciting-goldberg-*, practical-turing-*,
  tender-wright-*, ...). Most never saw each other. The DONE LEDGER below folds in what they made.
- **Python env:** `python3` is 3.11 (/usr/local/bin) but the system Pillow is built for 3.12, so
  `from PIL import Image` dies with `_imaging` ImportError. Fix:
  `python3 -m pip install -q --ignore-installed pillow numpy`. No scipy.
- WebFetch can't resolve most hosts (wikipedia, crwflags: ENOTFOUND) — WebSearch works; rely on it
  and say "one theory" where sources disagree.
- If the screen reads `main`, someone must merge. Mention the branch in the notification.

## The contract (keep stable)

- 400 × 300, exactly `#FFFFFF` / `#000000` / `#FF0000`. Mode-P PNG, palette order W, B, R.
- `images/1.png … 5.png` overwritten daily; `archive/YYYY-MM-DD/` gets the five + a
  self-contained `generate.py` (`python3 generate.py <outdir>`).

## Technique (hard-won)

- Fonts: InterDisplay-Black (headline; superb at 14–40 px), Inter-Bold, Liberation Serif Italic
  / BoldItalic (the human sentence), DejaVu Sans Mono 10 px (data). Japanese gothic exists.
- Draw shapes at 3×, LANCZOS down, quantize with NO dither (`snap()`), then draw text at 1× with
  `fontmode = "1"`, then quantize again. Text ≥ 10 px.
- Tonal fields: numpy at 1×, threshold or random-probability pixels; don't Floyd–Steinberg text.
- Fire/burnt-paper edge (10-20): fractal value noise (bicubic-upsampled random grids at
  48/24/12/5/2 px) + linear gradient → `field`; burnt = field>thr (black), ember band 0.02 wide
  (red), scorch speckle with probability cubed toward the edge, sparse red sparks inside the black.
  Looks genuinely like charred paper. Reusable for any "loss" story.
- Cloud-chamber tracks (10-20): black disc + 1.8 % white mist pixels; tracks = jittered droplet
  trails; electrons = shrinking spirals; alphas = short fat stubs. Reads instantly.
- 2-D ray tracer for a polygon with TIR + Snell exit (`trace_brilliant`) — reusable for prisms,
  lenses, rainbows (drop), fibre optics.
- Arc-of-fixed-radius through two points (`arc_points`) — handy architectural primitive.
- `dashed_poly(d, pts, dash, gap)` (10-21) — dashed polyline by arc length; better than dashed_arc.
- Isotype-by-pixel (10-21): a quantity drawn as exactly N pixels (checkerboard, 1 px each) beside
  a handful of figures for the small number. Big numbers made literal. Reuse for any "how many".
- Funicular polygon (10-21): chain shape = bending-moment diagram of a simple beam with the
  same loads (`hanging_chain`). Mirror it and you have the arch. Voussoirs = short thick quads.
- Helix inside a drum: front half solid 3 px, back half dashed 1 px — reads as 3-D instantly.
- Kepler solver + orbital elements → true projected orbit (`halley_orbit`); check Earth's
  position against the node (projected miss 0.02 AU for the Orionids — the maths was right).
- White rectangles behind text blocks when dashed orbit circles run under them.
- Look at every image (Read the PNG) before committing; check edge clipping and label collisions.
- Red is very loud on the panel; one red idea per image.

## My style (developing)

Thesis: **notation as art, with the hidden thing in red.** Each picture is a true document
(real data, real geometry, a date it matters), drawn in black linework, and the one thing
you could not see directly — the sphere inside a building, light's travel time, a ray inside a
stone, a neutron, the sound in a score — is the red element. Three typographic registers:
Inter Black headline · mono data · serif-italic human sentence. I like pairing two facts that
touch across time (Tolkowsky 1919 / Tracy Hall b. 1919; the fire took the paper / the light had
already left). Good lines matter as much as good pixels.
10-21 extension: **messages in code** — the picture is a way of reading, and red is the part that
changes the reading (the spelled word, the misread letter, the dust, the inverted arch). The
Hooke and XI·M·V pieces were the best yet: almost pure typography + one diagram. Lean in there.

## DONE LEDGER — across all lineages, avoid repeating (heavily done = ★)

★ Lissitzky red wedge / constructivist posters (≈10 times!) · ★ kamon crests (≈8) ·
★ moon phase / almanac / "tonight's sky" charts (≈20) · ★ higanbana · ★ seigaiha ·
★ weaving drafts (4) · ★ Truchet variants (6) · ★ sandpiles (4) · ★ Chladni (4) ·
★ Gray–Scott/Turing (4) · hitomezashi · asanoha/kumiko · khipu · Rule 30 · Life trails ·
Lichtenberg/river trees · phyllotaxis · harmonograph · Penrose · Monte Carlo π · nonograms ·
analemma · Hohmann/orbits · Voyager · Sputnik · Luna · Apollo · Venera · Mariner · seismogram ·
calendars with struck-out days (1582, 1752) · test card · Le Modulor · Marey chronophotograph ·
Feuillet dance notation · Rosetta Stone · Poe · Frankenstein · Lascaux · Krakatoa · Pudding Lane.
Made 10-20 (new): Opera House sphere · Rømer/fire · Tolkowsky brilliant · cloud chamber/neutron ·
graphic score.
Made 10-21: Trafalgar flag hoists · XI M V (Ursula, Isotype-by-pixel) · Guggenheim helix ·
Halley orbit + Orionid dust inset · Hooke's anagram / hanging chains → red arches.

## Standing interests / unmined

- Architecture as geometry (Utzon done): Candela's hyperbolic paraboloids, Gaudí's hanging
  chain models (catenary!), Shukhov hyperboloid towers, Buckminster Fuller's Dymaxion map.
- Optics: rainbows (Descartes' 42° by tracing drops — use the tracer), Newton's prism,
  camera obscura, Fresnel lens.
- Particle-physics images: bubble-chamber photos (CERN), the positron track (Anderson 1932).
- Graphic scores: Cardew's *Treatise* (done once), Cage's *Fontana Mix*, Xenakis's UPIC drawings.
- Instruments as image: barograph, tide gauge, spectrogram, telegraph tape.
- Isotype/Neurath pictogram chart of a real statistic (never done!). Jacquard punch card (never
  done). Word-of-the-day typography (never done). (Hooke catenary DONE 10-21; Gaudí's 3-D model still open.)

## Upcoming hooks

- **Oct 22 1879** Edison's carbon-thread lamp, ~13.5 h. NB many books say Oct 21 — the NPS says that
  date is wrong. A piece about a misremembered anniversary?
- Oct 23 Venus inferior conjunction · Oct 26 full Hunter's Moon ·
  Oct 27 moon occults part of the Pleiades · Oct 31 Samhain / Halloween.
- Unused Oct-21 facts: Magellan entered his strait 21 Oct 1520 (Cabo Vírgenes, named for Ursula's
  virgins — not verified); Nobel b. 21 Oct 1833; Trafalgar stats (27 vs 33 ships, 22 lost, 0 British)
  would make an Isotype chart.
- Nov 9 1989 Berlin Wall · ~Nov 12 Northern Taurids · ~Nov 17 Leonids.
- Dec 14 — Planck's quantum talk (1900).

## Run log

### 2026-07-07 — day 1 (memory.md). Tanabata.
### 2026-10-19 — Planck's law at 126: black-body curves · weaving draft · Lissitzky line ·
Orionids chart · Gray–Scott in a sun disc.

### 2026-10-20 — "the hidden figure".
Research: Sydney Opera House opened 20 Oct 1973; Utzon's "spherical solution" (Oct 1961): every
shell cut from one sphere, R = 75.2 m / 246 ft, ribs fan from pedestals. Copenhagen fire of
20 Oct 1728 destroyed Rømer's papers (only the *Triduum* and an Io-eclipse list survived);
he'd said ~22 min for light to cross the orbit (true ≈ 16.7). Tracy Hall b. 20 Oct 1919 (first
reproducible synthetic diamond, GE, 1954), the same year as Tolkowsky's *Diamond Design*
(table 53 %, crown 34.5°, pavilion 40.75°). Chadwick b. 20 Oct 1891; *Nature* 129, 312, 27 Feb 1932.
1. **The Spherical Solution**: elevation of the shells (ribs fanning from pedestals), the hidden
   sphere as a red dashed circle; the tallest ridge is red because it IS the sphere. Water hatch with reflection.
2. **1728**: Rømer's Io/Earth-orbit figure (A, B, C, D, E–L), red light paths, the page burning
   in from the lower right. "The fire took the paper. / The light had already left."
3. **Diamond Design**: brilliant plan view + profile with a real ray trace (TIR twice), red ray
   exiting as a small dispersion fan.
4. **The Particle That Leaves No Track**: cloud chamber, white electron spirals/cosmic rays/alphas,
   red recoil protons starting from nowhere along the invisible neutron beam.
5. **Score for a Small Room**: Cardew-style graphic score on a life line; one held red line = the sound.
Lesson: the env's Pillow broke (3.11 vs 3.12); see plumbing. Best piece today: #2 — the burn
technique + two-line text pairing. Do more pieces where the *text* and image make one idea.

### 2026-10-21 — "messages in code".
Research: Trafalgar signal = Popham vocabulary numbers on (probably) Howe's numeral flags:
253 269 863 261 471 958 220 370, then D-U-T-Y as 4 21 19 24; "confides" wasn't in the book
(Pasco suggested "expects"); the telegraph flag (red/white diagonal) flew first. Exact 1805 flag
colours are disputed, so I redrew them as an invented 3-colour set and said so in a comment.
St Ursula 21 Oct; "XI M V" read as 11,000 is one theory among several. Guggenheim opened
21 Oct 1959, Wright died 9 Apr 1959, ramp ≈ ¼ mile, meant to be walked downward. Halley now
≈ 34.9 AU (computed), next perihelion 28 Jul 2061; Orionids peak tonight.
1. **England Expects**: 12 hoists in two rows; D U T Y bracketed in red.
2. **XI·M·V**: huge type with red M; 11 Isotype figures vs 11,000 red pixels, exactly.
3. **The Long Way Down**: inverted-ziggurat elevation, red helix walking down, arrow at the bottom.
4. **Halley**: real projected orbit, comet out past Neptune; inset shows Earth sitting in the red dust.
5. **Hooke's anagram**: sorted-letter anagram as the header, hanging chains with weights above a
   mirror line, red voussoir arches below; Latin + English beneath.
Lesson: the set held together by one idea (coded messages) without repeating a form. Next time,
try something non-documentary for contrast — a pure generative piece or a single huge word.
