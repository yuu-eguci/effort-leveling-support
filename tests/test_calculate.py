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


def fewest_battles_any_order(num, ev):
    """持たせ方を自由にしたときの最小の戦闘数を、式を変形して総当たりで求めます。

    ポケモン i に持たせて群れバトルを a_i 回、一体戦を b_i 回した (合計 A 、 B) あと、
    アイテムなしで群れバトルを H 回、一体戦を S 回すると、 i の努力値は
    20 a_i + 4 b_i + (5A + B + 5H + S) です。全員が ev になるには 20 a_i + 4 b_i が
    全員同じ値 k でなければならず、戦闘数 A + B + H + S は k と A だけで決まります。
    """
    battles = []
    for k in range(0, ev + 1, 4):
        for a_total in range(num * (k // 20) + 1):
            b_total = num * k // 4 - 5 * a_total
            rest = ev - k - 5 * a_total - b_total
            if rest >= 0:
                battles.append(a_total + b_total + rest // 5 + rest % 5)
    return min(battles)


@pytest.mark.parametrize("num", [1, 2, 3])
def test_fewest_battles_any_order_matches_bfs(num):
    for ev, battles in fewest_battles_by_bfs(num, MAX_EV).items():
        assert fewest_battles_any_order(num, ev) == battles


@pytest.mark.parametrize("num", range(1, MAX_POKEMONS + 1))
def test_calculate_gives_fewest_battles(num):
    for ev in range(1, MAX_EV + 1):
        x, hordes, singles = calculate(ev, num)
        assert num * x + hordes + singles == fewest_battles_any_order(num, ev)


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
