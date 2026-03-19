#!/bin/bash
# Script para verificar las imágenes descargadas

echo "================================================"
echo "Verificación de Imágenes Descargadas"
echo "================================================"
echo ""

# Contar imágenes por tipo
echo "Imágenes por tipo:"
echo "  PNG:  $(find confluence_export -name "*.png" 2>/dev/null | wc -l | tr -d ' ')"
echo "  JPG:  $(find confluence_export -name "*.jpg" -o -name "*.jpeg" 2>/dev/null | wc -l | tr -d ' ')"
echo "  GIF:  $(find confluence_export -name "*.gif" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Otros: $(find confluence_export/*/images -type f ! -name "*.png" ! -name "*.jpg" ! -name "*.jpeg" ! -name "*.gif" 2>/dev/null | wc -l | tr -d ' ')"

echo ""
echo "Total de imágenes: $(find confluence_export -type d -name "images" -exec find {} -type f \; 2>/dev/null | wc -l | tr -d ' ')"

echo ""
echo "Carpetas con imágenes:"
find confluence_export -type d -name "images" -exec sh -c 'count=$(find "$1" -type f 2>/dev/null | wc -l | tr -d " "); if [ "$count" -gt 0 ]; then echo "  $(dirname "$1" | sed "s|confluence_export/||"): $count imágenes"; fi' _ {} \; 2>/dev/null | head -10

echo ""
echo "================================================"