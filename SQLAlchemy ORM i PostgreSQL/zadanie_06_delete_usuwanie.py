from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    email = Column(String(150), unique=True)


Session = sessionmaker(bind=engine)
session = Session()

try:
    # DELETE 1 - usunięcie najmłodszego studenta
    youngest = session.query(Student).order_by(
        Student.age.asc()
    ).first()

    if youngest is None:
        raise ValueError("Brak studentów w bazie.")

    print(
        f"Najmlodszy student: {youngest.name}, "
        f"wiek: {youngest.age}"
    )

    session.delete(youngest)
    session.commit()

    print(f"Usunieto studenta: {youngest.name}")

    # DELETE 2 - usunięcie wszystkich studentów starszych niż 24 lata
    deleted_count = session.query(Student).filter(
        Student.age > 24
    ).delete(synchronize_session="fetch")

    session.commit()

    print(
        f"\nUsunieto {deleted_count} studentow "
        "starszych niz 24 lata."
    )

    # Weryfikacja
    remaining_students = session.query(Student).order_by(
        Student.id
    ).all()

    print("\nPOZOSTALI STUDENCI:")

    for student in remaining_students:
        print(f"{student.name} | Wiek: {student.age}")

    print(
        f"\nLiczba pozostalych studentow: "
        f"{session.query(Student).count()}"
    )

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
