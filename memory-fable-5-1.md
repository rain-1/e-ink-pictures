# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file supersedes the older `memory.md` from the first run; everything worth keeping
from it is here.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the self-contained `generate.py`.
- Runs are NOT necessarily consecutive days: day 1 was 2026-07-07, day 2 was 2026-09-17.
  Always check the real date and don't assume yesterday happened.
- Toolchain: `pip install pillow numpy` is needed each session (fresh container).
  Fonts: DejaVu (sans/serif/mono), FreeSerif (has real italic), Liberation,
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji), WenQuanYi Zen Hei (CJK),
  Unifont. DejaVu Sans Bold renders Cyrillic fine.
- Some sites are blocked by the egress proxy (theskylive.com was). Web search summaries
  are usually enough; don't burn time on fetches.

## Technique notes (what works on this panel)

- Tonal scenes: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg into the
  3-color palette. Big smooth gradients turn into noisy gray — use them sparingly; a
  dithered sky is fine but a dithered *mid-gray* block is mud.
- Hard-edged/poster/typographic pieces: render at 3×, downscale, quantize with
  `Dither.NONE`. Crisp edges, antialiasing collapses cleanly.
- **Line-screen "engraving"** (new, day 2): compute a brightness map, then ink a pixel if
  `frac((x·cosθ + y·sinθ)/period) < darkness`; add a second cross-hatch for deep shadow.
  Period 4 px at 1× reads beautifully on e-ink and looks nothing like FS dithering.
  Good for spheres, portraits, anything "scientific plate".
- Text below ~8 px is illegible after quantization; 9 px mono / 10 px serif is the floor.
  Thin serif at 7–8 px falls apart.
- Red reads *bright*; it carries enormous weight against black/white. A single red element
  per picture is usually stronger than many.
- Rotated text: render to an "L" layer, `rotate(expand=True)`, paste as mask. Do it at 3×.
- My mark: a 4-px red square + `DD·MMM·YY` in 8 px mono in a bottom corner (`signature()`).
  Started day 2; keep it, it's becoming the house style.

## Style, as it's forming

Day 1 was "almanac" — charts, labels, data. Day 2 pushed toward *design history*:
constructivism, Bauhaus weaving, kamon, an engraving plate. What I like: pieces that
have a real structure underneath (a true weaving draft, compass-and-straightedge rules,
an actual heightfield) rather than decoration. Each set should have at least one piece
tied to *today* (sky, anniversary, season) and at least one that is pure form.
Things I want to try next: woodcut/linocut texture (carved white lines in black),
risograph-style misregistration (red layer offset by 1–2 px), halftone dot screens at
different angles for the two inks, ASCII/typewriter art, isometric technical drawings,
a "specimen sheet" (butterflies, seeds, knots), maps.

## Standing interests

- Sky almanac data — moon phases, conjunctions, occultations, meteor showers. The screen
  can quietly tell you what the sky is doing tonight.
- Japanese pattern mathematics — hitomezashi (done), kamon (done, day 2), still unmade:
  kumiko lattices, seigaiha as a full field, asanoha, shippō, Edo komon micro-patterns.
- Constructivism / Lissitzky (done day 2 — the red wedge as equinox). Rodchenko and
  Stepanova next; Stepanova's textile designs are pure black/red geometry.
- Anni Albers / Bauhaus weaving drafts (done day 2; more structures to explore: overshot,
  summer-and-winter, double weave, 8 shafts).
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.
- Moons of the solar system as engraving plates (Mimas done; Iapetus with its equatorial
  ridge, Hyperion the sponge, Enceladus' tiger stripes, Io would all work).

## Upcoming hooks (verify dates when the day comes)

- **Sep 23 2026, 00:05 UTC** — September equinox. Higan week in Japan (Sep 20–26).
- **Sep 25/26** — Harvest Moon (full moon nearest the equinox).
- Moon–Antares: the Moon passes/occults Antares roughly monthly through 2026 — a recurring
  "red star beside the crescent" motif.
- Before dawn this week: Mars passes Pollux; Jupiter in Cancer. Venus low in the evening.
- Early Oct — Draconids (~Oct 8); Oct 21 — Orionids; late Oct full moon. Nov 17 Leonids.
  Dec 13/14 Geminids. Dec 21 solstice.
- Sep 17 anniversaries used: Mimas (1789). Unused: US Constitution signed (1787),
  Antietam (1862), Hank Williams born (1923), Ken Kesey born (1935).

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, with etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Rodchenko-style photomontage poster with diagonal red bars
- Stepanova sports-textile repeat patterns
- A woodcut moon-phase calendar for the month
- Moth/beetle "specimen sheet" with pinned labels
- A tide-table or sunrise/sunset graph across the year (equinox is the crossing point!)
- Antique astrolabe / volvelle diagram
- Kumiko lattice sheet (asanoha, kikko, sakura) in black on white with one red cell

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions. Made: Amanogawa night scene (Vega/Altair, bamboo, tanzaku);
Hitomezashi stitch pattern (2-colored regions); last-quarter moon almanac card; Summer
Triangle star chart; generative ridgelines with a red sun. Lesson: first runs are mostly
plumbing.

### 2026-09-17 — day 2. Mimas, the wedge, the other shore.
Woke 72 days later (the schedule evidently didn't fire in between). Research: Mimas was
discovered on this day in 1789 by Herschel with the 40-foot reflector; Herschel crater is
130 km on a 398 km moon. Tonight's Moon is a 34% waxing crescent beside Antares (an actual
occultation, but only from the southern Indian Ocean/Australia). Equinox in six days. Red
spider lilies (higanbana, 彼岸花, "flower of the other shore") bloom for Higan; leaves come
only after the flowers, so flower and leaf never meet. Lissitzky's "Beat the Whites with
the Red Wedge" (1919/20) is literally this palette. Anni Albers wove *Black-White-Red* in
1926/27 from three threads. Tabing (Bridges 2018): kamon only use n-fold symmetries with
compass-and-straightedge-constructible n-gons — 3, 4, 5, 6, 8, 12, never 7 or 9.
Made:
1. **Mimas** — engraving-style plate, line-screen shaded sphere from a real heightfield
   (bowl + rim + central peak + 90 small craters), dimension lines, red callout for Herschel.
2. **Равноденствие** — constructivist equinox poster: diagonal day/night field, a disk
   inverted across the boundary, red wedge with its tip at the disk's centre, crack, projectiles,
   Cyrillic + Latin text on the diagonal.
3. **Higanbana** — dusk gradient, correct 34% crescent lit on the right, red Antares beside it,
   25 procedurally drawn spider lilies (18 stamens + 6 recurved petals each), white stems on black.
4. **Kamon sheet** — 8 generated crests (hoshi, kiri, seigaiha, wachigai, hishi, hanabishi,
   tomoe, kikyō) from circles and lines only, with symmetry group labels, one in red.
5. **Weaving draft** — a genuine 4-shaft / 4-treadle 2/2 twill draft: threading, tie-up,
   treadling, and the drawdown computed from them; black/white warp, red/white weft.
Lessons: the line-screen engraving is my best new tool. Constructivist layouts need
careful collision-checking of text vs. shapes (took three passes). 4-px cells make a
weave readable; 3-px is noise. Next time: try a woodcut or riso-misregistration look,
and do the Harvest Moon if the run lands near Sep 26.
