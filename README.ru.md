🌍 [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md)

# photoshop-helper-2026

Современная высокопроизводительная утилитарная библиотека на Python, предназначенная для оптимизации рабочих процессов Adobe Photoshop за счёт скриптовой автоматизации, пакетной обработки и управления ресурсами.

## Описание

`photoshop-helper-2026` устраняет разрыв между возможностями Python в области обработки данных и творческим потенциалом Adobe Photoshop. Он предоставляет надёжный API для выполнения команд ExtendScript (JSX), управления состоянием документов и автоматизации рутинных задач по дизайну. Созданный с упором на эффективность, он поддерживает как локальное выполнение, так и удалённую пакетную обработку, что делает его идеальным выбором для разработчиков, интегрирующих инструменты дизайна в более крупные производственные конвейеры.

## Возможности

- **Движок выполнения скриптов**: Бесшовное выполнение пользовательских файлов ExtendScript или JSX из Python с полной обработкой ошибок.
- **Управление документами**: Программное открытие, сохранение, закрытие и дублирование файлов PSD с поддержкой контроля версий.
- **Пакетная обработка**: Одновременная обработка сотен ресурсов с настраиваемой очередью и логикой повторных попыток.
- **Извлечение метаданных ресурсов**: Чтение и запись метаданных XMP, информации о слоях и свойств изображений.
- **Интеграция плагинов**: Динамическая загрузка и управление сторонними плагинами Photoshop.
- **Логирование и отладка**: Комплексная система логирования для отслеживания выполнения скриптов, ошибок и метрик производительности.
- **Поддержка асинхронности**: Непрерывные операции для одновременной обработки документов там, где это поддерживается средой.

## Установка

Убедитесь, что у вас установлен Python 3.8+. Вы можете установить пакет с помощью `pip`:

```bash
pip install photoshop-helper-2026
```

Если вы работаете в виртуальном окружении, активируйте его перед установкой:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install photoshop-helper-2026
```

## Пример использования

Следующий пример демонстрирует, как открыть документ Photoshop, применить базовый фильтр и сохранить результат с помощью `photoshop-helper-2026`.

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

## Конфигурация

`photoshop-helper-2026` поддерживает конфигурацию с помощью файла `config.yaml` или переменных окружения. Ниже приведён пример `config.yaml`:

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

Вы также можете переопределить определённые настройки с помощью переменных окружения:

- `PSHELPER_PHOTOSHOP_PATH`: Путь к исполняемому файлу Photoshop.
- `PSHELPER_PORT`: Номер порта для моста COM/OSC Photoshop.
- `PSHELPER_LOG_LEVEL`: Уровень логирования (DEBUG, INFO, WARNING, ERROR).

## Лицензия

Данный проект распространяется по лицензии MIT. Подробности см. в файле [LICENSE](LICENSE).