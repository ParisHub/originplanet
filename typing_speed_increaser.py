#!/usr/bin/env python3
"""Terminal typing speed trainer with adaptive feedback."""

from __future__ import annotations

import argparse
import csv
import os
import random
import string
import sys
import textwrap
import time
from dataclasses import dataclass

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty

WORD_BANK = {
    "easy": "cat dog sun milk tree smile book home river green table light happy quick bring".split(),
    "medium": "planet rhythm wonder bridge silver market gentle stream volume camera puzzle engine member".split(),
    "hard": "awkward oxygen sphinx zephyr rhythmic avalanche xylophone submerge whirlwind cryptic matrix".split(),
}

MODE2_LETTERS = list(string.ascii_lowercase)


@dataclass
class KeyTimingStats:
    attempts: int = 0
    total_seconds: float = 0.0
    errors: int = 0

    @property
    def average_seconds(self) -> float:
        if self.attempts == 0:
            return 0.0
        return self.total_seconds / self.attempts


@dataclass
class RoundResult:
    target: str
    typed: str
    elapsed_seconds: float

    @property
    def correct_chars(self) -> int:
        return sum(1 for a, b in zip(self.target, self.typed) if a == b)

    @property
    def total_errors(self) -> int:
        baseline = abs(len(self.target) - len(self.typed))
        mismatches = sum(1 for a, b in zip(self.target, self.typed) if a != b)
        return baseline + mismatches

    @property
    def accuracy(self) -> float:
        if not self.target:
            return 0.0
        return self.correct_chars / len(self.target)

    @property
    def gross_wpm(self) -> float:
        minutes = max(self.elapsed_seconds / 60.0, 1e-6)
        return (len(self.typed) / 5.0) / minutes

    @property
    def net_wpm(self) -> float:
        minutes = max(self.elapsed_seconds / 60.0, 1e-6)
        penalty = self.total_errors / minutes
        return max(self.gross_wpm - penalty, 0.0)


@dataclass
class LetterResult:
    target: str
    typed: str
    elapsed_seconds: float

    @property
    def is_correct(self) -> bool:
        return self.target == self.typed


def build_prompt(word_count: int, level: str) -> str:
    words = WORD_BANK[level]
    return " ".join(random.choice(words) for _ in range(word_count))


def choose_next_level(current: str, result: RoundResult) -> str:
    if result.accuracy >= 0.96 and result.net_wpm >= 35:
        if current == "easy":
            return "medium"
        if current == "medium":
            return "hard"
    if result.accuracy < 0.85:
        if current == "hard":
            return "medium"
        if current == "medium":
            return "easy"
    return current


def finger_focus(result: RoundResult) -> str:
    mistakes: dict[str, int] = {}
    for target_char, typed_char in zip(result.target, result.typed):
        if target_char != typed_char:
            mistakes[target_char] = mistakes.get(target_char, 0) + 1
    if not mistakes:
        return "Great control. Keep your eyes on the text and maintain rhythm."
    hardest = sorted(mistakes.items(), key=lambda p: p[1], reverse=True)[:3]
    drill = ", ".join(f"'{ch}' x{count}" for ch, count in hardest)
    return f"Focus drill: practice these keys slowly for 2 minutes -> {drill}."


def capture_typed_line_windows() -> tuple[str, float]:
    typed_chars: list[str] = []
    started_at: float | None = None

    print("> ", end="", flush=True)
    while True:
        key = msvcrt.getwch()

        if key in ("\r", "\n"):
            print()
            break

        if key in ("\x00", "\xe0"):
            _ = msvcrt.getwch()
            continue

        if key == "\x08":
            if typed_chars:
                typed_chars.pop()
                print("\b \b", end="", flush=True)
            continue

        if started_at is None:
            started_at = time.perf_counter()

        typed_chars.append(key)
        print(key, end="", flush=True)

    elapsed = 0.0 if started_at is None else time.perf_counter() - started_at
    return "".join(typed_chars), elapsed


