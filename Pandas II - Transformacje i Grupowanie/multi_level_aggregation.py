import pandas as pd

# ============================================================
# 1. WCZYTANIE DATASETU TITANIC
# ============================================================

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

titanic = pd.read_csv(url)

print("=== DATASET TITANIC ===")
print(f"Liczba rekordów: {len(titanic)}")

# ============================================================
# 2. UTWORZENIE KOLUMNY IS_ALONE
# ============================================================

titanic["Is_Alone"] = (
    titanic["SibSp"] + titanic["Parch"] == 0
)

# ============================================================
# 3. GRUPOWANIE I AGREGACJA
# ============================================================

result = (
    titanic
    .groupby(["Pclass", "Sex", "Is_Alone"])
    .agg(
        Avg_Age=("Age", "mean"),
        Survival_Rate=("Survived", "mean")
    )
    .reset_index()
)

# ============================================================
# 4. PREZENTACJA WYNIKÓW
# ============================================================

result["Avg_Age"] = result["Avg_Age"].round(2)
result["Survival_Rate"] = (result["Survival_Rate"] * 100).round(2)

print("\n=== WYNIKI MULTI-LEVEL AGGREGATION ===")
print(result.to_string(index=False))

print("\n=== LICZBA WSZYSTKICH KOMBINACJI ===")
print(len(result))

