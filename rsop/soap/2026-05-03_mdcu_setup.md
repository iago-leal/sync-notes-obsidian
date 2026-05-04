# SOAP: Integração do MDCU

**Data:** 2026-05-03

## S (Subjetivo)
- **Queixa:** Usuário sentiu necessidade de que o framework MDCU estivesse devidamente integrado ao repositório já criado.
- **Demanda:** Formalizar e materializar a fundação do MDCU (especificamente o prontuário RSOP e regras de versionamento) para estabilizar sessões futuras.

## O (Objetivo)
- Skills do framework fisicamente instanciadas no projeto (`.agents/skills`, `.claude/skills`).
- Diretório `rsop/` estava inexistente, impedindo a Fase 1 (Preparação) em futuros fluxos.
- Arquivo transitório `_mdcu.md` presente e suscetível a commits acidentais por ausência no `.gitignore`.

## A (Avaliação)
1. Faltava inicialização do repositório clínico (`rsop/`).
2. Faltava proteção do arquivo de lousa efêmera (`_mdcu.md`).

## P (Plano)
1. Criada a estrutura `rsop/` contendo `dados_base.md`, `lista_problemas.md` e `passivos.md`.
2. Adicionado o arquivo `_mdcu.md` ao final do arquivo `.gitignore`.

## R (Reflexão)
O ambiente agora suporta plenamente a metodologia de engenharia longitudinal do MDCU.
