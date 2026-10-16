import subprocess
import sys
from pathlib import Path

import pytest

from effort_leveling_support import MAX_EV, MAX_POKEMONS, calculate

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    ("ev", "num", "expected"),
    [
        (252, 1, (10, 0, 2)),
        (252, 3, (7, 1, 2)),
        (252, 5, (5, 5, 2)),
        (252, 6, (5, 0, 2)),
        (250, 2, (8, 2, 0)),
        (25, 1, (1, 0, 0)),
        (24, 1, (0, 4, 4)),
        (1, 6, (0, 0, 1)),
    ],
)
def test_calculate_returns_battle_counts(ev, num, expected):
    assert calculate(ev, num) == expected


def fewest_battles(ev, num):
    """全組み合わせを試して、ちょうど ev になる最小の戦闘数を求めます。"""
    ev_per_x = 25 + 5 * (num - 1)
    return min(
        num * x + hordes + (ev - ev_per_x * x - 5 * hordes)
        for x in range(ev // ev_per_x + 1)
        for hordes in range((ev - ev_per_x * x) // 5 + 1)
    )


@pytest.mark.parametrize("num", range(1, MAX_POKEMONS + 1))
def test_calculate_gives_exact_ev_with_fewest_battles(num):
    for ev in range(1, MAX_EV + 1):
        x, hordes, singles = calculate(ev, num)
        assert 25 * x + 5 * (num - 1) * x + 5 * hordes + singles == ev
        assert num * x + hordes + singles == fewest_battles(ev, num)


@pytest.mark.parametrize(
    ("ev", "num"),
    [(0, 1), (-1, 1), (253, 1), (5000, 1), (252, 0), (252, -3), (252, 7)],
)
def test_calculate_rejects_out_of_range_values(ev, num):
    with pytest.raises(ValueError):
        calculate(ev, num)


def test_import_does_not_start_gui():
    result = subprocess.run(
        [sys.executable, "-c", "import effort_leveling_support"],
        cwd=ROOT,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0
