#!/usr/bin/env python3
"""
Longxia Vlog fallback BGM generator.

This script is intentionally a fallback for offline/course environments. For
public social publishing, prefer a licensed music library and keep the source.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import shutil
import struct
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path


SAMPLE_RATE = 44100
DEFAULT_PEAK = 0.32

NOTES = {
    "C3": 130.81,
    "D3": 146.83,
    "E3": 164.81,
    "G3": 196.00,
    "A3": 220.00,
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "G4": 392.00,
    "A4": 440.00,
    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
    "G5": 783.99,
    "A5": 880.00,
}


@dataclass(frozen=True)
class Mood:
    name: str
    bpm: int
    melody: tuple[tuple[str, float], ...]
    chords: tuple[tuple[str, str, str], ...]
    percussion: bool
    swing: float


MOODS: dict[str, Mood] = {
    "warm-memory": Mood(
        name="warm-memory",
        bpm=82,
        melody=(
            ("E4", 1.0),
            ("G4", 1.0),
            ("A4", 1.5),
            ("G4", 0.5),
            ("E4", 1.0),
            ("C5", 1.0),
            ("A4", 1.0),
            ("G4", 1.0),
        ),
        chords=(("C3", "G3", "E4"), ("A3", "E4", "C5"), ("G3", "D4", "A4")),
        percussion=False,
        swing=0.04,
    ),
    "clean-training": Mood(
        name="clean-training",
        bpm=92,
        melody=(
            ("C4", 0.75),
            ("E4", 0.75),
            ("G4", 1.0),
            ("A4", 0.5),
            ("G4", 1.0),
            ("E4", 1.0),
            ("D4", 0.75),
            ("C4", 1.25),
        ),
        chords=(("C3", "G3", "E4"), ("G3", "D4", "A4"), ("E3", "A3", "E4")),
        percussion=True,
        swing=0.02,
    ),
    "upbeat-social": Mood(
        name="upbeat-social",
        bpm=108,
        melody=(
            ("G4", 0.5),
            ("A4", 0.5),
            ("C5", 0.75),
            ("A4", 0.25),
            ("G4", 0.5),
            ("E4", 0.5),
            ("G4", 0.5),
            ("A4", 1.0),
        ),
        chords=(("C3", "G3", "E4"), ("D3", "A3", "G4"), ("A3", "E4", "C5")),
        percussion=True,
        swing=0.01,
    ),
    "jiangnan-lite": Mood(
        name="jiangnan-lite",
        bpm=76,
        melody=(
            ("E4", 1.5),
            ("G4", 1.0),
            ("A4", 1.5),
            ("G4", 1.0),
            ("E4", 1.5),
            ("C5", 1.0),
            ("A4", 1.5),
            ("G4", 1.0),
        ),
        chords=(("C3", "G3", "E4"), ("D3", "A3", "G4"), ("A3", "E4", "C5")),
        percussion=False,
        swing=0.07,
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate fallback BGM for Longxia Vlog assets."
    )
    parser.add_argument("output_dir", help="Directory for bgm.wav and bgm.mp3")
    parser.add_argument(
        "--mood",
        choices=sorted(MOODS),
        default="warm-memory",
        help="BGM mood preset",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=60.0,
        help="Duration in seconds",
    )
    parser.add_argument(
        "--volume",
        type=float,
        default=0.75,
        help="Relative volume, 0.1-1.0",
    )
    parser.add_argument(
        "--keep-wav",
        action="store_true",
        help="Keep bgm.wav after mp3 conversion",
    )
    return parser.parse_args()


def envelope(position: float, duration: float, attack: float, release: float) -> float:
    if duration <= 0:
        return 0.0
    if position < attack:
        return position / attack
    if position > duration - release:
        return max(0.0, (duration - position) / release)
    return 1.0


def add_tone(
    left: list[float],
    right: list[float],
    start: float,
    duration: float,
    frequency: float,
    gain: float,
    pan: float,
    harmonic: bool = True,
) -> None:
    start_i = max(0, int(start * SAMPLE_RATE))
    end_i = min(len(left), int((start + duration) * SAMPLE_RATE))
    if start_i >= end_i:
        return

    attack = min(0.08, duration * 0.2)
    release = min(0.28, duration * 0.35)
    left_gain = gain * math.cos((pan + 1) * math.pi / 4)
    right_gain = gain * math.sin((pan + 1) * math.pi / 4)

    for index in range(start_i, end_i):
        rel = (index - start_i) / SAMPLE_RATE
        env = envelope(rel, duration, attack, release)
        base = math.sin(2 * math.pi * frequency * rel)
        if harmonic:
            base += 0.24 * math.sin(2 * math.pi * frequency * 2 * rel)
            base += 0.08 * math.sin(2 * math.pi * frequency * 3 * rel)
        sample = base * env * gain
        left[index] += sample * left_gain
        right[index] += sample * right_gain


def add_noise_hat(
    left: list[float], right: list[float], start: float, duration: float, gain: float
) -> None:
    start_i = max(0, int(start * SAMPLE_RATE))
    end_i = min(len(left), int((start + duration) * SAMPLE_RATE))
    for index in range(start_i, end_i):
        rel = (index - start_i) / SAMPLE_RATE
        env = math.exp(-rel * 42)
        noise = random.uniform(-1.0, 1.0) * env * gain
        left[index] += noise * 0.6
        right[index] += noise * 0.6


def add_soft_kick(
    left: list[float], right: list[float], start: float, duration: float, gain: float
) -> None:
    start_i = max(0, int(start * SAMPLE_RATE))
    end_i = min(len(left), int((start + duration) * SAMPLE_RATE))
    for index in range(start_i, end_i):
        rel = (index - start_i) / SAMPLE_RATE
        env = math.exp(-rel * 14)
        freq = 82 - 34 * min(1.0, rel / duration)
        sample = math.sin(2 * math.pi * freq * rel) * env * gain
        left[index] += sample
        right[index] += sample


def normalize(left: list[float], right: list[float], peak: float) -> None:
    max_value = max(max(abs(v) for v in left), max(abs(v) for v in right), 0.001)
    factor = peak / max_value
    for index in range(len(left)):
        left[index] *= factor
        right[index] *= factor


def fade_edges(left: list[float], right: list[float], duration: float) -> None:
    fade_in = int(min(1.0, duration * 0.1) * SAMPLE_RATE)
    fade_out = int(min(2.5, duration * 0.16) * SAMPLE_RATE)
    total = len(left)

    for index in range(fade_in):
        factor = index / max(1, fade_in)
        left[index] *= factor
        right[index] *= factor

    for offset in range(fade_out):
        index = total - fade_out + offset
        factor = (fade_out - offset) / max(1, fade_out)
        left[index] *= factor
        right[index] *= factor


def render(mood: Mood, duration: float, volume: float) -> tuple[list[float], list[float]]:
    total_samples = int(SAMPLE_RATE * duration)
    left = [0.0] * total_samples
    right = [0.0] * total_samples
    beat = 60 / mood.bpm
    random.seed(f"longxia-{mood.name}-{duration}")

    # Soft chord pad.
    bar = beat * 4
    chord_index = 0
    start = 0.0
    while start < duration:
        chord = mood.chords[chord_index % len(mood.chords)]
        for note_index, note in enumerate(chord):
            pan = (-0.45, 0.0, 0.45)[note_index]
            add_tone(left, right, start, bar * 1.05, NOTES[note], 0.055, pan)
        start += bar
        chord_index += 1

    # Lead melody.
    cursor = beat * 2
    melody_index = 0
    while cursor < duration - beat:
        note, beats = mood.melody[melody_index % len(mood.melody)]
        note_duration = beats * beat
        pan = -0.18 if melody_index % 2 == 0 else 0.18
        swing = mood.swing * beat if melody_index % 2 else 0
        add_tone(
            left,
            right,
            cursor + swing,
            note_duration * 0.92,
            NOTES[note],
            0.12,
            pan,
        )
        cursor += note_duration
        melody_index += 1

    # Gentle pulse for social/training moods.
    if mood.percussion:
        cursor = 0.0
        beat_index = 0
        while cursor < duration:
            if beat_index % 4 == 0:
                add_soft_kick(left, right, cursor, 0.28, 0.11)
            if beat_index % 2 == 1:
                add_noise_hat(left, right, cursor, 0.08, 0.018)
            cursor += beat
            beat_index += 1

    peak = DEFAULT_PEAK * max(0.1, min(volume, 1.0))
    normalize(left, right, peak)
    fade_edges(left, right, duration)
    return left, right


def write_wav(path: Path, left: list[float], right: list[float]) -> None:
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for l_sample, r_sample in zip(left, right):
            l_int = int(max(-1.0, min(1.0, l_sample)) * 32767)
            r_int = int(max(-1.0, min(1.0, r_sample)) * 32767)
            frames.extend(struct.pack("<hh", l_int, r_int))
        wav.writeframes(frames)


def convert_to_mp3(wav_path: Path, mp3_path: Path) -> bool:
    if shutil.which("ffmpeg") is None:
        return False

    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(wav_path),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "160k",
            str(mp3_path),
        ],
        check=True,
    )
    return True


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    mood = MOODS[args.mood]
    duration = max(5.0, min(args.duration, 180.0))
    left, right = render(mood, duration, args.volume)

    wav_path = output_dir / "bgm.wav"
    mp3_path = output_dir / "bgm.mp3"
    write_wav(wav_path, left, right)

    converted = convert_to_mp3(wav_path, mp3_path)
    if converted and not args.keep_wav:
        wav_path.unlink(missing_ok=True)

    print(f"BGM mood: {mood.name}")
    print(f"Duration: {duration:.1f}s")
    if converted:
        print(f"Output: {mp3_path} ({os.path.getsize(mp3_path) / 1024:.0f} KB)")
    else:
        print(f"Output: {wav_path} (ffmpeg not found; mp3 skipped)")
        print("Install ffmpeg or provide a licensed bgm.mp3 before rendering.")


if __name__ == "__main__":
    main()
