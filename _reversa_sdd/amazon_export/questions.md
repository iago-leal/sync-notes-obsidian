# Questions — unit `amazon_export`

> Reversa Writer, 2026-07-02.

| # | Pergunta | Contexto | Impacto |
|---|---|---|---|
| 1 | 🔴 Haverá livros anotados em Kindle configurado em inglês? Se sim, obter um export real para fixture (RF-11) | docstring `amazon_export.py:14` | Sem fixture, o suporte EN não nasce |
| 2 | 🟡 Como o pipeline reconciliará a mesma anotação vinda de duas fontes (My Clippings e export Amazon do mesmo livro)? O hash de idempotência (livro, snippet) cobre, mas título difere entre fontes (`Quincas Borba` vs `Dom Casmurro (Machado de Assis)` formats) | ERD: sem chave comum entre `KindleBook` e `AmazonBook` | Duplicação de callouts se a normalização de "livro" não for definida |
| 3 | 🟡 Destaques compostos só de números (tabelas) seriam descartados como ruído estrutural (`_BARE_DIGIT_RE`) — aceitável? | design §4 | Perda silenciosa em livros técnicos |
| 4 | 🟡 `coordinate_kind="page"` do export refere-se à paginação da edição comercial; ela coincide com a do PDF canônico (edição domínio público)? Se não, também precisa de resolver | lacuna 7 do domain.md | Âncora errada no callout |
