# Guía de Despliegue Completa - OCSP Stapling Fix

## Prerrequisitos

- Acceso SSH al servidor de producción
- Permisos para ejecutar Docker
- Acceso a ambos repositorios: `gipis-institucional` y `estacion-meteorologica`

## PARTE 1: Desplegar gipis-institucional (Sistema Principal)

### Paso 1: Conectar al servidor y ubicarse en el directorio del proyecto

```bash
# Conectar al servidor (ajustar según tu configuración)
ssh usuario@servidor-gipis

# Ir al directorio del proyecto
cd /ruta/completa/a/gipis-institucional

# Verificar que estás en el lugar correcto
pwd
ls -la
# Deberías ver: docker-compose.yml, app/, certs/, etc.
```

### Paso 2: Verificar estado actual de Git

```bash
# Ver en qué rama estás
git branch

# Ver si hay cambios sin commitear
git status

# Ver el último commit
git log -1 --oneline
```

**Resultado esperado**: Probablemente estés en la rama `main` o `master`.

### Paso 3: Obtener los cambios de la rama con el fix

Tienes dos opciones:

#### Opción A: Merge directo a main (recomendado para producción)

```bash
# Asegurarte de estar en la rama principal
git checkout main  # o master, según tu configuración

# Obtener últimos cambios del remoto
git fetch origin

# Mergear la rama con el fix
git merge origin/claude/fix-cert-revocation-3Zw7v

# Verificar que el merge fue exitoso
git log -3 --oneline
# Deberías ver los commits: 4922e14, 8c6b312, 79be86f
```

#### Opción B: Checkout directo a la rama del fix (para testing)

```bash
# Obtener últimos cambios del remoto
git fetch origin

# Cambiar a la rama del fix
git checkout claude/fix-cert-revocation-3Zw7v

# Actualizar con los últimos cambios
git pull origin claude/fix-cert-revocation-3Zw7v

# Verificar que tienes los commits correctos
git log -3 --oneline
# Deberías ver: 4922e14, 8c6b312, 79be86f
```

### Paso 4: Verificar que los archivos nuevos existen

```bash
# Verificar que los archivos nuevos están presentes
ls -la nginx/nginx.conf
ls -la scripts/verify-ocsp.sh
ls -la OCSP_STAPLING_FIX.md
ls -la WEATHER_SERVER_MIGRATION.md

# Verificar que docker-compose.yml tiene los cambios
grep "web-public" docker-compose.yml
grep "nginx:" docker-compose.yml

# Deberías ver referencias a "web-public" y el servicio "nginx"
```

**Si algún archivo no existe o docker-compose.yml no tiene los cambios, algo salió mal en el paso anterior. DETENTE y revisa.**

### Paso 5: Verificar certificados SSL

```bash
# Los certificados deben existir
ls -la certs/fullchain.pem
ls -la certs/privkey.pem

# Verificar fecha de expiración
openssl x509 -in certs/fullchain.pem -noout -enddate
# Debería mostrar: notAfter=May 26 ... 2026
```

**Si los certificados no existen, necesitas copiarlos antes de continuar.**

### Paso 6: Hacer backup de la configuración actual

```bash
# Backup del docker-compose actual (si existe uno viejo)
docker-compose ps > ~/backup-docker-state-$(date +%Y%m%d-%H%M%S).txt

# Backup de los contenedores corriendo
docker ps > ~/backup-containers-$(date +%Y%m%d-%H%M%S).txt

# Esto te permitirá saber qué estaba corriendo antes
cat ~/backup-docker-state-*.txt
```

### Paso 7: Detener servicios actuales

```bash
# Detener todos los servicios del compose
docker-compose down

# Verificar que se detuvieron
docker-compose ps
# Debería mostrar que no hay servicios corriendo

# Verificar contenedores Docker
docker ps | grep -E "traefik|gipis-web|nginx"
# No debería mostrar nada
```

### Paso 8: Limpiar red antigua (si existe)

```bash
# Verificar qué redes existen
docker network ls | grep -E "traefik|web-public"

# Intentar eliminar la red antigua (puede fallar si no existe, está OK)
docker network rm traefik-public

# Posible salida:
#   - "traefik-public" → éxito, red eliminada
#   - "Error: No such network: traefik-public" → OK, no existía
#   - "Error: network traefik-public has active endpoints" → HAY CONTENEDORES USANDO LA RED
```

**Si aparece el error de "active endpoints"**, significa que hay contenedores corriendo que usan esa red:

