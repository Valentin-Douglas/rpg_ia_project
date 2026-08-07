# main.py
import sys
import io

# Garante que o stdout lida com UTF-8 corretamente para exibir caracteres especiais
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from entities import Entity, Role, Rank
from dice_logic import DiceLogic
from narrator_engine import NarratorEngine

# main.py
import sys
import io

# Garante que o stdout lida com UTF-8 corretamente para exibir caracteres especiais
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from entities import Entity, Role, Rank
from dice_logic import DiceLogic
from narrator_engine import NarratorEngine

def main():
    """
    Função principal de teste para verificar a nova estrutura da entidade
    e a lógica de evolução do personagem.
    
    Para o Gemini Notebook, as interações do jogador (inputs) seriam capturadas
    e usadas para chamar as funções e métodos da Engine de forma limpa.
    """
    # print("--- RPG Engine Test ---")

    # 1. Criação de Entidade e Narrador
    # No Gemini Notebook, os dados abaixo poderiam vir de inputs do jogador
    # no início da sessão ou através de formulários/prompts interativos.
    # Exemplo:
    # player_name = input("Qual o nome do seu personagem? ")
    # player_conceito = input("Qual o conceito do seu personagem? ")
    # # Exemplo de criação de entidade com dados fixos para teste:
    # player = Entity(
    #     name="Zack", 
    #     role=Role.PLAYER,
    #     conceito="Mercenário Dimensional",
    #     origem="Terra-7B",
    #     ambicao="Encontrar o caminho de volta para casa"
    # )
    # narrator = NarratorEngine()

    # 2. Adicionar XP e mostrar a ficha inicial
    # O ganho de XP (Essência) ocorreria com base nas ações narrativas do jogador.
    # # Exemplo: player.gain_xp(narrator.resolve_narrative_event())
    # player.gain_xp(100)
    # print("\n--- Ficha Inicial ---")
    # print(narrator.show_sheet(player))
    # print(f"HP: {player.hp}, MP: {player.mp}")

    # 3. Evoluir Atributo (Força de 1 para 2)
    # A evolução seria uma escolha explícita do jogador em um menu de progressão.
    # Exemplo:
    # choice = input("Deseja evoluir qual atributo? (forca, agilidade, ...) ")
    # # if choice == "forca": player.spend_xp("forca", is_attribute=True)
    # print("\n--- Tentando evoluir Força (Custo: 5 XP) ---")
    # if player.spend_xp("forca", is_attribute=True):
    #     print("Força evoluída com sucesso!")
    # else:
    #     print("Falha ao evoluir Força. XP insuficiente ou nível máximo atingido.")
    # print(f"XP restante: {player.xp}")
    # print(narrator.show_sheet(player))

    # 4. Comprar Perícia Nova (Combate Nível 1)
    # O jogador escolheria comprar uma nova perícia.
    # Exemplo:
    # skill_to_buy = input("Qual perícia deseja comprar? ")
    # player.spend_xp(skill_to_buy, is_attribute=False)
    # print("\n--- Tentando comprar Perícia 'Combate' (Custo: 10 XP) ---")
    # if player.spend_xp("combate", is_attribute=False):
    #     print("Perícia 'Combate' comprada com sucesso!")
    # else:
    #     print("Falha ao comprar perícia. XP insuficiente.")
    # print(f"XP restante: {player.xp}")
    # print(narrator.show_sheet(player))

    # 5. Evoluir Perícia (Combate de 1 para 2)
    # # O jogador escolheria evoluir uma perícia existente.
    # print("\n--- Tentando evoluir Perícia 'Combate' (Custo: 3 XP) ---")
    # if player.spend_xp("combate", is_attribute=False):
    #     print("Perícia 'Combate' evoluída com sucesso!")
    # else:
    #     print("Falha ao evoluir perícia. XP insuficiente ou nível máximo atingido.")
    # print(f"XP restante: {player.xp}")
    # print(narrator.show_sheet(player))

    # 6. Absorver Habilidade Única (Rank C)
    # A absorção de habilidades únicas seria uma opção narrativa ou de progressão.
    # Exemplo:
    # power_choice = input("Deseja absorver 'Cura Acelerada' (Rank C)? (s/n) ")
    # if power_choice.lower() == 's':
    # #    player.absorver_habilidade_unica("Cura Acelerada", Rank.C)
    # print(f"\n--- Tentando absorver 'Cura Acelerada (Rank C)' (Custo: {Rank.C.value} XP) ---")
    # if player.absorver_habilidade_unica("Cura Acelerada", Rank.C):
    #     print("Habilidade absorvida com sucesso!")
    # else:
    #     print("Falha ao absorver habilidade. XP insuficiente.")
    # print(f"XP restante: {player.xp}")

    # 7. Mostrar a ficha final
    # # A ficha é mostrada em pontos chave de decisão ou ao final de um turno.
    # print("\n--- Ficha Final ---")
    # print(narrator.show_sheet(player))


if __name__ == "__main__":
    main()
