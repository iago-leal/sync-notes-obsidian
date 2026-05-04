# SOAP: Atualização do Framework MDCU

**Data:** 2026-05-03

## S (Subjetivo)
- **Queixa:** Repositório global MDCU recebeu uma nova atualização não especificada.
- **Demanda:** Sincronizar o projeto local com a versão mais recente do framework.

## O (Objetivo)
- O diretório `.agents/skills/` e `.claude/skills/` continham versões anteriores das skills.

## A (Avaliação)
1. Necessidade de atualizar as skills de governança para manter o projeto alinhado com o estado da arte do framework.

## P (Plano)
1. Clone do repositório `iago-leal/MDCU`.
2. Sobrescrita das skills locais pelas novas versões do repositório upstream.
3. Deleção do clone temporário.

## R (Reflexão)
O ambiente permanece coeso e operando sob o contrato metodológico mais recente sem vazamento de arquivos temporários.
