# Cambios Necesarios en estacion-meteorologica

## Resumen

Debido a la migración a nginx con OCSP stapling en el sistema principal, el repositorio `estacion-meteorologica` necesita dos cambios en su `docker-compose.yml`.

## Cambios Requeridos

### 1. Cambiar el entrypoint de HTTPS a HTTP

**Razón**: nginx ahora maneja todo el SSL/TLS. Traefik solo maneja routing HTTP interno.

```yaml
# ANTES (incorrecto):
- "traefik.http.routers.weather.entrypoints=websecure"
- "traefik.http.routers.weather.tls=true"

# DESPUÉS (correcto):
- "traefik.http.routers.weather.entrypoints=web"
# (eliminar la línea tls=true completamente)
```

### 2. Cambiar nombre de la red

**Razón**: La red se renombró de `traefik-public` a `web-public` para reflejar mejor la arquitectura.

```yaml
# ANTES (incorrecto):
networks:
  traefik-public:
    external: true

# DESPUÉS (correcto):
networks:
  web-public:
    external: true
```

**También cambiar en el servicio**:

```yaml
# ANTES (incorrecto):
services:
  weather-server:
    networks:
      - traefik-public

# DESPUÉS (correcto):
services:
  weather-server:
    networks:
      - web-public
```

## Archivo docker-compose.yml Completo Actualizado

```yaml
# ============================================
# GIPIS Weather Station Server
# Docker Compose con integración nginx + Traefik
# ============================================
#
# Este compose se conecta a la red web-public
# existente en tu infraestructura.
#
# Flujo de tráfico:
#   Internet → nginx (OCSP stapling) → Traefik → Weather Server
#
# Acceso: https://gipis.unp.edu.ar/weather/
#
# Uso:
#   docker compose up -d
#   docker compose logs -f
#
# ============================================

version: '3.8'

services:
  # ============================================
  # Weather Station Server - Node.js/Express
  # ============================================
  weather-server:
    build: .
    container_name: gipis-weather
    restart: unless-stopped

    # Volúmenes persistentes
    volumes:
      # Base de datos SQLite
      - weather-data:/app/data

    environment:
      - NODE_ENV=production
      - PORT=3000
      - TZ=America/Argentina/Buenos_Aires
      # Base path para cuando se usa PathPrefix
      - BASE_PATH=${BASE_PATH:-}

    expose:
      - "3000"

    networks:
      - web-public

    # ============================================
    # Labels de Traefik - PATH-BASED ROUTING
    # Acceso via: https://gipis.unp.edu.ar/weather/
    # (nginx maneja HTTPS, Traefik solo routing HTTP interno)
    # ============================================
    labels:
      - "traefik.enable=true"

      # Router: mismo dominio + path /weather
      - "traefik.http.routers.weather.rule=Host(`${MAIN_DOMAIN:-gipis.unp.edu.ar}`) && PathPrefix(`/weather`)"
      - "traefik.http.routers.weather.entrypoints=web"
      - "traefik.http.routers.weather.priority=100"

      # Servicio
      - "traefik.http.services.weather.loadbalancer.server.port=3000"

      # Middleware: Strip prefix /weather antes de enviar al backend
      # /weather/api/stations -> /api/stations
      - "traefik.http.middlewares.weather-stripprefix.stripprefix.prefixes=/weather"

      # Rate limiting
      - "traefik.http.middlewares.weather-ratelimit.ratelimit.average=100"
      - "traefik.http.middlewares.weather-ratelimit.ratelimit.burst=50"

      # Headers de seguridad
      - "traefik.http.middlewares.weather-headers.headers.stsSeconds=31536000"
      - "traefik.http.middlewares.weather-headers.headers.frameDeny=true"
      - "traefik.http.middlewares.weather-headers.headers.contentTypeNosniff=true"

      # Aplicar middlewares (stripprefix es crítico!)
      - "traefik.http.routers.weather.middlewares=weather-stripprefix,weather-ratelimit,weather-headers"

    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

# ============================================
# Volúmenes
# ============================================
volumes:
  weather-data:
    name: gipis-weather-data

# ============================================
# Red externa (del compose principal)
# ============================================
networks:
  web-public:
    external: true
```

## Proceso de Actualización

### 1. Actualizar el repositorio estacion-meteorologica

```bash
cd /ruta/a/estacion-meteorologica
# Editar docker-compose.yml con los cambios anteriores
```

### 2. Detener y eliminar el contenedor actual

```bash
docker-compose down
```

### 3. IMPORTANTE: Actualizar infraestructura principal primero

Antes de levantar el weather server, asegúrate de que el sistema principal (`gipis-institucional`) esté actualizado y corriendo con la nueva red `web-public`:

```bash
cd /ruta/a/gipis-institucional
docker-compose down
docker network rm traefik-public  # Eliminar red antigua si existe
docker-compose up -d
docker-compose ps  # Verificar que todo esté corriendo
```

### 4. Levantar el weather server con nueva configuración

```bash
cd /ruta/a/estacion-meteorologica
docker-compose up -d
```

### 5. Verificar que todo funciona

```bash
# Verificar que el contenedor está corriendo
docker ps | grep gipis-weather

# Verificar logs
docker logs gipis-weather

# Verificar conectividad
curl -I https://gipis.unp.edu.ar/weather/

# Debería devolver HTTP/2 200
```

## Solución de Problemas

### Error: "network web-public not found"

**Causa**: La red no existe porque el sistema principal no está corriendo o no se actualizó.

**Solución**:
```bash
# Ir al repositorio principal y levantar servicios
cd /ruta/a/gipis-institucional
docker-compose up -d

# Verificar que la red existe
docker network ls | grep web-public
```

### Error: No se puede acceder a /weather/

**Verificar**:
1. El contenedor está corriendo: `docker ps | grep gipis-weather`
2. El contenedor está en la red correcta: `docker network inspect web-public`
3. Los logs de Traefik: `docker logs traefik`
4. Los logs del weather server: `docker logs gipis-weather`

### El sitio no responde con HTTPS

**Causa**: El sistema principal (nginx + Traefik) no está corriendo.

**Solución**:
```bash
cd /ruta/a/gipis-institucional
docker-compose ps  # Verificar estado
docker-compose up -d  # Levantar si no está corriendo
```

## Arquitectura Actualizada

```
Internet
   ↓
[nginx:443] ← OCSP Stapling, SSL/TLS
   ↓
[Traefik:80] ← Routing HTTP interno
   ↓
   ├─→ [gipis-web:5000] ← Flask app (/)
   └─→ [gipis-weather:3000] ← Weather API (/weather)
```

**Red**: `web-public` (conecta nginx, Traefik, y todos los servicios)

## Notas Importantes

1. **No cambiar el host**: Sigue siendo `gipis.unp.edu.ar`
2. **No cambiar el path**: Sigue siendo `/weather`
3. **Los middlewares siguen igual**: stripprefix, ratelimit, y headers no cambian
4. **HTTPS es transparente**: nginx lo maneja automáticamente
5. **OCSP stapling**: Resuelve el error ERR_CERT_REVOKED automáticamente

## Referencias

- Ver `OCSP_STAPLING_FIX.md` en el repositorio principal para más detalles sobre la solución OCSP
- La arquitectura detallada está documentada en el repositorio `gipis-institucional`
