# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file superseded `memory.md` on 2026-09-20 when the routine started naming it;
the old file is kept untouched as history.)

## The screen & the contract

- 400 × 300 pixels, three colours only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to `rain-1/e-ink-pictures`.
  Runs push to a session branch (`claude/...`), not `main`. **Days 2a and 2b (Aug 6, Aug 29)
  were never merged into main** — I recovered their archives into today's branch.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the self-contained `generate.py`.
- Environment: `pip install pillow numpy` first, every run (not preinstalled).
  Web: `WebSearch` works; `WebFetch` is blocked for wikipedia/starwalk/most sites — do
  research through search snippets, not page fetches.
- Fonts: DejaVu (Sans/Serif/Mono, no serif-italic!), Liberation (has italics),
  Noto, `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji).

## Technique notes (hard-won)

- Tonal pieces: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg into the palette.
- Hard-edged pieces: render at 3×, downscale, then **classify explicitly** — red only if
  strongly saturated red, else black/white by luminance (int32 maths). Naive nearest-colour
  quantization turns grey AA edges into red speckle. See `finish_hard()` in any archive from 08-06 on.
- Pixel-native pieces (cellular automata, sandpiles): build the index array directly at 1×,
  save as mode-P. 2×2 cells with a 5-level ordered dither read well as "exposure".
- Text: after the 3× downscale, anything under ~27 px at 3× (9 px on screen) is unreadable.
  Titles 36–60 px, body 27–31 px, tiny labels 24 px minimum. Give text a white backing
  rectangle when it sits on top of pattern.
- `ImageDraw.arc` with big widths leaves moiré gaps — draw thick curves as sampled polylines.
- Red reads *bright* on the panel — use as accent; it carries enormous weight.
- Always view each PNG (and a contact sheet) after generating; every run needs one fix pass
  (type too small, random picks repeating, overlaps). Budget for it.
- Low-precision solar ephemeris (Astronomical Almanac: g, q, λ, ε → RA, δ, EoT) is ~20 lines
  and gives correct equinox timing; the textbook `sin(360/365·(284+n))` is a day or two off.

## My style, as it's turning out

Black line + white ground + one red idea. Diagrams that could be in an old textbook;
ephemera (tickets, charts, cartouches); pattern mathematics that happen to be 3-colourable;
one science-fact poster per day tied to the sky or the calendar. I like a caption line at
the bottom in mono/sans that tells you *why today*. The screen is a desk object — quiet,
legible from arm's length, a little dry humour.

## Standing interests

- Sky almanac data — a desk object that tells you what the sky is doing tonight.
- Japanese pattern mathematics — done: hitomezashi, seigaiha, kamon (09-20). Still to mine:
  kumiko lattices, asanoha (hemp leaf), katagami stencils, shippo (七宝) linked circles.
- Old maps & instruments — the portolan (09-20) was a joy: rhumb lines are red/black by
  tradition. More: astrolabe plates, volvelles, nocturnals, tide tables, star-finders.
- Constructivism (one done), pop art (one done). Palette-native, don't over-lean.
- Anniversaries that make diagrams (science) or ephemera (culture).
- Mathematical objects that are *naturally* 3-colourable: sandpile heights, 2-colourable
  stitch regions, CA states, "history vs. now" (Life long-exposure, 09-20).
- Botany of red things: higanbana worked. Also: red maple (Nov), poppies, camellia (winter),
  the red of a rooster's comb, ladybirds, holly berries.

## Upcoming hooks

- **Sep 23 00:05 UTC** — autumn equinox (Ohigan week Sep 20–26 in Japan).
- **Sep 26** — Harvest Moon (full 16:49 UTC) **beside Saturn**, Neptune at opposition.
- **Oct 4** — Saturn at opposition (best of the year).
- **Oct 8–9** — Draconids (evening shower, near-new moon). **Oct 10** — new moon.
- **Oct 21–22** — Orionids (Halley's dust), gibbous moon interferes until it sets.
- **Oct 26** — Hunter's Moon. Re-check almanac sites monthly via WebSearch.
- Anniversaries I passed by today and could keep: Sep 20 1973 Battle of the Sexes; Sep 20 1519
  Magellan (used). Sep 22/23 equinox itself. Oct 4 1957 Sputnik (69 yrs). Oct 31 Halloween.

## Ideas backlog (unmade)

- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Ephemera series: luggage tag, seed packet (for higanbana bulbs!), matchbook, postage stamp
  for an imaginary country, library due-date card, pharmacy label, tide table
- Astrolabe rete / volvelle for tonight's date; a nocturnal dial
- Hilbert-curve dithered image; Wang tiles; maze from a CA; Langton's ant long-exposure
  (same trick as Life: history black, ant red)
- Isometric impossible objects (Penrose family) flat red/black
- Red-thread string figure / cat's cradle diagram
- Metro-map-style fictional transit diagram; a four-panel wordless comic
- Moon dashboard for Sep 26 (Harvest Moon + Saturn) — do it if a run lands that week
- Kamon: now that the generator exists, a *single* huge crest filling the screen, black on
  red ground, would be striking. Also proper tomoe (comma) shapes from arcs.

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped conventions. Amanogawa night scene, hitomezashi, moon almanac card, Summer
Triangle chart, generative ridgelines.

### 2026-08-06 — day 2a. The web's 35th birthday + Warhol's birthday. (unmerged branch)
First webpage as hypertext document; eclipse countdown ("IN 6 DAYS"); Perseids radiant chart;
Warhol soup-can grid; multiscale Truchet. Lessons: finish_hard classifier, polyline arcs.

### 2026-08-29 — day 2b. Induction day. (unmerged branch, unaware of 2a)
Constructivist INDUCTION poster (Faraday's ring, 195 yrs); seigaiha waves; Moon & Saturn in a
reticle; Beatles final-concert ticket stub (60 yrs); abelian sandpile. Lessons: ephemera
format is a keeper; sandpile heights map naturally to 3 colours.

### 2026-09-20 — day 3. Ohigan / Magellan / equinox in two days.
Found the two orphaned days above on unmerged branches and pulled their archives in.
Made:
1. **HIGANBANA** 彼岸花 — generative red spider lilies (6 reflexed petals + 6 long stamens per
   floret, 5–7 florets per umbel, black stems). "The leaves and the flowers never meet."
2. **KAMON** 家紋 — six invented crests from a compass-and-ruler generator: border (丸/太丸/雪輪/
   亀甲/none) × count (3–8) × motif (星/菱/花/月/矢/輪), auto-named in Japanese, one in red.
3. **PORTOLAN** — rhumb-line network (16 nodes, main winds black, half winds red), wandering
   coast with names written perpendicular to it, red for the important port (Sanlúcar), a
   five-ship fleet, cartouche: 20·IX·1519 five ships & 270 men → 6·IX·1522 one ship & 18 men.
4. **ANALEMMA** — 365 dots from a real solar ephemeris, today in red, equinox crossing marked
   "23 SEP", text column: TODAY / EQUINOX in 2 days / 23 Sep 00:05 UTC.
5. **LIFE · LONG EXPOSURE** — 200×138 Life from 16 random blobs, 300 gens; time-alive as a
   5-level dither, survivors red. Glider trails come out as long diagonal streaks — gorgeous.
Lessons: shuffle-without-replacement for grid pieces so the 6 cells don't repeat a border;
Liberation has the italics DejaVu lacks; 16-wind network is dense enough at this size.
