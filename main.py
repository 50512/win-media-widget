import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Annotated

import pyautogui
import uvicorn
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import HTMLResponse

SECRET_TOKEN = os.getenv("MEDIA_API_TOKEN")
IP_API = os.getenv("SELF_API_IP", "0.0.0.0")

ERROR_RESPONSES = {
    401: {"description": "Token inválido o ausente"},
    404: {"description": "Acción multimedia no reconocida"},
}

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "panel.html", "r", encoding="utf-8") as f:
    TEMPLATE_HTML = f.read()

app = FastAPI()


def set_logger():
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    log_file = "server.log"

    log_file_handler = RotatingFileHandler(
        log_file, maxBytes=2 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    log_file_handler.setFormatter(log_formatter)

    logger = logging.getLogger("media_api")
    logger.setLevel(logging.INFO)
    logger.addHandler(log_file_handler)

    class LoggerWriter:
        def __init__(self, level):
            self.level = level

        def write(self, message: str):
            if message.strip():
                self.level(message.strip())

        def flush(self):
            # for avoid non exist function
            pass

    sys.stdout = LoggerWriter(logger.info)
    sys.stderr = LoggerWriter(logger.error)


def verify_token(token: str):
    if token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_RESPONSES[401]
        )


@app.get("/panel", response_class=HTMLResponse)
async def control_panel():
    return TEMPLATE_HTML.replace("__TOKEN_HERE__", SECRET_TOKEN)


@app.get("/health")
async def health():
    return {"status": "OK"}


@app.get("/media/{action}", responses=ERROR_RESPONSES)
async def control_media(action: str, x_token: Annotated[str | None, Header()]):
    verify_token(x_token)

    # Mapeo de la URL a las teclas virtuales del sistema operativo
    actions = {
        "play": "playpause",
        "pause": "playpause",
        "vol-up": "volumeup",
        "vol-down": "volumedown",
        "mute": "volumemute",
        "next": "nexttrack",
        "prev": "prevtrack",
    }

    if action in actions:
        pyautogui.press(actions[action])
        return {"status": "success", "action": action}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_RESPONSES[404]
    )


if __name__ == "__main__":
    if not SECRET_TOKEN:
        raise EnvironmentError("Token no existente")

    if sys.executable.endswith("pythonw.exe"):
        set_logger()

    uvicorn.run(app, host=IP_API, port=25012)
