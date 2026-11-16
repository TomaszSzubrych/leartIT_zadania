from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    event,
    select,
)
from sqlalchemy.orm import (
    Session as SQLAlchemySession,
    declarative_base,
    sessionmaker,
    with_loader_criteria,
)


# ============================================================
# KONFIGURACJA
# ============================================================

DATABASE_URL = (
    "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/soft_delete.db"
)

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()


# ============================================================
# MIXIN SOFT DELETE
# ============================================================

class SoftDeleteMixin:
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()

    def permanently_delete(self, session):
        session.permanently_delete(self)


# ============================================================
# MODEL
# ============================================================

class Product(Base, SoftDeleteMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


# ============================================================
# WŁASNA KLASA SESSION
# ============================================================

class SoftDeleteSession(SQLAlchemySession):

    def delete(self, instance):
        """
        Zamiast fizycznego usunięcia oznacza rekord
        jako usunięty, jeśli model obsługuje Soft Delete.
        """
        if isinstance(instance, SoftDeleteMixin):
            instance.soft_delete()
        else:
            super().delete(instance)

    def permanently_delete(self, instance):
        """Fizycznie usuwa rekord z bazy danych."""
        super().delete(instance)


SessionLocal = sessionmaker(
    bind=engine,
    class_=SoftDeleteSession,
)


# ============================================================
# DOMYŚLNE FILTROWANIE REKORDÓW
# ============================================================

@event.listens_for(SoftDeleteSession, "do_orm_execute")
def filter_deleted_records(execute_state):
    """
    Automatycznie ukrywa rekordy oznaczone jako usunięte.
    Można je odczytać, ustawiając execution option
    include_deleted=True.
    """
    if (
        execute_state.is_select
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.is_deleted.is_(False),
                include_aliases=True,
            )
        )


Base.metadata.create_all(engine)


# ============================================================
# DEMONSTRACJA
# ============================================================

session = SessionLocal()

try:
    # Przygotowanie czystych danych testowych.
    existing_products = session.scalars(
        select(Product).execution_options(include_deleted=True)
    ).all()

    for product in existing_products:
        session.permanently_delete(product)

    session.commit()

    # Utworzenie produktów.
    products = [
        Product(name="Wędka spinningowa"),
        Product(name="Kołowrotek 2500"),
        Product(name="Przynęta gumowa"),
    ]

    session.add_all(products)
    session.commit()

    print("=== REKORDY PRZED USUNIĘCIEM ===")

    for product in session.scalars(select(Product)).all():
        print(f"ID: {product.id} | {product.name}")

    assert session.query(Product).count() == 3

    # --------------------------------------------------------
    # SOFT DELETE — NADPISANA METODA delete()
    # --------------------------------------------------------

    soft_deleted_product = products[0]
    session.delete(soft_deleted_product)
    session.commit()

    print("\n=== PO SOFT DELETE ===")

    active_products = session.scalars(select(Product)).all()

    for product in active_products:
        print(f"ID: {product.id} | {product.name}")

    print(
        f"Liczba aktywnych produktów: {len(active_products)}"
    )

    # --------------------------------------------------------
    # ODCZYT REKORDÓW USUNIĘTYCH
    # --------------------------------------------------------

    all_products = session.scalars(
        select(Product).execution_options(include_deleted=True)
    ).all()

    deleted_products = [
        product for product in all_products
        if product.is_deleted
    ]

    print("\n=== REKORDY OZNACZONE JAKO USUNIĘTE ===")

    for product in deleted_products:
        print(
            f"ID: {product.id} | "
            f"{product.name} | "
            f"deleted_at: {product.deleted_at}"
        )

    # --------------------------------------------------------
    # PERMANENT DELETE
    # --------------------------------------------------------

    product_to_remove = next(
        product for product in all_products
        if product.name == "Kołowrotek 2500"
    )

    product_to_remove.permanently_delete(session)
    session.commit()

    print("\n=== PO PERMANENT DELETE ===")

    remaining_products = session.scalars(
        select(Product).execution_options(include_deleted=True)
    ).all()

    for product in remaining_products:
        print(
            f"ID: {product.id} | "
            f"{product.name} | "
            f"is_deleted: {product.is_deleted}"
        )

    # ========================================================
    # WALIDACJA
    # ========================================================

    active_count = session.query(Product).count()

    all_count = len(
        session.scalars(
            select(Product).execution_options(include_deleted=True)
        ).all()
    )

    soft_deleted_count = (
        session.query(Product)
        .execution_options(include_deleted=True)
        .filter(Product.is_deleted.is_(True))
        .count()
    )

    assert active_count == 1
    assert all_count == 2
    assert soft_deleted_count == 1

    assert soft_deleted_product.is_deleted is True
    assert soft_deleted_product.deleted_at is not None

    print("\n=== WALIDACJA ===")
    print(f"Aktywne rekordy: {active_count}")
    print(f"Wszystkie rekordy w bazie: {all_count}")
    print(f"Rekordy soft deleted: {soft_deleted_count}")
    print("Domyślne zapytanie ukrywa usunięte rekordy.")
    print("Soft Delete ustawia is_deleted i deleted_at.")
    print("Permanent Delete fizycznie usuwa rekord.")
    print("\nZadanie 18 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
