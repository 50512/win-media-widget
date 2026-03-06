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

## EndPoints

Este servicio se encarga de mapear ciertos EndPoints hacia teclas de Windows en la maquina que ejecuta el servidor.

### `/health`

EndPoint de `health` para poder verificar el estado del servicio.

### `/panel`

Un simple panel web con los 6 botones de acción, recomendado para usar como `iframe` en otros servicios (Dashy en nuestro caso).

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
