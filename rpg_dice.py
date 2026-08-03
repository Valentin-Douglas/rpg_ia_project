"""
rpg_dice.py
===========
Script de rolagem de dados de RPG em Python puro — sem dependências
externas, compatível com o notebook do Gemini (ou qualquer Jupyter/Colab).

Implementa:
  - Rolagem genérica de dados (qualquer tamanho, qualquer quantidade)
  - Notação padrão de RPG (ex: "2d6+3")
  - Vantagem/Desvantagem (padrão D&D 5E: rola 2, pega maior/menor)
  - Testes do Sistema Daemon (1d100, Fácil/Difícil, Atributo vs Atributo,
    Perícia vs Perícia)
  - Rolagem de pool de dados do Vampire: The Masquerade 5ª Ed.
    (d10, sucessos, críticos, dados de Fome)

Cada dado é sorteado individualmente (random.randint chamado uma vez por
dado), então o resultado nunca é influenciado pela quantidade de dados
rolados na mesma chamada.
"""

import random


# ---------------------------------------------------------------------------
# Rolagem genérica
# ---------------------------------------------------------------------------

def rolar_dados(quantidade: int, lados: int, modificador: int = 0) -> dict:
    """Rola 'quantidade' dados de 'lados' faces, cada um sorteado
    independentemente, e soma um modificador opcional."""
    resultados = [random.randint(1, lados) for _ in range(quantidade)]
    total = sum(resultados) + modificador
    return {
        "notacao": f"{quantidade}d{lados}" + (f"{modificador:+d}" if modificador else ""),
        "resultados_individuais": resultados,
        "modificador": modificador,
        "total": total,
    }


def rolar_notacao(notacao: str) -> dict:
    """Aceita notação padrão de RPG, ex: '2d6+3', '1d20', '4d8-2', '1d100'."""
    limpa = notacao.replace(" ", "").lower()
    modificador = 0

    if "+" in limpa:
        base, mod = limpa.split("+")
        modificador = int(mod)
    elif "-" in limpa[1:]:
        idx = limpa.index("-", 1)
        base, mod = limpa[:idx], limpa[idx:]
        modificador = int(mod)
    else:
        base = limpa

    quantidade_str, lados_str = base.split("d")
    quantidade = int(quantidade_str) if quantidade_str else 1
    lados = int(lados_str)

    return rolar_dados(quantidade, lados, modificador)


def rolar_com_vantagem(lados: int = 20, modificador: int = 0, modo: str = "vantagem") -> dict:
    """Rola 2 dados independentes e pega o maior ('vantagem') ou o menor
    ('desvantagem') — mecânica padrão de d20 (D&D 5E)."""
    d1 = random.randint(1, lados)
    d2 = random.randint(1, lados)
    if modo == "desvantagem":
        escolhido = min(d1, d2)
    else:
        modo = "vantagem"
        escolhido = max(d1, d2)
    return {
        "modo": modo,
        "dados_rolados": [d1, d2],
        "dado_escolhido": escolhido,
        "modificador": modificador,
        "total": escolhido + modificador,
    }


# ---------------------------------------------------------------------------
# Sistema Daemon (Anime RPG)
# ---------------------------------------------------------------------------

def _finalizar_teste_daemon(tipo: str, valor_final: float, dificuldade: str, extra: dict) -> dict:
    if valor_final > 100:
        resultado = {
            "sistema": "Daemon",
            "tipo": tipo,
            "dificuldade": dificuldade,
            "valor_final": round(valor_final, 1),
            "rolagem": None,
            "sucesso": True,
            "observacao": "Valor final acima de 100%: sucesso automático (sem rolagem).",
        }
    else:
        rolagem = random.randint(1, 100)
        # Regra: resultado > 95 é SEMPRE falha, independente do valor testado.
        sucesso = rolagem <= valor_final and rolagem <= 95
        resultado = {
            "sistema": "Daemon",
            "tipo": tipo,
            "dificuldade": dificuldade,
            "valor_final": round(valor_final, 1),
            "rolagem": rolagem,
            "sucesso": sucesso,
        }
    resultado.update(extra)
    return resultado


def teste_atributo_daemon(valor_atributo: int, dificuldade: str = "normal") -> dict:
    """Teste de Atributo do Sistema Daemon: valor = atributo x4.
    dificuldade: 'facil' (dobro), 'dificil' (metade) ou 'normal'."""
    valor_base = valor_atributo * 4
    if dificuldade == "facil":
        valor_final = valor_base * 2
    elif dificuldade == "dificil":
        valor_final = valor_base / 2
    else:
        dificuldade = "normal"
        valor_final = valor_base
    return _finalizar_teste_daemon(
        "Teste de Atributo", valor_final, dificuldade, {"valor_atributo": valor_atributo, "valor_base": valor_base}
    )


def teste_pericia_daemon(valor_pericia: int, dificuldade: str = "normal") -> dict:
    """Teste de Perícia do Sistema Daemon: valor = valor da própria perícia
    (sem multiplicar). dificuldade: 'facil' (dobro), 'dificil' (metade) ou 'normal'."""
    valor_base = valor_pericia
    if dificuldade == "facil":
        valor_final = valor_base * 2
    elif dificuldade == "dificil":
        valor_final = valor_base / 2
    else:
        dificuldade = "normal"
        valor_final = valor_base
    return _finalizar_teste_daemon(
        "Teste de Perícia", valor_final, dificuldade, {"valor_base": valor_base}
    )


