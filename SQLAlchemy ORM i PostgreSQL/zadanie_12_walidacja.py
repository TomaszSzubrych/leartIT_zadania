from sqlalchemy import create_engine, inspect
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext

DATABASE_URL = "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/test.db"

engine = create_engine(DATABASE_URL)

inspector = inspect(engine)
columns = inspector.get_columns("articles")

print("=== KOLUMNY TABELI ARTICLES ===")
for column in columns:
    print(
        f"{column['name']}: "
        f"{column['type']}, "
        f"nullable={column['nullable']}"
    )

with engine.connect() as connection:
    migration_context = MigrationContext.configure(connection)
    current_revision = migration_context.get_current_revision()

print("\n=== WERSJA MIGRACJI ===")
print(current_revision)

required_columns = {"id", "title", "content", "published_date"}
actual_columns = {column["name"] for column in columns}

assert required_columns.issubset(actual_columns), "Brakuje wymaganych kolumn!"
assert current_revision is not None, "Brak zastosowanej migracji!"

print("\nWalidacja struktury tabeli zakończona poprawnie.")
