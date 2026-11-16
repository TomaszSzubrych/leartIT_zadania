from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine,
    event,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    Query,
    Session as SQLAlchemySession,
    with_loader_criteria,
)


# ============================================================
# KONFIGURACJA
# ============================================================

DATABASE_URL = (
    "sqlite:///D:/learIT/SQLAlchemy ORM i PostgreSQL/multi_tenant.db"
)

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()


# ============================================================
# MODELE
# ============================================================

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)

    users = relationship(
        "User",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    projects = relationship(
        "Project",
        back_populates="organization",
        cascade="all, delete-orphan",
    )


class TenantMixin:
    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )


class User(Base, TenantMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)

    organization = relationship(
        "Organization",
        back_populates="users",
    )


class Project(Base, TenantMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    organization = relationship(
        "Organization",
        back_populates="projects",
    )


# ============================================================
# CUSTOM QUERY
# ============================================================

class TenantQuery(Query):

    def _add_tenant_filter(self):
        tenant_entities = []

        for description in self.column_descriptions:
            entity = description.get("entity")

            if (
                entity is not None
                and isinstance(entity, type)
                and issubclass(entity, TenantMixin)
            ):
                tenant_entities.append(entity)

        # Tabele nietenantowe, np. organizations,
        # nie wymagajÄ… aktywnego tenant scope.
        if not tenant_entities:
            return self

        organization_id = self.session.info.get("organization_id")

        if organization_id is None:
            raise RuntimeError(
                "Nie ustawiono organizacji. "
                "WywoĹ‚aj set_organization(id) przed zapytaniem."
            )

        query = self

        for entity in tenant_entities:
            query = query.filter(
                entity.organization_id == organization_id
            )

        return query

    def all(self):
        query = self._add_tenant_filter()
        return query.session.execute(
            query.statement
        ).scalars().all()

    def first(self):
        query = self._add_tenant_filter().limit(1)
        return query.session.execute(
            query.statement
        ).scalars().first()

    def count(self):
        from sqlalchemy import func, select

        query = self._add_tenant_filter()

        count_statement = select(
            func.count()
        ).select_from(
            query.statement.order_by(None).subquery()
        )

        return query.session.execute(
            count_statement
        ).scalar_one()


# ============================================================
# CUSTOM SESSION
# ============================================================

class TenantSession(SQLAlchemySession):

    def set_organization(self, organization_id):
        organization = self.get(Organization, organization_id)

        if organization is None:
            raise ValueError(
                f"Organizacja o ID {organization_id} nie istnieje."
            )

        self.info["organization_id"] = organization_id

    def add(self, instance, _warn=True):
        if isinstance(instance, TenantMixin):
            organization_id = self.info.get("organization_id")

            if organization_id is None:
                raise RuntimeError(
                    "Nie ustawiono organizacji przed dodaniem rekordu."
                )

            if (
                instance.organization_id is not None
                and instance.organization_id != organization_id
            ):
                raise ValueError(
                    "Nie moĹĽna dodaÄ‡ rekordu do innej organizacji."
                )

            instance.organization_id = organization_id

        super().add(instance, _warn=_warn)

    def add_all(self, instances):
        for instance in instances:
            self.add(instance)


SessionLocal = sessionmaker(
    bind=engine,
    class_=TenantSession,
    query_cls=TenantQuery,
)


# ============================================================
# AUTOMATYCZNY FILTR DLA SELECT I RELACJI ORM
# ============================================================

@event.listens_for(TenantSession, "do_orm_execute")
def apply_tenant_filter(execute_state):
    if not execute_state.is_select:
        return

    if execute_state.execution_options.get("skip_tenant_filter", False):
        return

    # Sprawdzamy, czy SELECT dotyczy modelu tenantowego.
    tenant_mappers = [
        mapper
        for mapper in execute_state.all_mappers
        if issubclass(mapper.class_, TenantMixin)
    ]

    # Odczyt Organization jest dozwolony bez aktywnej organizacji.
    if not tenant_mappers:
        return

    organization_id = execute_state.session.info.get(
        "organization_id"
    )

    if organization_id is None:
        raise RuntimeError(
            "Brak aktywnej organizacji â€” zapytanie zablokowane."
        )

    execute_state.statement = execute_state.statement.options(
        with_loader_criteria(
            TenantMixin,
            lambda cls: cls.organization_id == organization_id,
            include_aliases=True,
        )
    )


Base.metadata.create_all(engine)


# ============================================================
# FUNKCJA USTAWIANIA ORGANIZACJI
# ============================================================

def set_organization(session, organization_id):
    session.set_organization(organization_id)


# ============================================================
# DEMONSTRACJA
# ============================================================

session = SessionLocal()

try:
    # --------------------------------------------------------
    # CZYSZCZENIE DANYCH TESTOWYCH
    # --------------------------------------------------------

    # Usuwamy dane poprzedniego uruchomienia.
    # Operacja dotyczy wyĹ‚Ä…cznie osobnej bazy tego zadania.
    session.query(Project).delete()
    session.query(User).delete()
    session.query(Organization).delete()
    session.commit()

    # --------------------------------------------------------
    # UTWORZENIE 3 ORGANIZACJI
    # --------------------------------------------------------

    organizations = [
        Organization(name="PASKY-baits"),
        Organization(name="Fishing Team"),
        Organization(name="Data Solutions"),
    ]

    session.add_all(organizations)
    session.commit()

    organization_ids = {
        organization.name: organization.id
        for organization in organizations
    }

    print("=== ORGANIZACJE ===")

    for organization in organizations:
        print(
            f"{organization.id}: {organization.name}"
        )

    # --------------------------------------------------------
    # DODANIE DANYCH DO KAĹ»DEJ ORGANIZACJI
    # --------------------------------------------------------

    tenant_data = {
        "PASKY-baits": {
            "users": ["admin_pasky", "user_pasky"],
            "projects": ["Katalog przynÄ™t", "Sklep internetowy"],
        },
        "Fishing Team": {
            "users": ["admin_fishing", "user_fishing"],
            "projects": ["Zawody wÄ™dkarskie", "Relacje znad wody"],
        },
        "Data Solutions": {
            "users": ["admin_data", "user_data"],
            "projects": ["Analiza danych", "Model ML"],
        },
    }

    for organization_name, data in tenant_data.items():
        organization_id = organization_ids[organization_name]

        set_organization(session, organization_id)

        for username in data["users"]:
            session.add(User(username=username))

        for project_name in data["projects"]:
            session.add(Project(name=project_name))

        session.commit()

    # ========================================================
    # TEST SEPARACJI DANYCH
    # ========================================================

    print("\n=== SEPARACJA DANYCH ===")

    for organization_name, organization_id in organization_ids.items():
        set_organization(session, organization_id)

        users = session.query(User).order_by(User.id).all()
        projects = session.query(Project).order_by(Project.id).all()

        print(f"\nOrganizacja: {organization_name}")
        print(f"UĹĽytkownicy: {[user.username for user in users]}")
        print(f"Projekty: {[project.name for project in projects]}")

        assert len(users) == 2
        assert len(projects) == 2

        assert all(
            user.organization_id == organization_id
            for user in users
        )

        assert all(
            project.organization_id == organization_id
            for project in projects
        )

    # ========================================================
    # TEST BLOKADY ZAPYTANIA BEZ ORGANIZACJI
    # ========================================================

    print("\n=== TEST BLOKADY BRAKU ORGANIZACJI ===")

    session.info.pop("organization_id", None)

    blocked = False

    try:
        session.query(User).all()
    except RuntimeError:
        blocked = True
        session.rollback()

    assert blocked

    # ========================================================
    # TEST BLOKADY PRZYPISANIA DO INNEJ ORGANIZACJI
    # ========================================================

    print("\n=== TEST BLOKADY OBCYCH DANYCH ===")

    pasky_id = organization_ids["PASKY-baits"]
    fishing_id = organization_ids["Fishing Team"]

    set_organization(session, pasky_id)

    foreign_user = User(
        username="foreign_user",
        organization_id=fishing_id,
    )

    blocked_foreign = False

    try:
        session.add(foreign_user)
    except ValueError:
        blocked_foreign = True
        session.rollback()

    assert blocked_foreign

    # ========================================================
    # KOĹCOWA WALIDACJA
    # ========================================================

    total_users = 0
    total_projects = 0

    for organization_id in organization_ids.values():
        set_organization(session, organization_id)

        total_users += session.query(User).count()
        total_projects += session.query(Project).count()

    assert total_users == 6
    assert total_projects == 6

    print("\n=== WALIDACJA ===")
    print(f"Liczba organizacji: {len(organizations)}")
    print(f"Liczba uĹĽytkownikĂłw: {total_users}")
    print(f"Liczba projektĂłw: {total_projects}")
    print("Zapytania bez ustawionej organizacji sÄ… blokowane.")
    print("Dodawanie rekordĂłw do obcej organizacji jest blokowane.")
    print("Dane organizacji sÄ… odseparowane.")
    print("\nZadanie 20 wykonane poprawnie.")

except Exception:
    session.rollback()
    raise

finally:
    session.close()
    engine.dispose()
