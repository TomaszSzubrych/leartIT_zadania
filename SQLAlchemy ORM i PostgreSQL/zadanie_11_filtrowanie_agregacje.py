from pathlib import Path
from datetime import datetime, timedelta
import random

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    func
)
from sqlalchemy.orm import declarative_base, sessionmaker


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100), nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    # 1. Przygotowanie danych: 100 zamówień dla 10 klientów
    random.seed(42)

    customers = [
        f"Klient {number:02d}"
        for number in range(1, 11)
    ]

    now = datetime.now()
    start_date = now - timedelta(days=90)

    # Czyścimy wyłącznie tabelę orders.
    session.query(Order).delete(synchronize_session=False)

    orders = []

    for _ in range(100):
        random_seconds = random.randint(
            0,
            int((now - start_date).total_seconds())
        )

        order_date = start_date + timedelta(
            seconds=random_seconds
        )

        orders.append(
            Order(
                customer_name=random.choice(customers),
                total=round(random.uniform(10, 1000), 2),
                created_at=order_date
            )
        )

    session.add_all(orders)
    session.commit()

    print("=== DANE TESTOWE ===")
    print(f"Liczba zamówień: {session.query(Order).count()}")
    print(
        f"Liczba klientów: "
        f"{session.query(Order.customer_name).distinct().count()}"
    )

    # 2. Suma zamówień dla każdego klienta
    print("\n=== SUMA ZAMÓWIEŃ DLA KAŻDEGO KLIENTA ===")

    customer_totals = session.query(
        Order.customer_name,
        func.sum(Order.total).label("total_sum")
    ).group_by(
        Order.customer_name
    ).order_by(
        func.sum(Order.total).desc()
    ).all()

    for customer_name, total_sum in customer_totals:
        print(f"{customer_name}: {total_sum:.2f} zł")

    # 3. Średnia wartość zamówienia
    average_order = session.query(
        func.avg(Order.total)
    ).scalar()

    print("\n=== ŚREDNIA WARTOŚĆ ZAMÓWIENIA ===")
    print(f"{average_order:.2f} zł")

    # 4. Klient z największą sumą zamówień
    top_customer = session.query(
        Order.customer_name,
        func.sum(Order.total).label("total_sum")
    ).group_by(
        Order.customer_name
    ).order_by(
        func.sum(Order.total).desc()
    ).first()

    print("\n=== KLIENT Z NAJWIĘKSZĄ SUMĄ ZAMÓWIEŃ ===")

    if top_customer:
        print(
            f"{top_customer.customer_name}: "
            f"{top_customer.total_sum:.2f} zł"
        )

    # 5. Liczba zamówień w ostatnich 30 dniach
    last_month_start = now - timedelta(days=30)

    orders_last_month = session.query(
        func.count(Order.id)
    ).filter(
        Order.created_at >= last_month_start,
        Order.created_at <= now
    ).scalar()

    print("\n=== ZAMÓWIENIA W OSTATNICH 30 DNIACH ===")
    print(f"Liczba zamówień: {orders_last_month}")

    # 6. Kontrola zakresu danych
    invalid_orders = session.query(Order).filter(
        (Order.total < 10) | (Order.total > 1000)
    ).count()

    print("\n=== WALIDACJA ===")
    print(f"Zamówienia poza zakresem 10-1000 zł: {invalid_orders}")

    if session.query(Order).count() != 100:
        raise AssertionError("Nieprawidłowa liczba zamówień.")

    if len(customer_totals) != 10:
        raise AssertionError("Nieprawidłowa liczba klientów.")

    if invalid_orders != 0:
        raise AssertionError("Znaleziono zamówienia poza zakresem.")

    print("\nZadanie 11 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
