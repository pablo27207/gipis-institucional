# Reporte Técnico: Certificado SSL Revocado en nginx-pm.unp.edu.ar

**Fecha**: 18 de enero 2026
**Reportado por**: Equipo GIPIS
**Prioridad**: ALTA - Sitio inaccesible desde internet

---

## Resumen Ejecutivo

El dominio `gipis.unp.edu.ar` muestra error **ERR_CERT_REVOKED** al accederse desde internet, pero funciona correctamente en la red local. El problema está en el **proxy nginx-pm.unp.edu.ar** que usa un certificado SSL revocado.

---

## Diagnóstico Técnico

### 1. Arquitectura Actual

```
Internet → nginx-pm.unp.edu.ar (170.210.88.211) → Servidor GIPIS (10.15.24.26)
                     ↑
              CERTIFICADO REVOCADO
```

### 2. Detalles del Proxy (nginx-pm.unp.edu.ar)

**IP**: `170.210.88.211`
**Función**: Proxy reverso para dominios *.unp.edu.ar
**DNS**: `gipis.unp.edu.ar` es CNAME que apunta a `nginx-pm.unp.edu.ar`

### 3. Certificado Actual (REVOCADO)

```
Subject: *.unp.edu.ar
Issuer: Sectigo RSA Domain Validation Secure Server CA
Serial: 4444f53ab8dd86d964a8b216dd6ef9b5
Válido desde: 29 de abril 2025
Válido hasta: 26 de mayo 2026
Estado: REVOCADO ❌
Fingerprint SHA256: 42726bd9f308446662231854a44d10597b26c40f54136cb06c7b3dc66b07a1f2
```

**Verificado con**:
- SSL Labs: https://www.ssllabs.com/ssltest/analyze.html?d=gipis.unp.edu.ar
- OCSP Sectigo: Estado = Revoked
- Fecha de verificación: 18 enero 2026

### 4. Certificado Nuevo (VÁLIDO)

El servidor backend (10.15.24.26) ya tiene el certificado actualizado:

```
Subject: *.unp.edu.ar
Issuer: Sectigo RSA Domain Validation Secure Server CA
Serial: BDB9A9AF52A5A3532DED2E48A2C8687A
Válido desde: 3 de noviembre 2025
Válido hasta: 26 de mayo 2026
Estado: VÁLIDO ✅
Fingerprint SHA256: fde763868113cccf5104613

4e441df65b6c67be4
```

---

## Impacto

### Afectados
- ❌ **Usuarios externos** (internet): Error ERR_CERT_REVOKED
- ✅ **Usuarios internos** (red UNP): Funcionan correctamente

### Navegadores Afectados
- Chrome/Edge: Bloquea completamente (ERR_CERT_REVOKED)
- Firefox: Bloquea completamente
- Safari: Bloquea completamente
- Todos los navegadores modernos rechazan el certificado revocado

---

## Solución Requerida

### Opción 1: Actualizar Certificado en nginx-pm (RECOMENDADO)

Actualizar el certificado SSL en `nginx-pm.unp.edu.ar` con el nuevo certificado:

**Archivos necesarios**:
- `fullchain.pem` (certificado + cadena completa)
- `privkey.pem` (clave privada)

**Ubicación en servidor backend** (para copiarlos):
```bash
Servidor: 10.15.24.26
Usuario: gipis
Ruta: ~/gipis-institucional/certs/
Archivos: fullchain.pem, privkey.pem
```

**Pasos**:
1. Conectar a nginx-pm.unp.edu.ar (170.210.88.211)
2. Copiar los nuevos certificados desde el servidor backend
3. Actualizar configuración de Nginx Proxy Manager para `gipis.unp.edu.ar`
4. Verificar con: `openssl s_client -connect gipis.unp.edu.ar:443 -servername gipis.unp.edu.ar`

### Opción 2: Actualizar DNS (Alternativa)

Cambiar el DNS para que `gipis.unp.edu.ar` apunte directamente al servidor backend:

```
Actual:  gipis.unp.edu.ar → CNAME → nginx-pm.unp.edu.ar (170.210.88.211)
Nuevo:   gipis.unp.edu.ar → A → 10.15.24.26
```

⚠️ **Nota**: Esto requeriría que el servidor 10.15.24.26 sea accesible desde internet (configurar firewall/NAT).

---

## Verificación Post-Actualización

### 1. Verificar certificado desde internet

```bash
echo | openssl s_client -connect gipis.unp.edu.ar:443 -servername gipis.unp.edu.ar 2>/dev/null | openssl x509 -noout -dates -serial

# Salida esperada:
# notBefore=Nov  3 00:00:00 2025 GMT
# notAfter=May 26 23:59:59 2026 GMT
# serial=BDB9A9AF52A5A3532DED2E48A2C8687A
```

### 2. SSL Labs

Ejecutar: https://www.ssllabs.com/ssltest/analyze.html?d=gipis.unp.edu.ar

**Resultado esperado**:
- Revocation status: **Valid** (no "Revoked")
- Certificate válido desde noviembre 2025

### 3. Navegador

Acceder a `https://gipis.unp.edu.ar` desde internet (fuera de la red UNP):
- ✅ Sin errores de certificado
- ✅ Candado verde/seguro visible

---

## Información de Contacto

**Equipo GIPIS**
Servidor: 10.15.24.26
Usuario: gipis

**Documentación técnica completa**:
Repositorio: gipis-institucional
Branch: claude/fix-cert-revocation-3Zw7v
Archivos relevantes:
- `OCSP_STAPLING_FIX.md` - Solución OCSP stapling implementada
- `scripts/check-cert-status.sh` - Script diagnóstico
- `scripts/verify-ocsp.sh` - Verificación OCSP

---

## Evidencia Técnica

### SSL Labs Report (18 enero 2026)

```
Certificate #1: RSA 2048 bits (SHA256withRSA)
Subject: *.unp.edu.ar
Valid from: Tue, 29 Apr 2025 00:00:00 UTC
Valid until: Tue, 26 May 2026 23:59:59 UTC
Revocation status: Revoked INSECURE ❌
```

### nslookup desde Cliente Externo

```
C:\>nslookup gipis.unp.edu.ar
Nombre:  nginx-pm.unp.edu.ar
Address:  170.210.88.211
Aliases:  gipis.unp.edu.ar
```

### Verificación OCSP Directa (Sectigo)

```bash
# Consulta al servidor OCSP de Sectigo para el certificado viejo
Cert Status: revoked
Revocation Time: [Fecha de revocación]
```

---

## Urgencia

**ALTA** - El sitio está completamente inaccesible desde internet para todos los usuarios externos. Los navegadores modernos bloquean el acceso debido al certificado revocado.

---

## Próximos Pasos Recomendados

1. ✅ Confirmar recepción de este reporte
2. ⏳ Actualizar certificado en nginx-pm.unp.edu.ar (Opción 1)
3. ⏳ Verificar funcionamiento con SSL Labs
4. ⏳ Notificar al equipo GIPIS cuando esté resuelto

---

**Fin del Reporte**
