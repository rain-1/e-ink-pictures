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
- Push to the branch the routine names (it changes every run: day 1 `…-tnmhyw`, day 2 `…-9rbypm`).
  **Runs are never merged into main.** At the start, find the newest branch carrying this file:
  `git fetch origin; for b in $(git branch -r); do git log -1 --format='%cd %D' --date=iso $b; done | sort`
  then `git merge --ff-only` it into today's branch so memory and archive carry forward.
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
- **Pure-numpy index arrays** (0/1/2 straight into a P image) beat the 4× pipeline for anything
  grid- or particle-based: weaving cells, sand grains. Use the 4× pipeline only for lines and curves.
- Particle sims make *texture* without dithering: Chladni sand = 70k grains drifting down |u|²
  with a kick ∝|u|, only ~140 steps (more steps → perfect thin lines, which looks too clean).
- A weaving drawdown only shows a pattern when cells are SOLID (warp-up black / weft white).
  Decorating each float with borders turns it to noise. Tromp-as-writ + mirrored point threading = diamonds.

## Interests (things I genuinely want to keep pulling on)
- **Signals and distance**: light-time, radio, radar, echoes, interference. Day one's accidental theme, and I liked it.
- Physics made visible with *exact* geometry: wave interference, standing waves, caustics,
  Chladni figures, Lissajous, field lines, diffraction.
- Craft and making: spinning, weaving, knots, rope, joinery. These are "one motion, repeated".
- Animal movement: migration, murmuration, foraging paths. (Did ants' path integration on day 2.)
- **Traces**: things that leave a record of their own motion (day 2's theme). Pens, sand, cloth, tracks.
- Measurement instruments as an aesthetic: dials, verniers, scales, oscilloscope traces.

## Hooks ahead (dated)
- **Oct 4** — Sputnik 1 anniversary (1957): 0.3 s beeps alternating 20.005 / 40.002 MHz, 1 W. Missed
  this year; a pulse-train plate for 2027.
- **Oct 6** — Moon occults Jupiter
- **Oct 8–9** — Draconids, near new moon (3%) so dark skies. ~5/hr, evening, radiant in Draco (look north)
- **mid-Oct** — peak nocturnal bird migration (US radar: BirdCast dashboard)
- **Oct 21–22** — Orionids (Halley's debris)
- **Oct 26** — Hunter's Moon (full)
- **Nov 18 2026, 06:16 UTC** — Voyager 1 is exactly 1 light-day from Earth. **Must** mark this day
  (sequel to today's dial: the red disc closes).
- Saturn rings opening through 2026–2027 (−7.5° at Oct 2026 opposition)

## Ideas backlog (unmade, mine)
- Caustic of light in a coffee cup (cardioid) as a desk-object joke
- Knot diagrams: a single red strand through a black braid
- Tide clock / tidal harmonic constituents plotted as an instrument
- Field lines between two charges, which is day 1's interference piece's cousin
- Weaving, part 2: overshot or block weaves (summer & winter); a draft where the red is the *warp*
- A slime-mould (Physarum) network solving a map; an L-system or a growth trace
- Rope/knot plates: a bowline drawn as one continuous over-under strand
- Patents as plates: the date a thing became official, drawn as an engraved diagram (worked well day 2)

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

### 2026-10-03 — day two. Theme: traces.
1. **Chladni** (no text, as promised): 9:4 mode on a centre-clamped square plate, 70k white grains on
   black, red clamp + red violin bow on the edge. The particle-sim sand texture is lovely.
2. **Path Integration**: a desert ant's wandering outbound walk (black), straight red line home,
   then a red systematic-search spiral because the integrator is slightly off.
3. **US 2,524,035**: the point-contact transistor, patent granted 3 Oct 1950. Engraved wedge, slab
   and base (each with its own line-screen direction). Small red sine in, big red sine out.
4. **Harmonograph**: 2:3 slightly detuned, white hairline, last 7% of the trace in red ("until it stops.").
5. **Draft No. 1003**: a full weaving draft (threading/tie-up/treadling) with a diamond-twill drawdown
   seeded by the date, four red weft picks. Probably the best of the set; the notation itself is the art.
Lessons: first drafts of grids looked like noise until I removed decoration. Engraved objects read
better when each part has its own hatch direction (vertical slab, horizontal wedge).
Next time: nothing physics-y, and nothing with a sine wave. Maybe typographic, or a map, or an L-system.
Try a plate that is mostly *red*.
