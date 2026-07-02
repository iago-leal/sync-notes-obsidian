# Design — unit `boox` (stub)

> Reversa Writer, 2026-07-02.

Nada desenhado 🔴. Diretriz por analogia com as units irmãs 🟡:

1. Parser puro `parse_koreader_export(content: str) -> list[...]` no padrão de `parse_clippings` (falha local, dataclasses frozen).
2. Fixture real commitada antes do código (padrão ADR-007/008: fixture como contrato de regressão + TDD).
3. Reutilizar `ClippingType`; avaliar entidade própria (`BooxAnnotation`) vs. reuso de `KindleClipping` — depende dos campos que o KOReader exporta 🔴.

Pré-requisito operacional: decidir o plugin de export do KOReader (`evernote_export` vs `markdown_export`) e o caminho Syncthing de onde a CLI lê 🔴.
