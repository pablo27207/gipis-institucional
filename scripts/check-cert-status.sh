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

# Extraer el segundo certificado (emisor/CA intermedio)
csplit -s -f /tmp/cert- "$CERT_FILE" '/-----BEGIN CERTIFICATE-----/' '{*}'
ISSUER_CERT="/tmp/cert-02"

if [ ! -f "$ISSUER_CERT" ]; then
    echo "❌ Error: No se pudo extraer el certificado del emisor"
    rm -f /tmp/cert-*
    exit 1
fi

echo "✅ Certificado del emisor extraído"
echo ""

# 4. Consulta OCSP DIRECTA (sin usar stapling del servidor)
echo "4. Consultando DIRECTAMENTE al servidor OCSP de Sectigo:"
echo "=================================================="
echo "Esto puede tomar unos segundos..."
echo ""

OCSP_RESPONSE=$(openssl ocsp \
    -issuer "$ISSUER_CERT" \
    -cert "$CERT_FILE" \
    -url "$OCSP_URL" \
    -header "Host" "ocsp.sectigo.com" \
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

CRL_URL=$(openssl x509 -in "$CERT_FILE" -noout -text | grep -A 4 "CRL Distribution" | grep "URI:" | sed 's/.*URI://')

if [ -n "$CRL_URL" ]; then
    echo "CRL URL encontrada: $CRL_URL"
    echo "Descargando CRL..."

    # Descargar CRL
    CRL_FILE="/tmp/cert.crl"
    curl -s -o "$CRL_FILE" "$CRL_URL"

    if [ -f "$CRL_FILE" ]; then
        # Extraer número de serie del certificado
        SERIAL=$(openssl x509 -in "$CERT_FILE" -noout -serial | cut -d= -f2)
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
