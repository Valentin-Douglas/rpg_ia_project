# entities.py
from enum import Enum

class Role(Enum):
    PLAYER = "Jogador"
    ALLY = "Aliado"
    ENEMY = "Inimigo"

class Entity:
    """
    Representa uma entidade no jogo (Jogador, Aliado, Inimigo).
    A força da entidade é medida pela soma de seus pontos investidos.
    """
    def __init__(self, name: str, role: Role):
        self.name = name
        self.role = role

        # Atributos: Força, Agilidade, Vigor, Mana (1-5)
        self.attributes = {
            "forca": 1,
            "agilidade": 1,
            "vigor": 1,
            "mana": 1,
        }

        # Perícias (Habilidades): Começa vazio e pode ser expandido
        self.skills = {}

        # Habilidades Únicas (absorvidas)
        self.unique_abilities = []

        self.xp = 0  # Essência acumulada para gastar
        self.fatigue = 0  # Níveis de Fadiga (0-5)
        self.is_alive = True

    def get_power_level(self) -> int:
        """Calcula a força total da entidade somando atributos e perícias."""
        return sum(self.attributes.values()) + sum(self.skills.values())

    def gain_xp(self, amount: int):
        """Adiciona Essência (XP) à entidade."""
        if amount > 0:
            self.xp += amount

    def spend_xp(self, characteristic_name: str, is_attribute: bool) -> bool:
        """
        Gasta XP para aumentar um Atributo or Perícia.
        - Custo de Atributo: Nível Atual x 5 XP
        - Custo de Perícia: Nível Atual x 3 XP (ou 3 XP para Nível 1)
        """
        if is_attribute:
            if characteristic_name not in self.attributes:
                return False
            
            current_level = self.attributes[characteristic_name]
            cost = current_level * 5
            
            if self.xp >= cost and current_level < 5: # Limite de 5 para atributos
                self.xp -= cost
                self.attributes[characteristic_name] += 1
                return True
        else: # É uma perícia
            if characteristic_name not in self.skills:
                # Adiciona nova perícia se não existir
                self.skills[characteristic_name] = 0

            current_level = self.skills[characteristic_name]
            cost = max(1, current_level) * 3 # Custo mínimo de 3 XP para nível 1
            
            if self.xp >= cost and current_level < 5: # Limite de 5 para perícias
                self.xp -= cost
                self.skills[characteristic_name] += 1
                return True
        
        return False
