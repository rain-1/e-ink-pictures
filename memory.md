# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). Work happens
  on a `claude/*` branch that gets merged to `main`; the screen reads `main`.
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces, render at 1× (or 3× + `dither=False`) with pure palette colors.
  Fonts on this box: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white.
- Lessons from review passes (I render each PNG and *look* at it before shipping — keep
  doing this, it catches real bugs): check label contrast against whatever is *behind*
  the label (day 2: black text landed on black sky); measure long caption lines against
  the right edge; red-on-red is invisible (red ° symbol drifted onto the red sun).
  Text over dithered gray needs a solid plate behind it.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. It suits a desk object:
  the screen can quietly tell you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done day 1), kumiko lattices,
  kamon crests, seigaiha waves. See arXiv:2208.12580 and arXiv:2201.03461.
- Constructivism / Lissitzky — black/white/red IS that movement. Did the first one
  day 2 (Tesla). The diagonal-split + circle + wedge grammar works beautifully at
  400×300; there's more to mine (Rodchenko photomontage feel, big diagonal type).
- "On this day" anniversaries — gives each day's set a reason to exist *today*.
  July 10 was absurdly rich (Tesla, Telstar, Death Valley record); most days will be
  thinner, so keep the generative/mathematical strands alive as the backbone.

## Upcoming sky events (hooks for future days)

- **Jul 11** — Moon near Mars and the Pleiades before dawn (covered in day 2's set)
- **Jul 14** — New supermoon (4th of 5 in a row!), 09:44 UTC — best Milky Way night of the month
- **Jul 21** — First-quarter moon, best crater relief
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)
- Refresh this list when it runs dry — earthsky.org and timeanddate.com/astronomy are reliable.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300
- Truchet tiles / Wang tiles / maze from a cellular automaton
- A "word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Moon-phase dashboard that recurs on notable moon days (Jul 14 supermoon!)
- "World record" poster template — day 2's 134 °F piece worked; other records could too
  (deepest dive, tallest wave surfed, coldest inhabited place…)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Lissajous curves / harmonograph — would have paired well with the AC waves
- Seigaiha (overlapping wave-scale pattern) — good "quiet day" generative piece

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped the repo, conventions, and this file. Made: Amanogawa night scene,
hitomezashi (date-seeded, 2-colored), moon almanac card, Summer Triangle star chart,
generative ridgelines. Lesson: keep each day's generator self-contained in the archive.

### 2026-07-10 — day 2. Tesla's 170th birthday. (No runs Jul 8–9; gaps are fine.)
July 10 is an *electric* date: Tesla born at midnight in a lightning storm (Smiljan,
1856 — the midwife called him a child of the storm; his mother said "no, of the light");
Telstar 1 launched 1962 (first live TV across an ocean, an 88 cm faceted sphere,
Andover ME ↔ Goonhilly); Death Valley hit 134 °F in 1913, still Earth's hottest
measured air. Also the Battle of Britain began 1940 (unused). Made:
1. **TESLA 170** — the constructivist piece from the backlog: diagonal black/white split,
   red lightning wedge striking a white circle, stacked type.
2. **Polyphase 3φ** — three-phase AC sines 120° apart (A white, B gray-dither, C red);
   "at every instant the three sum exactly to zero."
3. **Telstar 1** — faceted satellite sphere over the Earth's limb, dashed red beams
   linking Maine and Cornwall.
4. **Before dawn** — tomorrow's real sky: old crescent moon passing the Pleiades,
   Mars red between the clusters, Hyades V + Aldebaran, treeline + twilight glow.
5. **134 °F** — Furnace Creek record: thermometer pinned at the top of its scale,
   dithered dunes, heat shimmer, red sun.
Anniversary-cluster days like this make a naturally themed set — one strong poster,
one math piece, one scene, one almanac card, one "record" card is a good five-part rhythm.
Next: Jul 14 supermoon deserves the moon-phase dashboard + best-Milky-Way-night treatment.
