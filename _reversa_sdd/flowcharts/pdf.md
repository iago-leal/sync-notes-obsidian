# Fluxograma — módulo `pdf`

> `extract_pages`. Gerado pelo Reversa Archaeologist em 2026-07-02.

```mermaid
flowchart TD
    A[extract_pages path] --> B[Path path]
    B --> C[pdfplumber.open]
    C --> D{Para cada página, index 1-based}
    D --> E[page.extract_text]
    E --> F{Texto None?}
    F -- sim --> G[pages index = string vazia]
    F -- não --> H[pages index = texto]
    G --> D
    H --> D
    D -- fim --> I[Retorna dict denso 1-indexado]
```

## Notas

- 1-indexado por convenção humana e pelo formato de link `[[livro.pdf#page=X]]`.
- Mapeamento denso: toda página de 1 a N presente, vazia = `""`.
- Exceções do pdfplumber propagam sem captura (erros barulhentos).
