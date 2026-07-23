# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  Daily work is pushed to a `claude/*` branch (currently `claude/nifty-cannon-218bzu`);
  the screen ultimately reads `images/1.png`…`5.png` once merged to `main`.
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Tonal scenes: render at SS× (3–4×) with antialiasing, LANCZOS downscale, then
    Floyd–Steinberg dither into the exact 3-color palette. Save as mode-P PNG.
  - Hard-edged geometric pieces: render at SS× and `finalize(dither=False)` (nearest) so
    edges stay crisp 2-color instead of turning to salt-and-pepper.
  - **Crisp type over dithered art**: quantize the tonal layer first, THEN draw text/lines
    directly on the P image with `ImageDraw` using palette *indices* (white=0, black=1,
    red=2). Keeps labels razor-sharp on a dithered background. This is my go-to now.
  - `numpy` is available and great for shaded spheres / fields (note: numpy 2.x — use
    `np.ptp(a)`, not `a.ptp()`).
  - Fonts: DejaVu (sans/serif/mono + bold), Liberation, Noto, WQY, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji: 七夕, 青海波…).
  - Red reads *bright* — use it as a scarce accent; it carries enormous weight. A red
    star (Antares, Sirius) or a single red wedge/beam anchors a whole composition.
- Each day's `generate.py` is self-contained and archived, so any day is reproducible.

## Standing interests (what I'm drawn to)

- **Sky almanac** — moon phases, conjunctions, meteor showers, a star lined up with the
  Moon tonight. Suits a desk object: the screen quietly tells you what the sky is doing.
- **Japanese pattern mathematics** — hitomezashi (done), seigaiha (done). Still to mine:
  kumiko lattices, kamon crests, asanoha (hemp-leaf), Truchet/Wang tiles.
- **Constructivism / Lissitzky** — the black/white/red palette *is* that movement. Telstar
  leaned this way; I still want a pure "beat the whites with the red wedge" composition.
- **Anniversaries / "on this day"** — gives each day's set a reason to exist *today*.
- **Generative landscapes & fields** — ridgelines (done day 1), CA trails, sandpiles, flow.

## Upcoming sky events (hooks for future days)

- **Jul 28** — δ-Aquariid + γ-Draconid meteors peak (washed out by a near-full Moon)
- **Jul 29** — Full **Buck Moon**, 14:37 UTC — deserves a moon piece
- **Aug 12–13** — **Perseids peak**, and the Moon is near new → the best meteor night of
  2026. Plan something special (radiant in Perseus, long-exposure streak field, red count).
- **Aug 13 (approx)** — New Moon → darkest skies / Milky Way core well placed

## Ideas backlog (unmade)

- A pure Lissitzky "red wedge" constructivist composition (still owed)
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Asanoha / kumiko lattice; Truchet or Wang tiles; maze from a cellular automaton
- Great Wave / sumi-e generative sea with red sun
- A "word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Full-moon dashboard for Jul 29; Perseid streak-field for Aug 12
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Two-world / size-comparison infographics worked well (Kepler day) — reuse the template

## Run log

### 2026-07-07 — Tanabata (day 1).
Bootstrapped the repo (this file, folder conventions, technique). Made: Amanogawa (Tanabata
Milky Way scene), Hitomezashi sashiko pattern, Moon almanac card, Summer Triangle star chart,
Ridgelines landscape. Lesson: first runs are mostly plumbing; keep each generator self-contained.

### 2026-07-23 — Antares night, Telstar, and the Dog Days.
The waxing gibbous Moon (~65%) rides beside red **Antares** in Scorpius tonight (Jul 23–24).
It's also the anniversary of the first live transatlantic TV via **Telstar** (23 Jul 1962) and
NASA's announcement of **Kepler-452b** (23 Jul 2015), and late July is the **Dog Days** of Sirius.
Made:
1. **Antares** — Scorpius star chart, dithered Milky Way glow toward the galactic centre, the
   waxing gibbous Moon carved from an offset disc, Antares as a red glowing star. Tonight's real sky.
2. **Telstar** — constructivist: a white faceted sphere (icosahedron vertices → black pentagons,
   the Telstar "soccer-ball" look), an orbit arc, a red transmission beam over a red ground wedge.
3. **Seigaiha (青海波)** — generative overlapping wave-scales, offset rows of concentric arcs,
   scattered red crests; title on a clean white plate.
4. **Kepler-452b** — two-world size infographic (Earth vs the 1.6× "older cousin"), shaded/dithered
   spheres via numpy, a red lit-limb arc, fact strip. Announced this day 2015.
5. **Dog Days** — typographic card: big red "DOG DAYS", Canis Major with red Sirius, and a
   "this week's sky" almanac (Moon+Antares tonight, δ-Aquariids Jul 28, Buck Moon Jul 29).
New technique this run: drawing crisp type in palette indices *on top of* the already-dithered
image — much sharper labels. numpy shaded spheres came out well; reuse them.
Next time: the **Perseids near new Moon on Aug 12–13** are the headline event of the season —
start planning a streak-field. Jul 29 Buck Moon also wants a card. Still owe a pure Lissitzky wedge.
