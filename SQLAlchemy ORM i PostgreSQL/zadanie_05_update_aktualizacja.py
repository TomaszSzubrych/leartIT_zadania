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
    # UPDATE 1 - zmiana wieku jednego studenta
    student = session.query(Student).filter(
        Student.name == "Anna Kowalska"
    ).first()

    if student is None:
        raise ValueError("Nie znaleziono Anny Kowalskiej.")

    student.age = 22

    session.commit()

    print(f"Zaktualizowano {student.name}: wiek = {student.age}")

    # UPDATE 2 - zwiększenie wieku wszystkich studentów o 1
    updated_count = session.query(Student).update(
        {Student.age: Student.age + 1},
        synchronize_session="fetch"
    )

    session.commit()

    print(f"\nZaktualizowano wiek {updated_count} studentow.")

    # Weryfikacja zmian
    print("\nSTUDENCI PO AKTUALIZACJI:")

    students = session.query(Student).order_by(Student.id).all()

    for student in students:
        print(f"{student.name} | Wiek: {student.age}")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
