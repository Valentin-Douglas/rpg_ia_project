import os

import db_manager
import dice_system
import game_master


def build_client():
    try:
        from google import genai
    except Exception as exc:
        print(f"SDK google-genai não disponível; usando modo local: {exc}")
        return None

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Variável GOOGLE_API_KEY não definida; usando modo local.")
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception as exc:
        print(f"Não foi possível iniciar o cliente Gemini: {exc}; usando modo local.")
        return None


def main():
    client = build_client()
    db = db_manager.DBManager()
    gm = game_master.GameMaster(client)
    inter_id = None

    print("--- Bem-vindo às Crônicas de Aethelgard ---")
    while True:
        try:
            user_in = input("\n[Sua Ação]: ")
            if user_in.lower() in ["sair", "exit"]:
                break

            turno, inter_id = gm.interagir(user_in, inter_id)

            print(f"\n📜 {turno.narrativa_ic}")
            print(f"\n⚙️ OOC: {turno.comando_ooc}")

            if turno.teste_sugerido:
                res = dice_system.rolar_pool_aethelgard(6, 1)
                print(f"🎲 Resultado do Teste: {res['sucessos']} sucessos. ({res['detalhes']})")

        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as exc:
            print(f"Erro no loop: {exc}")


if __name__ == "__main__":
    main()