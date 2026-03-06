from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import HTMLResponse
from typing import Annotated
from pathlib import Path
import pyautogui
import uvicorn
import sys
import os

SECRET_TOKEN = os.getenv("MEDIA_API_TOKEN")
IP_API = os.getenv("SELF_API_IP", "0.0.0.0")
LOG_PATH = r"C:\Scripts\MediaAPI\server.log"

ERROR_RESPONSES = {
    401: {"description": "Token inválido o ausente"},
    404: {"description": "Acción multimedia no reconocida"}
}

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "panel.html", "r", encoding="utf-8") as f:
    TEMPLATE_HTML = f.read()

app = FastAPI()


def verify_token(token: str):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_RESPONSES[401])


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
        "prev": "prevtrack"
    }

    if action in actions:
        pyautogui.press(actions[action])
        return {"status": "success", "action": action}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_RESPONSES[404])


if __name__ == "__main__":
    sys.stdout = open(LOG_PATH, 'a', encoding='utf-8')
    sys.stderr = open(LOG_PATH, 'a', encoding='utf-8')
    
    if not SECRET_TOKEN:
        raise EnvironmentError("Token no existente")
    uvicorn.run(app, host=IP_API, port=25012)