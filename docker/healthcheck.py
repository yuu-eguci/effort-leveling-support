"""noVNC の画面と VNC サーバーが応答するかを確かめます。

応答しなければ終了コード 1 で終わります。
"""

import socket
import sys
import urllib.request

try:
    with urllib.request.urlopen("http://localhost:6080/vnc.html", timeout=2) as res:
        res.read()
    with socket.create_connection(("localhost", 5900), timeout=2) as vnc:
        greeting = vnc.recv(12)
except OSError as error:
    sys.exit(f"unhealthy: {error}")
if not greeting.startswith(b"RFB "):
    sys.exit(f"unhealthy: unexpected VNC greeting {greeting!r}")
