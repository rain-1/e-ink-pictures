# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(`memory.md` is the older file from my Fable 5 run on 2026-07-07; I folded it into this
one on 2026-09-06 and this file is now the live one.)

## The screen & the contract

- 400 × 300 pixels, three colours only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of the five + the self-contained `generate.py`
    that made them (+ any data file it needs, e.g. a coastline geojson).
- The scheduled session pushes to whatever `claude/...` branch it is given, not `main`.
  Edward merges. Don't fight it.

## Tooling notes (learned the hard way)

- The container starts **without Pillow/numpy**: `pip install pillow numpy` first.
- `pip install zxing-cpp` gives a barcode decoder — used it to prove a Code 39 scans.
- Network: `WebSearch` works and is the main research tool. `WebFetch`/curl are blocked
  for most sites (wikipedia, space.com, starwalk, jsdelivr, bridges archive all 403).
  `raw.githubusercontent.com` **works** — fetched Natural Earth 110m land geojson from
  `nvkelso/natural-earth-vector`. It is saved in `archive/2026-09-06/ne_110m_land.geojson`
  (138 KB), so future map pieces can just copy it from there.
- Rendering: draw at 3× (1200×900) with AA, LANCZOS down, then `quantize(palette, dither)`.
  `dither=NONE` after the downscale gives crisp hard-edged pieces (posters, maps, crests);
  `FLOYDSTEINBERG` for tonal pieces (moon, sky). Mid-grey **text** turns to speckle under
  dither — keep text pure white/black/red.
- Fonts: DejaVu (sans/serif/mono), FreeSerif/FreeSans/FreeMono (nice italic serif),
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji), unifont.
- Legibility floor on this panel: ~7 px sans is the smallest readable caption; body text 8–9 px.
  Red reads *bright* on these panels — one decisive red accent per picture carries far.
- Rotated text: render to RGBA layer, `rotate(expand=True)`, paste with mask.
- Check every output: mode P, exactly 3 colours, 400×300. Look at each PNG before committing.

## Style (what I am becoming)

- One idea per picture, said once, big. A small caption strip in mono/sans anchors it.
- Hard edges and flat shapes are my home; dither is for skies and moons only.
- Red is a verb: the wedge, the route, the planet, the thing that moves.
- Each day's set mixes: (a) something *about today* (anniversary / sky), (b) a piece of
  mathematics or craft geometry, (c) one purely formal composition.
- Avoid repeating a format two days running (no second star chart on the next day, etc.).

## Standing interests

- Sky almanac data — moon phases, conjunctions, occultations. A desk object that quietly
  says what the sky is doing tonight.
- Japanese pattern mathematics: hitomezashi (done), kamon crests (done 09-06 — compass and
  ruler only; the "today's crest" generator with n-fold symmetry is worth reusing).
  Still to mine: kumiko lattices, seigaiha waves, kikkō hexagons, asanoha.
- Constructivism / Lissitzky — the palette *is* that movement. Did one on 09-06; there is
  room for a whole series (Rodchenko, Malevich, Bauhaus typographic posters).
- Voyages and maps: the Victoria map worked well — black land, white sea, red route.
  Other voyages: Zheng He, Cook, Shackleton's boat journey, the Kon-Tiki, Voyager 1.
- "On this day" with a *visual* mechanism, not just a date (Woodland's Morse-into-bars
  was a good one: the idea drawn, not described).

## Upcoming sky events (hooks)

- **Sep 8** — Moon occults Jupiter (visible N. America/Canada/Greenland), first since 2023
- **Sep 11** — New Moon
- **Sep 14** — Moon occults Venus
- **Sep 18** — Venus at greatest brilliance (evening); First-quarter Moon
- **Sep 19** — International Observe the Moon Night
- **Sep 22** — Autumnal equinox (northern)
- **Sep 25–26** — Neptune at opposition; **Sep 26** Full (Harvest) Moon
- Later: check Oct (Draconids ~Oct 8, Orionids ~Oct 21), Nov (Leonids), Dec 13–14 Geminids.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Kumiko lattice sheet (asanoha, kikkō) as a companion to the kamon sheet
- Equinox piece for Sep 22: day/night exactly split, analemma, or a sundial gnomon diagram
- Harvest Moon (Sep 26): big dithered full moon with a farm/field silhouette
- A "scan me" series: QR code of a poem? (Code 39 scanned fine from the PNG.)
- Malevich-style suprematist scatter; a Bauhaus-style "6" numeral poster
- Voyager 1 golden record cover, redrawn in 3 colours
- Map series template exists now (equirectangular, wrap-aware route) — reuse for other voyages

## Run log

### 2026-07-07 — day 1 (Fable 5). Tanabata.
Bootstrapped the repo conventions. Made: Amanogawa (Tanabata sky), Hitomezashi stitch pattern,
Moon almanac card, Summer Triangle star chart, generative Ridgelines with red sun.

### 2026-09-06 — day 2 (Fable 5.1). Two months' gap; picked up fresh.
Research: Moon 3° N of Mars in Gemini this dawn (26% waning crescent, earthshine);
Sept 6 1522 the Victoria reached Sanlúcar (18 men, cloves, one day lost); Norman Woodland
(barcode) born 6 Sept 1921 — drew the first barcode as four finger-lines in Miami sand, 1949;
kamon are built from circles and lines only (Bridges 2018 paper). Made:
1. **Red Wedge** — constructivist composition, "THREE COLOURS ARE ENOUGH" on the diagonal.
2. **Kamon** — six crests: mitsuboshi, kuyō, mitsu-uroko, mitsudomoe, yotsu-wachigai (woven),
   plus a red "today's crest" generated with 7-fold rays.
3. **Victoria** — world map with the circumnavigation route leaving the left edge and
   returning from the right; "504 years ago today".
4. **Moon & Mars** — this dawn's crescent with earthshine, Mars, Castor & Pollux, and a
   September almanac strip.
5. **Sand** — Morse for S·A·N·D pulled down into red bars; a real scannable Code 39 of
   "6 SEP 2026" below (verified with zxing).
Lessons: labels on a black land mass need to be moved into the sea, not haloed; rotated
text lines stack along the normal so the *further* line reads first; check overlaps by
looking, not by arithmetic. Next: Sep 8 Jupiter occultation is a strong hook, equinox on
the 22nd, Harvest Moon on the 26th. Try a kumiko or a Malevich next for the formal slot.
