# Confluence Space Downloader

Programa en Python para descargar automáticamente todo el contenido de un espacio de Confluence, incluyendo páginas e imágenes.

## Características

- ✅ Descarga todas las páginas de un espacio de Confluence
- ✅ Descarga imágenes adjuntas a las páginas
- ✅ Mantiene la jerarquía de páginas
- ✅ Guarda contenido en formato HTML
- ✅ Incluye metadata de cada página
- ✅ Genera índice general en JSON
- ✅ Manejo de rate limiting
- ✅ Nombres de archivo seguros

## Requisitos

- Python 3.7 o superior
- Cuenta de Atlassian con acceso al espacio de Confluence
- API Token de Atlassian

## Instalación

1. **Clonar o descargar este repositorio**

2. **Instalar dependencias:**
```bash
pip3 install -r requirements.txt
```

## Configuración

### Opción 1: Editar directamente el script

Abre `confluence_downloader.py` y modifica las variables en la función `main()`:

```python
BASE_URL = "https://tu-dominio.atlassian.net"
EMAIL = "tu-email@ejemplo.com"
API_TOKEN = "tu_api_token"
SPACE_KEY = "CLAVE_DEL_ESPACIO"
OUTPUT_DIR = "confluence_export"
```

### Opción 2: Usar variables de entorno

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita `.env` con tus credenciales

3. Modifica el script para usar `python-dotenv`

## Obtener API Token de Atlassian

1. Ve a https://id.atlassian.com/manage-profile/security/api-tokens
2. Haz clic en "Create API token"
3. Dale un nombre descriptivo (ej: "Confluence Downloader")
4. Copia el token generado (¡guárdalo de forma segura!)

## Uso

### Ejecución básica:

```bash
python3 confluence_downloader.py
```

### El script:

1. Se conecta a Confluence usando tus credenciales
2. Obtiene todas las páginas del espacio especificado
3. Descarga cada página con su contenido HTML
4. Descarga las imágenes adjuntas
5. Organiza todo en una estructura de carpetas jerárquica
6. Genera un índice JSON con toda la información

## Estructura de salida

```
confluence_export/
├── index.json                          # Índice general
├── Página Principal/
│   ├── index.html                      # Contenido de la página
│   ├── metadata.json                   # Metadata de la página
│   ├── images/                         # Imágenes de la página
│   │   ├── imagen1.png
│   │   └── imagen2.jpg
│   └── Subpágina/
│       ├── index.html
│       ├── metadata.json
│       └── images/
└── Otra Página/
    ├── index.html
    └── metadata.json
```

## Características del HTML generado

Cada página HTML incluye:
- Metadata de la página (título, ID, versión, fecha)
- Contenido completo en formato HTML
- Referencias a imágenes locales
- Estilos CSS básicos para mejor visualización
- Diseño responsive

## Limitaciones y consideraciones

- **Rate Limiting**: El script incluye pausas entre peticiones para respetar los límites de la API
- **Formato**: El contenido se guarda en formato HTML con imágenes convertidas a tags `<img>` estándar
- **Imágenes**: 
  - Solo se descargan imágenes adjuntas a las páginas
  - Las imágenes se convierten de formato Confluence (`<ac:image>`) a HTML estándar (`<img>`)
  - Las imágenes externas (URLs) no se descargan
  - Las imágenes se guardan en carpetas `images/` dentro de cada página
- **Permisos**: Solo descarga contenido al que tu usuario tiene acceso
- **Tamaño**: Espacios muy grandes pueden tardar bastante tiempo (aproximadamente 1-2 minutos por cada 10 páginas)
- **Tiempo de ejecución**: Para 57 páginas, el proceso tarda aproximadamente 5-10 minutos

## Solución de problemas

### Error de autenticación
- Verifica que el email y API token sean correctos
- Asegúrate de que el token no haya expirado
- Verifica que tienes acceso al espacio

### Error 404 en páginas
- Verifica que la clave del espacio sea correcta
- Asegúrate de tener permisos de lectura en el espacio

### Imágenes no se descargan
- Verifica que las imágenes estén adjuntas a la página
- Comprueba los permisos de acceso a los adjuntos

## Personalización

### Cambiar formato de salida

Puedes modificar la función `process_html_content()` para:
- Convertir a Markdown
- Generar PDFs
- Extraer solo texto plano

### Filtrar páginas

Modifica `get_all_pages()` para:
- Descargar solo páginas específicas
- Filtrar por etiquetas
- Limitar por fecha de modificación

### Descargar más tipos de adjuntos

Modifica `process_html_content()` para:
- Descargar PDFs
- Descargar documentos Office
- Descargar cualquier tipo de archivo

## Seguridad

⚠️ **IMPORTANTE**: 
- Nunca compartas tu API Token
- No subas el archivo `.env` a repositorios públicos
- Considera usar un gestor de secretos para producción
- El API Token tiene los mismos permisos que tu usuario

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Haz push a la rama
5. Abre un Pull Request

## Soporte

Para problemas o preguntas:
- Abre un issue en el repositorio
- Consulta la documentación de la API de Confluence: https://developer.atlassian.com/cloud/confluence/rest/

## Changelog

### v1.0.0 (2026-03-19)
- Versión inicial
- Descarga de páginas en HTML
- Descarga de imágenes
- Estructura jerárquica
- Generación de índice JSON