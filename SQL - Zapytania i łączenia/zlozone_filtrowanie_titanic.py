import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# 1. WCZYTANIE DANYCH TITANIC
# ============================================================

script_dir = Path(__file__).resolve().parent
csv_path = script_dir / "titanic.csv"

if not csv_path.exists():
    raise FileNotFoundError(
        f"Nie znaleziono pliku danych: {csv_path}"
    )

df_titanic = pd.read_csv(csv_path)

print("LICZBA REKORDÓW W ZBIORZE:")
print(len(df_titanic))

df_titanic = df_titanic[
    ["Survived", "Pclass", "Sex", "Age", "Fare"]
].copy()


# ============================================================
# 2. UTWORZENIE BAZY SQLITE
# ============================================================

conn = sqlite3.connect(":memory:")

df_titanic.to_sql(
    "titanic",
    conn,
    if_exists="replace",
    index=False
)


# ============================================================
# 3. ZŁOŻONE FILTROWANIE I PORÓWNANIE GRUP
# ============================================================

query = """
SELECT
    CASE
        WHEN Pclass = 1
             AND Sex = 'female'
             AND Survived = 1
        THEN 'Kobiety 1 klasa — przeżyły'

        WHEN Pclass = 3
             AND Sex = 'male'
             AND Survived = 0
        THEN 'Mężczyźni 3 klasa — nie przeżyli'
    END AS grupa,

    COUNT(*) AS liczba,
    AVG(Age) AS avg_age,
    AVG(Fare) AS avg_fare

FROM titanic

WHERE
    (Pclass = 1 AND Sex = 'female' AND Survived = 1)
    OR
    (Pclass = 3 AND Sex = 'male' AND Survived = 0)

GROUP BY grupa
ORDER BY grupa
"""

df_comparison = pd.read_sql_query(query, conn)

print("\nPORÓWNANIE DWÓCH GRUP PASAŻERÓW:")
print(df_comparison.to_string(index=False))


# ============================================================
# 4. TEKSTOWE SŁUPKI ŚREDNIEJ CENY BILETU
# ============================================================

print("\nTEKSTOWE SŁUPKI ŚREDNIEJ CENY BILETU:")
print("Skala: 1 znak = 5 jednostek Fare")

for _, row in df_comparison.iterrows():

    bar_length = int(row["avg_fare"] / 5)
    bar = "█" * bar_length

    print(
        f"{row['grupa']}: "
        f"{row['avg_fare']:.2f} | {bar}"
    )


# ============================================================
# 5. WALIDACJA
# ============================================================

if len(df_comparison) != 2:
    raise ValueError(
        "Oczekiwano dokładnie dwóch grup pasażerów."
    )

if (df_comparison["liczba"] <= 0).any():
    raise ValueError(
        "Jedna z grup nie zawiera pasażerów."
    )

print("\nWALIDACJA: znaleziono obie wymagane grupy.")

conn.close()
