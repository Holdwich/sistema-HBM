from core.database import SessionLocal

def get_db():
    """Gera um gerenciador de sessão de banco de dados para cada requisição.

    Yields:
        Session: gerenciador de sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
