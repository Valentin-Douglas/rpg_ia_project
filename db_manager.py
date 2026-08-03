import json
import sqlite3
from typing import Any, Dict, Optional


class DBManager:
    """Camada de persistência para o motor de RPG textual de Aethelgard."""

    def __init__(self, db_path: str = "aethelgard.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS personagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    fadiga INTEGER DEFAULT 0,
                    atributos TEXT,
                    xp INTEGER DEFAULT 0,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS sessoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    personagem_id INTEGER NOT NULL,
                    interaction_id TEXT,
                    resumo_narrativo TEXT,
                    iniciado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(personagem_id) REFERENCES personagens(id)
                );

                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sessao_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    conteudo TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(sessao_id) REFERENCES sessoes(id)
                );

                CREATE TABLE IF NOT EXISTS estado_mundo (
                    chave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                );
                """
            )
            conn.commit()

    def create_character(self, nome: str, atributos: Optional[Dict[str, Any]] = None, fadiga: int = 0, xp: int = 0) -> int:
        atributos_json = json.dumps(atributos or {}, ensure_ascii=False)
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO personagens (nome, fadiga, atributos, xp) VALUES (?, ?, ?, ?)",
                (nome, fadiga, atributos_json, xp),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def get_character(self, character_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM personagens WHERE id = ?", (character_id,)).fetchone()
            if not row:
                return None
            data = dict(row)
            data["atributos"] = json.loads(data["atributos"] or "{}")
            return data

    def update_character(self, character_id: int, **kwargs) -> None:
        allowed = {"nome", "fadiga", "atributos", "xp"}
        updates = []
        values = []
        for key, value in kwargs.items():
            if key not in allowed:
                continue
            if key == "atributos" and isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False)
            updates.append(f"{key} = ?")
            values.append(value)
        values.append(character_id)
        if not updates:
            return
        with self._connect() as conn:
            conn.execute(f"UPDATE personagens SET {', '.join(updates)} WHERE id = ?", values)
            conn.commit()

    def create_session(self, character_id: int, resumo: Optional[str] = None, interaction_id: Optional[str] = None) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO sessoes (personagem_id, interaction_id, resumo_narrativo) VALUES (?, ?, ?)",
                (character_id, interaction_id, resumo),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def get_last_session(self, character_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM sessoes WHERE personagem_id = ? ORDER BY id DESC LIMIT 1",
                (character_id,),
            ).fetchone()
            return dict(row) if row else None

    def append_event(self, session_id: int, event_type: str, content: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO eventos (sessao_id, tipo, conteudo) VALUES (?, ?, ?)",
                (session_id, event_type, content),
            )
            conn.commit()

    def get_recent_events(self, session_id: int, limit: int = 12) -> list[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM eventos WHERE sessao_id = ? ORDER BY id DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
            return [dict(row) for row in rows]

    def set_world_state(self, key: str, value: Any) -> None:
        payload = json.dumps(value, ensure_ascii=False)
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO estado_mundo (chave, valor) VALUES (?, ?) ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor",
                (key, payload),
            )
            conn.commit()

    def get_world_state(self, key: str, default: Any = None) -> Any:
        with self._connect() as conn:
            row = conn.execute("SELECT valor FROM estado_mundo WHERE chave = ?", (key,)).fetchone()
            if not row:
                return default
            return json.loads(row["valor"])

