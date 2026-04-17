"""
Ski Balance Board – spusť přes start.bat (nebo: python server.py)
Nakloň desku doleva/doprava → šipky ← →
"""

import asyncio
import json
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

import websockets
from pynput.keyboard import Key, Controller

HTTP_PORT = 8080
WS_PORT   = 8765
THRESHOLD = 0.20   # 20 % náklonu = stisk klávesy (zbytek = dead zone)

keyboard    = Controller()
left_held   = False
right_held  = False


VIRTUAL_PREFIXES = ("192.168.56.", "192.168.99.", "172.17.", "172.18.", "172.19.")

def get_local_ip():
    # Zkus se připojit přes každý lokální gateway a vyber první reálnou WiFi/LAN IP
    candidates = []
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None):
            ip = info[4][0]
            if not any(ip.startswith(p) for p in VIRTUAL_PREFIXES):
                if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
                    if ip not in candidates:
                        candidates.append(ip)
    except Exception:
        pass
    if candidates:
        return candidates[0]
    # Záloha: UDP trick
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "?.?.?.?"


def start_http_server():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phone_gyro.html")
    with open(html_path, "rb") as f:
        html_content = f.read()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content)
        def log_message(self, *a):
            pass

    HTTPServer(("0.0.0.0", HTTP_PORT), Handler).serve_forever()


def set_keys(go_left: bool, go_right: bool):
    global left_held, right_held

    if go_left and not left_held:
        keyboard.press(Key.left)
        left_held = True
    elif not go_left and left_held:
        keyboard.release(Key.left)
        left_held = False

    if go_right and not right_held:
        keyboard.press(Key.right)
        right_held = True
    elif not go_right and right_held:
        keyboard.release(Key.right)
        right_held = False


async def handler(websocket):
    addr = websocket.remote_address
    print(f"📱 Telefon připojen: {addr[0]}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                raw_x = int(data.get("x", 16383))
                norm  = (raw_x - 16383) / 16383   # -1 .. +1

                set_keys(norm < -THRESHOLD, norm > THRESHOLD)

            except (json.JSONDecodeError, KeyError, ValueError):
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        set_keys(False, False)   # uvolni klávesy při odpojení
        print(f"📵 Telefon odpojen: {addr[0]}")


async def main():
    ip = get_local_ip()

    threading.Thread(target=start_http_server, daemon=True).start()

    print("=" * 52)
    print("  🎿  Ski Balance Board – připraveno!")
    print("=" * 52)
    print(f"  1. Na telefonu otevři Chrome a jdi na:")
    print(f"     http://{ip}:{HTTP_PORT}/phone_gyro.html")
    print(f"  2. Do pole zadej a klikni Připojit:")
    print(f"     ws://{ip}:{WS_PORT}")
    print(f"  3. Polož telefon na desku, kalibruj, hraj!")
    print("=" * 52)

    async with websockets.serve(handler, "0.0.0.0", WS_PORT):
        await asyncio.Future()


asyncio.run(main())
