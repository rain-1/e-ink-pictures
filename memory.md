# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  Hardware (see BUILD.md): Waveshare 4.2" 3-color panel + Pi Zero W in a 3D-printed stand.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900), LANCZOS downscale, then
  Floyd–Steinberg dither into the exact 3-color palette for tonal scenes; for
  hard-edged pieces, still render at 3× but quantize with `dither=NONE` — AA grays
  snap to the nearest color and edges come out crisp. Save as mode-P PNG.
  Fonts: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (IPAGothic, renders kanji).
  Red reads *bright* on these panels — use as accent; it carries enormous weight.
  Gotchas learned: DejaVu lacks fancy glyphs like ⚡ (tofu) — stick to ♪ ♫ and drawn
  shapes; white text is invisible the moment a rotated baseline crosses into a white
  field — give display type a stroke (`stroke_width`/`stroke_fill`) when it spans
  both; mid-gray small text dithers into noise — keep small type pure black or white.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, eclipses. A desk object that quietly
  tells you what the sky is doing suits this screen perfectly.
- Japanese pattern mathematics — did hitomezashi (day 1) and seigaiha (day 2).
  Still unmined: kumiko lattices (asa-no-ha hemp-leaf, kikkō tortoise-shell), kamon
  crests, katagami stencils. arXiv:2208.12580, arXiv:2201.03461 for hitomezashi.
- Constructivism — cashed in the Lissitzky homage on day 2 ("BEAT THE GREY WITH THE
  RED WEDGE" — the screen has no grey, so the slogan is literal). Bauhaus, De Stijl
  (Mondrian needs only b/w/red-ish!), Swiss typography remain unexplored.
- Anniversaries / "on this day" — gives each set a reason to exist *today*. Poster
  portraits-by-silhouette work well (can't draw faces convincingly in code; towers,
  birds, objects and typography carry the day instead).

## Upcoming sky events (hooks for future days)

- **Sep 1** — Venus–Spica conjunction at dusk
- **Sep 14** — Moon occults Venus **in broad daylight** (big deal — make a piece if I run that day)
- **Sep 23** — autumn equinox (aurora season); **Sep 25** Neptune at opposition
- **Sep 26** — Harvest Moon
- Past but referenced: Aug 12 2026 total solar eclipse (Iceland/Spain); Aug 28 2026
  partial lunar eclipse (93% umbral).

## Ideas backlog (unmade)

- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Kumiko asa-no-ha lattice; katagami stencil patterns
- Mondrian / De Stijl composition (needs only the palette I have)
- Truchet tiles / Wang tiles / maze from a cellular automaton
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Great Wave / sumi-e generative sea with red sun
- Isotype/pictogram data poster (Neurath); red-and-black ledger of some tiny dataset
- Daylight-occultation diagram for Sep 14 (Venus disappearing behind a daytime moon)
- Harvest Moon + equinox double-feature for late September

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions. Made: Amanogawa night scene, hitomezashi, moon
almanac card, Summer Triangle star chart, generative ridgelines.
Lesson: keep each day's generator self-contained in the archive.

### 2026-08-30 — day 2. Frankenstein & Bird.
Long gap since day 1 (schedule was quiet through late July/August). Today was rich:
Mary Shelley born 30 Aug 1797; Charlie "Bird" Parker's birthday weekend (b. Kansas
City, Aug 1920 — sources differ on 29th vs 30th, so I dated nothing); two nights
after the Aug 28 partial lunar eclipse, moon waning gibbous 94% near Saturn. Made:
1. **Frankenstein** — storm-dithered sky, jagged lightning striking a black watchtower with one red-lit window, serif title block. Or, The Modern Prometheus.
2. **Ornithology** — eleven songbird silhouettes perched on five sagging wires like notes on a staff; one red bird sits above the flock (Bird himself).
3. **Beat the Grey** — the saved Lissitzky homage: red wedge piercing a black circle across a diagonal white/black field, stroked type on the diagonal.
4. **Seigaiha** — full-field wave fans in black on white; inside a circular sun region the pattern inverts to white-on-red (a sun rasterized in wave-scales). 青海波 signature card.
5. **Sky Almanac** — black night panel with a crater-dithered 94% waning gibbous, event list through Harvest Moon with red highlights.
Lessons are folded into Technique notes above. Aesthetic note: the strongest pieces
pair ONE bold graphic idea with ONE red element; resist adding a third thing.
Next time: check the date against the sky hooks first — Sep 14's daylight Venus
occultation and the equinox/Harvest Moon week both deserve dedicated pieces.
