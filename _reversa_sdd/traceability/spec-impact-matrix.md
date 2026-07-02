# Spec Impact Matrix — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Architect em 2026-07-02.
> Complementa (não substitui) a matriz canônica do projeto em `traceability/spec-impact-matrix.md` na raiz do repo (ADR-006). Esta versão cobre também os módulos futuros e os artefatos do Reversa.
> Legenda de risco: 🟥 crítico (exige ADR prévio) · 🟧 médio · 🟩 baixo.

## Matriz componente → impacto

| Mudança em ↓ | kindle | amazon_export | pdf | types | cli | obsidian | boox | testes | specs afetadas |
|---|---|---|---|---|---|---|---|---|---|
| **types.MatchResult** 🟥 | resolver | — | — | ● | consome | consome | — | smoke + futuros | ADR-002, guardrail #1 |
| **kindle.parse_clippings** 🟧 | ● | ClippingType | — | — | consome | via pipeline | — | test_kindle | domain.md regras parser |
| **kindle (resolver futuro)** 🟥 | ● | coordenadas | extract_pages | MatchResult | consome | alimenta | alimenta | novos | ADR-002, lacuna 3 |
| **amazon_export** 🟧 | ClippingType compartilhado | ● | — | — | consome | via pipeline | — | test_amazon_export + fixture real | ADR-007 retroativo |
| **pdf.extract_pages** 🟧 | resolver futuro | 🟡 duplicação | ● | — | — | — | — | test_pdf | convenção 1-indexada (links) |
| **obsidian (writer)** 🟥 | — | — | — | consome | consome | ● | — | inexistentes 🔴 | guardrails #2 #6 #12 #14 #15 |
| **cli** 🟧 | orquestra | orquestra | — | — | ● | orquestra | orquestra | test_smoke | guardrails #9 #10 #13 #14 |
| **boox** 🟩 | — | — | — | — | consome | via pipeline | ● | inexistentes 🔴 | lacuna 4 |
| **pyproject/uv.lock** 🟧 | todos | todos | todos | — | todos | todos | todos | todos | ADR-001, guardrail #4 |
| **ARCHITECTURE.md (guardrails)** 🟥 | contratos | contratos | convenções | contrato | contratos | contratos | contratos | expectativas | tudo |

● = o próprio componente.

## Células críticas 🟥 (Gate de Blast Radius, ADR-006)

1. **`types.MatchResult`** — interface pública do resolver; toca todo consumidor futuro. Mudança exige ADR.
2. **Resolver `loc→page`** — coração do valor de negócio; quando nascer, herda criticidade máxima.
3. **`obsidian.py` (append-only)** — única escrita no vault; erro aqui corrompe o destino único das anotações.
4. **Guardrails do ARCHITECTURE.md** — mudá-los é mudar o contrato do sistema (`/project-init --refresh`).

## Efeitos transversais

- Convenção **1-indexada** de página conecta `pdf.extract_pages` ↔ resolver ↔ formato de link `[[livro.pdf#page=X]]` ↔ obsidian-pdf-plus: quebra silenciosa se qualquer elo mudar a base 🟧.
- `ClippingType` é compartilhado entre os dois parsers: renomear valores quebra `amazon_export` e consumidores do vault 🟧.
- A fixture real (`amazon_export.pdf`) é contrato de regressão externo: mudança de layout da Amazon aparece como falha de teste, não como bug de produção 🟩 (desejável).