```bash
# Encontrar qué contenedores están usando la red
docker network inspect traefik-public | grep -A 10 "Containers"

# Detener esos contenedores
docker stop <nombre-contenedor>

# Intentar eliminar la red nuevamente
docker network rm traefik-public
```

### Paso 9: Levantar servicios con nueva configuración

```bash
# Levantar servicios en background
docker-compose up -d

# Ver logs en tiempo real (Ctrl+C para salir, no detiene los contenedores)
docker-compose logs -f
```

### Paso 10: Verificar que todos los servicios están corriendo

```bash
# Verificar estado de servicios
docker-compose ps

# Deberías ver 3 servicios corriendo:
# nginx-ocsp    (puerto 80/443)
# traefik       (sin puertos externos)
# gipis-web     (sin puertos externos)
```

**Salida esperada**:
```
NAME          IMAGE            STATUS         PORTS
nginx-ocsp    nginx:alpine     Up X seconds   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
traefik       traefik:v2.10    Up X seconds   80/tcp
gipis-web     ...              Up X seconds   5000/tcp
```

**Si algún contenedor no está "Up", revisar logs**:
```bash
docker logs nginx-ocsp
docker logs traefik
docker logs gipis-web
```

### Paso 11: Verificar que la red fue creada correctamente

```bash
# Verificar que la red web-public existe
docker network ls | grep web-public

# Verificar que los 3 contenedores están en la red
docker network inspect web-public | grep -A 5 "Containers"

# Deberías ver: nginx-ocsp, traefik, gipis-web
```

### Paso 12: Verificar conectividad HTTP/HTTPS

```bash
# Probar HTTP (debería redirigir a HTTPS)
curl -I http://gipis.unp.edu.ar

# Deberías ver: HTTP/1.1 301 Moved Permanently
# Location: https://gipis.unp.edu.ar/

# Probar HTTPS
curl -I https://gipis.unp.edu.ar

# Deberías ver: HTTP/2 200
```

### Paso 13: Verificar OCSP Stapling

```bash
# Hacer el script ejecutable (si no lo es)
chmod +x scripts/verify-ocsp.sh

# Ejecutar verificación de OCSP
./scripts/verify-ocsp.sh gipis.unp.edu.ar

# Salida esperada:
# ✅ OCSP Stapling funcionando correctamente
# El certificado está marcado como válido (good).
```

**Si falla**, revisar logs de nginx:
```bash
docker logs nginx-ocsp | grep -i ocsp
docker logs nginx-ocsp | grep -i error
```

### Paso 14: Verificar en navegador

Desde tu computadora local (no desde el servidor), abrir:
- https://gipis.unp.edu.ar

**Verificar**:
- ✅ El sitio carga correctamente
- ✅ No aparece error de certificado
- ✅ No aparece ERR_CERT_REVOKED
- ✅ El candado de seguridad está presente

---

## PARTE 2: Actualizar estacion-meteorologica (Weather Server)

### Paso 1: Ubicarse en el directorio del weather server

```bash
# Desde el servidor (ya conectado)
cd /ruta/completa/a/estacion-meteorologica

# Verificar ubicación
pwd
ls -la
# Deberías ver: docker-compose.yml, src/, data/, etc.
```

### Paso 2: Hacer backup del docker-compose.yml actual

```bash
# Backup del archivo
cp docker-compose.yml docker-compose.yml.backup-$(date +%Y%m%d-%H%M%S)

# Verificar que se creó el backup
ls -la docker-compose.yml.backup-*
```

### Paso 3: Editar docker-compose.yml

```bash
# Abrir con tu editor preferido
nano docker-compose.yml
# O: vi docker-compose.yml
# O: vim docker-compose.yml
```

**Cambios a realizar**:

#### Cambio 1: Buscar la línea del entrypoint (aproximadamente línea 54)

```yaml
# BUSCAR:
      - "traefik.http.routers.weather.entrypoints=websecure"

# CAMBIAR A:
      - "traefik.http.routers.weather.entrypoints=web"
```

#### Cambio 2: Buscar y eliminar la línea de TLS (aproximadamente línea 56)

```yaml
# BUSCAR Y ELIMINAR ESTA LÍNEA COMPLETA:
      - "traefik.http.routers.weather.tls=true"
```

#### Cambio 3: Buscar la sección de redes del servicio (aproximadamente línea 42)

```yaml
# BUSCAR:
    networks:
      - traefik-public

# CAMBIAR A:
    networks:
      - web-public
```

