from pathlib import Path
import time

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    event
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    joinedload
)


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=True
)

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)

    author_id = Column(
        Integer,
        ForeignKey("authors.id"),
        nullable=False
    )

    author = relationship("Author", back_populates="books")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# Licznik zapytań SELECT
query_counter = {"select": 0}


@event.listens_for(engine, "before_cursor_execute")
def count_select_queries(
    connection,
    cursor,
    statement,
    parameters,
    context,
    executemany
):
    if statement.lstrip().upper().startswith("SELECT"):
        query_counter["select"] += 1


def create_test_data():
    session = Session()

    try:
        for author_number in range(1, 11):
            author_name = f"Author {author_number:02d}"

            author = session.query(Author).filter_by(
                name=author_name
            ).first()

            if author is None:
                author = Author(name=author_name)
                session.add(author)
                session.flush()

            for book_number in range(1, 6):
                book_title = (
                    f"Book {author_number:02d}-{book_number:02d}"
                )

                existing_book = session.query(Book).filter_by(
                    title=book_title,
                    author_id=author.id
                ).first()

                if existing_book is None:
                    author.books.append(
                        Book(title=book_title)
                    )

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def benchmark_lazy_loading():
    session = Session()
    query_counter["select"] = 0

    try:
        start_time = time.perf_counter()

        authors = session.query(Author).order_by(
            Author.id
        ).all()

        total_books = 0

        for author in authors:
            total_books += len(author.books)

        elapsed_time = time.perf_counter() - start_time
        queries = query_counter["select"]

        return elapsed_time, queries, len(authors), total_books

    finally:
        session.close()


def benchmark_eager_loading():
    session = Session()
    query_counter["select"] = 0

    try:
        start_time = time.perf_counter()

        authors = session.query(Author).options(
            joinedload(Author.books)
        ).order_by(Author.id).all()

        total_books = 0

        for author in authors:
            total_books += len(author.books)

        elapsed_time = time.perf_counter() - start_time
        queries = query_counter["select"]

        return elapsed_time, queries, len(authors), total_books

    finally:
        session.close()


try:
    # 1. Przygotowanie danych
    print("\n=== PRZYGOTOWANIE DANYCH ===")

    create_test_data()

    verification_session = Session()

    try:
        authors_count = verification_session.query(Author).count()
        books_count = verification_session.query(Book).count()

    finally:
        verification_session.close()

    print(f"Liczba autorów: {authors_count}")
    print(f"Liczba książek: {books_count}")

    if authors_count != 10 or books_count != 50:
        raise ValueError(
            "Nieprawidłowa liczba autorów lub książek."
        )

    # 2. Lazy Loading - 3 powtórzenia
    print("\n=== LAZY LOADING ===")

    lazy_times = []
    lazy_queries = []

    for repetition in range(1, 4):
        elapsed, queries, authors, books = benchmark_lazy_loading()

        lazy_times.append(elapsed)
        lazy_queries.append(queries)

        print(
            f"Powtórzenie {repetition}: "
            f"{elapsed:.6f} s | "
            f"Zapytania SELECT: {queries} | "
            f"Autorzy: {authors} | "
            f"Książki: {books}"
        )

    # 3. Eager Loading - 3 powtórzenia
    print("\n=== EAGER LOADING (joinedload) ===")

    eager_times = []
    eager_queries = []

    for repetition in range(1, 4):
        elapsed, queries, authors, books = benchmark_eager_loading()

        eager_times.append(elapsed)
        eager_queries.append(queries)

        print(
            f"Powtórzenie {repetition}: "
            f"{elapsed:.6f} s | "
            f"Zapytania SELECT: {queries} | "
            f"Autorzy: {authors} | "
            f"Książki: {books}"
        )

    # 4. Obliczenie średnich
    average_lazy_time = sum(lazy_times) / len(lazy_times)
    average_eager_time = sum(eager_times) / len(eager_times)

    average_lazy_queries = sum(lazy_queries) / len(lazy_queries)
    average_eager_queries = sum(eager_queries) / len(eager_queries)

    print("\n=== PODSUMOWANIE BENCHMARKU ===")

    print(
        f"Lazy Loading - średni czas: "
        f"{average_lazy_time:.6f} s"
    )
    print(
        f"Lazy Loading - średnia liczba SELECT: "
        f"{average_lazy_queries:.1f}"
    )

    print(
        f"Eager Loading - średni czas: "
        f"{average_eager_time:.6f} s"
    )
    print(
        f"Eager Loading - średnia liczba SELECT: "
        f"{average_eager_queries:.1f}"
    )

    print("\n=== PORÓWNANIE ===")

    if average_eager_time < average_lazy_time:
        print("Eager Loading był szybszy w tym pomiarze.")
    elif average_lazy_time < average_eager_time:
        print("Lazy Loading był szybszy w tym pomiarze.")
    else:
        print("Obie metody uzyskały taki sam średni czas.")

    if average_lazy_queries > average_eager_queries:
        print(
            "Eager Loading wykonał mniej zapytań SQL."
        )

    print("\nBenchmark zakończony poprawnie.")

finally:
    engine.dispose()
