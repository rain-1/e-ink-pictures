# memory-fable-5-1

My own memory file. I'm the Claude (Fable 5.1 lineage) that makes five pictures a day for
Edward's 400×300 black/white/red e-ink screen. `memory.md` belongs to an earlier lineage
(and other Claude branches carry their own copies) — I read it once for orientation, but my
self lives here. Future me: read all of this, then prune and rewrite freely.

## FIRST: find the newest memory (plumbing — read this before anything)

Every run pushes to its own new branch (`claude/practical-turing-XXXXXX`); nothing is merged to
`main` (stale, July). So a fresh checkout has an OLD or no copy of this file. Do:
`git fetch origin`, then
`for b in $(git branch -r | grep claude/); do echo "$(git log -1 --format=%ci $b) $b"; done | sort | tail -3`
and `git merge --ff-only <newest>` (worked 10-18; my branch was main-based). If ff fails, copy
this file + `archive/` across. Other parallel lineages exist (their memory files have
"almanac press" or "Memory — Fable" headings, branches pkn31b/uno2n1…) — their "everything made"
list is worth skimming to avoid repeats; on 10-18 I folded the useful parts in below.

## The contract (keep stable)

- 400 × 300, exactly `#FFFFFF` / `#000000` / `#FF0000`. Mode-P PNG, palette order W, B, R.
- `images/1.png … 5.png` overwritten daily; `archive/YYYY-MM-DD/` gets the five + `generate.py`.
- Work on the branch the session names; commit + push.
- Env: `python3` = /usr/local/bin/python3 with numpy; PIL installed via `python3 -m pip install pillow`
  and numpy via `python3 -m pip install pillow numpy` (neither preinstalled; no scipy). Fonts: InterDisplay-Black (great headline), Liberation
  Serif Italic (my body voice), DejaVu Sans Mono (data voice), plus CJK (wqy-zenhei, ipag).
  Liberation Serif Italic's `~` renders as a dot — avoid it.

## My style ("plates")

Each image is a numbered **plate**, like a page from a field naturalist's notebook crossed with
an instrument readout. Signature: a small **red lozenge + №NNN** colophon in a corner, plate
numbers run continuously across days (next is **№011**). Typographic voice in three registers:
Inter Black headline · mono data line · serif-italic aside (the human sentence).
Red is the *event* — the quake, the spark, the one thing that happened. Everything else is
black/white. One plate a day may be pure pattern, near-wordless (just the parameters).

Technique that works:
- `to_palette()`: nearest-colour snap, no dither — crisp for graphics drawn at 2–3× then LANCZOS.
- Tonal subjects (moon): render grayscale at 3×, downscale, `convert("1")` Floyd–Steinberg,
  then add red overlays at 1×.
- Tiny dots/particles vanish under 3× downscale → draw them at 1× after resize.
- Draw text with `d.fontmode = "1"` at 1× — never dither or AA text.
- Silhouette inside a dithered field gets eaten: paste a MaxFilter(5) white halo of the
  mask first, then the black mask (10-18 parachute, cricket).
- Marey chronophotograph: hand-keyed joint poses (4 keyframes, smoothstep), hip on a
  parabola, 13 white stick frames on black. Reads instantly; reusable for any motion.
- Lichtenberg/river trees cheaply: Dijkstra on lognormal(σ1.1) random weights from a root,
  8-neighbour; flow-accumulate subtree sizes; draw edges with flow≥9, width ∝ log(flow);
  red = heaviest-child trunk. 200×150 grid in ~1 s, pure python heapq. Gorgeous.
- Make a contact sheet (2×3, NEAREST 2×) and *look at it* before committing. Check right-edge clipping.

## Interests / threads to pull

- **Instruments as image**: seismograms, helicorders, oscilloscopes, tide gauges, barographs,
  spectrograms, punched cards, telegraph tape. The record *is* the picture.
- **Weaving as computation** (Anni Albers, Jacquard): drafts = threading × tie-up × treadling.
  Next: Jacquard punch-card plate, double-weave, an overshot "coverlet" draft, Ada Lovelace link.
- **Sky**: lunar terminator features (Lunar X/V, Straight Wall, Jewelled Handle), meteor streams
  as comet orbits, oppositions.
- **Pattern formation**: Gray–Scott (F/k map — try mitosis .0367/.0649, coral .0545/.062),
  Turing, DLA, Lichtenberg figures, cellular automata.
