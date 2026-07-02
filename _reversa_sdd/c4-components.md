# C4 — Nível 3: Componentes (container CLI synctotes)

> Gerado pelo Reversa Architect em 2026-07-02.
> Único container de código; componentes = módulos do pacote.

```mermaid
C4Component
    title Componentes — pacote synctotes

    Container_Boundary(pkg, "synctotes") {
        Component(cli, "cli.py", "Typer 🔴 stub", "main() -> int; comandos reais em F6")
        Component(kindle, "kindle.py", "parser puro", "parse_clippings: My Clippings PT-BR/EN → KindleClipping; futuro lar do resolver")
        Component(amazon, "amazon_export.py", "parser + máquina de estados", "parse_export_pdf: PDF Amazon → ExportedNotebook")
        Component(boox, "boox.py", "🔴 stub", "ingest KOReader/Boox markdown")
        Component(pdf, "pdf.py", "pdfplumber wrapper", "extract_pages: PDF → dict[int, str] 1-indexado")
        Component(types, "types.py", "contratos frozen", "MatchResult, Candidate, MatchStatus (ADR-002)")
        Component(obsidian, "obsidian.py", "🔴 stub", "writer de callouts append-only, idempotente")
    }

    Rel(cli, kindle, "parse_clippings")
    Rel(cli, amazon, "parse_export_pdf")
    Rel(cli, boox, "futuro")
    Rel(cli, obsidian, "futuro")
    Rel(amazon, kindle, "ClippingType")
    Rel(amazon, pdf, "pdfplumber direto 🟡")
    Rel(kindle, types, "MatchResult (resolver futuro)")
    Rel(kindle, pdf, "extract_pages (resolver futuro)")
```

## Responsabilidades e dependências 🟢

| Componente | Depende de | Usado por | Pureza |
|---|---|---|---|
| `types` | — | kindle (futuro), cli (futuro) | dados imutáveis |
| `pdf` | pdfplumber | resolver futuro, testes | função pura sobre I/O de leitura |
| `kindle` | stdlib apenas | cli futuro; amazon_export (ClippingType) | puro (str → dataclasses) |
| `amazon_export` | pdfplumber, kindle.ClippingType | cli futuro | puro após extração |
| `boox` 🔴 | — | cli futuro | — |
| `obsidian` 🔴 | — | cli futuro | única escrita em disco do sistema |
| `cli` 🔴 | typer, rich (declarados) | usuário | casca imperativa |

## Observações arquiteturais

- 🟡 `amazon_export` chama pdfplumber diretamente em vez de reutilizar `pdf.extract_pages` — justificável (precisa do texto corrido, não paginado), mas duplica a fronteira com a lib externa; candidato a unificação quando o resolver nascer.
- 🟢 Nenhum módulo de domínio importa framework (Typer/rich ficam confinados ao `cli.py` futuro) — baixo acoplamento conforme contrato.
- 🟢 O resolver planejado vive em `kindle.py` (docstring), mas consumirá `pdf.extract_pages` e `rapidfuzz`; 🟡 considerar módulo próprio (`resolver.py`) para não inchar o parser — decisão em aberto para F6.
