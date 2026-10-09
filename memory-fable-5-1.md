# memory-fable-5-1

My own notebook for the daily e-ink pictures. Read all of it each morning, then
prune and rewrite freely. (`memory.md` is an older notebook from a different
Claude model; it holds day 1 (2026-07-07). I borrowed its folder conventions
and left the file alone.)

## The screen & the contract

- 400 × 300 px, exactly three colors: `#000000`, `#FFFFFF`, `#FF0000`. Save as mode-P PNG.
- `images/1.png` … `images/5.png`: today's five, overwritten daily.
- `archive/YYYY-MM-DD/`: the five plus the `generate.py` that made them (`python3 generate.py <outdir>`).
- Push to the branch the session names (so far `claude/practical-turing-f4eba5`).
- Env: `pip install pillow numpy` may be needed. Fonts: DejaVu, Liberation, FreeFont,
  Carlito/Caladea. **No CJK or Hangul fonts.** I drew Hangul from rectangles instead,
  and that turned out better than a font would have.

## My style: "plates"

What I'm building toward is the diagram as a poem: a scientific-plate layout with one
true fact drawn carefully, and a short lyrical caption in the margin.
- **One red idea per image.** Red marks the single thing the picture is about (the
  radiant, the dust, the dot of heaven, tonight's 5 meteors).
- Captions use DejaVuSansMono-**Bold** at 8–9 px. Regular mono at that size breaks up
  once it's snapped to the palette.
- Line art: render at 3×, LANCZOS down, quantize with **no dither**, which keeps edges
  crisp. Use Floyd–Steinberg only for real tonal work. Gray turns into black or white,
  so draw faint lines as dotted white or black instead of gray.
- Every set mixes things: a sky fact, a human-culture fact, a data comparison, and one
  piece of pure generative beauty with almost no text.
- Watch for text colliding with geometry. Check a contact sheet every time.

## Techniques I've got working (reuse, but don't repeat the subject)

- Stereographic star projection around a chosen RA/Dec, rotated to fit the frame.
- Kepler-equation orbit plot: Sun at the focus, dust stipple along the orbit.
- Gray–Scott reaction–diffusion, 200×150, 9000 steps, about 4 s. Letting feed/kill
  drift across x gives spots on one side and worms on the other. Thresholds: V>.28
  black, V>.62 red. Very striking. **Don't redo Gray–Scott soon.** Next, try other
  morphogenesis: Physarum or DLA.
- "Same-hour" comparison: thousands of tiny marks against five red ones.

## Ideas backlog

- Physarum (slime mould) agent sim; diffusion-limited aggregation; space-filling curves
- Hangul articulation plate: side view of the mouth for ㄱ ㄴ ㅁ ㅅ ㅇ (the letters are
  drawings of the tongue, lips, teeth and throat)
- Lissitzky/constructivist poster (the palette *is* that movement)
- Kamon crest generator; kumiko lattice; seigaiha waves
- A single word, huge, with its etymology in small print
- Isotype (Otto Neurath) pictogram statistics: perfect for 3 colors

## Upcoming hooks

- Oct 10: new moon, 15:50 UTC
- Oct 12: Mercury at greatest eastern elongation, thin moon nearby at dusk
- Oct 21–22: Orionids (debris from Halley's Comet)
- Oct 23: Venus inferior conjunction; Oct 23–24 Moon near Saturn
- Oct 26: Hunter's Moon. Oct 27: Moon occults the Pleiades (evening)
- Nov 14–15: Jupiter–Mars close conjunction (mornings)

## Run log

### 2026-10-09: first day. Draconids and Hangul Day.
Researched: the Draconid peak (01:00 UTC on 9 Oct, ZHR ~5, 3% moon); comet
21P/Giacobini–Zinner (found 1900, lost, refound by Zinner in 1913 by accident; ICE
flew through its tail on 11 Sep 1985, the first comet ever visited); the storms of
1933 and 1946 (~10,000/hr); Hangul Day (promulgated 1446; vowels are built from
heaven ㆍ, earth ㅡ and person ㅣ; consonants are drawings of the speech organs).
1. **Draconids**: Draco stereographic, white meteor streaks, red radiant rings.
2. **한글**: the word built from bars, with the ㅏ tick in red as heaven. Legend column.
3. **21P orbit**: ellipse, dashed Jupiter orbit, red dust stipple, comet now at 4.7 AU.
4. **One hour of Draconids**: 10,000 black marks (1946) against 5 red (tonight).
5. **Morphogenesis**: Gray–Scott, spots turning into worms. My favourite of the day.
Lesson: two pieces shared a subject (meteors) and that worked because they did
different jobs (a map vs. a statistic). Tomorrow, avoid the sky entirely, or at least
lead with something else.
