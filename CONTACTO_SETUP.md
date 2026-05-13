# Configuración del Formulario de Contacto — GIPIS

El formulario de contacto en `/contacto` envía emails a **gipis.unp@gmail.com** usando SMTP de Gmail.

## Estado actual

El formulario está **implementado pero necesita configuración SMTP** para enviar emails.
Sin la contraseña configurada, al enviar el formulario se mostrará un mensaje de error
pidiendo que escriban directamente al email.

---

## Pasos para activar el envío de emails

### 1. Generar una App Password de Gmail

> **Requisito**: La cuenta `gipis.unp@gmail.com` debe tener la **Verificación en 2 pasos** activada.

1. Iniciar sesión en [myaccount.google.com](https://myaccount.google.com) con `gipis.unp@gmail.com`
2. Ir a **Seguridad** → **Verificación en 2 pasos** y activarla si no lo está
3. Una vez activa, ir a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
4. En "Nombre de la app", escribir: `GIPIS Web`
5. Hacer click en **Crear**
6. Google va a mostrar una contraseña de 16 caracteres (ejemplo: `abcd efgh ijkl mnop`)
7. **Copiar esa contraseña** (sin espacios): `abcdefghijklmnop`

> ⚠️ **Esta contraseña se muestra una sola vez.** Si la perdés, hay que generar una nueva.

### 2. Configurar en el servidor (Producción)

Editar el archivo `.env` en el servidor y agregar:

```env
MAIL_USERNAME=gipis.unp@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
```

Verificar que en `docker-compose.yml`, el servicio `web` tenga estas variables de entorno:

```yaml
environment:
  - FLASK_ENV=production
  - SECRET_KEY=${SECRET_KEY:-cambia-esta-clave-en-produccion}
  - MAIL_USERNAME=${MAIL_USERNAME:-gipis.unp@gmail.com}
  - MAIL_PASSWORD=${MAIL_PASSWORD:-}
```

Luego reconstruir y levantar:

```bash
docker compose up -d --build web
```

### 3. Probar localmente (Desarrollo)

Para probar en local, ejecutar con la variable de entorno:

```bash
MAIL_PASSWORD="abcdefghijklmnop" docker compose -f docker-compose.local.yml up -d web
```

O crear un archivo `.env` en la raíz del proyecto:

```env
MAIL_PASSWORD=abcdefghijklmnop
```

> ⚠️ **No commitear el `.env` al repositorio.** Ya está en `.gitignore`.

---

## Cómo funciona

1. El visitante completa el formulario con: Nombre, Email, Asunto y Mensaje
2. Se envía un email a `gipis.unp@gmail.com` con el asunto `[GIPIS Web] <asunto>`
3. El email tiene `Reply-To` configurado con el email del visitante, así pueden responder directamente
4. Se envía en formato texto plano y HTML

## Archivos involucrados

| Archivo | Descripción |
|---------|-------------|
| `config.py` | Configuración SMTP (servidor, puerto, TLS) |
| `app/__init__.py` | Inicialización de Flask-Mail |
| `app/routes/main.py` | Ruta `/contacto` con lógica de envío |
| `app/templates/pages/contacto.xhtml` | Template del formulario |
| `docker-compose.yml` | Variables de entorno en producción |
| `docker-compose.local.yml` | Variables de entorno en desarrollo |

## Troubleshooting

### "Hubo un error al enviar el mensaje"

- Verificar que `MAIL_PASSWORD` está configurada correctamente
- Verificar que la App Password de Gmail es válida
- Revisar los logs: `docker logs gipis-web` (producción) o `docker logs gipis-web-local` (local)

### Gmail rechaza la conexión

- Asegurar que la Verificación en 2 pasos está **activa**
- Las contraseñas normales de Gmail **no funcionan** con SMTP; se necesita una App Password
- Si se cambió la contraseña de la cuenta, las App Passwords existentes se invalidan

### Quiero usar otro proveedor de email

Cambiar en `.env` o en `config.py`:

```env
MAIL_SERVER=smtp.tu-proveedor.com
MAIL_PORT=587
MAIL_USERNAME=tu@email.com
MAIL_PASSWORD=tu-password
```
