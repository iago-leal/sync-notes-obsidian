# _mdcu.md — Prontuário Clínico em Tempo Real

**Data de Início:** 2026-05-03
**Status:** F6. Execução
**Contador de Reenquadramento:** 0/2

---

## F1. Preparação
- Gatilho Dual: OK (`ARCHITECTURE.md` presente e atualizado; setup materializado via `uv` e `pre-commit`).
- Prontuário (`rsop/`): Inexistente (primeira sessão estrutural após o setup).
- Rastreio F1 (Segurança): Sem anomalias detetadas.

## F2. Escuta
*Separação ativa entre Demanda (problema) e Queixa (sintomas/relato).*
- **Queixa:** O usuário está colocando o MDCU no projeto e sente que precisa integrá-lo bem ao repositório já existente.
- **Demanda:** Formalizar e materializar a fundação do MDCU (especificamente o componente de prontuário RSOP e as regras de versionamento) para que as futuras sessões de desenvolvimento funcionem perfeitamente.

## F3. Exploração
*Ramificações sistêmicas da demanda.*
- As skills foram fisicamente copiadas para `.agents/skills` e `.claude/skills`.
- A arquitetura está documentada em `ARCHITECTURE.md`.
- O diretório `rsop/` ainda não existe. Sem ele, a F1 das próximas sessões e o fechamento (F6, `/mdcu fechar` -> `/rsop soap`) vão falhar.
- O arquivo `_mdcu.md` é o lousa efêmera do framework e não deve ir para o histórico do Git, mas atualmente ele não está no `.gitignore`.

## F4. Avaliação
*Formulação da hipótese estrutural.*
- #1 Inicialização Estrutural do RSOP (`rsop/dados_base.md`, `rsop/lista_problemas.md`, `rsop/passivos.md`, `rsop/soap/`).
- #2 Inserção de dados preliminares no `dados_base.md` extraídos da documentação atual.
- #3 Proteção do repositório adicionando `_mdcu.md` ao `.gitignore`.

## F5. Plano
*Alternativas viáveis com trade-offs.*
- **Alternativa A (Integração Total Inteligente):** Executamos a inicialização das pastas do RSOP, adicionamos o `_mdcu.md` no `.gitignore` e já preenchemos o `rsop/dados_base.md` com as informações que sabemos (nome do projeto, propósito e autor extraídos do `ARCHITECTURE.md`).
- **Alternativa B (Integração Vanilla):** Rodamos apenas o comando bruto `/rsop init` para gerar as pastas vazias e atualizamos o `.gitignore`, deixando o preenchimento manual do `dados_base.md` para você fazer depois via `/rsop dados`.

## F6. Execução e Fechamento
*Acompanhamento da execução delegada e integração.*
- **Decisão:** Alternativa A escolhida pelo usuário.
- **Delegação (F6.a):** Atuando como engine ad-hoc, criei a estrutura física do RSOP e o adicionei ao controle.
- **Gate de Integração (F6.c):** Testes executados (`uv run python -m pytest`) e 29 testes passaram.
- **Fechamento Próximo:** Aguardando comando de fechamento do usuário.
