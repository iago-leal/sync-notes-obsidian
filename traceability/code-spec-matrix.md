# Code/Spec Matrix — sync-notes-obsidian

> **Ground Truth (Ponto de Partida Retroativo)**
> Compilado via varredura integral para estabelecer a fundação de rastreabilidade do projeto.
> Status: **LOCKED** (Sob proteção da ADR-006)

---

## 1. Matriz: Arquivo Físico → Especificação de Design (SDD / ADR)

| Arquivo (Código) | Spec Correspondente | Status de Cobertura |
|---|---|---|
| `src/synctotes/cli.py` | `ARCHITECTURE.md` (CLI / Typer) | 🟢 Coberto |
| `src/synctotes/kindle.py` | `ADR-002` (Conversor determinístico `loc→page`) | 🟢 Coberto |
| `src/synctotes/boox.py` | `ARCHITECTURE.md` (Ingest Boox) | 🟢 Coberto |
| `src/synctotes/pdf.py` | `ADR-004` (PDF Canônico) | 🟢 Coberto |
| `src/synctotes/obsidian.py` | `ARCHITECTURE.md` (Escritor Vault / Idempotência) | 🟢 Coberto |
| `src/synctotes/types.py` | `ADR-002` (Interface `MatchResult`) | 🟢 Coberto |
| `.pre-commit-config.yaml` | `ADR-005` (Adoção de Pre-commit e Typer) | 🟢 Coberto |

---

## 2. Matriz Inversa: Visão por Regra de Negócio

| Regra de Negócio (Guardrail) | Implementação no Código |
|---|---|
| Append-Only Vault | `src/synctotes/obsidian.py` |
| Idempotência das Anotações | `src/synctotes/obsidian.py` |
| Fallback para texto puro sem PDF | `src/synctotes/obsidian.py` e `src/synctotes/kindle.py` |
| Extração preservando Layout | `src/synctotes/pdf.py` |

---

## 3. Lacunas Mapeadas (Technical Debt)

Nenhuma lacuna arquitetural ativa. O mapeamento cobre 100% dos *scripts* operacionais da CLI.
