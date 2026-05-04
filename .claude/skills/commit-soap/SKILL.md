---
name: commit-soap
version: "2.0.0"
author: Iago Leal
description: Gerador de mensagem de commit canônica (Selo Longitudinal Universal) derivada do A+P para garantir o histórico cognitivo no Git.
---

# commit-soap — Selo Longitudinal Universal

Você é a skill `commit-soap`, responsável por gerar o selo longitudinal no repositório. Você traduz o contexto cognitivo e arquitetural (MDCU, setup, refresh estrutural) em mensagens de commit estruturadas, mantendo a auditabilidade pura via `git log`.

## Mudança em v2.0.0 (Desacoplamento)

O escopo da skill expandiu. Antes restrita ao fechamento de `/mdcu`, agora a skill é o "selo longitudinal universal". Qualquer skill ou fluxo que produza Avaliação e Plano (A+P) estruturado pode invocar `/commit-soap --inline` para gerar marcos no Git.

## Formato Canônico e Regras Estritas

A sua mensagem gerada DEVE seguir rigidamente este formato:

1. **Linha 1 (Assunto):** Deve ter **no máximo 72 caracteres**.
2. **Corpo (A+P):** 
   - `A: [síntese do problema]` 
   - `P: [síntese do plano executado]`
   *(Se referenciar IDs do RSOP, use o formato `A: #N — [...]` e `P: #N — [...]`. Múltiplos IDs significam múltiplas linhas repetindo os prefixos A/P).*
3. **Trailer Refs:** Sempre inclua uma linha em branco seguida de `Refs: [caminho relativo do arquivo que originou a decisão]`.
4. **PROIBIDO `Co-Authored-By`:** Você NUNCA deve incluir trailers de co-autoria da IA (`Co-Authored-By: Claude`, etc.). Esta é uma regra global inviolável.

## Fontes Aceitas e Comandos

Você atua extraindo `A` e `P`. Se a extração falhar, **NÃO INVENTE** mensagens. Aborte.

- `/commit-soap`: Default. Localiza o SOAP mais recente em `rsop/soap/`. Se não existir, emita aviso (oriente a usar `git commit` se for apenas um WIP) e aborte. Se o arquivo existir mas a seção `## A` estiver vazia, aborte indicando malformação. Após ler, gere a mensagem, **exiba para o usuário**, e ao confirmar, comite.
- `/commit-soap --from <path>`: Localiza o arquivo apontado no `<path>` e extrai o A+P dele.
- `/commit-soap --inline`: Recebe o A+P como string de contexto de outra skill. (Ex: o `/project-setup` te passa as decisões pós-refresh).
- `/commit-soap --dry-run`: Exibe a mensagem gerada, mas NÃO executa o `git commit`.
- `/commit-soap --amend`: Executa `git commit --amend` usando a mensagem reformatada a partir da fonte atual. Se o último commit **não** contiver o formato `A:/P:/Refs:`, exija confirmação explícita perguntando: "o último commit não tem formato A:/P:/Refs: — reescrever mesmo assim?".

## Invariante de Uso

Esta skill é o marco cognitivo. É proibido usá-la para commits atômicos de WIP, typos, formatação ou micro-commits operacionais, os quais devem utilizar diretamente o cliente do Git.
