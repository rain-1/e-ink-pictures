#!/usr/bin/env python3
"""Ornithology, transcribed.

The eleven birds in 2.png sit on five wires at known coordinates in
generate.py. This script reads that flock as notation — wire height gives
pitch (C minor pentatonic, top wire highest), horizontal position gives
onset on a swing-eighth grid — and arranges the phrase as a small bebop
trio: alto sax (for Bird), walking bass, ride cymbal.

Outputs ornithology.mid; render to audio with fluidsynth + ffmpeg.
"""

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

# --- the flock, verbatim from generate.py: (x, wire), wire 0 = top wire ---
MELODY = [(70, 3), (100, 2), (124, 1), (150, 2), (186, 0), (214, 1),
          (244, 2), (272, 1), (300, 3), (330, 2), (352, 4)]
RED_IDX = 4  # the red bird — the high note

# wire -> pitch, C minor pentatonic, top wire highest
WIRE_PITCH = {0: 72, 1: 70, 2: 67, 3: 65, 4: 63}  # C5 Bb4 G4 F4 Eb4

TEMPO_BPM = 150
TPB = 480  # ticks per beat
SWING = 0.66  # offbeat lands two-thirds through the beat


def eighth_grid(melody):
    """Quantize bird x-positions onto a 16-slot swing-eighth grid (2 bars)."""
    x0, x1 = melody[0][0], melody[-1][0]
    step = (x1 - x0) / 15.0
    return [round((x - x0) / step) for x, _ in melody]


def swing_beat(pos):
    """Eighth-grid position -> beat offset with swing."""
    return pos // 2 + (SWING if pos % 2 else 0.0)


def t(beats):
    return int(round(beats * TPB))


def add_notes(track, channel, notes):
    """notes: list of (onset_beats, dur_beats, pitch, velocity); writes
    delta-timed note_on/note_off events."""
    events = []
    for onset, dur, pitch, vel in notes:
        events.append((t(onset), Message("note_on", channel=channel,
                                         note=pitch, velocity=vel)))
        events.append((t(onset + dur), Message("note_off", channel=channel,
                                               note=pitch, velocity=0)))
    events.sort(key=lambda e: e[0])
    now = 0
    for tick, msg in events:
        track.append(msg.copy(time=tick - now))
        now = tick
    return track


def bird_phrase(start_bar, octave=0, hold_last=1.5):
    """The eleven birds as (onset, dur, pitch, vel), starting at start_bar."""
    grid = eighth_grid(MELODY)
    base = start_bar * 4
    out = []
    for k, ((x, wire), pos) in enumerate(zip(MELODY, grid)):
        onset = base + swing_beat(pos)
        if k + 1 < len(grid):
            nxt = base + swing_beat(grid[k + 1])
            dur = (nxt - onset) * 0.88
        else:
            dur = hold_last
        pitch = WIRE_PITCH[wire] + 12 * octave
        vel = 118 if k == RED_IDX else (92 if pos % 2 == 0 else 84)
        out.append((onset, dur, pitch, vel))
    return out


def walking_bass(n_bars):
    """Quarter-note walk in C minor, two alternating shapes plus a turnaround."""
    shapes = [[36, 39, 41, 43], [44, 43, 41, 39], [36, 43, 46, 43],
              [41, 39, 38, 43]]
    notes = []
    for bar in range(n_bars - 1):
        line = shapes[bar % len(shapes)]
        for b, p in enumerate(line):
            notes.append((bar * 4 + b, 0.92, p, 88 if b % 2 == 0 else 78))
    # final bar: land on C, let it ring
    notes.append(((n_bars - 1) * 4, 3.5, 36, 96))
    return notes


def ride_pattern(n_bars):
    """Swing ride (51) with pedal hat (44) on 2 and 4; final crash-ish ride bell."""
    notes = []
    for bar in range(n_bars - 1):
        base = bar * 4
        for beat in range(4):
            notes.append((base + beat, 0.3, 51, 82 if beat % 2 == 0 else 72))
            if beat % 2 == 1:  # skip-note on 2 and 4
                notes.append((base + beat + SWING, 0.3, 51, 58))
                notes.append((base + beat, 0.3, 44, 70))
    notes.append(((n_bars - 1) * 4, 1.5, 53, 90))  # ride bell to finish
    return notes


def build():
    mid = MidiFile(ticks_per_beat=TPB)

    meta = MidiTrack()
    meta.append(MetaMessage("track_name", name="Ornithology (eleven birds on five wires)", time=0))
    meta.append(MetaMessage("set_tempo", tempo=bpm2tempo(TEMPO_BPM), time=0))
    meta.append(MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    mid.tracks.append(meta)

    # bars: 1 count-in | phrase 2-3 | phrase 4-5 (8va red bird) | phrase 6-7 | tag 8
    n_bars = 8

    sax = MidiTrack()
    sax.append(MetaMessage("track_name", name="alto sax (the birds)", time=0))
    sax.append(Message("program_change", channel=0, program=65, time=0))  # alto sax
    phrase = (bird_phrase(1)
              + [(o, d, p + (12 if k == RED_IDX else 0), v)
                 for k, (o, d, p, v) in enumerate(bird_phrase(3))]
              + bird_phrase(5, hold_last=0.8))
    # tag: the red bird gets the last word — C5 held over the final bar
    phrase.append((7 * 4 + SWING, 2.8, 72, 112))
    add_notes(sax, 0, phrase)
    mid.tracks.append(sax)

    bass = MidiTrack()
    bass.append(MetaMessage("track_name", name="walking bass", time=0))
    bass.append(Message("program_change", channel=1, program=32, time=0))  # acoustic bass
    add_notes(bass, 1, walking_bass(n_bars))
    mid.tracks.append(bass)

    drums = MidiTrack()
    drums.append(MetaMessage("track_name", name="ride", time=0))
    add_notes(drums, 9, ride_pattern(n_bars))
    mid.tracks.append(drums)

    return mid


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "ornithology.mid")
    build().save(out)
    grid = eighth_grid(MELODY)
    names = {63: "Eb4", 65: "F4", 67: "G4", 70: "Bb4", 72: "C5"}
    line = "  ".join(("[%s]" if k == RED_IDX else "%s") % names[WIRE_PITCH[w]]
                     for k, (_, w) in enumerate(MELODY))
    print("the flock reads:", line)
    print("swing-eighth grid:", grid)
    print("saved", out)
