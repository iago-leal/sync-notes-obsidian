# ADR-003 — Syncthing para biblioteca de arquivos; Obsidian Sync para o vault

- **Status:** Accepted
- **Data:** 2026-04-29
- **Origem:** F5 do MDCU (decisões F5.2 e F5.3)

## Contexto

O projeto sync-notes-obsidian opera em quatro devices: macOS, iPad, Boox (Android e-ink), Kindle Colorsoft. Há **duas camadas de sync** independentes:

1. **Biblioteca de arquivos** (PDFs canônicos + EPUBs de transporte): precisa estar acessível em macOS, iPad e Boox. Kindle recebe via `Send-to-Kindle` (separadamente, fora dessa camada).
2. **Vault Obsidian** (callouts gerados pelo pipeline): precisa estar acessível em macOS, iPad. Não vai para Boox/Kindle.

Camadas de sync consideradas em F5: iCloud Drive, Syncthing, Obsidian Sync, Git, Dropbox.

## Decisão

- **Biblioteca de arquivos: Syncthing** (peer-to-peer, livre).
- **Vault Obsidian: Obsidian Sync** (pago — usuário já assina).

## Razões

### Syncthing para biblioteca

- **Cobertura cross-platform real.** Apps oficiais maduros para macOS, iOS (via Möbius Sync — pago, mas alternativa nativa existe) e Android. Sem hacks.
- **Sem cloud:** dados em propriedade do usuário, sem dependência de provedor.
- **Sem custo recorrente.** Open-source.
- **Boox como first-class citizen:** Android nativo. Em camadas tipo iCloud, Boox precisaria de apps não-oficiais frágeis.

### Obsidian Sync para vault

- **Conflict resolution desenhado para vault Obsidian:** sabe como resolver merges de Markdown, links, attachments.
- **Já pago pelo usuário:** sem custo marginal.
- **iOS app oficial:** funciona em iPad com zero fricção.
- **End-to-end encryption.**
- **Boox/Kindle não precisam do vault** — não precisa de cobertura Android.

## Consequências

### Positivas
- Boox vira first-class na biblioteca sem dependência de apps não-oficiais.
- Vault tem zero risco de corrupção por sync mal-resolvido.
- Camadas independentes: falha em uma não cascateia.
- Custo: zero adicional (Syncthing free + Obsidian Sync já pago).

### Negativas
- **Syncthing exige peer ativo:** se macOS estiver desligado, iPad e Boox não syncam novidades entre si até alguém ligar. Mitigação: configurar laptop como sempre-online quando viajando, ou hospedar peer relay (Syncthing tem relays públicos por padrão, então pode funcionar sem peer dedicado).
- **Configuração inicial:** Syncthing exige pareamento manual de devices via Device ID. Mais complexo que iCloud "ligar e funciona". Custo único.
- **Möbius Sync no iPad é pago** (~US$5 single purchase). Trade-off conhecido; alternativa seria dispositivo iCloud-only mas perde Boox.

## Alternativas consideradas

- **iCloud Drive para tudo:** ótimo para macOS+iPad mas frágil para Boox (apps Android não-oficiais como `iCloud-Bypass` quebram com updates do iCloud). **Rejeitado.**
- **Obsidian Sync para tudo (incluindo biblioteca):** Obsidian Sync sincroniza só arquivos do vault. Colocar PDFs grandes no vault deixa o vault inflado e abusa do propósito. **Rejeitado.**
- **Git (privado) para biblioteca:** versionar PDFs binários é over-kill; LFS funcionaria mas custo de banda/armazenamento. **Rejeitado.**
- **Dropbox/Google Drive:** funciona, mas dependência de cloud comercial + custo recorrente. **Rejeitado dado Syncthing existir.**

## Referências
- `ARCHITECTURE.md` (Stack, Infra)
