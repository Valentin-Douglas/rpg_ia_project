# main.py
import sys
import io

# Garante que o stdout lida com UTF-8 corretamente para exibir caracteres especiais
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from entities import Entity, Role
from dice_logic import DiceLogic
from narrator_engine import NarratorEngine

def main():
    """
    Esta função principal contém um exemplo de teste para verificar a integração
    entre os módulos após a correção do dice_logic.py.
    """
    print("--- Verificando a nova integração do `dice_logic.py` ---")

    # 1. Criação de Entidade e Narrador
    player = Entity(name="Tester", role=Role.PLAYER)
    narrator = NarratorEngine()

    # 2. Adicionar uma perícia para o teste
    player.skills["combate"] = 2
    player.fatigue = 1
    print("\nFicha da Entidade para o teste:")
    print(narrator.show_sheet(player))

    # 3. Realizar o teste de habilidade usando a nova DiceLogic
    print("\n--- Realizando Teste de Força + Combate (Dificuldade 2) ---")
    dificuldade_teste = 2
    resultado = DiceLogic.teste_habilidade(
        entity=player,
        atributo="forca",
        pericia="combate",
        dificuldade=dificuldade_teste
    )

    # 4. Exibir o resultado formatado
    print("\n--- Resultado da Rolagem ---")
    print(DiceLogic.formatar_resultado(resultado))
    
    # 5. Interpretar o resultado
    print("\n--- Interpretação ---")
    if resultado["resultado_final"]:
        print("O teste foi um SUCESSO!")
    else:
        print("O teste foi uma FALHA.")
    
    if resultado["critico_bestial"]:
        print("Houve um crítico bestial!")
    if resultado["falha_bestial"]:
        print("Houve uma falha bestial!")


if __name__ == "__main__":
    main()
