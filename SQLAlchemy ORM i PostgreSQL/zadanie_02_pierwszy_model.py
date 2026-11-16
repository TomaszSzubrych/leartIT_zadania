from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    inspect
)
from sqlalchemy.orm import declarative_base


# Konfiguracja bazy danych
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)

Base = declarative_base()


# Model Student
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    email = Column(String(150), unique=True)


# Tworzenie tabel
Base.metadata.create_all(engine)


# Sprawdzenie struktury tabeli
inspector = inspect(engine)

print("Tabele w bazie:", inspector.get_table_names())

columns = inspector.get_columns("students")

print("\nStruktura tabeli students:")

for column in columns:
    print(
        f"Kolumna: {column['name']}, "
        f"Typ: {column['type']}, "
        f"Nullable: {column['nullable']}"
    )

print("\nModel Student utworzony poprawnie!")

engine.dispose()
