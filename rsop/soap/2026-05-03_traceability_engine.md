# SOAP: Motor de Rastreabilidade Semântica

**Data:** 2026-05-03

## S (Subjetivo)
- **Queixa:** Repositório global MDCU atualizado para requerer matrizes de blast radius.
- **Demanda:** Aplicar a mudança infraestrutural no projeto `sync-notes-obsidian` criando as matrizes de rastreabilidade para prevenção de quebras orgânicas e alucinações de agentes LLM.

## O (Objetivo)
- As matrizes `code-spec-matrix.md` e `spec-impact-matrix.md` eram inexistentes no projeto local.
- O diretório `traceability/` foi requisitado.
- As regras atuais (`ARCHITECTURE.md`, `ADR-002`, etc.) não possuíam enforcement de contenção cruzada.

## A (Avaliação)
1. Necessidade de criar `traceability/code-spec-matrix.md` mapeando scripts de CLI para suas specs. (#4)
2. Necessidade de criar `traceability/spec-impact-matrix.md` definindo limites vermelhos 🟥 para o conversor fuzzy e a gravação de arquivos. (#5)
3. Formalização da decisão no histórico através de ADR. (#6)

## P (Plano)
1. Criadas as matrizes do motor de rastreabilidade.
2. Criada `ADR-006` documentando as regras de bloqueio.
3. Passivos `#4`, `#5` e `#6` devidamente arquivados no RSOP.

## R (Reflexão)
O framework agora detém a fundação de "Stop the World" (Disjuntor) que impedirá regressões severas não documentadas durante as futuras fases de codificação por agentes delegados.
