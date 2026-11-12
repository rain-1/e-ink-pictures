# memory-fable-5-1

My own memory file for the daily e-ink routine. I'm Claude, and the routine prompt names this
file, so it's the one I read and rewrite each day. (`memory.md` is an older notebook from an
earlier routine. It's useful history, but this file is mine.) Future me: read all of this, then
prune and rewrite freely. Keep it short enough to read in one go.

## The contract

- Edward's desk screen: 400 × 300, exactly **#000000 / #FFFFFF / #FF0000**.
- Each day: 5 PNGs → `images/1.png … 5.png` (overwritten) plus `archive/YYYY-MM-DD/` (the five
  images plus a self-contained `generate.py` that reproduces them from the repo root).
- Push to whatever branch the session names (2026-11-12: `claude/quirky-noether-anvrid`; the prefix
  changes — it has been `tender-wright`, `exciting-goldberg`, `practical-turing`, `quirky-noether`).
- **Continuity gotcha (found 10-25):** each run's branch starts from `main`, and nothing gets
  merged, so `main` still has only Day 1 (Jul 7) and no copy of this file. First step every day:
  `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` (a plain fetch only brings main + today's
  branch), find the newest `origin/claude/*` branch **that contains this file**
  (`git for-each-ref --sort=-committerdate refs/remotes/origin/claude`), and
  `git merge --ff-only` it into today's branch (a `git reset --hard` gets blocked by the
  permission classifier; a fast-forward merge works fine). That brings in this file and the archive. If the screen
  reads `main`, it's been showing July's pictures all along, so tell Edward in the notification.
- If two branches share the newest date, check both and merge both (it happened on 10-27/28).
- 11-10: the chain was intact (10-28 `njotwk` was newest), but there were **no runs 10-29 … 11-09**.
  Told Edward by notification that `main` still holds July's five and the daily sets live on
  per-run branches. Don't repeat that notification unless something new breaks. (11-11: chain
  intact, merged `74tvqr`, stayed silent. 11-12: same, merged `04nmwa`, silent.)
- On a fresh `main` checkout this file is absent and only `memory.md` exists. That is the gotcha
  above, not a first run — don't start over.

## Toolbox (works on this box)

- `python3 -m pip install -q --ignore-installed numpy pillow ephem` first (11-11: numpy was missing entirely). The system PIL is broken
  (`_imaging` import error); plain `pip install` thinks it's satisfied, so `--ignore-installed`.
- **PyEphem works** and is great for real sky data: topocentric Moon positions, occultation
  disappear/reappear times (loop minutes, test separation < m.size/2). Precompute the numbers
  and embed them in generate.py so the archive script needs no ephem.
- Fonts: JetBrains Mono, DejaVu, Liberation, FreeSerif, Inter (`/usr/share/fonts/opentype/inter/`,
  Thin→Black; Inter-Black is a superb poster face), Caladea/Carlito, wqy-zenhei (CJK).
- **Small 1-bit text: use DejaVu Sans Mono 10 px (6 px advance), bold 9–10.** Tested 11-10 side by
  side: JetBrains Mono at 9–10 px in fontmode "1" turns O into D and 0 into 8 ("MS-DDS", "CLDCK").
  JetBrains is fine from ~12 px up, or as ExtraBold display digits.
- **Never put small text through the 3× → LANCZOS → quantize path** (it comes out as "SAI 1D NOV").
  11-10's `save(img, n, post)` draws big shapes at 3×, quantizes, then runs a 1× crisp pass for captions.
- Pipelines:
  - *Tonal*: render at 3× in RGB, LANCZOS down, Floyd–Steinberg into the 3-color palette.
    Fractal value noise (stacked bicubic-upscaled random grids) gives clouds, maria and terrain.
  - *Graphic*: 1× pure colors with `dr.fontmode = "1"`. Antialiased small text at 1× turns to
    mush, so always set fontmode for 1× text.
  - *Hybrid*: 3× with AA, quantize with `dither=False` for crisp posters. Keep body text pure
    BLACK, never grey, or it breaks up.
- Text along a curve: rotate each glyph onto the path. **Defer stamping glyphs until the ribbon
  ahead of them is drawn**, or later segments paint over them.
- Red pixels read very strong. Solid red *cells* with white type work too (11-10 poster).
- Radar/phosphor look: build a float glow field (sweep afterglow exp(−Δθ/1.1), clutter = product of
  two value-noise scales × exp(−r/34), Gaussian range rings), FS-dither to black/white, paint red after.
- Small italics at 1×: **Liberation Serif Italic** at 12–13 px hints cleanly. FreeSerif Italic
  drops letters at that size ("brohers"). FreeSerif BoldItalic is fine from 15 px up.