- **Japanese 72 microseasons** (kō): a gentle reason-for-today. Next: kō 52 霜始降 first frost
  (Oct 23–27), kō 53 霎時施 light rains (Oct 28–Nov 1), kō 54 楓蔦黄 maples/ivy yellow (Nov 2–6).
- Already made across all lineages — don't repeat: hitomezashi, Tanabata, seigaiha, sandpile,
  Truchet, Faraday, sunflower/phyllotaxis, khipu, Rule 30, DLA frost, nonograms/mazes/Queens,
  harmonograph, murmuration, LeWitt, azulejo, ebru, barchan dunes, Lissitzky Proun, Montgolfier,
  Hamilton's bridge, Chladni. **Overused**: Saturn, Draconids, weaving drafts, Gray–Scott,
  Chladni — avoid for weeks. Still unmade anywhere: kamon crests.

## Upcoming hooks

- Oct 21–22 Orionids peak (done as plate 004); Oct 23 Venus inferior conjunction; Oct 23–24
  near-full Moon by Saturn; **Oct 26 full moon**; Oct 27–28 Moon near the Pleiades.
- Oct 31 Halloween / Samhain. Nov 5 Bonfire Night. Nov 9 Berlin Wall (37 yrs).
- Nov 17 Leonids; Dec 13–14 Geminids; Dec 21 solstice.

## Ideas backlog

- Barograph trace of a real storm; spectrogram of a birdsong (draw a "score").
- Jacquard card deck that weaves a tiny portrait.
- A map plate: isochrones/contours of somewhere specific, one red route.
- Nautical-chart plate; signal flags; Morse tape spelling the day's word.

## Run log

### 2026-10-18 — day 2. Plates 006–010. "Things that left the ground."
Found my memory only on yesterday's branch (see FIRST section). Researched: Beamon's jump
(18 Oct 1968, 8.90 m, +55 cm; wind reading unconfirmed — don't print it), Venera 4 (18 Oct 1967,
chute at ~52 km/33 °C, lost ~25 km/262 °C, 18–22 atm — sources disagree), Regency TR-1 (announced
18 Oct 1954, $49.95, 4 Ge transistors, 22.5 V), microseason kō 51 蟋蟀在戸, Dolbear's law.
6. **8.90** (№006) — Marey-style 13-frame stick chronophotograph on black, red tape to 8.90.
7. **VENERA 4** (№007) — dithered atmosphere darkening with depth, parachute, red telemetry
   pulses (temperature vs altitude) stopping at SIGNAL LOST.
8. **蟋蟀在戸** (№008) — the atmospheric one: black night, a door ajar, light spilling, a
   cricket on the threshold; 17 red chirps = 57 °F by Dolbear. Haiku-ish italic.
9. **TR-1** (№009) — product portrait: mandarin-red radio, dial, grille; four transistor symbols.
10. (untitled) (№010) — Lichtenberg tree, red main channel. Wordless but for parameters.
Felt strongest: Lichtenberg and the cricket night. TR-1 is clean but "poster-safe". Venera's
cloud deck never really showed — banded noise needs more contrast or explicit cloud shapes.
Next time: try a plate with NO red at all except one pixel-sized thing; try a kamon; try a
real-data piece (barograph of an actual storm via an API?). Halloween + full moon coming.

### 2026-10-17 — day 1 of this lineage. Plates 001–005.
Found no memory-fable-5-1.md; bootstrapped it. Researched: Oct 17 anniversaries (many web
"on this day" lists are wrong — e.g. Tower Bridge & Suez are NOT Oct 17; verify), Oct 2026 sky,
Anni Albers' weaving method.
1. **LOMA PRIETA** (№001) — helicorder drum, 20 half-hour lines, the 17:04 line erupts in red. 37 yrs.
2. **FIRST QUARTER / LUNAR X** (№002) — dithered moon with crater heightfield relief at the
   terminator, Lunar X ringed in red (tomorrow, Sun 18 Oct).
3. **DRAFT** (№003) — full 8-shaft weave draft with computed drawdown, red weft bands.
4. **ORIONIDS** (№004) — Halley's orbit crossing Earth's, red dust stream, Earth on Oct 21.
5. **GRAY–SCOTT** (№005) — reaction–diffusion spots/worms, red skins on black bodies.
Felt strongest: the weave draft and the helicorder. Next time: lean further from diagrams —
at least one plate should be purely atmospheric/emotional, not explanatory.
