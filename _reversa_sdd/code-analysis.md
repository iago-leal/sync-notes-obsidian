# Análise de Código — jailbreak-kindle (`synctotes`)

> Gerado pelo Reversa Archaeologist em 2026-07-02.
> Escala: 🟢 CONFIRMADO · 🟡 INFERIDO · 🔴 LACUNA.

## Visão geral

O pacote implementa a **camada de ingestão** de um pipeline de sincronização de anotações de livros para o vault Obsidian. Dois parsers estão completos (Kindle `My Clippings.txt` e PDF de exportação da Amazon), apoiados por um extrator de texto de PDF e por contratos de domínio tipados. O coração do pipeline — o resolver `loc→page` — e a camada de saída (writer Obsidian, CLI real, ingest Boox) ainda não existem 🟢.

Padrões transversais 🟢:
- **Dataclasses `frozen=True`** em todas as entidades — imutabilidade como invariante.
- **Parsing tolerante a falhas**: blocos malformados são pulados em silêncio; datas ilegíveis viram `None` sem abortar o clipping.
- **Regex pré-compiladas em constantes `Final`** module-level.
- **mypy `--strict`** em todo o código, inclusive testes.
- Nenhum I/O de escrita em disco; somente leitura de PDFs/strings.

---

## Módulo `kindle` — `src/synctotes/kindle.py` (257 LOC)

**Propósito:** parser do `My Clippings.txt` do Kindle, locales PT-BR e EN. Futuro lar do resolver `loc→page` (ADR-002) 🟢.

### Fluxo de controle

| Função | Assinatura | Papel |
|---|---|---|
| `parse_clippings` | `(content: str) -> list[KindleClipping]` | API pública. Remove BOM, normaliza CRLF/CR→LF, divide por `==========`, delega blocos |
| `_parse_block` | `(block: str) -> KindleClipping \| None` | Valida bloco de ≥2 linhas: linha 1 livro, linha 2 metadata, resto texto |
| `_parse_book_line` | `(line: str) -> KindleBook \| None` | Regex `^(.*?)\s*\((.+)\)\s*$` — último parêntese é autor; sem parêntese, título puro |
| `_parse_metadata_line` | `(line: str) -> tuple \| None` | Exige prefixo `- `; divide por `\|`; tipo obrigatório na parte 0; varre todas as partes por posição/página e data |
| `_detect_type` | `(part: str) -> ClippingType \| None` | Busca substring case-insensitive em `_TYPE_KEYWORDS` (destaque/highlight, nota/note, marcador/bookmark) |
| `_parse_position` | `(part: str) -> (start, end, page)` | Página tem precedência sobre posição; posição aceita faixa `X-Y` ou única |
| `_parse_date` | `(part: str) -> datetime \| None` | PT-BR (`1 de junho de 2018 14:30:25`) e EN (`June 3, 2018 9:15:00 AM`) com conversão AM/PM |

### Algoritmos e regras embutidas

1. **Tolerância a formatos antigo/moderno** 🟢: o formato moderno junta tipo+posição numa parte só; o antigo separa. A varredura independente de cada parte (`kindle.py:186-192`) cobre ambos.
2. **Precedência página > posição** 🟢 (`kindle.py:208-215`): se a metadata menciona `página X`, o clipping ganha `page` e posições ficam `None`; caso contrário tenta `posição X[-Y]`.
3. **Primeira ocorrência vence** 🟢 (`kindle.py:187`): a varredura só preenche posição/página se ambos ainda estiverem vazios — partes subsequentes não sobrescrevem.
4. **Conversão AM/PM** 🟢 (`kindle.py:250-254`): `PM` soma 12 exceto `12 PM`; `12 AM` vira 0.
5. **Blocos malformados são descartados silenciosamente** 🟢 (docstring `kindle.py:102-103`): o chamador pode comparar contagens se detecção de defeito importar. 🟡 INFERIDO: decisão consciente de robustez sobre alarme (coerente com o guardrail de "erros barulhentos" apenas nas fronteiras do pipeline).
6. **Bookmark tem texto vazio** 🟢 (comprovado em `test_parse_clippings_bookmark_has_empty_text`).

### Casos-limite cobertos por teste 🟢

BOM UTF-8, CRLF/CR, livro sem autor, faixa de posição vs. posição única, página, os três tipos, datas nos dois locales, blocos malformados intercalados.

---

## Módulo `amazon_export` — `src/synctotes/amazon_export.py` (283 LOC)

**Propósito:** parser do PDF "Caderno de anotações" que a Amazon envia por e-mail. Locale PT-BR; EN pendente de fixture real 🟢 (docstring linha 14).

### Fluxo de controle

| Função | Assinatura | Papel |
|---|---|---|
| `parse_export_pdf` | `(path: Path \| str) -> ExportedNotebook` | API pública: extrai texto integral, parseia header e anotações |
| `_extract_full_text` | `(path: Path) -> str` | Concatena `page.extract_text()` de todas as páginas via pdfplumber |
| `_parse_header` | `(lines) -> (AmazonBook, int, int)` | Máquina posicional: 1ª linha não-vazia = título; `por X` = autor; `asin=` = ASIN; `Anotações (N)` = total; retorna índice onde começam as anotações |
| `_parse_annotations` | `(lines) -> list[AmazonAnnotation]` | **Máquina de estados** linha a linha com acumulador e `flush()` |

### Máquina de estados de `_parse_annotations` 🟢

Estados implícitos no acumulador (`cur_*`, `text_lines`, `note_text`, `in_note_block`):

