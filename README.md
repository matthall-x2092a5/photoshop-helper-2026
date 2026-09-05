# photoshop-helper-2026

A modern, high-performance Python utility library designed to streamline Adobe Photoshop workflows through scriptable automation, batch processing, and asset management.

## Description

`photoshop-helper-2026` bridges the gap between Python's data processing capabilities and Adobe Photoshop's creative power. It provides a robust API for executing ExtendScript (JSX) commands, managing document states, and automating repetitive design tasks. Built for efficiency, it supports both local execution and remote batch processing, making it ideal for developers integrating design tools into larger production pipelines.

## Features

- **Script Execution Engine**: Seamlessly execute custom ExtendScript or JSX files from Python with full error handling.
- **Document Management**: Open, save, close, and duplicate PSD files programmatically with support for version control.
- **Batch Processing**: Process hundreds of assets simultaneously with configurable queueing and retry logic.
- **Asset Metadata Extraction**: Read and write XMP metadata, layer information, and image properties.
- **Plugin Integration**: Load and manage third-party Photoshop plugins dynamically.
- **Logging & Debugging**: Comprehensive logging system to track script execution, errors, and performance metrics.
- **Async Support**: Non-blocking operations for concurrent document handling where supported by the environment.

## Installation

Ensure you have Python 3.8+ installed. You can install the package using `pip`:

```bash
pip install photoshop-helper-2026
```

If you are working in a virtual environment, activate it before installing:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install photoshop-helper-2026
```

## Usage Example

The following example demonstrates how to open a Photoshop document, apply a basic filter, and save the result using `photoshop-helper-2026`.

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

## Configuration

`photoshop-helper-2026` supports configuration via a `config.yaml` file or environment variables. Below is an example `config.yaml`:

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

You can also override specific settings via environment variables:

- `PSHELPER_PHOTOSHOP_PATH`: Path to the Photoshop executable.
- `PSHELPER_PORT`: Port number for the Photoshop COM/OSC bridge.
- `PSHELPER_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.