# Spec Impact Matrix — sync-notes-obsidian

> **Ground Truth (Matriz de Blast Radius)**
> Compilado conforme ADR-006. Atua como **Gate Disjuntor**.
> Legenda: 🟥 **Impacto Direto** (Bloqueia sem ADR) | 🟨 **Indireto** (Exige atenção) | 🟩 **Livre** (Sem impacto)

---

## 1. Matriz: Alvo de Mudança × Componente Impactado

| Proposta de Modificação ↓ / Impactado → | cli.py | kindle.py | boox.py | pdf.py | obsidian.py | types.py | Vault Obsidian |
|---|---|---|---|---|---|---|---|
| **Mudar estrutura de tipagem (MatchResult)** | 🟥 | 🟥 | 🟥 | 🟩 | 🟥 | 🟥 | 🟩 |
| **Mudar motor Fuzzy (Rapidfuzz)** | 🟩 | 🟥 | 🟥 | 🟩 | 🟩 | 🟩 | 🟨 |
| **Mudar formato de exportação de Callout** | 🟩 | 🟩 | 🟩 | 🟩 | 🟥 | 🟩 | 🟥 |
| **Adicionar Fallback LLM (v2)** | 🟨 | 🟥 | 🟥 | 🟩 | 🟩 | 🟨 | 🟩 |
| **Excluir anotações antigas (Romper Append-Only)** | 🟥 | 🟩 | 🟩 | 🟩 | 🟥 | 🟩 | 🟥 |
| **Trocar parser EPUB** | 🟩 | 🟥 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |

---

## 2. Leitura do Disjuntor

### Mudanças Restritas (Alta Fricção):
Qualquer alteração que proponha modificar a tipagem central (`MatchResult`) afeta todo o pipeline, do conversor até a CLI. Isso acionará células 🟥 e **deve falhar a automação orgânica**, exigindo aprovação via ADR. O mesmo vale para mexer na interface de gravação no Vault (`obsidian.py`) rompendo o Append-Only.

---

## 3. Autoridade e Enforcement
Esta matriz **não é uma sugestão**. Ela é a fronteira de controle de sanidade. Agentes de IA são proibidos de alterar componentes com impacto 🟥 se a modificação não estiver ancorada numa nova ADR ou sessão explícita autorizando o desvio.
