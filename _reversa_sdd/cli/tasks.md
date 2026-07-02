# Tasks — unit `cli`

> Reversa Writer, 2026-07-02.

| # | Task | Fonte | Critério de pronto | Confiança |
|---|---|---|---|---|
| 1 | Reproduzir stub atual (`main() -> int`, print + exit 0) | `cli.py:1-23` | `synctotes` roda e sai 0 | 🟢 |
| 2 | Decidir assinaturas dos comandos (ver questions.md) | 🔴 | registro em decisão/ADR | 🔴 |
| 3 | Implementar comandos Typer com `--dry-run` e logs rich | guardrails #9 #10 #14 | cenários alvo do requirements passam | 🟡 |
| 4 | Reportar itens malformados pulados (contagem dos parsers) | guardrail #13 | log rich com N pulados | 🟡 |
| 5 | Testes de CLI (runner do Typer) cobrindo dry-run e degradação | inexistentes | suíte nova verde | 🔴 |
