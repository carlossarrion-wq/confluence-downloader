#!/usr/bin/env python3
"""
Lista todas las páginas archivadas del espacio
"""

import requests
import json

# Configuración
BASE_URL = "https://tu-dominio.atlassian.net"
EMAIL = "tu-email@ejemplo.com"
API_TOKEN = "tu_api_token_aqui"

# Crear sesión
session = requests.Session()
session.auth = (EMAIL, API_TOKEN)
session.headers.update({'Accept': 'application/json'})

# Leer el índice
with open('confluence_export/index.json', 'r') as f:
    index = json.load(f)

print("="*60)
print("Verificando TODAS las páginas descargadas")
print("="*60)
print()

archived_pages = []
current_pages = []

for page in index['pages']:
    page_id = page['id']
    title = page['title']
    
    # Obtener información detallada
    url = f"{BASE_URL}/wiki/rest/api/content/{page_id}"
    params = {'expand': 'space,version'}
    
    try:
        response = session.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'N/A')
            
            if status == 'archived':
                archived_pages.append({
                    'title': title,
                    'id': page_id,
                    'modified': data.get('version', {}).get('when', 'N/A')
                })
            else:
                current_pages.append({
                    'title': title,
                    'id': page_id,
                    'status': status
                })
    except Exception as e:
        print(f"Error verificando {title}: {e}")

print(f"📊 RESUMEN:")
print(f"  Total de páginas: {len(index['pages'])}")
print(f"  Páginas activas: {len(current_pages)}")
print(f"  Páginas archivadas: {len(archived_pages)}")
print()

if archived_pages:
    print("="*60)
    print("📦 PÁGINAS ARCHIVADAS (no visibles en la web):")
    print("="*60)
    for i, page in enumerate(archived_pages, 1):
        print(f"\n{i}. {page['title']}")
        print(f"   ID: {page['id']}")
        print(f"   Última modificación: {page['modified']}")
        print(f"   URL: {BASE_URL}/wiki/spaces/Y/pages/{page['id']}")
    print()
    print("="*60)
    print("\n💡 EXPLICACIÓN:")
    print("Las páginas archivadas:")
    print("  ✓ Siguen existiendo en Confluence")
    print("  ✓ Conservan todo su contenido")
    print("  ✓ Son accesibles vía API")
    print("  ✗ NO aparecen en el árbol de páginas web")
    print("  ✗ NO aparecen en búsquedas normales")
    print("\nEstas páginas fueron archivadas (no borradas) por algún")
    print("administrador, probablemente porque:")
    print("  - Son versiones antiguas (OLD)")
    print("  - Contenido obsoleto pero que se quiere preservar")
    print("  - Documentación histórica de referencia")
    print("="*60)