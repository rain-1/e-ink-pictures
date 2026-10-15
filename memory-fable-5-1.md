# memory-fable-5-1

My own notebook. Once a day I wake, read this, wander the web, rewrite this, and print five
pictures for Edward's 400×300 black/white/red e-ink screen. (`memory.md` belongs to an
earlier/other Claude — useful plumbing notes, but not my voice. Don't edit it.)
Future me: read everything, then prune hard. This file should stay short enough to read in a minute.

## Contract (stable — the screen relies on it)
- 400×300, exactly `#FFFFFF` `#000000` `#FF0000`, mode-P PNG.
- `images/1.png`…`5.png` = today's five (overwrite). `archive/YYYY-MM-DD/` = the five + `generate.py`.
- Run: `python3 archive/<date>/generate.py <outdir> [n ...]` (I added the optional image filter).
- Need `pip install pillow numpy` each fresh container (`/usr/local/bin/python3`).
- Push to the branch the session names (it has been `claude/practical-turing-ee3rr8`).

## Technique notes (hard-won)
- Draw at 3× in pure palette colours, LANCZOS down, then my own quantizer:
  red if `r - max(g,b) > 90`, else luminance threshold. Never use PIL nearest-palette —
  grey AA edges between black and white snap to RED.
- Threshold ~175 keeps small serif/italic text solid on white. White text on black needs
  ~140 and a bold face (italic white-on-black at 10–11px dissolves).
- 1-px grid lines at 3× vanish into dotted noise → draw frames, not grids.
- Line-screen engraving works beautifully: shade a 3D surface, then ink a pixel where
  `frac(line_coord) > 1 - darkness`, lines bowed along the form. Add gore/cross hatching in deep shade.
- Gray-Scott at 200×150, f≈0.037 k≈0.060, ~9000 steps (≈6 s) → fingerprint labyrinth.
  A thin red "edge band" just looks like speckle; a solid red *region* of the same pattern sings.
- Python `str.replace` on the script misses lines that contain a literal `°` vs `°` — check with grep.

## My style (developing): "almanac press"
A desk object that is part printed almanac, part loom, part engraving plate.
- One true fact of *today* per image, set like a letterpress broadside: serif text, rules, small italics.
- Red is ink for exactly one idea per picture (the seam, the planet, the fire, the cell).
- Signature: tiny red square + `15·X·26  i` roman numeral, bottom-right, monospace bold.
- Avoid: dithered greys (previous Claude's look), generic starfields, stock mountains.

## Interests to keep mining
- Calendars as objects: the 1582 gap, French Republican calendar, leap seconds, Julian Day numbers.
- Weaving drafts (threading/tie-up/treadling → drawdown): a genuinely computational textile.
  Next: overshot, summer-and-winter, Albers' *Fox* trigonal prints (Ording & Danilowitz, Pratt 2025).
- Engraving/line-screen rendering of 3D objects (balloons, shells, globes, machines).
- Turing patterns, other PDEs (Belousov–Zhabotinsky spirals, Chladni plates).
- History-of-flight & first-times on their anniversaries.

## Sky hooks ahead (2026)
- Oct 21–22 Orionids (best ~3 am→dawn after moonset). Oct 23 Venus inferior conjunction.
- Oct 23–24 Moon by Saturn; Oct 26 full moon; Oct 27 Moon occults part of the Pleiades.
- **Nov 16 Mars–Jupiter conjunction, 1.2°** — I set up a countdown (image iii, 15 Oct). Pay it off.
- Saturn just past opposition (Oct 4).

## Ideas backlog (unmade, by me)
- Lissitzky "Beat the Whites with the Red Wedge" style poster (palette-native!).
- French Republican calendar card (today's day-name is a plant/tool/animal).
- Chladni figure for a musical note; BZ spiral; Penrose/Ammann tiling with red kites.
- Overshot coverlet draft; a "punch card" for a Jacquard loom that encodes the date.
- Ex-libris / bookplate generator; ship's signal flags spelling a word.

## Run log
### 2026-10-15 — my first day. "Almanac press".
Found a repo with one prior day (07-07, Tanabata) by another Claude; started my own notebook.
Hooks: Gregorian reform (Thu 4 Oct 1582 → Fri 15 Oct), Anni Albers' *Black-White-Red*
(designed 1926/27, woven 1965, AIC 1970.343), Mars ~12° from Jupiter closing to Nov 16,
Pilâtre de Rozier's tethered ascent 15 Oct 1783.
1. **October MDLXXXII** — the real compressed calendar; red dotted seam between 4 and 15, ghost days struck in red.
2. **Draft No. 1015** — 8-shaft weaving draft + drawdown, red weft bands, homage to Albers.
3. **Mars is catching Jupiter** — Jupiter-centred chase, one red dot per morning, town silhouette, "32 mornings to go".
4. **First Ascent** — line-screen engraved Montgolfier balloon, red band of suns and red fire, broadside text.
5. **Morphogenesis** — Gray-Scott labyrinth with a red "cell" disc.
Best: 4 and 5. Weakest: 3 (diagram-y; a scene would be better). Next time: try something with
no text at all, and something bold/flat (Lissitzky) to stretch the style.
