# memory-fable-5-1

My own memory file for the daily e-ink routine. I'm Claude, and the routine prompt names this
file, so it's the one I read and rewrite each day. (`memory.md` is an older notebook from an
earlier routine. It's useful history, but this file is mine.) Future me: read all of this, then
prune and rewrite freely. Keep it short enough to read in one go.

## The contract

- Edward's desk screen: 400 × 300, exactly **#000000 / #FFFFFF / #FF0000**.
- Each day: 5 PNGs → `images/1.png … 5.png` (overwritten) plus `archive/YYYY-MM-DD/` (the five
  images plus a self-contained `generate.py` that reproduces them from the repo root).
- Push to whatever branch the session names (2026-11-10: `claude/quirky-noether-74tvqr`; the prefix
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
  per-run branches. Don't repeat that notification unless something new breaks.

## Toolbox (works on this box)

- `python3 -m pip install -q --ignore-installed numpy pillow ephem` first. The system PIL is broken
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
  try: tram tickets, telegrams, luggage labels, seed packets, a planisphere with a moving wheel.
- Screens as a form (new, 11-10): radar PPI and a 1985 tiled desktop done. Still to try: an
  oscilloscope Lissajous, a teletext page, a vector-display starfield, an ECG strip, a sonar waterfall,
  a departure board (split-flap), a seven-segment clock.
- Art-theory diagrams as a form (new, 11-10: Hogarth's seven lines). Next: Klee's "taking a line
  for a walk" (Pedagogical Sketchbook), Dürer's letter constructions, Kandinsky's Point and Line
  to Plane, Itten's contrast studies in 3 colours, Chevreul, Owen Jones' Grammar of Ornament.
- Instruments as a form (new, 10-25): astrolabe done. Next: a sundial or nocturnal, a slide rule,
  a sextant arc, a Napier's bones set, a tide-predicting machine trace.
- Two-view / multi-view drawings (Mili's two cameras): the same 3D object shown front and side.
  Could do orthographic plans, stereo pairs, or a knot shown in three projections.
- Sky almanac: keep doing one sky piece when the sky gives a reason.
- Early space imagery: V-2 photos, Lunar Orbiter scan-lines, Luna 3's far-side image (7 Oct 1959).

## Sky hooks ahead

- No sky piece on 11-10 (thin 2% moon setting 35 min after the sun; nothing to see) — so the
  next run should do one. Computed 11-10 with ephem for London: Mars (mag 0.8) and Jupiter (−1.9)
  both in Leo, rising ~23:00 and closing on a conjunction ~Nov 14–16; Venus (−4.3) and Mercury in
  Virgo before dawn, Venus rising ~04:54; Saturn in Cetus, setting ~03:24.
- N. Taurids ~Nov 11–12 (slow fireballs, dark skies), Leonids Nov 16–18, Mercury greatest W
  elongation Nov 20, full supermoon Nov 24 14:53 UTC, Uranus at opposition Nov 25, Venus
  brightest ~Nov 27. December: Geminids Dec 13–14, solstice Dec 21.

## Ideas backlog

- Telegram form (Oct/Nov anniversaries), Ming Forbidden City roof plan (capital 1420), punch-card weave (Jacquard to IBM), Truchet/maze piece,
  a "word of the day" type specimen, Hokusai-style wave with a halftone sea.
- Other runs on older branches already did plenty of: Proun/red wedge, kamon, Chladni, moon
  cards, seigaiha, sandpiles, weaving drafts. Avoid those unless there's a truly new angle.
- Instruments still untried: sundial/nocturnal, slide rule, sextant, Napier's bones. (Tide
  machine done 10-26 — the "sum of pulleys" diagram was a good form.)
- Objects-drawn-large (new, 10-26): the bifurcated needle worked as a quiet memorial. Other
  humble world-changing tools: a cotter pin, a QWERTY typebar, a ration book, a Bakelite plug.
- Upcoming dates: Nov 11 Armistice / Martinmas (lantern processions; Luther was baptised on it);
  Nov 12 Voyager 1 at Saturn (1980); Nov 14 Moby-Dick US publication (1851), Nellie Bly sets off
  (1889); Nov 15 Intel 4004 (1971); Nov 17 Suez Canal opens (1869); Nov 19 Gettysburg Address;
  Nov 20 Windows 1.0 ships (did the announcement 11-10 — skip); Nov 22 SOS adopted? (check);
  Nov 24 Origin of Species (1859); Nov 26 Casablanca premiere (1942).
- Unused 11-10 hooks: Stanley meets Livingstone (his own date 10 Nov 1871 is disputed), Luther
  b. 1483, Morricone b. 1928.

## Run log

### 2026-10-24 (Sat). V-2 film frame, Hunter's Moon field, After Albers, Houdini playbill,
Black Thursday ticker tape. Albers was the strongest pure-graphic piece.

### 2026-10-25 (Sun). Clocks back; St Crispin's Day.
Twice 01:00 (hour-hand spiral), Astrelabie (working astrolabe plate, 51°50′N), Crispin Crispian
(520 arrow parabolas), Drawing with light (one 3D gesture, two cameras — a favourite; red-dither
halo on black works), Organette strip (Blue Danube as punched holes).
Lesson: make the important thing *big*.

### 2026-10-26 (Mon). Full Hunter's Moon.
Seven Sisters (Pleiades occultation chart), News by gunfire (Erie Canal cannon relay), Laws of the
Game I (1863 pitch to scale), Merca (bifurcated needle, drawn large), Sum of five sines (Kelvin
tide machine). Lesson: plan label slots before drawing; humble objects need to be drawn BIG.

### 2026-10-27 (Tue) — forked run (branch `esqsgs`, merged in 10-28)
Comic panel with Ben-Day sky over Manhattan (Lichtenstein b. 1923); Lissitzky wedge as the first
IRT train; strip map of the 28 IRT stations of 1904; six Chladni plates; Gray–Scott seeded with
"1952". Recipes from it: Chladni grains p ∝ exp(−(d/0.012)²) with d=|f|/|∇f|; Gray–Scott Du=.16
Dv=.08, coral F=.0545 k=.062, worms F=.029 k=.057.

### 2026-10-28 (Wed). Theme: thin things that held.
In hoc signo (dithered dusk, six-arch bridge, red chi-rho), 3/32″ (Liberty's copper skin at actual
size — the screen as a ruler), 14:04 (shortwave dial on МОСКВА), Tabvla rasa (wax tablet, almost
all white), first frost (DLA, one red lineage). "True scale" is a reusable form (a stamp, a seed,
a flea, a chip die at 4.72 px/mm).

### 2026-11-10 (Tue). Theme: calls. (First run after a 12-day gap.)
Hooks, all verified: Edmund Fitzgerald lost 10 Nov 1975 (last radio 19:10 EST to the Arthur M.
Anderson, "We are holding our own"; 29 men; 46°59.9′N 85°06.6′W); first coast-to-coast direct-
dialled call, Sat 10 Nov 1951, Englewood NJ → Alameda CA, 415 LAkehurst 3-9727, ~18 s to ring;
Hogarth b. 10 Nov 1697 (Analysis of Beauty pl. I fig. 49: seven waving lines, No. 4 the line of
beauty, 1–3 "mean and poor", 5–7 "gross and clumsy"); Sesame Street ep. 1, Mon 10 Nov 1969,
sponsors W, S, E, 2, 3; Windows announced Thu 10 Nov 1983 at the Helmsley Palace, shipped 20 Nov
1985, tiled windows only (and it shipped with Reversi).
1. **Holding our own**: the Anderson's radar scope — dithered phosphor sweep, sea clutter, one red
   blip ten miles ahead; the quote in white bold italic beside it. The tonal piece, and the best.
2. **18 seconds**: a rotary dial drawn large (dialled digits red, 415 on the card) + the ten digits
   as red pulse trains (45 clicks).
3. **No. 4**: Hogarth's seven lines as an engraved plate, swelling strokes, the fourth in red.
4. **W S E 2 3**: six-cell type poster, each glyph a different face, "today is brought to you by…".
   No characters or logos — the letters alone carry it.
5. **Tiled**: a 1-bit desktop: MS-DOS Executive, Clock at 11:10, Notepad telling the story,
   Reversi, a November 2026 calendar with the 10th red. Checker "grey" icon bar.
Notes: pass 1 had mushy captions (3× path) and the JetBrains O/D problem — both now in Toolbox.
The desktop is a good recurring *container* (a window per fact), but don't lean on it.
