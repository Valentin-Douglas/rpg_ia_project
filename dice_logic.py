# dice_logic.py
from entities import Entity
from rpg_dice import rolar_pool, formatar_resultado_pool

class DiceLogic:
    """
    Esta classe serve como uma interface entre a lógica de jogo (entidades, atributos)
    e o motor de rolagem de dados (rpg_dice.py). No Gemini Notebook, esta classe
    seria chamada pelo narrador sempre que uma ação do jogador exigir um teste.
    """
    @staticmethod
    def teste_habilidade(entity: Entity, atributo: str, pericia: str, dificuldade: int) -> dict:
        """
        Realiza um teste de habilidade para uma entidade.

        No Gemini Notebook, esta função seria o núcleo para resolver ações incertas.
        Por exemplo, se um jogador digitar "Tento escalar o muro", o narrador
        identificaria a ação, definiria o atributo ('forca'), a perícia ('mobilidade')
        e a dificuldade, e então chamaria esta função.

        Exemplo de chamada baseada no input:
        # input_jogador = "Tento arrombar a porta"
        # if "arrombar" in input_jogador:
        #     resultado = DiceLogic.teste_habilidade(player, "forca", "combate", dificuldade=2)

        Parâmetros:
        - entity: A entidade que realiza o teste.
        - atributo: O nome do atributo a ser usado (ex: "forca").
        - pericia: O nome da perícia a ser usada (ex: "combate").
        - dificuldade: O número de sucessos necessários.

        Retorna:
        - Um dicionário com o resultado completo da rolagem.
        """
        attribute_level = entity.attributes.get(atributo, 0)
        skill_level = entity.skills.get(pericia, 0)
        
        pool_total = attribute_level + skill_level
        nivel_fadiga = entity.fatigue

        # A chamada para rolar_pool é interna e não precisa de interação direta do jogador.
        resultado_rolagem = rolar_pool(
            pool=pool_total,
            fadiga=nivel_fadiga,
            dificuldade=dificuldade
        )
        
        return resultado_rolagem

    @staticmethod
    def formatar_resultado(resultado: dict) -> str:
        """
        Formata o dicionário de resultado da rolagem em uma string legível.
        Esta função é usada para apresentar o resultado do teste ao jogador
        de forma clara no Gemini Notebook.
        """
        return formatar_resultado_pool(resultado)
