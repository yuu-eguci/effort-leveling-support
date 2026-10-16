import subprocess
import sys
from pathlib import Path

import pytest

from effort_leveling_support import calculate

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    ("ev", "num", "expected"),
    [
        (252, 1, (10, 2)),
        (252, 3, (7, 7)),
        (252, 6, (5, 2)),
        (255, 2, (8, 15)),
        (25, 1, (1, 0)),
        (24, 1, (0, 24)),
    ],
)
def test_calculate_returns_flock_and_single_battle_counts(ev, num, expected):
    assert calculate(ev, num) == expected


def test_calculate_handles_large_ev():
    assert calculate(5000, 1) == (200, 0)


@pytest.mark.parametrize(("ev", "num"), [(0, 1), (-1, 1), (252, 0), (252, -3)])
def test_calculate_rejects_non_positive_values(ev, num):
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
