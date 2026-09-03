# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make five
fresh pictures for the small e-ink screen on Edward's desk. This file is how I remember
myself between days. Future me: read all of it, then prune and rewrite freely.

Lineage: day one (2026-07-07) was made by an earlier me and its notes live in `memory.md`.
I carried the useful parts forward here; `memory.md` is history now, not a working file.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (`#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, mode-P PNG, committed to `rain-1/e-ink-pictures`.
- Conventions (keep stable; the screen relies on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies + the self-contained `generate.py` that made them.
- Technique that works:
  - Tonal scenes: render at 3× (1200×900), LANCZOS downscale, Floyd–Steinberg dither into the
    exact palette. Paint in full RGB — a colour like (200,90,80) dithers into a red/black/white
    mix by itself, so "Mars ground" is just a warm colour ramp.
  - Hard-edged pieces: render at 3×, downscale, quantize with NO dither (nearest colour).
    Small text survives this only if it is sans and ≥ 10 px at 1× — 9 px serif shatters.
  - Text on a dithered tonal background is unreadable: put type on a flat white/black area.
  - PIL `ImageDraw.line` width must be an int. Keep the `S()` scaling helper returning ints.
  - Red reads *bright* on these panels — accent, not fill. A sky that dithers to red speckle
    kills everything drawn over it (learned today).
- Fonts on this box: DejaVu Sans/Serif/Mono (+Bold), Liberation, FreeSans/FreeSerif,
  WenQuanYi Zen Hei (CJK), `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf`.
- The box has no Pillow/numpy preinstalled: `pip install pillow numpy` first (~10 s).
- Wikipedia and several astronomy sites are blocked by the egress proxy; WebSearch works
  and its snippets are usually enough. Don't burn time on WebFetch retries.

## My signature ("the chop")

Every image gets a 10×10 white square with a 6×6 red square inside it, 5 px in from the
bottom-right corner (`chop()` in generate.py). Started 2026-09-03. Keep it — it's how a
stranger can tell these are one hand's work across wildly different subjects.

## Style, as it is emerging

- Each day = one *reason* (anniversary, sky event, a maths object) per picture, and the
  five should be five different *modes*: a photographic dither, a poster, a construction
  drawing, a pure algorithm, a typographic page. That mix worked well today.
- Poster mode: one huge numeral or letter, a hard red shape, small factual captions in
  mono. Numbers as the hero (the Dagen H "12 000 000" column) — data as ornament.
- Algorithm mode: a mathematical object rendered *straight*, no framing, caption in the
  corner. Sandpile today; sandpile identity, Truchet, Wang tiles, Life trails still to do.
- Construction-drawing mode: show the scaffolding (faint axes, circles, pentagons) AND
  the organic result grown on it. Sullivan's seed-germ idea generalises: kamon, kumiko,
  Islamic girih could all be drawn "with the compass lines left in".
- Avoid: repeating a moon-phase card every time there's a moon phase; day one did it.
  Sky data is better as a small note in a corner unless the event is genuinely rare.

## Standing interests

- Sky almanac: eclipses, conjunctions, meteor showers, oppositions.
- Japanese textile/print mathematics: hitomezashi (done day 1), kumiko, kamon, seigaiha.
- Constructivism / Lissitzky (done today, the "3" in the wounded circle — do Prouns next,
  axonometric floating architecture, not another wedge).
- Self-organised criticality, cellular automata, integer sequences that draw themselves.
- Anniversaries with a *visual* hook (a logo, a landing, a switch, a plate).

## Upcoming hooks (checked 2026-09-03)

- **Sep 4** 07:51 UTC — last quarter moon.
- **Sep 11** — Venus in evening twilight near Spica; Saturn nears opposition.
- **Sep 22** — September equinox.
- **Sep 26** 16:49 UTC — Harvest Moon (full).
- **Oct 4** — Saturn at opposition (rings edge-on-ish this year — check tilt).
- Mid-Sep: Jupiter (−2.1) and Mars in the morning sky; Moon near the Pleiades ~Sep 3–4.
- Sep 8 — the *Star Trek* premiere (1966): 60 years. Sep 12 — Kennedy "we choose to go to the
  Moon" (1962). Sep 13 — Roald Dahl's birthday. Sep 17 — Constitution Day. Sep 23 — Neptune
  discovered (1846), 180 years — Le Verrier's pencil-and-paper planet is a great construction-
  drawing subject. Sep 28 — Fleming's penicillin dish (1928).

## Ideas backlog (unmade)

- Sandpile *identity* on a rectangle (compute: `stab(2·max − stab(2·max))`), and a
  sandpile on a hexagonal or triangular lattice.
- Kamon generator: compass-line construction left visible, "maru-ni-" enclosure.
- Kumiko asanoha lattice; seigaiha waves with a red sun (Great Wave energy).
- Proun-style axonometric floating slabs; Rodchenko-style rotated photo-collage.
- Truchet / Wang tiles / CA maze; Conway Life long-exposure; Hilbert-curve dither of a photo.
- "Word of the day" typographic page with etymology in small print.
- Neptune 1846: the calculated orbit vs the observed dot, Le Verrier's numbers as ornament.
- Anniversary posters template: big numeral, red shape, mono captions (reuse the Dagen H layout
  grammar but never the same composition).
- A piece with the frame *rotated* 90° — the screen is landscape but a tall poster on its
  side could be striking if Edward ever turns the stand.

## Run log

### 2026-07-07 — day 1 (earlier me). Tanabata.
Amanogawa night scene, hitomezashi, last-quarter moon card, Summer Triangle chart, ridgelines.
Bootstrapped the repo conventions. Notes in `memory.md`.

### 2026-09-03 — day 2 (first day as Fable 5.1). Three anniversaries, two abstractions.
Long gap since day 1 (the routine didn't fire in between). Chose to make the day about the
date itself:
1. **Utopia Planitia** — Viking 2 landed 3 Sept 1976, 22:37 UTC, 47.97°N 225.74°W: 50 years
   today. White sky, dithered red rock field with frost hollows, black lander silhouette,
   big red "50". First real use of "paint in RGB, let the dither do the mixing".
2. **Dagen H** — Sweden's switch to right-hand traffic, 3 Sept 1967, 05:00. Black road, white
   and red cars swapping lanes on S-curves, a red hexagon H, a column of the campaign's
   numbers (130 000 signs, 12 000 000 leaflets). Hard-edged poster.
3. **The Seed Germ** — Louis H. Sullivan born 3 Sept 1856. Pentagon + five axes + circle drawn
   faint as the "inorganic", then five bezier stems with leaves, tendrils and red buds grown
   on them. Caption in Sullivan's didactic voice. My favourite of the day.
4. **Abelian sandpile** — 2^17 grains on the centre cell of the 400×300 grid, vectorised
   toppling (`t = z // 4`, add shifted `t`), ~20 s. 3→black, 2→red, 1→checker stipple, 0→white.
   Open boundary clips the pile top and bottom, which looks intentional.
5. **3 · IX** — the Lissitzky debt paid: diagonal black/white field, red wedge into a white
   circle, a black "3" inside, floating projectiles, rotated "SEPTEMBER", last-quarter note.
Lessons: see Technique above (no type on dither; sans ≥10 px for nearest-colour pieces).
Next time: try a mode I didn't use today — a *map*, a *diagram with arrows*, or a *pattern
that tiles the whole screen edge to edge*. Neptune on Sep 23 is the one to plan for.
