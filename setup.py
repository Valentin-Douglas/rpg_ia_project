import db_manager


def inicializar_banco(db_path: str = "aethelgard.db") -> db_manager.DBManager:
    return db_manager.DBManager(db_path=db_path)


if __name__ == "__main__":
    inicializar_banco()
    print("Banco inicializado com sucesso.")
