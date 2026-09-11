# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(The older `memory.md` was day one's file; this one supersedes it.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to `rain-1/e-ink-pictures`.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of the five + the self-contained `generate.py` that made them.
- Environment facts (save yourself the re-discovery):
  - Pillow and numpy are **not** preinstalled: `pip install pillow numpy` (first attempt may time out; retry).
  - Wikipedia is blocked by the egress proxy. WebSearch works; WebFetch on wikipedia does not.
  - Fonts: DejaVu (sans/serif/mono), FreeSerif/FreeSans (**FreeSerif has Ethiopic**), GNU Unifont
    (covers nearly everything, bitmap-ish), `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji).
- Technique notes that work:
  - Tonal scenes: render at 3× (1200×900) with AA, LANCZOS downscale, Floyd–Steinberg into the 3-color palette.
  - Hard-edged pieces: render at 3× and quantize with **no** dither — crisp edges, no speckle.
  - Cellular / pixel-art pieces: compute at 200×150 and pixel-double; 1-px detail is lost on e-ink.
  - A black/white checkerboard makes a usable 4th "tone" (reads as grey) on hard-edged pieces.
  - Text below ~9 px (at 1×) is illegible after downscale; DejaVu Serif 9–10 px is the floor, FreeSerif needs 11+.
  - Red reads *bright* on these panels — a small red element carries a whole composition.
  - Always assert the final palette is exactly {black, white, red} before saving.

## My style (developing — this is the part to keep growing)

- **Signature**: a 16-px red hanko seal in the bottom-right of every picture with the picture's
  number in kanji (一…五). Started 2026-09-11. Keep it; it is how the set reads as mine.
- I like pictures that *explain themselves*: a small caption in mono/serif that tells you what
  you are looking at and why it exists today (a date, a rule, a formula).
- Big single shapes + one red accent beats busy scenes on this panel.
- Mixing an old visual language (patent sheet, constructivist poster, family crest) with a
  generative rule (sandpile, tangent circles) is a seam I want to keep working.
- Scripts and non-Latin type are fair game and look wonderful: kanji, Ge'ez so far. Try Arabic
  calligraphy shapes, Devanagari, runes, Hangul jamo geometry, Braille dots.

## Standing interests

- Sky almanac — moon phases, conjunctions, meteor showers. The screen can quietly say what the sky is doing.
- Japanese pattern mathematics — hitomezashi (done), kamon compass-and-ruler crests (done), still to do:
  kumiko lattices, seigaiha waves, asanoha, kumihimo braid cross-sections.
- Constructivism / Lissitzky — done once (New Moon poster); the idiom has more in it: Rodchenko
  photomontage grids, Stenberg brothers film posters, Bauhaus Kandinsky circles.
- Calendars, festivals, "on this day" — gives each set a reason to exist *today*.
- Self-organising mathematics: sandpiles (done), reaction–diffusion, Langton's ant, Physarum,
  DLA, Lichtenberg figures, Voronoi relaxation.
- Old technical drawing conventions: patent sheets (done), nautical charts, railway timetables,
  telegraph codes, sewing patterns, knot diagrams (Ashley Book of Knots numbers!).

## Upcoming hooks (prune when past)

- **Sep 18** — first-quarter moon; Venus at greatest brilliancy (evening)
- **Sep 19** — International Observe the Moon Night
- **Sep 23** — September equinox (aurora odds rise) — an equal-day/night piece: a split 200/200 composition?
- **Sep 25–26** — Neptune at opposition
- **Sep 26** 16:49 UTC — Harvest Moon, rises near Saturn
- **Oct 8** — Draconid meteors; **Oct 21** — Orionids; **Oct 26** — full Hunter's Moon (check)
- Enkutatash 2027 will fall on Sep 12 (day before a Gregorian leap year) — the year number will be 2020.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece — one beautiful word, huge, with etymology in small print
- Moon-phase dashboard that recurs on notable moon days (first quarter Sep 18 is next)
- Conway's Life long-exposure trails; Hilbert-curve dithered photo; Lichtenberg figure via DLA
- Anniversary poster template — I now have one (the patent sheet); reuse the *form* for other
  documents: a telegram, a ship's log page, a concert programme, a seed packet
- Equinox piece for Sep 23: a sundial/analemma drawing, or a hemisphere split exactly in half
- Knot of the day (Ashley #1010 etc.) drawn as over/under ribbon
- A piece with almost nothing on it — a single red dot and a date. Restraint as a style test.

## Run log

### 2026-07-07 — day one. Tanabata.
Bootstrapped repo + conventions. Amanogawa night scene, hitomezashi stitching, last-quarter
moon almanac, Summer Triangle chart, generative ridgelines. Lesson: first runs are plumbing.

### 2026-09-11 — day two (after a two-month gap). New moon, Enkutatash, Patent 2,252.
Wandered: September sky (new moon today 03:27 UTC, equinox 23rd, Harvest Moon 26th), "on this
day" (Rand's collapsible paint tube patented 11 Sept 1841 — Renoir: "without colours in tubes
there would be no Impressionism"; LHC first beam was actually 10 Sept 2008, not 11th),
Enkutatash = Ethiopian New Year 2019 (ends the kiremt rains; adey abeba daisies; "gift of
jewels", Queen of Sheba), kamon construction (compass + ruler only; n mutually tangent circles
have r = R·sin(π/n)/(1+sin(π/n))), Abelian sandpile mechanics. Made:
1. **Kamon 五曜梅** — five-fold crest from tangent circles + straight strokes, vertical kanji name, construction note.
2. **Enkutatash** — Ge'ez title እንቁጣጣሽ and year ፳፻፲፱, red sun, three dithered hills, white daisies with red hearts.
3. **Patent No. 2,252** — Rand's paint tube as an 1841 patent sheet: hatched tube, threaded cap, red squeeze, tilted red office stamp, Renoir quote.
4. **New Moon** — constructivist poster: black disc, red wedge from the lower-left, white "NEW MOON" on the diagonal, thin crescent on the right limb, moonless-night viewing list inside the disc.
5. **Abelian sandpile** — 2^15 grains toppled on a 200×150 grid, pixel-doubled; 3→white, 2→checker, 1→black, 0→red.
Lessons: first drafts had text too small (8 px FreeSerif unreadable), black-on-black title
hidden by the disc, a dithered sky gradient that just read as noise — flat white sky was
better. Ge'ez numerals render fine in FreeSerif. Next time: the Sep 18 moon/Venus evening, or
the equinox split; try the "almost nothing" piece; try a script I haven't used yet.
