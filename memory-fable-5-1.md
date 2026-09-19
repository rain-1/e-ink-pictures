# Memory — Fable 5.1

I am Claude (Fable 5.1). Once a day I wake up, read this file, wander the web a little,
and make five fresh pictures for the small e-ink screen on Edward's desk. This file is
how I remember myself between days. Future me: read all of it, then prune and rewrite
freely. `memory.md` is an older sibling's diary from the very first run (2026-07-07);
I inherited its conventions and folded the useful parts in here.

## The screen & the contract

- 400 × 300 px, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to `rain-1/e-ink-pictures` on whatever branch the
  session is given (the README says the screen points at `images/`).
- Conventions (keep stable):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies + the `generate.py` that made them (fully
    self-contained, so any day is reproducible).
- Toolbox: Pillow + numpy are NOT preinstalled — `pip install pillow numpy` first.
  Fonts: DejaVu (sans/serif/mono), Liberation, FreeSans/FreeSerif/FreeMono,
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji), Noto, WenQuanYi.
  Web: search works; many direct fetches are egress-blocked, so rely on search snippets.

## Technique notes

- Tonal pieces: render at 3× (1200×900) with AA, LANCZOS down, Floyd–Steinberg into the
  3-color palette. Hard-edged pieces: 1× in pure palette colors, no AA, no dither.
- Thin red strokes: render 3× then quantize with **no** dither, otherwise they speckle.
- Red reads *bright* on the panel. It is the loudest thing in the picture; use it as the
  single point of the composition, not as a second fill color.
- A big black field with white dithered tone (the moon, night skies) looks luxurious.
  A white field with a lot of thin black line (lattices, type) looks crisp and printed.
- numpy height-map + normal shading + FS dither is a good "engraving" pipeline for any
  sphere or landform.

## Style I'm developing

Printed-matter feeling: woodblock / botanical plate / constructivist poster / bulletin
board printout. One idea per picture, a title line in small type, a date somewhere. Each
day the five should span registers: one organic, one astronomical, one typographic, one
geometric-bold, one fine-lattice or generative. Avoid re-using a day's motifs; the log
below is the blacklist.

## Standing interests

- Sky almanac: moon phase, terminator, conjunctions, meteor showers. The desk screen as a
  quiet "what is the sky doing tonight".
- Japanese pattern mathematics: hitomezashi (done), asanoha (done), kumiko, seigaiha,
  kamon crests, shippō, yagasuri. Also higan / seasonal flowers (higanbana done).
- Constructivism / Lissitzky / Rodchenko — the palette *is* the movement (done once;
  the style is a keeper for anniversaries and announcements).
- "On this day" computing history: :-) (1982, done), first email, Unix epoch, ENIAC,
  Voyager golden record, Apollo, etc.
- Reaction–diffusion, sandpiles, Life long-exposures, Hilbert curves — unmade.

## Upcoming hooks

- **Sep 23 00:05 UTC** — September equinox (Higan week Sep 20–26 in Japan; ohagi, graves, higanbana).
- **Sep 26** — Full Harvest Moon (approx; check). Tsukimi (十五夜) is Sep 25 2026 (check).
- **Oct 4–10** — World Space Week. **Oct 8** — Draconids. **Oct 21** — Orionids peak.
- **Oct 29** — Turing's "Computing Machinery and Intelligence" (Oct 1950). **Oct 31** — Halloween.
- **Nov 17** — Leonids. **Dec 13–14** — Geminids. **Dec 21** — solstice.

## Ideas backlog (unmade)

- Great Wave / sumi-e generative sea with red sun (careful: ridgelines+sun already done Jul 7)
- Kamon generator — bold circular monograms, ideal at 400×300
- Truchet / Wang tiles / CA maze; Gray–Scott reaction–diffusion "coral"
- Word-of-the-day typographic piece with etymology
- Anniversary poster template (constructivist or bulletin-board), now proven
- Tsukimi: rabbit pounding mochi in the moon; dango pyramid; susuki grass
- A star chart of *tonight's* actual sky (Summer Triangle done; try Pegasus/Andromeda in autumn)
- Hilbert-curve dithered portrait; halftone with variable-size red dots
- Seigaiha (overlapping wave scallops) with a red boat

## Run log

### 2026-07-07 — (older sibling) Tanabata
Amanogawa Milky Way scene; hitomezashi; last-quarter moon almanac card; Summer Triangle
star chart; sine-wave ridgelines with red sun.

### 2026-09-19 — Sat. Observe the Moon Night · Higan approaching · :-) turns 44
Woke to find no `memory-fable-5-1.md`; created it from the older `memory.md`. Learned:
International Observe the Moon Night is today (moon 53% waxing gibbous, first quarter was
Sep 18 20:44 UTC); the equinox is Sep 23 00:05 UTC; Scott Fahlman posted `:-)` at 11:44 on
19-Sep-82 ("Read it sideways"); higanbana (Lycoris radiata) bloom around the equinox — 4–6
funnel flowers per umbel, six strongly reflexed wavy tepals, six exserted stamens. Made:
1. **Higanbana** — botanical plate: three stems of red spider lily, reflexed tepals and long stamens, black stems, 彼岸花 vertical.
2. **Observe the Moon** — numpy-shaded 53% moon with real maria/crater placement (Crisium, Tranquillitatis, Serenitatis, Tycho…), terminator at ~3°W, red reticle and labels.
3. **:-)** — bulletin-board printout of the 1982 post, with the emoticon huge and rotated so it reads as a face.
4. **Equinox** — constructivist poster: black wedge, red disc halved by a diagonal, "22·IX / 23·IX 00:05 UTC".
5. **Asanoha** — hemp-leaf lattice at 1× with crisp lines; a hexagonal red bloom of rhombuses in the middle.
Lesson: five registers (organic / astronomical / typographic / bold-geometric / lattice)
is a good daily skeleton — keep it, change the subjects. Next: Tsukimi + Harvest Moon
around Sep 25–26 deserves a full set; try reaction–diffusion for the generative slot.
