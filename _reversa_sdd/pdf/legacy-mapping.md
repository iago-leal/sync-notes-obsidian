# Legacy Mapping — unit `pdf`

| Arquivo | Linhas | Papel |
|---|---|---|
| `src/synctotes/pdf.py` | 1-27 | `extract_pages`: dict denso 1-indexado página → texto |
| `tests/test_pdf.py` | 1-26 | 3 casos (1-indexação, texto por página, aceita str) |
| `tests/conftest.py` | 12-29 | Fixture de PDF sintético de 3 páginas (fpdf2) |
| `tests/fixtures/machado-quincas-borba/pd.pdf` | — | PDF de domínio público (Biblioteca Nacional) para testes de integração futuros |