def teste_atributo_vs_atributo_daemon(fonte_ativa: int, fonte_passiva: int) -> dict:
    """Atributo vs Atributo (Sistema Daemon): diferença x5 + 50%.
    Diferença >= 10 = sucesso automático da Fonte Ativa;
    diferença <= -10 = sucesso automático da Fonte Passiva."""
    diferenca = fonte_ativa - fonte_passiva
    if diferenca >= 10:
        return {
            "sistema": "Daemon", "tipo": "Atributo vs Atributo", "diferenca": diferenca,
            "rolagem": None, "vencedor": "Fonte Ativa", "observacao": "Sucesso automático.",
        }
    if diferenca <= -10:
        return {
            "sistema": "Daemon", "tipo": "Atributo vs Atributo", "diferenca": diferenca,
            "rolagem": None, "vencedor": "Fonte Passiva", "observacao": "Sucesso automático.",
        }
    chance = diferenca * 5 + 50
    rolagem = random.randint(1, 100)
    vence_ativa = rolagem <= chance
    return {
        "sistema": "Daemon",
        "tipo": "Atributo vs Atributo",
        "diferenca": diferenca,
        "chance_fonte_ativa": chance,
        "rolagem": rolagem,
        "vencedor": "Fonte Ativa" if vence_ativa else "Fonte Passiva",
    }


def teste_pericia_vs_pericia_daemon(pericia_ativa: int, pericia_passiva: int) -> dict:
    """Perícia vs Perícia (Sistema Daemon): 50% + perícia ativa - perícia passiva."""
    chance = 50 + pericia_ativa - pericia_passiva
    if chance >= 100:
        return {
            "sistema": "Daemon", "tipo": "Perícia vs Perícia", "chance_fonte_ativa": 100,
            "rolagem": None, "vencedor": "Fonte Ativa", "observacao": "Sucesso automático.",
        }
    if chance <= 0:
        return {
            "sistema": "Daemon", "tipo": "Perícia vs Perícia", "chance_fonte_ativa": 0,
            "rolagem": None, "vencedor": "Fonte Passiva", "observacao": "Sucesso automático.",
        }
    rolagem = random.randint(1, 100)
    vence_ativa = rolagem <= chance
    return {
        "sistema": "Daemon",
        "tipo": "Perícia vs Perícia",
        "chance_fonte_ativa": chance,
        "rolagem": rolagem,
        "vencedor": "Fonte Ativa" if vence_ativa else "Fonte Passiva",
    }


# ---------------------------------------------------------------------------
# Vampire: The Masquerade (5ª Edição) — Storyteller System
# ---------------------------------------------------------------------------

def rolar_pool_vampiro(pool: int, fome: int = 0, dificuldade: int = 1) -> dict:
    """Rola um pool de d10 do Vampire: The Masquerade.
    'fome' dados do pool são substituídos por dados de Fome (vermelhos).
    Cada 6-9 = 1 sucesso; cada 10 = 1 sucesso e conta para par crítico
    (cada par de 10 vale +2 sucessos extras, total 4). 'dificuldade' é o
    número de sucessos necessários para vencer o teste."""
    fome = max(0, min(fome, pool))
    dados_normais_qtd = pool - fome

    dados_normais = [random.randint(1, 10) for _ in range(dados_normais_qtd)]
    dados_fome = [random.randint(1, 10) for _ in range(fome)]
    todos = dados_normais + dados_fome

    sucessos_simples = sum(1 for d in todos if d >= 6)
    total_dez = todos.count(10)
    pares_de_dez = total_dez // 2
    sucessos_totais = sucessos_simples + pares_de_dez * 2  # cada par vira 4 no total

    critico = pares_de_dez > 0
    dez_em_fome = dados_fome.count(10)
    critico_messy = critico and dez_em_fome > 0

    vitoria = sucessos_totais >= dificuldade
    margem = max(0, sucessos_totais - dificuldade) if vitoria else 0

    uns_em_fome = dados_fome.count(1)
    falha_bestial = (not vitoria) and uns_em_fome > 0

    return {
        "sistema": "Vampire: The Masquerade",
        "pool": pool,
        "dados_fome": fome,
        "resultados_normais": dados_normais,
        "resultados_fome": dados_fome,
        "sucessos": sucessos_totais,
        "dificuldade": dificuldade,
        "vitoria": vitoria,
        "margem": margem,
        "critico": critico,
        "critico_messy": critico_messy,
        "falha_bestial": falha_bestial,
    }


# ---------------------------------------------------------------------------
# Exemplos de uso — rode este arquivo diretamente ou copie as chamadas
# para uma célula do notebook do Gemini
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Dados genéricos:")
    print(rolar_dados(1, 20))
    print(rolar_notacao("2d10+5"))
    print(rolar_com_vantagem(20, 3, "vantagem"))

    print("\nSistema Daemon:")
    print(teste_atributo_daemon(15, "normal"))
    print(teste_pericia_daemon(30, "facil"))
    print(teste_atributo_vs_atributo_daemon(16, 13))
    print(teste_pericia_vs_pericia_daemon(40, 30))

    print("\nVampire: The Masquerade:")
    print(rolar_pool_vampiro(6, fome=2, dificuldade=2))
