# Design — unit `pdf`

> Reversa Writer, 2026-07-02 · Fluxograma em `../flowcharts/pdf.md`.

Função única, wrapper fino sobre pdfplumber 🟢:

```python
def extract_pages(path: Path | str) -> dict[int, str]:
    with pdfplumber.open(Path(path)) as pdf:
        return {i: page.extract_text() or "" for i, page in enumerate(pdf.pages, start=1)}
```

(Implementação real usa loop explícito — semanticamente idêntica.)

## Decisões 🟢

1. **1-indexação** é contrato do sistema inteiro: alinhada ao formato `#page=X` do obsidian-pdf-plus e à convenção humana. Mudar a base quebra silenciosamente todos os links (célula 🟧 da spec-impact-matrix).
2. **Densidade** garante que o resolver possa iterar `range(1, max+1)` sem KeyError.
3. **Única fronteira planejada com pdfplumber** para o resolver — `amazon_export` mantém a própria (`_extract_full_text`, texto corrido) 🟡 candidatas a unificação futura.
