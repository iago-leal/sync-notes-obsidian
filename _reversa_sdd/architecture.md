# Arquitetura — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Architect em 2026-07-02.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA.

## Visão geral

`synctotes` é uma **CLI local, determinística e sem rede em runtime** que centraliza anotações de leitura de quatro devices num único destino: o vault Obsidian. A arquitetura operacional é maior que o código — plugins Obsidian, Syncthing e Send-to-Kindle fazem parte do pipeline, mas só a **conversão Kindle/Boox → vault** é responsabilidade deste pacote 🟢.

O estilo é **pipeline em camadas com núcleo funcional**: parsers puros (entrada) → resolver determinístico (domínio, futuro) → writer idempotente (saída, futuro), com contratos imutáveis (`frozen dataclasses`) entre as camadas. Paradigma declarado: funcional/procedural com dados imutáveis, em vez de OOP — ganho de coesão para um pipeline de transformação 🟢 (código) 🟡 (justificativa).

```
┌────────────────────────── entrada ──────────────────────────┐
│ kindle.parse_clippings      amazon_export.parse_export_pdf  │
│ (My Clippings.txt)          (PDF Caderno de anotações)      │
│ boox.* 🔴 stub              pdf.extract_pages (suporte)     │
└──────────────────────────────┬───────────────────────────────┘
                               │ dataclasses frozen
┌────────────────────────── domínio ───────────────────────────┐
│ resolver loc→page 🔴 não implementado (kindle.py futuro)     │
│ contrato: types.MatchResult (found/ambiguous/no_match)       │
└──────────────────────────────┬───────────────────────────────┘
                               │ MatchResult
┌────────────────────────── saída ─────────────────────────────┐
│ obsidian.py 🔴 stub — callouts append-only, idempotentes     │
│ cli.py 🔴 stub — Typer + rich + --dry-run                    │
└──────────────────────────────────────────────────────────────┘
```

## Containers (resumo; diagramas em `c4-*.md`)

| Container | Tecnologia | Papel | Estado |
|---|---|---|---|
| CLI `synctotes` | Python 3.12, Typer | Único container de código do projeto | parsers prontos; resolver/writer/CLI 🔴 |
| Vault Obsidian | Markdown + Obsidian Sync | Destino único; estado do sistema (sem banco) | externo, existente |
| Biblioteca de livros | PDFs canônicos + EPUBs, Syncthing | Fonte dos PDFs para o resolver e âncoras | externa, existente |
| Devices de leitura | Kindle Colorsoft, Boox, iPad, macOS | Origem das anotações | externos |

## Integrações externas 🟢

Nenhuma API de rede. Todas as integrações são **por arquivo**:

| Integração | Direção | Formato | Protocolo |
|---|---|---|---|
| `My Clippings.txt` | entrada | texto (blocos `==========`) | cópia manual via USB 🟡 |
| Export Amazon | entrada | PDF formatado | e-mail → arquivo local |
| Export KOReader/Boox | entrada | Markdown 🔴 formato não fixado | Syncthing 🟡 |
| PDF canônico | entrada (leitura) | PDF | filesystem (biblioteca Syncthing) |
| Vault Obsidian | saída | Markdown com callouts `[[livro.pdf#page=X]]` | filesystem (append-only) |
| `obsidian-pdf-plus` | paralela (não passa pela CLI) | anotações diretas no vault | plugin Obsidian |

## Decisões estruturantes (ver `adrs/000-indice.md`)

- PDF canônico / EPUB transporte (ADR-004) — define o formato do link e a necessidade do resolver.
- Determinístico-first com `MatchResult` fixado (ADR-002) — LLM só em v2, via decorator.
- Sem banco de dados: idempotência derivada do conteúdo do vault 🟢.
- Gate de Blast Radius (ADR-006): `traceability/` na raiz do repo protege células críticas.

## Dívidas técnicas

| # | Dívida | Severidade | Evidência |
|---|---|---|---|
| 1 | **CI sem lint/testes/audit**: ARCHITECTURE.md promete `pip-audit` a cada PR, mas só existem workflows do Claude; guardrails dependem do pre-commit local | Alta 🟡 | `.github/workflows/` |
| 2 | Coração do sistema (resolver `loc→page`) inexistente — todo valor de negócio depende dele | Alta 🟢 | `kindle.py` docstring |
| 3 | Duplicação de tabelas de meses PT (kindle `_PT_BR_MONTHS` × amazon_export `_MONTHS_PT`) e de extração de texto (pdf.extract_pages × amazon_export._extract_full_text) | Baixa 🟢 | código |
| 4 | Descarte silencioso de blocos malformados no parser contradiz guardrail #13 (log via rich) — conciliação prevista para a camada CLI | Média 🟢 | `kindle.py:102` |
| 5 | `ARCHITECTURE.md` desatualizado em pontos: prevê `test_obsidian.py`/`test_boox.py` inexistentes, não menciona `amazon_export.py` na estrutura | Média 🟢 | diff estrutura real |
| 6 | Datas parseadas como `datetime` naive, sem timezone | Baixa 🟢 | `kindle.py:239` |
| 7 | Matrizes de rastreabilidade (`traceability/`) exigem atualização manual contínua; risco de deriva em manutenção intermitente | Média 🟡 | ADR-006 |

## Qualidades sistêmicas

| Qualidade | Situação |
|---|---|
| Testabilidade | 🟢 alta nos parsers (funções puras, fixtures sintéticas + real) |
| Reprodutibilidade | 🟢 uv.lock commitado, versões pinadas |
| Observabilidade | 🔴 ainda nada de rich/logs — chega com a CLI |
| Segurança de dados | 🟢 por design: local-only, append-only, PDFs intocados |
| Performance | 🟢 fora de escopo declarado (≤1000 highlights/livro, ≤50 livros) |
