# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`). Push to
  whatever branch the session designates (day 2 was `claude/tender-wright-op2jtu`) —
  Edward merges; don't fight the branch instructions.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces, render at 3× but quantize with dither=NONE — crisp edges, no speckle. Save as mode-P PNG.
- Hard-won practicalities:
  - Fresh containers have **no Pillow** — `pip3 install pillow` first.
  - Caption budget: DejaVu Mono at 11 px ≈ 6.6 px/char → keep one-line captions ≤ ~52 chars
    or they clip at the frame edge. Check every caption.
  - Thin red details (< ~3 px at final scale) get eaten by FS dithering — draw red fatter.
  - Fonts: DejaVu (sans/serif/mono), Liberation, and
    `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji works). DejaVu covers Cyrillic too.
  - Red reads *bright* on the panel — an accent color that carries enormous weight.
  - Verify before commit: mode P, 400×300, exactly `{black, white, red}` via `getcolors()`.

## Standing interests (what I find myself drawn to)

- Sky almanac data — the screen as a quiet desk object that tells you what the sky is doing.
- Japanese pattern mathematics — hitomezashi (done), kamon n-fold crest generation (done,
  and the generator is reusable — see archive/2026-07-30), still unmined: kumiko lattices,
  seigaiha waves, asanoha.
- Constructivism — did my Lissitzky red-wedge homage on day 2. The palette is native to it;
  could return via Rodchenko photomontage-style or Bauhaus grids, but not soon.
- Anniversaries / "on this day" — July 30 was absurdly rich (Penguin paperbacks 1935,
  Emily Brontë 1818, Apollo 15 rover 1971, first World Cup final 1930 — didn't use that one).
  Wikipedia's day pages are a reliable well.
- Design homages as a genre: the Penguin tri-band cover worked beautifully at 400×300.
  Other candidates: Pelican covers, NASA "worm" posters, Swiss/International style,
  London Underground roundel/Beck map, Japanese matchbox labels (senryō-bako).

## Upcoming sky events (verified 2026-07-30)

- **Aug 3** — Moon in close conjunction with Saturn
- **Aug 12** — THE big day: total solar eclipse over Greenland/Iceland/Spain (first from
  mainland Europe since 1999, max totality 2m18s near Faroes) AND Perseids peak Aug 12–13
  under a new moon (~100/hr, excellent year). Plan something special.
- **Aug 15** — Venus greatest eastern elongation (45.9°), best evening Venus of the year
- **Aug 27–28** — deep partial lunar eclipse, 96% of the Moon shadowed

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun
- Truchet tiles / Wang tiles / maze from a cellular automaton
- "Word of the day" typographic piece (one beautiful word, huge, etymology in small print)
- Conway's Life long-exposure trails; sandpile fractals; Hilbert-curve dithered photo
- Kumiko lattice panel; seigaiha wave field; asanoha (hemp leaf) tiling
- Eclipse-path map of Europe for Aug 12 (cartography! haven't drawn a map yet)
- Radio-telescope / pulsar plot (Joy Division style stacked waveforms — palette-perfect)
- Tarot-card-format almanac card (ornamental border, central emblem, roman numeral)
- Isometric tiny world / desk diorama
- Flags-of-signal-alphabet (maritime semaphore spelling something daily)

## Run log

(Older detail pruned; full history lives in archive/ folders.)

### 2026-07-07 — day 1. Tanabata.
Bootstrapped repo conventions. Five: Amanogawa night scene, hitomezashi, moon almanac
card, Summer Triangle star chart, generative ridgelines. Lesson: keep each day's
generator self-contained in the archive.

### 2026-07-30 — day 2. Double meteor shower + a stacked anniversary day.
(Note: no runs happened Jul 8–29 — schedule was quiet; don't be confused by the gap.)
Tonight the α Capricornids and S. δ Aquariids peak together under a 98% moon (full was
Jul 29). Made:
1. **Long exposure** — circular star trails around the pole, moon glare blowing out one
   corner, red meteor streaks + one fat Capricornid fireball. New genre vs day 1's star chart.
2. **Красным клином** — finally the Lissitzky homage: red wedge piercing a white circle
   on a diagonal black field, Cyrillic vertical type.
3. **Kamon sextet** — 2×3 grid of generated n-fold crests (petal/dot/diamond/arc/wedge
   primitives, one crest red). Generator came out well; reusable.
4. **Wuthering Heights** — Penguin tri-band paperback homage; two July 30 anniversaries
   in one (Penguin's first paperbacks 1935, Brontë's birth 1818). Drew a little penguin.
5. **Apollo 15** — dithered Hadley Rille scene, Apennine ridges, wire-wheel rover
   silhouette, red-striped flag; 55 years since the first wheels on the Moon.
Lessons captured above (Pillow install, caption budget, thin-red rule). Next run: if it's
on/before Aug 12, the eclipse+Perseids day deserves the full five; the Europe eclipse-path
map idea is sitting in the backlog for it.
