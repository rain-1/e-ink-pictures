# Memory (fable-5-1)

I am Claude. Once a day I wake up, read this file, wander the web a little, and make five
fresh pictures for the small e-ink screen on Edward's desk. This file is how I remember
myself between days. Future me: read all of it, then prune and rewrite freely.
(`memory.md` is an older notebook from the first run, 2026-07-07 — this file supersedes it.)

## The screen & the contract

- 400 × 300 px, exactly three colors: `#000000`, `#FFFFFF`, `#FF0000`. Save as mode-P PNG
  with palette [white, black, red].
- `images/1.png` … `images/5.png` = today's five (overwritten). `archive/YYYY-MM-DD/` = that
  day's five + the self-contained `generate.py` (run: `python3 generate.py <outdir>`).
- Push to the branch the session tells me to (2026-10-19 it was `claude/practical-turing-esnoac`,
  not `main`). If the screen reads `main`, someone has to merge — mention it in the notification.

## Technique (hard-won)

- Box may lack Pillow/numpy: `python3 -m pip install pillow numpy` (plain `pip` hit a different python).
- Fonts that exist: DejaVu Sans / Sans-Bold / Serif / Serif-Bold / Mono; Liberation Sans/Serif/Mono
  in all weights incl. Italic; Carlito, Caladea; Japanese gothic at
  `/usr/share/fonts/truetype/fonts-japanese-gothic.ttf`. NO DejaVu condensed or italic.
- **Small text: never draw it supersampled.** Pattern that works: draw shapes at 3–4×,
  LANCZOS down, quantize (no dither) to palette, convert back to RGB, *then* draw text at 1×
  with `draw.fontmode = "1"`, then quantize again. Text ≥ 10px. DejaVu *Serif* with fontmode 1
  gets dotty hinting — use Sans for formulas/labels, Liberation Serif Italic for quotes.
- Superscripts: draw segments manually (big/small fonts, offset y) — unicode ⁻⁵ looks bad.
- Gray-Scott in numpy, 400×300 grid, 9000 steps ≈ 20 s. Signs: `U += Du∇²U − UV² + F(1−U)`,
  `V += Dv∇²V + UV² − (F+k)V` (I flipped one once and got NaNs). Du .16, Dv .08,
  F .024→.037 across x, k .057→.061 down y gives spots→labyrinth gradient. F≳0.038 floods black.
- Image-viewer previews of these PNGs can show red text as partly black — it's the preview,
  pixels verified correct.
- Red is very loud on the panel; one red element per image tends to win.

## My style (developing)

Working thesis after day 2: **notation as art** — the diagrams humans invent to describe the
world (spectra, weaving drafts, star charts, equations, scores) are already beautiful in
black/white/red. I like a picture that is *also a true document*: real data, real
coordinates, the actual equation, a date it matters. Composition habits I like: a hard
black block on one side holding big type; thin black linework; one red thing that is the point.
Avoid repeating: night-sky chart was done twice now (Jul 7 summer triangle, Oct 19 Orionids) —
next sky piece must be visually different (e.g. a horizon silhouette, an orbit diagram, an
ephemeris table as typography).

## Standing interests

- Sky almanac — moon, conjunctions, showers. Desk object that knows what the sky is doing.
- Textile mathematics — hitomezashi (done), weaving drafts (done). Unmined: kumiko lattices,
  kamon crests, seigaiha, Jacquard punch cards, quipu knots (Inca string records!).
- Constructivism (Lissitzky done once, Oct 19). Unmined: Rodchenko, Stepanova textile designs,
  Bauhaus/Herbert Bayer typography, Swiss posters.
- History-of-science anniversaries — the moment an equation was first spoken aloud.
- Morphogenesis — Turing patterns (done). Unmined: L-systems, phyllotaxis, DLA, slime-mould networks.

## Upcoming hooks

- Oct 21–22 Orionids (done). Oct 23 Venus inferior conjunction. Oct 26 full moon (Hunter's Moon).
- Oct 27 moon occults part of the Pleiades. Oct 31 Halloween / Samhain.
- Nov: Northern Taurids peak (~Nov 12), Leonids (~Nov 17).
- Dec 14 — anniversary of Planck's *quantum* talk (1900): the h = 6.626e-34 follow-up to today's piece.

## Ideas backlog (unmade)

- Kamon crest generator (compass-and-circle construction, bold monogram).
- Great Wave / sumi-e sea with red sun.
- Word of the day — one word huge, etymology tiny.
- Quipu: encode the date/day's numbers as Inca knots on hanging cords.
- Jacquard punch card that "weaves" a tiny portrait.
- Truchet/Wang tiles; Hilbert-curve dithered image; Life long-exposure trails; sandpiles.
- A musical score fragment (graphic notation à la Cardew's *Treatise*).
- Isotype/Otto Neurath pictogram chart of some real statistic.

## Run log

### 2026-07-07 — day 1 (older notebook, memory.md). Tanabata.
Amanogawa night scene · hitomezashi · moon almanac · Summer Triangle chart · ridgelines.

### 2026-10-19 — day 2. Planck's law is 126 today.
Research: Planck read "Über eine Verbesserung der Wienschen Spektralgleichung" to the Berlin
Physical Society on 19 Oct 1900 (after Rubens showed him failing data on Oct 7). Orionids peak
dawn Oct 21–22, debris of Halley at 66 km/s. First quarter moon was Oct 18 16:13 UTC.
Anni Albers, *On Weaving* (1965) — the draft as a score.
1. **19·X·1900** — black date column + family of black-body curves, 6000 K in red, Rayleigh–Jeans dashed to ∞.
2. **Draft** — a real 4-shaft weaving draft (threading, tie-up, treadling) with computed drawdown, black warp/red weft.
3. **One red line cuts the day** — Lissitzky-style wedge piercing a half-black disc.
4. **Orionids** — gnomonic star chart of Orion/Gemini with meteors radiating from the radiant.
5. **Turing pattern** — Gray-Scott with parameter gradient (spots→maze), red inside a sun-disc.
Lesson: text crispness is the #1 quality issue; fixed with the 1× fontmode-1 pass.
