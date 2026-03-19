#!/usr/bin/env python3
"""
Confluence Space Downloader
Descarga todo el contenido de un espacio de Confluence incluyendo páginas e imágenes
"""

import os
import requests
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict, Optional
import re

class ConfluenceDownloader:
    def __init__(self, base_url: str, email: str, api_token: str, space_key: str):
        """
        Inicializa el descargador de Confluence
        
        Args:
            base_url: URL base de Confluence (ej: https://naturgy-adn.atlassian.net)
            email: Email del usuario
            api_token: API Token de Atlassian
            space_key: Clave del espacio a descargar
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/wiki/rest/api"
        self.auth = (email, api_token)
        self.space_key = space_key
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Realiza una petición a la API de Confluence"""
        url = f"{self.api_base}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en petición a {url}: {e}")
            raise
    
    def get_all_pages(self) -> List[Dict]:
        """Obtiene todas las páginas del espacio"""
        print(f"Obteniendo páginas del espacio '{self.space_key}'...")
        pages = []
        start = 0
        limit = 50
        
        while True:
            params = {
                'spaceKey': self.space_key,
                'start': start,
                'limit': limit,
                'expand': 'version,space,ancestors'
            }
            
            data = self._make_request('content', params)
            results = data.get('results', [])
            
            if not results:
                break
                
            pages.extend(results)
            print(f"  Obtenidas {len(pages)} páginas...")
            
            if len(results) < limit:
                break
                
            start += limit
            time.sleep(0.5)  # Rate limiting
        
        print(f"Total de páginas encontradas: {len(pages)}")
        return pages
    
    def get_page_content(self, page_id: str) -> Dict:
        """Obtiene el contenido completo de una página"""
        params = {
            'expand': 'body.storage,version,space,ancestors,children.attachment'
        }
        return self._make_request(f'content/{page_id}', params)
    
    def download_attachment(self, attachment_url: str, output_path: Path) -> bool:
        """Descarga un adjunto"""
        try:
            # Construir URL completa si es relativa
            if not attachment_url.startswith('http'):
                attachment_url = urljoin(self.base_url, attachment_url)
            
            # FIX: Confluence Cloud requiere /wiki/ en la URL de descarga
            # Reemplazar /download/attachments/ por /wiki/download/attachments/
            if '/download/attachments/' in attachment_url and '/wiki/download/attachments/' not in attachment_url:
                attachment_url = attachment_url.replace('/download/attachments/', '/wiki/download/attachments/')
            
            response = self.session.get(attachment_url, stream=True)
            response.raise_for_status()
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"  Error descargando {attachment_url}: {e}")
            return False
    
    def sanitize_filename(self, filename: str) -> str:
        """Limpia el nombre de archivo para el sistema de archivos"""
        # Reemplazar caracteres no válidos
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limitar longitud
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
        return filename
    
    def get_page_hierarchy_path(self, page: Dict) -> str:
        """Construye la ruta jerárquica de una página"""
        ancestors = page.get('ancestors', [])
        path_parts = [self.sanitize_filename(a['title']) for a in ancestors]
        path_parts.append(self.sanitize_filename(page['title']))
        return os.path.join(*path_parts) if path_parts else self.sanitize_filename(page['title'])
    
    def process_html_content(self, html_content: str, page_dir: Path, page_id: str) -> str:
        """Procesa el contenido HTML y descarga las imágenes"""
        # Obtener adjuntos de la página primero
        page_data = self.get_page_content(page_id)
        attachments = page_data.get('children', {}).get('attachment', {}).get('results', [])
        
        if not attachments:
            return html_content
        
        # Crear directorio de imágenes
        images_dir = page_dir / 'images'
        images_dir.mkdir(exist_ok=True)
        
        # Buscar todas las referencias a imágenes en diferentes formatos
        # Formato 1: <ac:image><ri:attachment ri:filename="..."/>
        pattern1 = r'<ac:image[^>]*>.*?<ri:attachment ri:filename="([^"]+)"[^>]*/>.*?</ac:image>'
        # Formato 2: <ac:image><ri:url ri:value="..."/>
        pattern2 = r'<ac:image[^>]*>.*?<ri:url ri:value="([^"]+)"[^>]*/>.*?</ac:image>'
        
        images_found = set()
        images_found.update(re.findall(pattern1, html_content, re.DOTALL))
        
        if images_found:
            print(f"    Encontradas {len(images_found)} imágenes en la página")
            
            downloaded_count = 0
            # Descargar cada imagen
            for img_filename in images_found:
                # Buscar el adjunto correspondiente
                attachment = next((a for a in attachments if a['title'] == img_filename), None)
                
                if attachment:
                    download_url = attachment['_links']['download']
                    if not download_url.startswith('http'):
                        download_url = self.base_url + download_url
                    
                    safe_filename = self.sanitize_filename(img_filename)
                    img_path = images_dir / safe_filename
                    
                    print(f"      Descargando imagen: {img_filename}")
                    if self.download_attachment(download_url, img_path):
                        downloaded_count += 1
                        # Reemplazar el bloque completo de ac:image con un img tag HTML estándar
                        old_pattern = f'<ac:image[^>]*>.*?<ri:attachment ri:filename="{re.escape(img_filename)}"[^>]*/>.*?</ac:image>'
                        new_img = f'<img src="images/{safe_filename}" alt="{img_filename}" style="max-width: 100%;" />'
                        html_content = re.sub(old_pattern, new_img, html_content, flags=re.DOTALL)
                else:
                    print(f"      ⚠️ No se encontró adjunto para: {img_filename}")
            
            print(f"    ✓ Descargadas {downloaded_count}/{len(images_found)} imágenes")
        
        return html_content
    
    def download_space(self, output_dir: str = 'confluence_export'):
        """Descarga todo el espacio de Confluence"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Iniciando descarga del espacio '{self.space_key}'")
        print(f"Directorio de salida: {output_path.absolute()}")
        print(f"{'='*60}\n")
        
        # Obtener todas las páginas
        pages = self.get_all_pages()
        
        if not pages:
            print("No se encontraron páginas en el espacio.")
            return
        
        # Crear índice
        index_data = {
            'space_key': self.space_key,
            'total_pages': len(pages),
            'pages': []
        }
        
        # Procesar cada página
        for idx, page in enumerate(pages, 1):
            page_id = page['id']
            page_title = page['title']
            
            print(f"\n[{idx}/{len(pages)}] Procesando: {page_title}")
            
            try:
                # Obtener contenido completo
                full_page = self.get_page_content(page_id)
                
                # Crear directorio para la página
                page_path = self.get_page_hierarchy_path(full_page)
                page_dir = output_path / page_path
                page_dir.mkdir(parents=True, exist_ok=True)
                
                # Obtener contenido HTML
                html_content = full_page.get('body', {}).get('storage', {}).get('value', '')
                
                # Procesar imágenes
                html_content = self.process_html_content(html_content, page_dir, page_id)
                
                # Crear HTML completo
                html_full = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #172B4D;
            margin-top: 1.5em;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        .metadata {{
            background: #f4f5f7;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="metadata">
        <strong>Página:</strong> {page_title}<br>
        <strong>ID:</strong> {page_id}<br>
        <strong>Espacio:</strong> {self.space_key}<br>
        <strong>Versión:</strong> {full_page.get('version', {}).get('number', 'N/A')}<br>
        <strong>Última modificación:</strong> {full_page.get('version', {}).get('when', 'N/A')}
    </div>
    <hr>
    {html_content}
</body>
</html>"""
                
                # Guardar HTML
                html_file = page_dir / 'index.html'
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_full)
                
                # Guardar metadata
                metadata = {
                    'id': page_id,
                    'title': page_title,
                    'type': full_page.get('type'),
                    'version': full_page.get('version', {}).get('number'),
                    'last_modified': full_page.get('version', {}).get('when'),
                    'path': page_path
                }
                
                with open(page_dir / 'metadata.json', 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                index_data['pages'].append(metadata)
                
                print(f"  ✓ Guardado en: {page_dir}")
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"  ✗ Error procesando página: {e}")
                continue
        
        # Guardar índice general
        with open(output_path / 'index.json', 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"✓ Descarga completada!")
        print(f"  Total páginas: {len(pages)}")
        print(f"  Directorio: {output_path.absolute()}")
        print(f"{'='*60}\n")


def main():
    """Función principal"""
    # Configuración
    BASE_URL = "https://tu-dominio.atlassian.net"
    EMAIL = "tu-email@ejemplo.com"
    API_TOKEN = "tu_api_token_aqui"
    SPACE_KEY = "CLAVE_DEL_ESPACIO"
    OUTPUT_DIR = "confluence_export"
    
    # Crear descargador
    downloader = ConfluenceDownloader(BASE_URL, EMAIL, API_TOKEN, SPACE_KEY)
    
    # Descargar espacio
    downloader.download_space(OUTPUT_DIR)


if __name__ == "__main__":
    main()