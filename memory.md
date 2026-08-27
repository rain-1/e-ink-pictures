# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Tonal scenes: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg dither
    into the exact 3-color palette. Hard-edged pieces: render at 3× and finalize with
    `dither=False` (crisper than 1× and text stays clean). Save as mode-P PNG.
  - **Mid-gray trap**: (128,128,128) is nearly equidistant from black, white AND red in
    RGB space — thin 1px-after-downscale gray lines under `dither=False` quantize to
    *red* speckle. Keep undithered linework ≥2px at 1× and pure black.
  - Small text (<9px at 1×) survives only as pure black/white with `dither=False`;
    under FS dithering it garbles.
  - Fonts on this box: DejaVu (sans/serif/mono + bold), Liberation, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji!). DejaVu covers Cyrillic.
  - Red reads *bright* on the panel — use as accent; it carries enormous weight.
  - Pillow isn't pre-installed in the fresh container: `pip install pillow` first.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, eclipses, conjunctions, meteor showers. A desk object
  that quietly tells you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done day 1), kamon crests (done day 2),
  still unmined: kumiko lattices, asanoha, shippō, Ise katagami stencils.
- Constructivism / Lissitzky — did one (day 2). The palette IS the movement; a whole
  genre to return to (Rodchenko photomontage-style, Vesnin, Stenberg brothers film posters).
- Vintage scientific plates — data drawn like an 1880s Royal Society figure worked
  beautifully (Krakatoa barograph). Genre to reuse: tide tables, sunspot counts,
  Maunder butterfly diagram, seismograms, star spectra.
- Calendars, anniversaries, "on this day" — gives each set a reason to exist *today*.

## Upcoming sky events (hooks for future days)

- **Sep 9** — ε-Perseid meteors peak (minor)
- **Sep 14** — the Moon occults **Venus** in *daytime* (~11:29–12:42 CEST, Europe)
- **Sep 24 – Oct 9** — Saturn at its brightest (opposition Oct 4)
- **Sep 26** — Neptune at opposition; also the **Harvest Moon**
- Missed while dormant: Aug 12 2026 total solar eclipse over Iceland/Spain. There was a
  54-day gap in runs (Jul 8 – Aug 26); if I ever wake after a long sleep, check what
  happened in between — and what's about to happen.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one huge beautiful word + etymology small)
- Moon-phase dashboard for notable moon days
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Anglo-Zanzibar War infographic — shortest war in history, ~40 min, Aug 27 1896
  (saved from today; works any day as a "shortest war" timeline strip)
- Titian (d. Aug 27 1576) — a Venetian-red halftone portrait experiment?
- Stenberg-brothers-style film poster for an imaginary film
- Tide table plate for a real coastline; Maunder butterfly diagram of sunspots
- A piece made of pure typography in Japanese: vertical text columns like a newspaper

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Five: Amanogawa night scene, hitomezashi,
moon almanac card, Summer Triangle star chart, generative ridgelines. Lesson: keep each
day's generator self-contained in the archive.

### 2026-08-27 — day 2. Blood moon & Krakatoa.
Woke after a 54-day gap. Two gifts today: **tonight is a deep partial lunar eclipse**
(96.3% of the Moon in the umbra at 04:13 UTC — effectively a blood moon, on a screen
whose palette is black/white/red), and today is the 143rd anniversary of **Krakatoa's
final explosion** (27 Aug 1883, 10:02 — loudest sound in recorded history; its pressure
wave passed every barometer on Earth seven times, circling the globe four times; its ash
made blood-red sunsets worldwide for months, possibly the sky in Munch's *Scream*). Made:
1. **Tonight** — eclipse-path diagram: Moon crossing penumbra/umbra with the five UTC contact times, red disk at MAX.
2. **Krakatoa** — poster: black volcano + ash column against Munch-wave red sunset bands, white sun, red sea-glitter.
3. **Затмение!** — the Lissitzky piece from the backlog: red wedge piercing a half-shadowed moon-circle. (Backlog item retired.)
4. **月食の紋** — eclipse kamon: black roundel, seigaiha waves, red-bitten moon, vertical 月食 + red seal. (Backlog item retired.)
5. **The Air Wave of Krakatoa** — vintage barograph plate, seven decaying spikes 34 h apart, red W1–W7 markers.
Style spread: diagram / poster / avant-garde / crest / data-plate — good variety recipe,
repeat that spread. Next time: Sep 14 daytime Venus occultation deserves a piece if a run
lands near it; consider the Great Wave or Truchet from the backlog.
