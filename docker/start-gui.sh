#!/bin/sh
# 仮想ディスプレイ上で GUI を起動し、 noVNC (ポート 6080) から見えるようにします。
set -eu

export DISPLAY=:0
# 停止したコンテナを再起動したときに残っている、前回の Xvfb のロックを消します。
rm -f /tmp/.X0-lock /tmp/.X11-unix/X0
Xvfb "$DISPLAY" -screen 0 350x170x24 -nolisten tcp &
xvfb_pid=$!

# Xvfb の準備ができるまで最大 10 秒待ちます。
tries=0
until [ -e /tmp/.X11-unix/X0 ]; do
    if ! kill -0 "$xvfb_pid" 2>/dev/null || [ "$tries" -ge 100 ]; then
        echo "Xvfb did not start." >&2
        exit 1
    fi
    tries=$((tries + 1))
    sleep 0.1
done

x11vnc -display "$DISPLAY" -localhost -forever -shared -nopw -quiet &
websockify --web /opt/novnc 6080 localhost:5900 &

exec python effort_leveling_support.py
