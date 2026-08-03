import os
import sqlite3
import tempfile
import unittest


def make_temp_db_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    return path

from db_manager import DBManager
from dice_system import rolar_pool_aethelgard
from game_master import GameMaster, GMOutput
from session_manager import SessionManager


class CoreProjectTests(unittest.TestCase):
    def _list_tables(self, conn):
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        return [tuple(row) if isinstance(row, sqlite3.Row) else tuple(row) for row in rows]

    def test_db_manager_creates_tables(self):
        db_path = make_temp_db_path()
        try:
            db = DBManager(db_path=db_path)
            conn = db.get_connection()
            try:
                tables = self._list_tables(conn)
            finally:
                conn.close()
            self.assertIn(("personagens",), tables)
            self.assertIn(("sessoes",), tables)
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)

    def test_dice_system_returns_expected_structure(self):
        result = rolar_pool_aethelgard(6, 1)
        self.assertIn("sucessos", result)
        self.assertIn("detalhes", result)
        self.assertIn("falha_bestial", result)
        self.assertIsInstance(result["sucessos"], int)

    def test_game_master_fallback_response(self):
        gm = GameMaster(None)
        turno, interaction_id = gm.interagir("investigo a torre")
        self.assertIsInstance(turno, GMOutput)
        self.assertTrue(turno.narrativa_ic)
        self.assertTrue(turno.comando_ooc)
        self.assertIsNotNone(interaction_id)

    def test_session_manager_persists_interaction_id(self):
        db_path = make_temp_db_path()
        try:
            db = DBManager(db_path=db_path)
            gm = GameMaster(None)
            session = SessionManager(db, gm)
            session.iniciar_ou_retomar(1)
            session.salvar_estado("Resumo", "interaction-123")
            self.assertEqual(session.current_interaction_id, "interaction-123")
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)


if __name__ == "__main__":
    unittest.main()
