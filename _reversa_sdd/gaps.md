# Gaps — lacunas remanescentes

> Reversa Reviewer, 2026-07-02 · Lacunas 🔴 sem resposta no momento do fechamento da extração. Espelham o `questions.md`; atualizar ambos quando respondidas.
>
> **2026-07-02 — Resolução em bloco.** Todas as lacunas G1–G12 receberam decisão registrada (aprovação em bloco das 22 respostas do `questions.md`). As tabelas abaixo permanecem como registro histórico, com o status atualizado. As decisões só viram código no ciclo forward; até lá são contratos, não implementação.

## Críticas (bloqueavam a implementação do coração do sistema)

| # | Lacuna | Unit | Pergunta | Status |
|---|---|---|---|---|
| G1 | Limiar e heurísticas do resolver `loc→page` | kindle | Q1, Q2 | 🟢 decidido |
| G2 | Template do callout e organização no vault | obsidian | Q5, Q6 | 🟢 decidido |
| G3 | Normalização + algoritmo do hash de idempotência | obsidian | Q7, Q8 | 🟢 decidido |

## Moderadas (bloqueavam módulos específicos)

| # | Lacuna | Unit | Pergunta | Status |
|---|---|---|---|---|
| G4 | Superfície de comandos, config e exit codes da CLI | cli | Q10–Q12 | 🟢 decidido |
| G5 | Formato de entrada e fixture do Boox | boox | Q13, Q14 | 🟢 decidido (formato: `markdown_export`); ⚠️ fixture real ainda por obter |
| G6 | Localização do resolver (kindle.py vs resolver.py) | kindle | Q3 | 🟢 decidido (`resolver.py`) |
| G7 | Correspondência página-comercial × página-canônica no export Amazon | amazon_export | Q4 | 🟢 decidido (página como *hint*, sempre via resolver) |

## Cosméticas / de borda

| # | Lacuna | Pergunta | Status |
|---|---|---|---|
| G8 | Política para bookmarks, livros sem PDF, no_match | Q9, Q15, Q16 | 🟢 decidido |
| G9 | Identidade de livro entre fontes | Q17 | 🟢 decidido |
| G10 | Fixture EN do export Amazon | Q18 | 🟢 decidido (adiada, YAGNI) |
| G11 | Destaques só-numéricos (tabelas) | Q19 | 🟢 decidido (risco aceito) |
| G12 | Detalhes de dry-run, lock com Obsidian Sync, transporte do export Boox | Q20–Q22 | 🟢 decidido |

## Dívidas confirmadas fora do escopo de perguntas (ação, não resposta)

- CI sem lint/testes/pip-audit apesar do contrato (architecture.md, dívida #1).
- `ARCHITECTURE.md` desatualizado: não lista `amazon_export.py`, prevê testes inexistentes (dívida #5).
- Título com parênteses é dividido errado pelo parser Kindle — comportamento verificado empiricamente, documentado em `kindle/design.md` [Reviewer].
- ⚠️ Obter fixture real do `markdown_export` do KOReader (pré-requisito prático do `boox.py`, remanescente de G5).