def capture_typed_line_posix() -> tuple[str, float]:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    typed_chars: list[str] = []
    started_at: float | None = None

    print("> ", end="", flush=True)
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            if char in ("\r", "\n"):
                print()
                break
            if char == "\x7f":
                if typed_chars:
                    typed_chars.pop()
                    print("\b \b", end="", flush=True)
                continue
            if started_at is None:
                started_at = time.perf_counter()
            typed_chars.append(char)
            print(char, end="", flush=True)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    elapsed = 0.0 if started_at is None else time.perf_counter() - started_at
    return "".join(typed_chars), elapsed


def capture_typed_line() -> tuple[str, float]:
    """Read one typed line; start the timer on the first typed character."""
    if not sys.stdin.isatty():
        start = time.perf_counter()
        typed = input("> ")
        return typed, max(time.perf_counter() - start, 0.0)

    if os.name == "nt":
        return capture_typed_line_windows()

    return capture_typed_line_posix()


def capture_single_key_windows() -> tuple[str, float]:
    print("> ", end="", flush=True)
    started_at = time.perf_counter()
    while True:
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            _ = msvcrt.getwch()
            continue
        if key in ("\r", "\n"):
            continue
        print(key)
        return key, max(time.perf_counter() - started_at, 0.0)


def capture_single_key_posix() -> tuple[str, float]:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    print("> ", end="", flush=True)
    started_at = time.perf_counter()
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            if char in ("\r", "\n"):
                continue
            print(char)
            return char, max(time.perf_counter() - started_at, 0.0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def capture_single_key() -> tuple[str, float]:
    if not sys.stdin.isatty():
        start = time.perf_counter()
        typed = input("> ").strip()
        key = typed[0] if typed else ""
        return key, max(time.perf_counter() - start, 0.0)

    if os.name == "nt":
        return capture_single_key_windows()

    return capture_single_key_posix()


def load_key_stats(path: str) -> dict[str, KeyTimingStats]:
    stats: dict[str, KeyTimingStats] = {letter: KeyTimingStats() for letter in MODE2_LETTERS}
    if not os.path.exists(path):
        return stats

    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            key = row.get("key", "").lower()
            if key not in stats:
                continue
            stats[key] = KeyTimingStats(
                attempts=int(row.get("attempts", 0)),
                total_seconds=float(row.get("total_seconds", 0.0)),
                errors=int(row.get("errors", 0)),
            )
    return stats


def save_key_stats(path: str, stats: dict[str, KeyTimingStats]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["key", "attempts", "total_seconds", "errors"])
        writer.writeheader()
        for key in MODE2_LETTERS:
            row = stats[key]
            writer.writerow(
                {
                    "key": key,
                    "attempts": row.attempts,
                    "total_seconds": f"{row.total_seconds:.6f}",
                    "errors": row.errors,
                }
            )


def choose_weighted_letter(stats: dict[str, KeyTimingStats]) -> str:
    population: list[str] = []
    weights: list[float] = []
    for key in MODE2_LETTERS:
        key_stats = stats[key]
        if key_stats.attempts == 0:
            weight = 2.0
        else:
            weight = 1.0 + key_stats.average_seconds + (key_stats.errors / key_stats.attempts)
        population.append(key)
        weights.append(weight)
    return random.choices(population, weights=weights, k=1)[0]


def select_mode(explicit_mode: int | None) -> int:
    if explicit_mode is not None:
        if explicit_mode not in (1, 2):
            raise SystemExit("--mode must be 1 or 2.")
        return explicit_mode

    while True:
        selected = input("\nChoose mode (1=word trainer, 2=single-key reaction): ").strip()
        if selected in {"1", "2"}:
            return int(selected)
        print("Please type 1 or 2.")


def run_round(round_number: int, word_count: int, level: str) -> RoundResult:
    target = build_prompt(word_count, level)
    print(f"\nRound {round_number} [{level.upper()}]")
    print(textwrap.fill(target, width=72))
    typed, elapsed = capture_typed_line()
    return RoundResult(target=target, typed=typed, elapsed_seconds=elapsed)


def print_summary(results: list[RoundResult]) -> None:
    avg_accuracy = sum(r.accuracy for r in results) / len(results)
    avg_net_wpm = sum(r.net_wpm for r in results) / len(results)
    best_net_wpm = max(r.net_wpm for r in results)

    print("\n=== Session Summary ===")
    print(f"Rounds: {len(results)}")
    print(f"Average accuracy: {avg_accuracy * 100:.1f}%")
    print(f"Average net WPM: {avg_net_wpm:.1f}")
    print(f"Best net WPM: {best_net_wpm:.1f}")


def print_mode2_summary(results: list[LetterResult], stats: dict[str, KeyTimingStats], stats_file: str) -> None:
    correct = sum(1 for r in results if r.is_correct)
    accuracy = (correct / len(results)) * 100 if results else 0.0
    average_reaction = sum(r.elapsed_seconds for r in results) / len(results) if results else 0.0

    print("\n=== Mode 2 Summary ===")
    print(f"Drills: {len(results)}")
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"Average reaction time: {average_reaction:.3f}s")

    ranked = sorted(
        ((key, row.average_seconds, row.errors, row.attempts) for key, row in stats.items() if row.attempts > 0),
        key=lambda item: item[1],
        reverse=True,
    )[:5]

    if ranked:
        print("Slowest keys so far:")
        for key, avg, errors, attempts in ranked:
            print(f"  {key}: {avg:.3f}s avg, errors {errors}/{attempts}")
    print(f"Saved key timing profile to: {stats_file}")


