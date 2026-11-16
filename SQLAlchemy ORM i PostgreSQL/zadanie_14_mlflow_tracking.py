import random
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    create_engine,
    func,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# ============================================================
# KONFIGURACJA
# ============================================================

random.seed(42)

DATABASE_URL = (
    "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/mlflow_tracking.db"
)

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ============================================================
# MODELE
# ============================================================

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String(500))

    runs = relationship(
        "Run",
        back_populates="experiment",
        cascade="all, delete-orphan",
    )


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    experiment_id = Column(
        Integer,
        ForeignKey("experiments.id"),
        nullable=False,
    )

    experiment = relationship("Experiment", back_populates="runs")

    metrics = relationship(
        "Metric",
        back_populates="run",
        cascade="all, delete-orphan",
    )

    params = relationship(
        "Param",
        back_populates="run",
        cascade="all, delete-orphan",
    )


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)

    run = relationship("Run", back_populates="metrics")


class Param(Base):
    __tablename__ = "params"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)

    run = relationship("Run", back_populates="params")


Base.metadata.create_all(engine)


# ============================================================
# API TRACKINGU
# ============================================================

def log_param(session, run, name, value):
    """Zapisuje parametr eksperymentu."""
    param = Param(
        run=run,
        name=name,
        value=str(value),
    )
    session.add(param)


def log_metric(session, run, name, value):
    """Zapisuje metrykę eksperymentu."""
    metric = Metric(
        run=run,
        name=name,
        value=float(value),
    )
    session.add(metric)


def get_best_run(session, experiment, metric):
    """
    Zwraca run z najniższą wartością wskazanej metryki
    w obrębie wybranego eksperymentu.
    """
    return (
        session.query(Run, Metric.value)
        .join(Metric, Metric.run_id == Run.id)
        .filter(
            Run.experiment_id == experiment.id,
            Metric.name == metric,
        )
        .order_by(Metric.value.asc(), Run.id.asc())
        .first()
    )


# ============================================================
# DANE TESTOWE
# ============================================================

session = Session()

try:
    # Czyścimy wyłącznie dane tego zadania.
    session.query(Metric).delete()
    session.query(Param).delete()
    session.query(Run).delete()
    session.query(Experiment).delete()
    session.commit()

    experiment_definitions = [
        ("Image Classification", "Klasyfikacja obrazów"),
        ("Customer Churn Prediction", "Predykcja odejścia klientów"),
        ("House Price Prediction", "Predykcja cen nieruchomości"),
    ]

    experiments = []

    for name, description in experiment_definitions:
        experiment = Experiment(
            name=name,
            description=description,
        )
        experiments.append(experiment)

    session.add_all(experiments)
    session.flush()

    # Każdy eksperyment otrzymuje 5 runs.
    for experiment_index, experiment in enumerate(experiments):
        for run_index in range(1, 6):
            run = Run(
                name=f"run_{run_index:02d}",
                experiment=experiment,
            )

            learning_rate = random.choice([0.001, 0.01, 0.05])
            epochs = random.choice([10, 20, 30])

            log_param(session, run, "learning_rate", learning_rate)
            log_param(session, run, "epochs", epochs)
            log_param(session, run, "optimizer", "Adam")

            # Deterministyczne dane MSE dla demonstracji rankingu.
            mse = round(
                0.50
                - experiment_index * 0.08
                - run_index * 0.025
                + random.uniform(-0.01, 0.01),
                4,
            )

            accuracy = round(
                0.70
                + experiment_index * 0.05
                + run_index * 0.02
                + random.uniform(-0.01, 0.01),
                4,
            )

            log_metric(session, run, "MSE", mse)
            log_metric(session, run, "accuracy", accuracy)

            session.add(run)

    session.commit()

    # ========================================================
    # RAPORT EKSPERYMENTÓW
    # ========================================================

    print("=== EKSPERYMENTY I RUNS ===")

    for experiment in session.query(Experiment).order_by(Experiment.id):
        run_count = (
            session.query(Run)
            .filter(Run.experiment_id == experiment.id)
            .count()
        )

        print(
            f"{experiment.name}: "
            f"{run_count} runs"
        )

    # ========================================================
    # NAJLEPSZY RUN WEDŁUG MSE
    # ========================================================

    target_experiment = experiments[0]

    print("\n=== RANKING RUNS: MSE ===")

    ranking = (
        session.query(Run.name, Metric.value)
        .join(Metric, Metric.run_id == Run.id)
        .filter(
            Run.experiment_id == target_experiment.id,
            Metric.name == "MSE",
        )
        .order_by(Metric.value.asc())
        .all()
    )

    for position, (run_name, mse) in enumerate(ranking, start=1):
        print(f"{position}. {run_name}: MSE = {mse:.4f}")

    best = get_best_run(
        session,
        target_experiment,
        "MSE",
    )

    assert best is not None

    best_run, best_mse = best

    print("\n=== NAJLEPSZY RUN ===")
    print(f"Eksperyment: {target_experiment.name}")
    print(f"Run: {best_run.name}")
    print(f"Najniższe MSE: {best_mse:.4f}")

    # ========================================================
    # WALIDACJA
    # ========================================================

    experiment_count = session.query(Experiment).count()
    run_count = session.query(Run).count()
    metric_count = session.query(Metric).count()
    param_count = session.query(Param).count()

    assert experiment_count >= 3
    assert run_count >= 15
    assert metric_count >= 30
    assert param_count >= 45

    for experiment in experiments:
        count = (
            session.query(Run)
            .filter(Run.experiment_id == experiment.id)
            .count()
        )
        assert count >= 5

    assert best_mse == min(value for _, value in ranking)

    print("\n=== WALIDACJA ===")
    print(f"Experiments: {experiment_count}")
    print(f"Runs: {run_count}")
    print(f"Metrics: {metric_count}")
    print(f"Params: {param_count}")
    print("Każdy eksperyment ma minimum 5 runs.")
    print("Najlepszy run ma najniższą wartość MSE.")
    print("\nZadanie 14 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
