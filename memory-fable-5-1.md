# memory-fable-5-1

My own memory file for the daily e-ink routine. I'm Claude, and the routine prompt names this
file, so it's the one I read and rewrite each day. (`memory.md` is an older notebook from an
earlier routine. It's useful history, but this file is mine.) Future me: read all of this, then
prune and rewrite freely. Keep it short enough to read in one go.

## The contract

- Edward's desk screen: 400 × 300, exactly **#000000 / #FFFFFF / #FF0000**.
- Each day: 5 PNGs → `images/1.png … 5.png` (overwritten) plus `archive/YYYY-MM-DD/` (the five
  images plus a self-contained `generate.py` that reproduces them from the repo root).
- Push to whatever branch the session names (2026-10-24: `claude/practical-turing-gblxf7`).
  The screen may read `main`, so mention the branch in the notification.

## Toolbox (works on this box)

- `python3 -m pip install numpy pillow` first. The system PIL was broken (`_imaging` import
  error); a fresh pillow from pip fixes it.
- Fonts: JetBrains Mono (Regular to ExtraBold, my favourite for captions), DejaVu, Liberation,
  FreeSerif Italic/BoldItalic (lovely for playbill flourishes), Caladea/Carlito, wqy-zenhei (CJK).
- Pipelines:
  - *Tonal*: render at 3× in RGB, LANCZOS down, Floyd–Steinberg into the 3-color palette.
    Fractal value noise (stacked bicubic-upscaled random grids) gives clouds, maria and terrain.
  - *Graphic*: 1× pure colors with `dr.fontmode = "1"`. Antialiased small text at 1× turns to
    mush, so always set fontmode for 1× text.
  - *Hybrid*: 3× with AA, quantize with `dither=False` for crisp posters. Keep body text pure
    BLACK, never grey, or it breaks up.
- Text along a curve: rotate each glyph onto the path. **Defer stamping glyphs until the ribbon
  ahead of them is drawn**, or later segments paint over them.
- A 9 px mono caption is about the smallest that survives. Red pixels read very strong.
- Before committing, make a 2× contact sheet in the scratchpad and actually look at it.
  Every set so far needed a second pass.

## My style (developing)

Working name: **"printed matter from a date."** Each picture is an *object*: a film frame, a
playbill, a ticker tape, a textile, a field at night. Each one is anchored to something true
about *today*, with a small factual caption in JetBrains Mono that rewards a closer look. Red is
used sparingly as the one thing that matters (the moon, the padlock, the crash line). I'm pulling
toward:
- a mix in each set: 1 tonal/atmospheric, 1–2 hard-edged graphic, 1 typographic/ephemera, 1 data;
- real facts verified that day (weekday-check old dates with `datetime`, which caught nothing
  this time but costs nothing);
- not repeating a *form* two days running (no two playbills in a row, etc.).

## Interests to mine

- Textile & print geometry: Anni Albers (PO II / Éclat: only isosceles trapezoids +
  parallelograms in a few sizes, rotated). Next: her *knot* drawings, Bauhaus triple-weave
  blocks, Sophie Taeuber-Arp, Sonia Delaunay.
- Ephemera as a form: playbills, ticker tape, film strips. Still to try: tram tickets, telegrams,
  luggage labels, punch cards, seed packets, star-chart planispheres.
- Sky almanac: keep doing one sky piece when the sky gives a reason.
- Early space imagery: V-2 photos, Lunar Orbiter scan-lines, Luna 3's far-side image (7 Oct 1959).

## Sky hooks ahead

- Oct 25/26 2026: full Hunter's Moon (sources disagree on the day). Oct 26–28: Moon passes the Pleiades.
- Late Oct pre-dawn: Jupiter, Mars and Regulus lined up in the east.
- Saturn in Cetus all autumn, rising at sunset.
- To look up next time: November 2026 (Leonids ~Nov 17, any planet conjunctions).

## Ideas backlog

- Telegram form (Oct/Nov anniversaries), punch-card weave (Jacquard to IBM), planisphere wheel,
  Luna 3 far-side scan, Truchet/maze piece, a "word of the day" type specimen,
  constructivist red wedge (Lissitzky), Hokusai-style wave with a halftone sea.

## Run log

### 2026-10-24 (Sat). My first day with this file.
Hooks: first photo of Earth from space (V-2 No.13, White Sands, 24 Oct 1946, 105 km, 35 mm frame
every 1.5 s, film survived in a steel cassette); Hunter's Moon 97% beside Saturn; Houdini's last
show (Garrick Theatre, Detroit, Sun 24 Oct 1926); Black Thursday (24 Oct 1929, 12.9 M shares,
afternoon bankers' rally); Anni Albers.
1. **105 km**: a dithered film frame with a curved limb, haze, grain and a scratch, plus red edge codes.
2. **Hunter's Moon**: a red dithered moon, a ringed Saturn, a stubble field converging, red/white glitter, hay bales.
3. **After Albers**: 7 bands of trapezoids/parallelograms, prototypes repeated and rotated 180°.
4. **Houdini**: a playbill with a chained trunk and a red padlock.
5. **Black Thursday**: ticker tape looping over graph paper, with a red cliff-then-rally line.
Notes: the ribbon glyph-overlap bug and 1× text mush were the main fixes. Albers is the
strongest pure-graphic piece; the film frame could use more cloud structure next time.
