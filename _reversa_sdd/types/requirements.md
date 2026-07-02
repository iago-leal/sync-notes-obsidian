# Requirements — unit `types`

> Reversa Writer, 2026-07-02 · Fonte: `src/synctotes/types.py`, `tests/test_smoke.py`, ADR-002.

## Objetivo

Fixar o contrato público do resolver `loc→page` **antes** da implementação, porque refatorá-lo depois toca todos os consumidores (guardrail #1) 🟢.

## Requisitos funcionais

| ID | Requisito | MoSCoW | Confiança |
|---|---|---|---|
| RF-01 | `MatchStatus` = Literal `found` \| `ambiguous` \| `no_match` | Must | 🟢 |
| RF-02 | `Candidate` frozen: `page: int`, `score: float`, `excerpt: str` | Must | 🟢 |
| RF-03 | `MatchResult` frozen: `status` obrigatório; `page`/`confidence` default `None`; `candidates` default `()` | Must | 🟢 |
| RF-04 | Semântica por status: `found` → page+confidence; `ambiguous` → candidates; `no_match` → só status | Must | 🟢 docstring |
| RF-05 | Interface estável para decorator LLM-fallback em v2 | Should | 🟢 ADR-002 (contrato) |

## Critérios de aceitação

**Cenário feliz — construção default** 🟢
Dado `MatchResult(status="no_match")`
Então `page is None`, `confidence is None`, `candidates == ()`.

**Cenário de falha — imutabilidade** 🟢
Dado um `MatchResult` construído
Quando se tenta atribuir um campo
Então `FrozenInstanceError`.

## Restrição de mudança

🟥 Célula crítica do Gate de Blast Radius (ADR-006): **qualquer alteração nesta unit exige ADR prévio**.
