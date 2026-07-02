# Permissões — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Detective em 2026-07-02.

## RBAC/ACL de usuários

**Não existe.** Sistema single-user, CLI local, sem autenticação, sem papéis 🟢. O único "usuário" é o mantenedor (Iago), operando no próprio filesystem.

## Matriz de permissões do *software* sobre o filesystem

O modelo de permissões relevante aqui é o que o **pipeline pode fazer com os dados** — invariantes de segurança do vault (guardrails #7, #12, #14 do ARCHITECTURE.md) 🟢:

| Recurso | Ler | Criar | Anexar | Modificar | Deletar |
|---|---|---|---|---|---|
| PDF canônico (biblioteca) | ✅ | ❌ | ❌ | ❌ **nunca** (guardrail #7) | ❌ |
| EPUB de transporte | ✅ | ❌ | ❌ | ❌ | ❌ |
| `My Clippings.txt` / export Amazon / export Boox | ✅ | ❌ | ❌ | ❌ | ❌ |
| Arquivos `.md` do vault | ✅ | ✅ | ✅ callouts | 🟡 só para anexar | ❌ **nunca** (`os.remove` proibido, guardrail #12) |
| Rede em runtime | ❌ (guardrail #8) | — | — | — | — |

Regras associadas:

- Toda operação de escrita responde a `--dry-run` (guardrail #14) 🟢.
- Escrita idempotente: hash de (livro, snippet normalizado) impede duplicação (guardrail #6) 🟢.
- I/O com `encoding="utf-8"` explícito (guardrail #15) 🟢.

## Enforcement

| Mecanismo | Status |
|---|---|
| Declaração nos guardrails + docstrings dos stubs | 🟢 existente |
| Gate de Blast Radius (`traceability/spec-impact-matrix.md`, ADR-006): mudanças em células 🟥 exigem ADR prévio | 🟢 existente |
| Enforcement em código (writer append-only, dry-run) | 🔴 LACUNA — depende da implementação de `obsidian.py`/`cli.py` (F6.a) |
