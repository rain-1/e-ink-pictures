# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(`memory.md` is the older file from the first run on 2026-07-07; this one is live.)

## READ THIS FIRST — the branch problem, and the ledger

Every scheduled run starts from `main`, works on a fresh `claude/...` branch, and pushes
there. **Main was never updated after day 1**, so for two months every run woke up with
only the 2026-07-07 memory, believed it was "day 2", and re-made the same ideas: the
Lissitzky red wedge ~30 times, a kamon crest ~20 times, Truchet ~10, seigaiha ~10, the
abelian sandpile ~8, and a moon/almanac card almost every day. Nobody ever saw the
previous day's memory. On 2026-09-07 I found the 45 orphan branches, copied every day's
`archive/` folder onto this branch, and wrote the ledger below from all their run logs.

So: **if you are reading this, the fix worked** (Edward merged, or the screen points at
this branch). Check `ls archive/` — if it shows only 2026-07-07 plus today, you are on a
stale base again: fetch `origin`, look for the newest `claude/*` branch, and read *its*
`memory-fable-5-1.md` and archive before doing anything.

### The ledger — everything already made (do NOT remake these)

Counts are approximate, across 46 days (2026-07-07 → 2026-09-07):

- **Constructivist / Lissitzky red wedge** — ~30×. Retired. No more wedges, prouns,
  Cyrillic slogans, black-circle-red-triangle compositions. Not even "re-aimed".
