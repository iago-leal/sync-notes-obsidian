# ERD — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Architect em 2026-07-02.
> Não há banco de dados 🟢: as "entidades" são dataclasses imutáveis em memória; relacionamentos por composição, sem chaves persistidas. Cardinalidades refletem a estrutura dos objetos.

```mermaid
erDiagram
    KINDLE_BOOK ||--o{ KINDLE_CLIPPING : "identifica"
    AMAZON_BOOK ||--|| EXPORTED_NOTEBOOK : "descreve"
    EXPORTED_NOTEBOOK ||--o{ AMAZON_ANNOTATION : "contém"
    CLIPPING_TYPE ||--o{ KINDLE_CLIPPING : "classifica"
    CLIPPING_TYPE ||--o{ AMAZON_ANNOTATION : "classifica"
    MATCH_RESULT ||--o{ CANDIDATE : "lista quando ambiguous"

    KINDLE_BOOK {
        str title "obrigatório"
        str author "opcional"
    }
    KINDLE_CLIPPING {
        ClippingType kind
        int location_start "opcional"
        int location_end "opcional"
        int page "opcional; precedência sobre location"
        datetime added_at "opcional, naive"
        str text "vazio em bookmark"
    }
    AMAZON_BOOK {
        str title
        str author "opcional"
        str asin "opcional, 10 chars"
    }
    EXPORTED_NOTEBOOK {
        int summary_total "reconciliação com contagem Amazon"
    }
    AMAZON_ANNOTATION {
        ClippingType kind
        str color "opcional"
        str coordinate_kind "page | position"
        int coordinate_value "> 0"
        bool is_continuation
        str text
        str note "opcional, multilinha"
        date date_added "opcional"
    }
    CLIPPING_TYPE {
        str value "highlight | note | bookmark"
    }
    MATCH_RESULT {
        str status "found | ambiguous | no_match"
        int page "só em found"
        float confidence "só em found"
    }
    CANDIDATE {
        int page "1-indexado"
        float score
        str excerpt
    }
```

## Relações entre agregados 🟡

`KindleClipping` e `AmazonAnnotation` descrevem o **mesmo fato de domínio** (uma anotação de leitura) vindo de fontes diferentes, mas **não há hoje modelo unificado** que os reconcilie — nem chave natural conectando `KindleBook.title` a `AmazonBook.title/asin`. Essa unificação (🔴 LACUNA 7 do domain.md) será forçada quando resolver e writer existirem, pois o callout precisa de identidade única de livro e de highlight (hash de idempotência do guardrail #6).

## Persistência

| Aspecto | Situação |
|---|---|
| Banco de dados | inexistente por decisão 🟢 |
| Estado durável | o próprio vault (Markdown) 🟢 |
| Identidade de highlight | hash estável de (livro, snippet normalizado) 🔴 algoritmo não definido |
