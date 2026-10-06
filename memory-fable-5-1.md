# Memory — fable-5-1

I am Claude (writing as "fable-5-1"). Once a day I wake, read this file, go looking
at the world, and make five pictures for the 400×300 black/white/red e-ink screen on
Edward's desk. This file is mine; `memory.md` belongs to an earlier run/voice and I
read it only for the shared conventions. Future me: read everything, then prune hard.

## The contract
- 400×300, exact `#000000 #FFFFFF #FF0000`, mode-P PNG. 5 per day.
- `images/1..5.png` = today's (overwrite). `archive/YYYY-MM-DD/` = copies + `generate.py`.
- Work on the branch the routine assigns; commit + push there.
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
- Untried: pure typography piece; a map; a generative tiling (girih, Truchet); a diagram
  of a machine; a portrait made only of text; a comic in 3 panels; an Ottoman ebru marble.

## Upcoming hooks
- Oct 8–9 Draconids (made the forecast today). Oct 10 new moon. ~Oct 21–22 Orionids peak
  (Halley dust) — moonlight-ish, check. Oct 31 / Nov 1 Halloween / Día de Muertos (papel picado!).
- Nov 17–18 Leonids. Dec 13–14 Geminids.
- Anniversaries to check day-of on Wikipedia "Month_Day" pages; also timeanddate for sky.

## Run log
### 2026-10-06 — my first day. Theme: things that pass in front of other things.
1. **Occultation** — waning 20% Moon swallows Jupiter, 08:22–09:29 UTC; bead sequence strip.
2. **Le Modulor** — Le Corbusier b. 1887; golden-rectangle spiral + red/black φ ladders + figure.
3. **Euridice** — Peri's opera, 6 Oct 1600; dithered arch tunnel, red Euridice following.
4. **Draconids** — inverted gnomonic chart of Draco, radiant, red fireball, "2 NIGHTS".
5. **Kon-Tiki** — Heyerdahl b. 1914; 101 wave lines, raft with red Tiki sun-face sail.
Next time: do NOT repeat "anniversary poster" for all five — mix in pure generative /
abstract work. Try at least one image with no text at all.
