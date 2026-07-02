# Questions — unit `boox` (decididas)

> Reversa Writer, 2026-07-02 · Decisões aprovadas em bloco pelo mantenedor em 2026-07-02 e propagadas do `_reversa_sdd/questions.md` central (fonte autoritativa das respostas completas). Q13/Q14 deixam de bloquear o `boox.py`; resta obter fixture real do `markdown_export` antes de codar.

| # | Pergunta | Decisão | Ref |
|---|---|---|---|
| 1 | 🟢 DECIDIDO — Plugin de export do KOReader | `markdown_export` — saída já no idioma do vault, sem o envelope ENEX/XML do `evernote_export` | Q13 |
| 2 | 🟢 DECIDIDO — PDF ou EPUB reflow | Suportar ambos desde o parser, registrando `coordinate_kind` como no amazon_export: PDF nativo (página direta) dispensa resolver; EPUB reflow passa por ele. A proporção real de uso não precisa ser decidida | Q14 |
| 3 | 🟢 DECIDIDO — Transporte do export | Pasta de export do KOReader incluída no Syncthing da biblioteca; chega ao macOS sem ação manual | Q22 |
