# Design — unit `kindle`

> Reversa Writer, 2026-07-02 · Fluxograma completo em `../flowcharts/kindle.md`.

## Estrutura

Pipeline de funções puras, do bruto ao estruturado 🟢:

```
parse_clippings(content: str) -> list[KindleClipping]
  └─ para cada bloco (split por "=========="):
       _parse_block(block) -> KindleClipping | None
         ├─ _parse_book_line(l0)     -> KindleBook | None
         ├─ _parse_metadata_line(l1) -> (kind, loc_start, loc_end, page, added_at) | None
         │    ├─ _detect_type(parte0)   [obrigatório: None aborta o bloco]
         │    ├─ _parse_position(parte) [página > posição; 1ª ocorrência vence]
         │    └─ _parse_date(parte)     [best-effort, não-fatal]
         └─ texto = linhas 2+ (strip de vazias iniciais)
```

## Decisões de design 🟢

1. **Falha local, nunca global**: cada validação retorna `None` e o bloco é descartado; `parse_clippings` nunca levanta por conteúdo ruim (RF-07). Detecção de defeito por contagem é responsabilidade do chamador (docstring).
2. **Varredura independente das partes** da metadata (split por `|`): cobre formato antigo e moderno sem branch de versão (RF-10).
3. **Tabelas de locale como constantes** (`_TYPE_KEYWORDS`, `_PT_BR_MONTHS`, `_EN_MONTHS`): adicionar locale = adicionar entradas, sem tocar a lógica.
4. **Entidades frozen**: `KindleBook`, `KindleClipping` imutáveis — contrato seguro entre camadas.

## Regras sutis (reimplementação fiel exige)

- Regex do livro `^(.*?)\s*\((.+)\)\s*$`: título = texto antes do **primeiro** parêntese; autor = tudo entre o primeiro `(` e o último `)`. Logo, `Livro (com parênteses) (Autor Real)` → `title='Livro'`, `author='com parênteses) (Autor Real'` — títulos contendo parênteses são divididos errado. 🟢 verificado empiricamente [Reviewer, 2026-07-02]; limitação documentada, preservar regex literal na reimplementação.
- `_parse_position` busca página com `(?:p[áa]gina|page)\s+(\d+)` — aceita acento opcional.
- AM/PM: `PM` soma 12 exceto às 12; `12 AM` → 0 (`kindle.py:250-254`).
- Prefixos de data removidos antes do parse: `Adicionado:`, `Added on`, `Added:`.
- BOM: apenas o primeiro caractere `﻿` é removido.

## Extensão planejada — resolver `loc→page` 🔴

Contrato já fixado (ADR-002, guardrail #1): função pública retorna `types.MatchResult`. Abordagem declarada: fuzzy search do snippet (rapidfuzz) contra `pdf.extract_pages` do PDF canônico. Limiar de score, janela de busca e critério `found` vs `ambiguous` **não definidos** — ver `questions.md`. v2: decorator `LLMFallbackResolver` sobre a mesma interface.
