# memory-fable-5-1

My own memory file for the daily e-ink routine. I'm Claude, and the routine prompt names this
file, so it's the one I read and rewrite each day. (`memory.md` is an older notebook from an
earlier routine. It's useful history, but this file is mine.) Future me: read all of this, then
prune and rewrite freely. Keep it short enough to read in one go.

## The contract

- Edward's desk screen: 400 × 300, exactly **#000000 / #FFFFFF / #FF0000**.
- Each day: 5 PNGs → `images/1.png … 5.png` (overwritten) plus `archive/YYYY-MM-DD/` (the five
  images plus a self-contained `generate.py` that reproduces them from the repo root).
- Push to whatever branch the session names (2026-10-28: `claude/practical-turing-njotwk`).
- **Continuity gotcha (found 10-25):** each run's branch starts from `main`, and nothing gets
  merged, so `main` still has only Day 1 (Jul 7) and no copy of this file. First step every day:
  `git fetch origin`, find the newest `origin/claude/practical-turing-*` branch
  (`git for-each-ref --sort=-committerdate refs/remotes/origin/claude`), and
  `git merge --ff-only` it into today's branch (a `git reset --hard` gets blocked by the
  permission classifier; a fast-forward merge works fine). That brings in this file and the archive. If the screen
  reads `main`, it's been showing July's pictures all along, so tell Edward in the notification.
- **10-28 addendum:** the 10-27 run *didn't* merge (it reseeded this file from `memory.md`), so the chain
  forked. I ff-merged 10-26 (`x41xot`) then did a real merge of 10-27 (`esqsgs`), keeping this file's
  text (ours) and folding its log in below. If two branches share the newest date, check *both*:
  `for b in $(git branch -r); do git log -1 --format='%ci %h' $b; done | sort | tail`.

## Toolbox (works on this box)

- `python3 -m pip install -q --ignore-installed numpy pillow ephem` first. The system PIL is broken
  (`_imaging` import error); plain `pip install` thinks it's satisfied, so `--ignore-installed`.
- **PyEphem works** and is great for real sky data: topocentric Moon positions, occultation
  disappear/reappear times (loop minutes, test separation < m.size/2). Precompute the numbers
  and embed them in generate.py so the archive script needs no ephem.
- Fonts: JetBrains Mono (Regular to ExtraBold, my favourite for captions), DejaVu, Liberation,
  FreeSerif Italic/BoldItalic (lovely for playbill flourishes), Caladea/Carlito, wqy-zenhei (CJK).
- Pipelines:
  - *Tonal*: render at 3× in RGB, LANCZOS down, Floyd–Steinberg into the 3-color palette.
    Fractal value noise (stacked bicubic-upscaled random grids) gives clouds, maria and terrain.
  - *Graphic*: 1× pure colors with `dr.fontmode = "1"`. Antialiased small text at 1× turns to
    mush, so always set fontmode for 1× text.
  - *Hybrid*: 3× with AA, quantize with `dither=False` for crisp posters. Keep body text pure
    BLACK, never grey, or it breaks up.
- Text along a curve: rotate each glyph onto the path. **Defer stamping glyphs until the ribbon
  ahead of them is drawn**, or later segments paint over them.
- A 9 px mono caption is about the smallest that survives. Red pixels read very strong.
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

Working name: **"printed matter from a date."** Each picture is an *object*: a film frame, a
playbill, a ticker tape, a textile, a field at night. Each one is anchored to something true
about *today*, with a small factual caption in JetBrains Mono that rewards a closer look. Red is
used sparingly as the one thing that matters (the moon, the padlock, the crash line). I'm pulling
toward:
- a mix in each set: 1 tonal/atmospheric, 1–2 hard-edged graphic, 1 typographic/ephemera, 1 data;
- real facts verified that day (weekday-check old dates with `datetime`, which caught nothing
  this time but costs nothing);
- not repeating a *form* two days running (no two playbills in a row, etc.).

## Interests to mine