1. **Linha de metadata** (`Página|Posição N | Tipo (Cor)`) → `flush()` da anotação corrente e abre nova. Tipo mapeado: `Continuação do destaque`→HIGHLIGHT com `is_continuation=True`; `Destaque`→HIGHLIGHT; `Marcador`→BOOKMARK; `Nota`→NOTE.
2. **Ruído estrutural descartado**: linhas só-dígitos (números de página do próprio PDF) e numerais romanos (frontmatter) — `_BARE_DIGIT_RE`, `_ROMAN_RE`.
3. **`Nota: ...`** → inicia bloco de nota anexada (`in_note_block=True`); linhas seguintes concatenam na nota, não no texto.
4. **Linha de data** (`1 de abr. de 2026`) → vira `date_added` apenas se fora de bloco de nota e ainda não definida.
5. **Qualquer outra linha** → acumula em `text_lines` (ou na nota, se `in_note_block`).
6. **`flush()` final** garante a última anotação. Anotações sem tipo+coordenada completos são descartadas.

### Regras de negócio embutidas

1. **Dois sistemas de coordenadas** 🟢: `coordinate_kind` distingue `page` (edição comercial expõe páginas) de `position` (só locations) — decisão da Amazon por título/edição; o resolver despachará conforme o tipo (docstring linhas 8-12).
2. **Reconciliação com o sumário da Amazon** 🟢 (documentada em `test_total_annotations_match_summary`): a Amazon conta nota anexada como item separado e continuação como parte do destaque-pai; o parser faz o inverso (nota anexada dobra no campo `note`, continuação vira item próprio). Invariante: `itens_sem_continuação + notas_anexadas == summary_total`.
3. **Cor da anotação** 🟢: capturada do parêntese do tipo (`Destaque (Amarelo)`, `Marcador (Azul)`).
4. **Data dentro de bloco de nota é ignorada** 🟢 (`amazon_export.py:273`): evita que a data da nota sobrescreva a do destaque.

### Dependências internas

Importa `ClippingType` de `synctotes.kindle` 🟢 — acoplamento leve entre parsers pela taxonomia comum de tipos.

🟡 INFERIDO: fixture real (`tests/fixtures/machado-quincas-borba/amazon_export.pdf`, ASIN B09JWVC7X8, 61 anotações) serve de contrato de regressão do layout Amazon; mudanças de layout da Amazon quebrariam aqui primeiro.

---

## Módulo `pdf` — `src/synctotes/pdf.py` (27 LOC)

**Propósito:** extração de texto por página do PDF canônico, base para o fuzzy search do resolver 🟢.

- `extract_pages(path: Path | str) -> dict[int, str]` — mapeamento **denso** e **1-indexado** (convenção humana e do formato de link `[[livro.pdf#page=X]]`); página vazia vira `""`, nunca ausente 🟢.
- Sem tratamento de erro próprio: exceções do pdfplumber propagam 🟢. 🟡 INFERIDO: coerente com "erros barulhentos".

---

## Módulo `types` — `src/synctotes/types.py` (41 LOC)

**Propósito:** contrato público do resolver `loc→page` (guardrail #1, ADR-002). Estabelecido antes da implementação porque refatorá-lo depois custa caro — toca todo chamador 🟢.

- `MatchStatus = Literal["found", "ambiguous", "no_match"]`
- `Candidate(page: int, score: float, excerpt: str)` — frozen.
- `MatchResult(status, page=None, confidence=None, candidates=())` — frozen; semântica por status documentada: `found` → `page`+`confidence`; `ambiguous` → lista `candidates`; `no_match` → nada.
- 🟢 Fallback LLM planejado para v2 via **decorator pattern** sobre esta mesma interface (docstring linhas 6-8).

---

## Stubs — `cli`, `obsidian`, `boox` (39 LOC somados)

| Módulo | Contrato declarado no stub | Estado |
|---|---|---|
| `cli.py` | `main() -> int`; hoje imprime versão + aviso e retorna 0 — entry point verificado end-to-end no setup 🟢. Typer declarado na stack, ainda não usado no código 🟢 | 🔴 LACUNA: comandos reais não especificados no código |
| `obsidian.py` | Writer de callouts; link sempre ao PDF canônico `[[livro.pdf#page=X]]` (guardrail #2); idempotência por hash estável de (livro, snippet normalizado) (guardrail #6); implementação em F6.a 🟢 (docstring) | 🔴 LACUNA: formato exato do callout e algoritmo do hash não definidos |
| `boox.py` | Ingest de exports markdown do KOReader/Boox; implementação em F6.a 🟢 (docstring) | 🔴 LACUNA: formato de entrada não especificado |

---

## Síntese quantitativa

| Métrica | Valor |
|---|---|
| Módulos analisados | 7 (4 implementados, 3 stubs) |
| Funções públicas | 4 (`parse_clippings`, `parse_export_pdf`, `extract_pages`, `main`) |
| Entidades de domínio | 8 (`KindleBook`, `KindleClipping`, `ClippingType`, `AmazonBook`, `AmazonAnnotation`, `ExportedNotebook`, `Candidate`, `MatchResult`) |
| Algoritmos não-triviais | 2 (máquina de estados do export Amazon; parser tolerante multi-locale do My Clippings) |
| Testes | 29 casos em 4 suítes, todos verdes; cobertura 91% total (kindle 92%, amazon_export 95%, pdf/types 100%, stubs 0%) — verificado pelo Reviewer em 2026-07-02 |
