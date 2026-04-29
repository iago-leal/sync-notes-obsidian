# Architecture — sync-notes-obsidian

- **Atualizado:** 2026-04-29
- **Repositório:** https://github.com/iago-leal/sync-notes-obsidian
- **Pasta local:** `~/Desktop/jailbreak-kindle/` (nome preservado como evidência narrativa do reenquadramento MDCU — ver README e transcrição)

## Identificação

- **Propósito:** Vault Obsidian é destino único de todas as anotações de livros, vindas de leitor nativo de cada device (macOS, iPad, Boox, Kindle Colorsoft). Cada livro tem versão PDF (canônica, com âncoras de página) e versão EPUB (para leitura confortável no Kindle/Boox-reflow). Anotações vindas do Kindle (em location de EPUB) passam por conversor `loc→page` antes de virarem callout no vault, para que o link de volta sempre aponte para o PDF canônico. Modelo análogo ao Zotero.
- **Responsáveis:** Iago Leal (`iagobernardes13@gmail.com`)
- **Stakeholders:** uso pessoal, único stakeholder
- **Origem:** delimitação do problema via MDCU F2–F5 (ver `transcricao-mdcu-jailbreak-kindle.md`); cinco reenquadramentos sucessivos da demanda aparente "jailbreak Kindle" até cristalizar a demanda real.

## Stack

- **Linguagem:** Python 3.12+
- **Runtime:** CPython 3.12 (alvo macOS Apple Silicon; CLI portável a Linux)
- **Framework:** nenhum — CLI pura
- **Banco de dados:** nenhum — estado em arquivos (Markdown no vault + arquivos de log)
- **Infra:** macOS local + Syncthing (biblioteca de PDFs/EPUBs) + Obsidian Sync (vault) + Send-to-Kindle (transporte para Kindle Colorsoft)

## Dependências

- **Gerenciador:** `uv` (Astral)
- **Manifesto:** `pyproject.toml`
- **Lock file:** `uv.lock` — **COMMITADO** (regra canônica vinculante; nunca `.gitignore`-ado)
- **Política de versão:** `^` no manifesto (expressão de intenção), versão exata no lock (fato executável)
- **Auditoria:** `pip-audit` no CI a cada PR
- **Upgrades:** manuais via `uv lock --upgrade-package <X>`, com review humano. Sem Dependabot/Renovate por enquanto (projeto pequeno, baixa urgência).

### Bibliotecas principais

| Lib | Papel | Por quê |
|---|---|---|
| `pdfplumber` | Extração de texto + coordenadas de PDFs | Mais maduro do ecossistema Python para extrair texto preservando layout; expõe coords para futuras extensões |
| `rapidfuzz` | Fuzzy text matching | Implementação rápida (Cython) de Levenshtein/ratio; usado no conversor `loc→page` |
| `ebooklib` | Parsing de EPUB | Necessário para mapping inverso location→texto quando My Clippings traz só location, sem snippet |
| `pytest` | Testes | Padrão da comunidade Python |
| `ruff` | Lint + format | Substitui flake8 + black + isort; mais rápido, configuração unificada |
| `mypy` | Type checking | `--strict` é guardrail (ver Guardrails) |

### Componentes externos (pré-existentes, parte do pipeline)

Estes não são código deste projeto, mas são parte da arquitetura operacional:

- `obsidian-pdf-plus` (plugin Obsidian) — captura macOS/iPad
- `obsidian-kindle-plugin` (`hadynz/obsidian-kindle-plugin`) — captura Kindle (parsing My Clippings)
- KOReader Android com plugin `evernote_export` ou `markdown_export` — captura Boox
- Syncthing — sync da biblioteca
- Obsidian Sync — sync do vault

## Estrutura de diretórios

```
sync-notes-obsidian/
├── README.md
├── ARCHITECTURE.md                      ← este arquivo
├── pyproject.toml
├── uv.lock                              ← COMMITADO
├── .gitignore
├── .github/
│   └── workflows/                       ← Claude Code workflows (PR Assistant + Review)
├── src/
│   └── synctotes/
│       ├── __init__.py
│       ├── cli.py                       ← entry point (Click ou Typer)
│       ├── kindle.py                    ← parser My Clippings + conversor loc→page
│       ├── boox.py                      ← ingest de export KOReader
│       ├── obsidian.py                  ← writer de callouts no vault
│       ├── pdf.py                       ← extração de texto via pdfplumber
│       └── types.py                     ← MatchResult, Candidate, etc.
├── tests/
│   ├── fixtures/                        ← samples de My Clippings, PDFs, EPUBs
│   ├── test_kindle.py
│   ├── test_pdf.py
│   ├── test_obsidian.py
│   └── test_boox.py
├── docs/
│   └── adr/                             ← Architecture Decision Records
└── _mdcu.md                             ← TRANSITÓRIO — vivo durante sessão MDCU; deletado ao /mdcu fechar
```

## Convenções

