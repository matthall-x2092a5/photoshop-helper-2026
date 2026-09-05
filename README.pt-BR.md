🌍 [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md)

# photoshop-helper-2026

Uma biblioteca de utilitários moderna e de alto desempenho em Python, projetada para otimizar fluxos de trabalho do Adobe Photoshop por meio de automação por scripts, processamento em lote e gerenciamento de ativos.

## Descrição

`photoshop-helper-2026` preenche a lacuna entre as capacidades de processamento de dados do Python e o poder criativo do Adobe Photoshop. Ele fornece uma API robusta para executar comandos ExtendScript (JSX), gerenciar estados de documentos e automatizar tarefas de design repetitivas. Construída para eficiência, ela suporta tanto a execução local quanto o processamento em lote remoto, tornando-a ideal para desenvolvedores que integram ferramentas de design em pipelines de produção maiores.

## Funcionalidades

- **Motor de Execução de Scripts**: Execute arquivos personalizados de ExtendScript ou JSX a partir do Python com tratamento completo de erros.
- **Gerenciamento de Documentos**: Abra, salve, feche e duplique arquivos PSD programaticamente, com suporte para controle de versão.
- **Processamento em Lote**: Processe centenas de ativos simultaneamente com enfileiramento configurável e lógica de nova tentativa.
- **Extração de Metadados de Ativos**: Leia e escreva metadados XMP, informações de camadas e propriedades de imagem.
- **Integração de Plugins**: Carregue e gerencie plugins de terceiros do Photoshop dinamicamente.
- **Log e Depuração**: Sistema de log abrangente para rastrear a execução de scripts, erros e métricas de desempenho.
- **Suporte Assíncrono**: Operações não bloqueantes para processamento de documentos concorrentes, onde suportado pelo ambiente.

## Instalação

Certifique-se de ter o Python 3.8+ instalado. Você pode instalar o pacote usando o `pip`:

```bash
pip install photoshop-helper-2026
```

Se você estiver trabalhando em um ambiente virtual, ative-o antes de instalar:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install photoshop-helper-2026
```

## Exemplo de Uso

O exemplo a seguir demonstra como abrir um documento do Photoshop, aplicar um filtro básico e salvar o resultado usando `photoshop-helper-2026`.

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

## Configuração

`photoshop-helper-2026` suporta configuração por meio de um arquivo `config.yaml` ou variáveis de ambiente. Abaixo está um exemplo de `config.yaml`:

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

Você também pode sobrescrever configurações específicas por meio de variáveis de ambiente:

- `PSHELPER_PHOTOSHOP_PATH`: Caminho para o executável do Photoshop.
- `PSHELPER_PORT`: Número da porta para a ponte COM/OSC do Photoshop.
- `PSHELPER_LOG_LEVEL`: Nível de log (DEBUG, INFO, WARNING, ERROR).

## Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.