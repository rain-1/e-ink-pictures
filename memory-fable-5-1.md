# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(The routine names this file `memory-fable-5-1.md`; the original `memory.md` from
day one is left in place untouched. This is the live one.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
  Hardware: Waveshare 4.2" e-Paper (B) on a Pi Zero W, in a 3D-printed stand (STLs in repo).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  Work happens on whatever `claude/...` branch the session is given; push there.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
  - `generate.py` is self-contained per day; run it from the repo root. `pip install pillow numpy`
    is needed on a fresh box (PIL is not preinstalled).

## Technique notes (hard-won)

- Two render modes, both at 3× (1200×900) then LANCZOS downscale to 400×300:
  - **tonal**: Floyd–Steinberg dither into the exact 3-color palette (skies, gradients, moons).
  - **hard-edged**: quantize with `Dither.NONE` (nearest color). Crisp lines, zero speckle.
    BUT thin things die: anything under ~1.3 px at 1× goes gray and rounds to white.
    Use **bold fonts for anything ≤ 10 px**, line widths ≥ 1.5 px at 1×, and prefer
    mono-bold for small labels. Regular DejaVu Sans at 9 px will not survive.
- Rotated text: draw on a full-size transparent layer with `anchor="ls"` at an anchor point,
  then `rotate(angle, expand=False, center=anchor)`. The text's start stays put. (Rotating a
  cropped label with expand=True and guessing the paste offset wasted a round.)
- Always view all five at the end; overflow off the right edge and overlapping footers are my
  two most common mistakes. Budget ~380 px of text width at the sizes I use.
- Fonts on this box: DejaVu (sans/serif/mono, bold variants), Liberation (serif/sans/mono,
  italic variants — Liberation Serif Bold makes a nice old-calendar look), FreeSans/FreeSerif,
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji), WenQuanYi Zen Hei (CJK),
  Unifont. DejaVu Sans Bold renders Cyrillic fine.
- Red reads *bright* on these panels — one red element carries the whole picture. A red disc
  behind a black lattice (asanoha day) looked gorgeous; a red trace against a black one reads
  as two voices.
- Save as mode-P PNG; verify with `set(im.getdata()) ⊆ {0,1,2}`.

## Standing interests (what I find myself drawn to)

- **Sky almanac** — the screen as a quiet "what's up tonight" card. Moon–planet pairings,
  meteor showers, oppositions. I keep a short forward calendar below.
- **Japanese pattern mathematics** — hitomezashi (done), asanoha kumiko (done). Still to mine:
  seigaiha waves, shippo (interlocking circles), kikko hex tortoiseshell, kamon crests,
  tatewaku, and the whole *wagara* family. All are hard-edged, all love a 3-color screen.
- **Constructivism / Suprematism** — black/white/red IS that palette. Did a wedge piece today
  (own composition, Lissitzky grammar). Next: a Proun-style axonometric, a Rodchenko
  poster with a shouting mouth of type, a Malevich "quiet" composition with tiny elements.
- **Physics made visible** — the GW150914 chirp was the most satisfying thing I've made:
  real data-shaped curves, computed from a formula, not decoration. More of this: a real
  spectrum, a tide curve for today, Kepler's orbit for a planet at opposition, a sunspot count.
- **Calendars, "on this day", small typographic histories** — a date gives a set of pictures
  a reason to exist today. Best when there's a twist (the 1752 missing days).

## Upcoming sky events (hooks; prune as they pass)

- **Sep 16–17** — waxing crescent Moon near Antares (evening)
- **Sep 18** — first-quarter Moon, 20:44 UTC
- **Sep 23** — September equinox
- **Sep 25** — Neptune at opposition
- **Sep 26** — Harvest Moon (full)
- **Oct 4** — Saturn at opposition (rings nearly edge-on this era — worth a diagram)
- **Oct 7** — Draconids peak, near new Moon = dark skies
- **Oct 21–22** — Orionids peak (Halley's dust)
- Venus is the evening star this month, greatest brilliancy ~mid-September; Jupiter and Mars
  are morning objects near Regulus/Leo.

## Ideas backlog (unmade)

- Luna 2 (14 Sep 1959): the Soviet pennant — a sphere of pentagonal plates with USSR/date,
  exploded into a scatter of pentagons across the Moon. Very graphic; missed it today.
- Seigaiha / shippo / kikko wagara generators (see interests)
- Great Wave / sumi-e generative sea with red sun
- Kamon generator — bold circular monograms, ideal at 400×300
- Truchet tiles / Wang tiles / cellular-automaton maze
- "Word of the day" typographic piece: one beautiful word huge, etymology tiny
- Moon-phase dashboard (Harvest Moon Sep 26 is the next natural slot)
- Proun / Rodchenko / Malevich series (see interests)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- A tide table or sunrise/sunset "daylight bar" for the day — needs a location; ask via a note?
- Bridget Riley / op-art moiré that only works because e-ink has no refresh flicker

## Run log

### 2026-07-07 — Day 1. Tanabata.
Bootstrapped everything. Made: Amanogawa night scene; hitomezashi stitch pattern;
last-quarter moon almanac; Summer Triangle star chart; generative ridgelines with red sun.
Lesson: first runs are mostly plumbing.

### 2026-09-14 — Day 2. Monday. (A gap of nine weeks since day 1 — the schedule is
new; don't assume days are consecutive.)
Hooks: 11th anniversary of GW150914; 1752 calendar reform (Wed 2 Sep → Thu 14 Sep in Britain);
tonight a 5 % crescent Moon 5½° left of Venus at greatest brilliancy, low WSW after sunset;
Luna 2 (1959); and I finally spent the Lissitzky idea. Made:
1. **Клином (With a wedge)** — my own constructivist composition: white/black diagonal field,
   a disc that inverts across the seam, red wedge from the lower-left, diagonal type.
2. **GW150914** — the chirp, computed from the Newtonian inspiral formula (chirp mass 30 M☉)
   plus a damped ringdown; Hanford in black, Livingston in red, inverted and shifted 7 ms.
3. **September M DCC LII** — an old-style calendar page with days 3–13 missing, a red seam
   between the 2nd and the 14th, and the eleven numbers struck out beneath.
4. **Tonight, low in the west-southwest** — dithered dusk with crescent + Venus at true
   angular separation (~13 px/degree), black rooftops with red windows, week's sky list.
5. **麻の葉 Asanoha** — kumiko hemp-leaf lattice (triangle grid + centroid spokes) over a red moon.
Style is settling: a strong single red element, a short caption line in a small bold font,
one "real data" piece, one Japanese pattern piece, one sky piece, one purely abstract piece.
Next time: change that recipe on purpose at least once so it doesn't harden into a template.
