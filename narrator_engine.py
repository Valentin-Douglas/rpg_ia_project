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
        Perícias e Essência (XP), seguindo o modelo de ficha.
        """
        if entity.role not in [Role.PLAYER, Role.ALLY] and entity.is_alive:
            return "[Ficha Oculta]"
        
        if not entity.is_alive:
            return f"INIMIGO DERROTADO: {entity.name}"

        # I. IDENTIDADE
        identidade = (
            f"👤 IDENTIDADE E ANTECEDENTES\n"
            f"   Nome: {entity.name} | Conceito: {entity.conceito or 'Não definido'}\n"
            f"   Origem: {entity.origem or 'Não definido'}\n"
            f"   Ambição: {entity.ambicao or 'Não definido'}\n"
            f"   Âncora Moral: {entity.ancora_moral or 'Não definido'}\n"
            f"   Gatilho de Colapso: {entity.gatilho_colapso or 'Não definido'}\n"
        )

        # II. ATRIBUTOS
        attrs = entity.attributes
        atributos = (
            f"🧬 ATRIBUTOS NUCLEARES\n"
            f"   Força: {attrs['forca']} | Agilidade: {attrs['agilidade']} | Vitalidade: {attrs['vitalidade']} | "
            f"Eloquência: {attrs['eloquencia']} | Inteligência: {attrs['inteligencia']} | Foco: {attrs['foco']}\n"
        )

        # III. PERÍCIAS
        skills_list = [f"{name.capitalize()}({level})" for name, level in entity.skills.items()]
        skills_str = ", ".join(skills_list) if skills_list else "Nenhuma"
        pericias = (
            f"🎭 PERÍCIAS\n"
            f"   {skills_str}\n"
        )

        # IV. MOTOR DE RISCO
        motor_risco = (
            f"⚠️ MOTOR DE RISCO E CONDIÇÃO\n"
            f"   HP: {entity.hp} | MP: {entity.mp} | Fadiga: {entity.fatigue}/5\n"
        )

        # V. PODERES
        poderes_str = ', '.join(entity.unique_abilities) if entity.unique_abilities else 'Nenhum'
        poderes = (
            f"🔮 PODERES\n"
            f"   {poderes_str}\n"
        )

        # VI. EVOLUÇÃO
        evolucao = (
            f"💠 EVOLUÇÃO\n"
            f"   Essência (XP): {entity.xp}\n"
            f"   Poder Total: {entity.get_power_level()}"
        )

        return "\n".join(["--- Ficha de Personagem ---", identidade, atributos, pericias, motor_risco, poderes, evolucao])

    @staticmethod
    def present_choices(choices: list):
        print("\nO que você faz?")
        for choice in choices[:3]:
            print(f"– {choice}")
