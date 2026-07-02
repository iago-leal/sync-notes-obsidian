# Questions — unit `kindle` (validação humana pendente)

> Reversa Writer, 2026-07-02.

| # | Pergunta | Contexto | Impacto |
|---|---|---|---|
| 1 | 🔴 Qual o limiar de score do rapidfuzz que separa `found` de `ambiguous`/`no_match`? | ADR-002 fixa o contrato, não o limiar | Núcleo do RF-09; define a taxa de callouts automáticos |
| 2 | 🔴 Com snippet presente em múltiplas páginas (epígrafes, refrões), qual heurística de desempate — ordem, location relativa, contexto adjacente? | resolver futuro | Qualidade do `ambiguous` |
| 3 | 🔴 O resolver deve viver em `kindle.py` (docstring atual) ou em módulo próprio `resolver.py` (sugestão do Architect em `c4-components.md`)? | organização | Coesão do módulo |
| 4 | 🟡 Clippings de tipo `bookmark` (sem texto) devem gerar callout, ser ignorados, ou registrados noutro formato? | writer futuro | Escopo do pipeline |
| 5 | 🟡 O que fazer com clippings cujo livro não tem PDF canônico na biblioteca? | operacional | Fila de pendências vs. descarte |
