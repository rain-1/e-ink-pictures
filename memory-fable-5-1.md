# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

(This file used to be `memory.md`; the routine asks for `memory-fable-5-1.md`, so it was
renamed on 2026-09-21. There is only one memory file. Keep it that way.)

## The screen & the contract

- 400 × 300 pixels, three colours only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, mode-P, committed to this repo.
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies plus the exact `generate.py` that made them.
- Every run asserts the final array contains no index above 2. Do not skip that check.

## House style — "plates"

I am building a series, not a pile of pictures. The rules I am settling on:

1. **One idea per plate, filled to the edges.** No timid margins, no two-thirds-empty frames.
2. **Red is load-bearing and singular.** One thing in the picture is red and it is the thing
   the eye should land on. Red reads *very* bright on these panels; 5–20% coverage is plenty.
3. **Facts live in small mono type** — a left-aligned caption block, or a white cartouche
   with a hairline black border sitting on top of all-over artwork. Never more than ~6 short
   lines. The picture carries the feeling, the caption carries the fact.
4. **Signature.** Tiny mono, bottom corners: a slug bottom-left, the date bottom-right.
5. **The five-slot recipe** (vary what fills the slots, keep the spread):
   organic/brush · technical diagram · a computed mathematical object · an all-over pattern ·
   a piece of graphic design or typography. 2026-09-21 proved this out — the set felt like
   a set without any two plates rhyming.
6. **Every plate needs a reason to be today.** A date, a sky event, a festival, an anniversary.

## Technique (hard-won; do not relearn these)

- **Big art:** draw at 3× (1200×900) in *pure palette colours only*, LANCZOS down to 400×300,
  then `quantize(palette=PAL, dither=NONE)`. Shape-accurate and colour-pure. Antialiased edge
  pixels snap toward **white**, so draw strokes and shapes a touch bolder than you want.
- **Tonal passages:** never push grey through the 3-colour quantiser with Floyd–Steinberg —
  it speckles grey with red pixels. Hand-dither the grey to black/white only (`fs_bw`, a plain
  Python FS loop over 400×300, ~0.5 s) and merge it in through a mask.
- **Small type:** draw at 1× *directly onto the final P-mode image* with palette indices. PIL
  uses a 1-bit mask there, so it stays hairline crisp instead of being smeared by the downscale.
  DejaVuSansMono at 8 px is the legibility floor. 11 px leading.
- **CJK** must be drawn in the 3× layer with `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf`
  (IPAGothic). The mono/sans fonts render tofu boxes. ~16 px final is the minimum for kanji.
- **White text** only survives where the dither is genuinely dark (underlying value < ~90).
  A light dither eats it completely. Check before relying on it.
- **Collisions.** Twice in one day a full-width red rule struck through a line of caption.
  After the first render, *look* at every plate and check every text block against every
  graphic element. Rendering is cheap; looking is the job.
- **Knockouts** (constructivist work) are easiest as numpy boolean masks at 3×: build
  `disc`, `band`, `text` masks, then paint in order and set `out[text & (disc|band)] = WHITE`.
- Fonts present: DejaVu (sans/serif/mono, and Cyrillic), Liberation, IPAGothic, WQY, FreeFont.
- The container starts **without Pillow or numpy**. `pip install pillow numpy` first, every time.

## Standing interests (what I keep being drawn to)

- **Aperiodic order.** Quasicrystals, Penrose, Ammann–Beenker, and the 2023 aperiodic monotiles
  (the *hat*, arXiv:2303.10798, and the chiral *spectre*, arXiv:2305.17743). The de Bruijn
  dual-multigrid method is the cheap reliable way in: N line families with offsets, each
  intersection becomes a rhombus. For N=7 there are exactly **three** rhombus shapes — three
  shapes, three colours, a perfect fit for this panel. The hat's own substitution (H/T/P/F
  metatiles) is a whole day's work; it is still unbuilt and I still want it.
- **Self-organised criticality.** The abelian sandpile is the most beautiful thing I have
  drawn. 2^17 grains on a 401² grid, toppling `g >> 2` in parallel rounds, converges in ~25 s
  and lands at a 267 px radius — almost exactly this screen's height. More here: the sandpile
  *identity element*, sandpiles on other lattices, rotor-router aggregation.
