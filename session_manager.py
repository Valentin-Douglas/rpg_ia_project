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

    def iniciar_ou_retomar(self, personagem_id: int) -> dict:
        self.character_id = personagem_id
        last_session = self.db.get_last_session(personagem_id)
        if last_session:
            self.session_id = last_session["id"]
            self.current_interaction_id = last_session.get("interaction_id")
            resumo = last_session.get("resumo_narrativo") or "Sessão retomada."
        else:
            self.session_id = self.db.create_session(personagem_id, resumo="Nova sessão iniciada.")
            resumo = "Nova sessão iniciada."
        return {"session_id": self.session_id, "resumo": resumo}

    def registrar_turno(self, user_input: str, turno: dict) -> None:
        if not self.session_id:
            return
        self.db.append_event(self.session_id, "IC", turno["narrativa_ic"])
        self.db.append_event(self.session_id, "OOC", turno["comando_ooc"])
        self.db.update_character(self.character_id, fadiga=turno.get("fadiga", 0))