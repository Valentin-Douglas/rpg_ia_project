import sqlite3


class DBManager:
    def __init__(self, db_path="aethelgard.db"):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def close(self):
        return None

    def _init_db(self):
        """Cria o schema relacional para persistência estável."""
        with self.get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS personagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    fadiga INTEGER DEFAULT 0,
                    atributos TEXT,
                    xp INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS sessoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    personagem_id INTEGER,
                    interaction_id TEXT,
                    resumo_narrativo TEXT,
                    FOREIGN KEY(personagem_id) REFERENCES personagens(id)
                );
                """
            )

    def salvar_sessao(self, personagem_id, interaction_id, resumo_narrativo):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO sessoes (personagem_id, interaction_id, resumo_narrativo) VALUES (?, ?, ?)",
                (personagem_id, interaction_id, resumo_narrativo),
            )
            conn.commit()