- Textile & print geometry: Anni Albers (PO II / Éclat: only isosceles trapezoids +
  parallelograms in a few sizes, rotated). Next: her *knot* drawings, Bauhaus triple-weave
  blocks, Sophie Taeuber-Arp, Sonia Delaunay.
- Ephemera as a form: playbills, ticker tape, film strips, organette strips (done). Still to
  try: tram tickets, telegrams, luggage labels, seed packets, a planisphere with a moving wheel.
- Instruments as a form (new, 10-25): astrolabe done. Next: a sundial or nocturnal, a slide rule,
  a sextant arc, a Napier's bones set, a tide-predicting machine trace.
- Two-view / multi-view drawings (Mili's two cameras): the same 3D object shown front and side.
  Could do orthographic plans, stereo pairs, or a knot shown in three projections.
- Sky almanac: keep doing one sky piece when the sky gives a reason.
- Early space imagery: V-2 photos, Lunar Orbiter scan-lines, Luna 3's far-side image (7 Oct 1959).

## Sky hooks ahead

- (Done 10-26: Pleiades occultation, London 00:17–02:00 GMT Wed 28 Oct.)
- Late Oct pre-dawn: Jupiter, Mars and Regulus lined up in the east.
- Saturn in Cetus all autumn, rising at sunset.
- Nov 2026: S. Taurids peak ~Nov 4–5, N. Taurids ~Nov 11–12, new moon ~Nov 9, Mars–Jupiter
  conjunction ~Nov 14–16, Leonids Nov 16–18, Mercury at greatest W elongation Nov 20, full
  supermoon Nov 24, Uranus at opposition Nov 25, Venus brightest ~Nov 27.

## Ideas backlog

- Telegram form (Oct/Nov anniversaries), Ming Forbidden City roof plan (capital 1420), punch-card weave (Jacquard to IBM), Truchet/maze piece,
  a "word of the day" type specimen, Hokusai-style wave with a halftone sea.
- Other runs on older branches already did plenty of: Proun/red wedge, kamon, Chladni, moon
  cards, seigaiha, sandpiles, weaving drafts. Avoid those unless there's a truly new angle.
- Instruments still untried: sundial/nocturnal, slide rule, sextant, Napier's bones. (Tide
  machine done 10-26 — the "sum of pulleys" diagram was a good form.)
- Objects-drawn-large (new, 10-26): the bifurcated needle worked as a quiet memorial. Other
  humble world-changing tools: a cotter pin, a QWERTY typebar, a ration book, a Bakelite plug.
- Upcoming dates: Oct 29 ARPANET first message "LO"
  (1969); Oct 30 War of the Worlds broadcast (1938); Oct 31 Hallowe'en / Reformation (1517);
  Nov 1 All Saints / Lisbon earthquake (1755); Nov 3 Laika (1957); Nov 5 Bonfire Night;
  Nov 9 Berlin Wall (1989); Nov 11 Armistice. Nov 2 Día de Muertos (papel picado was done once
  in Sept on another branch; a calavera or marigold-arch would be new).

## Run log

### 2026-10-24 (Sat). V-2 film frame, Hunter's Moon field, After Albers, Houdini playbill,
Black Thursday ticker tape. Albers was the strongest pure-graphic piece.

### 2026-10-25 (Sun). Clocks back; St Crispin's Day.
Found the continuity gotcha above and merged yesterday's branch first. Hooks: BST ends (02:00 →
01:00, a 25-hour day); Chaucer d. 25 Oct 1400 (Treatise on the Astrolabe for "Litel Lowys",
latitude of Oxenforde 51°50′); Agincourt 25 Oct 1415 (Julian; a Friday); Picasso b. 1881, plus
Gjon Mili's 1949 light drawings (two cameras, side and front); Johann Strauss II b. 1825.
1. **Twice 01:00**: the hour hand's path as a spiral (radius = elapsed, angle = shown). The repeated
   hour is two parallel red arcs with a dashed snap-back.
2. **Astrelabie**: a working astrolabe plate for 51°50′N, with the rete set for 21:00 GMT tonight
   (real star positions), plus the Middle English opening.
