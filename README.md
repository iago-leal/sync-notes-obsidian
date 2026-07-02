# sync-notes-obsidian

> **Vault Obsidian é destino único de todas as anotações de livros, vindas do leitor nativo de cada device. Cada livro tem versão PDF (canônica, com âncoras de página) e versão EPUB (para leitura confortável no Kindle/Boox-reflow). Anotações vindas do Kindle (em location de EPUB) passam por um conversor `loc → page` antes de virarem callout no vault, para que o link de volta sempre aponte para o PDF canônico.**

Modelo análogo ao Zotero, generalizado para múltiplos devices (macOS, iPad, Boox, Kindle Colorsoft) com leitores nativos em cada um. O pacote Python que implementa o pipeline chama-se **`synctotes`**.

---

## Status

- **Contrato técnico:** fechado — ver [`ARCHITECTURE.md`](./ARCHITECTURE.md) (stack, guardrails, comandos canônicos) e os ADRs em [`docs/adr/`](./docs/adr/).
- **Implementado:** `pdf.extract_pages` (extração paginada via pdfplumber), `kindle.parse_clippings` (parser do My Clippings), `amazon_export` (parser do PDF "Caderno de anotações" exportado pela Amazon), tipos de domínio (`MatchResult` etc.) — tudo com testes.
- **Pendente:** conversor `loc → page` (coração do pipeline), writer de callouts no vault (`obsidian.py`), ingest do Boox (`boox.py`) e a CLI real (`cli.py` é stub verificado end-to-end).

## Como rodar

Gerenciador de dependências: [`uv`](https://github.com/astral-sh/uv). Os comandos abaixo são o contrato declarado no `ARCHITECTURE.md`.

```bash
uv sync                        # instala dependências (lock determinístico)
uv run pre-commit install      # guardrail local: ruff + mypy antes de cada commit
uv run synctotes --help        # CLI (ainda stub)
uv run pytest --cov=synctotes  # testes com cobertura
```

## Estrutura

```
.
├── README.md
├── ARCHITECTURE.md            ← contrato técnico (stack, guardrails, comandos)
├── pyproject.toml / uv.lock   ← manifesto + lock COMMITADO
├── src/synctotes/             ← pacote: pdf, kindle, amazon_export, obsidian, boox, types, cli
├── tests/                     ← pytest; fixtures em tests/fixtures/ (fair use; livros completos em local/, fora do repo)
├── docs/
│   ├── adr/                   ← ADR-001…006 (decisões arquiteturais)
│   └── transcricao-mdcu-jailbreak-kindle.md  ← transcrição da sessão de delimitação
├── rsop/                      ← registro de saúde orientado por problemas do projeto (framework MDCU)
└── traceability/              ← matrizes de rastreabilidade spec ↔ código
```

---

## Por que esta pasta ainda se chama `jailbreak-kindle` localmente

Esse mismatch é proposital: é **evidência narrativa do reenquadramento** que delimitou este projeto.

A sessão começou com a hipótese de que o problema fosse "jailbreak do Kindle" (escrever software custom para liberar o device). Ao longo de cinco rodadas de escuta MCCP/MDCU, a demanda aparente foi sendo reenquadrada até a demanda real emergir: o problema nunca foi jailbreak — foi **personal knowledge management com sync dual-format de anotações em ecossistema multi-device**, no modelo Zotero.

A pasta local guarda o nome inicial como cicatriz didática. O repositório no GitHub nasceu com o nome cristalizado.

| Camada                 | Nome                                          |
| ---------------------- | --------------------------------------------- |
| Pasta local (`~/dev/`) | `jailbreak-kindle` (nome da demanda aparente) |
| Repositório GitHub     | `sync-notes-obsidian` (nome da demanda real)  |

## Sobre o processo

Este projeto foi delimitado usando o framework [**MDCU — Método de Desenvolvimento Centrado no Usuário**](https://github.com/iago-leal/skills/tree/main/mdcu-framework), de autoria de [@iago-leal](https://github.com/iago-leal). O MDCU é uma transposição do **MCCP (Método Clínico Centrado na Pessoa)** — usado em Medicina de Família e Comunidade — para o domínio de Engenharia de Software.

A premissa central: o **especialista na experiência do problema é o usuário**, não o engenheiro. O agente IA é o operador clínico que extrai o problema com escuta estruturada, separa demanda aparente de demanda real, traduz complexidade técnica em decisão informada, e exerce dever de alerta sobre escolhas que comprometem bem-estar de longo prazo.

A [**transcrição literal da sessão de delimitação**](./docs/transcricao-mdcu-jailbreak-kindle.md) está neste repositório como evidência pedagógica do processo. Nela é possível observar:

1. Cinco reenquadramentos sucessivos da demanda apresentada.
2. Recusa do agente de aceitar a demanda inicial sem escuta.
3. Apresentação de trade-offs em pontos críticos (K1/K2/K3 sobre o papel do Kindle no workflow).
4. Bloqueios solicitados pelo usuário ("ainda não vamos passar para a próxima") sendo respeitados.
5. Cristalização do problema em F4 antes de qualquer linha de código ser escrita.

A mesma transcrição vive no [repositório do framework MDCU](https://github.com/iago-leal/skills/tree/main/mdcu-framework) como caso de estudo.

## Notas técnicas de projeto

Pontos de design estabelecidos na delimitação, hoje formalizados nos ADRs:

- **PDF é formato canônico** no vault (page-number estável). EPUB é variante de transporte para Kindle/Boox-reflow (ADR-004).
- **Conversor `loc EPUB → page PDF`** é o componente novo a construir, e é o coração do pipeline do Kindle. Caminho determinístico-first (fuzzy text-search no PDF extraído), com LLM-fallback como ponto de extensão para v2 (ADR-002).
- **Jailbreak do Kindle Colorsoft (firmware 5.19.2) está bloqueado por firmware** desde abril de 2026 e não é parte do escopo. Kindle entra como cidadão "1.5ª classe": lê PDFs vindos dos outros devices e suas anotações chegam ao vault via My Clippings ou export da Amazon.
- `obsidian-pdf-plus` (macOS/iPad) e `obsidian-kindle-plugin` (Kindle) são componentes existentes do pipeline; Boox depende de KOReader Android com export para markdown (ver ARCHITECTURE.md, "Componentes externos").
- Readwise é componente possível mas insuficiente: não cobre Boox, e o link de volta dele aponta para `read.amazon.com`, não para arquivo no vault.
