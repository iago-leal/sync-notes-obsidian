# Requirements — unit `boox` (stub — spec de alvo)

> Reversa Writer, 2026-07-02 · Fontes: docstring de `boox.py`, ARCHITECTURE.md (componentes externos). Implementação F6.a 🔴.

## Objetivo

Ingerir exports de anotações do KOReader (Boox) para o mesmo pipeline dos demais devices 🟢 (contrato).

## Requisitos funcionais

| ID | Requisito | MoSCoW | Confiança |
|---|---|---|---|
| RF-01 | Parsear export do KOReader em markdown para estrutura equivalente a `KindleClipping` | Must | 🟡 docstring |
| RF-02 | Formato de entrada: `evernote_export` ou `markdown_export` do KOReader | Must | 🔴 plugin não decidido |
| RF-03 | Anotações do Boox em PDF já têm página → dispensam resolver; em EPUB reflow → precisam de resolver | Should | 🟡 inferido do modelo PDF/EPUB (ADR-004) |

## Critérios de aceitação

🔴 Não deriváveis: sem formato de entrada fixado nem fixture, qualquer cenário seria invenção. Pré-requisito: exportar um arquivo real do KOReader do Boox e commitá-lo como fixture (mesmo padrão do export Amazon).

## Dependências

Consome: export markdown via Syncthing 🟡. Consumido por: CLI. Coordenadas EPUB passam pelo resolver 🟡.
