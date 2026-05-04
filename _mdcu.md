# _mdcu.md — Prontuário Clínico em Tempo Real

**Data de Início:** 2026-05-03
**Status:** F6. Execução
**Contador de Reenquadramento:** 0/2

---

## F1. Preparação
- Gatilho Dual: OK (`ARCHITECTURE.md` e repositório materializado).
- Prontuário (`rsop/`): Lido. Nenhuma anomalia, nenhum problema aberto na `lista_problemas.md`.
- Rastreio F1 (Segurança): Sem incidentes aparentes ao iniciar a sessão.

## F2. Escuta
*Separação ativa entre Demanda (problema) e Queixa (sintomas/relato).*
- **Queixa:** O usuário atualizou o repositório global do MDCU e precisa que as novas mudanças estruturais (matriz de rastreabilidade) sejam aplicadas no projeto.
- **Demanda:** Instituir o Motor de Rastreabilidade Semântica (matrizes de *blast radius* e *code-spec*) para o projeto `sync-notes-obsidian`, garantindo que pequenas mudanças não causem degradação sistêmica na arquitetura.

## F3. Exploração
*Ramificações sistêmicas da demanda.*
- A atualização do framework MDCU introduz a exigência de uma pasta `traceability/` contendo matrizes que funcionam como "Gate Disjuntor" para LLMs e agentes.
- Atualmente, o `sync-notes-obsidian` não possui essa matriz. Precisamos mapear nossos componentes vitais (`kindle.py`, `pdf.py`, `obsidian.py`) contra as especificações e regras de domínio (`ARCHITECTURE.md`, `ADR-002`, `ADR-004`).
- Qualquer futura alteração no projeto precisará consultar essa matriz para evitar *blast radius* não antecipado (por exemplo, alterar o conversor fuzzy pode quebrar a idempotência no Vault).

## F4. Avaliação
*Formulação da hipótese estrutural.*
- #4 Instituir `traceability/code-spec-matrix.md` para o código-fonte atual.
- #5 Instituir `traceability/spec-impact-matrix.md` definindo os impactos cruzados (blast radius) de alterações na CLI, no conversor fuzzy e nos callouts.
- #6 Adicionar a **ADR-006** oficializando a adoção do motor de rastreabilidade.

## F5. Plano
*Alternativas viáveis com trade-offs.*
- **Plano de Execução Direta:** 
  Como essa é uma exigência metodológica inegociável da nova versão do framework MDCU, aplicarei a criação da pasta `traceability/` com as duas matrizes devidamente adaptadas ao domínio do seu conversor Kindle-Obsidian, criarei a ADR-006 e registrarei a adoção no nosso prontuário RSOP.

## F6. Execução e Fechamento
*Acompanhamento da execução delegada e integração.*
- **Decisão:** Plano de Execução Direta aprovado.
- **Delegação:** Atuando como engine ad-hoc para criar a matriz de rastreabilidade, ADR-006 e atualizar o RSOP.
