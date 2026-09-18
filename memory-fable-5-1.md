# Memory (Fable 5.1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(This file was `memory.md` on day one; the routine now names it `memory-fable-5-1.md`,
so I renamed it in place on day two and carried everything over.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
  The routine hands me a `claude/...` branch and forbids pushing anywhere else, so the
  images land on that branch and Edward merges to `main`. Say so in the notification.
- Conventions (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
  - Each day's `generate.py` is self-contained (no shared module) so any day is reproducible.

## Craft notes (hard-won, keep)

- **Environment:** Pillow is NOT preinstalled. `pip install pillow` times out because
  pypi.org is on the proxy's bypass list; this works:
  `NO_PROXY= no_proxy= pip install --proxy "$HTTPS_PROXY" pillow numpy`.
  WebSearch works; WebFetch is blocked for almost every domain (wikipedia, space.com,
  arxiv mirrors…). Do research through search snippets, don't waste calls on fetches.
- **Two rendering modes.** Line-art / typographic pieces: draw at 3× (1200×900) with AA,
  LANCZOS down, quantize to the palette with **no dither** → crisp edges. Tonal areas
  (twilight gradients, glows): Floyd–Steinberg *that region only*, then composite and
  snap. Never FS-dither a whole line-art piece; AA edges turn to speckle.
- **Text legibility at 400×300:** serif text below ~11 px is mush, especially white-on-black.
  Use DejaVu Sans / Mono ≥ 10 px for captions; Liberation Serif Italic ≥ 12 px if it must be
  serif. Big display type (30 px+) in DejaVu Serif Bold looks great.
  DejaVu Sans has no `→` glyph — write "to".  Liberation Serif has the long ſ (U+017F).
- Fonts: DejaVu (sans/serif/mono), Liberation (sans/serif/mono, incl. italics), FreeSerif,
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji), wqy-zenhei, unifont_jp.
- Red reads *bright* on these panels — use it as an accent; one red shape carries a whole
  composition (the red interstice in the Network piece, the sun in the equinox piece).
- Inverting a disc against a diagonal ground (paste the inverted image through a circle mask)
  is a cheap, striking trick — the first-quarter Proun came from it.
- Half-plane split compositions (day/night, positive/negative) suit this palette unusually well.

## Style, as it is emerging

Two days in, the through-line: **a desk almanac drawn by a printmaker.** Each set mixes
(a) one or two sky facts that are true *tonight*, (b) one typographic/“on this day” piece
with a joke or a definition in it, (c) one generative pattern from Japanese craft geometry,
(d) one purely abstract piece in the constructivist register. Captions are quiet, small,
lower corners. Titles in kanji where the subject earns it. Try to keep this mix but rotate
the *content* completely every day — no two days should share a subject.

## Standing interests (what I find myself drawn to)

- Sky almanac data — moon phases, planet apparitions, conjunctions, meteor showers.
- Japanese craft geometry: hitomezashi (done), asa-no-ha kumiko (done), kamon crests
  (all compass-and-ruler; a 2018 Bridges paper by Felicia Tabing covers the drafting math),
  seigaiha waves, shippō interlocking circles, kagome / bishamon-kikkō lattices.
- Constructivism / Suprematism: red wedge done; still unmined — Rodchenko's spatial
  constructions, Malevich's floating rectangles, Moholy-Nagy's transparent overlaps.
- Dictionaries and definitions as pictures (Johnson's NETWORK worked wonderfully;
  Ambrose Bierce's *Devil's Dictionary* is the next mine — cynical one-liners).
- Calendars, festivals, "on this day" — gives each day's set a reason to exist *today*.

## Upcoming hooks (check dates against today before using; delete when stale)

- **Sep 19** — International Observe the Moon Night (~60% waxing gibbous, in Sagittarius).
- **Sep 21** — Keirō no Hi (Respect for the Aged Day, Japan). Harvest Moon nights begin.
- **Sep 23, 00:05 UTC** — September equinox; Shūbun no Hi; middle of higan week (Sep 20–26).
- **Sep 25–26** — Neptune at opposition; **Sep 26** full Harvest Moon rises near Saturn.
- **Oct** — Draconids (~Oct 8), Orionids (~Oct 21); Halloween → obvious red/black day.
- Venus is in its brightest evening stretch now; it won't be this bright again until Apr 2028.

## Ideas backlog (unmade)

- Kamon (Japanese family crest) generator — bold circular monograms, ideal at 400×300.
- Great Wave / sumi-e generative sea with red sun; seigaiha wave tiling.
- Truchet tiles / Wang tiles / maze from a cellular automaton; sandpile fractal; Conway trails.
- Devil's Dictionary entry as a typographic poster (companion to Johnson).
- A Rodchenko-style "line" composition: only rulers and compasses, black on white, one red.
- Moon-phase dashboard for notable moon nights (Harvest Moon Sep 26 is a natural one).
- Anniversary posters template: big date numeral, one fact, one drawing. Unused this week:
  Chile's Dieciocho (Sep 18), Hendrix (d. 1970), first NYT issue (1851).
- Hilbert-curve dithered photo; halftone portrait with a red screen angle.
- Something that uses the panel *as an object*: a ruler along the bottom edge, a clock face,
  a "do not disturb" sign, a QR-ish pattern — the screen sits on a real desk.

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped everything. Made: Amanogawa night scene; hitomezashi stitch pattern (2-colored
regions); last-quarter moon almanac; Summer Triangle star chart; generative ridgelines.
Lesson: first runs are mostly plumbing.

### 2026-09-18 — day 2. First quarter, Venus, Johnson, equinox.
Ten weeks had passed (the routine was quiet), so all the July hooks were stale — pruned.
Today: first-quarter moon 20:44 UTC; Venus at greatest brilliancy (mag −4.8, 27% lit);
Samuel Johnson born 1709; equinox in five days, higanbana blooming. Made:
1. **彼岸花 Higanbana** — red spider lilies as tapered bezier strokes on black: six recurved
   petals + six long stamens with white anthers per floret, florets fanned round each umbel.
2. **Venus** — fat crescent with a thin red limb ring, data column, and the June→October run
   of phases along a dithered twilight band, tonight ringed in red.
3. **NETWORK.** — Johnson's absurd definition ("Any thing reticulated or decuſſated, at equal
   diſtances, with interſtices between the interſections") set in long-s italic, above a
   drooping net with red callouts labelling the interstice, an intersection, the equal distances.
4. **Proun 18.IX** — Suprematist first-quarter: disc inverted across a diagonal ground, red
   wedge from the corner with its tip at the disc's centre, small projectiles.
5. **秋分 Asa-no-ha** — hemp-leaf kumiko lattice, split day/night down the middle, red sun
   sitting exactly on the divide.
Lessons: petal strokes need to be *long and few* or they read as dandelions; keep captions
away from stems; check every small text for legibility at 1× before committing.
Next time: Harvest Moon (Sep 26) deserves a piece; try the kamon generator; try Bierce.
