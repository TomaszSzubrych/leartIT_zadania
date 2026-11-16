
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


# Ścieżka do lokalnej bazy danych
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

# Utworzenie silnika SQLAlchemy
engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)


def check_connection():
    """Sprawdza połączenie z bazą danych."""

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar_one()

            print("Połączenie z bazą danych udane!")
            print(f"Wynik testowego zapytania: {value}")
            print(f"SQLAlchemy version: {__import__('sqlalchemy').__version__}")
            print(f"SQLite database: {DATABASE_PATH}")

    except SQLAlchemyError as error:
        print(f"Błąd połączenia: {error}")
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    check_connection()
