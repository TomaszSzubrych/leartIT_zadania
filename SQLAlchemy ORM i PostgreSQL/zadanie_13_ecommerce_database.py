import random
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# ============================================================
# KONFIGURACJA
# ============================================================

random.seed(42)

DATABASE_URL = "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/e_commerce.db"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ============================================================
# RELACJA MANY-TO-MANY: PRODUCTS <-> CATEGORIES
# ============================================================

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


# ============================================================
# MODELE
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price > 0", name="check_product_price_positive"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    categories = relationship(
        "Category",
        secondary=product_categories,
        back_populates="products",
    )

    order_items = relationship("OrderItem", back_populates="product")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    products = relationship(
        "Product",
        secondary=product_categories,
        back_populates="categories",
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="orders")

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_order_item_quantity_positive"),
    )

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


# ============================================================
# TWORZENIE SCHEMATU
# ============================================================

Base.metadata.create_all(engine)


# ============================================================
# DANE TESTOWE
# ============================================================

category_names = [
    "Wędki",
    "Kołowrotki",
    "Przynęty",
    "Akcesoria",
    "Odzież",
]

product_names = [
    "Wędka spinningowa 210",
    "Wędka spinningowa 240",
    "Wędka castingowa 198",
    "Kołowrotek 2000",
    "Kołowrotek 2500",
    "Kołowrotek 3000",
    "Przynęta gumowa 5 cm",
    "Przynęta gumowa 7 cm",
    "Wobler 6 cm",
    "Wobler 9 cm",
    "Błystka obrotowa 2",
    "Błystka wahadłowa 3",
    "Plecionka 0.08 mm",
    "Plecionka 0.10 mm",
    "Przypon stalowy",
    "Pudełko wędkarskie",
    "Podbierak składany",
    "Czapka wędkarska",
    "Bluza wędkarska",
    "Kamizelka wędkarska",
]

prices = [
    249.99, 289.99, 399.99, 199.99, 229.99,
    279.99, 12.99, 16.99, 24.99, 34.99,
    14.99, 19.99, 39.99, 49.99, 9.99,
    59.99, 89.99, 49.99, 159.99, 199.99,
]

# Każdy produkt otrzymuje co najmniej jedną kategorię.
product_category_map = {
    0: [0], 1: [0], 2: [0],
    3: [1], 4: [1], 5: [1],
    6: [2], 7: [2], 8: [2], 9: [2],
    10: [2], 11: [2],
    12: [3], 13: [3], 14: [3], 15: [3], 16: [3],
    17: [4], 18: [4], 19: [4],
}

session = Session()

try:
    # Usuwamy wyłącznie dane z tabel tego zadania.
    session.query(OrderItem).delete()
    session.query(Order).delete()
    session.execute(product_categories.delete())
    session.query(Product).delete()
    session.query(Category).delete()
    session.query(User).delete()
    session.commit()

    categories = [
        Category(name=name)
        for name in category_names
    ]

    users = [
        User(
            name=f"Użytkownik {i:02d}",
            email=f"user{i:02d}@example.com",
        )
        for i in range(1, 11)
    ]

    products = []

    for i, name in enumerate(product_names):
        product = Product(
            name=name,
            price=Decimal(str(prices[i])),
        )
        product.categories = [
            categories[category_id]
            for category_id in product_category_map[i]
        ]
        products.append(product)

    session.add_all(categories + users + products)
    session.flush()

    # 30 zamówień. Każde zawiera od 1 do 4 pozycji.
    orders = []

    for _ in range(30):
        order = Order(user=random.choice(users))

        for product in random.sample(products, k=random.randint(1, 4)):
            order.order_items.append(
                OrderItem(
                    product=product,
                    quantity=random.randint(1, 3),
                )
            )

        orders.append(order)

    session.add_all(orders)
    session.commit()

    # ========================================================
    # RAPORT TOP 5 NAJLEPIEJ SPRZEDAJĄCYCH SIĘ PRODUKTÓW
    # ========================================================

    top_products = session.execute(
        select(
            Product.name,
            func.sum(OrderItem.quantity).label("sold_quantity"),
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .order_by(func.sum(OrderItem.quantity).desc(), Product.name.asc())
        .limit(5)
    ).all()

    # ========================================================
    # WALIDACJA
    # ========================================================

    counts = {
        "users": session.query(User).count(),
        "products": session.query(Product).count(),
        "categories": session.query(Category).count(),
        "orders": session.query(Order).count(),
        "order_items": session.query(OrderItem).count(),
    }

    assert counts["users"] == 10
    assert counts["products"] == 20
    assert counts["categories"] == 5
    assert counts["orders"] == 30
    assert counts["order_items"] > 0

    assert session.query(Product).filter(Product.price <= 0).count() == 0

    assert (
        session.query(User.email)
        .group_by(User.email)
        .having(func.count(User.id) > 1)
        .count()
        == 0
    )

    assert all(
        len(product.categories) >= 1
        for product in session.query(Product).all()
    )

    assert all(
        len(order.order_items) >= 1
        for order in session.query(Order).all()
    )

    print("=== LICZBA REKORDÓW ===")
    for table_name, count in counts.items():
        print(f"{table_name}: {count}")

    print("\n=== TOP 5 NAJLEPIEJ SPRZEDAJĄCYCH SIĘ PRODUKTÓW ===")
    for position, (name, quantity) in enumerate(top_products, start=1):
        print(f"{position}. {name}: {quantity} szt.")

    print("\n=== WALIDACJA ===")
    print("Ceny wszystkich produktów są większe od zera.")
    print("Adresy email są unikalne.")
    print("Każdy produkt ma przypisaną kategorię.")
    print("Każde zamówienie zawiera co najmniej jedną pozycję.")
    print("\nZadanie 13 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