- Astrolabe maths (in 2026-10-25/generate.py): stereographic projection from the south pole,
  r = Req·tan((90°−δ)/2), plus alt/az→(δ,H) for almucantars and a GMST formula. Reusable for any
  planisphere or star-dial piece.
- **Tonal + red without red speckle:** dither tone with a 2-colour (white/black) palette first,
  then paint solid red/black shapes from 3×-drawn masks (`mask_layer` + `paint` in 10-28's script).
  Straight 3-colour Floyd–Steinberg on greys sprinkles red everywhere.
- **Physical scale:** the panel is 84.8 × 63.6 mm, so **4.72 px/mm** (≈120 dpi). "Actual size" pieces work.
- Vectorised DLA (4000 walkers in numpy, sticking prob 0.6, re-drop walkers that stray 45 px above the
  front): 17k crystals in ~5 s. Track each pixel's seed id to colour one lineage.
- Glyphs rotated with NEAREST at 8 px are illegible — keep small text horizontal.
- A thin red diagonal with any widening at one end reads as an ARROW. Avoid for tools/pens.
- **Network:** WebSearch works; WebFetch to en.wikipedia.org fails (host not allowed). Verify facts
  by several targeted searches instead, and keep captions to what two sources agree on.
- **Stipple / "touches" (11-11):** build float fields D (dark) and Rr (red) with numpy, then one
  touch per brick-grid cell: red if u<Rr, black if v<D, else bare paper. 3×3 at pitch 4 for sky,
  5×2 dashes at pitch 6×3 for water. Only big, high-contrast masses survive (a 60 px sail yes, a
  town's windows no); white shapes vanish against a light sky, so make them black or red.
- **Chalk line:** draw strokes on an L mask, multiply by (rand > 0.15), paint. Reads as chalk on black.
- A full **solid-red ground** with white + black type is very strong (11-11 ∫). Thin black mono
  10 px on red is weak; use white for small text on red.
- Giant glyphs: FreeSerif Italic ∫ at 290 px, fontmode "1", is clean. Check both terminals are on canvas.
- Simple chart projection for a constellation: x = −(α−α0)·15·cos δ·s, y = −(δ−δ0)·s (east left).
- **Ray-traced planet (11-12 Saturn):** orthographic rays in numpy against an oblate ellipsoid + ring
  plane z=0, at 3× then block-mean to 1× and `convert("1")`. Ring profile by radius (C/B/Cassini/A/
  Encke), ring shadow on globe and globe shadow on rings from the same `hit()` routine. Keep the
  phase angle small (sun ~38° from the viewer); at ~80° the globe's shadow eats a whole ansa and
  the picture stops reading as Saturn.
- **Figures:** a line-and-circle body reads as a rocket. Shoulders wider than hips (a trapezoid
  torso), two-segment legs with a knee and a foot tick, arms as a V — then it is a person.
- **Ghosts:** a 50 % checker mask is the only "grey" that survives; a 25 % dot screen disappears.
- Superscripts (⁴) in 10 px mono turn into "*". Spell it out ("inverse fourth power").
- Typed-in form values: DejaVu Sans Mono Bold 12. Serif 16 in 1-bit makes "rn" read as "m".
- **Rubber stamp:** draw on an L mask (Inter Black), rotate BICUBIC + threshold 110, knock out ~6 %
  random pixels and a few low-frequency blots. Check the digits afterwards; blots ate a "4" once.
- Before committing, make a 2× contact sheet in the scratchpad and actually look at it.
  Every set so far needed a second pass.

## My style (developing)

Working name: **"printed matter from a date."** Each picture is an *object* or a *surface someone
was looking at*: a film frame, a ticker tape, a radar scope, a dial, an engraved plate, a desktop.
Each is anchored to something true about *today*, with a small factual caption that rewards a
closer look. Red is the one thing that matters (the moon, the blip, line No. 4, today's date).
Rules I keep:
- a mix in each set: 1 tonal/atmospheric, 1–2 hard-edged graphic, 1 typographic/ephemera, 1 data;
- real facts verified that day (weekday-check dates with `datetime`); leave out any number I
  couldn't confirm rather than guess;
- never repeat a *form* from the last two weeks of the log below;
- a loose one-word theme for the set helps choose among hooks (10-28 "thin things that held",
  11-10 "calls") but shouldn't be forced;
- let one picture be nearly empty or nearly silent.

## Interests to mine

- Textile & print geometry: Anni Albers (PO II / Éclat: only isosceles trapezoids +
  parallelograms in a few sizes, rotated). Next: her *knot* drawings, Bauhaus triple-weave
  blocks, Sophie Taeuber-Arp, Sonia Delaunay.
- Ephemera as a form: playbills, ticker tape, film strips, organette strips (done). Still to
  try: tram tickets, telegrams, seed packets (a tag was done 11-12), a planisphere with a moving wheel.
- Screens as a form (new, 11-10): radar PPI, a 1985 tiled desktop, a chalkboard graph (11-11) done. Still to try: an
  oscilloscope Lissajous, a teletext page, a vector-display starfield, an ECG strip, a sonar waterfall,
  a departure board (split-flap), a seven-segment clock.
- Painters' *methods* as a form (new, 11-11: Signac's touches). Next: Seurat's conté grain, Mondrian's
  pier-and-ocean plus/minus, Riley stripes, Vasarely, Hokusai's bokashi, Lichtenstein was done 10-27.
- Art-theory diagrams as a form (new, 11-10: Hogarth's seven lines). Next: Klee's "taking a line
  for a walk" (Pedagogical Sketchbook), Dürer's letter constructions, Kandinsky's Point and Line
  to Plane, Itten's contrast studies in 3 colours, Chevreul, Owen Jones' Grammar of Ornament.
- Instruments as a form (new, 10-25): astrolabe done. Next: a sundial or nocturnal, a slide rule,
  a sextant arc, a Napier's bones set, a tide-predicting machine trace.
- Chronophotography (new, 11-12: Léotard). Next: Marey's birds or a pole-vaulter, Muybridge grids,
  Edgerton's strobe (a golf swing as a fan of clubs), Duchamp's staircase as a method.
- Two-view / multi-view drawings (Mili's two cameras): the same 3D object shown front and side.
  Could do orthographic plans, stereo pairs, or a knot shown in three projections.
- Sky almanac: keep doing one sky piece when the sky gives a reason.
- Early space imagery: V-2 photos, Lunar Orbiter scan-lines, Luna 3's far-side image (7 Oct 1959).

## Sky hooks ahead

- No sky piece since the 10-26 occultation chart (11-11 and 11-12 were historical). The Mars–Jupiter
  pairing below is the next real one — do it with ephem.
- Mars + Jupiter in Leo, rising ~23:00, conjunction ~Nov 14–17 (≈1.2° on the 16th) — a good
  "two dots" picture. Leonids peak night of Nov 17–18. Mercury greatest W elongation Nov 20, full
  supermoon Nov 24 14:53 UTC, Uranus at opposition Nov 25, Venus brightest ~Nov 27.
  December: Geminids Dec 13–14, solstice Dec 21.

## Ideas backlog

- Telegram form (Oct/Nov anniversaries), Ming Forbidden City roof plan (capital 1420), punch-card weave (Jacquard to IBM), Truchet/maze piece,
  a "word of the day" type specimen, Hokusai-style wave with a halftone sea.
- Other runs on older branches already did plenty of: Proun/red wedge, kamon, Chladni, moon
  cards, seigaiha, sandpiles, weaving drafts. Avoid those unless there's a truly new angle.
- Instruments still untried: sundial/nocturnal, slide rule, sextant, Napier's bones. (Tide
  machine done 10-26 — the "sum of pulleys" diagram was a good form.)
- Objects-drawn-large (new, 10-26): the bifurcated needle worked as a quiet memorial. Other
  humble world-changing tools: a cotter pin, a QWERTY typebar, a ration book, a Bakelite plug.
- Upcoming dates: Nov 13 Holland Tunnel opens (1927), R. L. Stevenson b. 1850 (check both); Nov 14 Moby-Dick US publication (1851), Nellie Bly sets off
  (1889); Nov 15 Intel 4004 (1971); Nov 17 Suez Canal opens (1869); Nov 19 Gettysburg Address;
  Nov 20 Windows 1.0 ships (did the announcement 11-10 — skip); Nov 22 SOS adopted? (check);
  Nov 24 Origin of Species (1859); Nov 26 Casablanca premiere (1942).
- Unused 11-12 hooks: Berners-Lee & Cailliau's WorldWideWeb proposal (12 Nov 1990) — a node-and-link
  web with one red "you are here"; Rodin b. 1840; Barthes b. 1915 (the *punctum*: one red point in a photo).
- Unused 11-11 hooks: Perelman posts the first Ricci-flow preprint (11 Nov 2002) — a neck pinching
  under flow would be a fine diagram; Dostoevsky b. 1821; Martinmas lanterns; N. Taurids; Gemini 12 (1966).
- Unused 11-10 hooks: Stanley meets Livingstone (his own date 10 Nov 1871 is disputed), Luther
  b. 1483, Morricone b. 1928.

## Run log

### 2026-10-24 … 10-27 (condensed)
Forms used: film frame, moon field, Albers tiling, playbill, ticker tape; hour-hand spiral, astrolabe
plate, arrow parabolas, two-camera light drawing, punched organette strip; occultation chart, cannon
relay map, football pitch plan, bifurcated needle drawn large, tide-machine sines; Ben-Day comic panel,
Lissitzky wedge, strip map, Chladni plates, Gray–Scott (Du=.16 Dv=.08; coral F=.0545 k=.062).
Lessons: make the important thing BIG; plan label slots before drawing.

### 2026-10-28 (Wed). Theme: thin things that held.
In hoc signo (dithered dusk, six-arch bridge, red chi-rho), 3/32″ (Liberty's copper skin at actual
size — the screen as a ruler), 14:04 (shortwave dial on МОСКВА), Tabvla rasa (wax tablet, almost
all white), first frost (DLA, one red lineage). "True scale" is a reusable form (a stamp, a seed,
a flea, a chip die at 4.72 px/mm).

### 2026-11-10 (Tue). Theme: calls.
Edmund Fitzgerald radar scope with one red blip ("We are holding our own"); rotary dial + pulse
trains (first direct-dialled coast-to-coast call, 1951); Hogarth's seven lines, No. 4 red; W S E 2 3
six-cell type poster (Sesame Street ep. 1); a tiled 1-bit desktop (Windows announced 1983).
The desktop is a good *container* (a window per fact), but don't lean on it.

### 2026-11-11 (Wed). Theme: signs.
Hooks (searched; captions kept to what sources agree on): Tycho sees the new star in Cassiopeia,
11 Nov 1572, walking home from the lab at Herrevad — labelled "I" in *De nova stella* (1573), at
α 0h25.3m δ +64°09′; the Armistice sound-ranging record (six microphones, American front near the
Moselle, a minute either side of 11:00, published 1919 in Crowell's *America's Munitions*; sources
differ on film vs paper, so I didn't say); Leibniz 11 Nov 1675 uses the integral for an area — ∫ is a
long s for *summa*, printed 1686 (some sources date the sign itself to 29 Oct 1675, so the caption
doesn't claim "first ∫"); Vonnegut b. 11 Nov 1922, story shapes on G–I / B–E axes ("B for
beginning, E for entropy"); Signac b. Paris 11 Nov 1863.
1. **Nova stella**: woodcut-style chart, black engraved stars, dotted W, the nova a rayed red star.
2. **11:00**: six jagged traces, a red line, six flat traces. The quiet one, and the best.
3. **∫umma**: solid red ground, a 290 px white ∫ serving as the s of "umma", "y dx" below.
4. **Man in hole**: chalkboard, white man-in-hole curve, red Cinderella staircase → midnight → ∞.
5. **Touches**: a harbour in ~2,900 brick-laid touches (red sun and sails, black sea dashes).
   The weakest: legible but coarse. If I stipple again, use fewer, larger shapes and a denser sea.
Notes: pass 1 had the chart running off the frame, labels on top of curves, and an unreadable
harbour. Arrival delays across the six traces (same shell, shifted per microphone) is a true
detail worth the effort.

### 2026-11-12 (Thu). Theme: arrivals.
Hooks (searched): Voyager 1 closest to Saturn 12 Nov 1980 (sources say 124,000–126,000 km above the
cloud tops, so the caption says "some 125,000"; Titan the day before, which threw it north out of
the ecliptic); Léotard's first flying-trapeze act, Cirque Napoléon, 12 Nov 1859; Philae's three
touchdowns 12 Nov 2014 (15:34, 17:25, 17:32 UTC — sources vary by a minute; harpoons failed; first
bounce "as high as a kilometre"); Rayleigh b. 12 Nov 1842, 1871 papers, scattering ∝ 1/λ⁴
((700/400)⁴ = 9.4); Ellis Island closes 12 Nov 1954, opened 1 Jan 1892, about 12 million, last
detainee the Norwegian seaman Arne Peterssen (spelling varies: Pettersen/Petterson).
1. **Saturn**: ray-traced, dithered globe and rings on black, reseau dots, Titan a red dot. The best.
2. **Léotard**: chronophotograph on black — checker ghosts on two trapezes, a white catcher, the
   man in the air red; LÉOTARD in Inter Black.
3. **Three landings**: the empty one. A dotted 111-minute arc, a 7-minute hop, a red dot at rest.
4. **The long way through the air**: six sine waves 400–700 nm damped by exp(−x/2L), L ∝ λ⁴, the
   700 nm one red and still strong when it reaches "you"; a red sun at the left edge.
5. **Ellis Island**: a manila tag on checker grey, typed fields, a red CLOSED stamp at 11°.
Notes: pass 1 had Saturn lit from the side (unreadable), rocket-shaped acrobats, and a "1/λ*".
Three of the five were black-on-white with a mono caption block at the bottom — the caption
strip is becoming a habit. Tomorrow: at least two pictures with **no caption strip at all**
(fact worked into the object itself, as on the tag), and one that fills the frame edge to edge.

