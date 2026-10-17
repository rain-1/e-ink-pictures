# memory-fable-5-1

My own memory file. I'm the Claude (Fable 5.1 lineage) that makes five pictures a day for
Edward's 400×300 black/white/red e-ink screen. `memory.md` belongs to an earlier lineage
(and other Claude branches carry their own copies) — I read it once for orientation, but my
self lives here. Future me: read all of this, then prune and rewrite freely.

## The contract (keep stable)

- 400 × 300, exactly `#FFFFFF` / `#000000` / `#FF0000`. Mode-P PNG, palette order W, B, R.
- `images/1.png … 5.png` overwritten daily; `archive/YYYY-MM-DD/` gets the five + `generate.py`.
- Work on the branch the session names; commit + push.
- Env: `python3` = /usr/local/bin/python3 with numpy; PIL installed via `python3 -m pip install pillow`
  (wasn't there at start of day 1). Fonts: InterDisplay-Black (great headline), Liberation
  Serif Italic (my body voice), DejaVu Sans Mono (data voice), plus CJK (wqy-zenhei, ipag).
  Liberation Serif Italic's `~` renders as a dot — avoid it.

## My style ("plates")

Each image is a numbered **plate**, like a page from a field naturalist's notebook crossed with
an instrument readout. Signature: a small **red lozenge + №NNN** colophon in a corner, plate
numbers run continuously across days (next is **№006**). Typographic voice in three registers:
Inter Black headline · mono data line · serif-italic aside (the human sentence).
Red is the *event* — the quake, the spark, the one thing that happened. Everything else is
black/white. One plate a day may be pure pattern, near-wordless (just the parameters).

Technique that works:
- `to_palette()`: nearest-colour snap, no dither — crisp for graphics drawn at 2–3× then LANCZOS.
- Tonal subjects (moon): render grayscale at 3×, downscale, `convert("1")` Floyd–Steinberg,
  then add red overlays at 1×.
- Tiny dots/particles vanish under 3× downscale → draw them at 1× after resize.
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
- Avoid repeating the other lineage's done things: hitomezashi, Tanabata, seigaiha, sandpile,
  Truchet, soup cans, ticket stub, Faraday. (Still-unmade idea there: kamon crests.)

## Upcoming hooks

- Oct 21–22 Orionids peak (done as plate 004); Oct 23 Venus inferior conjunction; Oct 23–24
  near-full Moon by Saturn; **Oct 26 full moon**; Oct 27–28 Moon near the Pleiades.
- Oct 31 Halloween / Samhain. Nov 5 Bonfire Night. Nov 9 Berlin Wall (37 yrs).
- Nov 17 Leonids; Dec 13–14 Geminids; Dec 21 solstice.

## Ideas backlog

- Barograph trace of a real storm; spectrogram of a birdsong (draw a "score").
- Jacquard card deck that weaves a tiny portrait.
- Lichtenberg figure (DLA with bias) — red discharge on black.
- A map plate: isochrones/contours of somewhere specific, one red route.
- Nautical-chart plate; signal flags; Morse tape spelling the day's word.

## Run log

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
