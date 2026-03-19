#!/bin/bash
# Script para verificar el progreso de la descarga

echo "================================================"
echo "Estado de la descarga de Confluence"
echo "================================================"
echo ""

# Verificar si el proceso está corriendo
if ps aux | grep -v grep | grep confluence_downloader.py > /dev/null; then
    echo "✓ El proceso está en ejecución"
    echo ""
else
    echo "✗ El proceso no está en ejecución"
    echo ""
fi

# Contar páginas descargadas
PAGES=$(find confluence_export -name "index.html" 2>/dev/null | wc -l | tr -d ' ')
echo "Páginas descargadas: $PAGES"

# Contar directorios con imágenes
IMAGES_DIRS=$(find confluence_export -type d -name "images" 2>/dev/null | wc -l | tr -d ' ')
echo "Páginas con imágenes: $IMAGES_DIRS"

# Contar total de imágenes
TOTAL_IMAGES=$(find confluence_export -type d -name "images" -exec find {} -type f \; 2>/dev/null | wc -l | tr -d ' ')
echo "Total de imágenes descargadas: $TOTAL_IMAGES"

# Tamaño total
SIZE=$(du -sh confluence_export 2>/dev/null | cut -f1)
echo "Tamaño total: $SIZE"

echo ""

# Verificar si existe el índice
if [ -f "confluence_export/index.json" ]; then
    echo "✓ Descarga completada - índice generado"
    TOTAL=$(grep -o '"total_pages":[0-9]*' confluence_export/index.json | cut -d: -f2)
    echo "Total de páginas en el espacio: $TOTAL"
else
    echo "⏳ Descarga en progreso..."
fi

echo ""
echo "================================================"