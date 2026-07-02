# Inventário — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Scout em 2026-07-02.
> Confiança: 🟢 CONFIRMADO salvo indicação contrária.

## Identificação

| Campo | Valor |
|---|---|
| Nome do pacote | `synctotes` v0.0.1 |
| Repositório | https://github.com/iago-leal/sync-notes-obsidian |
| Pasta local | `~/dev/jailbreak-kindle/` (nome preservado como evidência narrativa do reenquadramento MDCU) |
| Propósito | Pipeline determinístico para sincronizar anotações de livros (Kindle, Boox, KOReader) ao vault Obsidian via callouts com link âncora ao PDF canônico |
| Status declarado | Development Status :: 1 - Planning (parsers prontos; resolver `loc→page`, writer e CLI real pendentes) |
| Licença | MIT |

## Estrutura de pastas

```
.
├── ARCHITECTURE.md            ← contrato técnico (stack, guardrails, comandos)
├── README.md                  ← visão geral e como rodar
├── pyproject.toml             ← manifesto (hatchling + uv)
├── uv.lock                    ← lock determinístico (commitado, regra canônica)
├── .pre-commit-config.yaml    ← ruff + mypy --strict (exclui .agents/.claude/.reversa)
├── .github/workflows/         ← claude.yml, claude-code-review.yml
├── docs/
│   ├── adr/                   ← 6 ADRs (ADR-001 … ADR-006)
│   └── transcricao-mdcu-jailbreak-kindle.md
├── rsop/                      ← prontuário longitudinal MDCU (dados base, problemas, SOAPs)
├── traceability/              ← code-spec-matrix.md, spec-impact-matrix.md
├── src/synctotes/             ← pacote Python (8 arquivos, ~650 LOC)
│   ├── __init__.py            ← versão do pacote
│   ├── types.py               ← contratos de domínio (MatchResult, Candidate)
│   ├── kindle.py              ← parser My Clippings.txt (PT-BR/EN)
│   ├── amazon_export.py       ← parser do PDF "Caderno de anotações" da Amazon
│   ├── pdf.py                 ← extração paginada de texto via pdfplumber
│   ├── obsidian.py            ← writer de callouts no vault (stub, F6.a)
│   ├── boox.py                ← ingest KOReader/Boox markdown (stub, F6.a)
│   └── cli.py                 ← entry point Typer (stub verificado end-to-end)
└── tests/                     ← pytest (4 suítes + conftest + fixtures)
    └── fixtures/machado-quincas-borba/  ← PDFs reais de teste (domínio público)
```

## Linguagens

| Linguagem | Extensões | Arquivos | Observação |
|---|---|---|---|
| Python | `.py` | 13 | 8 em `src/`, 5 em `tests/` — ~1.018 LOC total |
| Markdown | `.md` | 20 | documentação, ADRs, prontuário rsop, rastreabilidade |
| YAML | `.yml`, `.yaml` | 3 | 2 workflows GitHub + pre-commit |
| TOML | `.toml` | 1 | `pyproject.toml` |

**Linguagem primária:** Python 3.12+ (mypy `--strict`).

## Módulos identificados

| Módulo | LOC | Estado | Responsabilidade |
|---|---|---|---|
| `kindle` | 257 | ✅ implementado + testado | Parser de `My Clippings.txt` (locales PT-BR e EN); futuro lar do resolver `loc→page` |
| `amazon_export` | 283 | ✅ implementado + testado | Parser do PDF de exportação Amazon ("Caderno de anotações"), coordenadas página/posição |
| `pdf` | 27 | ✅ implementado + testado | `extract_pages`: texto por página 1-indexada via pdfplumber |
| `types` | 41 | ✅ implementado | Contratos públicos do resolver: `MatchResult`, `Candidate`, `MatchStatus` (ADR-002) |
| `cli` | 23 | 🟡 stub | Entry point `synctotes` (Typer declarado na stack; hoje imprime aviso e sai 0) |
| `obsidian` | 10 | 🟡 stub | Writer de callouts com link `[[livro.pdf#page=X]]`; idempotência por hash (guardrail #6) |
| `boox` | 6 | 🟡 stub | Ingest de exports markdown do KOReader/Boox |

## Pontos de entrada

| Tipo | Caminho | Detalhe |
|---|---|---|
| CLI (console script) | `src/synctotes/cli.py` | `synctotes = "synctotes.cli:main"` no `pyproject.toml` |

## Configuração

- `pyproject.toml` — manifesto, ruff, mypy strict, pytest
- `.pre-commit-config.yaml` — ruff (`--fix`) + ruff-format + mypy `--strict`
- `.prettierignore` — exclui framework Reversa e artefatos
- Sem `.env` / variáveis de ambiente detectadas 🟢

## CI/CD

| Workflow | Gatilho | Função |
|---|---|---|
| `.github/workflows/claude.yml` | menções `@claude` em issues/PRs | agente Claude sob demanda |
| `.github/workflows/claude-code-review.yml` | PRs (opened/sync/ready/reopened) | code review automático |

🟡 INFERIDO: o `ARCHITECTURE.md` declara `pip-audit` "no CI a cada PR", mas nenhum workflow executa lint/testes/audit — o guardrail vive apenas no pre-commit local. Lacuna entre contrato e CI real.

## Docker / Infra

Sem `Dockerfile` ou `docker-compose.yml`. Infra operacional é externa ao código: Syncthing (biblioteca PDF/EPUB), Obsidian Sync (vault), Send-to-Kindle (transporte) 🟢.

## Banco de dados

Nenhum. Estado em arquivos (Markdown no vault + logs) — decisão registrada no `ARCHITECTURE.md` 🟢.

## Testes

| Item | Valor |
|---|---|
| Framework | pytest 9.0.3 + pytest-cov |
| Suítes | `test_kindle.py` (121 LOC), `test_amazon_export.py` (103), `test_pdf.py` (26), `test_smoke.py` (31) |
| Fixtures | `tests/fixtures/machado-quincas-borba/` (PDFs reais, domínio público); `tests/fixtures/local/` ignorado no git (copyright) |
| Cobertura | 🟡 INFERIDO: módulos implementados cobertos; stubs (`obsidian`, `boox`, `cli`) sem testes de comportamento |

## Documentação e governança

- 6 ADRs em `docs/adr/` (stack uv, MatchResult tipado, Syncthing, PDF canônico, Typer/pre-commit, motor de rastreabilidade)
- `rsop/` — prontuário longitudinal MDCU (SOAPs de sessão)
- `traceability/` — matrizes code↔spec e spec-impact pré-existentes (MDCU)
