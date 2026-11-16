from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Table,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "test.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)

Base = declarative_base()


# Tabela asocjacyjna Many-to-Many
movie_actor = Table(
    "movie_actor",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True)
)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False, unique=True)

    actors = relationship(
        "Actor",
        secondary=movie_actor,
        back_populates="movies"
    )


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    movies = relationship(
        "Movie",
        secondary=movie_actor,
        back_populates="actors"
    )


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    # 1. Dane: 5 filmów i 7 aktorów
    movie_data = {
        "Inception": [
            "Leonardo DiCaprio",
            "Joseph Gordon-Levitt",
            "Elliot Page"
        ],
        "Titanic": [
            "Leonardo DiCaprio",
            "Kate Winslet"
        ],
        "The Revenant": [
            "Leonardo DiCaprio",
            "Tom Hardy"
        ],
        "The Dark Knight": [
            "Joseph Gordon-Levitt",
            "Tom Hardy",
            "Christian Bale"
        ],
        "Interstellar": [
            "Matthew McConaughey",
            "Christian Bale",
            "Elliot Page"
        ]
    }

    # 2. Utworzenie lub pobranie aktorów
    actor_names = sorted({
        actor_name
        for names in movie_data.values()
        for actor_name in names
    })

    actors = {}

    for actor_name in actor_names:
        actor = session.query(Actor).filter_by(
            name=actor_name
        ).first()

        if actor is None:
            actor = Actor(name=actor_name)
            session.add(actor)

        actors[actor_name] = actor

    # 3. Utworzenie lub pobranie filmów i przypisanie aktorów
    for movie_title, actor_list in movie_data.items():
        movie = session.query(Movie).filter_by(
            title=movie_title
        ).first()

        if movie is None:
            movie = Movie(title=movie_title)
            session.add(movie)

        for actor_name in actor_list:
            actor = actors[actor_name]

            if actor not in movie.actors:
                movie.actors.append(actor)

    session.commit()

    # 4. Weryfikacja liczby danych
    movies = session.query(Movie).order_by(Movie.title).all()
    actors_from_db = session.query(Actor).order_by(Actor.name).all()

    print(f"Liczba filmów: {len(movies)}")
    print(f"Liczba aktorów: {len(actors_from_db)}")

    # 5. Zapytanie: Jakie filmy ma aktor X?
    actor_name = "Leonardo DiCaprio"

    actor = session.query(Actor).filter_by(
        name=actor_name
    ).first()

    print(f"\nFILMY AKTORA: {actor_name}")

    if actor:
        for movie in sorted(actor.movies, key=lambda item: item.title):
            print(f"- {movie.title}")

    # 6. Zapytanie: Jacy aktorzy grają w filmie Y?
    movie_title = "Inception"

    movie = session.query(Movie).filter_by(
        title=movie_title
    ).first()

    print(f"\nAKTORZY W FILMIE: {movie_title}")

    if movie:
        for actor in sorted(movie.actors, key=lambda item: item.name):
            print(f"- {actor.name}")

    # 7. Prezentacja wszystkich relacji
    print("\nWSZYSTKIE FILMY I AKTORZY:")

    for movie in movies:
        actor_list = ", ".join(
            actor.name
            for actor in sorted(movie.actors, key=lambda item: item.name)
        )
        print(f"{movie.title}: {actor_list}")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
