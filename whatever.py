"""A tiny terminal typing-speed test.

Run: python whatever.py [--words N] [--seed S]
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass

WORDS = [
    "the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
    "river", "mountain", "keyboard", "python", "silence", "window",
    "forest", "lantern", "coffee", "ocean", "garden", "compiler",
    "whisper", "ember", "pocket", "cloud", "thunder", "ripple",
    "echo", "signal", "paper", "candle", "ladder", "anchor",
    "prism", "orbit", "canvas", "pebble", "spark", "harbor",
]


@dataclass(frozen=True)
class Result:
    typed: str
    target: str
    elapsed: float

    @property
    def correct_chars(self) -> int:
        return sum(a == b for a, b in zip(self.typed, self.target))

    @property
    def accuracy(self) -> float:
        if not self.target:
            return 1.0
        return self.correct_chars / len(self.target)

    @property
    def wpm(self) -> float:
        if self.elapsed <= 0:
            return 0.0
        return (self.correct_chars / 5) / (self.elapsed / 60)


def make_prompt(n: int, rng: random.Random) -> str:
    return " ".join(rng.choice(WORDS) for _ in range(n))


def score(typed: str, target: str, elapsed: float) -> Result:
    return Result(typed=typed, target=target, elapsed=elapsed)


def _run(args: argparse.Namespace, *, input_fn=input, clock=time.perf_counter, out=sys.stdout) -> Result:
    rng = random.Random(args.seed)
    target = make_prompt(args.words, rng)
    print("Type this, then press Enter:\n", file=out)
    print(f"  {target}\n", file=out)
    start = clock()
    typed = input_fn("> ")
    elapsed = clock() - start
    result = score(typed, target, elapsed)
    print(
        f"\n{result.wpm:.1f} wpm  ·  {result.accuracy * 100:.0f}% accurate  ·  {elapsed:.1f}s",
        file=out,
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tiny typing-speed test.")
    parser.add_argument("--words", type=int, default=15, help="number of words in the prompt")
    parser.add_argument("--seed", type=int, default=None, help="seed for deterministic prompts")
    args = parser.parse_args(argv)
    try:
        _run(args)
    except (EOFError, KeyboardInterrupt):
        print("\naborted.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
