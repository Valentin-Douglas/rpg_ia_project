import random

def rolar_dados(pool_size, exhaustion_level=0):
    """
    Rola uma quantidade de dados de 10 faces, aplicando as regras de exaustão e acerto crítico.

    Args:
        pool_size (int): A quantidade total de dados a serem rolados (Atributo + Perícia).
        exhaustion_level (int): O nível de exaustão, que substitui dados normais por dados de exaustão.

    Returns:
        dict: Um dicionário contendo os resultados da rolagem.
              {
                  'sucessos': int,          # Número total de sucessos (>= 6)
                  'is_critico': bool,       # Se a rolagem foi um acerto crítico (2 ou mais 10s)
                  'complicacoes': int,      # Número de '1's em dados de exaustão
                  'consequencias': int,     # Número de '10's em dados de exaustão
                  'rolls_normais': list,    # Lista dos resultados dos dados normais
                  'rolls_exaustao': list    # Lista dos resultados dos dados de exaustão
              }
    """
    if exhaustion_level > pool_size:
        exhaustion_level = pool_size # Não pode ter mais dados de exaustão do que o pool total

    num_dados_normais = pool_size - exhaustion_level
    num_dados_exaustao = exhaustion_level

    rolls_normais = [random.randint(1, 10) for _ in range(num_dados_normais)]
    rolls_exaustao = [random.randint(1, 10) for _ in range(num_dados_exaustao)]

    todos_os_rolls = rolls_normais + rolls_exaustao

    # Calcula sucessos (qualquer dado >= 6)
    sucessos = sum(1 for r in todos_os_rolls if r >= 6)

    # Verifica acerto crítico (pelo menos dois 10s no total)
    num_tens = todos_os_rolls.count(10)
    is_critico = num_tens >= 2
    if is_critico:
        sucessos += 2  # Adiciona 2 sucessos bônus pelo crítico

    # Verifica complicações (resultado 1 nos dados de exaustão)
    complicacoes = rolls_exaustao.count(1)

    # Verifica consequências (resultado 10 nos dados de exaustão)
    consequencias = rolls_exaustao.count(10)
    
    resultado = {
        'sucessos': sucessos,
        'is_critico': is_critico,
        'complicacoes': complicacoes,
        'consequencias': consequencias,
        'rolls_normais': rolls_normais,
        'rolls_exaustao': rolls_exaustao
    }

    print(f"Rolagem: Pool={pool_size}, Exaustão={exhaustion_level}")
    print(f"  - Dados Normais: {rolls_normais}")
    print(f"  - Dados Exaustão: {rolls_exaustao}")
    print(f"  - Resultado Final: {resultado['sucessos']} sucessos.")
    if resultado['is_critico']:
        print("  - ACERTO CRÍTICO!")
    if resultado['complicacoes'] > 0:
        print(f"  - Complicações: {resultado['complicacoes']}")
    if resultado['consequencias'] > 0:
        print(f"  - Consequências: {resultado['consequencias']}")

    return resultado
