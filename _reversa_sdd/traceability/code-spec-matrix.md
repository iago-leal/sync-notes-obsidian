# Code/Spec Matrix — jailbreak-kindle (`synctotes`)

> Reversa Writer, 2026-07-02. Complementa a matriz canônica do repo (`traceability/code-spec-matrix.md` na raiz, ADR-006), mapeando **arquivo do legado → unit de spec do Reversa**.

| Arquivo do legado | Unit correspondente | Cobertura |
|---|---|---|
| `src/synctotes/kindle.py` | `kindle/` | 🟢 |
| `src/synctotes/amazon_export.py` | `amazon_export/` | 🟢 |
| `src/synctotes/pdf.py` | `pdf/` | 🟢 |
| `src/synctotes/types.py` | `types/` | 🟢 |
| `src/synctotes/cli.py` | `cli/` | 🟢 (stub; spec de alvo 🟡) |
| `src/synctotes/obsidian.py` | `obsidian/` | 🟢 (stub; spec de alvo 🟡) |
| `src/synctotes/boox.py` | `boox/` | 🟢 (stub; spec de alvo 🔴) |
| `src/synctotes/__init__.py` | transversal (versão) | 🟢 via inventory.md |
| `tests/test_kindle.py` | `kindle/` | 🟢 |
| `tests/test_amazon_export.py` | `amazon_export/` | 🟢 |
| `tests/test_pdf.py` | `pdf/` | 🟢 |
| `tests/test_smoke.py` | `types/` + `cli/` | 🟢 |
| `tests/conftest.py` | `kindle/`, `amazon_export/`, `pdf/` | 🟢 |
| `tests/fixtures/machado-quincas-borba/*` | `amazon_export/`, `pdf/` | 🟢 |
| `pyproject.toml`, `uv.lock` | transversal | 🟢 dependencies.md |
| `ARCHITECTURE.md` | transversal | 🟢 domain.md (guardrails), architecture.md |
| `docs/adr/ADR-001..006` | transversal | 🟢 adrs/000-indice.md |
| `docs/transcricao-mdcu-jailbreak-kindle.md` | transversal | 🟡 citada no domain.md (não analisada na íntegra) |
| `rsop/*` | transversal | 🟡 prontuário MDCU, citado no domain.md |
| `traceability/*` (raiz do repo) | transversal | 🟢 espelhada/complementada em `_reversa_sdd/traceability/` |
| `.github/workflows/*.yml` | transversal | 🟢 inventory.md (dívida #1) |
| `.pre-commit-config.yaml` | transversal | 🟢 inventory.md |
| `README.md`, `CLAUDE.md`, `AGENTS.md`, `LICENSE` | n/a (meta) | n/a |

## Cobertura

- **Código-fonte**: 8/8 arquivos do pacote mapeados a units (100%).
- **Testes e fixtures**: 100% mapeados.
- **Documentação de governança**: coberta pelos artefatos transversais.
- Nenhum arquivo `n/a` inesperado — os `n/a` são meta-arquivos sem comportamento.
