# Tasks — unit `obsidian`

> Reversa Writer, 2026-07-02.

| # | Task | Fonte | Critério de pronto | Confiança |
|---|---|---|---|---|
| 1 | Definir template do callout e organização no vault (questions 1-2) | 🔴 | decisão registrada (ADR ou principles) | 🔴 |
| 2 | Definir normalização do snippet + algoritmo do hash (estável, não-salted) | guardrail #6 | função pura testada | 🔴 |
| 3 | Implementar detecção de duplicata no vault | guardrail #6 | re-execução = no-op | 🟡 |
| 4 | Implementar escrita append-only com utf-8 e `--dry-run` | guardrails #12 #14 #15 | cenários alvo do requirements passam | 🟡 |
| 5 | Criar `tests/test_obsidian.py` (previsto no ARCHITECTURE.md, inexistente) | ARCHITECTURE.md | suíte verde com vault sintético em tmp_path | 🔴 |

⚠️ Célula 🟥 do Gate de Blast Radius: o mecanismo append-only é crítico (ADR-006) — mudanças exigem ADR.
