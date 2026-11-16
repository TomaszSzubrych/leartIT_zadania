import sqlite3
import pandas as pd


# ============================================================
# 1. DANE — HIERARCHIA PRACOWNIKÓW
# ============================================================

employees = [
    (1, "Anna Kowalska", None),
    (2, "Piotr Nowak", 1),
    (3, "Marta Wisniewska", 1),
    (4, "Jan Zielinski", 2),
    (5, "Ewa Wojcik", 2),
    (6, "Tomasz Kaminski", 3),
    (7, "Alicja Lewandowska", 3),
    (8, "Pawel Dabrowski", 4),
    (9, "Katarzyna Kozlowska", 4),
    (10, "Michal Jankowski", 5),
    (11, "Natalia Mazur", 5),
    (12, "Robert Krawczyk", 6),
    (13, "Monika Piotrowska", 6),
    (14, "Krzysztof Grabowski", 7),
    (15, "Joanna Nowicka", 7),
]


# ============================================================
# 2. UTWORZENIE BAZY I TABELI
# ============================================================

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id)
        REFERENCES employees(employee_id)
)
""")

conn.executemany("""
INSERT INTO employees (
    employee_id,
    name,
    manager_id
)
VALUES (?, ?, ?)
""", employees)

conn.commit()


# ============================================================
# 3. SELF-JOIN — PRACOWNIK I MANAGER
# ============================================================

query_hierarchy = """
SELECT
    e1.name AS employee,
    e2.name AS manager

FROM employees e1

LEFT JOIN employees e2
    ON e1.manager_id = e2.employee_id

ORDER BY e1.employee_id
"""

df_hierarchy = pd.read_sql_query(
    query_hierarchy,
    conn
)

print("HIERARCHIA PRACOWNIKÓW:")
print(df_hierarchy.to_string(index=False))


# ============================================================
# 4. TOP MANAGEMENT — PRACOWNICY BEZ MANAGERA
# ============================================================

query_top_management = """
SELECT
    employee_id,
    name

FROM employees

WHERE manager_id IS NULL

ORDER BY employee_id
"""

df_top_management = pd.read_sql_query(
    query_top_management,
    conn
)

print("\nTOP MANAGEMENT — PRACOWNICY BEZ MANAGERA:")
print(df_top_management.to_string(index=False))


# ============================================================
# 5. LICZBA PODWŁADNYCH KAŻDEGO MANAGERA
# ============================================================

query_subordinates = """
SELECT
    manager.employee_id AS manager_id,
    manager.name AS manager,
    COUNT(employee.employee_id) AS subordinate_count

FROM employees manager

INNER JOIN employees employee
    ON employee.manager_id = manager.employee_id

GROUP BY
    manager.employee_id,
    manager.name

ORDER BY
    subordinate_count DESC,
    manager.name
"""

df_subordinates = pd.read_sql_query(
    query_subordinates,
    conn
)

print("\nLICZBA BEZPOŚREDNICH PODWŁADNYCH:")
print(df_subordinates.to_string(index=False))


# ============================================================
# 6. WALIDACJA
# ============================================================

total_employees = conn.execute(
    "SELECT COUNT(*) FROM employees"
).fetchone()[0]

top_management_count = len(df_top_management)

total_direct_subordinates = int(
    df_subordinates["subordinate_count"].sum()
)

if total_employees != len(employees):
    raise ValueError("Nieprawidłowa liczba pracowników.")

if len(df_hierarchy) != total_employees:
    raise ValueError("SELF-JOIN nie zwrócił wszystkich pracowników.")

if top_management_count != 1:
    raise ValueError("Oczekiwano jednego pracownika TOP management.")

if total_direct_subordinates != total_employees - top_management_count:
    raise ValueError("Nieprawidłowa liczba przypisanych podwładnych.")

if df_hierarchy["employee"].duplicated().any():
    raise ValueError("Wykryto powielonych pracowników w wyniku SELF-JOIN.")

print("\nWALIDACJA ZAKOŃCZONA POPRAWNIE.")
print(f"Liczba pracowników: {total_employees}")
print(f"Pracownicy bez managera: {top_management_count}")
print(f"Liczba managerów z podwładnymi: {len(df_subordinates)}")
print(f"Liczba relacji pracownik-manager: {total_direct_subordinates}")

conn.close()
