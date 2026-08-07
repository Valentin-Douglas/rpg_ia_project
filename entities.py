import re

class Personagem:
    def __init__(self):
        # I. IDENTIDADE E ANTECEDENTES
        self.nome = ""
        self.conceito = ""
        self.origem = ""
        self.ambicao = ""
        self.ancora_moral = ""
        self.gatilho_colapso = ""

        # II. ATRIBUTOS NUCLEARES
        self.atributos = {
            "FORÇA": 1,
            "AGILIDADE": 1,
            "VITALIDADE": 1,
            "ELOQUÊNCIA": 1,
            "INTELIGÊNCIA": 1,
            "FOCO": 1
        }

        # III. PERÍCIAS
        self.pericias = {
            "Mobilidade": 0,
            "Combate corpo-a-corpo": 0,
            "Furtividade": 0,
            "Armas de Precisão": 0,
            "Sobrevivência": 0,
            "Empatia": 0,
            "Intimidação": 0,
            "Lábia": 0,
            "Liderança": 0,
            "Barganha": 0,
            "Erudição": 0,
            "Investigação": 0,
            "Medicina": 0,
            "Ocultismo": 0,
            "Tecnologia/Ofícios": 0
        }

        # IV. MOTOR DE RISCO E CONDIÇÃO
        self.exaustao = 0
        self._mp = None # Para permitir a dedução de MP
        
        # V. PODERES
        self.poderes = []

        # VI. EVOLUÇÃO
        self.xp = 0
        self.total_absorvido = 0

    @property
    def hp(self):
        return self.atributos["VITALIDADE"] + self.atributos["FOCO"]

    @property
    def mp(self):
        if self._mp is None:
            return self.atributos["FOCO"] + self.atributos["INTELIGÊNCIA"]
        return self._mp
    
    @mp.setter
    def mp(self, value):
        self._mp = value

    def adicionar_poder(self, nome, rank, efeito, exigencia):
        """Adiciona um poder à lista de poderes do personagem."""
        self.poderes.append({
            "Nome": nome,
            "Rank": rank,
            "Efeito": efeito,
            "Exigencia": exigencia
        })

    def evoluir_atributo(self, atributo, custo):
        if self.xp >= custo:
            if self.atributos[atributo] < 5:
                self.atributos[atributo] += 1
                self.xp -= custo
                print(f"Atributo {atributo} evoluído para {self.atributos[atributo]}!")
                return True
            else:
                print(f"Atributo {atributo} já está no nível máximo.")
                return False
        else:
            print("XP insuficiente.")
            return False

    def evoluir_pericia(self, pericia, custo):
        if self.xp >= custo:
            if self.pericias[pericia] < 5:
                self.pericias[pericia] += 1
                self.xp -= custo
                print(f"Perícia {pericia} evoluída para {self.pericias[pericia]}!")
                return True
            else:
                print(f"Perícia {pericia} já está no nível máximo.")
                return False
        else:
            print("XP insuficiente.")
            return False
            
    def __str__(self):
        poderes_str = "Nenhum poder adquirido."
        if self.poderes:
            poderes_str = ""
            for poder in self.poderes:
                poderes_str += f"- {poder['Nome']} (Rank: {poder['Rank']})\\n"
                poderes_str += f"  Efeito: {poder['Efeito']}\\n"
                poderes_str += f"  Exigencia: {poder['Exigencia']}\\n"

        pericias_str = "\\n".join([f"  {p}: {lvl}" for p, lvl in self.pericias.items()])

        return f"""
📜 FICHA DE PERSONAGEM 
👤 I. IDENTIDADE E ANTECEDENTES
Nome: {self.nome}
Conceito/Arquétipo: {self.conceito}
Origem/Mundo Natal: {self.origem}
Ambição: {self.ambicao}
Âncora Moral: {self.ancora_moral}
Gatilho de Colapso: {self.gatilho_colapso}

🧬 II. ATRIBUTOS NUCLEARES
FORÇA: {self.atributos['FORÇA']}
AGILIDADE: {self.atributos['AGILIDADE']}
VITALIDADE: {self.atributos['VITALIDADE']}
ELOQUÊNCIA: {self.atributos['ELOQUÊNCIA']}
INTELIGÊNCIA: {self.atributos['INTELIGÊNCIA']}
FOCO: {self.atributos['FOCO']}

🎭 III. PERÍCIAS
{pericias_str}

⚠️ IV. MOTOR DE RISCO E CONDIÇÃO
HP: {self.hp}
MP: {self.mp}
EXAUSTÃO: {self.exaustao}

🔮 V. PODERES
{poderes_str}

💠 VI. EVOLUÇÃO
XP: {self.xp}
"""


def carregar_personagem_de_arquivo(caminho_arquivo):
    personagem = Personagem()
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        content = f.read()

    # I. IDENTIDADE
    personagem.nome = re.search(r"Nome: (.*)", content).group(1).strip()
    personagem.conceito = re.search(r"Conceito/Arquétipo: (.*)", content).group(1).strip()
    personagem.origem = re.search(r"Origem/Mundo Natal: (.*)", content).group(1).strip()
    personagem.ambicao = re.search(r"Ambição: (.*)", content).group(1).strip()
    personagem.ancora_moral = re.search(r"Âncora Moral: (.*)", content).group(1).strip()
    personagem.gatilho_colapso = re.search(r"Gatilho de Colapso: (.*)", content).group(1).strip()

    # II. ATRIBUTOS
    atributos_matches = re.findall(r"\[(\d)\] (.*?):", content)
    for valor, nome in atributos_matches:
        nome_limpo = nome.strip().upper()
        if nome_limpo in personagem.atributos:
            personagem.atributos[nome_limpo] = int(valor)
    
    # III. PERÍCIAS
    pericias_matches = re.findall(r"\[(\d)\] (.*?)\s\(", content)
    for valor, nome in pericias_matches:
        nome_limpo = nome.strip()
        if nome_limpo in personagem.pericias:
            personagem.pericias[nome_limpo] = int(valor)

    # IV. MOTOR DE RISCO E CONDIÇÃO
    hp_match = re.search(r"HP: \[(\d)\]", content)
    if hp_match:
        # HP é calculado, mas podemos querer armazenar o atual no futuro
        pass
    mp_match = re.search(r"MP: \[(\d)\]", content)
    if mp_match:
        personagem.mp = int(mp_match.group(1))

    exaustao_match = re.search(r"EXAUSTÃO: \[(\d)\]", content)
    if exaustao_match:
        personagem.exaustao = int(exaustao_match.group(1))

    # V. PODERES
    poderes_section = re.search(r"🔮 V\. PODERES \((.*?)\)(.*?)💠 VI\.", content, re.DOTALL)
    if poderes_section:
        poderes_content = poderes_section.group(2)
        # Regex para encontrar múltiplos poderes
        poderes_matches = re.finditer(r"\[(.*?)\] — Rank: \[(.*?)\]\s*Efeito Narrativo e Mecânico: (.*?)\s*Exigencia: (.*?)(?=\n\[|$)", poderes_content, re.DOTALL)
        for match in poderes_matches:
            nome = match.group(1).strip()
            rank = match.group(2).strip()
            efeito = match.group(3).strip()
            exigencia = match.group(4).strip()
            if nome: # Garante que não adicionemos uma entrada vazia
                personagem.adicionar_poder(nome, rank, efeito, exigencia)


    # VI. EVOLUÇÃO
    xp_match = re.search(r"XP: (\d+) XP", content)
    if xp_match:
        personagem.xp = int(xp_match.group(1))

    return personagem
