#!/bin/bash

# ============================================
# Script de Diagnóstico de Estado de Certificado
# ============================================

echo "=================================================="
echo "  Diagnóstico Completo de Certificado SSL"
echo "=================================================="
echo ""

CERT_FILE="certs/fullchain.pem"

# 1. Extraer información básica del certificado
echo "1. Información del Certificado:"
echo "=================================================="
openssl x509 -in "$CERT_FILE" -noout -subject -issuer -dates
echo ""

# 2. Extraer URL del servidor OCSP
echo "2. URL del Servidor OCSP:"
echo "=================================================="
OCSP_URL=$(openssl x509 -in "$CERT_FILE" -noout -ocsp_uri)
echo "OCSP URL: $OCSP_URL"
echo ""

# 3. Extraer el certificado del emisor (CA) de la cadena
echo "3. Extrayendo certificado del emisor..."
echo "=================================================="
# El fullchain.pem contiene: [certificado del servidor] + [certificado intermedio] + [certificado raíz]
# Necesitamos el certificado intermedio para la consulta OCSP

# Contar certificados en la cadena
CERT_COUNT=$(grep -c "BEGIN CERTIFICATE" "$CERT_FILE")
echo "Certificados en la cadena: $CERT_COUNT"

# Extraer certificados individualmente
awk '/-----BEGIN CERTIFICATE-----/{n++}{print > "/tmp/cert-" n ".pem"}' "$CERT_FILE"

# El certificado del servidor es el primero
SERVER_CERT="/tmp/cert-1.pem"
# El certificado del emisor es el segundo
ISSUER_CERT="/tmp/cert-2.pem"

if [ ! -f "$SERVER_CERT" ] || [ ! -f "$ISSUER_CERT" ]; then
    echo "❌ Error: No se pudo extraer los certificados"
    rm -f /tmp/cert-*
    exit 1
fi

echo "✅ Certificados extraídos"

# Mostrar información del servidor y emisor
echo ""
echo "Certificado del servidor:"
openssl x509 -in "$SERVER_CERT" -noout -subject -issuer | sed 's/^/  /'

echo ""
echo "Certificado del emisor (CA):"
openssl x509 -in "$ISSUER_CERT" -noout -subject | sed 's/^/  /'

if [ "$CERT_COUNT" -lt 3 ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: La cadena solo tiene $CERT_COUNT certificados"
    echo "   Se esperan 3: [servidor] + [intermedio] + [raíz]"
    echo "   Esto puede causar problemas de validación en algunos navegadores."
fi

echo ""

# 4. Consulta OCSP DIRECTA (sin usar stapling del servidor)
echo "4. Consultando DIRECTAMENTE al servidor OCSP de Sectigo:"
echo "=================================================="
echo "Esto puede tomar unos segundos..."
echo ""

OCSP_RESPONSE=$(openssl ocsp \
    -issuer "$ISSUER_CERT" \
    -cert "$SERVER_CERT" \
    -url "$OCSP_URL" \
    -no_nonce \
    2>&1)

echo "$OCSP_RESPONSE"
echo ""

# 5. Analizar respuesta
echo "5. Análisis de Respuesta:"
echo "=================================================="

if echo "$OCSP_RESPONSE" | grep -q "good"; then
    echo "✅ Estado del certificado: VÁLIDO (good)"
    echo ""
    echo "El certificado NO está revocado según Sectigo OCSP."
    echo "Si el navegador muestra ERR_CERT_REVOKED, puede ser:"
    echo "  - Caché del navegador"
    echo "  - El navegador consulta CRL en lugar de OCSP"
    echo "  - Problema de sincronización de tiempo"
elif echo "$OCSP_RESPONSE" | grep -q "revoked"; then
    echo "❌ Estado del certificado: REVOCADO (revoked)"
    echo ""
    echo "El certificado HA SIDO REVOCADO por Sectigo."
    echo "Necesitas obtener un nuevo certificado de la universidad."

    # Mostrar detalles de la revocación
    echo ""
    echo "Detalles de la revocación:"
    echo "$OCSP_RESPONSE" | grep -A 5 "revoked"
else
    echo "⚠️  Estado desconocido o error en la consulta OCSP"
    echo ""
    echo "Verifica la salida anterior para más detalles."
fi

echo ""

# 6. Verificar CRL (Certificate Revocation List)
echo "6. Verificando CRL (Certificate Revocation List):"
echo "=================================================="

CRL_URL=$(openssl x509 -in "$SERVER_CERT" -noout -text | grep -A 4 "CRL Distribution" | grep "URI:" | head -1 | sed 's/.*URI://' | tr -d ' ')

if [ -n "$CRL_URL" ]; then
    echo "CRL URL encontrada: $CRL_URL"
    echo "Descargando CRL..."

    # Descargar CRL
    CRL_FILE="/tmp/cert.crl"
    curl -s -o "$CRL_FILE" "$CRL_URL"

    if [ -f "$CRL_FILE" ]; then
        # Extraer número de serie del certificado
        SERIAL=$(openssl x509 -in "$SERVER_CERT" -noout -serial | cut -d= -f2)
        echo "Número de serie del certificado: $SERIAL"

        # Convertir CRL a texto y buscar el número de serie
        openssl crl -inform DER -in "$CRL_FILE" -text -noout > /tmp/crl.txt

        if grep -q "$SERIAL" /tmp/crl.txt; then
            echo ""
            echo "❌ CERTIFICADO ENCONTRADO EN LA CRL - ESTÁ REVOCADO"
            echo ""
            echo "El certificado aparece en la lista de revocación."
            grep -A 10 "$SERIAL" /tmp/crl.txt
        else
            echo ""
            echo "✅ Certificado NO encontrado en CRL"
            echo "El certificado no aparece en la lista de revocación."
        fi

        rm -f "$CRL_FILE" /tmp/crl.txt
    else
        echo "⚠️  No se pudo descargar la CRL"
    fi
else
    echo "ℹ️  No hay URL de CRL en el certificado"
fi

echo ""

# 7. Verificar fecha/hora del sistema
echo "7. Verificación de Fecha/Hora del Sistema:"
echo "=================================================="
date
echo ""
echo "Si la fecha/hora está incorrecta, puede causar problemas de validación."

echo ""

# Limpieza
rm -f /tmp/cert-*

echo "=================================================="
echo "  Diagnóstico Completo"
echo "=================================================="
