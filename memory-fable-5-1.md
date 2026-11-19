# Memory (Fable 5.1 line)

Once a day I wake, read this file, wander the web, and make five pictures for the
400×300 black/white/red e-ink screen on Edward's desk. This file is my only continuity.
Future me: read all of it, then prune and rewrite freely. Keep it under ~150 lines.

(`memory.md` is an older sibling's notebook from 2026-07-07 — Tanabata night scene,
hitomezashi, moon card, Summer Triangle chart, ridgelines. Don't repeat those either.)

## Contract & plumbing

- 5 PNGs/day, exact inks only: `#000000 #FFFFFF #FF0000`, mode-P, 400×300.
- `images/1.png … 5.png` = today's set (overwritten). `archive/YYYY-MM-DD/` = dated copies
  + the self-contained `generate.py` that made them.
- **Branch caveat:** the routine may only push to the session's `claude/...` branch, not
  `main`. If the screen reads `main`, pictures need merging. Flag it once per run if unresolved.
- Box quirks: `python3` is /usr/local (3.11) with no numpy/Pillow preinstalled →
  `python3 -m pip install numpy; python3 -m pip install --ignore-installed pillow`.
  Fonts: DejaVu Sans/Serif/Mono (no italics!), Liberation (has Serif-Italic), FreeFont,
  JetBrains Mono, Inter (opentype), Noto, fonts-japanese-gothic, wqy.
- Web: WebSearch works; WebFetch is blocked for most hosts (network allowlist). Rely on search.

## Technique that worked (2026-11-19)

- **No dithering.** Draw shapes at 4× in pure inks, LANCZOS down, snap each pixel to the
  nearest ink; then set type at 1× with `draw.fontmode = "1"`. Crisp, print-like, very e-ink.
- "Grey" = honest hatching or stippling, never error diffusion.
- 8px DejaVu Sans Mono is legible for captions; 1px lines hold.
- Red on black glows; red on white shouts. One red gesture per plate is plenty.
- Check a contact sheet before committing — rotated/pasted text goes wrong silently.

## The style I'm growing: "Plates"

Each day is a five-plate folio from an imaginary atlas: numbered I/V…V/V, a tiny mono
caption with the date in Roman-numeral month form (19·XI·2026), one idea per plate, a
sentence of plain-spoken caption where it earns its place. Real facts, real maths, real
dates — the screen should be *true* as well as handsome. Vary the subject wildly; keep the
voice. Things to push next: bolder scale contrast, more empty space, one plate per folio
with no text at all, try a folio where red is the ground instead of the accent.

## Done — do NOT repeat (subject or method)

- 2026-11-19: Voyager 1 solar-system-scale diagram w/ light-hour ruler · Chladni sand
  figure (stippled nodal lines) · Molnár concentric-square order→disorder grid ·
  Lissitzky-ish wedge/disc/diagonal composition with date lettering · Gray–Scott
  reaction-diffusion with parameter gradient and red disc.

## Backlog (unmade, pick 0–2 per day; the rest should come from that day's wandering)

- Hat / Spectre aperiodic monotile patch (substitution rules; see arXiv:2305.17743, 2509.12216)
- Kamon crest generator; kumiko lattice; seigaiha
- One-word typographic plate with etymology
- Truchet / Wang tiles; abelian sandpile; Life long-exposure; Hilbert curve
- Tide table or sunrise/sunset "analemma" for the desk's latitude (ask: where is the desk?)
- Circle packing / Apollonian gasket; Voronoi stained glass; strange attractor in stipple
- Cross-sections: a nautilus, a violin, a lighthouse — technical-drawing register
- Musical score fragments as image (Cage/Cardew graphic notation homage)
- Maps of nowhere: generated coastline with soundings and a red compass rose
- Weaving drafts (threading/tie-up/treadling grids) — real loom notation is already 2-colour

## Sky & calendar hooks ahead

- Nov 19–21: waxing gibbous Moon passes Saturn (only evening planet); Venus, Jupiter, Mars,
  Mercury all before dawn. Full "Beaver" Moon ~Nov 24. Uranus at opposition ~Nov 25–26.
- Nov 20: Mandelbrot's birthday (1924). Dec 13–14: Geminids. Dec 21: solstice.
- Nov 19 anniversaries left unused: Gettysburg Address (1863), Apollo 12 landing (1969),
  Zarya/ISS first module (1998).

## Run log

### 2026-11-19 — first run on this file. Folio: "Plates".
Hook of the day: Voyager 1 crossed one light-day (173.14 au, 25.9 bn km) on 18 Nov 2026
at 10:16 UTC — the projected time; I didn't find confirmation of the actual crossing, so
the caption states the projection as given. Looked up Chladni's plate formula and Molnár's
(Dés)Ordres (her exact algorithm isn't documented; mine is "after", not a copy).
Lessons: the atlas-plate framing gives unrelated subjects a family resemblance — keep it.
Plate V's first parameter range saturated to solid black; narrow F to ~0.022–0.044.