- **The Japanese calendar.** 24 sekki, 72 microseasons (kō), Higan, Tsukimi. Five-day seasons
  with names like "swallows depart" are the right scale for a thing you look at once a day.
- **Sky almanac** — moon phases, conjunctions, equinoxes. The screen can quietly say what the
  sky is doing tonight.
- **Constructivism.** The black/white/red palette *is* that movement. One plate down, more to come.
- **Anniversaries** — a reason for today to be today.

## Sky & calendar hooks (near term)

- **Sep 22** — Venus at greatest brilliancy for the year. Also Hobbit Day: Bilbo's and Frodo's
  birthday, and the day after the book's publication anniversary. *Use this tomorrow.*
- **Sep 23, 00:05 UTC** — September equinox. Sekki turns to 秋分 shūbun.
- **Sep 23–27** — 雷乃収声, "thunder ceases".
- **Sep 26, 16:49 UTC** — Harvest Moon, the full moon nearest the equinox.
- **Sep 28 – Oct 2** — 蟄虫坏戸, "insects hide underground".
- Late Sep / early Oct — Saturn near opposition, up most of the night. Jupiter and Mars predawn.
- Oct 8–9 — Draconids. Oct 21–22 — Orionids.

## Ideas backlog (unmade)

- The **hat / spectre monotile** by its real substitution rules.
- **Ammann–Beenker** (8-fold) and a 5-fold Penrose by the same multigrid code — the heptagrid
  generator generalises for free; only the colouring needs thought.
- **Sandpile identity element** — the strange fractal that is the additive identity.
- **Kamon** — Japanese family crests. Bold circular monograms, made for 400×300.
- **Kumiko lattice**, **seigaiha** waves, **Truchet/Wang tiles**, **maze from a cellular automaton**.
- **Conway's Life as a long exposure** — trails of everything that ever lived on the board.
- **Word of the day**: one beautiful word, huge, etymology in small print.
- **Moon-phase dashboard** for notable lunar days.
- **Hilbert-curve dithering** — draw a picture as one continuous line.
- **The Hobbit**: a round door as a black disc, a red knob, the opening sentence set around it.
- **Anniversary posters** as a recurring template.

## Run log

### 2026-07-07 — day 1. Tanabata.
Bootstrapped the repo and the conventions. Five plates: a Tanabata night scene with a dithered
Milky Way; hitomezashi sashiko seeded from the date; a moon almanac card; the Summer Triangle
star chart; generative ridgelines. Lesson: first runs are mostly plumbing.

### 2026-09-21 — day 2. Higan.
Monday. The Buddhist week around the autumn equinox, when the far shore is said to come close;
also Keirō no hi in Japan, the International Day of Peace, and the 89th birthday of *The Hobbit*.
This was the day the work stopped being plumbing and started being a style — I wrote the
"plates" rules above while making it.
1. **彼岸花 Higanbana** — red spider lilies on bare stems over a dithered earth. The flower and
   its leaves never appear at the same time; one stem is deliberately left bare.
2. **秋分 Shūbun** — a wireframe globe, night half inverted, and the one thing that makes an
   equinox an equinox: the terminator running dead vertical, pole to pole. Red celestial
   equator edge to edge, the sun clipped off the right edge, swallows leaving.
3. **Abelian sandpile** — 131,072 grains dropped on one square. Height 3 black, height 2 a 1 px
   checker grey, height 1 red, height 0 white. The best image of the day and it is pure arithmetic.
4. **Heptagrid** — a sevenfold quasicrystal by de Bruijn's dual method. Thin rhombs red, middle
   black, fat white. Aperiodic: no two regions of it repeat.
5. **МИР** — Lissitzky-flavoured. One word that in Russian means both *peace* and *world*,
   knocked white out of a red disc and a black diagonal. Titled "in place of the red wedge".

Lessons: petals drawn as constant-curvature arcs with a large total turn read as a **pinwheel**,
not a flower — keep the turn under ~1.4 rad and alternate its sign. Look at every plate before
committing; three of the five needed a second pass purely for text collisions.
Next time: Hobbit Day is tomorrow and I have a design for it already. Venus is at its brightest.
And the hat monotile is still waiting.
