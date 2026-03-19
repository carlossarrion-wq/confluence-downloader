#!/usr/bin/env python3
"""
Script de prueba para probar diferentes métodos de descarga
"""

import requests

# Configuración
BASE_URL = "https://tu-dominio.atlassian.net"
EMAIL = "tu-email@ejemplo.com"
API_TOKEN = "tu_api_token_aqui"

# Crear sesión
session = requests.Session()
session.auth = (EMAIL, API_TOKEN)

# Datos del primer adjunto
att_id = "att1425932355"
page_id = "1424883735"
filename = "image-20250917-154039.png"

print("Probando diferentes URLs de descarga:")
print("="*60)

# Método 1: URL que da la API (sabemos que falla)
url1 = f"{BASE_URL}/download/attachments/{page_id}/{filename}?version=1&modificationDate=1760455617149&cacheVersion=1&api=v2"
print(f"\n1. URL de la API:")
print(f"   {url1}")
r = session.get(url1)
print(f"   Status: {r.status_code}")

# Método 2: URL sin parámetros
url2 = f"{BASE_URL}/download/attachments/{page_id}/{filename}"
print(f"\n2. URL sin parámetros:")
print(f"   {url2}")
r = session.get(url2)
print(f"   Status: {r.status_code}")

# Método 3: URL con /wiki/
url3 = f"{BASE_URL}/wiki/download/attachments/{page_id}/{filename}"
print(f"\n3. URL con /wiki/:")
print(f"   {url3}")
r = session.get(url3)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   ✓ ¡ÉXITO! Tamaño: {len(r.content)} bytes")

# Método 4: Usando el ID del adjunto directamente
url4 = f"{BASE_URL}/wiki/rest/api/content/{att_id}/download"
print(f"\n4. URL usando ID del adjunto:")
print(f"   {url4}")
r = session.get(url4)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   ✓ ¡ÉXITO! Tamaño: {len(r.content)} bytes")

# Método 5: Obtener datos del adjunto y usar su download link
url5 = f"{BASE_URL}/wiki/rest/api/content/{att_id}"
print(f"\n5. Obtener datos del adjunto:")
print(f"   {url5}")
r = session.get(url5, headers={'Accept': 'application/json'})
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    download_link = data.get('_links', {}).get('download', '')
    if download_link:
        if not download_link.startswith('http'):
            download_link = BASE_URL + download_link
        print(f"   Download link: {download_link}")
        r2 = session.get(download_link)
        print(f"   Download status: {r2.status_code}")
        if r2.status_code == 200:
            print(f"   ✓ ¡ÉXITO! Tamaño: {len(r2.content)} bytes")

# Método 6: URL alternativa con /download/
url6 = f"{BASE_URL}/wiki/download/{att_id}/{filename}"
print(f"\n6. URL alternativa con ID:")
print(f"   {url6}")
r = session.get(url6)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   ✓ ¡ÉXITO! Tamaño: {len(r.content)} bytes")

print("\n" + "="*60)