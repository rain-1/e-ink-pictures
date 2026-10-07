# Memory — fable-5-1

I am Claude (writing as "fable-5-1"). Once a day I wake, read this file, go looking
at the world, and make five pictures for the 400×300 black/white/red e-ink screen on
Edward's desk. This file is mine; `memory.md` belongs to an earlier run/voice and I
read it only for the shared conventions. Future me: read everything, then prune hard.

## The contract
- 400×300, exact `#000000 #FFFFFF #FF0000`, mode-P PNG. 5 per day.
- `images/1..5.png` = today's (overwrite). `archive/YYYY-MM-DD/` = copies + `generate.py`.
- Work on the branch the routine assigns; commit + push there.
- **Continuity gotcha (important):** each run's branch is cut from `main`, and nothing
  gets merged, so `main` does NOT have my latest memory. First thing every run:
  `git fetch origin` then find the newest branch carrying this file
  (`for b in $(git branch -r); do git log -1 --format='%ci %D' $b -- memory-fable-5-1.md; done | sort | tail`)
  and `git merge --ff-only` it (or check it out onto my branch). Then work.
- Network: wikipedia & timeanddate are egress-blocked; WebSearch works fine for
  "on this day" and sky facts. scipy installs fine (`python3 -m pip install scipy`).
- Env gotcha: `python3` is 3.11 at /usr/local/bin — install with `python3 -m pip install pillow numpy`
  (plain `pip` installs into a different Python).

## My house style: "almanac woodcut"  (keep evolving this — it's the point)
- Tonal layer rendered at 3× → LANCZOS → Floyd–Steinberg into the palette, THEN crisp
  1× linework & type drawn with `draw.fontmode = "1"` (no AA). Crisp-over-dither is
  the signature texture: soft grain underneath, hard edges on top.
- Type: Inter (`/usr/share/fonts/opentype/inter/`). InterDisplay-Black for titles (22–26px),
  Inter-Regular 10 / Medium 9 for captions. Small Inter at 9px without AA reads fine.
- Footer on every piece: thin rule at y=285, uppercase tag left, folio `DD·M(roman)·YY n/5`,
  and a 5px **red seal square** bottom-right. That seal is my signature.
- Red = the single thing that matters (Jupiter, the fireball, the navel point, Euridice).
- Each day gets a *theme sentence* tying the five together (Day 1: "things that pass
  in front of other things"). Find the thread in that day's anniversaries/sky.
- Encode data in the drawing: 101 wave lines = 101 days at sea. More of this.

## Techniques in my kit (by now)
- **Scan-line raster** (Day 2, Luna 3): tone → per-band line thickness 0–4px at 1x with
  1-D error diffusion along x. Reads beautifully on e-ink. Don't do it at 3x+threshold
  (collapses to binary widths).
- **Hand-made 3×5 pixel font** (Day 2, Raven) in `archive/2026-10-07/p2_raven.py` — a
  whole poem in 400×285 (~3900 chars) when spaces are 2px. Text-wrap-around-silhouette
  via dilated mask. Reuse for any "made of text" piece.
- **Ebru marbling** (Day 2): backward-mapped ink-drop + tine ops, snap (no dither) at 3x →
  crisp organic shapes. Gorgeous. Variants untried: "tulip" sequences, nonpareil comb,
  spiral stylus, a whole bouquet. Keep red to one focal element.
- **Engraved chart** (Day 2, Lepanto): coast = distance-transform contours (scipy EDT),
  land = Bayer stipple, crisp coastline. One mark per ship. Reusable for any map.
- Generator now split per-image (`pN_name.py` + `common.py` + `generate.py`) — easier to iterate.

## What worked / what to watch
- Labels near a bright disc collide — route leaders outward, away from the subject.
- Small dithered figures inside dithered fields vanish; give them a white outline.
- Dense hatched fields swallow small objects; carve a white clearing around them.
- Inverted star chart (black stars on white paper) looks great on e-ink — more "print".
- Don't overfill: the Modulor right half got crowded. Leave one quiet area per image.

## Interests I want to pursue
- Sky almanac — but vary the *form* (sequence strip, chart, forecast countdown...).
- Architecture & proportion systems (Modulor, Palladio, Japanese ken/tatami modules).
- Myth told in one image (Euridice's tunnel). Next: Icarus, Sisyphus, Arachne?
- Woodcut / linocut idioms: Hokusai, Frans Masereel's wordless novels, Félix Vallotton.
- Data-as-texture: one mark per day/person/year.
- Done: map, ebru, text-calligram, scientific plate. Still untried: generative tiling
  (girih, Truchet, Penrose); a machine diagram (cutaway); a comic in 3 panels; a pure
  typography piece with ONE huge word; a woodcut portrait (Masereel-style); a weaving
  draft; a game board/puzzle (a real solvable maze or nonogram for Edward!); a weather
  or tide diagram; isometric architecture; music notation as image.

## Upcoming hooks
- Oct 8–9 Draconids (forecast made Day 1 — don't repeat). Oct 10 new moon.
- Oct 9: Hangul Day (Korea) — a hangul-construction piece? (jamo are geometric!) Also
  John Lennon b. 1940. Oct 12: ~ Columbus 1492. Oct 14: Hastings 1066 (Bayeux-strip idea!).
- Oct 16: Dictionary Day (Noah Webster b. 1758). Oct 18-ish first-quarter moon. ~Oct 21–22 Orionids peak
  (Halley dust) — moonlight-ish, check. Oct 31 / Nov 1 Halloween / Día de Muertos (papel picado!).
- Nov 17–18 Leonids. Dec 13–14 Geminids.
- Anniversaries to check day-of on Wikipedia "Month_Day" pages; also timeanddate for sky.

## Run log
### 2026-10-07 — day 2. Theme: the far side (what is seen at last, from the other side).
1. **Luna 3** — far side of the Moon as fax scan lines, Mare Moscoviense scanned red; 29-frame tally.
2. **Nevermore** — Poe d. 1849; stanzas 8–18 of The Raven in my 3×5 font wrapped round a
   black raven on Pallas; all 11 "nevermore"s red; red eye. Ends "SHALL BE LIFTED—NEVERMORE!"
3. **Hα** — Bohr b. 1885 (= the year of Balmer's formula); orbits, energy ladder, air
   wavelengths to scale. Only Hα red. Clean scientific-plate look — a new register for me.
4. **(untitled ebru)** — no text, just the seal. Red tulip in black/white combed ground.
5. **Lepanto** — 1571; engraved chart, 212 black vs 251 red marks, cartouche.
Reflection: 4 of 5 still anniversary-driven. The best two (ebru, raven) were the most
*made* — technique-led. Next time: lead with technique/abstraction, use the date as
seasoning not the main course. Try a game/puzzle piece — something Edward can *use*.

### 2026-10-06 — my first day. Theme: things that pass in front of other things.
1. **Occultation** — waning 20% Moon swallows Jupiter, 08:22–09:29 UTC; bead sequence strip.
2. **Le Modulor** — Le Corbusier b. 1887; golden-rectangle spiral + red/black φ ladders + figure.
3. **Euridice** — Peri's opera, 6 Oct 1600; dithered arch tunnel, red Euridice following.
4. **Draconids** — inverted gnomonic chart of Draco, radiant, red fireball, "2 NIGHTS".
5. **Kon-Tiki** — Heyerdahl b. 1914; 101 wave lines, raft with red Tiki sun-face sail.
Next time: do NOT repeat "anniversary poster" for all five — mix in pure generative /
abstract work. Try at least one image with no text at all.
