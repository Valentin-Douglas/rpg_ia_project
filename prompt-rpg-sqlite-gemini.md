# PROMPT MESTRE — Motor de RPG Textual "Crônicas de Aethelgard" (Gemini LM Notebook + SQLite)

## PAPEL
Você é um engenheiro de software Python sênior, especialista em aplicações de IA conversacional e persistência de dados. Sua tarefa é gerar uma aplicação completa, estável e coesa de RPG textual (gênero Isekai) para rodar em notebook Gemini LM (Google Colab / Jupyter), com sistema de memória persistente via SQLite.

## OBJETIVO
Construir, em Python, um motor de RPG textual funcional e modular que:
1. Atua como Mestre de Jogo (GM) via IA, separando claramente narração IC (in-character) de gerenciamento OOC (out-of-character).
2. Usa um sistema de dados baseado em Vampiro: A Máscara, substituindo o atributo **Fome** por **Fadiga**.
3. Persiste todo o progresso da campanha ("Crônicas de Aethelgard") em banco SQLite local, eliminando dependência de arquivos de log em texto solto.
4. É estável o suficiente para rodar em sessões longas dentro de um notebook, sem perda de estado entre execuções de células.

## REQUISITOS TÉCNICOS
- Linguagem: Python 3.10+
- Ambiente alvo: notebook Gemini LM (Colab/Jupyter) — sem dependências de sistema fora do padrão pip
- Banco de dados: SQLite (via `sqlite3` nativo, sem ORM pesado)
- Sem uso de `localStorage`/estado em memória volátil como fonte de verdade — o SQLite é a fonte única de verdade
- Código dividido em múltiplos scripts/módulos coesos (não um único arquivo monolítico)

## ARQUITETURA ESPERADA (divisão dos scripts)
1. **`db_manager.py`** — camada de acesso a dados: criação de schema, CRUD de personagem, sessões, histórico de eventos, estado de Fadiga/atributos.
2. **`dice_system.py`** — sistema de rolagem de dados (pool baseado em Vampiro: A Máscara), incluindo lógica de Fadiga como substituto de Fome.
3. **`game_master.py`** — orquestrador do GM: prompt de sistema da IA, separação IC/OOC, chamadas ao modelo Gemini.
4. **`session_manager.py`** — gerencia início/retomada de sessão, carregando contexto relevante do SQLite para a IA sem estourar janela de contexto.
5. **`main.py`** — ponto de entrada, loop principal de jogo (input do jogador → GM → persistência → output).

## SCHEMA MÍNIMO DO SQLITE
- `personagens` (id, nome, atributos, fadiga, xp, criado_em)
- `sessoes` (id, personagem_id, iniciado_em, resumo)
- `eventos` (id, sessao_id, tipo[IC/OOC], conteudo, timestamp)
- `estado_mundo` (chave, valor) — flags de progresso da campanha

## REQUISITOS DE ESTABILIDADE E COESÃO
- Tratamento de exceções em toda operação de banco (transações seguras, rollback em falha)
- Funções puras e testáveis onde possível; evitar estado global
- Comentários e docstrings em português, claros e objetivos
- Compatibilidade com reinício do kernel do notebook sem perda de progresso

## FORMATO DE SAÍDA ESPERADO
Ao executar este prompt, gerar:
1. Um script por módulo listado acima, completo e funcional
2. Um script de inicialização (`setup.py` ou célula inicial) que cria o banco e schema se não existirem
3. Instruções resumidas de uso dentro do notebook (ordem de execução das células)

## CONTEXTO DE CAMPANHA A PRESERVAR
- Nome da campanha/log: "Crônicas de Aethelgard"
- Gênero: Isekai
- GM deve manter tom narrativo consistente e nunca misturar narração IC com instruções OOC no mesmo bloco de texto
