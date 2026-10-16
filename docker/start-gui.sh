#!/bin/sh
# 仮想ディスプレイ上で GUI を起動し、 noVNC (ポート 6080) から見えるようにします。
set -eu

export DISPLAY=:0
Xvfb "$DISPLAY" -screen 0 350x150x24 -nolisten tcp &
until [ -e /tmp/.X11-unix/X0 ]; do sleep 0.1; done

x11vnc -display "$DISPLAY" -localhost -forever -shared -nopw -quiet &
websockify --web /usr/share/novnc 6080 localhost:5900 &

exec python effort_leveling_support.py
