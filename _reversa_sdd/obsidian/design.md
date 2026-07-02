# Design — unit `obsidian` (stub — desenho alvo)

> Reversa Writer, 2026-07-02. Nada implementado; desenho derivado dos guardrails 🟡.

## Responsabilidades

1. **Normalização do snippet** para o hash de idempotência 🔴 (regras não definidas: caixa? espaços? pontuação? — ver questions.md).
2. **Cálculo do hash** de (livro, snippet normalizado) 🔴 (algoritmo não definido; requisito: estável entre execuções e plataformas — evitar `hash()` nativo do Python, que é salted).
3. **Detecção de existência**: verificar se o hash já está no vault antes de escrever 🟡 (provável: hash embutido no callout como comentário/atributo, escaneável).
4. **Render do callout** 🔴 template não definido; insumos disponíveis por anotação: texto, nota anexada, cor, data, página resolvida, confidence.
5. **Escrita append-only** com `encoding="utf-8"`, honrando `--dry-run`.

## Esboço de interface 🟡 (proposta do Reversa, não código)

```python
def write_callouts(
    annotations: Sequence[ResolvedAnnotation],  # 🔴 tipo unificado ainda não existe
    vault: Path,
    *,
    dry_run: bool = False,
) -> WriteReport:  # criados, pulados (hash existente), erros
```

## Riscos de design

- 🟡 A idempotência baseada em conteúdo exige escanear o vault (ou índice) a cada execução; com vault grande, custo cresce — aceitável no volume-alvo (≤50 livros).
- 🟡 Concorrência com Obsidian Sync: escrever enquanto o Sync roda pode gerar conflitos de arquivo; mitigação não discutida em nenhum documento 🔴.
