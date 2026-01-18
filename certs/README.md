# Certificados SSL
# ================
# Esta carpeta contiene los certificados SSL para HTTPS.
#
# IMPORTANTE: Los archivos .pem y .key NO deben subirse al repositorio.
#
# Para configurar SSL en producción:
# 1. Crear esta carpeta en el servidor: mkdir certs
# 2. Copiar los certificados de la universidad:
#    - fullchain.pem (certificado + cadena)
#    - privkey.pem (clave privada)
#    - traefik-tls.yml (ya incluido en el repo)
#
# Los certificados actuales vencen el 26 Mayo 2026.
#
# OCSP Stapling:
# ==============
# El sistema ahora usa nginx con OCSP stapling para prevenir errores
# de certificado revocado (ERR_CERT_REVOKED) al acceder desde internet.
#
# Ver OCSP_STAPLING_FIX.md en la raíz del proyecto para más detalles.
#
# Para verificar que OCSP stapling funciona correctamente:
#   ./scripts/verify-ocsp.sh gipis.unp.edu.ar
