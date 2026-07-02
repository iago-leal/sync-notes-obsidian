# Dicionário de Dados — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Archaeologist em 2026-07-02.
> Todas as entidades são dataclasses `frozen=True` (imutáveis) 🟢, salvo enums e aliases.

## Enums e aliases

### `ClippingType` — `src/synctotes/kindle.py:27` (StrEnum)

| Valor | Significado |
|---|---|
| `highlight` | Trecho destacado pelo leitor |
| `note` | Nota textual do leitor |
| `bookmark` | Marcador de página/posição (sem texto) |

### `MatchStatus` — `src/synctotes/types.py:26` (Literal)

| Valor | Significado |
|---|---|
| `found` | Match único de alta confiança |
| `ambiguous` | Múltiplos candidatos competindo |
| `no_match` | Nenhum candidato acima do limiar mínimo |

### `CoordinateKind` — `src/synctotes/amazon_export.py:29` (Literal)

| Valor | Significado |
|---|---|
| `page` | Coordenada em página da edição comercial |
| `position` | Coordenada em location Kindle (edição sem páginas expostas) |

## Entidades

### `KindleBook` — `kindle.py:36`

| Campo | Tipo | Obrigatório | Padrão | Observação |
|---|---|---|---|---|
| `title` | `str` | sim | — | Linha 1 do bloco, sem o parêntese final |
| `author` | `str \| None` | não | — | Conteúdo do último parêntese; `None` se ausente |

### `KindleClipping` — `kindle.py:44`

| Campo | Tipo | Obrigatório | Padrão | Observação |
|---|---|---|---|---|
| `book` | `KindleBook` | sim | — | |
| `kind` | `ClippingType` | sim | — | Detectado por keyword PT-BR/EN |
| `location_start` | `int \| None` | não | — | `None` quando a metadata traz página |
| `location_end` | `int \| None` | não | — | `None` em posição única |
| `page` | `int \| None` | não | — | Precedência sobre posição quando presente |
| `added_at` | `datetime \| None` | não | — | Naive; `None` se data ilegível (não-fatal) |
| `text` | `str` | sim | — | `""` para bookmarks |

### `AmazonBook` — `amazon_export.py:33`

| Campo | Tipo | Obrigatório | Padrão | Observação |
|---|---|---|---|---|
| `title` | `str` | sim | — | 1ª linha não-vazia do PDF; `""` se header ilegível |
| `author` | `str \| None` | não | — | Linha `por X` |
| `asin` | `str \| None` | não | — | Regex `asin=([A-Z0-9]{10})` |

### `AmazonAnnotation` — `amazon_export.py:42`

| Campo | Tipo | Obrigatório | Padrão | Observação |
|---|---|---|---|---|
| `kind` | `ClippingType` | sim | — | `Continuação do destaque` → `highlight` |
| `color` | `str \| None` | não | — | Parêntese do tipo: `Amarelo`, `Azul`… |
| `coordinate_kind` | `CoordinateKind` | sim | — | Despacho do resolver depende disto |
| `coordinate_value` | `int` | sim | — | Sempre `> 0` (invariante testada) |
| `is_continuation` | `bool` | sim | `False` | Continuação de destaque da página anterior |
| `text` | `str` | sim | — | Linhas acumuladas fora de bloco de nota |
| `note` | `str \| None` | não | — | Nota anexada (`Nota: ...`), multilinhas |
| `date_added` | `date \| None` | não | — | Ignorada dentro de bloco de nota |

### `ExportedNotebook` — `amazon_export.py:56`

| Campo | Tipo | Obrigatório | Padrão | Observação |
|---|---|---|---|---|
| `book` | `AmazonBook` | sim | — | |
| `annotations` | `tuple[AmazonAnnotation, ...]` | sim | — | Ordem do PDF preservada |
| `summary_total` | `int` | sim | — | Do header `Anotações (N)`; reconciliação: itens sem continuação + notas anexadas == total |

### `Candidate` — `types.py:18`

| Campo | Tipo | Obrigatório | Padrão | Observação |
|---|---|---|---|---|
| `page` | `int` | sim | — | Página candidata (1-indexada) |
| `score` | `float` | sim | — | Score de similaridade fuzzy |
| `excerpt` | `str` | sim | — | Trecho que motivou o match |

### `MatchResult` — `types.py:29`

| Campo | Tipo | Obrigatório | Padrão | Observação |
|---|---|---|---|---|
| `status` | `MatchStatus` | sim | — | Governa a semântica dos demais campos |
| `page` | `int \| None` | não | `None` | Preenchido só em `found` |
| `confidence` | `float \| None` | não | `None` | Preenchido só em `found` |
| `candidates` | `tuple[Candidate, ...]` | não | `()` | Preenchido só em `ambiguous` |

## Estruturas auxiliares (não-entidade)

| Estrutura | Local | Papel |
|---|---|---|
| `dict[int, str]` (retorno de `extract_pages`) | `pdf.py:15` | Página 1-indexada → texto; denso, página vazia = `""` |
| `_TYPE_KEYWORDS` | `kindle.py:58` | Keyword PT-BR/EN → `ClippingType` |
| `_PT_BR_MONTHS` / `_EN_MONTHS` | `kindle.py:67/82` | Nome do mês → número (datas do My Clippings) |
| `_MONTHS_PT` | `amazon_export.py:82` | Meses PT abreviados e por extenso (datas do export) |

## Relacionamentos

```
ExportedNotebook 1 ── 1 AmazonBook
ExportedNotebook 1 ── * AmazonAnnotation
KindleClipping   * ── 1 KindleBook        (por valor, sem chave)
AmazonAnnotation * ── 1 ClippingType      (compartilhado com KindleClipping)
MatchResult      1 ── * Candidate
```

Sem persistência: todos os relacionamentos são por composição em memória 🟢.
