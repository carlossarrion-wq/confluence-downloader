#!/bin/bash
# Script para ejecutar Confluence Downloader

# Activar entorno virtual
source venv/bin/activate

# Ejecutar el programa
python3 confluence_downloader.py

# Desactivar entorno virtual
deactivate