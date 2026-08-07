# narrator_engine.py
from entities import Entity, Role

class NarratorEngine:
    """
    Esta classe gerencia a interface de comunicação com o jogador.
    No Gemini Notebook, ela é responsável por toda a saída de texto que o
    jogador vê, separando a narração (IC) das informações de sistema (OOC).
    """
    @staticmethod
    def ic_message(text: str):
        """
        Envia uma mensagem 'In-Character' (dentro do personagem/narrativa).
        No Gemini Notebook, isso seria usado para descrever cenas, diálogos e ações.
        Exemplo: narrator.ic_message("A porta de carvalho range ao abrir...")
        """
        print(f"\n{text}")

    @staticmethod
    def ooc_message(data: str):
        """
        Envia uma mensagem 'Out-Of-Character' (fora do personagem, para o jogador).
        Usado para comunicar regras, ganhos de XP, ou status.
        Exemplo: narrator.ooc_message("Você ganhou 5 XP por resolver o enigma.")
        """
        print(f"\n[Sistema: {data}]")

    @staticmethod
    def show_sheet(entity: Entity):
        """
        Exibe a ficha da entidade. No Gemini Notebook, esta função seria chamada
        em momentos de pausa, como ao descansar ou ao abrir um menu de personagem,
        para que o jogador possa consultar seu estado e progresso.
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
        """
        Apresenta uma lista de ações sugeridas ao jogador. No Gemini Notebook,
        após apresentar as escolhas, o sistema aguardaria o input do jogador,
        que poderia ser uma das opções ou uma ação customizada.
        Exemplo:
        # narrator.present_choices(["Explorar a caverna", "Inspecionar o altar"])
        # player_input = input("> ")
        """
        print("\nO que você faz?")
        for choice in choices[:3]:
            print(f"– {choice}")
