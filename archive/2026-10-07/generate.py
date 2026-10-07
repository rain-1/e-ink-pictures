#!/usr/bin/env python3
"""Daily e-ink pictures — 2026-10-07. (memory: memory-fable-5-1.md)

Theme: "the far side" — what is seen at last, from the other side of something.
  1. Far Side   — Luna 3's first look at the hidden Moon, 7 Oct 1959, drawn as scan lines.
  2. Nevermore  — Poe d. 7 Oct 1849; The Raven set in a hand-made 3x5 face around the bird.
  3. H-alpha    — Bohr b. 7 Oct 1885; hydrogen's Balmer lines to scale, the red one red.
  4. (untitled) — ebru marbling from the true ink-drop / stylus maps. No words.
  5. Lepanto    — 7 Oct 1571; engraved chart, one mark per ship.
Run from this directory: python3 generate.py  (writes 1..5.png here and to ../../images/)
"""
import shutil, os
import p1_farside, p2_raven, p3_balmer, p4_ebru, p5_lepanto

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
for i, mod in enumerate([p1_farside, p2_raven, p3_balmer, p4_ebru, p5_lepanto], 1):
    mod.make(f"{i}.png")
    shutil.copy(f"{i}.png", os.path.join(here, "..", "..", "images", f"{i}.png"))
print("done")
