import subprocess
import sys
from collections import deque
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


def fewest_battles_by_bfs(num, max_ev):
    """持たせる相手や回数を自由に組み合わせたときの最小の戦闘数を、幅優先探索で求めます。

    戦闘は、パワーアイテムを持ったポケモンの群れバトル (本人 25 、ほか 5) と一体戦
    (本人 5 、ほか 1) 、アイテムなしの群れバトル (全員 5) と一体戦 (全員 1) です。
    """
    moves = [(1,) * num, (5,) * num]
    for holder in range(num):
        moves.append(tuple(5 if i == holder else 1 for i in range(num)))
        moves.append(tuple(25 if i == holder else 5 for i in range(num)))
    start = (0,) * num
    battles = {start: 0}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for move in moves:
            # ポケモンの並び順は結果に関係しないので、並べ替えて同じ状態にまとめます。
            reached = tuple(sorted(a + b for a, b in zip(state, move, strict=True)))
            if reached[-1] <= max_ev and reached not in battles:
                battles[reached] = battles[state] + 1
                queue.append(reached)
    return {ev: battles[(ev,) * num] for ev in range(1, max_ev + 1)}


@pytest.mark.parametrize("num", range(1, MAX_POKEMONS + 1))
def test_calculate_gives_exact_ev(num):
    for ev in range(1, MAX_EV + 1):
        x, hordes, singles = calculate(ev, num)
        assert 25 * x + 5 * (num - 1) * x + 5 * hordes + singles == ev


def fewest_battles_in_turns(num, ev):
    """全員に同じ回数ずつ持たせる場合に限って、全組み合わせから最小の戦闘数を求めます。"""
    ev_per_x = 25 + 5 * (num - 1)
    return min(
        num * x + hordes + (ev - ev_per_x * x - 5 * hordes)
        for x in range(ev // ev_per_x + 1)
        for hordes in range((ev - ev_per_x * x) // 5 + 1)
    )


@pytest.mark.parametrize("num", [1, 2, 3])
def test_calculate_gives_fewest_battles(num):
    for ev, battles in fewest_battles_by_bfs(num, MAX_EV).items():
        x, hordes, singles = calculate(ev, num)
        assert num * x + hordes + singles == battles


@pytest.mark.parametrize("num", range(1, MAX_POKEMONS + 1))
def test_calculate_gives_fewest_battles_in_turns(num):
    # 幅優先探索は 4 体以上だと重いため、持たせ方を順番に限った総当たりで確かめます。
    for ev in range(1, MAX_EV + 1):
        x, hordes, singles = calculate(ev, num)
        assert num * x + hordes + singles == fewest_battles_in_turns(num, ev)


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
