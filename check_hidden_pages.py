#!/usr/bin/env python3
"""
Script para verificar el estado de páginas que no aparecen en la web
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

# Buscar páginas específicas
search_terms = ["Mapa de integración", "OLD", "Ciclo de vida de lecturas (OLD)"]

print("="*60)
print("Verificando páginas que no aparecen en la web")
print("="*60)
print()

for page in index['pages']:
    title = page['title']
    
    # Verificar si coincide con algún término de búsqueda
    if any(term in title for term in search_terms):
        page_id = page['id']
        
        print(f"Página: {title}")
        print(f"ID: {page_id}")
        
        # Obtener información detallada de la página
        url = f"{BASE_URL}/wiki/rest/api/content/{page_id}"
        params = {'expand': 'metadata.labels,space,version,ancestors'}
        
        try:
            response = session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                # Verificar estado
                status = data.get('status', 'N/A')
                print(f"Estado: {status}")
                
                # Verificar si está archivada
                metadata = data.get('metadata', {})
                labels = metadata.get('labels', {}).get('results', [])
                label_names = [l.get('name') for l in labels]
                
                if label_names:
                    print(f"Etiquetas: {', '.join(label_names)}")
                
                # Verificar ancestros (páginas padre)
                ancestors = data.get('ancestors', [])
                if ancestors:
                    print(f"Página padre: {ancestors[-1].get('title', 'N/A')}")
                
                # URL de la página
                web_url = f"{BASE_URL}/wiki/spaces/{data['space']['key']}/pages/{page_id}"
                print(f"URL: {web_url}")
                
                # Verificar si está en el árbol de páginas
                print(f"Versión: {data.get('version', {}).get('number', 'N/A')}")
                print(f"Última modificación: {data.get('version', {}).get('when', 'N/A')}")
                
            else:
                print(f"Error al obtener información: {response.status_code}")
        
        except Exception as e:
            print(f"Error: {e}")
        
        print()
        print("-"*60)
        print()

print("="*60)
print("\nPosibles razones por las que no aparecen en la web:")
print("1. Páginas archivadas (archived)")
print("2. Páginas en borrador (draft)")
print("3. Páginas con restricciones de visualización")
print("4. Páginas huérfanas (sin padre visible)")
print("5. Páginas en espacios personales o privados")
print("="*60)