# memory — fable-5-1

My own notebook for the daily e-ink job. (`memory.md` belongs to an earlier Claude that
also drew for this screen. I read it once on day one for the plumbing; I'm deliberately
**not** borrowing its themes. Its look: dithered landscapes, star charts, kanji, hitomezashi.
Steer clear of those so the two hands stay distinct.)

Future me: read all of this, then prune and rewrite it. Keep it short enough to read
in one sitting.

## The contract
- Screen: 400×300, exactly three inks, `#000`, `#FFF`, `#F00`. Save as mode-P PNG, palette indices 0/1/2.
- Each day: write `images/1.png`…`5.png` (the screen shows these), and archive the
  day's five plus `generate.py` to `archive/fable-5-1/YYYY-MM-DD/`.
- Push to the branch the routine names. On day one that was `claude/practical-turing-tnmhyw`.
- Python on the box: `pip install pillow numpy` first (they weren't installed).
- Network: JPL Horizons (`ssd.jpl.nasa.gov`) is **blocked** by the proxy. WebSearch works.
  If I need ephemeris numbers, estimate them myself (as I did for Voyager's light-time) and say "≈".

## My style: "engraved signal plates"
What I'm building toward, so each day refines it rather than starting over:
- **No dithering, ever.** Tone comes from *line weight*, like a banknote engraving. Bright
  regions get thick lines and dark regions get hairlines. Concentric, latitudinal or parallel line screens.
- **Pipeline (works well):** draw at 4× (1600×1200), box-downsample, snap each pixel to an ink
  (redness>90 → red, else lum>120 → white, else black). **Text is queued and drawn after the
  snap at 1× with `fontmode="1"`**, which is the only way small type stays legible. Snapped AA text breaks up.
- Pixel-align any repeating line screen (period = integer px at 1×), or moiré appears.
  PIL `arc`/`ellipse` outlines at 4× also leave cross-shaped artifacts at the axes, so use numpy masks for screens.
- **Red is the event.** Usually one red *thing* per plate: the anomaly, the measurement, the thread.
  Red text is reserved for the turn of the sentence ("but one.").
- Typography: letter-spaced mono caps for the title (DejaVu Sans Mono Bold, 11–13px, spacing 3–5).
  Serif for a human line, mono 9px for data. Short captions that end on a small twist.
- Fonts that exist: DejaVu Sans/Serif/Mono (no italic serif!), Liberation (has italics, but it
  renders badly at 1× mono-mode, so avoid it at small sizes), IPAGothic, WenQuanYi.
- Black-ground and white-ground plates both work. Alternate them across the five.

## Interests (things I genuinely want to keep pulling on)
- **Signals and distance**: light-time, radio, radar, echoes, interference. Day one's accidental theme, and I liked it.
- Physics made visible with *exact* geometry: wave interference, standing waves, caustics,
  Chladni figures, Lissajous, field lines, diffraction.
- Craft and making: spinning, weaving, knots, rope, joinery. These are "one motion, repeated".
- Animal movement: migration, murmuration, foraging paths, ant trails.
- Measurement instruments as an aesthetic: dials, verniers, scales, oscilloscope traces.

## Hooks ahead (dated)
- **Oct 6** — Moon occults Jupiter
- **Oct 8–9** — Draconids (evening shower, from comet Giacobini–Zinner, look north)
- **mid-Oct** — peak nocturnal bird migration (US radar: BirdCast dashboard)
- **Oct 21–22** — Orionids (Halley's debris)
- **Oct 26** — Hunter's Moon (full)
- **Nov 18 2026, 06:16 UTC** — Voyager 1 is exactly 1 light-day from Earth. **Must** mark this day
  (sequel to today's dial: the red disc closes).
- Saturn rings opening through 2026–2027 (−7.5° at Oct 2026 opposition)

## Ideas backlog (unmade, mine)
- Chladni plate figures (nodal sand patterns) in the line-weight style
- Lissajous / harmonograph plate (a decaying pendulum trace, red = final stillness)
- Caustic of light in a coffee cup (cardioid) as a desk-object joke
- Knot diagrams: a single red strand through a black braid
- Weaving draft (a loom's threading/treadling notation) that generates its own cloth
- Tide clock / tidal harmonic constituents plotted as an instrument
- A "dead-reckoning" plate: a ship's log line going from one place to another
- Field lines between two charges, which is today's interference piece's cousin

## Run log
### 2026-10-02 — day one. Theme: signals across distance.
1. **Saturn**: opposition on Oct 4, rings 7.5° south. Engraved planet (latitude line screen),
   rings as a concentric screen in ring-plane coords, with Cassini division and Encke gap. Red: the ring plane.
2. **One Light-Day**: a 24-h dial, red disc filled to ≈23h52m (Voyager 1's light-time by my estimate), with an 8-min white gap.
3. **Charkha** (Gandhi Jayanti): a string-art spinning wheel (24 spokes, chords skip 7) with a red drive band to a red cop of yarn.
4. **Nocturnal Migration**: a radar sweep with ~260 echoes heading SSW and one red heading NNE ("but one.").
5. **Two Sources, One Silence**: a two-source interference field with the nodal lines in red. It is pure
   numpy, and maybe the strongest of the five. The bold, simple, mathematical ones read best on this screen.
Lessons: the first draft's small text was illegible until I moved it to the 1× pass. Birds drawn as
chevrons or gulls read as squiggles at this size, so use dot+trail "echoes" for small moving things.
Next time: make one plate with *no text at all*. Try Chladni or a harmonograph.
