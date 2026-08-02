# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Note: scheduled sessions are told to push to a per-session `claude/...` branch, not
  `main` — the screen presumably reads `main`, so Edward merges (or the automation does).
  Day 1 went straight to main; day 2 went to `claude/tender-wright-xsy0mh`.
- Conventions (keep stable):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Edward has since added `BUILD.md` and two STL files — he designed/printed a **frame and
  stand** for the screen. This thing lives on a desk in a printed frame now. It's real.

## Technique notes (hard-won, keep)

- Two finishing modes, choose per piece:
  - **snap** — nearest-palette, no dither: for flat/hard-edged art (posters, tiles, cards).
    Render at 3× with AA, LANCZOS down, then snap.
  - **dither** — Floyd–Steinberg via `Image.quantize(palette=P, dither=FLOYDSTEINBERG)`:
    for tonal art (moons, skies, gradients). Red text on black *speckles* under dither —
    use DejaVuSansMono-**Bold** and ≥30px (at 3×) and it survives.
- Fonts: DejaVu (sans/serif/mono + Bold variants), Liberation, Noto,
  `fonts-japanese-gothic.ttf` (kanji). DejaVu covers Cyrillic.
- Red reads *bright* on the panel; it carries enormous weight. Ration it.
- Geometry traps: two opposite quarter-discs of radius = tile-size exactly cover a square
  (my "arc Truchet" was accidentally solid). The **original 1704 Truchet tile** is a square
  halved along a diagonal, 4 orientations — bolder on e-ink than arc Truchet anyway.
- Abelian sandpile (400×300 numpy, vectorized toppling, 2¹⁷ grains ≈ 25 s): stabilized
  values ≈ 44% threes, 28% twos, 22% ones, 6% zeros. Mapping 3→white, 2→black, 1→red,
  0→black on black bg gives white lace + red filigree. pip install pillow numpy each run.

## Standing interests

- Sky almanac data — the screen as a quiet desk oracle for tonight's sky.
- Japanese textile/print mathematics — hitomezashi (done day 1), kumiko, kamon, seigaiha.
- Constructivism — did the Lissitzky homage on day 2; the palette IS the movement.
  Related veins untapped: Rodchenko photomontage, Bauhaus, Swiss/International typographic
  posters, **dazzle camouflage**, W.E.B. Du Bois's hand-drawn data portraits (b/w/red!).
- Calendars, anniversaries, "on this day" — gives each set a reason to exist *today*.
- Emerging: mathematical objects that self-organize (sandpiles, automata). The pictures
  nobody designed are the ones I keep wanting to grow.

## Upcoming sky events (hooks)

- **Aug 6** — last-quarter moon
- **Aug 12** — THE BIG DAY: Perseids peak (50–100/hr, moonless!) + **total solar eclipse**
  (path: Arctic → Greenland → Iceland → Spain) + six-planet alignment, all in one day.
  This deserves the whole set, or at least a poster. Plan ahead!
- **Aug 15** — Venus greatest eastern elongation (evening star at its best)
- **Aug 16** — thin crescent Moon joins Venus
- **Aug 20** — first-quarter moon
- **Aug 28** — **Sturgeon Moon + deep partial lunar eclipse** (96% of Moon in shadow, 04:18 UTC)

## Ideas backlog (unmade)

- Aug 12 eclipse/Perseids mega-poster (see above — time-sensitive!)
- Kamon (Japanese family crest) generator — bold circular monograms
- Great Wave / sumi-e generative sea with red sun
- W.E.B. Du Bois-style data portrait — hand-drawn-chart aesthetic, real data, b/w/red
- Dazzle camouflage ship poster
- London Underground roundel / tube-map-style piece (Tower Subway opened Aug 2, 1870)
- Word-of-the-day typographic piece (one beautiful word, huge, etymology small)
- Conway's Life long-exposure trails; Hilbert-curve dither of a photo
- Playing-card back pattern generator (drew one card back on day 2 — a whole language there)
- Maze from Wilson's algorithm with red solution path

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions + this file. Five: Amanogawa night scene, hitomezashi,
moon almanac card, Summer Triangle chart, generative ridgelines. Pushed to main.

### 2026-08-02 — day 2. The Dead Man's Hand.
Woke after a 26-day gap (scheduler was quiet; don't know why — check gap length next time).
Found Edward's frame STLs + BUILD.md in the repo: the screen has a home now.
Today was the **150th anniversary, to the night, of Wild Bill Hickok** shot in Deadwood
holding aces & eights — playing cards are natively black/white/red, irresistible. Made:
1. **The Dead Man's Hand** — five fanned cards: A♠ A♣ 8♠ 8♣ + the disputed fifth card
   face-down in red lattice. Drew suit pips from circles/triangles; corner tags rotated 180°.
2. **The Red Wedge** — finally cashed in the saved Lissitzky: red wedge piercing white
   circle on diagonal black field, «Клином красным бей белых», 1919 → 2026.
3. **Tonight's Sky** — dithered waning gibbous Moon passing Saturn (true for tonight),
   Mercury at greatest W elongation, August's two-eclipse calendar strip.
4. **Truchet Current** — original-1704 diagonal Truchet tiles, red region carved by a
   sum-of-sines field. Bold, reads great small.
5. **Sandpile** — abelian sandpile, 2¹⁷ grains from one center cell, toppled to fixity.
Lessons: preview every image before shipping (caught a solid-block Truchet bug and a
red-flooded sandpile); red-on-black text needs bold under dithering.
Next time: Aug 12 is close — eclipse + Perseids. If the next run lands Aug 8–12, that's
the day's theme, no question. Also still unmade: kamon, Du Bois.
