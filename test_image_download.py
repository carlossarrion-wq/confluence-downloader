#!/usr/bin/env python3
"""
Script de prueba para investigar la descarga de imágenes de Confluence
"""

import requests
import json

# Configuración
BASE_URL = "https://tu-dominio.atlassian.net"
EMAIL = "tu-email@ejemplo.com"
API_TOKEN = "tu_api_token_aqui"
PAGE_ID = "1424883735"  # ID de la página "3.3. NU_03 - Registro de contador"

# Crear sesión
session = requests.Session()
session.auth = (EMAIL, API_TOKEN)
session.headers.update({
    'Accept': 'application/json',
    'Content-Type': 'application/json'
})

print("="*60)
print("Investigando descarga de imágenes de Confluence")
print("="*60)
print()

# 1. Obtener información de la página
print(f"1. Obteniendo información de la página {PAGE_ID}...")
api_base = f"{BASE_URL}/wiki/rest/api"
url = f"{api_base}/content/{PAGE_ID}"
params = {
    'expand': 'body.storage,children.attachment'
}

response = session.get(url, params=params)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    page_data = response.json()
    print(f"   Título: {page_data.get('title')}")
    print()
    
    # 2. Ver adjuntos
    attachments = page_data.get('children', {}).get('attachment', {}).get('results', [])
    print(f"2. Adjuntos encontrados: {len(attachments)}")
    print()
    
    if attachments:
        for idx, att in enumerate(attachments[:3], 1):  # Solo primeros 3
            print(f"   Adjunto {idx}:")
            print(f"     - Título: {att.get('title')}")
            print(f"     - Tipo: {att.get('metadata', {}).get('mediaType', 'N/A')}")
            print(f"     - ID: {att.get('id')}")
            
            # Ver todos los links disponibles
            links = att.get('_links', {})
            print(f"     - Links disponibles:")
            for link_name, link_url in links.items():
                print(f"       * {link_name}: {link_url}")
            
            # Intentar descargar con diferentes URLs
            print(f"     - Intentando descargar...")
            
            # Método 1: URL de download del _links
            download_url = links.get('download', '')
            if download_url:
                if not download_url.startswith('http'):
                    download_url = BASE_URL + download_url
                
                print(f"       Método 1 (download link): {download_url}")
                try:
                    r = session.get(download_url, stream=True)
                    print(f"       → Status: {r.status_code}")
                    if r.status_code == 200:
                        print(f"       → ✓ Éxito! Content-Type: {r.headers.get('content-type')}")
                        print(f"       → Tamaño: {len(r.content)} bytes")
                    else:
                        print(f"       → ✗ Error: {r.text[:200]}")
                except Exception as e:
                    print(f"       → ✗ Excepción: {e}")
            
            # Método 2: URL webui
            webui_url = links.get('webui', '')
            if webui_url:
                if not webui_url.startswith('http'):
                    webui_url = BASE_URL + webui_url
                print(f"       Método 2 (webui): {webui_url}")
            
            print()
    
    # 3. Ver contenido HTML para entender el formato
    html_content = page_data.get('body', {}).get('storage', {}).get('value', '')
    if '<ac:image' in html_content:
        print("3. Formato de imágenes en el HTML:")
        import re
        images = re.findall(r'<ac:image[^>]*>.*?</ac:image>', html_content, re.DOTALL)
        for idx, img in enumerate(images[:2], 1):  # Solo primeras 2
            print(f"   Imagen {idx}:")
            print(f"   {img[:300]}...")
            print()
else:
    print(f"   Error: {response.text}")

print("="*60)