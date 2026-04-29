# ADR-001 — Python 3.12+ com uv como stack do projeto

- **Status:** Accepted
- **Data:** 2026-04-29
- **Origem:** F5 do MDCU (decisão F5.4 confirmada pelo usuário)

## Contexto

O projeto sync-notes-obsidian é uma CLI determinística que precisa:
- Extrair texto e coordenadas de PDFs.
- Fazer fuzzy text-search para resolver `location de EPUB → página de PDF`.
- Fazer parsing leve de EPUB (mapping inverso quando necessário).
- Gerar callouts Markdown idempotentes em vault Obsidian.

Volume esperado: ≤1000 highlights por livro, ≤50 livros ativos. Performance crítica não é vetor relevante.

Stacks consideradas em F5: Python, Node.js/TypeScript, Rust, Go.

## Decisão

**Python 3.12+ com `uv` (Astral) como gerenciador de pacotes.** Manifesto em `pyproject.toml`, lock file `uv.lock` commitado.

## Razões

- **Ecossistema PDF/text é o mais maduro em Python:** `pdfplumber`, `pdfminer.six`, `rapidfuzz`, `ebooklib` são bibliotecas estáveis e bem mantidas.
- **`uv` é estado da arte em 2026:** instalação 10–100× mais rápida que pip; lock file determinístico nativo; integração com PEP 735 (`[dependency-groups]`).
- **Familiaridade do desenvolvedor:** custo de aprendizado zero.
- **Tipagem estática viável:** `mypy --strict` cobre o código todo (escolhido como guardrail).
- **Volume esperado** torna performance de runtime irrelevante; cold start de Python (~50ms) é aceitável para CLI manual.

## Consequências

### Positivas
- Setup rápido (≈30 minutos do `uv init` ao primeiro `uv run synctotes`).
- Libs maduras eliminam reescrita de parsing de PDF/EPUB.
- Type-check estrito desde o início → menos bugs na fronteira de tipos.
- Comunidade enorme = soluções para edge cases já documentadas.

### Negativas
- Cold start (~50ms) é gargalo SE no futuro virar daemon — não é o caso no MVP.
- Empacotamento para distribuição binária é mais frágil que Rust/Go (mas ainda não é problema — uso pessoal local).

## Alternativas consideradas

- **Node.js/TypeScript:** melhor se o projeto evoluir para plugin Obsidian (TypeScript nativo). Mas ecossistema PDF/text é menos maduro (pdfjs-dist é viável, mas APIs menos ergonômicas que pdfplumber). Rejeitado para o MVP; pode ser reconsiderado em ADR futuro se F6 evoluir para plugin.
- **Rust:** performance superior e binário standalone. Overkill para o volume; custo de aprendizado e manutenção alto. Rejeitado.
- **Go:** ok, mas ecossistema de parsing PDF é menos completo que Python; fuzzy matching exigiria implementação manual ou wrapping de C. Rejeitado.

## Referências
- `ARCHITECTURE.md` (Stack, Dependências, Comandos principais)
- `pyproject.toml`
