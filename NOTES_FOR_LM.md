# Motor de RPG IA Generativo — Crônicas de Aethelgard

## Objetivo
Este projeto foi reorganizado como um motor estruturado de RPG textual, com foco em clareza, modularidade e persistência para uso em ambientes como Notebook LM do Gemini.

## Arquitetura
- db_manager.py: camada de persistência SQLite com personagens, sessões, eventos e estado do mundo.
- dice_system.py: sistema de rolagem de dados baseado em pool de d10 para Aethelgard.
- game_master.py: orquestrador do mestre de jogo com resposta estruturada IC/OOC.
- session_manager.py: continuidade de sessão e contexto resumido para o GM.
- main.py: ponto de entrada interativo para execução local.

## Fluxo principal
1. O jogador digita uma ação.
2. O GM gera uma resposta narrada e uma instrução OOC.
3. O sistema registra eventos no banco SQLite.
4. O estado do personagem e da campanha permanecem persistidos.

## Uso recomendado
- Execute main.py para rodar a experiência localmente.
- Para uso em notebook, importe os módulos e chame o fluxo de forma incremental.
- O banco é salvo em aethelgard.db.

## Observação
O projeto agora funciona com fallback local caso a API externa não esteja disponível, o que melhora estabilidade para ingestão e testes.
