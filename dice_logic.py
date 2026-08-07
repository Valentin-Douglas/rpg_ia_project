# dice_logic.py
from entities import Entity
from rpg_dice import rolar_pool, formatar_resultado_pool

class DiceLogic:
    """
    Esta classe serve como uma interface entre a lógica de jogo (entidades, atributos)
    e o motor de rolagem de dados (rpg_dice.py).
    """
    @staticmethod
    def teste_habilidade(entity: Entity, atributo: str, pericia: str, dificuldade: int) -> dict:
        """
        Realiza um teste de habilidade para uma entidade, usando o motor de dados do rpg_dice.
        
        Parâmetros:
        - entity: A entidade que está realizando o teste.
        - atributo: O nome do atributo a ser usado (ex: "forca").
        - pericia: O nome da perícia a ser usada (ex: "combate").
        - dificuldade: O número de sucessos necessários para o teste.

        Retorna:
        - Um dicionário com o resultado completo da rolagem, vindo de rpg_dice.rolar_pool.
        """
        attribute_level = entity.attributes.get(atributo, 0)
        skill_level = entity.skills.get(pericia, 0)
        
        pool_total = attribute_level + skill_level
        nivel_fadiga = entity.fatigue

        # Chama a função do motor de dados para obter o resultado
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
        """
        return formatar_resultado_pool(resultado)
