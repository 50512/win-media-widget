import webview
import os
import sys
import time
from dotenv import load_dotenv
from pathlib import Path

# Por compatibilidad con .env (recomendamos que el MEDIA_API_TOKEN este en las variables de entorno del sistema)
if getattr(sys, "frozen", False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent
    
load_dotenv(dotenv_path=base_path / ".env")
SECRET_TOKEN = os.getenv("MEDIA_API_TOKEN")
BIND_IP = os.getenv("SELF_API_IP")

def inject_token(window):
    time.sleep(1)
    if SECRET_TOKEN:
        
        js_code = f"localStorage.setItem('MEDIA_API_TOKEN', '{SECRET_TOKEN}')"
        window.evaluate_js(js_code)
        
def start_view():
    if not BIND_IP or BIND_IP == "0.0.0.0":
        host = "localhost"
    else:
        host = BIND_IP
        
    ws_panel_url = f"http://{host}:25012/ws/panel"
    
    window = webview.create_window(
        title="WinMediaWidget",
        url=ws_panel_url,
        width=470,
        height=470,
        resizable=True, # Si deseas lo cambias a False para evitar cambiar el tamaño
        on_top=True,
        frameless=False, # Puedes usar frameless, pero no lo recomiendo mucho
        background_color="#121212",
        transparent=False
    )
    
    webview.start(inject_token, window)
    
        

if __name__ == "__main__":
    start_view()