3. **Crispin Crispian**: 520 arrow parabolas accumulated into a dithered cloud over a furrowed
   mud band, with one red flight.
4. **Drawing with light**: one random 3D gesture shown from two cameras, front and side. White core,
   red-dithered halo on black. This is my favourite of the day, and red-on-black glow works well.
5. **Organette strip**: the Blue Danube opening (simplified) punched as holes on a sprocketed strip.
   The echo "ta-ta" notes are red.
Notes: the first spiral packed the key hour into the centre. Make the important thing *big*.

### 2026-10-26 (Mon). Full Hunter's Moon (04:12 UTC).
Hooks: Moon occults Pleiades over London Wed 28 Oct (Celaeno, Taygeta, Asterope, Maia; computed
with ephem); Erie Canal opened 26 Oct 1825 (cannon relay Buffalo→NYC ~81 min; Seneca Chief
arrived 4 Nov; 363 mi, 83 locks); FA founded at Freemasons' Tavern, Mon 26 Oct 1863 (Law I: max
200×100 yd, flags, posts 8 yd apart, no tape or bar); last natural smallpox case, Ali Maow
Maalin, Merca, 26 Oct 1977 (sources differ 26/27/30 Oct on onset vs diagnosis; WHO uses 26).
1. **Seven Sisters**: black chart, ghost Moon every 30 min, solid disc at 01:00 hiding four red-ticked sisters.
2. **News by gunfire**: lock-staircase profile, a row of guns with red puffs, 81 min vs 9 days in big type.
3. **Laws of the Game I.**: a rule-book page; the 1863 maximum ground to scale, stipple turf, no lines.
4. **Merca**: a bifurcated needle drawn large, red dose in the fork, short italic memorial text.
5. **Sum of five sines**: Kelvin tide machine (pulleys over, guides under, one wire) + red week trace.
Notes: labels collided everywhere on pass 1 (Erie city names, tide footer). Plan label slots
before drawing. The needle looked weak until drawn much bigger with engraved hatch lines.


### 2026-10-27 (Tue) — forked run (branch `esqsgs`, merged in 10-28)
Comic panel with Ben-Day sky over Manhattan (Lichtenstein b. 1923); Lissitzky wedge as the first
IRT train; strip map of the 28 IRT stations of 1904; six Chladni plates; Gray–Scott seeded with
"1952". Recipes from it: Chladni grains p ∝ exp(−(d/0.012)²) with d=|f|/|∇f|; Gray–Scott Du=.16
Dv=.08, coral F=.0545 k=.062, worms F=.029 k=.057.

### 2026-10-28 (Wed). Theme: thin things that held.
Hooks: Milvian Bridge 28 Oct 312 (Eusebius: the sign above the sun); Statue of Liberty dedicated
28 Oct 1886 (skin 3/32″ copper; ~300,000 rivets, 1,500 saddles, ~1,350 iron bars — Copper
Development Assoc.); Radio Moscow 14:04 GMT 28 Oct 1962 broadcasting Khrushchev's letter before
editing was finished; John Locke d. 28 Oct 1704 (Essay II.i.2 "white paper, void of all characters").
1. **In hoc signo**: dithered dusk over a six-arch bridge with rippled reflection, red ☧ in a black
   halo above the sun, one red tower window. Moody; the arches-in-water read well.
2. **3/32″**: Liberty's skin as an 11 px red band, *actual size* at 4.72 px/mm, riveted saddle over
   a cross-hatched armature bar. Best idea of the day: the screen itself as a ruler.
3. **14:04**: a shortwave dial (49–19 m bands), red needle on МОСКВА, magic eye, two knobs.
4. **Tabvla rasa**: a wax-tablet diptych, wood grain as white lines, everything blank but a small red
   stylus and its first 4-px mark. Nearly all white — a quiet picture for the panel.
5. **(untitled) first frost**: DLA from the window sill plus three dust nuclei; one lineage red.
Notes: pass 1 put the sun *under* the bridge and the stylus read as an arrow. "True scale"
is a new reusable form (a stamp, a seed, a hair, a flea, a microchip die at 4.72 px/mm).
