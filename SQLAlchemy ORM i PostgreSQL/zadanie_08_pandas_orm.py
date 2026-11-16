from pathlib import Path

import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    # 1. Utworzenie DataFrame z 10 produktami
    df = pd.DataFrame([
        {"name": "Laptop", "category": "Electronics", "price": 3500.00},
        {"name": "Smartphone", "category": "Electronics", "price": 2200.00},
        {"name": "Mouse", "category": "Electronics", "price": 75.00},
        {"name": "Keyboard", "category": "Electronics", "price": 150.00},
        {"name": "Monitor", "category": "Electronics", "price": 1100.00},
        {"name": "Desk", "category": "Furniture", "price": 800.00},
        {"name": "Chair", "category": "Furniture", "price": 450.00},
        {"name": "Bookshelf", "category": "Furniture", "price": 600.00},
        {"name": "Python Basics", "category": "Books", "price": 89.90},
        {"name": "Data Science Guide", "category": "Books", "price": 119.90}
    ])

    print("DATAFRAME:")
    print(df.to_string(index=False))
    print(f"\nLiczba produktów w DataFrame: {len(df)}")

    # 2. Konwersja DataFrame na obiekty ORM
    product_objects = [
        Product(**row)
        for row in df.to_dict(orient="records")
    ]

    # 3. Zapis produktów do bazy przez session.add_all()
    # Czyścimy wyłącznie tabelę products, aby ponowne uruchomienie
    # skryptu nie powodowało duplikowania rekordów.
    session.query(Product).delete(synchronize_session=False)

    session.add_all(product_objects)
    session.commit()

    print(f"\nZapisano produktów do bazy: {len(product_objects)}")

    # 4. Odczyt produktów z bazy danych
    products_from_db = session.query(Product).order_by(
        Product.id
    ).all()

    print("\nPRODUKTY ODCZYTANE Z BAZY:")

    for product in products_from_db:
        print(
            f"{product.name} | "
            f"{product.category} | "
            f"{product.price:.2f}"
        )

    # 5. Porównanie DataFrame z danymi z bazy
    dataframe_records = sorted(
        (
            row["name"],
            row["category"],
            round(float(row["price"]), 2)
        )
        for row in df.to_dict(orient="records")
    )

    database_records = sorted(
        (
            product.name,
            product.category,
            round(float(product.price), 2)
        )
        for product in products_from_db
    )

    print("\nPORÓWNANIE DANYCH:")

    if dataframe_records == database_records:
        print("SUKCES: dane w DataFrame i bazie danych są identyczne.")
    else:
        print("BLAD: dane w DataFrame i bazie danych różnią się.")

    print(f"Liczba rekordów w DataFrame: {len(dataframe_records)}")
    print(f"Liczba rekordów w bazie: {len(database_records)}")

    if dataframe_records != database_records:
        raise AssertionError("Porównanie danych zakończone niepowodzeniem.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
