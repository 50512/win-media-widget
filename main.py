from fastapi import FastAPI, Header, HTTPException, status
from typing import Annotated
import pyautogui
import uvicorn
import os

app = FastAPI()

SECRET_TOKEN = os.getenv("MEDIA_API_TOKEN")
IP_API = os.getenv("SELF_TAILSCALE_IP", "0.0.0.0")

ERROR_RESPONSES = {
    401: {"description": "Token inválido o ausente"},
    404: {"description": "Acción multimedia no reconocida"}
}

def verify_token(token: str):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ERROR_RESPONSES[401])

@app.get("/media/{action}", responses=ERROR_RESPONSES)
async def control_media(action: str, x_token: Annotated[str | None, Header()]):
    verify_token(x_token)

    # Mapeo de la URL a las teclas virtuales del sistema operativo
    actions = {
        "play": "playpause",
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
    if not SECRET_TOKEN:
        raise EnvironmentError("Token no existente")
    uvicorn.run(app, host=IP_API, port=8000)