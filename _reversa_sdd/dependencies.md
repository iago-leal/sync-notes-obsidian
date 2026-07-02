# Dependências — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Scout em 2026-07-02.
> Fontes: `pyproject.toml` (intenção) e `uv.lock` (versão exata instalada). 🟢 CONFIRMADO.

## Gerenciamento

| Item | Valor |
|---|---|
| Gerenciador | `uv` (Astral) |
| Build backend | `hatchling` |
| Lock file | `uv.lock` — commitado (regra canônica do ARCHITECTURE.md) |
| Python | `>=3.12` |
| Auditoria | `pip-audit` (grupo dev) |
| Upgrades | manuais via `uv lock --upgrade-package <X>`, com review humano |

## Runtime

| Pacote | Manifesto | Lock | Papel |
|---|---|---|---|
| `pdfplumber` | `>=0.11` | 0.11.9 | Extração de texto + coordenadas de PDFs (base do resolver `loc→page`) |
| `rapidfuzz` | `>=3.6` | 3.14.5 | Fuzzy matching (Levenshtein/ratio em Cython) para o resolver |
| `ebooklib` | `>=0.18` | 0.20 | Parsing de EPUB (mapping inverso location→texto) |
| `typer` | `>=0.25.1` | 0.25.1 | Framework CLI a partir de type hints |
| `rich` | `>=15.0.0` | 15.0.0 | Logs estruturados e legíveis no terminal |

## Desenvolvimento (`[dependency-groups] dev`)

| Pacote | Manifesto | Lock | Papel |
|---|---|---|---|
| `pytest` | `>=8.0` | 9.0.3 | Testes |
| `pytest-cov` | `>=7.1.0` | 7.1.0 | Cobertura |
| `ruff` | `>=0.5` | 0.15.12 | Lint + format (substitui flake8/black/isort) |
| `mypy` | `>=1.10` | 1.20.2 | Type checking `--strict` (guardrail) |
| `pip-audit` | `>=2.7` | 2.10.0 | Auditoria de vulnerabilidades |
| `fpdf2` | `>=2.7` | 2.8.7 | Geração de PDFs sintéticos para fixtures de teste 🟡 INFERIDO |
| `pre-commit` | `>=4.6.0` | 4.6.0 | Hooks de qualidade antes do commit |

## Componentes externos (fora do código, parte do pipeline operacional)

| Componente | Papel |
|---|---|
| `obsidian-pdf-plus` (plugin Obsidian) | Captura de anotações em macOS/iPad |
| `hadynz/obsidian-kindle-plugin` | Captura Kindle (parsing My Clippings) |
| KOReader Android (`evernote_export`/`markdown_export`) | Captura Boox |
| Syncthing | Sync da biblioteca de PDFs/EPUBs |
| Obsidian Sync | Sync do vault |
| Send-to-Kindle | Transporte de EPUBs ao Kindle Colorsoft |

## Observações de longevidade

- Todas as dependências têm release recente e manutenção ativa 🟢.
- `ebooklib` é a mais lenta em cadência de releases do conjunto; monitorar na revisão trimestral 🟡.
