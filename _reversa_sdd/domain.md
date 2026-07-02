# Domínio — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Detective em 2026-07-02.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA.

## O problema real (contexto de negócio)

A demanda aparente era "fazer jailbreak no Kindle"; cinco reenquadramentos sucessivos (MDCU F2–F5, documentados em `docs/transcricao-mdcu-jailbreak-kindle.md`) cristalizaram a demanda real 🟢: **o vault Obsidian como destino único de todas as anotações de livros**, vindas do leitor nativo de cada device (macOS, iPad, Boox, Kindle Colorsoft), com link de volta sempre apontando ao PDF canônico. Modelo mental: Zotero generalizado para múltiplos devices.

## Glossário

| Termo | Definição | Confiança |
|---|---|---|
| **PDF canônico** | Versão de referência do livro no vault; numeração de página estável; alvo de todos os links (`[[livro.pdf#page=X]]`) | 🟢 ADR-004 |
| **EPUB de transporte** | Variante reflowável do mesmo livro, fora do vault, só para leitura confortável em Kindle/Boox | 🟢 ADR-004 |
| **Location (posição)** | Coordenada de EPUB no Kindle; **instável** — varia por leitor, fonte e dispositivo (`loc 1432` num Kindle ≠ num Boox) | 🟢 ADR-004 |
| **Clipping** | Unidade do `My Clippings.txt`: highlight, note ou bookmark com livro, coordenada, data e texto | 🟢 `kindle.py` |
| **Caderno de anotações** | PDF que a Amazon envia por e-mail com todas as anotações de um livro; segunda fonte de ingest | 🟢 `amazon_export.py` |
| **Resolver `loc→page`** | Coração do pipeline: converte snippet+location em página do PDF canônico via fuzzy matching (`rapidfuzz` sobre `extract_pages`) | 🟢 ADR-002 (não implementado) |
| **`MatchResult`** | Contrato tipado do resolver: `found` / `ambiguous` / `no_match` | 🟢 `types.py` |
| **Callout** | Bloco Markdown gerado no vault com o highlight e link âncora ao PDF canônico | 🟢 (formato exato 🔴 LACUNA) |
| **Idempotência** | Re-rodar o pipeline não duplica callouts; identidade = hash estável de (livro, snippet normalizado) | 🟢 guardrail #6 |
| **Append-only** | O pipeline só adiciona callouts/cria arquivos no vault; jamais deleta `.md` | 🟢 guardrail #12 |
| **ASIN** | Identificador Amazon da edição comercial (ex.: B09JWVC7X8) | 🟢 `amazon_export.py` |
| **Continuação de destaque** | Highlight que atravessa quebra de página no export Amazon; item próprio com `is_continuation=True` | 🟢 |
| **Coordenada page vs position** | O export Amazon usa páginas quando a edição as expõe; caso contrário, positions — decisão da Amazon por título | 🟢 |

## Regras de domínio

### Invariantes arquiteturais (guardrails do ARCHITECTURE.md) 🟢

