#!/usr/bin/env python3
"""Terminal typing speed trainer with adaptive feedback."""

from __future__ import annotations

import argparse
import random
import textwrap
import time
from dataclasses import dataclass

WORD_BANK = {
    "easy": "cat dog sun milk tree smile book home river green table light happy quick bring".split(),
    "medium": "planet rhythm wonder bridge silver market gentle stream volume camera puzzle engine member".split(),
    "hard": "awkward oxygen sphinx zephyr rhythmic avalanche xylophone submerge whirlwind cryptic matrix".split(),
}


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


def run_round(round_number: int, word_count: int, level: str) -> RoundResult:
    target = build_prompt(word_count, level)
    print(f"\nRound {round_number} [{level.upper()}]")
    print(textwrap.fill(target, width=72))
    input("Press Enter to start typing... ")
    start = time.perf_counter()
    typed = input("> ")
    elapsed = time.perf_counter() - start
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Typing speed increaser: adaptive typing drills in your terminal."
    )
    parser.add_argument("--rounds", type=int, default=5, help="Number of rounds to run")
    parser.add_argument("--words", type=int, default=14, help="Words per round")
    parser.add_argument(
        "--seed", type=int, default=None, help="Optional random seed for repeatable prompts"
    )
    args = parser.parse_args()

    if args.rounds <= 0 or args.words <= 0:
        raise SystemExit("--rounds and --words must be positive integers.")

    if args.seed is not None:
        random.seed(args.seed)

    print("Typing Speed Increaser")
    print("Type exactly what you see, then press Enter.")

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


if __name__ == "__main__":
    main()
