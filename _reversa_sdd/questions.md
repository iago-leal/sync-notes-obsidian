# Questions — validação humana (com propostas do Reversa)

> Reversa Reviewer, 2026-07-02 · Atualizado com **propostas-padrão** após decisão do mantenedor de manter o legado.
> Status de cada resposta: ⏳ proposta pendente de veto · ✅ confirmada pelo usuário · ✋ vetada (registrar alternativa).
> Ao confirmar/vetar, as respostas serão propagadas às specs das units e viram 🟢 DECIDIDO.
>
> **2026-07-02 — Aprovação em bloco.** O mantenedor escolheu a rota "validar as respostas" e a opção recomendada de aprovação em bloco; as 22 propostas foram marcadas ✅ e propagadas às units. Qualquer veto posterior pode ser registrado trocando o status para ✋ com a alternativa — a propagação é reversível via git.

## Bloco A — Resolver `loc→page`

**Q1** 🔴 Limiar de score do resolver?
**Resposta ✅:** rapidfuzz `token_set_ratio` (0–100) do snippet contra o texto de cada página. `found` se melhor score ≥ 90 **e** vantagem ≥ 5 pontos sobre o 2º colocado; `ambiguous` se ≥ 75 sem essas condições (candidatos listados); `no_match` se < 75. `confidence = score/100`. Limiares como constantes nomeadas, calibráveis pela fixture real (Quincas Borba: `pd.pdf` + export com 61 anotações — dataset de calibração já commitado).

**Q2** 🔴 Desempate quando o snippet aparece em múltiplas páginas?
**Resposta ✅:** prior de posição relativa — `location/max_location` do livro estima `page/max_page`; vence o candidato com página mais próxima da estimativa, exigindo a mesma vantagem de 5 pontos combinada; persistindo empate, `ambiguous`.

**Q3** 🔴 Resolver em `kindle.py` ou módulo próprio?
**Resposta ✅:** módulo próprio `resolver.py` (coesão: `kindle.py` permanece parser puro; o resolver serve a todas as fontes). Registrar como microdecisão; a docstring de `kindle.py` será atualizada em F6.

**Q4** 🟡 Página do export Amazon coincide com a do PDF canônico?
**Resposta ✅:** não assumir. Toda coordenada (page ou position) passa pelo resolver, usando a página declarada como *hint* (busca começa na vizinhança do prior e só expande se não achar). Se o match confirmar a página declarada, `confidence` alta de graça.

## Bloco B — Writer Obsidian

**Q5** 🔴 Template do callout?
**Resposta ✅:**
```markdown
> [!quote] [[livro.pdf#page=42|p. 42]]
> Texto do destaque…
> — *Nota:* texto da nota anexada (linha presente só se houver)
> %% st:a1b2c3d4e5f60708 · amarelo · 2026-04-01 %%
```
Hash, cor e data no comentário Obsidian (`%% %%`): invisíveis no preview, greppáveis para idempotência. `confidence` não aparece no callout (ruído para leitura); vai só ao log.

**Q6** 🔴 Organização no vault?
**Resposta ✅:** um arquivo por livro em pasta dedicada (`Leituras/<Título Normalizado>.md`), criado pelo pipeline. Nunca fazer append em notas manuais existentes — evita colisão com o fluxo do `obsidian-pdf-plus` e mantém o append-only trivialmente seguro. Pasta configurável no config (Q11).

**Q7** 🔴 Normalização do snippet para o hash?
**Resposta ✅:** Unicode NFC → remoção de hífen de quebra (`-\n` → junção) → colapso de todo whitespace em espaço único → `strip()` → lowercase. **Sem** remover pontuação (preserva unicidade de trechos curtos).

**Q8** 🔴 Algoritmo e armazenamento do hash?
**Resposta ✅:** `sha256(titulo_normalizado + "\n" + snippet_normalizado)` em UTF-8, truncado a 16 hex. Gravado no comentário do callout (Q5). Detecção de duplicata por scan dos `%% st:… %%` do arquivo do livro (volume-alvo torna o scan barato).

**Q9** 🟡 Destino de `ambiguous`/`no_match`?
**Resposta ✅:** seção `## Pendentes` ao final do arquivo do livro: callout sem âncora com o texto e, quando `ambiguous`, as páginas candidatas com scores. Também logado via rich. Nada é descartado silenciosamente.

## Bloco C — CLI

**Q10** 🔴 Superfície de comandos?
**Resposta ✅:** subcomandos por fonte — `synctotes ingest kindle <path>`, `synctotes ingest amazon <path>`, `synctotes ingest boox <path>` — mais `synctotes status` (mostra config e contagens do vault). Sem `sync` monolítico no MVP.

**Q11** 🔴 Localização de vault e biblioteca?
**Resposta ✅:** config file `~/.config/synctotes/config.toml` (campos: `vault`, `library`, `leituras_folder`), com override por flags `--vault/--library`. Sem env vars. Alinha ao princípio "configuração fora do código".

**Q12** 🔴 Exit codes?
**Resposta ✅:** `0` sucesso, inclusive com itens pulados (reportados via rich); `1` erro de execução (I/O, PDF corrompido); `2` configuração inválida (vault/biblioteca inacessíveis). Skips não quebram automação.

## Bloco D — Boox

**Q13** 🔴 Plugin de export do KOReader?
**Resposta ✅:** `markdown_export` — saída já no idioma do vault, sem o envelope ENEX/XML do evernote_export.

**Q14** 🔴 Boox: PDF ou EPUB reflow?
**Resposta ✅:** suportar ambos desde o parser: registrar `coordinate_kind` como no amazon_export. PDF nativo (página direta) dispensa resolver; EPUB reflow passa por ele. A proporção real de uso não precisa ser decidida.

## Bloco E — Menores

**Q15** 🟡 Bookmarks geram callout? **✅** Não — sem texto, sem valor no vault; contados no log da execução.
**Q16** 🟡 Livro sem PDF canônico? **✅** Pular com aviso rich e listar no resumo final; nada é criado.
**Q17** 🟡 Identidade de livro entre fontes? **✅** Título normalizado (regras do Q7) + fuzzy ≥ 90 entre fontes; ASIN, quando presente, gravado como alias no frontmatter do arquivo do livro.
**Q18** 🟡 Fixture EN do export Amazon? **✅** Adiar até existir livro real anotado em EN (YAGNI); RF-11 permanece Could.
**Q19** 🟡 Destaques só-numéricos descartados? **✅** Aceitar o risco documentado (prosa domina o uso); reavaliar se um livro técnico entrar na biblioteca.
**Q20** 🟡 `--dry-run` mostra o quê? **✅** Diff completo: os callouts inteiros que seriam escritos, por arquivo de destino.
**Q21** 🟡 Lock contra Obsidian Sync? **✅** Sem lock no MVP; documentar no README a recomendação de não rodar durante sync ativo. Volume pequeno, escrita rápida, risco aceito.
**Q22** 🟡 Transporte do export Boox? **✅** Pasta de export do KOReader incluída no Syncthing da biblioteca; chega ao macOS sem ação manual.
