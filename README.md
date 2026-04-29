# sync-notes-obsidian

> **Vault Obsidian é destino único de todas as anotações de livros, vindas de leitor nativo de cada device. Cada livro tem versão PDF (canônica, com âncoras de página) e versão EPUB (para leitura confortável no Kindle/Boox-reflow). Anotações vindas do Kindle (em location de EPUB) passam por um conversor `loc → page` antes de virarem callout no vault, para que o link de volta sempre aponte para o PDF canônico.**

Modelo análogo ao Zotero, generalizado para múltiplos devices (macOS, iPad, Boox, Kindle Colorsoft) com leitores nativos em cada um.

---

## Por que esta pasta ainda se chama `jailbreak-kindle` no Desktop

Esse mismatch é proposital — é **evidência narrativa do reenquadramento** que delimitou este projeto.

A sessão começou com a hipótese de que o problema fosse "jailbreak do Kindle" (escrever software custom para liberar o device). Ao longo de cinco rodadas de escuta MCCP/MDCU, a demanda aparente foi sendo reenquadrada até a demanda real emergir: o problema nunca foi jailbreak — foi **personal knowledge management com sync dual-format de anotações em ecossistema multi-device**, no modelo Zotero.

A pasta local guarda o nome inicial como cicatriz didática. O repositório no GitHub já nasce com o nome cristalizado.

| Camada | Nome |
|---|---|
| Pasta local (`~/Desktop/`) | `jailbreak-kindle` (nome da demanda aparente) |
| Repositório GitHub | `sync-notes-obsidian` (nome da demanda real) |

---

## Status

- **F4 do MDCU:** fechada — problema cristalizado e validado pelo usuário ("acho que chegamos ao ponto. está lindo").
- **F5 do MDCU:** pendente — proposta de 2 alternativas de stack (MVP-minimal vs robusto) com trade-offs explícitos.
- **Código:** nenhum ainda. Decisão consciente — F5 é proposta, F6 é execução.
- **`ARCHITECTURE.md` + `project-setup`:** ainda não materializados (dependem de F5 fechar).

---

## Estrutura inicial

```
.
├── README.md                              ← este arquivo
├── _mdcu.md                               ← estado vivo da sessão MDCU (transitório; deletado ao /mdcu fechar)
├── transcricao-mdcu-jailbreak-kindle.md   ← transcrição literal da sessão de delimitação
└── .gitignore
```

Quando F5 fechar, surgirão `ARCHITECTURE.md` (contrato técnico) + manifesto da stack (Python/Node/etc.) + lock file determinístico + `src/` + `tests/`.

---

## Sobre o processo

Este projeto foi delimitado usando o framework [**MDCU — Método de Desenvolvimento Centrado no Usuário**](https://github.com/iago-leal/skills/tree/main/mdcu-framework), de autoria de [@iago-leal](https://github.com/iago-leal). O MDCU é uma transposição do **MCCP (Método Clínico Centrado na Pessoa)** — usado em Medicina de Família e Comunidade — para o domínio de Engenharia de Software.

A premissa central: o **especialista na experiência do problema é o usuário**, não o engenheiro. O agente IA é o operador clínico que extrai o problema com escuta estruturada, separa demanda aparente de demanda real, traduz complexidade técnica em decisão informada, e exerce dever de alerta sobre escolhas que comprometem bem-estar de longo prazo.

A [**transcrição literal da sessão de delimitação**](./transcricao-mdcu-jailbreak-kindle.md) está neste repositório como evidência pedagógica do processo. Nela é possível observar:

1. Cinco reenquadramentos sucessivos da demanda apresentada.
2. Recusa do agente de aceitar a demanda inicial sem escuta.
3. Apresentação de trade-offs em pontos críticos (K1/K2/K3 sobre o papel do Kindle no workflow).
4. Bloqueios solicitados pelo usuário ("ainda não vamos passar para a próxima") sendo respeitados.
5. Cristalização do problema em F4 antes de qualquer linha de código ser escrita.

A mesma transcrição vive no [repositório do framework MDCU](https://github.com/iago-leal/skills/tree/main/mdcu-framework) como caso de estudo.

---

## Notas técnicas conhecidas (para F5)

Pontos de design já estabelecidos em F4 que vão informar F5:

- **PDF é formato canônico** no vault (page-number estável). EPUB é variante de transporte para Kindle/Boox-reflow.
- **Conversor `loc EPUB → page PDF`** é o componente novo a construir, e é o coração do pipeline do Kindle.
- Caminho determinístico-first (fuzzy text-search em PDF extraído) é alternativa ao LLM-local-first sugerido pelo usuário — decisão técnica pendente para F5.
- **Jailbreak do Kindle Colorsoft (firmware 5.19.2) está bloqueado por firmware** em abril de 2026 e não é parte do escopo. Kindle entra como cidadão "1.5ª classe" (lê PDFs vindos dos outros devices; suas anotações chegam ao vault com granularidade de página, não de trecho exato).
- `obsidian-pdf-plus` (macOS/iPad) e `obsidian-kindle-plugin` (Kindle) são componentes existentes do pipeline. Boox depende de KOReader Android ou app nativo Boox com export para markdown.
- Readwise é componente possível mas insuficiente — não cobre Boox; link de volta dele aponta para `read.amazon.com`, não para arquivo no vault.
