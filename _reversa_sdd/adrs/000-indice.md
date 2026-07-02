# Índice de ADRs — jailbreak-kindle

> Gerado pelo Reversa Detective em 2026-07-02.
> O projeto **já mantém ADRs formais** em `docs/adr/` (fonte autoritativa). Este índice os cataloga e adiciona ADRs **retroativos** — decisões evidentes no código/histórico que ainda não têm registro formal. Retroativos ficam aqui em `_reversa_sdd/adrs/`; promovê-los a `docs/adr/` é decisão do mantenedor.

## ADRs formais existentes (docs/adr/) 🟢

| # | Título | Data | Essência |
|---|---|---|---|
| ADR-001 | Python 3.12+ com uv | 2026-04-29 | Ecossistema PDF/texto mais maduro; volume pequeno dispensa performance |
| ADR-002 | Determinístico-first, `MatchResult` tipado | 2026-04-29 | Sem LLM no MVP; fallback v2 via decorator sobre interface fixada desde o dia 1 |
| ADR-003 | Syncthing (biblioteca) + Obsidian Sync (vault) | 2026-04-29 | Duas camadas de sync independentes; Kindle via Send-to-Kindle |
| ADR-004 | PDF canônico, EPUB transporte | 2026-04-29 | Página de PDF é estável; location de EPUB não; callouts sempre `[[livro.pdf#page=X]]` |
| ADR-005 | Typer, Rich e pre-commit | 2026-05-03 | Tipagem de borda na CLI, logs legíveis, barreira de qualidade local |
| ADR-006 | Motor de rastreabilidade semântica | 2026-05-03 | Matrizes code-spec e blast-radius; células 🟥 exigem ADR prévio |

## ADRs retroativos (este diretório)

| # | Título | Origem da evidência |
|---|---|---|
| [007](007-amazon-export-segunda-fonte-ingest.md) | Export Amazon como segunda fonte de ingest, com fixture real como contrato de regressão | commit `8ee7284`, `amazon_export.py`, `test_amazon_export.py` |
| [008](008-contrato-antes-do-codigo.md) | Contrato antes do código (spec-first + TDD) | commits `90afe8f`, `164f155`; ARCHITECTURE.md § Histórico |
