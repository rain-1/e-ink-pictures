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
- Technique notes that work: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg
  dither into the exact 3-color palette for tonal scenes; `dither=False` for hard-edged
  graphic pieces (AA edges snap cleanly to the palette). Save as mode-P PNG.
  Fonts: DejaVu (sans/serif/mono), Liberation, and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji OK).
  Red reads *bright* — use as accent, it carries enormous weight.
- **Dither lessons (day 2):** a full-frame gray gradient dithers into noise that drowns
  text, thin lines, and dark-red glows. Keep gradients confined (e.g. hugging the
  horizon), draw all labels/linework in *pure palette colors* only, and never use dark
  red (`#8B0000`-ish) on a dithered ground — it speckles. A bright planet = pure-red
  disc + white core + thin red diffraction spikes; reads beautifully.
- Pillow isn't preinstalled in the container — `pip install pillow` at the top of each run.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, conjunctions, meteor showers. A desk object that
  quietly tells you what the sky is doing tonight.
- Japanese pattern mathematics — hitomezashi (done day 1), kamon crests (generator built
  day 2 — circles + n-fold symmetry + maru-ni enclosure; endless seed/motif variations
  left: tomoe swirls, seigaiha waves, kumiko lattices). See Felicia Tabing's Bridges 2018
  paper on kamon drafting math.
- Constructivism — spent the saved Lissitzky idea on day 2 (Dylan poster). The palette
  still IS the movement; more compositions possible but don't repeat too soon.
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.
  Anniversaries of *artworks* (Warhol day 2) are a rich seam: art about art.

## Upcoming sky events (hooks for future days)

- **Jul 11** — Moon near Mars and the Pleiades (pre-dawn)
- **Jul 14** — New supermoon (4th of 5 in a row!), 09:44 UTC — best Milky Way night of
  the month. *Also Bastille Day* — tricolor minus blue = our palette. Double feature?
- **Jul 21** — First-quarter moon, best crater relief
- **Jul 31** — double meteor shower (α Capricornids + Southern δ Aquariids)
- Refresh this list when it runs low: search "night sky this month" (Planetary Society,
  EarthSky, whenthecurveslineup.com are good).

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology small)
- Moon-phase dashboard that recurs on notable moon days (Jul 14 supermoon!)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Kamon II: tomoe (comma-swirl) or seigaiha motif, different symmetry
- Tarot-card / playing-card frame layout — ornamental border + one central emblem
- Isotype/pictogram statistics poster (Neurath) — b/w/r was literally Isotype's palette
- Swiss/International-style grid poster with one huge numeral (the date)

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo, conventions, this file. Made: Amanogawa night scene, hitomezashi,
moon almanac card, Summer Triangle chart, generative ridgelines. Lesson: keep each
day's generator self-contained in the archive.

### 2026-07-09 — day 2. Conjunction day. (No run on Jul 8 — schedule started Jul 7,
then skipped a day; don't assume daily continuity, always check the date.)
Researched: Venus–Regulus conjunction TONIGHT (1.1° apart, closest of the year, look
west 45 min after sunset, Venus −4.1 vs Regulus +1.4); July 9 anniversaries — Argentina
independence 1816 (210 years!), Warhol's Soup Cans debut at Ferus Gallery 1962, Dylan
recorded "Blowin' in the Wind" 1962; Sun of May construction (32 rays: 16 straight +
16 wavy, serene face); kamon drafting rules (pure circles/lines, n-fold symmetry,
maru-ni format). Made:
1. **Venus passes Regulus** — twilight chart, Sickle of Leo, red-blazing Venus, tonight's real sky.
2. **Sol de Mayo** — Argentina bicentennial-plus-ten poster; red wavy rays alternate black straight ones.
3. **Blowin' in the Wind** — constructivist poster; red wedge as the wind, black circle as "THE ANSWER".
4. **Kamon** — generative 6-petal crest, date-seeded, red hanko seal reading 七月九日.
5. **Soup!** — 12-can pop grid in rotating b/w/r colorways for the Ferus anniversary.
Next time: Jul 11 moon–Mars–Pleiades if running that day; Jul 14 supermoon + Bastille
deserves the moon-dashboard treatment. Maybe the Great Wave for a no-event day.
