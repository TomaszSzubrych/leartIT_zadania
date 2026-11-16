import json
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    create_engine,
    event,
    inspect,
)
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# KONFIGURACJA
# ============================================================

DATABASE_URL = (
    "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/auditing.db"
)

CURRENT_USER = "admin"

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ============================================================
# MODEL AUDIT LOG
# ============================================================

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(String(100), nullable=False)
    action = Column(String(20), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    user = Column(String(100), nullable=False)


# ============================================================
# MODEL TESTOWY
# ============================================================

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    price = Column(Integer, nullable=False)


Base.metadata.create_all(engine)


# ============================================================
# POMOCNICZE FUNKCJE AUDYTU
# ============================================================

def serialize_values(values):
    return json.dumps(
        values,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )


def get_product_values(target):
    return {
        "id": target.id,
        "name": target.name,
        "price": target.price,
    }


def add_audit_log(
    connection,
    table_name,
    record_id,
    action,
    old_value,
    new_value,
):
    connection.execute(
        AuditLog.__table__.insert().values(
            table_name=table_name,
            record_id=str(record_id),
            action=action,
            old_value=(
                serialize_values(old_value)
                if old_value is not None
                else None
            ),
            new_value=(
                serialize_values(new_value)
                if new_value is not None
                else None
            ),
            timestamp=datetime.now(),
            user=CURRENT_USER,
        )
    )


# ============================================================
# EVENT LISTENER: AFTER INSERT
# ============================================================

@event.listens_for(Product, "after_insert")
def audit_after_insert(mapper, connection, target):
    add_audit_log(
        connection=connection,
        table_name=target.__tablename__,
        record_id=target.id,
        action="INSERT",
        old_value=None,
        new_value=get_product_values(target),
    )


# ============================================================
# EVENT LISTENER: BEFORE UPDATE
# ============================================================

@event.listens_for(Product, "before_update")
def audit_before_update(mapper, connection, target):
    state = inspect(target)

    old_values = {}
    new_values = {}

    for attribute in ("name", "price"):
        history = state.attrs[attribute].history

        if history.has_changes():
            old_values[attribute] = (
                history.deleted[0]
                if history.deleted
                else None
            )

            new_values[attribute] = getattr(target, attribute)

    if old_values or new_values:
        add_audit_log(
            connection=connection,
            table_name=target.__tablename__,
            record_id=target.id,
            action="UPDATE",
            old_value=old_values,
            new_value=new_values,
        )


# ============================================================
# EVENT LISTENER: AFTER DELETE
# ============================================================

@event.listens_for(Product, "after_delete")
def audit_after_delete(mapper, connection, target):
    add_audit_log(
        connection=connection,
        table_name=target.__tablename__,
        record_id=target.id,
        action="DELETE",
        old_value=get_product_values(target),
        new_value=None,
    )


# ============================================================
# TEST SYSTEMU AUDYTU
# ============================================================

session = Session()

try:
    # Czyścimy wyłącznie dane testowe tego zadania.
    session.query(AuditLog).delete()
    session.query(Product).delete()
    session.commit()

    print("=== 1. INSERT ===")

    product = Product(
        name="Wędka spinningowa",
        price=250,
    )

    session.add(product)
    session.commit()

    product_id = product.id

    print(f"Utworzono produkt ID: {product_id}")

    print("\n=== 2. UPDATE ===")

    product.name = "Wędka spinningowa PRO"
    product.price = 350

    session.commit()

    print("Zaktualizowano nazwę i cenę produktu.")

    print("\n=== 3. DELETE ===")

    session.delete(product)
    session.commit()

    print(f"Usunięto produkt ID: {product_id}")

    # ========================================================
    # ODCZYT HISTORII
    # ========================================================

    logs = (
        session.query(AuditLog)
        .order_by(AuditLog.id)
        .all()
    )

    print("\n=== HISTORIA ZMIAN AUDIT_LOG ===")

    for log in logs:
        print(f"\nID logu: {log.id}")
        print(f"Tabela: {log.table_name}")
        print(f"Rekord: {log.record_id}")
        print(f"Akcja: {log.action}")
        print(f"Użytkownik: {log.user}")
        print(f"Timestamp: {log.timestamp}")
        print(f"OLD: {log.old_value}")
        print(f"NEW: {log.new_value}")

    # ========================================================
    # WALIDACJA
    # ========================================================

    actions = [log.action for log in logs]

    assert len(logs) == 3
    assert actions == ["INSERT", "UPDATE", "DELETE"]

    insert_log = logs[0]
    update_log = logs[1]
    delete_log = logs[2]

    insert_new = json.loads(insert_log.new_value)
    update_old = json.loads(update_log.old_value)
    update_new = json.loads(update_log.new_value)
    delete_old = json.loads(delete_log.old_value)

    assert insert_new["name"] == "Wędka spinningowa"
    assert insert_new["price"] == 250

    assert update_old["name"] == "Wędka spinningowa"
    assert update_old["price"] == 250

    assert update_new["name"] == "Wędka spinningowa PRO"
    assert update_new["price"] == 350

    assert delete_old["name"] == "Wędka spinningowa PRO"
    assert delete_old["price"] == 350

    assert all(log.user == CURRENT_USER for log in logs)

    product_exists = (
        session.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    assert product_exists is None

    print("\n=== WALIDACJA ===")
    print(f"Liczba wpisów audytu: {len(logs)}")
    print(f"Zarejestrowane akcje: {', '.join(actions)}")
    print("INSERT zapisuje nowe wartości.")
    print("UPDATE zapisuje stare i nowe wartości.")
    print("DELETE zapisuje wartości usuniętego rekordu.")
    print("Historia pozwala odtworzyć stan przed aktualizacją.")
    print("\nZadanie 19 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
