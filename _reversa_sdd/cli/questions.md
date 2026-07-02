# Questions — unit `cli` (decididas)

> Reversa Writer, 2026-07-02 · Decisões aprovadas em bloco pelo mantenedor em 2026-07-02 e propagadas do `_reversa_sdd/questions.md` central (fonte autoritativa das respostas completas).

| # | Pergunta | Decisão | Ref |
|---|---|---|---|
| 1 | 🟢 DECIDIDO — Superfície de comandos | Subcomandos por fonte: `synctotes ingest kindle <path>`, `synctotes ingest amazon <path>`, `synctotes ingest boox <path>`, mais `synctotes status` (config e contagens do vault). Sem `sync` monolítico no MVP | Q10 |
| 2 | 🟢 DECIDIDO — Localização de vault e biblioteca | Config file `~/.config/synctotes/config.toml` (campos `vault`, `library`, `leituras_folder`), com override por flags `--vault/--library`. Sem env vars | Q11 |
| 3 | 🟢 DECIDIDO — Exit codes | `0` sucesso (inclusive com itens pulados, reportados via rich); `1` erro de execução (I/O, PDF corrompido); `2` configuração inválida. Skips não quebram automação | Q12 |
| 4 | 🟢 DECIDIDO — `--dry-run` | Diff completo: os callouts inteiros que seriam escritos, por arquivo de destino | Q20 |
