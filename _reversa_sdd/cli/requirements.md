# Requirements — unit `cli` (stub — spec de alvo)

> Reversa Writer, 2026-07-02 · Fontes: `cli.py` (stub), guardrails #9 #10 #13 #14, ADR-005. Quase tudo aqui é contrato declarado, não código 🟡/🔴.

## Objetivo

Casca imperativa do pipeline: expor comandos tipados (Typer) que orquestram parse → resolve → write com segurança operacional (dry-run, logs rich) 🟢 (contrato).

## Requisitos funcionais

| ID | Requisito | MoSCoW | Confiança |
|---|---|---|---|
| RF-01 | Entry point `synctotes` (console script) retorna exit code int | Must | 🟢 implementado (stub retorna 0) |
| RF-02 | CLI construída com Typer a partir de type hints; `argparse`/`sys.argv` proibidos | Must | 🟢 guardrail #9 (contrato) 🔴 código |
| RF-03 | Toda função que altera o vault aceita `--dry-run` | Must | 🟢 guardrail #14 🔴 código |
| RF-04 | Erros e logs ao usuário via rich | Must | 🟢 guardrail #10 🔴 código |
| RF-05 | Degradação graciosa: anotação malformada é logada e pulada, processamento continua | Must | 🟢 guardrail #13 🔴 código |
| RF-06 | Comandos concretos (ingest kindle, ingest amazon, ingest boox, sync...) | Must | 🔴 assinaturas não especificadas em lugar nenhum |

## Critérios de aceitação

**Cenário atual (stub verificado)** 🟢
Dado o pacote instalado
Quando `uv run synctotes` executa
Então imprime versão + aviso de pipeline não implementado e sai com código 0.

**Cenário alvo — dry-run** 🟡 (derivado do guardrail #14)
Dado um `My Clippings.txt` válido e a flag `--dry-run`
Quando o comando de sync executa
Então nenhum arquivo do vault é criado/alterado e a saída lista o que *seria* escrito.

**Cenário alvo — degradação graciosa** 🟡 (guardrail #13)
Dado um arquivo com 10 anotações, 2 malformadas
Quando o ingest executa
Então 8 são processadas, 2 são reportadas via rich, exit code de sucesso.

## Dependências

Orquestra: kindle, amazon_export, boox, obsidian. Frameworks confinados aqui: typer, rich (domínio permanece puro) 🟢 (contrato arquitetural).
