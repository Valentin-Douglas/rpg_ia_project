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
    """
    print("--- RPG Engine Test ---")

    # 1. Criação de Entidade e Narrador
    player = Entity(
        name="Zack", 
        role=Role.PLAYER,
        conceito="Mercenário Dimensional",
        origem="Terra-7B",
        ambicao="Encontrar o caminho de volta para casa"
    )
    narrator = NarratorEngine()

    # 2. Adicionar XP e mostrar a ficha inicial
    player.gain_xp(100)
    print("\n--- Ficha Inicial ---")
    print(narrator.show_sheet(player))
    print(f"HP: {player.hp}, MP: {player.mp}")

    # 3. Evoluir Atributo (Força de 1 para 2)
    print("\n--- Tentando evoluir Força (Custo: 5 XP) ---")
    if player.spend_xp("forca", is_attribute=True):
        print("Força evoluída com sucesso!")
    else:
        print("Falha ao evoluir Força.")
    print(f"XP restante: {player.xp}")
    print(narrator.show_sheet(player))

    # 4. Comprar Perícia Nova (Combate Nível 1)
    print("\n--- Tentando comprar Perícia 'Combate' (Custo: 10 XP) ---")
    if player.spend_xp("combate", is_attribute=False):
        print("Perícia 'Combate' comprada com sucesso!")
    else:
        print("Falha ao comprar perícia.")
    print(f"XP restante: {player.xp}")
    print(narrator.show_sheet(player))

    # 5. Evoluir Perícia (Combate de 1 para 2)
    print("\n--- Tentando evoluir Perícia 'Combate' (Custo: 3 XP) ---")
    if player.spend_xp("combate", is_attribute=False):
        print("Perícia 'Combate' evoluída com sucesso!")
    else:
        print("Falha ao evoluir perícia.")
    print(f"XP restante: {player.xp}")
    print(narrator.show_sheet(player))

    # 6. Absorver Habilidade Única (Rank C)
    print(f"\n--- Tentando absorver 'Cura Acelerada (Rank C)' (Custo: {Rank.C.value} XP) ---")
    if player.absorver_habilidade_unica("Cura Acelerada", Rank.C):
        print("Habilidade absorvida com sucesso!")
    else:
        print("Falha ao absorver habilidade.")
    print(f"XP restante: {player.xp}")

    # 7. Mostrar a ficha final
    print("\n--- Ficha Final ---")
    print(narrator.show_sheet(player))



if __name__ == "__main__":
    main()
