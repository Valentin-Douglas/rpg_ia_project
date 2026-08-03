from __future__ import annotations

from typing import Optional

from db_manager import DBManager


class SessionManager:
    """Gerencia continuidade da sessão e contexto resumido para o GM."""

    def __init__(self, db: DBManager, gm):
        self.db = db
        self.gm = gm
        self.current_interaction_id: Optional[str] = None
        self.character_id: Optional[int] = None
        self.session_id: Optional[int] = None

    def iniciar_ou_retomar(self, personagem_id: int) -> Optional[str]:
        self.character_id = personagem_id
        last_session = self.db.get_last_session(personagem_id)
        if last_session:
            self.session_id = last_session["id"]
            self.current_interaction_id = last_session.get("interaction_id")
        else:
            self.session_id = self.db.create_session(personagem_id, resumo="Nova sessão iniciada.")
        return self.current_interaction_id

    def salvar_estado(self, resumo: str, interaction_id: Optional[str] = None) -> Optional[str]:
        if self.character_id is None:
            raise ValueError("Nenhum personagem foi inicializado para a sessão.")

        if interaction_id is not None:
            self.current_interaction_id = interaction_id

        self.db.salvar_sessao(
            self.character_id,
            self.current_interaction_id,
            resumo,
        )
        return self.current_interaction_id

    def registrar_turno(self, user_input: str, turno: dict) -> None:
        if not self.session_id:
            return
        self.db.append_event(self.session_id, "IC", turno["narrativa_ic"])
        self.db.append_event(self.session_id, "OOC", turno["comando_ooc"])
        self.db.update_character(self.character_id, fadiga=turno.get("fadiga", 0))