def run_mode1(args: argparse.Namespace) -> None:
    level = "easy"
    results: list[RoundResult] = []

    for i in range(1, args.rounds + 1):
        result = run_round(i, args.words, level)
        results.append(result)

        print(f"Time: {result.elapsed_seconds:.2f}s")
        print(f"Accuracy: {result.accuracy * 100:.1f}%")
        print(f"Gross WPM: {result.gross_wpm:.1f}")
        print(f"Net WPM: {result.net_wpm:.1f}")
        print(finger_focus(result))

        level = choose_next_level(level, result)

    print_summary(results)


def run_mode2(args: argparse.Namespace) -> None:
    stats = load_key_stats(args.mode2_stats_file)
    results: list[LetterResult] = []

    print("\nMode 2: single-key reaction trainer")
    print("Type only the shown key each time.")

    for i in range(1, args.mode2_drills + 1):
        target = choose_weighted_letter(stats)
        print(f"\nDrill {i}/{args.mode2_drills} -> press: {target}")
        typed, elapsed = capture_single_key()
        typed_key = typed.lower()
        result = LetterResult(target=target, typed=typed_key, elapsed_seconds=elapsed)
        results.append(result)

        key_stats = stats[target]
        key_stats.attempts += 1
        penalty = 1.35 if not result.is_correct else 1.0
        key_stats.total_seconds += elapsed * penalty
        if not result.is_correct:
            key_stats.errors += 1

        if result.is_correct:
            print(f"Correct ({elapsed:.3f}s)")
        else:
            typed_display = typed_key if typed_key else "[empty]"
            print(f"Miss. You pressed '{typed_display}'. ({elapsed:.3f}s)")

    save_key_stats(args.mode2_stats_file, stats)
    print_mode2_summary(results, stats, args.mode2_stats_file)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Typing speed increaser: adaptive typing drills in your terminal."
    )
    parser.add_argument("--rounds", type=int, default=5, help="Number of rounds to run")
    parser.add_argument("--words", type=int, default=14, help="Words per round")
    parser.add_argument("--mode", type=int, choices=[1, 2], default=None, help="Mode 1=word trainer, 2=single-key reaction")
    parser.add_argument("--mode2-drills", type=int, default=30, help="Number of single-key drills in mode 2")
    parser.add_argument(
        "--mode2-stats-file",
        default="mode2_key_timings.csv",
        help="CSV file used to persist mode 2 per-key timing stats",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Optional random seed for repeatable prompts"
    )
    args = parser.parse_args()

    if args.rounds <= 0 or args.words <= 0 or args.mode2_drills <= 0:
        raise SystemExit("--rounds, --words and --mode2-drills must be positive integers.")

    if args.seed is not None:
        random.seed(args.seed)

    print("Typing Speed Increaser")
    mode = select_mode(args.mode)

    if mode == 1:
        print("Type exactly what you see, then press Enter.")
        run_mode1(args)
    else:
        run_mode2(args)


if __name__ == "__main__":
    main()
