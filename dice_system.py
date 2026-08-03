import random


def rolar_pool_aethelgard(pool_total, fadiga):
    """
    Sistema de d10: Sucessos em 6-9, Críticos em 10 (pares somam +2).
    Fadiga substitui dados normais e pode gerar falhas atrozes.
    """
    fadiga = max(0, min(fadiga, pool_total))
    dados_normais = pool_total - fadiga

    res_normais = [random.randint(1, 10) for _ in range(dados_normais)]
    res_fadiga = [random.randint(1, 10) for _ in range(fadiga)]

    total = res_normais + res_fadiga
    sucessos = sum(1 for d in total if d >= 6)
    dez_total = total.count(10)
    sucessos += (dez_total // 2) * 2

    return {
        "sucessos": sucessos,
        "detalhes": f"Normal: {res_normais} | Fadiga: {res_fadiga}",
        "falha_bestial": (1 in res_fadiga and sucessos == 0),
    }
