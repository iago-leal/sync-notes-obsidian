# Tasks — unit `kindle` (reimplementação fiel)

> Reversa Writer, 2026-07-02 · Cada task cita o arquivo-fonte do comportamento.

| # | Task | Fonte | Critério de pronto | Confiança |
|---|---|---|---|---|
| 1 | Definir `ClippingType` (StrEnum: highlight/note/bookmark), `KindleBook` e `KindleClipping` frozen | `kindle.py:27-53` | dataclasses imutáveis, campos e opcionalidades idênticos ao dicionário de dados | 🟢 |
| 2 | Implementar normalização de entrada: strip de BOM, CRLF/CR→LF | `kindle.py:105-107` | testes de BOM e CRLF passam | 🟢 |
| 3 | Implementar split por `==========` e loop de blocos com descarte silencioso | `kindle.py:109-117` | bloco malformado não derruba o parse; contagem correta | 🟢 |
| 4 | Implementar `_parse_book_line` com regex literal `^(.*?)\s*\((.+)\)\s*$` | `kindle.py:151-158` | com/sem autor cobertos | 🟢 |
| 5 | Implementar `_parse_metadata_line`: prefixo `- `, split por `\|`, tipo obrigatório na parte 0, varredura independente | `kindle.py:161-194` | formatos antigo e moderno aceitos | 🟢 |
| 6 | Implementar `_parse_position` com precedência página > posição | `kindle.py:205-216` | página zera posições; faixa X-Y e única cobertas | 🟢 |
| 7 | Implementar `_parse_date` PT-BR + EN com regra AM/PM | `kindle.py:219-257` | datas dos dois locales; ilegível → None | 🟢 |
| 8 | Portar suíte de 15 testes | `tests/test_kindle.py` | 100% verde | 🟢 |
| 9 | **Implementar resolver `loc→page`** retornando `MatchResult` | contrato: `types.py`, ADR-002 | found/ambiguous/no_match com limiar decidido (ver questions.md) | 🔴 |
| 10 | Expor contagem de blocos descartados para a CLI logar via rich (conciliação guardrail #13) | `kindle.py:102-103` + guardrail | CLI reporta N blocos pulados | 🟡 proposta |
