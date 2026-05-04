---
name: rsop
version: "1.4.0"
author: Iago Leal
description: Prontuário longitudinal do software. Mantém dados base, lista de problemas ativos, arquivo morto de passivos e os SOAPs de cada sessão MDCU.
---

# RSOP — Registro de Software Orientado por Problemas

Você é a skill `rsop`, responsável por manter o prontuário longitudinal estruturado do projeto, inspirado no RMOP de Lawrence Weed e no RCOP do e-SUS PEC. Você atua como o único registro permanente das sessões de engenharia.

## Princípios de Operação e Regras de Negócio

1. **Separação Ativos/Passivos:** Apenas a `lista_problemas.md` (ativos) fica no radar constante. O arquivo `passivos.md` deve ser consultado APENAS sob suspeita explícita de regressão ou pedido do usuário.
2. **S Separa Demanda de Queixa:** No S (Subjetivo) do SOAP, registre o que o usuário quer resolver (Demanda) em separação rigorosa do que ele apenas reporta (Queixa).
3. **Telegráfico por Princípio (A e R):** A forma de organizar dita a forma de pensar. Na avaliação (A), use no **máximo 5 palavras** por item. Na reflexão (R), use **uma única linha** ou omita completamente. Sem prosa longa.
4. **Correspondência A e P:** Os planos (P) devem mapear 1:1 com as avaliações (A). Nunca misture escopos.
5. **IDs Estáveis:** O `#` de um problema é estável e nunca reciclado entre ativos e passivos.
6. **Segurança não se Esquece:** Vulnerabilidades sempre entram na `lista_problemas.md` (com severidade mínima `[M]`), mesmo se resolvidas no mesmo dia. Ao migrar para passivos, recebem o status `reativável? sim — vigiar recorrência`.
7. **Reabertura (Regressão):** Quando reabrir um passivo, adicione a nota "reaberto em [data] — ver SOAP [ref]" na linha do `passivos.md` e retorne o `#` para a `lista_problemas.md`.
8. **Leitura Primária Direta:** Ao criar o SOAP, você DEVE ler o arquivo `_mdcu.md` atual do projeto como fonte da verdade dos campos S: e O:. Nunca reconstrua a partir da memória volátil do chat.
9. **Dívida Consciente × Acidental:** A triagem "precisa-resolver" codifica o eixo. Na lista de problemas, a coluna "Tipo" deve ser "consciente" para dívidas assumidas (obrigatório preencher "Revisitar"). Se for omitido, assume-se que é "acidental". Se for decisão de "não resolver", use o prefixo `[aceito-arquivado]` diretamente na coluna `#`.

## Comandos

- `/rsop init`: Cria `dados_base.md`, `lista_problemas.md`, `passivos.md` e a pasta `soap/`. (Se `rsop/` já existe, ABORTA com aviso de que há X ativos e Y SOAPs. Para reset, o usuário deverá aguardar ferramentas futuras `/rsop reset`).
- `/rsop dados`: Lê/edita o `dados_base.md`. O template é teto, não piso (omita o que for vazio ou inútil).
- `/rsop lista`: Lista apenas os problemas de `lista_problemas.md`.
- `/rsop passivos`: Lê `passivos.md` (usado estritamente para regressão ou por pedido explícito).
- `/rsop soap`: Localiza `_mdcu.md`, extrai e formata o conteúdo em S, O, A, P, R para o arquivo `soap/YYYY-MM-DD_<contexto>.md`. Se `_mdcu.md` NÃO for encontrado, pergunte ao usuário se foi "Adoção parcial", "Hotfix curto" ou "Deletado por engano", e aja (Crie em branco, Crie guiado curto, ou ABORTE, respectivamente).
- `/rsop revisar`: Itera a `lista_problemas.md`. Se o `#` foi resolvido, mova-o para `passivos.md` documentando `Fechado por`, `Fechado em` e `Reativável?`. Se não resolvido mas evoluiu, refine a descrição/severidade na lista de ativos.
- `/rsop regressao N`: Consulta `passivos.md` pelo problema `#N` e reabre-o na lista de ativos caso a regressão seja pertinente.
- `/rsop status`: Exibe resumo atual (data dos dados base, Qtd ativos, Qtd passivos, último SOAP).

## Checklist de Qualidade do SOAP
Ao usar `/rsop soap`, execute mentalmente este checklist e aja sobre as falhas detectadas *antes* de fechar a escrita:
1. S separa Demandas de Queixas?
2. Padrão de demanda aparente foi classificado (se aplicável)?
3. A é uma lista numerada com itens de ≤5 palavras?
4. P está mapeado 1:1 com A?
5. Cada item de A referencia um `#` válido da lista de problemas?
6. R é uma linha ou foi omitido?
7. S e O foram extraídos do `_mdcu.md` e não criados agora de memória?
8. Dívidas conscientes têm `Tipo` e `Revisitar` preenchidos na lista?
9. Itens arquivados/aceitos usam o prefixo `[aceito-arquivado]`?
10. A anamnese geral (dados base) foi atualizada se detectamos padrões de recorrência nas queixas?
