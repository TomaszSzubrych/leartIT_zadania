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
    # 1. READ - wszyscy studenci
    print("1. WSZYSCY STUDENCI")

    all_students = session.query(Student).all()

    for student in all_students:
        print(f"{student.id} | {student.name} | {student.age}")

    # 2. READ - student o konkretnym imieniu
    print("\n2. STUDENT: Anna Kowalska")

    student = session.query(Student).filter(
        Student.name == "Anna Kowalska"
    ).first()

    if student:
        print(f"Znaleziono: {student.name}, wiek: {student.age}")
    else:
        print("Nie znaleziono studenta.")

    # 3. READ - studenci starsi niż 20 lat
    print("\n3. STUDENCI STARSZI NIZ 20 LAT")

    older_students = session.query(Student).filter(
        Student.age > 20
    ).all()

    for student in older_students:
        print(f"{student.name} | Wiek: {student.age}")

    # 4. READ - liczba wszystkich studentów
    print("\n4. LICZBA STUDENTOW")

    students_count = session.query(Student).count()

    print(f"Liczba studentow: {students_count}")

finally:
    session.close()
    engine.dispose()
