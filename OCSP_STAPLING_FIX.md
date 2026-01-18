# Solución al Error ERR_CERT_REVOKED

## Problema Identificado

El sistema experimentaba el error `ERR_CERT_REVOKED` cuando se accedía desde fuera de la red local, específicamente:
- **En red local**: Los certificados funcionaban correctamente
- **Desde internet**: Después de algunos usos, el navegador mostraba error de certificado revocado

### Causa Raíz

El error se debía a la falta de **OCSP Stapling** en la configuración SSL/TLS:

1. **Traefik v2.10** no soporta OCSP stapling nativamente
2. Los navegadores intentaban verificar el estado del certificado contactando directamente el servidor OCSP de la CA
3. Problemas de conectividad, timeouts o respuestas incorrectas del servidor OCSP causaban que el navegador interpretara el certificado como revocado

## Solución Implementada

Se ha implementado **nginx** como capa frontend con soporte completo para OCSP stapling.

### Nueva Arquitectura

```
Internet → nginx (OCSP stapling) → Traefik (routing) → Flask App
         [Puerto 80/443]         [Puerto 80 interno]   [Puerto 5000]
```

### Componentes Agregados

1. **nginx/nginx.conf**: Configuración de nginx con:
   - OCSP stapling habilitado (`ssl_stapling on`)
   - Verificación de respuestas OCSP (`ssl_stapling_verify on`)
   - Resolvers DNS configurados
   - Timeouts apropiados para OCSP
   - Headers de seguridad (HSTS, X-Frame-Options, etc.)
   - Proxy hacia Traefik para el routing

2. **docker-compose.yml actualizado**:
   - Nuevo servicio `nginx` que maneja SSL/TLS y OCSP stapling
   - Traefik modificado para solo manejar routing HTTP interno
   - Puertos 80/443 ahora expuestos por nginx (no Traefik)

## ¿Qué es OCSP Stapling?

**OCSP (Online Certificate Status Protocol)** es un protocolo para verificar si un certificado SSL/TLS ha sido revocado.

**Sin OCSP Stapling** (problema anterior):
```
Cliente → Servidor Web
Cliente → Servidor OCSP de CA (verificación adicional)
```
- El cliente debe contactar el servidor OCSP directamente
- Puede fallar por timeouts, conectividad o sobrecarga del servidor OCSP
- Reduce privacidad (la CA sabe qué sitios visitas)
- Ralentiza la conexión

**Con OCSP Stapling** (solución implementada):
```
Servidor Web → Servidor OCSP de CA (cada ~5 minutos)
Cliente → Servidor Web (incluye respuesta OCSP "grapada")
```
- El servidor obtiene la respuesta OCSP y la "grapa" (staple) al handshake TLS
- El cliente no necesita contactar el servidor OCSP
- Conexiones más rápidas y confiables
- Mayor privacidad

## Cómo Verificar que Funciona

### 1. Verificar OCSP Stapling con OpenSSL

Desde cualquier computadora con openssl instalado:

```bash
echo QUIT | openssl s_client -connect gipis.unp.edu.ar:443 -status -servername gipis.unp.edu.ar 2>/dev/null | grep -A 20 "OCSP Response Status"
```

**Salida esperada** (éxito):
```
OCSP Response Status: successful (0x0)
OCSP Response Data:
    OCSP Response Status: successful (0x0)
    Cert Status: good
    ...
```

Si ves `Cert Status: good`, OCSP stapling está funcionando correctamente.

### 2. Verificar en Navegadores

**Chrome/Chromium**:
1. Ir a `chrome://net-internals/#security`
2. Buscar el dominio `gipis.unp.edu.ar`
3. Verificar que muestre información de OCSP stapling

**Firefox**:
1. Hacer clic en el candado en la barra de direcciones
2. Más información → Ver certificado
3. En la sección "Varios", verificar que muestre información OCSP

### 3. Verificar Logs de nginx

```bash
docker logs nginx-ocsp 2>&1 | grep -i ocsp
```

