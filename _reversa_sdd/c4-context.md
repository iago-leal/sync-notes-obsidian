# C4 — Nível 1: Contexto

> Gerado pelo Reversa Architect em 2026-07-02.

```mermaid
C4Context
    title Contexto — synctotes (jailbreak-kindle)

    Person(iago, "Leitor (Iago)", "Lê e anota livros em 4 devices; consulta tudo no vault")

    System(synctotes, "synctotes (CLI)", "Pipeline determinístico: parseia anotações Kindle/Boox/Amazon e escreve callouts idempotentes no vault, ancorados ao PDF canônico")

    System_Ext(kindle, "Kindle Colorsoft", "Leitor de EPUB; gera My Clippings.txt e exports Amazon")
    System_Ext(boox, "Boox (KOReader)", "Leitor Android e-ink; exporta anotações em markdown")
    System_Ext(vault, "Vault Obsidian", "Destino único das anotações (Obsidian Sync)")
    System_Ext(biblioteca, "Biblioteca Syncthing", "PDFs canônicos + EPUBs de transporte")
    System_Ext(pdfplus, "obsidian-pdf-plus", "Anotações macOS/iPad direto no vault (não passam pela CLI)")
    System_Ext(amazon, "Amazon (e-mail)", "Envia PDF 'Caderno de anotações' por e-mail")

    Rel(iago, synctotes, "roda", "CLI local")
    Rel(kindle, synctotes, "My Clippings.txt", "USB")
    Rel(amazon, synctotes, "export PDF", "e-mail → arquivo")
    Rel(boox, synctotes, "export markdown 🔴", "Syncthing")
    Rel(biblioteca, synctotes, "PDF canônico (texto por página)", "filesystem")
    Rel(synctotes, vault, "callouts [[livro.pdf#page=X]]", "append-only")
    Rel(iago, pdfplus, "anota no macOS/iPad")
    Rel(pdfplus, vault, "callouts diretos")
    Rel(biblioteca, kindle, "EPUB", "Send-to-Kindle")
    Rel(biblioteca, boox, "PDF/EPUB", "Syncthing")
```

## Leitura

- O **caminho macOS/iPad não passa pela CLI**: `obsidian-pdf-plus` anota direto no vault com âncora de página 🟢.
- A CLI existe para os devices cujas anotações nascem em coordenadas erradas (location de EPUB) ou formatos alheios ao vault: Kindle e Boox 🟢.
- Fluxo Boox 🔴: formato de export e transporte ainda não fixados.
