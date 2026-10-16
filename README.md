EffortLevelingSupport
===

tkinter を使った、ポケモンの努力値振りをサポートする GUI ツールです。

- Docker: 対応!
- Python: 3.15!
- Linter: Ruff 0.17!
- Test: pytest 9.1!
- GUI: tkinter (Tk 8.6) 。 Docker ではブラウザ (noVNC) から操作します

## パッと実行してみたい

```bash
docker compose up --build
```

- ブラウザで http://localhost:6080/vnc.html?autoconnect=true を開くと、 GUI が表示されます
- `EV` に振りたい努力値、 `to` に同時に育てるポケモン数を入れて `Calculate!` を押すと、下に結果が出ます
    - 例: `252` と `3` → `Give power-item each of them 7 times in flock battle. And then kick 7 pokemons' ass`
    - 数字以外や 0 以下を入れると `Please input valid numbers.` と出ます
- 止めるときは `Ctrl+C` (別ターミナルなら `docker compose down`) です
- ポートはホストの `127.0.0.1:6080` だけに公開します。 VNC にパスワードはないので、ほかのマシンへ公開しないでください
- 6080 が使用中なら `ELS_PORT=16080 docker compose up --build` のようにホスト側のポートを変えられます

lint とテストもコンテナの中で動きます。

```bash
docker compose run --rm app ruff check .
docker compose run --rm app ruff format --check .
docker compose run --rm app xvfb-run -a pytest
```

- `ruff` はエラーがなければ `All checks passed!` などを出して終了コード 0 で終わります
- `pytest` は仮想ディスプレイ (Xvfb) 上で GUI のテストまで実行します
- GitHub Actions (`.github/workflows/ci.yml`) でも、 push と pull request のたびに同じ 3 コマンドを実行します。デプロイや公開はしません

Docker を使わずに動かすなら、 Tk 付きの Python 3.15 と [uv](https://docs.astral.sh/uv/) を用意して次のとおりです。

```bash
uv run python effort_leveling_support.py
uv sync && uv run ruff check . && uv run pytest
```

## どんなツール?

![eff](https://user-images.githubusercontent.com/28250432/107610242-8226dd00-6c84-11eb-96ba-1aa984da26ad.png)

以下の条件のときが対象。

- n体以上のポケモンにeずつ努力値を振りたい
- ただしパワー系アイテムが一個しかない

以下のようなことを教えてくれます

- 「パワーアイテムを各ポケモンに順番に持たせそれぞれ群れバトルx戦せよ」
- 「その後、パワーアイテムをもたせず一体戦をy戦せよ」

計算は第6世代 (XY / ORAS) の仕様を前提にしています。

- 群れバトルは相手が5体で、1体あたり努力値1
- パワー系アイテムは1体あたり +4 → 持たせたポケモンは群れバトル1戦で 25
- 学習装置で、持たせていないポケモンも群れバトル1戦で 5
- 一体戦は1戦で 1
