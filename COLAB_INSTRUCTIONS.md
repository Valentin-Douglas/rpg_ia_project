# Instruções para Google Colab

1. Abra o Google Colab e crie um novo notebook.
2. Faça upload dos arquivos do projeto para o ambiente do Colab:
   - db_manager.py
   - dice_system.py
   - game_master.py
   - session_manager.py
   - colab_notebook.py
3. No Colab, abra o arquivo colab_notebook.py como uma célula de Python ou copie o conteúdo para o notebook.
4. Se quiser usar a API do Gemini, adicione um segredo chamado GEMINI_API_KEY no painel de segredos do Colab.
5. Execute as células em ordem.

## Observação
Sem a chave GEMINI_API_KEY, o projeto funciona em modo local/fallback e ainda mantém a lógica de RPG, dados e persistência.
