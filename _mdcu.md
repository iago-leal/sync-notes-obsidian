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

## F5 Plano (decisão compartilhada — em andamento)

### Componentes técnicos derivados
1. Captura macOS/iPad: pdf-plus existente (pronto)
2. Captura Boox: KOReader Android export (pronto, integrar)
3. Captura Kindle: My Clippings + obsidian-kindle-plugin + conversor loc→page (NOVO — coração do projeto)
4. Sync biblioteca: escolha de camada
5. Sync vault: escolha de camada (separado de biblioteca)
6. Operação: manual (A) vs automática (B)

### Alternativa A — MVP-minimal (CLI Python determinística)
- Python 3.12+ + uv + pdfplumber + rapidfuzz + ebooklib
- CLI pura, sem LLM, sem daemon, sem plugin
- Conversor loc→page determinístico-first; snippets ambíguos viram log + ajuste manual
- Custo: 3-5 dias código + 1-2 dias tests
- Pros: reversível, determinístico, manutenção mínima
- Cons: manual; cobre ~80-90% dos casos
- Rastreio segurança: OK em todos os 5 itens

### Alternativa B — Robusto (CLI + LLM-fallback + watcher + plugin)
- Tudo de A + Ollama (LLM local fallback) + launchd job + plugin Obsidian TypeScript
- Custo: 2-3 semanas
- Pros: quase autônomo; LLM cobre 10-20% restante
- Cons: 4-5× custo; mais superfície de bug; LLM = não-determinismo
- Rastreio segurança: OK com cuidado em LaunchAgent permissions

### Recomendação do agente
**A com porta deliberadamente aberta para B.** Começar determinístico-manual, observar fricção real, só então adicionar pedaços de B onde a dor justificar. Decisão reversível com feedback loop curto.

**Alerta sobre LLM-fallback:** usuário sugeriu em F4. Recomendação contra usar de início — determinístico-first até medir onde falha. Se for preferência tecnológica (vontade de mexer com LLM local), declarar como tal — legítimo, mas distinguir de necessidade técnica.

### Decisões secundárias propostas
- S1 sync biblioteca: **Syncthing** recomendado (cobre Boox; iCloud só Apple)
- S2 sync vault: **Obsidian Sync** recomendado (conflict resolution desenhado para o caso)
- S3 linguagem: **Python 3.12+ com uv** (ecossistema PDF/text mais maduro; uv é estado da arte)
- S4 estrutura: src/synctotes/ com cli.py + kindle.py + boox.py + obsidian.py + pdf.py

### Decisões fechadas (F5.1–F5.5)
- F5.1: Alternativa A com porta deliberadamente aberta para B (decisão reversível, feedback loop curto)
- F5.2: Syncthing para biblioteca (cobre Boox; iCloud só Apple)
- F5.3: Obsidian Sync para vault (já pago pelo usuário)
- F5.4: Python 3.12+ com uv
- F5.5: LLM-fallback ABANDONADO no MVP, MAS condição de desenho preservada — interface pública do conversor retorna `MatchResult` tipado (status: found/ambiguous/no_match + candidates) desde a primeira linha. Ponto de extensão via decorator pattern. Custo de adicionar futuro: ~80-100 linhas + 1 dep + 1-2 dias, zero regressão. Decisão: dívida explícita, baixa, com gancho preservado.

### Objetivo SMART do MVP
Pipeline funcional cobrindo 3 caminhos (macOS/iPad já existente; Boox via KOReader export; Kindle via My Clippings + conversor) entregando ≥85% dos highlights de sample de 3 livros como callouts no vault com link de página correto no PDF, em até 2 semanas.

### Responsabilidades
- Usuário: fornecer sample de teste (3 livros — PDF + EPUB + recorte My Clippings); validar callouts; feedback iterativo.
- Agente: implementação, tests, manutenção _mdcu.md/RSOP, ADRs.

### ADRs a registrar (arquivos separados em F6.a)
- ADR-001: Python + uv como stack
- ADR-002: Determinístico-first com MatchResult tipado; LLM-fallback como ponto de extensão futuro (decorator pattern)
- ADR-003: Syncthing biblioteca / Obsidian Sync vault
- ADR-004: PDF como canônico no vault; EPUB como variante de transporte

