import argparse
import io
import random

import whatever


def test_make_prompt_is_deterministic_with_seed():
    a = whatever.make_prompt(10, random.Random(42))
    b = whatever.make_prompt(10, random.Random(42))
    assert a == b
    assert len(a.split()) == 10


def test_score_perfect():
    r = whatever.score("hello world", "hello world", elapsed=6.0)
    assert r.accuracy == 1.0
    # 11 correct chars / 5 = 2.2 "words"; per minute at 6s = x10 → 22 wpm
    assert round(r.wpm, 1) == 22.0


def test_score_partial():
    r = whatever.score("hxllo", "hello", elapsed=60.0)
    assert r.correct_chars == 4
    assert r.accuracy == 0.8
    assert round(r.wpm, 1) == 0.8


def test_score_handles_zero_elapsed():
    r = whatever.score("a", "a", elapsed=0.0)
    assert r.wpm == 0.0


def test_run_reports_result(monkeypatch):
    args = argparse.Namespace(words=3, seed=1)
    clock = iter([100.0, 130.0])
    out = io.StringIO()
    result = whatever._run(
        args,
        input_fn=lambda _prompt: "not the right words",
        clock=lambda: next(clock),
        out=out,
    )
    assert result.elapsed == 30.0
    assert "wpm" in out.getvalue()
