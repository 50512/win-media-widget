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

Este servicio se encarga de mapear ciertos EndPoints hacia teclas de Windows en la maquina que ejecuta el servidor. **Todos los EndPoints son precedidos por `media/`**

### Health

Se agrego un EndPoint de `health` para poder verificar el estado del servicio. Es el único EndPoint que no requiere el `X-Header`

### Todos los demás

| EndPoint   | Tecla virtual |
| ---------- | ------------- |
| `play`     | `playpause`   |
| `pause`    | `playpause`   |
| `vol-up`   | `volumeup`    |
| `vol-down` | `volumedown`  |
| `mute`     | `volumemute`  |
| `next`     | `nexttrack`   |
| `prev`     | `prevtrack`   |
