# ADR 005: Adoção de Typer, Rich e Pre-commit para Resiliência

**Data:** 2026-05-03

## Contexto
O projeto lida com *fuzzy matching* e manipulação do Obsidian Vault. Falhas silenciosas ou interfaces frágeis de CLI podem causar perda de dados ou má experiência (ex: anotações injetadas nos PDFs errados). Precisamos garantir tipagem de borda, logs amigáveis, cobertura de testes e que apenas código nos padrões entre na `main`.

## Decisão
- Adoção de `typer` para gerar a CLI a partir dos type hints nativos, eliminando o boilerplate e risco de parsing de `argparse`.
- Adoção de `rich` para formatar os logs no terminal de forma legível.
- Adoção de `pytest-cov` e `pre-commit` (`ruff`, `mypy`) para garantir que o código submetido tem a qualidade mínima exigida pelo contrato e evitar acumular débitos de formatação.
- Guardrails operacionais estabelecidos (Append-only no Vault, dry-run mandatório).

## Consequências
- Aumento sutil na base de dependências.
- Desenvolvimento local tem uma barreira estrita (`pre-commit`), aumentando a fricção inicial mas garantindo a qualidade de longo prazo.
- Typer amarra a arquitetura da CLI aos type hints, o que já era uma exigência do projeto (via `mypy`).
