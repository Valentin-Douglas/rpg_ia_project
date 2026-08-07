"""
rpg_dice.py
===========
Este script é o motor de rolagem de dados do RPG. Ele não é projetado para
ser chamado diretamente a partir de um input do jogador no Gemini Notebook.

Em vez disso, a classe `DiceLogic` atua como uma ponte. O fluxo é:
1. Jogador envia um comando (ex: "atacar o guarda").
2. O Narrador interpreta a ação e chama `DiceLogic.teste_habilidade()`.
3. `DiceLogic` determina o pool de dados e chama `rolar_pool()` deste arquivo.
"""

import random

def rolar_pool(pool: int, fadiga: int = 0, dificuldade: int = 1) -> dict:
    """
    Rola um pool de dados (d10) e retorna um dicionário com os resultados.
    Esta função é o núcleo mecânico dos testes e não deve ser exposta
    diretamente ao jogador.
    """
    num_total_dados = pool
    num_dados_fadiga = min(num_total_dados, max(0, fadiga))
    num_dados_normais = num_total_dados - num_dados_fadiga

    resultados_normais = [random.randint(1, 10) for _ in range(num_dados_normais)]
    resultados_fadiga = [random.randint(1, 10) for _ in range(num_dados_fadiga)]
    todos = resultados_normais + resultados_fadiga

    sucessos_totais = sum(1 for d in todos if d >= 6)

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
    """
    Formata o dicionário de resultados em uma string legível para o jogador.
    É chamado pelo `DiceLogic` para exibir os resultados no Gemini Notebook.
    """
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

# # Modelo de uso para testes diretos do script
# if __name__ == "__main__":
#     pool_value = random.randint(1, 10)
#     fadiga_value = random.randint(1, 5)
#     dificuldade_value = random.randint(1, 20)

#     resultado_pool = rolar_pool(pool=pool_value, fadiga=fadiga_value, dificuldade=dificuldade_value)
#     print("--- Teste de Rolagem de Dados ---")
#     print(formatar_resultado_pool(resultado_pool))