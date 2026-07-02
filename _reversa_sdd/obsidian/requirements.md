# Requirements — unit `obsidian` (stub — spec de alvo)

> Reversa Writer, 2026-07-02 · Fontes: docstring de `obsidian.py`, guardrails #2 #6 #7 #12 #14 #15, ADR-004. Contrato declarado; implementação F6.a 🔴.

## Objetivo

Única camada de escrita do sistema: materializar anotações resolvidas como callouts Markdown no vault, de forma **idempotente** e **append-only**, sempre ancoradas ao PDF canônico 🟢 (contrato).

## Requisitos funcionais

| ID | Requisito | MoSCoW | Confiança |
|---|---|---|---|
| RF-01 | Callout linka SEMPRE o PDF canônico no formato `[[livro.pdf#page=X]]`; nunca EPUB | Must | 🟢 guardrail #2, ADR-004 |
| RF-02 | Idempotência: identidade do highlight = hash estável de (livro, snippet normalizado); re-execução não duplica | Must | 🟢 guardrail #6 (algoritmo 🔴) |
| RF-03 | Append-only: apenas adicionar callouts ou criar arquivos novos; `os.remove`/deleção de `.md` proibidos | Must | 🟢 guardrail #12 |
| RF-04 | Responder a `--dry-run`: relatar sem escrever | Must | 🟢 guardrail #14 |
| RF-05 | Escrita com `encoding="utf-8"` explícito | Must | 🟢 guardrail #15 |
| RF-06 | Formato/template do callout (tipo, metadados: cor? data? nota anexada?) | Must | 🔴 não especificado |
| RF-07 | Organização no vault: um arquivo por livro? nota existente do livro? pasta dedicada? | Must | 🔴 não especificado |
| RF-08 | PDFs originais jamais são modificados | Must | 🟢 guardrail #7 |

## Critérios de aceitação

**Cenário alvo — idempotência** 🟡 (derivado do guardrail #6)
Dado um vault já contendo o callout do highlight H
Quando o pipeline re-processa o mesmo `My Clippings.txt`
Então nenhum callout novo é criado e nenhum arquivo é modificado.

**Cenário alvo — append-only** 🟡 (guardrail #12)
Dado qualquer execução do writer
Quando inspecionado o conjunto de operações de filesystem
Então há apenas criações e appends; nenhuma deleção ou reescrita de conteúdo pré-existente.

**Cenário alvo — dry-run** 🟡 (guardrail #14)
Dado `--dry-run`
Quando o writer executa
Então o vault permanece byte-idêntico e a saída lista os callouts que seriam escritos.

## Dependências

Consome: `MatchResult` (types), anotações parseadas. Consumido por: CLI. Escreve em: vault (Obsidian Sync) 🟢.
