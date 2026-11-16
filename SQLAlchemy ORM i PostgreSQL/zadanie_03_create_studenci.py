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


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    # CREATE - pięciu studentów
    students = [
        Student(name="Anna Kowalska", age=21, email="anna@example.com"),
        Student(name="Jan Nowak", age=23, email="jan@example.com"),
        Student(name="Maria Wisniewska", age=19, email="maria@example.com"),
        Student(name="Piotr Zielinski", age=25, email="piotr@example.com"),
        Student(name="Katarzyna Wozniak", age=20, email="katarzyna@example.com"),
    ]

    # Dodanie wielu rekordów
    session.add_all(students)

    # Zapis do bazy
    session.commit()

    print(f"Dodano {len(students)} studentow.")

    # READ - weryfikacja zapisanych rekordow
    all_students = session.query(Student).order_by(Student.id).all()

    print(f"\nLiczba studentow w bazie: {len(all_students)}")
    print("\nLista studentow:")

    for student in all_students:
        print(
            f"ID: {student.id} | "
            f"Imie: {student.name} | "
            f"Wiek: {student.age} | "
            f"Email: {student.email}"
        )

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
