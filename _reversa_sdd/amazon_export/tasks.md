# Tasks — unit `amazon_export` (reimplementação fiel)

> Reversa Writer, 2026-07-02.

| # | Task | Fonte | Critério de pronto | Confiança |
|---|---|---|---|---|
| 1 | Definir `AmazonBook`, `AmazonAnnotation`, `ExportedNotebook` frozen + alias `CoordinateKind` | `amazon_export.py:29-61` | campos idênticos ao dicionário de dados | 🟢 |
| 2 | Implementar `_extract_full_text` (pdfplumber, join por `\n`) | `amazon_export.py:126-131` | páginas vazias viram `""` | 🟢 |
| 3 | Implementar as 8 regexes literais do design | `amazon_export.py:64-80` | idênticas byte a byte | 🟢 |
| 4 | Implementar `_parse_header` posicional com os dois fallbacks | `amazon_export.py:134-167` | header do fixture real extraído corretamente | 🟢 |
| 5 | Implementar máquina de estados `_parse_annotations` com `flush()` e a ordem exata de avaliação | `amazon_export.py:170-283` | 61 anotações reconciliadas no fixture | 🟢 |
| 6 | Implementar tabela `_MONTHS_PT` (abreviados + extensos) | `amazon_export.py:82-107` | datas `1 de abr. de 2026` parseadas | 🟢 |
| 7 | Portar suíte de 8 testes contra o fixture real | `tests/test_amazon_export.py` | 100% verde | 🟢 |
| 8 | Adicionar suporte EN quando houver fixture real | docstring linha 14 | fixture EN commitada + testes | 🔴 |
