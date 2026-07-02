# Questions — unit `obsidian` (decididas)

> Reversa Writer, 2026-07-02 · Era a unit com o maior número de lacunas críticas; decisões aprovadas em bloco pelo mantenedor em 2026-07-02 e propagadas do `_reversa_sdd/questions.md` central (fonte autoritativa das respostas completas).

| # | Pergunta | Decisão | Ref |
|---|---|---|---|
| 1 | 🟢 DECIDIDO — Template do callout | `> [!quote] [[livro.pdf#page=42\|p. 42]]` + texto do destaque + linha `— *Nota:*` só se houver nota anexada + comentário `%% st:<hash16> · <cor> · <data> %%` (invisível no preview, greppável). `confidence` não entra no callout; vai só ao log | Q5 |
| 2 | 🟢 DECIDIDO — Organização no vault | Um arquivo por livro em pasta dedicada (`Leituras/<Título Normalizado>.md`), criado pelo pipeline; nunca fazer append em notas manuais existentes (evita colisão com o obsidian-pdf-plus). Pasta configurável no config | Q6 |
| 3 | 🟢 DECIDIDO — Normalização do snippet | Unicode NFC → remoção de hífen de quebra (`-\n` → junção) → colapso de whitespace em espaço único → `strip()` → lowercase. **Sem** remover pontuação (preserva unicidade de trechos curtos) | Q7 |
| 4 | 🟢 DECIDIDO — Hash de idempotência | `sha256(titulo_normalizado + "\n" + snippet_normalizado)` em UTF-8, truncado a 16 hex; gravado no comentário do callout. Duplicata detectada por scan dos `%% st:… %%` do arquivo do livro | Q8 |
| 5 | 🟢 DECIDIDO — Destino de `ambiguous`/`no_match` | Seção `## Pendentes` ao final do arquivo do livro: callout sem âncora com o texto e, quando `ambiguous`, as páginas candidatas com scores. Também logado via rich; nada descartado silenciosamente | Q9 |
| 6 | 🟢 DECIDIDO — Lock contra Obsidian Sync | Sem lock no MVP; documentar no README a recomendação de não rodar durante sync ativo. Volume pequeno, escrita rápida, risco aceito | Q21 |
