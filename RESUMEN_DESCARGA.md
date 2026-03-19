# Resumen de la Descarga de Confluence

## Información General

- **Espacio descargado**: Y (Nedgia - YoLeoGas)
- **URL**: https://naturgy-adn.atlassian.net/wiki/spaces/Y/overview
- **Fecha de descarga**: 19 de marzo de 2026
- **Total de páginas**: 57

## Estadísticas

- **Páginas descargadas**: 57
- **Páginas con imágenes**: 26
- **Tamaño total**: ~1.1 MB

## Estructura del Contenido

El contenido se ha organizado en la siguiente estructura:

```
confluence_export/
├── index.json                          # Índice completo con metadata
├── Nedgia - YoLeoGas/                  # Página principal
│   ├── Documentación Funcional/
│   │   ├── DF App Mobile/
│   │   │   ├── DF App YoLeoGas/
│   │   │   └── 🧪 Plan de Pruebas – YoLeoGas APP/
│   │   ├── DF Procesos Backend/
│   │   │   └── DF Procesos Backend/
│   │   └── DF Web BackOffice/
│   │       ├── DF Web BackOffice YoLeoGas/
│   │       └── 🧪 Plan de pruebas - Web Backoffice YoLeoGas/
│   ├── Documentación Técnica/
│   │   ├── DT App Mobile/
│   │   ├── DT Web App BackOffice/
│   │   ├── DT Web App Backend y WebApi/
│   │   └── General/
│   └── Soporte/
└── [Páginas individuales en raíz]
```

## Contenido por Categoría

### Documentación Funcional (DF)

#### App Mobile
- Introducción
- Descripción conceptual
- Descripción funcional detallada (7 casos de uso)
- Plan de pruebas

#### Web BackOffice
- Introducción
- Descripción conceptual
- Descripción funcional detallada (10 casos de uso)
- Plan de pruebas

#### Procesos Backend
- Introducción
- Descripción conceptual
- Descripción funcional detallada (5 casos de uso)

### Documentación Técnica (DT)

- App Flutter
- API Rest
- Base de Datos
- Front React
- Backend y WebApi
- Análisis de Arquitectura

### Soporte

- Sistemas de Monitorización YoLeoGas

## Formato de las Páginas

Cada página descargada incluye:

1. **index.html**: Contenido completo de la página con:
   - Metadata (título, ID, versión, fecha de modificación)
   - Contenido HTML original de Confluence
   - Estilos CSS para visualización
   - Referencias a imágenes locales

2. **metadata.json**: Información estructurada:
   - ID de la página
   - Título
   - Tipo
   - Número de versión
   - Fecha de última modificación
   - Ruta en la jerarquía

3. **images/** (si aplica): Carpeta con imágenes adjuntas

## Cómo Navegar el Contenido

### Opción 1: Navegador Web
Abre cualquier archivo `index.html` en tu navegador favorito:
```bash
open confluence_export/Nedgia\ -\ YoLeoGas/index.html
```

### Opción 2: Explorador de Archivos
Navega por las carpetas usando Finder (macOS) o tu explorador de archivos.

### Opción 3: Búsqueda por Contenido
Usa grep para buscar contenido específico:
```bash
grep -r "palabra_clave" confluence_export/
```

### Opción 4: Consultar el Índice
El archivo `index.json` contiene toda la metadata:
```bash
cat confluence_export/index.json | jq '.pages[] | {title, path}'
```

## Páginas Principales

1. **Nedgia - YoLeoGas** (Página raíz)
2. **DF App YoLeoGas** - Documentación funcional de la app móvil
3. **DF Web BackOffice YoLeoGas** - Documentación del backoffice web
4. **DF Procesos Backend** - Documentación de procesos backend
5. **Documentación Técnica** - Especificaciones técnicas

## Notas Importantes

- ✅ Todas las páginas se descargaron correctamente
- ✅ La jerarquía de páginas se mantiene
- ✅ Las imágenes adjuntas están en carpetas `images/`
- ✅ Las imágenes se convierten a tags HTML estándar `<img>`
- ✅ **Solución aplicada**: Las URLs de descarga de Confluence Cloud requieren `/wiki/` en la ruta
- ℹ️ Algunas páginas pueden tener caracteres especiales en los nombres

## Próximos Pasos Sugeridos

1. **Backup**: Considera hacer una copia de seguridad de `confluence_export/`
2. **Conversión**: Si necesitas otro formato (Markdown, PDF), puedes usar herramientas adicionales
3. **Búsqueda**: Implementa un sistema de búsqueda local si lo necesitas
4. **Actualización**: Ejecuta el script periódicamente para mantener actualizado el contenido

## Comandos Útiles

### Ver estadísticas
```bash
./check_progress.sh
```

### Buscar una página específica
```bash
find confluence_export -name "*nombre_pagina*"
```

### Listar todas las páginas
```bash
find confluence_export -name "index.html" -exec dirname {} \;
```

### Ver metadata de una página
```bash
cat "confluence_export/Nedgia - YoLeoGas/metadata.json" | jq
```

## Soporte

Si necesitas ayuda o tienes preguntas:
- Revisa el README.md para instrucciones detalladas
- Consulta el código fuente en `confluence_downloader.py`
- Verifica los logs de ejecución si hubo errores