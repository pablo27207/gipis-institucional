# Configuración de Umami Analytics — GIPIS

Umami es una herramienta de analytics self-hosted, liviana y respetuosa de la privacidad (no usa cookies).

## Arquitectura

```
Visitante → Traefik → /umami/* → Umami (puerto 3000)
                    → /*       → Flask (puerto 5000)
```

Umami corre como un servicio Docker adicional con su propia base de datos PostgreSQL.

---

## Primer inicio (Local)

### 1. Levantar los servicios

```bash
docker compose -f docker-compose.local.yml up -d
```

Esto levanta: Traefik + Flask + Umami + PostgreSQL

### 2. Acceder al panel de Umami

Ir a: **http://localhost/umami**

Credenciales por defecto:
- **Usuario**: `admin`
- **Contraseña**: `umami`

> ⚠️ **Cambiar la contraseña inmediatamente** desde Settings → Profile.

### 3. Crear el sitio web en Umami

1. Ir a **Settings** → **Websites** → **Add website**
2. Completar:
   - **Name**: `GIPIS`
   - **Domain**: `localhost` (o `gipis.unp.edu.ar` en producción)
3. Hacer click en **Save**
4. Copiar el **Website ID** que aparece (es un UUID, ej: `a1b2c3d4-e5f6-...`)

### 4. Configurar el Website ID

Agregar el ID al archivo `.env` o pasarlo como variable:

```bash
UMAMI_WEBSITE_ID=a1b2c3d4-e5f6-... docker compose -f docker-compose.local.yml up -d web
```

O en `.env`:
```env
UMAMI_WEBSITE_ID=a1b2c3d4-e5f6-...
```

### 5. Verificar

Recargar cualquier página del sitio y verificar en el panel de Umami que aparecen visitas.

---

## Producción

### 1. Configurar variables en `.env`

```env
UMAMI_WEBSITE_ID=tu-website-id-aqui
UMAMI_SCRIPT_URL=/umami/script.js
UMAMI_DB_PASSWORD=una-contraseña-segura
UMAMI_APP_SECRET=otro-secreto-seguro
```

### 2. Levantar

```bash
docker compose up -d
```

### 3. Configurar en Umami

Acceder a `https://gipis.unp.edu.ar/umami`, crear el sitio con dominio `gipis.unp.edu.ar` y copiar el Website ID al `.env`.

---

## Dashboard

El dashboard de Umami muestra:
- **Visitantes únicos** por día/semana/mes
- **Páginas más visitadas**
- **Fuentes de tráfico** (referrers)
- **Dispositivos y navegadores**
- **Países de origen**
- **Tiempo en el sitio**

Todo sin cookies y cumpliendo GDPR.

## Troubleshooting

### Umami no carga en /umami

- Verificar que los contenedores estén corriendo: `docker ps`
- Verificar logs: `docker logs gipis-umami-local`
- Verificar que Traefik reconoce la ruta: ir a `http://localhost:8080` (dashboard de Traefik)

### No se registran visitas

- Verificar que `UMAMI_WEBSITE_ID` está configurado en el `.env`
- Verificar con inspeccionar elemento que el script de Umami se carga en el HTML
- Verificar en la consola del navegador que no hay errores 404 para `/umami/script.js`
