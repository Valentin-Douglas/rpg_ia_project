"""
rpg_dice.py
===========
Script de rolagem de dados de RPG em Python puro — sem dependências
externas, compatível com o notebook do Gemini.
"""

import random
import json


# ---------------------------------------------------------------------------
# Storyteller System 
# ---------------------------------------------------------------------------

def rolar_pool(pool: int, fadiga: int = 0, dificuldade: int = 1) -> dict:
    """ Rola um pool de dados do Storyteller System (Customizado) e retorna um dicionário com os resultados.
    Parâmetros:
    - pool: quantidade de dados normais a serem rolados (d10)
    - fadiga: quantidade de dados de fadiga a serem rolados (d10)
    - dificuldade: número de sucessos necessários para o teste ser bem-sucedido
    Retorna:
    - dicionário com os resultados da rolagem, incluindo:
        - sistema: nome do sistema de RPG
        - pool: quantidade de dados normais rolados
        - dados_fadiga: quantidade de dados de fadiga rolados
        - resultados_normais: lista com os resultados dos dados normais
        - resultados_fadiga: lista com os resultados dos dados de fadiga
        - sucessos: quantidade total de sucessos obtidos
        - dificuldade: número de sucessos necessários para o teste ser bem-sucedido
        - resultado_final: True se o teste foi bem-sucedido, False caso contrário
        - sucesso_critico: True se houve um sucesso crítico (1 ou mais 10s nos dados de fadiga), False caso contrário
        - falha_critica: True se houve uma falha crítica (1 ou mais 1s nos dados de fadiga), False caso contrário
"""
    # Define a quantidade de dados a rolar, implementando a troca de dados normais por dados de fadiga
    num_total_dados = pool
    num_dados_fadiga = min(num_total_dados, max(0, fadiga))
    num_dados_normais = num_total_dados - num_dados_fadiga

    # Rolagem dos dados
    resultados_normais = [random.randint(1, 10) for _ in range(num_dados_normais)]
    resultados_fadiga = [random.randint(1, 10) for _ in range(num_dados_fadiga)]
    todos = resultados_normais + resultados_fadiga

    # Contagem de sucessos simples (qualquer dado >= 6)
    sucessos_totais = sum(1 for d in todos if d >= 6)

    # Flags de estado da rolagem, baseadas apenas nos dados de fadiga
    sucesso_critico = resultados_fadiga.count(10) >= 1
    falha_critica = resultados_fadiga.count(1) >= 1

    resultado_final = sucessos_totais >= dificuldade

    return {
        "sistema": "Motor de RPG MCP (README)",
        "pool": pool,
        "dados_fadiga": num_dados_fadiga,
        "resultados_normais": resultados_normais,
        "resultados_fadiga": resultados_fadiga,
        "sucessos": sucessos_totais,
        "dificuldade": dificuldade,
        "resultado_final": resultado_final,
        "sucesso_critico": sucesso_critico,
        "falha_critica": falha_critica,
    }


def formatar_resultado_pool(resultado: dict) -> str:
    """Formata o dicionário de resultados da rolagem de pool em uma string legível."""
    
    # Mapear booleanos para 'Sim'/'Nao'
    sucesso_critico_str = 'Sim' if resultado['sucesso_critico'] else 'Nao'
    falha_critica_str = 'Sim' if resultado['falha_critica'] else 'Nao'

    return (
        f"sistema: {resultado['sistema']}\n"
        f"pool: {resultado['pool']}\n"
        f"dados_fadiga: {resultado['dados_fadiga']}\n"
        f"resultados_normais: {resultado['resultados_normais']}\n"
        f"resultados_fadiga: {resultado['resultados_fadiga']}\n"
        f"sucessos: {resultado['sucessos']}\n"
        f"dificuldade: {resultado['dificuldade']}\n"
        f"resultado_final: {'Sucesso' if resultado['resultado_final'] else 'Falha'}\n"
        f"sucesso_critico: {sucesso_critico_str}\n"
        f"falha_critica: {falha_critica_str}"
    )

# # Modelo de uso 
# if __name__ == "__main__":
#     pool_value = random.randint(1, 10)
#     fadiga_value = random.randint(1, 5)
#     dificuldade_value = random.randint(1, 20)

#     resultado_pool = rolar_pool(pool=pool_value, fadiga=fadiga_value, dificuldade=dificuldade_value)
#     print(formatar_resultado_pool(resultado_pool))