🌍 [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md)

# photoshop-helper-2026

一个现代的、高性能的 Python 实用程序库，旨在通过可脚本化自动化、批量处理和资产管理来简化 Adobe Photoshop 工作流程。

## Description

`photoshop-helper-2026` 弥合了 Python 的数据处理能力与 Adobe Photoshop 的创意能力之间的鸿沟。它提供了一个强大的 API，用于执行 ExtendScript (JSX) 命令、管理文档状态以及自动化重复的设计任务。它专为效率而构建，支持本地执行和远程批量处理，使其成为将设计工具集成到大型生产流程中的开发人员的理想选择。

## Features

- **脚本执行引擎**: 从 Python 无缝执行自定义 ExtendScript 或 JSX 文件，并提供完整的错误处理。
- **文档管理**: 以编程方式打开、保存、关闭和复制 PSD 文件，并支持版本控制。
- **批量处理**: 通过可配置的队列和重试逻辑，同时处理数百个资产。
- **资产元数据提取**: 读取和写入 XMP 元数据、图层信息和图像属性。
- **插件集成**: 动态加载和管理第三方 Photoshop 插件。
- **日志记录与调试**: 全面的日志系统，用于跟踪脚本执行、错误和性能指标。
- **异步支持**: 在环境支持的情况下，为并发文档处理提供非阻塞操作。

## Installation

确保您已安装 Python 3.8+。您可以使用 `pip` 安装此包：

```bash
pip install photoshop-helper-2026
```

如果您正在虚拟环境中工作，请在安装前激活它：

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install photoshop-helper-2026
```

## Usage Example

以下示例演示了如何使用 `photoshop-helper-2026` 打开 Photoshop 文档、应用基本滤镜并保存结果。

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

`photoshop-helper-2026` 支持通过 `config.yaml` 文件或环境变量进行配置。以下是一个 `config.yaml` 示例：

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

您还可以通过环境变量覆盖特定设置：

- `PSHELPER_PHOTOSHOP_PATH`: Path to the Photoshop executable.
- `PSHELPER_PORT`: Port number for the Photoshop COM/OSC bridge.
- `PSHELPER_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR).

## License

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。