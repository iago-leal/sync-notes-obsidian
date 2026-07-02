# Questions — unit `obsidian`

> Reversa Writer, 2026-07-02. Unit com o maior número de lacunas críticas do projeto.

| # | Pergunta | Impacto |
|---|---|---|
| 1 | 🔴 Template do callout: que tipo de callout Obsidian (`> [!quote]`?), quais metadados entram (cor, data, nota anexada, confidence do resolver)? | Formato de todo o output do sistema |
| 2 | 🔴 Organização no vault: um `.md` por livro em pasta dedicada, ou append na nota existente do livro (integração com notas do obsidian-pdf-plus)? | Estrutura do vault; risco de colisão com notas manuais |
| 3 | 🔴 Normalização do snippet para o hash: lowercase? colapso de espaços? remoção de pontuação/hífens de quebra? | Falso-negativo = callout duplicado; falso-positivo = highlight engolido |
| 4 | 🔴 Algoritmo do hash (sha256 truncado? blake2?) e onde ele fica gravado (comentário HTML no callout? propriedade?) | Detecção de duplicata |
| 5 | 🟡 Anotações `ambiguous`/`no_match` geram callout sem âncora, entram numa nota de pendências, ou são só logadas? | Completude do vault |
| 6 | 🟡 Execução simultânea ao Obsidian Sync: precisa de lock/aviso? | Integridade em edge case |
