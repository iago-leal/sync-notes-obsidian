# Legacy Mapping — unit `amazon_export`

| Arquivo | Linhas | Papel |
|---|---|---|
| `src/synctotes/amazon_export.py` | 1-283 | Módulo inteiro: entidades (32-61), regexes/meses (64-107), parser (110-283) |
| `tests/test_amazon_export.py` | 1-103 | 8 casos contra fixture real |
| `tests/conftest.py` | 66-76 | Fixtures dos PDFs Quincas Borba |
| `tests/fixtures/machado-quincas-borba/amazon_export.pdf` | — | Fixture real (ASIN B09JWVC7X8, 61 anotações) — contrato de regressão do layout Amazon |

Funções públicas: `parse_export_pdf` (`amazon_export.py:110`). Entidades: `AmazonBook` (33), `AmazonAnnotation` (42), `ExportedNotebook` (56). Importa `ClippingType` da unit `kindle`.
