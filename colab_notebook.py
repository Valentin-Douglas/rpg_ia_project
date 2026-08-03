# -*- coding: utf-8 -*-
"""Notebook-ready version for Google Colab.

Execução:
1. Instale dependências (se necessário).
2. Execute as células em sequência.
3. Digite sua ação no final para jogar.
"""

# %% [markdown]
# # Motor de RPG IA Generativo — Crônicas de Aethelgard
# Este notebook é uma versão adaptada para o Google Colab.

# %%
!pip install -q google-generativeai

# %%
import os
import json
import sqlite3
from datetime import datetime

# %%
from google.colab import userdata

GEMINI_API_KEY = userdata.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
    print('Chave de API carregada do Colab Secrets.')
else:
    print('Sem GEMINI_API_KEY definida. O jogo usará o modo local/fallback.')

# %%
from db_manager import DBManager
from dice_system import rolar_pool_aethelgard
from game_master import GameMaster
from session_manager import SessionManager

# %%
DB_PATH = 'aethelgard_colab.db'
db = DBManager(DB_PATH)
gm = GameMaster(client=None)
sm = SessionManager(db, gm)

print('Banco inicializado em', DB_PATH)

# %%
nome = input('Nome do personagem: ').strip() or 'Aelion'
personagem_id = db.create_character(
    nome=nome,
    atributos={'forca': 3, 'agilidade': 3, 'vontade': 3},
    fadiga=0,
    xp=0,
)
sm.iniciar_ou_retomar(personagem_id)
print('Personagem criado:', nome)

# %%
inter_id = None
while True:
    user_in = input('\n[Sua ação] (digite sair para encerrar): ').strip()
    if user_in.lower() in {'sair', 'exit'}:
        break

    turno, inter_id = gm.interagir(user_in, inter_id, character_context=db.get_character(personagem_id))
    print('\n📜', turno.narrativa_ic)
    print('\n⚙️', turno.comando_ooc)

    if turno.teste_sugerido:
        res = rolar_pool_aethelgard(6, 1)
        print('🎲', res)

    sm.registrar_turno(user_in, {'narrativa_ic': turno.narrativa_ic, 'comando_ooc': turno.comando_ooc, 'fadiga': 0})
