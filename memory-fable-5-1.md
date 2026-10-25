# memory-fable-5-1

My own memory file for the daily e-ink routine. I'm Claude, and the routine prompt names this
file, so it's the one I read and rewrite each day. (`memory.md` is an older notebook from an
earlier routine. It's useful history, but this file is mine.) Future me: read all of this, then
prune and rewrite freely. Keep it short enough to read in one go.

## The contract

- Edward's desk screen: 400 × 300, exactly **#000000 / #FFFFFF / #FF0000**.
- Each day: 5 PNGs → `images/1.png … 5.png` (overwritten) plus `archive/YYYY-MM-DD/` (the five
  images plus a self-contained `generate.py` that reproduces them from the repo root).
- Push to whatever branch the session names (2026-10-25: `claude/practical-turing-jzmuhe`).
- **Continuity gotcha (found 10-25):** each run's branch starts from `main`, and nothing gets
  merged, so `main` still has only Day 1 (Jul 7) and no copy of this file. First step every day:
  `git fetch origin`, find the newest `origin/claude/practical-turing-*` branch
  (`git for-each-ref --sort=-committerdate refs/remotes/origin/claude`), and
  `git merge` it into today's branch. That brings in this file and the archive. If the screen
  reads `main`, it's been showing July's pictures all along, so tell Edward in the notification.

## Toolbox (works on this box)

- `python3 -m pip install numpy pillow` first. The system PIL was broken (`_imaging` import
  error); a fresh pillow from pip fixes it.
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

- Full Hunter's Moon 04:12 UTC Mon 26 Oct. Moon occults Pleiades stars on Oct 27 (good hook!).
- Late Oct pre-dawn: Jupiter, Mars and Regulus lined up in the east.
- Saturn in Cetus all autumn, rising at sunset.
- Nov 2026: S. Taurids peak ~Nov 4–5, N. Taurids ~Nov 11–12, new moon ~Nov 9, Mars–Jupiter
  conjunction ~Nov 14–16, Leonids Nov 16–18, Mercury at greatest W elongation Nov 20, full
  supermoon Nov 24, Uranus at opposition Nov 25, Venus brightest ~Nov 27.

## Ideas backlog

- Telegram form (Oct/Nov anniversaries), punch-card weave (Jacquard to IBM), Truchet/maze piece,
  a "word of the day" type specimen, Hokusai-style wave with a halftone sea.
- Other runs on older branches already did plenty of: Proun/red wedge, kamon, Chladni, moon
  cards, seigaiha, sandpiles, weaving drafts. Avoid those unless there's a truly new angle.
- Upcoming dates: Oct 27 Pleiades occultation; Oct 31 Hallowe'en / Reformation (1517);
  Nov 1 All Saints / Lisbon earthquake (1755); Nov 3 Laika (1957); Nov 5 Bonfire Night;
  Nov 9 Berlin Wall (1989); Nov 11 Armistice.

## Run log

### 2026-10-24 (Sat). My first day with this file.
Hooks: first photo of Earth from space (V-2 No.13, White Sands, 24 Oct 1946, 105 km, 35 mm frame
every 1.5 s, film survived in a steel cassette); Hunter's Moon 97% beside Saturn; Houdini's last
show (Garrick Theatre, Detroit, Sun 24 Oct 1926); Black Thursday (24 Oct 1929, 12.9 M shares,
afternoon bankers' rally); Anni Albers.
1. **105 km**: a dithered film frame with a curved limb, haze, grain and a scratch, plus red edge codes.
2. **Hunter's Moon**: a red dithered moon, a ringed Saturn, a stubble field converging, red/white glitter, hay bales.
3. **After Albers**: 7 bands of trapezoids/parallelograms, prototypes repeated and rotated 180°.
4. **Houdini**: a playbill with a chained trunk and a red padlock.
5. **Black Thursday**: ticker tape looping over graph paper, with a red cliff-then-rally line.
Notes: the ribbon glyph-overlap bug and 1× text mush were the main fixes. Albers is the
strongest pure-graphic piece; the film frame could use more cloud structure next time.

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

