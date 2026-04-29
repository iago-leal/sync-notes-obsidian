# Sessão 2026-04-29 — jailbreak-kindle (inicial)
Tentativas de Reenquadramento: 0/2

## F1 Preparação

**Gatilho de Conformidade — verificação:**
- ARCHITECTURE.md: AUSENTE
- Setup materializado (manifesto + lock + estrutura): AUSENTE
- Repositório git: NÃO inicializado
- RSOP: AUSENTE (primeiro ciclo no projeto)

**Estado:** F1 INTERROMPIDA. Diretório criado hoje (2026-04-29), totalmente vazio. Não há contrato técnico extraído nem materializado.

**Anamnese pendente antes de delegar ao project-init:** o nome "jailbreak-kindle" é ambíguo quanto à natureza do projeto:
- (a) projeto de software (escrever scripts/ferramentas próprias) → project-init aplica em cheio
- (b) repositório de notas/documentação sobre processo manual → project-init não aplica (não há stack)
- (c) fork/análise de software de terceiros (ex: KOReader, JailBreak Bridge) → project-init com escopo de análise/integração

Decisão: fazer **uma pergunta aberta** ao usuário (F2 mínima) para determinar tipo, antes de invocar /project-init.

**Vieses percebidos:**
- diretório vazio + nome técnico → tentação de assumir "é projeto de software" e ir direto para stack
- "jailbreak" como termo carregado → tentação de levantar bandeiras éticas onde não há sinal de uso ilegítimo (Kindle do próprio usuário, prática amplamente documentada)

**Reenquadramento pendente:** N/A (primeiro ciclo).

## F2 Escuta
S:
- **Demanda aparente inicial:** "jailbreak Kindle" / escrever software próprio para Kindle (escopo "a")
- **Demanda real (após escuta):** sincronizar ebooks **e** anotações de ebooks entre Kindle + Obsidian + outros devices. Workflow multi-device de personal knowledge management.
- **Reenquadramento F2 (não conta para Disjuntor — ainda não estamos em F6):** "jailbreak Kindle" era cartão de visita / hipótese de solução do próprio usuário. O problema-fim é PKM com sync de ebooks+annotations. Jailbreak é meio, não fim.
- **Hardware:** Kindle Colorsoft, firmware 5.19.2.
- **Constraint:** kindle-alvo NÃO é descartável. Conteúdo dele é. Mas precisa voltar a funcionar como Kindle normal se algo der errado → fallback de recuperação obrigatório, snapshot antes de qualquer ação destrutiva.
- **Ambiguidade pendente (preciso clarificar antes de F4):** o que significa "ebook no Obsidian"? (α) sync de progresso, (β) arquivos replicados, (γ) índice/metadata no vault, (δ) tudo junto?

## F3 Exploração
O:
- **Jailbreak Colorsoft 5.19.2:** NÃO existe hoje (abr/2026). KindleModding confirma: 5.19+ sem jailbreak. Scribe Colorsoft 5.19.1 teve exploit em jan/2026 (scam.net) mas ainda é exploit, não jailbreak funcional. Caminho fechado por enquanto.
- **KOReader no Colorsoft:** issue #14285 aberto — instalador não reconhece GR7455 (modelo do Colorsoft). Mesmo com jailbreak, hoje, não roda. Suporte a cor experimental.
- **Conexão USB do Colorsoft:** MTP (não Mass Storage). Acesso a `My Clippings.txt` via cabo OK no Windows nativo; Mac requer OpenMTP ou Send-to-Kindle app.
- **Plugin Obsidian existente:** `hadynz/obsidian-kindle-plugin` — sync por (a) login em read.amazon.com (livros Amazon) ou (b) upload do `My Clippings.txt` (qualquer livro, incluindo sideloaded). Maduro, mantido.
- **Whispersync nativo:** sync de progresso de leitura entre Kindle/Apps Amazon já é nativo para livros Amazon. Sem código.
- **Calibre + Calibre-Web:** caminho clássico para biblioteca pessoal de ebooks multi-device sem jailbreak. Send-to-Kindle ou cabo para Kindle; OPDS para celular/desktop.
- **Rastreio de segurança (preliminar):**
  1. Dados sensíveis: anotações pessoais — sensíveis para o usuário, mas só dele. Sem PII de terceiros.
  2. Auth/autz: SE caminho for via read.amazon.com, sessão Amazon fica exposta a outros plugins do Obsidian (alerta documentado pelo próprio plugin). `[M]`.
  3. Input externo: parser de My Clippings.txt = input de arquivo confiável (próprio dispositivo). OK.
  4. Dependências: a definir conforme stack escolhida.
  5. Segredos: SE houver login Amazon, credentials só via mecanismo seguro (não em código).

## F4 Avaliação

### Reformulação canônica do problema (após terceira clarificação — Zotero + dual-format)

> "Vault Obsidian é o destino único de todas as anotações de livros, vindas de leitor nativo de cada device. Cada livro tem versão PDF (canônica, com âncoras de página) e versão EPUB (para leitura confortável no Kindle/Boox-reflow). Anotações vindas do Kindle (em location de EPUB) passam por um conversor `loc → page` antes de virarem callout no vault, para que o link de volta sempre aponte para o PDF canônico."

