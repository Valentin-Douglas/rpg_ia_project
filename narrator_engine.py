from entities import Personagem
from dice_logic import rolar_dados
import re

class NarratorEngine:
    RANK_BONUS = {
        "F": 1, "E": 2, "D": 3, "C": 4, "B": 5, 
        "A": 6, "S": 7, "SS": 8, "SSS": 9
    }

    def __init__(self, personagem):
        self.personagem = personagem

    def realizar_teste(self, atributo, pericia, dificuldade):
        """
        Realiza um teste de atributo + perícia contra uma dificuldade.
        """
        pool = self.personagem.atributos[atributo.upper()] + self.personagem.pericias[pericia]
        
        resultado_rolagem = rolar_dados(pool, self.personagem.exaustao)
        sucessos = resultado_rolagem['sucessos']

        if sucessos >= dificuldade:
            print("Resultado do Teste: SUCESSO!")
            return True
        else:
            print("Resultado do Teste: FALHA.")
            return False

    def combate(self, oponente, atributo_ataque, pericia_ataque, atributo_defesa, pericia_defesa):
        """
        Realiza uma rodada de combate simples.
        """
        # Ataque
        print(f"--- {self.personagem.nome} ataca {oponente.nome} ---")
        pool_ataque = self.personagem.atributos[atributo_ataque.upper()] + self.personagem.pericias[pericia_ataque]
        resultado_ataque = rolar_dados(pool_ataque, self.personagem.exaustao)
        sucessos_ataque = resultado_ataque['sucessos']

        # Defesa
        print(f"--- {oponente.nome} defende ---")
        pool_defesa = oponente.atributos[atributo_defesa.upper()] + oponente.pericias[pericia_defesa]
        resultado_defesa = rolar_dados(pool_defesa, oponente.exaustao)
        sucessos_defesa = resultado_defesa['sucessos']

        print("--- Resolução do Combate ---")
        if sucessos_ataque > sucessos_defesa:
            dano = sucessos_ataque - sucessos_defesa
            # A lógica de aplicar o dano (reduzir HP) seria implementada aqui.
            print(f"Ataque bem-sucedido! Dano causado: {dano}")
            return dano
        else:
            print("Ataque falhou ou foi defendido.")
            return 0

    def _aplicar_custo_poder(self, exigencia_str):
        """Aplica o custo de um poder (MP ou Exaustão)."""
        # Custo de MP
        custo_mp_match = re.search(r"custa (\d+) de m[p|ana]", exigencia_str, re.IGNORECASE)
        if custo_mp_match:
            custo = int(custo_mp_match.group(1))
            if self.personagem.mp >= custo:
                self.personagem.mp -= custo
                print(f"Gasto {custo} de MP. MP restante: {self.personagem.mp}")
                return True
            else:
                print(f"MP insuficiente para usar o poder. MP necessário: {custo}, MP atual: {self.personagem.mp}")
                return False
        
        # Custo de Exaustão
        custo_exaustao_match = re.search(r"gera \+(\d+) de exaustão", exigencia_str, re.IGNORECASE)
        if custo_exaustao_match:
            custo = int(custo_exaustao_match.group(1))
            if self.personagem.exaustao < 5:
                 self.personagem.exaustao += custo
                 print(f"Personagem ganha {custo} de Exaustão. Nível atual: {self.personagem.exaustao}")
                 # Limita a exaustão a 5
                 if self.personagem.exaustao > 5:
                     self.personagem.exaustao = 5
                 return True
            else:
                print("Personagem já está no nível máximo de exaustão.")
                return False # Ou talvez o poder ainda funcione, mas com penalidade máxima? Decisão de mestre.

        return True # Poder não tem custo definido que o sistema entenda

    def soltar_poder(self, nome_poder, atributo, pericia, dificuldade):
        """
        Tenta usar um poder, pagando seu custo e realizando um teste.
        A rolagem inclui um bônus de dados baseado no Rank do poder.
        A escolha do atributo e da perícia é uma decisão do Mestre (o usuário do notebook).
        """
        poder_encontrado = None
        for p in self.personagem.poderes:
            if p['Nome'].lower() == nome_poder.lower():
                poder_encontrado = p
                break
        
        if not poder_encontrado:
            print(f"Poder '{nome_poder}' não encontrado na ficha do personagem.")
            return False

        print(f"--- {self.personagem.nome} tenta usar o poder: {poder_encontrado['Nome']} ---")

        # 1. Aplicar o custo ANTES do teste
        if not self._aplicar_custo_poder(poder_encontrado['Exigencia']):
            # Não foi possível pagar o custo
            return False

        # 2. Calcular o pool de dados para a conjuração
        base_pool = self.personagem.atributos[atributo.upper()] + self.personagem.pericias[pericia]
        rank_bonus = self.RANK_BONUS.get(poder_encontrado['Rank'].upper(), 0)
        total_pool = base_pool + rank_bonus

        print(f"Teste de conjuração: {atributo} ({self.personagem.atributos[atributo.upper()]}) + {pericia} ({self.personagem.pericias[pericia]}) + Bônus de Rank {poder_encontrado['Rank']} (+{rank_bonus}d) vs Dificuldade {dificuldade}")
        print(f"Pool Total: {total_pool} dados")

        # 3. Realizar o teste
        resultado_rolagem = rolar_dados(total_pool, self.personagem.exaustao)
        sucessos = resultado_rolagem['sucessos']

        if sucessos >= dificuldade:
            print(f"Poder '{poder_encontrado['Nome']}' ativado com SUCESSO!")
            return True
        else:
            print(f"Falha ao tentar ativar o poder '{poder_encontrado['Nome']}'.")
            return False