#### Cambio 4: Buscar la sección de redes al final del archivo (aproximadamente línea 100)

```yaml
# BUSCAR:
networks:
  traefik-public:
    external: true

# CAMBIAR A:
networks:
  web-public:
    external: true
```

**Guardar el archivo**:
- En nano: Ctrl+X, luego Y, luego Enter
- En vi/vim: ESC, luego :wq, luego Enter

### Paso 4: Verificar los cambios realizados

```bash
# Verificar que "web-public" aparece en el archivo
grep "web-public" docker-compose.yml

# Deberías ver 2 líneas:
#       - web-public
#   web-public:

# Verificar que "websecure" NO aparece
grep "websecure" docker-compose.yml

# No debería mostrar nada

# Verificar que "tls=true" NO aparece
grep "tls=true" docker-compose.yml

# No debería mostrar nada

# Verificar que "entrypoints=web" aparece
grep "entrypoints=web" docker-compose.yml

# Debería mostrar:
#       - "traefik.http.routers.weather.entrypoints=web"
```

**Si alguna verificación falla, volver al paso 3 y corregir.**

### Paso 5: Verificar que la red web-public existe

```bash
# La red debe existir desde el paso anterior (gipis-institucional)
docker network ls | grep web-public

# Debería mostrar:
# NETWORK ID     NAME         DRIVER    SCOPE
# xxxxx          web-public   bridge    local
```

**Si la red NO existe**, volver a PARTE 1 y verificar que gipis-institucional está corriendo correctamente.

### Paso 6: Detener el contenedor actual

```bash
# Detener el weather server
docker-compose down

# Verificar que se detuvo
docker-compose ps
# No debería mostrar nada

docker ps | grep gipis-weather
# No debería mostrar nada
```

### Paso 7: Levantar con nueva configuración

```bash
# Levantar el servicio
docker-compose up -d

# Ver logs (Ctrl+C para salir)
docker-compose logs -f
```

### Paso 8: Verificar que el contenedor está corriendo

```bash
# Verificar estado
docker-compose ps

# Deberías ver:
# NAME            IMAGE    STATUS         PORTS
# gipis-weather   ...      Up X seconds   3000/tcp
```

### Paso 9: Verificar que está en la red correcta

```bash
# Verificar que gipis-weather está en web-public
docker network inspect web-public | grep gipis-weather

# Debería mostrar:
# "Name": "gipis-weather",
```

### Paso 10: Probar conectividad del weather server

```bash
# Desde el servidor
curl -I http://localhost:3000/health

# Debería mostrar: HTTP/1.1 200 OK

# Probar desde internet (HTTPS)
curl -I https://gipis.unp.edu.ar/weather/

# Debería mostrar: HTTP/2 200
```

### Paso 11: Verificar en navegador

Desde tu computadora local, abrir:
- https://gipis.unp.edu.ar/weather/

**Verificar**:
- ✅ El sitio carga correctamente
- ✅ No aparece error de certificado
- ✅ La API responde correctamente

---

## PARTE 3: Verificación Final

### Paso 1: Verificar todos los contenedores están corriendo

```bash
# Ver todos los contenedores de ambos proyectos
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Deberías ver:
# nginx-ocsp     Up X minutes   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
# traefik        Up X minutes   80/tcp
# gipis-web      Up X minutes   5000/tcp
# gipis-weather  Up X minutes   3000/tcp
```

### Paso 2: Verificar red web-public

```bash
# Inspeccionar la red
docker network inspect web-public --format '{{range .Containers}}{{.Name}} {{end}}'

# Deberías ver los 4 contenedores:
# nginx-ocsp traefik gipis-web gipis-weather
```

### Paso 3: Verificar logs sin errores

```bash
# Logs de nginx (últimas 20 líneas)
docker logs --tail 20 nginx-ocsp

# Logs de Traefik (últimas 20 líneas)
docker logs --tail 20 traefik

# Buscar errores en ambos
docker logs nginx-ocsp 2>&1 | grep -i error
docker logs traefik 2>&1 | grep -i error

# Idealmente no deberían mostrar errores críticos
```

### Paso 4: Pruebas funcionales completas

```bash
# 1. Probar sitio principal
curl -I https://gipis.unp.edu.ar
# Esperar: HTTP/2 200

# 2. Probar weather server
curl -I https://gipis.unp.edu.ar/weather/
# Esperar: HTTP/2 200

# 3. Verificar OCSP stapling
./gipis-institucional/scripts/verify-ocsp.sh gipis.unp.edu.ar
# Esperar: ✅ OCSP Stapling funcionando correctamente
```