**Refinamento crítico (terceira escuta):** PDFs no Kindle são experiência ruim → Kindle SEMPRE lê EPUB. Logo, biblioteca tem o mesmo livro em DOIS formatos. Pipeline do Kindle precisa traduzir `location EPUB → page PDF` para que o link no vault aponte para o PDF canônico.

**Modelo de fluxo (4 caixas):**
1. **Biblioteca:** `livro.pdf` (canônico, vault ou path linkado) + `livro.epub` (variante de leitura). Sync via iCloud/Syncthing distribui PDF+EPUB para macOS/iPad/Boox; Send-to-Kindle entrega EPUB ao Kindle.
2. **Captura por device:**
   - macOS/iPad: pdf-plus → callout com âncora exata
   - Boox: KOReader/leitor Boox export → callout (página)
   - Kindle: My Clippings.txt → CONVERSOR loc→page → callout (página)
3. **Vault:** notas markdown com callouts contendo texto + ref ao livro + link `[[livro.pdf#page=X]]`.
4. **Sync de anotações:** depende da camada de sync escolhida em F5 (vault no iCloud/Obsidian Sync/Syncthing/git).

**Decisão técnica do conversor loc→page (a refinar em F5):**
- Caminho determinístico-first: My Clippings traz texto do highlight → fuzzy text-search no texto extraído do PDF (`pdfminer`/`pdfplumber`) → retorna página. Cobre 90% dos casos.
- LLM local como fallback: para snippets ambíguos, curtos, ou quando OCR do PDF está sujo.
- Usuário sugeriu LLM local de cara — ofereci o determinístico-first como alternativa mais barata/robusta. Decisão final fica para F5.

**Implicações da virada:**
- Jailbreak NÃO é necessário. Kindle anota normalmente em EPUB; cola pega My Clippings + traduz para página do PDF.
- Granularidade do link varia por device: macOS/iPad com pdf-plus = trecho exato; Kindle/Boox = página.
- PDF é canônico no vault sempre; EPUB é variante de transporte para Kindle/Boox-reflow.
- Readwise: componente possível do pipeline, não o pipeline inteiro (não cobre Boox; link de volta dele aponta para read.amazon.com, não para PDF do vault).

### Mapa do terreno (4 devices)
- macOS: Obsidian + pdf-plus → 1ª classe em PDF.
- iPad: Obsidian iOS + pdf-plus, ou PDF Expert/GoodReader → 1ª classe em PDF.
- Boox: Android, leitor nativo + KOReader Android → 1ª classe em PDF e EPUB.
- **Kindle Colorsoft: outlier.** Não abre EPUB nativamente. Abre PDF mas anotações ficam em camada Amazon (não no arquivo). Sem jailbreak, ilha.

### Gargalo central
Kindle Colorsoft sem jailbreak quebra homogeneidade do workflow. Anotação no Kindle ≠ PDF annotation standard. Caminho de volta (Kindle → arquivo mestre) é frágil.

### Pergunta-pivô (decisão pendente — bloqueia F5)
- **K1 — Kindle 1ª classe:** anotar no Kindle deve fluir para arquivo mestre. Bloqueado hoje por firmware (sem jailbreak Colorsoft 5.19.2). Cola manual frágil é alternativa única.
- **K2 — Kindle 2ª classe:** Kindle lê PDFs com anotações vindas de outros devices, mas anotações feitas no Kindle vão pro vault como texto separado (via My Clippings + plugin), não como annotation no PDF. **Solúvel hoje sem jailbreak.**
- **K3 — Kindle fora do workflow PDF/EPUB primário:** Kindle só pra livros Amazon (Whispersync nativo). Workflow de PDF/EPUB anotado vive em iPad+Boox+macOS. **Mais simples.**

### Decisões secundárias (dependem de K1/K2/K3)
- Lingua franca: **recomendação PDF** (PDF annotations standard são cross-platform; EPUB não tem standard universal de anotação embebida).
- Camada de sync: iCloud / Syncthing / Obsidian Sync / git — trade-offs com Boox e Kindle.
- Biblioteca-mestre: Calibre vs estrutura de pastas pura.

### Rastreio de segurança (atualizado)
- 1. Dados sensíveis: anotações pessoais. Sem PII de terceiros. OK.
- 2. Auth/autz: depende da camada de sync. iCloud = Apple ID (já gerenciado). Syncthing = sem auth externo. Git em provider público = atenção a privacidade do conteúdo das anotações. `[L]`-`[M]`.
- 3. Input externo: parsers (My Clippings, sidecar files) = arquivos de origem confiável (próprio dispositivo). OK.
- 4. Dependências: a definir.
- 5. Segredos: depende da camada de sync.

## F5 Plano
(bloqueado — aguarda resposta K1/K2/K3 do usuário)

## F6 Execução

## F4 Avaliação

## F5 Plano

## F6 Execução
