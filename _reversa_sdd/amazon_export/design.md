# Design — unit `amazon_export`

> Reversa Writer, 2026-07-02 · Máquina de estados detalhada em `../flowcharts/amazon_export.md` e `../state-machines.md` §2.

## Estrutura 🟢

```
parse_export_pdf(path) -> ExportedNotebook
  ├─ _extract_full_text(path) -> str        # pdfplumber, páginas concatenadas com \n
  ├─ _parse_header(lines) -> (AmazonBook, total, annotations_start)
  └─ _parse_annotations(lines[start:]) -> list[AmazonAnnotation]
```

## `_parse_header` — parser posicional 🟢

Percorre linhas não-vazias na ordem: título (1ª), autor (`por `), ASIN (regex), total (`Anotações (N)`). Ao achar o total, avança até a primeira linha que casa `_METADATA_RE` e retorna esse índice como início das anotações. Fallbacks: sem metadata após o total → `index+1`; sem total → fim das linhas (nenhuma anotação).

## `_parse_annotations` — máquina de estados com acumulador 🟢

Estado: `cur_kind/color/coord_kind/coord_value/is_continuation`, `text_lines`, `note_text`, `date_added`, `in_note_block`. Closure `flush()` emite a anotação corrente **somente se** tipo+coordenada completos, e zera o estado.

Ordem de avaliação por linha (a ordem importa — reimplementação deve preservá-la):
1. vazia → skip; 2. só-dígitos → skip; 3. romanos → skip;
4. metadata → flush + abre nova anotação;
5. sem anotação aberta → skip;
6. `Nota:` → abre bloco de nota;
7. data → só vale fora de bloco de nota e se ainda vazia;
8. resto → acumula (nota se `in_note_block`, senão texto).

## Regexes literais (contrato de reimplementação) 🟢

| Nome | Padrão |
|---|---|
| `_ASIN_RE` | `asin=([A-Z0-9]{10})` |
| `_TOTAL_RE` | `Anota[çc][õo]es\s*\((\d+)\)` |
| `_METADATA_RE` | `^(P[áa]gina\|Posi[çc][ãa]o)\s+(\d+)\s*\\|\s*(.+)$` (IGNORECASE) |
| `_TYPE_COLOR_RE` | `^(Destaque\|Marcador\|Nota\|Continua[çc][ãa]o\s+do\s+destaque)\s*(?:\(([^)]+)\))?\s*$` (IGNORECASE) |
| `_DATE_RE` | `^\s*(\d{1,2})\s+de\s+([\w]+?)\.?\s+de\s+(\d{4})\s*$` (IGNORECASE\|UNICODE) |
| `_NOTE_RE` | `^Nota:\s*(.+)$` |
| `_ROMAN_RE` | `^[IVXLCDM]+$` |
| `_BARE_DIGIT_RE` | `^\d+$` |

## Decisões de design

1. **Fixture real como contrato** 🟢: o layout da Amazon não é documentado; o teste contra o PDF real é a especificação executável (ADR-007 retroativo).
2. **Semântica de contagem própria** 🟢: continuações são itens (rastreiam quebra de página); notas anexadas são atributo do destaque. Reconciliação com o total da Amazon é invariante de teste, não do parser.
3. **Detecção de coordenada por substring** (`"agina" in coord_lower`) 🟢 — tolera capitalização e acento.
4. 🟡 Ruído estrutural (dígitos/romanos) assume que nenhum destaque legítimo é composto apenas por um número — aceitável para prosa; pode comer destaques de tabelas numéricas (caso de borda não testado).
