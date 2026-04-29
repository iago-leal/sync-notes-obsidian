# ADR-004 — PDF como formato canônico no vault; EPUB como variante de transporte

- **Status:** Accepted
- **Data:** 2026-04-29
- **Origem:** F4 do MDCU (terceira clarificação — Zotero + dual-format)

## Contexto

Cada livro da biblioteca existe em **dois formatos**:

- **PDF:** layout fixo, numeração de página estável, suporte rico a anotações via `obsidian-pdf-plus` (callouts no vault que abrem o PDF na página exata via popover).
- **EPUB:** layout reflowável, numeração de location/posição (não estável — varia entre leitores), formato amigável para e-readers como Kindle e Boox em modo reflow.

A decisão crítica em F4 do MDCU foi: **qual formato é canônico no vault?** A resposta determina para qual arquivo os callouts apontam, e como o link de volta funciona.

## Decisão

- **PDF é o formato canônico no vault.**
- **EPUB é variante de transporte fora do vault** — existe apenas para o Kindle/Boox-reflow lerem confortavelmente.
- **Links de callouts no vault SEMPRE apontam para PDF**, no formato `[[livro.pdf#page=X]]`. Nunca para EPUB.

## Razões

- **Estabilidade de coordenada:** página de PDF é determinada pelo layout do PDF. Não muda entre leitores. Location de EPUB é calculada por cada leitor com base no tamanho de fonte do usuário, dispositivo, etc. — `loc 1432` em um Kindle ≠ `loc 1432` em um Boox.
- **`obsidian-pdf-plus` opera sobre PDF.** Toda a experiência rica de anotação e popover é PDF-native.
- **PDF é universal.** macOS, iPad, Boox, qualquer app de leitura abre. Não depende de app específico.
- **Callouts apontando para EPUB seriam frágeis** — qual leitor abre? Qual location interpreta? Sem âncora estável, o link de volta é teatro.
- **PDF preservation:** o projeto NUNCA modifica o PDF (guardrail #7 do ARCHITECTURE.md). Anotações vivem no vault como callouts; PDF fica intocado. Modelo Zotero puro.

## Consequências

### Positivas
- Links no vault são estáveis ao longo do tempo (independem de mudança de fonte do leitor, etc.).
- `obsidian-pdf-plus` integra naturalmente.
- Renderização cross-device do callout é confiável.
- PDF original preservado — pode ser substituído por nova versão do livro sem invalidar anotações antigas (com cuidado em re-mapping).

### Negativas
- **Usuário precisa ter PDF de cada livro.** Se só tem EPUB:
  - **Caminho A:** converter EPUB → PDF via Calibre antes de adicionar à biblioteca. Layout pode ficar feio, mas é navegável.
  - **Caminho B:** anotações sem link clicável — vão como callout textual com referência "EPUB, location ~1432" sem âncora. Warning no log.
- **Pipeline do Kindle precisa do conversor `loc → page`** (ver ADR-002) porque Kindle lê EPUB e produz highlights em location, mas o link tem que apontar para PDF. Esse é o coração da complexidade.
- **EPUB-only books são cidadãos de segunda classe** no vault — anotação chega, mas sem âncora.

## Alternativas consideradas

- **EPUB canônico:** rejeitado por instabilidade de location entre leitores. Link `livro.epub#loc=1432` no vault não significa nada para um futuro leitor que renderize com fonte diferente.
- **Ambos canônicos (PDF e EPUB simultâneos):** dobra complexidade — toda anotação vira par `(link PDF, link EPUB)`, conversores precisam lidar com mapping bilateral, vault fica inflado. Rejeitado por carga cognitiva.
- **HTML/CFI (EPUB Canonical Fragment Identifier):** padrão técnico que poderia dar âncora estável ao EPUB, mas suporte é fraco entre leitores reais (Kindle não usa, Boox parcial). Rejeitado por imaturidade de adoção.
- **Markdown puro como canônico (sem PDF):** se fôssemos extrair texto do PDF e armazenar como markdown no vault. Perde estrutura visual (figuras, tabelas, equações), e o original deixa de ser referenciável. Rejeitado.

## Referências
- `ARCHITECTURE.md` (Guardrail #2, Guardrail #3, Guardrail #7)
- ADR-002 (conversor `loc→page` decorre dessa decisão)
- `transcricao-mdcu-jailbreak-kindle.md` (turnos 7–8, onde a virada Zotero+dual-format foi cristalizada)
