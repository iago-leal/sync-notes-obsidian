# Requirements — unit `pdf`

> Reversa Writer, 2026-07-02 · Fonte: `src/synctotes/pdf.py`, `tests/test_pdf.py`.

## Objetivo

Fornecer o texto de cada página de um PDF como mapeamento denso 1-indexado, base do fuzzy search do resolver 🟢.

## Requisitos funcionais

| ID | Requisito | MoSCoW | Confiança |
|---|---|---|---|
| RF-01 | `extract_pages(path)` aceita `Path` ou `str` | Must | 🟢 |
| RF-02 | Retornar `dict[int, str]` com chave = página **1-indexada** (convenção do link `[[livro.pdf#page=X]]`) | Must | 🟢 |
| RF-03 | Mapeamento denso: toda página de 1 a N presente; página sem texto = `""` | Must | 🟢 |
| RF-04 | Exceções do pdfplumber propagam sem captura (erros barulhentos) | Should | 🟢 |

## Requisitos não funcionais

| ID | Requisito | Evidência |
|---|---|---|
| RNF-01 | Volume-alvo pequeno (≤50 livros); sem cache nem lazy-loading | 🟢 ADR-001 |

## Critérios de aceitação

**Cenário feliz** 🟢
Dado um PDF de 3 páginas com texto conhecido
Quando `extract_pages` processa
Então retorna dict com chaves {1,2,3} e o texto correto em cada.

**Cenário de falha** 🟡
Dado um path inexistente ou PDF corrompido
Quando `extract_pages` processa
Então a exceção do pdfplumber propaga (não há captura) — comportamento inferido da ausência de try/except.

## Dependências

Consome: `pdfplumber`. Consumido por: resolver futuro (RF-09 da unit kindle) 🟢.