### 4. Herramientas Online

- **SSL Labs**: https://www.ssllabs.com/ssltest/analyze.html?d=gipis.unp.edu.ar
  - Buscar "OCSP stapling: Yes" en el reporte

## Despliegue

### 1. Detener servicios actuales

```bash
docker-compose down
```

### 2. Iniciar con nueva configuración

```bash
docker-compose up -d
```

### 3. Verificar que todos los servicios estén corriendo

```bash
docker-compose ps
```

Deberías ver:
- `nginx-ocsp` (corriendo)
- `traefik` (corriendo)
- `gipis-web` (corriendo)

### 4. Verificar logs

```bash
# Ver logs de nginx
docker logs nginx-ocsp

# Ver logs de Traefik
docker logs traefik

# Ver todos los logs
docker-compose logs -f
```

## Configuración de DNS y Resolvers

La configuración actual usa los DNS públicos de Google (`8.8.8.8` y `8.8.4.4`) para resolver las consultas OCSP.

Si prefieres usar los DNS de la universidad, edita `nginx/nginx.conf`:

```nginx
resolver <DNS_UNIVERSIDAD_1> <DNS_UNIVERSIDAD_2> valid=300s;
```

## Troubleshooting

### Error: "OCSP stapling verification failed"

Posibles causas:
1. El certificado no tiene información de OCSP en su metadata
2. El servidor OCSP de la CA no está accesible
3. Problemas con el resolver DNS

**Solución temporal**: Deshabilitar verificación (no recomendado en producción):
```nginx
ssl_stapling on;
ssl_stapling_verify off;  # Cambiar a off temporalmente
```

### Error: "nginx: [emerg] host not found in resolver"

El resolver DNS no puede encontrar el servidor OCSP.

**Solución**: Verificar conectividad DNS desde el contenedor:
```bash
docker exec nginx-ocsp nslookup <servidor-ocsp-de-la-ca>
```

### Los certificados siguen dando error

1. Limpiar caché del navegador
2. Verificar que los certificados en `certs/` sean válidos y no estén realmente revocados
3. Contactar con el administrador de certificados de la universidad

## Información Técnica Adicional

### Timeouts Configurados

- **OCSP Response Timeout**: 5 segundos
- **Resolver Timeout**: 5 segundos
- **OCSP Cache Validity**: 300 segundos (5 minutos)
- **SSL Session Cache**: 10 minutos

### Headers de Seguridad Implementados

- `Strict-Transport-Security`: Fuerza HTTPS durante 1 año
- `X-Frame-Options`: Previene clickjacking
- `X-Content-Type-Options`: Previene MIME sniffing
- `X-XSS-Protection`: Protección contra XSS

### Soporte WebSocket

La configuración incluye soporte completo para WebSockets:
- `Upgrade` header
- `Connection` header
- HTTP/1.1 para proxy

## Alternativas Consideradas

### 1. Actualizar a Traefik v3.x
**Ventajas**: Traefik v3 tiene mejor soporte OCSP
**Desventajas**: Requiere cambios significativos en configuración, posible breaking changes

### 2. Solicitar certificado sin OCSP Must-Staple
**Ventajas**: Más simple
**Desventajas**: Menos seguro, depende de políticas de la universidad

### 3. Usar nginx directamente (sin Traefik)
**Ventajas**: Más simple, menos overhead
**Desventajas**: Perder capacidades de routing dinámico de Traefik

## Conclusión

La solución implementada con nginx + OCSP stapling es:
- ✅ **Segura**: OCSP stapling habilitado y verificado
- ✅ **Confiable**: No depende de conectividad del cliente al servidor OCSP
- ✅ **Rápida**: Respuestas OCSP cacheadas en el servidor
- ✅ **Compatible**: Mantiene toda la funcionalidad existente de Traefik
- ✅ **Privada**: Los clientes no revelan sus visitas a la CA

El error `ERR_CERT_REVOKED` debería estar completamente resuelto.
