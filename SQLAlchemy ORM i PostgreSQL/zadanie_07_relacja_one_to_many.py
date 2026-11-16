from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)

Base = declarative_base()


# Model Teacher - jeden nauczyciel
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    courses = relationship("Course", back_populates="teacher")


# Model Course - wiele kursów
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)

    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="courses")


# Tworzenie tabel
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Utworzenie nauczyciela i przypisanie kursów
    teacher = session.query(Teacher).filter_by(
        name="Adam Nowicki"
    ).first()

    if teacher is None:
        teacher = Teacher(name="Adam Nowicki")
        session.add(teacher)
        session.flush()

    # Dodanie trzech kursów, jeśli jeszcze nie istnieją
    course_titles = [
        "Python Programming",
        "Data Science",
        "Machine Learning"
    ]

    existing_titles = {course.title for course in teacher.courses}

    for title in course_titles:
        if title not in existing_titles:
            teacher.courses.append(Course(title=title))

    session.commit()

    # Weryfikacja relacji One-to-Many
    print(f"Nauczyciel: {teacher.name}")
    print(f"ID nauczyciela: {teacher.id}")
    print("\nKursy nauczyciela:")

    for course in teacher.courses:
        print(
            f"ID kursu: {course.id} | "
            f"Temat: {course.title} | "
            f"Teacher ID: {course.teacher_id}"
        )

    print(f"\nLiczba kursów: {len(teacher.courses)}")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
