# ADR-008 (retroativo) — Contrato antes do código (spec-first + TDD)

- **Status:** Inferido do histórico (🟡 proposto para formalização)
- **Data da decisão evidenciada:** 2026-04-29 (commits `15c67e2`, `90afe8f`, `164f155`)
- **Gerado por:** Reversa Detective, 2026-07-02

## Contexto

O histórico Git mostra uma sequência incomum e deliberada: o commit `90afe8f` declara o **contrato técnico completo** (ARCHITECTURE.md com stack, 15 guardrails e comandos canônicos) *antes de existir qualquer linha de código de aplicação* — mensagem explícita: "ainda não materializado". A implementação chega depois (`164f155`), anunciando TDD na própria mensagem.

## Decisão evidenciada 🟢

1. Especificação e guardrails precedem implementação (MDCU F2–F5 → só então F6).
2. Interfaces caras de refatorar (`MatchResult`) são fixadas em código antes dos seus consumidores existirem (guardrail #1; docstring de `types.py`: "refactoring this contract later is expensive").
3. Implementação guiada por testes, com fixtures sintéticas (fpdf2, clippings artificiais) e reais (Quincas Borba).
4. Stubs commitados com docstrings-contrato (`obsidian.py`, `boox.py`) reservam o lugar e o comportamento esperado dos módulos futuros.

## Razões 🟢 (declaradas na transcrição MDCU e no CLAUDE.md global do mantenedor)

- Mantenedor único e intermitente: o projeto precisa ser retomável após meses; contrato escrito vale mais que memória.
- Agentes de IA participam do desenvolvimento: guardrails e matrizes de rastreabilidade (ADR-006) blindam contra refatorações mal calculadas.

## Consequências

- O repositório é **legível por documentos**: quase nenhuma decisão vive só no código.
- Fricção de entrada alta (pre-commit, mypy strict, matrizes) aceita como custo de longevidade.
- Risco residual 🟡: documentos podem divergir do código em pausas longas (ex.: ARCHITECTURE.md prometia `pip-audit` no CI e `test_obsidian.py`/`test_boox.py` que ainda não existem) — o README de 2026-07-02 já corrige parte dessa deriva.
