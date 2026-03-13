import argparse
import os
import sys
import time
from pathlib import Path

import webview
from dotenv import load_dotenv

# Por compatibilidad con .env (recomendamos que el MEDIA_API_TOKEN este en las variables de entorno del sistema)
if getattr(sys, "frozen", False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent

load_dotenv(dotenv_path=base_path / ".env")
DEBUG_MODE = os.getenv("DEBUG")
SECRET_TOKEN = os.getenv("MEDIA_API_TOKEN")
BIND_IP = os.getenv("SELF_API_IP")


def get_host_by_bind():
    if not BIND_IP or BIND_IP == "0.0.0.0":
        return "localhost"
    else:
        return BIND_IP


def inject_token(window):
    time.sleep(1)
    if SECRET_TOKEN:
        js_code = f"localStorage.setItem('MEDIA_API_TOKEN', '{SECRET_TOKEN}')"
        window.evaluate_js(js_code)


def start_view(
    url: str,
    resizable: bool = True,
    always_on_top: bool = True,
    frameless: bool = False,
    width: int = 470,
    height: int = 470,
):
    window = webview.create_window(
        title="WinMediaWidget",
        url=url,
        width=width,
        height=height,
        resizable=resizable,  # Si deseas lo cambias a False para evitar cambiar el tamaño
        on_top=always_on_top,
        frameless=frameless,  # Puedes usar frameless, pero no lo recomiendo mucho
        background_color="#121212",
        transparent=False,
    )

    webview.start(inject_token, window)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Win Media Widget Client",
        description="Open a WebView of the Win Media Widget panel (WebSocket version as default)",
    )

    parser.add_argument(
        "--resizable", action="store_true", help="Made the WebView resizable"
    )
    parser.add_argument(
        "--on-top",
        "--always-on-top",
        action="store_true",
        help="Set the WebView to 'Always on Top' mode",
    )
    parser.add_argument(
        "--frameless", action="store_true", help="Made the WebView 'frameless'"
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Width (in pixels) of the WebView window. 300 as default",
        default=300,
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Height (in pixels) of the WebView window. 500 as default",
        default=500,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_host = subparsers.add_parser("set-host", help="To use host and port")
    parser_host.add_argument(
        "--host",
        type=str,
        help="Host to connect. Get SELF_API_IP or 'localhost' as default",
        default=get_host_by_bind(),
    )
    parser_host.add_argument(
        "--port",
        type=int,
        help="Port where the server is exposed. 25012 as default",
        default=25012,
    )

    parser_url = subparsers.add_parser("set-url", help="To use url")
    parser_url.add_argument(
        "--url", type=str, required=True, help="URL to connect the WebView"
    )

    args = parser.parse_args()

    if args.command == "set-host":
        url = f"http://{args.host}:{args.port}/ws/panel"
    elif args.command == "set-url":
        url = args.url
    else:
        url = f"http://{get_host_by_bind()}:25012/ws/panel"

    if DEBUG_MODE:
        print(args)
        print(url)

    start_view(
        url,
        resizable=args.resizable,
        always_on_top=args.on_top,
        frameless=args.frameless,
        width=args.width,
        height=args.height,
    )
