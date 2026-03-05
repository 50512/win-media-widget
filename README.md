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
