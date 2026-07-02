# Confidence Report — jailbreak-kindle (`synctotes`)

> Reversa Reviewer, 2026-07-02 · Fechamento da extração (doc_level: completo).
>
> **Adendo 2026-07-02:** as 22 perguntas do `questions.md` foram respondidas (aprovação em bloco pelo mantenedor). As lacunas 🔴 das units stub deixam de ser "sem decisão" e passam a "decidido, não implementado" — os percentuais abaixo refletem o momento do fechamento e permanecem como registro.

## Verificações empíricas do Reviewer

| Verificação | Resultado |
|---|---|
| Suíte de testes | ✅ 29/29 verdes (`uv run pytest --cov=synctotes`) |
| Cobertura | 91% total — kindle 92%, amazon_export 95%, pdf/types/`__init__` 100%, stubs 0% |
| Caso de borda regex do título | ✅ verificado e reclassificado 🟡→🟢 (`kindle/design.md`) |
| Contagem de testes no code-analysis | corrigida 27→29 |
| Units × módulos do surface.json | 7/7 — nenhuma unit faltante |
| Code/Spec Matrix | 100% do código-fonte mapeado |
| Revisão cruzada externa | não realizada (engine externa indisponível na sessão) |

## Confiança por artefato

| Artefato | 🟢 | 🟡 | 🔴 | Leitura |
|---|---|---|---|---|
| inventory.md / dependencies.md | alto | 2 | 0 | fatos de manifesto e lock |
| code-analysis.md / data-dictionary.md / flowcharts | alto | 3 | 3 | extração direta; 🔴 são os stubs |
| domain.md | alto | 4 | 7 | guardrails 🟢; lacunas concentradas no futuro |
| state-machines.md / permissions.md | alto | 3 | 3 | enforcement futuro é a lacuna |
| architecture.md / c4 / erd / matrizes | alto | 6 | 2 | síntese fiel; inferências sinalizadas |
| units implementadas (kindle, amazon_export, pdf, types) | **~90% 🟢** | poucos | 1 cada | contratos operacionais prontos para reimplementação |
| units stub (cli, obsidian, boox) | ~30% 🟢 (guardrails) | médio | **alto** | specs de alvo; respostas do questions.md decididas em 2026-07-02 (ver adendo) |

## Percentual geral estimado

Ponderando pelos artefatos: **≈70% 🟢 · 18% 🟡 · 12% 🔴**.

A leitura correta do 12% vermelho: **não é ignorância sobre o código existente** (este está ~95% 🟢) — é o retrato fiel de um projeto cujo coração (resolver, writer, CLI real) ainda não foi construído. As lacunas estão nomeadas, numeradas (Q1–Q22) e, desde 2026-07-02, **todas decididas** (aprovação em bloco; ver `questions.md` e `gaps.md`).

## Reclassificações desta revisão

| De → Para | Item | Motivo |
|---|---|---|
| 🟡 → 🟢 | Comportamento da regex de título com parênteses (`kindle/design.md`) | Verificado empiricamente |
| (correção) | 27 → 29 testes (`code-analysis.md`) | Execução real da suíte |

## Aptidão para os próximos fluxos

- **`/reversa-reconstructor`** (reimplementação): apto para as 4 units implementadas; Q1–Q14 respondidas — os stubs só aguardam a fixture real do `markdown_export` (boox).
- **`/reversa-forward`** (evolução): apto — a feature natural é "implementar resolver `loc→page`" partindo de `kindle/requirements.md` RF-09.
- **`/reversa-migrate`**: aplicável, mas prematuro — o sistema ainda não completou o próprio MVP.
