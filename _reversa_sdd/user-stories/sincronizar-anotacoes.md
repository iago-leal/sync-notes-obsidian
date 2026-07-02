# User Stories — Sincronizar anotações ao vault

> Reversa Writer, 2026-07-02. Persona única: o leitor (Iago), single-user 🟢.

## US-01 — Anotações do Kindle no vault 🟡 (fluxo alvo; parsers 🟢, resto 🔴)

**Como** leitor que destaca trechos no Kindle Colorsoft (EPUB),
**quero** que meus destaques apareçam no vault Obsidian como callouts linkando a página exata do PDF canônico,
**para** consultar tudo num lugar só, com link de volta confiável.

Aceitação:
- Dado um `My Clippings.txt` copiado do Kindle, quando rodo `synctotes` apontando para ele, então cada destaque vira callout `[[livro.pdf#page=X]]` no vault (página via resolver `loc→page`).
- Re-rodar o comando não duplica nada (idempotência).
- Blocos malformados são reportados e pulados, sem abortar.

## US-02 — Anotações do export Amazon no vault 🟡

**Como** leitor que recebe o "Caderno de anotações" por e-mail,
**quero** ingerir esse PDF diretamente,
**para** aproveitar cores e notas anexadas que o My Clippings não traz — sem cabo USB.

Aceitação:
- Dado o PDF de export, quando ingerido, então destaques com coordenada de página viram callouts diretos; com posição, passam pelo resolver.
- Notas anexadas acompanham o destaque-pai no callout 🔴 formato pendente.

## US-03 — Anotações do Boox no vault 🔴 (bloqueada por decisões)

**Como** leitor que usa KOReader no Boox,
**quero** que o export do KOReader entre no mesmo pipeline,
**para** nenhum device ficar de fora do destino único.

Aceitação: 🔴 não derivável — depende do plugin de export e de fixture real (boox/questions.md).

## US-04 — Revisão segura antes de escrever 🟡 (guardrail #14)

**Como** mantenedor cauteloso com o próprio vault,
**quero** `--dry-run` em qualquer comando que escreva,
**para** ver o que seria criado antes de tocar os arquivos.

Aceitação:
- Dado `--dry-run`, quando executo qualquer ingest, então o vault permanece intacto e a saída lista as escritas previstas.

## Fora de escopo declarado 🟢

- Anotações de macOS/iPad: já fluem pelo `obsidian-pdf-plus`, sem passar pela CLI (ADR-003/004).
- Modificar PDFs, deletar notas, sync de rede: proibidos por guardrail.
