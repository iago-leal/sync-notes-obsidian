# ADR-007 (retroativo) — Export Amazon "Caderno de anotações" como segunda fonte de ingest

- **Status:** Inferido do código (🟡 proposto para formalização)
- **Data da decisão evidenciada:** 2026-04-29 (commit `8ee7284`)
- **Gerado por:** Reversa Detective, 2026-07-02

## Contexto

O plano original (ARCHITECTURE.md, estrutura de diretórios) previa ingest via `My Clippings.txt` (kindle) e KOReader/Boox (boox). O commit `8ee7284` — no mesmo dia da primeira implementação — adicionou um terceiro caminho não previsto na estrutura declarada: parser do PDF "Caderno de anotações" que a Amazon envia por e-mail (`amazon_export.py`, 283 LOC, o maior módulo do pacote).

## Decisão evidenciada 🟢

1. O PDF de export da Amazon é fonte de ingest de primeira classe, com entidades próprias (`AmazonBook`, `AmazonAnnotation`, `ExportedNotebook`).
2. O parser registra **qual sistema de coordenadas** cada anotação usa (`page` vs `position`), porque a mesma biblioteca mistura edições com e sem numeração de página exposta — o resolver despachará conforme o tipo.
3. Uma **fixture real** (Quincas Borba, ASIN B09JWVC7X8, 61 anotações, domínio público) foi commitada como contrato de regressão: mudanças de layout no export da Amazon quebram a suíte antes de quebrar o pipeline.
4. A reconciliação com o sumário da Amazon (`Anotações (N)`) é testada com semântica invertida documentada: nota anexada dobra no destaque; continuação vira item próprio.

## Razões prováveis 🟡

- O export Amazon traz **cor** e **notas anexadas** estruturadas, que o `My Clippings.txt` não expõe, além de coordenadas de página quando a edição as tem — dados mais ricos para o callout.
- PDF por e-mail dispensa acesso físico ao device (o `My Clippings.txt` exige cabo USB).

## Consequências

- Acoplamento leve entre parsers pela taxonomia comum `ClippingType` (importada de `kindle`).
- 🔴 LACUNA: suporte a export em inglês pendente de fixture real (docstring, `amazon_export.py:14`).
- 🔴 LACUNA: unificação das duas fontes (clipping vs annotation) num modelo comum ainda não existe — provável responsabilidade do resolver/writer futuros.