- **Kamon crest generators** (n-fold petals in a ring, umebachi, mitsudomoe, "today's
  crest") — ~20×. Retired.
- **Truchet arc tilings** (single-scale, multi-scale, pipes, pools, original 1704) — ~10×. Retired.
- **Seigaiha wave scales** (flat, perspective, inverted-in-sun) — ~10×. Retired.
- **Abelian sandpile** (2^16–2^17 grains, various LUTs) — ~8×. Retired.
- **Moon almanac / "sky tonight" / "September sky" cards**, star charts with real
  positions (Summer Triangle, Scorpius/Antares, Leo/Venus, Pleiades, Teapot, Perseids,
  Cassiopeia) — nearly every day. A sky piece is fine occasionally, but never as a card
  with a moon disc and a dated event list again. Find a new *mechanism* if the sky is used.
- **Hitomezashi** (07-07), **asanoha kumiko** (07-17, 09-04), **Rule 30** (07-13),
  **Conway Life trails** (07-18), **Lichtenberg DLA** (07-10), **Gray–Scott** (09-02),
  **phyllotaxis sunflower** (09-02), **Monte Carlo π / Archimedes polygons** (07-22),
  **geodesic sphere** (07-12), **Hohmann transfer** (07-20), **three-phase AC** (07-10),
  **10 PRINT maze / TRS-80** (07-16, 08-03), **Etch A Sketch line** (07-12),
  **Vogel/flow-field Van Gogh skies** (07-27, 07-29), **ridgelines** (07-07).
- Maps: Victoria circumnavigation (09-06), Channel swim (08-25), Atlantic telegraph
  (08-05), Boston subway diagram (09-01), Nautilus cross-section (08-03).
- Typographic/ephemera: syzygy & 星月夜 & 物の哀れ word cards, Declaration of Sentiments,
  Pi 22/7, ticket stub (Beatles 08-29), patent sheet (07-31), Penguin paperback (07-30),
  Dead Man's Hand cards (08-02), soup-can grids ×2, first webpage (08-06), STOP signal
  (08-05), Roman inscription (09-04), Riso two-plate prints (09-02), 1752 calendar,
  Code 39 barcode (09-06), seven-segment "1.00" (07-18), Beck subway map.
- Scenes: Tanabata Milky Way, Walden, Great-Wave sea (07-13), Zeppelin, Skylab, Saturn V,
  Tranquility Base, Chryse Planitia, Trinity flash, Berkowski eclipse, Krakatoa, Vesuvius,
  Pluto, Neptune rings, Golden Record cover, Pale Blue Dot, Earthrise/Lunar Orbiter,
  Frankenstein tower, Man on Wire, Machu Picchu, Martha the pigeon flock, wheat/Lughnasadh,
  二百十日 wind grass, Moby-Dick whale, thylacine linocut (09-07).
- Eclipse pieces (Aug 12 solar countdowns ×6, Aug 27–28 lunar ×5). Done to death.
- 2026-09-07 (this file's first consolidated day): test card, thylacine linocut, Penrose
  P3, Vasarely bulge, weaver's drawdown.

### Modes still untouched (mine the list, then extend it)

Islamic girih / zellige · Celtic knotwork · Escher-style tessellation of a creature ·
the hat/spectre aperiodic monotile · Wang tiles · Voronoi / Lloyd stipple · moiré ·
Bridget Riley line op-art (Fall, Current) · Anni Albers-style multi-colour weave, tartan
sett · ikat · quilt blocks (Gee's Bend, log cabin) · Amish bar quilts · Ukiyo-e crop
compositions (Hiroshige rain) · linocut/woodcut animals (one done; a series is fine:
kakapo, quagga, dodo, ivory-bill) · anatomical/botanical plates · Haeckel radiolaria ·
Snowflake / Koch / Sierpiński / dragon curve / Hilbert · L-system plants · knot theory
tables · Feynman diagrams · chess problem diagrams (mate in 2) · Go position ·
crossword/nonogram that actually solves to a picture · semaphore/flag alphabets ·
maritime signal flags · braille poster · musical score (real notation) · Sol LeWitt wall
drawing instructions · Josef Albers squares (in 3 colours!) · Bauhaus numeral posters ·
Swiss typographic grid posters · Saul Bass film-poster style · Olympic pictograms
(Otl Aicher) · isotype (Neurath) · WPA park posters · railway heraldry · a comic strip ·
a recipe card · a page from a field notebook · a seismogram / tide table / barograph
(barograph done once, 08-27) · a knitting chart · a punched card / paper tape ·
a Morse or Baudot poster · a slide rule · a nomogram · a sundial · a star trail *photo*
style · a glitch/CRT scanline piece · dither *as the subject* (Bayer vs FS vs Atkinson).

## The screen & the contract

- 400 × 300 pixels, three colours only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of the five + the self-contained `generate.py`
    that made them (+ any data file it needs, e.g. `archive/2026-09-06/ne_110m_land.geojson`).
- The scheduled session pushes to whatever `claude/...` branch it is given, not `main`.

## Tooling notes (learned the hard way)

- The container starts **without Pillow/numpy**: `pip install pillow numpy` first.
- `pip install zxing-cpp` gives a barcode decoder (used 09-06 to prove a Code 39 scans).
- Network: `WebSearch` works and is the main research tool. `WebFetch`/curl are blocked
  for most sites (wikipedia, space.com, starwalk, bridges archive, christophercarlson.com,
  whenthecurveslineup.com all blocked). `raw.githubusercontent.com` works.
- Rendering: draw at 3× (1200×900) with AA, LANCZOS down, then `quantize(palette, dither)`.
  `dither=NONE` after the downscale gives crisp hard-edged pieces (posters, tilings, crests);
  `FLOYDSTEINBERG` only for tonal pieces. Mid-grey **text** turns to speckle under dither —
  keep text pure white/black/red. FS dither on a canvas that is *mostly* pure palette
  colours is harmless (the test card mixes a dithered grey ramp with crisp type).
- numpy per-pixel pieces (op-art warps, cellular things): build a 1200×900 uint8 RGB
  array, `Image.fromarray`, then the same finalize. Inverse-map (sample the source at a
  warped coordinate), never forward-map.
- Chaikin corner-cutting (3 passes) on a hand-placed control polygon gives a smooth animal
  silhouette; carve stripes/eyes as a separate L mask and combine with numpy
  (`body & ~cuts`). That is the linocut recipe.
- Penrose P3: Robinson-triangle subdivision (preshing's 20-line version), 5 levels from a
  10-triangle wheel of radius 300 px gives ~26 px rhombs; outline C→A→B only (BC is the
  internal diagonal). Type 0 = thick rhomb halves, type 1 = thin.
- Weave drawdown: warp end j shows on pick i iff `shaft[j] in tieup[treadle[i]]`. Draw
  wefts, then warp floats over them, 6 px pitch / 5 px thread at 1×.
- Fonts: DejaVu (sans/serif/mono), FreeSans/FreeSerif/FreeMono (FreeSansBold ≈ Helvetica
  Bold, good for posters), Liberation (Serif Italic is the nice italic),
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji), unifont, wqy-zenhei.
- Legibility floor: 9 px mono / 10–11 px serif for anything that must be read; italic
  serif under 11 px is marginal. Red text on black is low-contrast — keep red text on white
  or make it bold. Red reads *bright* on the panel; one decisive red element per picture.
- Rotated text: render to RGBA layer, `rotate(expand=True)`, paste with mask.
- Always render, **look at all five**, fix collisions, render again. Every day's log says
  the same thing: first drafts had text under shapes or off the edge.
- Check every output: mode P, exactly 3 colours, 400×300 (`save()` asserts this).

## Style (what I am becoming)

- One idea per picture, said once, big. A small caption anchors it — or no words at all.
- Hard edges and flat shapes are home; dither only when tone *is* the subject.
- Red is a verb: the thing that moves, the thing that is different, the one warm object.
- Each day's set mixes: (a) something *about today*, (b) a piece of mathematics or craft
  with a real mechanism (a draft, a substitution rule, a mapping), (c) one purely formal
  composition, and at least one piece with **no words**.
- Never repeat a format two days running; never repeat a *retired* format at all.
- The strongest pieces pair ONE bold graphic idea with ONE red element. Resist the third thing.

## Standing interests

- Craft mathematics with a notation: weaving drafts, knitting charts, lace prickings,
  quilt blocks, kumiko (asanoha done; kikkō, mie-hishi, goma-gara not), girih.
- Substitution tilings and aperiodicity: Penrose (done 09-07), Ammann bars, hat/spectre
  monotile, pinwheel, Danzer.
- Op art: Vasarely bulge done; Riley's line pieces, Anuszkiewicz, Soto's moiré not.
- Lost animals & the linocut register: the thylacine was dignified and worked. A quiet series.
- Television / signal / test-pattern history; the test card was the most *useful* picture yet
  (it doubles as a display test for Edward).
- Sky only when a real *event* lands on the day and a new mechanism presents itself.

## Upcoming hooks (verified 2026-09-07; verify again before use)

- **Sep 8** — Moon occults Jupiter (N. America / Greenland; morning). Also Star Trek 60th (1966).
- **Sep 11** — New Moon (~22 UTC).  **Sep 14** — Moon occults Venus (daytime).
- **Sep 18** — Venus greatest brilliance; first-quarter Moon. **Sep 19** — Observe the Moon Night.
- **Sep 22** — Autumnal equinox (northern), ~20 UTC.
- **Sep 26** — Full Harvest Moon 16:49 UTC, in Pisces near Saturn; Neptune at opposition Sep 25.
- Oct: Draconids ~Oct 8, Orionids ~Oct 21, Hunter's Moon ~Oct 26. Nov 17 Leonids. Dec 13–14 Geminids.
- Dates worth a look: Sep 8 (Star Trek), Sep 9 (the first computer "bug", 1947 — the moth),
  Sep 10 (LHC first beam 2008), Sep 12 (Lascaux found 1940), Sep 13 (Roald Dahl b.),
  Sep 17 (Constitution 1787), Sep 19 (Talk Like a Pirate), Sep 21 (Peace Day), Sep 23
  (Neptune discovered 1846), Sep 28 (Fleming/penicillin 1928), Oct 4 (Sputnik 1957).

## Ideas backlog (unmade, concrete)

- Equinox: a gnomon shadow diagram, or an analemma drawn as 365 red dots with today marked.
- Harvest Moon: NOT a card. Try a moonrise *sequence* strip, or a Hiroshige-style crop.
- Jupiter occultation (Sep 8): a four-frame film strip of the Galilean moons vanishing behind
  the bright limb (ingress at the bright limb for a waning crescent; egress from the dark limb).
- Escher-style tessellation of a thylacine/bird; a knitting chart that spells something;
  a nonogram whose solution is a picture; a chess mate-in-two diagram; Albers "Homage to
  the Square" in three inks; a Bayer-vs-Floyd-Steinberg comparison sheet; an Otl Aicher
  pictogram row; a Sol LeWitt instruction executed literally with the instruction as caption.
- Girih strapwork from the five polygon tiles; Celtic knot on a grid with over/under.

## Run log

### 2026-07-07 — day 1. Tanabata.
Amanogawa night scene, hitomezashi, moon almanac card, Summer Triangle chart, ridgelines.

### 2026-07-08 → 2026-09-06 — 44 orphan days (see the ledger above; full detail in `archive/`).
Each ran from a stale `main`. Highlights worth remembering as *good*: Martha the pigeon flock
(09-01), Victoria map (09-06), Mariner 4 paint-by-numbers (07-15), Dagen H (09-03), Foote's
jars (08-23), Beatles ticket stub (08-29), Dead Man's Hand (08-02), first-quarter Lambert moon
(07-21), Krakatoa barograph (08-27), Riso two-plate set (09-02), Golden Record cover (09-05).

### 2026-09-07 — day 47 (first consolidated day). Monday; US Labor Day.
Found the branch drift, merged 46 archives, wrote the ledger. Research: Farnsworth's image
dissector sent the first all-electronic TV picture on 7 Sept 1927 — a straight line on a
glass slide (202 Green St, San Francisco); the last thylacine died at Beaumaris Zoo, Hobart,
7 Sept 1936 (National Threatened Species Day, 90 years); this dawn a 19% waning crescent
near Castor & Pollux with Jupiter and Mars low in the east; Carlson's multi-scale Truchet
paper (Bridges 2018) — read, then *didn't* make it because Truchet is retired. Made:
1. **Test card** — a proper TV test card for this screen: dithered 9-step grey ramp, colour
   bars in the three inks, resolution wedges, corner registration marks, and at the centre a
   black plate showing one white straight line: "the first picture". Also a real display test.
2. **Thylacine** — linocut: black silhouette with white stripe cuts across the rump, gouge
   texture, red sun behind, black ground band with grass cuts. "the last one."
3. **Penrose** — P3 rhombus tiling, five-fold sun at centre, thick rhombs white, thin black,
   the central ten in red. No words.
4. **Vasarely bulge** — 25 px checkerboard with a spherical bulge (inverse asin mapping);
   inside the sphere the black checks turn red. No words. Came out exactly as imagined.
5. **Goose-eye** — a weaver's drawdown: 4-shaft point threading × 2/2 twill tie-up × point
   treadling rendered as actual interlaced threads (white warp, black weft, a red weft band),
   with the draft notation drawn in the corner the way weavers write it.
Lessons: the linocut recipe (Chaikin + mask carving) is reusable; clipping the radius in the
bulge mapping accidentally produced a radial-ray op-art field — a different, good picture,
worth doing on purpose one day. Next: the Sep 8 occultation film-strip if a run lands then;
otherwise pick from "modes still untouched". Keep at least one wordless piece per day.
