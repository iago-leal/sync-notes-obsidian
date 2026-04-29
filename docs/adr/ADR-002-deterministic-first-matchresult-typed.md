# ADR-002 — Conversor `loc→page` determinístico-first com `MatchResult` tipado; LLM-fallback como ponto de extensão (decorator pattern)

- **Status:** Accepted
- **Data:** 2026-04-29
- **Origem:** F5 do MDCU (decisão F5.5)

## Contexto

O coração do projeto é o conversor `loc EPUB → page PDF`: dado um highlight do Kindle (que vem do `My Clippings.txt` com snippet de texto + location no AZW3), precisa-se descobrir a qual página do PDF canônico esse trecho corresponde, para que o callout no vault aponte para a página correta.

Duas abordagens foram propostas em F5:

- **Determinístico-first:** fuzzy text-search do snippet contra o texto extraído do PDF (`pdfplumber` + `rapidfuzz`).
- **LLM-first:** rodar um LLM local (Ollama) que recebe snippet + contexto do PDF e retorna a página.

A pergunta crítica em F5.5 do usuário foi: **qual o custo de adiar LLM-fallback para v2?**

## Decisão

1. **MVP usa apenas o caminho determinístico.** Sem LLM. Sem dependência de Ollama. Sem GPU/RAM extra.
2. **Interface pública do conversor é tipada via `MatchResult` desde a primeira linha de código** (ver `src/synctotes/types.py`). Status: `found` | `ambiguous` | `no_match`. Inclui `page`, `confidence`, `candidates`.
3. **LLM-fallback é ponto de extensão preservado** via decorator pattern sobre essa mesma interface. Quando dor real for medida (frequência de status `ambiguous` ou `no_match` for incômoda), implementação adicional sem refatoração:

```python
class LLMFallbackResolver:
    def __init__(self, primary: Resolver, llm_client): ...
    def resolve(self, snippet, pdf_text) -> MatchResult:
        result = self.primary.resolve(snippet, pdf_text)
        if result.status == "ambiguous":
            return self.llm_disambiguate(result.candidates, snippet)
        return result
```

## Razões

- **Determinístico é debugável; LLM é não-determinismo.** Mesmo input → mesmo output em todas as runs. Bug é reproduzível.
- **Fuzzy text-search resolve 80–90% dos casos** quando snippets têm >30 caracteres (verificável empiricamente em F6).
- **Custo de adicionar LLM no futuro é baixo** (≈80–100 linhas + 1 dep + 1–2 dias) **se a interface tipada já existir**. Sem `MatchResult`, refatorar todos os call sites é doloroso → dívida vira cara.
- **Premature optimization avoidance:** a complexidade de LLM cobre 10–20% que determinístico não cobre. Se esse 10–20% for raro no uso real, LLM nunca se justifica.
- **Princípio MDCU:** "Three similar lines is better than a premature abstraction." Mas tipos públicos não são abstração prematura — são contrato; estabelecer cedo é zero overhead.

## Consequências

### Positivas
- MVP atinge funcionalidade em ≈3–5 dias.
- Determinístico = `pytest` consegue cobrir 100% dos branches.
- Zero dependência de runtime de modelo grande.
- `MatchResult` tipado força tratamento explícito de cada status no caller (ergo bugs silenciosos são improváveis).

### Negativas
- Snippets curtos, repetidos ou ambíguos em livros com referências cruzadas → `status="ambiguous"`. Sem LLM, esses viram log warning + escolha do top-1 candidato (com aviso) → exigem ajuste manual no vault.
- Cobertura realista de highlights em livros narrativos: provavelmente 90%+. Em livros técnicos com muita repetição de termos: pode cair para 70–80%.

### Acompanhamento
- Em F6.b (acompanhamento), instrumentar contagem de `found` vs `ambiguous` vs `no_match` em log estruturado. Quando ambíguos passarem de 15–20% por livro de forma persistente, reabrir essa decisão e considerar implementação do `LLMFallbackResolver`.

## Alternativas consideradas

- **LLM-first (sugestão inicial do usuário em F4):** cobertura mais alta, mas:
  - Adiciona dep pesada desde dia 1 (Ollama + modelo).
  - Não-determinismo dificulta testing.
  - Custo de implementação MVP 4–5× maior.
  - Dívida de não-ter-determinístico é IGUAL à de não-ter-LLM (ambos exigiriam refatoração depois). Logo, LLM-first não é claramente superior.
  - **Rejeitado** após análise de custo.
- **Determinístico sem `MatchResult` tipado** (retornar `int | None`): refatorar depois para adicionar fallback exigiria tocar todos os call sites. Dívida cara. **Rejeitado.**
- **Esperar para decidir:** "a gente vê depois". Decisão por inércia produz design ruim. **Rejeitado.**

## Referências
- `ARCHITECTURE.md` (Guardrail #1, Guardrail #5)
- `src/synctotes/types.py` (implementação do contrato)
- `tests/test_smoke.py` (validação que o contrato está exposto)
