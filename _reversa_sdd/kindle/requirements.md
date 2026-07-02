# Requirements — unit `kindle`

> Reversa Writer, 2026-07-02 · Fonte: `src/synctotes/kindle.py`, `tests/test_kindle.py` · 🟢/🟡/🔴

## Objetivo

Converter o conteúdo bruto de um `My Clippings.txt` de Kindle em objetos `KindleClipping` estruturados e imutáveis, tolerando os locales PT-BR e EN e as variações históricas do formato 🟢.

## Requisitos funcionais

| ID | Requisito | MoSCoW | Confiança |
|---|---|---|---|
| RF-01 | Dividir o arquivo em blocos pelo separador `==========` e parsear cada bloco independentemente | Must | 🟢 |
| RF-02 | Remover BOM UTF-8 inicial e normalizar CRLF/CR para LF antes do parse | Must | 🟢 |
| RF-03 | Extrair título e autor da 1ª linha (`Título (Autor)`); sem parêntese, autor = `None` | Must | 🟢 |
| RF-04 | Reconhecer tipo do clipping por keyword case-insensitive: destaque/highlight, nota/note, marcador/bookmark | Must | 🟢 |
| RF-05 | Extrair coordenada: página (`na página X` / `on page X`) tem precedência sobre posição (`na posição X[-Y]` / `on Location X[-Y]`) | Must | 🟢 |
| RF-06 | Extrair data PT-BR (`1 de junho de 2018 14:30:25`) e EN (`June 3, 2018 9:15:00 AM`, com AM/PM); falha de data é não-fatal (`added_at=None`) | Should | 🟢 |
| RF-07 | Descartar blocos malformados sem interromper o parse dos demais | Must | 🟢 |
| RF-08 | Texto do clipping = linhas a partir da 3ª, sem linhas vazias iniciais; bookmark resulta em texto vazio | Must | 🟢 |
| RF-09 | Resolver `loc→page`: dado snippet+location, retornar `MatchResult` via fuzzy match contra o PDF canônico | Must | 🔴 não implementado (ADR-002; planejado neste módulo) |
| RF-10 | Tolerar formato antigo (tipo e posição em partes separadas) e moderno (combinados) da linha de metadata | Should | 🟢 |

## Requisitos não funcionais

| ID | Requisito | Evidência |
|---|---|---|
| RNF-01 | Pureza: função sem I/O — recebe `str`, retorna dataclasses frozen | 🟢 assinatura |
| RNF-02 | Sem dependências externas (stdlib apenas) | 🟢 imports |
| RNF-03 | Tipagem estrita (mypy `--strict`) | 🟢 pyproject |

## Critérios de aceitação

**Cenário feliz — clipping PT-BR com faixa de posição** 🟢
Dado um bloco com `Dom Casmurro (Machado de Assis)` e `- Seu destaque na posição 1234-1235 | Adicionado: ...`
Quando `parse_clippings` processa o conteúdo
Então retorna 1 clipping com `title="Dom Casmurro"`, `author="Machado de Assis"`, `kind=HIGHLIGHT`, `location_start=1234`, `location_end=1235` e o texto do destaque.

**Cenário feliz — página tem precedência** 🟢
Dado um bloco com `- Seu destaque na página 42 | ...`
Quando parseado
Então `page=42` e `location_start/location_end` são `None`.

**Cenário de falha — bloco malformado** 🟢
Dado conteúdo com um bloco válido, um bloco de linha única sem metadata, e outro válido
Quando parseado
Então retorna exatamente 2 clippings e não levanta exceção.

**Cenário de falha — data ilegível** 🟢
Dado metadata com data fora dos padrões conhecidos
Quando parseado
Então o clipping é retornado com `added_at=None`.

## Dependências

- Consome: nada (stdlib). Consumido por: `amazon_export` (ClippingType), CLI futura 🟢.
- RF-09 consumirá `pdf.extract_pages` + `rapidfuzz` e retornará `types.MatchResult` 🟢 (contrato) 🔴 (implementação).
