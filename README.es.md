🌍 [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md)

# photoshop-helper-2026

Una biblioteca de utilidades Python moderna y de alto rendimiento diseñada para optimizar los flujos de trabajo de Adobe Photoshop mediante automatización programable, procesamiento por lotes y gestión de activos.

## Descripción

`photoshop-helper-2026` cierra la brecha entre las capacidades de procesamiento de datos de Python y el poder creativo de Adobe Photoshop. Proporciona una API robusta para ejecutar comandos ExtendScript (JSX), gestionar estados de documentos y automatizar tareas de diseño repetitivas. Construida para la eficiencia, soporta tanto la ejecución local como el procesamiento remoto por lotes, lo que la hace ideal para desarrolladores que integran herramientas de diseño en pipelines de producción más grandes.

## Características

- **Motor de Ejecución de Scripts**: Ejecuta sin problemas archivos ExtendScript o JSX personalizados desde Python con manejo completo de errores.
- **Gestión de Documentos**: Abre, guarda, cierra y duplica archivos PSD programáticamente con soporte para control de versiones.
- **Procesamiento por Lotes**: Procesa cientos de activos simultáneamente con colas configurables y lógica de reintento.
- **Extracción de Metadatos de Activos**: Lee y escribe metadatos XMP, información de capas y propiedades de imagen.
- **Integración de Plugins**: Carga y gestiona plugins de Photoshop de terceros dinámicamente.
- **Registro y Depuración**: Sistema de registro completo para rastrear la ejecución de scripts, errores y métricas de rendimiento.
- **Soporte Asíncrono**: Operaciones no bloqueantes para el manejo concurrente de documentos donde el entorno lo soporte.

## Instalación

Asegúrate de tener Python 3.8+ instalado. Puedes instalar el paquete usando `pip`:

```bash
pip install photoshop-helper-2026
```

Si estás trabajando en un entorno virtual, actívalo antes de instalar:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install photoshop-helper-2026
```

## Ejemplo de Uso

El siguiente ejemplo demuestra cómo abrir un documento de Photoshop, aplicar un filtro básico y guardar el resultado usando `photoshop-helper-2026`.

```python
from photoshop_helper import PhotoshopSession
from photoshop_helper.config import PhotoshopConfig

# Initialize configuration
config = PhotoshopConfig(
    photoshop_path="/Applications/Adobe Photoshop 2026.app",
    port=1049,
    timeout=30
)

# Create a session
with PhotoshopSession(config) as ps:
    # Open a document
    doc = ps.open_document("/path/to/source_image.psd")
    
    # Apply a Gaussian Blur filter (example JSX command)
    jsx_code = """
    var doc = app.activeDocument;
    var gbl = new ActionReference();
    gbl.putProperty(charIDToTypeID("Prpr"), stringIDToTypeID("GaussianBlur"));
    var gblDesc = new ActionDescriptor();
    gblDesc.putUnitDouble(stringIDToTypeID("Radius"), charIDToTypeID("#Pxl"), 5.0);
    gblDesc.putString(stringIDToTypeID("version"), "11.0");
    
    var desc = new ActionDescriptor();
    desc.putReference(stringIDToTypeID("null"), gbl);
    desc.putObject(stringIDToTypeID("T"), stringIDToTypeID("RVS"), "GaussianBlur");
    desc.putObject(stringIDToTypeID("T"), stringIDToTypeID("GaussianBlur"), gblDesc);
    
    var eventID = stringIDToTypeID("set");
    var eventRef = new ActionReference();
    eventRef.putClass(stringIDToTypeID("Plyr"));
    executeAction(eventID, desc, DialogModes.NO);
    """
    
    ps.execute_jsx(jsx_code)
    
    # Save as a new file
    ps.save_as(doc, "/path/to/output_image.psd", format="psd")
    
    # Close the document
    ps.close(doc, save_changes=True)

print("Batch processing completed successfully.")
```

## Configuración

`photoshop-helper-2026` soporta la configuración a través de un archivo `config.yaml` o variables de entorno. A continuación se muestra un ejemplo de `config.yaml`:

```yaml
photoshop:
  path: "/Applications/Adobe Photoshop 2026.app"
  port: 1049
  timeout: 30

logging:
  level: "INFO"
  file: "photoshop_helper.log"
  format: "%(asctime)s - %(levelname)s - %(message)s"

batch:
  max_workers: 4
  retry_attempts: 3
  retry_delay: 2
```

También puedes anular configuraciones específicas a través de variables de entorno:

- `PSHELPER_PHOTOSHOP_PATH`: Path al ejecutable de Photoshop.
- `PSHELPER_PORT`: Número de puerto para el puente COM/OSC de Photoshop.
- `PSHELPER_LOG_LEVEL`: Nivel de registro (DEBUG, INFO, WARNING, ERROR).

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.