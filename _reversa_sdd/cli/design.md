# Design — unit `cli` (stub — desenho alvo)

> Reversa Writer, 2026-07-02.

## Estado atual 🟢

`main() -> int` imprime versão + aviso e retorna 0. Serve para verificar o console script end-to-end desde o setup.

## Desenho alvo 🟡 (inferido de ADR-005 + guardrails; sem código)

```
app = typer.Typer()

@app.command()  # assinaturas 🔴 a decidir
def ingest_kindle(clippings: Path, vault: Path, library: Path, dry_run: bool = False): ...
def ingest_amazon(export_pdf: Path, vault: Path, dry_run: bool = False): ...
def ingest_boox(export_md: Path, vault: Path, dry_run: bool = False): ...
```

Responsabilidades da casca (e só dela):
1. Validação de paths de entrada (Typer/type hints).
2. Log estruturado via rich — inclusive contagem de blocos descartados pelos parsers (conciliação do guardrail #13 com o descarte silencioso do `kindle.py`).
3. Propagação da flag `--dry-run` ao writer.
4. Exit codes: 0 sucesso (mesmo com itens pulados 🟡), ≠0 para falha de I/O ou vault inacessível 🔴 política não definida.

## Restrições

- Nenhuma regra de negócio aqui: parsing, matching e escrita vivem nos módulos de domínio 🟢 (contrato).
- UTF-8 explícito em qualquer leitura de arquivo (guardrail #15) 🟢.
