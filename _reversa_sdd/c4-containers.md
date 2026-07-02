# C4 — Nível 2: Containers

> Gerado pelo Reversa Architect em 2026-07-02.

```mermaid
C4Container
    title Containers — synctotes

    Person(iago, "Leitor (Iago)")

    System_Boundary(sys, "synctotes") {
        Container(cli, "CLI synctotes", "Python 3.12 + Typer + rich", "Entry point; orquestra parse → resolve → write; --dry-run mandatório 🔴 stub")
        Container(parsers, "Parsers de ingest", "Python puro", "kindle (My Clippings), amazon_export (PDF Amazon), boox 🔴 stub")
        Container(resolver, "Resolver loc→page", "pdfplumber + rapidfuzz", "Fuzzy match do snippet contra o PDF canônico; retorna MatchResult 🔴 não implementado")
        Container(writer, "Writer Obsidian", "Python puro", "Callouts idempotentes, append-only, hash de (livro, snippet) 🔴 stub")
    }

    ContainerDb_Ext(vault, "Vault Obsidian", "Markdown", "Estado do sistema — sem banco de dados")
    ContainerDb_Ext(biblioteca, "Biblioteca", "PDF/EPUB via Syncthing", "PDFs canônicos")
    System_Ext(fontes, "Fontes de anotações", "My Clippings.txt, export Amazon, export Boox")

    Rel(iago, cli, "synctotes <cmd>", "terminal")
    Rel(cli, parsers, "arquivos de entrada")
    Rel(parsers, resolver, "KindleClipping / AmazonAnnotation")
    Rel(biblioteca, resolver, "extract_pages(pdf)")
    Rel(resolver, writer, "MatchResult")
    Rel(writer, vault, "callouts", "filesystem, append-only, utf-8")
    Rel(fontes, cli, "paths", "argumentos CLI")
```

## Comunicação entre containers 🟢

Toda comunicação é **chamada de função em processo único** com dataclasses imutáveis como contrato — não há serviços, filas ou IPC. "Containers" aqui são fronteiras lógicas de responsabilidade dentro de um único processo CLI.

| De → Para | Contrato |
|---|---|
| parsers → resolver | `KindleClipping`, `AmazonAnnotation` (frozen) |
| resolver → writer | `MatchResult` (frozen; guardrail #1) |
| pdf → resolver | `dict[int, str]` denso 1-indexado |
| writer → vault | Markdown append-only com `encoding="utf-8"` |
