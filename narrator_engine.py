# narrator_engine.py
from entities import Entity, Role

class NarratorEngine:
    @staticmethod
    def ic_message(text: str):
        print(f"\n{text}")

    @staticmethod
    def ooc_message(data: str):
        print(f"\n[Sistema: {data}]")

    @staticmethod
    def show_sheet(entity: Entity):
        """
        Exibe a ficha da entidade de forma limpa, focada nos Atributos,
        Perícias e Essência (XP).
        """
        if entity.role in [Role.PLAYER, Role.ALLY] or not entity.is_alive:
            if not entity.is_alive:
                return f"INIMIGO DERROTADO: {entity.name}"

            l1 = f"--- Ficha de {entity.name} ---"
            l2 = f"| Força: {entity.attributes['forca']} | Agilidade: {entity.attributes['agilidade']} | Vigor: {entity.attributes['vigor']} | Mana: {entity.attributes['mana']} |"
            skills_list = [f"{name.capitalize()}({level})" for name, level in entity.skills.items()]
            skills_str = ", ".join(skills_list) if skills_list else "Nenhuma"
            l3 = f"| Perícias: {skills_str} |"
            l4 = f"| Nível de Poder Total: {entity.get_power_level()} |"
            l5 = f"| Essência (XP): {entity.xp} | Fadiga: {entity.fatigue}/5 |"
            sheet_data = "\n".join([l1, l2, l3, l4, l5])
            return sheet_data
        
        return "[Ficha Oculta]"

    @staticmethod
    def present_choices(choices: list):
        print("\nO que você faz?")
        for choice in choices[:3]:
            print(f"– {choice}")
