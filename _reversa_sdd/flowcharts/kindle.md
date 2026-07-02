# Fluxograma — módulo `kindle`

> `parse_clippings` e auxiliares. Gerado pelo Reversa Archaeologist em 2026-07-02.

```mermaid
flowchart TD
    A[parse_clippings content] --> B{Começa com BOM?}
    B -- sim --> C[Remove BOM]
    B -- não --> D
    C --> D[Normaliza CRLF/CR para LF]
    D --> E[Divide por '==========']
    E --> F{Para cada bloco não-vazio}
    F --> G[_parse_block]
    G --> H{>= 2 linhas?}
    H -- não --> X[Descarta bloco em silêncio]
    H -- sim --> I[_parse_book_line linha 1]
    I --> J{Linha vazia?}
    J -- sim --> X
    J -- não --> K{Regex 'Título (Autor)'?}
    K -- sim --> L[KindleBook com autor]
    K -- não --> M[KindleBook sem autor]
    L --> N[_parse_metadata_line linha 2]
    M --> N
    N --> O{Prefixo '- '?}
    O -- não --> X
    O -- sim --> P[Divide por pipe]
    P --> Q[_detect_type na parte 0]
    Q --> R{Tipo reconhecido?}
    R -- não --> X
    R -- sim --> S[Varre partes: _parse_position + _parse_date]
    S --> T{Parte menciona página?}
    T -- sim --> U[page = X; posições = None]
    T -- não --> V{Menciona posição X-Y?}
    V -- sim --> W[loc_start=X, loc_end=Y ou None]
    V -- não --> S2[Coordenadas None]
    U --> Y[Texto = linhas 3+ sem vazias iniciais]
    W --> Y
    S2 --> Y
    Y --> Z[KindleClipping frozen]
    Z --> F
    X --> F
    F -- fim --> AA[Retorna list de KindleClipping]
```

## Notas

- Precedência página > posição dentro de cada parte (`kindle.py:208-215`).
- A varredura só preenche coordenadas/data se ainda vazias — primeira ocorrência vence.
- `_parse_date` cobre PT-BR (`1 de junho de 2018 14:30:25`) e EN (`June 3, 2018 9:15:00 AM`, com regra AM/PM); falha de data é não-fatal (`added_at = None`).
