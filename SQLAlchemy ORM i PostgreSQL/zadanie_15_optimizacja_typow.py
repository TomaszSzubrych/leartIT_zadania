import sys
import uuid
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Numeric,
    LargeBinary,
    Enum,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# KONFIGURACJA
# ============================================================

DATABASE_URL = (
    "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/transactions_optimized.db"
)

RECORD_COUNT = 1_000_000

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ============================================================
# ANALIZA ROZMIARÓW PYTHON (sizeof)
# ============================================================

sample_uuid = str(uuid.uuid4())
sample_uuid_binary = uuid.UUID(sample_uuid).bytes

sample_amount_float = 9999.99
sample_amount_decimal = Decimal("9999.99")

sample_status = "completed"

print("=== ANALIZA sizeof() — OBIEKTY PYTHON ===")

sizes = {
    "UUID jako String(36)": sys.getsizeof(sample_uuid),
    "UUID jako bytes (16)": sys.getsizeof(sample_uuid_binary),
    "Float": sys.getsizeof(sample_amount_float),
    "Decimal": sys.getsizeof(sample_amount_decimal),
    "Status jako String": sys.getsizeof(sample_status),
}

for name, size in sizes.items():
    print(f"{name}: {size} B")

print(
    "\nUwaga: sys.getsizeof() mierzy obiekty Pythona, "
    "a nie rzeczywisty rozmiar kolumn w bazie danych."
)


# ============================================================
# UPROSZCZONA KALKULACJA ROZMIARU DANYCH
# ============================================================

# Szacunek dla PostgreSQL:
# UUID zapisany jako tekst: 36 B
# Float (double precision): 8 B
# VARCHAR(20): maksymalnie 20 B danych
#
# Proponowane:
# UUID binary: 16 B
# NUMERIC(7,2): przyjęto szacunkowo 7 B
# ENUM PostgreSQL: 4 B
#
# To model porównawczy payloadu kolumn, bez narzutu wierszy,
# nagłówków, wyrównania, indeksów i TOAST.

original_sizes = {
    "UUID String(36)": 36,
    "Float": 8,
    "Status String(20)": 20,
}

optimized_sizes = {
    "UUID binary": 16,
    "Numeric(7,2)": 7,
    "Enum": 4,
}

original_per_record = sum(original_sizes.values())
optimized_per_record = sum(optimized_sizes.values())

original_total = original_per_record * RECORD_COUNT
optimized_total = optimized_per_record * RECORD_COUNT

saved_bytes = original_total - optimized_total
saved_mb = saved_bytes / (1024 * 1024)
saving_percent = saved_bytes / original_total * 100

print("\n=== SZACUNEK ROZMIARU DANYCH DLA 1 MLN REKORDÓW ===")

print("\nModel pierwotny:")
for name, size in original_sizes.items():
    print(f"{name}: {size} B")

print(f"Razem na rekord: {original_per_record} B")
print(f"Razem: {original_total / (1024 * 1024):.2f} MB")

print("\nModel zoptymalizowany:")
for name, size in optimized_sizes.items():
    print(f"{name}: {size} B")

print(f"Razem na rekord: {optimized_per_record} B")
print(f"Razem: {optimized_total / (1024 * 1024):.2f} MB")

print("\n=== OSZCZĘDNOŚCI ===")
print(f"Oszczędność na rekord: {original_per_record - optimized_per_record} B")
print(f"Oszczędność łącznie: {saved_mb:.2f} MB")
print(f"Procentowa oszczędność: {saving_percent:.2f}%")


# ============================================================
# ZOPTYMALIZOWANY MODEL
# ============================================================

class TransactionStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(LargeBinary(16), primary_key=True)
    amount = Column(Numeric(7, 2), nullable=False)
    status = Column(
        Enum(
            TransactionStatus,
            native_enum=False,
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
    )


Base.metadata.create_all(engine)


# ============================================================
# TEST ZAPISU I ODCZYTU
# ============================================================

session = Session()

try:
    session.query(Transaction).delete()
    session.commit()

    test_transactions = [
        Transaction(
            id=uuid.uuid4().bytes,
            amount=Decimal("125.50"),
            status=TransactionStatus.PENDING,
        ),
        Transaction(
            id=uuid.uuid4().bytes,
            amount=Decimal("9999.99"),
            status=TransactionStatus.COMPLETED,
        ),
        Transaction(
            id=uuid.uuid4().bytes,
            amount=Decimal("10.00"),
            status=TransactionStatus.FAILED,
        ),
    ]

    session.add_all(test_transactions)
    session.commit()

    print("\n=== TEST ZOPTYMALIZOWANEGO MODELU ===")

    records = session.query(Transaction).all()

    for transaction in records:
        print(
            f"UUID: {uuid.UUID(bytes=transaction.id)} | "
            f"Amount: {transaction.amount} | "
            f"Status: {transaction.status.value}"
        )

    # ========================================================
    # WALIDACJA
    # ========================================================

    assert len(records) == 3

    for transaction in records:
        assert isinstance(transaction.id, bytes)
        assert len(transaction.id) == 16
        assert isinstance(transaction.amount, Decimal)
        assert transaction.amount >= Decimal("0")
        assert transaction.amount <= Decimal("10000")
        assert isinstance(transaction.status, TransactionStatus)

    assert original_per_record == 64
    assert optimized_per_record == 27
    assert saved_bytes > 0

    print("\n=== WALIDACJA ===")
    print("UUID przechowywany jako 16 bajtów.")
    print("Kwota odczytywana jako Decimal.")
    print("Status odczytywany jako Enum.")
    print("3 przykładowe rekordy zapisane i odczytane poprawnie.")
    print("Kalkulacja dla 1 mln rekordów wykonana.")
    print("\nZadanie 15 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
