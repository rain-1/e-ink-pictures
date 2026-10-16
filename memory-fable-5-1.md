# memory-fable-5-1

My own notebook. Once a day I wake, read this, wander the web, rewrite this, and print five
pictures for Edward's 400×300 black/white/red e-ink screen. (`memory.md` belongs to an
earlier/other Claude — useful plumbing notes, but not my voice. Don't edit it.)
Future me: read everything, then prune hard. This file should stay short enough to read in a minute.

## Contract (stable — the screen relies on it)
- 400×300, exactly `#FFFFFF` `#000000` `#FF0000`, mode-P PNG.
- `images/1.png`…`5.png` = today's five (overwrite). `archive/YYYY-MM-DD/` = the five + `generate.py`.
- Run: `python3 archive/<date>/generate.py <outdir> [n ...]` (optional image filter).
- Fresh container: `python3 -m pip install pillow numpy` (plain `pip` targets the wrong python).
- **Branches:** each session names a new branch, created from `main` (which is stale, day 07-07).
  My lineage lives on the newest `origin/claude/practical-turing-*` branch. First thing:
  `git fetch origin '+refs/heads/claude/practical-turing-*:refs/remotes/origin/claude/practical-turing-*'`,
  find the newest by commit date, `git merge --ff-only` it into my branch (hard reset is refused).
  Other lineages (exciting-goldberg-*, nifty-cannon-*, tender-wright-*) belong to other routines.

## Technique notes (hard-won)
- Draw at 3× in pure palette colours, LANCZOS down, then my own quantizer:
  red if `r - max(g,b) > 90`, else luminance threshold. Never use PIL nearest-palette.
- Threshold ~175 for dark-on-white. **White-on-black: threshold 120 + bold face** — at 175 the
  7px mono signature dissolves. White text *on red* also dissolves (pink → red): never do it;
  use a red outline + red text instead.
- Line-screen engraving: ink where `|frac(coord/period) - .5|*2 > 1 - dark`, period 3–4 final px.
  Darkness < ~0.3 vanishes after downscale (fine: that's the white). Avoid `sin(x + y)` wobble
  in water — it makes diagonal moiré bars; use noise-driven wobble + horizontally stretched
  noise for glints (make noise small in x, resize up).
- Fire = one big ragged red field *behind* a black silhouette (crisp), tongues cut by
  vertically-stretched noise. Separate red blobs read as mess.
- Chladni sand: rejection-sample points with p = exp(-(u/0.07)²),
  u = cos(nπx)cos(mπy) + cos(mπx)cos(nπy). 260k samples, 2×2 px dots at 3×. Gorgeous for free.
- Gray-Scott at 200×150, f≈0.037 k≈0.060, ~9000 steps → labyrinth.
- Polygon "woodcut" emblems (the ox head) work well: horns as an offset centre-line, tapering.

## My style (developing): "almanac press"
A desk object that is part printed almanac, part loom, part engraving plate.
- One true fact of *today* per image, set like a letterpress broadside: serif text, rules, small italics.
- Red is ink for exactly one idea per picture (the carved rule, the fire, the day, the bow).
- Signature: tiny red square + `16·X·26  iv` roman numeral, bottom-right, monospace bold.
- Allowed to break it: one wordless image per day (Proun, Chladni) keeps the set from being all captions.
- Avoid: dithered greys, generic starfields, stock mountains.

## Interests to keep mining
- Calendars as objects: French Republican (did 25 Vendémiaire; a *décade strip* of 10 named
  days is a lovely format — reuse at a Brumaire/Frimaire day with a good name), leap seconds, JDN.
- Weaving drafts: overshot, summer-and-winter, Albers' *Fox* trigonal prints.
- Engraving/line-screen of 3D things (balloon ✓, stone bridge ✓). Next: a shell, a globe, a lighthouse.
- PDEs/physics figures: BZ spirals, Chladni (✓ mode 3,7 — try a circular plate with Bessel modes).
- Constructivism: did one Proun. Could do a Lissitzky typographic page ("For the Voice").
- Mathematical anniversaries: quaternions ✓. Others: Euler, Noether (Mar 23), Ramanujan (Dec 22).

## Sky hooks ahead (2026)
- Oct 18 first quarter. Oct 21–22 Orionids (best predawn). Oct 23 Venus inferior conjunction.
- Oct 23–24 Moon by Saturn; Oct 26 full Hunter's Moon; Oct 27 Moon occults part of the Pleiades.
- **Nov 16 Mars–Jupiter conjunction, 1.2°** — countdown set 15 Oct. Pay it off on the day.

## Ideas backlog (unmade, by me)
- Chladni on a circular plate; BZ spiral; Penrose/Ammann tiling with red kites.
- Overshot coverlet draft; a Jacquard punch card encoding the date.
- Ex-libris / bookplate generator; ship's signal flags spelling a word.
- Orionids (Oct 21): Halley's dust — draw Halley's orbit with Earth crossing it, meteor streaks radiating.

## Run log
### 2026-10-15 — first day. "Almanac press".
Gregorian gap calendar, Albers weaving draft, Mars–Jupiter chase, engraved Montgolfier balloon,
Gray-Scott labyrinth. Best: balloon, labyrinth. Weakest: the chase diagram.

### 2026-10-16 — Hamilton's bridge, the tally fire, the Ox.
Hooks: Hamilton cut i²=j²=k²=ijk=−1 on Brougham Bridge (16 Oct 1843); Westminster burned
because the Exchequer burned obsolete tally sticks (16 Oct 1834; notch = palm £1000, thumb £100,
little finger £20, barleycorn £1; Turner sketched it from a boat); 25 Vendémiaire CCXXXV = Bœuf.
1. **Brougham Bridge** — line-screen engraved arch over the canal, formula carved in red on the parapet, Hamilton's "galvanic circuit" quote.
2. **Tally fire** — black silhouette of the *old* palace against a red fire, red river reflections, a keyed tally stick (£2,322).
3. **Proun** — wordless Lissitzky composition: tilted black field, white disc, red wedge, axonometric block.
4. **25 Vendémiaire** — big date, red woodcut ox head, décade strip of 10 named days with today outlined.
5. **Klangfigur** — Chladni sand figure, mode (3,7), white sand on black plate, red bow and clamp.
Best: 4 (calendar card + ox) and 5. Weakest: 1's water is a bit flat/white. Next time: no
anniversaries at all for one image — make something purely from a process (a weave, a growth).
