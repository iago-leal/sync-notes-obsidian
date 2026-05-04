# RSOP: Dados Base

## Identificação
- **Projeto:** sync-notes-obsidian
- **Propósito:** Vault Obsidian é destino único de todas as anotações de livros, vindas de leitor nativo de cada device (macOS, iPad, Boox, Kindle Colorsoft). Conversão via fuzzy text matching de location EPUB para página PDF.
- **Autor/Responsável:** Iago Leal
- **Repositório:** https://github.com/iago-leal/sync-notes-obsidian

## Stack Atual
- Python 3.12+ (uv manager)
- CLI com Typer e Rich
- Pre-commit (ruff, mypy --strict)
- Testes com pytest-cov

## Guardrails e Invariantes
1. Vault é "Append-Only" (proibido deletar arquivos locais ou modificar os PDFs canônicos).
2. Interface Tipada (`MatchResult`) e CLI (`Typer`).
3. Degradação Graciosa (pular anotações malformadas).
4. `--dry-run` mandatório.
5. Operações devem usar explícito `encoding="utf-8"`.
