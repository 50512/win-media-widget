# Media API para Windows

## Variables de entorno

Este proyecto depende de la variable de entorno `MEDIA_API_TOKEN` que se usará para restringir el acceso a clientes autorizados por este token.

Recomendamos generarlos por uno de estos métodos:

1. Python Secrets

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. OpenSSL

```bash
openssl rand -base64 32
```

Sea cual sea el método usado, debes crear la variable de entorno de usuario `MEDIA_API_TOKEN` para que el código funcione.

Otra variable a usar (pero opcional) es `SELF_API_IP`, para solo aceptar conexiones a través de la interfaz especifica, de no encontrarse, se usara la interfaz `0.0.0.0`.

## Media panel

Una de las características principales es la presencia de un panel web, que sirve para visualizar el estado de la reproducción y controlarlo.

El panel posee 3 estados:

### Sin sesión multimedia

![Panel sin sesión multimedia](./assets/panel-without-session.png)

Este estado aparece cuando no hay ninguna sesión multimedia reconocida por Windows. Se muestra una caratula por defecto (la misma se usa si no hay caratula disponible en la reproducción) y un mensaje de que no todavía no hay sesión. En este estado el botón `play-pause` tiene un logo combinado por la falta de estado.

### Reproduciendo

![Panel reproduciendo música](./assets/panel-playing.png)

Lo mas llamativo de este estado es el poder ver la caratula de la canción o media en reproducción, con un efecto de _Ambilight_, formado por el uso de 4 `box-shadow` que promedian la información de color de un "anillo interno" dividido en cuartos. Gracias a eso se genera ese curioso efecto al rededor de la caratula.

En este estado, el botón `play-pause` tiene el logo de "pausa", representando la acción que va a realizar al presionarse.

### En pausa

![Panel en pausa](./assets/panel-no-playing.png)

Al estar en pausa, se deshabilita el efecto de luz de la caratula, y se cambia el logo del botón `play-pause`.

#### Punto importante

Los botones del panel están mapeados a los end points de [acciones multimedia](#mediaaction), y **siempre están activos**, sin importar el estado.

## EndPoints

Este servicio se encarga de mapear ciertos EndPoints hacia teclas de Windows en la maquina que ejecuta el servidor.

### `/health`

EndPoint de `health` para poder verificar el estado del servicio.

### `/panel`

Donde se expone el [panel HTML](#media-panel).

### `/media/info`

Obtiene la información de la sesión multimedia en curso (de existir).

Hay 2 respuesta posibles:

1. Sin sesión:

```json
{
  "status": "inactive"
}
```

2. Con sesión:

```json
{
   "status": "active",
   "is_playing": is_playing,     // Booleano del estado de reproducción
   "title": media_props.title,   // Titulo de la canción
   "artist": media_props.artist, // Artista de la canción
}
```

### `/media/thumbnail`

Debido a la forma en que Windows almacena las caratulas, es necesario un end point dedicado a la caratula.

Este end point devuelve la imagen almacenada en memoria correspondiente a la caratula.

### `/media/{action}`

| EndPoint   | Tecla virtual |
| ---------- | ------------- |
| `play`     | `playpause`   |
| `pause`    | `playpause`   |
| `vol-up`   | `volumeup`    |
| `vol-down` | `volumedown`  |
| `mute`     | `volumemute`  |
| `next`     | `nexttrack`   |
| `prev`     | `prevtrack`   |

## Levantar como servicio

Para que este servidor se ejecute cada vez que se inicia sesión, recomendamos seguir esta guía.

Recomendamos que el contenido de este repositorio este en `C:\Scripts\MediaAPI\` ya que los comandos incluidos aca están destinados a dicho scope.

### Preparación del entorno

Por comodidad y aislamiento del servicio, usaremos un entorno virtual de `Python 3.14.0`.

```bash
python -m venv .venv
```

Y luego instalamos las dependencias en dicho `.venv`:

- Para `bash` en Windows:

```bash
source /c/Scripts/MediaAPI/.venv/Scripts/activate
pip install -r requirements.txt
```

- Para `CMD`:

```bat
C:\Scripts\MediaAPI\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

- Para `PowerShell`:

```powershell
C:\Scripts\MediaAPI\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Crear tarea

Ahora se debe crear la tarea a ejecutarse en el inicio de sesión.

Primero ejecutar `taskschd.msc` (usando `Win` + `R` o el buscador al presionar `Win`). Una vez abierto, seleccionamos en `Acción` y en `Crear tarea...`, para seguir estas instrucciones:

1. `General`: Poner un nombre y seleccionar `Ejecutar solo cuando el usuario haya iniciado sesión`.
2. `Desencadenadores`: Darle en `Nuevo...`
   - `Iniciar la tarea`: `Al iniciar la sesión`.
   - Seleccionar `Cualquier usuario` (recomendado).
   - `Configuración avanzada`: Desmarcar todo excepto la casilla `Habilitado`.
3. `Acciones`: Darle en `Nueva...`
   - `Acción`: `Iniciar un programa`.
   - `Programa o script`: `C:\Scripts\MediaAPI\.venv\Scripts\pythonw.exe` (para inicio sin ventanas que molesten).
   - `Agregar argumentos`: `"C:\Scripts\MediaAPI\main.py"` (con todo comillas).
   - `Iniciar en`: `C:\Scripts\MediaAPI`.
4. `Condiciones`:
   - `Inactivo`: Desmarcar todo.
   - `Energía`: Desmarcar todo.
   - `Red`: Desmarcar todo.
5. `Configuración`:
   - Desmarcar `Detener la tarea si se ejecuta durante más de:`.
   - En el menú desplegable seleccionar: `Detener la instancia existente`.

### Primer despliegue

Por ultimo, para ejecutar la tarea sin reiniciar, seleccionar `Biblioteca del Programador de tareas`, buscar la tarea que acabas de crear, seleccionarla y darle en `Ejecutar`.

Para probar el funcionamiento puedes acceder al endPoint del panel con la IP de tu computadora (o la que hayas apuntado en la variable `SELF_API_IP`) en el puerto `25012`
