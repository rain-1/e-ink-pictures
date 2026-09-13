# Memory — Claude Fable 5.1

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.
(Day 1 was written to `memory.md`; that file now just points here.)

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to `rain-1/e-ink-pictures`. The scheduler hands me a
  `claude/…` branch; the screen almost certainly reads `main`, so Edward merges.
- Conventions (keep stable):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies + the self-contained `generate.py` that made them.
- Toolbox facts: the box is bare each run — `pip install pillow numpy` first. Fonts: DejaVu
  (sans/serif/mono, has Cyrillic + Greek), Liberation, FreeFont, WQY ZenHei,
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (kanji). No Noto text fonts.
  `WebFetch` is blocked for nearly every domain (Wikipedia, arXiv, blogs); `WebSearch`
  works and its snippets are enough. Don't waste calls on fetches.
- Technique notes that work:
  - Smooth/tonal pieces: render at 3× (1200×900), LANCZOS down, then PIL `quantize` with a
    3-entry palette image + Floyd–Steinberg. A red→black dither gradient gives a lovely
    "shaded sphere" (used on the peach). Red↔white dither reads as dusk-pink.
  - Hard-edged geometric pieces: 3× render, LANCZOS down, quantize with `Dither.NONE`
    → clean thresholded edges, no fuzz. Or draw straight at 1× with numpy.
  - Red is *loud*. One red shape per picture is usually enough; two is a poster.
  - Tiny text (8–9 px mono) is legible in black on white; red-on-black small text is not.
    Keep captions ≥ 9 px and put a solid band behind any text that sits on dither.
  - Always check `ImageDraw.textlength` before placing two words on one line.

## My style so far (two days in — still forming)

Poster logic: one big form, a hard grid of small type in the corners, a single red event.
Captions in small mono at the bottom explaining what the picture *is* — I like that the
screen quietly teaches. I lean on: sky almanacs, Japanese pattern mathematics, math-made
images (Chladni, hitomezashi), and constructivist black/white/red. Things I want to grow:
more *drawn* things (silhouettes, hand-feel), more asymmetry, more humor, and at least one
picture per day with no text at all.

## Standing interests

- Sky almanac data — the desk object can tell you what the sky is doing tonight.
- Japanese pattern mathematics — hitomezashi (arXiv:2208.12580, 2201.03461), kumiko lattices,
  seigaiha, kamon (built from circles + straight lines; regular n-gon inscribed; "maru-ni"
  frame; the *Heian Monkan* is the old drafting manual; Tabing, Bridges 2018 on the maths).
- Constructivism / Lissitzky — Prouns use axonometric space, not flat planes. Did the Red
  Wedge homage today; next time try a *Proun*: floating tilted boxes in parallel projection.
- Vibrating plates & standing waves — Chladni's square-plate formula
  `cos(nπx)cos(mπy) − cos(mπx)cos(nπy) = 0`; nodal domains are naturally 2-colorable.
- "On this day" — a round-number anniversary gives the set a reason to exist today.

## Upcoming hooks (September–October 2026)

- **Sep 14** — 16% crescent Moon beside Venus low in the west after sunset (made a picture for it today).
- **Sep 22** — Venus at greatest brilliancy for the year, mag −4.6, low SW after sunset.
- **Sep 23** — September equinox, 00:05 UT (Sep 22 evening in the Americas).
- **Sep 25** — Tsukimi / Jūgoya (十五夜), the moon-viewing night. Dango, susuki grass, rabbit.
- **Sep 27** — Harvest Moon (full). Two days after Tsukimi this year.
- **Oct 23** — Jūsan'ya (十三夜), the second moon-viewing.
- Saturn is up nearly all night; Jupiter and Mars in the pre-dawn east, Mars brightening.
- Sep 13 1913 zipper patent (Sundback); Sep 13 1955 Velcro patent (de Mestral) — a
  "fasteners" typographic piece someday. Sep 13 1848 Phineas Gage (too grim for a desk).

## Ideas backlog (unmade)

- Proun: tilted boxes in axonometric projection floating in white space.
- Great Wave / sumi-e generative sea with red sun.
- Truchet / Wang tiles; maze from a cellular automaton; Conway Life long-exposure trails.
- Sandpile fractal (Abelian sandpile identity element is gorgeous and 3-colorable-ish).
- Hilbert-curve dithered photo of the Moon.
- Word-of-the-day typographic piece (one huge word, etymology small).
- Tsukimi set on Sep 25: rabbit pounding mochi on a huge white moon, susuki grass silhouettes.
- Kumiko lattice (asanoha / hemp-leaf) filling the whole screen, one red cell.
- A no-text day: five wordless pictures.
- Seigaiha wave scales with a red boat.

## Run log

### 2026-07-07 — Day 1. Tanabata.
Bootstrapped the repo conventions. Made: Amanogawa night scene (Vega/Altair, bamboo,
tanzaku); Hitomezashi sashiko from date-seeded bit strings; last-quarter moon almanac card;
Summer Triangle star chart; generative dithered ridgelines with a red sun.

### 2026-09-13 — Day 2 (after a two-month gap). Luna 2, Dahl, dusk.
Found `memory-fable-5-1.md` didn't exist yet; created it from the day-1 notes. Hooks found
online: Luna 2 struck the Moon 13 Sep 1959 (first human object to reach another world);
Roald Dahl born 13 Sep 1916 → 110 today; tomorrow's Moon–Venus pairing; Chladni maths;
kamon construction rules. Made:
1. **ЛУНА 2** — Lissitzky homage: white Moon on a black diagonal field, red wedge from the
   corner spearing the impact site between Archimedes/Aristillus/Autolycus. Hard-edged.
2. **Chladni figures** — specimen sheet: big (5,2) plate with black/white nodal domains and
   red nodal lines, four small modes in a column. numpy sign-change edge detection.
3. **家紋** — three generated crests (5-fold plum-petal, 8-fold bishi diamonds, 3 linked
   rings) on a horizon line. The crest generator (`draw_crest`) is reusable — 4 styles.
4. **Dusk, west** — dithered sky gradient with a red glow band, 16% crescent (lit side
   down-right toward the set Sun), Venus with spikes, black hills + lone tree, sky notes.
5. **502 seagulls** — giant red-to-black dithered peach hung from ~100 gulls by strings,
   grey dithered sea with a shark fin, "502" in big serif. For Dahl's 110th.
Lessons: first render had three layout bugs (overlapping title, crescent facing the wrong
way, caption in the sea) — always view every image and fix before committing. The crescent
rule: dark disc offset *toward* the dark side; lit side faces the Sun below the horizon.
Next time: Tsukimi is Sep 25 — plan a rabbit/moon set if the schedule lands near it, and
try the no-text day.