- **Lint + format:** `ruff` (regras: estilo PEP-8 + isort + bugbear + comprehensions; line length 100)
- **Type checking:** `mypy --strict` em `src/`. Anotações de tipo obrigatórias em todas as funções públicas.
- **Naming:** `snake_case` para funções/variáveis, `PascalCase` para classes, `SCREAMING_SNAKE_CASE` para constantes (Python idiomático)
- **Branches:** trunk-based, PRs curtos
- **Commits:**
  - Marcos longitudinais (fim de feature, fechamento de sessão MDCU, mudança em `ARCHITECTURE.md`) → skill `commit-soap` (formato A+P)
  - WIPs intermediários → `git commit` padrão
  - **NUNCA** trailer `Co-Authored-By: Claude` (regra global do usuário)
- **Idioma:** Português para mensagens de commit, comentários, READMEs internos. Código (identificadores, docstrings) em inglês — convenção de comunidade Python.

## Comandos principais

| Alias | Comando real |
|---|---|
| `install` | `uv sync` |
| `dev` | `uv run synctotes --help` |
| `test` | `uv run pytest` |
| `lint` | `uv run ruff check` |
| `format` | `uv run ruff format` |
| `typecheck` | `uv run mypy src/` |
| `audit` | `uv run pip-audit` |

Estes são contrato. Em F6 do MDCU, o agente usa estes — não inventa variantes (`pip install`, `python -m pytest`, etc.).

## Guardrails (invariantes — não mudar sem `/project-init --refresh`)

1. **Interface tipada do conversor `loc→page`.** A função pública retorna `MatchResult` (status: `found` | `ambiguous` | `no_match`; mais `page`, `confidence`, `candidates`) **desde a primeira linha de código**. Refatorar essa interface depois é débito caro porque toca todos os call sites. Esta interface é o ponto de extensão para LLM-fallback via decorator pattern (ver ADR-002).

2. **PDF é formato canônico no vault.** Links de callouts SEMPRE apontam para PDF (`[[livro.pdf#page=X]]`), nunca para EPUB. Se o usuário não tem PDF de um livro, a anotação fica como callout de texto simples com referência textual (sem link clicável), com warning no log.

3. **EPUB é variante de transporte, fora do vault.** EPUB existe para o Kindle/Boox lerem confortavelmente. Não vai para o vault. Não tem callout apontando para `.epub#loc=X` (location não é estável entre leitores).

4. **Lock file (`uv.lock`) sempre commitado.** Nunca em `.gitignore`. Toda alteração de dependência é commit de duas partes (manifesto + lock).

5. **Sem LLM no MVP.** LLM-fallback é decisão deliberada para v2, ativada só quando dor real for medida (frequência de status `ambiguous` ou `no_match` for incômoda no uso real). Adicionar antes é over-engineering. Ver ADR-002.

6. **Idempotência das anotações no vault.** Re-rodar o pipeline sobre o mesmo `My Clippings.txt` (ou export do Boox) **não duplica callouts**. Identidade do highlight = hash estável de (livro, snippet normalizado). Re-execução é segura.

7. **Sem modificação de PDFs originais.** O projeto NÃO escreve no PDF — segue o modelo Zotero/`obsidian-pdf-plus`: anotações vivem no vault, PDF fica intocado. (Mesmo se quisermos no futuro, viola o modelo declarado em F4.)

8. **Sem dependência de serviços de rede em runtime.** Nada de chamadas a APIs externas no pipeline. Tudo local. (Apenas o instalador de dependências usa rede.)

## Escopo

### Faz

- Pipeline Python que ingere highlights de Kindle (`My Clippings.txt`) e exports de KOReader/Boox.
- Conversor determinístico `loc EPUB → page PDF` via fuzzy text-search.
- Geração de callouts Obsidian no vault, com link de página para o PDF canônico.
- CLI manual (`synctotes ingest ...`).
- Idempotência via hash de highlight.

### NÃO faz

- Leitor de ebook próprio.
- Modificação de PDF original.
- Jailbreak de Kindle ou qualquer modificação de firmware.
- Sync de progresso de leitura entre devices (Whispersync nativo da Amazon já cobre para livros Amazon; não é problema deste projeto).
- Cobertura de livros DRM Amazon que não foram convertidos para PDF.
- Plugin Obsidian custom (decisão F5: deixado como ponto de extensão para v2).
- Daemon/watcher automático (decisão F5: manual no MVP).
- LLM-fallback no MVP (decisão F5: ponto de extensão preservado, não implementado).

## ADRs relacionados

A serem criados em `docs/adr/` após `project-setup` materializar a estrutura:

- **ADR-001** — Python 3.12+ com `uv` como stack
- **ADR-002** — Conversor determinístico-first com `MatchResult` tipado; LLM-fallback como ponto de extensão (decorator pattern)
- **ADR-003** — Syncthing para biblioteca; Obsidian Sync para vault
- **ADR-004** — PDF como formato canônico do vault; EPUB como variante de transporte

## Histórico

- **2026-04-29:** Sessão MDCU inaugural. Demanda aparente "jailbreak-kindle" reenquadrada cinco vezes até cristalizar a demanda real. F2–F5 do MDCU produziram este contrato sem nenhuma linha de código escrita. Próximo passo: `/project-setup` materializa stack.
