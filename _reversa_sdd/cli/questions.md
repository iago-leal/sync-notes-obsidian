# Questions — unit `cli`

> Reversa Writer, 2026-07-02.

| # | Pergunta | Impacto |
|---|---|---|
| 1 | 🔴 Quais comandos a CLI expõe? Um `sync` monolítico, ou `ingest-kindle`/`ingest-amazon`/`ingest-boox` separados? | Toda a superfície pública |
| 2 | 🔴 Como a CLI localiza vault e biblioteca — argumentos, config file (`~/.synctotes.toml`?), env vars? (ARCHITECTURE não define; CLAUDE.md global do usuário pede config fora do código) | UX e reprodutibilidade |
| 3 | 🔴 Exit code com itens pulados: sucesso (0) ou código dedicado? | Automação via cron/scripts |
| 4 | 🟡 `--dry-run` imprime diff completo dos callouts ou só contagem? | Utilidade da revisão manual |