### Paso 5: Monitorear logs en tiempo real (opcional)

```bash
# Ver logs de todos los servicios en tiempo real
cd /ruta/a/gipis-institucional
docker-compose logs -f

# En otra terminal
cd /ruta/a/estacion-meteorologica
docker-compose logs -f

# Presionar Ctrl+C para salir (no detiene contenedores)
```

---

## Troubleshooting

### Problema: "network web-public not found" en weather server

**Causa**: El sistema principal no está corriendo o no creó la red.

**Solución**:
```bash
cd /ruta/a/gipis-institucional
docker-compose ps
# Si no están corriendo, ejecutar:
docker-compose up -d
# Luego verificar:
docker network ls | grep web-public
```

### Problema: nginx no inicia - "cannot find certificate"

**Causa**: Los certificados no existen en `certs/`.

**Solución**:
```bash
# Verificar certificados
ls -la certs/fullchain.pem certs/privkey.pem

# Si no existen, copiarlos
# cp /ruta/a/certificados/fullchain.pem certs/
# cp /ruta/a/certificados/privkey.pem certs/
```

### Problema: ERR_CERT_REVOKED sigue apareciendo

**Causa**: OCSP stapling no está funcionando o hay caché en el navegador.

**Solución**:
```bash
# 1. Verificar OCSP stapling
./scripts/verify-ocsp.sh gipis.unp.edu.ar

# 2. Revisar logs de nginx
docker logs nginx-ocsp | grep -i ocsp

# 3. Limpiar caché del navegador (Ctrl+Shift+Del)
# 4. Probar en modo incógnito o desde otro dispositivo
```

### Problema: "Port is already allocated" al levantar nginx

**Causa**: Otro proceso usa el puerto 80 o 443.

**Solución**:
```bash
# Ver qué usa el puerto 80
sudo netstat -tlnp | grep :80

# Ver qué usa el puerto 443
sudo netstat -tlnp | grep :443

# Detener el servicio que lo usa, o matar el proceso
sudo kill <PID>
```

### Problema: Weather server no responde en /weather/

**Causa**: Traefik no está ruteando correctamente.

**Solución**:
```bash
# Verificar logs de Traefik
docker logs traefik | grep weather

# Verificar que el contenedor está en la red correcta
docker network inspect web-public | grep gipis-weather

# Verificar que las labels son correctas
docker inspect gipis-weather | grep -A 20 Labels
```

---

## Rollback (si algo sale mal)

Si necesitas volver atrás:

### Rollback gipis-institucional

```bash
cd /ruta/a/gipis-institucional

# Detener servicios actuales
docker-compose down

# Volver a la rama anterior
git checkout main  # o la rama que usabas antes

# Recrear red antigua
docker network create traefik-public

# Levantar servicios con configuración anterior
docker-compose up -d
```

### Rollback estacion-meteorologica

```bash
cd /ruta/a/estacion-meteorologica

# Detener servicio
docker-compose down

# Restaurar backup
cp docker-compose.yml.backup-XXXXXX docker-compose.yml

# Levantar con configuración anterior
docker-compose up -d
```

---

## Resumen de Archivos y Cambios

### Archivos nuevos creados:
- `nginx/nginx.conf` - Configuración nginx con OCSP stapling
- `nginx/nginx.conf.no-verify` - Configuración alternativa sin verificación
- `scripts/verify-ocsp.sh` - Script de verificación OCSP
- `OCSP_STAPLING_FIX.md` - Documentación técnica del fix
- `WEATHER_SERVER_MIGRATION.md` - Guía de migración weather server
- `DEPLOYMENT_GUIDE.md` - Esta guía

### Archivos modificados:
- `docker-compose.yml` - Agregado nginx, modificado Traefik, cambiada red
- `certs/README.md` - Agregada información sobre OCSP stapling

### Commits relevantes:
- `79be86f` - fix: Implement OCSP stapling with nginx
- `8c6b312` - refactor: Rename network from traefik-public to web-public
- `4922e14` - docs: Add migration guide for weather server

---

## Contacto y Soporte

Si tienes problemas durante el despliegue:
1. Revisar logs: `docker logs <contenedor>`
2. Consultar esta guía en la sección Troubleshooting
3. Revisar OCSP_STAPLING_FIX.md para detalles técnicos
