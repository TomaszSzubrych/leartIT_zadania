import time
import statistics

import pandas as pd

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# KONFIGURACJA
# ============================================================

DATABASE_URL = (
    "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/bulk_insert.db"
)

RECORD_COUNT = 10_000
REPETITIONS = 3

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ============================================================
# MODEL
# ============================================================

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)


Base.metadata.create_all(engine)


# ============================================================
# DATAFRAME
# ============================================================

categories = [
    "Electronics",
    "Fishing",
    "Clothing",
    "Accessories",
    "Outdoor",
]

data = {
    "name": [f"Product {i:05d}" for i in range(1, RECORD_COUNT + 1)],
    "category": [
        categories[(i - 1) % len(categories)]
        for i in range(1, RECORD_COUNT + 1)
    ],
    "price": [
        round(10.0 + ((i * 17) % 990), 2)
        for i in range(1, RECORD_COUNT + 1)
    ],
}

df = pd.DataFrame(data)


# ============================================================
# METODA 1: session.add() + commit per row
# ============================================================

def insert_add_commit_per_row(dataframe):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    try:
        for row in dataframe.itertuples(index=False):
            product = Product(
                name=row.name,
                category=row.category,
                price=row.price,
            )

            session.add(product)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ============================================================
# METODA 2: session.add_all() + jeden commit
# ============================================================

def insert_add_all(dataframe):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    try:
        products = [
            Product(
                name=row.name,
                category=row.category,
                price=row.price,
            )
            for row in dataframe.itertuples(index=False)
        ]

        session.add_all(products)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ============================================================
# METODA 3: pandas to_sql(method="multi")
# ============================================================

def insert_pandas_to_sql(dataframe):
    Base.metadata.drop_all(engine)

    dataframe.to_sql(
        "products",
        con=engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=500,
    )


# ============================================================
# POMIAR CZASU
# ============================================================

methods = [
    (
        "add() + commit per row",
        insert_add_commit_per_row,
    ),
    (
        "add_all() + 1 commit",
        insert_add_all,
    ),
    (
        "pandas to_sql(method=multi)",
        insert_pandas_to_sql,
    ),
]

results = {}

print("=== POMIARY WYDAJNOŚCI ===")
print(f"Liczba rekordów na próbę: {RECORD_COUNT}")
print(f"Liczba powtórzeń: {REPETITIONS}")

for method_name, method_function in methods:
    times = []

    print(f"\nMetoda: {method_name}")

    for repetition in range(1, REPETITIONS + 1):
        start = time.perf_counter()

        method_function(df)

        elapsed = time.perf_counter() - start
        times.append(elapsed)

        # Kontrola liczby zapisanych rekordów po każdej próbie.
        with engine.connect() as connection:
            count = connection.exec_driver_sql(
                "SELECT COUNT(*) FROM products"
            ).scalar_one()

        assert count == RECORD_COUNT, (
            f"Nieprawidłowa liczba rekordów: {count}"
        )

        print(
            f"Powtórzenie {repetition}: "
            f"{elapsed:.4f} s | rekordów: {count}"
        )

    results[method_name] = statistics.mean(times)


# ============================================================
# PORÓWNANIE
# ============================================================

baseline_name = methods[0][0]
baseline_time = results[baseline_name]

print("\n=== ŚREDNIE CZASY ===")
print(f"{'Metoda':35} | {'Czas (s)':>10} | Wykres")
print("-" * 75)

for method_name, average_time in results.items():
    bar_length = max(
        1,
        round(average_time / max(results.values()) * 30),
    )

    bar = "█" * bar_length

    print(
        f"{method_name:35} | "
        f"{average_time:10.4f} | "
        f"{bar}"
    )


# ============================================================
# SPEEDUP
# ============================================================

speedup_add_all = baseline_time / results[methods[1][0]]
speedup_pandas = baseline_time / results[methods[2][0]]

print("\n=== SPEEDUP WZGLĘDEM METODY 1 ===")
print(f"add_all(): {speedup_add_all:.2f}x")
print(f"pandas to_sql(): {speedup_pandas:.2f}x")


# ============================================================
# WNIOSEK
# ============================================================

fastest_name = min(results, key=results.get)
fastest_time = results[fastest_name]

print("\n=== WNIOSEK ===")
print(f"Najszybsza metoda: {fastest_name}")
print(f"Średni czas: {fastest_time:.4f} s")

print(
    "\nMetoda add() z commit po każdym rekordzie wykonuje "
    "wiele osobnych transakcji. Każdy commit generuje dodatkowy "
    "narzut operacyjny."
)

print(
    "add_all() ogranicza liczbę transakcji do jednej, a pandas "
    "to_sql(method='multi') wysyła wiele rekordów w grupach. "
    "Batching ogranicza narzut komunikacji i operacji bazodanowych."
)


# ============================================================
# KOŃCOWA WALIDACJA
# ============================================================

with engine.connect() as connection:
    final_count = connection.exec_driver_sql(
        "SELECT COUNT(*) FROM products"
    ).scalar_one()

assert final_count == RECORD_COUNT
assert len(results) == 3
assert all(value > 0 for value in results.values())

print("\n=== WALIDACJA ===")
print(f"Końcowa liczba rekordów: {final_count}")
print(f"Metody porównane: {len(results)}")
print(f"Powtórzenia każdej metody: {REPETITIONS}")
print("Wszystkie pomiary zakończone poprawnie.")
print("\nZadanie 17 wykonane poprawnie.")

engine.dispose()
