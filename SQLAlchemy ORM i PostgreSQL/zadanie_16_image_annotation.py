import random

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    JSON,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# ============================================================
# KONFIGURACJA
# ============================================================

random.seed(42)

DATABASE_URL = (
    "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/image_annotation.db"
)

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ============================================================
# MODELE
# ============================================================

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String(200), nullable=False, unique=True)

    annotations = relationship(
        "Annotation",
        back_populates="image",
        cascade="all, delete-orphan",
    )


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    annotations = relationship(
        "Annotation",
        back_populates="label",
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)

    annotations = relationship(
        "Annotation",
        back_populates="user",
    )


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    bbox = Column(JSON, nullable=False)

    image = relationship("Image", back_populates="annotations")
    label = relationship("Label", back_populates="annotations")
    user = relationship("User", back_populates="annotations")


Base.metadata.create_all(engine)


# ============================================================
# DANE TESTOWE
# ============================================================

label_names = [
    "cat",
    "dog",
    "car",
    "person",
    "bicycle",
    "bird",
    "tree",
    "house",
    "chair",
    "boat",
]

session = Session()

try:
    # Czyścimy wyłącznie dane tego zadania.
    session.query(Annotation).delete()
    session.query(Image).delete()
    session.query(Label).delete()
    session.query(User).delete()
    session.commit()

    images = [
        Image(filename=f"image_{i:03d}.jpg")
        for i in range(1, 101)
    ]

    labels = [
        Label(name=name)
        for name in label_names
    ]

    users = [
        User(username=f"annotator_{i:02d}")
        for i in range(1, 6)
    ]

    session.add_all(images + labels + users)
    session.flush()

    # Dokładnie 500 adnotacji.
    annotations = []

    for _ in range(500):
        bbox = {
            "x": random.randint(0, 1000),
            "y": random.randint(0, 1000),
            "width": random.randint(20, 300),
            "height": random.randint(20, 300),
        }

        annotation = Annotation(
            image=random.choice(images),
            label=random.choice(labels),
            user=random.choice(users),
            bbox=bbox,
        )

        annotations.append(annotation)

    session.add_all(annotations)
    session.commit()

    # ========================================================
    # ZAPYTANIE 1: ILE ANNOTACJI MA OBRAZ X?
    # ========================================================

    target_image = (
        session.query(Image)
        .filter(Image.filename == "image_001.jpg")
        .one()
    )

    image_annotation_count = (
        session.query(func.count(Annotation.id))
        .filter(Annotation.image_id == target_image.id)
        .scalar()
    )

    print("=== LICZBA ADNOTACJI DLA OBRAZU X ===")
    print(f"Obraz: {target_image.filename}")
    print(f"Liczba adnotacji: {image_annotation_count}")

    # ========================================================
    # ZAPYTANIE 2: KTÓRE OBRAZY MAJĄ LABEL CAT?
    # ========================================================

    cat_images = (
        session.query(Image)
        .join(Annotation, Annotation.image_id == Image.id)
        .join(Label, Annotation.label_id == Label.id)
        .filter(Label.name == "cat")
        .distinct()
        .order_by(Image.filename)
        .all()
    )

    print("\n=== OBRAZY Z ETYKIETĄ CAT ===")
    for image in cat_images:
        print(image.filename)

    # ========================================================
    # STATYSTYKI ANOTACJI
    # ========================================================

    label_statistics = (
        session.query(
            Label.name,
            func.count(Annotation.id).label("annotation_count"),
        )
        .outerjoin(Annotation, Annotation.label_id == Label.id)
        .group_by(Label.id, Label.name)
        .order_by(func.count(Annotation.id).desc(), Label.name)
        .all()
    )

    user_statistics = (
        session.query(
            User.username,
            func.count(Annotation.id).label("annotation_count"),
        )
        .outerjoin(Annotation, Annotation.user_id == User.id)
        .group_by(User.id, User.username)
        .order_by(func.count(Annotation.id).desc())
        .all()
    )

    print("\n=== STATYSTYKI WEDŁUG ETYKIET ===")
    for label_name, count in label_statistics:
        print(f"{label_name}: {count}")

    print("\n=== STATYSTYKI WEDŁUG UŻYTKOWNIKÓW ===")
    for username, count in user_statistics:
        print(f"{username}: {count}")

    # ========================================================
    # WALIDACJA
    # ========================================================

    image_count = session.query(Image).count()
    label_count = session.query(Label).count()
    user_count = session.query(User).count()
    annotation_count = session.query(Annotation).count()

    assert image_count == 100
    assert label_count == 10
    assert user_count == 5
    assert annotation_count == 500

    # Kontrola struktury JSON.
    for annotation in session.query(Annotation).all():
        bbox = annotation.bbox

        assert isinstance(bbox, dict)
        assert set(bbox.keys()) == {"x", "y", "width", "height"}

        assert all(
            isinstance(bbox[key], int)
            for key in ("x", "y", "width", "height")
        )

        assert bbox["width"] > 0
        assert bbox["height"] > 0

        assert annotation.image is not None
        assert annotation.label is not None
        assert annotation.user is not None

    # Kontrola zapytania dla etykiety cat.
    cat_label = (
        session.query(Label)
        .filter(Label.name == "cat")
        .one()
    )

    expected_cat_image_ids = {
        annotation.image_id
        for annotation in session.query(Annotation)
        .filter(Annotation.label_id == cat_label.id)
        .all()
    }

    actual_cat_image_ids = {
        image.id for image in cat_images
    }

    assert actual_cat_image_ids == expected_cat_image_ids

    assert sum(count for _, count in label_statistics) == 500
    assert sum(count for _, count in user_statistics) == 500

    print("\n=== WALIDACJA ===")
    print(f"Images: {image_count}")
    print(f"Labels: {label_count}")
    print(f"Users: {user_count}")
    print(f"Annotations: {annotation_count}")
    print("Wszystkie pola bbox zawierają poprawny JSON.")
    print("Relacje Image, Label i User są poprawne.")
    print("Zapytanie dla etykiety cat zwraca poprawne obrazy.")
    print("\nZadanie 16 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
