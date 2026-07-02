# Gaps — lacunas remanescentes

> Reversa Reviewer, 2026-07-02 · Lacunas 🔴 sem resposta no momento do fechamento da extração. Espelham o `questions.md`; atualizar ambos quando respondidas.

## Críticas (bloqueiam a implementação do coração do sistema)

| # | Lacuna | Unit | Pergunta |
|---|---|---|---|
| G1 | Limiar e heurísticas do resolver `loc→page` | kindle | Q1, Q2 |
| G2 | Template do callout e organização no vault | obsidian | Q5, Q6 |
| G3 | Normalização + algoritmo do hash de idempotência | obsidian | Q7, Q8 |

## Moderadas (bloqueiam módulos específicos)

| # | Lacuna | Unit | Pergunta |
|---|---|---|---|
| G4 | Superfície de comandos, config e exit codes da CLI | cli | Q10–Q12 |
| G5 | Formato de entrada e fixture do Boox | boox | Q13, Q14 |
| G6 | Localização do resolver (kindle.py vs resolver.py) | kindle | Q3 |
| G7 | Correspondência página-comercial × página-canônica no export Amazon | amazon_export | Q4 |

## Cosméticas / de borda

| # | Lacuna | Pergunta |
|---|---|---|
| G8 | Política para bookmarks, livros sem PDF, no_match | Q9, Q15, Q16 |
| G9 | Identidade de livro entre fontes | Q17 |
| G10 | Fixture EN do export Amazon | Q18 |
| G11 | Destaques só-numéricos (tabelas) | Q19 |
| G12 | Detalhes de dry-run, lock com Obsidian Sync, transporte do export Boox | Q20–Q22 |

## Dívidas confirmadas fora do escopo de perguntas (ação, não resposta)

- CI sem lint/testes/pip-audit apesar do contrato (architecture.md, dívida #1).
- `ARCHITECTURE.md` desatualizado: não lista `amazon_export.py`, prevê testes inexistentes (dívida #5).
- Título com parênteses é dividido errado pelo parser Kindle — comportamento verificado empiricamente, documentado em `kindle/design.md` [Reviewer].
