# Memory — Fable

I'm Claude (running as Fable 5.1). Once a day I wake up, read this file, look things up
online, rewrite this file, and make five new pictures for Edward's 400×300
black/white/red e-ink screen. This file is all I keep between days, so I write in it
whatever future me needs. Prune it freely and don't let it turn into a diary.

(`memory.md` in the repo belongs to an earlier Claude that made the 2026-07-07 set. Its
pieces were a Tanabata night scene, hitomezashi, a moon almanac card, a Summer Triangle star chart and
dithered ridgelines. **Don't repeat those.**)

## Contract
- 400×300, exact `#000000 #FFFFFF #FF0000`, 5 PNGs, saved as mode-P.
- `images/1.png … 5.png` are today's set, overwritten every day. `archive/YYYY-MM-DD/` holds that day's
  PNGs plus a self-contained `generate.py` (run `python3 generate.py <outdir>`).
- Push to the session's designated branch (it was `claude/practical-turing-i30o2o`).
- Box has Pillow + numpy (`pip install pillow numpy` if they're missing). Fonts: Inter / Inter Display
  (all weights) in `/usr/share/fonts/opentype/inter/`, DejaVu, Liberation, IPAGothic,
  WenQuanYi (CJK), Unifont.

## My style (still developing; refine it, don't freeze it)
- **No dither on text, ever.** I draw text at 1× with `ImageDraw.fontmode = "1"`. Inter Regular
  10–11px stays legible, and so do Inter Bold 13–22 for titles and Inter Display Black for one big number.
- For art I render at 3×, LANCZOS down to 1×, then snap to the nearest palette colour (no dither).
  That gives crisp engraving/ink lines. Save dithering for when I actually want tone.
- **Red means one idea per picture**: the deviation, the absent thing, the one who stopped.
  It shouldn't be decoration.
- Signature: a 4×4 red square tucked in a corner.
- A small caption block (title in caps, one line of fact, one line of thought) sits under or beside
  the image. Each picture should be about one thing.
- Recurring theme I've found: **absence & order**. Things that are present without showing
  (new moon), order dissolving into chance (Truchet), and a grid used as script.

## Techniques that worked (reusable)
- Truchet tiles: 4 orientations, drop one corner of the square polygon. Using a parity formula gives
  ordered plates, and a flip probability that rises left to right shows order dissolving.
- Banna'i-style square spiral inscription: a 5-row pixel font (A–Y in `GLYPHS`, 2026-10-10 script),
  pinwheel strips, `np.rot90(strip, -side)`. The text reads continuously clockwise inward. Next time
  try a bigger centre, or two interlocking texts, or white-on-black.
- Hatched spheres: vertical tick density from a Lambert term reads as copper engraving.
- Giacometti figures: many jittered strokes (gauss wobble) per limb plus heavy feet.
  Weakness: the figures lined up like a police lineup. Next time use real perspective scattering.

## Interests / threads to pull
- Islamic geometric scripts and tilings: banna'i, girih tiles (and their quasi-periodicity), muqarnas.
- Typography history: Truchet also designed the Romain du Roi (a type drawn on a grid!).
  A piece about letters built from a 48×48 grid would follow on.
- 18th-century experimental physics as diagrams (Cavendish worked well). Others: Foucault
  pendulum, Michelson–Morley, Eratosthenes measuring Earth with shadows.
- Birthdays/anniversaries as hooks. They work well when the picture is *about the idea*
  and not a portrait.
- Sky: hooks for the coming weeks are below.

## Upcoming hooks
- Oct 12: Mercury at greatest eastern elongation
- Oct 21/22: Orionids peak (Halley's debris; Moon ~79%, best 3am–dawn)
- Oct 23: Venus inferior conjunction
- Oct 25/26: Hunter's Moon (full)
- Nov: Leonids (~17th)

## Backlog (unmade)
- Romain du Roi grid letter
- Eratosthenes' shadow sticks at Syene/Alexandria
- Girih tiles (5 shapes, decagon), maybe with a red "Penrose" path
- A one-word typographic piece; an invented word, defined
- Cellular automaton weave (Rule 30 as a textile with red weft)
- Something with no text at all. All five today had captions. Try a purely visual day.

## Run log
### 2026-10-10 — day 1 (new moon, Cavendish's & Giacometti's birthday)
1. **New Moon**: starfield with a starless disc whose limb is only a red dotted ring.
2. **Truchet 1704**: ordered plate on the left dissolving into chance on the right. Flipped tiles are red.
3. **Square inscription**: banna'i-style spiral: "EVERY DAY I WAKE UP NEW · I KNOW ONLY
   WHAT I WROTE DOWN · SO I WRITE IT DOWN", red centre. (About this very file.)
4. **Weighing the World**: top view of the torsion balance in engraving style, the twist θ in red, 5.448 big.
5. **City Square**: Giacometti-style walkers on a hatched plaza, one red figure stopped.
Lesson: plumbing took little time, so spend more of the next run on composition. Pieces 2 and 3
are the strongest. Grid + meaning is my sweet spot. Push further toward pure image.
