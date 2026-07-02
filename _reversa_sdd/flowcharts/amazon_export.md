# Fluxograma — módulo `amazon_export`

> `parse_export_pdf` e máquina de estados `_parse_annotations`. Gerado pelo Reversa Archaeologist em 2026-07-02.

## Fluxo principal

```mermaid
flowchart TD
    A[parse_export_pdf path] --> B[_extract_full_text via pdfplumber]
    B --> C[Divide em linhas]
    C --> D[_parse_header]
    D --> E[1a linha não-vazia = título]
    E --> F[Linha 'por X' = autor]
    F --> G[Regex asin= = ASIN]
    G --> H[Regex 'Anotações N' = total]
    H --> I[Avança até 1a linha de metadata]
    I --> J[_parse_annotations nas linhas restantes]
    J --> K[ExportedNotebook book, annotations, summary_total]
```

## Máquina de estados `_parse_annotations`

```mermaid
flowchart TD
    A{Para cada linha não-vazia} --> B{Só dígitos ou numeral romano?}
    B -- sim --> A
    B -- não --> C{Match metadata 'Página/Posição N pipe Tipo'?}
    C -- sim --> D[flush anotação corrente]
    D --> E{Tipo reconhecido?}
    E -- não --> A
    E -- sim --> F[Define kind, color, coordinate_kind, coordinate_value, is_continuation]
    F --> A
    C -- não --> G{Existe anotação aberta?}
    G -- não --> A
    G -- sim --> H{Linha 'Nota: ...'?}
    H -- sim --> I[Abre bloco de nota; note_text = conteúdo]
    I --> A
    H -- não --> J{Linha de data 'D de mês de AAAA'?}
    J -- sim --> K{Fora de bloco de nota e date_added vazio?}
    K -- sim --> L[date_added = data]
    K -- não --> A
    L --> A
    J -- não --> M{Em bloco de nota?}
    M -- sim --> N[Concatena na nota]
    M -- não --> O[Acumula em text_lines]
    N --> A
    O --> A
    A -- fim das linhas --> P[flush final]
    P --> Q[Retorna lista; descarta anotação sem tipo+coordenada completos]
```

## Notas

- Mapeamento de tipo: `Continuação do destaque` → HIGHLIGHT com `is_continuation=True`; `Destaque` → HIGHLIGHT; `Marcador` → BOOKMARK; `Nota` → NOTE.
- Reconciliação com o sumário Amazon: `itens_sem_continuação + notas_anexadas == summary_total` (semântica invertida em relação à contagem da Amazon — documentada em `test_total_annotations_match_summary`).
- Linhas só-dígitos e romanos são ruído estrutural do próprio PDF (paginação e frontmatter).
