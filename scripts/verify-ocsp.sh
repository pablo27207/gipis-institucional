#!/bin/bash

# ============================================
# Script de Verificación de OCSP Stapling
# ============================================
# Este script verifica que OCSP stapling esté
# funcionando correctamente en el servidor.
# ============================================

DOMAIN="${1:-gipis.unp.edu.ar}"
PORT="${2:-443}"

echo "=================================================="
echo "  Verificación de OCSP Stapling"
echo "=================================================="
echo ""
echo "Dominio: $DOMAIN"
echo "Puerto: $PORT"
echo ""

# Verificar que openssl esté instalado
if ! command -v openssl &> /dev/null; then
    echo "❌ Error: openssl no está instalado"
    echo "   Instalar con: apt-get install openssl (Debian/Ubuntu)"
    echo "               o yum install openssl (CentOS/RHEL)"
    exit 1
fi

echo "🔍 Consultando estado OCSP..."
echo ""

# Realizar la consulta OCSP
OCSP_OUTPUT=$(echo QUIT | openssl s_client -connect "$DOMAIN:$PORT" -status -servername "$DOMAIN" 2>&1)

# Verificar si la conexión fue exitosa
if [ $? -ne 0 ]; then
    echo "❌ Error: No se pudo conectar a $DOMAIN:$PORT"
    echo ""
    echo "Detalles del error:"
    echo "$OCSP_OUTPUT" | grep -i "error\|fail" | head -5
    exit 1
fi

# Buscar información de OCSP en la salida
echo "=================================================="
echo "  Respuesta OCSP:"
echo "=================================================="
echo ""

OCSP_STATUS=$(echo "$OCSP_OUTPUT" | grep -A 20 "OCSP Response Status")

if [ -z "$OCSP_STATUS" ]; then
    echo "❌ OCSP Stapling NO está habilitado"
    echo ""
    echo "El servidor no está enviando respuestas OCSP stapled."
    echo "Esto puede causar el error ERR_CERT_REVOKED en navegadores."
    echo ""
    echo "Sugerencias:"
    echo "1. Verificar que nginx esté corriendo: docker ps | grep nginx"
    echo "2. Verificar logs de nginx: docker logs nginx-ocsp"
    echo "3. Revisar configuración en nginx/nginx.conf"
    exit 1
else
    echo "$OCSP_STATUS"
    echo ""

    # Verificar el estado del certificado
    if echo "$OCSP_STATUS" | grep -q "Cert Status: good"; then
        echo "=================================================="
        echo "✅ OCSP Stapling funcionando correctamente"
        echo "=================================================="
        echo ""
        echo "El certificado está marcado como válido (good)."
        echo "El error ERR_CERT_REVOKED debería estar resuelto."
        exit 0
    elif echo "$OCSP_STATUS" | grep -q "Cert Status: revoked"; then
        echo "=================================================="
        echo "⚠️  ADVERTENCIA: Certificado REVOCADO"
        echo "=================================================="
        echo ""
        echo "El certificado ha sido revocado por la CA."
        echo "Necesitas obtener un nuevo certificado de la universidad."
        exit 1
    else
        echo "=================================================="
        echo "⚠️  Estado OCSP desconocido"
        echo "=================================================="
        echo ""
        echo "No se pudo determinar el estado del certificado."
        echo "Revisa la salida anterior para más detalles."
        exit 1
    fi
fi
