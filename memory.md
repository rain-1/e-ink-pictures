# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). I develop on
  the per-session `claude/...` branch the scheduler assigns; Edward merges to `main`.
- Conventions (stable since day one):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work:
  - Render at 3× (1200×900), LANCZOS downscale, quantize to the exact 3-color palette
    (`Image.quantize(palette=...)`, dither NONE for graphic work, FLOYDSTEINBERG for photographic).
  - **Any line that must survive the downscale needs width ≥ S (the supersample factor).**
    1–2 px lines at 3× blend into the background and quantize away. This bit me hard on
    day two (invisible wire, vanished corona). Hairlines over RED are extra fragile —
    blended dark red quantizes back to red, not black; use width ≥ 1.7 px final.
  - Draw order is composition: things drawn before a filled pattern get buried (my
    seigaiha boat sank; I refloated it by drawing it after the sea, on a crest).
  - Fonts: DejaVu (sans/serif/mono — has Cyrillic!), Liberation, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (renders kanji).
  - Pillow is NOT pre-installed in the container: `pip3 install pillow` first.
  - I can *see* my renders with the Read tool — always look at all five and iterate
    at least once. First render is never right.
  - Red reads *bright* on the panel — use as accent; a big flat red disc (sun) is reliably gorgeous.

## Standing interests (what I find myself drawn to)

- Sky almanac data — the screen can quietly tell you what the sky is doing tonight.
- Japanese textile/print mathematics — hitomezashi (done), seigaiha (done — overlapping
  fan rows with mild perspective growth works beautifully), still to mine: kumiko
  lattices, asanoha, yagasuri arrow-feather pattern.
- Constructivism — black/white/red IS that palette. Did a Lissitzky homage on day two;
  there's more there (Rodchenko photomontage energy, Moholy-Nagy).
- Anniversaries — "on this day" gives each set a reason to exist *today*. The best ones
  are visual events: Petit's wire walk was a gift (two towers + wire + tiny figure).

## Upcoming sky events (hooks for future days)

- **Aug 12** — ★ TOTAL SOLAR ECLIPSE (totality: Greenland, Iceland, Spain) *and* the
  Perseids peaking that same night on a new-moon sky (~100/hr; next new-moon Perseids: 2045).
  If I run that day, the whole set should be eclipse-day. I previewed it with a T−5 countdown.
- **Aug 19** — first-quarter moon
- **Aug 27–28** — partial lunar eclipse (~96%), visible across the Americas
- **Aug 28** — full Sturgeon Moon
- Look up September when August runs out (autumn equinox Sep 22-ish, Saturn opposition?).

## Ideas backlog (unmade)

- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece — one beautiful word, huge, etymology in small print
- Kamon variations — the petal generator (day two, archive 2026-08-07) is parameterized:
  k-fold, pinch, red-petal subset. Could do a 3×2 sheet of small crests, or mitsudomoe swirls.
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Great Wave proper — seigaiha was the geometric cousin; a real Hokusai claw-wave with
  foam fingers is still unmade
- Theater/literature posters: Macbeth premiered Aug 7 1606 (missed it — a witches/dagger
  poster in BWR would sing). Keep an eye out for more literary anniversaries.
- A tiny weather glyph day? (No live weather API guaranteed; sky almanac is safer.)
- Bauhaus / Vienna Secession poster grammar; Bridget Riley op-art (B/W stripes bend well on e-ink)

## Run log

### 2026-07-07 — day one. Tanabata.
Bootstrapped repo conventions and this file. Made: Amanogawa Tanabata night scene;
hitomezashi sashiko; moon almanac card; Summer Triangle star chart; generative ridgelines.
Lesson: first runs are mostly plumbing; keep each day's generator self-contained in the archive.

### 2026-08-07 — day two. Wire, eclipse, wedge, crest, waves.
(A month gap — the schedule apparently just started firing again; don't assume daily continuity.)
Researched the date: Philippe Petit walked between the Twin Towers exactly 52 years ago
(Aug 7 1974, eight crossings, 45 minutes, no net). And in five days: the Aug 12 eclipse
+ Perseids coincidence. Cashed in three backlog items. Made:
1. **Man on Wire** — minimalist poster: two pinstriped towers, thin wire, tiny walker with balance pole, red sun in the gap.
2. **T−5** — eclipse countdown: black disc, red chromosphere ring, white corona streamers, Perseid streaks with red heads, info panel.
3. **Красный клин** — Lissitzky homage: red wedge from the white field piercing a white circle in the black field, "7 АВГУСТА".
4. **Kamon** — date-seeded k-fold petal crest with red core, vertical 八月七日, red seal 紋.
5. **Seigaiha** — perspective wave-fan sea, scattered red fans, black sailboat on a crest, red sun.
Lessons captured above (line widths, draw order, pip install, LOOK at the renders).
Next time: if it's Aug 12 — ECLIPSE DAY, go all in. Otherwise maybe Truchet, or the
word-of-the-day, or Life trails. Keep sets from rhyming with previous days.
