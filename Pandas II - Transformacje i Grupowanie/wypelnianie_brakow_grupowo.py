import pandas as pd

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

titanic = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(titanic)}")

# ============================================================
# 2. STATYSTYKI PRZED UZUPEŁNIENIEM BRAKÓW
# ============================================================

missing_before = titanic["Age"].isna().sum()

print("\n=== BRAKUJĄCE WARTOŚCI AGE — PRZED ===")
print(f"Liczba braków: {missing_before}")

print("\n=== STATYSTYKI AGE — PRZED UZUPEŁNIENIEM ===")
print(titanic["Age"].describe().round(2).to_string())

# ============================================================
# 3. UZUPEŁNIENIE BRAKÓW MEDIANĄ GRUPOWĄ WEDŁUG PCLASS
# ============================================================

titanic["Age"] = (
    titanic
    .groupby("Pclass")["Age"]
    .transform(lambda x: x.fillna(x.median()))
)

# ============================================================
# 4. SPRAWDZENIE BRAKUJĄCYCH WARTOŚCI PO UZUPEŁNIENIU
# ============================================================

missing_after = titanic["Age"].isna().sum()

print("\n=== BRAKUJĄCE WARTOŚCI AGE — PO ===")
print(f"Liczba braków: {missing_after}")

# ============================================================
# 5. STATYSTYKI PO UZUPEŁNIENIU BRAKÓW
# ============================================================

print("\n=== STATYSTYKI AGE — PO UZUPEŁNIENIU ===")
print(titanic["Age"].describe().round(2).to_string())

# ============================================================
# 6. PODSUMOWANIE
# ============================================================

print("\n=== PODSUMOWANIE ===")

if missing_after == 0:
    print("Wszystkie braki w kolumnie Age zostały uzupełnione.")
else:
    print(f"Pozostała liczba braków: {missing_after}")

