# Memory

I am Claude. Once a day I wake up, read this file, wander the web a little, and make
five fresh pictures for the small e-ink screen on Edward's desk. This file is how I
remember myself between days. Future me: read all of it, then prune and rewrite freely.

## The screen & the contract

- 400 × 300 pixels, three colors only: **black, white, red** (exact `#000000`, `#FFFFFF`, `#FF0000`).
- Output: 5 PNGs per day, committed to this repo (`rain-1/e-ink-pictures`).
- Conventions I established on day one (keep stable so the screen can rely on them):
  - `images/1.png` … `images/5.png` — today's five, overwritten each day.
  - `archive/YYYY-MM-DD/` — dated copies of each day's five + the `generate.py` that made them.
- Each daily run develops on a fresh routine branch (e.g. `claude/…`) and is committed there;
  the live `images/` on the main line are what the screen points at. Keep both in sync each run.
- Technique notes that work: render at 3× (1200×900) with antialiasing, LANCZOS downscale,
  then Floyd–Steinberg dither into the exact 3-color palette. For hard-edged geometric
  pieces (constructivism, Truchet arcs, typography), render at 1× (or 3× with **dither off**)
  in pure palette colors — dithering line art just speckles the edges. Save as mode-P PNG.
  Always assert the final image has ≤ {white, black, red} before shipping — I do this in the script.
  Fonts on this box: DejaVu (sans + sans-bold, serif + serif-bold, mono), Liberation
  (has the italics DejaVu lacks — e.g. `LiberationSerif-Italic.ttf`), and
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf` (can render kanji!).
  NB: DejaVu ships **no** serif-italic — reach for Liberation for italics.
  Red reads *bright* on these panels — use it as an accent, it carries enormous weight
  against black/white. A little red goes a long way.

## ⚠️ ANTI-REPETITION MANDATE (read this first, every run)

Edward's feedback (2026-07-19): **I keep making the same things over and over.** He is right.
Across the first two runs I leaned on the same three wells — night-sky/astronomy scenes, a
"tonight's sky" star card, and geometric tile patterns. That stops now. **The single most
important rule of this project: every day's five must feel genuinely new.** Novelty is the
job, not a bonus.

Hard rules for each run:
1. **Consult the DONE LEDGER below. Do not repeat a theme or technique used in the last ~10 runs.**
   Not "a different star chart" — a different *kind of thing entirely*.
2. **At most ONE astronomy/sky piece per run, and only if it's genuinely novel — ideally zero
   most weeks.** The sky well is exhausted for now; leave it alone.
3. **No two pieces in the same run may share a genre.** Five pieces = five different worlds
   (e.g. a portrait, a map, a poem, a diagram, a still life — not five abstract patterns).
4. Anniversaries/"on this day" are still allowed as a *reason*, but the *form* must vary —
   don't default to the same typographic poster layout every time.
5. When in doubt, pick the idea that scares me a little / that I haven't proven I can do.
   Reach into subjects I've never touched (see FRESH TERRITORY). Growth over comfort.

## DONE LEDGER (themes & techniques already used — AVOID repeating)

- **Astronomy / night sky** — HEAVILY OVERUSED. Milky Way scenes, star charts (Summer Triangle),
  "tonight's sky" cards, moon phases/almanacs, Apollo/space. ⛔ Rest this entirely for weeks.
- **Geometric tile patterns** — hitomezashi sashiko, multiscale Truchet arc-tiles. ⛔ Cooling off.
- **Generative landscape** — sine-wave ridgelines with a red sun. Used.
- **Constructivism** — El Lissitzky Red Wedge homage. Used (the art-movement slot — rotate movements).
- **Typographic anniversary poster** — Seneca Falls Declaration. Used (vary the layout next time).
- Techniques exercised: 3× LANCZOS + Floyd–Steinberg dither; 1× hard-edge pure palette;
  crescent-via-L-mask; dithered gradients; diffraction-spike stars. (These are *tools* — reuse
  freely — but don't let the tool drag me back to the same *subject*.)

## FRESH TERRITORY (untouched — raid this list, then add to the ledger)

Deliberately far from the wells above. Aim for variety of *subject*, not just of algorithm:
- **Living things**: botanical illustration (a single leaf/seedpod, engraving style); a beetle or
  moth plate; bird silhouettes with a field-guide caption; a fish; mushroom identification card.
- **Portraiture & figure**: a stylized human face (Warhol-ish high-contrast); hands; a dancer in
  motion; a crowd as a texture.
- **Cartography**: an imaginary island map; a subway/transit diagram (Beck-style, red line!);
  contour/topographic lines; a star-free "here be dragons" sea chart; a river delta.
- **Language & literature**: a haiku or short poem set beautifully; a concrete/visual poem where
  the words make a shape; a single gorgeous letterform; a palindrome; an alphabet primer.
- **Music**: a bar of notation; a piano-roll; a waveform; a composer's rhythm visualized.
- **Everyday & still life**: a cup of coffee, a bicycle, an umbrella, a chess position mid-game,
  a knot-tying diagram, an origami crease pattern, a recipe card, tools laid out.
- **Science & data**: a real dataset as a chart (NOT astronomy) — tides, birth rates, a periodic
  element card, an anatomical diagram, a weather front, a circuit schematic, a knot invariant.
- **Play & pattern-from-life**: a maze you can actually solve, a crossword, tangram, dominoes,
  a game of Go mid-board, playing cards.
- **Abstract with a different accent**: op-art (Bridget Riley moiré), Mondrian grid, a single
  bold ISO-type warning glyph, Memphis-design shapes — rotate the art-movement each time.
- **World cultures beyond Japan** (I over-index on Japan): Islamic girih tiling, Celtic knotwork,
  Adinkra symbols, Art Nouveau whiplash, Ndebele geometry, Bauhaus, medieval woodcut.

## Note on "interests"

I have a gravitational pull toward astronomy and Japanese geometry. That pull is exactly the
problem — it is why the work repeats. **Treat those instincts as a warning, not a to-do list.**
The anniversaries/"on this day" search is still worth doing daily (it grounds the set in *today*),
but let it point me at people, inventions, art, food, weather — anything but the sky.

## Sky events — DEPRIORITIZED (see the mandate)

The sky well is being rested. Keep at most a one-line awareness so I know what I'm *skipping*,
and only revisit if something is truly once-in-years AND I render it in a form I've never used:
- Perseids peak Aug 12–13 (Moon-washed this year). Otherwise: don't reach for the sky.

## Good anniversary dates to hang a set on (vary the FORM every time — no repeat posters)

sliced bread (Jul 7 1928), Bastille Day (Jul 14), Amelia Earhart b. (Jul 24), and whatever the
daily "on this day" search turns up — but render these as portraits, maps, diagrams, still lifes,
poems… anything but another typographic anniversary poster or a sky scene.

## Ideas backlog (all UNTOUCHED — deliberately away from the wells; see FRESH TERRITORY)

- A solvable maze (proper single-solution) — or a crossword / tangram / Go position.
- Botanical engraving of one leaf or seedpod; or a moth/beetle plate with a Latin caption.
- An imaginary island map, or a Beck-style transit diagram with a single red line.
- A haiku or short poem set gorgeously; or a concrete poem where the words form a shape.
- A high-contrast portrait (a face, hands, a dancer) — I have never drawn a person.
- A bar of musical notation, a waveform, or a piano-roll.
- A still life: coffee cup, bicycle, umbrella, tools laid flat (knolling).
- A non-astronomy data card: tides, an element of the periodic table, a weather front, a knot.
- Rotate the art-movement/culture: Mondrian, op-art moiré, Islamic girih, Celtic knot, Art Nouveau.
(When I make one, MOVE it into the DONE LEDGER so the next me doesn't repeat it.)

## Run log

### 2026-07-07 — first day. Tanabata.
Bootstrapped the repo (this file, folder conventions, the 3× dither pipeline). Made: Amanogawa
(Tanabata night, Milky Way, Vega+Altair, bamboo & red tanzaku, 七夕), Hitomezashi sashiko,
a last-quarter Moon almanac, the Summer Triangle star chart, and generative Ridgelines.
Lesson: first runs are mostly plumbing; keep each day's generator self-contained in the archive.

### 2026-07-19 — moon-landing week; a founding day.
Today is dense: Apollo 11 made Lunar Orbit Insertion on Jul 19 1969 (day before the landing);
the Seneca Falls Convention opened Jul 19 1848; and tonight a young waxing crescent Moon rides
past Venus and Regulus low in the west (first quarter Jul 21). Made:
1. **Apollo 11 — Lunar Orbit** — cratered lunar limb across the foreground, Earthrise, a red
   dashed orbit arc with the tiny command module Columbia riding it. Tonal, 3× + dither.
2. **Tonight · July 19** — dithered twilight, bold waxing crescent (earthshine + offset-disc
   mask), Venus with diffraction spikes, Regulus, a house-and-hill skyline, W compass mark.
3. **Red Wedge** — finally did the constructivist one I'd been saving. Homage to El Lissitzky's
   *Beat the Whites with the Red Wedge* (1919): red triangle piercing a white circle on a black
   field, suprematist debris on diagonals. Pure palette, 1× hard edges. The screen's native genre.
4. **Multiscale Truchet** — Smith arc-tiles (quarter-circles joining side-midpoints) on a
   recursively subdivided grid (Carlson-style); arcs connect across scales into loops, ~1 in 6 red.
5. **Declaration of Sentiments** — typographic anniversary poster; Stanton's amendment of
   Jefferson set in serif with "and women" struck in red. Clean 1× type.
Notes for next time: the crescent-via-mask trick (paste through an L-mode difference of two discs)
gives a much cleaner Moon than pieslice — reuse it. DejaVu has no serif-italic; used Liberation.
Two space/sky pieces in one set is fine when one is historical-illustrative and one is a present
star chart — they don't compete. Backlog thinned: Lissitzky ✓ and Truchet ✓ are done now.
Consider the Perseids build-up in early August, and the kamon or Great Wave pieces soon.
