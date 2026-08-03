from db_manager import DBManager


class SessionManager:
    def __init__(self, db: DBManager, gm):
        self.db = db
        self.gm = gm
        self.current_interaction_id = None
        self.character_id = None

    def iniciar_ou_retomar(self, personagem_id):
        """Resgata o estado do banco para manter a continuidade."""
        self.character_id = personagem_id
        with self.db.get_connection() as conn:
            row = conn.execute(
                "SELECT interaction_id FROM sessoes WHERE personagem_id = ? ORDER BY id DESC LIMIT 1",
                (personagem_id,),
            ).fetchone()
        if row:
            self.current_interaction_id = row[0]
        return self.current_interaction_id

    def salvar_estado(self, resumo, interaction_id=None):
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