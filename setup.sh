#!/bin/bash
# Script de instalación para Confluence Downloader

echo "================================================"
echo "Confluence Space Downloader - Instalación"
echo "================================================"
echo ""

# Crear entorno virtual
echo "1. Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "2. Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "3. Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "================================================"
echo "✓ Instalación completada!"
echo "================================================"
echo ""
echo "Para ejecutar el programa:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ejecuta el script: python3 confluence_downloader.py"
echo "  3. Para desactivar el entorno: deactivate"
echo ""