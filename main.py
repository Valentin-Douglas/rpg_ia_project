from __future__ import annotations

import os
from typing import Optional

import db_manager
import dice_system
import game_master
import session_manager


def iniciar_jogo() -> None:
    print("--- Bem-vindo às Crônicas de Aethelgard ---")
    db = db_manager.DBManager()
    gm = game_master.GameMaster(client=None)
    sm = session_manager.SessionManager(db, gm)

    personagem_id = None
    while personagem_id is None:
        nome = input("Digite o nome do personagem (ou deixe em branco para criar um padrão): ").strip()
        if not nome:
            nome = "Aelion"
        personagem_id = db.create_character(nome=nome, atributos={"forca": 3, "agilidade": 3, "vontade": 3}, fadiga=0, xp=0)
        break

    sm.iniciar_ou_retomar(personagem_id)
    print(f"Personagem carregado: {db.get_character(personagem_id)['nome']}")

    inter_id: Optional[str] = None
    while True:
        try:
            user_in = input("\n[Sua Ação] (digite 'sair' para encerrar): ")
            if user_in.lower() in {"sair", "exit"}:
                break

            turno, inter_id = gm.interagir(user_in, inter_id, character_context=db.get_character(personagem_id))
            print(f"\n📜 {turno.narrativa_ic}")
            print(f"\n⚙️ OOC: {turno.comando_ooc}")

            if turno.teste_sugerido:
                res = dice_system.rolar_pool_aethelgard(6, 1)
                print(f"🎲 Resultado do Teste: {res['sucessos']} sucessos. ({res['detalhes']})")

            sm.registrar_turno(user_in, {"narrativa_ic": turno.narrativa_ic, "comando_ooc": turno.comando_ooc, "fadiga": 0})
        except KeyboardInterrupt:
            print("\nSessão encerrada.")
            break
        except Exception as exc:
            print(f"Erro no loop: {exc}")


if __name__ == "__main__":
    iniciar_jogo()