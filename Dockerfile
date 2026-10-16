FROM python:3.15-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

# 公式 slim イメージは Tk のライブラリを含まないため libtk8.6 を入れます。
# Xvfb (仮想ディスプレイ) 、 x11vnc 、 noVNC でブラウザから GUI を操作できるようにします。
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libtk8.6 xvfb xauth x11vnc novnc fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    RUFF_CACHE_DIR=/tmp/ruff-cache

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked
COPY . .

EXPOSE 6080
CMD ["docker/start-gui.sh"]
