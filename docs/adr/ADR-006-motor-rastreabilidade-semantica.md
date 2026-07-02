# ADR 006: Motor de Rastreabilidade Semântica

**Data:** 2026-05-03

## Contexto
O projeto foi submetido a uma atualização metodológica profunda baseada no framework MDCU, a qual instituiu a obrigatoriedade de matrizes de rastreabilidade para agentes de IA atuando como desenvolvedores. Para garantir a sustentabilidade do código e evitar que agentes introduzam refatorações mal calculadas (causando degradação arquitetural silenciosa), é imperativo adotar um disjuntor semântico ("Gate de Blast Radius").

## Decisão
Foi instituído o diretório `traceability/` contendo:
1. **`code-spec-matrix.md`**: Matriz que mapeia cada arquivo físico de código com a respectiva regra arquitetural (ARCHITECTURE.md ou ADRs). Nenhuma linha de código deve existir sem uma especificação âncora.
2. **`spec-impact-matrix.md`**: Matriz cruzada apontando o raio de impacto de alterações específicas. Alterações que tocam células 🟥 (críticas) necessitarão de elaboração prévia e aprovação explícita via novas ADRs.

## Consequências
- Aumento da segurança de desenvolvimento (blindagem contra IA operando sem contexto).
- Exigência contínua de atualização das matrizes ao se adicionar novos módulos ou fluxos.
- Maior fricção ("alta barreira") para realizar refatorações em componentes cruciais como `MatchResult` (interface tipada) e o mecanismo de Append-Only no `obsidian.py`.
