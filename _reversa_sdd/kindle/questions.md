# Questions — unit `kindle` (decididas)

> Reversa Writer, 2026-07-02 · Decisões aprovadas em bloco pelo mantenedor em 2026-07-02 e propagadas do `_reversa_sdd/questions.md` central (fonte autoritativa das respostas completas).

| # | Pergunta | Decisão | Ref |
|---|---|---|---|
| 1 | 🟢 DECIDIDO — Limiar de score do resolver | rapidfuzz `token_set_ratio` sobre o texto de cada página: `found` se ≥ 90 **e** vantagem ≥ 5 pontos sobre o 2º colocado; `ambiguous` se ≥ 75 sem essas condições; `no_match` se < 75. `confidence = score/100`. Limiares como constantes nomeadas, calibráveis pela fixture Quincas Borba | Q1 |
| 2 | 🟢 DECIDIDO — Desempate multi-página | Prior de posição relativa: `location/max_location` estima `page/max_page`; vence o candidato com página mais próxima da estimativa, mantida a vantagem de 5 pontos; persistindo empate, `ambiguous` | Q2 |
| 3 | 🟢 DECIDIDO — Localização do resolver | Módulo próprio `resolver.py` (`kindle.py` permanece parser puro; o resolver serve a todas as fontes). Registrar microdecisão; docstring de `kindle.py` atualizada em F6 | Q3 |
| 4 | 🟢 DECIDIDO — Bookmarks | Não geram callout (sem texto, sem valor no vault); contados no log da execução | Q15 |
| 5 | 🟢 DECIDIDO — Livro sem PDF canônico | Pular com aviso rich e listar no resumo final; nada é criado | Q16 |