1. Interface do resolver retorna `MatchResult` tipado desde a primeira linha (guardrail #1, ADR-002).
2. Links de callouts SEMPRE apontam para o PDF canônico, nunca EPUB (#2, ADR-004).
3. EPUB vive fora do vault (#3).
4. `uv.lock` sempre commitado (#4, ADR-001).
5. **Sem LLM no MVP** — fallback LLM é decisão deliberada para v2, via decorator sobre `MatchResult` (#5, ADR-002).
6. Idempotência por hash de (livro, snippet normalizado) (#6).
7. PDFs originais jamais são modificados (#7).
8. Sem rede em runtime — tudo local (#8).
9. CLI mandatoriamente via Typer, nunca `argparse`/`sys.argv` (#9, ADR-005).
10. Erros e logs ao usuário via `rich` (#10, ADR-005).
11. Nenhum commit com violação de ruff/mypy — pre-commit local (#11).
12. Vault append-only: nunca deletar `.md` (#12).
13. Degradação graciosa no ingest: anotação malformada é logada, pulada, e o processamento continua (#13).
14. `--dry-run` mandatório em toda função que altera o vault (#14).
15. I/O sempre com `encoding="utf-8"` explícito (#15).

### Regras embutidas nos parsers 🟢

- Página tem precedência sobre posição na metadata de um clipping (`kindle.py:205-216`).
- Blocos malformados do My Clippings são descartados em silêncio; a detecção de defeito por contagem fica a cargo do chamador (`kindle.py:98-117`). 🟡 Aparente tensão com o guardrail #13 (que pede log via rich) — o log deverá ser adicionado na camada CLI, não no parser puro.
- Falha de parse de data é não-fatal (`added_at`/`date_added` = `None`).
- Bookmarks têm texto vazio.
- Reconciliação com o sumário Amazon: `itens_sem_continuação + notas_anexadas == summary_total` — o parser inverte deliberadamente a semântica de contagem da Amazon (nota anexada dobra no destaque; continuação vira item próprio).
- Data dentro de bloco de nota não sobrescreve a data do destaque.
- Volume de projeto: ≤1000 highlights/livro, ≤50 livros ativos — performance não é vetor (ADR-001).

### Regras operacionais (fora do código) 🟢

- Biblioteca de PDFs/EPUBs sincroniza via Syncthing; vault via Obsidian Sync; Kindle recebe EPUBs via Send-to-Kindle (ADR-003).
- Alterações em células críticas da `spec-impact-matrix.md` (🟥) exigem ADR prévio — "Gate de Blast Radius" (ADR-006).
- Commits de marco usam o formato A+P (skill `commit-soap`); código em inglês, commits/docs em português.

## Lacunas de domínio 🔴

| # | Lacuna | Onde dói |
|---|---|---|
| 1 | Formato exato do callout Obsidian (template, callout type, metadados) | `obsidian.py` stub |
| 2 | Algoritmo do hash de idempotência (normalização do snippet não definida) | `obsidian.py` stub |
| 3 | Limiar de score do resolver (o que separa `found` de `ambiguous`/`no_match`) | resolver não implementado |
| 4 | Formato de entrada do Boox (evernote_export vs markdown_export do KOReader) | `boox.py` stub |
| 5 | Comandos e assinatura da CLI real (Typer) | `cli.py` stub |
| 6 | Suporte EN no export Amazon (pendente fixture real) | `amazon_export.py:14` |
| 7 | Estratégia quando `coordinate_kind == "page"` do export difere da paginação do PDF canônico (edição comercial ≠ edição de domínio público) | resolver futuro |

## Arqueologia Git (16 commits, 2026-04-29 → 2026-07-02) 🟢

| Marco | Commits | Leitura |
|---|---|---|
| Nascimento metodológico | `7352885` → `15c67e2` → `90afe8f` | Projeto nasceu de workflows GitHub + cristalização MDCU F4/F5: **contrato declarado antes de qualquer código** |
| ADRs formais | `001764a` | ADR-001 a 004 registrados no mesmo dia da primeira implementação |
| Implementação TDD | `164f155`, `8ee7284` | `extract_pages` + `parse_clippings` com TDD; parser Amazon com fixture real no dia seguinte ao contrato |
| Endurecimento | `de058ca`, `1dfbd35`, `2d2d385`, `bbb0175` (2026-05-03) | Typer/rich/pre-commit (ADR-005) + motor de rastreabilidade (ADR-006) |
| Pausa e retomada | gap de 2 meses → `7ea55a6` (2026-07-02) | Reorganização de repo e README honesto ao estado real — padrão de manutenção intermitente 🟡 |

Sem reverts, sem hotfixes, sem refatorações grandes 🟢 — histórico jovem e linear; o conhecimento de negócio está nos documentos, não em cicatrizes de código.
