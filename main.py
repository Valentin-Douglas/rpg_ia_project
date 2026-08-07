# Bem-vindo ao motor de RPG MCP (Modular Core Progression)
# Este arquivo serve como um guia para o Gemini Notebook interagir com o sistema.

# Para começar, importe as classes e funções necessárias:
from entities import Personagem, carregar_personagem_de_arquivo
from narrator_engine import NarratorEngine
from dice_logic import rolar_dados

def main():
    # =================================================================================
    # COMO CARREGAR UM PERSONAGEM
    # =================================================================================
    # Use a função `carregar_personagem_de_arquivo` para criar uma instância de Personagem
    # a partir de um arquivo de ficha, como o `ficha_teste.md`.

    # personagem_principal = carregar_personagem_de_arquivo("ficha_teste.md")

    # # Para visualizar a ficha carregada:
    # print(personagem_principal)


    # =================================================================================
    # COMO CRIAR UM OPONENTE BÁSICO
    # =================================================================================
    # Você pode criar um oponente simples instanciando a classe Personagem e 
    # ajustando seus atributos e perícias.

    # oponente = Personagem()
    # oponente.nome = "Goblin Batedor"
    # oponente.atributos["FORÇA"] = 2
    # oponente.atributos["AGILIDADE"] = 3
    # oponente.atributos["VITALIDADE"] = 2
    # oponente.pericias["Combate corpo-a-corpo"] = 2


    # =================================================================================
    # COMO USAR O NARRATOR ENGINE
    # =================================================================================
    # O NarratorEngine é o responsável por gerenciar as ações do personagem.
    # Instancie o engine com o personagem que realizará as ações.

    # motor_narrativo = NarratorEngine(personagem_principal)


    # =================================================================================
    # COMO REALIZAR UM TESTE DE PERÍCIA
    # =================================================================================
    # Use o método `realizar_teste` do motor_narrativo.
    # Ele recebe o atributo, a perícia e a dificuldade como argumentos.
    # Exemplo: Teste de Agilidade + Furtividade, dificuldade 3

    # print("\\n--- Exemplo de Teste de Perícia ---")
    # motor_narrativo.realizar_teste("AGILIDADE", "Furtividade", 3)
    

    # =================================================================================
    # COMO REALIZAR UM COMBATE
    # =================================================================================
    # Use o método `combate` do motor_narrativo.
    # Ele simula uma rodada de ataque vs. defesa.

    # print("\\n--- Exemplo de Combate ---")
    # motor_narrativo.combate(oponente, "FORÇA", "Combate corpo-a-corpo", "AGILIDADE", "Combate corpo-a-corpo")


    # =================================================================================
    # COMO ADICIONAR E SOLTAR UM PODER
    # =================================================================================
    # Primeiro, adicione um poder ao personagem usando o método `adicionar_poder`.
    
    # personagem_principal.adicionar_poder(
    #     nome="Bola de Fogo",
    #     rank="F",
    #     efeito="Lança uma pequena bola de fogo que causa dano em área.",
    #     exigencia="Custa 4 de MP"
    # )
    # print("\\n--- Personagem com novo poder ---")
    # print(personagem_principal)

    # Para usar o poder, chame `soltar_poder`.
    # O Mestre (você, no Notebook) decide qual Atributo e Perícia são mais
    # apropriados para o teste, com base no efeito do poder e na situação.
    # Por exemplo, uma "Bola de Fogo" pode exigir FOCO + OCULTISMO.

    # print("\\n--- Exemplo de Soltar um Poder ---")
    # motor_narrativo.soltar_poder(
    #     nome_poder="Bola de Fogo", 
    #     atributo="FOCO", 
    #     pericia="Ocultismo", 
    #     dificuldade=2
    # )


    # =================================================================================
    # COMO USAR A LÓGICA DE DADOS DIRETAMENTE
    # =================================================================================
    # Você também pode usar a função `rolar_dados` diretamente se precisar.
    # Exemplo: rolar 5 dados com 1 nível de exaustão.
    
    # print("\\n--- Exemplo de Rolagem de Dados Direta ---")
    # rolar_dados(5, 1)

    pass # Deixe o "pass" aqui para manter o arquivo executável.

if __name__ == "__main__":
    main()
