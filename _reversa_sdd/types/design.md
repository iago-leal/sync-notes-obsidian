# Design — unit `types`

> Reversa Writer, 2026-07-02.

Módulo de dados puro, sem lógica 🟢:

```python
MatchStatus = Literal["found", "ambiguous", "no_match"]

@dataclass(frozen=True)
class Candidate:
    page: int
    score: float
    excerpt: str

@dataclass(frozen=True)
class MatchResult:
    status: MatchStatus
    page: int | None = None
    confidence: float | None = None
    candidates: tuple[Candidate, ...] = field(default_factory=tuple)
```

## Decisões 🟢

1. **Literal em vez de Enum** para `MatchStatus`: comparação por string simples nos consumidores, exaustividade verificável pelo mypy.
2. **`tuple` em vez de `list`** para `candidates`: imutabilidade profunda.
3. **Estados ilegais não são prevenidos por tipo** (ex.: `found` sem `page` é construível) 🟡 — validação ficará nos produtores; documentado só em docstring. Alternativa (union de dataclasses por status) foi preterida pela simplicidade — ver ADR-002.
