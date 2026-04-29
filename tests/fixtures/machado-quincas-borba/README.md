# Fixture — Quincas Borba (Machado de Assis, 1891)

Esta fixture é o **caso de teste cross-edition** central do projeto. Permite validar o conversor de coordenadas (`página/posição da edição comercial → página da edição PD canônica`) contra material real, sem comprometer copyright porque a obra está em domínio público desde 1979 (Brasil — 70 anos pós-morte de Machado de Assis em 1908).

## Arquivos

### `pd.pdf` — edição em domínio público

- **Origem provável:** Biblioteca Nacional do Brasil (prefixo `bn` no nome original `bn000106.pdf`).
- **139 páginas.**
- Texto extrai limpo via `pdfplumber`.
- **Esta é a edição canônica** — links de callouts no vault apontam para ela (`[[pd.pdf#page=X]]`).

### `amazon_export.pdf` — Amazon "Caderno de anotações"

- **Origem:** exportação por email da função "Enviar notas" do app Kindle / web reader.
- **ASIN da edição comercial:** `B09JWVC7X8` (extraído da URL `read.amazon.com/kp/kshare?asin=...` no header do PDF).
- **10 páginas, 61 anotações:**
  - 48 destaques (Amarelo: 30, Azul-piscina: 14, Rosa: 2, Verde: 2)
  - 2 marcadores (Azul: 2)
  - 11 notas
- Anotações usam coordenada `Página X` (algumas edições Amazon usam `Posição X` em vez disso — o parser detecta ambos).
- **Este NÃO é o `My Clippings.txt`** — é o PDF formatado que a Amazon envia por email. Os dois caminhos coexistem como inputs paralelos do pipeline.

### `my_clippings_excerpt.txt` — *(ainda não presente)*

Recorte do `My Clippings.txt` original do Kindle, filtrado para conter apenas highlights de Quincas Borba. A ser gerado a partir do `My Clippings.txt` completo (que vive em `tests/fixtures/local/` e não vai para o repo público).

## Por que esta fixture existe

O conversor de coordenadas é o coração técnico do projeto (ver `ARCHITECTURE.md` guardrail #1 e ADR-002). Ele precisa funcionar quando:

1. **Edições são distintas** — paginação da edição comercial Kindle ≠ paginação da edição PD canônica. Um snippet referenciando "Página 22" da edição comercial não está na página 22 do PDF da BN.
2. **Coordenada de origem varia** — alguns livros têm `Página X`; outros (especialmente ficção contemporânea ou edições mais antigas no catálogo Amazon) têm `Posição X` (location). O Boox também usa posição. O conversor precisa lidar com ambos.
3. **Ortografia, capitalização e tipografia podem divergir** entre edições — aspas curvas vs retas, ortografia atualizada, ligaduras tipográficas.

Validar contra um livro **real** com edições reais protege contra overfitting que ocorreria com fixture sintética.

## Sobre `tests/fixtures/local/`

Pasta irmã `tests/fixtures/local/` está no `.gitignore` e abriga arquivos privados que NÃO vão para o repo público:

- `My Clippings.txt` completo do Kindle (highlights de todos os livros que o usuário já leu — dado pessoal).
- Qualquer arquivo da edição comercial Kindle (copyright vivo).

Ao clonar o repo, esta pasta vem vazia. Tests que dependem dela são marcados (futuramente) com `pytest.mark.requires_local_fixtures` e skipados em CI.
