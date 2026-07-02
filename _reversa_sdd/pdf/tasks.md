# Tasks — unit `pdf`

> Reversa Writer, 2026-07-02.

| # | Task | Fonte | Critério de pronto | Confiança |
|---|---|---|---|---|
| 1 | Implementar `extract_pages` com enumerate 1-based e fallback `or ""` | `pdf.py:15-27` | dict denso 1-indexado | 🟢 |
| 2 | Portar 3 testes (1-indexação, texto por página, aceita str) com fixture sintética fpdf2 | `tests/test_pdf.py`, `tests/conftest.py:12-29` | 100% verde | 🟢 |