### Próximo passo
F6.a — retomar /project-init com stack consolidada → ARCHITECTURE.md → /project-setup materializa (pyproject.toml + uv.lock + src/ + .gitignore Python).

## F6 Execução

### F6.a — Setup técnico (CONCLUÍDO, 2026-04-29)

**Gatilho de conformidade da F1 do MDCU agora formalmente satisfeito:** ARCHITECTURE.md presente + setup materializado em disco.

Materialização produzida (commit 90afe8f, pushed em main):
- ARCHITECTURE.md (contrato técnico do project-init)
- pyproject.toml + uv.lock (50 packages, lock determinístico commitado)
- .gitignore expandido para Python (lock preservado conforme guardrail #4)
- src/synctotes/ com 6 módulos: __init__.py, cli.py, types.py (com MatchResult+Candidate tipados conforme guardrail #1), kindle.py, boox.py, obsidian.py, pdf.py
- tests/ com test_smoke.py (3 passing) + fixtures/.gitkeep
- docs/adr/ (vazio, esperando ADR-001 a 004)

Validações verdes: ruff check + format, mypy --strict, pytest, CLI executa.

Modo de execução: monolítico declarado (critério de saída: cookiecutter/copier MDCU-aderente quando existir).

### F6.a — Implementação (em andamento)

**Concluído (commitado em `main`):**
- ✅ ADR-001 a 004 em `docs/adr/` (commit `001764a`)
- ✅ `pdf.py` — `extract_pages` via pdfplumber + 3 tests (commit `164f155`)
- ✅ `kindle.py` — parser My Clippings PT-BR/EN + 15 tests (commit `164f155`)
- ✅ `amazon_export.py` — parser PDF Caderno de anotações + 8 tests com fixture real Quincas Borba (commit `8ee7284`)

**Em revisão (PR #7 aberto, aguardando merge manual do usuário):**
- 🔄 `resolver.py` — `resolve_to_pd_page` determinístico via rapidfuzz + 10 tests (8 com fixture real + 2 unit puros).
  - PR: https://github.com/iago-leal/sync-notes-obsidian/pull/7
  - Commits: `79eff77` (feat) + `d4e698a` (refactor — fixes do `/simplify`)
  - Workflow `claude-review` rodando; precisa `ANTHROPIC_API_KEY` no repo Settings para postar comentário.
  - Closes issue #2 ao mergear.

**Pendente (issues abertas no v0.1.0):**
- ⏳ Issue #3 — `obsidian.py`: writer de callouts idempotentes via hash (guardrail #6)
- ⏳ Issue #4 — `cli.py`: wire-up Typer com subcomandos `ingest amazon-export` / `ingest my-clippings`
- ⏳ Issue #5 — E2E test ≥85% Quincas Borba (critério de fechamento do milestone v0.1.0)
- ⏳ Issue #6 — Documentação no README

**Backlog v0.2.0+ (não bloqueante):**
- `boox.py`: parser de export KOReader Android
- LLM-fallback (ADR-002, decorator pattern sobre MatchResult)
- My Clippings.txt real do usuário (em `tests/fixtures/local/`)

### Pausa — 2026-04-29

Sessão pausada após ~11 commits longitudinais e setup completo de governança (4 milestones, 5 issues, 6 labels custom, workflows Claude Code instalados). MDCU permanece aberto (`_mdcu.md` vivo, F6.a em andamento). Retomar via `/mdcu` lê este arquivo e continua de onde parou. Próxima ação natural ao retomar: confirmar merge do PR #7 e atacar issue #3 (writer Obsidian).

### F6.b — Acompanhamento (a iniciar quando F6.a começar)
Metaprotocolo de observação ativo durante implementação. Releitura periódica de S/O/A/P. Disjuntor 2/2 monitorado.

### F6.c — Tradução de retorno e fechamento (a iniciar ao concluir MVP)
Fechamento da sessão MDCU via /rsop soap → /commit-soap → delete _mdcu.md.

## F6 Execução

## F4 Avaliação

## F5 Plano

## F6 Execução
