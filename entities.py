# entities.py
from enum import Enum

class Role(Enum):
    PLAYER = "Jogador"
    ALLY = "Aliado"
    ENEMY = "Inimigo"

class Rank(Enum):
    F = 5
    E = 15
    D = 25
    C = 50
    B = 75
    A = 150
    S = 300
    SS = 500
    SSS = 2000

class Entity:
    """
    Representa uma entidade no jogo (Jogador, Aliado, Inimigo).
    A força da entidade é medida pela soma de seus pontos investidos.
    """
    def __init__(self, name: str, role: Role, conceito: str = None, origem: str = None, ambicao: str = None, ancora_moral: str = None, gatilho_colapso: str = None):
        self.name = name
        self.role = role
        
        # I. IDENTIDADE E ANTECEDENTES
        self.conceito = conceito
        self.origem = origem
        self.ambicao = ambicao
        self.ancora_moral = ancora_moral
        self.gatilho_colapso = gatilho_colapso

        # II. ATRIBUTOS NUCLEARES (1-5)
        self.attributes = {
            "forca": 1,
            "agilidade": 1,
            "vitalidade": 1,
            "eloquencia": 1,
            "inteligencia": 1,
            "foco": 1,
        }

        # III. PERÍCIAS (0-5)
        self.skills = {}

        # V. PODERES (Habilidades Únicas)
        self.unique_abilities = []

        # VI. EVOLUÇÃO (Essência)
        self.xp = 0
        
        # IV. MOTOR DE RISCO E CONDIÇÃO
        self.fatigue = 0  # Níveis de Fadiga (0-5)
        self.is_alive = True

    @property
    def hp(self) -> int:
        """HP é calculado por Vitalidade + Foco."""
        return self.attributes.get("vitalidade", 0) + self.attributes.get("foco", 0)

    @property
    def mp(self) -> int:
        """MP é calculado por Foco + Inteligência."""
        return self.attributes.get("foco", 0) + self.attributes.get("inteligencia", 0)

    def get_power_level(self) -> int:
        """Calcula a força total da entidade somando atributos e perícias."""
        return sum(self.attributes.values()) + sum(self.skills.values())

    def gain_xp(self, amount: int):
        """Adiciona Essência (XP) à entidade."""
        if amount > 0:
            self.xp += amount

    def absorver_habilidade_unica(self, habilidade_nome: str, rank: Rank) -> bool:
        """
        Gasta XP para absorver uma Habilidade Única com base no seu Rank.
        """
        cost = rank.value
        if self.xp >= cost:
            self.xp -= cost
            self.unique_abilities.append(f"{habilidade_nome} (Rank {rank.name})")
            return True
        return False

    def spend_xp(self, characteristic_name: str, is_attribute: bool) -> bool:
        """
        Gasta XP para aumentar um Atributo ou Perícia.
        - Custo de Atributo: Nível Atual x 5 XP
        - Custo de Perícia Nova: 10 XP para Nível 1
        - Custo de Evoluir Perícia: Nível Atual x 3 XP
        """
        if is_attribute:
            if characteristic_name not in self.attributes:
                return False
            
            current_level = self.attributes[characteristic_name]
            if current_level >= 5: return False # Limite de 5 para atributos
            
            cost = current_level * 5
            
            if self.xp >= cost:
                self.xp -= cost
                self.attributes[characteristic_name] += 1
                return True
        else: # É uma perícia
            current_level = self.skills.get(characteristic_name, 0)
            if current_level >= 5: return False # Limite de 5 para perícias

            if current_level == 0: # Comprar nova perícia
                cost = 10
                if self.xp >= cost:
                    self.xp -= cost
                    self.skills[characteristic_name] = 1
                    return True
            else: # Evoluir perícia existente
                cost = current_level * 3
                if self.xp >= cost:
                    self.xp -= cost
                    self.skills[characteristic_name] += 1
                    return True
        
        return False
