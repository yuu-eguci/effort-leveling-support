# syntax=docker/dockerfile:1
FROM python:3.15-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

# 公式 slim イメージは Tk のライブラリを含まないため libtk8.6 を入れます。
# Xvfb (仮想ディスプレイ) 、 x11vnc 、 websockify + noVNC でブラウザから GUI を操作できるようにします。
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libtk8.6 xvfb xauth x11vnc websockify fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Debian の novnc パッケージは nodejs まで入って大きくなるため、 noVNC の公式 release を使います。
ADD --checksum=sha256:b1003a11b6e6e8d8f7f5e5586daae7f8ca651d8aee0aa155ff9ac841c48f52c6 \
    https://github.com/novnc/noVNC/archive/refs/tags/v1.7.0.tar.gz /tmp/novnc.tar.gz
RUN mkdir /opt/novnc \
    && tar -xzf /tmp/novnc.tar.gz -C /opt/novnc --strip-components=1 \
    && rm /tmp/novnc.tar.gz

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
# noVNC の画面と、その先の VNC サーバーが応答すれば healthy です。
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --start-interval=1s --retries=3 \
    CMD ["python", "docker/healthcheck.py"]
CMD ["docker/start-gui.sh"]
