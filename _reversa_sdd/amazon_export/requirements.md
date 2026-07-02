# Requirements — unit `amazon_export`

> Reversa Writer, 2026-07-02 · Fonte: `src/synctotes/amazon_export.py`, `tests/test_amazon_export.py` · 🟢/🟡/🔴

## Objetivo

Extrair de um PDF "Caderno de anotações" (export que a Amazon envia por e-mail) o livro, o total declarado e todas as anotações estruturadas, preservando o sistema de coordenadas de cada uma 🟢.

## Requisitos funcionais

| ID | Requisito | MoSCoW | Confiança |
|---|---|---|---|
| RF-01 | Extrair texto integral do PDF (todas as páginas concatenadas) via pdfplumber | Must | 🟢 |
| RF-02 | Parsear header: 1ª linha não-vazia = título; linha `por X` = autor; `asin=XXXXXXXXXX` = ASIN; `Anotações (N)` = total | Must | 🟢 |
| RF-03 | Localizar o início das anotações: primeira linha de metadata após o total | Must | 🟢 |
| RF-04 | Reconhecer metadata `Página\|Posição N \| Tipo (Cor)` e classificar: Destaque→highlight, Marcador→bookmark, Nota→note, Continuação do destaque→highlight com `is_continuation=True` | Must | 🟢 |
| RF-05 | Registrar o sistema de coordenadas (`page`/`position`) de cada anotação | Must | 🟢 |
| RF-06 | Capturar cor do parêntese do tipo (`Amarelo`, `Azul`, ...) | Should | 🟢 |
| RF-07 | Dobrar nota anexada (`Nota: ...`, multilinha) no campo `note` do destaque corrente | Must | 🟢 |
| RF-08 | Capturar data (`1 de abr. de 2026`), ignorando datas dentro de bloco de nota | Should | 🟢 |
| RF-09 | Descartar ruído estrutural: linhas só-dígitos e numerais romanos | Must | 🟢 |
| RF-10 | Descartar anotação incompleta (sem tipo ou coordenada) no flush | Must | 🟢 |
| RF-11 | Suportar export em inglês | Could | 🔴 pendente fixture real (docstring linha 14) |

## Requisitos não funcionais

| ID | Requisito | Evidência |
|---|---|---|
| RNF-01 | Regressão contra layout Amazon garantida por fixture real (Quincas Borba, ASIN B09JWVC7X8, 61 anotações) | 🟢 tests/fixtures |
| RNF-02 | Entidades imutáveis (frozen) | 🟢 |
| RNF-03 | Locale PT-BR com meses abreviados e por extenso | 🟢 `_MONTHS_PT` |

## Critérios de aceitação

**Cenário feliz — header completo** 🟢
Dado o export real de Quincas Borba
Quando `parse_export_pdf` processa o arquivo
Então `title="Quincas Borba"`, `author="Assis, Machado de"`, `asin="B09JWVC7X8"`, `summary_total=61`.

**Cenário feliz — reconciliação de contagem** 🟢
Dado o mesmo export
Quando parseado
Então `itens_com_is_continuation=False` + `itens_com_note≠None` == `summary_total` (semântica invertida em relação à contagem da Amazon, documentada no teste).

**Cenário feliz — nota anexada** 🟢
Dado um destaque na página 29 seguido de `Nota: falsas esperanças...`
Quando parseado
Então o destaque tem `note` preenchido e nenhuma anotação `note` independente é criada para essa linha.

**Cenário de falha — metadata com tipo irreconhecível** 🟢
Dado uma linha `Página 10 | TipoInventado`
Quando parseada
Então a linha é ignorada e o parser continua (sem exceção).

## Dependências

- Consome: `pdfplumber` (direto), `kindle.ClippingType` 🟢.
- Consumido por: CLI futura; resolver futuro despachará por `coordinate_kind` 🟢 (contrato) 🔴 (implementação).
